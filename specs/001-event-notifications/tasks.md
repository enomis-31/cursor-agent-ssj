# Tasks: Calendar Event Notifications

**Input**: Design documents from `/specs/001-event-notifications/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the feature specification. Focus on implementation tasks for MVP.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: Next.js App Router structure with `app/` directory
- Components: `app/components/notifications/`
- Services: `app/lib/services/`
- Hooks: `app/lib/hooks/`
- Utils: `app/lib/utils/`
- Types: `app/types/`
- Tests: `tests/unit/`, `tests/integration/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create Next.js 14+ project structure with App Router in repository root
- [ ] T002 [P] Install and configure dependencies: next, react, react-dom, typescript, tailwindcss, shadcn-ui, sonner, date-fns, next-pwa
- [ ] T003 [P] Configure Tailwind CSS with mobile-first responsive design (iPhone 15: 390x844px breakpoints)
- [ ] T004 [P] Initialize ShadCN UI components library and install Sonner toast component
- [ ] T005 [P] Configure next-pwa for Progressive Web Application support in next.config.js
- [ ] T006 [P] Setup TypeScript configuration (tsconfig.json) with strict mode
- [ ] T007 [P] Create project directory structure: app/components/notifications/, app/lib/services/, app/lib/hooks/, app/lib/utils/, app/types/, public/sounds/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 [P] Create CalendarEvent type definition in app/types/event.ts with id, title, startTime, description? attributes
- [ ] T009 [P] Create NotificationState type definition in app/types/event.ts with id, eventId, eventTitle, eventStartTime, triggeredAt, isDismissed, isSoundMuted, isDetailsShown attributes
- [ ] T010 [P] Create storage utility functions in app/lib/utils/storage.ts: getEventsFromStorage(), getEventById(eventId), handle localStorage JSON parsing with error handling
- [ ] T011 [P] Create date utility functions in app/lib/utils/date-utils.ts: isEventTimeInWindow(eventStartTime, windowSeconds), formatEventTime(startTime), getCurrentTime()
- [ ] T012 Create NotificationContext and Provider in app/lib/hooks/use-notifications.ts with React Context API and useReducer for state management
- [ ] T013 Implement notification reducer actions in app/lib/hooks/use-notifications.ts: ADD_NOTIFICATION, DISMISS_NOTIFICATION, SHOW_EVENT_DETAILS, CLEAR_OLD_NOTIFICATIONS
- [ ] T014 Create useNotifications custom hook in app/lib/hooks/use-notifications.ts that provides access to notification state and actions
- [ ] T015 Add NotificationProvider to app layout in app/layout.tsx to wrap application with notification context

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Receive Notification When Event Time Arrives (Priority: P1) 🎯 MVP

**Goal**: Users receive notifications (popup and sound) when calendar event start times arrive while the app is open

**Independent Test**: Create a calendar event with start time 1 minute in the future, keep app open, verify notification appears when event time arrives. Test delivers immediate value by alerting users to upcoming events.

### Implementation for User Story 1

