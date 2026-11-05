# Workflow: Design Feature (Technical Architecture)

**Workflow ID:** `feature_design`  
**Entry Point:** `workflows/design-feature.md`  
**Primary Roles:** System Architect, Developer (Approver)  
**Applicable Skills:**  
- `skills/project-discovery/SKILL.md`  
- `skills/system-design/SKILL.md`  
**Governing Gate:** Architecture Gate (`config/quality-gates.yaml`)  

---

## 1. Purpose & Overview

The `feature_design` workflow governs the architectural design phase of feature development. It transforms an approved `requirement.md` specification into an approved, cohesive, and maintainable `system-design.md` document.

The workflow guarantees that technical architecture is grounded in actual project conventions (via Project Discovery), satisfies all functional and non-functional requirements, avoids unnecessary complexity, and secures explicit developer sign-off on consequential architectural, data model, and security decisions before technical planning begins.

---

## 2. Prerequisites & Entry Conditions

1. **Trigger:**
   - Follows successful completion of the `new-feature` workflow (`workflows/new-feature.md`).
   - Developer requests architectural design for a feature (e.g., *"design the architecture for property reviews"* or *"run design-feature for auth"*).
2. **Approved Requirements Check (Mandatory Precondition):**
   - The target feature directory `.dev-team/features/<feature-slug>/` must contain an approved `requirement.md`.
   - Verify that `requirement.md` has status `APPROVED` (per `SAFE-001` and `REQ-GATE-4`).
   - If `requirement.md` is missing, draft, or pending approval, **halt execution** and notify the developer to complete the requirements workflow first.
3. **Collision & Revision Check:**
   - Inspect `.dev-team/features/<feature-slug>/system-design.md`.
   - If an approved `system-design.md` already exists, **do not overwrite it silently** (SAFE-004, SAFE-006). Ask the developer whether to create a revision, branch, or cancel.

---

## 3. Quality Gates Enforced

Per `config/quality-gates.yaml` and system safety boundaries:
- [x] **ARCH-GATE-1 (Project Discovery):** System Architect must inspect project context before proposing architecture (`require_project_discovery: true`).
- [x] **ARCH-GATE-2 (Architectural Justification):** Technical choices must be justified with rationale and trade-offs in ADR format (`require_architectural_justification: true`).
- [x] **ARCH-GATE-3 (Consequential Approvals):** Consequential decisions (schema changes, new dependencies, auth boundary changes) require explicit developer approval (`require_developer_approval_for_significant_decisions: true`, `SAFE-002`).
- [x] **ARCH-GATE-4 (Zero Assumptions):** Foreign or hardcoded framework assumptions are prohibited (`prohibit_hardcoded_framework_assumptions: true`, `REQ-014`, `REQ-065`).

---

## 4. Execution Sequence

```mermaid
flowchart TD
    A[Start: Request Feature Design] --> B[Phase 1: Ingest Approved Requirements]
    B --> C{Approved requirement.md exists?}
    C -->|No| D[Halt: Request Requirements Sign-Off]
    C -->|Yes| E[Phase 2: Project Discovery & Context Alignment]
    E --> F[Phase 3: System Architecture Design (System Architect)]
    F --> G[Phase 4: Proportionality & Quality Check]
    G --> H[Phase 5: Developer Architecture Approval Gate]
    H --> I{Developer Decision?}
    I -->|Revisions Requested| F
    I -->|Approved| J[Phase 6: Baseline as APPROVED]
    J --> K[Next: Create Plan Workflow]
```

### Phase 1: Ingest Approved Requirements
1. Resolve the feature slug and documentation directory:
   - Directory: `.dev-team/features/<feature-slug>/`
   - Requirements file: `.dev-team/features/<feature-slug>/requirement.md`
   - Target design file: `.dev-team/features/<feature-slug>/system-design.md`
2. Read `requirement.md` and verify:
   - Document status is `APPROVED`.
   - Stable requirement identifiers (`REQ-001`, `REQ-002`, ...) exist with testable acceptance criteria.
3. If requirement is unapproved or missing, stop and advise the developer.

