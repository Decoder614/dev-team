---
name: [skill-name]
description: >-
  [Comprehensive description of this procedural skill. Include explicit activation
  triggers, e.g. "Activate when [trigger condition] to [action/purpose]. Used by [Role]."]
---

# [Skill Display Name]

> **Role:** [Governing Role, e.g. Developer / QA Engineer / System Architect]  
> **Lifecycle Gate:** [Governing Quality Gate, e.g. Implementation Gate]  
> **Traceability:** [Relevant Requirements and Architectural References]

---

## 1. Overview & Purpose

[Describe what this skill accomplishes, its place in the virtual AI software engineering team, and why this procedure exists.]

---

## 2. When to Use & Activation Triggers

Activate this skill when:
- **Trigger 1:** [Specific developer request, workflow phase, or slash command]
- **Trigger 2:** [Specific condition detected in workspace or target project]
- **Trigger 3:** [Prerequisite artifact is approved and next step begins]

Do NOT use this skill when:
- [Boundary condition where another skill or manual developer action is appropriate]

---

## 3. Required Inputs & Context

Before executing this skill, ensure the following inputs are available and inspected:
1. **Target Project Context:** Read `.dev-team/project-context.md` (or run project discovery if missing).
2. **Prerequisite Deliverable:** [e.g. Approved requirement.md, approved system-design.md, or active task.md].
3. **Working Tree State:** Inspect git status to ensure no uncommitted developer work is at risk.

---

## 4. Core Principles & Boundaries

1. **Smallest Useful Solution First:** [Implement minimal, maintainable logic; avoid speculative complexity].
2. **Follow Approved Context:** [Respect patterns established in the target codebase and project context].
3. **Evidence Over Assumptions:** [Verify observable outputs before claiming completion (SAFE-009)].
4. **Preserve User Changes:** [Never overwrite unrelated uncommitted files (SAFE-010)].

---

## 5. Phased Execution Procedure

### Phase 1: Context & Input Ingestion
1. Inspect required inputs and verify entry gates.
2. Formulate execution plan aligned with governing constraints.

### Phase 2: Core Execution & Transformation
1. Perform the procedural actions step-by-step.
2. Maintain adherence to target project conventions.

### Phase 3: Verification & Concrete Evidence
1. Execute deterministic checks (tests, linters, structural validators).
2. Observe and record actual command output as evidence.

### Phase 4: Output Scaffolding & State Update
1. Update target artifact or deliverable file.
2. Record transition in task log or audit report.

---

## 6. Safety Boundaries & Quality Gates

### Mandatory Safety Boundaries
- **SAFE-001 / SAFE-002 / SAFE-003:** Respect developer approval gates before proceeding across phases.
- **SAFE-005:** Never output, commit, or log credentials, secrets, or API keys.
- **SAFE-006:** Do not run destructive filesystem or git commands without explicit authorization.
- **SAFE-009:** Never claim success without executing verification commands and observing tangible output.
- **SAFE-012:** If required information is missing, halt and ask for clarification rather than guessing.

### Exit Criteria
- [ ] All procedural steps executed deterministically.
- [ ] Verification commands passed with observed output.
- [ ] Deliverable conforms to approved template format.
- [ ] Working tree left clean and ready for developer inspection.

