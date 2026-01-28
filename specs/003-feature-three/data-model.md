# Data Model: Cursor Cloud Agent Orchestrator

## Entities

### 1. OrchestratorState (Global)
Represents the current progress of the project orchestration.

**Example Structure (`state.json`):**
```json
{
  "last_successful_branch": "feature/001-cloud-agent-orchestrator",
  "tasks": {
    "T1": {
      "status": "completed",
      "agent_id": "agt_123",
      "retries": 1,
      "last_verification_result": "pass",
      "last_delta_summary": "..."
    }
  }
}
```

- `last_successful_branch`: String (Name of the branch produced by the last successful task).
- `tasks`: Map<TaskID, TaskMetadata> (History and details for each task).

### 2. TaskMetadata
Metadata for an individual task execution.
- `status`: Enum (pending, running, verifying, completed, failed).
- `agent_id`: String (Cursor Agent ID).
- `retries`: Integer (Number of retries performed).
- `last_verification_result`: Enum (pass, fail, null).
- `last_delta_summary`: String (The differential feedback report from GPT-mini).

### 3. AgentContext (Dynamic)
The payload sent to the Cursor API.
- `prompt`: String (Unified context from Spec + Plan + Task).
- `source_ref`: String (The branch to start from - for chaining).

## State Transitions
1. **PENDING** -> **RUNNING**: When an agent is launched via `/v0/agents`.
2. **RUNNING** -> **VERIFYING**: When the agent status becomes `FINISHED`.
3. **VERIFYING** -> **COMPLETED**: When GPT-mini confirms requirements are met.
4. **VERIFYING** -> **RUNNING** (Retry): When verification fails but `attempts < 2`.
5. **VERIFYING** -> **FAILED**: When verification fails and `attempts == 2`.