- [ ] T016 [P] [US1] Create EventMonitor service class in app/lib/services/event-monitor.ts with startMonitoring() and stopMonitoring() methods
- [ ] T017 [US1] Implement polling logic in app/lib/services/event-monitor.ts: setInterval every 60 seconds, check localStorage for events
- [ ] T018 [US1] Implement time window check in app/lib/services/event-monitor.ts: filter events where startTime falls within ±5 seconds of current time
- [ ] T019 [US1] Implement duplicate prevention in app/lib/services/event-monitor.ts: track notified events by eventId + time window to prevent duplicate notifications
- [ ] T020 [US1] Create NotificationService class in app/lib/services/notification-service.ts with triggerNotification(event) method
- [ ] T021 [US1] Implement notification creation in app/lib/services/notification-service.ts: create NotificationState object and dispatch ADD_NOTIFICATION action
- [ ] T022 [P] [US1] Create NotificationPopup component in app/components/notifications/NotificationPopup.tsx using ShadCN UI Sonner/Toast
- [ ] T023 [US1] Implement notification display in app/components/notifications/NotificationPopup.tsx: show event title and scheduled time, mobile-responsive design (iPhone 15 optimized)
- [ ] T024 [US1] Create audio service in app/lib/services/notification-service.ts: playNotificationSound() using HTML5 Audio API
- [ ] T025 [US1] Add notification sound file to public/sounds/notification.mp3 (short, pleasant sound < 2 seconds)
- [ ] T026 [US1] Integrate audio playback in app/lib/services/notification-service.ts: play sound by default when notification triggers, handle browser autoplay policies
- [ ] T027 [US1] Create NotificationManager client component in app/components/notifications/NotificationManager.tsx that initializes EventMonitor on mount
- [ ] T028 [US1] Implement tab visibility check in app/lib/services/event-monitor.ts: only trigger notifications when browser tab is active (FR-006 requirement)
- [ ] T029 [US1] Add NotificationManager to app layout in app/layout.tsx to start event monitoring when app loads
- [ ] T030 [US1] Implement multiple simultaneous notifications support in app/components/notifications/NotificationList.tsx: display up to 10 notifications (SC-004 requirement)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can receive notifications when event times arrive.

---

## Phase 4: User Story 2 - Dismiss Notification Popup (Priority: P2)

**Goal**: Users can dismiss notification popups to clear them from the screen and continue working

**Independent Test**: Trigger a notification, verify popup appears, click dismiss button, confirm popup disappears. Test delivers value by giving users control over their notification experience.

### Implementation for User Story 2

- [ ] T031 [US2] Add dismiss button to NotificationPopup component in app/components/notifications/NotificationPopup.tsx using ShadCN UI Button component
- [ ] T032 [US2] Implement dismiss handler in app/components/notifications/NotificationPopup.tsx: call dismissNotification action from context on button click
- [ ] T033 [US2] Update notification reducer in app/lib/hooks/use-notifications.ts: handle DISMISS_NOTIFICATION action, set isDismissed flag, remove from state
- [ ] T034 [US2] Implement immediate UI removal in app/components/notifications/NotificationPopup.tsx: animate out notification on dismiss, remove from DOM after animation
- [ ] T035 [US2] Add dismiss functionality to NotificationList component in app/components/notifications/NotificationList.tsx: each notification can be dismissed independently
- [ ] T036 [US2] Test multiple notification dismissal: verify dismissing one notification doesn't affect others (FR-007, FR-010 requirement)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can receive and dismiss notifications.

---

## Phase 5: User Story 3 - View Event Details from Notification (Priority: P3)

**Goal**: Users can click on notifications to view expanded event details without navigating through the calendar

**Independent Test**: Trigger a notification, click on notification popup (not dismiss button), verify event details modal opens with full event information. Test delivers value by providing contextual information without leaving current view.

### Implementation for User Story 3

- [ ] T037 [P] [US3] Create EventDetailsModal component in app/components/notifications/EventDetailsModal.tsx using ShadCN UI Dialog/Modal
- [ ] T038 [US3] Implement click handler in app/components/notifications/NotificationPopup.tsx: detect click on notification body (not dismiss button), trigger showEventDetails action
- [ ] T039 [US3] Update notification reducer in app/lib/hooks/use-notifications.ts: handle SHOW_EVENT_DETAILS action, set isDetailsShown flag, dismiss notification popup
- [ ] T040 [US3] Implement event data retrieval in app/lib/services/notification-service.ts: showEventDetails(notificationId) method that fetches event from localStorage by eventId
- [ ] T041 [US3] Display event details in app/components/notifications/EventDetailsModal.tsx: show event title, scheduled time (formatted), description if available
- [ ] T042 [US3] Add close button to EventDetailsModal in app/components/notifications/EventDetailsModal.tsx: close modal and return to main view
- [ ] T043 [US3] Implement modal state management in app/lib/hooks/use-notifications.ts: track which notification has details shown, handle modal open/close
- [ ] T044 [US3] Add backdrop click handler in app/components/notifications/EventDetailsModal.tsx: close modal when clicking outside (optional enhancement)

