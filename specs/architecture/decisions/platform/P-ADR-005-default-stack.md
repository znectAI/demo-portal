> Source: znectAI standards v1, decisions/P-ADR-005-default-stack.md. Do not edit here:
> amend it with a project ADR, or change the standard.

# P-ADR-005 Default stack: FastAPI, Postgres, React
Status: Accepted · 2026-11-20 · from reference-orders ADR-005 and overview (2026-11-16)

## Context
The platform's agents, worker image, checks and pattern catalogue are built for one stack at
a time. A default stack keeps projects predictable; a project can still choose another
through its own ADR when the platform supports it.

## Decision
- Backend: Python 3.12, FastAPI on uvicorn, Pydantic v2, SQLAlchemy 2 Core with psycopg 3,
  Alembic, Postgres 16, httpx for outbound HTTP. Development: pytest, ruff, import-linter,
  PyYAML, jsonschema.
- Web UI (when the project has one): React, TypeScript (strict), Vite; eslint, tsc, Vitest
  and Testing Library. Built to static files the backend serves; the Vite dev server proxies
  the BFF in development.
- Pattern catalogue: [patterns/python-fastapi.md](../patterns/python-fastapi.md).
- Any other dependency needs the product owner's approval (constitution).

## Consequences
- The worker and CI run Python, and Node when a project has a web UI.
- Another stack (Spring Boot is planned) needs its own pattern catalogue and worker support
  before a project can choose it.
