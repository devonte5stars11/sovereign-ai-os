"""Capability-based routing.

The router never reasons about model names. It takes a task's required
capabilities and a budget, and picks the cheapest provider whose manifest
satisfies every requirement. This is what lets the OS survive new model
releases without any routing-code changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

from .manifest import ProviderManifest


@dataclass
class TaskSpec:
    """What a task needs, expressed in capability terms."""

    required_capabilities: List[str]
    max_budget_usd: float = float("inf")
    preferred_capabilities: List[str] = None
    prefer_local: bool = False
    exclude: List[str] = None  # provider names to skip

    def __post_init__(self):
        if self.preferred_capabilities is None:
            self.preferred_capabilities = []
        if self.exclude is None:
            self.exclude = []


@dataclass
class RouteResult:
    """Outcome of a routing decision."""

    provider: Optional[ProviderManifest]
    candidates: List[ProviderManifest]
    rejected: List[ProviderManifest]
    reason: str = ""

    @property
    def success(self) -> bool:
        return self.provider is not None


class CapabilityRouter:
    """Routes TaskSpecs to the cheapest capable provider."""

    def __init__(self, manifests: Iterable[ProviderManifest]):
        self._manifests = list(manifests)

    @property
    def manifests(self) -> List[ProviderManifest]:
        return list(self._manifests)

    def route(self, spec: TaskSpec) -> RouteResult:
        candidates: List[ProviderManifest] = []
        rejected: List[ProviderManifest] = []

        for m in self._manifests:
            if m.provider in spec.exclude:
                rejected.append(m)
                continue
            if spec.prefer_local and not m.is_local:
                rejected.append(m)
                continue
            if m.cost_input_per_1k > spec.max_budget_usd:
                # crude budget gate on input price
                rejected.append(m)
                continue
            if m.supports_all(spec.required_capabilities):
                candidates.append(m)
            else:
                rejected.append(m)

        if not candidates:
            return RouteResult(None, [], rejected, reason="no provider satisfies all required capabilities")

        # Rank candidates by cost (cheapest input first, then cheapest output).
        candidates.sort(
            key=lambda m: (
                m.cost_input_per_1k,
                m.cost_output_per_1k,
                # stability: prefer local for identical cost (privacy)
                0 if m.is_local else 1,
            )
        )
        best = candidates[0]

        # Within candidates, prefer ones matching preferred capabilities when
        # the cost difference is negligible (provides taste/preference without
        # sacrificing the core cost discipline).
        if spec.preferred_capabilities:
            for c in candidates:
                has = all(c.supports(p) for p in spec.preferred_capabilities)
                if has and c.estimated_cost_usd(1000, 1000) <= best.estimated_cost_usd(1000, 1000) * 1.5:
                    best = c
                    break

        return RouteResult(best, candidates, rejected, reason="cheapest capable provider")
