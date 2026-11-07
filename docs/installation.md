# Dev-Team Installation & Configuration Guide

> **Specification-Driven AI Software Development Team**  
> Comprehensive setup instructions for deploying Dev-Team skills, CLI, and workflows across independent target repositories (Version 1.1).

---

## 1. Overview & Architecture

Dev-Team provides a **CLI-first, hybrid-distribution** architecture that coordinates specialized engineering roles across independent repositories:

- **Dedicated Dev-Team CLI (`dev-team`):** Deterministic tool managing installation, initialization, updates, and diagnostics without requiring an LLM (`REQ-066`, `REQ-067`, `REQ-072`).
- **Global Installation (`~/.dev-team/`):** Centrally stores reusable Agent Skills (`SKILL.md`), templates, and platform adapters (`REQ-069`, `REQ-071`).
- **Target Application Repositories (`.dev-team/`):** Each target repository maintains its own isolated configuration (`config.yaml`), persistent context (`project-context.md`), and optional local custom skills (`REQ-070`).
- **Platform Adapters:** Expose reusable skills to target AI coding platforms (OpenAI Codex CLI, Claude Code, Cursor, Copilot, Gemini).

---

## 2. Prerequisites

| Tool | Minimum Version | Verification Command | Notes |
|---|---|---|---|
| **Python** | 3.10+ | `python --version` | Required for the Dev-Team CLI engine (`REQ-021`, `REQ-072`). |
| **Git** | 2.30+ | `git --version` | Required for repository detection and status checks. |
| **AI Coding Platform** | Current release | `codex --version` / `claude --version` | OpenAI Codex CLI (initial reference integration) or other supported platform. |
| **PowerShell / Bash** | PS 5.1+ / Bash 4+ | `$PSVersionTable.PSVersion` / `bash --version` | System shell for environment setup and automated script installation. |

---

## 3. Supported Codex Skill Discovery

OpenAI Codex CLI automatically discovers procedural skills from designated directories (`REQ-067`, `REQ-071`):

1. **User-Level Skills (Global):**
   - **Windows:** `$env:USERPROFILE\.codex\skills\` (or `$env:CODEX_HOME\skills\` if set)
   - **Unix / macOS:** `~/.codex/skills/` (or `$CODEX_HOME/skills` if set)
   - *Behavior:* Skills placed in this directory are available across **all** repositories and workspaces opened with Codex CLI.

2. **Repository-Level Skills (Local Projection):**
   - `<workspace>/.agents/skills/` or `<workspace>/.codex/skills/`
   - *Behavior:* Skills projected here are scoped strictly to the current workspace.

### Reusable Skills Packaging
Each skill in `dev-team/skills/` conforms to the standard Agent Skills specification (`SKILL.md` with YAML frontmatter).

---

## 4. Installation Strategies

Dev-Team supports three primary installation strategies (`REQ-069`, `ADR-016`):

### Option A — Hybrid Mode (Recommended Default)
```bash
dev-team init --mode hybrid --platform codex
```
- Core reusable skills reside centrally in `~/.dev-team/skills/`.
- Target repository creates `.dev-team/` for local configuration and context.
- Skill projections are safely linked into the platform discovery location (`.agents/skills/`).
- Maximum efficiency, zero unnecessary file duplication, and clean project isolation.

### Option B — Global Mode
```bash
dev-team install --global --platform codex
```
- Installs canonical skills directly to user-level discovery (`~/.codex/skills/` or `~/.dev-team/`).
- Available across all workspaces without modifying repository files.

### Option C — Project Copy Mode
```bash
dev-team init --mode copy
```
- Copies independent skill directories directly into the target project workspace.
- Useful for offline or restricted environments where filesystem links are prohibited.

---

## 5. Automated Installation on Windows

### 5.1 CLI-First Installation (Recommended)
Install the CLI and global skills:
```powershell
# From the dev-team clone
pip install -e .\cli

