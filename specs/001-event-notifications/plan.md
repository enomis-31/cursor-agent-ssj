# Implementation Plan: Calendar Event Notifications

**Branch**: `001-event-notifications` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-event-notifications/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement calendar event notifications that alert users when scheduled event times arrive while the app is open. The system monitors calendar events, detects when event start times fall within a ±5 second window of the current time, and displays visible popup notifications with optional sound alerts. Users can dismiss notifications and view event details. 

**Technical Approach**: Built as a Next.js 14+ Progressive Web Application using ShadCN UI (Sonner/Toast) components and Tailwind CSS. Event monitoring uses React `useEffect` with `setInterval` for 60-second polling. Audio playback via HTML5 Audio API. State management with React Context + useReducer. Event storage in browser localStorage (simple JSON array - front-end only test app). Optimized for mobile devices (iPhone 15 reference: 390x844px) with a modern, professional design. PWA capabilities via `next-pwa` package.

## Technical Context

**Language/Version**: TypeScript 5.x, JavaScript (ES2022+)  
**Primary Dependencies**: Next.js 14+ (App Router), React 18+, ShadCN UI, Tailwind CSS 3.x, date-fns (for date/time operations), next-pwa (for PWA capabilities)  
**Storage**: Browser localStorage (simple JSON array storage - per user clarification, front-end only test app)  
**Testing**: Jest, React Testing Library, Playwright (for integration tests)  
**Target Platform**: Web browsers (Chrome, Firefox, Safari), Progressive Web App (PWA) for mobile devices, iPhone 15+ as reference design  
**Project Type**: Web application (Next.js frontend)  
**Performance Goals**: Notifications appear within 5 seconds of event time (SC-002), dismiss actions complete within 1 second (SC-006), event details load in under 2 seconds (SC-008), app remains responsive during notification checks (SC-005)  
**Constraints**: Must work only when app is open and browser tab is active (FR-006), no background notifications, must handle up to 10 simultaneous events (SC-004), polling interval at least once per minute (FR-008), must meet WCAG AA contrast standards (constitution)  
**Scale/Scope**: Single-user application, handles typical calendar event volumes (dozens to hundreds of events), notification system checks events every minute, designed for iPhone 15 screen dimensions (390x844px) as mobile reference

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Simplicity First ✅
- Notification system uses simple polling mechanism (once per minute) - no complex scheduling
- Single notification component with basic dismiss functionality
- Sound notification is simple toggle, no persistent preferences storage
- **Status**: PASS - Implementation is minimal and focused on core requirements

### II. User Experience Priority ✅
- Clear, visible notification popups with event title and time
- Intuitive dismiss button
- Sound provides immediate feedback
- Mobile-responsive design ensures usability on iPhone 15
- **Status**: PASS - UX requirements are clear and user-focused

### III. Component-Based Architecture ✅
- Notification popup as reusable component
- Event details view as separate component
- Notification manager service as independent module
- **Status**: PASS - Architecture aligns with component-based approach

### IV. Data Persistence ✅
- Calendar events stored in localStorage (simple JSON array - per user clarification)
- No backend server required
- Notification state (dismissed notifications) can use localStorage or React state
- **Status**: PASS - Uses browser-local storage as required, simplified for test app

### V. Progressive Enhancement ✅
- User Story 1 (P1) provides core notification functionality independently
- User Story 2 (P2) adds dismiss capability incrementally
- User Story 3 (P3) adds event details view as enhancement
- **Status**: PASS - Feature can be delivered incrementally

**Overall Status**: ✅ ALL GATES PASS - No violations detected. Implementation plan complies with all constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-event-notifications/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
app/
├── (routes)/
│   ├── calendar/
│   └── notifications/
├── components/
│   ├── ui/              # ShadCN UI components
│   ├── notifications/
│   │   ├── NotificationPopup.tsx
│   │   ├── NotificationList.tsx
│   │   └── EventDetailsModal.tsx
│   └── layout/
├── lib/
│   ├── services/
│   │   ├── notification-service.ts
│   │   └── event-monitor.ts
│   ├── hooks/
│   │   └── use-notifications.ts
│   └── utils/
│       ├── date-utils.ts
│       └── storage.ts
├── types/
│   └── event.ts
└── public/
    └── sounds/          # Notification sound files

tests/
├── unit/
│   ├── services/
│   └── utils/
├── integration/
│   └── notifications.test.tsx
└── __mocks__/
```

**Structure Decision**: Next.js App Router structure with feature-based component organization. Components are organized by feature (notifications) with shared UI components from ShadCN UI. Services and hooks are separated for testability. This structure supports component-based architecture (Constitution Principle III) and enables independent testing of notification functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected - complexity tracking not required.
