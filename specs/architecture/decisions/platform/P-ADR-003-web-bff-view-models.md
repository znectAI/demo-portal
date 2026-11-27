> Source: znectAI standards v1, decisions/P-ADR-003-web-bff-view-models.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# P-ADR-003 Web UIs get view models from a backend-for-frontend
Status: Accepted · 2026-11-20 · from reference-orders ADR-003 (2026-11-16)
Applies to: projects with a web UI. A project without one doesn't adopt it.

## Context
A web UI needs formatted money, local times, status labels and totals. Doing this in the
browser duplicates business-adjacent rules in TypeScript, lets them drift from the API and
other consumers, and leaks the canonical model to the browser.

## Decision
- The UI calls only its BFF (by convention `/ui/api`), served by the backend.
- The BFF returns view models produced by the UI's mapping module: display-ready strings and
  flags, in the UI's naming convention (camelCase).
- The UI renders view models as given; it holds no money, time or status logic.
- Errors reach the UI in its own terms too: `fieldErrors` keyed by the form's field names
  (P-ADR-006).

## Consequences
- All formatting rules live in the backend, tested once, and specified in the UI's consumer
  spec.
- A public API stays independent of screen needs and can be versioned separately.
- A screen change that needs new data is a consumer spec change.
