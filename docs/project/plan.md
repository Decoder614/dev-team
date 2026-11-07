# Dev-Team — Implementation Plan

**Document type:** Technical Implementation Plan  
**Project:** Dev-Team  
**Repository:** `dev-team`  
**Version:** 1.1  
**Status:** Approved (v1.1 Roadmap)  
**Last updated:** 2026-11-06  
**Based on:**
- `requirements.md` — Approved v1.1
- `system-design.md` — Approved v1.1

---

# 1. Implementation Overview

## 1.1 Objective

Implement Dev-Team as a cross-platform, reusable AI-assisted software development toolkit based on the approved v1.1 architecture:
1. **Hybrid distribution:** Globally installable core skills reused across independent repositories, paired with isolated project configuration, context, and custom skills under `.dev-team/`.
2. **CLI-first installation:** A dedicated, lightweight `dev-team` CLI managing installation, initialization, updates, and diagnostics.
3. **Platform-independent core:** Agent Skills (`SKILL.md`) isolated from proprietary APIs and integrated via modular platform adapters (initial platform: OpenAI Codex CLI).
4. **Foundational project initialization:** A two-tier onboarding architecture separating deterministic CLI bootstrapping (`dev-team init`) from contextual AI project onboarding (`project-initializer`).
5. **Specification-driven engineering lifecycle:** Modular workflows guiding features from requirements through design, planning, controlled implementation, QA, and defect repair.

## 1.2 Execution Strategy

The project follows a sequenced, eight-milestone implementation roadmap:

```text
M1: Core Foundation ──► M2: CLI Foundation ──► M3: Hybrid Distribution ──► M4: Project Initializer
                                                                                    │
M8: Pilot & Refinement ◄── M7: Additional Adapters ◄── M6: Engineering Workflows ◄──┘
                                                                ▲
                                                    M5: Codex Integration
```

Execution rules:
- Implement one task at a time.
- Verify each deliverable with automated tests or deterministic checks before marking complete.
- Keep reusable logic project-agnostic.
- Enforce developer approval gates at each milestone transition.

---

# 2. Milestone Overview

| Milestone | Title | Focus & Primary Deliverable |
|---|---|---|
| **M1** | Core Foundation | Canonical repository tree, Agent Skills standard, templates suite, schemas, and policies. |
| **M2** | CLI Foundation | Dedicated `dev-team` CLI, workspace detection, global installation (`~/.dev-team/`), doctor. |
| **M3** | Hybrid Distribution | Project initialization (`dev-team init`), `.dev-team/` configuration, skill projections, updates. |
| **M4** | Project Initializer | AI onboarding skill (`project-initializer`), multi-stack classification, context generation. |
| **M5** | Codex Integration | Reference platform adapter (`adapters/codex/`), discovery paths, operating instructions. |
| **M6** | Engineering Workflows | Complete lifecycle workflows: requirements, design, planning, development, QA, and bug fixing. |
| **M7** | Additional Platform Adapters | Adapters for Claude Code, Cursor, Copilot, and Gemini / Antigravity. |
| **M8** | Pilot & System Validation | End-to-end pilot on Gotilo, cross-project verification, and workflow refinement. |

---

# 3. Milestone 1 — Core Foundation

**Objective:** Establish the canonical repository layout, core schemas, configuration standards, and template suites.

## Task M1-T01 — Canonical Repository Organization
- **Scope:** Establish the directory structure conforming to v1.1 architecture: `cli/`, `skills/`, `agents/`, `workflows/`, `templates/`, `adapters/`, `schemas/`, `config/`, and `docs/`.
- **Deliverables:** Directory tree with initial `.gitkeep` placeholders and root documentation links.
- **Validation:** Filesystem inspection script verifying all required directories exist.

## Task M1-T02 — Agent Skills Standard & Canonical Skill Directory Layout
- **Scope:** Define the Agent Skills standard (`SKILL.md` with YAML frontmatter) and establish canonical skill folders in `skills/`.
- **Deliverables:** Skill specification standard document and template `SKILL.md` format.
- **Validation:** Schema validation verifying valid YAML frontmatter across all skill definitions.

