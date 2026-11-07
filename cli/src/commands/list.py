"""Catalog inspection command handler: dev-team list."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from dev_team.core.constants import GLOBAL_HOME_DIR, SUPPORTED_PLATFORMS
from dev_team.detection.platform import detect_all_platforms
from dev_team.detection.workspace import find_canonical_source_repo
from dev_team.reporting.tables import render_table


def list_command(
    show_skills: bool = True,
    show_platforms: bool = False,
    show_local: bool = False,
    global_dir: Optional[str] = None,
) -> int:
    """Lists available canonical skills, installed skills, or supported platforms."""
    gdir = Path(global_dir).resolve() if global_dir else Path.home() / GLOBAL_HOME_DIR

    if show_platforms:
        print("\nSupported AI Coding Platforms:")
        plat_info = detect_all_platforms()
        headers = ["Platform ID", "Platform Name", "CLI in PATH", "Readiness"]
        rows = [
            [
                p.id,
                p.name,
                "[PASS]" if p.cli_available else "[INFO] Missing",
                "[PASS] Ready" if p.is_ready else "[INFO] Available",
            ]
            for p in plat_info.values()
        ]
        print(render_table(headers, rows))
        return 0

    # Skills catalog
    print(f"\nDev-Team Skills Catalog (Global: {gdir}):")
    headers = ["Skill Name", "Source", "Status"]
    rows = []

    # Check global directory
    global_skills_dir = gdir / "skills"
    if global_skills_dir.is_dir():
        for d in sorted(global_skills_dir.iterdir()):
            if d.is_dir() and (d / "SKILL.md").is_file():
                rows.append([d.name, "Global (~/.dev-team/skills/)", "[PASS] Installed"])

    # Check canonical repo if global was empty
    if not rows:
        src = find_canonical_source_repo()
        if src and (src / "skills").is_dir():
            for d in sorted((src / "skills").iterdir()):
                if d.is_dir() and (d / "SKILL.md").is_file():
                    rows.append([d.name, "Canonical Repository", "[INFO] Available to install"])

    if rows:
        print(render_table(headers, rows))
    else:
        print("No skills currently detected. Run: dev-team install --global")

    return 0


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'list' subcommand with argparse."""
    parser = subparsers.add_parser(
        "list",
        help="List available skills, installed packages, or supported platforms.",
    )
    parser.add_argument(
        "--skills", "-s",
        action="store_true",
        default=True,
        help="List canonical and installed skills.",
    )
    parser.add_argument(
        "--platforms", "-p",
        action="store_true",
        help="List supported AI coding platforms and readiness.",
    )
    parser.add_argument(
        "--local", "-l",
        action="store_true",
        help="List project-local skills in current repository.",
    )
    parser.set_defaults(func=lambda args: list_command(
        show_skills=args.skills,
        show_platforms=args.platforms,
        show_local=args.local,
    ))

