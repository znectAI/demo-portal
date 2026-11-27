# UC-003 Send daily booking update

Status: Draft · Patterns: P1, P3

Requirements: R-USE-15, R-USE-16, R-USE-17, R-USE-18, R-USE-19, R-USE-20, R-USE-21, R-ROLE-2, R-RULE-11, R-AC-20, R-AC-21, R-AC-22

## Goal

The business owner receives one email each day with the previous day's portal booking count, so he can check whether the daily target is being met.

## Actors

The system (scheduler); the recipient is the business owner.

## Trigger

Every day at 07:00 business local time.

## Preconditions

The portal has been launched and is recording bookings with their creation times.

## Main flow

1. Count appointments booked through the portal during the previous calendar day (00:00–23:59 local time).
2. Also show the 7-day average and the number of appointments scheduled for today.
3. Email the summary to the owner's address.

## Alternative and error flows

- **Zero bookings:** the email is still sent, showing 0.
- **Send fails:** it is retried 3 times within 1 hour, then logged as Failed, and the operator is alerted about the missed daily update.

## Data

The count of appointments created through the portal on the previous calendar day, the number cancelled, the 7-day average, and the number scheduled for today.

## Rules

- **R-RULE-11** The daily update counts appointments created through the portal on the previous calendar day (local time) regardless of the appointment date; cancelled ones are still counted, and the number cancelled is shown separately.

## Acceptance criteria

- **UC-003.AC1** Given 6 appointments were created through the portal yesterday and 1 of them has since been cancelled, when it is 07:00 local time, by 07:15 the owner receives one email showing 6 booked yesterday, 1 cancelled, the 7-day average, and the number of appointments scheduled for today. ← R-AC-20
- **UC-003.AC2** Given one booking created at 23:59 local time on Monday for an appointment next week, and one created at 00:01 on Tuesday, when Tuesday's update is sent, it counts 1 (the Monday booking), and Wednesday's update counts the 00:01 booking. ← R-AC-21
- **UC-003.AC3** Given no portal bookings yesterday, the email is still sent showing 0; given the email service fails, sending is retried 3 times within 1 hour, then logged as Failed, and the operator is alerted about the missed daily update. ← R-AC-22

## Non-functional

The daily update arrives by 07:15 local time (R-USE-18, R-USE-20). Delivery timings are the design's concern (gate 2).

## Assumptions

None.