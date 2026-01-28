# Quickstart Guide: User Filtering and Workload Indicators

**Feature**: User Filtering and Workload Indicators  
**Date**: 2026-01-25  
**Purpose**: Get the filtering and workload indicator feature running quickly for testing and validation

## Prerequisites

- Next.js 14+ project initialized
- ShadCN UI installed and configured
- Tailwind CSS configured
- localStorage accessible (modern browser)
- Kanban board and cards exist (created by board feature)
- Users exist in the system (created by user management feature)
- Cards have `assignedUserId` property (single user assignment)

## Setup Steps

### 1. Install Dependencies

```bash
# ShadCN UI components (if not already installed)
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add select

# Ensure core dependencies are installed
npm install next react react-dom
npm install -D @types/node @types/react typescript
```

### 2. Set Up Project Structure

Create the following directories:

```
app/
├── components/
│   └── board/
│       ├── UserFilter.tsx
│       ├── WorkloadIndicator.tsx
│       └── UserStatusBadge.tsx
├── lib/
│   ├── services/
│   │   ├── filter-service.ts
│   │   └── workload-calculator.ts
│   └── hooks/
│       └── use-user-filter.ts
└── types/
    └── user.ts
```

### 3. Create Type Definitions

Create `app/types/user.ts`:

```typescript
export interface User {
  id: string;
  name: string;
}

export interface UserWorkload {
  userId: string;
  cardCount: number;
  status: "OK" | "Busy";
  hasIndicator: boolean;
}

export interface Card {
  id: string;
  assignedUserId: string | null;
  title: string;
  columnId?: string;
  // ... other card properties
}
```

### 4. Implement Core Services

#### Create `lib/services/filter-service.ts`

```typescript
import { Card } from '@/types/user';

export const getFilteredCards = (cards: Card[], userId: string | null): Card[] => {
  if (!userId) return cards;
  return cards.filter(card => card.assignedUserId === userId);
};

export const saveFilterToStorage = (userId: string | null): void => {
  if (typeof window === 'undefined') return;
  try {
    if (userId) {
      localStorage.setItem('user_filter', userId);
    } else {
      localStorage.removeItem('user_filter');
    }
  } catch (error) {
    console.error('Error saving filter to localStorage:', error);
  }
};

export const loadFilterFromStorage = (): string | null => {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem('user_filter') || null;
  } catch (error) {
    console.error('Error loading filter from localStorage:', error);
    return null;
  }
};
```

#### Create `lib/services/workload-calculator.ts`

```typescript
import { Card, UserWorkload } from '@/types/user';

export const calculateUserWorkloads = (cards: Card[]): Map<string, UserWorkload> => {
  const workloads = new Map<string, UserWorkload>();
  
  // Count cards per user
  const counts = new Map<string, number>();
  cards.forEach(card => {
    if (card.assignedUserId) {
      counts.set(card.assignedUserId, (counts.get(card.assignedUserId) || 0) + 1);
    }
  });
  
  // Create workload objects
  counts.forEach((cardCount, userId) => {
    workloads.set(userId, {
      userId,
      cardCount,
      status: cardCount <= 3 ? "OK" : "Busy",
      hasIndicator: cardCount > 3
    });
  });
  
  return workloads;
};

export const getUserStatus = (cardCount: number): "OK" | "Busy" => {
  return cardCount <= 3 ? "OK" : "Busy";
};
```

### 5. Create React Hook

Create `lib/hooks/use-user-filter.ts`:

```typescript
import { useState, useEffect, useMemo } from 'react';
import { Card } from '@/types/user';
import { getFilteredCards, saveFilterToStorage, loadFilterFromStorage } from '@/lib/services/filter-service';

export const useUserFilter = (cards: Card[]) => {
  const [selectedUserId, setSelectedUserIdState] = useState<string | null>(null);
  
  // Load saved filter on mount
  useEffect(() => {
    const saved = loadFilterFromStorage();
    if (saved) setSelectedUserIdState(saved);
  }, []);
  
  // Memoized filtered cards
  const filteredCards = useMemo(() => {
    return getFilteredCards(cards, selectedUserId);
  }, [cards, selectedUserId]);
  
  const setSelectedUserId = (userId: string | null) => {
    setSelectedUserIdState(userId);
    saveFilterToStorage(userId);
  };
  
  const clearFilter = () => {
    setSelectedUserId(null);
  };
  
  return {
    selectedUserId,
    setSelectedUserId,
    clearFilter,
    filteredCards,
    isFilterActive: selectedUserId !== null
  };
};
```

### 6. Create Components

#### Create `app/components/board/UserFilter.tsx`

```typescript
'use client';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { User } from '@/types/user';

interface UserFilterProps {
  users: User[];
  selectedUserId: string | null;
  onUserSelect: (userId: string | null) => void;
  onClearFilter: () => void;
}

export const UserFilter = ({ users, selectedUserId, onUserSelect, onClearFilter }: UserFilterProps) => {
  return (
    <div className="flex items-center gap-2">
      <Select value={selectedUserId || ''} onValueChange={(value) => onUserSelect(value || null)}>
        <SelectTrigger className="w-[200px]">
          <SelectValue placeholder="Filter by user..." />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">All users</SelectItem>
          {users.map(user => (
            <SelectItem key={user.id} value={user.id}>
              {user.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {selectedUserId && (
        <button onClick={onClearFilter} className="text-sm text-gray-500 hover:text-gray-700">
          Clear
        </button>
      )}
    </div>
  );
};
```

