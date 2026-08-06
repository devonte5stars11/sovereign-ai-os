"""Unified event schema + durable event log."""

import uuid

from ai_os_kernel import Event, EventLog


def test_emit_assigns_id_and_timestamp(tmp_path):
    log = EventLog(tmp_path / "events.sqlite3")
    e = log.emit("task.received", source="pipeline", payload={"task": "x"})
    assert e.event_id
    assert e.timestamp
    assert e.event_type == "task.received"
    assert log.count() == 1


def test_emit_accepts_ids_and_metadata(tmp_path):
    log = EventLog(tmp_path / "events.sqlite3")
    corr = str(uuid.uuid4())
    e = log.emit(
        "artifact.created",
        source="pipeline",
        actor="sovereign_note",
        correlation_id=corr,
        workflow_id="sovereign_note",
        artifact_id="1234",
        payload={"checksum": "abc"},
        metadata={"env": "test"},
    )
    assert e.actor == "sovereign_note"
    assert e.workflow_id == "sovereign_note"


def test_by_correlation_returns_emission_order(tmp_path):
    log = EventLog(tmp_path / "events.sqlite3")
    corr = str(uuid.uuid4())
    log.emit("a", source="p", correlation_id=corr)
    log.emit("b", source="p", correlation_id=corr)
    log.emit("c", source="p")  # different correlation
    events = log.by_correlation(corr)
    assert [e.event_type for e in events] == ["a", "b"]


def test_by_type(tmp_path):
    log = EventLog(tmp_path / "events.sqlite3")
    log.emit("x", source="p")
    log.emit("y", source="p")
    log.emit("x", source="p")
    assert len(log.by_type("x")) == 2


def test_recent_newest_first(tmp_path):
    log = EventLog(tmp_path / "events.sqlite3")
    log.emit("first", source="p")
    log.emit("second", source="p")
    recent = log.recent(10)
    assert recent[0].event_type == "second"
    assert recent[1].event_type == "first"


def test_event_to_dict_shape(tmp_path):
    log = EventLog(tmp_path / "events.sqlite3")
    e = log.emit("x", source="p", payload={"k": "v"})
    d = e.to_dict()
    for key in [
        "event_id",
        "event_type",
        "source",
        "timestamp",
        "actor",
        "correlation_id",
        "workflow_id",
        "artifact_id",
        "payload",
        "metadata",
    ]:
        assert key in d
    assert Event.from_dict(d).event_type == "x"
