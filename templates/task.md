# Task Specification: [Task ID] — [Task Title]

**Task ID:** `[M<milestone_number>-T<task_number>]` <!-- e.g. M1-T01 -->  
**Title:** [Action-oriented task title]  
**Feature:** `[feature-slug]`  
**Milestone:** `[Milestone ID — Milestone Title]`  
**Status:** PENDING <!-- Allowed: PENDING, IN_PROGRESS, BLOCKED, COMPLETED, NEEDS_REVIEW -->  
**Created Date:** [YYYY-MM-DD]  
**Last Updated:** [YYYY-MM-DD]  
**Assignee:** [Developer / Agent Role]  
**Plan Reference:** `plan.md` (Section [X.X])  

---

## 1. Task Objective & Context

### 1.1 Objective
<!-- Concise 1-2 sentence description of the exact capability, component, or fix this task implements -->
[Describe what this task achieves.]

### 1.2 System Context & Rationale
<!-- How this task connects to system architecture and target application patterns -->
[Explain where this component lives in the architecture and why this step is sequenced here.]

---

## 2. Requirements & Traceability

<!-- Explicitly link this task to approved requirements and system design sections -->

| Item | Reference | Summary |
|---|---|---|
| **Requirement(s)** | `[REQ-xxx]` | [Summary of requirement requirement satisfied] |
| **Architecture Section** | `system-design.md` § [X.X] | [Summary of layer, entity, or service design] |
| **Data Model / Schema** | `system-design.md` § [X.X] | [Table, entity, or contract definition] |

---

## 3. Dependencies & Execution Mode

- **Prerequisite Tasks:**
  - `[None / M<m>-T<nn>]` (Must be in `COMPLETED` status before starting)
- **Downstream Dependent Tasks:**
  - `[M<m>-T<nn>]` (Blocked until this task is completed)
- **Execution Mode:** `[Sequential / Independent]`
  - *Sequential:* Must execute strictly after prerequisites.
  - *Independent:* Can be executed concurrently if prerequisites are met.

---

## 4. Scope & File Targets

<!-- Explicitly declare affected paths to prevent accidental scope expansion or conflicting modifications -->

### Files to Create
- `[path/to/new_file.dart]` — [Purpose of file]
- `[test/path/to/new_file_test.dart]` — [Targeted unit/widget test file]

### Files to Modify
- `[path/to/existing_file.dart]` — [Specific change: e.g., export new model, register dependency]

### Files to Inspect / Reference
- `[path/to/reference_implementation.dart]` — [Existing pattern or base class to replicate]

### Explicit Exclusions (Out of Scope)
- Do NOT modify [unrelated components or downstream UI].
- Do NOT perform unsolicited refactoring outside the targeted files.

---

## 5. Implementation Guidance

<!-- Actionable procedural notes for the developer or implementing agent -->
1. **Design Pattern Alignment:** Follow project conventions discovered in `.dev-team/project-profile.yaml`.
2. **Interface Contract:** [Specify function signatures, class interfaces, or contracts to implement].
3. **Error Handling:** Follow project error handling guidelines (e.g., custom exceptions, Result types, failure states).
4. **Clean Code & Comments:** Preserve documentation integrity and existing comments.

---

## 6. Deliverables

- [ ] New source file(s) implemented and properly exported.
- [ ] Comprehensive automated test file covering success, failure, and edge cases.
- [ ] Clean static analysis output with zero warnings or errors.

---

## 7. Acceptance Criteria

<!-- Verifiable, unambiguous conditions required to mark this task COMPLETED -->
- [ ] Acceptance criterion 1: [Condition].
- [ ] Acceptance criterion 2: [Condition].
- [ ] Edge case handling verified: [Empty state / null handling / invalid input].
- [ ] Code strictly follows repository conventions and passes all linters.
- [ ] All automated tests for this task pass deterministically.

---

## 8. Deterministic Validation Procedure

<!-- Concrete commands to execute. NEVER claim a pass without running them and observing output (SAFE-009) -->

```bash
# Step 1: Format and linting verification
[e.g., flutter analyze lib/features/path/to/file.dart]

# Step 2: Automated test execution
[e.g., flutter test test/features/path/to/file_test.dart]

# Step 3: Build runner / code generation (if applicable)
[e.g., dart run build_runner build --delete-conflicting-outputs]
```

**Expected Result:**
- Exit code: 0
- Output: Zero errors, zero warnings, all test cases passing.

---

## 9. Execution Log & Evidence

<!-- Update during and after implementation as tangible proof of execution (SAFE-009) -->

### 9.1 State Transitions
- **`PENDING`** → `IN_PROGRESS` on [YYYY-MM-DD HH:MM]
- **`IN_PROGRESS`** → `[COMPLETED / BLOCKED]` on [YYYY-MM-DD HH:MM]

### 9.2 Validation Evidence
```text
[Paste actual command execution output here showing tests passed]
```

### 9.3 Modified Files
- `[path/to/created_or_modified_file]`

---

## 10. Blocker & Replanning Escalation (REQ-030)

<!-- Complete ONLY if task becomes BLOCKED during execution -->

- **Blocker Encountered:** [None / Detailed description of obstacle]
- **Category:** [Architecture Flaw / Requirement Gap / External Dependency / Broken Test]
- **Action Taken:** Task paused; escalated to developer.
- **Resolution / Decision:** [Document developer guidance prior to unblocking]

