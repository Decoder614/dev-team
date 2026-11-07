"""Unit tests for global skill and template installation."""

from pathlib import Path
import pytest

from dev_team.core.constants import DEFAULT_VERSION, GLOBAL_MANIFEST_FILE, GLOBAL_VERSION_FILE
from dev_team.installation.global_installer import install_global


def test_install_global_to_target_dir(tmp_path):
    """Verify install_global populates skills, templates, version, and manifest in destination."""
    dest = tmp_path / "global_dest"

    result = install_global(
        target_dir=dest,
        platform="codex",
        project_platform=False,
    )

    assert result.success is True
    assert dest.is_dir()
    assert (dest / "skills").is_dir()
    assert (dest / "templates").is_dir()
    assert (dest / "adapters").is_dir()

    # Version file
    version_file = dest / GLOBAL_VERSION_FILE
    assert version_file.is_file()
    assert version_file.read_text(encoding="utf-8").strip() == DEFAULT_VERSION

    # Manifest file
    manifest_file = dest / GLOBAL_MANIFEST_FILE
    assert manifest_file.is_file()
    assert result.manifest is not None
    assert len(result.installed_skills) >= 9

    # Check verification on installed files
    verification = result.manifest.verify(dest)
    assert verification.all_valid is True
    assert verification.missing_count == 0
    assert verification.modified_count == 0


def test_install_global_single_skill(tmp_path):
    """Verify installing only a single specified skill."""
    dest = tmp_path / "single_skill_dest"

    result = install_global(
        target_dir=dest,
        specific_skill="flutter-development",
        project_platform=False,
    )

    assert result.success is True
    assert result.installed_skills == ["flutter-development"]
    assert (dest / "skills" / "flutter-development" / "SKILL.md").is_file()
    assert not (dest / "skills" / "system-design").exists()

