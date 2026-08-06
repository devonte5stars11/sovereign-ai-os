# Contributing

Thanks for your interest in **Sovereign AI OS**. The architecture is deliberately
**frozen** — most valuable work happens in isolated, testable slices, not by
expanding the conceptual model.

## Ground rules

1. **Architecture changes need an ADR.** If you want to change the frozen
   reference architecture, first add an Architecture Decision Record under
   `docs/adr/` and get agreement before coding.
2. **Adapters and plugins are the only extension points.** New providers,
   tools, and integrations enter through adapters/plugins — never by editing the
   kernel's routing or planning.
3. **Everything you add ships with tests.** We keep a coverage gate ≥ 80% and a
   green CI.
4. **Keep knowledge vendor-independent.** No data model should assume a specific
   provider.

## Setup

```bash
git clone https://github.com/devonte5stars11/sovereign-ai-os.git
cd sovereign-ai-os
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"
```

## Before you submit

Run the same gates CI runs:

```bash
ruff format .                    # then ruff format --check .
ruff check .
pytest --cov=ai_os_kernel --cov-fail-under=80 -q
bandit -r kernel/ai_os_kernel    # advisory
```

If your change touches a provider, add transport-mocked integration tests under
`tests/integration/` (see `tests/integration/conftest.py` for the `FakeSession`
helpers) and, where appropriate, a live toggle using the `live` marker.

## Adding a provider

1. Write your manifest under `providers/<name>.yaml`.
2. Implement `ProviderAdapter` in `kernel/ai_os_kernel/adapters/<name>.py` —
   match the shape of `adapters/gemini.py`.
3. Register it in an `AdapterRegistry`.
4. Add capability tests + mocked integration tests. Wire live-mode via an env var.

## Issues & PRs

- Use clear, single-purpose PRs.
- Reference the issue or ADR your change addresses.
- Keep the README/status table in sync if you add a component.
