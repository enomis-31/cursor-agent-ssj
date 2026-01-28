import argparse
import sys
import os

# Add project root to sys.path to support 'src.' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import logger, get_env_var
from src.orchestrator import assemble_prompt, monitor_agent
from src.cursor_api import launch_agent, add_followup
from src.verifier import run_verification
from src.state_manager import load_state, save_state, sync_task_to_md, get_pending_tasks

def get_feature_dir(feature_arg=None):
    """Determine the feature directory to use."""
    specs_root = "specs"
    if not os.path.exists(specs_root):
        raise FileNotFoundError("The 'specs' directory does not exist.")

    # 1. Use explicit argument
    if feature_arg:
        path = os.path.join(specs_root, feature_arg)
        if os.path.exists(path):
            return path
        raise FileNotFoundError(f"Feature directory not found: {path}")

    # 2. Try to auto-detect if there's only one feature
    features = [d for d in os.listdir(specs_root) if os.path.isdir(os.path.join(specs_root, d))]
    if len(features) == 1:
        logger.info(f"Auto-detected single feature: {features[0]}")
        return os.path.join(specs_root, features[0])

    # 3. Fail if ambiguous
    if len(features) > 1:
        logger.error("Multiple features found in 'specs/'. Please specify one using --feature <name>.")
        logger.error(f"Available features: {', '.join(features)}")
        sys.exit(1)
    
    raise FileNotFoundError("No feature directories found in 'specs/'.")

def process_task(task_id, feature_dir, repo_url, state):
    """Full workflow for processing a single task with retries."""
    spec_path = os.path.join(feature_dir, "spec.md")
    plan_path = os.path.join(feature_dir, "plan.md")
    tasks_md_path = os.path.join(feature_dir, "tasks.md")

    if "tasks" not in state: state["tasks"] = {}
    if task_id not in state["tasks"]:
        state["tasks"][task_id] = {"status": "pending", "retries": 0}

    task_meta = state["tasks"][task_id]
    if task_meta.get("status") == "completed":
        logger.info(f"Task {task_id} is already completed. Skipping.")
        return

    MAX_RETRIES = 2
    while task_meta.get("retries", 0) <= MAX_RETRIES:
        try:
            current_retry = task_meta.get("retries", 0)
            if current_retry == 0:
                prompt = assemble_prompt(task_id, spec_path, plan_path, tasks_md_path)
                source_ref = state.get("last_successful_branch", "main")
                logger.info(f"Launching initial agent for {task_id} from base: {source_ref}...")
                result = launch_agent(f"Task {task_id}", prompt, repo_url, source_ref=source_ref)
                agent_id = result.get("id")
            else:
                logger.info(f"Retry {current_retry}/{MAX_RETRIES} for {task_id}...")
                feedback = task_meta.get("last_delta_summary", "Requirements not fully met.")
                followup_prompt = f"VERIFICATION FAILED:\n{feedback}\n\nPlease fix the issues and build upon the previous work."
                agent_id = task_meta.get("agent_id")
                add_followup(agent_id, followup_prompt)
            
            task_meta["agent_id"] = agent_id
            task_meta["status"] = "running"
            save_state(state)
            
            logger.info(f"Monitoring agent {agent_id} for task {task_id}...")
            status_data = monitor_agent(agent_id)
            output_summary = status_data.get("summary", "Task execution finished.")
            
            logger.info(f"Verifying {task_id} (Attempt {current_retry+1})...")
            with open(spec_path, 'r') as f: spec_content = f.read()
            v_status, v_feedback = run_verification(task_id, spec_content, output_summary)
            
            if v_status == "pass":
                logger.info(f"Task {task_id} PASSED verification.")
                task_meta["status"] = "completed"
                task_meta["last_verification_result"] = "pass"
                new_branch = status_data.get("target", {}).get("branchName")
                if new_branch:
                    state["last_successful_branch"] = new_branch
                    logger.info(f"Updated last successful branch to: {new_branch}")
                
                save_state(state)
                sync_task_to_md(task_id, tasks_md_path, completed=True)
                return
            else:
                logger.warning(f"Verification FAILED for {task_id}: {v_feedback}")
                task_meta["retries"] = current_retry + 1
                task_meta["status"] = "failed"
                task_meta["last_verification_result"] = "fail"
                task_meta["last_delta_summary"] = v_feedback
                save_state(state)
                
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            task_meta["status"] = "failed"
            save_state(state)
            raise

    logger.error(f"Task {task_id} failed after {MAX_RETRIES} retries. Stopping.")
    raise RuntimeError(f"Max retries reached for task {task_id}")

def main():
    parser = argparse.ArgumentParser(description="Cursor Cloud Agent Orchestrator")
    parser.add_argument("--feature", help="Feature directory name inside specs/ (e.g., 001-ui-theme)")
    parser.add_argument("--task", help="Run a specific task ID (e.g., T001)")
    parser.add_argument("--dry-run", action="store_true", help="Prepare prompt without launching agent")
    args = parser.parse_args()

    REPO_URL = get_env_var("GITHUB_REPO_URL")

    try:
        feature_dir = get_feature_dir(args.feature)
        tasks_md_path = os.path.join(feature_dir, "tasks.md")
        state = load_state()
        
        if args.task:
            if args.dry_run:
                spec_path = os.path.join(feature_dir, "spec.md")
                plan_path = os.path.join(feature_dir, "plan.md")
                prompt = assemble_prompt(args.task, spec_path, plan_path, tasks_md_path)
                print("\n--- DRY RUN: PROMPT ---")
                print(prompt)
                print("--- END PROMPT ---\n")
                sys.exit(0)
            process_task(args.task, feature_dir, REPO_URL, state)
        else:
            logger.info(f"Starting iterative task loop for: {feature_dir}...")
            pending = get_pending_tasks(tasks_md_path)
            if not pending:
                logger.info("No pending tasks to process.")
                sys.exit(0)
            
            for task_id in pending:
                logger.info(f"\n--- NEXT TASK: {task_id} ---")
                process_task(task_id, feature_dir, REPO_URL, state)
                logger.info(f"--- FINISHED TASK: {task_id} ---\n")
            
            logger.info(f"All tasks in {tasks_md_path} processed successfully!")

    except Exception as e:
        logger.error(f"Fatal loop error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
