"""Provider capability manifests.

A provider adapter publishes a machine-readable manifest declaring its
capabilities, cost, and limits. The router consumes these manifests so that
providers can be added or replaced without changing routing logic.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

try:  # sturdy YAML when available
    import yaml

    _HAS_YAML = True
except Exception:  # noqa: BLE001 - pragma: no cover - only reached without PyYAML
    _HAS_YAML = False


class ManifestError(Exception):
    """Raised when a manifest is malformed or missing required fields."""


@dataclass
class ProviderManifest:
    """A single provider's public capability contract."""

    provider: str
    version: str
    adapter: str = ""
    capabilities: set[str] = field(default_factory=set)
    cost_input_per_1k: float = 0.0
    cost_output_per_1k: float = 0.0
    limits: dict[str, float] = field(default_factory=dict)
    properties: dict[str, object] = field(default_factory=dict)
    source: str = ""

    # -- convenience -----------------------------------------------------
    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    def supports_all(self, required: Iterable[str]) -> bool:
        return all(self.supports(c) for c in required)

    def estimated_cost_usd(self, input_tokens: float, output_tokens: float) -> float:
        """Estimated cost in USD for a given token usage."""
        return (input_tokens / 1000.0 * self.cost_input_per_1k) + (
            output_tokens / 1000.0 * self.cost_output_per_1k
        )

    @property
    def is_local(self) -> bool:
        return self.supports("local")

    # -- (de)serialization ----------------------------------------------
    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "version": self.version,
            "adapter": self.adapter,
            "capabilities": sorted(self.capabilities),
            "cost": {
                "input": self.cost_input_per_1k,
                "output": self.cost_output_per_1k,
            },
            "limits": dict(self.limits),
            "properties": dict(self.properties),
        }

    @classmethod
    def from_dict(cls, data: dict, source: str = "") -> ProviderManifest:
        caps = data.get("capabilities", {})
        capabilities = {
            name for name, enabled in caps.items() if isinstance(enabled, bool) and enabled
        }
        cost = data.get("cost", {}) or {}
        return cls(
            provider=str(data.get("provider", "")),
            version=str(data.get("version", "")),
            adapter=str(data.get("adapter", "")),
            capabilities=capabilities,
            cost_input_per_1k=float(cost.get("input", 0.0)),
            cost_output_per_1k=float(cost.get("output", 0.0)),
            limits=data.get("limits", {}) or {},
            properties=data.get("properties", {}) or {},
            source=source,
        )


def load_manifest(path: str | os.PathLike) -> ProviderManifest:
    """Load a single YAML manifest file into a ProviderManifest."""
    p = Path(path)
    if not p.exists():
        raise ManifestError(f"manifest not found: {p}")
    if not _HAS_YAML:  # pragma: no cover
        raise ManifestError("PyYAML is required to load YAML manifests.")
    with open(p, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ManifestError(f"manifest must be a mapping: {p}")
    if not data.get("provider"):
        raise ManifestError(f"manifest missing 'provider': {p}")
    return ProviderManifest.from_dict(data, source=str(p))


def load_manifests(
    paths: str | os.PathLike | Iterable[str | os.PathLike] | None = None,
) -> list[ProviderManifest]:
    """Load several manifests.

    ``paths`` may be a directory (glob *.yaml), a single file, or an iterable
    of paths. Defaults to every *.yaml under ``providers/`` in the repo root.
    """
    if paths is None:
        here = Path(__file__).resolve().parent.parent.parent  # repo root
        paths = sorted((here / "providers").glob("*.yaml"))
    elif isinstance(paths, (str, os.PathLike)):
        p = Path(paths)
        paths = sorted(p.glob("*.yaml")) if p.is_dir() else [p]
    return [load_manifest(p) for p in paths]
