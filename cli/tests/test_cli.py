"""Unit tests for Dev-Team CLI entry point, argument parsing, and command routing."""

import pytest
from dev_team.core.constants import DEFAULT_VERSION
from dev_team.main import create_parser, main


def test_cli_parser_creation():
    """Verify primary parser defines all required commands."""
    parser = create_parser()
    assert parser.prog == "dev-team"

    # Inspect subparsers
    subparser_actions = [
        action for action in parser._actions
        if action.__class__.__name__ == "_SubParsersAction"
    ]
    assert len(subparser_actions) == 1
    choices = subparser_actions[0].choices
    for cmd in ["install", "doctor", "init", "list", "status", "update", "uninstall"]:
        assert cmd in choices, f"Expected subcommand '{cmd}' missing from parser"


def test_cli_version_flag(capsys):
    """Verify --version prints the expected version string."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert f"dev-team {DEFAULT_VERSION}" in captured.out


def test_cli_no_args_displays_help(capsys):
    """Verify running dev-team with no arguments displays help and exits 0."""
    code = main([])
    assert code == 0
    captured = capsys.readouterr()
    assert "Available Dev-Team engineering commands" in captured.out