## Task M1-T03 — Standardized Templates Suite
- **Scope:** Create standard templates in `templates/` for feature deliverables (`requirement.md`, `system-design.md`, `plan.md`, `task.md`, `qa-report.md`, `bug-report.md`) and project scaffolding in `templates/project/` (`AGENTS.md`, `rules.md`, `DESIGN.md`, `overview.md`, `requirements.md`, `system-design.md`, `plan.md`, `tech-stack.md`, `architecture.md`).
- **Deliverables:** Comprehensive markdown templates in `templates/` and `templates/project/`.
- **Validation:** Markdown linting and template variable validation checks.

## Task M1-T04 — JSON Schemas for Declarative Contracts
- **Scope:** Create declarative schemas in `schemas/`:
  - `project-config.schema.json` (Validates `.dev-team/config.yaml`)
  - `adapter-manifest.schema.json` (Validates platform adapter manifests)
  - `installation-manifest.schema.json` (Validates installed artifact tracking)
- **Deliverables:** Valid JSON Schema Draft 7/2020-12 definition files in `schemas/`.
- **Validation:** Validate sample configurations against the JSON schemas.

## Task M1-T05 — Framework Policies & Quality Gates Configuration
- **Scope:** Define system-wide declarative policies in `config/`:
  - `workflow.yaml`: Workflow registry, entry points, and governing roles.
  - `quality-gates.yaml`: Mandatory checks for each lifecycle gate (`SAFE-001` to `SAFE-012`).
  - `defaults.yaml`: Standard paths, artifact statuses, and task lifecycle states.
- **Deliverables:** Valid YAML configuration files in `config/`.
- **Validation:** Parse and validate configuration syntax and integrity.

---

# 4. Milestone 2 — CLI Foundation

**Objective:** Build the core `dev-team` CLI for workspace detection, global asset installation, and diagnostics.

## Task M2-T01 — CLI Architecture & Project Setup
- **Scope:** Initialize the CLI package under `cli/` with entry point `dev-team`, argument parsing, and command routing.
- **Deliverables:** Working CLI package structure with modular command handlers (`cli/src/commands/`).
- **Validation:** CLI displays help text, version number, and command list (`dev-team --help`, `dev-team --version`).

## Task M2-T02 — Repository & Workspace Detection
- **Scope:** Implement workspace detection engine in `cli/src/detection/` capable of identifying Git repository roots, workspace types, and existing configuration.
- **Deliverables:** Detection module with unit tests for various repository structures.
- **Validation:** Execute detection unit tests on empty folders, Git repos, and nested directories.

## Task M2-T03 — Global Skill Installation Command
- **Scope:** Implement `dev-team install --global` to copy canonical skills, templates, and adapters from the source repo into the user's home directory (`~/.dev-team/`).
- **Deliverables:** Global installation command handler with platform selection flags.
- **Validation:** Run `dev-team install --global` and verify `~/.dev-team/skills/`, `templates/`, and `version` are created.

## Task M2-T04 — Installation Manifest & Provenance Engine
- **Scope:** Implement manifest tracking in `cli/src/core/` recording artifact paths, types, SHA-256 source hashes, and installation timestamps.
- **Deliverables:** Manifest generation and verification engine.
- **Validation:** Verify manifest is correctly written to `~/.dev-team/manifest.json` and hashes match source files.

## Task M2-T05 — Installation Diagnostics (`dev-team doctor`)
- **Scope:** Implement `dev-team doctor` command to inspect global installation, check filesystem permissions, verify Python/Git versions, and report platform readiness.
- **Deliverables:** Diagnostic command handler and tabular reporting.
- **Validation:** Run `dev-team doctor` in healthy and incomplete environments; observe accurate diagnostic output.

---

# 5. Milestone 3 — Hybrid Distribution

**Objective:** Implement project-level initialization, configuration management, local custom skills, and non-destructive updates.

## Task M3-T01 — Project Initialization Command (`dev-team init`)
- **Scope:** Implement `dev-team init` command to bootstrap target repositories deterministically without modifying source code.
- **Deliverables:** Project initialization command handler in `cli/src/commands/init.py`.
- **Validation:** Run `dev-team init` in a fresh test repository; verify `.dev-team/` is created cleanly.

## Task M3-T02 — Project Configuration Scaffolding (`.dev-team/config.yaml`)
- **Scope:** Scaffold `.dev-team/config.yaml` based on detected project properties and `schemas/project-config.schema.json`.
- **Deliverables:** Project configuration generator and schema validator.
- **Validation:** Verify created `config.yaml` adheres strictly to `project-config.schema.json`.

