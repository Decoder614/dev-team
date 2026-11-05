# Workflow: Create Plan (Implementation Planning)

**Workflow ID:** `create_plan`  
**Entry Point:** `workflows/create-plan.md`  
**Primary Roles:** Technical Planner, Plan Reviewer, Developer (Approver)  
**Applicable Skills:**  
- `skills/project-discovery/SKILL.md`  
- `skills/technical-planning/SKILL.md`  
**Governing Gate:** Planning Gate (`config/quality-gates.yaml`)  

---

## 1. Purpose & Overview

The `create_plan` workflow governs the technical planning phase of feature engineering. It transforms approved feature requirements (`requirement.md`) and architectural specifications (`system-design.md`) into an approved, cohesive, and actionable implementation plan (`plan.md`).

This workflow ensures that implementation work is broken down into small, bite-sized tasks organized into logical milestones, each with explicit dependencies, concrete file targets, unambiguous acceptance criteria, and deterministic validation commands. By securing explicit developer approval before implementation begins, it prevents scope creep, uncoordinated refactoring, and untraceable modifications.

---

## 2. Prerequisites & Entry Conditions

1. **Trigger:**
   - Follows successful completion of the `feature_design` workflow (`workflows/design-feature.md`).
   - Developer requests implementation planning for a feature (e.g., *"create the implementation plan for property reviews"* or *"break down the plan for auth"*).
2. **Approved Requirements Check (Mandatory Precondition):**
   - The target feature directory `.dev-team/features/<feature-slug>/` must contain an approved `requirement.md`.
   - Verify that `requirement.md` has status `APPROVED` (per `SAFE-001` and `REQ-GATE-4`).
   - If missing, draft, or pending approval, **halt execution** and notify developer that requirements sign-off is required.
3. **Approved Architecture Check (Mandatory Precondition):**
   - The target feature directory `.dev-team/features/<feature-slug>/` must contain an approved `system-design.md`.
   - Verify that `system-design.md` has status `APPROVED` (per `SAFE-002` and `ARCH-GATE-3`).
   - If missing, draft, or pending approval, **halt execution** and notify developer that architecture sign-off is required.
4. **Collision & Revision Check:**
   - Inspect `.dev-team/features/<feature-slug>/plan.md`.
   - If an approved `plan.md` already exists, **do not overwrite it silently** (`SAFE-004`, `SAFE-006`). Ask the developer whether to create a revision, replan, or cancel.

---

## 3. Quality Gates Enforced

Per `config/quality-gates.yaml` and system safety boundaries:
- [x] **PLAN-GATE-1 (Traceability):** Every task must map to at least one approved requirement ID (`require_traceability_to_requirements: true`, `REQ-027`).
- [x] **PLAN-GATE-2 (Independent & Verifiable):** Tasks must be small, focused, and verifiable with deterministic commands (`require_independent_verifiable_tasks: true`, `REQ-024`, `REQ-025`).
- [x] **PLAN-GATE-3 (Developer Plan Approval):** Developer must explicitly approve the plan before implementation begins (`require_developer_plan_approval: true`, `SAFE-003`, `REQ-029`).
- [x] **PLAN-GATE-4 (Explicit Task Dependencies):** All task dependencies must be recorded; sequential and independent tasks must be distinguished (`require_explicit_task_dependencies: true`, `REQ-026`).
- [x] **PLAN-GATE-5 (Plan Review Audit):** Independent audit must verify coverage, dependencies, ordering, scope, risk, and testability (`REQ-028`).

---

## 4. Execution Sequence

```mermaid
flowchart TD
    A[Start: Request Implementation Plan] --> B[Phase 1: Ingest Approved Requirements & Design]
    B --> C{Both requirement.md & system-design.md APPROVED?}
    C -->|No| D[Halt: Request Prerequisite Approvals]
    C -->|Yes| E[Phase 2: Context Alignment & Validation Discovery]
    E --> F[Phase 3: Milestone & Task Decomposition (Technical Planner)]
    F --> G[Phase 4: Dependency Graph & Execution Order Mapping]
    G --> H[Phase 5: Plan Review Audit (Plan Reviewer / REQ-028)]
    H --> I{Review Passed?}
    I -->|Defects Found| F
    I -->|Passed| J[Phase 6: Developer Plan Approval Gate (SAFE-003)]
    J --> K{Developer Decision?}
    K -->|Revisions Requested| F
    K -->|Approved| L[Phase 7: Baseline as APPROVED]
    L --> M[Next: Implement Next Task Workflow]
```

### Phase 1: Ingest Approved Requirements & Design
1. Resolve the feature directory and target artifact paths:
   - Feature directory: `.dev-team/features/<feature-slug>/`
   - Requirements: `.dev-team/features/<feature-slug>/requirement.md`
   - Design: `.dev-team/features/<feature-slug>/system-design.md`
   - Plan destination: `.dev-team/features/<feature-slug>/plan.md`
