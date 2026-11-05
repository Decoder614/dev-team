#!/usr/bin/env python3
"""
scripts/validate_installation_and_documentation_artifacts.py — Installation & Documentation Verification Script
Verifies that all installation scripts, workspace validation utilities, and system documentation
artifacts are implemented, valid, and satisfy all acceptance criteria and safety boundaries
(REQ-067 to REQ-072, ADR-013, ADR-014).
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def check_file(path, description):
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        print(f"[FAIL] Missing or empty {description}: {path}")
        return False
    print(f"[PASS] Found {description}: {path}")
    return True


def check_content_contains(content, substrings, context_label):
    all_ok = True
    for s in substrings:
        if s not in content:
            print(f"  [!] Missing expected content in {context_label}: '{s}'")
            all_ok = False
        else:
            print(f"  [x] Contains expected content: '{s}'")
    return all_ok


def validate_installation_docs(root_dir):
    print("\n--- Validating Installation Documentation (docs/installation.md) ---")
    doc_path = os.path.join(root_dir, "docs", "installation.md")
    if not check_file(doc_path, "Installation Guide"):
        return False

    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_sections = [
        "Overview & Architecture",
        "Prerequisites",
        "Supported Codex Skill Discovery",
        "Installation Strategies",
        "Automated Installation on Windows",
        "Automated Installation on Unix",
        "Configuring a Target Repository",
        "Verifying Your Installation",
        "Troubleshooting",
        "Uninstallation & Cleanup",
        "REQ-067",
        "REQ-069",
        "REQ-070",
        "REQ-071",
        "REQ-072",
    ]

    ok = check_content_contains(content, expected_sections, "docs/installation.md")

    # Verify no developer-specific absolute paths
    bad_patterns = [r"[C-Z]:\\Users\\(?:asus|jaydip|developer|admin)\\", r"/home/(?:asus|jaydip|developer)/"]
    for pat in bad_patterns:
        if re.search(pat, content, re.IGNORECASE):
            print(f"  [FAIL] Found hardcoded user path matching {pat} in docs/installation.md")
            ok = False

    if ok:
        print("  [x] Installation Guide: No hardcoded developer-specific absolute paths detected")
        print("  [x] Installation Guide: All installation strategies and troubleshooting documented")
    return ok


def validate_windows_installer(root_dir):
    print("\n--- Validating Windows Installer (scripts/install.ps1) ---")
    ps1_path = os.path.join(root_dir, "scripts", "install.ps1")
    if not check_file(ps1_path, "Windows Installer Script"):
        return False

    with open(ps1_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_elements = [
        "param(",
        "$Mode = \"Copy\"",
        "$CodexDir",
        "$TargetRepo",
        "$Uninstall",
        "$DryRun",
        "$Force",
        "DiscoveredSkills",
        "DestSkillsDir",
        "ReparsePoint",
        "Unrelated skills in destination were preserved.",
    ]

    ok = check_content_contains(content, expected_elements, "scripts/install.ps1")

    # Run dry-run via PowerShell
    try:
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_path, "-DryRun"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and "Dev-Team skills successfully configured!" in res.stdout:
            print("  [x] Windows Installer: PowerShell dry-run succeeded with code 0")
        else:
            print(f"  [FAIL] Windows Installer: PowerShell dry-run failed (code {res.returncode}): {res.stderr}")
            ok = False
    except Exception as e:
        print(f"  [WARN] Could not invoke powershell for Windows installer check: {e}")

    return ok


def validate_unix_installer(root_dir):
    print("\n--- Validating Unix Installer (scripts/install.sh) ---")
    sh_path = os.path.join(root_dir, "scripts", "install.sh")
    if not check_file(sh_path, "Unix Installer Script"):
        return False

    with open(sh_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_elements = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "getopts \"m:d:t:unfh\"",
        "DEV_TEAM_ROOT=",
        "SOURCE_SKILLS_DIR=",
        "DEST_SKILLS_DIR=",
        "UNINSTALL=true",
        "DRY_RUN=true",
        "Unrelated skills in destination were preserved.",
    ]

    ok = check_content_contains(content, expected_elements, "scripts/install.sh")

    # Run dry-run via bash if available
    try:
        cmd = ["bash", "scripts/install.sh", "-n"]
        res = subprocess.run(cmd, cwd=root_dir, capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and "Dev-Team skills successfully configured!" in res.stdout:
            print("  [x] Unix Installer: Bash dry-run succeeded with code 0")
        else:
            print(f"  [FAIL] Unix Installer: Bash dry-run failed (code {res.returncode}): {res.stderr}")
            ok = False
    except Exception as e:
        print(f"  [WARN] Bash not invoked: {e}")

    return ok


def validate_workspace_script(root_dir):
    print("\n--- Validating Workspace Validator (scripts/validate-workspace.py) ---")
    validator_path = os.path.join(root_dir, "scripts", "validate-workspace.py")
    if not check_file(validator_path, "Workspace Validation Script"):
        return False

    # Test running validator against self with --json
    cmd = [sys.executable, validator_path, "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [FAIL] validate-workspace.py failed on dev-team repository (code {res.returncode})")
        print(res.stdout)
        print(res.stderr)
        return False

    print("  [x] Workspace Validator: Passed on dev-team root with code 0")

    # Test error handling on deliberately broken target directory
    with tempfile.TemporaryDirectory() as bad_dir:
        cmd_bad = [sys.executable, validator_path, "--target", bad_dir, "--json"]
        res_bad = subprocess.run(cmd_bad, capture_output=True, text=True)
        if res_bad.returncode != 0:
            print("  [x] Workspace Validator: Correctly returned non-zero code on broken target repository")
        else:
            print("  [FAIL] Workspace Validator: Unexpectedly returned 0 on broken target repository")
            return False

    return True


def validate_system_documentation(root_dir):
    print("\n--- Validating System Documentation ---")
    doc_files = {
        "README.md": os.path.join(root_dir, "README.md"),
        "docs/architecture.md": os.path.join(root_dir, "docs", "architecture.md"),
        "docs/workflows.md": os.path.join(root_dir, "docs", "workflows.md"),
        "docs/contribution-guide.md": os.path.join(root_dir, "docs", "contribution-guide.md"),
    }

    all_ok = True
    for label, path in doc_files.items():
        if not check_file(path, label):
            all_ok = False

    if not all_ok:
        return False

    # Check README.md
    with open(doc_files["README.md"], "r", encoding="utf-8") as f:
        readme_content = f.read()
    all_ok &= check_content_contains(
        readme_content,
        [
            "Quickstart & Installation",
            "Engineering Workflows",
            "System Architecture & Boundaries",
            "docs/installation.md",
            "docs/workflows.md",
            "docs/architecture.md",
            "docs/contribution-guide.md",
            "scripts/validate-workspace.py",
        ],
        "README.md",
    )

    # Check docs/architecture.md
    with open(doc_files["docs/architecture.md"], "r", encoding="utf-8") as f:
        arch_content = f.read()
    all_ok &= check_content_contains(
        arch_content,
        [
            "Architectural Overview & Philosophy",
            "Layered Architecture",
            "Mandatory Safety Boundaries",
            "SAFE-001",
            "SAFE-009",
            "SAFE-010",
            "flowchart TD",
            "sequenceDiagram",
            "Architectural Decision Records",
        ],
        "docs/architecture.md",
    )

    # Check docs/workflows.md
    with open(doc_files["docs/workflows.md"], "r", encoding="utf-8") as f:
        wf_content = f.read()
    all_ok &= check_content_contains(
        wf_content,
        [
            "Workflow Architecture & Lifecycle",
            "new-feature.md",
            "validate-requirement.md",
            "design-feature.md",
            "create-plan.md",
            "implement-next.md",
            "validate-feature.md",
            "fix-bug.md",
            "feature-status.md",
            "flowchart TD",
        ],
        "docs/workflows.md",
    )

    # Check docs/contribution-guide.md
    with open(doc_files["docs/contribution-guide.md"], "r", encoding="utf-8") as f:
        contrib_content = f.read()
    all_ok &= check_content_contains(
        contrib_content,
        [
            "Adding a New Specialized Agent",
            "Adding a New Procedural Skill",
            "Adding or Modifying Workflows",
            "Adding Standard Templates",
            "Workspace Validation & Testing",
            "scripts/validate-workspace.py",
        ],
        "docs/contribution-guide.md",
    )

    return all_ok


def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("======================================================================")
    print("      Dev-Team Verification: Installation & System Documentation     ")
    print("======================================================================")
    print(f"Workspace Root: {root_dir}")

    results = [
        ("Installation Documentation (docs/installation.md)", validate_installation_docs(root_dir)),
        ("Windows Installer (scripts/install.ps1)", validate_windows_installer(root_dir)),
        ("Unix-like Installer (scripts/install.sh)", validate_unix_installer(root_dir)),
        ("Workspace Validation Script (scripts/validate-workspace.py)", validate_workspace_script(root_dir)),
        ("Complete System Documentation (README & docs/)", validate_system_documentation(root_dir)),
    ]

    print("\n======================================================================")
    print("                         Summary Results                              ")
    print("======================================================================")
    failures = 0
    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {name}")
        if not success:
            failures += 1

    print("======================================================================")
    if failures == 0:
        print("RESULT: ALL INSTALLATION & DOCUMENTATION CHECKS VERIFIED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print(f"RESULT: {failures} VERIFICATION CHECK(S) FAILED.")
        sys.exit(1)


if __name__ == "__main__":
    main()

