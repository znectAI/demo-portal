# Use cases

One file per end-to-end use case (`UC-nnn-<name>.md`), written by the znectAI architect from the
signed-off requirements and signed off by the business (gate 1). Each use case names the
requirement ids it covers; each acceptance criterion has a permanent id (`UC-nnn.ACn`) and at
least one test that names it.

| Id | Name | Actors | Goal |
|---|---|---|---|
| UC-001 | Book an appointment | Customer | Book one appointment and get a confirmation, instead of phoning |
| UC-002 | Send appointment reminder email | System → Customer | Send one reminder at the chosen time |
| UC-003 | Send daily booking update | System → Business owner | One daily email with the previous day's booking count |
| UC-004 | Connect Google Calendar and configure booking settings | Business owner | Connect the calendar and set slot length, time zone and business details |
| UC-005 | Maintain availability | Business owner | Control when customers may book via his Google Calendar |
| UC-006 | Detect cancelled and moved appointments | System | Keep bookings in step with calendar deletions and moves |

## Not in scope

From the requirements (signed off as out of scope for now):

- Online payment (R-SCOPE-4).
- Customer accounts (R-SCOPE-5).
- Cancelling or rescheduling appointments in the portal (R-SCOPE-6) — cancellations are phoned in.
- SMS or WhatsApp reminders; email only (R-SCOPE-9).
- Several staff members, rooms, or service types; one provider, one appointment type, one calendar (R-SCOPE-10).
- Two-way sync: appointments created directly in Google Calendar are not imported as bookings, they only block time (R-SCOPE-11).