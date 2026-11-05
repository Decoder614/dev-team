# Dev-Team Engineering Workflows

> **Virtual AI Software Development Team**  
> Operational manual for standard engineering workflows coordinating roles, skills, templates, and quality gates.

---

## 1. Workflow Architecture & Lifecycle

Dev-Team workflows guide software delivery through eight standard operating procedures. Each workflow governs a specific phase of the engineering lifecycle, coordinating specialized roles and enforcing quality gates:

```mermaid
flowchart TD
    Idea([Product Idea / Need]) --> WF1[1. new-feature\nProduct Analyst]
    WF1 --> ReqDraft[/requirement.md (DRAFT)/]
    
    ReqDraft --> WF2[2. validate-requirement\nProduct Reviewer]
    WF2 --> ReqApproved{Developer Approval Gate\nSAFE-001}
    
    ReqApproved -->|Approved| WF3[3. design-feature\nSystem Architect]
    ReqApproved -->|Needs Revision| WF1
    
    WF3 --> DesignApproved{Developer Approval Gate\nSAFE-002}
    
    DesignApproved -->|Approved| WF4[4. create-plan\nTechnical Planner]
    DesignApproved -->|Needs Revision| WF3
    
    WF4 --> PlanApproved{Developer Approval Gate\nSAFE-003}
    
    PlanApproved -->|Approved| WF5[5. implement-next\nDeveloper]
    PlanApproved -->|Needs Revision| WF4
    
    WF5 --> NextTaskCheck{More Tasks?}
    NextTaskCheck -->|Yes| WF5
    NextTaskCheck -->|All Tasks Done| WF6[6. validate-feature\nQA Engineer]
    
    WF6 --> QAPass{QA Verdict & Final Gate\nSAFE-001}
    QAPass -->|Pass & Accepted| Done([Feature Delivered & Accepted])
    QAPass -->|Defects Found| WF7[7. fix-bug\nDeveloper & QA]
    WF7 --> WF6
    
    Audit([Progress Query]) -.-> WF8[8. feature-status\nZero-Hallucination Audit]
    WF8 -.-> Dashboard[/Status Dashboard/]
```

---

## 2. Core Workflows Summary

| # | Workflow ID | Entry Point | Primary Role | Activated Skill | Governing Gate | Primary Deliverable |
|---|---|---|---|---|---|---|
| **1** | `new_feature` | `workflows/new-feature.md` | Product Analyst | `product-requirements` | Requirements Gate | `.dev-team/features/<f>/requirement.md` |
| **2** | `requirement_validation` | `workflows/validate-requirement.md` | Product Reviewer | `requirement-validation` | Review Audit Gate | Audit report & resolved questions |
| **3** | `feature_design` | `workflows/design-feature.md` | System Architect | `system-design`, `project-discovery` | Architecture Gate | `.dev-team/features/<f>/system-design.md` |
| **4** | `create_plan` | `workflows/create-plan.md` | Technical Planner | `technical-planning` | Plan Gate | `.dev-team/features/<f>/plan.md` |
| **5** | `implementation` | `workflows/implement-next.md` | Developer | `flutter-development` | Implementation Gate | Code modifications, unit tests |
| **6** | `feature_validation` | `workflows/validate-feature.md` | QA Engineer | `feature-validation`, `code-review` | Final Acceptance Gate | `.dev-team/features/<f>/qa-report.md` |
| **7** | `bug_fixing` | `workflows/fix-bug.md` | Developer / QA | `bug-fixing` | Defect Verification Gate | Minimal fix, regression test |
| **8** | `feature_status` | `workflows/feature-status.md` | Auditor | *None (Direct inspection)* | Audit Accuracy Gate | Progress dashboard & blockers |

---

## 3. Workflow Specifications

### 3.1 New Feature Workflow (`workflows/new-feature.md`)
- **Role:** Product Analyst (`agents/product-analyst.toml`)
- **Purpose:** Converts unstructured product concepts, feature requests, or developer ideas into structured, testable requirements documents.
- **Entry Trigger:** Developer requests a new feature or capability.
- **Prerequisites:** Informal feature brief, problem statement, or user story.
- **Phases:**
  1. Ingest feature concept and target project context.
  2. Elicit functional scope, user journeys, and edge cases.
  3. Formulate verifiable acceptance criteria.
  4. Identify open technical or UX questions.
  5. Populate `requirement.md` from `templates/requirement.md`.
  6. Present draft for developer review.

### 3.2 Requirement Validation Workflow (`workflows/validate-requirement.md`)
- **Role:** Product Reviewer (`agents/product-reviewer.toml`)
- **Purpose:** Conducts an independent, adversarial audit of draft requirements to detect ambiguities, missing edge cases, security implications, and scope creep before architecture begins.
- **Entry Trigger:** Requirement document reaches `DRAFT` or `IN_REVIEW`.
- **Governing Gate:** `SAFE-001` (Developer approval prerequisite).
- **Phases:**
  1. Inspect `requirement.md` against quality criteria.
  2. Evaluate acceptance testability and completeness.
  3. Surface critical ambiguities or missing failure scenarios.
  4. Submit structured audit feedback to the developer.

### 3.3 Design Feature Workflow (`workflows/design-feature.md`)
- **Role:** System Architect (`agents/system-architect.toml`)
- **Purpose:** Discovers target project conventions and creates modular technical designs aligned with the existing codebase without introducing hardcoded technology prescriptions.
- **Entry Trigger:** Developer approves `requirement.md` (`SAFE-001`).
- **Governing Gate:** `SAFE-002` (Developer architectural approval).
- **Phases:**
  1. Run project discovery on target repository structure and dependencies.
  2. Map requirements to application layers, components, and data models.
  3. Evaluate trade-offs, state management, and error handling.
  4. Identify architectural decisions requiring developer signoff.
  5. Generate `system-design.md` from `templates/system-design.md`.

