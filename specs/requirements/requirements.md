# Requirements — Appointment booking

Sign-off record:
- overview playback: Ravi (business owner), 2026-11-24 19:37 UTC
- final sign-off: Ravi (business owner), 2026-11-24 19:56 UTC

Each item shows where it came from: *stated* by a person, *inferred* from what was stated, *assumed* by znectAI as a sensible default, or a *platform default* (a znectAI standard). Assumed items nobody confirmed are listed at the end. You can edit this file directly: keep each item's id (R-RULE-2 and so on), delete a line to remove an item, and add a line without an id for a new item.

## Overview

### Goal, success measures, current state

- **R-GOAL-1** *current state:* Today customers phone the business owner, who sets up their appointments manually in his calendar. _[stated · confirmed by Ravi]_
- **R-GOAL-2** *goal:* Customers book appointments themselves through an online portal instead of phoning. _[stated · confirmed by Ravi]_
- **R-GOAL-3** *success measure:* Success target: at least 5 appointments booked through the portal per day within 2 months of launch. Ravi chose option A. Ravi will track it through the daily update with the number of appointments booked. _[stated · confirmed by Ravi]_

### Users, main capabilities, systems

- **R-HEAD-1** *users:* End customers are the users of the portal. _[stated · confirmed by Ravi]_
- **R-HEAD-2** *capabilities:* Customers open the portal and choose from available timeslots to book an appointment. _[stated · confirmed by Ravi]_
- **R-HEAD-3** *capabilities:* Customers receive a confirmation email when an appointment is booked. _[stated · confirmed by Ravi]_
- **R-HEAD-4** *capabilities:* Customers receive a reminder email based on their preference; the default is 15 minutes before the appointment. _[stated · confirmed by Ravi]_
- **R-HEAD-5** *capabilities:* The business owner receives a daily update with the number of appointments booked through the portal. _[stated · confirmed by Ravi]_
- **R-HEAD-6** *systems:* The business owner's calendar today is Google Calendar. Appointments booked through the portal should appear in it automatically, so he only has to look in one place. _[stated · confirmed by Ravi]_
- **R-HEAD-7** *users:* The business owner (Ravi) is also a user. He receives the daily booking update, sees portal bookings in his Google Calendar and maintains his bookable working hours. _[inferred · confirmed by Ravi]_
- **R-HEAD-8** *capabilities:* The business owner controls when customers may book through his Google Calendar. The portal offers only times that are free in that calendar. There are no separate working hours in the portal. _[stated · confirmed by Ravi]_
- **R-HEAD-9** *systems:* A transactional email service sends the confirmation, reminder and daily update emails. _[inferred · high impact · confirmed by Ravi]_

### Scope, priorities, budget, deadline

- **R-SCOPE-1** *in scope:* Automatic creation of portal bookings in the business owner's Google Calendar is in scope. _[stated · confirmed by Ravi]_
- **R-SCOPE-2** *priority:* First priority: booking timeslots, confirmation email, and appointments appearing automatically in Google Calendar. Ravi agreed to this ordering with "ok". _[stated · confirmed by Ravi]_
- **R-SCOPE-3** *priority:* Next priority, after the first group: reminder emails and the daily count of booked appointments for the business owner. Ravi agreed to this ordering with "ok". _[stated · confirmed by Ravi]_
- **R-SCOPE-4** *out of scope:* Online payment is out of scope for now. Ravi agreed with "ok". _[stated · confirmed by Ravi]_
- **R-SCOPE-5** *out of scope:* Customer accounts are out of scope for now. Ravi agreed with "ok". _[stated · confirmed by Ravi]_
- **R-SCOPE-6** *out of scope:* Cancelling or rescheduling appointments in the portal is out of scope for now. Ravi agreed with "ok". _[stated · confirmed by Ravi]_
- **R-SCOPE-7** *in scope:* A simple owner settings page for connecting the Google Calendar and setting the slot length is in scope. Working hours and blocked dates are not set in the portal; they come from the Google Calendar. _[stated · confirmed by Ravi]_
- **R-SCOPE-8** *priority:* The owner settings page (working hours, blocked dates) belongs to the first priority group, because booking cannot work without it. _[inferred · confirmed by Ravi]_
- **R-SCOPE-9** *out of scope:* Out of scope for now: SMS or WhatsApp reminders (email only). _[assumed · confirmed by Ravi]_
- **R-SCOPE-10** *out of scope:* Out of scope for now: several staff members or rooms, and several service types. There is one provider (the business owner), one appointment type and one calendar. _[assumed · high impact · confirmed by Ravi]_
- **R-SCOPE-11** *out of scope:* Out of scope for now: two-way sync, meaning appointments created directly in Google Calendar are not imported as portal bookings. They only block time (see r2). _[assumed · high impact · confirmed by Ravi]_

