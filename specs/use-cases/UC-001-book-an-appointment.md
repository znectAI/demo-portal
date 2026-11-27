# UC-001 Book an appointment

Status: Draft · Patterns: P1, P2, P3

Requirements: R-USE-1, R-USE-2, R-USE-3, R-USE-4, R-USE-5, R-USE-6, R-USE-7, R-ROLE-1, R-RULE-1, R-RULE-2, R-RULE-3, R-RULE-4, R-RULE-5, R-RULE-6, R-RULE-7, R-RULE-8, R-RULE-9, R-AC-1, R-AC-2, R-AC-3, R-AC-4, R-AC-5, R-AC-6, R-AC-7, R-AC-8, R-AC-9, R-AC-10, R-AC-11, R-AC-13, R-AC-14

## Goal

A customer books one appointment themselves through the portal — choose a free slot, enter their details, and get a confirmation — instead of phoning.

## Actors

Customer (anonymous, no account).

## Trigger

The customer opens the portal link (from the business website, Google listing or a shared link) wanting an appointment.

## Preconditions

The owner has connected his Google Calendar and set the slot length and the business time zone (UC-004). The portal is reading the owner's busy times.

## Main flow

1. The portal shows free slots for the next 30 days, grouped by day, in the business's local time.
2. The customer picks a slot.
3. The customer enters name and email (required), plus phone and a note of up to 500 characters (both optional per R-USE-4; see Assumptions), and a reminder time (default 15 minutes before).
4. The customer reviews the summary and presses Confirm.
5. The system re-checks that the slot is still free, both in the portal and as busy time in Google Calendar, then saves the appointment as Booked.
6. A confirmation screen shows date, time and a "to cancel or change, please call" note with the business phone number.
7. A confirmation email is sent within 1 minute.
8. An event is created in the owner's Google Calendar with the customer's name, email, phone and note.

## Alternative and error flows

- **No free slots in the window:** the portal says so and shows the business phone number.
- **Slot taken in the meantime:** the customer sees "This time was just booked, please pick another"; the slot list refreshes and the entered details are kept.
- **Invalid details:** a missing or invalid name or email gives a field-level message and nothing is saved; a note longer than 500 characters does the same.
- **Limit reached (R-RULE-8):** the customer is asked to phone the business.
- **Google Calendar unreachable:** the booking stays confirmed, the event is retried for up to 24 hours, and the owner gets an alert email after 1 hour of failures.
- **Confirmation email fails:** it is retried for up to 24 hours and the failure is logged, without affecting the saved booking.

## Data

The appointment (reference number, start and end, status, customer name, email, phone, note, reminder choice, created time), the slot, and the owner's free/busy times read from Google Calendar. No payment data and no customer account.

## Rules

- **R-RULE-1** The default reminder email is sent 15 minutes before the appointment; the customer may choose a different reminder time.
- **R-RULE-2** Appointments have one fixed length (30 minutes unless the owner changes it to 15, 30, 45 or 60); slots start on the hour and half hour and must fit entirely within free time in Google Calendar.
- **R-RULE-3** A slot is offered only if it lies within the owner's working hours, is not on a blocked date, is not already booked in the portal, and does not overlap a busy event in Google Calendar.
- **R-RULE-4** The earliest bookable slot starts at least 2 hours from now; the latest is 30 days ahead.
- **R-RULE-5** Each slot holds exactly one appointment; of two customers confirming the same slot, the first saved wins and the second gets the "just booked" message.
- **R-RULE-6** The customer may choose 15 minutes before (default), 1 hour before, 24 hours before, or no reminder; a reminder time already past at booking is not sent.
- **R-RULE-7** Customer details per booking: name (2–100 characters), a valid email and a phone number are all required; a note (up to 500 characters) is optional; no account or password.
- **R-RULE-8** At most 2 upcoming appointments per email address at the same time.
- **R-RULE-9** Times are shown to customers in the business's local time and stored in UTC.

## Acceptance criteria

