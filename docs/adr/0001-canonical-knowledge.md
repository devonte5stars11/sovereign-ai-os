# ADR-0001 — Markdown + Git + Obsidian as Canonical Knowledge

- **Status:** Accepted
- **Date:** 2026-08-05
- **Deciders:** Empire owner / kernel architect

## Context
Proprietary chat histories are a poor long-term store: they are siloed,
unportable, and not versionable. Knowledge must outlive any single provider.

## Decision
Markdown is the canonical human-readable format. Git provides versioning and
history. Obsidian is the human-facing workspace. Everything else (knowledge
graph, vector index, artifact store, metadata DB) is a synchronized *view* of
this store, never an independent source of truth.

## Consequences
- Knowledge remains **vendor-independent** and portable.
- Hermes is the **orchestrator**, never the permanent memory store.
- Synchronization between views is an engineering responsibility.
