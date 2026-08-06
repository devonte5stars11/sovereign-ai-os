# Sovereign Hermes AI OS — Lobster Empire Edition · v5.1

A personal AI operating system that owns its knowledge permanently
(Markdown + Git + Obsidian), routes every task by **capability and cost**, and
improves itself through Loop-Driven Development (LDD). This repo is the
**Kernel MVP** vertical slice — buildable, testable, and runnable today.

## Quickstart
```bash
cd ai-os
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"   # Windows (git-bash)
# .venv/bin/python -m pip install -e ".[dev]"    # macOS/Linux
.venv/Scripts/python -m pytest -q                 # run the suite (62 tests)
```

## Commands
```bash
# List provider capability manifests (static defaults)
.venv/Scripts/python -m ai_os_kernel.cli capabilities

# Route a task by required capabilities to the cheapest capable provider
.venv/Scripts/python -m ai_os_kernel.cli route long_context vision
.venv/Scripts/python -m ai_os_kernel.cli route browser

# Merge souls into a working profile
.venv/Scripts/python -m ai_os_kernel.cli souls main cdl-expert closer visionary

# Async pipeline (Kernel MVP)
.venv/Scripts/python -m ai_os_kernel.cli vertical

# NEW — provider adapters (dynamic discovery + health)
.venv/Scripts/python -m ai_os_kernel.cli adapters

# NEW — one-shot completion via the active adapter (offline by default)
.venv/Scripts/python -m ai_os_kernel.cli chat "Summarize fleet fuel optimization"

# NEW — full end-to-end milestone pipeline
.venv/Scripts/python -m ai_os_kernel.cli pipeline "How a CDL owner-operator can cut fuel costs"

# NEW — inspect the evaluation database
.venv/Scripts/python -m ai_os_kernel.cli eval
```

## Provider abstraction & live mode
Every provider implements the same `ProviderAdapter` contract
(`kernel/ai_os_kernel/provider.py`): `capabilities()`, `health()`, `complete()`,
`stream()`, `tool_call()`, `embeddings()`. The kernel only ever talks to this
interface — it never knows which provider is executing.

- **Gemini** is the first real adapter (`adapters/gemini.py`), talking to the
  Google Generative Language API with injected transport for testability.
- **Offline** (`adapters/offline.py`) is a credential-free demo adapter.

**Go live** by setting a key and rerunning — no code changes:
```bash
cp .env.example .env        # GEMINI_API_KEY=your_key_here
set -a; source .env; set +a   # load it into the env
.venv/Scripts/python -m ai_os_kernel.cli pipeline "your live task"
```

Capabilities are **discovered dynamically** at runtime (cached with a TTL) via
`CapabilityRegistry` instead of being hardcoded forever — adapters report their
capabilities and health, and those feed routing.

## Testing
```bash
.venv/Scripts/python -m pytest -q            # unit + integration (transport-mocked)
.venv/Scripts/python -m pytest -q -m live    # live API tests (skipped without key)
```

The transport-mocked integration tests exercise the real adapter code path
(request building, response parsing, retry/backoff, streaming, json mode)
against a fake HTTP session — no network or credentials required to run them.

## What's in the box
| Path | Contents |
| ---- | -------- |
| `00-core/` | SOUL, META, design, principles, constitution, maturity model |
| `souls/` | SoulVault — 9 human-readable personality files |
| `profiles/soulvault.yaml` | Souls as composable, data-driven profiles |
| `specs/` | SpecStack — brand / frame / ui |
| `providers/` | Capability manifests: gemini, gpt, grok, local |
| `kernel/ai_os_kernel/` | The Python kernel |
| `graphs/` `graph-registry/` | Prompt graph definitions + workflow registry |
| `memory/` | reflections.md (LDD log) + memory README |
| `tests/` | pytest suite (unit + structure validation) |
| `docs/adr/` | Architecture Decision Records |

## The kernel (`ai_os_kernel`)
- **manifest.py** — provider capability manifests + loader
- **capability_router.py** — routes tasks to cheapest capable provider
- **profiles.py** — SoulVault merges as composable profiles
- **context_packet.py** — standardized context handed to every agent
- **resources.py** — resource budgets + recovery policies
- **prompt_graph.py** — versioned DAGs, topological order, cycle detection
- **workflow_registry.py** — versioned/evaluated workflow library + promotion
- **artifact_registry.py** — typed artifacts with provenance + checksum
- **constitution.py** — the AI Constitution + Policy Engine

## Next steps (the remaining vertical slices)
1. **Knowledge slice** — real capture → clean → link → markdown → git retrieval.
2. **Coding slice** — repo editing, testing, PR creation, artifact logging (OMP).
3. **Creative slice** — asset generation → metadata → knowledge pipeline.
4. **Business slice** — proposal + minimal Next.js product (Product Studio).
5. **Optimization slice** — live evaluation, graph versioning, auto-promotion.

See `docs/architecture.md` and the ADRs in `docs/adr/` for the frozen contract.
