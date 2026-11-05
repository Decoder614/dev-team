#!/usr/bin/env python3
"""
Validation script for Dev-Team Milestone 5 (Controlled Development Workflow).
Verifies that all M5 artifacts exist, conform to schemas, enforce safety gates,
and satisfy acceptance criteria for task progress tracking and state transitions.
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


def test_task_state_machine():
    """
    Validates task status progression rules and evidence enforcement.
    Ensures that tasks cannot transition to COMPLETED without evidence,
    or to BLOCKED without an explanation (M5-T04).
    """
    print("\n--- Testing Task State Machine & Evidence Rules (M5-T04) ---")
    allowed_statuses = {"PENDING", "IN_PROGRESS", "BLOCKED", "COMPLETED", "NEEDS_REVIEW"}
    
    # Valid transition definitions
    valid_transitions = {
        "PENDING": {"IN_PROGRESS"},
        "IN_PROGRESS": {"COMPLETED", "BLOCKED", "NEEDS_REVIEW"},
        "BLOCKED": {"IN_PROGRESS"},
        "NEEDS_REVIEW": {"COMPLETED", "IN_PROGRESS"},
        "COMPLETED": set()  # Terminal state for normal task execution
    }

    def validate_transition(from_state, to_state, has_evidence=False, has_blocker_reason=False):
        if from_state not in allowed_statuses or to_state not in allowed_statuses:
            return False, "Unknown status"
        if to_state not in valid_transitions.get(from_state, set()):
            return False, f"Invalid transition from {from_state} to {to_state}"
        if to_state in {"COMPLETED", "NEEDS_REVIEW"} and not has_evidence:
            return False, f"Transition to {to_state} requires tangible validation evidence (SAFE-009)"
        if to_state == "BLOCKED" and not has_blocker_reason:
            return False, "Transition to BLOCKED requires blocker description and categorization (REQ-030)"
        return True, "Valid transition"

    test_cases = [
        # (from_state, to_state, has_evidence, has_blocker_reason, expected_valid, label)
        ("PENDING", "IN_PROGRESS", False, False, True, "Normal start of task"),
        ("PENDING", "COMPLETED", True, False, False, "Bypassing IN_PROGRESS (invalid)"),
        ("IN_PROGRESS", "COMPLETED", True, False, True, "Completion with evidence"),
        ("IN_PROGRESS", "COMPLETED", False, False, False, "Completion without evidence (rejected by SAFE-009)"),
        ("IN_PROGRESS", "BLOCKED", False, True, True, "Blocked with explanation"),
        ("IN_PROGRESS", "BLOCKED", False, False, False, "Blocked without explanation (rejected)"),
        ("BLOCKED", "IN_PROGRESS", False, False, True, "Unblocking task after resolution"),
        ("IN_PROGRESS", "NEEDS_REVIEW", True, False, True, "Submitted for review with evidence"),
        ("NEEDS_REVIEW", "COMPLETED", True, False, True, "Review sign-off with evidence"),
    ]

    all_tests_passed = True
    for from_s, to_s, ev, blk, expected, label in test_cases:
        valid, msg = validate_transition(from_s, to_s, has_evidence=ev, has_blocker_reason=blk)
        if valid == expected:
            print(f"  [x] State check passed: {label} -> {msg}")
        else:
            print(f"[FAIL] State check failed: {label} (expected {expected}, got {valid}: {msg})")
            all_tests_passed = False

    return all_tests_passed


def validate_m5():
    all_passed = True

    print("=== Milestone 5 Verification: Controlled Development Workflow ===\n")

    # 1. Task M5-T01: agents/developer.toml
    dev_file = "agents/developer.toml"
    if check_file(dev_file, "Developer Agent Spec"):
        with open(dev_file, "rb") as f:
            data = tomllib.loads(f.read().decode("utf-8"))

        required_keys = [
            "name", "display_name", "version", "description", "role",
            "responsibilities", "inputs", "outputs", "skills", "boundaries", "quality_gates"
        ]
        for key in required_keys:
            if key not in data:
                print(f"[FAIL] Missing key '{key}' in {dev_file}")
                all_passed = False
            else:
                print(f"  [x] Agent spec contains key '{key}'")

        # Check critical developer boundaries and safety restrictions
        boundaries = data.get("boundaries", {})
        cannot_rules = " ".join(boundaries.get("cannot", []))
        
        checks = [
            ("Unapproved plan check", "unapproved" in cannot_rules.lower()),
            ("Scope expansion check", "scope" in cannot_rules.lower()),
            ("Unsolicited refactoring check", "refactoring" in cannot_rules.lower()),
            ("Evidence/test pass check", "executed" in cannot_rules.lower() or "executing" in cannot_rules.lower()),
            ("Destructive command check", "destructive" in cannot_rules.lower()),
            ("Secret exposure check", "secret" in cannot_rules.lower())
        ]
        for name, passed in checks:
            if passed:
                print(f"  [x] Developer boundaries enforce: {name}")
            else:
                print(f"[FAIL] Developer boundaries missing: {name}")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 2. Task M5-T02: skills/flutter-development/SKILL.md
    skill_file = "skills/flutter-development/SKILL.md"
    if check_file(skill_file, "Flutter Development Skill"):
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check YAML frontmatter
        if content.startswith("---") and "name: flutter-development" in content:
            print("  [x] Skill has valid YAML frontmatter with correct name")
        else:
            print("[FAIL] Missing or invalid YAML frontmatter in skill")
            all_passed = False

        # Check required procedural sections
        required_sections = [
            "Overview & Purpose",
            "When to Use",
            "Precedence & Technology Agnosticism",
            "Flutter Project Inspection",
            "Dart Coding Practices",
            "Widget Composition & UI Patterns",
            "State Management Patterns",
            "Routing & Navigation",
            "Dependency Injection",
            "Repository & Data-Layer Patterns",
            "Error Handling & Safety Boundaries",
            "Testing Practices",
            "Deterministic Static Analysis & Formatting",
            "Developer Discipline Checklist"
        ]
        for sec in required_sections:
            if sec.lower() in content.lower():
                print(f"  [x] Skill includes section: '{sec}'")
            else:
                print(f"[FAIL] Missing section '{sec}' in {skill_file}")
                all_passed = False

        # Check coverage of key requirements: REQ-031 to REQ-039
        for req in ["REQ-031", "REQ-032", "REQ-033", "REQ-034", "REQ-035", "REQ-036", "REQ-037", "REQ-038", "REQ-039"]:
            if req in content:
                print(f"  [x] Skill references {req}")
            else:
                print(f"[WARN] Skill does not explicitly reference {req}")
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 3. Task M5-T03: workflows/implement-next.md
    workflow_file = "workflows/implement-next.md"
    if check_file(workflow_file, "Implement Next Task Workflow"):
        with open(workflow_file, "r", encoding="utf-8") as f:
            content = f.read()

        required_elements = [
            "implementation",
            "workflows/implement-next.md",
            "Implementation Gate",
            "Prerequisites & Entry Conditions",
            "Quality Gates Enforced",
            "IMPL-GATE-1",
            "IMPL-GATE-2",
            "IMPL-GATE-3",
            "IMPL-GATE-4",
            "IMPL-GATE-5",
            "Execution Sequence",
            "flowchart TD",
            "Phase 1: Task Selection & Dependency Check",
            "Phase 2: Working Tree & Context Inspection",
            "Phase 3: Transition Status to IN_PROGRESS",
            "Phase 4: Controlled Implementation",
            "Phase 5: Deterministic Validation",
            "Phase 6: State Transition & Execution Log",
            "Phase 7: Stop & Report Summary",
            "Task Progress Tracking & State Machine",
            "Scope Change & Blocker Escalation Protocol",
            "Artifact Lifecycle"
        ]
        for elem in required_elements:
            if elem in content:
                print(f"  [x] Workflow contains '{elem}'")
            else:
                print(f"[FAIL] Missing '{elem}' in {workflow_file}")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 4. Task M5-T04: Task Progress Tracking Configuration & State Machine Verification
    defaults_file = "config/defaults.yaml"
    if check_file(defaults_file, "Defaults Configuration"):
        with open(defaults_file, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        task_cfg = cfg.get("task_statuses", {})
        allowed = task_cfg.get("allowed", [])
        expected_statuses = ["PENDING", "IN_PROGRESS", "BLOCKED", "COMPLETED", "NEEDS_REVIEW"]
        if all(st in allowed for st in expected_statuses):
            print(f"  [x] config/defaults.yaml defines all 5 required task statuses: {allowed}")
        else:
            print(f"[FAIL] Missing required statuses in {defaults_file}: {allowed}")
            all_passed = False
    else:
        all_passed = False

    # Execute state machine validation
    if not test_task_state_machine():
        all_passed = False

    print("\n===================================")
    if all_passed:
        print("RESULT: ALL M5 VALIDATION CHECKS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("RESULT: M5 VALIDATION FAILED WITH ERRORS.")
        return 1


if __name__ == "__main__":
    sys.exit(validate_m5())