- **UC-001.AC1** Given working hours Mon–Fri 09:00–17:00, slot length 30 minutes and no bookings, when a customer opens the portal on Monday at 08:00 local time, the first slot offered is Monday 10:00; slots start on the hour and half hour, are grouped by day in the business's local time, and run up to 30 days ahead. ← R-AC-1
- **UC-001.AC2** Given a free slot, when the customer enters a valid name and email, keeps the default reminder and presses Confirm, the appointment is saved as Booked with a unique reference number, the slot is no longer offered to anyone, the confirmation screen shows the date, time, reference and the "to cancel or change, please call" note with the business phone, and a confirmation email with an .ics attachment reaches the customer within 1 minute. ← R-AC-2
- **UC-001.AC3** Given a booking has just been confirmed, within 5 minutes the owner's chosen calendar has one event titled "Appointment: <customer name>" with the booked start and end, and a description holding the reference, email, phone, note and reminder choice; the appointment's sync status is Synced and its Google event id is stored. ← R-AC-3
- **UC-001.AC4** Given the owner has a busy event in Google Calendar on Tuesday 14:00–15:00, when a customer views Tuesday, the 14:00 and 14:30 slots are not offered; given an event marked "free" covers the same period, those slots are offered. ← R-AC-4
- **UC-001.AC5** Given two customers have both chosen Wednesday 11:00, when both press Confirm within the same second, exactly one appointment is saved as Booked; the other sees "This time was just booked, please pick another", the slot list refreshes without 11:00, and that customer's entered details are kept. ← R-AC-5
- **UC-001.AC6** Given the booking form, when the name is missing, shorter than 2 or longer than 100 characters, or the email is invalid, or the note is longer than 500 characters, a message appears at the field concerned and nothing is saved, emailed or sent to Google. ← R-AC-6
- **UC-001.AC7** Given an email address already has 2 upcoming Booked appointments, a third booking with that email is refused with a message asking the customer to phone the business; given one of the two is cancelled or has already taken place, a new booking is allowed. ← R-AC-7
- **UC-001.AC8** Given Google Calendar returns errors, when a customer books, the booking is still confirmed with screen and email, and sync status is Pending; retries run at 1, 2, 4 … minutes, capped at 30; the owner gets an alert email after 1 hour of failures; when Google recovers exactly one event is created (no duplicates); if it is still failing after 24 hours the status becomes Failed and the owner gets a second alert. ← R-AC-8
- **UC-001.AC9** Given the Google free/busy check at Confirm takes longer than 3 seconds, when the customer confirms, the busy data cached in the last 5 minutes is used and Confirm responds within 2 seconds at the 95th percentile. ← R-AC-9
- **UC-001.AC10** Given the time is 10:00, when the customer views slots, 12:00 is offered and 11:30 is not; the last day offered is today plus 30 days, and day 31 is not offered; blocked dates show no slots. ← R-AC-10
- **UC-001.AC11** Given no free slot exists in the next 30 days, when a customer opens the portal, a message says no times are available and shows the business phone number. ← R-AC-11
- **UC-001.AC12** Given 10 booking attempts from one IP address in the last hour, an 11th attempt is refused with a "too many attempts, please try later or call" message, and a failed CAPTCHA also blocks Confirm. ← R-AC-13
- **UC-001.AC13** Given a booking for 10:00 local time on the day after the clocks change, when it is saved, it is stored in UTC with the correct offset, and the confirmation email, the Google event and the reminder all use 10:00 local time. ← R-AC-14
- **UC-001.AC14** Given the confirmation email fails to send, when a booking has been confirmed, the email is retried for up to 24 hours and each failure is logged, without affecting the saved booking.

## Non-functional

The customer books in under 2 minutes without phoning, and the owner sees the appointment in Google Calendar within 5 minutes of booking (R-USE-7). Availability, performance and capacity targets are the design's concern (gate 2).

## Assumptions

- **Architect's assumption — phone required or optional:** R-USE-4 (step 3) calls the phone number optional, while R-RULE-7 and R-DATA-1 (both "stated") call it required, and R-AC-2/R-AC-6 do not test the phone. I have recorded both as written and left them for the business to reconcile at gate 1: if phone is optional, R-RULE-7 and R-DATA-1 need amending; if required, R-USE-4 does.