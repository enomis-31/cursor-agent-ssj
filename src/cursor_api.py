import requests
from src.utils import get_env_var, logger

CURSOR_API_URL = "https://api.cursor.com/v0/agents"

def get_headers():
    """Return headers for the Cursor API."""
    return {
        "Content-Type": "application/json"
    }

def launch_agent(name, prompt_text, repository_url, source_ref="main", model=None):
    """Launch a new Cursor Cloud Agent."""
    payload = {
        "source": {
            "repository": repository_url,
            "ref": source_ref
        },
        "prompt": {
            "text": prompt_text
        }
    }
    
    if model:
        payload["model"] = model
    
    api_key = get_env_var("CURSOR_API_KEY")
    response = requests.post(CURSOR_API_URL, headers=get_headers(), json=payload, auth=(api_key, ""))
    if not (200 <= response.status_code < 300):
        logger.error(f"Failed to launch agent (HTTP {response.status_code}): {response.text}")
        response.raise_for_status()
    
    return response.json()

def get_agent_status(agent_id):
    """Retrieve the status of a Cursor Cloud Agent."""
    url = f"{CURSOR_API_URL}/{agent_id}"
    api_key = get_env_var("CURSOR_API_KEY")
    response = requests.get(url, headers=get_headers(), auth=(api_key, ""))
    if not (200 <= response.status_code < 300):
        logger.error(f"Failed to get agent status (HTTP {response.status_code}): {response.text}")
        response.raise_for_status()
    
    return response.json()

def add_followup(agent_id, followup_text):
    """Add a follow-up instruction to a Cursor Cloud Agent."""
    url = f"{CURSOR_API_URL}/{agent_id}/followup"
    payload = {
        "prompt": {
            "text": followup_text
        }
    }
    
    api_key = get_env_var("CURSOR_API_KEY")
    response = requests.post(url, headers=get_headers(), json=payload, auth=(api_key, ""))
    if not (200 <= response.status_code < 300):
        logger.error(f"Failed to add followup (HTTP {response.status_code}): {response.text}")
        response.raise_for_status()
    
    return response.json()
