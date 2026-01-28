import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("orchestrator")

def get_env_var(name, required=True):
    """Retrieve environment variable or raise error if required."""
    value = os.getenv(name)
    if required and not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value

def setup_logging():
    """Returns the logger instance."""
    return logger

# Polling and retry constants
POLLING_INTERVAL = 5  # seconds
MAX_POLLING_ATTEMPTS = 60  # total 5 minutes

import subprocess

def run_command(cmd):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}\nError: {e.stderr}")
        raise

def get_current_branch():
    """Get the name of the current git branch."""
    return run_command("git branch --show-current")

def checkout_branch(branch_name, create=False):
    """Checkout a branch, optionally creating it."""
    flag = "-b" if create else ""
    run_command(f"git checkout {flag} {branch_name}")

def push_branch(branch_name):
    """Push the branch to origin."""
    run_command(f"git push origin {branch_name}")
