# ADR-0007 — Unified Event Schema

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Multiple subsystems (graphs, providers, tools, plugins, the pipeline) each
produce observability signals in different shapes. That makes tracing, replay,
and analytics ad hoc.

## Decision
All subsystems emit the **same canonical event structure**:

```
event_id  event_type  source  timestamp  actor
correlation_id  workflow_id  artifact_id  payload  metadata
```

Events are persisted append-only in a durable `EventLog` (SQLite). A single
`correlation_id` traces a whole run end-to-end. The pipeline emits
`task.received → souls.selected → task.routed → provider.invoked →
artifact.created → markdown.written → git.committed → evaluation.logged`.

## Consequences
- Deterministic replay and tracing by correlation_id.
- Analytics, monitoring, and audit come from one source.
- New subsystems emit events without knowing downstream consumers.