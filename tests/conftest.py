"""Shared fixtures / path setup for the kernel test suite."""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = REPO_ROOT / "kernel"

if str(KERNEL_DIR) not in sys.path:
    sys.path.insert(0, str(KERNEL_DIR))


# Expose a stable repo-root path to every test module.
@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def providers_dir(repo_root: Path) -> Path:
    return repo_root / "providers"


@pytest.fixture
def profiles_path(repo_root: Path) -> Path:
    return repo_root / "profiles" / "soulvault.yaml"


@pytest.fixture
def soul_names(repo_root: Path):
    souls_dir = repo_root / "souls"
    return sorted(p.stem for p in souls_dir.glob("*.md"))


@pytest.fixture
def manifests(providers_dir):
    from ai_os_kernel import load_manifests

    return load_manifests(providers_dir)


@pytest.fixture
def profile_manager(profiles_path):
    from ai_os_kernel import ProfileManager

    return ProfileManager(profiles_path)
