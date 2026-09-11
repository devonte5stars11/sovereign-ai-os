# Aether Documentation & Data Master Plan

Status: canonical planning document for the Aether bootstrap branch

## Purpose

Aether must be reproducible, auditable, portable, safe, and capable of compounding knowledge across ChatGPT/OpenAI, Codex, Hermes Max, Gemini, Grok/xAI, Google Drive, Notion, GitHub, local runtimes, future providers, and vertical-agent products.

The system therefore treats documentation and datasets as first-class product infrastructure rather than afterthoughts.

This document defines the complete documentation set, reference corpus, dataset classes, governance rules, lineage requirements, and minimum evidence needed to operate Aether and its Vertical Agent Foundry safely at high quality.

## Documentation hierarchy

### 1. Constitution and product doctrine

Required documents:

- `AETHER_MASTER_ARCHITECTURE.md` — system boundaries, responsibilities, principles, and north-star architecture.
- `AETHER_CONSTITUTION.md` — immutable/owner-controlled rules: sovereignty, permission inheritance, least privilege, data separation, reversible actions, approval tiers, self-improvement boundaries, and provider independence.
- `AETHER_EXPERIENCE_PRINCIPLES.md` — UX/EX rules: calm-by-default, exception-driven attention, receipts, progressive disclosure, undo-first interaction, human-readable failure states, and satisfaction metrics.
- `AETHER_TRUST_MODEL.md` — A0–A4 action tiers, Safe/Copilot/Autopilot modes, step-up authentication, intent authorization, capability delegation, and emergency locks.

### 2. Identity, authentication, and authorization

Required documents:

- `IDENTITY_ARCHITECTURE.md` — Google-rooted identity, Aether principal mapping, passkeys/WebAuthn, sessions, recovery identity, device trust, and workload identities.
- `CREDENTIAL_BROKER.md` — provider OAuth/API credentials, short-lived tokens, workload identity federation, secret storage, token refresh, revocation, and credential non-exportability.
- `CAPABILITY_POLICY.md` — human-readable and machine-readable capability rules.
- `AUTH_THREAT_MODEL.md` — stolen session, compromised device, token replay, OAuth abuse, privilege escalation, rogue agent, confused deputy, and recovery-account threats.

### 3. Control plane and runtime

Required documents:

- `CONTROL_PLANE.md` — intent normalization, context compilation, provider routing, workflow planning, policy gates, approvals, receipts, and state transitions.
- `CAPABILITY_MESH.md` — capability registry schema, providers, tools, models, MCP servers, local runtimes, availability, privacy, cost, latency, health, and reversibility metadata.
- `PROVIDER_ADAPTER_CONTRACT.md` — stable interface for OpenAI, xAI, Gemini, local models, and future providers.
- `RUNTIME_SELECTION_POLICY.md` — subscription-first economics, quality floors, failover, provider health, and cost/performance routing.
- `WORKFLOW_RUNTIME.md` — objectives, workflows, runs, steps, checkpoints, retries, pause/resume, idempotency, cancellation, and durable state.
- `RETURN_ENVELOPE.md` — structured return format for Codex, Hermes, subagents, and provider workers.

### 4. ChatGPT, Codex, and Hermes Max backbone

Required documents:

- `OPENAI_BACKBONE.md` — ChatGPT as primary conversational cognition, Codex as engineering runtime, supported subscription/OAuth paths, Agents API usage, API fallback, and production-vs-personal separation.
- `HERMES_MAX_ARCHITECTURE.md` — custom Hermes profiles, tools, MCP, skills, local/cloud nodes, sandbox tiers, subagents, scheduling, memory boundaries, upgrade management, and reproducibility.
- `HERMES_PERMISSION_MODEL.md` — job-scoped capability envelopes, parent/child privilege rules, filesystem/network/tool restrictions, and expiration.
- `HERMES_SKILL_STANDARD.md` — skill metadata, inputs, outputs, required tools, examples, evals, failure conditions, versions, ownership, and permissions.
- `HERMES_UPSTREAM_COMPATIBILITY.md` — upstream tracking, patch strategy, regression tests, migration process, and rollback.

### 5. Universal context and memory

Required documents:

