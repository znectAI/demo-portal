> Source: znectAI standards v1, decisions/P-ADR-004-outbound-integrations-outbox.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# P-ADR-004 Outbound integrations go through an outbox, outside the domain transaction
Status: Accepted · 2026-11-20 · generic part of reference-orders ADR-004 (2026-11-16)

## Context
A change to the system's own state must not fail or slow down because an external system is
unavailable, and the external system must not receive the same change twice. Calling it
inside the database transaction couples the two; calling it after commit with no record can
lose the change if the process dies.

## Decision
- The command that makes the change writes an outbox row in the same transaction.
- After commit, it tries to send immediately (best effort).
- A retry job sends due outbox rows with exponential backoff; rejected or exhausted ones are
  marked permanent for a human.
- Every send carries a stable idempotency key (the entity's id).
- The integration follows pattern P3 and P-ADR-006: the integrations layer maps transport
  failures to its own errors (`Unavailable`, `Rejected`), and the service decides between
  retry and permanent failure.

## Consequences
- No lost changes and no duplicates, without a message broker.
- A short window where the change is committed but not yet at the external system is normal,
  and the specs say so.
- Moving to an event or queue design later (P6) is an architecture change.
