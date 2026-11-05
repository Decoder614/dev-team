# QA & Feature Validation Report: [Feature Name]

**Document Type:** Quality Assurance & Feature Validation Report  
**Feature ID:** `[feature-slug]`  
**Project:** `[Target Project Name]`  
**Status:** DRAFT <!-- Allowed: DRAFT, IN_REVIEW, APPROVED, NEEDS_REVISION, SUPERSEDED -->  
**Version:** 1.0  
**Review Date:** [YYYY-MM-DD]  
**Lead QA Reviewer:** [QA Engineer / Reviewer Name]  
**Developer Sign-off:** [Developer Name] (Pending Final Acceptance)  
**Based On:**
- `requirement.md` — Approved ([Version], [Approval Date])
- `system-design.md` — Approved ([Version], [Approval Date])
- `plan.md` — Approved ([Version], [Approval Date])

---

## 1. Executive Summary

### 1.1 Review Determination
<!-- Select exactly one outcome: APPROVED, APPROVED_WITH_FOLLOW_UPS, or NEEDS_REVISION -->
**Overall Determination:** `[APPROVED | APPROVED_WITH_FOLLOW_UPS | NEEDS_REVISION]`

<!-- Summary of evaluation outcome and readiness for production / developer acceptance -->
[Provide a 1-2 paragraph executive summary explaining the overall assessment, state of requirements coverage, testing outcomes, and justification for the determination.]

### 1.2 Quality Metrics Summary

| Metric | Target | Actual Result | Status |
|---|---|---|---|
| **Mandatory Requirements Coverage** | 100% | `[X%]` (`[M / N]` criteria) | `[PASS / FAIL]` |
| **Blocker / Critical Defects** | 0 | `[Count]` | `[PASS / FAIL]` |
| **Major Defects** | 0 | `[Count]` | `[PASS / WARN / FAIL]` |
| **Minor / Trivial Suggestions** | N/A | `[Count]` | `[INFO]` |
| **Automated Tests Executed** | All applicable | `[Count]` executed (`[Count]` passed) | `[PASS / FAIL]` |
| **Static Analysis / Linter Errors** | 0 | `[Count]` errors, `[Count]` warnings | `[PASS / FAIL]` |
| **Code Formatting Status** | Clean | `[Clean / Out of sync]` | `[PASS / FAIL]` |

---

## 2. Review Scope & Context

### 2.1 Artifacts & Commit Baseline Evaluated

| Item | Details |
|---|---|
| **Feature Slug / Directory** | `.dev-team/features/[feature-slug]/` |
| **Git Baseline / Target Branch** | `[master / main]` |
| **Feature Branch / Commit Hash** | `[feature/branch-name @ abc1234]` |
| **Implementation Tasks Evaluated** | `[e.g., M1-T01 through M3-T04]` |

### 2.2 Files Modified / Inspected
<!-- List the core source and test files verified during this QA review -->
- `lib/features/[feature-slug]/presentation/...`
- `lib/features/[feature-slug]/domain/...`
- `lib/features/[feature-slug]/data/...`
- `test/features/[feature-slug]/...`

---

## 3. Requirements Coverage Matrix

<!-- Evaluates every mandatory functional (REQ) and non-functional (NFR) acceptance criterion from requirement.md -->
<!-- Verification Status must be one of: VERIFIED, PARTIAL, UNMET, UNVERIFIED -->

| Req ID | Acceptance Criterion | Implementing Task | Verification Method | Status | Evidence / Test Reference |
|---|---|---|---|---|---|
| `REQ-001` | [Acceptance criterion 1 description] | `M1-T01` | Automated Unit Test | `VERIFIED` | `test/.../auth_repository_test.dart:42` |
| `REQ-002` | [Acceptance criterion 2 description] | `M1-T02` | Widget Test | `VERIFIED` | `test/.../login_screen_test.dart:78` |
| `REQ-003` | [Acceptance criterion 3 description] | `M2-T01` | Static Inspection | `PARTIAL` | Edge case for offline mode not covered |
| `REQ-004` | [Acceptance criterion 4 description] | `M2-T02` | Automated Test | `UNMET` | Validation fails on null email input |
| `NFR-001` | [Performance / Security criterion] | `M3-T01` | Static Analyzer | `VERIFIED` | Zero leaks observed; analyzer clean |
| `NFR-002` | [Native hardware / Push notification] | `M3-T02` | Manual Simulation | `UNVERIFIED` | Physical device test unavailable |

---

## 4. Multi-Dimensional Code Review Findings

