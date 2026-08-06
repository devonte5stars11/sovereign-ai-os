"""GeminiAdapter against a mocked transport: request building + parsing.

The same adapter code path that would run against the live API is exercised
here with a fake HTTP session — no network, no credentials.
"""

import pytest

from ai_os_kernel import CompletionRequest, Message, ProviderError
from ai_os_kernel.adapters.gemini import GeminiAdapter

from .conftest import FakeSession, gemini_completion_body


def test_complete_parses_response():
    session = FakeSession(lambda s: (200, gemini_completion_body()))
    adapter = make_gemini(session)
    resp = adapter.complete(CompletionRequest(messages=[Message("user", "hi")]))
    assert resp.success
    assert resp.text == "Hello from Gemini"
    assert resp.prompt_tokens == 10
    assert resp.completion_tokens == 25
    # cost = 10/1000*in + 25/1000*out
    assert resp.cost_usd == pytest.approx(10/1000*0.000002 + 25/1000*0.000008)


def test_complete_sends_expected_url_and_body():
    session = FakeSession(lambda s: (200, gemini_completion_body()))
    adapter = make_gemini(session)
    adapter.complete(CompletionRequest(messages=[Message("user", "hi")], model="m"))
    call = session.calls[0]
    assert "generateContent" in call["url"]
    assert "key=TEST_KEY" in call["url"]
    assert call["json_body"]["contents"][0]["parts"][0]["text"] == "hi"


def test_json_mode_sets_response_mime_type():
    session = FakeSession(lambda s: (200, gemini_completion_body(text='{"a":1}')))
    adapter = make_gemini(session)
    adapter.complete(CompletionRequest(messages=[Message("user", "x")], json_mode=True))
    cfg = session.calls[0]["json_body"]["generationConfig"]
    assert cfg["responseMimeType"] == "application/json"


def test_http_error_raises_provider_error():
    session = FakeSession(lambda s: (400, {"error": {"message": "bad input"}}))
    adapter = make_gemini(session)
    with pytest.raises(ProviderError) as exc:
        adapter.complete(CompletionRequest(messages=[Message("user", "x")]))
    assert "400" in str(exc.value)


def test_missing_key_raises():
    from ai_os_kernel.adapters.gemini import GeminiAdapter

    adapter = GeminiAdapter(api_key="", session=FakeSession())
    with pytest.raises(ProviderError):
        adapter.complete(CompletionRequest(messages=[Message("user", "x")]))


def test_health_with_key_and_ok():
    session = FakeSession(lambda s: (200, {"models": []}))
    adapter = make_gemini(session)
    assert adapter.health().ok is True


def test_health_no_key_not_ok():
    from ai_os_kernel.adapters.gemini import GeminiAdapter

    adapter = GeminiAdapter(api_key="", session=FakeSession())
    assert adapter.health().ok is False


def test_stream_yields_deltas():
    from .conftest import STREAM_SSE

    session = FakeSession(lambda s: (200, STREAM_SSE))
    adapter = make_gemini(session)
    deltas = list(adapter.stream(CompletionRequest(messages=[Message("user", "x")])))
    assert "".join(deltas) == "Hello Gemini"


# Import helper defined above module-level for clarity.
from .conftest import make_gemini  # noqa: E402
