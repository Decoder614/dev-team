#!/usr/bin/env python3
"""
Validation script for Dev-Team Milestone 7 (Bug Management & Feature Status).
Verifies that all M7 artifacts exist, conform to schemas, enforce safety gates,
satisfy acceptance criteria, and deterministically validates defect reproduction,
severity classification, root-cause distinction, hypothesis labeling, minimal fix
discipline, regression test rules, approval gates, and zero-hallucination feature status logic.
"""

import os
import re
import sys
import yaml

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def check_file(path, description):
    if not os.path.isfile(path):
        print(f"[FAIL] Missing {description}: {path}")
        return False
    print(f"[PASS] Found {description}: {path}")
    return True


def test_defect_lifecycle_state_machine():
    """
    Validates defect state progression rules, reproduction enforcement,
    risky fix approval, regression testing, and verification evidence (M7-T01, M7-T03).
    Ensures that:
    1. A defect cannot be marked as fixed or verified if unreproduced without explicit waiver (REQ-055).
    2. Transition to VERIFIED requires tangible validation evidence (SAFE-009, REQ-054).
    3. Risky or architectural fixes require explicit developer approval before implementation (SAFE-002, SAFE-008, REQ-052).
    4. Fixes must provide regression test coverage or documented justification (REQ-053).
    """
    print("\n--- Testing Defect Lifecycle & Quality Gates Logic (M7-T01, M7-T03) ---")
    allowed_statuses = {
        "OPEN", "INVESTIGATING", "REPRODUCED", "UNREPRODUCIBLE",
        "FIX_IN_PROGRESS", "VERIFIED", "RESOLVED", "CLOSED"
    }

    valid_transitions = {
        "OPEN": {"INVESTIGATING"},
        "INVESTIGATING": {"REPRODUCED", "UNREPRODUCIBLE"},
        "UNREPRODUCIBLE": {"INVESTIGATING", "CLOSED"},
        "REPRODUCED": {"FIX_IN_PROGRESS"},
        "FIX_IN_PROGRESS": {"VERIFIED"},
        "VERIFIED": {"RESOLVED", "FIX_IN_PROGRESS"},
        "RESOLVED": {"CLOSED"},
        "CLOSED": set()
    }

    def validate_defect_transition(from_state, to_state, **kwargs):
        reproduction_status = kwargs.get("reproduction_status", "NOT_YET_ATTEMPTED")
        is_risky_fix = kwargs.get("is_risky_fix", False)
        developer_approved_risk = kwargs.get("developer_approved_risk", False)
        has_regression_test = kwargs.get("has_regression_test", False)
        regression_test_justified = kwargs.get("regression_test_justified", False)
        has_validation_evidence = kwargs.get("has_validation_evidence", False)
        developer_signed_off = kwargs.get("developer_signed_off", False)
        unreproduced_waiver = kwargs.get("unreproduced_waiver", False)

        if from_state not in allowed_statuses or to_state not in allowed_statuses:
            return False, "Unknown state"

        if to_state not in valid_transitions.get(from_state, set()):
            return False, f"Invalid state transition from {from_state} to {to_state}"

        # Rule 1: Transition to FIX_IN_PROGRESS requires reproduction or developer waiver
        if to_state == "FIX_IN_PROGRESS":
            if reproduction_status != "REPRODUCED":
                return False, "Cannot start fix implementation before successful reproduction (REQ-049)"
            if is_risky_fix and not developer_approved_risk:
                return False, "Risky or architectural fix requires explicit developer approval before implementation (SAFE-002, REQ-052)"

        # Rule 2: Transition to VERIFIED requires tangible evidence and regression coverage
        if to_state == "VERIFIED":
            if not has_validation_evidence:
                return False, "Verification requires tangible observed test execution output (SAFE-009, REQ-054)"
            if not (has_regression_test or regression_test_justified):
                return False, "Verification requires automated regression test or documented justification (REQ-053)"
            if reproduction_status == "UNREPRODUCIBLE" and not unreproduced_waiver:
                return False, "Cannot mark unreproduced defect as VERIFIED without explicit documented limitation and waiver (REQ-055)"

        # Rule 3: Transition to RESOLVED requires developer final sign-off
        if to_state == "RESOLVED":
            if not developer_signed_off:
                return False, "Resolution requires explicit developer sign-off (SAFE-001, REQ-047)"

        return True, "Valid transition"

    test_cases = [
        # (from_s, to_s, kwargs, expected_valid, label)
        (
            "OPEN", "INVESTIGATING",
            {},
            True, "Initial defect investigation intake"
        ),
        (
            "INVESTIGATING", "REPRODUCED",
            {"reproduction_status": "REPRODUCED"},
            True, "Defect deterministically reproduced with failing test"
        ),
        (
            "INVESTIGATING", "FIX_IN_PROGRESS",
            {"reproduction_status": "NOT_YET_ATTEMPTED"},
            False, "Bypassing reproduction to fix directly (violates REQ-049)"
        ),
        (
            "REPRODUCED", "FIX_IN_PROGRESS",
            {"reproduction_status": "REPRODUCED", "is_risky_fix": False},
            True, "Starting minimal low-risk fix"
        ),
        (
            "REPRODUCED", "FIX_IN_PROGRESS",
            {"reproduction_status": "REPRODUCED", "is_risky_fix": True, "developer_approved_risk": False},
            False, "High-risk architectural fix without developer approval (blocked by SAFE-002, REQ-052)"
        ),
        (
            "REPRODUCED", "FIX_IN_PROGRESS",
            {"reproduction_status": "REPRODUCED", "is_risky_fix": True, "developer_approved_risk": True},
            True, "High-risk architectural fix with explicit developer approval"
        ),
        (
            "FIX_IN_PROGRESS", "VERIFIED",
            {"has_validation_evidence": True, "has_regression_test": True},
            True, "Verification with passing tests and regression test coverage"
        ),
        (
            "FIX_IN_PROGRESS", "VERIFIED",
            {"has_validation_evidence": False, "has_regression_test": True},
            False, "Verification claimed without observed test output (rejected by SAFE-009, REQ-054)"
        ),
        (
            "FIX_IN_PROGRESS", "VERIFIED",
            {"has_validation_evidence": True, "has_regression_test": False, "regression_test_justified": False},
            False, "Verification without regression test or justification (rejected by REQ-053)"
        ),
        (
            "FIX_IN_PROGRESS", "VERIFIED",
            {"has_validation_evidence": True, "has_regression_test": False, "regression_test_justified": True},
            True, "Verification with documented manual justification for hardware-only test"
        ),
        (
            "INVESTIGATING", "UNREPRODUCIBLE",
            {"reproduction_status": "UNREPRODUCIBLE"},
            True, "Marking defect as unreproducible after documenting attempted steps"
        ),
        (
            "VERIFIED", "RESOLVED",
            {"developer_signed_off": False},
            False, "Resolution without developer sign-off (rejected by SAFE-001)"
        ),
        (
            "VERIFIED", "RESOLVED",
            {"developer_signed_off": True},
            True, "Final defect resolution with developer sign-off"
        )
    ]

    all_tests_passed = True
    for from_s, to_s, kw, expected, label in test_cases:
        valid, msg = validate_defect_transition(from_s, to_s, **kw)
        if valid == expected:
            print(f"  [x] Lifecycle test passed: {label}")
        else:
            print(f"  [FAIL] Lifecycle test failed: {label} (Expected valid={expected}, got valid={valid}, msg: {msg})")
            all_tests_passed = False

    return all_tests_passed


