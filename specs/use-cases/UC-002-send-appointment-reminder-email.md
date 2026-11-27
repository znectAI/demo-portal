# UC-002 Send appointment reminder email

Status: Draft · Patterns: P1, P3

Requirements: R-USE-8, R-USE-9, R-USE-10, R-USE-11, R-USE-12, R-USE-13, R-USE-14, R-ROLE-1, R-RULE-1, R-RULE-6, R-RULE-10, R-AC-15, R-AC-16, R-AC-17, R-AC-18, R-AC-19

## Goal

The customer receives exactly one reminder email at the time they chose, which reduces no-shows.

## Actors

The system (scheduler); the recipient is the customer.

## Trigger

The reminder time is reached: the appointment start minus the customer's chosen reminder time.

## Preconditions

The appointment is booked and has a reminder choice other than "no reminder". The reminder time has not already passed when the booking was made (UC-001).

## Main flow

1. The scheduler checks every minute for reminders due.
2. It checks the appointment is still Booked (not cancelled; see UC-006).
3. It sends a reminder email with date, time, business address and phone.
4. It records the reminder as sent so it is never sent twice.

## Alternative and error flows

- **No reminder chosen:** nothing is sent.
- **Reminder time already past at booking:** no reminder is sent; this is logged as Skipped.
- **Send fails:** it is retried every 2 minutes until the appointment start time, then marked Failed in the email log.
- **Scheduler restarts mid-send:** the customer still receives at most one reminder.

## Data

The reminder choice on the appointment, the reminder due time, and the email log entry (appointment reference, type, recipient, scheduled and sent time, status, attempts).

## Rules

- **R-RULE-1** The default reminder is 15 minutes before the appointment; the customer may choose a different time.
- **R-RULE-6** Reminder options are 15 minutes (default), 1 hour, 24 hours, or no reminder; a reminder time already past at booking is not sent.
- **R-RULE-10** A cancelled appointment does not get its reminder: when the portal detects the deletion in Google Calendar it marks the appointment Cancelled and does not send the reminder.

## Acceptance criteria

- **UC-002.AC1** Given an appointment at 10:00 with the default reminder, when the time reaches 09:45, exactly one reminder email is sent by 09:47, shows the date, time, business address and phone, and is logged as Sent. ← R-AC-15
- **UC-002.AC2** Given appointments with 1-hour, 24-hour and "no reminder" choices, when their reminder times arrive, reminders go out at start minus 1 hour and start minus 24 hours (each within 2 minutes), and none is sent for "no reminder". ← R-AC-16
- **UC-002.AC3** Given a booking made 3 hours before the appointment with a 24-hour reminder, when it is saved, no reminder is sent and the email log shows the reminder as Skipped. ← R-AC-17
- **UC-002.AC4** Given the owner deleted the appointment's Google event at least 15 minutes before the reminder time, when the reminder time arrives, no reminder is sent. ← R-AC-18
- **UC-002.AC5** Given the email service fails when the reminder is due, it is retried every 2 minutes until the appointment start, then logged as Failed; given the scheduler restarts while a reminder is being sent, the customer still receives at most one reminder. ← R-AC-19

## Non-functional

The customer is reminded at the chosen time, within 2 minutes (R-USE-14). Delivery timings and retry limits are the design's concern (gate 2).

## Assumptions

None.