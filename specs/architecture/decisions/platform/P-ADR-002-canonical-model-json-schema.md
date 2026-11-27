> Source: znectAI standards v1, decisions/P-ADR-002-canonical-model-json-schema.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# P-ADR-002 Canonical model as JSON Schema in YAML; money in minor units
Status: Accepted · 2026-11-20 · from reference-orders ADR-002 (2026-11-16)

## Context
A system usually has several consumers with different formats (a web UI, a public API,
partner systems, files). Without one internal model, each pair of components invents its
own, and conversions multiply. The model must be readable by people, checkable by machines,
and not tied to one language, because the platform serves more than one stack.

## Decision
- One canonical model per project, `specs/architecture/model/canonical.yaml`, JSON Schema
  2020-12 in YAML, with its invariants (`x-invariants`, INV-n).
- Code models mirror it (Pydantic in `app/canonical/` on the FastAPI stack); CI checks they
  match.
- Money is `{minor_units: integer, currency}`. Floats are never used for money. Consumers get
  their own money format from the mapping layer.
- Derived values are marked `x-derived` and never stored.

## Consequences
- Every consumer format is a mapping from one model: adding a consumer is one module and one
  spec file.
- Changing the canonical model is an architecture change (ADR, approval).
- The schema and the code models are kept in sync by a check, not by generation; this keeps
  the code readable but means both must be edited.
