# Research: Calendar Event Notifications

**Feature**: Calendar Event Notifications  
**Date**: 2026-01-25  
**Phase**: 0 - Research & Technical Decisions

## Research Questions

### 1. Next.js Notification/Toast Patterns

**Decision**: Use ShadCN UI Toast component (Sonner or Radix UI Toast) for notification popups

**Rationale**: 
- ShadCN UI provides pre-built, accessible toast/notification components that integrate seamlessly with Tailwind CSS
- Sonner (toast library) is lightweight and provides excellent mobile support
- Radix UI Toast offers more customization but Sonner is simpler for MVP
- Both support dismiss functionality, positioning, and animations out of the box

**Alternatives considered**:
- Custom notification component: More control but violates simplicity principle
- React Hot Toast: Good alternative but ShadCN UI is already in tech stack
- Browser Notification API: Only works when app is closed (not our use case per FR-006)

**Implementation notes**:
- Use ShadCN UI's `sonner` package for toast notifications
- Configure toast position for mobile (bottom-center recommended for iPhone 15)
- Support multiple simultaneous toasts (FR-007 requirement)

### 2. Time-Based Event Monitoring in Next.js

**Decision**: Use React `useEffect` with `setInterval` for polling, combined with `useState` for event tracking

**Rationale**:
- Simple polling mechanism aligns with Simplicity First principle
- `setInterval` with 60-second intervals (FR-008: at least once per minute) is performant
- React hooks provide clean state management for tracked events
- Can use `useRef` to track which events have already triggered notifications to prevent duplicates

**Alternatives considered**:
- Web Workers: Overkill for simple polling, adds complexity
- Server-Sent Events: Requires backend (violates constitution - no backend)
- WebSocket: Requires backend and adds unnecessary complexity
- `requestAnimationFrame`: Too frequent, wastes resources

**Implementation notes**:
- Poll every 60 seconds (meets FR-008 minimum requirement)
- Use `Date.now()` for current time comparison
- Check if event time falls within ±5 second window (per clarification)
- Track notified events by ID to prevent duplicate notifications

### 3. Audio Playback in Web Browsers

**Decision**: Use HTML5 `Audio` API with preloaded sound files

**Rationale**:
- Native browser API, no external dependencies
- Simple to implement and control (play/pause/mute)
- Works across all modern browsers
- Can preload audio files for instant playback
- Supports user-initiated audio (required for autoplay policies)

**Alternatives considered**:
- Web Audio API: More complex, unnecessary for simple notification sounds
- Third-party audio libraries: Adds dependencies, violates simplicity
- Text-to-speech: Not suitable for notification sounds

**Implementation notes**:
- Store sound files in `public/sounds/` directory
- Use short, pleasant notification sound (< 2 seconds)
- Preload audio on app initialization
- Respect browser autoplay policies (sound only plays after user interaction)
- Provide mute toggle per notification (per clarification)

### 4. PWA Implementation with Next.js

**Decision**: Use `next-pwa` package for PWA capabilities

**Rationale**:
- `next-pwa` is the standard solution for Next.js PWA support
- Handles service worker generation, manifest creation, and offline support
- Well-maintained and compatible with Next.js App Router
- Supports iPhone/iOS PWA installation

**Alternatives considered**:
- Manual service worker setup: Too complex, violates simplicity
- Workbox directly: More control but requires more setup
- Other PWA libraries: Less Next.js-specific integration

**Implementation notes**:
- Configure `next-pwa` with appropriate caching strategies
- Create `manifest.json` with app metadata
- Ensure service worker doesn't interfere with notification polling
- Test PWA installation on iPhone 15 Safari

### 5. Mobile-Responsive Design for iPhone 15

**Decision**: Use Tailwind CSS responsive utilities with iPhone 15 dimensions (390x844px) as mobile breakpoint

**Rationale**:
- Tailwind CSS provides excellent mobile-first responsive design utilities
- iPhone 15 dimensions (390x844px) represent modern mobile standard
- ShadCN UI components are already mobile-responsive
- Tailwind's `sm:`, `md:`, `lg:` breakpoints work well for progressive enhancement

