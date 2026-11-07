"""Clean removal command handler: dev-team uninstall."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from dev_team.core.constants import GLOBAL_HOME_DIR, GLOBAL_MANIFEST_FILE
from dev_team.core.manifest import Manifest


def uninstall_command(
    is_global: bool = False,
    is_project: bool = False,
    purge: bool = False,
    target: str = None,
) -> int:
    """Safely removes Dev-Team artifacts while strictly preserving unrelated user files."""
    dest = Path(target).resolve() if target else Path.home() / GLOBAL_HOME_DIR

    if not is_global and not is_project and not target:
        print("[ERROR] Please specify '--global' or '--project'.")
        return 1

    if is_global or target:
        if not dest.exists():
            print(f"[INFO] Global installation does not exist at {dest}.")
            return 0

        manifest_file = dest / GLOBAL_MANIFEST_FILE
        if manifest_file.is_file() and not purge:
            try:
                manifest = Manifest.load(manifest_file)
                print(f"Removing {len(manifest.artifacts)} managed artifacts from {dest}...")
                for art in manifest.artifacts:
                    art_file = dest / art.path
                    if art_file.is_file():
                        art_file.unlink()
                print("[PASS] Removed managed artifacts cleanly.")
                # If directory is now empty or only manifest remains
                manifest_file.unlink(missing_ok=True)
            except Exception as e:
                print(f"[WARN] Error reading manifest: {e}. Purging safe directory.")
                shutil.rmtree(dest, ignore_errors=True)
        else:
            print(f"Purging Dev-Team directory at {dest}...")
            shutil.rmtree(dest, ignore_errors=True)

        print("[SUCCESS] Uninstallation completed.")

    return 0


def register_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Registers the 'uninstall' subcommand with argparse."""
    parser = subparsers.add_parser(
        "uninstall",
        help="Safely remove Dev-Team managed artifacts.",
    )
    parser.add_argument(
        "--global", "-g",
        dest="is_global",
        action="store_true",
        help="Remove global installation in ~/.dev-team/.",
    )
    parser.add_argument(
        "--project", "-p",
        dest="is_project",
        action="store_true",
        help="Remove project-level .dev-team configuration and projections.",
    )
    parser.add_argument(
        "--purge",
        action="store_true",
        help="Force delete the managed directory completely.",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Custom destination directory override.",
    )
    parser.set_defaults(func=lambda args: uninstall_command(
        is_global=args.is_global,
        is_project=args.is_project,
        purge=args.purge,
        target=args.target,
    ))