### Participants

- Ravi — business owner: goal, scope, priorities, budget, decisions, sign-off

### Client's design idea

_Nothing recorded._

## Business

### Users and roles

- **R-ROLE-1** Customer (anonymous, no account). Tasks: view available timeslots, book one appointment, choose a reminder time, receive confirmation and reminder emails. Permissions: sees only free/busy slots, never other customers' details. Cannot cancel or reschedule in the portal; does so by phoning the business. _[inferred · high impact · confirmed by Ravi]_
- **R-ROLE-2** Business owner (single administrator). Tasks: maintain working hours, slot length and blocked dates; receive the daily update; see and manage appointments in Google Calendar; handle cancellations phoned in by deleting the calendar event. Permissions: full access to settings and all appointment and customer data. Logs in with email and password. _[assumed · high impact · confirmed by Ravi]_

### Use cases

- **R-USE-1** Book an appointment _[inferred · high impact · confirmed by Ravi]_
  - **R-USE-2** *actor:* Customer (no account). _[inferred · confirmed by Ravi]_
  - **R-USE-3** *trigger:* The customer opens the portal link (from the business website, Google listing or a shared link) wanting an appointment. _[assumed · confirmed by Ravi]_
  - **R-USE-4** *steps:* 1) The portal shows free slots for the next 30 days, grouped by day, in the business's local time. 2) The customer picks a slot. 3) The customer enters name and email (required), plus phone and a note of up to 500 characters (both optional), and a reminder time (default 15 minutes before). 4) The customer reviews the summary and presses Confirm. 5) The system re-checks that the slot is still free, both in the portal and as busy time in Google Calendar, then saves the appointment as Booked. 6) A confirmation screen shows date, time and a 'to cancel or change, please call' note with the business phone number. 7) A confirmation email is sent within 1 minute. 8) An event is created in the owner's Google Calendar with the customer's name, email, phone and note. Alternative: if there are no free slots in the 30-day window, the portal says so and shows the business phone number. _[assumed · high impact · confirmed by Ravi]_
  - **R-USE-5** *errors:* If the slot is taken in the meantime, the customer sees 'This time was just booked, please pick another'; the slot list refreshes and the entered details are kept. Invalid or missing email or name gives a field-level message and nothing is saved. If the limit in r7 is reached, the customer is asked to phone the business. If Google Calendar is unreachable, the booking stays confirmed, the event is retried for up to 24 hours, and the owner gets an alert email after 1 hour of failures. If the confirmation email fails, it is retried for up to 24 hours and the failure is logged. _[assumed · high impact · confirmed by Ravi]_
  - **R-USE-6** *end result:* An appointment with status Booked exists, the slot is no longer offered to anyone, a confirmation email has gone to the customer, a reminder is scheduled, and an event exists in the owner's Google Calendar. _[inferred · high impact · confirmed by Ravi]_
  - **R-USE-7** *expected outcome:* The customer books in under 2 minutes without phoning. The owner sees the appointment in Google Calendar within 5 minutes of booking. _[assumed · confirmed by Ravi]_
- **R-USE-8** Send appointment reminder email _[inferred · high impact · confirmed by Ravi]_
  - **R-USE-9** *actor:* The system (scheduler); the recipient is the customer. _[inferred · confirmed by Ravi]_
  - **R-USE-10** *trigger:* The reminder time is reached, which is the appointment start minus the customer's chosen reminder time. _[inferred · confirmed by Ravi]_
  - **R-USE-11** *steps:* 1) The scheduler checks every minute for reminders due. 2) It checks the appointment is still Booked (not cancelled, see r9). 3) It sends a reminder email with date, time, business address and phone. 4) It records the reminder as sent so it is never sent twice. Alternative: if the customer chose 'no reminder', nothing is sent. _[assumed · high impact · confirmed by Ravi]_
  - **R-USE-12** *errors:* If sending fails, it is retried every 2 minutes until the appointment start time, then marked Failed in the email log. If the reminder time was already past at booking time, no reminder is sent and this is logged as Skipped. _[assumed · confirmed by Ravi]_
  - **R-USE-13** *end result:* Exactly one reminder email has been sent (or skipped or failed, with the reason logged) per appointment. _[assumed · confirmed by Ravi]_
  - **R-USE-14** *expected outcome:* The customer is reminded at the chosen time, within 2 minutes, which reduces no-shows. _[assumed · confirmed by Ravi]_
