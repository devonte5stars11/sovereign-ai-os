# graphs/ — Prompt Graph Definitions

Prompt Graphs (G1–G4) are the formalized, reusable workflows of the system.
They are versioned like code and stored in the **Workflow Registry**
(`graph-registry/`) once approved. Reflection revises *graphs*, not ad-hoc
prompts.

## The four canonical graph archetypes

| Graph | Purpose | Typical nodes |
| ----- | ------- | ------------- |
| **G1** | Simple linear task | prompt → output |
| **G2** | Retrieve-augmented | planner → retriever → specialist → verifier → aggregator → artifact |
| **G3** | Multi-agent collaboration | planner → {specialists...} → verifier → aggregator → artifact |
| **G4** | Self-evaluating / improving | G2/G3 + evaluation node → metrics → graph revision → version bump → promotion |

## Node roles

- `planner` — breaks the task into sub-steps.
- `retriever` — pulls relevant memory/knowledge (Context Budget Manager).
- `specialist` — a domain expert (routes via SoulVault profiles).
- `verifier` — checks quality, SpecStack compliance, provenance.
- `aggregator` — assembles the final typed artifact.
- `evaluation` — records latency, cost, success, retries, human feedback.

## Versioning + promotion

```
draft  →  candidate  →  promoted  →  deprecated
```

A graph is only queried/executed at scale once it is `promoted`, at which
point it is frozen and only replaced by a higher-version revision.

## Machine representation

The kernel's `PromptGraph` (kernel/ai_os_kernel/prompt_graph.py) is the
executable form; these markdown files are the human-readable specification.
Graph definitions should be mirrored as YAML/JSON in `graph-registry/`.
