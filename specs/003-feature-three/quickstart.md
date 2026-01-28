# Quickstart: Cursor Cloud Agent Orchestrator

## Prerequisites
- Python 3.10+
- `pip install requests openai python-dotenv`
- Cursor API Key (obtained from settings)
- OpenAI API Key

## Configuration
Create a `.env` file in the project root:
```env
CURSOR_API_KEY=your_key
OPENAI_API_KEY=your_key
GITHUB_REPO_URL=https://github.com/user/repo
```

## Usage

### 1. Dry Run
See what the orchestrator would do without launching agents:
```bash
python src/main.py --dry-run
```

### 2. Run Orchestration Loop
Start the iterative loop for all pending tasks in `tasks.md`:
```bash
python src/main.py
```

### 3. Process Specific Task
Run the orchestrator for a single task:
```bash
python src/main.py --task T1
```

## Monitoring
Check `state.json` for real-time metadata on agent IDs and verification results.
Check `tasks.md` for the updated list of completed tasks.
