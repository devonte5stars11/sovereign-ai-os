# Aether Capability Mesh

Status: P0 architecture

## Purpose

Aether routes work by capability rather than by chatbot brand. The Capability Mesh is a live registry of models, tools, runtimes, MCP servers, local nodes, applications, subscriptions, and provider features available to the owner or a tenant.

## Capability record

Each capability should expose at minimum:

- `capability_id`
- provider/runtime
- category and operation
- authentication method
- required scopes
- tenant/project boundaries
- privacy/sensitivity ceiling
- approval tier
- reversibility
- estimated quality
- historical success rate
- latency distribution
- marginal cost
- subscription/included status
- quota/remaining allowance where knowable
- health/availability
- locality (`cloud|local|hybrid`)
- supported input/output modalities
- version and freshness timestamp

## Capability classes

- cognition: reasoning, synthesis, planning, classification
- coding: repository analysis, patching, tests, review
- research: web, X/social, file search, knowledge retrieval
- multimodal: image, audio, video, long-document analysis
- execution: shell, filesystem, browser, computer/app control
- data: SQL, analytics, transformations, vector/full-text retrieval
- collaboration: Notion, GitHub, Drive, messaging, CRM
- workflow: cron, webhooks, durable jobs, queues
- generation: documents, code, media, reports, artifacts

## Default backbone

- **ChatGPT/OpenAI** — primary conversational cognition and synthesis.
- **Codex** — primary software-engineering runtime.
- **Hermes Max** — persistent local/cloud execution substrate.
- **Gemini** — specialist multimodal/large-context/Google-connected capability.
- **Grok/xAI** — specialist current-information/X-oriented research and independent critique.
- **GitHub** — executable/versioned truth and software collaboration.
- **Notion** — human-readable operational state.
- **Google Drive** — human-accessible evidence/artifact lake.

These are defaults, not hard dependencies.

## Routing policy

Aether filters candidates in this order:

1. policy and sensitivity eligibility
2. required capability coverage
3. provider/runtime health
4. quality floor
5. privacy/locality requirements
6. approval/reversibility compatibility
7. subscription availability and marginal cost
8. latency
9. measured task-specific success

A route score may combine quality, reliability, capability fit, privacy fit, latency, and marginal cost, but policy constraints are hard gates rather than weighted preferences.

## Subscription-first economics

Preferred routing order when quality remains sufficient:

1. already-paid supported subscription capability
2. included/near-zero marginal-cost capability
3. local runtime/model
4. inexpensive metered API
5. premium frontier API
6. owner approval when predicted spend exceeds policy

The system must not assume a consumer subscription grants arbitrary API rights. The registry distinguishes app-only, subscription-backed, OAuth-backed, API, MCP, CLI, and local capabilities.

## Fallback

For each critical capability define:

- primary route
- equivalent fallback(s)
- quality degradation threshold
- cost escalation threshold
- state-transfer requirements
- user-notification policy

A fallback should be silent when outcome quality and policy remain within bounds; otherwise surface the consequence.

## Tool registry safety

Every tool action declares:

- side-effect class
- idempotency characteristics
- validation schema
- timeout
- retry policy
- approval tier
- compensating/rollback action if available

Tools never inherit authority merely because a model can call them.

## Health and discovery

Aether periodically verifies capability manifests, connection state, provider health, model/tool availability, and version freshness. Discovery may add candidates but may not automatically widen permissions.

## Evaluation

Routing decisions must be evaluated using held-out task sets and production outcomes. Aether records chosen route, alternatives considered, quality, latency, cost, failures, corrections, and user acceptance so routing can improve without changing constitutional limits.
