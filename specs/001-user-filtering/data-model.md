# Data Model: User Filtering and Workload Indicators

**Feature**: User Filtering and Workload Indicators  
**Date**: 2026-01-25  
**Phase**: 1 - Design & Contracts

## Entities

### User

Represents a team member or assignee who can be assigned to cards and filtered in the board view.

**Attributes**:
- `id` (string, required, unique): Unique identifier for the user. Used for filtering and card assignment.
- `name` (string, required): Display name of the user. Shown in filter dropdown and board header.
- `status` (string, computed): Current workload status. Values: "OK" (3 or fewer cards, including 0), "Busy" (more than 3 cards). Calculated dynamically based on card count.

**Validation Rules**:
- `id` must be non-empty string
- `name` must be non-empty string, max 200 characters
- `status` is computed, not stored (derived from card count)

**Storage**:
- Users are assumed to exist in the system (managed by separate user management feature)
- User data may be stored in localStorage or provided via props/context
- Status is computed on-the-fly, not persisted

**Relationships**:
- One-to-many with Card (one user can have many cards assigned)
- Status calculated from Card count

### Card

Represents a task or work item on the Kanban board that can be assigned to a user and filtered.

**Attributes**:
- `id` (string, required, unique): Unique identifier for the card.
- `assignedUserId` (string, optional): ID of the user assigned to this card. Single user only (per clarification). If null/undefined, card is unassigned.
- `title` (string, required): Card title/name.
- `columnId` (string, optional): ID of the column the card is in (for board organization).
- Other card attributes (description, due date, etc.) are assumed from existing board feature.

**Validation Rules**:
- `id` must be non-empty string
- `assignedUserId` must reference a valid User ID if provided
- `title` must be non-empty string

**Storage**:
- Cards are stored in localStorage (assumed from existing board feature)
- Cards array structure: `[{ id, assignedUserId, title, columnId, ... }, ...]`

**Relationships**:
- Many-to-one with User (many cards can be assigned to one user)
- Cards contribute to user workload calculation

### User Workload

Represents the calculated workload state for a user based on their assigned cards.

**Attributes**:
- `userId` (string, required): Reference to User ID.
- `cardCount` (number, computed): Number of cards assigned to this user. Calculated by counting cards where `assignedUserId === userId`.
- `status` (string, computed): Workload status. Values: "OK" (cardCount ≤ 3), "Busy" (cardCount > 3).
- `hasIndicator` (boolean, computed): Whether workload indicator should be displayed. True when cardCount > 3.

**Validation Rules**:
- `cardCount` must be non-negative integer
- `status` must be "OK" or "Busy"
- `hasIndicator` is true when cardCount > 3

**Storage**:
- Not persisted - calculated on-the-fly from cards array
- Stored in memory as Map<userId, UserWorkload> for efficient lookup

**Relationships**:
- One-to-one with User (each user has one workload calculation)
- Derived from Card assignments

### Filter State

Represents the current user filter selection state.

**Attributes**:
- `selectedUserId` (string | null, required): ID of the currently selected user for filtering. If null, no filter is active (show all cards).
- `isActive` (boolean, computed): Whether filter is currently active. True when selectedUserId !== null.

**Validation Rules**:
- `selectedUserId` must be valid User ID or null
- `isActive` is computed from selectedUserId

**Storage**:
- Stored in localStorage under key `user_filter` (string value of userId or empty string for no filter)
- Also stored in React component state for reactivity
- Persisted across page refreshes

**Relationships**:
- References User (selectedUserId → User.id)

## Data Flow

### Filter Application Flow

1. **User Selection**: User selects a user from filter dropdown
2. **State Update**: `selectedUserId` is set in React state
3. **Persistence**: Filter value saved to localStorage
4. **Card Filtering**: Cards array filtered using `useMemo`: `cards.filter(card => card.assignedUserId === selectedUserId)`
5. **UI Update**: Board displays only filtered cards, other cards hidden

### Workload Calculation Flow

1. **Card Change**: Card assigned/reassigned (cards array updated)
2. **Recalculation**: `calculateUserWorkloads(cards)` function called
3. **Counting**: Iterate through cards, count per userId: `Map<userId, count>`
4. **Status Calculation**: For each user, determine status: count ≤ 3 ? "OK" : "Busy"
5. **Indicator Flag**: Set `hasIndicator = true` when count > 3
6. **Memoization**: Result memoized with `useMemo` to avoid recalculation
7. **UI Update**: Status and indicators update in filter control/header

### Status Update Flow

1. **Card Assignment Change**: Card assigned to user (cardCount increases)
2. **Threshold Check**: If cardCount crosses 3 (becomes 4), status changes from "OK" to "Busy"
3. **Immediate Update**: Status badge updates immediately via React re-render
4. **Indicator Display**: Workload indicator (badge + color) appears
5. **Reverse Change**: If cardCount decreases to 3 or less, status changes back to "OK", indicator disappears

## State Management

### Filter State Structure

```typescript
interface FilterState {
  selectedUserId: string | null;
  setSelectedUserId: (userId: string | null) => void;
  clearFilter: () => void;
}
```

### Workload State Structure

```typescript
interface UserWorkload {
  userId: string;
  cardCount: number;
  status: "OK" | "Busy";
  hasIndicator: boolean;
}

type WorkloadMap = Map<string, UserWorkload>;
```

### React Hooks

- `useUserFilter()`: Manages filter state, localStorage persistence, filtered cards
- `useUserWorkloads(cards)`: Calculates and memoizes user workloads from cards array

## localStorage Schema

### Filter State Storage

```typescript
// Stored as string in localStorage
localStorage.setItem('user_filter', userId); // or '' for no filter

// Retrieved on mount
const savedFilter = localStorage.getItem('user_filter') || null;
```

### Card Storage (Assumed from Existing Feature)

```typescript
// Cards stored as JSON array
localStorage.setItem('kanban_cards', JSON.stringify([
  { id: 'card-1', assignedUserId: 'user-1', title: 'Task 1', ... },
  { id: 'card-2', assignedUserId: 'user-2', title: 'Task 2', ... },
  // ... more cards
]));
```

## Performance Considerations

- Filtering uses `useMemo` to avoid recalculation when filter or cards haven't changed
- Workload calculation uses `useMemo` to avoid recalculation when cards array hasn't changed
- Workload map provides O(1) lookup for user card counts
- For typical board sizes (dozens to hundreds of cards), in-memory operations are fast
- No database queries needed (front-end only app)
- React re-renders only when filter value or cards array changes

## Data Migration & Compatibility

**Current Version**: 1.0.0

**Future Considerations**:
- If card schema changes (e.g., multi-user assignment), filter logic may need updates
- If user schema changes, filter dropdown may need updates
- Filter state format is simple (string userId), unlikely to need migration
- Workload calculation is computed, no migration needed
