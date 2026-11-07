# Dev-Team Contribution & Extension Guide

> **Virtual AI Software Development Team**  
> Instructions for contributing to Dev-Team, adding new specialized agents, procedural skills, workflows, and templates.

---

## 1. Guiding Principles for Contributors

When extending Dev-Team or contributing new capabilities, adhere to the core system tenets:

1. **Keep Framework Project-Agnostic:** Never commit hardcoded assumptions about specific frameworks, database schemas, or proprietary cloud providers into `dev-team`. Reusable skills must discover target conventions dynamically (`REQ-071`).
2. **Smallest Useful Solution First:** Add only what is needed. Avoid speculative architecture, complex orchestrators, or unnecessary abstraction layers.
3. **Procedural Skills Over Complex Orchestration:** Prefer self-contained skills loaded into the primary Codex CLI session over fragile inter-agent messaging pipelines.
4. **Enforce Developer Approval:** Any consequential action (requirements change, architectural shift, plan modification, destructive execution) must respect explicit approval gates (`SAFE-001` through `SAFE-004`).
5. **Deterministic Verification:** Every new agent, skill, or workflow must be validated with automated, deterministic tests and verification scripts (`REQ-072`).

---

## 2. Adding a New Specialized Agent

Agents represent specialized virtual team roles. Agent specifications reside in `agents/<agent-name>.toml`.

### 2.1 File Structure

Create `agents/<agent-name>.toml` using TOML syntax:

```toml
# Dev-Team Agent Specification: Security Auditor
# Role: Independent security and vulnerability analysis.

name = "security-auditor"
display_name = "Security Auditor"
version = "1.0"
description = "Analyzes source code, configurations, and dependencies for security flaws, credentials leaks, and OWASP vulnerabilities."

[role]
category = "Quality Assurance & Compliance"
purpose = "Perform independent security assessments on target projects without modifying production code."
primary_responsibility = "Vulnerability identification, credential audit, dependency inspection, and remediation planning."

[responsibilities]
core_tasks = [
  "Inspect target application source code for hardcoded secrets (SAFE-005).",
  "Audit dependency manifests for known CVEs.",
  "Evaluate authentication and authorization logic against requirements.",
  "Produce structured vulnerability reports with remediation steps."
]

[inputs]
required = [
  "Target repository source code and dependency manifests.",
  "Approved architecture document (system-design.md)."
]
optional = [
  "Target project security policies in AGENTS.md."
]

[outputs]
deliverables = [
  "Security audit section in qa-report.md.",
  "Vulnerability cards for identified issues."
]

[skills]
primary = [
  "skills/code-review/SKILL.md"
]
secondary = [
  "skills/project-discovery/SKILL.md"
]

[boundaries]
can = [
  "Inspect codebase, configuration files, and dependencies.",
  "Execute static analysis security scanners in read-only mode.",
  "Document security risks and recommend mitigations."
]
cannot = [
  "Cannot modify application source files directly.",
  "Cannot approve production deployment without developer sign-off.",
  "Cannot print discovered secrets or keys to terminal logs (SAFE-005)."
]

[quality_gates]
mandatory_checks = [
  "Must verify no unmasked credentials appear in reports (SAFE-005).",
  "Must provide reproduction evidence for any reported exploit."
]
```

### 2.2 Validation Checklist for Agents
- [ ] Spec uses valid TOML syntax.
- [ ] All required sections present: `name`, `display_name`, `version`, `role`, `responsibilities`, `inputs`, `outputs`, `skills`, `boundaries`, `quality_gates`.
- [ ] Negative boundaries (`cannot`) explicitly defined to prevent unauthorized actions.
- [ ] Referenced skills exist in `skills/`.

---

## 3. Adding a New Procedural Skill

Skills contain modular, repeatable procedures discovered on demand by Codex CLI. Reusable skills reside in `skills/<skill-name>/SKILL.md`.

### 3.1 File Structure

Each skill must be placed in its own directory with a `SKILL.md` file containing YAML frontmatter:

