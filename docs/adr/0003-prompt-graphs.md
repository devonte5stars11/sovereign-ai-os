# ADR-0003 — Prompt Graphs as Versioned Workflow Assets

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Accumulating one-off prompt edits over time is unmaintainable and untestable.

## Decision
Workflows are expressed as **Prompt Graphs** (G1–G4): directed acyclic graphs
of typed nodes (planner, retriever, specialist, verifier, aggregator,
evaluation), versioned like code. Reflection updates **graphs**, not ad-hoc
prompts:

```
Evaluation → Graph metrics → Graph revision → Version bump → Promotion
```

## Consequences
- Reusable, testable, replayable workflows.
- The graph's version propagates into every produced artifact (provenance).
- Promotion gates (draft→candidate→promoted) control what runs at scale.
