# Demo portal

A znectAI project. The specs in [`specs/`](specs/) are the source of truth: code follows them.

| Stage | Where | Who signs it off |
|---|---|---|
| Requirements | [`specs/requirements/requirements.md`](specs/requirements/) | the business owner (merged PR) |
| Use cases | [`specs/use-cases/`](specs/use-cases/) | the business people (gate 1) |
| Design | [`specs/architecture/`](specs/architecture/) | the technical reviewer (gate 2) |
| Stories | GitHub issues: one per use case, stories as its sub-issues | the owner approves the plan |

Each story labelled `ready` is built by the znectAI pipeline (plan, tests first, code, CI, agent
review) and reviewed by a person before it merges. The rules everyone follows, people and agents,
are in [`specs/constitution.md`](specs/constitution.md).

Repo: `znectAI/demo-portal` · created from the znectAI project template (standards v1).
