#!/usr/bin/env python3
"""Main entry point and command-line router for the dev-team CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure CLI source directory and dev_team namespace are available
cli_src = Path(__file__).resolve().parent
if str(cli_src) not in sys.path:
    sys.path.insert(0, str(cli_src))

if "dev_team" not in sys.modules:
    import types
    dev_team_pkg = types.ModuleType("dev_team")
    dev_team_pkg.__path__ = [str(cli_src)]
    dev_team_pkg.__file__ = str(cli_src / "__init__.py")
    sys.modules["dev_team"] = dev_team_pkg

from dev_team.core.constants import DEFAULT_VERSION
from dev_team.commands import (
    doctor,
    init,
    install,
    list as list_cmd,
    status,
    uninstall,
    update,
)


def create_parser() -> argparse.ArgumentParser:
    """Builds and returns the primary argument parser for dev-team."""
    parser = argparse.ArgumentParser(
        prog="dev-team",
        description="Dev-Team: Specification-Driven AI Software Development Toolkit CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dev-team install --global --platform codex
  dev-team doctor --verbose
  dev-team init --mode hybrid --platform codex
  dev-team list --skills
  dev-team status
""",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"dev-team {DEFAULT_VERSION}",
        help="Show Dev-Team CLI version and exit.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available Dev-Team engineering commands",
        metavar="<command>",
    )

    # Register modular command handlers
    doctor.register_subcommand(subparsers)
    install.register_subcommand(subparsers)
    init.register_subcommand(subparsers)
    list_cmd.register_subcommand(subparsers)
    status.register_subcommand(subparsers)
    update.register_subcommand(subparsers)
    uninstall.register_subcommand(subparsers)

    return parser


def main(args: list[str] | None = None) -> int:
    """Primary execution entry point for console script."""
    parser = create_parser()

    if args is None:
        args = sys.argv[1:]

    # If no arguments provided, show help
    if not args:
        parser.print_help()
        return 0

    parsed = parser.parse_args(args)

    if hasattr(parsed, "func"):
        try:
            return parsed.func(parsed)
        except Exception as e:
            print(f"[FATAL ERROR] {e}", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
