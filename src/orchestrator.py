import os
import re
import time
from src.utils import logger, get_env_var, POLLING_INTERVAL, MAX_POLLING_ATTEMPTS
from src.cursor_api import get_agent_status

IMPLEMENT_INSTRUCTIONS = """
### IMPLEMENTATION RULES (from speckit.implement.md):
1. **Analyze Context**: Read tasks.md, plan.md, and any other available spec files (data-model.md, research.md, etc.).
2. **Setup Verification**: Ensure proper ignore files (.gitignore, etc.) are present and correct for the tech stack.
3. **Phase-by-Phase**: Complete each phase (Setup, Core, Integration, Polish) defined in tasks.md.
4. **Progress Tracking**: After each completed task, mark it as [X] in tasks.md and report progress.
5. **Fail Fast**: If a non-parallel task fails, stop and report the error with context.
6. **Final Validation**: Ensure all tasks match the original specification and the technical plan.
"""

POLISH_PROMPTS = {
    "logs": """
### POLISH PHASE: LOGS
Goal: Ensure consistent, informative, and traceable logging.
- Check all major functions for entry/exit logs.
- Ensure log levels (INFO, ERROR, DEBUG) are used appropriately.
- Add context to log messages where necessary.
""",
    "errors": """
### POLISH PHASE: ERRORS
Goal: Ensure robust error handling following the 'Fail Fast & Loud' policy.
- Ensure all potential exceptions are caught and reported clearly.
- Avoid silent failures (e.g., empty 'except' blocks).
- Raise descriptive errors that help in debugging.
""",
    "hinting": """
### POLISH PHASE: HINTING
Goal: Ensure proper type hinting and inline documentation.
- Add type hints to all function arguments and return types.
- Ensure complex data structures are well-documented.
- Follow PEP 8 and standard docstring conventions.
""",
    "tests": """
### POLISH PHASE: TESTS
Goal: Ensure existence and passing of unit, integration, and E2E tests.
- Verify that all core functionalities have corresponding tests.
- Run the tests to ensure they pass.
- Add missing tests for edge cases identified during implementation.
"""
}

def assemble_feature_prompt(feature_dir):
    """Assemble a prompt for a full feature implementation."""
    spec_path = os.path.join(feature_dir, "spec.md")
    plan_path = os.path.join(feature_dir, "plan.md")
    tasks_path = os.path.join(feature_dir, "tasks.md")

    if not os.path.exists(spec_path) or not os.path.exists(plan_path) or not os.path.exists(tasks_path):
        raise FileNotFoundError(f"Missing core spec files in {feature_dir}")

    try:
        with open(spec_path, 'r') as f: spec_content = f.read()
        with open(plan_path, 'r') as f: plan_content = f.read()
        with open(tasks_path, 'r') as f: tasks_content = f.read()
    except Exception as e:
        logger.error(f"Error reading feature files: {e}")
        raise

    prompt = f"""
You are a Cursor Cloud Agent assigned to implement an entire feature.

### CONTEXT:
#### SPECIFICATION:
{spec_content}

#### IMPLEMENTATION PLAN:
{plan_content}

#### TASKS TO EXECUTE:
{tasks_content}

{IMPLEMENT_INSTRUCTIONS}

Please implement the feature as described. Follow the plan and stay within the specification.
Maintain progress in tasks.md as you work.
Once finished, provide a summary of your changes.
"""
    return prompt.strip()

def assemble_polish_prompt(phase_name):
    """Assemble a prompt for a global polish phase."""
    if phase_name not in POLISH_PROMPTS:
        raise ValueError(f"Unknown polish phase: {phase_name}")

    prompt = f"""
You are a Cursor Cloud Agent assigned to a global polish phase of the project.

{POLISH_PROMPTS[phase_name]}

Please review the current state of the codebase and apply the necessary improvements as described.
Once finished, provide a summary of your changes.
"""
    return prompt.strip()

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

# Legacy functions kept for backward compatibility if needed temporarily
def extract_task_details(task_id, tasks_md_path):
    # (Implementation remains same or simplified if no longer used)
    return {"id": task_id, "title": "Legacy Task", "description": ""}

def assemble_prompt(task_id, spec_path, plan_path, tasks_md_path):
    # (Implementation remains same or simplified if no longer used)
    return "Legacy prompt"
