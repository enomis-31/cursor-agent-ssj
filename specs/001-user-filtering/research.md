# Research: User Filtering and Workload Indicators

**Feature**: User Filtering and Workload Indicators  
**Date**: 2026-01-25  
**Phase**: 0 - Research & Technical Decisions

## Research Questions

### 1. User Filtering Implementation in Next.js/React

**Decision**: Use React state management with `useState` for filter selection, combined with `useMemo` for efficient card filtering

**Rationale**: 
- React `useState` provides simple, reactive state management for filter selection
- `useMemo` ensures filtering only recalculates when filter value or cards change (performance optimization)
- No need for complex state management libraries (Redux, Zustand) - violates simplicity principle
- Filter state can be persisted to localStorage for user preference

**Alternatives considered**:
- URL query parameters: More complex, requires Next.js router manipulation, not needed for simple filter
- Global state management (Redux/Zustand): Overkill for single filter value, violates simplicity
- Context API: Could work but adds complexity for simple filter state

**Implementation notes**:
- Use `useState` for current filter value (userId or null)
- Use `useMemo` to filter cards array: `cards.filter(card => card.assignedUserId === filterUserId)`
- Persist filter state to localStorage on change
- Restore filter state from localStorage on component mount

### 2. Workload Calculation (Card Counting per User)

**Decision**: Calculate card counts in-memory using `Array.reduce` or `Map` for efficient counting

**Rationale**:
- Simple in-memory calculation is fast for typical board sizes (dozens to hundreds of cards)
- No need for database queries or complex indexing (front-end only app)
- Can be memoized with `useMemo` to avoid recalculation on every render
- Aligns with simplicity principle - no over-engineering

**Alternatives considered**:
- IndexedDB with indexes: Overkill for simple counting, adds complexity
- Server-side calculation: Violates constitution (no backend)
- Web Workers: Unnecessary for simple counting operation

**Implementation notes**:
- Create `calculateUserWorkloads(cards: Card[]): Map<userId, count>` function
- Use `useMemo` to recalculate only when cards array changes
- Return Map for O(1) lookup of user card counts
- Threshold check: count > 3 triggers "Busy" status

### 3. Visual Indicator Implementation (Badge + Color Highlight)

**Decision**: Use ShadCN UI Badge component with Tailwind CSS color utilities for highlights

**Rationale**:
- ShadCN UI Badge provides accessible, styled badge component out of the box
- Tailwind CSS color utilities allow easy color highlighting (e.g., `bg-orange-100`, `text-orange-800`)
- Non-blocking: Badge is inline element, doesn't block board interface
- Can display card count text inside badge
- Aligns with existing tech stack (ShadCN UI + Tailwind)

**Alternatives considered**:
- Custom badge component: More work, ShadCN UI already provides this
- Toast/notification: Too intrusive, violates non-blocking requirement
- Modal/overlay: Blocks interface, violates FR-007

**Implementation notes**:
- Use ShadCN UI `<Badge>` component with variant for overload state
- Apply Tailwind color classes: `bg-orange-100 border-orange-300 text-orange-800` for "Busy" state
- Display card count: `{cardCount} cards` or `{cardCount}+` if >3
- Position badge next to user name in filter control/header

### 4. Status Display Implementation

**Decision**: Display status as text badge next to user name in filter control/board header

**Rationale**:
- Simple text display ("OK" or "Busy") is clear and unambiguous
- Positioned next to user name provides context (status is for that user)
- Can use same Badge component with different variant/color for status
- Visible at a glance without cluttering interface

**Alternatives considered**:
- Icon-only status: Less clear, requires tooltip (adds complexity)
- Separate status panel: Takes up space, not needed for simple status
- Color-only indicator: Less accessible, text is clearer

**Implementation notes**:
- Use ShadCN UI Badge with "OK" (green variant) or "Busy" (orange/red variant)
- Position in filter control next to selected user name
- Update immediately when card count crosses threshold (3 cards)

### 5. Real-Time Updates When Cards Change

