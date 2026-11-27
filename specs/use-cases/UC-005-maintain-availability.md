# UC-005 Maintain availability

Status: Draft · Patterns: P1, P4

Requirements: R-USE-22, R-USE-23, R-USE-24, R-USE-25, R-USE-26, R-USE-27, R-USE-28, R-ROLE-2, R-RULE-3, R-AC-24, R-AC-25, R-AC-26, R-AC-27

## Goal

The business owner controls when customers may book, so customers are only offered times the owner can really serve and there are no double bookings with his private or phone-booked appointments.

## Actors

Business owner (single administrator).

## Trigger

A change of working hours, a holiday or a day off.

## Preconditions

The owner has connected his Google Calendar (UC-004). The portal reads his calendar's busy times.

## Main flow

1. The owner marks the times he is unavailable (non-working time, breaks, days off) as busy events in his Google Calendar.
2. The portal reads the calendar and offers only the free slots.
3. Changes in Google Calendar show up in the portal's slots.

## Alternative and error flows

- **Invalid ranges:** an end time before the start time, or overlapping ranges or breaks, is rejected with a message.
- **Change removes hours that already have bookings:** the affected appointments are handled per the rules (see Assumptions) and the owner sees a list of them so he can phone those customers.

## Data

The owner's busy times in Google Calendar, the slot length, and the resulting free slots. The business has no separate working-hours or blocked-dates store of its own.

## Rules

- **R-RULE-3** A slot is offered only if it lies within the owner's working hours, is not on a blocked date, is not already booked in the portal, and does not overlap a busy event in Google Calendar.

## Acceptance criteria

- **UC-005.AC1** Given Monday hours 09:00–17:00, when the owner changes them to 09:00–12:00 with no break and saves, a newly loaded slot list shows Monday slots only up to 11:30, and the change is recorded in the audit trail with who changed it and when. ← R-AC-24
- **UC-005.AC2** Given a break 12:00–13:00 and blocked dates 24–26 December, when the owner saves, no slots are offered 12:00–12:59 on any working day, and no slots at all on 24–26 December. ← R-AC-25
- **UC-005.AC3** Given the settings page, when the owner enters an end time before the start time, or overlapping ranges or breaks, saving is refused with a message and the previous settings stay in force. ← R-AC-26
- **UC-005.AC4** Given 2 Booked appointments on Friday afternoon, when the owner blocks that Friday, both appointments are automatically set to Cancelled, their scheduled reminders are cancelled, a cancellation email is sent to each customer, and the owner sees a list of the 2 cancelled appointments with customer name, phone and email. ← R-AC-27

## Non-functional

Changes in Google Calendar show up in the portal's slots promptly. The timeliness of reading the calendar is the design's concern (gate 2).

## Assumptions

- **Architect's assumption — where availability is stored:** the requirements disagree. R-HEAD-8, R-SCOPE-7 and R-USE-25 ("the portal has no working hours or blocked dates settings") say availability comes only from Google Calendar, yet R-AC-24, R-AC-25 and R-AC-26 describe editing working hours, breaks and blocked dates on a settings page, and R-DATA-2 lists those as availability settings. I have kept both in this use case (the Google-Calendar flow above, and the settings-page acceptance criteria below) and flagged the contradiction for the business to resolve at gate 1.
- **Architect's assumption — effect on existing bookings:** R-USE-26 says a change that removes hours "keeps" the existing bookings and lists them for the owner to phone; R-AC-27 says the affected appointments are "automatically set to Cancelled" with a cancellation email sent. I have followed R-AC-27 (which is "stated · confirmed") in UC-005.AC4 and flagged the difference here for the business.