<!-- Evaluates the 8 dimensions defined in skills/code-review/SKILL.md -->
<!-- Severity: BLOCKER, CRITICAL, MAJOR, MINOR, TRIVIAL -->

### 4.1 Findings Summary Table

| Finding ID | Severity | Dimension | File Location | Summary Description |
|---|---|---|---|---|
| `FIND-001` | `[Severity]` | `[Dimension]` | `[lib/path/to/file.dart:line]` | `[Brief title / summary]` |
| `FIND-002` | `[Severity]` | `[Dimension]` | `[lib/path/to/file.dart:line]` | `[Brief title / summary]` |

### 4.2 Detailed Finding Descriptions

#### Finding `FIND-001`: [Finding Title]
- **Severity:** `[BLOCKER | CRITICAL | MAJOR | MINOR | TRIVIAL]`
- **Dimension:** `[Correctness | Maintainability | Security | Performance | Data Integrity | Error Handling | Regression | Conventions]`
- **Location:** `[filepath]:[line_number_or_range]`
- **Traceability:** Associated Requirement `[REQ-xxx]` / Task `[M<m>-T<nn>]`
- **Description:** [Clear explanation of the defect, why it occurs, and its operational risk.]
- **Evidence / Reproduction:**
  ```text
  [Insert terminal log, reproduction steps, or code snippet showing the issue]
  ```
- **Actionable Remediation:**
  [Specify exact code change or architectural fix required.]

---

## 5. Test Execution Log

<!-- Records deterministic commands executed, actual outputs, and exit codes per SAFE-009, REQ-042, REQ-043 -->

| Command Invoked | Purpose | Exit Code | Outcome | Tangible Output Summary |
|---|---|---|---|---|
| `dart format --output=none --set-exit-if-changed .` | Code style & formatting | `0` | `PASSED` | All source files formatted cleanly |
| `flutter analyze --no-fatal-infos` | Static type & lint analysis | `0` | `PASSED` | 0 issues found |
| `flutter test test/features/[feature-slug]/` | Feature unit & widget test suite | `0` | `PASSED` | All 18 tests passed |
| `flutter test integration_test/` | Hardware / End-to-end suite | `N/A` | `SKIPPED` | No physical emulator attached (Unverified) |

### 5.1 Test Failure Output Details (if any)
```text
[Insert failing test output, stack trace, or compiler error if any test failed]
```

---

## 6. Unverified Areas & Environmental Limitations

<!-- Enforces REQ-043: Distinguish verified results from checks that could not be run -->

The following areas, platforms, or integrations could **not** be verified in this evaluation session:

| Unverified Area / Capability | Reason for Inability to Verify | Associated Req / Component | Residual Risk | Recommended Follow-up Action |
|---|---|---|---|---|
| `[e.g., Physical Biometric Sensor]` | No hardware device connected in CI/local shell | `REQ-008` / `BiometricAuthService` | Runtime crash on unsupported devices | Developer manual test on physical Android/iOS device prior to release |
| `[e.g., Live Payment Webhook]` | Requires public internet tunneling | `REQ-012` / `StripeWebhookHandler` | Payload format mismatch | Verify payload against Stripe CLI mock webhook in staging |

---

## 7. Remaining Issues & Blockers

<!-- Complete list of open defects or architectural discrepancies preventing immediate release -->

- [ ] **Issue 1:** `[Description of blocker or critical defect]` (Finding ID: `FIND-xxx`)
- [ ] **Issue 2:** `[Description of unmet mandatory acceptance criterion]` (Req ID: `REQ-xxx`)

---

## 8. Final Recommendation & Developer Acceptance Gate

<!-- Enforces SAFE-001 and REQ-047: Developer makes the final acceptance decision -->

### 8.1 QA Recommendation
- [ ] **Ready for Final Developer Acceptance:** All acceptance criteria verified; zero blocker/critical issues; static analysis and test suites pass.
- [ ] **Conditionally Acceptable:** Minor follow-ups recorded; no blockers; developer review required for follow-up scheduling.
- [ ] **Needs Revision:** Blocker or critical defects found, or mandatory acceptance criteria unmet. Returned to Developer role for remediation.

### 8.2 Developer Acceptance Sign-off
<!-- Mandatory sign-off block for developer review -->

| Decision | Developer Name | Signature / Confirmation Date | Notes / Conditions |
|---|---|---|---|
| `[ACCEPTED / REJECTED / CHANGES_REQUESTED]` | `[Developer Name]` | `[YYYY-MM-DD]` | `[Sign-off remarks]` |