- `UNIVERSAL_MEMORY.md` — raw evidence, normalized objects, retrieval chunks, knowledge relationships, memory candidates, canonical memory, working context, freshness, confidence, and supersession.
- `CONVERSATION_LEDGER.md` — cross-platform conversation capture and objective/project linking.
- `CONTEXT_COMPILER.md` — task-specific context packs, token budgets, relevance, privacy filtering, provider-aware disclosure, source ranking, and stale-context prevention.
- `MEMORY_PROMOTION_POLICY.md` — when evidence becomes durable memory and how contradictions are handled.
- `CONTRADICTION_RESOLUTION.md` — conflict detection, temporal supersession, conditional truths, human resolution, and canonicalization.
- `PROVENANCE_STANDARD.md` — source IDs, hashes, lineage, timestamps, model/tool versions, transformation history, and evidence links.

### 6. Capture and source systems

Required documents:

- `INGESTION_STANDARD.md` — normalized source envelope, idempotency, deduplication, content extraction, classification, and failure handling.
- `GOOGLE_DRIVE_EVIDENCE_LAKE.md` — folder conventions, raw chat exports, artifacts, project evidence, retention, and links to private machine state.
- `NOTION_OPERATIONAL_SURFACE.md` — projects, tasks, decisions, sources, runs, agents, evaluations, and human-readable state.
- `GITHUB_EXECUTABLE_TRUTH.md` — what belongs in Git, what must remain private, branch/PR rules, source control conventions, and release discipline.
- `APPLE_CAPTURE.md` — Share-to-Aether and Apple Notes capture path.
- `CHAT_CAPTURE_ADAPTERS.md` — ChatGPT, Codex, Grok, Gemini, Hermes, Claude, exports, APIs, supported local capture, and browser/share flows.

### 7. Artifacts and knowledge

Required documents:

- `ARTIFACT_MODEL.md` — document/code/image/video/audio/dataset/report lineage, ownership, versions, sensitivity, canonical status, and related decisions/runs.
- `KNOWLEDGE_GRAPH_MODEL.md` — entities and relationships across people, projects, objectives, workflows, sources, artifacts, memories, decisions, agents, and providers.
- `SEARCH_AND_RETRIEVAL.md` — metadata, Postgres full-text, pgvector, graph expansion, reranking, recency, confidence, and permissions.

### 8. Security, privacy, and compliance

Required documents:

- `SECURITY_ARCHITECTURE.md` — trust boundaries, zero-trust assumptions, secrets, encryption, sandboxing, network boundaries, dependency security, and audit.
- `PROMPT_INJECTION_DEFENSE.md` — retrieved content as untrusted data, tool output trust, instruction hierarchy, sanitization, approvals, exfiltration tests, and red-team fixtures.
- `DATA_CLASSIFICATION.md` — public/private/confidential/highly-sensitive/client-scoped classes and permitted providers.
- `DATA_RETENTION_AND_DELETION.md` — retention classes, deletion semantics, exports, legal holds where applicable, tombstones, and index rebuilding.
- `PRIVACY_MODEL.md` — minimization, purpose limitation, provider disclosure, customer isolation, local-only processing, and consent.
- `INCIDENT_RESPONSE.md` — containment, credential rotation, provider revocation, event reconstruction, user notification, recovery, and postmortem.
- `SECURITY_TEST_PLAN.md` — OWASP LLM/agentic risks, NIST-aligned control checks, SAST, secret scanning, dependency scanning, SBOM, and adversarial tests.

### 9. Reliability and operations

Required documents:

- `SLO_SLA_POLICY.md` — availability, completion success, latency, recovery time, and workflow-specific targets.
- `OBSERVABILITY.md` — event schema, traces, logs, metrics, correlation IDs, redaction, provider/tool telemetry, and retention.
- `RUNBOOKS.md` — provider outage, failed ingestion, stuck workflow, invalid credential, corrupted index, duplicate data, failed deployment, and compromised node.
- `BACKUP_AND_DISASTER_RECOVERY.md` — Postgres/object-store backups, restore drills, Git recovery, Notion/Drive reconciliation, recovery objectives, and integrity checks.
- `COST_GOVERNANCE.md` — per-provider/project/workflow budgets, subscription utilization, API thresholds, anomaly detection, and showback/chargeback.
- `RELEASE_AND_CHANGE_MANAGEMENT.md` — dev/staging/prod, feature flags, migrations, eval gates, rollback, and approvals.

