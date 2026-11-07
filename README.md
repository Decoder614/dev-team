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

## 2. Quickstart & Installation (CLI & Hybrid Distribution)

Dev-Team provides a **CLI-first, hybrid distribution model**. You install the CLI and global skills once, then initialize and onboard any target repository.

### 2.1 Bootstrap the CLI

```bash
# Install the Dev-Team CLI in editable/user mode
pip install -e ./cli
```

### 2.2 Global Skill Installation

Install the canonical Dev-Team skills, templates, and adapters globally:

```bash
dev-team install --global --platform codex
```

### 2.3 Initialize Target Project & AI Onboarding

Navigate to your target application repository:

```bash
cd /path/to/my-application

# 1. Deterministic CLI initialization (creates .dev-team/ and links skills)
dev-team init --mode hybrid --platform codex

# 2. Contextual AI onboarding (inside OpenAI Codex CLI or supported shell)
# Run: /project-initializer
```

For complete prerequisites, custom paths, and platform matrices, see the [Installation Guide](docs/installation.md) and [Platform Compatibility Guide](docs/platform-compatibility.md).

---

## 3. Engineering Workflows

Dev-Team coordinates engineering through nine standard operating procedures:

| Workflow | Entry Point | Primary Role | Activated Skill | Purpose |
|---|---|---|---|---|
| **Initialize Project** | `workflows/initialize-project.md` | Initializer / Architect | `project-initializer` | Onboard repository, classify state, establish persistent context |
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

Dev-Team operates across five decoupled architectural layers:

```text
Layer 1 — Developer Interface (Dev-Team CLI · AI Coding Agents)
Layer 2 — Platform Adapters (Codex · Claude Code · Cursor · Copilot · Gemini)
Layer 3 — Dev-Team Core (Skills · Workflows · Agents · Templates · Policies)
Layer 4 — Project Context (.dev-team/ · project-context.md · config.yaml · local skills)
Layer 5 — Target Repository (Application source code · Tests · CI/CD)
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
├── cli/                   # Dedicated Dev-Team CLI engine (init, install, update, doctor)
│
├── adapters/              # Modular platform adapters (codex, claude-code, cursor, copilot, gemini)
│
├── schemas/               # JSON schemas (project-config, adapter-manifest, installation-manifest)
│
├── config/                # System-wide configuration (workflow.yaml, quality-gates.yaml, defaults.yaml)
│
├── agents/                # Specialized AI agent role definitions (Analyst, Reviewer, Architect, etc.)
│
├── skills/                # Reusable procedural engineering skills (Agent Skills: SKILL.md)
│
├── workflows/             # End-to-end engineering workflows (new-feature, design-feature, etc.)
│
├── templates/             # Standardized document templates & target project scaffolding
│
├── scripts/               # Deterministic automation and workspace verification scripts
│
└── docs/                  # System documentation and project artifacts
    ├── architecture.md
    ├── installation.md
    ├── platform-compatibility.md
    ├── workflows.md
    ├── contribution-guide.md
    └── project/           # Internal Dev-Team specifications (requirements, system-design, plan)
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