## Testing Scenarios

### Manual Test: User Story 1 - Filter Board by User

1. **Setup**: Ensure you have a Kanban board with multiple cards assigned to different users
2. **Test Filter Selection**:
   - Open the board
   - Select a user from the filter dropdown
   - **Verify**: Only cards assigned to that user are displayed (SC-004)
   - **Verify**: Cards assigned to other users are hidden (SC-005)
   - **Verify**: Filter completes within 2 seconds (SC-001)
3. **Test Filter Clear**:
   - Click "Clear filter" or select "All users"
   - **Verify**: All cards are displayed again
4. **Test Dynamic Updates**:
   - With filter active, assign a new card to the filtered user
   - **Verify**: New card appears in filtered view immediately
   - Reassign a card from filtered user to another user
   - **Verify**: Card disappears from filtered view immediately

### Manual Test: User Story 2 - Visual Workload Indicator

1. **Setup**: Create a user with 4 or more cards assigned
2. **Test Indicator Display**:
   - Filter board by the overloaded user
   - **Verify**: Workload indicator (badge with count + color highlight) appears (SC-002: within 1 second)
   - **Verify**: Badge shows card count (e.g., "4 cards")
   - **Verify**: Color highlight is visible (orange/red background)
3. **Test Indicator Removal**:
   - Reassign one card from the user (reducing to 3 cards)
   - **Verify**: Indicator disappears immediately
4. **Test Non-Blocking**:
   - With indicator displayed, interact with board (move cards, create cards)
   - **Verify**: Indicator remains visible but doesn't block interactions (FR-007)

### Manual Test: User Story 3 - User Status Change

1. **Setup**: Create a user with 3 or fewer cards
2. **Test Status Display**:
   - Filter board by the user
   - **Verify**: Status displays as "OK" next to user name
3. **Test Status Change to Busy**:
   - Assign a new card to the user (increasing to 4 cards)
   - **Verify**: Status changes to "Busy" immediately (SC-003: within 1 second)
   - **Verify**: Status is visible in filter control/board header (FR-012)
4. **Test Status Change to OK**:
   - Reassign one card from the user (reducing to 3 cards)
   - **Verify**: Status changes back to "OK" immediately
5. **Test Boundary Condition**:
   - User with exactly 3 cards should show "OK" status
   - User with exactly 4 cards should show "Busy" status

### Edge Case Testing

1. **User with 0 Cards**:
   - Filter by user with no cards assigned
   - **Verify**: User appears in filter dropdown
   - **Verify**: Status shows "OK" (0 ≤ 3)
   - **Verify**: No cards displayed (empty filtered view)
2. **Rapid Status Changes**:
   - Quickly assign and reassign cards
   - **Verify**: Status updates correctly without flickering
3. **Filter Persistence**:
   - Select a user filter
   - Refresh the page
   - **Verify**: Filter is restored from localStorage
4. **Multiple Users**:
   - Filter by different users
   - **Verify**: Each user's status and indicators are accurate
   - **Verify**: Workload calculations are correct for all users

## Validation Checklist

Use this checklist to validate the implementation:

- [ ] All functional requirements (FR-001 to FR-013) are implemented
- [ ] All user stories (US1, US2, US3) are fully functional
- [ ] All success criteria (SC-001 to SC-008) are met and measurable
- [ ] Filtering completes within 2 seconds (SC-001)
- [ ] Indicators appear within 1 second (SC-002)
- [ ] Status changes visible within 1 second (SC-003)
- [ ] 100% accuracy for filtered cards (SC-004, SC-005)
- [ ] Board remains responsive during filtering (SC-007)
- [ ] Indicators and status are 100% accurate (SC-008)
- [ ] Filter state persists in localStorage
- [ ] Workload calculation is efficient (no performance issues)
- [ ] Visual indicators are non-blocking (FR-007)
- [ ] Status display is prominent and visible at a glance (FR-012)
- [ ] Mobile responsiveness maintained (if applicable)

## Browser Console Testing

You can test the feature using browser console:

```javascript
// Test filter persistence
localStorage.setItem('user_filter', 'user-123');
console.log('Filter saved:', localStorage.getItem('user_filter'));

// Test card filtering (assuming cards exist in localStorage)
const cards = JSON.parse(localStorage.getItem('kanban_cards') || '[]');
const filtered = cards.filter(card => card.assignedUserId === 'user-123');
console.log('Filtered cards:', filtered);

// Test workload calculation
const counts = {};
cards.forEach(card => {
  if (card.assignedUserId) {
    counts[card.assignedUserId] = (counts[card.assignedUserId] || 0) + 1;
  }
});
console.log('User card counts:', counts);
```

## Next Steps

After validating the feature:

1. Run automated tests (if implemented)
2. Check accessibility (WCAG AA compliance)
3. Test on different browsers (Chrome, Firefox, Safari)
4. Verify performance with larger card sets (100+ cards)
5. Proceed to `/speckit.tasks` to generate implementation tasks
