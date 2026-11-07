"""Status reporting command handler: dev-team status."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from dev_team.core.constants import GLOBAL_HOME_DIR, GLOBAL_VERSION_FILE
from dev_team.detection.workspace import detect_workspace
from dev_team.reporting.tables import render_table


def status_command(workspace: Optional[str] = None) -> int:
    """Displays installation and workspace onboarding status."""
    ws_path = Path(workspace).resolve() if workspace else Path.cwd().resolve()
    ws = detect_workspace(ws_path)

    global_dir = Path.home() / GLOBAL_HOME_DIR
    global_installed = global_dir.exists()
    global_version = "None"
    if (global_dir / GLOBAL_VERSION_FILE).is_file():
        global_version = (global_dir / GLOBAL_VERSION_FILE).read_text(encoding="utf-8").strip()

    headers = ["Aspect", "State / Value"]
    rows = [
        ["Active Directory", str(ws.path)],
        ["Workspace Type", ws.workspace_type],
        ["Git Repository", "Yes" if ws.is_git_repo else "No"],
        ["Dev-Team Global Install", f"{global_dir} (v{global_version})" if global_installed else "Not Installed"],
        ["Target Onboarded", "Yes" if ws.is_target_project else "No"],
    ]

    print("\n" + render_table(headers, rows, title="Dev-Team Status"))
    return 0


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'status' subcommand with argparse."""
    parser = subparsers.add_parser(
        "status",
        help="Display current repository configuration and initialization status.",
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        default=None,
        help="Workspace to inspect (defaults to current directory).",
    )
    parser.set_defaults(func=lambda args: status_command(workspace=args.workspace))

