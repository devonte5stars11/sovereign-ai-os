"""The AI Constitution and Policy Engine.

The constitution is the root policy for every workflow. The Policy Engine
enforces it before, during, and after execution — checking for knowledge
immutability, cost discipline, and the requirement of approval for destructive
or externally-reaching actions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Principle:
    number: int
    name: str
    guidance: str


PRINCIPLES = [
    Principle(1, "truthfulness", "Truth over speculation; distinguish fact from inference."),
    Principle(2, "preserve_canonical_knowledge", "Store of truth is Markdown/Git/Obsidian."),
    Principle(3, "minimize_cost", "Cheapest capable path; escalate on demonstrated need."),
    Principle(
        4,
        "require_approval_for_destructive",
        "Approval for deletes and irrecoverable changes.",
    ),
    Principle(5, "cite_provenance", "Record source, workflow, and graph version."),
    Principle(6, "prefer_reusable_artifacts", "Favor typed, versioned, reusable outputs."),
    Principle(7, "vendor_independence", "No knowledge trapped in one provider."),
]


class Constitution:
    """The version-controlled root policy."""

    def __init__(self, principles: list[Principle] | None = None):
        self.principles = principles or PRINCIPLES

    def __iter__(self):
        return iter(self.principles)


class PolicyViolation(Exception):
    """Raised when an action violates the constitution."""

    def __init__(self, principle_number: int, message: str):
        self.principle_number = principle_number
        super().__init__(f"[Constitution #{principle_number}] {message}")


class PolicyEngine:
    """Enforces the constitution on proposed actions."""

    def __init__(self, constitution: Constitution | None = None, require_approval: bool = True):
        self.constitution = constitution or Constitution()
        self.require_approval = require_approval
        self._violations: list[str] = []

    @property
    def violations(self) -> list[str]:
        return list(self._violations)

    def check_cost(self, estimated_usd: float, budget_usd: float) -> None:
        """Principle 3: respect the resource budget."""
        if estimated_usd > budget_usd:
            raise PolicyViolation(
                3,
                f"estimated cost ${estimated_usd:.4f} exceeds budget ${budget_usd:.4f}",
            )

    def check_source_provided(self, has_source: bool) -> None:
        """Principle 5: cite provenance."""
        if not has_source:
            raise PolicyViolation(5, "no provenance/source recorded for artifact")

    def approve_if_needed(self, action: str) -> None:
        """Principle 4: destructive / external actions require approval."""
        if self.require_approval:
            raise PolicyViolation(4, f"approval required for action: {action}")

    # -- run-mode -------------------------------------------------------
    def run_thresholds(
        self, workflow_name: str, estimated_usd: float, budget_usd: float
    ) -> list[str]:
        """Non-raising check; returns human-readable problems."""
        self._violations = []
        if estimated_usd > budget_usd:
            self._violations.append(
                f"[Constitution #3] {workflow_name}: cost ${estimated_usd:.4f} > budget ${budget_usd:.4f}"
            )
        return self._violations
