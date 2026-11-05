#!/usr/bin/env python3
"""
Validation script for Dev-Team Milestone 4 (Technical Planning Workflow).
Verifies that all M4 artifacts exist, conform to schemas, and satisfy acceptance criteria.
"""

import os
import re
import sys

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


def validate_m4():
    all_passed = True

    print("=== Milestone 4 Verification ===\n")

    # 1. Task M4-T01: agents/technical-planner.toml
    planner_file = "agents/technical-planner.toml"
    if check_file(planner_file, "Technical Planner Agent Spec"):
        with open(planner_file, "rb") as f:
            data = tomllib.loads(f.read().decode("utf-8"))
        
        required_keys = ["name", "display_name", "version", "description", "role",
                         "responsibilities", "inputs", "outputs", "skills", "boundaries", "quality_gates"]
        for key in required_keys:
            if key not in data:
                print(f"[FAIL] Missing key '{key}' in {planner_file}")
                all_passed = False
            else:
                print(f"  [x] Agent spec contains key '{key}'")
        
        # Check specific boundaries and quality gates
        if "cannot" in data.get("boundaries", {}):
            print("  [x] Planner defines clear negative boundaries (cannot)")
        else:
            print("[FAIL] Missing 'cannot' in boundaries")
            all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 2. Task M4-T02: skills/technical-planning/SKILL.md
    skill_file = "skills/technical-planning/SKILL.md"
    if check_file(skill_file, "Technical Planning Skill"):
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check YAML frontmatter
        if content.startswith("---") and "name: technical-planning" in content:
            print("  [x] Skill has valid YAML frontmatter with correct name")
        else:
            print("[FAIL] Missing or invalid YAML frontmatter in skill")
            all_passed = False

        # Check required procedural sections
        required_sections = [
            "Overview & Purpose",
            "When to Use",
            "Required Inputs",
            "Core Principles",
            "Execution Procedure",
            "Task Slicing Rules",
            "Scope Change & Replanning",
            "Quality Gate Checklist"
        ]
        for sec in required_sections:
            if sec.lower() in content.lower():
                print(f"  [x] Skill includes section: '{sec}'")
            else:
                print(f"[FAIL] Missing section '{sec}' in {skill_file}")
                all_passed = False

        # Check coverage of key requirements: REQ-022 to REQ-030
        for req in ["REQ-022", "REQ-023", "REQ-024", "REQ-025", "REQ-026", "REQ-027", "REQ-028", "REQ-029", "REQ-030"]:
            if req in content:
                print(f"  [x] Skill references {req}")
            else:
                print(f"[WARN] Skill does not explicitly reference {req}")
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 3. Task M4-T03: templates/plan.md
    plan_template = "templates/plan.md"
    if check_file(plan_template, "Implementation Plan Template"):
        with open(plan_template, "r", encoding="utf-8") as f:
            content = f.read()

        required_sections = [
            "Document Type:",
            "Status:",
            "Implementation Overview",
            "Requirement-to-Task Traceability Matrix",
            "Milestone Overview",
            "Milestone & Task Specifications",
            "Task Dependency Graph",
            "Verification & Quality Strategy",
            "Risk Management",
            "Plan Review Audit",
            "Developer Plan Approval Gate"
        ]
        for sec in required_sections:
            if sec in content:
                print(f"  [x] Plan template contains '{sec}'")
            else:
                print(f"[FAIL] Missing '{sec}' in {plan_template}")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 4. Task M4-T04: templates/task.md
    task_template = "templates/task.md"
    if check_file(task_template, "Task Template"):
        with open(task_template, "r", encoding="utf-8") as f:
            content = f.read()

        required_sections = [
            "Task ID:",
            "Title:",
            "Status:",
            "Task Objective & Context",
            "Requirements & Traceability",
            "Dependencies & Execution Mode",
            "Scope & File Targets",
            "Deliverables",
            "Acceptance Criteria",
            "Deterministic Validation Procedure",
            "Execution Log & Evidence"
        ]
        for sec in required_sections:
            if sec in content:
                print(f"  [x] Task template contains '{sec}'")
            else:
                print(f"[FAIL] Missing '{sec}' in {task_template}")
                all_passed = False
    else:
        all_passed = False

    print("\n-----------------------------------\n")

    # 5. Task M4-T05: workflows/create-plan.md
    workflow_file = "workflows/create-plan.md"
    if check_file(workflow_file, "Create Plan Workflow"):
        with open(workflow_file, "r", encoding="utf-8") as f:
            content = f.read()

        required_elements = [
            "create_plan",
            "workflows/create-plan.md",
            "Planning Gate",
            "Prerequisites & Entry Conditions",
            "Quality Gates Enforced",
            "PLAN-GATE-1",
            "PLAN-GATE-2",
            "PLAN-GATE-3",
            "PLAN-GATE-4",
            "PLAN-GATE-5",
            "Execution Sequence",
            "flowchart TD",
            "Phase 1: Ingest Approved Requirements & Design",
            "Phase 2: Context Alignment & Validation Discovery",
            "Phase 3: Milestone & Task Decomposition",
            "Phase 4: Dependency Graph & Execution Sequencing",
            "Phase 5: Plan Review Audit",
            "Phase 6: Developer Plan Approval Gate",
            "Phase 7: Baseline & Transition",
            "Scope Change & Replanning Protocol",
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

    print("\n===================================")
    if all_passed:
        print("RESULT: ALL M4 VALIDATION CHECKS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("RESULT: M4 VALIDATION FAILED WITH ERRORS.")
        return 1


if __name__ == "__main__":
    sys.exit(validate_m4())
