# ADR-0006 — Typed Configuration (Schema Validation)

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Free-form YAML lets bad config (unknown capabilities, negative costs, missing
required fields) surface deep in routing rather than at startup.

## Decision
Every public manifest is validated against a declared vocabulary at load time:
- `ProviderManifest` is checked against the canonical capability set and for
  structural rules (provider/version present, non-negative costs).
- `PromptGraph`/`Workflow` are already validated (cycle detection, dependencies)
  at registration.
- Invalid configuration raises `ManifestError` immediately, at startup, with a
  precise reason.

## Consequences
- Errors are caught early, not mid-run.
- Adding a capability to a provider requires it to be in the known vocabulary.
- Manifest schema is the source of truth for routing.