"""Provider resilience: rate-limit retry + timeout/network failure."""

import pytest
from ai_os_kernel import CompletionRequest, Message, ProviderError

from .conftest import FakeSession, gemini_completion_body, make_gemini


def test_rate_limit_retries_then_succeeds(monkeypatch):
    calls = {"n": 0}

    def responder(session):
        calls["n"] += 1
        if calls["n"] <= 2:
            return 429, {"error": {"message": "quota exceeded"}}
        return 200, gemini_completion_body()

    monkeypatch.setattr("ai_os_kernel.adapters.gemini.time.sleep", lambda s: None)
    adapter = make_gemini(FakeSession(responder))
    req = CompletionRequest(messages=[Message("user", "hi")], max_retries=3)
    resp = adapter.complete(req)
    assert resp.success
    assert calls["n"] == 3  # two 429s, then success


def test_rate_limit_exhausts_retries(monkeypatch):
    monkeypatch.setattr("ai_os_kernel.adapters.gemini.time.sleep", lambda s: None)
    adapter = make_gemini(FakeSession(lambda s: (429, {"error": {"message": "nope"}})))
    with pytest.raises(ProviderError) as exc:
        adapter.complete(CompletionRequest(messages=[Message("user", "x")], max_retries=1))
    assert "failed after retries" in str(exc.value)


def test_timeout_network_failure_raises():
    def responder(session):
        raise ProviderError("network error: timed out")

    adapter = make_gemini(FakeSession(responder))
    with pytest.raises(ProviderError):
        adapter.complete(CompletionRequest(messages=[Message("user", "x")]))
