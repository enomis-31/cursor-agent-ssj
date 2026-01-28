import argparse
import sys
from src.utils import logger, get_env_var
from src.orchestrator import assemble_prompt, monitor_agent
from src.cursor_api import launch_agent, add_followup
from src.verifier import run_verification
from src.state_manager import load_state, save_state, sync_task_to_md, get_pending_tasks, TASKS_MD

def process_task(task_id, spec_path, plan_path, repo_url, state):
    """Full workflow for processing a single task with retries."""
    if "tasks" not in state: state["tasks"] = {}
    
    if task_id not in state["tasks"]:
        state["tasks"][task_id] = {"status": "pending", "retries": 0}

    task_meta = state["tasks"][task_id]
    
    # Check if already completed
    if task_meta.get("status") == "completed":
        logger.info(f"Task {task_id} is already completed. Skipping.")
        return

    MAX_RETRIES = 2
    
    while task_meta.get("retries", 0) <= MAX_RETRIES:
        try:
            current_retry = task_meta.get("retries", 0)
            if current_retry == 0:
                prompt = assemble_prompt(task_id, spec_path, plan_path)
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
            
            # Monitor
            logger.info(f"Monitoring agent {agent_id} for task {task_id}...")
            status_data = monitor_agent(agent_id)
            output_summary = status_data.get("summary", "Task execution finished.")
            
            # Verify
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
                sync_task_to_md(task_id, completed=True)
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
    parser.add_argument("--task", help="Run a specific task ID (e.g., T001)")
    parser.add_argument("--dry-run", action="store_true", help="Prepare prompt without launching agent")
    args = parser.parse_args()

    # Paths (could be made dynamic)
    SPEC_PATH = "specs/001-cloud-agent-orchestrator/spec.md"
    PLAN_PATH = "specs/001-cloud-agent-orchestrator/plan.md"
    REPO_URL = get_env_var("GITHUB_REPO_URL")

    try:
        state = load_state()
        
        if args.task:
            if args.dry_run:
                prompt = assemble_prompt(args.task, SPEC_PATH, PLAN_PATH)
                print("\n--- DRY RUN: PROMPT ---")
                print(prompt)
                print("--- END PROMPT ---\n")
                sys.exit(0)
            process_task(args.task, SPEC_PATH, PLAN_PATH, REPO_URL, state)
        else:
            # Full loop logic
            logger.info("Starting iterative task loop...")
            pending = get_pending_tasks(TASKS_MD)
            if not pending:
                logger.info("No pending tasks to process.")
                sys.exit(0)
            
            for task_id in pending:
                logger.info(f"\n--- NEXT TASK: {task_id} ---")
                process_task(task_id, SPEC_PATH, PLAN_PATH, REPO_URL, state)
                logger.info(f"--- FINISHED TASK: {task_id} ---\n")
            
            logger.info("All tasks in tasks.md processed successfully!")

    except Exception as e:
        logger.error(f"Fatal loop error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
