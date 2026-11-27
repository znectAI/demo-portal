# UC-004 Connect Google Calendar and configure booking settings

Status: Draft · Patterns: P1, P2

Requirements: R-USE-22, R-USE-23, R-USE-24, R-USE-25, R-ROLE-2, R-RULE-2, R-RULE-9, R-AC-23, R-AC-28

## Goal

The business owner connects his Google Calendar once and sets the booking settings the portal needs, so that bookings appear in his calendar and the slot list is correct.

## Actors

Business owner (single administrator, logs in with email and password).

## Trigger

Initial setup before launch — or a change that needs the settings page, such as disconnecting and reconnecting Google.

## Preconditions

The owner has an account for the settings page and access to his Google account.

## Main flow

1. The owner logs in to the settings page with his email and password (plus a one-time authenticator code).
2. The owner connects his Google Calendar to the portal once, choosing the calendar the portal writes to (default: his primary calendar).
3. The owner sets the slot length (15, 30, 45 or 60 minutes).
4. The owner sets the business time zone (once).
5. The owner sets the business phone number and address shown in emails, and the notification address for the daily update and alerts.
6. The portal saves the settings and uses them for all new bookings.

Note: working hours and blocked dates are not part of these settings — they come from Google Calendar (see UC-005 and the requirements R-HEAD-8, R-SCOPE-7).

## Alternative and error flows

- **Failed login:** a wrong password or code is refused; after 5 failed attempts the account locks for 15 minutes; after 8 hours without activity the owner must log in again.
- **Google authorisation revoked or expired:** the owner receives an alert email and the settings page shows a "reconnect Google Calendar" banner; after reconnecting, pending events are created.

## Data

The availability settings: business time zone, slot length, business phone and address shown in emails, and the owner notification email. The Google connection itself (which calendar, OAuth grant).

## Rules

- **R-RULE-2** Slot length is one of 15, 30, 45 or 60 minutes, set in settings; it starts on the hour and half hour.
- **R-RULE-9** All times are shown to customers and the owner in the business's local time zone (set once in settings) and stored in UTC.

## Acceptance criteria

- **UC-004.AC1** Given the owner account, when the correct password and a valid authenticator code are entered, the settings page opens; given 5 failed attempts, the account locks for 15 minutes; given 8 hours without activity, the owner must log in again. ← R-AC-23
- **UC-004.AC2** Given the owner's Google authorisation is revoked, when the portal next calls Google, the owner receives an alert email and the settings page shows a "reconnect Google Calendar" banner; after reconnecting, pending events are created. ← R-AC-28
- **UC-004.AC3** Given the owner changes the slot length to one of 15, 30, 45 or 60 minutes and saves, newly offered slots use that length and start on the hour and half hour.
- **UC-004.AC4** Given the owner sets the business time zone once, all times are shown to customers and the owner in that zone, and stored in UTC.

## Non-functional

The owner settings page loads quickly and always reflects the current connection state. Performance targets are the design's concern (gate 2).

## Assumptions

- **Architect's assumption — what the settings page holds:** R-SCOPE-7 names the settings page only for "connecting the Google Calendar and setting the slot length", while R-DATA-2 and R-SRC-2 also list the time zone, business phone/address and notification email as settings. I have included these in the settings page because the reminders, confirmation and daily update (UC-001, UC-002, UC-003) need them; if the business intends them to be set elsewhere, those fields move to the design.