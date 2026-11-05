# Workflow: Validate Feature (QA & Feature Validation)

**Workflow ID:** `feature_validation`  
**Entry Point:** `workflows/validate-feature.md`  
**Primary Roles:** QA Engineer, Developer (Final Sign-off Authority)  
**Applicable Skills:**  
- `skills/code-review/SKILL.md`  
- `skills/feature-validation/SKILL.md`  
- `skills/project-discovery/SKILL.md`  
**Governing Gates:** `testing`, `code_review`, `final_acceptance` (`config/quality-gates.yaml`)  

---

## 1. Purpose & Overview

The `feature_validation` workflow executes independent quality assurance and verification for an implemented feature before developer acceptance and release.

This workflow enforces the core validation and safety principles of Dev-Team:
- **Independent QA Assessment:** The QA Engineer independently inspects changed code and verifies functionality against approved requirements, not developer claims (`REQ-040`, `REQ-041`).
- **Comprehensive 8-Dimension Review:** Evaluates correctness, maintainability, security, performance, data integrity, error handling, regression risks, and project conventions (`REQ-041`, `skills/code-review/SKILL.md`).
- **Deterministic Validation & Tangible Evidence:** Executes test runners, linters, and static analyzers, capturing actual command output and exit codes (`SAFE-009`, `REQ-042`).
- **Honest Limitations & Unverified Areas:** Explicitly records unexecuted checks, missing emulators, or untestable environments rather than falsely claiming passes (`SAFE-009`, `REQ-043`).
- **Blocking Defects Halt Release:** No feature can be marked fully complete or approved while blocking defects or unmet mandatory criteria remain (`REQ-046`).
- **Developer Final Acceptance Authority:** The developer alone holds final sign-off authority for product acceptance (`SAFE-001`, `REQ-047`).

---

## 2. Prerequisites & Entry Conditions

1. **Trigger:**
   - Invoked after completing tasks in an implementation milestone via `workflows/implement-next.md`.
   - Developer explicitly requests feature verification (e.g., *"validate feature"*, *"run QA on auth feature"*, or *"review implemented feature"*).
   - Pre-merge validation check for a feature branch.
2. **Approved Artifact Requirements:**
   - Target feature directory `.dev-team/features/<feature-slug>/` must contain:
     - `requirement.md` with `Status: APPROVED` (`SAFE-001`).
     - `plan.md` with `Status: APPROVED` (`SAFE-003`).
   - If either artifact is missing or unapproved, halt execution and inform developer.
3. **Task Completion Check:**
   - Verify that target implementation tasks in `plan.md` have reached `COMPLETED` or `NEEDS_REVIEW`.
4. **Clean Baseline Inspection (`SAFE-010`):**
   - Execute `git status` to identify modified, added, or uncommitted files.

---

## 3. Quality Gates Enforced

Per `config/quality-gates.yaml`:

### Testing Gate
- [x] `require_test_result_reporting: true` — All executed tests must be recorded with command lines, test counts, and pass/fail counts.
- [x] `prohibit_unverified_pass_claims: true` — Unexecuted tests must never be marked as passed.
- [x] `require_observed_command_output: true` — Command outputs and exit codes must be captured directly from shell execution.

### Code Review Gate
- [x] `require_independent_review: true` — Independent review executed using `skills/code-review/SKILL.md`.
- [x] `check_correctness_and_conventions: true` — Functional correctness, edge cases, and code style verified.
- [x] `check_security_and_data_integrity: true` — Credential exposure, injection, state consistency, and data validation verified.
- [x] `check_regression_risk: true` — Shared contracts, backward compatibility, and existing tests verified.

### Final Acceptance Gate
- [x] `require_completed_qa_report: true` — `qa-report.md` produced conforming to `templates/qa-report.md`.
- [x] `require_clean_git_status: true` — Working tree status inspected and verified clean.
- [x] `require_developer_signoff: true` — Developer sign-off block presented for explicit final decision (`SAFE-001`).

---

## 4. Execution Sequence

```mermaid
flowchart TD
    A[Start: Request Feature Validation] --> B[Phase 1: Input Baseline & Context Ingestion]
    B --> C{Approved Specs Exist & Code Available?}
    C -->|No| D[Halt: Missing Approved Specs or Code]
    C -->|Yes| E[Phase 2: Static Analysis & Test Execution]
    E --> F[Phase 3: Multi-Dimensional Code Review]
    F --> G[Phase 4: Requirements Coverage Evaluation]
    G --> H[Phase 5: Document Limitations & Unverified Areas]
    H --> F2[Phase 6: Compile QA Report (qa-report.md)]
    F2 --> I{Blockers or Unmet Mandatory Criteria?}
    I -->|Yes| J[Recommendation: NEEDS_REVISION (Return to Developer)]
    I -->|No| K[Recommendation: APPROVED / WITH_FOLLOW_UPS]
    K --> L[Phase 7: Developer Acceptance Sign-off Gate]
```

### Phase 1: Input Baseline & Context Ingestion
1. Ingest `.dev-team/features/<feature-slug>/requirement.md`. Verify status is `APPROVED`.
2. Ingest `.dev-team/features/<feature-slug>/plan.md`. Verify status is `APPROVED`.
3. Read target project `AGENTS.md` and `.dev-team/project-profile.yaml` to discover project validation commands and architecture.
4. Execute `git status` and `git diff` against base branch to identify the exact files modified during implementation.

### Phase 2: Static Analysis & Test Execution
*Enforces `SAFE-009`, `REQ-042`, and `REQ-043`.*
1. Execute code formatting validation:
   ```bash
   # Check code formatting without mutating files
   dart format --output=none --set-exit-if-changed lib/ test/
   ```
