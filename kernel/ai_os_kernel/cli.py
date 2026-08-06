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
    result = router.route(spec)
    if result.success:
        print(f"=> routed CDL package build to: {result.provider.provider}")
    else:
        print(f"=> NO ROUTE: {result.reason}")
        return 1

    from .artifact_registry import Artifact, ArtifactRegistry
    from .workflow_registry import Workflow, WorkflowRegistry
    from .prompt_graph import GraphNode, PromptGraph

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
    wf.promote()
    print(f"=> workflow '{wf.name}' registered & {wf.status} (order: {graph.order()})")

    artifact = (
        Artifact(
            type="offer_package",
            creator="cdl_package_build",
            workflow=wf.name,
            graph_version=graph.version,
            source="internal synthesis",
            trust=0.9,
            content="CDL AI Automation Retainer — proposal outline (simulated).",
        )
        .seal()
    )
    art_reg = ArtifactRegistry()
    art_reg.add(artifact)
    print(f"=> artifact {artifact.artifact_id[:8]}… sealed; verifies={art_reg.verify(artifact.artifact_id)}")
    return 0


COMMANDS = {
    "capabilities": cmd_capabilities,
    "route": cmd_route,
    "souls": cmd_souls,
    "vertical": cmd_vertical,
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
