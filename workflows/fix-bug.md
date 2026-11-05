# Workflow: Fix Bug (Bug Diagnosis & Defect Remediation)

**Workflow ID:** `bug_fixing`  
**Entry Point:** `workflows/fix-bug.md`  
**Primary Roles:** Developer, QA Engineer, Developer (Final Approval Authority)  
**Applicable Skills:**  
- `skills/bug-fixing/SKILL.md`  
- `skills/code-review/SKILL.md`  
- `skills/project-discovery/SKILL.md`  
- `skills/flutter-development/SKILL.md`  
**Governing Gates:** `implementation`, `testing`, `code_review`, `final_acceptance` (`config/quality-gates.yaml`)  

---

## 1. Purpose & Overview

The `bug_fixing` workflow governs the diagnosis, reproduction, root-cause analysis, surgical remediation, regression testing, and verification of software defects.

Unlike new feature development, defect remediation operates under a disciplined troubleshooting protocol:
- **Defect Intake Without Boilerplate:** Ingests reported issues, error outputs, logs, and reproduction steps into a structured bug report (`REQ-048`).
- **Reproduction First:** Requires deterministic reproduction before modifying any production code (`REQ-049`).
- **Root-Cause Analysis Over Symptoms:** Distinguishes underlying root causes from superficial symptoms, requiring unverified assumptions to be labeled as hypotheses (`REQ-050`).
- **Minimal Fix Discipline:** Restricts code edits to the smallest reasonable fix required to eliminate the root cause, forbidding opportunistic refactoring (`REQ-051`, `REQ-034`).
- **Explicit Approval for Risky Changes:** Enforces developer sign-off before applying fixes that touch database schemas, public APIs, or core architectural layers (`REQ-052`, `SAFE-002`, `SAFE-008`).
- **Mandatory Regression Coverage:** Mandates adding or updating automated regression tests to permanently prevent defect recurrence (`REQ-053`).
- **Deterministic Verification:** Verifies fixes with actual test executions and observed outputs, barring unsubstantiated claims (`REQ-054`, `SAFE-009`).
- **Honest Accounting of Limitations:** Forbids claiming an unreproduced defect is resolved without explicit documented limitations and developer consent (`REQ-055`).
- **Working Tree Integrity:** Inspects Git status and safeguards unrelated developer changes before editing (`SAFE-010`).

---

## 2. Prerequisites & Entry Conditions

1. **Trigger:**
   - Developer reports a defect (e.g., *"fix bug in property review submission"*, *"app crashes on null avatar URL"*, or *"reproduce and fix issue BUG-001"*).
   - Defect discovered during QA validation (`workflows/validate-feature.md`).
   - Automated test failure in CI or local test runs.
2. **Input Baseline Check:**
   - Ingest defect details from `.dev-team/features/<feature-slug>/bugs/<bug-id>.md` if existing, or initialize a new defect record conforming to `templates/bug-report.md`.
3. **Working Tree Cleanliness Check (`SAFE-010`):**
   - Execute `git status`.
   - Ensure the working tree is clean or existing uncommitted changes are identified and preserved. Never overwrite user files without explicit authorization.
4. **Project Discovery & Context Inspection:**
   - Inspect target project `AGENTS.md` and `.dev-team/project-profile.yaml` to discover project test runners, coding conventions, and architectural layering.

---

## 3. Quality Gates Enforced

Per `config/quality-gates.yaml` and system safety boundaries:

### Implementation & Safety Gates
- [x] **Reproduction Gate (`REQ-049`):** Attempt defect reproduction and record evidence before modifying production code.
- [x] **Minimal Scope Gate (`REQ-051`, `REQ-034`):** Surgical fix only; opportunistic refactoring or styling rewrites are strictly prohibited.
- [x] **Risky Fix Approval Gate (`REQ-052`, `SAFE-002`, `SAFE-008`):** Architectural, database schema, or public contract changes require explicit developer sign-off.
- [x] **Working Tree Gate (`SAFE-010`):** Verify `git status` before file modifications and preserve unrelated work.

