"""Diagnostics and health-check command handler: dev-team doctor."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from dev_team.core.constants import (
    GLOBAL_CONFIG_FILE,
    GLOBAL_HOME_DIR,
    GLOBAL_MANIFEST_FILE,
    GLOBAL_VERSION_FILE,
    SUPPORTED_PLATFORMS,
)
from dev_team.core.manifest import Manifest
from dev_team.detection.platform import detect_all_platforms, detect_system_tools
from dev_team.detection.workspace import detect_workspace
from dev_team.reporting.tables import format_status_badge, render_table


@dataclass
class DiagnosticCheck:
    """Represents a single diagnostic evaluation."""

    category: str
    name: str
    status: str  # PASS, WARN, FAIL, INFO
    details: str


class DoctorEngine:
    """Engine executing environment, installation, and workspace diagnostic checks."""

    def __init__(
        self,
        target_dir: Optional[Path | str] = None,
        workspace_dir: Optional[Path | str] = None,
        verbose: bool = False,
    ):
        self.global_dir = Path(target_dir).resolve() if target_dir else Path.home() / GLOBAL_HOME_DIR
        self.workspace_dir = Path(workspace_dir).resolve() if workspace_dir else Path.cwd().resolve()
        self.verbose = verbose
        self.checks: List[DiagnosticCheck] = []

    def log(self, category: str, name: str, status: str, details: str) -> None:
        self.checks.append(DiagnosticCheck(category, name, status, details))

    def run_all(self) -> int:
        """Executes all diagnostics and returns exit code (0 = success, 1 = failure)."""
        self._check_prerequisites()
        self._check_filesystem_permissions()
        self._check_global_installation()
        self._check_platforms()
        self._check_workspace()

        # Render report
        headers = ["Category", "Check / Component", "Status", "Details"]
        rows = [
            [c.category, c.name, format_status_badge(c.status), c.details]
            for c in self.checks
        ]

        title = "Dev-Team System & Installation Diagnostics"
        print("\n" + render_table(headers, rows, title=title))

        passes = sum(1 for c in self.checks if c.status.upper() in ("PASS", "OK"))
        fails = sum(1 for c in self.checks if c.status.upper() in ("FAIL", "ERROR"))
        warns = sum(1 for c in self.checks if c.status.upper() in ("WARN", "WARNING"))

        print("\n" + "=" * 60)
        print(f"Summary: {passes} Passed, {warns} Warnings, {fails} Failed")
        print("=" * 60)

        if fails > 0:
            print("[DOCTOR RESULT] Failures detected. Review output above.")
            return 1
        elif warns > 0:
            print("[DOCTOR RESULT] System is operational with warnings.")
            return 0
        else:
            print("[DOCTOR RESULT] All diagnostics passed successfully! System healthy.")
            return 0

    def _check_prerequisites(self) -> None:
        """Inspects Python and Git prerequisites."""
        tools = detect_system_tools()

        # Python
        py = tools["python"]
        if py.meets_prerequisite:
            self.log("Prerequisites", "Python Version", "PASS", f"{py.version} ({py.path})")
        else:
            self.log("Prerequisites", "Python Version", "FAIL", f"{py.version} — Required: {py.required_version}")

        # Git
        git = tools["git"]
        if git.meets_prerequisite:
            self.log("Prerequisites", "Git Version", "PASS", f"{git.version} ({git.path})")
        elif git.available:
            self.log("Prerequisites", "Git Version", "WARN", f"{git.version} — Recommended: {git.required_version}")
        else:
            self.log("Prerequisites", "Git Installed", "FAIL", "Git was not found in PATH")

        # Dev-Team CLI in PATH
        dev_team_bin = shutil.which("dev-team")
        if dev_team_bin:
            self.log("Prerequisites", "CLI in PATH", "PASS", f"Executable found: {dev_team_bin}")
        else:
            user_scripts = self._find_user_scripts_dir()
            if user_scripts and (user_scripts / "dev-team.exe").is_file():
                self.log(
                    "Prerequisites",
                    "CLI in PATH",
                    "WARN",
                    f"Installed at {user_scripts} but missing from PATH. Run: dev-team doctor --fix-path",
                )
            else:
                self.log(
                    "Prerequisites",
                    "CLI in PATH",
                    "INFO",
                    "Command not found in PATH (running via python -m dev_team.main)",
                )

    def _find_user_scripts_dir(self) -> Optional[Path]:
        """Locates Python user Scripts directory where pip installs console_scripts."""
        try:
            import site
            if sys.platform.startswith("win"):
                p = Path(site.USER_BASE) / f"Python{sys.version_info.major}{sys.version_info.minor}" / "Scripts"
                if p.is_dir():
                    return p
            else:
                p = Path(site.USER_BASE) / "bin"
                if p.is_dir():
                    return p
        except Exception:
            pass
        return None

    def fix_path(self) -> bool:
        """Automatically adds Python Scripts directory to Windows User PATH environment variable."""
        if not sys.platform.startswith("win"):
            print("[INFO] Automatic PATH fix is only supported on Windows. On Unix, add ~/.local/bin to your shell rc file.")
            return False

        scripts_dir = self._find_user_scripts_dir()
        if not scripts_dir:
            print("[FAIL] Could not determine Python user Scripts directory.")
            return False

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                try:
                    val, typ = winreg.QueryValueEx(key, "Path")
                except FileNotFoundError:
                    val, typ = "", winreg.REG_EXPAND_SZ

                paths = [p.strip() for p in val.split(";") if p.strip()]
                target_str = str(scripts_dir)

                if target_str not in paths:
                    paths.append(target_str)
                    new_val = ";".join(paths)
                    winreg.SetValueEx(key, "Path", 0, typ, new_val)
                    os.environ["PATH"] = os.environ.get("PATH", "") + ";" + target_str
                    print(f"[SUCCESS] Added to Windows User PATH: {target_str}")
                    print("Note: New terminal windows will automatically recognize 'dev-team'.")
                    return True
                else:
                    print(f"[INFO] Already in User PATH: {target_str}")
                    return True
        except Exception as e:
            print(f"[FAIL] Could not update User PATH in Windows registry: {e}")
            return False

    def _check_filesystem_permissions(self) -> None:
        """Checks read/write permissions in global directory and workspace."""
        # Global parent directory write test
        try:
            existed = self.global_dir.exists()
            target_to_test = self.global_dir if existed else self.global_dir.parent
            target_to_test.mkdir(parents=True, exist_ok=True)
            test_file = target_to_test / ".perm_check.tmp"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            self.log("Permissions", "Global Directory Write", "PASS", f"Writable: {target_to_test}")
        except Exception as e:
            self.log("Permissions", "Global Directory Write", "FAIL", f"Cannot write to {self.global_dir}: {e}")

        # Workspace directory write test
        try:
            test_file = self.workspace_dir / ".perm_check.tmp"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            self.log("Permissions", "Workspace Write", "PASS", f"Writable: {self.workspace_dir}")
        except Exception as e:
            self.log("Permissions", "Workspace Write", "WARN", f"Cannot write to workspace {self.workspace_dir}: {e}")

    def _check_global_installation(self) -> None:
        """Inspects global ~/.dev-team/ installation, version, skills, and manifest."""
        version_file = self.global_dir / GLOBAL_VERSION_FILE
        manifest_file = self.global_dir / GLOBAL_MANIFEST_FILE

        if not self.global_dir.exists():
            self.log("Global Install", "Installation Root", "WARN", f"Not installed at {self.global_dir}. Run: dev-team install --global")
            return
        elif not version_file.exists() and not manifest_file.exists():
            self.log("Global Install", "Installation Root", "WARN", f"Directory exists at {self.global_dir} but is uninitialized. Run: dev-team install --global")
            return

        self.log("Global Install", "Installation Root", "PASS", f"Found: {self.global_dir}")

        # Version file
        version_file = self.global_dir / GLOBAL_VERSION_FILE
        if version_file.is_file():
            ver = version_file.read_text(encoding="utf-8").strip()
            self.log("Global Install", "Installed Version", "PASS", f"Version {ver}")
        else:
            self.log("Global Install", "Installed Version", "WARN", "Missing 'version' file in global directory")

        # Skills directory
        skills_dir = self.global_dir / "skills"
        if skills_dir.is_dir():
            skills = [
                d.name for d in skills_dir.iterdir()
                if d.is_dir() and (d / "SKILL.md").is_file()
            ]
            if skills:
                self.log("Global Install", "Canonical Skills", "PASS", f"{len(skills)} skills installed ({', '.join(skills[:3])}...)")
            else:
                self.log("Global Install", "Canonical Skills", "WARN", "skills/ directory is empty")
        else:
            self.log("Global Install", "Canonical Skills", "WARN", "skills/ directory missing")

        # Templates directory
        templates_dir = self.global_dir / "templates"
        if templates_dir.is_dir():
            templates = list(templates_dir.glob("*.md"))
            self.log("Global Install", "Templates", "PASS", f"templates/ directory found ({len(templates)} templates)")
        else:
            self.log("Global Install", "Templates", "WARN", "templates/ directory missing")

        # Adapters directory
        adapters_dir = self.global_dir / "adapters"
        if adapters_dir.is_dir():
            self.log("Global Install", "Adapters", "PASS", f"adapters/ directory found")
        else:
            self.log("Global Install", "Adapters", "WARN", "adapters/ directory missing")

        # Manifest verification
        manifest_file = self.global_dir / GLOBAL_MANIFEST_FILE
        if manifest_file.is_file():
            try:
                manifest = Manifest.load(manifest_file)
                self.log("Global Install", "Manifest Schema", "PASS", f"manifest.json valid (mode: {manifest.installation_mode})")

                # Verify files on disk against hashes
                verification = manifest.verify(self.global_dir)
                if verification.all_valid:
                    self.log("Global Install", "Integrity Check", "PASS", f"All {verification.total_artifacts} tracked artifacts intact (0 modified, 0 missing)")
                else:
                    details = []
                    if verification.missing_artifacts:
                        details.append(f"{len(verification.missing_artifacts)} missing")
                    if verification.modified_artifacts:
                        details.append(f"{len(verification.modified_artifacts)} modified")
                    self.log("Global Install", "Integrity Check", "WARN", f"Provenance mismatch: {', '.join(details)}")
            except Exception as e:
                self.log("Global Install", "Manifest Validation", "FAIL", f"Manifest error: {e}")
        else:
            self.log("Global Install", "Manifest File", "WARN", "manifest.json missing in global directory")

    def _check_platforms(self) -> None:
        """Inspects status and discovery paths for AI coding platforms."""
        platforms = detect_all_platforms(self.global_dir.parent if self.global_dir else None)

        for pid, pinfo in platforms.items():
            if pinfo.is_ready:
                status = "PASS" if pinfo.cli_available else "INFO"
                self.log("Platform", pinfo.name, status, pinfo.details)
            else:
                self.log("Platform", pinfo.name, "INFO", pinfo.details)

    def _check_workspace(self) -> None:
        """Inspects current active workspace directory."""
        ws = detect_workspace(self.workspace_dir)
        self.log("Workspace", "Workspace Type", "INFO", f"Type: {ws.workspace_type} ({self.workspace_dir})")

        if ws.is_git_repo:
            self.log("Workspace", "Git Repository", "PASS", f"Root: {ws.git_root}")
        else:
            self.log("Workspace", "Git Repository", "INFO", "Not a git repository")

        if ws.is_canonical_dev_team:
            self.log("Workspace", "Dev-Team Repository", "PASS", "Operating inside Dev-Team source framework")
        elif ws.is_target_project:
            cfg = ws.configuration
            self.log("Workspace", "Target Project", "PASS", f"Configured target project (config: {cfg['has_config']})")


def doctor_command(
    verbose: bool = False,
    target: Optional[str] = None,
    workspace: Optional[str] = None,
    fix_path: bool = False,
) -> int:
    """Entry point for dev-team doctor command."""
    engine = DoctorEngine(target_dir=target, workspace_dir=workspace, verbose=verbose)
    if fix_path:
        engine.fix_path()
        return 0
    return engine.run_all()


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'doctor' subcommand with argparse."""
    parser = subparsers.add_parser(
        "doctor",
        help="Diagnose Dev-Team installation health, dependencies, and platform readiness.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Display detailed diagnostic and artifact information.",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Custom global installation path to inspect (defaults to ~/.dev-team).",
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="Workspace directory to inspect (defaults to current directory).",
    )
    parser.add_argument(
        "--fix-path",
        action="store_true",
        help="Automatically add Python user Scripts directory to Windows User PATH.",
    )
    parser.set_defaults(func=lambda args: doctor_command(
        verbose=args.verbose,
        target=args.target,
        workspace=args.workspace,
        fix_path=getattr(args, "fix_path", False),
    ))