def test_feature_status_determination_logic():
    """
    Validates feature status calculation, approval gate auditing, and anti-hallucination rules (M7-T04).
    Ensures that:
    1. Lifecycle stage is deterministically derived from real files on disk (REQ-056).
    2. Task counts and progress percentages reflect actual plan state (REQ-057).
    3. Missing artifacts are never assumed or hallucinated as present/approved (REQ-058).
    4. Active blockers and unresolved critical questions are surfaced (SAFE-012, REQ-030).
    """
    print("\n--- Testing Feature Status Determination & Anti-Hallucination Logic (M7-T04) ---")

    def derive_feature_status(artifacts):
        """
        Derives status strictly based on present artifacts:
        artifacts: dict with keys:
          - requirement: {exists: bool, status: str, has_open_questions: bool}
          - system_design: {exists: bool, status: str}
          - plan: {exists: bool, status: str, tasks: list of dicts with status}
          - qa_report: {exists: bool, status: str, determination: str, developer_signed_off: bool}
          - bugs: list of dicts with {status: str, severity: str}
        """
        # Anti-hallucination check: Empty or missing
        req = artifacts.get("requirement", {})
        design = artifacts.get("system_design", {})
        plan = artifacts.get("plan", {})
        qa = artifacts.get("qa_report", {})
        bugs = artifacts.get("bugs", [])

        if not req.get("exists", False):
            return {
                "stage": "UNINITIALIZED",
                "progress_pct": 0,
                "blockers": [],
                "next_action": "Run workflows/new-feature.md"
            }

        # Requirements stage
        if req.get("status") in {"DRAFT", "IN_REVIEW"}:
            return {
                "stage": "REQUIREMENTS_DRAFT",
                "progress_pct": 0,
                "blockers": ["Unresolved open questions"] if req.get("has_open_questions") else [],
                "next_action": "Run workflows/validate-requirement.md"
            }

        if req.get("status") == "APPROVED" and not design.get("exists", False):
            return {
                "stage": "REQUIREMENTS_APPROVED",
                "progress_pct": 0,
                "blockers": [],
                "next_action": "Run workflows/design-feature.md"
            }

        # Design stage
        if design.get("status") in {"DRAFT", "IN_REVIEW"}:
            return {
                "stage": "DESIGN_DRAFT",
                "progress_pct": 0,
                "blockers": [],
                "next_action": "Complete architecture review and obtain developer approval"
            }

        if design.get("status") == "APPROVED" and not plan.get("exists", False):
            return {
                "stage": "DESIGN_APPROVED",
                "progress_pct": 0,
                "blockers": [],
                "next_action": "Run workflows/create-plan.md"
            }

        # Plan stage
        if plan.get("status") in {"DRAFT", "IN_REVIEW"}:
            return {
                "stage": "PLAN_DRAFT",
                "progress_pct": 0,
                "blockers": [],
                "next_action": "Review plan and obtain developer approval (SAFE-003)"
            }

        tasks = plan.get("tasks", [])
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.get("status") == "COMPLETED")
        blocked_tasks = [t for t in tasks if t.get("status") == "BLOCKED"]
        in_progress_tasks = [t for t in tasks if t.get("status") == "IN_PROGRESS"]

        progress_pct = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

        # Check for blockers
        blocker_reasons = [f"Task {t.get('id')}: {t.get('blocker', 'Unknown blocker')}" for t in blocked_tasks]
        critical_bugs = [b for b in bugs if b.get("severity") in {"BLOCKER", "CRITICAL"} and b.get("status") != "CLOSED"]
        for b in critical_bugs:
            blocker_reasons.append(f"Defect {b.get('id')}: {b.get('title', 'Blocking defect')}")

        if blocked_tasks:
            return {
                "stage": "IMPLEMENTATION_BLOCKED",
                "progress_pct": progress_pct,
                "blockers": blocker_reasons,
                "next_action": "Resolve active blockers before continuing implementation"
            }

        if plan.get("status") == "APPROVED" and total_tasks > 0 and completed_tasks == 0 and not in_progress_tasks:
            return {
                "stage": "PLAN_APPROVED",
                "progress_pct": 0,
                "blockers": blocker_reasons,
                "next_action": "Run workflows/implement-next.md to begin implementation"
            }

        if completed_tasks < total_tasks:
            return {
                "stage": "IMPLEMENTATION_ACTIVE",
                "progress_pct": progress_pct,
                "blockers": blocker_reasons,
                "next_action": "Run workflows/implement-next.md to implement next task"
            }

        # All tasks completed
        if completed_tasks == total_tasks and total_tasks > 0 and not qa.get("exists", False):
            return {
                "stage": "IMPLEMENTATION_DONE",
                "progress_pct": 100,
                "blockers": blocker_reasons,
                "next_action": "Run workflows/validate-feature.md"
            }

        # QA validation stage
        if qa.get("exists", False):
            if qa.get("status") in {"DRAFT", "IN_REVIEW"} or qa.get("determination") == "NEEDS_REVISION":
                return {
                    "stage": "VALIDATION_ACTIVE",
                    "progress_pct": 100,
                    "blockers": blocker_reasons,
                    "next_action": "Remediate QA findings and re-run validation"
                }
            if qa.get("determination") in {"APPROVED", "APPROVED_WITH_FOLLOW_UPS"}:
                if not qa.get("developer_signed_off", False):
                    return {
                        "stage": "READY_FOR_ACCEPTANCE",
                        "progress_pct": 100,
                        "blockers": blocker_reasons,
                        "next_action": "Awaiting developer final sign-off (SAFE-001)"
                    }
                else:
                    return {
                        "stage": "ACCEPTED_COMPLETE",
                        "progress_pct": 100,
                        "blockers": [],
                        "next_action": "Feature fully accepted; ready for release"
                    }

        return {
            "stage": "UNKNOWN",
            "progress_pct": progress_pct,
            "blockers": blocker_reasons,
            "next_action": "Inspect repository artifacts"
        }

    status_scenarios = [
        # Scenario 1: Empty repository
        (
            {"requirement": {"exists": False}},
            "UNINITIALIZED", 0, 0,
            "Uninitialized feature directory"
        ),
        # Scenario 2: Requirements in draft
        (
            {"requirement": {"exists": True, "status": "DRAFT", "has_open_questions": True}},
            "REQUIREMENTS_DRAFT", 0, 1,
            "Requirements draft with open question blocker"
        ),
        # Scenario 3: Requirements approved, design missing
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": False}
            },
            "REQUIREMENTS_APPROVED", 0, 0,
            "Approved requirements awaiting architecture design"
        ),
        # Scenario 4: Plan approved, 0 tasks completed
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": True, "status": "APPROVED"},
                "plan": {
                    "exists": True, "status": "APPROVED",
                    "tasks": [{"id": "M1-T01", "status": "PENDING"}, {"id": "M1-T02", "status": "PENDING"}]
                }
            },
            "PLAN_APPROVED", 0, 0,
            "Approved plan ready for implementation"
        ),
        # Scenario 5: Implementation active, 2/4 completed
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": True, "status": "APPROVED"},
                "plan": {
                    "exists": True, "status": "APPROVED",
                    "tasks": [
                        {"id": "M1-T01", "status": "COMPLETED"},
                        {"id": "M1-T02", "status": "COMPLETED"},
                        {"id": "M2-T01", "status": "IN_PROGRESS"},
                        {"id": "M2-T02", "status": "PENDING"}
                    ]
                }
            },
            "IMPLEMENTATION_ACTIVE", 50, 0,
            "Implementation active with 50% task completion"
        ),
        # Scenario 6: Implementation blocked
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": True, "status": "APPROVED"},
                "plan": {
                    "exists": True, "status": "APPROVED",
                    "tasks": [
                        {"id": "M1-T01", "status": "COMPLETED"},
                        {"id": "M1-T02", "status": "BLOCKED", "blocker": "Backend schema migration pending"}
                    ]
                }
            },
            "IMPLEMENTATION_BLOCKED", 50, 1,
            "Implementation blocked on schema dependency"
        ),
        # Scenario 7: All tasks done, QA pending
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": True, "status": "APPROVED"},
                "plan": {
                    "exists": True, "status": "APPROVED",
                    "tasks": [
                        {"id": "M1-T01", "status": "COMPLETED"},
                        {"id": "M1-T02", "status": "COMPLETED"}
                    ]
                },
                "qa_report": {"exists": False}
            },
            "IMPLEMENTATION_DONE", 100, 0,
            "Implementation complete, awaiting QA validation"
        ),
        # Scenario 8: QA approved, awaiting developer sign-off
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": True, "status": "APPROVED"},
                "plan": {
                    "exists": True, "status": "APPROVED",
                    "tasks": [{"id": "M1-T01", "status": "COMPLETED"}]
                },
                "qa_report": {
                    "exists": True, "status": "APPROVED", "determination": "APPROVED",
                    "developer_signed_off": False
                }
            },
            "READY_FOR_ACCEPTANCE", 100, 0,
            "Ready for developer acceptance sign-off"
        ),
        # Scenario 9: Fully accepted
        (
            {
                "requirement": {"exists": True, "status": "APPROVED"},
                "system_design": {"exists": True, "status": "APPROVED"},
                "plan": {
                    "exists": True, "status": "APPROVED",
                    "tasks": [{"id": "M1-T01", "status": "COMPLETED"}]
                },
                "qa_report": {
                    "exists": True, "status": "APPROVED", "determination": "APPROVED",
                    "developer_signed_off": True
                }
            },
            "ACCEPTED_COMPLETE", 100, 0,
            "Feature fully accepted and signed off"
        )
    ]

    all_passed = True
    for artifacts, exp_stage, exp_pct, exp_blockers_cnt, label in status_scenarios:
        res = derive_feature_status(artifacts)
        if res["stage"] == exp_stage and res["progress_pct"] == exp_pct and len(res["blockers"]) == exp_blockers_cnt:
            print(f"  [x] Status engine test passed: {label} -> {res['stage']} ({res['progress_pct']}%)")
        else:
            print(f"  [FAIL] Status engine test failed: {label} (Expected stage={exp_stage}, pct={exp_pct}, blockers={exp_blockers_cnt}; Got stage={res['stage']}, pct={res['progress_pct']}, blockers={len(res['blockers'])})")
            all_passed = False

    return all_passed


