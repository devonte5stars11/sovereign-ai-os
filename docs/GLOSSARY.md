# Glossary — Fixed Terminology

Keeping these definitions stable makes the project easier for contributors to
understand and prevents concept overlap. This is the canonical meaning of every
core term; a term means exactly this everywhere in the codebase.

| Concept       | Meaning                                                           |
| ------------- | ----------------------------------------------------------------- |
| **Agent**     | Runtime executor — an instance that runs a profile and executes steps. |
| **Profile**   | Configuration for an agent (role, capabilities, tool_access, evaluation rules). |
| **Soul**      | User-facing preset built from one or more profiles (SoulVault ergonomics). |
| **Workflow**  | End-to-end business process; lives in the Workflow Registry with a state machine. |
| **Prompt Graph** | Executable DAG inside a workflow (G1–G4), versioned like code. |
| **Skill**     | Reusable function/tool invocation.                                |
| **Capability**| What a provider or tool can do (declared in a capability manifest). |
| **Plugin**    | Installable extension that adds capabilities.                     |
| **Artifact**  | Immutable, provenance-bearing output (checksummed; confidence + freshness). |
| **Event**     | The single canonical record of something happening (unified schema). |
| **Manifest**  | Typed, validated configuration (provider / workflow / graph / policy). |
| **Capability Router** | Picks the cheapest provider whose manifest satisfies a task's required capabilities. |
| **Evaluation**| Per-run metrics (latency, cost, tokens, success, retries, rating) + cost rollups. |

## Relationship
```
Soul (user preset) = one or more Profiles → an Agent runs a Profile
Agent executes a Workflow → Workflow owns one or more Prompt Graphs
A Prompt Graph node may call Skills / Tools / Capabilities
Artifacts + Events are produced along the way and persisted for audit & evaluation
```

## What is deliberately NOT added
Per the architecture freeze (PRINCIPLES, ADR-0001), the following are treated as
**already covered or deferred**, not as separate new concepts:
- New "souls", agents, memory types, orchestration layers, or routing systems.
- Identity, secrets, workspace isolation, and plugin marketplace are **deferred/
  operational** concerns tracked in the roadmap, not new kernel concepts.