- **R-USE-15** Send daily booking update to the business owner _[inferred · confirmed by Ravi]_
  - **R-USE-16** *actor:* The system (scheduler); the recipient is the business owner. _[inferred · confirmed by Ravi]_
  - **R-USE-17** *trigger:* Every day at 07:00 business local time. _[assumed · high impact · confirmed by Ravi]_
  - **R-USE-18** *steps:* 1) Count appointments booked through the portal during the previous calendar day (00:00–23:59 local time). 2) Also show the 7-day average and the number of appointments scheduled for today. 3) Email the summary to the owner's address. _[assumed · high impact · confirmed by Ravi]_
  - **R-USE-19** *errors:* On days with zero bookings, the email is still sent showing 0. If sending fails, it is retried 3 times within 1 hour, then logged as Failed. _[assumed · confirmed by Ravi]_
  - **R-USE-20** *end result:* The owner has one email per day with the previous day's portal booking count. _[inferred · confirmed by Ravi]_
  - **R-USE-21** *expected outcome:* Ravi can check daily whether the target of at least 5 portal bookings per day within 2 months is being met. _[inferred · confirmed by Ravi]_
- **R-USE-22** Business owner maintains availability in his Google Calendar _[stated · confirmed by Ravi]_
  - **R-USE-23** *actor:* Business owner. _[assumed · confirmed by Ravi]_
  - **R-USE-24** *trigger:* Initial setup before launch, a change of working hours, or a holiday or day off. _[assumed · confirmed by Ravi]_
  - **R-USE-25** *steps:* 1) The owner connects his Google Calendar to the portal once. 2) He marks the times he is unavailable (including non-working time, breaks and days off) as busy events in Google Calendar. 3) The portal reads the calendar and offers only the free slots. 4) Changes in Google Calendar show up in the portal's slots. 5) The portal has no working hours or blocked dates settings. _[stated · confirmed by Ravi]_
  - **R-USE-26** *errors:* An end time before the start time, or overlapping ranges, is rejected with a message. If a change removes hours that already have bookings, the existing bookings are kept and the owner sees a list of the affected appointments so he can phone those customers. _[assumed · confirmed by Ravi]_
  - **R-USE-27** *end result:* The new availability is saved and used for all new bookings. _[assumed · confirmed by Ravi]_
  - **R-USE-28** *expected outcome:* Customers are only offered times the owner can really serve, so there are no double bookings with his private or phone-booked appointments. _[assumed · confirmed by Ravi]_

### Business rules

- **R-RULE-1** Default reminder email is sent 15 minutes before the appointment; the customer can choose a different reminder time (the allowed options are not yet specified). _[stated · confirmed by Ravi]_
- **R-RULE-2** Appointments have one fixed length of 30 minutes, which the owner can change in settings (15, 30, 45 or 60 minutes). Slots start on the hour and half hour and must fit entirely within free time in the owner's Google Calendar. There is no buffer between appointments. _[stated · confirmed by Ravi]_
- **R-RULE-3** A slot is offered only if it lies within the owner's working hours, is not on a blocked date, is not already booked in the portal, and does not overlap any event marked busy in the owner's Google Calendar. _[assumed · high impact · confirmed by Ravi]_
- **R-RULE-4** Booking window: the earliest bookable slot starts at least 2 hours from now; the latest is 30 days ahead. _[assumed · high impact · confirmed by Ravi]_
- **R-RULE-5** Each slot holds exactly one appointment. If two customers confirm the same slot, the first saved wins and the second gets the 'just booked' message. _[assumed · high impact · confirmed by Ravi]_
- **R-RULE-6** Reminder options the customer can choose: 15 minutes before (default), 1 hour before, 24 hours before, or no reminder. If the chosen reminder time is already past when booking, no reminder is sent. _[assumed · high impact · confirmed by Ravi]_
- **R-RULE-7** Customer details per booking: name (2–100 characters), a valid email and a phone number are all required; a note (up to 500 characters) is optional. No account or password. _[stated · confirmed by Ravi]_
- **R-RULE-8** Anti-abuse limit: at most 2 upcoming appointments per email address at the same time. _[assumed · high impact · confirmed by Ravi]_
- **R-RULE-9** All times are shown to customers and the owner in the business's local time zone (set once in settings) and stored in UTC. _[platform default · confirmed by Ravi]_
- **R-RULE-10** Cancellations and changes are phoned in. The owner deletes or moves the event in Google Calendar; the portal detects the deleted event within 15 minutes, marks the appointment Cancelled, frees the slot and does not send the reminder. Moved events are treated as cancellation plus busy time. _[assumed · high impact · confirmed by Ravi]_
- **R-RULE-11** The daily update counts appointments created through the portal on the previous calendar day, local time, regardless of the appointment date. Cancelled ones are still counted, and the number cancelled is shown separately. _[assumed · high impact · confirmed by Ravi]_

