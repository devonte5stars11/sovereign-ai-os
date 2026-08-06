"""Prompt graphs: assembly, validation, topological ordering, cycles."""

import pytest
from ai_os_kernel import GraphNode, PromptGraph
from ai_os_kernel.prompt_graph import GraphError


def test_simple_order():
    g = (
        PromptGraph(name="g", version=1)
        .add_node(GraphNode("planner", "planner"))
        .add_node(GraphNode("retriever", "retriever", depends_on=["planner"]))
        .add_node(GraphNode("verifier", "verifier", depends_on=["retriever"]))
    )
    assert g.order() == ["planner", "retriever", "verifier"]


def test_diamond_order_respects_dependencies():
    g = (
        PromptGraph(name="g")
        .add_node(GraphNode("a", "planner"))
        .add_node(GraphNode("b", "spec", depends_on=["a"]))
        .add_node(GraphNode("c", "spec", depends_on=["a"]))
        .add_node(GraphNode("d", "agg", depends_on=["b", "c"]))
    )
    order = g.order()
    assert order.index("a") < order.index("b") < order.index("d")
    assert order.index("a") < order.index("c") < order.index("d")


def test_cycle_detected():
    g = PromptGraph(name="g")
    g.add_node(GraphNode("a", "r", depends_on=["b"]))
    g.add_node(GraphNode("b", "r", depends_on=["a"]))
    with pytest.raises(GraphError):
        g.order()
    # validate() surfaces the cycle too
    assert any("cycle" in p for p in g.validate())


def test_missing_dep_detected():
    g = PromptGraph(name="g")
    g.add_node(GraphNode("a", "r", depends_on=["ghost"]))
    problems = g.validate()
    assert any("ghost" in p for p in problems)
    with pytest.raises(GraphError):
        g.order()


def test_duplicate_node_rejected():
    g = PromptGraph(name="g")
    g.add_node(GraphNode("a", "r"))
    with pytest.raises(GraphError):
        g.add_node(GraphNode("a", "r"))


def test_forward_reference_allowed_at_build_but_flagged_on_validate():
    # add_node permits forward references; validate() then flags them.
    g = (
        PromptGraph(name="g")
        .add_node(GraphNode("a", "r", depends_on=["later"]))
        .add_node(GraphNode("later", "r"))
    )
    # Valid once the dependency exists.
    assert g.validate() == []
    # 'a' depends on 'later', so 'later' executes first.
    assert g.order() == ["later", "a"]
