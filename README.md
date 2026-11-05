# Dev-Team

> **Your AI Software Development Team.**

Dev-Team is a reusable, AI-powered software engineering system designed to help an individual developer coordinate a virtual team of specialized AI agents across multiple independent software projects using OpenAI Codex CLI.

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

## 2. High-Level Architecture

Dev-Team operates as a modular, skill-driven system coordinated within OpenAI Codex CLI:

- **Interface Layer:** Accepts developer requests through Codex CLI.
- **Orchestration Layer:** Coordinates workflows, manages stage transitions, and enforces developer approval gates (`AGENTS.md`).
- **Agent Layer (`agents/`):** Specialized engineering roles (Product Analyst, Product Reviewer, System Architect, Technical Planner, Developer, QA Engineer).
- **Skill Layer (`skills/`):** Reusable procedural knowledge and domain expertise discovered on demand.
- **Workflow Layer (`workflows/`):** Step-by-step procedures guiding complete engineering processes.
- **Template Layer (`templates/`):** Standardized markdown templates for requirements, designs, plans, tasks, and reports.
- **Configuration Layer (`config/`):** Workflow settings, defaults, and quality gates.
- **Project Context Layer:** Discovered dynamically from the target application repository.

---

## 3. Repository Organization

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

### Directory Responsibilities

| Directory | Responsibility |
|---|---|
| `config/` | Contains system-wide configuration defining workflow behaviors, default settings, and quality requirements. |
| `agents/` | Contains specialized agent definitions describing roles, responsibilities, boundaries, and expected outputs. |
| `skills/` | Contains reusable procedures and engineering knowledge, independently discoverable and loaded only when relevant. |
| `workflows/` | Defines the sequence of activities required to complete an engineering process, coordinating agents and skills. |
| `templates/` | Contains standardized document structures for engineering artifacts (requirements, designs, plans, reports). |
| `scripts/` | Contains deterministic utilities for installation, workspace validation, and other repeatable operations. |
| `docs/` | Contains system architecture, installation guides, workflows documentation, and project specifications. |

---

## 4. Implementation Milestones

Dev-Team is implemented following a sequential, milestone-based plan:

| Milestone | Title | Focus |
|---|---|---|
| **M0** | **Repository Foundation** | Git setup, core directory structure, README, LICENSE, `.gitignore` |
| **M1** | **Core Instructions & Configuration** | Root `AGENTS.md`, `workflow.yaml`, `quality-gates.yaml`, `defaults.yaml` |
| **M2** | **Product Engineering Workflow** | Product Analyst, Product Reviewer, Requirements skill & template, workflows |
| **M3** | **Project Discovery & Architecture** | Project discovery skill, System Architect agent, System Design skill & template |
| **M4** | **Technical Planning Workflow** | Technical Planner agent, Planning skill, Plan & Task templates, planning workflow |
| **M5** | **Controlled Development Workflow** | Developer agent, Flutter development skill, `implement-next` workflow |
| **M6** | **QA & Feature Validation** | QA Engineer agent, Feature Validation skill, Code Review skill, QA template |
| **M7** | **Bug Management & Status** | Bug Fixing skill, Bug Report template, `fix-bug` and `feature-status` workflows |
| **M8** | **Installation & Documentation** | Cross-platform install scripts, workspace validation, user documentation |
| **M9** | **Pilot & System Validation** | End-to-end pilot on real projects, portability validation, MVP acceptance |

---

## 5. License

This project is licensed under the [MIT License](LICENSE).