### Data (business view)

- **R-DATA-1** Appointment: reference number, start and end time (UTC), status (Booked, Cancelled), customer name, email, phone (required), note (optional), reminder choice, reminder status, created at, Google Calendar event id, calendar sync status. _[stated · confirmed by Ravi]_
- **R-DATA-2** Availability settings: business time zone, working hours per weekday with breaks, slot length, minimum notice (2 hours), booking horizon (30 days), blocked dates, business phone and address shown in emails, owner notification email. _[assumed · high impact · confirmed by Ravi]_
- **R-DATA-3** Email log: appointment reference (if any), type (confirmation, reminder, daily update, alert), recipient, scheduled time, sent time, status (Sent, Failed, Skipped), attempts. _[assumed · confirmed by Ravi]_
- **R-DATA-4** Customer details are stored on each appointment; there is no separate customer record or account. _[inferred · high impact · confirmed by Ravi]_
- **R-DATA-5** Money and payment fields: none, because online payment is out of scope. _[inferred · confirmed by Ravi]_

## Technical

### Integrations

- **R-INT-1** *direction:* Google Calendar: each appointment booked through the portal is added automatically to the business owner's Google Calendar (portal to Google Calendar). Format, transport, auth, access and failure handling are not yet specified. _[stated · confirmed by Ravi]_
  - **R-INT-2** *direction:* Two directions. Portal to Google Calendar: create one event per booking. Google Calendar to portal (read only): every 5 minutes, read the owner's busy times for the next 30 days to filter slots (r3), and read the status of portal-created events to detect deletions or moves (r10). Events created directly in Google Calendar are never imported as bookings. _[assumed · high impact · confirmed by Ravi]_
  - **R-INT-3** *format:* Google Calendar API v3 JSON. Event title: 'Appointment: <customer name>'. Start and end are taken from the appointment. Description holds the reference number, email, phone, note and reminder choice. Private extended property 'portalRef' holds the appointment reference. The event id is stored on the appointment. Busy times are read with the freeBusy query. _[assumed · high impact · confirmed by Ravi]_
  - **R-INT-4** *transport:* HTTPS REST calls to googleapis.com. Event creation goes through the outbox after the booking is saved, never inside the booking transaction. The re-check of busy time at confirm (step 5 of booking) is a synchronous freeBusy call with a 3-second timeout. If that call times out, the last cached busy data (at most 5 minutes old) is used. Deletions are detected by polling every 5 minutes, which keeps detection within the 15 minutes required by r10. _[platform default · confirmed by Ravi]_
  - **R-INT-5** *auth:* OAuth 2.0. The owner connects his Google account once from the settings page and grants the scopes calendar.events and calendar.freebusy. The refresh token is stored encrypted. If the token is revoked or expires, the owner gets an alert email and a banner on the settings page. _[assumed · high impact · confirmed by Ravi]_
  - **R-INT-6** *access:* Access covers one calendar, which the owner chooses in settings (default: his primary calendar). The portal writes only events it created. It reads only free/busy data from the owner's other events, never their titles or contents. _[assumed · high impact · confirmed by Ravi]_
  - **R-INT-7** *failure:* Event creation is retried with exponential backoff (1, 2, 4 … minutes, capped at 30) for up to 24 hours. The owner is alerted by email after 1 hour of failures, and again when the job finally fails. Sync status on the appointment is Pending, Synced or Failed. If the freeBusy read fails for more than 15 minutes, the owner is alerted and slots are still offered from portal data and working hours. _[assumed · high impact · confirmed by Ravi]_
- **R-INT-8** Transactional email service (for example Postmark or Amazon SES) sends the confirmation, reminder, daily update and owner alert emails. _[inferred · high impact · confirmed by Ravi]_
  - **R-INT-9** *direction:* Outbound from the portal to the email service. Delivery and bounce status comes back through a webhook and is written to the email log. _[assumed · confirmed by Ravi]_
  - **R-INT-10** *format:* JSON API request with HTML and plain-text bodies built from portal templates in English. Times are shown in the business's local time. The confirmation email includes an .ics calendar attachment. _[assumed · confirmed by Ravi]_
  - **R-INT-11** *transport:* HTTPS API, sent through the outbox after the domain transaction commits. The sender domain is verified with SPF, DKIM and DMARC so emails reach the inbox. _[platform default · confirmed by Ravi]_
  - **R-INT-12** *auth:* API key kept in the hosting secret store. Webhooks are verified by signature or basic auth. _[assumed · high impact · confirmed by Ravi]_
  - **R-INT-13** *access:* A send-only key for one verified sender domain, which the business provides. Recipients are customers and the owner's notification email. _[assumed · confirmed by Ravi]_
  - **R-INT-14** *failure:* Retries follow each use case: confirmation up to 24 hours, reminder every 2 minutes until the appointment start, daily update 3 times within 1 hour. Hard bounces are marked Failed and not retried. Each attempt is recorded in the email log. _[inferred · confirmed by Ravi]_

