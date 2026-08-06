"""Provider abstraction — the contract every adapter implements.

The kernel is completely unaware of which provider executes a request: it only
talks to the ``ProviderAdapter`` interface. Gemini, GPT, Grok, local — all
implement exactly the same surface. Add or replace a provider by adding an
adapter; nothing else in the kernel changes.

Transport is injectable: adapters use an ``HttpClient``-like ``session`` so
tests can substitute a fake transport (no live network required) and so the
same code path is exercised against real APIs when credentials are present.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Tuple

from .manifest import ProviderManifest


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Message:
    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class CompletionRequest:
    messages: List[Message]
    model: str = ""                 # empty -> adapter default
    system: str = ""                # optional system prompt
    temperature: float = 0.7
    max_tokens: int = 1024
    json_mode: bool = False
    timeout_seconds: float = 30.0
    max_retries: int = 2

    def to_dict(self) -> dict:
        return {
            "messages": [{"role": m.role, "content": m.content} for m in self.messages],
            "model": self.model,
            "system": self.system,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "json_mode": self.json_mode,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass
class CompletionResponse:
    text: str
    provider: str
    model: str
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    success: bool = True
    error: str = ""
    raw: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "provider": self.provider,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "cost_usd": self.cost_usd,
            "success": self.success,
            "error": self.error,
        }


@dataclass
class HealthStatus:
    ok: bool
    provider: str
    latency_ms: float = 0.0
    error: str = ""


class ProviderError(Exception):
    """Raised when an adapter cannot complete an operation."""


# ---------------------------------------------------------------------------
# Abstract adapter
# ---------------------------------------------------------------------------

class ProviderAdapter(ABC):
    """The single contract every provider adapter implements."""

    name: str = ""
    # Static defaults (from providers/*.yaml). Runtime discovery may override.
    manifest: Optional[ProviderManifest] = None

    @abstractmethod
    def capabilities(self) -> ProviderManifest:
        """Report the provider's current capabilities (may be dynamic)."""

    @abstractmethod
    def health(self) -> HealthStatus:
        """Lightweight liveness/readiness probe."""

    @abstractmethod
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Single-turn completion. May raise ProviderError on hard failure."""

    def stream(self, request: CompletionRequest) -> Iterator[str]:
        """Yield text deltas as they arrive. Default: buffered complete()."""
        yield self.complete(request).text

    def tool_call(self, request: CompletionRequest) -> CompletionResponse:
        """Tool/function-calling completion."""
        raise NotImplementedError(f"{self.name} does not implement tool_call yet")

    def embeddings(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Embed a list of texts."""
        raise NotImplementedError(f"{self.name} does not implement embeddings yet")


# ---------------------------------------------------------------------------
# Transport (stdlib, injectable)
# ---------------------------------------------------------------------------

class HttpClient:
    """Minimal JSON POST/GET client over urllib (no optional deps)."""

    def __init__(self, base_headers: Optional[Dict[str, str]] = None,
                 timeout: float = 30.0):
        self.base_headers = base_headers or {}
        self.timeout = timeout

    def post(self, url: str, json_body: Optional[dict] = None,
             headers: Optional[Dict[str, str]] = None,
             timeout: Optional[float] = None,
             raw_response: bool = False) -> Tuple[int, object]:
        """POST and return (status_code, parsed_json | raw bytes)."""
        data = None
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
        hdrs = dict(self.base_headers)
        hdrs.setdefault("Content-Type", "application/json")
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                body = resp.read()
                code = getattr(resp, "status", 200)
        except urllib.error.HTTPError as exc:
            code = exc.code
            body = exc.read()
        except urllib.error.URLError as exc:  # e.g. timeout, DNS
            raise ProviderError(f"network error: {exc.reason}") from exc
        if raw_response:
            return code, body
        try:
            return code, json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            return code, body
