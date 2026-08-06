# ADR-0008 — Workflow State Machine

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Workflow status was an ad-hoc string (`draft | candidate | promoted |
deprecated`). Anything could transition to anything, so lifecycle errors were
silent.

## Decision
Every workflow/graph follows one explicit, enforced lifecycle:

```
draft → validated → candidate → promoted → deprecated → archived
```

Happy path: `draft → validated → candidate → promoted`, then
`promoted → deprecated → archived`. `deprecated` is reachable from any state
except `archived`; `archived` is terminal. An illegal transition raises
`WorkflowError` with the allowed targets.

## Consequences
- Lifecycle errors are caught instead of silent.
- Promotion to production can only happen through review and validation.
- Every workflow also carries a stable `workflow_id` (identity everywhere).