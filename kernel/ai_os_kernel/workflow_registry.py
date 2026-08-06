"""Workflow Registry.

Instead of storing Prompt Graphs in isolation, workflows carry a prompt graph,
evaluation history, metrics, versions, and approval status. This creates a
library of reusable, continuously improving workflows.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .prompt_graph import PromptGraph
from .resources import RecoveryPolicy, ResourceBudget


class WorkflowError(Exception):
    pass


# Explicit state machine for every workflow/graph lifecycle (see ADR-0008).
# A transition not listed here is illegal and raises WorkflowError.
WORKFLOW_STATES = ("draft", "validated", "candidate", "promoted", "deprecated", "archived")

WORKFLOW_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"validated", "deprecated"},
    "validated": {"candidate", "deprecated"},
    "candidate": {"promoted", "deprecated"},
    "promoted": {"deprecated"},
    "deprecated": {"archived"},
    "archived": set(),  # terminal
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Workflow:
    """A versioned, approved, evaluated workflow with an explicit lifecycle."""

    name: str
    graph: PromptGraph
    budget: ResourceBudget = field(default_factory=ResourceBudget)
    recovery: RecoveryPolicy = field(default_factory=RecoveryPolicy)
    status: str = "draft"  # state machine: WORKFLOW_STATES
    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    approval_required: bool = False
    created_at: str = field(default_factory=_now)
    version: int = 1
    metrics: dict[str, float] = field(default_factory=dict)

    # -- lifecycle (state machine) --------------------------------------
    def transition(self, new_status: str) -> Workflow:
        if new_status not in WORKFLOW_STATES:
            raise WorkflowError(f"unknown state: {new_status}")
        legal = WORKFLOW_TRANSITIONS[self.status]
        if new_status not in legal:
            raise WorkflowError(
                f"illegal transition: {self.status} -> {new_status} "
                f"(allowed: {sorted(legal) or 'terminal'})"
            )
        self.status = new_status
        return self

    def mark_validated(self) -> Workflow:
        return self.transition("validated")

    def stage_candidate(self) -> Workflow:
        return self.transition("candidate")

    def promote(self) -> Workflow:
        return self.transition("promoted")

    def deprecate(self) -> Workflow:
        return self.transition("deprecated")

    def archive(self) -> Workflow:
        return self.transition("archived")

    def record_metrics(self, **metrics: float) -> None:
        self.metrics.update(metrics)


class WorkflowRegistry:
    """Stores and manages workflows by name."""

    def __init__(self) -> None:
        self._workflows: dict[str, Workflow] = {}

    def register(self, workflow: Workflow) -> None:
        if workflow.graph.validate():
            raise WorkflowError(
                f"graph for '{workflow.name}' is invalid: {workflow.graph.validate()}"
            )
        if workflow.name in self._workflows:
            raise WorkflowError(f"workflow already registered: {workflow.name}")
        self._workflows[workflow.name] = workflow

    def get(self, name: str) -> Workflow | None:
        return self._workflows.get(name)

    def __contains__(self, name: str) -> bool:
        return name in self._workflows

    @property
    def names(self) -> list[str]:
        return sorted(self._workflows)

    def promoted(self) -> list[Workflow]:
        return [w for w in self._workflows.values() if w.status == "promoted"]

    def by_status(self, status: str) -> list[Workflow]:
        return [w for w in self._workflows.values() if w.status == status]
