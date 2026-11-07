"""Workspace and Git repository detection engine for Dev-Team."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from dev_team.core.constants import (
    INSTRUCTIONS_FILE,
    PROJECT_CONFIG_FILE,
    PROJECT_CONTEXT_FILE,
    PROJECT_DEV_TEAM_DIR,
    PROJECT_MANIFEST_FILE,
    RULES_FILE,
)


@dataclass
class WorkspaceInfo:
    """Detailed summary of a detected workspace directory."""

    path: Path
    workspace_type: str
    is_git_repo: bool
    git_root: Optional[Path] = None
    is_canonical_dev_team: bool = False
    is_target_project: bool = False
    is_empty: bool = False
    configuration: Dict[str, Any] = field(default_factory=dict)


def find_git_root(start_dir: Path | str) -> Optional[Path]:
    """
    Traverses upwards from start_dir to find the root of a Git repository.
    Recognizes both directory `.git` and file `.git` (used by worktrees and submodules).
    """
    current = Path(start_dir).resolve()
    # If a file was passed, start from its parent directory
    if current.is_file():
        current = current.parent

    for parent in [current, *current.parents]:
        git_entry = parent / ".git"
        if git_entry.exists():
            return parent
    return None


def detect_workspace_type(dir_path: Path | str) -> str:
    """
    Classifies a directory structure into:
    - EMPTY: contains no non-hidden files
    - DEV_TEAM_REPO: canonical Dev-Team framework repository
    - TARGET_PROJECT: application repository with .dev-team or build manifests
    - GIT_REPO: standard Git repository without dev-team artifacts
    - DIRECTORY: arbitrary directory with files, not tracked by git
    """
    target = Path(dir_path).resolve()
    if not target.exists() or not target.is_dir():
        return "UNKNOWN"

    # Check for empty directory (ignoring OS files like .DS_Store, Thumbs.db)
    items = [
        p.name
        for p in target.iterdir()
        if p.name not in [".DS_Store", "Thumbs.db", ".git"]
    ]
    if not items:
        # If there's only .git or nothing at all
        if (target / ".git").exists():
            return "GIT_REPO"
        return "EMPTY"

    # Check if this is the canonical Dev-Team framework repository
    canonical_markers = ["skills", "agents", "workflows", "templates", "cli"]
    if all((target / marker).is_dir() for marker in canonical_markers):
        return "DEV_TEAM_REPO"

    # Check if target is an onboarded or pending target project
    dev_team_dir = target / PROJECT_DEV_TEAM_DIR
    if dev_team_dir.is_dir():
        return "TARGET_PROJECT"

    # Check common project manifest files
    project_indicators = [
        "pubspec.yaml",       # Flutter / Dart
        "package.json",       # Node.js
        "pyproject.toml",     # Python
        "Cargo.toml",         # Rust
        "go.mod",             # Go
        "pom.xml",            # Java Maven
        "build.gradle",       # Java / Android Gradle
        "Gemfile",            # Ruby
        "composer.json",      # PHP
        "CMakeLists.txt",     # C/C++
    ]
    if any((target / indicator).exists() for indicator in project_indicators):
        return "TARGET_PROJECT"

    # Check if standard git repo
    if (target / ".git").exists():
        return "GIT_REPO"

    return "DIRECTORY"


def detect_existing_configuration(dir_path: Path | str) -> Dict[str, Any]:
    """
    Inspects target directory for existing Dev-Team scaffolding, configuration,
    documentation, and platform projections.
    """
    target = Path(dir_path).resolve()
    dev_team_dir = target / PROJECT_DEV_TEAM_DIR
    has_dev_team_dir = dev_team_dir.is_dir()

    config_file = dev_team_dir / PROJECT_CONFIG_FILE
    has_config = config_file.is_file()

    context_file = dev_team_dir / PROJECT_CONTEXT_FILE
    has_context = context_file.is_file()

    manifest_file = dev_team_dir / PROJECT_MANIFEST_FILE
    has_manifest = manifest_file.is_file()

    instructions_file = target / INSTRUCTIONS_FILE
    has_instructions = instructions_file.is_file()

    rules_file = target / RULES_FILE
    has_rules = rules_file.is_file()

    project_skills_dir = dev_team_dir / "skills"
    has_project_skills = project_skills_dir.is_dir()
    project_skills: List[str] = []
    if has_project_skills:
        project_skills = [
            p.name
            for p in project_skills_dir.iterdir()
            if p.is_dir() and (p / "SKILL.md").is_file()
        ]

    # Projections
    projections: Dict[str, bool] = {
        "agents_skills": (target / ".agents" / "skills").exists(),
        "codex_skills": (target / ".codex" / "skills").exists(),
        "claude_skills": (target / ".claude" / "skills").exists(),
    }

    return {
        "has_dev_team_dir": has_dev_team_dir,
        "dev_team_dir": str(dev_team_dir) if has_dev_team_dir else None,
        "has_config": has_config,
        "config_path": str(config_file) if has_config else None,
        "has_context": has_context,
        "context_path": str(context_file) if has_context else None,
        "has_manifest": has_manifest,
        "manifest_path": str(manifest_file) if has_manifest else None,
        "has_instructions": has_instructions,
        "instructions_path": str(instructions_file) if has_instructions else None,
        "has_rules": has_rules,
        "rules_path": str(rules_file) if has_rules else None,
        "has_project_skills": has_project_skills,
        "project_skills": project_skills,
        "projections": projections,
    }


def find_canonical_source_repo(start_path: Optional[Path | str] = None) -> Optional[Path]:
    """
    Locates the source Dev-Team canonical repository by checking:
    1. start_path or current working directory and its parents
    2. DEV_TEAM_SOURCE environment variable
    3. Path relative to this package installation
    """
    candidates: List[Path] = []

    if start_path:
        candidates.append(Path(start_path).resolve())

    cwd = Path.cwd().resolve()
    candidates.append(cwd)
    candidates.extend(cwd.parents)

    env_source = os.environ.get("DEV_TEAM_SOURCE")
    if env_source:
        candidates.append(Path(env_source).resolve())

    # Codebase root relative to this file: cli/src/detection/workspace.py -> 3 levels up = dev-team root
    relative_root = Path(__file__).resolve().parents[3]
    candidates.append(relative_root)

    for cand in candidates:
        if cand.is_dir():
            canonical_markers = ["skills", "agents", "workflows", "templates", "cli"]
            if all((cand / marker).is_dir() for marker in canonical_markers):
                return cand

    return None


def detect_workspace(path: Path | str) -> WorkspaceInfo:
    """Generates complete WorkspaceInfo for a specified directory path."""
    target = Path(path).resolve()
    git_root = find_git_root(target)
    ws_type = detect_workspace_type(target)
    config = detect_existing_configuration(target)

    is_canonical = (ws_type == "DEV_TEAM_REPO")
    is_target = (ws_type == "TARGET_PROJECT" or config["has_dev_team_dir"])
    is_empty = (ws_type == "EMPTY")

    return WorkspaceInfo(
        path=target,
        workspace_type=ws_type,
        is_git_repo=(git_root is not None),
        git_root=git_root,
        is_canonical_dev_team=is_canonical,
        is_target_project=is_target,
        is_empty=is_empty,
        configuration=config,
    )