### Data (sources, ownership, retention)

- **R-SRC-1** Appointment. Source: created by the customer in the portal; status changes come from Google Calendar sync. Owner: the business (Ravi) is data controller; the portal database is the system of record for portal bookings. Retention: kept 12 months after the appointment date. After that, name, email, phone and note are anonymised; reference, times and status are kept for statistics. _[stated · confirmed by Ravi]_
- **R-SRC-2** Availability settings. Source: entered by the owner on the settings page. Owner: the business. Retention: current values kept indefinitely, with a change history of who changed what and when, kept for 12 months. _[assumed · confirmed by Ravi]_
- **R-SRC-3** Email log. Source: generated by the portal and updated by email provider webhooks. Owner: the business. Retention: 90 days, then deleted. _[assumed · confirmed by Ravi]_
- **R-SRC-4** Google Calendar events and busy times. Source and owner: the owner's Google account, which is the system of record for his calendar. The portal stores only the event id and sync status on the appointment. Busy times are cached in memory or a cache table for at most 5 minutes and never kept long term. _[assumed · high impact · confirmed by Ravi]_
- **R-SRC-5** Owner account and Google OAuth token. Source: owner setup. Owner: the business. Retention: kept while the account is active; deleted immediately when the owner disconnects Google or the account is closed. The password is stored only as an Argon2 or bcrypt hash. _[assumed · high impact · confirmed by Ravi]_
- **R-SRC-6** All timestamps are stored in UTC and converted to the business time zone for display. All entities are defined in one canonical JSON Schema model. Web pages get their data from a backend-for-frontend. _[platform default · confirmed by Ravi]_

### Non-functional

- **R-NFR-1** Availability is 99.5% per month for the booking portal, which allows about 3.6 hours of downtime. Planned maintenance happens between 22:00 and 06:00 business local time. _[assumed · confirmed by Ravi]_
- **R-NFR-2** Performance at the 95th percentile: the slot list loads in under 1.5 seconds; Confirm responds in under 2 seconds, including the Google free/busy re-check; owner settings pages load in under 1 second. _[assumed · confirmed by Ravi]_
- **R-NFR-3** Capacity: 100 concurrent visitors and 200 bookings per day without slowing down. This is about 40 times the success target of 5 bookings per day. _[inferred · confirmed by Ravi]_
- **R-NFR-4** Timeliness: confirmation email sent within 1 minute; event created in Google Calendar within 5 minutes; reminders sent within 2 minutes of the due time; Google deletions detected within 15 minutes; daily update sent by 07:15 local time. _[inferred · confirmed by Ravi]_
- **R-NFR-5** Backup and recovery: daily database backups plus point-in-time recovery, with backups kept for 30 days. Recovery point objective is 1 hour (at most 1 hour of data lost); recovery time objective is 8 hours (service restored within 8 hours). _[assumed · confirmed by Ravi]_
- **R-NFR-6** Usability: the portal works on mobile phones (screens 360 px wide and up) and on the last 2 versions of Chrome, Safari, Edge and Firefox. It meets WCAG 2.1 AA. The interface is in English only. _[assumed · confirmed by Ravi]_
- **R-NFR-7** Monitoring: uptime is checked every 1 minute. The operator is alerted on error rate above 5% over 5 minutes, outbox jobs older than 1 hour, or a missed daily update. _[assumed · confirmed by Ravi]_

### Security and compliance

