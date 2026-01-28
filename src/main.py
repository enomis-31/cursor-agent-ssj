import argparse
import sys
import os

# Add project root to sys.path to support 'src.' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import logger, get_env_var
from src.orchestrator import assemble_feature_prompt, assemble_polish_prompt, monitor_agent
from src.cursor_api import launch_agent, add_followup
from src.verifier import run_verification
from src.state_manager import load_state, save_state

def run_agent_workflow(name, prompt, repo_url, state, verifier_context=None, no_verify=False, model=None, existing_agent_id=None):
    """Common workflow for launching an agent and optionally verifying its output."""
    
    if existing_agent_id:
        logger.info(f"Resuming polling for existing agent '{name}' (ID: {existing_agent_id})...")
        agent_id = existing_agent_id
    else:
        source_ref = state.get("last_successful_branch", "main")
        logger.info(f"Launching agent '{name}' from base: {source_ref}...")
        
        result = launch_agent(name, prompt, repo_url, source_ref=source_ref, model=model)
        agent_id = result.get("id")
        logger.info(f"Agent launched successfully! ID: {agent_id}")
    
    # Monitor
    status_data = monitor_agent(agent_id)
    output_summary = status_data.get("summary", "Agent finished execution.")
    
    # Verification
    if no_verify:
        logger.info("Verification skipped (--no-verify or SKIP_VERIFICATION=true).")
        v_status, v_feedback = "pass", "Verification skipped."
    else:
        logger.info("Starting verification via GPT-mini...")
        # verifier_context should be the spec content for features or polish goal for polish
        v_status, v_feedback = run_verification(name, verifier_context or "General verification", output_summary)
    
    if v_status == "pass":
        logger.info(f"Workflow '{name}' PASSED.")
        new_branch = status_data.get("target", {}).get("branchName")
        if new_branch:
            state["last_successful_branch"] = new_branch
            logger.info(f"Updated last successful branch to: {new_branch}")
        return True, v_feedback, agent_id
    else:
        logger.error(f"Workflow '{name}' FAILED: {v_feedback}")
        return False, v_feedback, agent_id

def process_feature(feature_name, feature_dir, repo_url, state, no_verify=False, model=None):
    """Handle the implementation of a single feature."""
    feature_state = state["features"].get(feature_name, {})
    
    if feature_state.get("status") == "completed":
        logger.info(f"Feature {feature_name} already completed.")
        return True

    # Resume logic: if agent_id exists but not completed, try to resume polling
    existing_id = feature_state.get("agent_id")
    
    prompt = assemble_feature_prompt(feature_dir)
    with open(os.path.join(feature_dir, "spec.md"), 'r') as f: spec_content = f.read()

    success, feedback, agent_id = run_agent_workflow(
        f"Feature: {feature_name}", 
        prompt, 
        repo_url, 
        state, 
        verifier_context=spec_content, 
        no_verify=no_verify,
        model=model,
        existing_agent_id=existing_id
    )
    
    state["features"][feature_name] = {
        "status": "completed" if success else "failed",
        "agent_id": agent_id,
        "last_feedback": feedback
    }
    save_state(state)
    return success

def process_polish(phase_name, repo_url, state, no_verify=False, model=None):
    """Handle a single polish phase."""
    polish_state = state["polish"].get(phase_name, {})
    
    if polish_state.get("status") == "completed":
        logger.info(f"Polish phase {phase_name} already completed.")
        return True

    # Resume logic
    existing_id = polish_state.get("agent_id")

    prompt = assemble_polish_prompt(phase_name)
    success, feedback, agent_id = run_agent_workflow(
        f"Polish: {phase_name}", 
        prompt, 
        repo_url, 
        state, 
        verifier_context=f"Polish goal: {phase_name}", 
        no_verify=no_verify,
        model=model,
        existing_agent_id=existing_id
    )
    
    state["polish"][phase_name] = {
        "status": "completed" if success else "failed",
        "agent_id": agent_id,
        "last_feedback": feedback
    }
    save_state(state)
    return success

def main():
    parser = argparse.ArgumentParser(description="Cursor Cloud Agent Orchestrator")
    parser.add_argument("--feature", help="Feature directory name inside specs/ to implement (skips full loop)")
    parser.add_argument("--agent-id", help="Manually provide a Cursor Agent ID to resume polling/verification")
    parser.add_argument("--no-verify", action="store_true", help="Disable GPT-mini verification")
    parser.add_argument("--dry-run", action="store_true", help="Prepare prompt without launching agent")
    args = parser.parse_args()

    REPO_URL = get_env_var("GITHUB_REPO_URL")
    SKIP_VERIFICATION = args.no_verify or os.getenv("SKIP_VERIFICATION") == "true"
    AGENT_MODEL = os.getenv("CURSOR_AGENT_MODEL") # Optional

    try:
        state = load_state()
        specs_root = "specs"

        # If agent-id is provided manually via CLI, inject it into the state for the target feature
        if args.agent_id:
            if not args.feature:
                # Try to detect which feature to attach the ID to if not provided
                features = sorted([d for d in os.listdir(specs_root) if os.path.isdir(os.path.join(specs_root, d))])
                # Filter out completed ones if possible, or just pick the first one
                target_feature = None
                for f in features:
                    if state["features"].get(f, {}).get("status") != "completed":
                        target_feature = f
                        break
                
                if not target_feature:
                    logger.error("No active feature found to attach agent-id. Please use --feature <name> --agent-id <id>")
                    sys.exit(1)
                
                logger.info(f"Attaching manual agent-id {args.agent_id} to feature: {target_feature}")
                if target_feature not in state["features"]: state["features"][target_feature] = {}
                state["features"][target_feature]["agent_id"] = args.agent_id
            else:
                logger.info(f"Attaching manual agent-id {args.agent_id} to feature: {args.feature}")
                if args.feature not in state["features"]: state["features"][args.feature] = {}
                state["features"][args.feature]["agent_id"] = args.agent_id
            
            save_state(state)

        # Phase 1: Features
        if state["current_phase"] == "features":
            logger.info("--- PHASE 1: FEATURES ---")
            features = sorted([d for d in os.listdir(specs_root) if os.path.isdir(os.path.join(specs_root, d))])
            
            for feature in features:
                if args.feature and feature != args.feature:
                    continue
                    
                feature_dir = os.path.join(specs_root, feature)
                if args.dry_run:
                    print(f"\n--- DRY RUN: FEATURE {feature} ---")
                    print(assemble_feature_prompt(feature_dir))
                    continue

                if not process_feature(feature, feature_dir, REPO_URL, state, no_verify=SKIP_VERIFICATION, model=AGENT_MODEL):
                    logger.error(f"Feature {feature} implementation failed. Stopping.")
                    sys.exit(1)
            
            if not args.feature and not args.dry_run:
                state["current_phase"] = "polish"
                save_state(state)
                logger.info("All features completed. Moving to Phase 2: Polish.")

        # Phase 2: Polish
        if state["current_phase"] == "polish" and not args.feature:
            logger.info("--- PHASE 2: POLISH ---")
            polish_phases = ["logs", "errors", "hinting", "tests"]
            
            for phase in polish_phases:
                if args.dry_run:
                    print(f"\n--- DRY RUN: POLISH {phase} ---")
                    print(assemble_polish_prompt(phase))
                    continue

                if not process_polish(phase, REPO_URL, state, no_verify=SKIP_VERIFICATION, model=AGENT_MODEL):
                    logger.error(f"Polish phase {phase} failed. Stopping.")
                    sys.exit(1)
            
            if not args.dry_run:
                logger.info("All polish phases completed successfully!")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