**Decision**: Use React state synchronization - filter component subscribes to card changes via props/context

**Rationale**:
- React's reactive state ensures UI updates when card data changes
- If cards are managed in parent component or context, filter can receive updated cards array
- No need for event listeners or polling - React handles reactivity
- Simple and aligns with React patterns

**Alternatives considered**:
- Event emitters: More complex, React state is sufficient
- Polling: Wastes resources, React state is reactive
- WebSockets: Requires backend, violates constitution

**Implementation notes**:
- Filter component receives `cards` array as prop or from context
- When cards change (assigned/reassigned), parent updates cards array
- Filter component's `useMemo` recalculates filtered cards automatically
- Workload calculation `useMemo` also recalculates automatically
- Status and indicators update immediately via React re-render

### 6. Filter State Persistence

**Decision**: Use localStorage to persist selected user filter, restore on component mount

**Rationale**:
- localStorage is simple key-value storage, aligns with constitution (browser-local storage)
- Persists filter preference across page refreshes
- No complex state management needed
- Can be cleared/reset easily

**Alternatives considered**:
- Session storage: Doesn't persist across sessions, less useful
- URL query params: More complex, requires router manipulation
- No persistence: User loses filter preference on refresh

**Implementation notes**:
- Store filter value: `localStorage.setItem('user_filter', userId)`
- Restore on mount: `const savedFilter = localStorage.getItem('user_filter')`
- Clear filter: `localStorage.removeItem('user_filter')`
- Handle localStorage unavailability gracefully (private browsing mode)

### 7. Performance Optimization for Large Card Lists

**Decision**: Use React `useMemo` for filtering and workload calculation, avoid unnecessary re-renders

**Rationale**:
- `useMemo` prevents recalculation when dependencies haven't changed
- Filtering only recalculates when filter value or cards array changes
- Workload calculation only recalculates when cards array changes
- React's built-in optimization is sufficient for typical board sizes

**Alternatives considered**:
- Virtual scrolling: Overkill for typical board sizes (dozens to hundreds of cards)
- Web Workers: Unnecessary for simple filtering/counting
- Debouncing: Not needed, filtering is fast enough

**Implementation notes**:
- Memoize filtered cards: `const filteredCards = useMemo(() => cards.filter(...), [cards, filterUserId])`
- Memoize workload map: `const workloads = useMemo(() => calculateUserWorkloads(cards), [cards])`
- Ensure cards array reference stability (don't create new array on every render)

## Technical Decisions Summary

| Decision Area | Chosen Solution | Key Rationale |
|---------------|----------------|---------------|
| Filter State Management | React `useState` + `useMemo` | Simple, reactive, performant |
| Card Filtering | `Array.filter` with `useMemo` | Efficient, no unnecessary recalculations |
| Workload Calculation | In-memory `Map` with `useMemo` | Fast for typical board sizes, simple |
| Visual Indicator | ShadCN UI Badge + Tailwind colors | Non-blocking, accessible, matches stack |
| Status Display | Text badge next to user name | Clear, visible at a glance |
| Real-Time Updates | React state synchronization | Reactive, no polling needed |
| Filter Persistence | localStorage | Simple, aligns with constitution |
| Performance | `useMemo` optimization | Prevents unnecessary recalculations |

## Dependencies to Add

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@radix-ui/react-select": "^2.0.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0",
    "playwright": "^1.40.0"
  }
}
```

**Note**: ShadCN UI components (Badge, Select) should be installed via `npx shadcn-ui@latest add badge` and `npx shadcn-ui@latest add select` if not already present.

## Open Questions Resolved

- ✅ Filtering implementation: React useState + useMemo
- ✅ Workload calculation: In-memory Map with useMemo
- ✅ Visual indicator: ShadCN UI Badge + Tailwind colors
- ✅ Status display: Text badge next to user name
- ✅ Real-time updates: React state synchronization
- ✅ Filter persistence: localStorage
- ✅ Performance: useMemo optimization

All technical decisions align with constitution principles (Simplicity First, Component-Based Architecture) and user requirements.
