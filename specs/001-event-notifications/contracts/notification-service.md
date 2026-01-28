# Notification Service Contract

**Feature**: Calendar Event Notifications  
**Date**: 2026-01-25  
**Type**: Service Interface Contract

## Service: EventMonitor

Monitors calendar events and triggers notifications when event times arrive.

### Methods

#### `startMonitoring(): void`

Starts the event monitoring process. Begins polling IndexedDB for events every 60 seconds.

**Preconditions**:
- localStorage is accessible
- Calendar events exist in localStorage (stored as JSON array)

**Postconditions**:
- Polling interval is active
- Events are checked every 60 seconds

**Side Effects**:
- Sets up `setInterval` for polling
- May trigger notifications when events are detected

**Error Handling**:
- If localStorage access fails (e.g., private browsing), log error and retry after delay
- If JSON parsing fails, log error and continue with next interval
- If polling fails, continue with next interval

---

#### `stopMonitoring(): void`

Stops the event monitoring process. Clears the polling interval.

**Preconditions**:
- Monitoring is currently active

**Postconditions**:
- Polling interval is cleared
- No further event checks occur

**Side Effects**:
- Removes interval timer
- Stops notification triggering

---

#### `checkEventsForNotifications(): Promise<void>`

Checks all calendar events and triggers notifications for events whose start time falls within ±5 seconds of current time.

**Preconditions**:
- localStorage is accessible
- Current system time is available

**Postconditions**:
- All events within time window have notifications triggered
- No duplicate notifications for same event within same time window

**Algorithm**:
1. Get current time: `const now = Date.now()`
2. Calculate time window: `[now - 5000, now + 5000]`
3. Retrieve events from localStorage: `JSON.parse(localStorage.getItem('calendar_events') || '[]')`
4. Filter events where `startTime` falls within time window
5. For each matching event:
   - Check if notification already triggered (by eventId + time window)
   - If not, create and dispatch notification
   - Mark event as notified for this time window

