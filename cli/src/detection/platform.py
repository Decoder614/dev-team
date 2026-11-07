"""Platform and environment readiness detection for Dev-Team."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from dev_team.core.constants import SUPPORTED_PLATFORMS


@dataclass
class ToolInfo:
    """Status and version information for a host system tool."""

    name: str
    available: bool
    version: Optional[str]
    meets_prerequisite: bool
    required_version: str
    path: Optional[str]
    message: str


@dataclass
class PlatformInfo:
    """Status and discovery configuration for an AI coding platform."""

    id: str
    name: str
    cli_available: bool
    cli_path: Optional[str]
    discovery_dir: Path
    discovery_dir_exists: bool
    is_ready: bool
    details: str


def check_command_version(
    cmd: str, version_arg: str = "--version"
) -> tuple[bool, Optional[str], Optional[str]]:
    """Runs a command with version argument and returns (available, version_string, binary_path)."""
    binary = shutil.which(cmd)
    if not binary:
        return False, None, None

    try:
        proc = subprocess.run(
            [cmd, version_arg],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        output = proc.stdout.strip() or proc.stderr.strip()
        first_line = output.splitlines()[0] if output else ""
        return True, first_line, binary
    except Exception:
        return True, "Unknown version", binary


def detect_system_tools() -> Dict[str, ToolInfo]:
    """Detects mandatory host environment tools (Python and Git)."""
    tools: Dict[str, ToolInfo] = {}

    # 1. Python check
    py_ver = sys.version_info
    py_ver_str = f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"
    py_meets = (py_ver.major == 3 and py_ver.minor >= 10) or (py_ver.major > 3)
    tools["python"] = ToolInfo(
        name="Python",
        available=True,
        version=py_ver_str,
        meets_prerequisite=py_meets,
        required_version=">= 3.10",
        path=sys.executable,
        message=f"Python {py_ver_str} meets requirement (>= 3.10)"
        if py_meets
        else f"Python {py_ver_str} is below requirement (>= 3.10)",
    )

    # 2. Git check
    git_avail, git_out, git_path = check_command_version("git", "--version")
    git_meets = False
    git_ver = None
    git_msg = "Git is not installed or not in PATH"

    if git_avail and git_out:
        match = re.search(r"(\d+\.\d+(?:\.\d+)?)", git_out)
        if match:
            git_ver = match.group(1)
            parts = [int(p) for p in git_ver.split(".")[:2]]
            if len(parts) == 1:
                parts.append(0)
            git_meets = (parts[0] > 2) or (parts[0] == 2 and parts[1] >= 30)
            git_msg = (
                f"Git {git_ver} meets requirement (>= 2.30)"
                if git_meets
                else f"Git {git_ver} is below recommended (>= 2.30)"
            )
        else:
            git_ver = git_out
            git_meets = True
            git_msg = f"Git detected: {git_out}"

    tools["git"] = ToolInfo(
        name="Git",
        available=git_avail,
        version=git_ver,
        meets_prerequisite=git_meets,
        required_version=">= 2.30",
        path=git_path,
        message=git_msg,
    )

    return tools


def get_platform_discovery_dir(platform_id: str, home_dir: Optional[Path] = None) -> Path:
    """Resolves the user-level global skill discovery path for a platform."""
    home = home_dir or Path.home()
    is_win = sys.platform.startswith("win")

    if platform_id == "codex":
        # Windows: %USERPROFILE%\.codex\skills, Unix: ~/.codex/skills
        codex_home = os.environ.get("CODEX_HOME")
        if codex_home:
            return Path(codex_home) / "skills"
        return home / ".codex" / "skills"

    elif platform_id == "claude-code":
        if is_win:
            appdata = os.environ.get("APPDATA")
            if appdata:
                return Path(appdata) / "claude" / "skills"
        return home / ".claude" / "skills"

    elif platform_id == "cursor":
        return home / ".cursor" / "skills"

    elif platform_id == "copilot":
        return home / ".copilot" / "skills"

    elif platform_id == "gemini":
        return home / ".gemini" / "antigravity" / "skills"

    return home / f".{platform_id}" / "skills"


def detect_platform_readiness(
    platform_id: str, home_dir: Optional[Path] = None
) -> PlatformInfo:
    """Checks presence of CLI and discovery path for a specific platform."""
    platform_names = {
        "codex": "OpenAI Codex CLI",
        "claude-code": "Anthropic Claude Code",
        "cursor": "Cursor IDE",
        "copilot": "GitHub Copilot",
        "gemini": "Google Antigravity / Gemini",
    }
    cmd_names = {
        "codex": "codex",
        "claude-code": "claude",
        "cursor": "cursor",
        "copilot": "gh",
        "gemini": "agy",
    }

    pname = platform_names.get(platform_id, platform_id)
    cmd = cmd_names.get(platform_id, platform_id)
    avail, ver, path = check_command_version(cmd)

    discovery_dir = get_platform_discovery_dir(platform_id, home_dir)
    dir_exists = discovery_dir.exists()

    # Ready if either discovery directory exists or CLI is installed
    is_ready = dir_exists or avail

    details_parts = []
    if avail:
        details_parts.append(f"CLI: {path}")
    else:
        details_parts.append("CLI: Not in PATH")

    if dir_exists:
        details_parts.append(f"Discovery: {discovery_dir} (exists)")
    else:
        details_parts.append(f"Discovery: {discovery_dir} (will be created)")

    return PlatformInfo(
        id=platform_id,
        name=pname,
        cli_available=avail,
        cli_path=path,
        discovery_dir=discovery_dir,
        discovery_dir_exists=dir_exists,
        is_ready=is_ready,
        details=" | ".join(details_parts),
    )


def detect_all_platforms(home_dir: Optional[Path] = None) -> Dict[str, PlatformInfo]:
    """Detects environment readiness for all supported platforms."""
    return {
        pid: detect_platform_readiness(pid, home_dir)
        for pid in SUPPORTED_PLATFORMS
    }

