"""Resource budgets and recovery policies.

Every workflow declares explicit limits (time, cost, tokens, retries, parallel
workers) and explicit fallback behavior so autonomous runs stay bounded and
degrade gracefully when providers change or fail.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResourceBudget:
    """Bounded execution limits for a workflow/run."""

    time_seconds: float = float("inf")
    budget_usd: float = float("inf")
    max_tokens: int = 0  # 0 == unlimited
    max_retries: int = 2
    max_parallel_workers: int = 5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time_seconds": self.time_seconds,
            "budget_usd": self.budget_usd,
            "max_tokens": self.max_tokens,
            "max_retries": self.max_retries,
            "max_parallel_workers": self.max_parallel_workers,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResourceBudget":
        return cls(
            time_seconds=float(data.get("time_seconds", float("inf"))),
            budget_usd=float(data.get("budget_usd", float("inf"))),
            max_tokens=int(data.get("max_tokens", 0)),
            max_retries=int(data.get("max_retries", 2)),
            max_parallel_workers=int(data.get("max_parallel_workers", 5)),
        )


@dataclass
class RecoveryPolicy:
    """Ordered fallback chain: try each alternative until one succeeds.

    Example: NotebookLM unavailable -> Gemini -> Local RAG -> Cached summary
             -> Ask human.
    """

    fallbacks: List[str] = field(default_factory=list)
    ask_human_on_exhaustion: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fallbacks": list(self.fallbacks),
            "ask_human_on_exhaustion": self.ask_human_on_exhaustion,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecoveryPolicy":
        return cls(
            fallbacks=list(data.get("fallbacks", [])),
            ask_human_on_exhaustion=bool(data.get("ask_human_on_exhaustion", True)),
        )
