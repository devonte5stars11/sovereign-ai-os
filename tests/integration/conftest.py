"""Shared transport-mocking helpers for integration tests.

These exercise the real adapter/HTTP code path but substitute a fake transport,
so the full request-building + response-parsing + retry logic runs without any
live network or credentials. A separate set of live-gated tests run against the
real Gemini API when GEMINI_API_KEY is set.
"""

import pytest


class FakeSession:
    """Drop-in for `ai_os_kernel.provider.HttpClient`.

    ``responder`` is a callable receiving this session and returning
    ``(status_code, body)`` where body is a dict (JSON) or str (raw).
    """

    def __init__(self, responder=None):
        self.responder = responder or (lambda s: (200, {"ok": True}))
        self.calls = []

    def post(self, url, json_body=None, headers=None, timeout=None, raw_response=False):
        self.calls.append(
            {
                "url": url,
                "json_body": json_body,
                "headers": headers,
                "timeout": timeout,
                "raw_response": raw_response,
            }
        )
        code, data = self.responder(self)
        if raw_response and isinstance(data, (str, bytes)):
            return code, data if isinstance(data, bytes) else data.encode("utf-8")
        return code, data


def gemini_completion_body(prompt_tokens=10, completion_tokens=25, text="Hello from Gemini"):
    return {
        "candidates": [{"content": {"parts": [{"text": text}]}}],
        "usageMetadata": {
            "promptTokenCount": prompt_tokens,
            "candidatesTokenCount": completion_tokens,
        },
    }


STREAM_SSE = (
    'data: {"candidates": [{"content": {"parts": [{"text": "Hel"}]}}]}\n\n'
    'data: {"candidates": [{"content": {"parts": [{"text": "lo "}]}}]}\n\n'
    'data: {"candidates": [{"content": {"parts": [{"text": "Gemini"}]}}]}\n\n'
)


def make_gemini(session):
    from ai_os_kernel.adapters.gemini import GeminiAdapter

    return GeminiAdapter(api_key="TEST_KEY", session=session)


@pytest.fixture
def offline_registry(tmp_path, monkeypatch):
    """Registry containing only the OfflineAdapter (no live key, no network)."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    from ai_os_kernel.adapters import OfflineAdapter
    from ai_os_kernel.capability_registry import AdapterRegistry

    reg = AdapterRegistry()
    reg.register(OfflineAdapter())
    return reg
