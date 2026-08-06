"""Typed Artifact Registry.

Every artifact receives a unique ID and full provenance metadata (type,
creator, workflow, graph version, source, trust, checksum, timestamp). This
enables reproducibility and lineage tracking.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


class ArtifactError(Exception):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Artifact:
    """A versioned, provable artifact with provenance + confidence metadata."""

    type: str
    creator: str
    workflow: str = ""
    graph_version: int = 0
    source: str = ""
    trust: float = 0.5  # 0..1 (legacy trust score)
    content: str = ""
    confidence: float = 0.0  # 0..1 knowledge-confidence score (see ADR-0009)
    freshness: str = ""  # ISO timestamp of last review/refresh
    verified_by: str = ""  # actor who verified ("human", an evaluator, etc.)
    expiry: str = ""  # ISO expiration, empty = no expiry
    artifact_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    checksum: str = ""
    timestamp: str = field(default_factory=_now)

    def compute_checksum(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()

    def seal(self) -> Artifact:
        """Stamp the checksum so the artifact is immutable/verifiable."""
        self.checksum = self.compute_checksum()
        return self

    def verify(self) -> bool:
        """True if the stored checksum matches the current content."""
        return bool(self.checksum) and self.checksum == self.compute_checksum()

    def mark_verified(self, by: str, freshness: str | None = None) -> Artifact:
        """Record that this artifact was verified; bumps freshness."""
        self.verified_by = by
        self.freshness = freshness or _now()
        return self

    @property
    def is_expired(self) -> bool:
        """True if this artifact has passed its expiry (if any)."""
        if not self.expiry:
            return False
        try:
            from datetime import datetime as _dt

            expiry = _dt.fromisoformat(self.expiry)
            return _dt.now(expiry.tzinfo) > expiry
        except ValueError:
            return False

    def to_dict(self) -> dict:
        return {
            "artifact_id": self.artifact_id,
            "type": self.type,
            "creator": self.creator,
            "workflow": self.workflow,
            "graph_version": self.graph_version,
            "source": self.source,
            "trust": self.trust,
            "confidence": self.confidence,
            "freshness": self.freshness,
            "verified_by": self.verified_by,
            "expiry": self.expiry,
            "checksum": self.checksum,
            "timestamp": self.timestamp,
        }


class ArtifactRegistry:
    """Stores and verifies artifacts, keyed by stable artifact_id."""

    def __init__(self) -> None:
        self._store: dict[str, Artifact] = {}

    def add(self, artifact: Artifact) -> Artifact:
        if artifact.artifact_id in self._store:
            raise ArtifactError(f"artifact already registered: {artifact.artifact_id}")
        artifact.seal()
        self._store[artifact.artifact_id] = artifact
        return artifact

    def get(self, artifact_id: str) -> Artifact | None:
        return self._store.get(artifact_id)

    def verify(self, artifact_id: str) -> bool:
        art = self._store.get(artifact_id)
        return art is not None and art.verify()

    def __len__(self) -> int:
        return len(self._store)

    def items(self) -> dict[str, Artifact]:
        return dict(self._store)
