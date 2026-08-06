# principles.md — Engineering Principles

These are the invariants. Any proposed change that violates one requires an ADR explaining why.

1. **Knowledge ownership.** Markdown + Git + Obsidian are the permanent, vendor-independent store of truth. Nothing important lives in proprietary chat history.
2. **Hermes is the orchestrator.** It routes, plans, and executes — it is never treated as the durable memory store.
3. **Capability over brand.** Providers are selected by declared capabilities (verified by capability tests), never by hardcoded model names.
4. **Adapters and plugins are the only extension points.** New capabilities enter through adapters/plugins, never by editing the kernel.
5. **Open interfaces where practical.** Prefer standards like MCP, but keep adapters flexible enough for SDKs, REST, CLI, or local integrations.
6. **Prompt Graphs are assets.** Versioned and testable like code; reflection revises graphs, not one-off prompts.
7. **First-class evaluation.** Every workflow records latency, success, cost, retries, human feedback, and graph version. Metrics drive optimization.
8. **Resource discipline.** Every workflow declares explicit time/budget/token/retry/parallel limits.
9. **Resilience by design.** Every workflow defines recovery policies so provider changes or failures degrade gracefully.
10. **Privacy first.** Client work runs in isolated sandboxes; sensitive data stays local.
11. **Simplify by evidence.** Future changes come from observed bottlenecks or new requirements — not from adding conceptual layers.
12. **Separate architecture from policy.** The architecture doc stays stable; routing rules, budgets, and approval policies live in configuration.
