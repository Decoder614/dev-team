"""Installation command handler: dev-team install."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from dev_team.core.constants import DEFAULT_PLATFORM, SUPPORTED_PLATFORMS
from dev_team.installation.global_installer import install_global
from dev_team.reporting.tables import render_table


def install_command(
    is_global: bool = False,
    platform: str = DEFAULT_PLATFORM,
    skill: Optional[str] = None,
    source: Optional[str] = None,
    target: Optional[str] = None,
    dry_run: bool = False,
    verbose: bool = False,
) -> int:
    """Handles dev-team install invocation."""
    if not is_global and not target:
        print("[ERROR] Please specify '--global' to install Dev-Team assets globally (~/.dev-team/) or supply '--target <path>'.")
        print("Usage example: dev-team install --global --platform codex")
        return 1

    if platform not in SUPPORTED_PLATFORMS:
        print(f"[ERROR] Unsupported platform '{platform}'. Supported platforms: {SUPPORTED_PLATFORMS}")
        return 1

    print(f"Installing Dev-Team assets (global mode: {is_global}, platform: {platform})...")

    result = install_global(
        source_repo=source,
        target_dir=target,
        platform=platform,
        specific_skill=skill,
        dry_run=dry_run,
        verbose=verbose,
    )

    if not result.success:
        print("\n[INSTALL FAILED]")
        for err in result.errors:
            print(f"  - {err}")
        return 1

    # Render installation report
    print("\n" + "=" * 60)
    print("Dev-Team Installation Completed Successfully")
    print("=" * 60)
    print(f"Destination:     {result.target_directory}")
    print(f"Version:         {result.version}")
    print(f"Platform:        {result.platform}")
    print(f"Skills:          {len(result.installed_skills)} ({', '.join(result.installed_skills[:4])}...)")
    print(f"Total Artifacts: {result.total_files_installed}")
    if result.manifest_path:
        print(f"Manifest:        {result.manifest_path}")
    if result.platform_projection_dir:
        print(f"Platform Dir:    {result.platform_projection_dir}")

    for msg in result.messages:
        print(f"  {msg}")

    print("\nNext steps:")
    print("  1. Run 'dev-team doctor' to verify system readiness.")
    print("  2. In your target repository, run 'dev-team init --mode hybrid' to onboard.")
    return 0


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'install' subcommand with argparse."""
    parser = subparsers.add_parser(
        "install",
        help="Install Dev-Team canonical skills, templates, and adapters globally or locally.",
    )
    parser.add_argument(
        "--global", "-g",
        dest="is_global",
        action="store_true",
        help="Install canonical assets into the global user directory (~/.dev-team/).",
    )
    parser.add_argument(
        "--platform", "-p",
        type=str,
        default=DEFAULT_PLATFORM,
        choices=SUPPORTED_PLATFORMS,
        help=f"Target AI coding platform (default: {DEFAULT_PLATFORM}).",
    )
    parser.add_argument(
        "--skill", "-s",
        type=str,
        default=None,
        help="Install a single specific skill instead of all canonical skills.",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Path to canonical Dev-Team repository (defaults to auto-detection).",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Custom destination directory override (defaults to ~/.dev-team/ in global mode).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files to disk.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Display verbose installation log.",
    )
    parser.set_defaults(func=lambda args: install_command(
        is_global=args.is_global,
        platform=args.platform,
        skill=args.skill,
        source=args.source,
        target=args.target,
        dry_run=args.dry_run,
        verbose=args.verbose,
    ))