```markdown
---
name: my-new-skill
description: >-
  Reusable procedural skill for [specific task]. Activates when [trigger condition],
  such as when analyzing [X] or executing [workflow].
---

# My New Skill

## 1. Overview & Purpose
Explain what this skill accomplishes and its role in the virtual team.

## 2. When to Use
Specify concrete activation triggers and boundary conditions.

## 3. Core Principles
List the non-negotiable engineering rules governing this procedure.

## 4. Execution Procedure
Provide step-by-step guidance:
1. **Phase 1: Input Discovery:** ...
2. **Phase 2: Analysis & Execution:** ...
3. **Phase 3: Validation & Output:** ...

## 5. Safety Boundaries & Quality Gates
Detail constraints, checks, and prohibited actions.
```

### 3.2 Guidelines for Skill Authors
- **Frontmatter Name:** Must match the parent directory name exactly.
- **Trigger-Rich Description:** Provide explicit context triggers (e.g., `"Activate when diagnosing defects..."`) to enable Codex's automatic skill discovery.
- **Project Agnosticism:** Inspect project profile and conventions before suggesting framework-specific code.

---

## 4. Adding or Modifying Workflows

Workflows reside in `workflows/<workflow-name>.md` and define end-to-end multi-step procedures.

### 4.1 Workflow Structure
Every workflow document must include:
1. **Metadata Header:** Workflow ID, Entry Point, Roles, and Governing Gates.
2. **Mermaid Flowchart:** Visual representation of phase sequence and decision points.
3. **Phased Execution Sequence:** Ordered phases with clear entry and exit criteria.
4. **Escalation Protocols:** Explicit instructions for handling blockers or scope changes.

### 4.2 Registering the Workflow
Register the new workflow in `config/workflow.yaml`:

```yaml
workflows:
  my_new_workflow:
    enabled: true
    description: "Brief summary of what this workflow accomplishes"
    entry_point: "workflows/my-new-workflow.md"
```

---

## 5. Adding Standard Templates

Templates enforce consistent engineering artifacts across target projects and reside in `templates/<template-name>.md`.

### 5.1 Template Conventions
- Include a standardized YAML/Markdown metadata block at the top:
  ```markdown
  # [Document Title]

  | Field | Value |
  |---|---|
  | **Document Type** | [Requirement / Design / Plan / QA Report] |
  | **Status** | DRAFT | IN_REVIEW | APPROVED | NEEDS_REVISION |
  | **Last Updated** | YYYY-MM-DD |
  | **Approved By** | [Developer Name or Pending] |
  ```
- Use GitHub Flavored Markdown and standard alerts (`> [!NOTE]`, `> [!IMPORTANT]`, `> [!WARNING]`).

---

## 6. Adding a Platform Adapter

Dev-Team is platform-independent; platform integrations reside in `adapters/<platform-id>/`.

### 6.1 Adapter Structure
Each adapter must contain:
1. `manifest.yaml`: Declarative manifest conforming to `schemas/adapter-manifest.schema.json`.
2. `adapter.py`: Python adapter module implementing discovery path resolution, skill projection, and instruction file generation.

### 6.2 Example Manifest
```yaml
id: my-platform
name: My AI Coding Tool
version: 1.0.0
capabilities:
  agent_skills: true
  project_instructions: true
  global_skills: true
  project_skills: true
  subagents: false
  tool_execution: true

locations:
  global_skills_dir:
    windows: "$USERPROFILE/.my-platform/skills"
    unix: "~/.my-platform/skills"
  project_skills_dir: ".my-platform/skills"
  project_instructions: "INSTRUCTIONS.md"
```

---

## 7. Adding CLI Commands

Dev-Team CLI commands reside in `cli/src/commands/<command_name>.py`.
- Each command must be a modular, self-contained handler.
- Register commands in `cli/src/main.py`.
- Ensure commands operate deterministically and exit with code 0 on success.
- Never add LLM dependencies to the CLI.

---

## 8. Workspace Validation & Testing

Always validate your changes deterministically before submitting:

```bash
# 1. Run deterministic workspace validator
python scripts/validate-workspace.py --verbose

# 2. Run all milestone verification test suites
python scripts/validate_planning_artifacts.py
python scripts/validate_development_artifacts.py
python scripts/validate_qa_artifacts.py
python scripts/validate_bug_and_status_artifacts.py
python scripts/validate_installation_and_documentation_artifacts.py

# 3. Test Windows and Unix installers
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -DryRun
bash scripts/install.sh -n
```

All commands must exit with code `0`.

