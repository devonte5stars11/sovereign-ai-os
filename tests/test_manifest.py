"""Provider manifest loading + capability declaration."""

import pytest
from ai_os_kernel import load_manifest, validate_manifest
from ai_os_kernel.manifest import ManifestError, ProviderManifest


def test_load_single_manifest(providers_dir):
    m = load_manifest(providers_dir / "gemini.yaml")
    assert m.provider == "gemini"
    assert m.supports("long_context")
    assert m.supports("vision")
    assert not m.supports("browser")


def test_gemini_is_not_local(providers_dir):
    m = load_manifest(providers_dir / "gemini.yaml")
    assert not m.is_local


def test_local_manifest_is_local(providers_dir):
    m = load_manifest(providers_dir / "local.yaml")
    assert m.is_local
    assert m.cost_input_per_1k == 0.0


def test_load_all_manifests(manifests):
    names = {m.provider for m in manifests}
    assert names == {"gemini", "gpt", "grok", "local"}


def test_supports_all(tmp_path):
    from ai_os_kernel.manifest import ProviderManifest

    m = ProviderManifest(provider="x", version="1", capabilities={"a", "b"})
    assert m.supports_all(["a", "b"])
    assert not m.supports_all(["a", "z"])


def test_cost_estimate():
    from ai_os_kernel.manifest import ProviderManifest

    m = ProviderManifest(
        provider="x",
        version="1",
        capabilities=set(),
        cost_input_per_1k=1.0,
        cost_output_per_1k=4.0,
    )
    # 1k input * 1.0 + 1k output * 4.0 => 5.0
    assert m.estimated_cost_usd(1000, 1000) == pytest.approx(5.0)
    assert m.estimated_cost_usd(0, 0) == 0.0


def test_missing_manifest_raises(tmp_path):
    with pytest.raises(ManifestError):
        load_manifest(tmp_path / "nope.yaml")


def test_manifest_requires_provider(tmp_path):

    bad = tmp_path / "bad.yaml"
    bad.write_text("capabilities: {long_context: true}\n", encoding="utf-8")
    with pytest.raises(ManifestError):
        load_manifest(bad)


# -- typed-config validation (ADR-0006) ----------------------------------


def test_validate_manifest_unknown_capability():
    m = ProviderManifest(provider="x", version="1", capabilities={"long_context", "hoverboard"})
    problems = validate_manifest(m)
    assert any("hoverboard" in p for p in problems)


def test_validate_manifest_negative_cost():
    m = ProviderManifest(
        provider="x",
        version="1",
        capabilities={"json_mode"},
        cost_input_per_1k=-1.0,
    )
    assert any("negative" in p for p in validate_manifest(m))


def test_validate_manifest_ok():
    m = ProviderManifest(provider="x", version="1", capabilities={"json_mode", "streaming"})
    assert validate_manifest(m) == []


def test_load_manifest_rejects_invalid(tmp_path):
    import yaml

    bad = tmp_path / "bad.yaml"
    bad.write_text(
        yaml.safe_dump(
            {
                "provider": "x",
                "version": "1",
                "capabilities": {"json_mode": True, "bogus_cap": True},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="invalid manifest"):
        load_manifest(bad)