- **R-SEC-1** Data classes: customer personal data (name, email, optional phone, free-text note) is Confidential. Owner credentials and the Google OAuth token are Secret. Settings and slot availability are Internal; free/busy is public to customers without any details. The note field may contain sensitive information, so the booking form says 'do not include health or other sensitive details'. _[assumed · high impact · confirmed by Ravi]_
- **R-SEC-2** Regulation: the national privacy law of the business's own country applies (the owner confirmed this rather than GDPR). The specific law still needs to be named. The booking form links to a privacy notice. Customer data is processed only to deliver the appointment, with no marketing use. Access and deletion requests are handled by the owner from the settings page by searching by email, within 30 days, or sooner if the national law requires it. Data processing agreements are in place with the hosting provider, the email provider and Google. _[stated · confirmed by Ravi]_
- **R-SEC-3** Protection: HTTPS only (TLS 1.2 or higher, with HSTS). Database and backups are encrypted at rest. The OAuth token and API keys are kept in the secret store and encrypted in the database. Secrets never appear in logs or emails, apart from the customer's own details in their own emails. _[assumed · high impact · confirmed by Ravi]_
- **R-SEC-4** Owner login: email and password of at least 12 characters, plus a one-time code from an authenticator app (TOTP). The account locks for 15 minutes after 5 failed attempts. The session expires after 8 hours of inactivity. _[assumed · high impact · confirmed by Ravi]_
- **R-SEC-5** Anti-abuse on the public portal: at most 10 booking attempts per IP address per hour; an invisible CAPTCHA (for example Cloudflare Turnstile) on Confirm; plus the limit of 2 upcoming appointments per email (r7). Booking responses never show other customers' details. _[assumed · high impact · confirmed by Ravi]_
- **R-SEC-6** Application logs mask customer email and phone and are kept for 30 days. An audit trail of owner logins and settings changes is kept for 12 months. _[assumed · confirmed by Ravi]_

### Technical constraints

- **R-CON-1** The stack is Python/FastAPI, Postgres, and a React + TypeScript web UI, with a backend-for-frontend for the portal and settings pages. _[platform default · confirmed by Ravi]_
- **R-CON-2** Must use: the owner's existing Google Calendar account. No other calendar products are supported. _[inferred · high impact · confirmed by Ravi]_
- **R-CON-3** Hosting is a managed cloud platform with managed Postgres, in a data centre region inside the business's own country (the owner confirmed this; not the EU unless the country is in it). znectAI operates it, and the business pays the running costs, estimated under 50 USD per month at the target volume. The cost estimate needs re-checking if the country has limited cloud regions. _[stated · confirmed by Ravi]_
- **R-CON-4** Integrations are called only through the outbox, after the domain transaction commits. Each layer (API, domain, integration) maps data at its interface and has its own error types; for example, Google errors are never shown raw to customers. _[platform default · confirmed by Ravi]_
- **R-CON-5** The portal runs on the business's own domain or subdomain (for example book.<business>.com), which the business provides. Email is sent from the same domain. _[assumed · confirmed by Ravi]_

## Testing

### Acceptance criteria

