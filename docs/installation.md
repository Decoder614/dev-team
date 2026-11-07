# Dev-Team Installation & Configuration Guide

> **Specification-Driven AI Software Development Team**  
> Comprehensive setup instructions for deploying Dev-Team skills and workflows across independent target repositories.

---

## 1. Overview & Architecture

Dev-Team is a reusable, modular framework that coordinates specialized engineering roles using the OpenAI Codex CLI. It follows a strict **separation of concerns**:

- **Reusable Framework (`dev-team`):** General workflows, role specifications (`agents/`), reusable procedural skills (`skills/`), standardized templates (`templates/`), and quality configuration (`config/`) remain strictly project-agnostic (`REQ-071`).
- **Target Application Repositories:** Framework-specific conventions, business logic, architecture records, and task documentation reside exclusively inside each target project's repository under `AGENTS.md` and `.dev-team/` (`REQ-070`).

Target applications consume Dev-Team capabilities through the Codex CLI's built-in skill discovery mechanism without duplicating the entire framework repository (`REQ-067`, `REQ-069`).

---

## 2. Prerequisites

Before installing Dev-Team, ensure the following tools are available on your system:

| Component | Minimum Version | Verification Command | Notes |
|---|---|---|---|
| **OpenAI Codex CLI** | Any supported release | `codex --version` | Must be authenticated and operational. |
| **Python** | 3.10+ | `python --version` | Required for deterministic workspace validation scripts (`REQ-072`). |
| **Git** | 2.30+ | `git --version` | Required for version control and status inspection. |
| **PowerShell** | 5.1+ (Windows) | `$PSVersionTable.PSVersion` | Required for Windows automated installation (`install.ps1`). |
| **Bash / POSIX Shell** | Bash 4.0+ / POSIX | `bash --version` | Required for Unix-like automated installation (`install.sh`). |

---

## 3. Supported Codex Skill Discovery

OpenAI Codex CLI automatically discovers procedural skills from designated directories:

1. **User-Level Skills (Global):**
   - **Windows:** `$env:USERPROFILE\.codex\skills\` (or `$env:CODEX_HOME\skills\` if set)
   - **Unix / macOS:** `~/.codex/skills/` (or `$CODEX_HOME/skills` if set)
   - *Behavior:* Skills placed in this directory are available across **all** repositories and workspaces opened with Codex CLI.

2. **Repository-Level Skills (Local):**
   - `<repository-root>/.codex/skills/` or `<repository-root>/skills/`
   - *Behavior:* Skills placed here are scoped strictly to the current workspace.

### Reusable Skills Packaging

Each skill in `dev-team/skills/` conforms to the standard Codex skill specification (`REQ-067`):

```text
skills/<skill-name>/
└── SKILL.md
```

The `SKILL.md` file contains YAML frontmatter defining `name` and `description` triggers, followed by modular procedural instructions:

```yaml
---
name: <skill-name>
description: Reusable procedural skill for ... Activate when ...
---
```

---

## 4. Installation Strategies

Dev-Team provides two primary installation strategies (`ADR-013`):

### Option A — Shared Skill Installation (Copy Mode, Recommended Default)

Copies each reusable skill directory from `dev-team/skills/` into the user-level Codex skills directory.

- **Advantages:**
  - Fully decoupled from the location of the `dev-team` repository clone.
  - Safe, immutable, and does not require administrative privileges.
  - Fully portable across all user workspaces.
- **Trade-off:**
  - When updating Dev-Team, you must re-run the installer to copy the latest skills.

### Option B — Symbolic Linking (Symlink / Junction Mode)

Creates filesystem links from the user-level Codex skills directory pointing directly to the `dev-team/skills/` directories.

- **Advantages:**
  - Real-time updates: Edits in `dev-team` take effect immediately without re-installing.
  - Zero disk duplication.
- **Trade-off:**
  - On Windows, creating symbolic links requires Developer Mode or administrator privileges. If privileges are absent, the installer automatically falls back to NTFS Directory Junctions (`mklink /J`).

---

## 5. Automated Installation on Windows

Use the PowerShell installer `scripts/install.ps1` (`Task M8-T02`).

### 5.1 Basic Installation (Copy Mode)

Open PowerShell and run:

```powershell
# From the dev-team repository root
.\scripts\install.ps1
```

By default, this installs all skills to `$env:USERPROFILE\.codex\skills\`.

### 5.2 Symlink / Junction Mode

To link skills directly from the source repository:

```powershell
.\scripts\install.ps1 -Mode Symlink
```

### 5.3 Custom Codex Skills Directory

If your Codex configuration uses a custom directory or `$env:CODEX_HOME`:

```powershell
.\scripts\install.ps1 -CodexDir "D:\CustomCodex\skills"
```

### 5.4 Target Repository Installation

To install skills directly into a specific target application repository:

```powershell
.\scripts\install.ps1 -TargetRepo "E:\apps\my-flutter-app"
```

This installs skills into `E:\apps\my-flutter-app\.codex\skills\` and initializes the target directory structure (`.dev-team/`).

### 5.5 Dry-Run Mode

Preview actions without modifying the filesystem:

```powershell
.\scripts\install.ps1 -DryRun
```

### 5.6 Uninstallation

To cleanly remove only the Dev-Team skills while **strictly preserving** any other user-installed skills:

```powershell
.\scripts\install.ps1 -Uninstall
```

---

## 6. Automated Installation on Unix / macOS

Use the POSIX-compliant shell script `scripts/install.sh` (`Task M8-T03`).

### 6.1 Basic Installation (Copy Mode)

```bash
# Make script executable if necessary
chmod +x scripts/install.sh

