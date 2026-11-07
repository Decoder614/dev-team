"""Unit tests for installation manifest and provenance engine."""

import json
from pathlib import Path
import pytest

from dev_team.core.constants import DEFAULT_VERSION
from dev_team.core.exceptions import ManifestError
from dev_team.core.manifest import Manifest, ManifestArtifact
from dev_team.core.provenance import compute_directory_hashes, compute_file_sha256


def test_compute_file_sha256(tmp_path):
    """Verify SHA-256 calculation."""
    f = tmp_path / "sample.txt"
    f.write_text("hello dev-team\n", encoding="utf-8")
    sha = compute_file_sha256(f)
    assert isinstance(sha, str)
    assert len(sha) == 64


def test_manifest_creation_and_serialization(tmp_path):
    """Verify manifest creation, validation, and JSON serialization."""
    manifest = Manifest(
        dev_team_version=DEFAULT_VERSION,
        installation_mode="hybrid",
        platform="codex",
    )
    manifest.add_artifact(
        path="skills/flutter-development/SKILL.md",
        artifact_type="skill",
        managed_by_dev_team=True,
        strategy="copy",
        source="skills/flutter-development/SKILL.md",
        source_hash="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    )

    errors = manifest.validate_schema()
    assert len(errors) == 0

    out_file = tmp_path / "manifest.json"
    manifest.save(out_file)
    assert out_file.is_file()

    # Load back
    loaded = Manifest.load(out_file)
    assert loaded.dev_team_version == DEFAULT_VERSION
    assert loaded.installation_mode == "hybrid"
    assert loaded.platform == "codex"
    assert len(loaded.artifacts) == 1
    assert loaded.artifacts[0].path == "skills/flutter-development/SKILL.md"


def test_manifest_validation_rejects_invalid_values():
    """Verify schema validator catches invalid fields."""
    # Invalid installation mode
    m = Manifest(installation_mode="invalid_mode")
    errors = m.validate_schema()
    assert any("installation_mode" in e for e in errors)

    # Invalid artifact type
    m2 = Manifest()
    with pytest.raises(ManifestError):
        m2.add_artifact(path="foo", artifact_type="non_existent_type")


def test_manifest_drift_detection(tmp_path):
    """Verify manifest verification detects intact, missing, and modified files."""
    f1 = tmp_path / "intact.txt"
    f1.write_text("intact content\n", encoding="utf-8")
    h1 = compute_file_sha256(f1)

    f2 = tmp_path / "modified.txt"
    f2.write_text("original content\n", encoding="utf-8")
    h2 = compute_file_sha256(f2)

    manifest = Manifest()
    manifest.add_artifact("intact.txt", "documentation", source_hash=h1)
    manifest.add_artifact("modified.txt", "documentation", source_hash=h2)
    manifest.add_artifact("missing.txt", "documentation", source_hash="dummy")

    # Modify f2 on disk
    f2.write_text("user modified content\n", encoding="utf-8")

    verification = manifest.verify(tmp_path)
    assert verification.all_valid is False
    assert "intact.txt" in verification.intact_artifacts
    assert "modified.txt" in verification.modified_artifacts
    assert "missing.txt" in verification.missing_artifacts
    assert verification.missing_count == 1
    assert verification.modified_count == 1
    assert verification.intact_count == 1