**Alternatives considered**:
- Custom CSS media queries: More verbose, Tailwind is already in stack
- CSS-in-JS solutions: Adds runtime overhead, Tailwind is compile-time
- Separate mobile stylesheet: Unnecessary complexity

**Implementation notes**:
- Design notification popups for mobile-first (390px width)
- Use Tailwind's `max-w-sm` or `max-w-md` for notification width
- Position notifications appropriately for mobile (avoid keyboard overlap)
- Test touch targets (minimum 44x44px for iOS)
- Ensure text is readable at mobile sizes (minimum 16px font size)

### 6. Event Storage and Retrieval

**Decision**: Use browser localStorage for event storage (simple JSON array)

**Rationale**:
- localStorage is the simplest storage mechanism for a front-end only test app
- No complex IndexedDB setup or async operations needed
- Sufficient for typical calendar event volumes (dozens to hundreds of events)
- Aligns with constitution requirement (localStorage or IndexedDB) and user preference for simplicity
- Synchronous API makes querying straightforward
- Perfect for test/development scenarios where complexity should be minimized

**Alternatives considered**:
- IndexedDB: More complex setup, async operations, unnecessary for test app scale
- In-memory only: Data lost on refresh (violates data persistence requirement)
- External database: Violates constitution (no backend)

**Implementation notes**:
- Store events as JSON array in localStorage under key `calendar_events`
- Structure: `[{ id, title, startTime, description? }, ...]`
- For time-based queries, parse JSON and filter array in memory
- Handle localStorage quota limits (typically 5-10MB, sufficient for test app)
- Simple error handling if localStorage is unavailable (private browsing mode)

### 7. Notification State Management

**Decision**: Use React Context API with `useReducer` for notification state

**Rationale**:
- React Context provides simple state management without external dependencies
- `useReducer` handles complex state updates (add, dismiss, show details) cleanly
- No need for Redux or Zustand (violates simplicity)
- State persists in component tree, accessible to all notification components

**Alternatives considered**:
- Redux: Overkill for simple notification state
- Zustand: Good but adds dependency, Context is sufficient
- Prop drilling: Not scalable, Context is better
- Global state library: Unnecessary complexity

**Implementation notes**:
- Create `NotificationContext` with provider
- Use reducer for actions: `ADD_NOTIFICATION`, `DISMISS_NOTIFICATION`, `SHOW_DETAILS`
- Track dismissed notifications to prevent re-showing
- Clear old notifications after reasonable time (e.g., 5 minutes)

## Technical Decisions Summary

| Decision Area | Chosen Solution | Key Rationale |
|---------------|----------------|---------------|
| Notification UI | ShadCN UI Sonner/Toast | Pre-built, accessible, mobile-friendly |
| Event Monitoring | React `useEffect` + `setInterval` | Simple polling, meets requirements |
| Audio Playback | HTML5 `Audio` API | Native, simple, no dependencies |
| PWA Support | `next-pwa` | Standard Next.js PWA solution |
| Mobile Design | Tailwind CSS responsive | Already in stack, mobile-first approach |
| Event Storage | localStorage | Simple, front-end only, sufficient for test app |
| State Management | React Context + useReducer | Simple, no external dependencies |

## Dependencies to Add

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@radix-ui/react-toast": "^1.1.0",
    "sonner": "^1.0.0",
    "tailwindcss": "^3.4.0",
    "date-fns": "^2.30.0",
    "next-pwa": "^5.6.0"
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

## Open Questions Resolved

- ✅ Notification component library: ShadCN UI Sonner
- ✅ Polling mechanism: React useEffect + setInterval
- ✅ Audio implementation: HTML5 Audio API
- ✅ PWA setup: next-pwa package
- ✅ Mobile responsiveness: Tailwind CSS with iPhone 15 breakpoints
- ✅ Data storage: localStorage for events (simple JSON array)
- ✅ State management: React Context + useReducer

All technical decisions align with constitution principles (Simplicity First, Component-Based Architecture) and user requirements.