**Error Handling**:
- If localStorage access fails, log error and return (don't throw)
- If JSON parsing fails, log error and return (don't throw)
- If notification creation fails, log error and continue with next event

---

## Service: NotificationService

Manages notification display, dismissal, and audio playback.

### Methods

#### `triggerNotification(event: CalendarEvent): NotificationState`

Creates and displays a notification for the given event.

**Parameters**:
- `event` (CalendarEvent): The event that triggered the notification

**Returns**: `NotificationState` object representing the created notification

**Preconditions**:
- Event has valid `id`, `title`, and `startTime`
- App is open and browser tab is active (enforced by caller)

**Postconditions**:
- Notification popup is displayed
- Sound plays (unless muted)
- Notification state is added to React Context

**Side Effects**:
- Updates React Context with new notification
- Plays audio file (if enabled)
- Renders notification UI component

**Error Handling**:
- If event data is invalid, log error and return null
- If audio playback fails, continue without sound (notification still displays)

---

#### `dismissNotification(notificationId: string): void`

Dismisses and removes a notification from the UI.

**Parameters**:
- `notificationId` (string): ID of notification to dismiss

**Preconditions**:
- Notification exists in state
- Notification ID is valid

**Postconditions**:
- Notification is marked as dismissed
- Notification popup is removed from UI
- Notification state is updated in React Context

**Side Effects**:
- Updates React Context state
- Triggers UI animation for dismissal
- Removes notification from DOM after animation

**Error Handling**:
- If notification not found, log warning and return (idempotent)

---

#### `showEventDetails(notificationId: string): Promise<void>`

Displays event details modal for the given notification.

**Parameters**:
- `notificationId` (string): ID of notification to show details for

**Preconditions**:
- Notification exists in state
- Associated event exists in localStorage

**Postconditions**:
- Notification popup is dismissed
- Event details modal is displayed
- Full event data is loaded and shown

**Side Effects**:
- Dismisses notification popup
- Opens event details modal
- Retrieves event data from localStorage array

**Error Handling**:
- If notification not found, log error and return
- If event not found in localStorage, show error message in modal
- If localStorage access fails, display error state in modal

---

#### `playNotificationSound(): Promise<void>`

Plays the notification sound audio file.

**Preconditions**:
- Audio file exists in `public/sounds/`
- Browser supports HTML5 Audio API
- User has interacted with page (for autoplay policy)

**Postconditions**:
- Sound file plays to completion or until stopped

**Side Effects**:
- Creates Audio object and plays sound
- May require user interaction first (browser autoplay policy)

**Error Handling**:
- If audio file not found, log warning and continue silently
- If autoplay blocked, log info (expected behavior)
- If audio API unavailable, continue without sound

---

#### `muteNotificationSound(notificationId: string): void`

Mutes the sound for a specific notification.

**Parameters**:
- `notificationId` (string): ID of notification to mute

**Preconditions**:
- Notification exists in state
- Sound is currently playing or about to play

**Postconditions**:
- Notification's `isSoundMuted` flag is set to true
- Sound playback is stopped if currently playing

**Side Effects**:
- Updates notification state
- Stops audio playback if active

---

## Service: StorageService

Handles IndexedDB operations for calendar events.

### Methods

#### `getEventsInTimeWindow(startTime: Date, endTime: Date): Promise<CalendarEvent[]>`

Queries IndexedDB for events whose start time falls within the specified time window.

**Parameters**:
- `startTime` (Date): Start of time window
- `endTime` (Date): End of time window

**Returns**: Array of CalendarEvent objects within the time window

**Preconditions**:
- localStorage is accessible
- Time window is valid (startTime < endTime)

**Postconditions**:
- All events within window are returned
- Results are sorted by startTime

**Error Handling**:
- If localStorage access fails, return empty array and log error
- If JSON parsing fails, return empty array and log error
- If filtering fails, return empty array and log error

---

#### `getEventById(eventId: string): Promise<CalendarEvent | null>`

Retrieves a single event by its unique ID.

**Parameters**:
- `eventId` (string): Unique event identifier

**Returns**: CalendarEvent object or null if not found

**Preconditions**:
- localStorage is accessible
- Event ID is valid string

**Postconditions**:
- Event is returned if exists, null otherwise

**Error Handling**:
- If localStorage access fails, return null and log error
- If JSON parsing fails, return null and log error
- If event not found, return null (not an error)

---

## Component Contracts

### NotificationPopup Component

**Props**:
```typescript
interface NotificationPopupProps {
  notification: NotificationState;
  onDismiss: (id: string) => void;
  onShowDetails: (id: string) => void;
  onMuteSound: (id: string) => void;
}
```

**Behavior**:
- Displays event title and start time
- Shows dismiss button
- Plays sound on mount (if not muted)
- Handles click to show details
- Animates in/out transitions

**Accessibility**:
- ARIA role="alert" for screen readers
- Keyboard navigation support (Enter to show details, Escape to dismiss)
- Focus management when displayed

---

### EventDetailsModal Component

**Props**:
```typescript
interface EventDetailsModalProps {
  event: CalendarEvent;
  isOpen: boolean;
  onClose: () => void;
}
```

**Behavior**:
- Displays full event information (title, time, description)
- Provides close button
- Handles backdrop click to close
- Manages focus trap when open

**Accessibility**:
- ARIA modal attributes
- Focus trap
- Escape key to close
- Screen reader announcements

---

## React Hooks Contract

### `useNotifications(): NotificationContextValue`

Custom hook to access notification state and actions.

**Returns**:
```typescript
{
  notifications: NotificationState[];
  addNotification: (event: CalendarEvent) => void;
  dismissNotification: (id: string) => void;
  showEventDetails: (id: string) => void;
  clearOldNotifications: () => void;
}
```

**Usage**:
- Must be used within NotificationProvider
- Provides reactive access to notification state
- Actions update state and trigger UI updates

---

## Error Contract

All services should follow consistent error handling:

- **Logging**: Use console.error for unexpected errors, console.warn for recoverable issues
- **User Feedback**: Display user-friendly error messages in UI when appropriate
- **Graceful Degradation**: Continue operation when possible (e.g., notification without sound if audio fails)
- **No Throwing**: Services should not throw errors that crash the app (catch and log instead)
