<div align="center">

# Sovereign AI OS

**A provider-agnostic AI operating system** for orchestration, knowledge management,
workflow execution, and product delivery.

Capability-based routing · versioned Prompt Graph workflows · provider abstraction ·
artifact provenance · evaluation pipeline · Obsidian/Git knowledge ownership

[![CI](https://github.com/devonte5stars11/sovereign-ai-os/actions/workflows/ci.yml/badge.svg)](https://github.com/devonte5stars11/sovereign-ai-os/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![tests](https://img.shields.io/badge/tests-93%20passing-brightgreen)
![coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Why this exists

Most AI "systems" are one model wrapper. This is an **operating system around
models** — it treats knowledge, routing, workflows, and providers as first-class
concerns so no vendor, workflow, or idea is ever trapped. It was built as the
kernel of a personal AI agency serving HVAC/plumbing contractors and CDL/trucking
operators, but the architecture is fully generic.

**The core bet:** every task is routed by *capability* (need `vision`? need
`browser`? need to stay cheap?), never by hardcoded model name. Add or replace a
provider → drop in an adapter → routing adapts automatically.

## Highlights

- **Capability-based routing** — the cheapecapable provider wins, no model names in router logic
- **Provider abstraction** — same `ProviderAdapter` interface for Gemini, GPT, Grok, local; kernel never knows the vendor
- **Runtime capability discovery** — adapters *report* their capabilities (TTL-cached), not hardcoded manifests
- **Versioned Prompt Graph workflows** — G1–G4 DAGs with cycle detection, promotion, and evaluation
- **Artifact registry** — every output is typed, checksummed, and provenanced (reproducible)
- **SQLite evaluation database** — latency, cost, tokens, success, retries drive routing policy with evidence
- **End-to-end pipeline** — request → route → adapter → graph → artifact → Obsidian markdown → git commit → reflection → evaluation
- **AI Constitution + Policy Engine** — cost discipline and approval gates enforced at runtime
- **Integration-tested kernel** — 93 tests incl. transport-mocked adapter/retry/streaming coverage, with live-mode toggle

## Status

| Component              | Status     |
| ---------------------- | ---------- |
| Kernel                 | ✅         |
| Provider abstraction   | ✅         |
| Capability router      | ✅         |
| Prompt Graph engine    | ✅         |
| Dynamic capability discovery | ✅  |
| Artifact registry      | ✅         |
| Evaluation pipeline    | ✅         |
| Gemini adapter         | ✅         |
| Offline mode           | ✅         |
| CI (lint/test/coverage)| ✅         |
| Additional providers   | 🚧 planned |
| Knowledge graph/vector | 🚧 planned |

## Architecture

```
YOU
 │
 Experience Layer (Voice • Web • Dashboards • Human Modes)
 │
 Hermes Kernel
   Planner · Capability Router · Prompt Graph Engine (G1–G4)
   Memory Manager · Scheduler + Budgets · Policy Engine + AI Constitution
   Workflow Registry · Capability Registry
 │
 Multi-Agent Organization (SoulVault as composable profiles)
 │
 Execution & Service Layer (MCP · REST · SDKs · Browser · Git · Docker · Service Discovery)
 │
 Provider Adapter Layer (each publishes a capability manifest + capability tests)
 │
 Knowledge Pipeline + Artifact Registry
   Capture → Clean → Verify → Link → Graph ↔ Vector ↔ Artifact ↔ Metadata
   → Markdown → Git → Backups
 │
 Permanent Knowledge (Obsidian as the human-readable view)
```

## Quick start

```bash
git clone https://github.com/devonte5stars11/sovereign-ai-os.git
cd sovereign-ai-os
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"     # Windows (git-bash)
# .venv/bin/python -m pip install -e ".[dev]"       # macOS / Linux
.venv/Scripts/python -m pytest -q                    # run the suite
```

**Runs fully offline** — the `OfflineAdapter` needs zero credentials, so the whole
system (routing, pipeline, artifacts, evaluation) works out of the box.

**Go live** — set a key and rerun, no code changes:

```bash
cp .env.example .env        # GEMINI_API_KEY=your_key_here
set -a; source .env; set +a
.venv/Scripts/python -m ai_os_kernel.cli pipeline "your live task"
```

## CLI

```bash
.venv/Scripts/python -m ai_os_kernel.cli capabilities      # static provider manifests
.venv/Scripts/python -m ai_os_kernel.cli route vision       # route by capability
.venv/Scripts/python -m ai_os_kernel.cli souls main cdl-expert  # merge souls
.venv/Scripts/python -m ai_os_kernel.cli adapters           # dynamic discovery + health
.venv/Scripts/python -m ai_os_kernel.cli chat "message"     # one-shot completion
.venv/Scripts/python -m ai_os_kernel.cli pipeline "task"    # full end-to-end pipeline
.venv/Scripts/python -m ai_os_kernel.cli eval               # evaluation database
```

## Repository layout

```
ai-os/
├── 00-core/          mission, design, principles, constitution, maturity model
├── souls/            SoulVault — human-readable personality files
├── profiles/         souls as composable, data-driven profiles (YAML)
├── specs/            SpecStack — brand / frame / ui
├── providers/        capability manifests (gemini, gpt, grok, local)
├── graphs/           prompt graph definitions (G1–G4)
├── kernel/           the Python kernel (ai_os_kernel)
│   └── ai_os_kernel/
│       ├── provider.py            ProviderAdapter contract + transport
│       ├── adapters/              GeminiAdapter, OfflineAdapter
│       ├── capability_router.py   cheapest-capable routing
│       ├── capability_registry.py runtime discovery + cache
│       ├── prompt_graph.py        versioned DAGs
│       ├── workflow_registry.py   versioned, evaluated workflows
│       ├── artifact_registry.py   checksummed artifacts
│       ├── evaluation_store.py    SQLite metrics
│       ├── constitution.py        AI Constitution + policy engine
│       └── pipeline.py            end-to-end execution
├── tests/            unit + integration (transport-mocked) + live-toggle
├── docs/             architecture, ADRs, demo
└── .github/workflows CI
```

## Testing & quality gates

```bash
ruff format --check .        # formatting
ruff check .                 # linting
pytest --cov=ai_os_kernel --cov-fail-under=80 -q   # tests + coverage gate
bandit -r kernel/ai_os_kernel # advisory security scan
pytest -q -m live            # live API tests (needs GEMINI_API_KEY)
```

All gates run automatically in CI on every push/PR across Python 3.10–3.12.

## Roadmap

- [x] Kernel MVP + provider abstraction + Gemini/offline adapters
- [ ] Additional adapters (GPT, Grok, local)
- [ ] Knowledge slice — capture → clean → link → markdown → git → retrieval
- [ ] Coding slice — repo editing, PR creation, artifact logging
- [ ] Creative slice — asset generation → metadata → knowledge pipeline
- [ ] Business slice — proposal + minimal product (Product Studio)
- [ ] Optimization slice — live evaluation, graph auto-promotion
- [ ] Knowledge graph + vector index (multi-view memory)

## License & docs

- [Architecture](docs/architecture.md) · [ADRs](docs/adr/) · [Demo](docs/DEMO.md)
- MIT — see [LICENSE](LICENSE) · Contributions welcome — see [CONTRIBUTING](CONTRIBUTING.md)
