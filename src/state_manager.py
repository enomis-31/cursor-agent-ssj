import json
import os
import re
from src.utils import logger

STATE_FILE = "state.json"

def load_state():
    """Load the orchestrator state from state.json."""
    if not os.path.exists(STATE_FILE):
        return {"last_successful_branch": "main", "tasks": {}}
    
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load state: {e}")
        raise RuntimeError("Cannot proceed: state file is missing or corrupted.")

def save_state(state):
    """Save the orchestrator state to state.json."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        logger.error(f"Failed to save state: {e}")
        raise

def sync_task_to_md(task_id, tasks_md_path, completed=True):
    """Sync a task's completion status back to the tasks.md file."""
    if not os.path.exists(tasks_md_path):
        logger.warning(f"Tasks file not found: {tasks_md_path}. Skipping sync.")
        return

    try:
        with open(tasks_md_path, 'r') as f:
            content = f.read()

        marker = "[x]" if completed else "[ ]"
        # Match - [ ] T001 or - [x] T001
        pattern = rf"- \[ [x ] \] {task_id}"
        replacement = f"- {marker} {task_id}"
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(tasks_md_path, 'w') as f:
                f.write(new_content)
            logger.info(f"Synced {task_id} status to {tasks_md_path}")
        else:
            logger.warning(f"Task {task_id} not found in {tasks_md_path} for sync.")
            
    except Exception as e:
        logger.error(f"Failed to sync task to markdown: {e}")
        raise

def get_pending_tasks(tasks_md_path):
    """Parse tasks.md and return a list of pending task IDs in order."""
    if not os.path.exists(tasks_md_path):
        return []
    
    pending = []
    try:
        with open(tasks_md_path, 'r') as f:
            for line in f:
                match = re.search(r"- \[ \] (T\d+)", line)
                if match:
                    pending.append(match.group(1))
    except Exception as e:
        logger.error(f"Error parsing tasks file: {e}")
    
    return pending
