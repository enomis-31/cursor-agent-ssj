# Cursor Cloud Agent Orchestrator

A lightweight local orchestrator for Cursor Cloud Agents, driven by Spec Kit.

## Features
- **Feature-Centric Workflow**: Iterates through high-level features defined in `specs/`.
- **Polish Phases**: Automated global polish for Logs, Errors, Hinting, and Tests.
- **Branch Chaining**: Sequential git branch chaining for each phase.
- **Verification (Optional)**: Uses GPT-4o-mini to verify output against specifications.
- **Verifier Bypass**: Disable AI verification with `--no-verify` for faster execution.
- **State Persistence**: Maintains progress in `state.json`.

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file:
```env
CURSOR_API_KEY=your_cursor_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional if using --no-verify
GITHUB_REPO_URL=https://github.com/your-org/your-repo
```

## Usage

### 1. Run Full Workflow
Automatically processes all features in `specs/` followed by the 4 polish phases:
```bash
python src/main.py
```

### 2. Run with Verifier Bypass
Skip GPT-mini verification (useful for rapid iteration or cost saving):
```bash
python src/main.py --no-verify
```

### 3. Run Specific Feature
Implement only a specific feature directory:
```bash
python src/main.py --feature 001-cloud-agent-orchestrator
```

### 4. Dry Run
View the prompts that would be sent to the agents:
```bash
python src/main.py --dry-run
```

## Workflow Phases
1. **Phase 1: Features**: Sequential implementation of all directories in `specs/`.
2. **Phase 2: Polish**:
   - **Logs**: Consistent and traceable logging.
   - **Errors**: Robust error handling (Fail Fast & Loud).
   - **Hinting**: Type hints and inline documentation.
   - **Tests**: Unit, Integration, and E2E test existence.

## Architecture
- `src/main.py`: Phase management and orchestration loop.
- `src/orchestrator.py`: Logic for assembling feature and polish prompts.
- `src/cursor_api.py`: Wrapper for Cursor Cloud API.
- `src/verifier.py`: GPT-mini verification logic.
- `src/state_manager.py`: State persistence in `state.json`.
- `src/utils.py`: Git and logging utilities.
