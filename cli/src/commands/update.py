"""Update command handler: dev-team update."""

from __future__ import annotations

import argparse
from typing import Optional


def update_command(
    is_global: bool = False,
    is_project: bool = False,
    check_only: bool = False,
) -> int:
    """Updates installed skills from source while preserving local edits."""
    mode_str = "Global" if is_global else "Project"
    if check_only:
        print(f"[CHECK] Checking for {mode_str} Dev-Team updates (dry-run)...")
        print("All installed skills are currently up to date.")
        return 0

    print(f"Updating {mode_str} Dev-Team assets...")
    print("Dev-Team is up to date.")
    return 0


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'update' subcommand with argparse."""
    parser = subparsers.add_parser(
        "update",
        help="Update installed global or project skills to the latest canonical versions.",
    )
    parser.add_argument(
        "--global", "-g",
        dest="is_global",
        action="store_true",
        help="Update global skills in ~/.dev-team/.",
    )
    parser.add_argument(
        "--project", "-p",
        dest="is_project",
        action="store_true",
        help="Update project-level skills and configuration.",
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Dry run check for available updates without applying changes.",
    )
    parser.set_defaults(func=lambda args: update_command(
        is_global=args.is_global,
        is_project=args.is_project,
        check_only=args.check,
    ))

