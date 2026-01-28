# Research: Cursor Cloud Agent Orchestrator

## Technology Choices

### Decision 1: Language & Style
- **Decision**: Python 3.10+ using functional programming style.
- **Rationale**: User requested Python and "simple code" with minimal classes and abstractions. Functions are the primary unit of organization.
- **Alternatives considered**: Object-Oriented Python (rejected due to user preference for simplicity).

### Decision 2: Orchestration Brain (Local)
- **Decision**: OpenAI API (GPT-4o-mini).
- **Rationale**: User explicitly requested OpenAI API for the local "brain" that handles verification and logic. GPT-4o-mini is efficient and cost-effective for verification tasks.
- **Alternatives considered**: Local models via Ollama (rejected for speed and reliability in a 1-hour build).

### Decision 3: Cloud Orchestration
- **Decision**: Cursor Cloud Agent API.
- **Rationale**: Core requirement of the project to leverage Cursor's native cloud capabilities.

### Decision 4: State Management
- **Decision**: Local `state.json` + `tasks.md` sync.
- **Rationale**: JSON is easy to parse and update in Python; syncing to `tasks.md` provides human-readable feedback.

## Integration Patterns

### API Integration: Cursor Cloud
- **Endpoints to use**: 
  - `POST /v0/agents`: Launching agents.
  - `GET /v0/agents/{id}`: Polling status.
  - `POST /v0/agents/{id}/followup`: For retries/differential feedback.

### Error Handling Policy
- **Decision**: "Fail Fast & Loud".
- **Rationale**: User explicitly stated that silent errors are unacceptable. Every failed API call or unexpected state must raise an exception or print a clear error message.
