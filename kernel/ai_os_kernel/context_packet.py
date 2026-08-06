"""Standardized Context Packets.

Every agent receives the same structured context format. This avoids bespoke
prompts and improves interoperability across workflows and providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextPacket:
    """The uniform context handed to any agent.

    Fields mirror the standard: Task, Goals, Constraints, Relevant Memory,
    Artifacts, Policies, Budget, Expected Output.
    """

    task: str
    goals: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    relevant_memory: list[str] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    policies: list[str] = field(default_factory=list)
    budget: dict[str, Any] = field(default_factory=dict)
    expected_output: str = ""
    context: dict[str, Any] = field(default_factory=dict)  # freeform extras

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "goals": list(self.goals),
            "constraints": list(self.constraints),
            "relevant_memory": list(self.relevant_memory),
            "artifacts": list(self.artifacts),
            "policies": list(self.policies),
            "budget": dict(self.budget),
            "expected_output": self.expected_output,
            "context": dict(self.context),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContextPacket:
        return cls(
            task=data.get("task", ""),
            goals=list(data.get("goals", [])),
            constraints=list(data.get("constraints", [])),
            relevant_memory=list(data.get("relevant_memory", [])),
            artifacts=list(data.get("artifacts", [])),
            policies=list(data.get("policies", [])),
            budget=data.get("budget", {}) or {},
            expected_output=data.get("expected_output", ""),
            context=data.get("context", {}) or {},
        )

    def validate(self) -> list[str]:
        """Return a list of missing-field problems (empty == valid)."""
        problems = []
        if not self.task:
            problems.append("task is required")
        if not self.expected_output:
            problems.append("expected_output is required")
        return problems
