import os
import re
from src.utils import logger, get_env_var
import time
from src.cursor_api import get_agent_status
from src.utils import POLLING_INTERVAL, MAX_POLLING_ATTEMPTS

# ... existing code ...

def monitor_agent(agent_id):
    """Poll agent status until FINISHED or error."""
    attempts = 0
    while attempts < MAX_POLLING_ATTEMPTS:
        logger.info(f"Polling status for agent {agent_id} (attempt {attempts+1})...")
        status_data = get_agent_status(agent_id)
        status = status_data.get("status")
        
        logger.info(f"Agent status: {status}")
        
        if status == "FINISHED":
            return status_data
        elif status in ["FAILED", "STOPPED", "DELETED"]:
            raise RuntimeError(f"Agent {agent_id} ended with terminal status: {status}")
        
        time.sleep(POLLING_INTERVAL)
        attempts += 1
    
    raise TimeoutError(f"Polling timeout for agent {agent_id}")
    """Extract task title and description from tasks.md."""
    if not os.path.exists(TASKS_MD):
        raise FileNotFoundError(f"Tasks file not found: {TASKS_MD}")
    
    task_details = {"id": task_id, "title": "", "description": ""}
    
    try:
        with open(TASKS_MD, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if f"- [ ] {task_id}" in line or f"- [x] {task_id}" in line:
                    task_details["title"] = line.strip().split(task_id)[-1].strip()
                    # Check next line for description
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("- Description:"):
                        task_details["description"] = lines[i+1].strip().replace("- Description:", "").strip()
                    break
    except Exception as e:
        logger.error(f"Error extracting task details: {e}")
        raise
    
    return task_details

def assemble_prompt(task_id, spec_path, plan_path):
    """Combine Spec, Plan, and Task into a unified prompt."""
    task = extract_task_details(task_id)
    
    try:
        with open(spec_path, 'r') as f:
            spec_content = f.read()
        with open(plan_path, 'r') as f:
            plan_content = f.read()
    except Exception as e:
        logger.error(f"Error reading spec or plan: {e}")
        raise

    prompt = f"""
    You are a Cursor Cloud Agent assigned to complete a specific task.
    
    ### CONTEXT:
    #### SPECIFICATION:
    {spec_content}
    
    #### IMPLEMENTATION PLAN:
    {plan_content}
    
    ### YOUR TASK:
    **Task ID**: {task_id}
    **Title**: {task['title']}
    **Description**: {task['description']}
    
    Please implement this task. Follow the plan and stay within the specification.
    Once finished, provide a summary of your changes.
    """
    return prompt.strip()