### Phase 2: Project Discovery & Context Alignment
*Activate `skills/project-discovery/SKILL.md`.*
1. Inspect repository instructions (`AGENTS.md`) and `.dev-team/project-profile.yaml`.
2. If `project-profile.yaml` is missing or out-of-date, inspect:
   - Package manifest (`pubspec.yaml`, `package.json`, etc.).
   - Source directory layout and feature slicing conventions.
   - State management libraries in use (BLoC, Riverpod, Provider, etc.).
   - Navigation and routing approach (GoRouter, AutoRoute, Navigator).
   - Dependency injection mechanism (GetIt, Provider, manual).
   - Backend integrations (Supabase, Firebase, REST/Dio, GraphQL).
   - Database migrations and persistence tools (PostgreSQL, SQLite, Drift, Hive).
   - Testing patterns (`flutter_test`, `mocktail`, `integration_test`).
   - Shared design system tokens and widgets.
3. Update `.dev-team/project-profile.yaml` with discovered conventions.

### Phase 3: System Architecture Design (System Architect)
*Activate `skills/system-design/SKILL.md` (System Architect role).*
1. **Traceability:** Build the Requirement Traceability Matrix connecting each `REQ-xxx` to its implementing components.
2. **Layer Architecture:** Define component boundaries across Presentation, Domain (if applicable), and Data layers conforming to existing repository conventions.
3. **Data Flow & State Lifecycle:** Detail reactive streams, state models (initial, loading, success, empty, error), and mutations.
4. **Data Modeling & Database Changes (if applicable):**
   - Specify table definitions, columns, constraints, foreign keys, and query indexes.
   - Outline deterministic migration scripts.
   - Define Row-Level Security (RLS) policies.
5. **API & Integration Specifications (if applicable):**
   - Detail endpoints, HTTP methods, JSON request/response payloads, and error codes.
   - Specify timeout limits, exponential backoff, and offline fallback behavior.
6. **UI/UX & Routing (if applicable):**
   - Define route paths, parameters, route guards, and screen states.
   - Map components to existing design system tokens (colors, typography, spacing).
7. **Security & Privacy:** Detail authentication checks, role permissions, input validation, and data sanitization.
8. **Error Handling & Resilience:** Define failure states, user-facing error recovery, and retry mechanisms.
9. **Testing Strategy:** Specify verification scope for unit, widget, and integration tests.
10. **Architecture Decision Records (ADRs):** Justify non-trivial decisions with context, alternatives, rationale, and consequences.
11. **Populate Artifact:** Draft `system-design.md` from `templates/system-design.md` with status `DRAFT`.
12. Save to `.dev-team/features/<feature-slug>/system-design.md`.

### Phase 4: Proportionality & Quality Check
1. Verify the design adheres to the **Smallest Useful Solution First** principle:
   - No unnecessary layers, abstractions, or foreign dependencies added.
   - Minor features omit non-applicable sections (REQ-021).
2. Verify zero credentials, secrets, or tokens are present in documentation (SAFE-005).
3. Ensure all consequential decisions are compiled into Section 13 (*Consequential Decisions & Approval Gate*).

### Phase 5: Developer Architecture Approval Gate (Mandatory)
1. Present an architectural summary and the consequential decisions checklist to the developer:
   - Summary of layer structure and data flow.
   - Summary of database schema changes / migrations (if any).
   - List of newly introduced packages or dependencies (if any).
   - Security, authentication, and permission impacts.
2. Explicitly prompt the developer for review and approval:
   > *"Technical design for `[feature-name]` has been drafted at `.dev-team/features/<feature-slug>/system-design.md`. Please review the architecture, particularly the consequential decisions in Section 13, and confirm your approval before we proceed to technical implementation planning."*
3. Wait for developer response:
   - If developer requests modifications: incorporate feedback and revise `system-design.md` (return to Phase 3).
   - If developer approves: proceed to Phase 6.

### Phase 6: Baseline & Transition
1. Update `system-design.md` metadata:
   - Set `Status: APPROVED`.
   - Update `Approver: [Developer Name]`.
   - Set `Approval Date: [Current Date]`.
2. Report completion to developer and recommend the next workflow step:
   > *"System design for `[feature-name]` is approved. The feature is ready for technical planning via `workflows/create-plan.md`."*

