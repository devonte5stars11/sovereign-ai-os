# ADR-0004 — Souls as Data-Driven Composable Profiles

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Treating each "soul" (personality) as a separate hard-coded personality is
inflexible and hard to compose.

## Decision
The user-facing **SoulVault** metaphor remains for ergonomics (files in
`souls/*.md`), but the implementation is **data-driven composable profiles**
(`profiles/soulvault.yaml`): each soul is a profile with role, domain,
authority, tool_access, prompt_overlays, evaluation_rules, and
preferred_capabilities. Multiple selected souls merge per declared merge rules
(authority=max, tool_access=union, preferred_capabilities=union, etc.).

## Consequences
- Souls compose cleanly (CEO + CDL Expert + Closer + Visionary).
- No personality-switching code paths; profiles are just data.
