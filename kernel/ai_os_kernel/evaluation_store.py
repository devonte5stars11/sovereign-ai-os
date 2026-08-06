"""Evaluation store — records per-execution metrics.

Once real providers run, capture: graph version, provider, latency, tokens,
cost, success, retries, human rating. SQLite-backed (stdlib, durable); a
markdown mirror keeps the data human-readable in the knowledge store.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    workflow TEXT NOT NULL,
    graph_version INTEGER DEFAULT 0,
    provider TEXT,
    model TEXT,
    latency_ms REAL,
    prompt_tokens INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0,
    success INTEGER DEFAULT 1,
    retries INTEGER DEFAULT 0,
    human_rating REAL
);
"""


class EvaluationStore:
    """Durable store of workflow execution metrics."""

    def __init__(self, path: str | Path = "evaluation/eval.sqlite3"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.execute(_SCHEMA)

    def record(self, workflow: str, provider: str, *, graph_version: int = 0,
               model: str = "", latency_ms: float = 0.0, prompt_tokens: int = 0,
               completion_tokens: int = 0, cost_usd: float = 0.0,
               success: bool = True, retries: int = 0) -> int:
        cur = self._conn.execute(
            """INSERT INTO runs (ts, workflow, graph_version, provider, model,
               latency_ms, prompt_tokens, completion_tokens, cost_usd, success, retries)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (_now(), workflow, graph_version, provider, model, latency_ms,
             prompt_tokens, completion_tokens, cost_usd, int(success), retries),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def rate(self, run_id: int, rating: float) -> None:
        self._conn.execute("UPDATE runs SET human_rating=? WHERE id=?",
                           (rating, run_id))
        self._conn.commit()

    def recent(self, limit: int = 20) -> List[Dict]:
        rows = self._conn.execute(
            "SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = [c[0] for c in self._conn.execute("SELECT * FROM runs LIMIT 0").description]
        return [dict(zip(cols, r)) for r in rows]

    def summary(self) -> Dict:
        row = self._conn.execute(
            """SELECT COUNT(*) AS runs,
                      AVG(latency_ms) AS avg_latency_ms,
                      SUM(cost_usd) AS total_cost_usd,
                      SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) AS failures,
                      SUM(retries) AS total_retries
               FROM runs"""
        ).fetchone()
        cols = [c[0] for c in self._conn.execute(
            "SELECT COUNT(*) AS runs, AVG(latency_ms) AS avg_latency_ms, "
            "SUM(cost_usd) AS total_cost_usd, "
            "SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) AS failures, "
            "SUM(retries) AS total_retries FROM runs LIMIT 0").description]
        return dict(zip(cols, row or (0, 0, 0, 0, 0)))

    def count(self) -> int:
        return int(self._conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0])

    def export_markdown(self, path: str | Path) -> Path:
        """Write a human-readable markdown mirror of recent runs."""
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# Evaluation Log\n", ""]
        lines.append("| id | ts | workflow | provider | latency_ms | cost_usd | ok | retries | rating |")
        lines.append("|----|----|----------|----------|-----------:|--------:|:--:|-------:|-------:|")
        for r in self.recent():
            rating = f"{r['human_rating']:.1f}" if r["human_rating"] is not None else "-"
            lines.append(
                f"| {r['id']} | {r['ts']} | {r['workflow']} | {r['provider']} | "
                f"{r['latency_ms']:.0f} | {r['cost_usd']:.5f} | "
                f"{'ok' if r['success'] else 'FAIL'} | {r['retries']} | {rating} |"
            )
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return out

    def close(self) -> None:
        self._conn.close()
