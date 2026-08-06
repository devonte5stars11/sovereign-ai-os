"""Workflow registry: registration, validation, promotion."""

import pytest
from ai_os_kernel import GraphNode, PromptGraph, Workflow, WorkflowRegistry
from ai_os_kernel.workflow_registry import WorkflowError


def _valid_workflow(name="wf"):
    g = (
        PromptGraph(name=name)
        .add_node(GraphNode("in", "input"))
        .add_node(GraphNode("out", "output", depends_on=["in"]))
    )
    return Workflow(name=name, graph=g)


def test_register_and_get():
    reg = WorkflowRegistry()
    wf = _valid_workflow("alpha")
    reg.register(wf)
    assert reg.get("alpha") is wf
    assert "alpha" in reg


def test_duplicate_rejected():
    reg = WorkflowRegistry()
    reg.register(_valid_workflow("dup"))
    with pytest.raises(WorkflowError):
        reg.register(_valid_workflow("dup"))


def test_invalid_graph_rejected():
    reg = WorkflowRegistry()
    g = PromptGraph(name="bad")
    g.add_node(GraphNode("a", "r", depends_on=["b"]))
    g.add_node(GraphNode("b", "r", depends_on=["a"]))
    wf = Workflow(name="bad", graph=g)
    with pytest.raises(WorkflowError):
        reg.register(wf)


def test_promotion_lifecycle():
    wf = _valid_workflow("promo")
    assert wf.status == "draft"
    wf.promote()
    assert wf.status == "candidate"
    wf.promote()
    assert wf.status == "promoted"


def test_metrics_recorded():
    wf = _valid_workflow("m")
    wf.record_metrics(latency_ms=1200, cost_usd=0.01, success=True)
    assert wf.metrics["cost_usd"] == 0.01
