"""Typed artifact registry: provenance, checksums, verification."""

import pytest
from ai_os_kernel import Artifact, ArtifactRegistry
from ai_os_kernel.artifact_registry import ArtifactError


def test_seal_sets_checksum():
    a = Artifact(type="proposal", creator="wf", content="hello world").seal()
    assert a.checksum
    assert a.verify()


def test_add_and_verify():
    reg = ArtifactRegistry()
    a = Artifact(type="doc", creator="wf", workflow="w", trust=0.9, content="the body")
    reg.add(a)
    assert len(reg) == 1
    assert reg.verify(a.artifact_id)


def test_tamper_detected():
    reg = ArtifactRegistry()
    a = Artifact(type="doc", creator="wf", content="original").seal()
    reg.add(a)
    stored = reg.get(a.artifact_id)
    stored.content = "tampered"
    assert not reg.verify(a.artifact_id)
    assert not stored.verify()


def test_duplicate_id_rejected():
    reg = ArtifactRegistry()
    a = Artifact(type="doc", creator="wf", artifact_id="fixed-id", content="x")
    reg.add(a)
    b = Artifact(type="doc", creator="wf", artifact_id="fixed-id", content="y")
    with pytest.raises(ArtifactError):
        reg.add(b)


def test_artifact_metadata_complete():
    a = Artifact(
        type="video_concept",
        creator="creative_wf",
        workflow="wf",
        graph_version=2,
        source="spec",
        trust=0.95,
        content="",
    )
    d = a.to_dict()
    for key in [
        "artifact_id",
        "type",
        "creator",
        "workflow",
        "graph_version",
        "source",
        "trust",
        "checksum",
        "timestamp",
    ]:
        assert key in d
