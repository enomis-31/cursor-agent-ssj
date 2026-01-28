# Data Model: Calendar Event Notifications

**Feature**: Calendar Event Notifications  
**Date**: 2026-01-25  
**Phase**: 1 - Design & Contracts

## Entities

### Calendar Event

Represents a scheduled appointment or meeting that can trigger notifications.

**Attributes**:
- `id` (string, required, unique): Unique identifier for the event. Generated when event is created. Used to distinguish events even if they share the same title and time.
- `title` (string, required): Event title/name displayed in notifications. Maximum length: 200 characters.
- `startTime` (Date/ISO string, required): Scheduled start time of the event. Stored as ISO 8601 string for serialization. Used to determine when notification should trigger.
- `description` (string, optional): Additional event details. Maximum length: 1000 characters. Displayed in event details view (User Story 3).
- `endTime` (Date/ISO string, optional): Scheduled end time. Not used for notifications (notifications trigger only at start time per spec).
- `createdAt` (Date/ISO string, optional): Timestamp when event was created. For audit/debugging purposes.
- `updatedAt` (Date/ISO string, optional): Timestamp when event was last modified. For audit/debugging purposes.

**Validation Rules**:
- `id` must be non-empty string
- `title` must be non-empty string, max 200 characters
- `startTime` must be valid date/time, cannot be in the past when creating (enforced by calendar feature, not this feature)
- `description` is optional but if provided, max 1000 characters

**Storage**:
- Stored in browser localStorage as JSON array under key `calendar_events`
- Events stored as array of objects: `[{ id, title, startTime, description?, ... }, ...]`
- Simple key-value storage, no complex indexing needed for test app

**Relationships**:
- None (events are independent entities)
- Notification system reads events but doesn't modify them (events managed by separate calendar feature)

### Notification State

Represents the current state of a displayed notification.

**Attributes**:
- `id` (string, required, unique): Unique identifier for this notification instance. Generated when notification is created.
- `eventId` (string, required): Reference to the Calendar Event that triggered this notification. Foreign key to Calendar Event.
- `eventTitle` (string, required): Cached event title for display (denormalized for performance).
- `eventStartTime` (Date/ISO string, required): Cached event start time for display.
- `triggeredAt` (Date/ISO string, required): Timestamp when notification was triggered. Used for ordering and cleanup.
- `isDismissed` (boolean, default: false): Whether user has dismissed this notification.
- `isSoundMuted` (boolean, default: false): Whether sound was muted for this notification (per-notification mute, not global).
- `isDetailsShown` (boolean, default: false): Whether event details view is currently displayed for this notification.

**Validation Rules**:
- `eventId` must reference a valid Calendar Event
- `triggeredAt` must be valid timestamp
- All boolean flags default to false

**Storage**:
- Stored in React state (NotificationContext)
- Not persisted to storage (notifications are ephemeral)
- Cleared when dismissed or after timeout (e.g., 5 minutes)

**Relationships**:
- `eventId` → Calendar Event (one notification per event trigger, but same event can trigger multiple notifications if time window allows)

### Notification Preferences (Future Enhancement)

**Note**: Not part of MVP per spec assumptions. Included here for future reference.

**Attributes**:
- `soundEnabled` (boolean, default: true): Global sound preference
- `notificationStyle` (string, enum: "popup" | "toast" | "banner", default: "popup"): Preferred notification display style

**Storage**: localStorage (simple key-value storage sufficient for preferences)

## Data Flow

### Notification Trigger Flow

1. **Event Monitoring**: `EventMonitor` service polls localStorage every 60 seconds
2. **Time Check**: For each event in localStorage array, check if `startTime` falls within ±5 seconds of current time
3. **Duplicate Prevention**: Check if notification already triggered for this event (by `eventId` + time window)
4. **Notification Creation**: Create `NotificationState` object with event data
5. **State Update**: Add notification to React Context state
6. **UI Display**: Notification component renders popup
7. **Audio Playback**: Play sound if not muted (default: play)

### Notification Dismissal Flow

1. **User Action**: User clicks dismiss button
2. **State Update**: Set `isDismissed: true` in notification state
3. **UI Removal**: Notification component removes popup from DOM
4. **State Cleanup**: Remove notification from React Context after animation completes

### Event Details View Flow

1. **User Action**: User clicks notification popup (not dismiss button)
2. **State Update**: Set `isDetailsShown: true`, `isDismissed: true` (notification popup dismissed)
3. **Data Fetch**: Retrieve full event data from localStorage array by `eventId`
4. **UI Display**: EventDetailsModal component displays event information
5. **Close Action**: User closes modal, return to main view

## localStorage Schema

### Storage Key: `calendar_events`

```typescript
// Stored as JSON string in localStorage
localStorage.setItem('calendar_events', JSON.stringify([
  { id: 'event-1', title: 'Meeting', startTime: '2026-01-25T14:30:00Z', ... },
  { id: 'event-2', title: 'Appointment', startTime: '2026-01-25T15:00:00Z', ... },
  // ... more events
]));
```

### Query Patterns

- **Get all events**: Parse JSON from localStorage
  ```typescript
  const events = JSON.parse(localStorage.getItem('calendar_events') || '[]');
  ```

- **Time-based filter**: Filter events where `startTime` is within time window
  ```typescript
  const now = Date.now();
  const windowStart = now - 5000;
  const windowEnd = now + 5000;
  const matchingEvents = events.filter(event => {
    const eventTime = new Date(event.startTime).getTime();
    return eventTime >= windowStart && eventTime <= windowEnd;
  });
  ```

- **Single event lookup**: Find event by `id` in array
  ```typescript
  const event = events.find(e => e.id === eventId);
  ```

## State Management

### NotificationContext Structure

```typescript
interface NotificationState {
  notifications: NotificationState[];
  addNotification: (event: CalendarEvent) => void;
  dismissNotification: (notificationId: string) => void;
  showEventDetails: (notificationId: string) => void;
  clearOldNotifications: () => void;
}
```

### Reducer Actions

- `ADD_NOTIFICATION`: Add new notification to state
- `DISMISS_NOTIFICATION`: Mark notification as dismissed, remove from UI
- `SHOW_EVENT_DETAILS`: Open event details modal for notification
- `CLEAR_OLD_NOTIFICATIONS`: Remove notifications older than 5 minutes

## Data Migration & Compatibility

**Current Version**: 1.0.0

**Future Considerations**:
- If event schema changes, localStorage data structure may need migration (simple version check + data transformation)
- Notification state is ephemeral, no migration needed
- Event data is managed by calendar feature, this feature only reads
- localStorage has ~5-10MB limit per domain, sufficient for test app but may need IndexedDB if scaling to thousands of events

## Performance Considerations

- localStorage access is synchronous and fast for small datasets (typical calendar: dozens to hundreds of events)
- For time-based filtering, iterate through events array and filter in memory (acceptable for test app scale)
- Notification state kept in memory (React Context) for fast UI updates
- Old notifications auto-cleared to prevent memory leaks
- Event data cached in notification state to avoid repeated localStorage reads
- Note: For production apps with thousands of events, IndexedDB would be better, but localStorage is sufficient for this test application