## Task M3-T03 — Skill Projection Engine
- **Scope:** Implement skill projection in `cli/src/installation/` capable of exposing global skills to platform discovery paths (`.agents/skills/` or user-level paths) using symlinks, NTFS junctions on Windows, or safe-copy fallback.
- **Deliverables:** Multi-strategy projection engine with automatic privilege fallback.
- **Validation:** Test projection on Windows with and without admin privileges; verify fallback mechanism.

## Task M3-T04 — Local Custom Skills Support & Resolution Engine
- **Scope:** Implement support for project-local skills under `.dev-team/skills/` and implement the 3-tier resolution hierarchy (Local -> Global -> Platform).
- **Deliverables:** Skill resolver module and CLI command `dev-team list --skills`.
- **Validation:** Verify local skill overrides take precedence over global skills with identical names.

## Task M3-T05 — Non-Destructive Update Engine (`dev-team update`)
- **Scope:** Implement `dev-team update` command that compares installed files against canonical source hashes and upgrades unmodified assets while preserving local customizations.
- **Deliverables:** Safe update command with `--check` dry-run mode.
- **Validation:** Simulate user edits in an installed skill, execute `dev-team update`, and confirm local edits are preserved.

## Task M3-T06 — Safe Removal Command (`dev-team uninstall`)
- **Scope:** Implement `dev-team uninstall` to cleanly remove managed artifacts recorded in `installation-manifest.json` without touching unrelated repository files.
- **Deliverables:** Uninstall command handler with confirmation prompts and `--purge` flag.
- **Validation:** Verify uninstallation leaves application code and unmanaged files intact.

---

# 6. Milestone 4 — Project Initializer Skill

**Objective:** Build the foundational AI onboarding skill that discovers repository context, conducts adaptive interviews, and scaffolds documentation.

## Task M4-T01 — Project Initializer Skill Specification
- **Scope:** Create `skills/project-initializer/SKILL.md` defining triggers, activation rules, and onboarding procedures conforming to the Agent Skills standard.
- **Deliverables:** Canonical `SKILL.md` with complete reference documentation.
- **Validation:** Validate skill metadata and frontmatter parsing.

## Task M4-T02 — Multi-Stack Inspection & Classification Engine
- **Scope:** Implement detection scripts and procedures in `skills/project-initializer/` to classify repositories as `EXISTING`, `EMPTY`, or `PARTIAL`, extracting tech stacks (Flutter, Node, Python, Java, etc.) without guessing.
- **Deliverables:** Structural analysis script (`scripts/check-project-structure.py`) and reference guides.
- **Validation:** Run structural inspection across sample repositories (empty, Flutter, Node.js).

## Task M4-T03 — Adaptive Onboarding Interview Protocol
- **Scope:** Define the structured, adaptive interview process for empty or partially initialized repositories, ensuring no speculative architecture is invented.
- **Deliverables:** Interview protocol reference documentation (`references/context-gathering.md`).
- **Validation:** Verify questions adapt to confirmed facts and skip already-known properties.

## Task M4-T04 — Context Validation & Developer Confirmation Gate
- **Scope:** Implement validation procedures presenting discovered facts, active assumptions, and open questions to the developer for explicit approval before file creation.
- **Deliverables:** Confirmation gate procedure enforcing `SAFE-001`, `SAFE-002`, and `SAFE-012`.
- **Validation:** Simulate approval workflow; verify execution halts if developer rejects proposed context.

## Task M4-T05 — Project Documentation Generator
- **Scope:** Implement template instantiation generating `AGENTS.md`, `rules.md`, `DESIGN.md` (if applicable), and baseline project documentation in `docs/project/`.
- **Deliverables:** Scaffolding generation logic with conflict detection for existing files.
- **Validation:** Verify generated files maintain cross-document consistency and do not overwrite existing files without signoff.

## Task M4-T06 — Canonical Context Store & Initialization Audit Report
- **Scope:** Generate `.dev-team/project-context.md` (partitioning `CONFIRMED_FACTS` vs `ACTIVE_ASSUMPTIONS`) and `.dev-team/initialization-report.md`.
- **Deliverables:** Central context file generator and initialization audit reporting.
- **Validation:** Inspect generated `project-context.md` and verify downstream skills can consume it directly.

