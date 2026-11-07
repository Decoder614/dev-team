"""Unit tests for Dev-Team doctor diagnostic checks."""

from pathlib import Path
import pytest

from dev_team.commands.doctor import DoctorEngine, doctor_command
from dev_team.installation.global_installer import install_global


def test_doctor_in_empty_environment(tmp_path):
    """Verify doctor returns 0 with warnings when global directory is uninitialized."""
    empty_global = tmp_path / "empty_global"
    engine = DoctorEngine(target_dir=empty_global, workspace_dir=tmp_path)
    exit_code = engine.run_all()
    # No fatal failures, but warnings about missing installation
    assert exit_code == 0
    checks = {c.name: c.status for c in engine.checks}
    assert checks["Python Version"] == "PASS"
    assert checks["Git Version"] == "PASS"


def test_doctor_in_healthy_installed_environment(tmp_path):
    """Verify doctor reports PASS across all installation categories after install."""
    installed_global = tmp_path / "healthy_global"

    # Run installation
    result = install_global(target_dir=installed_global, project_platform=False)
    assert result.success is True

    # Run doctor against installed directory
    engine = DoctorEngine(target_dir=installed_global, workspace_dir=tmp_path)
    exit_code = engine.run_all()
    assert exit_code == 0

    checks = {c.name: c.status for c in engine.checks}
    assert checks["Installed Version"] == "PASS"
    assert checks["Canonical Skills"] == "PASS"
    assert checks["Templates"] == "PASS"
    assert checks["Adapters"] == "PASS"
    assert checks["Manifest Schema"] == "PASS"
    assert checks["Integrity Check"] == "PASS"

