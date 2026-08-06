"""Command-line entrypoint for the ai_os_kernel.

Demonstrates the Kernel MVP vertical slice end-to-end without needing any real
provider credentials:

    Tasks declare capabilities -> router picks cheapest capable provider
    -> selected souls merge into a profile -> a workflow graph builds a typed,
    checksummed artifact -> the constitution gates it.

Run:  python -m ai_os_kernel.cli
"""

from __future__ import annotations

import sys
from pathlib import Path

from .capability_router import CapabilityRouter, TaskSpec
from .manifest import load_manifests
from .profiles import ProfileManager

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _fmt_manifest(m, indent="  ") -> None:
    print(f"{indent}{m.provider:<10} in=${m.cost_input_per_1k:<10} out=${m.cost_output_per_1k}")
    print(f"{indent}  capabilities: {', '.join(sorted(m.capabilities)) or '(none)'}")


def cmd_capabilities(_: list[str]) -> int:
    for m in load_manifests(REPO_ROOT / "providers"):
        _fmt_manifest(m)
    return 0


def cmd_route(argv: list[str]) -> int:
    caps = argv or ["long_context"]
    router = CapabilityRouter(load_manifests(REPO_ROOT / "providers"))
    result = router.route(TaskSpec(required_capabilities=caps, prefer_local=False))
    print(f"required: {caps}")
    for c in result.candidates:
        print(f"  candidate: {c.provider}")
    if result.success:
        assert result.provider is not None
        print(f"=> routed to: {result.provider.provider}  ({result.reason})")
    else:
        print(f"=> NO ROUTE: {result.reason}")
        print(f"   rejected: {[m.provider for m in result.rejected]}")
    return 0 if result.success else 1


def cmd_souls(argv: list[str]) -> int:
    pm = ProfileManager(REPO_ROOT / "profiles" / "soulvault.yaml")
    names = argv or [pm.names[0]]
    merged = pm.merge(*names)
    print(merged.describe())
    print(f"tool_access: {', '.join(merged.tool_access)}")
    print(f"preferred_capabilities: {', '.join(merged.preferred_capabilities)}")
    return 0


def cmd_vertical(argv: list[str]) -> int:
    """Full vertical slice: route the CDL package build with the right souls."""
    souls = ["main", "cdl-expert", "closer", "visionary"]
    pm = ProfileManager(REPO_ROOT / "profiles" / "soulvault.yaml")
    merged = pm.merge(*souls)
    print(merged.describe())

    router = CapabilityRouter(load_manifests(REPO_ROOT / "providers"))
    spec = TaskSpec(
        required_capabilities=["long_context"],
        preferred_capabilities=merged.preferred_capabilities,
        max_budget_usd=0.02,
    )
    route = router.route(spec)
    if route.success:
        assert route.provider is not None
        print(f"=> routed CDL package build to: {route.provider.provider}")
    else:
        print(f"=> NO ROUTE: {route.reason}")
        return 1

    from .artifact_registry import Artifact, ArtifactRegistry
    from .prompt_graph import GraphNode, PromptGraph
    from .workflow_registry import Workflow, WorkflowRegistry

    graph = (
        PromptGraph(name="cdl_package", version=1)
        .add_node(GraphNode("planner", "planner", "plan the offer"))
        .add_node(GraphNode("domain", "specialist", "CDL domain detail", depends_on=["planner"]))
        .add_node(GraphNode("offer", "aggregator", "package the offer", depends_on=["domain"]))
        .add_node(GraphNode("verifier", "verifier", "check quality", depends_on=["offer"]))
    )
    wf = Workflow(
        name="cdl_package_build",
        graph=graph,
        approval_required=False,
    )
    reg = WorkflowRegistry()
    reg.register(wf)
    wf.mark_validated().stage_candidate()
    print(f"=> workflow '{wf.name}' registered & {wf.status} (order: {graph.order()})")

    artifact = Artifact(
        type="offer_package",
        creator="cdl_package_build",
        workflow=wf.name,
        graph_version=graph.version,
        source="internal synthesis",
        trust=0.9,
        content="CDL AI Automation Retainer — proposal outline (simulated).",
    ).seal()
    art_reg = ArtifactRegistry()
    art_reg.add(artifact)
    print(
        f"=> artifact {artifact.artifact_id[:8]}… sealed; verifies={art_reg.verify(artifact.artifact_id)}"
    )
    return 0