---

# 7. Milestone 5 — OpenAI Codex Platform Adapter

**Objective:** Implement the initial reference platform adapter integrating Dev-Team with OpenAI Codex CLI.

## Task M5-T01 — Codex Adapter Manifest & Configuration
- **Scope:** Create `adapters/codex/manifest.yaml` declaring capabilities, discovery paths (`~/.codex/skills/`, `.agents/skills/`), and root instruction integration (`AGENTS.md`).
- **Deliverables:** Declarative manifest conforming to `schemas/adapter-manifest.schema.json`.
- **Validation:** Manifest schema validation.

## Task M5-T02 — Codex Skill Discovery Mapping
- **Scope:** Implement discovery mapping linking canonical skills into Codex user-level and repository-level skill directories.
- **Deliverables:** Adapter execution logic in `adapters/codex/adapter.py`.
- **Validation:** Verify Codex CLI discovers skills via `codex skills list` or standard discovery.

## Task M5-T03 — Operating Instructions Integration
- **Scope:** Configure root `AGENTS.md` instructions tailored for Codex orchestration, defining role boundaries, workflow triggers, and approval gates.
- **Deliverables:** Codex-optimized root operating instructions.
- **Validation:** Verify Codex session adheres to operating boundaries in `AGENTS.md`.

## Task M5-T04 — Declarative Role Specifications Mapping
- **Scope:** Map Dev-Team specialized roles (`agents/*.toml`) into Codex execution instructions.
- **Deliverables:** Validated TOML role specifications in `agents/`.
- **Validation:** Verify all 6 roles (Analyst, Reviewer, Architect, Planner, Developer, QA) have valid TOML specifications.

## Task M5-T05 — End-to-End Codex Discovery & Execution Test
- **Scope:** Test end-to-end skill discovery and workflow execution using OpenAI Codex CLI in a clean workspace.
- **Deliverables:** Verification log demonstrating successful skill discovery and execution.
- **Validation:** Run `/project-initializer` under Codex and observe successful execution.

---

# 8. Milestone 6 — Engineering Workflows

**Objective:** Implement the complete six-stage engineering lifecycle workflows, specialized skills, and approval gates.

## Task M6-T01 — Product Requirements Workflow (`new-feature`)
- **Scope:** Implement `workflows/new-feature.md` and `skills/product-requirements/SKILL.md` (Product Analyst role).
- **Deliverables:** Idea-to-requirements workflow and skill generating `.dev-team/features/<f>/requirement.md`.
- **Validation:** Convert sample feature idea into structured requirement document.

## Task M6-T02 — Requirement Validation Workflow (`validate-requirement`)
- **Scope:** Implement `workflows/validate-requirement.md` and `skills/requirement-validation/SKILL.md` (Product Reviewer role).
- **Deliverables:** Adversarial audit workflow identifying ambiguities, omissions, and testability gaps.
- **Validation:** Run audit on incomplete requirement; verify gaps are surfaced and `SAFE-001` gate is enforced.

## Task M6-T03 — Feature Discovery & System Design Workflow (`design-feature`)
- **Scope:** Implement `workflows/design-feature.md`, `skills/system-design/SKILL.md`, and `skills/project-discovery/SKILL.md` (System Architect role).
- **Deliverables:** Architecture workflow generating `system-design.md` and schema/UX specs.
- **Validation:** Generate technical design conforming to target repository patterns and enforce `SAFE-002`.

## Task M6-T04 — Technical Planning Workflow (`create-plan`)
- **Scope:** Implement `workflows/create-plan.md` and `skills/technical-planning/SKILL.md` (Technical Planner role).
- **Deliverables:** Task decomposition workflow generating sequenced `plan.md` mapped to requirement IDs.
- **Validation:** Generate task plan with acceptance criteria, validation steps, and enforce `SAFE-003`.

## Task M6-T05 — Controlled Implementation Workflow (`implement-next`)
- **Scope:** Implement `workflows/implement-next.md` and `skills/flutter-development/SKILL.md` (Developer role).
- **Deliverables:** Single-task implementation workflow with pre-task git check and automated verification.
- **Validation:** Execute one task; observe code modifications, test execution, and evidence recording.