R-USE-1 Book an appointment:
- **R-AC-1** Show free slots. Given working hours Mon–Fri 09:00–17:00, slot length 30 minutes and no bookings, When a customer opens the portal on Monday at 08:00 local time, Then the first slot offered is Monday 10:00. Slots start on the hour and half hour, are grouped by day in the business's local time, and run up to 30 days ahead. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-2** Successful booking. Given a free slot, When the customer enters a valid name and email, keeps the default reminder and presses Confirm, Then: the appointment is saved as Booked with a unique reference number; the slot is no longer offered to anyone; the confirmation screen shows date, time, the reference and the 'to cancel or change, please call' note with the business phone; and a confirmation email with an .ics attachment reaches the customer within 1 minute. _[inferred · high impact · confirmed by Ravi]_
- **R-AC-3** Event in Google Calendar. Given a booking has just been confirmed, When up to 5 minutes have passed, Then the owner's chosen calendar has one event. The event is titled 'Appointment: <customer name>', has the booked start and end, and its description holds the reference, email, phone, note and reminder choice. The appointment's sync status is Synced and its Google event id is stored. _[inferred · high impact · confirmed by Ravi]_
- **R-AC-4** Busy time blocks slots. Given the owner has a busy event in Google Calendar on Tuesday 14:00–15:00, When a customer views Tuesday, Then the 14:00 and 14:30 slots are not offered. Given an event marked 'free' covers the same period, Then those slots are offered. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-5** Two customers, one slot. Given two customers have both chosen Wednesday 11:00, When both press Confirm within the same second, Then exactly one appointment is saved as Booked. The other customer sees 'This time was just booked, please pick another', the slot list refreshes without 11:00, and that customer's entered details are kept. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-6** Invalid details. Given the booking form, When the name is missing, shorter than 2 or longer than 100 characters, or the email is invalid, or the note is longer than 500 characters, Then a message appears at the field concerned and nothing is saved, emailed or sent to Google. _[assumed · confirmed by Ravi]_
- **R-AC-7** Limit per email. Given an email address already has 2 upcoming Booked appointments, When a third booking is confirmed with that email, Then it is refused with a message asking the customer to phone the business. Given one of the two is cancelled or has already taken place, Then a new booking is allowed. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-8** Google Calendar down. Given Google Calendar returns errors, When a customer books, Then the booking is still confirmed with screen and email, and sync status is Pending. Retries run at 1, 2, 4 … minutes, capped at 30. The owner gets an alert email after 1 hour of failures. When Google recovers, exactly one event is created (no duplicates). If it is still failing after 24 hours, the status becomes Failed and the owner gets a second alert. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-9** Confirm re-check is slow. Given the Google free/busy check at Confirm takes longer than 3 seconds, When the customer confirms, Then the busy data cached in the last 5 minutes is used and Confirm responds within 2 seconds at the 95th percentile. _[assumed · confirmed by Ravi]_
- **R-AC-10** Window boundaries. Given the time is 10:00, When the customer views slots, Then 12:00 is offered and 11:30 is not. The last day offered is today plus 30 days, and day 31 is not offered. Blocked dates show no slots. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-11** No slots available. Given no free slot exists in the next 30 days, When a customer opens the portal, Then a message says no times are available and shows the business phone number. _[assumed · confirmed by Ravi]_
- **R-AC-12** Cancellation in Google frees the slot. Given a Booked appointment, When the owner deletes its event in Google Calendar, Then within 15 minutes the appointment is Cancelled and the slot is offered again. When the owner moves the event, Then the original appointment is Cancelled and the new time is treated as busy. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-13** Abuse limit per IP address. Given 10 booking attempts from one IP address in the last hour, When an 11th attempt is made, Then it is refused with a 'too many attempts, please try later or call' message. A failed CAPTCHA also blocks Confirm. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-14** Daylight saving time. Given a booking for 10:00 local time on the day after the clocks change, When it is saved, Then it is stored in UTC with the correct offset. The confirmation email, the Google event and the reminder all use 10:00 local time. _[platform default · confirmed by Ravi]_
R-USE-8 Send appointment reminder email:
- **R-AC-15** Default reminder. Given an appointment at 10:00 with the default reminder, When the time reaches 09:45, Then exactly one reminder email is sent by 09:47. It shows the date, time, business address and phone, and is logged as Sent. _[inferred · high impact · confirmed by Ravi]_
- **R-AC-16** Chosen reminder times. Given appointments with 1-hour, 24-hour and 'no reminder' choices, When their reminder times arrive, Then reminders go out at start minus 1 hour and start minus 24 hours (each within 2 minutes), and none is sent for 'no reminder'. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-17** Reminder time already past. Given a booking made 3 hours before the appointment with a 24-hour reminder, When it is saved, Then no reminder is sent and the email log shows the reminder as Skipped. _[assumed · confirmed by Ravi]_
- **R-AC-18** Cancelled before the reminder. Given the owner deleted the appointment's Google event at least 15 minutes before the reminder time, When the reminder time arrives, Then no reminder is sent. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-19** Send failure and no duplicates. Given the email service fails, When the reminder is due, Then it is retried every 2 minutes until the appointment start, then logged as Failed. Given the scheduler restarts while a reminder is being sent, Then the customer still receives at most one reminder. _[assumed · confirmed by Ravi]_
R-USE-15 Send daily booking update to the business owner:
- **R-AC-20** Daily update content. Given 6 appointments were created through the portal yesterday and 1 of them has since been cancelled, When it is 07:00 local time, Then by 07:15 the owner receives one email showing: 6 booked yesterday, 1 cancelled, the 7-day average, and the number of appointments scheduled for today. _[inferred · high impact · confirmed by Ravi]_
- **R-AC-21** Counting by creation day. Given one booking created at 23:59 local time on Monday for an appointment next week, and one created at 00:01 on Tuesday, When Tuesday's update is sent, Then it counts 1 (the Monday booking), and Wednesday's update counts the 00:01 booking. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-22** Zero bookings and failure. Given no portal bookings yesterday, When it is 07:00, Then the email is still sent showing 0. Given the email service fails, Then sending is retried 3 times within 1 hour, then logged as Failed, and the operator is alerted about the missed daily update. _[assumed · confirmed by Ravi]_
R-USE-22 Business owner maintains availability in his Google Calendar:
- **R-AC-23** Owner login. Given the owner account, When the correct password and a valid authenticator code are entered, Then the settings page opens. Given 5 failed attempts, Then the account locks for 15 minutes. Given 8 hours without activity, Then the owner must log in again. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-24** Change working hours. Given Monday hours of 09:00–17:00, When the owner changes them to 09:00–12:00 with no break and saves, Then a newly loaded slot list shows Monday slots only up to 11:30. The change is recorded in the audit trail with who changed it and when. _[assumed · high impact · confirmed by Ravi]_
- **R-AC-25** Blocked dates and breaks. Given a break 12:00–13:00 and blocked dates 24–26 December, When the owner saves, Then no slots are offered 12:00–12:59 on any working day, and no slots at all on 24–26 December. _[assumed · confirmed by Ravi]_
- **R-AC-26** Invalid hours. Given the settings page, When the owner enters an end time before the start time, or overlapping ranges or breaks, Then saving is refused with a message and the previous settings stay in force. _[assumed · confirmed by Ravi]_
- **R-AC-27** Change hits existing bookings. Given 2 Booked appointments on Friday afternoon, When the owner blocks that Friday, Then both appointments are automatically set to Cancelled, their scheduled reminders are cancelled, and a cancellation email is sent to each customer (sent through the outbox). The owner sees a list of the 2 cancelled appointments with customer name, phone and email. _[stated · confirmed by Ravi]_
- **R-AC-28** Google connection lost. Given the owner's Google authorisation is revoked, When the portal next calls Google, Then the owner receives an alert email and the settings page shows a 'reconnect Google Calendar' banner. After reconnecting, Pending events are created. _[assumed · high impact · confirmed by Ravi]_