### Testing & Verification Gates
- [x] **Regression Coverage Gate (`REQ-053`):** An automated regression test must be added or updated, or an explicit justification documented for untestable environments.
- [x] **Deterministic Output Gate (`REQ-054`, `SAFE-009`):** Command executions, test counts, and exit codes must be captured directly from shell output.
- [x] **Unreproduced Fix Prohibition Gate (`REQ-055`):** A defect cannot be marked as resolved if it was never reproduced, unless environmental limitations are documented and accepted by the developer.

### Final Acceptance Gate
- [x] **Developer Sign-off Gate (`SAFE-001`, `REQ-047`):** Final resolution and defect closure require developer review.

---

## 4. Execution Sequence

```mermaid
flowchart TD
    A[Start: Defect Reported / Intake] --> B[Phase 1: Ingest & Initialize Bug Report]
    B --> C[Phase 2: Systematic Reproduction (REQ-049)]
    C --> D{Reproduced Successfully?}
    D -->|No: Unreproducible| E[Document Limitations & Request Details (REQ-055, SAFE-012)]
    D -->|Yes: Reproduced| F[Phase 3: Root-Cause Investigation & Hypothesis Labeling (REQ-050)]
    F --> G[Phase 4: Minimal Fix Planning & Risk Assessment]
    G --> H{Risky or Architectural Fix?}
    H -->|Yes| I[Halt: Request Developer Approval (REQ-052, SAFE-002)]
    H -->|No| J[Phase 5: Implement Minimal Surgical Fix (REQ-051)]
    I -->|Approved| J
    I -->|Rejected| G
    J --> K[Phase 6: Create or Update Regression Test (REQ-053)]
    K --> L[Phase 7: Deterministic Validation (REQ-054, SAFE-009)]
    L --> M{All Tests & Checks Pass?}
    M -->|Failures / Errors| J
    M -->|Passed| N[Phase 8: Independent Verification & Sign-Off Gate]
    N --> O[End: Defect Resolved & Documented]
```

### Phase 1: Ingest & Initialize Bug Report (`REQ-048`)
1. Create or open `.dev-team/features/<feature-slug>/bugs/<bug-id>.md` (or `.dev-team/bugs/<bug-id>.md`) using `templates/bug-report.md`.
2. Populate initial metadata: Bug ID, title, environment details, expected behavior, actual behavior, and reporter notes.
3. Keep unknown fields optional; do not halt for missing optional information.
4. Set status to `INVESTIGATING`.

### Phase 2: Systematic Reproduction (`REQ-049`, `REQ-055`)
*Do not alter application code in this phase.*
1. Review the reported reproduction steps and trigger conditions.
2. Attempt to trigger the failure deterministically:
   - Prefer writing a small failing unit/widget test in `test/` reproducing the exact failure scenario, or
   - Execute the CLI command, script, or workflow triggering the error.
3. Record findings in `bug-report.md`:
   - If reproduced: Set status to `REPRODUCED`. Capture the exact error log, failing assertion, and stack trace in Section 2.4.
   - If not reproduced: Set status to `UNREPRODUCIBLE`. Document what steps were attempted, differences in environment, and pause to ask the developer for missing reproduction details (`SAFE-012`). Do not mark as resolved (`REQ-055`).

### Phase 3: Root-Cause Investigation & Hypothesis Labeling (`REQ-050`)
1. Trace the execution path from symptom to root cause.
2. Clearly separate symptoms (what failed) from the underlying defect (why it failed):
   - Document symptoms and root causes in Section 3.1 of `bug-report.md`.
3. Label diagnostic assumptions:
   - Mark unconfirmed theories as `[HYPOTHESIS]`.
   - Update to `[CONFIRMED ROOT CAUSE]` once verified via code inspection, debugger, or test assertion.
4. Pinpoint exact files, classes, and line numbers responsible for the defect.
5. Classify defect severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, or `TRIVIAL`.

