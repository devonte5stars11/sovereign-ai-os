# Aether v1 — Universal AI Operating System Master Plan

Status: bootstrap candidate

## Mission

Aether is the user's personal AI control plane. It unifies OpenAI, xAI/Grok, Google Gemini, Hermes Agent, Notion, GitHub, Apple Notes, Google Drive, and future tools behind stable capability, memory, policy, provenance, and evaluation contracts.

The system optimizes for user agency, security, completion, low friction, portability, and compounding knowledge.

## Canonical system of record

- **Notion** — human-readable operational state: projects, tasks, decisions, durable-memory summaries, sources, runs, and evaluation views.
- **GitHub** — executable/versioned truth: code, prompts, schemas, policies, workflows, eval fixtures, CI, and ADRs.
- **Apple Notes** — capture edge only. Important notes are promoted into Aether; Apple Notes is not the canonical database.
- **Google Drive** — source/artifact repository and Google Workspace surface; ingest or link valuable material without making Drive the orchestration brain.
- **Private database/object store** — raw private source objects, machine state, attachments, and sensitive artifacts that do not belong in Notion or the public Git repository.
- **Vector/full-text indexes** — derived retrieval indexes, rebuildable from canonical source objects. An embedding index is never the source of truth.

## Aether control plane

Aether owns:

1. Intent normalization
2. Context assembly
3. Capability-based routing
4. Provider/model selection
5. Tool authorization
6. Multi-agent delegation
7. Artifact/provenance logging
8. Evaluation, latency, and budget telemetry
9. Durable-memory promotion
10. Human approval gates

Provider adapters never own business logic. They translate stable Aether contracts into vendor-specific APIs.

## Provider roles

### OpenAI
High-reliability agent workflows, coding, structured outputs, tool use, and manager-style orchestration.

### xAI / Grok
Current-information research, independent critique, broad synthesis, and provider diversity.

### Google Gemini
Multimodal analysis, large-context workflows, and Google-connected work.

### Hermes Agent
Bounded peer executor with its own agentic environment. Aether exposes approved context/tools to Hermes and ingests outputs/traces through the same provenance and evaluation pipeline as every other provider.

## Universal memory

Memory has four durable layers plus working context:

1. **Working context** — ephemeral task/session context.
2. **Event log** — append-only normalized run/tool/artifact/policy events.
3. **Source objects** — original chats, notes, documents, code snapshots, and research artifacts with immutable source IDs and hashes.
4. **Durable memory** — distilled facts, preferences, decisions, procedures, project context, and summaries with provenance, confidence, sensitivity, freshness, and supersession metadata.
5. **Derived retrieval indexes** — full-text, vector, and graph projections rebuilt from source objects and durable memory.

Retrieval is hybrid: metadata filters + full-text/BM25 + vector similarity + graph relations + recency/freshness + confidence + sensitivity policy.

Conflicting memories coexist until resolution. Aether never silently overwrites contradictory evidence.

## Ingestion contract

All importers produce the same normalized envelope:

```json
{
  "source_system": "chatgpt|grok|gemini|hermes|notion|apple_notes|github|google_drive|web|manual",
  "external_id": "provider-stable-id",
  "captured_at": "ISO-8601",
  "content_type": "conversation|note|document|code|artifact|event",
  "content_hash": "sha256",
  "sensitivity": "public|private|sensitive",
  "project_refs": [],
  "raw_uri": "private-object-uri",
  "metadata": {}
}
```

Pipeline:

capture -> normalize -> deduplicate -> classify sensitivity -> store source object -> chunk -> enrich metadata -> extract candidate memories -> index -> promote durable memory under policy -> write human-readable operational state to Notion -> commit only non-sensitive executable knowledge to GitHub.

Idempotency is enforced with `source_system + external_id + content_hash`.

## Security model

- Least privilege by tool, provider, project, data class, and environment.
- No secrets in prompts, Git, ordinary Notion pages, traces, vector metadata, or logs.
- Prefer OAuth/OIDC and short-lived credentials over static secrets when supported.
- Default-deny destructive, financial, account, publish/send, credential, and infrastructure-changing actions.
- Treat retrieved content and model outputs as untrusted input.
- Validate structured tool arguments before execution.
- Redact sensitive traces when required.
- Maintain append-only audit events for approvals, tool calls, policy decisions, data promotions, and state changes.
- Keep the generic/public kernel separate from private personal memory and client data.

### Approval tiers

- **A0 Read** — search/retrieve/summarize. Automatic inside approved scope.
- **A1 Draft** — create local/internal drafts and artifacts without external side effects. Automatic with logging.
- **A2 Reversible Write** — internal Notion updates, branches, PR drafts, reversible state changes. Scoped policy may authorize automatically.
- **A3 External Side Effect** — messages, publishing, deployments, purchases, account changes. Human approval by default.
- **A4 High Risk / Irreversible** — credential/security changes, destructive data operations, financial transfers, legal commitments. Explicit confirmation plus policy checks.

