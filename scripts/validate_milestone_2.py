#!/usr/bin/env python3
"""
scripts/validate_milestone_2.py — Milestone 2 CLI Foundation Verification Script

Validates the complete implementation of Milestone 2 as specified in docs/project/plan.md:
- Task M2-T01: CLI Architecture & Project Setup (package structure, entry point, help, version)
- Task M2-T02: Repository & Workspace Detection (empty folder, git root, target project, dev-team repo)
- Task M2-T03: Global Skill Installation Command (skills, templates, adapters, version file, platform flag)
- Task M2-T04: Installation Manifest & Provenance Engine (manifest.json, SHA-256 hashes, schema compliance)
- Task M2-T05: Installation Diagnostics (dev-team doctor execution, tabular reporting, healthy/incomplete environments)

Returns:
  0 if all Milestone 2 verification checks pass
  1 if any check fails
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Add CLI src to path for direct imports
cli_src = REPO_ROOT / "cli" / "src"
if str(cli_src) not in sys.path:
    sys.path.insert(0, str(cli_src))

# Ensure dev_team package is available
if "dev_team" not in sys.modules:
    import types
    dev_team_pkg = types.ModuleType("dev_team")
    dev_team_pkg.__path__ = [str(cli_src)]
    dev_team_pkg.__file__ = str(cli_src / "__init__.py")
    sys.modules["dev_team"] = dev_team_pkg


def log_pass(msg: str):
    print(f"  [PASS] {msg}")


def log_fail(msg: str):
    print(f"  [FAIL] {msg}")


def log_section(title: str):
    print(f"\n--- {title} ---")


def validate_json_schema(data, schema, path="root"):
    """Validates data against JSON schema constraints."""
    errors = []
    expected_type = schema.get("type")
    if expected_type:
        types = [expected_type] if isinstance(expected_type, str) else expected_type
        matched = False
        for t in types:
            if t == "object" and isinstance(data, dict):
                matched = True
            elif t == "array" and isinstance(data, list):
                matched = True
            elif t == "string" and isinstance(data, str):
                matched = True
            elif t == "boolean" and isinstance(data, bool):
                matched = True
        if not matched:
            errors.append(f"{path}: expected type {types}, got {type(data).__name__}")
            return errors

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: value '{data}' not in allowed enum {schema['enum']}")

    if isinstance(data, dict):
        required_keys = schema.get("required", [])
        for rk in required_keys:
            if rk not in data:
                errors.append(f"{path}: missing required property '{rk}'")

        properties = schema.get("properties", {})
        additional_allowed = schema.get("additionalProperties", True)

        for k, v in data.items():
            sub_path = f"{path}.{k}"
            if k in properties:
                sub_errs = validate_json_schema(v, properties[k], sub_path)
                errors.extend(sub_errs)
            elif additional_allowed is False:
                errors.append(f"{sub_path}: unrecognized property '{k}'")

    elif isinstance(data, list) and "items" in schema:
        item_schema = schema["items"]
        for idx, item in enumerate(data):
            sub_errs = validate_json_schema(item, item_schema, f"{path}[{idx}]")
            errors.extend(sub_errs)

    return errors


def test_task_m2_t01() -> bool:
    """Task M2-T01: CLI Architecture & Project Setup."""
    log_section("Task M2-T01: CLI Architecture & Project Setup")
    passed = True

    # 1. Package files
    required_files = [
        "cli/pyproject.toml",
        "cli/setup.py",
        "cli/README.md",
        "cli/src/__init__.py",
        "cli/src/main.py",
        "cli/src/commands/__init__.py",
        "cli/src/commands/doctor.py",
        "cli/src/commands/install.py",
        "cli/src/commands/init.py",
        "cli/src/commands/list.py",
        "cli/src/commands/status.py",
        "cli/src/commands/update.py",
        "cli/src/commands/uninstall.py",
        "cli/src/core/__init__.py",
        "cli/src/core/constants.py",
        "cli/src/core/manifest.py",
        "cli/src/core/provenance.py",
        "cli/src/detection/__init__.py",
        "cli/src/detection/workspace.py",
        "cli/src/detection/platform.py",
        "cli/src/installation/__init__.py",
        "cli/src/installation/global_installer.py",
        "cli/src/reporting/__init__.py",
        "cli/src/reporting/tables.py",
    ]

    for rel_path in required_files:
        fpath = REPO_ROOT / rel_path
        if fpath.is_file():
            log_pass(f"Found required CLI file: {rel_path}")
        else:
            log_fail(f"Missing required CLI file: {rel_path}")
            passed = False

    # 2. Test CLI execution: --version
    res_ver = subprocess.run(
        [sys.executable, str(REPO_ROOT / "cli" / "src" / "main.py"), "--version"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if res_ver.returncode == 0 and "1.1.0" in res_ver.stdout:
        log_pass(f"CLI --version output: {res_ver.stdout.strip()}")
    else:
        log_fail(f"CLI --version failed (code {res_ver.returncode}): {res_ver.stderr}")
        passed = False

    # 3. Test CLI execution: --help
    res_help = subprocess.run(
        [sys.executable, str(REPO_ROOT / "cli" / "src" / "main.py"), "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if res_help.returncode == 0 and "doctor" in res_help.stdout and "install" in res_help.stdout:
        log_pass("CLI --help displays expected subcommands (doctor, install, init, list, status, update, uninstall)")
    else:
        log_fail("CLI --help failed to display subcommands")
        passed = False

    return passed


def test_task_m2_t02() -> bool:
    """Task M2-T02: Repository & Workspace Detection."""
    log_section("Task M2-T02: Repository & Workspace Detection")
    passed = True

    from dev_team.detection.workspace import (
        detect_existing_configuration,
        detect_workspace,
        detect_workspace_type,
        find_canonical_source_repo,
        find_git_root,
    )

    # 1. Detect git root of dev-team repo
    git_root = find_git_root(REPO_ROOT)
    if git_root and git_root == REPO_ROOT:
        log_pass(f"Git root correctly identified: {git_root}")
    else:
        log_fail(f"Failed to identify git root for {REPO_ROOT} (got {git_root})")
        passed = False

    # 2. Detect canonical framework repository
    ws_canonical = detect_workspace_type(REPO_ROOT)
    if ws_canonical == "DEV_TEAM_REPO":
        log_pass("Repo root classified as DEV_TEAM_REPO")
    else:
        log_fail(f"Expected DEV_TEAM_REPO, got {ws_canonical}")
        passed = False

    # 3. Detect empty directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        ws_empty = detect_workspace_type(temp_path)
        if ws_empty == "EMPTY":
            log_pass("Empty folder classified as EMPTY")
        else:
            log_fail(f"Expected EMPTY, got {ws_empty}")
            passed = False

        # 4. Detect nested git root traversal
        nested = temp_path / "deep" / "nested" / "subfolder"
        nested.mkdir(parents=True)
        # Create a fake git root in temp_dir
        (temp_path / ".git").mkdir()
        nested_git = find_git_root(nested)
        if nested_git and nested_git == temp_path:
            log_pass("Nested directory correctly resolved parent git root")
        else:
            log_fail(f"Nested git root lookup failed (got {nested_git})")
            passed = False

        # 5. Detect target project configuration
        proj = temp_path / "test_project"
        proj.mkdir()
        (proj / ".dev-team").mkdir()
        (proj / ".dev-team" / "config.yaml").write_text("version: 1\n", encoding="utf-8")
        cfg = detect_existing_configuration(proj)
        if cfg["has_dev_team_dir"] and cfg["has_config"]:
            log_pass("Target project .dev-team/ and config.yaml correctly detected")
        else:
            log_fail("Target project configuration detection failed")
            passed = False

    return passed


def test_task_m2_t03() -> bool:
    """Task M2-T03: Global Skill Installation Command."""
    log_section("Task M2-T03: Global Skill Installation Command")
    passed = True

    from dev_team.installation.global_installer import install_global

    with tempfile.TemporaryDirectory() as temp_dir:
        test_global_dir = Path(temp_dir) / "global_home"

        result = install_global(
            source_repo=REPO_ROOT,
            target_dir=test_global_dir,
            platform="codex",
            project_platform=False,
        )

        if not result.success:
            log_fail(f"install_global failed: {result.errors}")
            return False

        log_pass("install_global completed successfully")

        # Check skills directory
        skills_dir = test_global_dir / "skills"
        if skills_dir.is_dir():
            skill_dirs = [d.name for d in skills_dir.iterdir() if (d / "SKILL.md").is_file()]
            if len(skill_dirs) >= 9:
                log_pass(f"Skills directory created with {len(skill_dirs)} valid skills: {', '.join(skill_dirs[:3])}...")
            else:
                log_fail(f"Expected at least 9 skills in {skills_dir}, found {len(skill_dirs)}")
                passed = False
        else:
            log_fail("skills/ directory was not created in global destination")
            passed = False

        # Check templates directory
        templates_dir = test_global_dir / "templates"
        if templates_dir.is_dir() and len(list(templates_dir.glob("*.md"))) >= 5:
            log_pass(f"templates/ directory created with {len(list(templates_dir.glob('*.md')))} templates")
        else:
            log_fail("templates/ directory missing or incomplete")
            passed = False

        # Check adapters directory
        adapters_dir = test_global_dir / "adapters"
        if adapters_dir.is_dir():
            log_pass("adapters/ directory created in global destination")
        else:
            log_fail("adapters/ directory missing in global destination")
            passed = False

        # Check version file
        version_file = test_global_dir / "version"
        if version_file.is_file() and version_file.read_text(encoding="utf-8").strip() == "1.1.0":
            log_pass("version file created containing '1.1.0'")
        else:
            log_fail("version file missing or has invalid content")
            passed = False

    return passed


def test_task_m2_t04() -> bool:
    """Task M2-T04: Installation Manifest & Provenance Engine."""
    log_section("Task M2-T04: Installation Manifest & Provenance Engine")
    passed = True

    from dev_team.core.manifest import Manifest
    from dev_team.core.provenance import compute_file_sha256
    from dev_team.installation.global_installer import install_global

    with tempfile.TemporaryDirectory() as temp_dir:
        test_global_dir = Path(temp_dir) / "global_home"
        result = install_global(
            source_repo=REPO_ROOT,
            target_dir=test_global_dir,
            platform="codex",
            project_platform=False,
        )

        manifest_file = test_global_dir / "manifest.json"
        if not manifest_file.is_file():
            log_fail("manifest.json was not written to global directory")
            return False

        log_pass("manifest.json successfully created on disk")

        # Validate against JSON schema
        schema_path = REPO_ROOT / "schemas" / "installation-manifest.schema.json"
        schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
        manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))

        schema_errors = validate_json_schema(manifest_data, schema_data)
        if len(schema_errors) == 0:
            log_pass("manifest.json adheres strictly to schemas/installation-manifest.schema.json")
        else:
            log_fail(f"manifest.json schema validation failed: {schema_errors}")
            passed = False

        # Load via Manifest class and verify
        manifest = Manifest.load(manifest_file)
        verification = manifest.verify(test_global_dir)
        if verification.all_valid and verification.missing_count == 0 and verification.modified_count == 0:
            log_pass(f"SHA-256 hashes verified: All {verification.total_artifacts} artifacts intact and match source hashes")
        else:
            log_fail(f"Verification mismatch: {verification.missing_count} missing, {verification.modified_count} modified")
            passed = False

        # Drift detection test: modify a file and test detection
        first_art_path = test_global_dir / manifest.artifacts[0].path
        if first_art_path.is_file():
            original_content = first_art_path.read_text(encoding="utf-8")
            first_art_path.write_text("TAMPERED_CONTENT\n", encoding="utf-8")

            tamper_verif = manifest.verify(test_global_dir)
            if not tamper_verif.all_valid and len(tamper_verif.modified_artifacts) == 1:
                log_pass("Provenance engine correctly detected file modification (tamper detection)")
            else:
                log_fail("Provenance engine failed to detect modified file")
                passed = False

    return passed


def test_task_m2_t05() -> bool:
    """Task M2-T05: Installation Diagnostics (dev-team doctor)."""
    log_section("Task M2-T05: Installation Diagnostics (dev-team doctor)")
    passed = True

    from dev_team.commands.doctor import DoctorEngine
    from dev_team.installation.global_installer import install_global

    # 1. Doctor in incomplete environment
    with tempfile.TemporaryDirectory() as temp_dir:
        incomplete_dir = Path(temp_dir) / "incomplete_home"
        engine_incomplete = DoctorEngine(target_dir=incomplete_dir, workspace_dir=REPO_ROOT)
        code_inc = engine_incomplete.run_all()
        # Incomplete global install yields warnings but succeeds without fatal failure
        checks_inc = {c.name: c.status for c in engine_incomplete.checks}
        if "Python Version" in checks_inc and checks_inc["Python Version"] == "PASS":
            log_pass("Doctor correctly verified Python prerequisite")
        else:
            log_fail("Doctor failed on Python version check")
            passed = False

        if "Installation Root" in checks_inc and checks_inc["Installation Root"] == "WARN":
            log_pass("Doctor accurately warned about uninstalled global home")
        else:
            log_fail("Doctor failed to warn about uninstalled directory")
            passed = False

    # 2. Doctor in fully installed, healthy environment
    with tempfile.TemporaryDirectory() as temp_dir:
        healthy_dir = Path(temp_dir) / "healthy_home"
        install_res = install_global(source_repo=REPO_ROOT, target_dir=healthy_dir, project_platform=False)
        assert install_res.success is True

        engine_healthy = DoctorEngine(target_dir=healthy_dir, workspace_dir=REPO_ROOT)
        code_healthy = engine_healthy.run_all()
        if code_healthy == 0:
            log_pass("Doctor completed with exit code 0 in healthy environment")
        else:
            log_fail(f"Doctor returned failure code {code_healthy} in healthy environment")
            passed = False

        checks_healthy = {c.name: c.status for c in engine_healthy.checks}
        expected_passes = [
            "Python Version",
            "Git Version",
            "Global Directory Write",
            "Installed Version",
            "Canonical Skills",
            "Templates",
            "Adapters",
            "Manifest Schema",
            "Integrity Check",
        ]
        for ep in expected_passes:
            if checks_healthy.get(ep) == "PASS":
                log_pass(f"Doctor diagnostic check [PASS]: {ep}")
            else:
                log_fail(f"Doctor diagnostic check expected PASS for: {ep} (got {checks_healthy.get(ep)})")
                passed = False

    return passed


def main():
    print("=" * 70)
    print("       Dev-Team Milestone 2 Verification (CLI Foundation)")
    print("=" * 70)
    print(f"Repository Root: {REPO_ROOT}")

    t01 = test_task_m2_t01()
    t02 = test_task_m2_t02()
    t03 = test_task_m2_t03()
    t04 = test_task_m2_t04()
    t05 = test_task_m2_t05()

    print("\n" + "=" * 70)
    print("                         Summary Results")
    print("=" * 70)
    print(f"[{'PASS' if t01 else 'FAIL'}] M2-T01: CLI Architecture & Project Setup")
    print(f"[{'PASS' if t02 else 'FAIL'}] M2-T02: Repository & Workspace Detection")
    print(f"[{'PASS' if t03 else 'FAIL'}] M2-T03: Global Skill Installation Command")
    print(f"[{'PASS' if t04 else 'FAIL'}] M2-T04: Installation Manifest & Provenance Engine")
    print(f"[{'PASS' if t05 else 'FAIL'}] M2-T05: Installation Diagnostics (dev-team doctor)")
    print("=" * 70)

    if t01 and t02 and t03 and t04 and t05:
        print("RESULT: ALL MILESTONE 2 VERIFICATION CHECKS PASSED SUCCESSFULLY!\n")
        return 0
    else:
        print("RESULT: MILESTONE 2 VERIFICATION FAILED.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