2. Execute static analysis / lint check:
   ```bash
   # Static analyzer check
   flutter analyze --no-fatal-infos
   ```
3. Execute relevant automated test suites:
   ```bash
   # Targeted unit and widget tests for the feature
   flutter test test/features/<feature-slug>/
   ```
4. Observe and record:
   - Command line executed.
   - Command exit code (`0` = clean pass).
   - Tangible output log summary (e.g. `All 14 tests passed!`).
5. For any test or check that cannot be run (e.g., integration tests requiring live hardware, camera, external APIs):
   - Record explicitly as `UNVERIFIED` / `SKIPPED`. Do NOT report as passed.

### Phase 3: Multi-Dimensional Code Review
*Activate `skills/code-review/SKILL.md` (QA Engineer role).*
1. Review all modified and added files across the 8 dimensions:
   - **Correctness & Logic:** Edge cases, null safety, boundary checks, async/stream safety.
   - **Maintainability & Readability:** Clean architecture, single responsibility, no dead code.
   - **Security & Privacy:** No hardcoded secrets (`SAFE-005`), sanitized inputs, secure storage.
   - **Performance:** Resource disposal (`dispose()`), rebuild minimization, non-blocking I/O.
   - **Data Integrity:** Schema validation, state immutability, race condition prevention.
   - **Error Handling:** Graceful failure states, empty UI views, no swallowed exceptions.
   - **Regression Risks:** Compatibility with existing contracts, shared services, and existing tests.
   - **Project Conventions:** Naming, directory layout, DI, and state patterns.
2. For each identified defect, record:
   - Severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `TRIVIAL`.
   - File path and line range.
   - Clear description and failure evidence.
   - Concrete, actionable remediation instructions.

### Phase 4: Requirements Coverage Evaluation
*Activate `skills/feature-validation/SKILL.md`.*
1. Extract all functional requirements (`REQ-xxx`) and non-functional requirements (`NFR-xxx`) from `requirement.md`.
2. Construct the Requirements Coverage Matrix:
   - Cross-reference each acceptance criterion with implemented code and automated test evidence.
   - Assign status: `VERIFIED`, `PARTIAL`, `UNMET`, or `UNVERIFIED`.
3. If any mandatory acceptance criterion is not satisfied:
   - Mark as `UNMET`.
   - File a corresponding defect finding linking to the Requirement ID.

### Phase 5: Document Limitations & Unverified Areas
*Enforces `REQ-043`.*
1. Identify all tests, environments, or edge cases that could not be verified automatically.
2. Document each in the QA report with:
   - Reason for inability to verify (e.g., missing biometric hardware, unmocked payment service).
   - Residual operational risk.
   - Recommended follow-up action for the developer.

### Phase 6: Compile QA Report (`qa-report.md`)
1. Create or overwrite `.dev-team/features/<feature-slug>/qa-report.md` using `templates/qa-report.md`.
2. Populate all sections:
   - Executive Summary and Quality Metrics Table.
   - Artifact Baseline & Modified Files.
   - Requirements Coverage Matrix.
   - Code Review Findings Table and Detailed Findings.
   - Test Execution Log with tangible outputs.
   - Unverified Areas & Environmental Limitations.
   - Remaining Issues & Blockers.
3. Determine QA recommendation:
   - **`NEEDS_REVISION`**: If any `BLOCKER` or `CRITICAL` defect exists, or if any mandatory acceptance criterion is `UNMET` (`REQ-046`).
   - **`APPROVED_WITH_FOLLOW_UPS`**: If all mandatory criteria are `VERIFIED`, zero `BLOCKER`/`CRITICAL` issues exist, but non-blocking `MAJOR`/`MINOR` items remain.
   - **`APPROVED`**: If all criteria are `VERIFIED`, zero defects or only trivial suggestions exist.

### Phase 7: Developer Acceptance Sign-off Gate
*Enforces `SAFE-001` and `REQ-047`.*
1. Present the executive summary and QA determination to the developer:
   ```text
   QA Evaluation Complete for Feature: [Feature Name]
   Determination: [APPROVED | APPROVED_WITH_FOLLOW_UPS | NEEDS_REVISION]
   Requirements Coverage: [X / Y] criteria VERIFIED
   Defects Found: [B] Blocker, [C] Critical, [M] Major, [m] Minor
   QA Report Location: .dev-team/features/<feature-slug>/qa-report.md
   ```
2. If determination is `NEEDS_REVISION`:
   - Detail the blocking issues.
   - Recommend transitioning back to the Developer role for remediation via `workflows/implement-next.md` or `workflows/fix-bug.md`.
3. If determination is `APPROVED` or `APPROVED_WITH_FOLLOW_UPS`:
   - Prompt the developer for final acceptance sign-off.
   - Once explicitly confirmed by the developer, update `qa-report.md` status to `APPROVED` and record the developer acceptance sign-off.

---

## 5. Escalation & Remediation Routing

```text
QA Determination: NEEDS_REVISION
            │
            ▼
Are defects new bugs in newly written code?
   ├── Yes ──> Route to Developer via workflows/implement-next.md
   └── Regression / Complex Defect ──> Route to workflows/fix-bug.md
```

If an issue reveals an ambiguity in original requirements or an architectural mismatch:
1. Do NOT guess or rewrite requirements silently (`SAFE-004`, `SAFE-012`).
2. Escalate to the developer with the specific conflict and trade-offs.
3. Upon developer approval of updated requirements or design, update the respective baseline artifacts and re-evaluate.