Agents cannot silently expand their own permissions.

## Identity and Google Sign-In

Google Sign-In may authenticate the human user to an Aether UI for convenience. It is **not** a universal provider credential.

Each provider/integration keeps its own OAuth grant, API key, local credential, or service identity with independent scopes. Aether maps them to one internal user identity and stores provider credentials only in an appropriate protected secret store.

Never pass a Google access token to OpenAI, xAI, Hermes, or any unrelated provider.

## Orchestration strategy

Start deterministic and add agentic behavior only where measured value justifies it.

1. Policy pre-filter determines allowed tools, sensitivity, budget, approval tier, and required capabilities.
2. Capability router creates a provider shortlist.
3. Route scorer chooses the primary provider using measured quality, cost, latency, availability, privacy requirements, and task fit.
4. Manager decomposition is used for genuinely complex work.
5. Independent subtasks run in parallel when safe.
6. A critic/reviewer is invoked only when task value/risk or evaluation history justifies extra latency and spend.
7. Aether synthesizes and validates the final result.
8. Events, artifacts, costs, routes, and evaluations are logged.
9. Candidate durable memories are promoted according to memory policy.

Multi-agent debate is not the default. Use it for consequential decisions, ambiguous research, architecture, evaluation failures, or tasks where provider diversity has demonstrated benefit.

## Self-improvement loop

observe -> score -> diagnose -> propose -> test in candidate/shadow mode -> compare with baseline -> approve when required -> promote -> monitor -> rollback on regression.

Automatic improvement is allowed only for reversible low-risk configuration within explicit bounds. Aether never auto-disables security policy, exposes secrets, expands permissions, or promotes untested code directly to production.

## Aether v1 implementation slices

### Slice 1 — Control plane and providers
- Production OpenAI adapter
- Production xAI adapter
- Keep and verify Gemini adapter
- Hermes peer adapter / MCP boundary
- Provider health and capability discovery
- Stable structured input/output/tool contracts

### Slice 2 — Shared operational surface
- Notion Projects, Tasks, Memory, Decisions, Agents, Sources, Runs, Evaluations
- GitHub ADRs, schemas, prompts, policies, tests, and CI
- Cross-links between Notion project records and GitHub repos/issues/PRs

### Slice 3 — Capture and memory
- Apple Shortcut: share note/text -> authenticated Aether Inbox endpoint
- Chat export/import adapters
- Google Drive discovery/import connector
- Canonical source-object store
- PostgreSQL + pgvector hybrid retrieval baseline
- Idempotent ingestion and provenance

### Slice 4 — Reliability and bounded autonomy
- Eval datasets and rubrics
- Route-quality metrics
- Cost/latency budgets
- Approval-policy tests
- Prompt-injection/tool-misuse fixtures
- Candidate prompt/routing/config promotion only after passing gates

## Suggested technical baseline

- Python 3.12+
- Pydantic v2 for contracts and configuration
- FastAPI for the local/server control plane
- PostgreSQL + pgvector for private structured machine state and vector retrieval
- PostgreSQL full-text search first; add a dedicated search engine only if benchmarks justify it
- Object storage for immutable raw artifacts and exports
- Redis only when distributed queue/caching needs justify it
- Temporal when durable, resumable, long-running workflows outgrow simple jobs/cron
- OpenTelemetry-compatible traces alongside the existing canonical event schema
- MCP as an interoperability/tool boundary, not as the memory database or orchestration brain
- OpenAI agent tooling selectively inside the OpenAI adapter; never force non-OpenAI providers through an OpenAI-specific abstraction
- Docker Compose for reproducible local development
- GitHub Actions for lint/test/evals/security checks
- OIDC for cloud deployment credentials where supported
- Dependency pinning, automated dependency updates, SBOM generation, secret scanning, SAST, and provenance/attestation where practical

## Definition of done for Aether v1

Aether v1 is operational when the user can:

1. Capture an Apple Note, import a source, or submit a goal.
2. Retrieve relevant prior context across imported sources with permission-aware hybrid retrieval.
3. Route a task to OpenAI, Grok, Gemini, Hermes, or a local executor through a stable capability contract.
4. Execute bounded tools under approval policy.
5. Receive one synthesized result with source/artifact provenance.
6. Write project, task, decision, memory, source, run, and evaluation state back to Notion.
7. Store executable/versioned changes in GitHub through reviewable branches/PRs.
8. Inspect route, provider, cost, latency, tool, policy, and evaluation traces.
9. Re-run ingestion idempotently without duplicating durable memory.
10. Test a proposed prompt/routing/policy improvement against a baseline before promotion.

That is the first complete Aether: small enough to operate, strong enough to compound, and designed to grow without rebuilding the foundation.