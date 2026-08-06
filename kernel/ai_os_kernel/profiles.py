"""SoulVault as data-driven composable profiles.

The user-facing "souls" remain as ergonomic markdown files; this module is the
machine-readable implementation. Each soul is a profile that can be merged with
others (CEO + CDL Expert + Closer + Visionary) following declared merge rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml

    _HAS_YAML = True
except Exception:  # noqa: BLE001 - pragma: no cover
    _HAS_YAML = False


class ProfileError(Exception):
    pass


@dataclass
class Profile:
    name: str
    role: str = ""
    domain: str = "general"
    authority: int = 0
    tool_access: list[str] = field(default_factory=list)
    prompt_overlays: list[str] = field(default_factory=list)
    evaluation_rules: dict[str, object] = field(default_factory=dict)
    preferred_capabilities: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, name: str, data: dict) -> Profile:
        return cls(
            name=name,
            role=str(data.get("role", "")),
            domain=str(data.get("domain", "general")),
            authority=int(data.get("authority", 0)),
            tool_access=list(data.get("tool_access", [])),
            prompt_overlays=list(data.get("prompt_overlays", [])),
            evaluation_rules=data.get("evaluation_rules", {}) or {},
            preferred_capabilities=list(data.get("preferred_capabilities", [])),
        )


@dataclass
class MergedProfile:
    """The result of merging one or more selected souls."""

    names: list[str]
    role: str
    domains: list[str]
    authority: int
    tool_access: list[str]
    prompt_overlays: list[str]
    evaluation_rules: dict[str, object]
    preferred_capabilities: list[str]

    def describe(self) -> str:
        return (
            f"Soul(s) selected: {' + '.join(self.names)}\n"
            f"role={self.role} | authority={self.authority} | domains={', '.join(self.domains)}"
        )


class ProfileManager:
    """Loads souls from a YAML vault and merges selections."""

    def __init__(self, source: str | Path = "profiles/soulvault.yaml"):
        self.source = Path(source)
        self._profiles: dict[str, Profile] = {}
        self._merge_rules: dict[str, str] = {}
        if self.source.exists():
            self._load()

    def _load(self) -> None:
        if not _HAS_YAML:  # pragma: no cover
            raise ProfileError("PyYAML required to load soulvault.")
        with open(self.source, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        souls = data.get("souls", {}) or {}
        for name, raw in souls.items():
            self._profiles[name] = Profile.from_dict(name, raw)
        self._merge_rules = data.get("merge_rules", {}) or {}

    @property
    def names(self) -> list[str]:
        return sorted(self._profiles)

    def __contains__(self, name: str) -> bool:
        return name in self._profiles

    def get(self, name: str) -> Profile | None:
        return self._profiles.get(name)

    def merge(self, *names: str) -> MergedProfile:
        if not names:
            raise ProfileError("at least one soul must be selected")
        missing = [n for n in names if n not in self._profiles]
        if missing:
            raise ProfileError(f"unknown soul(s): {', '.join(missing)}")
        selected = [self._profiles[n] for n in names]

        # Merge rules from the vault, defaulting to sensible behavior.
        tool_access = sorted({t for p in selected for t in p.tool_access})
        overlays: list[str] = []
        for p in selected:
            for o in p.prompt_overlays:
                if o not in overlays:
                    overlays.append(o)
        preferred = sorted({c for p in selected for c in p.preferred_capabilities})
        authority = max((p.authority for p in selected), default=0)
        domains = [p.domain for p in selected]
        roles = [p.role for p in selected]

        # Evaluation rules: most specific wins (first non-empty is a proxy);
        # merge dicts shallowly with later profiles overlaying earlier ones.
        merged_eval: dict[str, object] = {}
        for p in selected:
            merged_eval.update(p.evaluation_rules)

        return MergedProfile(
            names=list(names),
            role="+".join(dict.fromkeys(roles)),
            domains=domains,
            authority=authority,
            tool_access=tool_access,
            prompt_overlays=overlays,
            evaluation_rules=merged_eval,
            preferred_capabilities=preferred,
        )