### 10. Evaluation and self-improvement

Required documents:

- `EVAL_STRATEGY.md` — golden, adversarial, edge-case, policy, tool-use, recovery, human-escalation, cost, latency, and regression evals.
- `MODEL_ROUTING_EVALS.md` — provider/model comparison methodology and confidence thresholds.
- `EXPERIENCE_EVALS.md` — user correction, undo, acceptance, unnecessary interruption, notification usefulness, and satisfaction metrics.
- `SELF_IMPROVEMENT_GOVERNANCE.md` — observe/diagnose/propose/shadow-test/promote/monitor/rollback loop; operational vs behavioral vs constitutional changes.
- `RED_TEAM_PROGRAM.md` — attack scenarios for prompt injection, data exfiltration, social engineering, tool misuse, authorization bypass, memory poisoning, and agent collusion.

### 11. Vertical Agent Foundry

Required documents:

- `AGENT_FOUNDRY.md` — idea selection, validation, domain expert loop, proof-of-value, pilot, production, measurement, and expansion.
- `DOMAIN_PACK_STANDARD.md` — ontology, workflows, tools, schemas, policies, approval graph, exception library, examples, evals, ROI metrics, and compliance requirements.
- `WORKFLOW_DEFINITION_OF_DONE.md` — machine-readable completion contracts.
- `VERTICAL_PRODUCT_SECURITY.md` — tenant isolation, customer credentials, customer-data boundaries, and production credentials independent of the owner's personal subscriptions.
- `PILOT_PLAYBOOK.md` — baseline measurement, pilot success metrics, instrumentation, human supervision, kill criteria, and rollout.
- `ROI_MEASUREMENT.md` — business outcome metrics, baselines, counterfactuals, time saved, error reduction, revenue protected/recovered, and cost per successful workflow.
- `MULTI_TENANCY.md` — tenant IDs, row/object separation, indexes, secrets, logs, rate limits, billing, deletion, and export.
- `CUSTOMER_ONBOARDING.md` — system connections, permissions, data mapping, policy import, sandbox pilot, approvals, and signoff.

### 12. Business and governance

Required documents:

- `PRODUCT_STRATEGY.md` — wedge selection, expansion rules, ICP, buyer, job-to-be-done, and positioning.
- `GTM_PLAYBOOK.md` — founder-led sales, discovery, pilots, case studies, pricing, expansion, and renewal.
- `PRICING_AND_UNIT_ECONOMICS.md` — workflow cost, gross margin, support burden, value-based pricing, and API/infrastructure costs.
- `VENDOR_RISK.md` — provider dependency, lock-in, data terms, quota risk, model deprecation, portability, and exit plan.
- `LEGAL_COMPLIANCE_REGISTER.md` — jurisdiction/vertical-specific obligations tracked as requirements, not guessed by agents.

## External reference corpus

Aether should maintain a versioned reference registry containing links, retrieval dates, hashes where license permits, and notes for authoritative documentation. Prefer live links plus metadata over copying content when licensing or freshness favors retrieval.

Core reference families:

1. OpenAI
   - Agents API overview/quickstart
   - Responses API and Agents SDK documentation
   - Codex documentation
   - tool calling, structured outputs, files, web/file search, MCP, background/long-running agent documentation
   - workload identity federation and authentication documentation
   - model catalog, pricing, rate limits, data controls, safety/usage policies

2. Hermes Agent / Nous Research
   - installation and provider configuration
   - tools/toolsets
   - MCP
   - skills and progressive disclosure
   - memory/session search
   - subagent/delegation behavior
   - cron/scheduling and messaging
   - command approvals and sandbox/isolation
   - release notes/upstream changes

3. Google / Gemini
   - Gemini API/Interactions API
   - function calling/tool combination
   - context caching/long context
   - files and multimodal inputs
   - Google OAuth/OIDC and Cloud IAM/workload identity
   - Drive API/changes/watch mechanisms
   - data use and retention controls

4. xAI / Grok
   - Responses API/Chat Completions compatibility
   - function calling and built-in tools
   - web/X search where exposed
   - MCP/connectors where exposed
   - models, rate limits, pricing, and data controls

