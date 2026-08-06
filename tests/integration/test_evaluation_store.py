"""EvaluationStore: durable per-run metrics + markdown mirror."""

from ai_os_kernel import EvaluationStore


def test_record_and_count(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("wf", "offline", cost_usd=0.001, latency_ms=10.0, success=True)
    store.record("wf", "offline", cost_usd=0.002, latency_ms=20.0, success=False, retries=1)
    assert store.count() == 2


def test_summary_aggregates(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("a", "x", latency_ms=10, cost_usd=0.5, success=True)
    store.record("a", "x", latency_ms=30, cost_usd=0.5, success=False, retries=2)
    s = store.summary()
    assert s["runs"] == 2
    assert s["avg_latency_ms"] == 20.0
    assert s["total_cost_usd"] == 1.0
    assert s["failures"] == 1
    assert s["total_retries"] == 2


def test_rate_run(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    rid = store.record("wf", "offline")
    store.rate(rid, 4.5)
    assert store.recent(1)[0]["human_rating"] == 4.5


def test_export_markdown(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("wf", "offline", latency_ms=5, cost_usd=0.0)
    out = store.export_markdown(tmp_path / "log.md")
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "# Evaluation Log" in text
    assert "| id |" in text
