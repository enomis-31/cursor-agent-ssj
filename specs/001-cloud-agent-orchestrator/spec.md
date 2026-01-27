# Feature Specification: Cursor Cloud Agent Orchestrator

**Feature Branch**: `001-cloud-agent-orchestrator`  
**Created**: 2026-01-28  
**Status**: Draft  
**Input**: User description: "Implementa l'orchestratore locale per chiamare Cursor Cloud Agents via API, tracciando lo stato dei task definiti in specs/ e seguendo un loop iterativo. Mi raccomando, manteniamoci sulla semplicità, in quanto è un progetto che voglio realizzare nel giro di un'ora. Quindi, dobbiamo fare solamente il necessario e dobbiamo essere efficienti. Quello che voglio andare a fare, semplicemente, è sfruttare l'alta descrizione del requisito che si riesce ad ottenere tramite Spec Kit, in maniera tale da fornire alla gente Cursor delle istruzioni precisissime. Quello che voglio fare, locale al massimo, è forse testing dell'output della gente Cursor e la verifica dell'avanzamento dei requisiti. Cioè non so. Vorrei limitare al massimo quello che facciamo in locale, perchè non abbiamo intelligenza, non possiamo seguire ovviamente modelli. Potremmo usare un API, in realtà, per orchestrare il locale. Effettivamente, potremmo usare un API economica tipo GPT-mini, che è il cervello locale che orchestra la parte locale, sempre implementato in maniera molto semplice. Di base, il locale deve solo verificare qual'è l'output o, comunque, orchestrare i processi. Non so se questa cosa conviene farla tramite script puro o aggiungere un po' di intelligenza, quindi avere anche un'altra fonte di intelligenza artificiale da inserire nell'operatività locale."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single Task Execution (Priority: P1)

As a developer, I want the local orchestrator to take a single task from my `tasks.md`, prepare a prompt using the associated `spec.md` and `plan.md`, and launch a Cursor Cloud Agent via API.

**Why this priority**: This is the core functionality. Without being able to launch an agent with the right context, the orchestrator cannot function.

**Independent Test**: Can be tested by running the orchestrator on a specific task ID and verifying (via API log or Cursor Dashboard) that a Cloud Agent was launched with the correct prompt and context.

**Acceptance Scenarios**:

1. **Given** a project with initialized Spec Kit files and one pending task, **When** the orchestrator is run for that task, **Then** a Cursor Cloud Agent is launched with a prompt containing relevant specification details.
2. **Given** an invalid task ID, **When** the orchestrator is run, **Then** it returns a clear error message.

---

### User Story 2 - Status Tracking & Verification (Priority: P2)

As a developer, I want the orchestrator to monitor the Cloud Agent's progress and, once finished, verify if the task requirements were met before marking the task as completed in the local state.

**Why this priority**: Ensures that the "Source of Truth" (local specs) stays in sync with the actual implementation in Cloud.

**Independent Test**: Can be tested by simulating an agent completion and checking if the orchestrator updates the task status in `tasks.md` (or a local state file) based on the verification result.

**Acceptance Scenarios**:

1. **Given** a running Cloud Agent, **When** it finishes with status `FINISHED`, **Then** the orchestrator performs a verification check and updates the task status to `[x]`.
2. **Given** an agent that fails or is stopped, **When** the orchestrator detects this, **Then** the task status remains `[ ]` and the error is logged locally.

---

### User Story 3 - Iterative Task Loop (Priority: P3)

As a developer, I want the orchestrator to automatically pick the next available task and repeat the process until the entire project (as defined in `tasks.md`) is complete.

**Why this priority**: Provides the "loop" capability that turns a single agent into an autonomous workflow.

**Independent Test**: Can be tested by providing 3 simple tasks and verifying that the orchestrator executes them sequentially without manual intervention.

**Acceptance Scenarios**:

1. **Given** multiple pending tasks, **When** the orchestrator completes one task successfully, **Then** it automatically proceeds to the next pending task.

---

### Edge Cases

- **API Rate Limits**: How does the system handle hitting Cursor API or LLM API rate limits?
- **Agent Timeout**: What happens if a Cloud Agent hangs or takes too long?
- **Inconsistent Specs**: How does the system handle tasks that don't have a clear mapping to a requirement in `spec.md`?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse Spec Kit `tasks.md` to identify pending tasks and their descriptions.
- **FR-002**: System MUST inject context from `spec.md` and `plan.md` into the prompt sent to the Cloud Agent.
- **FR-003**: System MUST call the Cursor Cloud Agent API (POST `/v0/agents`) to launch tasks.
- **FR-004**: System MUST monitor agent status (GET `/v0/agents/{id}`) until completion.
- **FR-005**: System MUST update the local task status (e.g., in `tasks.md`) upon completion.
- **FR-006**: System SHOULD use a lightweight/cheap LLM (e.g., GPT-4o-mini) to coordinate local orchestration decisions if simple logic is insufficient.
- **FR-007**: System MUST support a "dry-run" mode to see what prompts would be sent without actually launching agents.

### Key Entities

- **Task**: An individual work item with an ID, title, description, and status.
- **Orchestrator State**: A tracking mechanism (could be `tasks.md` itself or a `state.json`) for the current project progress.
- **Agent Context**: The bundle of information (Spec + Plan + Task) sent to the Cloud Agent.

## Assumptions & Constraints

- **Spec Kit Compatibility**: The system assumes the project follows the standard Spec Kit structure (specs/feature/spec.md, plan.md, tasks.md).
- **API Availability**: Assumes the Cursor Cloud Agent API is available and accessible with a valid API key.
- **Task Format**: Assumes tasks in `tasks.md` follow the standard markdown TODO format.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Orchestrator can launch a Cloud Agent within 5 seconds of command execution.
- **SC-002**: 100% of tasks completed by the agent are correctly reflected in the local status file.
- **SC-003**: System can run a full loop of at least 3 tasks without requiring manual CLI input between tasks.
- **SC-004**: Verification logic correctly identifies a failed implementation at least 80% of the time (if using LLM verification).