5. GitHub
   - GitHub Apps/OAuth
   - Actions/OIDC
   - contents/git/PR/issues/actions APIs
   - branch protection/rulesets
   - code scanning, secret scanning, Dependabot, SBOM/attestations

6. Notion
   - OAuth authorization
   - REST API
   - webhooks/event delivery
   - data-source/database schema behavior
   - rate limits/versioning

7. Standards and security
   - Model Context Protocol specification
   - OAuth 2.0/OIDC/WebAuthn/passkeys
   - JSON Schema/OpenAPI
   - OpenTelemetry
   - NIST AI RMF and Generative AI Profile
   - OWASP LLM Top 10 and Agentic Applications Top 10
   - MITRE ATLAS where relevant
   - SOC 2/ISO 27001/HIPAA/other vertical frameworks only when actually applicable

## Dataset architecture

Aether datasets must be separated by purpose and provenance. Never mix raw private evidence, evaluation data, training/fine-tuning data, product analytics, and customer data without explicit policy.

### Dataset classes

#### A. Source/evidence datasets

Purpose: durable record of what actually happened.

Examples:
- chat exports
- source documents
- tool results
- run traces
- provider responses
- artifacts
- code snapshots
- human approvals/corrections

Storage: private object store and/or Drive evidence lake; indexes are derived.

#### B. Canonical memory dataset

Purpose: durable beliefs/decisions/procedures derived from evidence.

Required fields:
- memory ID
- statement/content
- type
- project/tenant
- provenance links
- confidence
- freshness
- sensitivity
- valid-from/valid-to
- supersedes/superseded-by
- verifier/human confirmation where required

#### C. Retrieval benchmark dataset

Purpose: prove that Aether can find the correct source/context.

Each record includes:
- query
- expected relevant source IDs
- forbidden source IDs/privacy domains
- expected canonical answer facts
- stale/superseded distractors
- minimum precision/recall or rank targets

#### D. Context-compiler dataset

Purpose: verify that each agent receives enough context but not too much.

Each case includes:
- task
- candidate context pool
- required context
- forbidden context
- token budget
- provider privacy constraints
- expected context pack

#### E. Tool-use dataset

Purpose: test correct tool selection and argument construction.

Include:
- normal tool calls
- ambiguous cases
- malformed inputs
- permission-denied cases
- dangerous actions
- idempotency/retry cases
- stale credentials
- partial outages

#### F. Authorization/policy dataset

Purpose: enforce A0–A4 rules and capability inheritance.

Include:
- allowed/denied actions
- step-up auth cases
- owner overrides
- child-agent privilege-escalation attempts
- cross-project/tenant access attempts
- expired delegation
- emergency lock behavior

#### G. Security/red-team dataset

Purpose: continuously test adversarial resilience.

Include:
- direct/indirect prompt injection
- malicious retrieved documents
- credential-exfiltration requests
- memory poisoning
- tool output injection
- confused deputy cases
- social engineering
- malicious MCP/tool descriptions
- cross-tenant leakage probes
- data-retention/deletion verification

#### H. Provider routing dataset

Purpose: evaluate best model/provider/tool path.

Fields:
- task class
- privacy class
- expected quality rubric
- latency target
- cost target
- required capabilities
- provider/model candidates
- measured outcome

#### I. Experience/UX dataset

Purpose: optimize satisfaction rather than only model accuracy.

Signals:
- accepted without edit
- corrected
- undone
- ignored notification
- unnecessary approval
- time-to-completion
- interruption count
- user-requested detail level
- preference overrides

Do not infer sensitive personal attributes for UX optimization.

#### J. Reliability/chaos dataset

Purpose: validate recovery.

Cases:
- provider 429/5xx
- network interruption
- node restart
- duplicated webhook
- reordered event
- expired token
- partial write
- corrupted index
- missing object
- timeout
- sandbox reset
- user cancellation

#### K. Domain Pack datasets

Each commercial vertical gets its own isolated pack:

- ontology/entity examples
- workflow traces
- policy versions
- definitions of done
- exception corpus
- approval examples
- golden cases
- edge/adversarial cases
- real anonymized production outcomes where permitted
- synthetic cases covering rare failures
- schema mappings
- ROI baselines and outcomes

