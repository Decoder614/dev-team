# Workflow: New Feature (Idea to Requirements)

**Workflow ID:** `new-feature`  
**Entry Point:** `workflows/new-feature.md`  
**Primary Roles:** Product Analyst, Product Reviewer, Developer (Approver)  
**Applicable Skills:**  
- `skills/product-requirements/SKILL.md`  
- `skills/requirement-validation/SKILL.md`  
**Governing Gate:** Requirements Gate (`config/quality-gates.yaml`)  

---

## 1. Purpose & Overview

The `new-feature` workflow governs the end-to-end process of turning an informal developer idea, enhancement request, or product requirement into a structured, independently reviewed, and developer-approved `requirement.md` specification.

No technical architecture or implementation code may be produced until this workflow successfully concludes with explicit developer approval.

---

## 2. Prerequisites & Entry Conditions

1. **Trigger:** Developer provides a feature idea, problem description, user story, or requests a new feature.
2. **Context Discovery:**
   - Inspect target repository root for `AGENTS.md` to discover project-specific guidelines.
   - Inspect `.dev-team/project-profile.yaml` (or `config/defaults.yaml`) to identify the configured features directory (`.dev-team/features/`).
3. **Collision Check:**
   - Inspect `.dev-team/features/<feature-name>/requirement.md`.
   - If an approved requirement document already exists, **do not overwrite it**. Inform the developer and request instructions to revise, branch, or cancel.

---

## 3. Quality Gates Enforced

Per `config/quality-gates.yaml` and system safety boundaries:
- [x] **REQ-GATE-1 (Acceptance Criteria):** Every functional requirement must have verifiable acceptance criteria.
- [x] **REQ-GATE-2 (Independent Review):** An independent audit must be conducted by the Product Reviewer before requesting approval.
- [x] **REQ-GATE-3 (Zero Blockers):** No unresolved BLOCKER or CRITICAL findings may remain.
- [x] **REQ-GATE-4 (Developer Approval):** Explicit developer sign-off is mandatory before marking status `APPROVED` (SAFE-001).

---

## 4. Execution Sequence

```mermaid
flowchart TD
    A[Developer Feature Idea] --> B[Phase 1: Project Discovery & Ingestion]
    B --> C[Phase 2: Requirements Elaboration (Product Analyst)]
    C --> D{Clarification Needed?}
    D -->|Yes| E[Ask Focused Questions] --> C
    D -->|No| F[Draft requirement.md]
    F --> G[Phase 3: Independent Review (Product Reviewer)]
    G --> H{Review Outcome?}
    H -->|NEEDS_REVISION| I[Incorporate Review Findings] --> C
    H -->|APPROVED / WITH_FOLLOW_UPS| J[Phase 4: Developer Approval Gate]
    J --> K{Developer Decision?}
    K -->|Revisions Requested| C
    K -->|Approved| L[Phase 5: Baseline as APPROVED]
    L --> M[Next: Design Feature Workflow]
```

### Phase 1: Context Discovery & Ingestion
1. Determine feature slug and documentation directory:
   - Directory: `.dev-team/features/<feature-slug>/`
   - Target file: `.dev-team/features/<feature-slug>/requirement.md`
2. Inspect target project `AGENTS.md` and `.dev-team/project-profile.yaml` for context.
3. Check for existing artifacts:
   - If `requirement.md` exists with status `APPROVED`, stop and ask developer whether to revise.
   - If none exists, create the feature directory.

### Phase 2: Requirements Elaboration (Product Analyst)
*Activate `skills/product-requirements/SKILL.md` (Product Analyst role).*
1. Parse the developer's idea into problem statement, target users, goals, and non-goals.
2. If critical assumptions or domain details are missing, ask targeted clarifying questions (SAFE-012).
3. Formulate atomic functional requirements with unique stable IDs (`REQ-001`, `REQ-002`, ...).
4. Define non-functional requirements (performance, security, error handling, accessibility).
5. Map user flows, edge cases, error states, and empty states.
6. Populate `templates/requirement.md` with initial status `DRAFT`.
7. Save the drafted `requirement.md` in `.dev-team/features/<feature-slug>/`.

### Phase 3: Independent Requirement Review (Product Reviewer)
*Activate `skills/requirement-validation/SKILL.md` (Product Reviewer role).*
1. Review the draft independently across the eight audit dimensions:
   - Clarity, Completeness, Consistency, Feasibility, Testability, Security, Edge Cases, Error/Empty States.
2. Classify findings by severity (`BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `TRIVIAL`).
3. Generate review determination:
   - **`NEEDS_REVISION`:** If any BLOCKER or CRITICAL finding exists. Return to Phase 2 for Product Analyst remediation.
   - **`APPROVED`** or **`APPROVED_WITH_FOLLOW_UPS`:** Proceed to Phase 4.
4. Record findings and update Section 9.1 (*Independent Review Summary*) of `requirement.md`.

### Phase 4: Developer Approval Gate (Mandatory)
1. Present the requirement document summary, review determination, and any open questions to the developer.
2. Explicitly prompt the developer for review and approval:
   > *"Requirement draft for `[feature-name]` has passed independent review with status `[DETERMINATION]`. Please review `.dev-team/features/<feature-slug>/requirement.md` and confirm your approval before we proceed to technical design."*
3. Wait for developer response.
   - If developer requests modifications: update draft (return to Phase 2).
   - If developer approves: proceed to Phase 5.

### Phase 5: Baseline & Transition
1. Update `requirement.md` frontmatter and metadata:
   - `Status: APPROVED`
   - `Approver: [Developer Name]`
   - `Approval Date: [Current Date]`
2. Commit or stage the approved `requirement.md`.
3. Report completion to developer and recommend the next step:
   - Transition to `workflows/design-feature.md` for technical architecture and design.

---

## 5. Artifact Lifecycle & Status Values

Throughout this workflow, `requirement.md` transitions as follows:
- `DRAFT` (Initial creation by Product Analyst)
- `IN_REVIEW` (Under evaluation by Product Reviewer)
- `NEEDS_REVISION` (If review uncovers BLOCKER or CRITICAL issues)
- `APPROVED` (Solely upon explicit developer sign-off)

---

## 6. Safety & Boundary Rules

- **SAFE-001:** No agent or workflow may treat requirements as approved without explicit developer confirmation.
- **SAFE-004:** Existing approved requirements must never be overwritten or changed without developer authorization.
- **SAFE-006:** Do not delete existing feature directories or artifacts.
- **SAFE-012:** When business rules or security constraints are uncertain, stop and ask the developer.

