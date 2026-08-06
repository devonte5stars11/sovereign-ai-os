"""Prompt Graphs (G1-G4) — versioned, testable, reusable workflow assets.

A Prompt Graph is a directed acyclic graph of steps. Instead of linear
prompt->response chains, you compose reusable nodes (planner, retriever,
specialists, verifier, aggregator) and version the whole graph like code.
Reflection revises graphs, not ad-hoc prompts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


class GraphError(Exception):
    pass


@dataclass
class GraphNode:
    """A single step in a prompt graph."""

    id: str
    role: str  # e.g. planner, retriever, specialist, verifier, aggregator
    prompt_template: str = ""
    required_capabilities: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role": self.role,
            "prompt_template": self.prompt_template,
            "required_capabilities": list(self.required_capabilities),
            "depends_on": list(self.depends_on),
        }


@dataclass
class PromptGraph:
    """A DAG of steps. ``order()`` yields a valid topological execution order."""

    name: str
    version: int = 1
    nodes: Dict[str, GraphNode] = field(default_factory=dict)

    def add_node(self, node: GraphNode) -> "PromptGraph":
        if node.id in self.nodes:
            raise GraphError(f"duplicate node id: {node.id}")
        # Dependencies may be forward references; structural problems are
        # surfaced by validate() / order(), not rejected eagerly here.
        self.nodes[node.id] = node
        return self

    def validate(self) -> List[str]:
        """Return structural problems; empty list means the graph is valid."""
        problems: List[str] = []
        for node in self.nodes.values():
            for dep in node.depends_on:
                if dep not in self.nodes:
                    problems.append(f"node '{node.id}' depends on missing '{dep}'")
        try:
            self.order()
        except GraphError as exc:
            problems.append(str(exc))
        return problems

    def order(self) -> List[str]:
        """Topological order of node ids (Kahn's algorithm)."""
        # guard against unknown deps
        for node in self.nodes.values():
            for dep in node.depends_on:
                if dep not in self.nodes:
                    raise GraphError(f"node '{node.id}' depends on missing '{dep}'")
        indegree: Dict[str, int] = {n: 0 for n in self.nodes}
        adj: Dict[str, List[str]] = {n: [] for n in self.nodes}
        for node in self.nodes.values():
            for dep in node.depends_on:
                if dep == node.id:
                    continue  # self-dependency is a cycle
                adj[dep].append(node.id)
                indegree[node.id] += 1
        queue = [n for n, d in indegree.items() if d == 0]
        order: List[str] = []
        while queue:
            n = queue.pop(0)
            order.append(n)
            for m in adj[n]:
                indegree[m] -= 1
                if indegree[m] == 0:
                    queue.append(m)
        if len(order) != len(self.nodes):
            raise GraphError(f"graph has a cycle: {self.name}")
        return order

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "nodes": [self.nodes[n].to_dict() for n in self.order()],
        }
