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
# List provider capability manifests
.venv/Scripts/python -m ai_os_kernel.cli capabilities

# Route a task by required capabilities to the cheapest capable provider
.venv/Scripts/python -m ai_os_kernel.cli route long_context vision
.venv/Scripts/python -m ai_os_kernel.cli route browser

# Merge souls into a working profile
.venv/Scripts/python -m ai_os_kernel.cli souls main cdl-expert closer visionary

# Run the end-to-end vertical slice (no live provider needed)
.venv/Scripts/python -m ai_os_kernel.cli vertical
```

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
