"""Unified event schema + durable event log.

Every subsystem (graphs, providers, tools, plugins, the pipeline) emits the
*same* canonical event structure. A single correlation_id traces a whole run,
which makes replay, debugging, analytics, monitoring, and audit dramatically
easier.

Canonical fields (see ADR-0007):
    event_id, event_type, source, timestamp, actor, correlation_id,
    workflow_id, artifact_id, payload, metadata
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL,
    source TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    actor TEXT,
    correlation_id TEXT,
    workflow_id TEXT,
    artifact_id TEXT,
    payload TEXT,
    metadata TEXT
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


@dataclass
class Event:
    """The single canonical event format shared by the whole system."""

    event_type: str
    source: str
    actor: str = ""
    correlation_id: str = ""
    workflow_id: str = ""
    artifact_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "correlation_id": self.correlation_id,
            "workflow_id": self.workflow_id,
            "artifact_id": self.artifact_id,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        return cls(
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
            actor=data.get("actor", ""),
            correlation_id=data.get("correlation_id", ""),
            workflow_id=data.get("workflow_id", ""),
            artifact_id=data.get("artifact_id", ""),
            payload=data.get("payload", {}) or {},
            metadata=data.get("metadata", {}) or {},
            event_id=data.get("event_id", ""),
            timestamp=data.get("timestamp", ""),
        )


class EventLog:
    """Durable, append-only store of canonical events."""

    def __init__(self, path: str | Path = "evaluation/events.sqlite3"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.execute(_SCHEMA)

    def emit(
        self,
        event_type: str,
        source: str,
        *,
        actor: str = "",
        correlation_id: str = "",
        workflow_id: str = "",
        artifact_id: str = "",
        payload: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Event:
        """Create and persist an event; returns the stored event."""
        event = Event(
            event_type=event_type,
            source=source,
            actor=actor,
            correlation_id=correlation_id,
            workflow_id=workflow_id,
            artifact_id=artifact_id,
            payload=payload or {},
            metadata=metadata or {},
        )
        self._conn.execute(
            """INSERT INTO events (event_id, event_type, source, timestamp, actor,
               correlation_id, workflow_id, artifact_id, payload, metadata)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                event.event_id,
                event.event_type,
                event.source,
                event.timestamp,
                event.actor,
                event.correlation_id,
                event.workflow_id,
                event.artifact_id,
                json.dumps(event.payload),
                json.dumps(event.metadata),
            ),
        )
        self._conn.commit()
        return event

    def count(self) -> int:
        return int(self._conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])

    def recent(self, limit: int = 50) -> list[Event]:
        rows = self._conn.execute(
            "SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = [c[0] for c in self._conn.execute("SELECT * FROM events LIMIT 0").description]
        events = []
        for r in rows:
            d = dict(zip(cols, r, strict=False))
            d["payload"] = json.loads(d["payload"] or "{}")
            d["metadata"] = json.loads(d["metadata"] or "{}")
            events.append(Event.from_dict(d))
        return events

    def by_correlation(self, correlation_id: str) -> list[Event]:
        """All events for one run, in emission order (perfect for replay/tracing)."""
        rows = self._conn.execute(
            "SELECT * FROM events WHERE correlation_id=? ORDER BY id ASC",
            (correlation_id,),
        ).fetchall()
        cols = [c[0] for c in self._conn.execute("SELECT * FROM events LIMIT 0").description]
        events = []
        for r in rows:
            d = dict(zip(cols, r, strict=False))
            d["payload"] = json.loads(d["payload"] or "{}")
            d["metadata"] = json.loads(d["metadata"] or "{}")
            events.append(Event.from_dict(d))
        return events

    def by_type(self, event_type: str, limit: int = 100) -> list[Event]:
        rows = self._conn.execute(
            "SELECT * FROM events WHERE event_type=? ORDER BY id DESC LIMIT ?",
            (event_type, limit),
        ).fetchall()
        cols = [c[0] for c in self._conn.execute("SELECT * FROM events LIMIT 0").description]
        events = []
        for r in rows:
            d = dict(zip(cols, r, strict=False))
            d["payload"] = json.loads(d["payload"] or "{}")
            d["metadata"] = json.loads(d["metadata"] or "{}")
            events.append(Event.from_dict(d))
        return events

    def close(self) -> None:
        self._conn.close()
