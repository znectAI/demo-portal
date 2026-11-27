# UC-006 Detect cancelled and moved appointments

Status: Draft · Patterns: P2, P4

Requirements: R-RULE-10, R-AC-12

## Goal

The portal keeps its bookings in step with the owner's Google Calendar: when the owner deletes or moves a portal-created event there, the portal marks the appointment Cancelled and frees the slot.

## Actors

The system (scheduler). The change is triggered by the business owner deleting or moving the event in Google Calendar.

## Trigger

The portal's periodic check of the status of portal-created events in Google Calendar finds one deleted or moved.

## Preconditions

Appointments have been created in Google Calendar (UC-001) and their Google event ids are stored.

## Main flow

1. The portal periodically checks the status of the events it created in Google Calendar.
2. An event found deleted marks the appointment Cancelled and frees its slot.
3. A moved event cancels the original appointment and treats the new time as busy time.
4. A cancelled appointment gets no reminder (UC-002).

## Alternative and error flows

- **No change:** the appointment stays as it is; nothing is sent.

## Data

The appointment's Google Calendar event id and sync status, and its status (Booked → Cancelled).

## Rules

- **R-RULE-10** Cancellations and changes are phoned in. The owner deletes or moves the event in Google Calendar; the portal detects the deleted event within 15 minutes, marks the appointment Cancelled, frees the slot and does not send the reminder. Moved events are treated as cancellation plus busy time.

## Acceptance criteria

- **UC-006.AC1** Given a Booked appointment, when the owner deletes its event in Google Calendar, within 15 minutes the appointment is Cancelled and the slot is offered again; when the owner moves the event, the original appointment is Cancelled and the new time is treated as busy. ← R-AC-12

## Non-functional

Deletions are detected within 15 minutes (R-RULE-10). Detection timeliness is the design's concern (gate 2).

## Assumptions

None.