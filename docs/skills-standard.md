# Agent Skills Standard Specification

> **Dev-Team Specification: Agent Skills Format & Canonical Layout**  
> Version: 1.1  
> Status: Approved Standard  
> Scope: Platform-independent procedural skills for AI coding agents (`skills/*/SKILL.md`).

---

## 1. Overview & Purpose

Dev-Team Agent Skills provide modular, reusable, procedural engineering instructions that AI coding assistants discover and execute on demand.

To ensure long-term portability and avoid platform lock-in (`REQ-020`, `REQ-084`, `ADR-003`), Dev-Team standardizes on the open **Agent Skills specification**:
1. **Self-Contained Instruction Packages:** Each skill resides in a standalone folder named after the skill.
2. **Deterministic Discovery Metadata:** Standardized YAML frontmatter enclosed in `---` lines at the top of `SKILL.md`.
3. **Platform Independence:** Core procedural instructions are written in standard Markdown and do not rely on proprietary AI tool wrappers or private model formats. Platform adapters (`adapters/`) handle projection into tool-specific locations.
4. **Separation of Procedural Knowledge from Project Context:** Reusable engineering techniques remain generic; project-specific conventions are inspected dynamically from `.dev-team/project-context.md` or repository files.

---

## 2. Directory Layout & Organization

### 2.1 Skill Directory Structure

Every canonical skill in `skills/` or target repository custom skill in `.dev-team/skills/` must follow this structure:

```text
skills/<skill-name>/
├── SKILL.md                 # Primary procedural instruction file (REQUIRED)
├── references/              # Detailed background guides, checklists, or reference docs (OPTIONAL)
│   ├── context-gathering.md
│   └── project-detection.md
├── resources/               # Templates or artifact skeletons bundled with this skill (OPTIONAL)
│   └── sample-output.md
└── scripts/                 # Deterministic helper scripts supporting the skill (OPTIONAL)
    └── check-structure.py
```

### 2.2 Canonical Skills Registry

The Dev-Team core repository includes 10 canonical skills:

| Skill Directory | Governing Role | Primary Activation Trigger |
|---|---|---|
| `skills/project-initializer/` | Initializer / Architect | Repository onboarding, greenfield bootstrapping, or framework classification. |
| `skills/product-requirements/` | Product Analyst | Drafting new feature requirements, user stories, and acceptance criteria. |
| `skills/requirement-validation/` | Product Reviewer | Auditing requirements for completeness, ambiguity, and testability. |
| `skills/project-discovery/` | System Architect | Extracting target repository conventions, tech stack, and structure. |
| `skills/system-design/` | System Architect | Architectural design, module boundaries, data models, and API contracts. |
| `skills/technical-planning/` | Technical Planner | Decomposing designs into sequenced, verifiable, single-task implementation plans. |
| `skills/flutter-development/` | Developer | Implementing Dart/Flutter features following clean architecture conventions. |
| `skills/code-review/` | QA Engineer | Multi-dimensional static review (correctness, security, style, performance). |
| `skills/feature-validation/` | QA Engineer | Independent end-to-end verification and QA report compilation against acceptance criteria. |
| `skills/bug-fixing/` | Developer / QA | Reproducing defects deterministically, surgical fixing, and regression testing. |

---

## 3. Frontmatter Specification

Every `SKILL.md` must begin with a YAML frontmatter block demarcated by triple dashes (`---`).

### 3.1 Frontmatter Schema

```yaml
---
name: <kebab-case-name>
description: >-
  <Comprehensive multi-sentence description including clear activation triggers,
  contexts of use, target technologies, and what problem it solves.>
---
```

### 3.2 Required Fields

| Field | Type | Rules & Validation Constraints |
|---|---|---|
| `name` | `string` | **Mandatory.** Must strictly match the parent directory name. Must use lowercase alphanumeric characters and hyphens (`^[a-z0-9]+(-[a-z0-9]+)*$`). |
| `description` | `string` | **Mandatory.** Must be at least 20 characters long. Must provide clear activation triggers (e.g. "Activate when...", "Used by [Role] to...") so that AI platforms can index and match user intent. |

---

## 4. Markdown Body Structure

The body of `SKILL.md` must follow a standardized, six-section template:

```markdown
# [Skill Title]

## 1. Overview & Purpose
High-level summary of what the skill accomplishes, which virtual team role executes it, and its place in the lifecycle.

## 2. When to Use & Activation Triggers
Explicit bullet points detailing when the primary session or agent should activate this skill.

## 3. Required Inputs & Context
Prerequisites, files to read, and developer sign-offs required prior to execution.

## 4. Core Principles & Non-Negotiable Rules
Key engineering principles governing this procedure (e.g. smallest useful change, evidence over assumptions).

## 5. Phased Execution Procedure
Step-by-step phased instructions:
- **Phase 1: Discovery & Input Validation**
- **Phase 2: Execution & Transformation**
- **Phase 3: Verification & Concrete Evidence**
- **Phase 4: Output Scaffolding & Logging**

## 6. Safety Boundaries & Quality Gates
Explicit safety boundaries (`SAFE-001` through `SAFE-012`), prohibited actions, and mandatory gates.
```

---

## 5. Skill Resolution Hierarchy

When an agent or workflow requires a skill, Dev-Team resolves the skill via a 3-tier hierarchy:

1. **Priority 1 (Project-Local):** `.dev-team/skills/<skill-name>/SKILL.md`  
   Overrides global definitions to specialize project behaviors (e.g. specialized framework linters, custom DB tools).
2. **Priority 2 (Global Dev-Team):** `~/.dev-team/skills/<skill-name>/SKILL.md`  
   The canonical shared engineering skills reused across projects.
3. **Priority 3 (Platform Discovery):** Native or bundled platform skills.

> **Safety Invariant:** Local skill overrides must never disable or bypass system safety boundaries (`SAFE-001` through `SAFE-012`).

---

## 6. Authoring Checklist & Verification

When creating or modifying an Agent Skill:
- [ ] Directory is created under `skills/<skill-name>/` (or `.dev-team/skills/<skill-name>/`).
- [ ] `SKILL.md` starts with valid YAML frontmatter delimiter `---`.
- [ ] `name` field exactly matches `<skill-name>`.
- [ ] `description` clearly explains triggers, roles, and purpose.
- [ ] Contains all 6 standard structural sections.
- [ ] Contains no platform-proprietary wrappers or hardcoded developer-specific local paths.
- [ ] Validated with `scripts/validate-workspace.py` and `scripts/validate_milestone_1.py`.

