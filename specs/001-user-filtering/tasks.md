# Tasks: User Filtering and Workload Indicators

**Input**: Design documents from `/specs/001-user-filtering/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the feature specification. Focus on implementation tasks for MVP.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: Next.js App Router structure with `app/` directory
- Components: `app/components/board/`
- Services: `app/lib/services/`
- Hooks: `app/lib/hooks/`
- Utils: `app/lib/utils/`
- Types: `app/types/`
- Tests: `tests/unit/`, `tests/integration/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Install ShadCN UI Badge and Select components: `npx shadcn-ui@latest add badge` and `npx shadcn-ui@latest add select`
- [ ] T002 [P] Ensure Next.js 14+ project structure exists with App Router in repository root
- [ ] T003 [P] Verify Tailwind CSS 3.x is configured with mobile-first responsive design (iPhone 15: 390x844px breakpoints)
- [ ] T004 [P] Verify TypeScript 5.x configuration (tsconfig.json) with strict mode
- [ ] T005 [P] Create project directory structure: app/components/board/, app/lib/services/, app/lib/hooks/, app/lib/utils/, app/types/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Create User type definition in app/types/user.ts with id, name attributes
- [ ] T007 [P] Create Card type definition in app/types/user.ts with id, assignedUserId, title, columnId attributes
- [ ] T008 [P] Create UserWorkload type definition in app/types/user.ts with userId, cardCount, status, hasIndicator attributes
- [ ] T009 [P] Create FilterState type definition in app/types/user.ts with selectedUserId, filteredCards, isFilterActive attributes
- [ ] T010 [P] Create storage utility functions in app/lib/utils/storage.ts: saveToStorage(key, value), loadFromStorage(key), handle localStorage JSON parsing with error handling
- [ ] T011 Create FilterService in app/lib/services/filter-service.ts with getFilteredCards(), saveFilterToStorage(), loadFilterFromStorage(), clearFilter() methods
- [ ] T012 Create WorkloadCalculator in app/lib/services/workload-calculator.ts with calculateUserWorkloads(), getUserWorkload(), getUserStatus() methods

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Filter Board by User (Priority: P1) 🎯 MVP

**Goal**: Users can filter the Kanban board to show only cards assigned to a specific user

**Independent Test**: Select a user from filter control, verify only that user's cards are displayed, confirm other users' cards are hidden. Test delivers immediate value by enabling focused view of individual user workloads.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create useUserFilter hook in app/lib/hooks/use-user-filter.ts with useState, useEffect, useMemo for filter state management
- [ ] T014 [US1] Implement filter state persistence in app/lib/hooks/use-user-filter.ts: load saved filter from localStorage on mount, save filter to localStorage on change
- [ ] T015 [US1] Implement filtered cards calculation in app/lib/hooks/use-user-filter.ts: use useMemo to filter cards array based on selectedUserId
- [ ] T016 [P] [US1] Create UserFilter component in app/components/board/UserFilter.tsx using ShadCN UI Select component
- [ ] T017 [US1] Implement user selection dropdown in app/components/board/UserFilter.tsx: display all users (including users with 0 cards), handle user selection, show "All users" option
- [ ] T018 [US1] Implement clear filter button in app/components/board/UserFilter.tsx: reset filter to show all cards
- [ ] T019 [US1] Integrate UserFilter component into board layout in app/(routes)/board/page.tsx or app/components/board/Board.tsx
- [ ] T020 [US1] Implement card filtering logic in board component: use filteredCards from useUserFilter hook, hide cards not matching filter
- [ ] T021 [US1] Test filter persistence: select user, refresh page, verify filter is restored from localStorage
- [ ] T022 [US1] Test dynamic updates: with filter active, assign new card to filtered user, verify card appears immediately

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can filter board by user and see only that user's cards.

---

## Phase 4: User Story 2 - Visual Workload Indicator for Overloaded Users (Priority: P2)

**Goal**: Users see a visual indicator (badge with card count + color highlight) when the selected user has more than 3 cards

**Independent Test**: Filter board for user with 4+ cards, verify workload indicator appears with badge showing count and color highlight, confirm indicator is visible but non-blocking. Test delivers value by making workload imbalances immediately apparent.

### Implementation for User Story 2

- [ ] T023 [P] [US2] Create WorkloadIndicator component in app/components/board/WorkloadIndicator.tsx using ShadCN UI Badge component
- [ ] T024 [US2] Implement badge display in app/components/board/WorkloadIndicator.tsx: show card count (e.g., "4 cards"), apply color highlight (Tailwind: bg-orange-100 border-orange-300 text-orange-800)
- [ ] T025 [US2] Implement conditional rendering in app/components/board/WorkloadIndicator.tsx: only display when cardCount > 3
- [ ] T026 [US2] Integrate WorkloadIndicator into UserFilter component in app/components/board/UserFilter.tsx: display next to user name when user has >3 cards
- [ ] T027 [US2] Connect WorkloadIndicator to workload calculation: use calculateUserWorkloads() to get cardCount for selected user
- [ ] T028 [US2] Implement real-time updates in app/components/board/WorkloadIndicator.tsx: update immediately when card assignments change
- [ ] T029 [US2] Test indicator appearance: assign 4th card to user, verify indicator appears within 1 second (SC-002)
- [ ] T030 [US2] Test indicator removal: reassign card to reduce count to 3, verify indicator disappears immediately
- [ ] T031 [US2] Test non-blocking behavior: with indicator displayed, interact with board, verify indicator doesn't block interactions (FR-007)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can filter by user and see workload indicators for overloaded users.

---

## Phase 5: User Story 3 - User Status Change Based on Workload (Priority: P3)

**Goal**: Users see the selected user's status (OK/Busy) change based on card count, displayed next to user name

