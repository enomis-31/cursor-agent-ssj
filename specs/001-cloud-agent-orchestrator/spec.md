# Feature Specification: Cursor Cloud Agent Orchestrator

**Feature Branch**: `001-cloud-agent-orchestrator`  
**Created**: 2026-01-28  
**Status**: Draft  
**Input**: User description: "Implementa l'orchestratore locale per chiamare Cursor Cloud Agents via API, tracciando lo stato dei task definiti in specs/ e seguendo un loop iterativo. Mi raccomando, manteniamoci sulla semplicità, in quanto è un progetto che voglio realizzare nel giro di un'ora. Quindi, dobbiamo fare solamente il necessario e dobbiamo essere efficienti. Quello che voglio andare a fare, semplicemente, è sfruttare l'alta descrizione del requisito che si riesce ad ottenere tramite Spec Kit, in maniera tale da fornire alla gente Cursor delle istruzioni precisissime. Quello che voglio fare, locale al massimo, è forse testing dell'output della gente Cursor e la verifica dell'avanzamento dei requisiti. Cioè non so. Vorrei limitare al massimo quello che facciamo in locale, perchè non abbiamo intelligenza, non possiamo seguire ovviamente modelli. Potremmo usare un API, in realtà, per orchestrare il locale. Effettivamente, potremmo usare un API economica tipo GPT-mini, che è il cervello locale che orchestra la parte locale, sempre implementato in maniera molto semplice. Di base, il locale deve solo verificare qual'è l'output o, comunque, orchestrare i processi. Non so se questa cosa conviene farla tramite script puro o aggiungere un po' di intelligenza, quindi avere anche un'altra fonte di intelligenza artificiale da inserire nell'operatività locale."

## Clarifications

### Session 2026-01-28
- Q: Come deve essere gestita la logica di decisione locale (es. decidere se un task è completato o scegliere il prossimo task)? → A: Hybrid (GPT-mini): Usa un LLM solo per la *verifica* dell'output (valutare se il codice prodotto soddisfa la spec).
- Q: Dove deve risiedere la "verità" sull'avanzamento dei task durante l'esecuzione del loop? → A: State JSON: Usa un `state.json` locale per i metadati (ID agenti, log errori) e aggiorna `tasks.md` a completamento.
- Q: Cosa deve fare l'orchestratore quando un task non supera la verifica? → A: Tenta fino a due follow-up di correzione (double retry) e poi si ferma per intervento umano.
- Q: Come deve gestire l'orchestratore la creazione e la progressione dei branch per ogni nuovo task del loop? → A: Sequenziale: Il task N parte dal branch prodotto dal task N-1 (Chaining).
- Q: Come gestire un adempimento parziale delle specifiche mantenendo la base del lavoro precedente? → A: Feedback Differenziale + Summary Reprompt: Invia un report "Delta" (cosa manca) insieme a un riepilogo della specifica originale per mantenere il contesto, lavorando sul branch esistente.
- Q: Come viene selezionato il prossimo task? → A: Il prossimo task pendente è il primo con `[ ]` in `tasks.md`, in ordine top-down di file.
- Q: Quali sono le regole di base per la verifica GPT-mini? → A: Il task è PASS se tutti gli acceptance criteria della User Story sono marcati come soddisfatti dall'LLM; altrimenti FAIL.
- Q: Come vengono gestiti i timeout e gli stati dell'API? → A: Vedere la tabella di mapping "status → azione" nei requisiti funzionali.

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

- **FR-001**: System MUST parse Spec Kit `tasks.md` to identify pending tasks. The next pending task is the first one marked with `[ ]`, in top-down order.
- **FR-002**: System MUST inject context from `spec.md` and `plan.md` into the prompt sent to the Cloud Agent.
- **FR-003**: System MUST call the Cursor Cloud Agent API (POST `/v0/agents`) to launch tasks.
- **FR-004**: System MUST monitor agent status (GET `/v0/agents/{id}`) until completion.
  - **Status Mapping**:
    - `FINISHED` -> Proceed to Verification.
    - `RUNNING` / `PENDING` -> Continue Polling.
    - `FAILED` / `STOPPED` / `DELETED` -> Log error and stop loop.
- **FR-005**: System MUST maintain execution state in a `state.json` file and sync completion status back to `tasks.md`.
- **FR-006**: System MUST use a lightweight LLM (e.g., GPT-4o-mini) specifically for verifying Cloud Agent output.
  - **Verification Rules**: Task is **PASS** if all acceptance criteria of the User Story are satisfied; otherwise **FAIL**.
- **FR-008**: Local orchestration logic (task selection, sequence) MUST remain deterministic/script-based for maximum efficiency.
- **FR-009**: System MUST support up to 2 automatic retries via follow-up prompts if verification fails.
- **FR-013**: Retry prompts MUST include a "Differential Feedback" report (what is missing/wrong) and a "Summary Reprompt" of the core requirements to maintain context.
- **FR-014**: Retry operations MUST continue working on the same branch as the previous attempt to build upon existing progress.
- **FR-010**: System MUST stop and alert the user if a task fails verification after the maximum number of retries.
- **FR-011**: System MUST implement sequential branch chaining: Task N MUST use the resulting branch from Task N-1 as its base (`source.ref`).
- **FR-012**: System MUST track the latest successful branch name in `state.json`.
- **FR-015**: System MUST handle lack of tasks or corrupt state by stopping with a clear message:
  - No tasks: "No pending tasks to process."
  - Corrupt/Missing state: "Cannot proceed: state file is missing or corrupted."
- **FR-007**: System MUST support a "dry-run" mode to see what prompts would be sent without actually launching agents.

### Key Entities

- **Task**: An individual work item with an ID, title, description, status, and associated branch name.
- **Orchestrator State**: A `state.json` file tracking project progress, Agent IDs, verification results, and the current head branch for chaining.
- **Agent Context**: The bundle of information (Spec + Plan + Task) sent to the Cloud Agent, including the correct source branch reference.

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
