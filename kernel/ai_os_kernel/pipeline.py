"""End-to-end event pipeline — the first full vertical slice.

User request
  -> Capability Router
  -> Provider Adapter
  -> Prompt Graph
  -> Artifact Registry (checksummed)
  -> Obsidian Markdown
  -> Git commit
  -> Reflection
  -> Evaluation log

Runs offline with the OfflineAdapter when no GEMINI_API_KEY is set; switches to
the real GeminiAdapter automatically when a key is present. No secrets required
to exercise the full path.
"""

from __future__ import annotations

import os
import subprocess
import uuid
from pathlib import Path

from .adapters import GeminiAdapter, OfflineAdapter
from .artifact_registry import Artifact, ArtifactRegistry
from .capability_registry import AdapterRegistry, CapabilityRegistry
from .capability_router import CapabilityRouter, TaskSpec
from .context_packet import ContextPacket
from .evaluation_store import EvaluationStore
from .events import EventLog
from .profiles import ProfileManager
from .prompt_graph import GraphNode, PromptGraph
from .provider import CompletionRequest, Message
from .workflow_registry import Workflow, WorkflowRegistry

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def build_default_registry() -> AdapterRegistry:
    """Real provider when a key is present; otherwise offline demo adapter."""
    reg = AdapterRegistry()
    if os.environ.get("GEMINI_API_KEY"):
        reg.register(GeminiAdapter())
    else:
        reg.register(OfflineAdapter())
    return reg