Customer data must remain tenant-scoped. Cross-customer learning must use explicit legal/privacy mechanisms and de-identification/aggregation where appropriate; never silently mix customer datasets.

## Dataset lifecycle

Every dataset follows:

`collect -> validate provenance/licensing -> classify sensitivity -> normalize -> deduplicate -> version -> split -> evaluate -> monitor drift -> deprecate/archive`

No dataset is considered production-grade without ownership, purpose, provenance, license/usage basis, sensitivity, version, and quality criteria.

## Dataset registry fields

Every dataset entry must define at minimum:

- `dataset_id`
- `name`
- `version`
- `purpose`
- `owner`
- `source_type`
- `provenance_uri`
- `license_or_usage_basis`
- `sensitivity`
- `tenant_scope`
- `pii_classification`
- `retention_policy`
- `storage_location`
- `schema_version`
- `row_or_object_count`
- `created_at`
- `last_updated_at`
- `quality_checks`
- `eval_or_training_allowed`
- `provider_disclosure_allowed`
- `deletion_method`
- `supersedes`

## Data quality gates

Before use in evals, routing, memory promotion, or any learning loop, datasets should be checked for:

- provenance completeness
- duplicates
- contradictory labels
- temporal leakage
- train/eval contamination
- customer/tenant leakage
- stale policy versions
- malformed schemas
- unredacted secrets
- unsafe PII/sensitive attributes
- license/terms restrictions
- class imbalance
- missing rare/exception cases

## Golden datasets to build first

1. **Aether Memory Retrieval v1** — 100–300 queries across project decisions, chats, Drive evidence, Notion state, and GitHub artifacts.
2. **Aether Context Compiler v1** — 50–100 tasks with required and forbidden context.
3. **Aether Authorization v1** — 200+ A0–A4 cases including agent privilege inheritance.
4. **Aether Tool Safety v1** — safe, ambiguous, dangerous, malformed, and retry/idempotency cases.
5. **Aether Prompt Injection v1** — direct and indirect injection, malicious files, tool outputs, and MCP metadata.
6. **Aether Provider Router v1** — representative coding, research, extraction, multimodal, long-context, and local/private tasks.
7. **Aether Recovery v1** — provider failures, sandbox resets, partial writes, duplicate events, and resumability.
8. **Aether EX v1** — interruption, notification, receipt, undo, and approval scenarios.
9. **Hermes Max Engineer v1** — repository navigation, implementation, tests, branch/PR workflows, permission denials, and rollback.
10. **Vertical Domain Pack v1** — created only after choosing the first paid workflow; includes its golden/edge/exception/ROI corpus.

## Synthetic vs production data

Use synthetic data heavily for rare, dangerous, destructive, or privacy-sensitive scenarios. Production traces should be promoted into datasets only under explicit governance and with appropriate redaction/de-identification. Synthetic cases do not replace real-world validation; they complement it.

## Fine-tuning policy

Do not fine-tune merely because data exists. Prefer prompt/skill/tool/context improvements first. Fine-tuning is justified only when a stable repeated behavior has sufficient high-quality examples and evaluation evidence shows it materially improves cost, latency, or quality. Training data must have explicit provenance, rights, tenant scope, and leakage checks.

## Documentation freshness automation

Aether should maintain a documentation watcher for critical upstream dependencies:

- OpenAI Agents API / Codex / model/tool/auth changes
- Hermes releases and docs
- Gemini API changes
- xAI API changes
- MCP specification changes
- GitHub API/auth/security changes
- Notion API/webhook changes
- NIST/OWASP security guidance changes

Each watcher creates a diff, impact classification, affected components, required tests, and proposed documentation/code changes. It must not silently change security or production policy.

## Minimum documentation gate for production

No customer-facing vertical agent should enter production without:

- architecture and data-flow diagram
- threat model
- domain workflow and definition-of-done
- tool/permission inventory
- approval matrix
- data classification/retention policy
- tenant-isolation design
- rollback/recovery plan
- eval suite and release thresholds
- incident runbook
- observability/receipt schema
- cost model
- customer-facing limitations/escalation policy
- vendor dependency register

## Principle

Aether's source code is only part of the system. The complete product is:

`code + policies + documentation + datasets + evals + evidence + provenance + skills + workflows + operational history`.

If any of these are missing, the system is not fully reproducible or trustworthy.