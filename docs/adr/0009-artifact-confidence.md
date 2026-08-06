# ADR-0009 — Artifact Confidence & Freshness

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Artifacts carried a single `trust` value. Long-lived knowledge needs richer
signals: how confident are we, is it still fresh, who verified it, when does it
expire.

## Decision
Artifacts extend provenance with a knowledge-confidence model:
- `confidence` (0..1) — how confident we are in the content.
- `freshness` (ISO) — last reviewed/refreshed timestamp.
- `verified_by` — the actor that verified it ("human", an evaluator, etc.).
- `expiry` (ISO) — optional; `is_expired` detects past expiry.
- `mark_verified(by)` stamps freshness + verifier.

Checksums and IDs remain; confidence is orthogonal metadata for routing and
retention.

## Consequences
- Retrieval and knowledge-lifecycle policy can rank by confidence + freshness.
- Expiring artifacts can be flagged for re-verification or archival.