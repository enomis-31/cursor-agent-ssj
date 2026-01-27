<!--
  Sync Impact Report:
  - Version change: none → 1.0.0
  - List of modified principles:
    - [PRINCIPLE_1_NAME] → I. Simple Local Orchestration
    - [PRINCIPLE_2_NAME] → II. Spec-Driven Development
    - [PRINCIPLE_3_NAME] → III. Statefulness & Traceability
    - [PRINCIPLE_4_NAME] → IV. Hierarchical Orchestration
    - [PRINCIPLE_5_NAME] → V. Cloud-First Execution
  - Added sections: Governance, Input/Output Standard, Orchestration Process.
  - Templates requiring updates: ✅ updated (checked plan-template.md, spec-template.md, tasks-template.md)
  - Follow-up TODOs: none.
-->

# Cursor Cloud Agent Orchestrator Constitution

## Core Principles

### I. Simple Local Orchestration
The orchestrator must remain simple and efficient, running on the local PC while delegating the heavy lifting to Cursor Cloud Agents. The local system acts as the "brain" that coordinates, while the Cloud Agents act as the "hands."

### II. Spec-Driven Development
All orchestration must be driven by a set of specifications that are the output of Spec Kit. This ensures that every action taken by a Cloud Agent is grounded in a well-defined requirement, plan, or task.

### III. Statefulness & Traceability
The orchestrator must maintain an accurate and real-time state of the project. It must track which parts of the specifications are completed, which are in progress, and which are pending, ensuring no task is lost or duplicated.

### IV. Hierarchical Orchestration (The Outer Loop)
The system operates as a high-level orchestrator above Cursor's native cloud orchestration. It breaks down large projects into smaller, intermediate tasks that can be independently executed by Cloud Agents, following an iterative pattern similar to a "Ralph Loop."

### V. Cloud-First Execution
The system must leverage Cursor's native Cloud Agent APIs and orchestration capabilities wherever possible. The orchestrator's goal is to complement and guide these capabilities, not to reinvent them locally.

## Input/Output Standard

The orchestrator uses the following Spec Kit artifacts as primary inputs:
- **Spec**: High-level feature definitions and user stories.
- **Plan**: Technical architecture and integration strategy.
- **Tasks**: Granular, executable todo items.

All outputs from Cloud Agents must be validated against these artifacts before being marked as complete.

## Orchestration Process

1. **Decomposition**: The orchestrator reads the Spec Kit output and decomposes the project into a sequence of executable tasks.
2. **Dispatch**: Tasks are dispatched to Cursor Cloud Agents via the API.
3. **Monitoring**: The orchestrator monitors the status of the Cloud Agent.
4. **Verification**: Once a Cloud Agent finishes, the orchestrator verifies the work against the original specification.
5. **Iteration**: If more work is needed, the orchestrator initiates a follow-up or a new agent call.

## Governance

- **Supremacy**: This constitution supersedes all other development guidelines within this project.
- **Amendments**: Any change to this constitution requires a version bump and a Sync Impact Report.
- **Compliance**: Every implemented feature must be traceable back to a requirement in the Spec Kit artifacts.

**Version**: 1.0.0 | **Ratified**: 2026-01-28 | **Last Amended**: 2026-01-28