### Phase 4: Minimal Fix Planning & Risk Assessment (`REQ-051`, `REQ-052`)
1. Design the smallest surgical modification to eliminate the confirmed root cause.
2. Actively eliminate unnecessary changes:
   - No opportunistic code formatting of untouched lines.
   - No unsolicited renaming, refactoring, or restructuring.
   - No newly added third-party dependencies unless strictly required and approved.
3. Evaluate fix risk:
   - **Low Risk:** Localized fix within existing method boundaries; fully verifiable via existing tests.
   - **High Risk:** Changes shared database schemas, alters public API signatures, affects core architecture, or modifies shared state structures.
4. *Approval Gate (`SAFE-002`, `SAFE-008`, `REQ-052`):*
   - If classified as **High Risk**, pause execution immediately.
   - Present the proposed fix, architectural rationale, and regression risks to the developer.
   - Require explicit developer approval before modifying files.

### Phase 5: Implement Minimal Surgical Fix (`REQ-033`, `REQ-051`)
1. Check `git status` to ensure working tree safety (`SAFE-010`).
2. Update bug report status to `FIX_IN_PROGRESS`.
3. Apply the targeted fix strictly to the identified target files.
4. Adhere to target project conventions (Clean Architecture, BLoC/Riverpod, naming conventions, error handling).

### Phase 6: Create or Update Regression Test (`REQ-053`)
*Mandatory verification protection against defect recurrence.*
1. If a reproducing test was created in Phase 2, verify that it transitions from failing to passing with the fix applied.
2. If not already created, implement an automated regression test:
   - Add unit or widget test asserting the previously broken condition.
   - Include test case in the appropriate `test/` subdirectory.
   - Document the test file path and test description in Section 5 of `bug-report.md`.
3. If automated testing is technically impractical:
   - Document the explicit justification (e.g. requires native physical camera or third-party webview).
   - Document explicit manual regression verification steps.

### Phase 7: Deterministic Validation (`REQ-054`, `SAFE-009`)
1. Execute the regression test and project test suite:
   ```bash
   # Flutter example
   flutter test test/path/to/regression_test.dart
   ```
2. Execute static analysis and formatting verification:
   ```bash
   flutter analyze --no-fatal-infos
   dart format --output=none --set-exit-if-changed lib/ test/
   ```
3. Capture actual outputs:
   - Command line invoked.
   - Exit code (`0` required).
   - Observed stdout/stderr summary.
4. If checks fail:
   - Do not claim success.
   - Return to Phase 5 to refine the fix.
5. If all checks pass:
   - Record tangible evidence in Section 6 of `bug-report.md`.
   - Update defect status to `VERIFIED`.

### Phase 8: Independent Verification & Sign-Off Gate (`REQ-047`, `SAFE-001`)
1. Conduct independent review using `skills/code-review/SKILL.md` to ensure:
   - No regressions or performance leaks were introduced.
   - Fix remains surgical and minimal.
2. Complete Section 7 of `bug-report.md` with final determination (`RESOLVED`).
3. Present the remediation report and observed test evidence to the developer for final sign-off.

---

## 5. Escalation & Remediation Routing

| Scenario | Workflow Action | Governing Rule |
|---|---|---|
| **Defect is unreproducible** | Document attempted setups, set status to `UNREPRODUCIBLE`, request developer input. Never mark as fixed without explicit consent. | `REQ-055`, `SAFE-012` |
| **Fix requires schema or architectural change** | Halt at Phase 4 approval gate, present impact analysis to developer, await explicit sign-off before proceeding. | `REQ-052`, `SAFE-002`, `SAFE-008` |
| **Fix causes regression in existing tests** | Immediately revert or refine fix in Phase 5; do not modify existing tests to accommodate broken behavior without authorization. | `SAFE-004`, `REQ-041` |
| **Working tree has uncommitted user changes** | Halt and inspect `git status`; warn developer before modifying any file with pending changes. | `SAFE-010` |
| **Test runner unavailable or failing in environment** | Explicitly log test limitation in `bug-report.md`; never invent a passing test result. | `SAFE-009`, `REQ-043` |