2. Verify document statuses:
   - `requirement.md` must be `APPROVED`.
   - `system-design.md` must be `APPROVED`.
3. If either document is missing or not approved, halt and inform the developer immediately.

### Phase 2: Context Alignment & Validation Discovery
*Activate `skills/project-discovery/SKILL.md`.*
1. Inspect project profile (`.dev-team/project-profile.yaml`) and target repository `AGENTS.md`.
2. Discover deterministic validation commands:
   - Static analysis / linter command (e.g. `flutter analyze`, `npm run lint`).
   - Unit and integration test command (e.g. `flutter test test/...`, `pytest`).
   - Code generation / migration command (e.g. `dart run build_runner build`, `npx prisma migrate`).
3. Identify existing test conventions and source directories.

### Phase 3: Milestone & Task Decomposition (Technical Planner)
*Activate `skills/technical-planning/SKILL.md` (Technical Planner role).*
1. **Deconstruct Scope:** Ingest all `REQ-xxx` IDs, non-functional requirements, and architectural components (schemas, entities, repositories, state controllers, UI widgets).
2. **Define Milestones:** Establish logical milestones ordered by dependency (e.g. Data Foundation → State & Business Logic → Presentation → Integration & Validation).
3. **Formulate Tasks:** Slice work into granular tasks (`M<m>-T<nn>`):
   - Clear objective and scope.
   - Requirements covered (`REQ-xxx`).
   - Exact files to create, modify, or inspect.
   - Specific deliverables.
   - Testable acceptance criteria.
   - Deterministic validation commands and expected outputs.
4. **Task Granularity Decision:**
   - Standard features: Store all tasks directly in `plan.md`.
   - Complex features (10+ tasks): In addition to `plan.md`, generate discrete task cards in `.dev-team/features/<feature-slug>/tasks/` conforming to `templates/task.md`.

### Phase 4: Dependency Graph & Execution Sequencing
1. Map task prerequisites and verify the dependency graph is acyclic (no circular dependencies).
2. Identify tasks that are strictly sequential versus tasks that can be performed independently (REQ-026).
3. Generate the Mermaid flowchart depicting the task execution DAG.
4. Establish the Requirement Traceability Matrix connecting each `REQ-xxx` to its implementing tasks.

### Phase 5: Plan Review Audit (Plan Reviewer / REQ-028)
Audit the drafted plan across the six critical dimensions:
1. **Coverage:** Every `REQ-xxx` maps to at least one task.
2. **Dependencies:** Prerequisites are complete, valid, and non-circular.
3. **Ordering:** Sequence respects architectural layering (data before state, state before UI).
4. **Scope:** No extraneous tasks or speculative features outside approved requirements and design.
5. **Risk:** High-risk tasks (database migrations, auth modifications) are isolated with specific rollback/verification plans.
6. **Testability:** Every task includes concrete test commands and observable pass criteria.

If issues are found, update the plan. When satisfied, record the audit summary in Section 7.1 of `plan.md`.

### Phase 6: Developer Plan Approval Gate (Mandatory)
*Enforces `SAFE-003` and `REQ-029`.*
1. Present the plan overview to the developer:
   - Summary of milestones and task counts.
   - Requirement coverage confirmation.
   - Plan review audit determination.
   - Link to `.dev-team/features/<feature-slug>/plan.md`.
2. Explicitly request developer review and sign-off:
   > *"The implementation plan for `[feature-slug]` has been prepared with [N] tasks across [M] milestones and passed review. Please review `.dev-team/features/<feature-slug>/plan.md` and confirm your approval before we proceed to implementation."*
3. **Wait for developer decision.**
   - If revisions requested: incorporate feedback (return to Phase 3).
   - If approved: proceed to Phase 7.

### Phase 7: Baseline & Transition
1. Update `plan.md` header metadata:
   - Set `Status:` to `APPROVED`.
   - Set `Last Updated:` and record developer approver name and approval timestamp.
2. Transition to controlled implementation:
   - Next active workflow: `workflows/implement-next.md`.
   - First task ready for execution: `M1-T01`.

---

## 5. Scope Change & Replanning Protocol (REQ-030)

If implementation of any task reveals unforeseen architectural discrepancies, unstated requirements, or broken assumptions:
1. **Pause Task:** Set active task status to `BLOCKED`. Do not proceed with subsequent tasks.
2. **Identify Impact:** Assess if changes require updates to `requirement.md`, `system-design.md`, or solely `plan.md`.
3. **Escalate to Developer:** Present findings and propose adjustments (SAFE-008, SAFE-012).
4. **Re-Approval:** Update artifacts, obtain developer sign-off on the updated plan, and resume controlled implementation.

---

## 6. Artifact Lifecycle

```text
Drafted plan.md (Status: DRAFT)
       |
       v
Plan Review Audit (REQ-028)
       |
       v
Developer Approval Gate (SAFE-003, REQ-029)
       |
       v
Approved Implementation Plan (Status: APPROVED)
       |
       v
Controlled Implementation (workflows/implement-next.md)
```

