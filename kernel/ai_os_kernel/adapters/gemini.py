"""GeminiAdapter — first real implementation of the ProviderAdapter contract.

Talks to the Google Generative Language API. The transport (``session``) is
injectable so the exact same code path is exercised by transport-mocked
integration tests (no network) and against the live API when a key is present.
"""

from __future__ import annotations

import os
import time
from typing import Dict, Iterator, List, Optional, Tuple

from ..manifest import ProviderManifest, load_manifest
from ..provider import (
    CompletionRequest,
    CompletionResponse,
    HealthStatus,
    HttpClient,
    ProviderAdapter,
    ProviderError,
)

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiAdapter(ProviderAdapter):
    name = "gemini"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        session=None,
        manifest: Optional[ProviderManifest] = None,
    ):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = model
        self.session = session if session is not None else HttpClient()
        self.manifest = manifest or self._load_static_manifest()

    # -- discovery --------------------------------------------------------
    def _load_static_manifest(self) -> ProviderManifest:
        here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(here, "providers", "gemini.yaml")
        try:
            return load_manifest(path)
        except Exception:
            return ProviderManifest(
                provider="gemini", version="2.5", adapter="gemini",
                capabilities={"long_context", "vision", "json_mode", "tool_calling",
                              "streaming", "code_execution", "file_editing"},
                cost_input_per_1k=0.000002, cost_output_per_1k=0.000008,
            )

    def capabilities(self) -> ProviderManifest:
        return self.manifest

    # -- helpers ----------------------------------------------------------
    def _auth_params(self) -> str:
        return f"?key={self.api_key}"

    # -- health -----------------------------------------------------------
    def health(self) -> HealthStatus:
        start = time.perf_counter()
        if not self.api_key:
            return HealthStatus(False, self.name, 0.0, "no GEMINI_API_KEY configured")
        try:
            url = f"{GEMINI_BASE}/models?key={self.api_key}"
            code, _ = self.session.post(url, json_body=None, timeout=10.0, raw_response=False)
            ok = code == 200
            return HealthStatus(ok, self.name, (time.perf_counter() - start) * 1000)
        except ProviderError as exc:
            return HealthStatus(False, self.name, (time.perf_counter() - start) * 1000, str(exc))

    # -- completion -------------------------------------------------------
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        if not self.api_key:
            raise ProviderError(f"{self.name}: no GEMINI_API_KEY configured (set it to go live, or use the OfflineAdapter)")
        body = self._build_body(request, stream=False)
        url = f"{GEMINI_BASE}/models/{self.model}:generateContent{self._auth_params()}"
        last_error: Optional[str] = None
        for attempt in range(request.max_retries + 1):
            start = time.perf_counter()
            try:
                code, data = self.session.post(
                    url, json_body=body, timeout=request.timeout_seconds
                )
                latency = (time.perf_counter() - start) * 1000
                if code == 429:
                    # rate-limited -> backoff and retry
                    time.sleep(0.5 * (2 ** attempt))
                    last_error = f"rate limited (HTTP 429) attempt {attempt + 1}"
                    continue
                if code != 200:
                    raise ProviderError(f"{self.name}: HTTP {code}: {self._error_from(data)}")
                return self._parse_completion(data, latency)
            except ProviderError:
                raise
            except Exception as exc:  # transport-level retryable
                last_error = str(exc)
                time.sleep(0.5 * (2 ** attempt))
        raise ProviderError(f"{self.name}: failed after retries: {last_error}")

    # -- streaming --------------------------------------------------------
    def stream(self, request: CompletionRequest) -> Iterator[str]:
        if not self.api_key:
            raise ProviderError(f"{self.name}: no GEMINI_API_KEY configured")
        body = self._build_body(request, stream=True)
        url = f"{GEMINI_BASE}/models/{self.model}:streamGenerateContent{self._auth_params()}"
        code, raw = self.session.post(
            url, json_body=body, timeout=request.timeout_seconds, raw_response=True
        )
        if code != 200:
            raise ProviderError(f"{self.name}: HTTP {code} on stream")
        text = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload in ("[DONE]", ""):
                continue
            yield self._delta_from_event(payload)

    # -- body / parsing ---------------------------------------------------
    def _build_body(self, request: CompletionRequest, stream: bool) -> dict:
        contents = []
        if request.system:
            contents.append({"role": "user", "parts": [{"text": request.system}]})
        for m in request.messages:
            if m.role == "system":
                continue
            contents.append({"role": "user" if m.role != "assistant" else "model",
                             "parts": [{"text": m.content}]})
        body: dict = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            },
        }
        if request.json_mode:
            body["generationConfig"]["responseMimeType"] = "application/json"
        return body

    def _parse_completion(self, data, latency_ms: float) -> CompletionResponse:
        if isinstance(data, (bytes, str)):
            raise ProviderError(f"{self.name}: non-JSON response: {str(data)[:200]}")
        candidates = (data.get("candidates") or [{}])
        parts = (candidates[0].get("content", {}).get("parts") or [{}]) if candidates else [{}]
        text = "".join(p.get("text", "") for p in parts)
        usage = data.get("usageMetadata") or {}
        prompt_tokens = int(usage.get("promptTokenCount", 0) or 0)
        completion_tokens = int(usage.get("candidatesTokenCount", 0) or 0)
        cost = self._cost(prompt_tokens, completion_tokens)
        return CompletionResponse(
            text=text, provider=self.name, model=self.model, latency_ms=latency_ms,
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            cost_usd=cost, success=True, raw=data,
        )

    def _delta_from_event(self, payload: str) -> str:
        import json

        try:
            evt = json.loads(payload)
        except ValueError:
            return ""
        parts = ((evt.get("candidates") or [{}])[0].get("content", {}).get("parts") or [{}])
        return "".join(p.get("text", "") for p in parts)

    def _error_from(self, data) -> str:
        if isinstance(data, dict):
            err = data.get("error") or {}
            return str(err.get("message", data))
        return str(data)[:300]

    def _cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        m = self.manifest
        return (prompt_tokens / 1000.0 * m.cost_input_per_1k) + (
            completion_tokens / 1000.0 * m.cost_output_per_1k
        )
