# Feature Specification: User Filtering and Workload Indicators

**Feature Branch**: `001-user-filtering`  
**Created**: 2026-01-25  
**Status**: Draft  
**Input**: User description: "La Kanban board deve supportare un sistema di filtraggio per utente, che permette di visualizzare solo le card assegnate a uno specifico user. Quando un utente selezionato ha più di tre card assegnate, la board deve renderlo evidente tramite un indicatore visivo non bloccante (notifica/UI highlight) associato allo user. Questo indicatore non interrompe il flusso di lavoro ma segnala un potenziale sovraccarico. Lo stato dell'utente può cambiare (es. \"OK\" → \"Busy\") quando supera il limite di tre card. Il cambio di stato deve essere visibile a colpo d'occhio nel contesto del board filtrato. L'obiettivo della feature è evidenziare lo sbilanciamento del carico tra utenti e facilitare il monitoraggio della distribuzione del lavoro."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Filter Board by User (Priority: P1)

As a user viewing the Kanban board, I want to filter the board to show only cards assigned to a specific user, so that I can focus on that user's workload and tasks.

**Why this priority**: Filtering is the foundation of this feature. Without the ability to filter by user, workload indicators and status changes cannot be meaningfully displayed in context. This must work reliably as the base functionality for all workload monitoring features.

**Independent Test**: Can be fully tested by selecting a user from a filter control, verifying that only cards assigned to that user are displayed, and confirming that cards assigned to other users are hidden. This delivers immediate value by enabling focused view of individual user workloads.

**Acceptance Scenarios**:

1. **Given** I am viewing the Kanban board with multiple cards assigned to different users, **When** I select a specific user from the filter control, **Then** only cards assigned to that user are displayed and all other cards are hidden
2. **Given** I have filtered the board to show cards for a specific user, **When** I clear or reset the filter, **Then** all cards are displayed again regardless of assignment
3. **Given** I have filtered the board by user, **When** a new card is assigned to the filtered user, **Then** the new card appears in the filtered view immediately
4. **Given** I have filtered the board by user, **When** a card is reassigned from the filtered user to another user, **Then** the card disappears from the filtered view

---

### User Story 2 - Visual Workload Indicator for Overloaded Users (Priority: P2)

As a user viewing a filtered Kanban board, I want to see a visual indicator when the selected user has more than three cards assigned, so that I can quickly identify potential workload imbalances.

**Why this priority**: The workload indicator provides immediate visual feedback about user overload. While filtering (User Story 1) enables viewing a user's cards, the indicator highlights when that user may be overloaded, which is the core value of workload monitoring. This must be visible but non-intrusive to avoid disrupting workflow.

**Independent Test**: Can be fully tested by filtering the board for a user with more than three cards, verifying that a visual indicator (badge showing card count combined with color highlight) appears associated with that user, and confirming the indicator is visible but doesn't block the board interface. This delivers value by making workload imbalances immediately apparent.

**Acceptance Scenarios**:

1. **Given** I have filtered the board to show cards for a user with exactly 3 cards, **When** I view the filtered board, **Then** no workload indicator is displayed
2. **Given** I have filtered the board to show cards for a user with 4 or more cards, **When** I view the filtered board, **Then** a visual indicator (badge showing card count combined with color highlight) appears associated with that user showing they have more than 3 cards
3. **Given** a user has 4 cards and a workload indicator is displayed, **When** one of their cards is completed or reassigned (reducing to 3 or fewer), **Then** the workload indicator disappears
4. **Given** a user has 3 cards and no indicator, **When** a new card is assigned to them (increasing to 4), **Then** the workload indicator appears immediately
5. **Given** a workload indicator is displayed, **When** I interact with the board (move cards, create cards), **Then** the indicator remains visible but does not block or interrupt my workflow

---

### User Story 3 - User Status Change Based on Workload (Priority: P3)

As a user viewing a filtered Kanban board, I want to see the selected user's status change (e.g., "OK" to "Busy") when they have more than three cards, so that I can quickly assess their availability and workload at a glance.

**Why this priority**: Status changes provide additional context beyond the visual indicator. While the indicator (User Story 2) shows overload, the status change provides a clear, at-a-glance understanding of user availability. This enhances the workload monitoring capability but can be implemented after the core filtering and indicator functionality.

**Independent Test**: Can be fully tested by filtering the board for a user, verifying their status displays as "OK" when they have 3 or fewer cards, then assigning additional cards to exceed 3, and confirming the status changes to "Busy" (or equivalent) and is visible in the filtered board context. This delivers value by providing clear status information that supports workload balancing decisions.

**Acceptance Scenarios**:

1. **Given** I have filtered the board to show cards for a user with 3 or fewer cards, **When** I view the filtered board, **Then** the user's status is displayed as "OK" (or equivalent normal status)
2. **Given** a user has 3 cards and status "OK", **When** a new card is assigned to them (increasing to 4), **Then** their status changes to "Busy" (or equivalent overloaded status) and is visible in the filtered board
3. **Given** a user has 4 cards and status "Busy", **When** one of their cards is completed or reassigned (reducing to 3 or fewer), **Then** their status changes back to "OK"
4. **Given** I am viewing a filtered board with a user's status displayed, **When** the status changes, **Then** the change is immediately visible without requiring page refresh or manual update
5. **Given** a user's status is "Busy" in the filtered view, **When** I clear the filter to show all users, **Then** the status information remains accurate for that user in any context where it's displayed