## Task M6-T06 — Code Review & Feature Validation Workflow (`validate-feature`)
- **Scope:** Implement `workflows/validate-feature.md`, `skills/code-review/SKILL.md`, and `skills/feature-validation/SKILL.md` (QA Engineer role).
- **Deliverables:** Independent verification workflow generating `qa-report.md`.
- **Validation:** Validate completed feature against requirement acceptance criteria; report pass/fail.

## Task M6-T07 — Defect Diagnosis & Bug-Fixing Workflow (`fix-bug`)
- **Scope:** Implement `workflows/fix-bug.md` and `skills/bug-fixing/SKILL.md`.
- **Deliverables:** Controlled bug reproduction, minimal fix, and regression testing workflow.
- **Validation:** Reproduce defect deterministically before applying fix and verify regression test passes.

## Task M6-T08 — Feature Status Reporting (`feature-status`)
- **Scope:** Implement `workflows/feature-status.md` for zero-hallucination progress auditing.
- **Deliverables:** Status reporting procedure inspecting on-disk artifacts.
- **Validation:** Verify status accurately reflects actual task states without optimistic fabrication.

---

# 9. Milestone 7 — Additional Platform Adapters

**Objective:** Implement modular platform adapters extending Dev-Team beyond Codex.

## Task M7-T01 — Claude Code Platform Adapter
- **Scope:** Implement `adapters/claude-code/` manifest and discovery mapping for Anthropic Claude Code (`CLAUDE.md`, `~/.claude/skills/`).
- **Deliverables:** Claude Code adapter manifest and integration script.
- **Validation:** Verify skill discovery and instruction reading under Claude Code.

## Task M7-T02 — Cursor Platform Adapter
- **Scope:** Implement `adapters/cursor/` manifest and discovery mapping for Cursor IDE (`.cursorrules`, `.cursor/skills/`).
- **Deliverables:** Cursor adapter manifest and integration script.
- **Validation:** Verify Cursor rule loading and skill accessibility.

## Task M7-T03 — GitHub Copilot Platform Adapter
- **Scope:** Implement `adapters/copilot/` manifest and discovery mapping for GitHub Copilot (`.github/copilot-instructions.md`).
- **Deliverables:** Copilot adapter manifest and integration script.
- **Validation:** Verify instruction generation and skill linking.

## Task M7-T04 — Gemini / Antigravity Platform Adapter
- **Scope:** Implement `adapters/gemini/` manifest and discovery mapping for Google Antigravity / Gemini CLI (`.gemini/antigravity/skills/`).
- **Deliverables:** Gemini adapter manifest and integration script.
- **Validation:** Verify skill registration and execution.

---

# 10. Milestone 8 — Pilot, System Validation & Refinement

**Objective:** Validate Dev-Team on real-world application codebases and refine based on observed results.

## Task M8-T01 — Pilot Environment Setup in Gotilo Repository
- **Scope:** Execute `dev-team init --platform codex --mode hybrid` in the Gotilo repository, followed by `/project-initializer`.
- **Deliverables:** Initialized Gotilo workspace with `.dev-team/` configuration and verified context.
- **Validation:** Confirm Gotilo source code is untouched and `.dev-team/project-context.md` accurately reflects its Flutter/Supabase architecture.

## Task M8-T02 — End-to-End Pilot Feature Execution
- **Scope:** Execute the complete lifecycle (idea -> requirements -> design -> plan -> implementation -> QA) for Gotilo's Property Rating & Review feature.
- **Deliverables:** Complete feature artifacts (`requirement.md`, `system-design.md`, `plan.md`, `qa-report.md`) and implemented feature code.
- **Validation:** Verify all approval gates were respected and all acceptance criteria pass.

## Task M8-T03 — Secondary Project Validation (Cross-Project Reuse)
- **Scope:** Initialize a second independent repository (e.g. a Node.js or Python CLI project) using the same global Dev-Team installation.
- **Deliverables:** Verification report demonstrating cross-project reuse without context leakage.
- **Validation:** Verify second project consumes global skills with its own isolated `.dev-team/` context.

## Task M8-T04 — Final Refinement & Documentation Polish
- **Scope:** Review friction logs, address observed workflow gaps, refine prompts, and update all user documentation.
- **Deliverables:** Finalized documentation, release tag v1.1.0, and updated README.
- **Validation:** Clean pass of `dev-team doctor` and workspace validation across platforms.
