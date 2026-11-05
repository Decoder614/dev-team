# Dev-Team

> **Your AI Software Development Team.**

Dev-Team is a reusable, specification-driven AI software engineering framework designed to help an individual developer coordinate a virtual team of specialized AI agents across multiple independent software projects using OpenAI Codex CLI.

It provides repeatable workflows, role-specific agent instructions, reusable skills, templates, quality gates, and project discovery mechanisms. Dev-Team guides work through the entire software engineering lifecycle—from rough product idea to validated, production-ready code.

---

## 1. Product Overview

### 1.1 Purpose
When developing software independently, a single developer must switch between product management, system architecture, UI/UX, implementation, quality assurance, code review, debugging, and release preparation.

Dev-Team provides a structured, specification-driven engineering system that:
- Converts informal feature ideas into unambiguous, testable requirements.
- Independently reviews requirements before implementation.
- Discovers target project conventions without enforcing hardcoded technology stacks.
- Produces modular technical designs and sequenced implementation plans.
- Implements code one approved task at a time following established project patterns.
- Performs independent QA and validation based on concrete observed evidence.
- Diagnoses and resolves defects through a systematic bug-fixing process.
- Reuses common engineering procedures across separate application repositories.

### 1.2 Core Principles
1. **Developer remains in control:** AI agents recommend and implement approved work; approval authority remains with the developer.
2. **Requirements before implementation:** Work begins with agreed problem statements and acceptance criteria.
3. **Project-aware, not project-prescriptive:** Dev-Team respects and adopts target repository conventions rather than imposing a single framework or architecture.
4. **Simple before sophisticated:** Favor minimal, maintainable solutions over complex orchestration.
5. **Small, verifiable tasks:** Implementation proceeds one deliverable at a time with testable acceptance criteria.
6. **Evidence over claims:** A task or feature is marked complete only when verified by actual test and command execution.
7. **Traceability:** Requirements map to design decisions, implementation tasks, tests, and QA results.
8. **Separation of concerns:** Reusable system capabilities remain in `dev-team`; project-specific facts remain in the target repository.

---

## 2. Quickstart & Installation

Dev-Team skills can be installed globally into your user-level Codex skills directory or linked into specific target projects.

### 2.1 Windows Installation

```powershell
# Default installation (copies skills to ~/.codex/skills/)
.\scripts\install.ps1

# Symlink/junction installation (live updates from source repository)
.\scripts\install.ps1 -Mode Symlink

# Install directly into a specific target project repository
.\scripts\install.ps1 -TargetRepo "C:\apps\my-project"
```

### 2.2 Unix / macOS Installation

```bash
# Default installation
./scripts/install.sh

# Symlink mode
./scripts/install.sh -m symlink

# Install into a target project repository
./scripts/install.sh -t "/path/to/my-project"
```

For complete prerequisites, custom paths, and uninstallation instructions, see the [Installation Guide](docs/installation.md).

```powershell
# Default installation (copies skills to ~/.codex/skills/)
.\scripts\install.ps1

# Symlink/junction installation (live updates from source repository)
.\scripts\install.ps1 -Mode Symlink

# Install directly into a specific target project repository
.\scripts\install.ps1 -TargetRepo "E:\apps\my-project"
```

### 2.2 Unix / macOS Installation

```bash
# Default installation
./scripts/install.sh

# Symlink mode
./scripts/install.sh -m symlink

# Install into a target project repository
./scripts/install.sh -t "/path/to/my-project"
```

For complete prerequisites, custom paths, and uninstallation instructions, see the [Installation Guide](docs/installation.md).

---

## 3. Engineering Workflows

Dev-Team coordinates engineering through eight standard operating procedures:

| Workflow | Entry Point | Primary Role | Activated Skill | Purpose |
|---|---|---|---|---|
| **New Feature** | `workflows/new-feature.md` | Product Analyst | `product-requirements` | Draft requirements and acceptance criteria |
| **Validate Requirement** | `workflows/validate-requirement.md` | Product Reviewer | `requirement-validation` | Independent requirements audit and gap check |
| **Design Feature** | `workflows/design-feature.md` | System Architect | `system-design` | Technical architecture and data modeling |
| **Create Plan** | `workflows/create-plan.md` | Technical Planner | `technical-planning` | Task slicing, dependencies, and validation steps |
| **Implement Next** | `workflows/implement-next.md` | Developer | `flutter-development` | Controlled single-task implementation & tests |
| **Validate Feature** | `workflows/validate-feature.md` | QA Engineer | `feature-validation` | End-to-end verification and QA report |
| **Fix Bug** | `workflows/fix-bug.md` | Developer / QA | `bug-fixing` | Defect reproduction, minimal fix & regression tests |
| **Feature Status** | `workflows/feature-status.md` | Auditor | *Direct Inspection* | Zero-hallucination progress accounting |

