# Defect Report: [BUG-ID] — [Defect Title]

**Document Type:** Defect & Bug Report  
**Bug ID:** `[BUG-xxx]` <!-- e.g., BUG-001 -->  
**Feature Reference:** `[feature-slug / N/A]`  
**Status:** OPEN <!-- Allowed: OPEN, INVESTIGATING, REPRODUCED, UNREPRODUCIBLE, FIX_IN_PROGRESS, VERIFIED, RESOLVED, CLOSED -->  
**Severity:** `[BLOCKER | CRITICAL | MAJOR | MINOR | TRIVIAL]`  
**Date Reported:** [YYYY-MM-DD]  
**Last Updated:** [YYYY-MM-DD]  
**Reporter:** [Developer / Tester / Role]  
**Assignee:** [Developer / Agent Role]  
**Associated Requirements:** `[REQ-xxx / N/A]`  

---

## 1. Defect Overview & Environment

### 1.1 Summary
<!-- Concise 1-2 sentence description of the defect and the failure manifestation -->
[Provide a clear summary of what fails, under what condition, and the immediate impact.]

### 1.2 Environment Details
<!-- Unknown or inapplicable details may remain empty or marked as N/A -->

| Attribute | Value | Notes / Description |
|---|---|---|
| **Operating System** | `[e.g., Windows 11 / macOS 14 / Linux]` | Host system running the test or build |
| **Framework / Language** | `[e.g., Flutter 3.24 / Dart 3.5]` | Core runtime framework |
| **Commit Hash / Branch** | `[e.g., master @ abc1234]` | Baseline git reference |
| **Device / Emulator** | `[Optional: e.g., Pixel 7 API 34 / Chrome / iOS Sim]` | Target runtime platform |
| **Target App Version** | `[Optional: e.g., 1.2.0+42]` | Target application release version |
| **Environment Configuration** | `[Optional: e.g., local mock, staging, prod]` | Backend or configuration environment |

### 1.3 Expected Behavior
<!-- What the software should do according to approved specifications or requirements -->
[Describe the expected, correct application behavior.]

### 1.4 Actual Behavior
<!-- What the software actually does that constitutes a defect -->
[Describe the incorrect behavior, exception, crash, or unexpected state observed.]

---

## 2. Defect Reproduction & Evidence

### 2.1 Reproduction Status
<!-- Allowed: REPRODUCED, UNREPRODUCIBLE, NOT_YET_ATTEMPTED -->
**Current Status:** `[REPRODUCED | UNREPRODUCIBLE | NOT_YET_ATTEMPTED]`

### 2.2 Step-by-Step Reproduction Procedure
<!-- Numbered, deterministic steps to trigger the defect from a clean state -->
1. [Step 1: Initial state or precondition]
2. [Step 2: Specific user action, API call, or CLI invocation]
3. [Step 3: Triggering action that causes the defect]
4. [Observed result at completion of steps]

### 2.3 Reproduction Rate
- **Frequency:** `[100% Deterministic | Intermittent (~X% frequency) | One-off / Environmental]`
- **Preconditions / Triggers:** [State any specific network condition, data setup, or configuration necessary.]

### 2.4 Evidence & Diagnostic Logs
<!-- Paste observed stack traces, terminal outputs, or log records -->

```text
[Insert exact stack trace, error logs, or terminal command failure output here]
```

### 2.5 Unreproducible Notes & Limitations
<!-- Required ONLY if status is UNREPRODUCIBLE. Explain what was tried and what is missing. -->
> [!NOTE]
> [If unreproducible, document the exact configurations attempted, missing emulators/hardware, or external services that prevented reproduction. Defect cannot be marked as fixed while unreproduced without developer approval (REQ-055).]

---

## 3. Root Cause Analysis

### 3.1 Observed Symptoms vs Root Cause
<!-- Distinguish superficial manifestation from underlying software bug (REQ-050) -->

| Perspective | Description |
|---|---|
| **Observed Symptom** | [What the user or test sees, e.g. UI freeze, null error, HTTP 500] |
| **Underlying Root Cause** | [The actual code, data model, or concurrency flaw causing the symptom] |

### 3.2 Diagnostic Analysis & Hypothesis Tracking
<!-- Label unverified diagnostic assumptions as HYPOTHESIS until confirmed by tests/tracing (REQ-050) -->

- **Status:** `[HYPOTHESIS | CONFIRMED]`
- **Analysis Details:**  
  [Explain the technical mechanism causing the defect. If an assumption has not yet been proven through debugger inspection or a failing test, prefix with `[HYPOTHESIS]`. Once proven, prefix with `[CONFIRMED ROOT CAUSE]`.]

### 3.3 Affected Components & Source Locations

| File Path | Line Range | Component / Class | Role in Defect |
|---|---|---|---|
| `[lib/path/to/source_file.dart]` | `L[start]-L[end]` | `[ClassName / FunctionName]` | [Origin of defect / incorrect calculation] |
| `[Optional: lib/path/to/related_file.dart]` | `L[start]-L[end]` | `[ClassName / FunctionName]` | [Propagator of bad state] |