### Edge Cases

- How does the system handle rapid status changes (e.g., card assigned then immediately reassigned)?
- What happens if the filter is applied while cards are being moved between columns?
- How does the system handle users that don't exist or have been removed?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a user filter control that allows users to select a specific user from a list of available users (including users with 0 cards)
- **FR-002**: System MUST filter the Kanban board to display only cards assigned to the selected user when a user filter is active
- **FR-003**: System MUST hide all cards not assigned to the selected user when a user filter is active
- **FR-004**: System MUST allow users to clear or reset the filter to display all cards again
- **FR-005**: System MUST count the number of cards assigned to each user
- **FR-006**: System MUST display a visual indicator (badge showing card count combined with color highlight) when a filtered user has more than 3 cards assigned
- **FR-007**: System MUST ensure the workload indicator is non-blocking and does not interrupt the user's workflow
- **FR-008**: System MUST update the workload indicator immediately when card assignments change (card added, removed, or reassigned)
- **FR-009**: System MUST display user status as "OK" (or equivalent) when a user has 3 or fewer cards assigned
- **FR-010**: System MUST display user status as "Busy" (or equivalent) when a user has more than 3 cards assigned
- **FR-011**: System MUST update user status immediately when the card count crosses the threshold (3 cards)
- **FR-012**: System MUST display user status prominently next to the user's name in the filter control or board header area so it's visible at a glance
- **FR-013**: System MUST maintain accurate card counts and status even when cards are moved between columns or modified
- **FR-014**: System MUST be mobile-responsive and work on mobile devices (iPhone 15+ as reference design: 390x844px)
- **FR-015**: System MUST be integrated as a Progressive Web Application (PWA) with offline capabilities and installability

### Key Entities *(include if feature involves data)*

- **User**: Represents a team member or assignee. Must have at minimum: unique identifier (ID), display name. Users can be assigned to cards and have a status (OK/Busy) based on their card count.
- **Card**: Represents a task or work item on the Kanban board. Must have at minimum: unique identifier (ID), assigned user (single user only). Cards can be filtered by assigned user and contribute to user workload calculations.
- **User Status**: Represents the current workload state of a user. Values: "OK" (3 or fewer cards, including 0 cards), "Busy" (more than 3 cards). Status is calculated based on card count and updates automatically.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can filter the board by a specific user and see only that user's cards within 2 seconds of selecting the filter
- **SC-002**: Workload indicators appear within 1 second when a user's card count exceeds 3
- **SC-003**: User status changes are visible immediately (within 1 second) when card count crosses the 3-card threshold
- **SC-004**: 100% of cards assigned to the filtered user are displayed when filter is active
- **SC-005**: 0% of cards not assigned to the filtered user are displayed when filter is active
- **SC-006**: Users can identify workload imbalances (users with >3 cards) at a glance without manual counting
- **SC-007**: Filtering and workload indicators operate without causing noticeable performance degradation (board remains responsive)
- **SC-008**: Workload indicators and status changes are accurate 100% of the time (no false positives or negatives)
- **SC-009**: Feature works correctly on mobile devices (iPhone 15+ reference) with touch-friendly interactions and responsive layout
- **SC-010**: Feature functions as PWA with offline support and can be installed on mobile devices

## Clarifications

### Session 2026-01-25

- Q: When a card is assigned to multiple users, how should it be handled in filtering and workload calculations? → A: Cards can only be assigned to a single user, not multiple users
- Q: When a user has exactly 3 cards, should their status be "OK" or "Busy"? → A: Status is "OK" when user has exactly 3 cards (3 is the maximum for "OK" status)
- Q: Should users with zero cards appear in the filter dropdown, and what should their status be? → A: Users with 0 cards appear in filter options and have "OK" status (0 ≤ 3)
- Q: Where should the user status be displayed in the filtered board view? → A: Status displayed next to the user's name in the filter control or board header area
- Q: What type of visual indicator should be used when a user has more than 3 cards? → A: Badge indicator showing card count combined with color highlight (badge with count + subtle color highlight)
- Q: Should this feature support mobile devices and PWA capabilities? → A: Yes, the feature must be mobile-responsive and integrated as a Progressive Web Application (PWA)

## Assumptions

- Kanban board and cards already exist in the system (this feature assumes board and card functionality from separate features)
- Cards have a single assigned user (user assignment functionality exists, one user per card)
- Users are identifiable and have unique identifiers
- The system can count cards per user efficiently
- Filter state can be persisted or reset as needed
- Visual indicators can be implemented as non-blocking UI elements (badges, highlights, or subtle notifications)
- Status values "OK" and "Busy" are sufficient for MVP (additional statuses can be added later)
- The 3-card threshold is fixed for MVP (configurable thresholds can be added in future enhancements)
- Feature must be mobile-responsive and work on mobile devices (iPhone 15+ as reference: 390x844px)
- Feature must be integrated as a Progressive Web Application (PWA) with offline capabilities and installability