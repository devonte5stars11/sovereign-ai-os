# Sovereign Hermes AI OS — v5.1 Frozen Reference Architecture

This is the definitive architecture. It is **frozen**; future changes arrive
via Architecture Decision Records (ADRs) in `docs/adr/`, not ad-hoc expansion.

## Reference architecture
```
YOU
 │
 Experience Layer (Buzz • Voice • Mobile • Web • Dashboards • Human Modes)
 │
 Hermes Kernel
   Planner · Capability Router · Prompt Graph Engine (G1–G4)
   Context Budget Manager · Memory Manager · Reflection · Digital Twin
   Scheduler + Resource Budgets · Policy Engine + AI Constitution
   Workflow Registry · Capability Registry
 │
 Multi-Agent Organization (SoulVault as composable profiles)
 │
 Execution & Service Layer
   MCP · REST · SDKs · Browser · Git · Docker · OMP · Service Discovery · Plugin Manifests
 │
 Provider Adapter Layer (Capability Manifest + Capability Tests each)
 │
 Knowledge Pipeline + Artifact Registry
   Capture → Clean → Verify → Link → Graph ↔ Vector ↔ Artifact ↔ Metadata
   → Markdown → Git → Backups
 │
 Permanent Sovereign Knowledge (Obsidian as human-readable view)
```

## Frozen invariants
1. **Markdown + Git + Obsidian** = permanent, vendor-independent knowledge.
2. **Hermes is the orchestrator**, never the permanent memory store.
3. **Capability-based routing** via manifests + capability tests.
4. **Prompt Graphs** are versioned, testable, reusable assets.
5. **Product Studio and Creative Studio** are independent delivery layers.
6. **Evaluation, provenance, governance, typed artifacts** are first-class.
7. **Adapters and plugins** are the only extension points.
8. **SoulVault** is data-driven composable profiles (engine) + ergonomic md (UX).

## SOP — the LDD operating loop
1. Observe context (input, Obsidian, intelligence).
2. Select Soul(s); state them explicitly.
3. Choose the lowest-cost capable model (router).
4. Apply relevant SpecStack files.
5. Execute with recovery fallbacks defined.
6. Validate (code review, Taste Refiner, SpecStack compliance).
7. Log traces to `memory/reflections.md` and evolve graphs.
8. Output clean Markdown with next steps + Obsidian references.

## Maturity model
L1 Personal assistant → L2 Multi-agent collaborator → L3 Autonomous research →
L4 Product dev studio → L5 Enterprise OS → L6 Self-improving knowledge platform.

## Build roadmap (vertical slices — each independently useful)
1. **Kernel MVP** ✅ (this repo): foundation, capability registry, provider
   manifests, profiles, prompt graphs, workflow registry, artifact registry,
   constitution — all tested.
2. **Knowledge slice** — capture → process → markdown → git → retrieval.
3. **Coding slice** — repo editing, testing, PR creation, artifact logging.
4. **Creative slice** — asset generation → metadata → knowledge pipeline.
5. **Business slice** — proposal + simple Next.js deployment (Product Studio).
6. **Optimization slice** — evaluation, graph versioning, automated promotion.
