> Source: znectAI standards v1, decisions/P-ADR-001-specs-as-source-of-truth.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# P-ADR-001 Specs in the repo are the source of truth
Status: Accepted · 2026-11-20 · from reference-orders ADR-001 (2026-11-16)

## Context
Agents and people both change the code. Without a written, versioned description of what
the system must do, every change is judged only against the story that asked for it, and
behaviour drifts.

## Decision
- Two levels of spec live in the project's `specs/`: the architecture (layers, canonical
  model, persistence, consumers, patterns, decisions) and end-to-end use cases.
- User stories are changes to the system, tracked as sub-issues of the use-case issue. Most
  fit the spec; those that change it update the spec in the same PR.
- The parts that matter most are machine-checked in CI (`tools/spec_check`, import-linter):
  model conformance, persistence references, layering, and traceability from acceptance
  criteria and mapping examples to tests.

## Consequences
- Reviewers and agents have an objective baseline.
- Spec changes need human approval, which adds reading for stories that change behaviour.
- Specs must stay short to stay current; anything that can be checked by a machine is.
