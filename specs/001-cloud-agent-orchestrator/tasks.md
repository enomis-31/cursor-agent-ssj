---

description: "Task list for Cursor Cloud Agent Orchestrator implementation"
---

# Tasks: Cursor Cloud Agent Orchestrator

**Input**: Design documents from `/specs/001-cloud-agent-orchestrator/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Test tasks are included using GPT-mini for verification logic.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan (src/ folder)
- [x] T002 [P] Initialize Python project with dependencies (requests, openai, python-dotenv) in requirements.txt
- [x] T003 [P] Setup environment configuration helpers in src/utils.py (logging, env loading)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Implement state management logic in src/state_manager.py (state.json CRUD and tasks.md sync)
- [x] T005 [P] Implement Git utility functions in src/utils.py (branch creation, current branch detection)
- [x] T006 [P] Implement Cursor Cloud API wrappers in src/cursor_api.py (launch, poll status, followup)
- [x] T007 [P] Implement OpenAI/GPT-mini client in src/verifier.py (completion verification logic)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Single Task Execution (Priority: P1) 🎯 MVP

**Goal**: Prepare prompt and launch a single task from tasks.md via Cursor API.

**Independent Test**: Run `python src/main.py --task T1` and verify agent launch in Cursor Dashboard.

### Implementation for User Story 1

- [x] T008 [US1] Implement task parsing logic in src/orchestrator.py (extract T<n> from tasks.md)
- [x] T009 [US1] Implement prompt assembly logic in src/orchestrator.py (inject Spec + Plan context)
- [x] T010 [US1] Create CLI entry point in src/main.py to handle --task and --dry-run arguments
- [x] T011 [US1] Add "Fail Fast & Loud" error handling for API launch failures in src/cursor_api.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Status Tracking & Verification (Priority: P2)

**Goal**: Monitor agent progress and verify output using GPT-mini before marking as complete.

**Independent Test**: Simulate agent completion and check if state.json and tasks.md are updated correctly.

### Implementation for User Story 2

- [x] T012 [US2] Implement polling loop in src/orchestrator.py (monitor status via cursor_api.py)
- [x] T013 [US2] Implement verification workflow in src/verifier.py (GPT-mini pass/fail logic)
- [x] T014 [US2] Implement state synchronization in src/state_manager.py (update JSON and tasks.md [x])
- [x] T015 [US2] Add observability logging for polling and verification steps in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Iterative Task Loop (Priority: P3)

**Goal**: Automatically process all pending tasks in sequence with branch chaining and retries.

**Independent Test**: Run `python src/main.py` and verify it processes 3 tasks in a row automatically.

### Implementation for User Story 3

- [x] T016 [US3] Implement sequential loop logic in src/main.py (pick first [ ] task)
- [x] T017 [US3] Implement branch chaining in src/orchestrator.py (use last_successful_branch as base)
- [x] T018 [US3] Implement double-retry logic with differential feedback in src/orchestrator.py
- [x] T019 [US3] Implement stop-on-failure logic with clear error reporting in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and documentation

- [x] T020 [P] Finalize README.md and documentation in docs/
- [x] T021 [P] Add final dry-run validation checks across all components
- [x] T022 Run quickstart.md validation to ensure everything works as documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - Sequential execution: US1 (P1) → US2 (P2) → US3 (P3)
- **Polish (Final Phase)**: Depends on all user stories being complete

---

## Parallel Example: Foundational Phase

```bash
# Launch independent foundational tasks together:
Task: "Implement Git utility functions in src/utils.py"
Task: "Implement Cursor Cloud API wrappers in src/cursor_api.py"
Task: "Implement OpenAI/GPT-mini client in src/verifier.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Launch a single task manually.

### Incremental Delivery

1. Add US2: Enable tracking and verification.
2. Add US3: Enable the full autonomous loop.
3. Each story adds value without breaking previous stories.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Commit after each task or logical group
- Avoid vague tasks, keep implementations simple as per constitution.
