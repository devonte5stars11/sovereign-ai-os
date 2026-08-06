# Demo — running the Sovereign AI OS kernel

These are **real** captured outputs from the running kernel (offline mode — no
credentials required). To reproduce: `pip install -e ".[dev]"` then run the
commands below.

## 1. Provider capability manifests

```console
$ python -m ai_os_kernel.cli capabilities
  gemini     in=$2e-06      out=$8e-06
    capabilities: audio, code_execution, file_editing, image_generation, json_mode, long_context, streaming, tool_calling, vision
  gpt        in=$2.5e-06    out=$1e-05
    capabilities: audio, code_execution, computer_use, file_editing, image_generation, json_mode, long_context, streaming, tool_calling, vision
  grok       in=$3e-06      out=$1.5e-05
    capabilities: browser, code_execution, file_editing, json_mode, long_context, streaming, tool_calling, vision
  local      in=$0.0        out=$0.0
    capabilities: json_mode, local, streaming
```

## 2. Capability-based routing (no model names)

```console
$ python -m ai_os_kernel.cli route long_context vision
required: ['long_context', 'vision']
  candidate: gemini
  candidate: gpt
  candidate: grok
=> routed to: gemini  (cheapest capable provider)

$ python -m ai_os_kernel.cli route browser
required: ['browser']
  candidate: grok
=> routed to: grok  (cheapest capable provider)
```

## 3. Dynamic adapter discovery + health

```console
$ python -m ai_os_kernel.cli adapters
offline    ok=True  latency=1.0ms caps=3
gemini     ok=False latency=0.0ms caps=7
           health: no GEMINI_API_KEY configured
```

`offline` is healthy and ready; `gemini` reports its capabilities immediately but
its health reflects the missing key. Set `GEMINI_API_KEY` and it flips to live —
no code changes.

## 4. One-shot completion (offline)

```console
$ python -m ai_os_kernel.cli chat "Summarize fleet fuel optimization"
provider: offline (mode=offline)
[offline-demo] received 1 message(s). Echoing user prompt: Summarize fleet fuel optimization

[latency=0ms cost=$0.00000 tokens=0/11]
```

## 5. Full end-to-end pipeline

```console
$ python -m ai_os_kernel.cli pipeline "How a CDL owner-operator can cut fuel costs"
full pipeline complete.
  run_id       1
  provider     offline
  model        offline-demo
  task         How a CDL owner-operator can cut fuel costs
  graph_order  ['planner', 'writer', 'verifier', 'aggregator']
  artifact_id  340abfc7-2055-40b5-9d8f-8c2a5ac77906
  markdown     knowledge\output\how-a-cdl-owner-operator-can-cut-fuel-costs.md
  cost_usd     0.0
  latency_ms   0.003
  souls        ['main', 'cdl-expert']
  git_committed True
```

The generated note (checksummed, artefacts provenance) is committed, a reflection
is appended to `memory/reflections.md`, and an evaluation row is logged:

```console
$ python -m ai_os_kernel.cli eval
summary: {'runs': 1, 'avg_latency_ms': 0.0, 'total_cost_usd': 0.0, 'failures': 0, 'total_retries': 0}
recent runs:
  #1 sovereign_note    offline   0ms $0.00000 ok=True retries=0
```

## 6. Test suite

```console
$ python -m pytest -q
93 passed, 1 skipped in 1.55s     # 1 skipped = live Gemini test (no key)
```

## Going live

```bash
cp .env.example .env        # GEMINI_API_KEY=your_key_here
set -a; source .env; set +a
python -m ai_os_kernel.cli pipeline "any real task"    # now uses GeminiAdapter
python -m pytest -q -m live                            # live integration tests
```
