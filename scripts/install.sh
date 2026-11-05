#!/usr/bin/env bash
# ==============================================================================
# Dev-Team Installer for Unix-like Systems (Linux, macOS, WSL)
# Installs, links, or uninstalls Dev-Team skills for OpenAI Codex CLI.
# ==============================================================================

set -euo pipefail

MODE="copy"
CODEX_DIR=""
TARGET_REPO=""
UNINSTALL=false
FORCE=false
DRY_RUN=false

show_help() {
    cat <<EOF
Dev-Team Installer for Unix / macOS

Usage:
  ./scripts/install.sh [options]

Options:
  -m <copy|symlink>   Installation mode: 'copy' (default) or 'symlink'
  -d <dir>            Custom Codex skills directory (default: \$CODEX_HOME/skills or ~/.codex/skills)
  -t <repo>           Target application repository to install skills locally
  -u                  Uninstall Dev-Team skills (preserves unrelated user skills)
  -n                  Dry-run mode (simulate operations without modifying files)
  -f                  Force overwrite of existing targets
  -h                  Show this help message and exit

Examples:
  ./scripts/install.sh
  ./scripts/install.sh -m symlink
  ./scripts/install.sh -t /path/to/my-project
  ./scripts/install.sh -u
EOF
}

# Parse command line options
while getopts "m:d:t:unfh" opt; do
    case "$opt" in
        m)
            MODE="$(echo "$OPTARG" | tr '[:upper:]' '[:lower:]')"
            if [ "$MODE" != "copy" ] && [ "$MODE" != "symlink" ]; then
                echo "[ERROR] Invalid mode '$OPTARG'. Must be 'copy' or 'symlink'." >&2
                exit 1
            fi
            ;;
        d)
            CODEX_DIR="$OPTARG"
            ;;
        t)
            TARGET_REPO="$OPTARG"
            ;;
        u)
            UNINSTALL=true
            ;;
        n)
            DRY_RUN=true
            ;;
        f)
            FORCE=true
            ;;
        h)
            show_help
            exit 0
            ;;
        \?)
            echo "[ERROR] Invalid option -$OPTARG. Use -h for help." >&2
            exit 1
            ;;
    esac
done

echo "============================================================"
echo "             Dev-Team Installer for Unix / macOS            "
echo "============================================================"

# 1. Resolve Dev-Team root and skills directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEV_TEAM_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_SKILLS_DIR="$DEV_TEAM_ROOT/skills"

if [ ! -d "$SOURCE_SKILLS_DIR" ]; then
    echo "[FAIL] Source skills directory not found at: $SOURCE_SKILLS_DIR" >&2
    exit 1
fi

