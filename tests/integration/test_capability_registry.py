"""Capability discovery registry: caching, refresh, failure isolation."""

from ai_os_kernel import CapabilityRegistry
from ai_os_kernel.manifest import ProviderManifest
from ai_os_kernel.provider import ProviderAdapter


class _Canned(ProviderAdapter):
    def __init__(self, name, caps, fail=False):
        self.name = name
        self._caps = caps
        self._fail = fail
        self.probe_count = 0

    def capabilities(self):
        self.probe_count += 1
        if self._fail:
            raise RuntimeError("boom")
        return ProviderManifest(provider=self.name, version="1", capabilities=self._caps)

    def health(self):
        return None

    def complete(self, request):
        from ai_os_kernel.provider import CompletionResponse

        return CompletionResponse(text="", provider=self.name, model="x")


def test_discover_calls_adapters():
    a = _Canned("a", {"x"})
    b = _Canned("b", {"y"})
    reg = CapabilityRegistry([a, b], ttl_seconds=300)
    manis = reg.discover(force=True)
    assert {m.provider for m in manis} == {"a", "b"}


def test_cache_avoids_reprobing_within_ttl():
    a = _Canned("a", {"x"})
    reg = CapabilityRegistry([a], ttl_seconds=300)
    reg.discover(force=True)
    reg.discover()  # within ttl -> cached
    assert a.probe_count == 1


def test_force_refresh_reprobes():
    a = _Canned("a", {"x"})
    reg = CapabilityRegistry([a], ttl_seconds=300)
    reg.discover(force=True)
    reg.refresh()
    assert a.probe_count == 2


def test_failing_adapter_isolated():
    a = _Canned("good", {"x"})
    b = _Canned("bad", set(), fail=True)
    reg = CapabilityRegistry([a, b], ttl_seconds=300)
    manis = reg.discover(force=True)
    by = {m.provider: m for m in manis}
    assert by["good"].supports("x")
    assert by["bad"].capabilities == set()  # error manifest, no crash
