---
name: technical-planning
description: >-
  Reusable procedural skill for decomposing approved feature requirements (requirement.md)
  and architecture designs (system-design.md) into structured, sequenced, and verifiable
  implementation plans (plan.md) and task specifications (task.md). Establishes milestones,
  dependency graphs, acceptance criteria, deterministic validation commands, and conducts
  plan quality reviews before seeking developer approval. Activate when creating an implementation
  plan, breaking down a feature into tasks, or executing the create-plan workflow.
---

# Technical Planning Skill

## 1. Overview & Purpose

This skill defines the standardized procedure for translating approved requirements (`requirement.md`) and system designs (`system-design.md`) into a structured, actionable, and verifiable implementation plan (`plan.md`) (REQ-022), accompanied by modular task specifications (`task.md`) when feature complexity justifies them.

The primary objective is to enable **controlled, one-task-at-a-time implementation** (M5). By breaking work down into bite-sized, logically sequenced units with explicit dependencies and deterministic validation criteria, developers and AI agents can execute each task safely without losing context, introducing scope creep, or breaking existing codebase conventions.

---

## 2. When to Use

Activate this skill when:
- Approved `requirement.md` and `system-design.md` documents exist for a feature.
- The `create_plan` workflow (`workflows/create-plan.md`) is executed.
- The developer asks to plan, decompose, or schedule implementation for a feature (e.g., *"create the implementation plan for property reviews"* or *"break this design down into tasks"*).
- Implementation reveals an unforeseen architectural gap or scope change requiring formal replanning (REQ-030).

---

## 3. Required Inputs

1. **Approved Requirement Document:** Path to `.dev-team/features/<feature-name>/requirement.md` (must have status `APPROVED` per `SAFE-001`).
2. **Approved System Design Document:** Path to `.dev-team/features/<feature-name>/system-design.md` (must have status `APPROVED` per `SAFE-002`).
3. **Project Context & Profile:**
   - `.dev-team/project-profile.yaml` (discovered commands, conventions, test runners, directories).
   - Target project `AGENTS.md` for coding conventions and task constraints.
   - Codebase inspection to verify existing test suites, linter scripts, and directory structures.
4. **Existing Plan (if replanning):** Previous `plan.md` to update or supersede.

---

## 4. Core Principles of Technical Planning

1. **Smallest Useful Tasks First:** Slicing should produce tasks that can be implemented and validated in a single focused session. Avoid omnibus or vague tasks.
2. **Deterministic Verification:** Every task must specify exact validation commands (e.g. `flutter test test/...`, `dart run build_runner build`, `npm test`) with tangible expected output. Never assume completion without observable evidence (SAFE-009).
3. **Bidirectional Traceability:** Every task must reference one or more `REQ-xxx` IDs and specific architectural components from `system-design.md` (REQ-027).
4. **Explicit Dependency Graph (DAG):** Preconditions and task prerequisites must be unambiguous. Identify tasks that must execute sequentially versus tasks that can be performed independently (REQ-026).
5. **No Scope Creep:** The plan must strictly implement the approved design. If a missing capability or discrepancy is discovered, pause and ask the developer (SAFE-004, REQ-030).
6. **Explicit Plan Approval Gate:** No implementation code may be written until the developer explicitly approves the plan (SAFE-003, REQ-029).

---

## 5. Execution Procedure

Follow these sequential steps to produce an approved implementation plan:

### Step 1: Ingest Preconditions & Verify Approval Gates
1. Read `.dev-team/features/<feature-name>/requirement.md` and check:
   - Status is `APPROVED`.
   - Stable requirement identifiers (`REQ-001`, `REQ-002`, ...) are present.
2. Read `.dev-team/features/<feature-name>/system-design.md` and check:
   - Status is `APPROVED`.
   - Architectural components, data models, and ADRs are documented.
3. **Safety Check:** If either document is missing, in draft, or awaiting review, **HALT** immediately. Inform the developer that prerequisite approvals are required (`SAFE-001`, `SAFE-002`).

