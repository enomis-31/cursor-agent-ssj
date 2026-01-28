# Implementation Plan: User Filtering and Workload Indicators

**Branch**: `001-user-filtering` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-user-filtering/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement user filtering and workload indicators for the Kanban board. The system allows users to filter the board by a specific user, displays visual indicators (badge with card count + color highlight) when a user has more than 3 cards, and shows user status (OK/Busy) based on card count. Status and indicators update immediately when card assignments change.

**Technical Approach**: Built as a Next.js 14+ web application using ShadCN UI components and Tailwind CSS. Filtering uses React state management with localStorage persistence. Workload calculation uses efficient card counting per user. Visual indicators implemented as non-blocking badges with color highlights. Status display integrated into filter control/board header. Real-time updates via React state synchronization when cards are assigned/reassigned.

## Technical Context

**Language/Version**: TypeScript 5.x, JavaScript (ES2022+)  
**Primary Dependencies**: Next.js 14+ (App Router), React 18+, ShadCN UI, Tailwind CSS 3.x  
**Storage**: Browser localStorage (simple JSON array storage - per constitution, front-end only test app)  
**Testing**: Jest, React Testing Library, Playwright (for integration tests)  
**Target Platform**: Web browsers (Chrome, Firefox, Safari), desktop-first with mobile responsiveness  
**Project Type**: Web application (Next.js frontend)  
**Performance Goals**: Filtering completes within 2 seconds (SC-001), indicators appear within 1 second (SC-002), status changes visible immediately within 1 second (SC-003), board remains responsive during filtering (SC-007)  
**Constraints**: Must work with existing Kanban board and card functionality, filter state can persist in localStorage, must meet WCAG AA contrast standards (constitution), indicators must be non-blocking (FR-007)  
**Scale/Scope**: Single-user application, handles typical Kanban board volumes (dozens to hundreds of cards), designed for desktop browsers with mobile responsiveness

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Simplicity First ✅
- Filtering uses simple React state + localStorage persistence - no complex state management
- Workload calculation is straightforward card counting per user
- Visual indicators are simple badges with color highlights - no complex animations
- Status calculation is simple threshold check (≤3 = OK, >3 = Busy)
- **Status**: PASS - Implementation is minimal and focused on core requirements

### II. User Experience Priority ✅
- Clear filter control with user selection
- Visual indicators (badge + color) provide immediate feedback
- Status display is prominent and visible at a glance
- Non-blocking indicators don't interrupt workflow
- **Status**: PASS - UX requirements are clear and user-focused

### III. Component-Based Architecture ✅
- User filter control as reusable component
- Workload indicator badge as separate component
- Status display as independent component
- Filter logic as service/hook module
- **Status**: PASS - Architecture aligns with component-based approach

### IV. Data Persistence ✅
- Filter state stored in localStorage (per constitution)
- Card data already persisted (assumed from existing board feature)
- No backend server required
- **Status**: PASS - Uses browser-local storage as required

### V. Progressive Enhancement ✅
- User Story 1 (P1) provides core filtering functionality independently
- User Story 2 (P2) adds workload indicators incrementally
- User Story 3 (P3) adds status display as enhancement
- **Status**: PASS - Feature can be delivered incrementally

**Overall Status**: ✅ ALL GATES PASS - No violations detected. Implementation plan complies with all constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-user-filtering/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md         # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
app/
├── (routes)/
│   └── board/
├── components/
│   ├── ui/              # ShadCN UI components
│   ├── board/
│   │   ├── UserFilter.tsx
│   │   ├── WorkloadIndicator.tsx
│   │   └── UserStatusBadge.tsx
│   └── layout/
├── lib/
│   ├── services/
│   │   ├── filter-service.ts
│   │   └── workload-calculator.ts
│   ├── hooks/
│   │   └── use-user-filter.ts
│   └── utils/
│       └── storage.ts
├── types/
│   └── user.ts
└── public/

tests/
├── unit/
│   ├── services/
│   └── utils/
├── integration/
│   └── user-filtering.test.tsx
└── __mocks__/
```

**Structure Decision**: Next.js App Router structure with feature-based component organization. Components are organized by feature (board filtering) with shared UI components from ShadCN UI. Services and hooks are separated for testability. This structure supports component-based architecture (Constitution Principle III) and enables independent testing of filtering functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected - complexity tracking not required.
