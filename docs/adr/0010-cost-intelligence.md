# ADR-0010 — Cost Intelligence

- **Status:** Accepted
- **Date:** 2026-08-05

## Context
Costs were logged per run but not aggregated, so there was no way to answer
"what is this *actually* costing me" per provider, workflow, or month.

## Decision
The evaluation store gains a first-class cost-intelligence view:
- `cost_by_provider()`, `cost_by_workflow()`, `cost_by_day()`.
- `monthly_cost(year, month)` and `within_monthly_budget(max)` as a guard.
- `cli eval` reports summary, cost by provider/workflow, and monthly spend.

This turns evaluation data into a budget discipline primitive (Constitution rule 3).

## Consequences
- Spend is visible per provider/workflow/time — the basis for optimizing routing
  by evidence.
- A monthly budget guard exists for autonomous/running systems.
- Independent of any provider pricing API (computed from recorded cost per run).