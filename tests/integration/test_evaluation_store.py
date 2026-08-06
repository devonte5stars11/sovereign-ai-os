"""EvaluationStore: durable per-run metrics + markdown mirror."""

import pytest
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


def test_cost_by_provider_and_workflow(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("wfA", "gemini", cost_usd=0.5)
    store.record("wfA", "offline", cost_usd=0.1)
    store.record("wfB", "gemini", cost_usd=0.2)
    assert store.cost_by_provider()["gemini"] == pytest.approx(0.7)
    assert store.cost_by_workflow()["wfA"] == pytest.approx(0.6)


def test_monthly_cost_and_budget(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("wf", "x", cost_usd=2.0)
    spend, ok = store.within_monthly_budget(10.0)
    assert spend >= 2.0
    assert ok is True
    _, not_ok = store.within_monthly_budget(1.0)
    assert not_ok is False


def test_cost_by_day(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("wf", "x", cost_usd=1.5)
    days = store.cost_by_day(7)
    assert len(days) >= 1
    assert sum(days.values()) == pytest.approx(1.5)


def test_export_markdown(tmp_path):
    store = EvaluationStore(tmp_path / "eval.sqlite3")
    store.record("wf", "offline", latency_ms=5, cost_usd=0.0)
    out = store.export_markdown(tmp_path / "log.md")
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "# Evaluation Log" in text
    assert "| id |" in text
