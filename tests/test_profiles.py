"""SoulVault profiles: loading, selection, and merging."""

import pytest
from ai_os_kernel.profiles import MergedProfile, ProfileError


def test_load_all_souls(profile_manager):
    assert set(profile_manager.names) == {
        "main",
        "visionary",
        "blueprint-genesis",
        "closer",
        "intelligence",
        "orchestrator",
        "hvac-expert",
        "cdl-expert",
        "rainmaker",
    }


def test_get_single_profile(profile_manager):
    p = profile_manager.get("cdl-expert")
    assert p is not None
    assert p.domain == "trucking_logistics"
    assert "code_execution" in p.preferred_capabilities


def test_merge_single(profile_manager):
    merged = profile_manager.merge("main")
    assert isinstance(merged, MergedProfile)
    assert merged.authority == 10  # main's authority


def test_merge_multiple_dedupes_and_max_authority(profile_manager):
    merged = profile_manager.merge("main", "cdl-expert", "closer", "visionary")
    assert merged.authority == 10  # max
    # overlays from all four, deduped (each points to its own soul file so all present)
    assert any("cdl-expert" in o for o in merged.prompt_overlays)
    assert any("visionary" in o for o in merged.prompt_overlays)
    # tool_access union
    assert "knowledge" in merged.tool_access
    assert "communication" in merged.tool_access


def test_merge_tool_union(profile_manager):
    merged = profile_manager.merge("intelligence", "orchestrator")
    assert "scheduler" in merged.tool_access
    assert "web" in merged.tool_access


def test_merge_unknown_soul_raises(profile_manager):
    with pytest.raises(ProfileError):
        profile_manager.merge("main", "does-not-exist")


def test_merge_none_raises(profile_manager):
    with pytest.raises(ProfileError):
        profile_manager.merge()


def test_merge_preferred_capabilities_union(profile_manager):
    merged = profile_manager.merge("cdl-expert", "visionary")
    assert "code_execution" in merged.preferred_capabilities
    assert "image_generation" in merged.preferred_capabilities