# Install global skills and Codex platform integration
dev-team install --global --platform codex
```

### 5.2 PowerShell Script Installation (`scripts/install.ps1`)
Alternatively, use the deterministic PowerShell bootstrap script:
```powershell
# Default installation (copies skills to user Codex skills directory)
.\scripts\install.ps1

# Symlink / Junction mode
.\scripts\install.ps1 -Mode Symlink

# Target repository installation
.\scripts\install.ps1 -TargetRepo "C:\apps\my-project"

# Dry-run preview
.\scripts\install.ps1 -DryRun
```

---

## 6. Automated Installation on Unix

### 6.1 CLI-First Installation (Recommended)
```bash
# Install the CLI
pip install -e ./cli

# Install global skills
dev-team install --global --platform codex
```

### 6.2 Bash Script Installation (`scripts/install.sh`)
Alternatively, use the POSIX shell bootstrap script:
```bash
# Default installation
./scripts/install.sh

# Symlink mode
./scripts/install.sh -m symlink

# Target repository installation
./scripts/install.sh -t "/path/to/my-project"

# Dry-run preview
./scripts/install.sh -n
```

---

## 7. Configuring a Target Repository

To onboard any target software repository for Dev-Team:

### Step 1: Deterministic CLI Initialization
Navigate to the target application repository:
```bash
cd /path/to/my-application
dev-team init --platform codex --mode hybrid
```
This command sets up `.dev-team/config.yaml`, creates skill projections in `.agents/skills/`, and writes `installation-manifest.json` (`REQ-067`, `REQ-070`).

### Step 2: Contextual AI Onboarding (`/project-initializer`)
Open the target repository in OpenAI Codex CLI and run:
```text
> /project-initializer
```
The AI onboarding skill:
1. Inspects repository manifests, dependencies, and code structure.
2. Classifies project state (`EXISTING`, `EMPTY`, or `PARTIAL`).
3. Gathers confirmed facts versus active assumptions.
4. Requests developer approval before generating files (`SAFE-001`).
5. Scaffolds `AGENTS.md`, `rules.md`, `DESIGN.md`, and baseline `docs/project/`.
6. Establishes the canonical context store in `.dev-team/project-context.md`.

---

## 8. Verifying Your Installation

Validate your Dev-Team setup and workspace health using `dev-team doctor`:

```bash
# Run installation diagnostics
dev-team doctor

# Verbose inspection of paths, manifests, and hashes
dev-team doctor --verbose
```

You can also run the deterministic workspace validator script:
```bash
python scripts/validate-workspace.py --verbose
```

---

## 9. Uninstallation & Cleanup

Dev-Team provides safe, non-destructive removal of managed files:

### CLI Removal
```bash
# Remove global Dev-Team assets and links
dev-team uninstall --global

# Remove project-level projections and configuration
dev-team uninstall --project
```

### Script Cleanup
```powershell
# Windows
.\scripts\install.ps1 -Uninstall
```
```bash
# Unix
./scripts/install.sh -u
```
> **Safety Guarantee:** Uninstallation deletes *only* files tracked as managed in the installation manifest. Unrelated developer files, custom skills, and application code are strictly preserved.

---

## 10. Troubleshooting & FAQ

### Q: Does Dev-Team alter application source code during installation?
**No.** `dev-team init` operates non-invasively (`REQ-075`). It only creates `.dev-team/`, platform discovery projections, and initial documentation. Your source code and architecture remain untouched.

### Q: How do symlinks work on Windows?
On Windows 10/11, symbolic links require Developer Mode or elevated privileges. If privileges are absent, the Dev-Team CLI automatically falls back to **NTFS Directory Junctions** (`mklink /J`), which require no administrator rights. If junctions are unsupported, it falls back to safe file copies.

### Q: Can I customize a skill for a specific project?
**Yes.** Place your customized skill in `<project-root>/.dev-team/skills/<skill-name>/SKILL.md`. Dev-Team's resolution engine always gives project-local skills higher priority than globally installed skills (`REQ-081`).