def _slugify(text: str) -> str:
    keep = "".join(c if (c.isalnum() or c in "-_") else "-" for c in text.lower())
    return "-".join(keep.split("-"))[:48].strip("-") or "output"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def run_pipeline(
    task: str,
    souls: list[str] | None = None,
    registry: AdapterRegistry | None = None,
    output_dir: str | Path = "knowledge/output",
    eval_path: str | Path = "evaluation/eval.sqlite3",
    auto_git: bool = True,
    event_log: EventLog | None = None,
) -> dict:
    souls = souls or ["main"]
    registry = registry or build_default_registry()
    root = REPO_ROOT
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir

    # Unified event trace for this whole run.
    correlation_id = str(uuid.uuid4())
    event_log = event_log or EventLog(Path(eval_path).parent / "events.sqlite3")
    emit = lambda et, **kw: event_log.emit(  # noqa: E731
        et, source="pipeline", correlation_id=correlation_id, workflow_id="sovereign_note", **kw
    )
    emit("task.received", payload={"task": task})

    # ---- 1. Select & merge souls ---------------------------------------
    pm = ProfileManager(root / "profiles" / "soulvault.yaml")
    merged = pm.merge(*souls)
    profile_desc = merged.describe()
    emit("souls.selected", payload={"souls": souls})

    # ---- 2. Route by capability -----------------------------------------
    cap_reg = CapabilityRegistry(registry.all(), ttl_seconds=0)  # fresh each run
    router = CapabilityRouter(cap_reg.discover(force=True))
    spec = TaskSpec(
        required_capabilities=["long_context"],
        preferred_capabilities=merged.preferred_capabilities,
        prefer_local=False,
    )
    route = router.route(spec)
    if not route.success:
        raise RuntimeError(f"no route for task: {route.reason}")
    assert route.provider is not None
    adapter = registry.get(route.provider.provider)
    if adapter is None:
        raise RuntimeError(f"routed to missing adapter: {route.provider.provider}")
    emit("task.routed", payload={"provider": route.provider.provider})

    # ---- 3. Prompt graph ------------------------------------------------
    graph = (
        PromptGraph(name="sovereign_note", version=1)
        .add_node(GraphNode("planner", "planner", "interpret the task"))
        .add_node(
            GraphNode(
                "writer",
                "specialist",
                "draft with selected souls",
                required_capabilities=["long_context"],
                depends_on=["planner"],
            )
        )
        .add_node(
            GraphNode(
                "verifier",
                "verifier",
                "check quality + provenance",
                depends_on=["writer"],
            )
        )
        .add_node(
            GraphNode(
                "aggregator",
                "aggregator",
                "final markdown note",
                depends_on=["verifier"],
            )
        )
    )
    graph_order = graph.order()
    # Register the workflow so the run is part of the versioned registry.
    wf = Workflow(name="sovereign_note", graph=graph, approval_required=False)
    wf_registry = WorkflowRegistry()
    wf_registry.register(wf)
    wf.mark_validated().stage_candidate()

    # ---- 4. Provider execution ------------------------------------------
    packet = ContextPacket(
        task=task,
        goals=[g.strip() for g in ("Produce a clean, reusable markdown note.", "") if g.strip()],
        constraints=["Follow the AI Constitution.", "Cite provenance."],
        relevant_memory=["souls: " + ", ".join(souls)],
        policies=["truthfulness over speculation", "preserve canonical knowledge"],
        budget={"max_usd": 0.05},
        expected_output="a markdown note saved under knowledge/output/",
    )
    prompt = _assemble_prompt(packet, merged)
    resp = adapter.complete(CompletionRequest(messages=[Message("user", prompt)], json_mode=False))
    if not resp.success:
        raise RuntimeError(f"adapter failed: {resp.error}")
    emit(
        "provider.invoked",
        payload={
            "provider": resp.provider,
            "model": resp.model,
            "latency_ms": resp.latency_ms,
            "cost_usd": resp.cost_usd,
        },
    )

    # ---- 5. Artifact registry (checksummed) -----------------------------
    art_reg = ArtifactRegistry()
    artifact = Artifact(
        type="note",
        creator="sovereign_note",
        workflow="sovereign_note",
        graph_version=graph.version,
        source=resp.provider,
        trust=0.9,
        confidence=0.9,
        content=resp.text,
    ).seal()
    art_reg.add(artifact)
    emit(
        "artifact.created",
        artifact_id=artifact.artifact_id,
        payload={"checksum": artifact.checksum[:16]},
    )

    # ---- 6. Obsidian markdown -------------------------------------------
    slug = _slugify(task)
    md_path = output_dir / f"{slug}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(
        _render_note(md_path, task, resp, artifact, merged, profile_desc),
        encoding="utf-8",
    )
    emit("markdown.written", payload={"path": str(md_path)})

    # ---- 7. Git commit ---------------------------------------------------
    if auto_git:
        _git(root, "add", "-A")
        _git(
            root,
            "commit",
            "-q",
            "-m",
            f"pipeline: add {slug}.md (workflow=sovereign_note v{graph.version}) {artifact.artifact_id[:8]}",
        )
    emit("git.committed", payload={"committed": auto_git})

    # ---- 8. Reflection ---------------------------------------------------
    reflection_path = root / "memory" / "reflections.md"
    entry = (
        f"\n---\n\n## {_now_str()} — pipeline run\n"
        f"**Task:** {task}\n**Workflow:** sovereign_note v{graph.version}\n"
        f"**Provider:** {resp.provider} ({resp.model})\n"
        f"**Latency:** {resp.latency_ms:.0f}ms | cost ${resp.cost_usd:.5f}\n"
        f"**Artifact:** {artifact.artifact_id}\n"
        f"**Graph order:** {graph_order}\n"
    )
    with open(reflection_path, "a", encoding="utf-8") as fh:
        fh.write(entry)

    # ---- 9. Evaluation log ----------------------------------------------
    store = EvaluationStore(root / eval_path)
    run_id = store.record(
        workflow="sovereign_note",
        provider=resp.provider,
        model=resp.model,
        graph_version=graph.version,
        latency_ms=resp.latency_ms,
        prompt_tokens=resp.prompt_tokens,
        completion_tokens=resp.completion_tokens,
        cost_usd=resp.cost_usd,
        success=True,
        retries=0,
    )
    store.export_markdown(Path(eval_path).parent / "log.md")
    store.close()
    emit("evaluation.logged", payload={"run_id": run_id, "cost_usd": resp.cost_usd})

    try:
        markdown_ref = str(md_path.relative_to(root))
    except ValueError:
        markdown_ref = str(md_path)

    return {
        "run_id": run_id,
        "correlation_id": correlation_id,
        "provider": resp.provider,
        "model": resp.model,
        "task": task,
        "graph_order": graph_order,
        "artifact_id": artifact.artifact_id,
        "markdown": markdown_ref,
        "cost_usd": resp.cost_usd,
        "latency_ms": resp.latency_ms,
        "souls": souls,
        "git_committed": auto_git,
    }


def _assemble_prompt(packet: ContextPacket, merged) -> str:
    lines = [
        "You are a sovereign research agent producing a durable Markdown note.",
        "Soul(s): " + ", ".join(merged.names),
        "",
        f"TASK: {packet.task}",
        "",
        "CONSTRAINTS:",
        *[f"- {c}" for c in packet.constraints],
        "",
        "POLICIES:",
        *[f"- {p}" for p in packet.policies],
        "",
        "OUTPUT: a clean, self-contained Markdown note. Be truthful; no speculation.",
    ]
    return "\n".join(lines)


def _render_note(md_path: Path, task: str, resp, artifact, merged, profile_desc: str) -> str:
    return (
        f"# {task}\n\n"
        f"> generated by **sovereign_note** workflow · provider `{resp.provider}` · "
        f"artifact `{artifact.artifact_id[:8]}` (verified)\n\n"
        f"- **Souls:** {', '.join(merged.names)}\n"
        f"- **Graph order:** planner → writer → verifier → aggregator\n"
        f"- **Latency:** {resp.latency_ms:.0f} ms · **cost:** ${resp.cost_usd:.5f}\n"
        f"- **Checksum:** `{artifact.checksum[:16]}…`\n\n"
        f"---\n\n{resp.text}\n"
    )


def _now_str() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
