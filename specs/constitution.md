> Source: znectAI standards v1, constitution.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# Constitution — Demo portal

Standing rules for everyone who changes this repo, people and agents. The specs in
`specs/` are the source of truth; code follows them, never the other way round.

## Specs
1. Every behaviour the system has is described by a use case in `specs/use-cases/` or by the
   architecture in `specs/architecture/`. Behaviour that isn't specified is a defect.
2. A change that alters a use case or the architecture changes the spec **in the same PR** as
   the code. An architecture change also adds an ADR in `specs/architecture/decisions/`.
3. Acceptance criteria have permanent IDs (`UC-003.AC2`). Never renumber; retire an ID by
   marking it `Removed` and keep it in the file.
4. Every acceptance criterion has at least one test that names it, and every mapping example
   has a test. `tools/spec_check` enforces this in CI.
5. Platform standards copied into `specs/` (the files under
   `specs/architecture/decisions/platform/`) are never edited in the project. A project
   departs from one only through its own ADR that amends it and says why.

## Architecture
6. Layers and allowed dependencies are defined in `architecture/overview.md` and enforced by
   import-linter. A web UI talks to the backend only over HTTP, through its BFF.
7. The canonical model (`architecture/model/canonical.yaml`) is the only internal model.
   Each consumer gets its own format from the **mapping** layer; consumer formats never leak
   into the service or repository layers, and canonical types never leave the backend.
8. Mapping happens at the interface between two layers, only where the representations on
   either side differ. Each layer handles its own errors and exposes only its own error types
   (P-ADR-006).
9. New use cases follow a pattern from `architecture/patterns.md` and copy its reference
   implementation. A use case that needs a new pattern is an architecture change.

## Code
10. Money is integer minor units plus currency in the canonical model and the database. Never
    use floats for money anywhere.
11. Times are stored and exchanged in UTC (ISO 8601). Local time appears only in consumer
    formats that ask for it.
12. API errors use RFC 9457 problem+json. Domain rule violations become 422; unknown
    resources 404; conflicts 409.
13. The stack is the one in `architecture/overview.md` (by default P-ADR-005). Code is lint
    clean and type clean with the stack's tools.
14. No new runtime dependency without approval; the pipeline blocks them by default.
15. Database changes go through migrations that match `architecture/persistence.yaml`.

## Tests
16. Tests prove acceptance criteria through public interfaces: HTTP for the backend, rendered
    components for a UI. Name each test with the criteria it proves:
    `@pytest.mark.req("UC-001.AC2")` in Python, `[UC-003.AC1]` in the test title in TypeScript.
17. Backend tests run against the real database engine (for Postgres, never SQLite). External
    services are faked at the HTTP boundary.
