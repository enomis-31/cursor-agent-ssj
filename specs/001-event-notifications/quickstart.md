# Quickstart Guide: Calendar Event Notifications

**Feature**: Calendar Event Notifications  
**Date**: 2026-01-25  
**Purpose**: Get the notification feature running quickly for testing and validation

## Prerequisites

- Next.js 14+ project initialized
- ShadCN UI installed and configured
- Tailwind CSS configured
- localStorage accessible (modern browser)
- Calendar events exist in localStorage (created by calendar feature, stored as JSON array under key `calendar_events`)

## Setup Steps

### 1. Install Dependencies

```bash
npm install sonner date-fns next-pwa
npm install -D @types/node @types/react typescript
```

### 2. Configure PWA (next-pwa)

Create or update `next.config.js`:

```javascript
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development'
});

module.exports = withPWA({
  // Your existing Next.js config
});
```

### 3. Create Notification Sound File

Place a notification sound file at `public/sounds/notification.mp3` (or `.wav`, `.ogg`).

**Recommendation**: Use a short, pleasant sound (< 2 seconds). Free options available at freesound.org.

### 4. Set Up Project Structure

Create the following directories:
```
app/
├── components/
│   └── notifications/
├── lib/
│   ├── services/
│   └── hooks/
└── types/
```

### 5. Implement Core Services

#### Create `lib/services/event-monitor.ts`

```typescript
// Basic structure - full implementation in tasks
export class EventMonitor {
  private intervalId: NodeJS.Timeout | null = null;
  
  startMonitoring() {
    // Poll every 60 seconds
    // Check events in ±5 second window
    // Trigger notifications
  }
  
  stopMonitoring() {
    // Clear interval
  }
}
```

#### Create `lib/services/notification-service.ts`

```typescript
// Basic structure - full implementation in tasks
export class NotificationService {
  triggerNotification(event: CalendarEvent) {
    // Create notification state
    // Play sound
    // Update React Context
  }
  
  dismissNotification(id: string) {
    // Update state
    // Remove from UI
  }
}
```

### 6. Create React Context

#### Create `lib/hooks/use-notifications.ts`

```typescript
// NotificationContext setup
// Provider component
// useNotifications hook
```

### 7. Create UI Components

#### Create `app/components/notifications/NotificationPopup.tsx`

```typescript
// ShadCN UI Toast/Sonner integration
// Display event title and time
// Dismiss button
// Click handler for details
```

#### Create `app/components/notifications/EventDetailsModal.tsx`

```typescript
// ShadCN UI Dialog/Modal
// Display full event information
// Close button
```

### 8. Integrate into App Layout

Add NotificationProvider to root layout:

```typescript
// app/layout.tsx
import { NotificationProvider } from '@/lib/hooks/use-notifications';

export default function RootLayout({ children }) {
  return (
    <NotificationProvider>
      {children}
      <NotificationContainer />
    </NotificationProvider>
  );
}
```

### 9. Start Event Monitoring

Initialize EventMonitor in a client component:

```typescript
'use client';
import { useEffect } from 'react';
import { EventMonitor } from '@/lib/services/event-monitor';

export function NotificationManager() {
  useEffect(() => {
    const monitor = new EventMonitor();
    monitor.startMonitoring();
    
    return () => {
      monitor.stopMonitoring();
    };
  }, []);
  
  return null;
}
```

## Testing the Feature

### Manual Test: Basic Notification

1. **Create a test event** in localStorage with start time 1 minute in the future
   ```javascript
   const events = [{ id: 'test-1', title: 'Test Event', startTime: new Date(Date.now() + 60000).toISOString() }];
   localStorage.setItem('calendar_events', JSON.stringify(events));
   ```
2. **Open the app** and wait for notification
3. **Verify**:
   - Notification popup appears within 5 seconds of event time
   - Event title and time are visible
   - Sound plays (if enabled)
   - Notification can be dismissed

### Manual Test: Multiple Events

1. **Create 3 events** with start times 1, 2, and 3 minutes in the future
2. **Open the app** and wait
3. **Verify**:
   - Each event triggers a notification at its respective time
   - Multiple notifications can be displayed simultaneously
   - Each notification can be dismissed independently

### Manual Test: Event Details

1. **Trigger a notification** (as above)
2. **Click on the notification popup** (not dismiss button)
3. **Verify**:
   - Notification popup is dismissed
   - Event details modal opens
   - Full event information is displayed
   - Modal can be closed

### Automated Test: Unit Tests

```typescript
// tests/unit/services/event-monitor.test.ts
describe('EventMonitor', () => {
  it('should trigger notification when event time arrives', async () => {
    // Test implementation
  });
  
  it('should not trigger duplicate notifications', async () => {
    // Test implementation
  });
});
```

### Automated Test: Integration Tests

```typescript
// tests/integration/notifications.test.tsx
describe('Notification Flow', () => {
  it('should display notification when event time matches', async () => {
    // Test implementation with React Testing Library
  });
  
  it('should dismiss notification on button click', async () => {
    // Test implementation
  });
});
```

## Common Issues & Solutions

### Issue: Notifications not appearing

**Check**:
- EventMonitor is started (check console logs)
- Events exist in localStorage with valid startTime (check `localStorage.getItem('calendar_events')`)
- Current time is within ±5 seconds of event time
- Browser tab is active (FR-006 requirement)
- localStorage is accessible (not in private browsing mode)

### Issue: Sound not playing

**Check**:
- Audio file exists at `public/sounds/notification.mp3`
- Browser autoplay policy (may require user interaction first)
- Sound is not muted
- Audio API is supported by browser

### Issue: Multiple notifications for same event

**Check**:
- Duplicate prevention logic is working
- Event IDs are unique
- Time window calculation is correct

### Issue: PWA not installing on iPhone

**Check**:
- `manifest.json` is properly configured
- Service worker is registered
- App is served over HTTPS (or localhost)
- Safari on iOS supports PWA installation

## Next Steps

After quickstart validation:
1. Implement full service logic (see tasks.md)
2. Add comprehensive error handling
3. Implement accessibility features
4. Add unit and integration tests
5. Optimize for mobile performance
6. Test on actual iPhone 15 device

## Validation Checklist

- [ ] Notification appears when event time arrives
- [ ] Sound plays (if enabled)
- [ ] Notification can be dismissed
- [ ] Event details modal opens on click
- [ ] Multiple notifications work simultaneously
- [ ] No duplicate notifications for same event
- [ ] Works on mobile (iPhone 15 Safari)
- [ ] PWA can be installed
- [ ] App remains responsive during notifications
