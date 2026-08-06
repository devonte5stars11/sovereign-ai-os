"""Workflow Registry.

Instead of storing Prompt Graphs in isolation, workflows carry a prompt graph,
evaluation history, metrics, versions, and approval status. This creates a
library of reusable, continuously improving workflows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .prompt_graph import PromptGraph
from .resources import RecoveryPolicy, ResourceBudget


class WorkflowError(Exception):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Workflow:
    """A versioned, approved, evaluated workflow."""

    name: str
    graph: PromptGraph
    budget: ResourceBudget = field(default_factory=ResourceBudget)
    recovery: RecoveryPolicy = field(default_factory=RecoveryPolicy)
    status: str = "draft"  # draft | candidate | promoted | deprecated
    approval_required: bool = False
    created_at: str = field(default_factory=_now)
    version: int = 1
    metrics: dict[str, float] = field(default_factory=dict)

    def promote(self) -> None:
        if self.status == "draft":
            self.status = "candidate"
        elif self.status == "candidate":
            self.status = "promoted"
        elif self.status == "promoted":
            raise WorkflowError("already promoted")

    def deprecate(self) -> None:
        self.status = "deprecated"

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
