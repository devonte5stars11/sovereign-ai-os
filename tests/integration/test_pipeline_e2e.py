"""Full end-to-end pipeline: route -> adapter -> graph -> artifact ->
Obsidian markdown -> (git) -> reflection -> evaluation."""

import os

import pytest
from ai_os_kernel import EvaluationStore, build_default_registry, run_pipeline


def test_pipeline_runs_end_to_end(offline_registry, tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    out = tmp_path / "knowledge"
    ev = tmp_path / "eval.sqlite3"

    result = run_pipeline(
        "A note about fuel saving for CDL owner-operators",
        souls=["main", "cdl-expert"],
        registry=offline_registry,
        output_dir=out,
        eval_path=ev,
        auto_git=False,
    )

    assert result["provider"] == "offline"
    assert result["graph_order"] == ["planner", "writer", "verifier", "aggregator"]

    # artifact was created and is checksummed in an artifact registry
    assert result["artifact_id"]

    # Obsidian markdown exists on disk in the output dir
    note = next(out.glob("*.md"))
    assert note.exists()
    assert "[offline-demo]" in note.read_text(encoding="utf-8")

    # evaluation row was recorded
    store = EvaluationStore(ev)
    assert store.count() >= 1
    store.close()


@pytest.mark.live
def test_pipeline_with_live_key_uses_gemini(tmp_path):
    """Gated: only runs when a real GEMINI_API_KEY is present."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        pytest.skip("GEMINI_API_KEY not set; live adapter test skipped")

    result = run_pipeline(
        "Live pipeline smoke test",
        souls=["main"],
        registry=build_default_registry(),
        output_dir=tmp_path / "knowledge",
        eval_path=tmp_path / "eval.sqlite3",
        auto_git=False,
    )
    assert result["provider"] == "gemini"
    assert result["model"]
