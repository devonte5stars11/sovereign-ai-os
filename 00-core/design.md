# design.md — System Design & Architecture (Reference)

This document captures the frozen reference architecture. It is the **stable contract**; policy (routing rules, budgets, provider preferences) lives in configuration, not here.

## Highest-level view
```
YOU
 │
 Experience Layer (Buzz • Voice • Mobile • Web • Dashboards • Human Modes)
 │
 Hermes Kernel
   Planner
   Capability Router
   Prompt Graph Engine (G1–G4)
   Context Budget Manager
   Memory Manager (Working / Project / Evergreen / Archive)
   Reflection (updates graphs, not just prompts)
   Digital Twin
   Scheduler + Resource Budgets
   Policy Engine + AI Constitution
   Workflow Registry
   Capability Registry
 │
 Multi-Agent Organization (SoulVault as composable profiles)
 │
 Execution & Service Layer
   MCP • REST • SDKs • Browser • Git • Docker • OMP • Service Discovery • Plugin Manifests
 │
 Provider Adapter Layer (each publishes Capability Manifest + Capability Tests)
 │
 Knowledge Pipeline + Artifact Registry
   Capture → Clean → Verify → Link
   → Knowledge Graph ↔ Vector ↔ Artifact Store ↔ Metadata DB
   → Markdown → Git → Backups
 │
 Permanent Sovereign Knowledge (Obsidian as the human-readable view)
```

## Key mechanisms
1. **Capability-based routing** — tasks declare capabilities needed; the router picks the cheapest adapter whose manifest satisfies them.
2. **Prompt Graphs (G1–G4)** — versioned, testable, reusable workflow assets; reflection updates graphs, not ad-hoc prompts.
3. **Context Budget Manager** — Need → Retrieve → Compress → Rank → Assemble → Reason → Discard.
4. **Standardized Context Packets** — every agent receives the same structure (Task, Goals, Constraints, Relevant Memory, Artifacts, Policies, Budget, Expected Output).
5. **Resource Budgets** — Time, Budget ($), Tokens, Retries, Parallel workers.
6. **Recovery Policies** — every workflow defines fallbacks.
7. **Typed Artifacts** — unique ID, type, creator, workflow, graph version, source, trust, checksum, timestamp.
8. **Evaluation on every workflow** — latency, cost, quality, success, retries, human feedback, graph version.
9. **Event-driven reactions** — composable, no agent needs to know the full pipeline.
10. **AI Constitution** — root policy enforced by the Policy Engine.

## Separation of concerns
**Runtime:** Planner, Router, Memory, Execution, Monitoring.
**Build time:** Prompt Graph Editor, Skill Builder, Plugin SDK, Testing, Evaluation, CI.
**Delivery isolation:** Product Studio (builds SaaS — Hermes is not the SaaS) and Creative Studio (adapter-swappable creators) are independent.

## Maturity model
| Level | Goal                              |
| ----- | --------------------------------- |
| L1    | Personal assistant                |
| L2    | Multi-agent collaborator          |
| L3    | Autonomous research system        |
| L4    | Product development studio        |
| L5    | Enterprise operating system       |
| L6    | Self-improving knowledge platform |

## Implementation order (vertical slices only)
1. **Kernel MVP** — foundation, capability registry, one provider, Obsidian, Git, a simple Prompt Graph.
2. **Knowledge slice** — Capture → Process → Markdown → Git → Retrieval.
3. **Coding slice** — repo editing, testing, PR creation, artifact logging.
4. **Creative slice** — generate asset → store metadata → knowledge pipeline.
5. **Business slice** — proposal + simple Next.js deployment.
6. **Optimization slice** — evaluation, graph versioning, automated promotion, resource budgets.

Each slice must be independently useful before adding more infrastructure.
