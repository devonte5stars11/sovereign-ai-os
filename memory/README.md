# memory/ — Time-Horizon Memory

Memory is treated as a database, not files. Markdown is the canonical
human-readable format; internally it supports multiple synchronized views.

## Time horizons
| Horizon | Scope | Retention policy |
| ------- | ----- | ---------------- |
| Working | current task | discarded after task |
| Project | active projects / clients | until project closes |
| Evergreen | durable knowledge | permanent, curated |
| Archive  | cold data               | permanent, de-indexed |

## reflections.md
The LDD evolution log. After every meaningful workflow, record:
- what was run (workflow + graph version)
- metrics (latency, cost, success, retries)
- what worked / what didn't
- the proposed graph/policy revision (→ next candidate)

A seed template lives at `memory/reflections.md`.