### Step 2: Extract Requirement & Architecture Inventory
Construct an internal inventory of items to be implemented:
- **Functional Requirements:** Every atomic `REQ-xxx` to be fulfilled.
- **Non-Functional Requirements:** `NFR-xxx` for performance, caching, security, error handling.
- **Architectural Deliverables:**
  - Database tables, migrations, RLS policies (from design Section 4).
  - Domain entities, models, DTOs, JSON serializers (Section 3).
  - Repositories, data sources, API clients (Section 3).
  - Business logic, state controllers, Blocs, Notifiers (Section 3).
  - UI screens, widgets, form validation, error states, empty states (Section 3).
  - Unit, widget, and integration test suites (Section 8).

### Step 3: Discover Validation Commands & Testing Conventions
1. Inspect `.dev-team/project-profile.yaml` and repository root for test runners:
   - Flutter: `flutter analyze`, `flutter test test/path/to/test.dart`, `dart run build_runner build --delete-conflicting-outputs`
   - Node/TypeScript: `npm run lint`, `npm test -- path/to/test.spec.ts`
   - Python: `pytest tests/path/to/test.py`, `ruff check`
2. Identify target file paths conforming to project convention (e.g. `lib/features/<name>/...` vs `lib/domain/...`).

### Step 4: Milestone Decomposition
Group tasks into logical, cohesive milestones. Milestones should typically follow a bottom-up or layer-by-layer dependency sequence:
- **Milestone 1 — Data & Persistence Foundation:** Schemas, migrations, domain models/entities, serialization, data sources, repositories.
- **Milestone 2 — State Management & Business Logic:** Use cases, service classes, Blocs/Notifiers/Controllers, state transitions, state unit tests.
- **Milestone 3 — Presentation & UI Components:** Reusable widgets, screens, routing, form validation, error/loading/empty states, widget tests.
- **Milestone 4 — Feature Integration & End-to-End Validation:** Full workflow integration, mock backend verification, integration tests, QA readiness.

*Note:* For small features (e.g., minor UI fix or isolated utility), 1 or 2 concise milestones are sufficient. Do not force unnecessary milestones on simple tasks.

### Step 5: Task Slicing & Formulation (REQ-023, REQ-024, REQ-025)
For each milestone, define atomic implementation tasks with the identifier format `M<milestone_number>-T<task_number>` (e.g., `M1-T01`, `M1-T02`).

Each task must include (REQ-024):
- **Task ID & Title:** Clear, action-oriented name (e.g., `M1-T01: Create Property Review data model and serialization`).
- **Objective:** What problem this task solves in 1-2 concise sentences.
- **Requirements Covered:** Specific `REQ-xxx` IDs satisfied by this task (REQ-027).
- **Dependencies:** List of prerequisite Task IDs that must complete first.
- **Execution Mode:** `Sequential` (must follow dependency) or `Independent` (can run in parallel if multiple sessions/agents exist) (REQ-026).
- **Scope & Expected Files:**
  - Files to create (with exact relative paths).
  - Files to modify.
  - Files to inspect.
- **Deliverables:** Tangible artifacts produced upon task completion.
- **Acceptance Criteria:** Verifiable bulleted checklist defining "done".
- **Validation Procedure:** Exact shell command(s) and observable passing output (REQ-025).
- **Initial Status:** `PENDING`.

### Step 6: Identify Dependency Graph & Execution Order
1. Build the Directed Acyclic Graph (DAG) of task dependencies.
2. Verify there are **no circular dependencies**.
3. Clearly mark tasks that are strictly sequential versus tasks that can be performed in parallel (REQ-026).
4. Represent the task dependency flow using a Mermaid flowchart.

### Step 7: Decide on Task Granularity & Discrete Task Files
Evaluate the feature scope:
- **Standard Features (< 8-10 tasks):** Keep all task definitions directly within `plan.md`. This minimizes file clutter and keeps the plan cohesive.
- **Complex Features (10+ tasks, multi-developer, or deep components):** Maintain high-level task summaries in `plan.md` and generate discrete `tasks/<task-id>.md` files conforming to `templates/task.md` in `.dev-team/features/<feature-name>/tasks/`. This allows workers to consume individual task cards without loading the entire plan.