**Checkpoint**: At this point, all user stories should be independently functional. Users can receive notifications, dismiss them, and view event details.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Add error handling for localStorage access failures (private browsing mode) in app/lib/utils/storage.ts
- [ ] T046 [P] Add error handling for audio playback failures in app/lib/services/notification-service.ts: gracefully continue without sound if audio fails
- [ ] T047 [P] Implement notification cleanup in app/lib/hooks/use-notifications.ts: clearOldNotifications() removes notifications older than 5 minutes
- [ ] T048 [P] Add loading states for event data retrieval in app/components/notifications/EventDetailsModal.tsx
- [ ] T049 [P] Optimize notification rendering performance: ensure app remains responsive during notification checks (SC-005 requirement)
- [ ] T050 [P] Add accessibility features: ARIA labels, keyboard navigation (Enter to show details, Escape to dismiss) in app/components/notifications/NotificationPopup.tsx
- [ ] T051 [P] Ensure WCAG AA color contrast standards in app/components/notifications/NotificationPopup.tsx and EventDetailsModal.tsx
- [ ] T052 [P] Test mobile responsiveness on iPhone 15 dimensions (390x844px): verify notifications display correctly, touch targets are adequate (44x44px minimum)
- [ ] T053 [P] Test PWA installation: verify app can be installed on iPhone 15 Safari, service worker doesn't interfere with notification polling
- [ ] T054 [P] Add console logging for debugging: log notification triggers, dismissals, event monitoring cycles (development mode only)
- [ ] T055 Run quickstart.md validation: test all manual test scenarios from quickstart guide

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories. Core notification functionality.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 1 components (NotificationPopup) but adds independent dismiss functionality
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on User Story 1 components (NotificationPopup) but adds independent event details functionality

### Within Each User Story

- Services before components (EventMonitor/NotificationService before UI components)
- Core functionality before enhancements (notification display before sound, basic popup before details modal)
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T007)
- All Foundational tasks marked [P] can run in parallel (T008-T011)
- Once Foundational phase completes:
  - User Story 1: T016, T022, T025 can run in parallel
  - User Story 2: Can start after US1 NotificationPopup exists
  - User Story 3: T037 can start in parallel with US2
- Polish phase tasks marked [P] can all run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch foundational type definitions in parallel:
Task: "Create CalendarEvent type definition in app/types/event.ts"
Task: "Create NotificationState type definition in app/types/event.ts"

# Launch utility functions in parallel:
Task: "Create storage utility functions in app/lib/utils/storage.ts"
Task: "Create date utility functions in app/lib/utils/date-utils.ts"

# Launch User Story 1 components in parallel:
Task: "Create NotificationPopup component in app/components/notifications/NotificationPopup.tsx"
Task: "Add notification sound file to public/sounds/notification.mp3"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (Next.js, dependencies, ShadCN UI, Tailwind, PWA)
2. Complete Phase 2: Foundational (types, utils, context) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (event monitoring, notifications, sound)
4. **STOP and VALIDATE**: Test User Story 1 independently - create test event, verify notification appears
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - notifications work!)
3. Add User Story 2 → Test independently → Deploy/Demo (users can dismiss)
4. Add User Story 3 → Test independently → Deploy/Demo (users can view details)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (EventMonitor, NotificationService, NotificationPopup)
   - Developer B: User Story 2 (dismiss functionality) - can start after US1 NotificationPopup
   - Developer C: User Story 3 (EventDetailsModal) - can start after US1 NotificationPopup
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- localStorage key for events: `calendar_events` (JSON array)
- Notification sound: short, pleasant sound file in `public/sounds/notification.mp3`
- Mobile-first design: optimize for iPhone 15 (390x844px) as reference
- PWA: Ensure service worker doesn't interfere with 60-second polling interval
