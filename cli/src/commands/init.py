"""Project initialization command handler: dev-team init."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from dev_team.core.constants import (
    ALLOWED_INSTALLATION_MODES,
    DEFAULT_INSTALLATION_MODE,
    DEFAULT_PLATFORM,
    PROJECT_DEV_TEAM_DIR,
    SUPPORTED_PLATFORMS,
)
from dev_team.detection.workspace import detect_workspace


def init_command(
    platform: str = DEFAULT_PLATFORM,
    mode: str = DEFAULT_INSTALLATION_MODE,
    target: Optional[str] = None,
    force: bool = False,
) -> int:
    """Bootstrap a target repository with Dev-Team configuration."""
    target_path = Path(target).resolve() if target else Path.cwd().resolve()
    ws = detect_workspace(target_path)

    print(f"Initializing Dev-Team in workspace: {target_path}")
    print(f"Platform: {platform} | Mode: {mode}")

    dev_team_dir = target_path / PROJECT_DEV_TEAM_DIR
    if dev_team_dir.exists() and not force:
        print(f"[NOTE] .dev-team/ already exists in {target_path}.")
    else:
        dev_team_dir.mkdir(parents=True, exist_ok=True)
        print(f"[PASS] Created {dev_team_dir}")

    print("\nInitialization foundation prepared.")
    print("Next step: Run the project-initializer AI skill to establish project context:")
    print("  > /project-initializer")
    return 0


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'init' subcommand with argparse."""
    parser = subparsers.add_parser(
        "init",
        help="Initialize Dev-Team configuration and scaffolding in the current repository.",
    )
    parser.add_argument(
        "--platform", "-p",
        type=str,
        default=DEFAULT_PLATFORM,
        choices=SUPPORTED_PLATFORMS,
        help=f"Target platform (default: {DEFAULT_PLATFORM}).",
    )
    parser.add_argument(
        "--mode", "-m",
        type=str,
        default=DEFAULT_INSTALLATION_MODE,
        choices=ALLOWED_INSTALLATION_MODES,
        help=f"Distribution mode (default: {DEFAULT_INSTALLATION_MODE}).",
    )
    parser.add_argument(
        "--target", "-t",
        type=str,
        default=None,
        help="Target repository directory (defaults to current directory).",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing configuration if present.",
    )
    parser.set_defaults(func=lambda args: init_command(
        platform=args.platform,
        mode=args.mode,
        target=args.target,
        force=args.force,
    ))

