# Dev-Team CLI

Dedicated Command-Line Interface package for **Dev-Team**, a specification-driven, modular AI software engineering framework.

---

## 1. Overview

The `dev-team` CLI handles deterministic filesystem operations, workspace inspection, global asset distribution, provenance tracking, and environment diagnostics:

- **Global Asset Management (`~/.dev-team/`):** Centrally installs and tracks canonical skills, templates, and platform adapter manifests.
- **Workspace & Stack Detection:** Identifies Git roots, workspace structures, and existing Dev-Team configurations without heuristic guesswork.
- **Provenance & Integrity Engine:** Computes SHA-256 digests for all managed artifacts and tracks them in `manifest.json` adhering to `schemas/installation-manifest.schema.json`.
- **System Diagnostics (`dev-team doctor`):** Audits Python/Git prerequisites, write permissions, manifest integrity, and AI coding platform discovery paths.

---

## 2. Installation

### From Source (Editable Mode)

```powershell
# Windows
pip install -e .\cli

# Unix / macOS
pip install -e ./cli
```

Verify installation:

```bash
dev-team --version
dev-team --help
```

---

## 3. Command Usage

### 3.1 Global Installation (`install`)

Installs canonical skills, templates, adapters, version, and provenance manifest into `~/.dev-team/`:

```bash
# Install all canonical assets for OpenAI Codex CLI
dev-team install --global --platform codex

# Install a specific skill
dev-team install --global --skill flutter-development

# Dry-run preview
dev-team install --global --dry-run
```

### 3.2 System & Installation Diagnostics (`doctor`)

Diagnoses host environment prerequisites, global installation integrity, and AI platform discovery:

```bash
# Run diagnostics
dev-team doctor

# Inspect custom target installation
dev-team doctor --target /path/to/.dev-team
```

### 3.3 Workspace Inspection (`status` & `list`)

```bash
# Check current workspace state
dev-team status

# List canonical skills and installation status
dev-team list --skills

# List supported AI coding platforms
dev-team list --platforms
```

### 3.4 Target Repository Scaffolding (`init`)

```bash
# Prepare .dev-team/ scaffolding for subsequent AI onboarding
dev-team init --mode hybrid --platform codex
```

---

## 4. Architecture & Package Structure

```text
cli/
├── pyproject.toml              # Build backend configuration
├── setup.py                    # Package specification and console_scripts
├── README.md                   # CLI documentation
├── src/
│   ├── __init__.py             # Package version
│   ├── main.py                 # CLI entry point and argument routing
│   ├── commands/               # Modular command handlers
│   │   ├── doctor.py           # Environment and manifest diagnostics
│   │   ├── install.py          # Global asset installation
│   │   ├── init.py             # Target repo initialization
│   │   ├── list.py             # Skills and platforms catalog
│   │   ├── status.py           # Workspace status reporting
│   │   ├── update.py           # Asset updating
│   │   └── uninstall.py        # Clean asset removal
│   ├── core/                   # Provenance, hashing, and manifests
│   │   ├── constants.py        # Default paths, versions, and enums
│   │   ├── exceptions.py       # Custom exception hierarchy
│   │   ├── manifest.py         # Manifest tracking & validation
│   │   └── provenance.py       # SHA-256 calculation & drift detection
│   ├── detection/              # Workspace and platform detection
│   │   ├── platform.py         # AI platform readiness checks
│   │   └── workspace.py        # Git root and project classifier
│   ├── installation/           # Filesystem strategies & global installer
│   │   ├── global_installer.py # ~/.dev-team/ distribution engine
│   │   └── strategies.py       # Safe copy, symlink, and junctions
│   └── reporting/              # Formatting and terminal tables
│       └── tables.py           # Table rendering and status badges
└── tests/                      # Automated test suite
    ├── test_cli.py
    ├── test_detection.py
    ├── test_doctor.py
    ├── test_global_installer.py
    └── test_manifest.py
```

---

## 5. Running Tests

```bash
# Run all unit and integration tests
pytest cli/tests -v

# Run Milestone 2 deterministic validation script
python scripts/validate_milestone_2.py
```
