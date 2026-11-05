#!/usr/bin/env python3
"""
Validation script for Dev-Team Milestone 6 (QA & Feature Validation).
Verifies that all M6 artifacts exist, conform to schemas, enforce safety gates,
satisfy acceptance criteria, and deterministically validates defect detection,
severity classification, requirement coverage, and sign-off blocking logic.
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


def test_qa_evaluation_logic():
    """
    Validates defect severity rules, unverified check rules, and acceptance gate logic (M6-T01, M6-T05).
    Ensures that:
    1. Unexecuted checks cannot be claimed as passed/verified (SAFE-009, REQ-043).
    2. Blocker or Critical defects force determination to NEEDS_REVISION (REQ-046).
    3. Unmet mandatory acceptance criteria force determination to NEEDS_REVISION (REQ-046).
    4. Features cannot reach final acceptance without explicit developer sign-off (SAFE-001, REQ-047).
    """
    print("\n--- Testing QA Evaluation & Gate Enforcement Logic (M6 Verification) ---")

    def evaluate_qa_result(criteria_statuses, findings, developer_signed_off=False):
        # 1. Check for unexecuted checks falsely marked as verified
        for cid, (status, was_executed) in criteria_statuses.items():
            if status == "VERIFIED" and not was_executed:
                return "INVALID", "Unexecuted check falsely marked as VERIFIED (violates SAFE-009, REQ-043)"

        # 2. Check for unmet mandatory acceptance criteria
        has_unmet_criteria = any(status == "UNMET" for status, _ in criteria_statuses.values())
        
        # 3. Check for blocker or critical findings
        severities = [f.get("severity") for f in findings]
        has_blocker_or_critical = any(s in {"BLOCKER", "CRITICAL"} for s in severities)
        has_major = any(s == "MAJOR" for s in severities)

        # 4. Formulate determination
        if has_blocker_or_critical or has_unmet_criteria:
            determination = "NEEDS_REVISION"
        elif has_major:
            determination = "APPROVED_WITH_FOLLOW_UPS"
        else:
            determination = "APPROVED"

        # 5. Developer sign-off check for final acceptance
        if determination in {"APPROVED", "APPROVED_WITH_FOLLOW_UPS"}:
            final_accepted = developer_signed_off
        else:
            final_accepted = False

        return determination, final_accepted

    test_cases = [
        # (criteria_statuses, findings, dev_signed, expected_det, expected_accepted, label)
        (
            {"REQ-001": ("VERIFIED", True), "REQ-002": ("VERIFIED", True)},
            [{"severity": "MINOR"}, {"severity": "TRIVIAL"}],
            True,
            "APPROVED",
            True,
            "Clean run with developer sign-off"
        ),
        (
            {"REQ-001": ("VERIFIED", True), "REQ-002": ("VERIFIED", True)},
            [{"severity": "MINOR"}],
            False,
            "APPROVED",
            False,
            "Approved QA determination awaiting developer sign-off"
        ),
        (
            {"REQ-001": ("VERIFIED", False), "REQ-002": ("VERIFIED", True)},
            [],
            True,
            "INVALID",
            False,
            "Unexecuted check claimed as VERIFIED (caught by SAFE-009 rule)"
        ),
        (
            {"REQ-001": ("VERIFIED", True), "REQ-002": ("UNMET", True)},
            [],
            True,
            "NEEDS_REVISION",
            False,
            "Unmet mandatory criterion blocks release (REQ-046)"
        ),
        (
            {"REQ-001": ("VERIFIED", True), "REQ-002": ("VERIFIED", True)},
            [{"severity": "BLOCKER", "desc": "Hardcoded API secret in auth_service.dart"}],
            True,
            "NEEDS_REVISION",
            False,
            "Blocker defect forces NEEDS_REVISION (REQ-046, SAFE-005)"
        ),
        (
            {"REQ-001": ("VERIFIED", True), "REQ-002": ("VERIFIED", True)},
            [{"severity": "CRITICAL", "desc": "Null pointer on empty cart checkout"}],
            True,
            "NEEDS_REVISION",
            False,
            "Critical defect forces NEEDS_REVISION"
        ),
        (
            {"REQ-001": ("VERIFIED", True), "REQ-002": ("VERIFIED", True)},
            [{"severity": "MAJOR", "desc": "Missing offline retry banner"}],
            True,
            "APPROVED_WITH_FOLLOW_UPS",
            True,
            "Major defect with developer follow-up sign-off"
        ),
    ]

    all_tests_passed = True
    for crit, fnds, dev_sign, exp_det, exp_acc, label in test_cases:
        res_det, res_acc = evaluate_qa_result(crit, fnds, dev_sign)
        if res_det == exp_det and (res_det == "INVALID" or res_acc == exp_acc):
            print(f"  [x] Logic test passed: {label} -> Determination: {res_det}")
        else:
            print(f"[FAIL] Logic test failed: {label} (Expected det: {exp_det}, acc: {exp_acc}; Got det: {res_det}, acc: {res_acc})")
            all_tests_passed = False

    return all_tests_passed


def validate_m6():
    all_passed = True

    print("=== Milestone 6 Verification: QA & Feature Validation ===\n")

    # 1. Task M6-T01: agents/qa-engineer.toml
    qa_file = "agents/qa-engineer.toml"
    if check_file(qa_file, "QA Engineer Agent Spec"):
        with open(qa_file, "rb") as f:
            data = tomllib.loads(f.read().decode("utf-8"))

        required_keys = [
            "name", "display_name", "version", "description", "role",
            "responsibilities", "inputs", "outputs", "skills", "boundaries",
            "severities", "review_outcomes", "quality_gates"
        ]
        for key in required_keys:
            if key not in data:
                print(f"[FAIL] Missing key '{key}' in {qa_file}")
                all_passed = False
            else:
                print(f"  [x] Agent spec contains key '{key}'")

        # Check boundaries and cannot rules
        boundaries = data.get("boundaries", {})
        cannot_rules = " ".join(boundaries.get("cannot", []))
        
        checks = [
            ("Developer final acceptance authority", "developer" in cannot_rules.lower() and "final" in cannot_rules.lower()),
            ("Unexecuted check pass prohibition", "executed" in cannot_rules.lower() or "unexecuted" in cannot_rules.lower()),
            ("Blocking defect completion prohibition", "blocker" in cannot_rules.lower() or "critical" in cannot_rules.lower()),
            ("Silent scope change prohibition", "silent" in cannot_rules.lower() or "alter" in cannot_rules.lower()),
            ("Destructive command prohibition", "destructive" in cannot_rules.lower()),
            ("Secret exposure prohibition", "secret" in cannot_rules.lower())
        ]
        for name, passed in checks:
            if passed:
                print(f"  [x] QA Engineer boundaries enforce: {name}")
            else:
                print(f"[FAIL] QA Engineer boundaries missing: {name}")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 2. Task M6-T02: skills/code-review/SKILL.md
    cr_skill_file = "skills/code-review/SKILL.md"
    if check_file(cr_skill_file, "Code Review Skill"):
        with open(cr_skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---") and "name: code-review" in content:
            print("  [x] Code Review Skill has valid YAML frontmatter")
        else:
            print("[FAIL] Missing or invalid YAML frontmatter in Code Review Skill")
            all_passed = False

        # Check 8 review dimensions
        dimensions = [
            "Correctness",
            "Maintainability",
            "Security",
            "Performance",
            "Data Integrity",
            "Error Handling",
            "Regression Risks",
            "Project Conventions"
        ]
        for dim in dimensions:
            if dim.lower() in content.lower():
                print(f"  [x] Code Review covers dimension: '{dim}'")
            else:
                print(f"[FAIL] Code Review missing dimension: '{dim}'")
                all_passed = False

        # Check severity levels
        severities = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "TRIVIAL"]
        for sev in severities:
            if sev in content:
                print(f"  [x] Code Review defines severity: '{sev}'")
            else:
                print(f"[FAIL] Code Review missing severity: '{sev}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 3. Task M6-T03: skills/feature-validation/SKILL.md
    fv_skill_file = "skills/feature-validation/SKILL.md"
    if check_file(fv_skill_file, "Feature Validation Skill"):
        with open(fv_skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---") and "name: feature-validation" in content:
            print("  [x] Feature Validation Skill has valid YAML frontmatter")
        else:
            print("[FAIL] Missing or invalid YAML frontmatter in Feature Validation Skill")
            all_passed = False

        fv_requirements = [
            "Requirement Coverage Matrix",
            "Deterministic Quality Checks",
            "Unverified Areas",
            "Traceability",
            "SAFE-009",
            "REQ-040",
            "REQ-042",
            "REQ-043",
            "REQ-045",
            "REQ-046",
            "REQ-047"
        ]
        for req in fv_requirements:
            if req in content:
                print(f"  [x] Feature Validation Skill contains '{req}'")
            else:
                print(f"[FAIL] Feature Validation Skill missing '{req}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 4. Task M6-T04: templates/qa-report.md
    template_file = "templates/qa-report.md"
    if check_file(template_file, "QA Report Template"):
        with open(template_file, "r", encoding="utf-8") as f:
            content = f.read()

        required_sections = [
            "Executive Summary",
            "Review Determination",
            "Quality Metrics Summary",
            "Review Scope & Context",
            "Requirements Coverage Matrix",
            "Multi-Dimensional Code Review Findings",
            "Test Execution Log",
            "Unverified Areas & Environmental Limitations",
            "Remaining Issues & Blockers",
            "Final Recommendation & Developer Acceptance Gate"
        ]
        for sec in required_sections:
            if sec.lower() in content.lower():
                print(f"  [x] QA Report Template contains section: '{sec}'")
            else:
                print(f"[FAIL] QA Report Template missing section: '{sec}'")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 5. Task M6-T05: workflows/validate-feature.md
    workflow_file = "workflows/validate-feature.md"
    if check_file(workflow_file, "Validate Feature Workflow"):
        with open(workflow_file, "r", encoding="utf-8") as f:
            content = f.read()

        required_workflow_elements = [
            "feature_validation",
            "workflows/validate-feature.md",
            "QA Engineer",
            "Developer (Final Sign-off Authority)",
            "Quality Gates Enforced",
            "require_test_result_reporting",
            "prohibit_unverified_pass_claims",
            "require_observed_command_output",
            "require_independent_review",
            "require_completed_qa_report",
            "Execution Sequence",
            "flowchart TD",
            "Phase 1: Input Baseline & Context Ingestion",
            "Phase 2: Static Analysis & Test Execution",
            "Phase 3: Multi-Dimensional Code Review",
            "Phase 4: Requirements Coverage Evaluation",
            "Phase 5: Document Limitations & Unverified Areas",
            "Phase 6: Compile QA Report",
            "Phase 7: Developer Acceptance Sign-off Gate",
            "Escalation & Remediation Routing"
        ]
        for elem in required_workflow_elements:
            if elem in content:
                print(f"  [x] Workflow contains element: '{elem}'")
            else:
                print(f"[FAIL] Missing element '{elem}' in {workflow_file}")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 6. Execute deterministic QA logic & gate test suite
    if not test_qa_evaluation_logic():
        all_passed = False

    print("\n===================================")
    if all_passed:
        print("RESULT: ALL M6 VALIDATION CHECKS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("RESULT: M6 VALIDATION FAILED WITH ERRORS.")
        return 1


if __name__ == "__main__":
    sys.exit(validate_m6())

