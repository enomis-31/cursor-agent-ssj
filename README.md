# Cursor Cloud Agent Orchestrator

A lightweight local orchestrator for Cursor Cloud Agents, driven by Spec Kit.

## Features
- **Iterative Loop**: Automatically processes tasks from `tasks.md`.
- **Branch Chaining**: Sequential git branch chaining for each task.
- **Smart Verification**: Uses GPT-4o-mini to verify agent output against specifications.
- **Auto-Retry**: Supports up to 2 automatic retries with differential feedback on failure.
- **State Persistence**: Maintains progress in `state.json`.

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file:
```env
CURSOR_API_KEY=your_cursor_api_key
OPENAI_API_KEY=your_openai_api_key
GITHUB_REPO_URL=https://github.com/your-org/your-repo
```

## Run the full orchestration loop (auto-detects if only one feature exists):
```bash
python src/main.py
```

Run a specific feature:
```bash
python src/main.py --feature 001-cloud-agent-orchestrator
```

Run a specific task:
```bash
python src/main.py --task T001
```

Dry run (view prompts):
```bash
python src/main.py --task T001 --dry-run
```

## Architecture
- `src/main.py`: Entry point and orchestration loop.
- `src/orchestrator.py`: Logic for task parsing and prompt assembly.
- `src/cursor_api.py`: Wrapper for Cursor Cloud API endpoints.
- `src/verifier.py`: GPT-mini verification logic.
- `src/state_manager.py`: JSON state management and Markdown sync.
- `src/utils.py`: Git utilities and logging.