For comprehensive phase diagrams, prerequisites, and developer commands, see the [Workflows Guide](docs/workflows.md).

---

## 4. System Architecture & Boundaries

Dev-Team operates across eight modular architectural layers:

```text
Interface Layer (Codex CLI)
  └── Orchestration Layer (Root AGENTS.md & Approval Gates)
        ├── Configuration Layer (workflow.yaml, quality-gates.yaml, defaults.yaml)
        ├── Agent Layer (6 declarative role specifications in agents/*.toml)
        ├── Skill Layer (9 reusable procedural skills in skills/*/SKILL.md)
        ├── Workflow Layer (8 end-to-end procedures in workflows/*.md)
        ├── Template Layer (6 standardized artifact formats in templates/*.md)
        └── Project Context Layer (target AGENTS.md, .dev-team/project-profile.yaml)
```

### Mandatory Safety Gates
- **SAFE-001:** Developer must approve requirements before implementation begins.
- **SAFE-002:** Developer must approve significant architecture and data-model changes.
- **SAFE-003:** Developer must approve technical implementation plan before code modifications.
- **SAFE-009:** Never claim tests passed without executing commands and observing output.
- **SAFE-010:** Inspect git status prior to edits; never overwrite uncommitted developer work.

For complete architectural details, see the [Architecture Guide](docs/architecture.md).

---

## 5. Repository Organization

```text
dev-team/
├── README.md              # Project overview and system documentation
├── AGENTS.md              # Root operating instructions for Codex CLI
├── LICENSE                # Open-source license (MIT)
├── .gitignore             # Ignored environment, cache, and OS files
│
├── config/                # System-wide configuration
│   ├── workflow.yaml      # Workflow execution settings and defaults
│   ├── quality-gates.yaml # Quality and acceptance criteria gates
│   └── defaults.yaml      # Reusable system defaults
│
├── agents/                # Specialized AI agent role definitions
│   ├── product-analyst.toml
│   ├── product-reviewer.toml
│   ├── system-architect.toml
│   ├── technical-planner.toml
│   ├── developer.toml
│   └── qa-engineer.toml
│
├── skills/                # Reusable procedural engineering skills
│   ├── product-requirements/
│   ├── requirement-validation/
│   ├── project-discovery/
│   ├── system-design/
│   ├── technical-planning/
│   ├── flutter-development/
│   ├── code-review/
│   ├── feature-validation/
│   └── bug-fixing/
│
├── workflows/             # End-to-end engineering workflows
│   ├── new-feature.md
│   ├── validate-requirement.md
│   ├── design-feature.md
│   ├── create-plan.md
│   ├── implement-next.md
│   ├── validate-feature.md
│   ├── fix-bug.md
│   └── feature-status.md
│
├── templates/             # Standardized document templates
│   ├── requirement.md
│   ├── system-design.md
│   ├── plan.md
│   ├── task.md
│   ├── bug-report.md
│   └── qa-report.md
│
├── scripts/               # Deterministic automation and validation scripts
│   ├── install.ps1
│   ├── install.sh
│   └── validate-workspace.py
│
└── docs/                  # System documentation and project artifacts
    ├── architecture.md
    ├── installation.md
    ├── workflows.md
    ├── contribution-guide.md
    └── project/           # Internal Dev-Team specifications
        ├── requirements.md
        ├── system-design.md
        └── plan.md
```

---

## 6. Workspace Validation

Verify the integrity of the framework or a configured target application repository using the deterministic validator:

```bash
# Validate Dev-Team workspace
python scripts/validate-workspace.py --verbose

# Validate a target project repository
python scripts/validate-workspace.py --target "/path/to/target-project"
```

---

## Contributing

Contributions are welcome! Read the [Contribution Guide](docs/contribution-guide.md) for instructions on creating new agents, authoring reusable skills, and submitting pull requests.

---

## License

This project is licensed under the [MIT License](LICENSE).