# Run standard installation
./scripts/install.sh
```

### 6.2 Symlink Mode

```bash
./scripts/install.sh -m symlink
```

### 6.3 Custom Codex Skills Directory

```bash
./scripts/install.sh -d "$HOME/.custom-codex/skills"
```

### 6.4 Target Repository Installation

```bash
./scripts/install.sh -t "/path/to/my-application"
```

### 6.5 Dry-Run Mode

```bash
./scripts/install.sh -n
```

### 6.6 Uninstallation

```bash
./scripts/install.sh -u
```

---

## 7. Configuring a Target Repository

Once Dev-Team skills are installed globally or locally, configure your target application repository to activate the virtual team workflows (`REQ-070`).

### Automated Initialization (Recommended)

Run the automated repository onboarding workflow within the target repository using Codex CLI:

```text
/project-initializer
```
Or instruct Codex:
> *"Initialize this repository for Dev-Team"*

This runs `workflows/initialize-project.md`, executes `check-project-structure.py`, identifies your tech stack, conducts an adaptive interview if empty, and instantiates the complete templates suite (`templates/project/`) establishing `AGENTS.md`, `rules.md`, `DESIGN.md`, `.dev-team/config.yaml`, `.dev-team/project-context.md`, and baseline docs under `docs/project/`.

### Manual Initialization

Alternatively, you can manually bootstrap the target repository:

#### Step 1: Create `AGENTS.md` and `rules.md` in Target Repository Root
Instantiate from `templates/project/AGENTS.md` and `templates/project/rules.md`.

Example target `AGENTS.md`:

```markdown
# AGENTS.md — Target Project Operating Instructions

> Operating instructions for OpenAI Codex CLI in this project.

## 1. Project Overview & Dev-Team Integration
This repository uses the Dev-Team specification-driven engineering framework.
Engineering workflows follow the approved lifecycle:
`Requirement -> System Design -> Plan -> Implementation -> QA Report -> Acceptance`.

## 2. Workflows & Skill Activation
- Project Initialization: Invoke `initialize_project` workflow using `project-initializer` skill.
- New Feature: Invoke `new-feature` workflow using `product-requirements` skill.
- Requirements Audit: Invoke `validate-requirement` workflow using `requirement-validation` skill.
- Technical Design: Invoke `design-feature` workflow using `project-discovery` and `system-design` skills.
- Planning: Invoke `create-plan` workflow using `technical-planning` skill.
- Implementation: Invoke `implement-next` workflow using `flutter-development` or domain skills.
- Verification: Invoke `validate-feature` workflow using `feature-validation` and `code-review` skills.
- Bug Fixing: Invoke `fix-bug` workflow using `bug-fixing` skill.
- Feature Status: Invoke `feature-status` workflow.

## 3. Mandatory Safety Boundaries
- SAFE-001: Requirements must be approved by developer prior to implementation.
- SAFE-002: Architecture and schema changes require developer approval.
- SAFE-003: Technical plan must be approved prior to starting code modifications.
- SAFE-009: Never claim tests passed without executing verification commands and observing output.
- SAFE-010: Never overwrite uncommitted developer changes.
```

### Step 2: Initialize `.dev-team/project-profile.yaml`

Create `.dev-team/project-profile.yaml` to inform Dev-Team of your project's technology stack, test commands, and conventions:

```yaml
version: 1
project:
  name: "my-app"
  framework: "flutter" # or react, node, django, go, etc.
  language: "dart"

paths:
  features_directory: ".dev-team/features"
  source_directory: "lib"
  test_directory: "test"

validation:
  test_command: "flutter test"
  analyze_command: "flutter analyze"
  format_command: "dart format --output=none --set-exit-if-changed ."
```

### Step 3: Feature Artifact Directory

Feature specifications, design docs, plans, and QA reports will be organized under:

```text
.dev-team/features/<feature-name>/
├── requirement.md
├── system-design.md
├── plan.md
├── tasks/ (optional)
└── qa-report.md
```

---

## 8. Verifying Your Installation

Use the workspace validation utility `scripts/validate-workspace.py` (`Task M8-T04`) to verify system integrity:

```bash
# Validate Dev-Team workspace
python scripts/validate-workspace.py

# Validate a target project repository
python scripts/validate-workspace.py --target "/path/to/target-project"
```

A return code of `0` indicates all directories, configurations, skills, and templates are structurally valid.

---

## 9. Troubleshooting

### Problem: Codex CLI does not discover installed skills
- **Cause:** Codex CLI caches skills at startup or looks at a different user home directory.
- **Solution:** 
  1. Restart your Codex CLI session.
  2. Verify that `$env:USERPROFILE\.codex\skills` (Windows) or `~/.codex/skills` (Unix) contains subdirectories with `SKILL.md`.
  3. Ensure YAML frontmatter in `SKILL.md` starts on line 1 with `---`.

### Problem: Symlink creation failed on Windows
- **Cause:** Windows requires administrator privileges or Developer Mode to create symbolic links.
- **Solution:** 
  - `install.ps1` automatically detects this and falls back to NTFS Junctions (`mklink /J`), which require no administrator privileges.
  - Alternatively, use Copy Mode: `.\scripts\install.ps1 -Mode Copy`.

### Problem: Target repository has an existing `AGENTS.md`
- **Cause:** Repository already has local agent rules.
- **Solution:** Merge the Dev-Team workflow entry points into your existing `AGENTS.md`. Target project instructions always take precedence over generic instructions (`REQ-070`).

---

## 10. Uninstallation & Cleanup

To remove Dev-Team skills completely:

```powershell
# Windows
.\scripts\install.ps1 -Uninstall
```

```bash
# Unix / macOS
./scripts/install.sh -u
```

The uninstallation scripts:
1. Scan for skills originally installed by Dev-Team.
2. Remove only those matching directories or links.
3. Leave all non-Dev-Team skills untouched.