### Step 8: Plan Review & Quality Audit (REQ-028)
Perform a rigorous plan audit across six dimensions before presenting to the developer:
1. **Coverage:** Does every single functional requirement (`REQ-xxx`) map to at least one task?
2. **Dependencies:** Are task prerequisites logically ordered (e.g. data models before UI)? Are there missing dependencies?
3. **Ordering:** Is the execution sequence optimal and unambiguous?
4. **Scope:** Does any task introduce code or behavior not specified in `system-design.md`?
5. **Risk:** Are high-risk operations (migrations, shared code refactoring, breaking API changes) isolated into dedicated tasks?
6. **Testability:** Does every task have explicit validation commands and observable success criteria?

*Document the audit findings in the Plan Review section of `plan.md`.*

### Step 9: Assemble `plan.md`
1. Load `templates/plan.md`.
2. Populate all sections with the synthesized plan data.
3. Set status to `DRAFT`.
4. Save the file to `.dev-team/features/<feature-name>/plan.md`.

### Step 10: Developer Plan Approval Gate (SAFE-003, REQ-029)
1. Present the plan overview to the developer:
   - Milestone breakdown.
   - Total task count and critical path.
   - Plan review audit result.
2. Request explicit developer sign-off:
   > *"The implementation plan for `[feature-name]` has been generated with [N] tasks across [M] milestones and passed review. Please review `.dev-team/features/<feature-name>/plan.md` and confirm your approval before implementation begins."*
3. **Wait for explicit approval.**
   - If revisions requested: update tasks or dependencies and re-verify.
   - If approved: update status to `APPROVED`, record approval timestamp and approver name in `plan.md`, and proceed to `workflows/implement-next.md`.

---

## 6. Task Slicing Rules & Anti-Patterns

### Good Task Characteristics:
- **Single Responsibility:** Implements one logical piece (e.g., only the repository, or only the bloc, or only the widget).
- **Timebox-Friendly:** Can be executed and verified within 15–45 minutes of agent work.
- **Explicit File Boundaries:** Lists exact file paths that will be touched.
- **Deterministic Check:** Can be proven to work via a command that exits with code 0.

### Anti-Patterns to Avoid:
- **The "Everything Bagel" Task:** *"Implement entire review system"* (violates REQ-023; impossible to review or roll back incrementally).
- **Vague Acceptance Criteria:** *"Should work properly and handle errors well"* (unverifiable).
- **Missing Validation Commands:** *"Manual testing by developer later"* (violates SAFE-009; tasks must specify immediate verification).
- **Premature Downstream Changes:** Modifying UI before state management or models are completed.

---

## 7. Scope Change & Replanning Protocol (REQ-030)

If, during task implementation, an unexpected architectural flaw, dependency conflict, or missing product requirement is discovered:
1. **Pause Affected Work:** Immediately halt execution on the current task and downstream dependent tasks. Do not attempt unapproved workarounds.
2. **Isolate the Delta:** Identify whether the change affects requirements (`requirement.md`), architecture (`system-design.md`), or purely task sequencing (`plan.md`).
3. **Escalate to Developer:** Present the discovered obstacle, explain the impact (SAFE-008), and propose specific revision options.
4. **Update Artifacts:** Upon developer decision, update the upstream artifacts, re-run relevant validation, update `plan.md`, obtain re-approval, and resume execution.

---

## 8. Quality Gate Checklist (Planning Phase)

Before submitting `plan.md` for developer approval, confirm all gates pass:

- [ ] **PLAN-GATE-1 (Traceability):** Every task maps to at least one approved requirement ID (`REQ-xxx`).
- [ ] **PLAN-GATE-2 (Independent & Verifiable):** Tasks have explicit scopes, expected files, deliverables, and validation commands.
- [ ] **PLAN-GATE-3 (Explicit Approval):** Developer must explicitly approve the plan before implementation begins (`SAFE-003`, `REQ-029`).
- [ ] **PLAN-GATE-4 (Explicit Dependencies):** All task dependencies are declared; sequential and parallelizable tasks are distinguished (`REQ-026`).
- [ ] **PLAN-GATE-5 (Audit Completed):** Six-dimension plan review (coverage, dependencies, ordering, scope, risk, testability) recorded in plan (`REQ-028`).
