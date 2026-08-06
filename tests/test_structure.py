"""Structural validation: the repo layout and its assets are complete and parse."""

import yaml


def test_repo_layout_exists(repo_root):
    expected_dirs = [
        "00-core", "souls", "specs", "memory", "providers", "profiles",
        "graphs", "graph-registry", "kernel", "tests", "docs/adr",
        "knowledge", "artifact-registry", "evaluation", "operations",
        "plugins", "capabilities",
    ]
    for d in expected_dirs:
        assert (repo_root / d).is_dir(), f"missing directory: {d}"


def test_all_nine_souls_present(soul_names):
    assert set(soul_names) == {
        "main", "visionary", "blueprint-genesis", "closer", "intelligence",
        "orchestrator", "hvac-expert", "cdl-expert", "rainmaker",
    }


def test_specstack_present(repo_root):
    for f in ["brand.md", "frame.md", "ui.md"]:
        assert (repo_root / "specs" / f).is_file(), f"missing spec: {f}"


def test_core_files_present(repo_root):
    for f in ["SOUL.md", "META.md", "design.md", "principles.md", "constitution.md", "maturity-model.md"]:
        assert (repo_root / "00-core" / f).is_file(), f"missing core file: {f}"


def test_provider_manifests_parse(providers_dir):
    manifests = sorted(providers_dir.glob("*.yaml"))
    names = {m.stem for m in manifests}
    assert names == {"gemini", "gpt", "grok", "local"}, f"unexpected manifests: {names}"
    for m in manifests:
        data = yaml.safe_load(m.read_text(encoding="utf-8"))
        assert data.get("provider"), f"{m.name} missing provider"
        assert isinstance(data.get("capabilities"), dict)


def test_capability_catalog_present(repo_root):
    raw = (repo_root / "capabilities" / "catalog.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    assert "long_context" in data["capabilities"]
    assert "local" in data["capabilities"]


def test_soulvault_parse_and_merge_rules(profiles_path):
    data = yaml.safe_load(profiles_path.read_text(encoding="utf-8"))
    assert data.get("default_soul") == "main"
    assert "merge_rules" in data
    assert len(data["souls"]) == 9
