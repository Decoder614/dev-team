"""Constants and default configuration parameters for Dev-Team."""

from pathlib import Path

DEFAULT_VERSION = "1.1.0"
GLOBAL_HOME_DIR = ".dev-team"
GLOBAL_MANIFEST_FILE = "manifest.json"
GLOBAL_VERSION_FILE = "version"
GLOBAL_CONFIG_FILE = "config.yaml"

PROJECT_DEV_TEAM_DIR = ".dev-team"
PROJECT_MANIFEST_FILE = "installation-manifest.json"
PROJECT_CONFIG_FILE = "config.yaml"
PROJECT_CONTEXT_FILE = "project-context.md"

INSTRUCTIONS_FILE = "AGENTS.md"
RULES_FILE = "rules.md"

SUPPORTED_PLATFORMS = [
    "codex",
    "claude-code",
    "cursor",
    "copilot",
    "gemini",
]

DEFAULT_PLATFORM = "codex"

ALLOWED_INSTALLATION_MODES = [
    "hybrid",
    "copy",
    "symlink",
]

DEFAULT_INSTALLATION_MODE = "hybrid"

ARTIFACT_TYPES = [
    "skill_projection",
    "skill",
    "template",
    "adapter",
    "configuration",
    "documentation",
    "script",
    "other",
]

STRATEGIES = [
    "symlink",
    "junction",
    "copy",
    "managed_file",
]