def cmd_adapters(argv: list[str]) -> int:
    from .adapters import GeminiAdapter, OfflineAdapter
    from .capability_registry import AdapterRegistry, CapabilityRegistry

    reg = AdapterRegistry()
    reg.register(OfflineAdapter())
    reg.register(GeminiAdapter())  # always show; health reports key presence
    cap = CapabilityRegistry(reg.all(), ttl_seconds=0)
    for m in cap.refresh():
        adapter = reg.get(m.provider)
        assert adapter is not None
        h = adapter.health()
        print(
            f"{m.provider:<10} ok={h.ok!s:<5} latency={h.latency_ms:.1f}ms "
            f"caps={len(m.capabilities)}"
        )
        if not h.ok and h.error:
            print(f"           health: {h.error}")
    return 0


def cmd_chat(argv: list[str]) -> int:
    from .pipeline import build_default_registry
    from .provider import CompletionRequest, Message

    prompt = " ".join(argv) or "Say hello."
    reg = build_default_registry()
    adapter = reg.all()[0]
    print(
        f"provider: {adapter.name} (mode={'live' if 'GEMINI_API_KEY' in __import__('os').environ else 'offline'})"
    )
    resp = adapter.complete(CompletionRequest(messages=[Message("user", prompt)]))
    if not resp.success:
        print(f"ERROR: {resp.error}")
        return 1
    print(resp.text)
    print(
        f"\n[latency={resp.latency_ms:.0f}ms cost=${resp.cost_usd:.5f} "
        f"tokens={resp.prompt_tokens}/{resp.completion_tokens}]"
    )
    return 0


def cmd_pipeline(argv: list[str]) -> int:
    from .pipeline import run_pipeline

    task = " ".join(argv)
    if not task:
        task = "Sample sovereign note: how a CDL owner-operator can save fuel costs"
    result = run_pipeline(task, souls=["main", "cdl-expert"])
    print("full pipeline complete.")
    for k, v in result.items():
        print(f"  {k:<12} {v}")
    return 0


def cmd_eval(argv: list[str]) -> int:
    from .evaluation_store import EvaluationStore

    store = EvaluationStore(REPO_ROOT / "evaluation" / "eval.sqlite3")
    print("summary:", store.summary())
    print("cost by provider:", store.cost_by_provider())
    print("cost by workflow:", store.cost_by_workflow())
    spend, ok = store.within_monthly_budget(float("inf"))
    print(f"monthly spend: ${spend:.5f} (within budget: {ok})")
    print("recent runs:")
    for r in store.recent(10):
        print(
            f"  #{r['id']} {r['workflow']:<16} {r['provider']:<8} "
            f"{r['latency_ms']:.0f}ms ${r['cost_usd']:.5f} "
            f"ok={bool(r['success'])} retries={r['retries']}"
        )
    store.close()
    return 0


def cmd_events(argv: list[str]) -> int:
    from .events import EventLog

    log = EventLog(REPO_ROOT / "evaluation" / "events.sqlite3")
    for e in log.recent(int(argv[0]) if argv else 20):
        print(
            f"{e.timestamp} [{e.event_type}] corr={e.correlation_id[:8]} "
            f"src={e.source} payload={e.payload}"
        )
    log.close()
    return 0


COMMANDS = {
    "capabilities": cmd_capabilities,
    "route": cmd_route,
    "souls": cmd_souls,
    "vertical": cmd_vertical,
    "adapters": cmd_adapters,
    "chat": cmd_chat,
    "pipeline": cmd_pipeline,
    "eval": cmd_eval,
    "events": cmd_events,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("Usage: python -m ai_os_kernel.cli <command> [args...]")
        print("Commands: " + ", ".join(COMMANDS))
        print("  e.g. route long_context vision ; souls main cdl_expert ; vertical")
        return 0
    cmd, *rest = argv
    fn = COMMANDS.get(cmd)
    if fn is None:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    return fn(rest)


if __name__ == "__main__":
    raise SystemExit(main())
