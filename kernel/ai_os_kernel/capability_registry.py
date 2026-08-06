"""Adapter registry + capability discovery.

Manifests are not hardcoded forever: adapters *report* their capabilities via
``adapter.capabilities()``, and a CapabilityRegistry caches those (with a TTL)
and feeds them to the router. The static providers/*.yaml files remain as
defaults; runtime discovery keeps the registry current as providers change.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass

from .manifest import ProviderManifest
from .provider import ProviderAdapter


@dataclass
class DiscoveredManifest:
    manifest: ProviderManifest
    discovered_at: float

    @property
    def age_seconds(self) -> float:
        return time.time() - self.discovered_at


class AdapterRegistry:
    """Holds provider adapter instances; a single place to add/replace providers."""

    def __init__(self, adapters: Iterable[ProviderAdapter] | None = None):
        self._adapters: dict[str, ProviderAdapter] = {}
        for a in adapters or []:
            self.register(a)

    def register(self, adapter: ProviderAdapter) -> None:
        if adapter.name in self._adapters:
            raise ValueError(f"adapter already registered: {adapter.name}")
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> ProviderAdapter | None:
        return self._adapters.get(name)

    @property
    def names(self) -> list[str]:
        return sorted(self._adapters)

    def all(self) -> list[ProviderAdapter]:
        return list(self._adapters.values())


class CapabilityRegistry:
    """Caches each adapter's reported capabilities with a TTL, so routing
    decisions use current data without re-probing on every request."""

    def __init__(self, adapters: Iterable[ProviderAdapter], ttl_seconds: float = 300.0):
        self._adapters = {a.name: a for a in adapters}
        self._cache: dict[str, DiscoveredManifest] = {}
        self.ttl_seconds = ttl_seconds
        self._lock = threading.Lock()

    def _fresh(self) -> bool:
        return all(m.age_seconds < self.ttl_seconds for m in self._cache.values()) and len(
            self._cache
        ) == len(self._adapters)

    def discover(self, force: bool = False) -> list[ProviderManifest]:
        """Probe adapters and rebuild/refresh the cache."""
        with self._lock:
            if not force and self._fresh():
                return [m.manifest for m in self._cache.values()]
            for name, adapter in self._adapters.items():
                try:
                    manifest = adapter.capabilities()
                except Exception as exc:  # noqa: BLE001 - a failing adapter must not break routing
                    manifest = ProviderManifest(
                        provider=name,
                        version="error",
                        capabilities=set(),
                        properties={"error": str(exc)},
                    )
                self._cache[name] = DiscoveredManifest(manifest, time.time())
            return [m.manifest for m in self._cache.values()]

    @property
    def manifests(self) -> list[ProviderManifest]:
        return self.discover()

    def refresh(self) -> list[ProviderManifest]:
        return self.discover(force=True)
