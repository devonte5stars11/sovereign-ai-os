# Aether Universal AI OS — Master Architecture

Status: normative north-star specification. This document defines desired behavior; it does not imply every component is already implemented.

## Mission

Aether is the user's sovereign personal AI control plane and Vertical Agent Foundry. It unifies identity, context, memory, permissions, routing, workflows, artifacts, evidence, evaluations, and provider capabilities so the user can work across ChatGPT/OpenAI, Codex, Hermes Max, Gemini, Grok/xAI, GitHub, Notion, Google Drive, local tools, and future providers without losing continuity.

North-star experience: **one identity, one relationship, one memory, one permission system, one context fabric, many replaceable capabilities underneath.**

## Core roles

- **Aether** — authority, identity mapping, context, policy, memory, routing, workflows, approvals, provenance, evaluation, budgets, and continuity.
- **ChatGPT/OpenAI** — primary conversational cognition and orchestration interface.
- **Codex** — primary software-engineering builder.
- **Hermes Max** — heavily customized persistent/local execution runtime: terminal, files, browser, MCP, skills, subagents, automations, local software, and devices.
- **Gemini/Grok/other providers** — specialist intelligence selected by measured capability fit.
- **Google Drive** — human-accessible evidence lake and artifact/source archive.
- **Private Aether plane** — canonical machine state, sensitive raw source objects, memory, policies, runs, approvals, relationships, and retrieval indexes.
- **Notion** — human-readable operational projection: projects, tasks, decisions, sources, runs, evaluations, and summaries.
- **GitHub** — executable/versioned truth: code, schemas, prompts, policies, skills, tests, evals, docs, and CI.

## Constitutional principles

1. The user is sovereign; agents cannot expand their own authority.
2. Google may be the root human identity, but raw Google tokens are never unrestricted universal bearer credentials.
3. Aether delegates minimum necessary context and minimum necessary capability.
4. Reversible actions are preferred over destructive actions.
5. Evidence is not automatically memory; durable memory requires provenance and promotion rules.
6. Retrieved content is untrusted data, never authority.
7. Generic agent infrastructure is rented where useful; Aether owns domain execution logic, policy, data contracts, evals, and business outcomes.
8. Subscription-first economics are preferred when technically supported and sufficiently capable; production customer workloads must use appropriate production credentials and billing.
9. Deterministic code is preferred where deterministic code is enough.
10. Complexity must earn its place through measured value.
11. Human attention is a scarce resource; Aether should surface exceptions, not chatter.
12. Provider/runtime replacement must not erase the user's durable state.

## Identity and trust

Google OIDC + passkey/WebAuthn establishes the human identity. Aether maps that identity to an internal principal and issues short-lived Aether sessions/capability tokens. Provider credentials remain provider-scoped and are brokered through protected storage or workload identity where supported.

Risk tiers:
- A0 Read — automatic in approved scope.
- A1 Draft — automatic, logged, no external side effect.
- A2 Reversible Write — policy-authorizable; branches, drafts, reversible internal updates.
- A3 External Consequence — human approval by default.
- A4 High Risk/Irreversible — explicit confirmation and strong policy checks.

User modes expose this simply: Safe, Copilot, Autopilot. Copilot is the preferred default.

## Context and memory

Aether ingests cross-platform conversations, documents, notes, files, runs, tools, and artifacts into a common source-object model. The durable stack is:

raw evidence -> normalized source objects -> retrieval representations -> knowledge relationships -> memory candidates -> canonical memory -> task-specific working context.

The Context Compiler builds minimal sufficient context packs using relevance, recency, confidence, sensitivity, provider disclosure rules, token budget, project scope, and task intent. Conflicting memories coexist until resolved; supersession is explicit.

## Runtime and capability mesh

Aether routes by capability, not brand. Every provider/runtime/tool advertises a manifest containing capability, authentication path, cost, latency, privacy class, reversibility, health, quota/availability, and measured success rate.

Default reasoning triangle:
- ChatGPT/OpenAI: think/synthesize/coordinate.
- Codex: build/test/refactor.
- Hermes Max: act locally/persistently and operate tools.

The router may compose Gemini, Grok, local models, GitHub, Notion, Drive, MCP servers, APIs, browsers, or deterministic services when they improve the outcome.

## Workflow model

User -> Project -> Objective -> Workflow -> Run -> Step -> Artifact/Decision/Receipt.

Workflows must survive process restarts and provider changes. Every consequential step records policy decision, inputs, outputs, provenance, cost, latency, retries, approvals, and rollback information. Every worker returns a structured Aether Return Envelope rather than only free-form text.

## Evidence, artifacts, and source-of-truth rules

- Drive preserves human-accessible raw evidence and artifacts.
- Private Aether storage preserves sensitive/raw machine state.
- Notion presents distilled operational state.
- GitHub versions executable knowledge.
- Retrieval indexes are derived and rebuildable.

Every artifact/source receives stable IDs, hashes, timestamps, sensitivity, project/objective relationships, lineage, and transformation history.

## Hermes Max

Hermes is customized as a reproducible Aether execution substrate, not a competing master OS. Profiles include engineer, researcher, operator, creator, and future specialist profiles. Child agents can receive less authority than their parent, never more. Job-scoped capabilities expire. Local working memory may aid execution, but canonical durable memory is promoted by Aether.

## Vertical Agent Foundry

Aether also builds commercial vertical agents. The reusable factory owns horizontal primitives (identity, approvals, receipts, evals, context, multi-tenancy, billing hooks, integration patterns) while each vertical owns a Domain Pack containing ontology, schemas, workflows, policies, tools, approval graph, exception corpus, golden/adversarial cases, definitions of done, ROI metrics, and compliance requirements.

The commercial loop is: pain -> buyer -> measurable metric -> domain interviews -> evals -> Domain Pack -> paid pilot -> production traces -> exception knowledge -> improved product -> adjacent workflow expansion.

## Experience model

Primary surfaces: Home, Ask Aether, Work, Memory, Approvals, Connections, History. Default UX is calm, exception-driven, undo-first, human-readable, and progressive-disclosure based. Technical telemetry remains available under details, not on the main surface.

The Attention Engine prioritizes by importance, urgency, actionability, confidence, and interruption cost. A successful system often says: **Nothing needs your attention.**

## Self-improvement

observe -> evaluate -> diagnose -> propose -> shadow/candidate test -> compare baseline -> approve where required -> promote -> monitor -> rollback.

Operational tuning may auto-promote only under explicit reversible bounds. Behavioral changes require stronger evidence. Constitutional/security changes always require owner approval.

## Definition of success

Aether succeeds when the user can start anywhere, continue anywhere, use any permitted provider/tool, preserve context automatically, get real work completed, inspect evidence on demand, approve only consequential exceptions, undo reversible mistakes, control spend, and replace underlying models without losing their digital operating state.