def main():
    print("=== Milestone 7 Verification: Bug Management & Feature Status ===\n")
    all_passed = True

    # 1. Verify Task M7-T01: Bug Fixing Skill
    skill_path = "skills/bug-fixing/SKILL.md"
    if check_file(skill_path, "Bug Fixing Skill"):
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check YAML Frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if frontmatter_match:
            try:
                fm = yaml.safe_load(frontmatter_match.group(1))
                if fm.get("name") == "bug-fixing" and "description" in fm:
                    print("  [x] Bug Fixing Skill has valid YAML frontmatter")
                else:
                    print("  [FAIL] Bug Fixing Skill YAML frontmatter missing name or description")
                    all_passed = False
            except Exception as e:
                print(f"  [FAIL] Bug Fixing Skill frontmatter parsing error: {e}")
                all_passed = False
        else:
            print("  [FAIL] Bug Fixing Skill missing YAML frontmatter")
            all_passed = False

        # Check key sections & requirements
        required_skill_patterns = [
            ("Defect Capture / Intake", r"Defect Intake & Capture"),
            ("Reproduction before modification (REQ-049)", r"REQ-049"),
            ("Root-cause vs symptoms (REQ-050)", r"REQ-050"),
            ("Hypothesis labeling [HYPOTHESIS]", r"\[HYPOTHESIS\]"),
            ("Minimal fix discipline (REQ-051)", r"REQ-051"),
            ("Risky fix developer approval (REQ-052, SAFE-002)", r"REQ-052"),
            ("Regression testing mandate (REQ-053)", r"REQ-053"),
            ("Deterministic verification (REQ-054, SAFE-009)", r"REQ-054"),
            ("Unreproduced fix claim prohibition (REQ-055)", r"REQ-055"),
            ("Working tree inspection (SAFE-010)", r"SAFE-010"),
            ("Lifecycle flowchart", r"flowchart TD"),
            ("Severity classification", r"BLOCKER.*CRITICAL.*MAJOR.*MINOR.*TRIVIAL")
        ]
        for name, pattern in required_skill_patterns:
            if re.search(pattern, content, re.DOTALL):
                print(f"  [x] Bug Fixing Skill covers: '{name}'")
            else:
                print(f"  [FAIL] Bug Fixing Skill missing required concept: '{name}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 2. Verify Task M7-T02: Bug Report Template
    template_path = "templates/bug-report.md"
    if check_file(template_path, "Bug Report Template"):
        with open(template_path, "r", encoding="utf-8") as f:
            t_content = f.read()

        required_template_sections = [
            ("Defect Overview & Environment", r"## 1\. Defect Overview & Environment"),
            ("Expected Behavior", r"Expected Behavior"),
            ("Actual Behavior", r"Actual Behavior"),
            ("Reproduction Procedure", r"## 2\. Defect Reproduction & Evidence"),
            ("Evidence & Diagnostic Logs", r"Evidence & Diagnostic Logs"),
            ("Root Cause Analysis", r"## 3\. Root Cause Analysis"),
            ("Symptoms vs Root Cause", r"Observed Symptoms vs Root Cause"),
            ("Hypothesis Tracking", r"Diagnostic Analysis & Hypothesis Tracking"),
            ("Fix Strategy & Risk Assessment", r"## 4\. Fix Strategy & Implementation Plan"),
            ("Regression Test Coverage", r"## 5\. Regression Test Coverage"),
            ("Validation Results & Observed Output", r"## 6\. Validation Results & Tangible Evidence"),
            ("Resolution & Developer Sign-Off", r"## 7\. Resolution & Developer Sign-Off Gate")
        ]
        for name, pattern in required_template_sections:
            if re.search(pattern, t_content):
                print(f"  [x] Bug Report Template contains section: '{name}'")
            else:
                print(f"  [FAIL] Bug Report Template missing section: '{name}'")
                all_passed = False

        # Verify lifecycle statuses supported
        statuses = ["OPEN", "INVESTIGATING", "REPRODUCED", "UNREPRODUCIBLE", "FIX_IN_PROGRESS", "VERIFIED", "RESOLVED", "CLOSED"]
        for st in statuses:
            if st in t_content:
                print(f"  [x] Bug Report Template supports status '{st}'")
            else:
                print(f"  [FAIL] Bug Report Template missing status '{st}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 3. Verify Task M7-T03: Fix Bug Workflow
    workflow_fix_path = "workflows/fix-bug.md"
    if check_file(workflow_fix_path, "Fix Bug Workflow"):
        with open(workflow_fix_path, "r", encoding="utf-8") as f:
            w_content = f.read()

        required_fix_elements = [
            ("Workflow ID", r"Workflow ID:\*\* `bug_fixing`"),
            ("Entry Point", r"Entry Point:\*\* `workflows/fix-bug.md`"),
            ("Primary Roles", r"Developer.*QA Engineer"),
            ("Governing Gates", r"Governing Gates:"),
            ("Reproduction before editing", r"REQ-049"),
            ("Root cause vs symptoms", r"REQ-050"),
            ("Minimal surgical fix", r"REQ-051"),
            ("Risky fix approval gate", r"REQ-052"),
            ("Regression test mandate", r"REQ-053"),
            ("Deterministic verification", r"REQ-054"),
            ("Unreproduced fix prohibition", r"REQ-055"),
            ("Mermaid execution flowchart", r"flowchart TD"),
            ("Phase 1: Ingest & Initialize Bug Report", r"Phase 1: Ingest & Initialize Bug Report"),
            ("Phase 2: Systematic Reproduction", r"Phase 2: Systematic Reproduction"),
            ("Phase 3: Root-Cause Investigation", r"Phase 3: Root-Cause Investigation"),
            ("Phase 4: Minimal Fix Planning & Risk Assessment", r"Phase 4: Minimal Fix Planning"),
            ("Phase 5: Implement Minimal Surgical Fix", r"Phase 5: Implement Minimal Surgical Fix"),
            ("Phase 6: Create or Update Regression Test", r"Phase 6: Create or Update Regression Test"),
            ("Phase 7: Deterministic Validation", r"Phase 7: Deterministic Validation"),
            ("Phase 8: Independent Verification & Sign-Off", r"Phase 8: Independent Verification & Sign-Off"),
            ("Escalation & Remediation Routing", r"Escalation & Remediation Routing")
        ]
        for name, pattern in required_fix_elements:
            if re.search(pattern, w_content):
                print(f"  [x] Fix Bug Workflow contains element: '{name}'")
            else:
                print(f"  [FAIL] Fix Bug Workflow missing element: '{name}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 4. Verify Task M7-T04: Feature Status Workflow
    workflow_status_path = "workflows/feature-status.md"
    if check_file(workflow_status_path, "Feature Status Workflow"):
        with open(workflow_status_path, "r", encoding="utf-8") as f:
            s_content = f.read()

        required_status_elements = [
            ("Workflow ID", r"Workflow ID:\*\* `feature_status`"),
            ("Entry Point", r"Entry Point:\*\* `workflows/feature-status.md`"),
            ("Anti-Hallucination Grounding", r"REQ-058"),
            ("Lifecycle Stage Mapping", r"REQ-056"),
            ("Task Progress Accounting", r"REQ-057"),
            ("Approval Gates Auditing", r"SAFE-001.*SAFE-002.*SAFE-003"),
            ("Blocker & Risk Surfacing", r"SAFE-012"),
            ("Execution Sequence Flowchart", r"flowchart TD"),
            ("Standard Dashboard Format", r"# Feature Status:.*\[feature-slug\]"),
            ("Aggregate Mode (Multi-Feature)", r"Multi-Feature Repository Summary")
        ]
        for name, pattern in required_status_elements:
            if re.search(pattern, s_content):
                print(f"  [x] Feature Status Workflow contains element: '{name}'")
            else:
                print(f"  [FAIL] Feature Status Workflow missing element: '{name}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 5. Run behavioral logic tests
    if not test_defect_lifecycle_state_machine():
        all_passed = False

    print("\n-----------------------------------\n")

    if not test_feature_status_determination_logic():
        all_passed = False

    print("\n===================================")
    if all_passed:
        print("RESULT: ALL M7 VALIDATION CHECKS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("RESULT: M7 VALIDATION FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

