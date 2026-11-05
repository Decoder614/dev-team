---
name: requirement-validation
description: >-
  Reusable procedural skill for independently auditing and validating product requirement
  documents (requirement.md). Evaluates clarity, completeness, consistency, feasibility,
  testability, security, edge cases, and error states, producing categorized findings and a review determination.
  Activate when validating a requirement document, conducting peer review, or running the validate-requirement workflow.
---

# Requirement Validation Skill

## 1. Overview & Purpose

This skill provides an objective, repeatable procedure for independently auditing feature requirements before design and implementation work begins.

The purpose is to challenge assumptions, catch ambiguities, prevent contradictions, and ensure every requirement is testable and secure, preventing costly downstream rework.

---

## 2. When to Use

Activate this skill when:
- A `requirement.md` draft has been produced and requires independent review.
- The `validate-requirement` workflow (`workflows/validate-requirement.md`) is executed.
- The developer asks to review, audit, sanity-check, or critique a feature specification.
- Changes or additions are proposed to an existing requirement document.

---

## 3. Required Inputs

1. **Target Requirement Document:** Path to `requirement.md` (e.g. `.dev-team/features/<feature-name>/requirement.md`).
2. **Project Context (if applicable):**
   - Target project `AGENTS.md` and `.dev-team/project-profile.yaml`.
   - Existing architecture or database schema documentation when checking technical feasibility.

---

## 4. Eight-Dimension Audit Procedure

Evaluate the requirement document systematically across these eight core dimensions:

### Dimension 1: Clarity & Precision
- Are terms defined unambiguously?
- Flag subjective or unmeasurable words: *"fast"*, *"intuitive"*, *"robust"*, *"user-friendly"*, *"efficient"*, *"etc."*.
- Ensure user roles, inputs, system actions, and outputs are clearly articulated.

### Dimension 2: Completeness
- Does the document include all essential sections (Problem, Goals, Non-Goals, Functional Requirements, Non-Functional Requirements, Edge Cases)?
- Are all user personas accounted for?
- Are business rules and validation constraints fully stated, or are there obvious omissions?

### Dimension 3: Consistency & Alignment
- Do functional requirements directly support the stated Goals?
- Are there contradictions between different requirements (e.g., REQ-001 requires immediate persistence, but REQ-004 specifies deferred batching)?
- Does any requirement inadvertently conflict with the Non-Goals?

### Dimension 4: Feasibility & Technology Alignment
- Can the requirements be realistically implemented within the target project's tech stack (e.g., Flutter, database, backend)?
- Are there impossible or overly speculative expectations?
- Does the requirement respect known platform constraints (mobile, web, offline)?

### Dimension 5: Testability & Verifiability
- Does each requirement have verifiable Acceptance Criteria?
- Can a QA engineer or developer write an automated unit/widget/integration test or execute a concrete manual check for each criterion?
- Are acceptance criteria formatted with measurable preconditions, actions, and expected outcomes?

### Dimension 6: Security & Privacy
- Are authorization and authentication expectations explicit?
- Does the feature handle sensitive data (passwords, tokens, PII, payment info)? If so, are encryption and sanitization stated?
- Are multi-tenant or role-based boundary conditions respected?

### Dimension 7: User Scenarios & Edge Cases
- Are primary (happy path) and alternative flows documented?
- What happens if the user cancels midway, submits duplicate requests, or inputs boundary values (0, negative, maximum length)?
- Are concurrency or race conditions considered?

### Dimension 8: Error, Loading, and Empty States
- How does the UI behave when no records exist (Empty State)?
- How does the UI indicate background network activity (Loading State)?
- How does the system handle network disconnection, timeouts, or 5xx server errors (Error State)?
- Is recovery or retry guidance provided to the user?

---

## 5. Finding Severity Classification

Every finding must be assigned one of the standard severity levels (from `config/defaults.yaml`):

| Severity | Definition | Action Required |
|---|---|---|
| **BLOCKER** | Fundamental contradiction, critical security/data-loss risk, or complete absence of testability that prevents design or implementation. | Must be resolved before proceeding. Workflow halts. |
| **CRITICAL** | Major missing user flow, unhandled error state with severe UX disruption, or unstated essential business rule. | Must be resolved before design approval. |
| **MAJOR** | Ambiguity in business logic, missing acceptance criteria, or unaddressed high-probability edge case. | Resolution recommended before design; may be tracked as explicit follow-up. |
| **MINOR** | Phrasing ambiguity, minor omission, or non-blocking open question that can be refined during planning. | Address during draft revision. |
| **TRIVIAL** | Typo, formatting issue, or cosmetic documentation improvement. | Fix when convenient. |

---

## 6. Review Determinations

Based on the findings, assign one of three standard outcomes:

1. **`APPROVED`**:
   - Zero BLOCKER and zero CRITICAL findings.
   - All acceptance criteria are testable.
   - Requirements are clear, complete, and consistent.
   - Ready for developer sign-off.

2. **`APPROVED_WITH_FOLLOW_UPS`**:
   - Zero BLOCKER and zero CRITICAL findings.
   - Contains MINOR or minor MAJOR findings that are non-blocking and can be clarified in technical design.
   - Open items must be explicitly listed with responsible owners.

3. **`NEEDS_REVISION`**:
   - One or more BLOCKER or CRITICAL findings exist.
   - The requirement document cannot serve as an implementation source of truth until revised.
   - Product Analyst must update the draft.

---

## 7. Review Report Format

Generate the review report following this standard structure:

```markdown
# Requirement Audit Report: [Feature Name]

**Document Evaluated:** `[path/to/requirement.md]`  
**Reviewer:** Product Reviewer  
**Date:** [YYYY-MM-DD]  
**Determination:** [APPROVED / APPROVED_WITH_FOLLOW_UPS / NEEDS_REVISION]  

## Summary of Audit
[Brief executive summary of document quality and readiness]

## Findings by Severity

### Blocker Findings
- None (or list: `[REQ-xxx]` Issue description — Remediation)

### Critical Findings
- [List or None]

### Major Findings
- [List or None]

### Minor & Trivial Findings
- [List or None]

## Detailed Dimension Evaluation
1. Clarity & Precision: [Pass / Concerns]
2. Completeness: [Pass / Concerns]
3. Consistency: [Pass / Concerns]
4. Feasibility: [Pass / Concerns]
5. Testability: [Pass / Concerns]
6. Security & Privacy: [Pass / Concerns]
7. User Scenarios & Edge Cases: [Pass / Concerns]
8. Error, Loading & Empty States: [Pass / Concerns]

## Next Steps
- [Actionable next steps based on determination]
```

### Updating `requirement.md`
Record the summary in Section 9.1 (*Independent Review Summary*) of the target `requirement.md`:
- Set `Review Outcome` to the determination.
- Update document `Status` if appropriate (`IN_REVIEW` or `NEEDS_REVISION`).

---

## 8. Safety & Quality Boundaries

- **SAFE-001:** The reviewer's approval does NOT replace developer sign-off. Only the developer can grant final authorization to proceed to design.
- **SAFE-004:** Never silently edit or overwrite existing approved requirements while reviewing.
- **SAFE-012:** When missing information could materially impact security or correctness, flag as BLOCKER and pause for developer input.

