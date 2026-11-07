"""Global installation engine for installing Dev-Team assets into ~/.dev-team/."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from dev_team.core.constants import (
    DEFAULT_PLATFORM,
    DEFAULT_VERSION,
    GLOBAL_CONFIG_FILE,
    GLOBAL_HOME_DIR,
    GLOBAL_MANIFEST_FILE,
    GLOBAL_VERSION_FILE,
)
from dev_team.core.exceptions import DevTeamError, ManifestError
from dev_team.core.manifest import Manifest
from dev_team.core.provenance import compute_file_sha256
from dev_team.detection.platform import get_platform_discovery_dir
from dev_team.detection.workspace import find_canonical_source_repo
from dev_team.installation.strategies import copy_file_safe


@dataclass
class GlobalInstallResult:
    """Summary of global installation execution."""

    success: bool
    target_directory: Path
    version: str
    platform: str
    installed_skills: List[str] = field(default_factory=list)
    total_files_installed: int = 0
    manifest_path: Optional[Path] = None
    manifest: Optional[Manifest] = None
    platform_projection_dir: Optional[Path] = None
    messages: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def install_global(
    source_repo: Optional[Path | str] = None,
    target_dir: Optional[Path | str] = None,
    platform: str = DEFAULT_PLATFORM,
    specific_skill: Optional[str] = None,
    project_platform: bool = True,
    dry_run: bool = False,
    verbose: bool = False,
) -> GlobalInstallResult:
    """
    Installs canonical Dev-Team assets (skills, templates, adapters, version)
    into the global home directory (~/.dev-team/), generates manifest.json,
    and optionally configures platform skill discovery.
    """
    # 1. Resolve source repository
    src_path = find_canonical_source_repo(source_repo)
    if not src_path or not src_path.is_dir():
        err = f"Could not locate canonical Dev-Team repository at '{source_repo or 'auto-detect'}'."
        return GlobalInstallResult(
            success=False,
            target_directory=Path(target_dir) if target_dir else Path.home() / GLOBAL_HOME_DIR,
            version=DEFAULT_VERSION,
            platform=platform,
            errors=[err],
        )

    # 2. Resolve destination directory
    dest_path = Path(target_dir).resolve() if target_dir else Path.home() / GLOBAL_HOME_DIR
    skills_src = src_path / "skills"
    templates_src = src_path / "templates"
    adapters_src = src_path / "adapters"

    if not skills_src.is_dir():
        return GlobalInstallResult(
            success=False,
            target_directory=dest_path,
            version=DEFAULT_VERSION,
            platform=platform,
            errors=[f"Source skills directory missing: {skills_src}"],
        )

    result = GlobalInstallResult(
        success=True,
        target_directory=dest_path,
        version=DEFAULT_VERSION,
        platform=platform,
    )

    manifest = Manifest(
        dev_team_version=DEFAULT_VERSION,
        installation_mode="copy",
        platform=platform,
        installed_at=datetime.now(timezone.utc).isoformat(),
    )

    files_installed_count = 0
    installed_skills: List[str] = []

    # 3. Install Skills
    skills_dest = dest_path / "skills"
    skill_folders = [
        d for d in skills_src.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    ]

    if specific_skill:
        skill_folders = [d for d in skill_folders if d.name == specific_skill]
        if not skill_folders:
            result.success = False
            result.errors.append(f"Skill '{specific_skill}' not found in canonical source.")
            return result

    for skill_dir in skill_folders:
        installed_skills.append(skill_dir.name)
        target_skill_dir = skills_dest / skill_dir.name

        for file_path in skill_dir.rglob("*"):
            if file_path.is_file():
                rel_to_skill = file_path.relative_to(skills_src)
                dest_file = skills_dest / rel_to_skill
                sha = compute_file_sha256(file_path)

                if not dry_run:
                    copy_file_safe(file_path, dest_file)

                # Relative to global root
                rel_global = f"skills/{rel_to_skill.as_posix()}"
                manifest.add_artifact(
                    path=rel_global,
                    artifact_type="skill",
                    managed_by_dev_team=True,
                    strategy="copy",
                    source=file_path.as_posix(),
                    source_hash=sha,
                )
                files_installed_count += 1

    result.installed_skills = installed_skills

    # 4. Install Templates
    if templates_src.is_dir():
        templates_dest = dest_path / "templates"
        for file_path in templates_src.rglob("*"):
            if file_path.is_file():
                rel_to_templates = file_path.relative_to(templates_src)
                dest_file = templates_dest / rel_to_templates
                sha = compute_file_sha256(file_path)

                if not dry_run:
                    copy_file_safe(file_path, dest_file)

                rel_global = f"templates/{rel_to_templates.as_posix()}"
                manifest.add_artifact(
                    path=rel_global,
                    artifact_type="template",
                    managed_by_dev_team=True,
                    strategy="copy",
                    source=file_path.as_posix(),
                    source_hash=sha,
                )
                files_installed_count += 1

    # 5. Install Adapters
    if adapters_src.is_dir():
        adapters_dest = dest_path / "adapters"
        for file_path in adapters_src.rglob("*"):
            if file_path.is_file():
                rel_to_adapters = file_path.relative_to(adapters_src)
                dest_file = adapters_dest / rel_to_adapters
                sha = compute_file_sha256(file_path)

                if not dry_run:
                    copy_file_safe(file_path, dest_file)

                rel_global = f"adapters/{rel_to_adapters.as_posix()}"
                manifest.add_artifact(
                    path=rel_global,
                    artifact_type="adapter",
                    managed_by_dev_team=True,
                    strategy="copy",
                    source=file_path.as_posix(),
                    source_hash=sha,
                )
                files_installed_count += 1

    # 6. Write version file
    version_file = dest_path / GLOBAL_VERSION_FILE
    if not dry_run:
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text(f"{DEFAULT_VERSION}\n", encoding="utf-8")

    manifest.add_artifact(
        path=GLOBAL_VERSION_FILE,
        artifact_type="configuration",
        managed_by_dev_team=True,
        strategy="managed_file",
        source=None,
        source_hash=compute_file_sha256(version_file) if not dry_run else None,
    )
    files_installed_count += 1

    # 7. Write global default config.yaml if not existing
    config_file = dest_path / GLOBAL_CONFIG_FILE
    if not config_file.exists() and not dry_run:
        config_src = src_path / "config" / "defaults.yaml"
        if config_src.is_file():
            shutil.copy2(config_src, config_file)
        else:
            config_file.write_text(f"version: 1\ndefault_platform: {platform}\n", encoding="utf-8")

    if config_file.exists():
        manifest.add_artifact(
            path=GLOBAL_CONFIG_FILE,
            artifact_type="configuration",
            managed_by_dev_team=True,
            strategy="managed_file",
            source=None,
            source_hash=compute_file_sha256(config_file) if not dry_run else None,
        )
        files_installed_count += 1

    # 8. Platform skill projection (optional)
    if project_platform and platform:
        # Determine platform global discovery folder
        plat_home = dest_path.parent if target_dir else Path.home()
        plat_discovery = get_platform_discovery_dir(platform, plat_home)

        if not dry_run:
            plat_discovery.mkdir(parents=True, exist_ok=True)
            result.platform_projection_dir = plat_discovery

            # Link or copy each skill into platform discovery folder
            for sname in installed_skills:
                src_skill = skills_dest / sname
                dst_skill = plat_discovery / sname
                if not dst_skill.exists():
                    try:
                        # Attempt to copy or directory link
                        shutil.copytree(src_skill, dst_skill, dirs_exist_ok=True)
                    except Exception as e:
                        result.messages.append(f"Platform projection notice: {e}")

    # 9. Save manifest.json
    manifest_file = dest_path / GLOBAL_MANIFEST_FILE
    result.manifest_path = manifest_file
    result.manifest = manifest
    result.total_files_installed = files_installed_count

    if not dry_run:
        manifest.save(manifest_file)

    result.messages.append(
        f"Installed {len(installed_skills)} skills, templates, and adapters ({files_installed_count} total artifacts) into {dest_path}"
    )

    return result

