"""OfflineAdapter — a dependency-free demo/test adapter.

Implements the exact same ProviderAdapter contract but never touches the
network. Lets the full pipeline (route -> complete -> graph -> artifact ->
markdown -> git -> evaluation) run end-to-end with zero credentials, and gives
integration tests a deterministic target. Clearly labeled; never used as a
production model.
"""

from __future__ import annotations

import time
from collections.abc import Iterator

from ..manifest import ProviderManifest
from ..provider import (
    CompletionRequest,
    CompletionResponse,
    HealthStatus,
    ProviderAdapter,
)


class OfflineAdapter(ProviderAdapter):
    name = "offline"

    def __init__(self, manifest: ProviderManifest | None = None):
        self.manifest = manifest or ProviderManifest(
            provider="offline",
            version="demo",
            adapter="offline",
            capabilities={"long_context", "json_mode", "streaming"},
            cost_input_per_1k=0.0,
            cost_output_per_1k=0.0,
        )

    def capabilities(self) -> ProviderManifest:
        assert self.manifest is not None
        return self.manifest

    def health(self) -> HealthStatus:
        return HealthStatus(True, self.name, 1.0)

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        start = time.perf_counter()
        user = next((m.content for m in request.messages if m.role == "user"), "")
        text = (
            f"[offline-demo] received {len(request.messages)} message(s). "
            f"Echoing user prompt: {user or '(none)'}"
        )
        return CompletionResponse(
            text=text,
            provider=self.name,
            model="offline-demo",
            latency_ms=(time.perf_counter() - start) * 1000,
            prompt_tokens=0,
            completion_tokens=len(text.split()),
            cost_usd=0.0,
            success=True,
        )

    def stream(self, request: CompletionRequest) -> Iterator[str]:
        text = self.complete(request).text
        # yield word-by-word to emulate streaming
        for i in range(0, len(text), 8):
            yield text[i : i + 8]