# Discover valid skills (directories containing SKILL.md)
SKILLS=()
for skill_path in "$SOURCE_SKILLS_DIR"/*; do
    if [ -d "$skill_path" ] && [ -f "$skill_path/SKILL.md" ]; then
        SKILLS+=("$(basename "$skill_path")")
    fi
done

if [ ${#SKILLS[@]} -eq 0 ]; then
    echo "[FAIL] No valid skills found in $SOURCE_SKILLS_DIR" >&2
    exit 1
fi

echo "Dev-Team Root : $DEV_TEAM_ROOT"
echo "Source Skills : $SOURCE_SKILLS_DIR (${#SKILLS[@]} skills found)"

# 2. Determine destination skills directory
if [ -n "$TARGET_REPO" ]; then
    if [ ! -d "$TARGET_REPO" ]; then
        echo "[FAIL] Specified TargetRepo directory does not exist: $TARGET_REPO" >&2
        exit 1
    fi
    RESOLVED_TARGET="$(cd "$TARGET_REPO" && pwd)"
    DEST_SKILLS_DIR="$RESOLVED_TARGET/.codex/skills"
    echo "Target Mode   : Target Repository ($RESOLVED_TARGET)"
elif [ -n "$CODEX_DIR" ]; then
    DEST_SKILLS_DIR="$CODEX_DIR"
    echo "Target Mode   : Custom Directory ($DEST_SKILLS_DIR)"
else
    if [ -n "${CODEX_HOME:-}" ]; then
        DEST_SKILLS_DIR="$CODEX_HOME/skills"
    else
        DEST_SKILLS_DIR="$HOME/.codex/skills"
    fi
    echo "Target Mode   : User-Level Codex Skills ($DEST_SKILLS_DIR)"
fi

echo "Destination   : $DEST_SKILLS_DIR"
if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] No filesystem modifications will be made."
fi
echo "------------------------------------------------------------"

# 3. Handle uninstallation
if [ "$UNINSTALL" = true ]; then
    echo "Starting uninstallation of Dev-Team skills..."
    REMOVED_COUNT=0
    SKIPPED_COUNT=0

    if [ ! -d "$DEST_SKILLS_DIR" ]; then
        echo "Destination directory does not exist. Nothing to uninstall."
        exit 0
    fi

    for skill_name in "${SKILLS[@]}"; do
        target_path="$DEST_SKILLS_DIR/$skill_name"
        if [ -L "$target_path" ] || [ -d "$target_path" ]; then
            echo "  -> Removing Dev-Team skill: $skill_name"
            if [ "$DRY_RUN" = false ]; then
                rm -rf "$target_path"
            fi
            REMOVED_COUNT=$((REMOVED_COUNT + 1))
        else
            SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        fi
    done

    echo "------------------------------------------------------------"
    echo "Uninstallation Summary:"
    echo "  Skills Removed : $REMOVED_COUNT"
    echo "  Not Found/Skip : $SKIPPED_COUNT"
    echo "  Unrelated skills in destination were preserved."
    exit 0
fi

# 4. Handle installation
echo "Starting installation (Mode: $MODE)..."

if [ ! -d "$DEST_SKILLS_DIR" ] && [ "$DRY_RUN" = false ]; then
    mkdir -p "$DEST_SKILLS_DIR"
    echo "Created destination skills directory: $DEST_SKILLS_DIR"
fi

if [ -n "$TARGET_REPO" ] && [ "$DRY_RUN" = false ]; then
    mkdir -p "$RESOLVED_TARGET/.dev-team/features"
    echo "Scaffolded target directory: $RESOLVED_TARGET/.dev-team/features"
fi

INSTALLED_COUNT=0
UPDATED_COUNT=0
SKIPPED_COUNT=0
FAILED_COUNT=0

for skill_name in "${SKILLS[@]}"; do
    src_path="$SOURCE_SKILLS_DIR/$skill_name"
    dest_path="$DEST_SKILLS_DIR/$skill_name"

    if [ "$MODE" = "copy" ]; then
        if [ -d "$dest_path" ] || [ -L "$dest_path" ]; then
            echo "  [UPDATE] Updating existing skill: $skill_name"
            if [ "$DRY_RUN" = false ]; then
                rm -rf "$dest_path"
                cp -R "$src_path" "$dest_path"
            fi
            UPDATED_COUNT=$((UPDATED_COUNT + 1))
        else
            echo "  [INSTALL] Copying skill: $skill_name"
            if [ "$DRY_RUN" = false ]; then
                cp -R "$src_path" "$dest_path"
            fi
            INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
        fi
    elif [ "$MODE" = "symlink" ]; then
        if [ -L "$dest_path" ]; then
            current_target="$(readlink "$dest_path" || true)"
            if [ "$current_target" = "$src_path" ]; then
                echo "  [SKIP] Link already points to target: $skill_name"
                SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
                continue
            fi
        fi

        if [ -e "$dest_path" ] || [ -L "$dest_path" ]; then
            if [ "$FORCE" = true ]; then
                echo "  [REPLACE] Overwriting existing destination for symlink: $skill_name"
                if [ "$DRY_RUN" = false ]; then
                    rm -rf "$dest_path"
                    ln -s "$src_path" "$dest_path"
                fi
                INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
            else
                echo "  [SKIP] Destination already exists (use -f to replace): $skill_name"
                SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
                continue
            fi
        else
            echo "  [LINK] Creating symlink for skill: $skill_name"
            if [ "$DRY_RUN" = false ]; then
                ln -s "$src_path" "$dest_path"
            fi
            INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
        fi
    fi
done

echo "------------------------------------------------------------"
echo "Installation Summary:"
echo "  New Skills Installed : $INSTALLED_COUNT"
echo "  Skills Updated       : $UPDATED_COUNT"
echo "  Skills Skipped       : $SKIPPED_COUNT"
echo "  Skills Failed        : $FAILED_COUNT"

if [ "$FAILED_COUNT" -gt 0 ]; then
    echo "[RESULT] Installation finished with errors." >&2
    exit 1
fi

echo "[RESULT] Dev-Team skills successfully configured!"
exit 0