### Testing and acceptance

- **R-TEST-1** *environments:* Three environments: local development, a staging (test) environment on the same managed cloud as production with its own database, and production. Staging uses a separate Google test account and calendar, and an email sandbox or a test sender subdomain that only delivers to an allow-list of test addresses. Production secrets are never used in staging. _[assumed · high impact · confirmed by Ravi]_
- **R-TEST-2** *environments:* Automated tests run on every change: unit tests for the slot, reminder and counting rules; integration tests with Google and the email service simulated (including errors and timeouts); and end-to-end tests in staging against the real Google test calendar for each acceptance criterion. Before go-live, a load test in staging checks 100 concurrent visitors and the response times in R-NFR-2. _[assumed · confirmed by Ravi]_
- **R-TEST-3** *test data:* Only made-up customer data is used in development and staging (for example test1@<test-domain>); real customer data is never copied out of production. Standard test setup: business time zone set, Mon–Fri 09:00–17:00 with a break 12:00–13:00, 30-minute slots, one blocked date range, and Google test calendar events marked busy and free. _[assumed · high impact · confirmed by Ravi]_
- **R-TEST-4** *test data:* Staging has an adjustable test clock, so the 2-hour notice, the 30-day horizon, reminder times, the 07:00 daily update and daylight-saving changes can be tested without waiting. Test data can be reset to the standard setup with one command. _[assumed · confirmed by Ravi]_
- **R-TEST-5** *uat owner:* Ravi (business owner) owns user acceptance testing and gives the final sign-off. _[inferred · confirmed by Ravi]_
- **R-TEST-6** *uat owner:* UAT takes 1 week in staging. Ravi sets his real working hours and connects a separate test Google calendar. He makes at least 10 test bookings from his phone and a computer, covering: default and chosen reminders, a clash with a busy event, a deletion in Google, a blocked date, and the daily update. znectAI provides a checklist mapped to the acceptance criteria. _[assumed · high impact · confirmed by Ravi]_
- **R-TEST-7** *uat owner:* Go-live gate: all acceptance criteria for the first priority group (booking, confirmation email, Google Calendar sync, owner settings) pass, there are no open critical or major defects, and Ravi signs off in writing. Reminder and daily update criteria must pass before those features are switched on. After launch, Ravi connects his real calendar and makes 1 live test booking that is then deleted. _[assumed · high impact · confirmed by Ravi]_

## Assumptions

_None._

## Platform defaults

- R-AC-14: Daylight saving time. Given a booking for 10:00 local time on the day after the clocks change, When it is saved, Then it is stored in UTC with the correct offset. The confirmation email, the Google event and the reminder all use 10:00 local time.
- R-CON-1: The stack is Python/FastAPI, Postgres, and a React + TypeScript web UI, with a backend-for-frontend for the portal and settings pages.
- R-CON-4: Integrations are called only through the outbox, after the domain transaction commits. Each layer (API, domain, integration) maps data at its interface and has its own error types; for example, Google errors are never shown raw to customers.
- R-INT-4: HTTPS REST calls to googleapis.com. Event creation goes through the outbox after the booking is saved, never inside the booking transaction. The re-check of busy time at confirm (step 5 of booking) is a synchronous freeBusy call with a 3-second timeout. If that call times out, the last cached busy data (at most 5 minutes old) is used. Deletions are detected by polling every 5 minutes, which keeps detection within the 15 minutes required by r10.
- R-INT-11: HTTPS API, sent through the outbox after the domain transaction commits. The sender domain is verified with SPF, DKIM and DMARC so emails reach the inbox.
- R-RULE-9: All times are shown to customers and the owner in the business's local time zone (set once in settings) and stored in UTC.
- R-SRC-6: All timestamps are stored in UTC and converted to the business time zone for display. All entities are defined in one canonical JSON Schema model. Web pages get their data from a backend-for-frontend.
