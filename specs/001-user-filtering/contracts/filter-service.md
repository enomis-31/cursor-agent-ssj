# Service Contracts: User Filtering and Workload Indicators

**Feature**: User Filtering and Workload Indicators  
**Date**: 2026-01-25  
**Phase**: 1 - Design & Contracts

## Services

### FilterService (lib/services/filter-service.ts)

**Purpose**: Manages user filter state and persistence.

**Methods**:

- `getFilteredCards(cards: Card[], userId: string | null): Card[]`
  - **Description**: Filters cards array to show only cards assigned to the specified user.
  - **Parameters**: 
    - `cards` (Card[]): Array of all cards from the board
    - `userId` (string | null): ID of user to filter by, or null to show all cards
  - **Returns**: Filtered array of cards (only cards where `assignedUserId === userId`, or all cards if userId is null)
  - **Error Handling**: Returns empty array if cards is empty or invalid

- `saveFilterToStorage(userId: string | null): void`
  - **Description**: Persists filter selection to localStorage.
  - **Parameters**: `userId` (string | null) - User ID to save, or null to clear filter
  - **Behavior**: Saves userId to localStorage key `user_filter` (empty string if null)
  - **Error Handling**: Logs error if localStorage write fails, continues without persistence

- `loadFilterFromStorage(): string | null`
  - **Description**: Loads saved filter selection from localStorage.
  - **Returns**: User ID string if filter was saved, or null if no filter saved
  - **Error Handling**: Returns null if localStorage read fails or key doesn't exist

- `clearFilter(): void`
  - **Description**: Clears the active filter (shows all cards).
  - **Behavior**: Removes `user_filter` key from localStorage, sets filter to null

### WorkloadCalculator (lib/services/workload-calculator.ts)

**Purpose**: Calculates user workloads (card counts and status) from cards array.

**Methods**:

- `calculateUserWorkloads(cards: Card[]): Map<string, UserWorkload>`
  - **Description**: Calculates card count and status for each user from cards array.
  - **Parameters**: `cards` (Card[]) - Array of all cards
  - **Returns**: Map where key is userId and value is UserWorkload object with cardCount, status, hasIndicator
  - **Calculation Logic**:
    - Count cards per user: `cards.filter(card => card.assignedUserId === userId).length`
    - Status: "OK" if count ≤ 3, "Busy" if count > 3
    - hasIndicator: true if count > 3
  - **Error Handling**: Returns empty Map if cards is empty or invalid

- `getUserWorkload(workloads: Map<string, UserWorkload>, userId: string): UserWorkload | null`
  - **Description**: Gets workload information for a specific user.
  - **Parameters**: 
    - `workloads` (Map<string, UserWorkload>) - Workload map from calculateUserWorkloads
    - `userId` (string) - User ID to look up
  - **Returns**: UserWorkload object if user found, or null if user not found
  - **Error Handling**: Returns null if userId is invalid or not in map

- `getUserStatus(cardCount: number): "OK" | "Busy"`
  - **Description**: Determines user status based on card count.
  - **Parameters**: `cardCount` (number) - Number of cards assigned to user
  - **Returns**: "OK" if cardCount ≤ 3, "Busy" if cardCount > 3
  - **Error Handling**: Treats negative counts as 0 (returns "OK")

## Components

### UserFilter (app/components/board/UserFilter.tsx)

**Purpose**: Filter control component that allows users to select a user for filtering.

**Props**:
- `users` (User[]): Array of available users to filter by
- `selectedUserId` (string | null): Currently selected user ID (null = no filter)
- `onUserSelect` (function): Callback when user is selected: `(userId: string | null) => void`
- `onClearFilter` (function): Callback when filter is cleared: `() => void`

**UI Elements**:
- Dropdown/Select control (ShadCN UI Select component) showing list of users
- "Clear filter" button or option
- Displays selected user name when filter is active

**Behavior**:
- Shows all users in dropdown (including users with 0 cards)
- Persists selection to localStorage on change
- Restores saved filter on mount

### WorkloadIndicator (app/components/board/WorkloadIndicator.tsx)

**Purpose**: Displays visual indicator (badge + color highlight) when user has more than 3 cards.

**Props**:
- `cardCount` (number): Number of cards assigned to user
- `userId` (string): User ID (for accessibility/aria-label)
- `show` (boolean): Whether indicator should be displayed (true when cardCount > 3)

**UI Elements**:
- ShadCN UI Badge component showing card count (e.g., "4 cards")
- Color highlight (Tailwind: `bg-orange-100 border-orange-300 text-orange-800`)
- Positioned next to user name

**Behavior**:
- Only displays when `show === true` (cardCount > 3)
- Updates immediately when cardCount changes
- Non-blocking (doesn't interrupt board interaction)

### UserStatusBadge (app/components/board/UserStatusBadge.tsx)

**Purpose**: Displays user status (OK/Busy) as a badge next to user name.

**Props**:
- `status` ("OK" | "Busy"): Current user status
- `userId` (string): User ID (for accessibility/aria-label)

**UI Elements**:
- ShadCN UI Badge component with status text ("OK" or "Busy")
- Color variants: Green for "OK", Orange/Red for "Busy"
- Positioned next to user name in filter control/board header

**Behavior**:
- Updates immediately when status changes
- Visible at a glance in filtered board context
- Accessible (proper ARIA labels)

## React Hooks Contract

### useUserFilter (lib/hooks/use-user-filter.ts)

**Purpose**: Provides filter state management and filtered cards.

**Returns**:
- `selectedUserId` (string | null): Currently selected user ID
- `setSelectedUserId` (function): Function to set filter: `(userId: string | null) => void`
- `clearFilter` (function): Function to clear filter: `() => void`
- `filteredCards` (Card[]): Memoized filtered cards array (only cards for selected user, or all cards if no filter)
- `isFilterActive` (boolean): Whether filter is currently active

**Dependencies**:
- `cards` (Card[]): All cards from board (passed as parameter or from context)
- Persists to localStorage automatically

### useUserWorkloads (lib/hooks/use-user-workloads.ts)

**Purpose**: Calculates and memoizes user workloads from cards array.

**Parameters**:
- `cards` (Card[]): Array of all cards

**Returns**:
- `workloads` (Map<string, UserWorkload>): Map of userId → UserWorkload
- `getUserWorkload` (function): Helper to get workload for specific user: `(userId: string) => UserWorkload | null`

**Behavior**:
- Recalculates only when cards array changes (memoized with useMemo)
- Returns Map for efficient O(1) lookup

## Data Structures (Internal)

### Card (types/card.ts)

```typescript
interface Card {
  id: string;
  assignedUserId: string | null; // Single user only
  title: string;
  columnId?: string;
  // ... other card properties from existing board feature
}
```

### User (types/user.ts)

```typescript
interface User {
  id: string;
  name: string;
  // status is computed, not stored
}
```

### UserWorkload (types/user.ts)

```typescript
interface UserWorkload {
  userId: string;
  cardCount: number;
  status: "OK" | "Busy";
  hasIndicator: boolean;
}
```

### FilterState (Internal to hook)

```typescript
interface FilterState {
  selectedUserId: string | null;
  filteredCards: Card[];
  isFilterActive: boolean;
}
```
