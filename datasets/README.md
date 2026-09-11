# Aether Datasets

This directory is the versioned manifest and evaluation-data surface for Aether. Raw private evidence, secrets, customer data, and large licensed datasets do **not** belong in this public repository.

## What belongs here

- dataset schemas
- dataset registry metadata
- synthetic fixtures safe for public source control
- golden evaluation cases that contain no sensitive data
- generators for synthetic/adversarial cases
- redacted examples
- split/version manifests
- quality checks
- eval rubrics
- expected outputs where safe

## What does not belong here

- API keys or OAuth tokens
- raw ChatGPT/Grok/Gemini/Hermes exports containing private history
- personal memory databases
- client/customer records
- production PII or regulated data
- copyrighted corpora copied without a valid basis
- provider secrets
- private object-store snapshots

## Core dataset families

1. `memory_retrieval/` — find the right evidence/memory and reject stale or forbidden context.
2. `context_compiler/` — build minimal sufficient provider-safe context packs.
3. `authorization/` — A0–A4 policy, step-up auth, privilege inheritance, tenant/project boundaries.
4. `tool_safety/` — correct tool selection, arguments, retries, idempotency, and dangerous-action handling.
5. `prompt_injection/` — direct/indirect injection, malicious files, tool output, MCP metadata, and exfiltration.
6. `provider_routing/` — quality/cost/latency/privacy benchmarks across available runtimes.
7. `recovery/` — outages, sandbox resets, duplicate events, partial writes, cancellation, and resumption.
8. `experience/` — notification, approval, receipt, undo, and interruption-quality scenarios.
9. `hermes_max/` — coding, local execution, sandboxing, skills, subagents, and permission-bounded workflows.
10. `domain_packs/` — vertical-specific ontology, workflows, exception corpora, golden cases, and ROI evaluation data.

## Required governance

Every dataset must have a registry entry using `registry.schema.json` and must document its provenance, usage basis/license, sensitivity, tenant scope, retention, provider-disclosure policy, and whether it may be used for evaluation, training/fine-tuning, or both.

## Versioning

Use semantic-style dataset versions when practical. Changes to labels, policies, schemas, or expected outputs require a new version. Never silently mutate a benchmark after a model/provider has been evaluated against it.

## Splits

Keep development, validation, regression, and holdout sets separate. Protect holdouts from accidental prompt exposure or tuning. Track generated/synthetic fixtures separately from real-world evidence.

## Principle

Datasets are product code. Aether must be able to explain where a case came from, why it exists, who may use it, and what system behavior it protects.