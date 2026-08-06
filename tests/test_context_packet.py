"""Standardized context packets."""

from ai_os_kernel import ContextPacket


def test_validate_empty():
    assert ContextPacket(task="", expected_output="").validate()


def test_validate_complete():
    p = ContextPacket(
        task="Build CDL offer",
        goals=["Generate leads"],
        constraints=["<$500/mo"],
        expected_output="proposal.md",
    )
    assert p.validate() == []


def test_roundtrip_dict():
    p = ContextPacket(
        task="t",
        goals=["g1"],
        constraints=["c1"],
        relevant_memory=["m1"],
        artifacts=[{"type": "doc"}],
        policies=["constitution"],
        budget={"usd": 5},
        expected_output="out.md",
        context={"k": "v"},
    )
    assert ContextPacket.from_dict(p.to_dict()).to_dict() == p.to_dict()


def test_to_dict_shape():
    p = ContextPacket(task="t", expected_output="out")
    d = p.to_dict()
    assert set(d) == {
        "task", "goals", "constraints", "relevant_memory", "artifacts",
        "policies", "budget", "expected_output", "context",
    }