**Independent Test**: Filter board for user, verify status shows "OK" with 3 or fewer cards, assign 4th card, verify status changes to "Busy" immediately. Test delivers value by providing clear status information for workload balancing decisions.

### Implementation for User Story 3

- [ ] T032 [P] [US3] Create UserStatusBadge component in app/components/board/UserStatusBadge.tsx using ShadCN UI Badge component
- [ ] T033 [US3] Implement status display in app/components/board/UserStatusBadge.tsx: show "OK" (green variant) or "Busy" (orange/red variant) based on status prop
- [ ] T034 [US3] Implement status calculation logic in app/components/board/UserStatusBadge.tsx: use getUserStatus() from WorkloadCalculator (≤3 = OK, >3 = Busy)
- [ ] T035 [US3] Integrate UserStatusBadge into UserFilter component in app/components/board/UserFilter.tsx: display next to selected user name in filter control/board header
- [ ] T036 [US3] Connect UserStatusBadge to workload calculation: use calculateUserWorkloads() to get status for selected user
- [ ] T037 [US3] Implement real-time status updates in app/components/board/UserStatusBadge.tsx: update immediately when card count crosses threshold (3 cards)
- [ ] T038 [US3] Test status display: filter by user with 3 cards, verify status shows "OK"
- [ ] T039 [US3] Test status change to Busy: assign 4th card to user, verify status changes to "Busy" within 1 second (SC-003)
- [ ] T040 [US3] Test status change to OK: reassign card to reduce count to 3, verify status changes back to "OK" immediately
- [ ] T041 [US3] Test boundary condition: user with exactly 3 cards shows "OK" status

**Checkpoint**: At this point, all user stories should be independently functional. Users can filter by user, see workload indicators, and view user status.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T042 [P] Add mobile-responsive design to UserFilter component in app/components/board/UserFilter.tsx: ensure touch-friendly interactions, responsive layout for iPhone 15 (390x844px)
- [ ] T043 [P] Add mobile-responsive design to WorkloadIndicator component in app/components/board/WorkloadIndicator.tsx: ensure badge is readable and touch-friendly on mobile
- [ ] T044 [P] Add mobile-responsive design to UserStatusBadge component in app/components/board/UserStatusBadge.tsx: ensure status badge is visible and accessible on mobile
- [ ] T045 [P] Configure PWA support: verify next-pwa is configured in next.config.js, ensure service worker doesn't interfere with localStorage operations
- [ ] T046 [P] Test PWA installation: verify app can be installed on iPhone 15 Safari, test offline functionality with filter state persistence
- [ ] T047 [P] Add error handling for localStorage access failures (private browsing mode) in app/lib/utils/storage.ts and app/lib/services/filter-service.ts
- [ ] T048 [P] Optimize performance: ensure useMemo prevents unnecessary recalculations, verify filtering completes within 2 seconds (SC-001)
- [ ] T049 [P] Add accessibility features: ARIA labels for filter control, keyboard navigation support, WCAG AA color contrast for badges and status
- [ ] T050 [P] Test edge cases: user with 0 cards (shows in filter, status OK), rapid status changes, filter applied during card movement
- [ ] T051 [P] Test on mobile devices: verify feature works correctly on iPhone 15+ with touch interactions and responsive layout (SC-009)
- [ ] T052 [P] Test PWA functionality: verify offline support works, filter state persists, app can be installed (SC-010)
- [ ] T053 Run quickstart.md validation: test all manual test scenarios from quickstart guide

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

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories. Core filtering functionality.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 1 components (UserFilter) but adds independent workload indicator functionality
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on User Story 1 components (UserFilter) but adds independent status display functionality

### Within Each User Story

- Types before services (types defined in Phase 2)
- Services before hooks (FilterService, WorkloadCalculator before useUserFilter)
- Hooks before components (useUserFilter before UserFilter component)
- Components before integration (individual components before board integration)
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T001-T005)
- All Foundational tasks marked [P] can run in parallel (T006-T010)
- Once Foundational phase completes:
  - User Story 1: T013, T016 can run in parallel
  - User Story 2: T023 can start after US1 UserFilter exists
  - User Story 3: T032 can start after US1 UserFilter exists
- Polish phase tasks marked [P] can all run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch foundational type definitions in parallel:
Task: "Create User type definition in app/types/user.ts"
Task: "Create Card type definition in app/types/user.ts"
Task: "Create UserWorkload type definition in app/types/user.ts"
Task: "Create FilterState type definition in app/types/user.ts"

# Launch User Story 1 components in parallel:
Task: "Create useUserFilter hook in app/lib/hooks/use-user-filter.ts"
Task: "Create UserFilter component in app/components/board/UserFilter.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (ShadCN UI components, directory structure)
2. Complete Phase 2: Foundational (types, services) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (filtering functionality)
4. **STOP and VALIDATE**: Test User Story 1 independently - select user, verify filtering works
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - filtering works!)
3. Add User Story 2 → Test independently → Deploy/Demo (users can see workload indicators)
4. Add User Story 3 → Test independently → Deploy/Demo (users can see status)
5. Add Polish phase → Mobile/PWA support → Final validation
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (FilterService, useUserFilter, UserFilter component)
   - Developer B: User Story 2 (WorkloadIndicator component) - can start after US1 UserFilter
   - Developer C: User Story 3 (UserStatusBadge component) - can start after US1 UserFilter
3. Stories complete and integrate independently
4. Polish phase: Mobile/PWA tasks can be done in parallel

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- localStorage key for filter: `user_filter` (string value of userId or empty string)
- Mobile-first design: optimize for iPhone 15 (390x844px) as reference
- PWA: Ensure service worker doesn't interfere with localStorage filter persistence
- Performance: Use useMemo to prevent unnecessary recalculations (filtering, workload calculation)
