# ADR-0002 — Capability-Based Routing

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Routing by hardcoded model names breaks whenever providers release new models
or change capabilities.

## Decision
Providers publish machine-readable **capability manifests** (`providers/*.yaml`)
describing capabilities, cost, and limits. Tasks declare **required
capabilities**; the `CapabilityRouter` selects the cheapest provider whose
manifest satisfies every requirement, optionally honoring `prefer_local` and
preferred capabilities. Capability tests periodically re-verify manifests so
routing decisions stay accurate.

## Consequences
- New providers = new manifest; **no routing-code changes**.
- Cost discipline is enforced centrally.
- Requires every provider to keep its manifest + capability tests current.
