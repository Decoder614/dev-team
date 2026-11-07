"""Unit tests for repository and workspace detection."""

import os
from pathlib import Path
import pytest

from dev_team.detection.workspace import (
    detect_existing_configuration,
    detect_workspace,
    detect_workspace_type,
    find_canonical_source_repo,
    find_git_root,
)


def test_find_git_root_in_current_repo():
    """Verify git root is discovered when executing inside dev-team repository."""
    repo_root = Path(__file__).resolve().parents[2]
    found = find_git_root(repo_root)
    assert found is not None
    assert (found / ".git").exists()


def test_find_git_root_in_nested_directory():
    """Verify git root discovery walks up from deeply nested directories."""
    deep_path = Path(__file__).resolve().parent
    found = find_git_root(deep_path)
    assert found is not None
    assert (found / ".git").exists()


def test_find_git_root_non_git_dir(tmp_path):
    """Verify non-git directories return None."""
    non_git = tmp_path / "plain_dir"
    non_git.mkdir()
    assert find_git_root(non_git) is None


def test_detect_workspace_type_empty(tmp_path):
    """Verify empty directory classification."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    assert detect_workspace_type(empty_dir) == "EMPTY"


def test_detect_workspace_type_canonical():
    """Verify canonical Dev-Team repository classification."""
    repo_root = Path(__file__).resolve().parents[2]
    assert detect_workspace_type(repo_root) == "DEV_TEAM_REPO"


def test_detect_workspace_type_target_project(tmp_path):
    """Verify target project classification by manifest or .dev-team/ directory."""
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    (project_dir / "package.json").write_text("{}", encoding="utf-8")
    assert detect_workspace_type(project_dir) == "TARGET_PROJECT"

    # Also with .dev-team directory
    p2 = tmp_path / "onboarded_project"
    p2.mkdir()
    (p2 / ".dev-team").mkdir()
    assert detect_workspace_type(p2) == "TARGET_PROJECT"


def test_detect_existing_configuration(tmp_path):
    """Verify extraction of existing project configuration and documentation."""
    proj = tmp_path / "configured_repo"
    proj.mkdir()
    dt = proj / ".dev-team"
    dt.mkdir()
    (dt / "config.yaml").write_text("version: 1\n", encoding="utf-8")
    (proj / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")

    cfg = detect_existing_configuration(proj)
    assert cfg["has_dev_team_dir"] is True
    assert cfg["has_config"] is True
    assert cfg["has_instructions"] is True
    assert cfg["has_context"] is False


def test_find_canonical_source_repo():
    """Verify canonical source repo discovery."""
    source = find_canonical_source_repo()
    assert source is not None
    assert (source / "skills").is_dir()
    assert (source / "templates").is_dir()
    assert (source / "agents").is_dir()

