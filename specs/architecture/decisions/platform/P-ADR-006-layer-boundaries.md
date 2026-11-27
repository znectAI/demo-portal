> Source: znectAI standards v1, decisions/P-ADR-006-layer-boundaries.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# P-ADR-006 Layer boundaries: mapping at the interface, errors per layer
Status: Accepted · 2026-11-20 · decided by Ravi (architect)

## Context
In reference-orders UC-001, a domain error's canonical field (`customer_id`) reached the web
BFF unchanged, because the consumer specs mapped data but not errors. The fix was then put in
the API layer instead of the mapping layer. Nothing stopped a database or HTTP-client
exception from crossing layers either: a unique-key violation in the repository would have
reached the API as an unhandled 500.

## Decision
1. **Mapping happens at the interface between two layers, and only where it is needed.**
   Where the representations on the two sides of an interface differ, that interface maps
   between them. Where both sides already use the canonical model, there is no mapper.

   | Interface | Representation outside the canonical model | Mapper |
   |---|---|---|
   | consumer ↔ api | the consumer's format (view models, API resources, webhooks) | the consumer's module in `app/mapping/`, in and out |
   | repository ↔ database | table rows, per `persistence.yaml` | row ↔ canonical functions at the repository's interface |
   | integrations ↔ external system | the external system's format | the external system's module in `app/mapping/`, used by `app/integrations/` |
   | api ↔ service, service ↔ repository, service ↔ integrations | none: canonical on both sides | no mapper |

2. **Mappings cover errors as well as data.** Every consumer that sends requests has an error
   mapping: for each domain error (code plus canonical field) and for request-validation
   errors, the consumer's error shape — HTTP status, problem type, the field name in the
   consumer's own terms, and the message. Its consumer spec has an **Error mapping** section
   with executable examples.

3. **Each layer handles its own errors and exposes only its own error types at its
   interface.**
   - repository: catches database-driver errors and raises repository errors (for example
     `NotFound`, `Conflict` for a unique-key clash).
   - integrations: catches transport errors and raises integration errors (for example
     `Unavailable`, `Rejected`).
   - service: turns repository and integration errors into domain errors, or handles them
     (for example a retry). It never lets a driver or transport exception through.
   - mapping: turns domain and validation errors into each consumer's error shape.
   - api: serializes what the mapping returns. Anything unexpected becomes a 500 problem+json
     with no internals in it.

4. **A layer doesn't depend on another layer's libraries.** Only the repository imports the
   database libraries (SQLAlchemy, psycopg); only integrations imports the HTTP client
   (httpx); only the api (and the composition root, `app/main.py`) imports the web framework
   (FastAPI). The service owns transactions through an interface the repository provides,
   not through database-library objects. Import-linter contracts enforce this
   (`include_external_packages = True`).

## Consequences
- Each interface has one place where its translation lives, data and errors alike, specified
  and tested by example.
- A consumer's field names never leak into the domain, and the domain's never leak into a
  consumer.
- A little more code at each interface that changes representation: error types per layer,
  and a transaction interface in the repository. Interfaces that don't change representation
  get no mapper, so there is no copy-the-fields boilerplate.
- Existing projects adopt it with a project ADR and a retrofit story; new projects start with
  it.