### 3.4 Create Plan Workflow (`workflows/create-plan.md`)
- **Role:** Technical Planner (`agents/technical-planner.toml`)
- **Purpose:** Decomposes approved architecture into sequenced, granular implementation tasks with explicit dependencies, file targets, and deterministic validation commands.
- **Entry Trigger:** Developer approves `system-design.md` (`SAFE-002`).
- **Governing Gate:** `SAFE-003` (Developer plan approval).
- **Phases:**
  1. Ingest approved architecture and requirements.
  2. Slice deliverables into small, atomic tasks (1 task = 1 clear deliverable).
  3. Construct a directed dependency graph.
  4. Define validation procedures and acceptance criteria for each task.
  5. Generate `plan.md` from `templates/plan.md`.

### 3.5 Implement Next Task Workflow (`workflows/implement-next.md`)
- **Role:** Developer (`agents/developer.toml`)
- **Purpose:** Executes exactly one approved, unblocked implementation task per session, strictly adhering to existing project idioms and capturing concrete validation evidence.
- **Entry Trigger:** Developer requests task execution on an approved plan.
- **Governing Gate:** `IMPL-GATE-1` through `IMPL-GATE-5`, `SAFE-009`, `SAFE-010`.
- **Phases:**
  1. Select next `PENDING` task whose dependencies are `COMPLETED`.
  2. Inspect git status to safeguard uncommitted developer work (`SAFE-010`).
  3. Transition task status to `IN_PROGRESS`.
  4. Implement minimal, surgical code changes within approved scope.
  5. Create or update unit and widget tests.
  6. Execute validation commands and observe exit codes (`SAFE-009`).
  7. Record tangible evidence and transition task to `COMPLETED`.
  8. Stop and summarize modified files.

### 3.6 Validate Feature Workflow (`workflows/validate-feature.md`)
- **Role:** QA Engineer (`agents/qa-engineer.toml`)
- **Purpose:** Independently validates the complete implemented feature against requirements, conducts security and regression audits, and prepares the final QA report.
- **Entry Trigger:** All implementation tasks in the approved plan are `COMPLETED`.
- **Governing Gate:** `QA-GATE-1` through `QA-GATE-5`, `SAFE-001`.
- **Phases:**
  1. Cross-reference implemented code against all acceptance criteria.
  2. Execute full project test suite, static analysis, and formatters.
  3. Perform adversarial edge case testing and code review.
  4. Generate `qa-report.md` from `templates/qa-report.md`.
  5. Present final acceptance verdict to the developer.

### 3.7 Fix Bug Workflow (`workflows/fix-bug.md`)
- **Role:** Developer (`agents/developer.toml`) and QA Engineer (`agents/qa-engineer.toml`)
- **Purpose:** Diagnoses defects, deterministically reproduces them prior to code editing, isolates root causes from symptoms, implements minimal surgical fixes, and ensures regression test coverage.
- **Entry Trigger:** Defect reported during validation or in production.
- **Governing Gate:** Reproduction Gate (`REQ-049`), Risky Fix Approval Gate (`REQ-052`).
- **Phases:**
  1. Ingest defect symptoms, environment, and logs into `bug-report.md`.
  2. Deterministically reproduce the defect with a failing test (`REQ-049`).
  3. Perform root-cause analysis (explicitly labeling hypotheses).
  4. Plan minimal surgical fix; escalate if architectural changes are required.
  5. Implement minimal fix and add automated regression test (`REQ-053`).
  6. Execute deterministic validation suite and verify fix (`SAFE-009`).
  7. Submit for independent verification and developer resolution.

### 3.8 Feature Status Workflow (`workflows/feature-status.md`)
- **Role:** Framework Auditor / Any Agent
- **Purpose:** Provides zero-hallucination status accounting by inspecting on-disk artifacts (`requirement.md`, `system-design.md`, `plan.md`, `qa-report.md`), calculating exact task completion percentages, and surfacing active blockers.
- **Entry Trigger:** Developer queries project or feature progress.
- **Governing Gate:** Zero-Hallucination Grounding (`REQ-057` to `REQ-061`).
- **Phases:**
  1. Inspect target feature directory and discover existing artifacts.
  2. Verify document approval headers and gate statuses.
  3. Parse plan task states (`PENDING`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`, `NEEDS_REVIEW`).
  4. Compute mathematical progress percentage based on verified tasks.
  5. Surface active blockers, open architectural questions, or review items.
  6. Render formatted terminal status dashboard.

---

## 4. Execution Guidance for Developers

To execute workflows in your Codex CLI session:

- **Start a new feature:**  
  `"Run the new-feature workflow to design user authentication."`
- **Audit requirements:**  
  `"Audit the draft requirements using the validate-requirement workflow."`
- **Design architecture:**  
  `"Execute design-feature for user-authentication."`
- **Generate plan:**  
  `"Create an implementation plan for user-authentication."`
- **Implement next task:**  
  `"Implement the next pending task in user-authentication."`
- **Validate feature:**  
  `"Run the validate-feature workflow on user-authentication."`
- **Fix a bug:**  
  `"Execute fix-bug workflow for issue #42: token refresh timeout."`
- **Check feature progress:**  
  `"Report feature-status for user-authentication."`