### 3.4 Impact & Regression Scope
<!-- What other areas, modules, or requirements might be impacted by this defect or its fix? -->
- **Affected User Flows:** [List impacted user interactions or background jobs]
- **Affected Requirements:** `[REQ-xxx / N/A]`
- **Security / Privacy Impact:** `[None / Describe any credential or data exposure risk (SAFE-005)]`
- **Data Integrity Impact:** `[None / Describe any potential data corruption or uncommitted state]`

---

## 4. Fix Strategy & Implementation Plan

### 4.1 Minimal Proposed Fix Description
<!-- Enforces REQ-051: Smallest reasonable fix. Forbids opportunistic refactoring. -->
[Describe the minimal, surgical change required to address the confirmed root cause. Do not include unrelated refactoring or style cleanups.]

### 4.2 Risk Assessment & Approval Gate Trigger
<!-- Determine if this fix requires explicit developer approval before modifying code (SAFE-002, SAFE-008, REQ-052) -->

- **Risk Level:** `[LOW | HIGH]`
- **Architectural / Schema Changes:** `[Yes / No]`
- **Public API Contract Changes:** `[Yes / No]`
- **Third-Party Dependency Changes:** `[Yes / No]`

> [!IMPORTANT]
> If Risk Level is **HIGH** (touches shared schemas, changes public APIs, or alters core architecture), developer approval is mandatory before proceeding to code changes (`SAFE-002`, `SAFE-008`, `REQ-052`).

### 4.3 Files to Modify or Create

```text
[lib/path/to/file_to_modify.dart]       # Surgical bug fix
[test/path/to/regression_test.dart]     # Automated regression test
```

### 4.4 Alternatives Considered & Rejected
<!-- Optional: Explain alternative solutions and why the chosen minimal fix was preferred -->
- *Alternative 1:* [Description of alternative approach and why it was rejected, e.g. too broad, risky, or breaks backwards compatibility.]

---

## 5. Regression Test Coverage

<!-- Enforces REQ-053: Add or update regression tests where practical -->

### 5.1 Automated Regression Test Specification

| Property | Details |
|---|---|
| **Test File Path** | `[test/path/to/regression_test.dart]` |
| **Test Case Name** | `[test('should handle edge case without crashing', () { ... })]` |
| **Test Type** | `[Unit Test | Widget Test | Integration Test]` |
| **Failure Mode Without Fix** | [Describes how this test fails when the bug is present] |
| **Passing Assertion** | [Describes the exact expected condition verified by this test] |

### 5.2 Manual Regression Verification (Fallback)
<!-- Only applicable if automated testing is technically impractical. Provide strong justification. -->
- **Justification for Manual Verification:** [Explain why automated regression is impossible, e.g. hardware sensor, external payment portal]
- **Manual Verification Steps:**
  1. [Step 1]
  2. [Step 2]

---

## 6. Validation Results & Tangible Evidence

<!-- Enforces SAFE-009, REQ-054: Require observed command output and exit codes -->

### 6.1 Validation Commands Executed

| Command Executed | Exit Code | Observed Output Summary | Status |
|---|---|---|---|
| `[flutter test test/path/to/regression_test.dart]` | `[0]` | `[All 1 tests passed!]` | `[PASS]` |
| `[flutter analyze --no-fatal-infos]` | `[0]` | `[No issues found!]` | `[PASS]` |
| `[dart format --output=none --set-exit-if-changed ...]` | `[0]` | `[Formatted 2 files (0 changed)]` | `[PASS]` |

### 6.2 Pre-Fix vs Post-Fix Comparison

| State | Behavior Observed | Evidence Reference |
|---|---|---|
| **Pre-Fix (Defect Present)** | [e.g., App crashed with NullPointerException] | Section 2.4 |
| **Post-Fix (Defect Resolved)** | [e.g., Handled fallback gracefully, returned expected model] | Section 6.1 |

### 6.3 Limitations & Unverified Conditions
<!-- Detail any checks or platforms that could not be executed locally (REQ-055) -->
- `[None / List untestable device configurations or mock service limitations]`

---

## 7. Resolution & Developer Sign-Off Gate

### 7.1 Final Resolution State
<!-- Allowed: RESOLVED, UNRESOLVED, BLOCKED, WONT_FIX -->
**Determination:** `[RESOLVED | UNRESOLVED | BLOCKED | WONT_FIX]`

### 7.2 Developer Sign-off Block
<!-- Enforces SAFE-001, REQ-047, REQ-052: Final acceptance remains with developer -->

| Field | Value |
|---|---|
| **Developer Name** | `[Developer Name]` |
| **Sign-off Decision** | `[APPROVED / REJECTED / NEEDS_ADDITIONAL_FIX]` |
| **Sign-off Date** | `[YYYY-MM-DD]` |
| **Commit Reference** | `[Optional: git commit hash resolving the defect]` |
| **Developer Notes** | `[Optional developer comments or acceptance notes]` |

