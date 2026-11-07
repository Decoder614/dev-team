#!/usr/bin/env python3
"""
scripts/validate-workspace.py — Workspace Validation Utility for Dev-Team

Deterministically validates the Dev-Team repository workspace or target application repositories.
Checks:
1. Directory structure and required files.
2. Configuration syntax (YAML/TOML) and structural validity.
3. Skill structure, YAML frontmatter, and metadata naming consistency.
4. Agent specifications, role boundaries, and cross-references.
5. Template existence and completeness.
6. Workflow structure and cross-reference integrity.
7. Target application repository scaffolding (.dev-team/ and AGENTS.md) when in --target mode.

Returns:
  0 on complete validation success
  1 if any errors are encountered
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FAIL] Missing dependency: pyyaml. Install with 'pip install pyyaml'.")
    sys.exit(1)

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("[FAIL] Missing TOML parser. Install 'tomli' or use Python 3.11+.")
        sys.exit(1)


class ValidationReporter:
    def __init__(self, verbose=False, json_output=False):
        self.verbose = verbose
        self.json_output = json_output
        self.passes = []
        self.failures = []
        self.warnings = []

    def log_pass(self, check_name, detail=""):
        self.passes.append({"check": check_name, "detail": detail})
        if not self.json_output and (self.verbose or detail == ""):
            msg = f"[PASS] {check_name}"
            if detail:
                msg += f" — {detail}"
            print(msg)

    def log_fail(self, check_name, error_msg, file_path=None):
        entry = {"check": check_name, "error": error_msg, "file": str(file_path) if file_path else None}
        self.failures.append(entry)
        if not self.json_output:
            loc = f" [{file_path}]" if file_path else ""
            print(f"[FAIL] {check_name}{loc}: {error_msg}")

    def log_warn(self, check_name, warn_msg, file_path=None):
        entry = {"check": check_name, "warning": warn_msg, "file": str(file_path) if file_path else None}
        self.warnings.append(entry)
        if not self.json_output:
            loc = f" [{file_path}]" if file_path else ""
            print(f"[WARN] {check_name}{loc}: {warn_msg}")

    def print_summary(self):
        total_checks = len(self.passes) + len(self.failures)
        if self.json_output:
            result = {
                "success": len(self.failures) == 0,
                "total_checks": total_checks,
                "passed": len(self.passes),
                "failed": len(self.failures),
                "warnings": len(self.warnings),
                "failures": self.failures,
                "warnings": self.warnings,
            }
            print(json.dumps(result, indent=2))
        else:
            print("\n============================================================")
            print(f"Validation Summary: {len(self.passes)} Passed, {len(self.failures)} Failed, {len(self.warnings)} Warnings")
            print("============================================================")
            if self.failures:
                print(f"[RESULT] FAILED with {len(self.failures)} error(s).")
            else:
                print("[RESULT] ALL CHECKS PASSED SUCCESSFULLY!")

        return 0 if len(self.failures) == 0 else 1


def parse_yaml_file(file_path, reporter):
    if not os.path.isfile(file_path):
        reporter.log_fail("File Existence", f"File not found: {file_path}", file_path)
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        reporter.log_pass(f"YAML Syntax: {os.path.basename(file_path)}")
        return data
    except Exception as e:
        reporter.log_fail("YAML Syntax", f"YAML parsing error: {e}", file_path)
        return None


def parse_toml_file(file_path, reporter):
    if not os.path.isfile(file_path):
        reporter.log_fail("File Existence", f"File not found: {file_path}", file_path)
        return None
    try:
        with open(file_path, "rb") as f:
            data = tomllib.load(f)
        reporter.log_pass(f"TOML Syntax: {os.path.basename(file_path)}")
        return data
    except Exception as e:
        reporter.log_fail("TOML Syntax", f"TOML parsing error: {e}", file_path)
        return None


def parse_skill_frontmatter(skill_md_path, reporter):
    if not os.path.isfile(skill_md_path):
        reporter.log_fail("Skill File Missing", f"SKILL.md not found in {os.path.dirname(skill_md_path)}", skill_md_path)
        return None
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not match:
            reporter.log_fail("Skill Frontmatter", "Missing standard YAML frontmatter (--- delimiter) at start of file", skill_md_path)
            return None

        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            reporter.log_fail("Skill Frontmatter", "Frontmatter must be a YAML dictionary", skill_md_path)
            return None

        return frontmatter
    except Exception as e:
        reporter.log_fail("Skill Frontmatter", f"Error parsing skill frontmatter: {e}", skill_md_path)
        return None


def validate_dev_team_workspace(root_path, reporter):
    """Validates the dev-team framework repository itself."""
    if not reporter.json_output:
        print(f"Validating Dev-Team Framework Workspace at: {root_path}")
        print("------------------------------------------------------------")

    # 1. Directory Structure (Canonical v1.1 Repository Organization)
    expected_directories = [
        "cli",
        "adapters",
        "schemas",
        "config",
        "agents",
        "skills",
        "workflows",
        "templates",
        "scripts",
        "docs",
    ]
    for d in expected_directories:
        dir_path = os.path.join(root_path, d)
        if os.path.isdir(dir_path):
            reporter.log_pass(f"Directory: {d}/")
        else:
            reporter.log_fail("Directory Structure", f"Required directory missing: {d}/", dir_path)

    # 2. Core Root Files
    expected_root_files = ["README.md", "AGENTS.md", "LICENSE"]
    for f in expected_root_files:
        file_path = os.path.join(root_path, f)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            reporter.log_pass(f"Root File: {f}")
        else:
            reporter.log_fail("Root Files", f"Required root file missing or empty: {f}", file_path)

    # 3. Configuration Files
    config_dir = os.path.join(root_path, "config")
    workflow_yaml_path = os.path.join(config_dir, "workflow.yaml")
    quality_gates_yaml_path = os.path.join(config_dir, "quality-gates.yaml")
    defaults_yaml_path = os.path.join(config_dir, "defaults.yaml")

    workflow_cfg = parse_yaml_file(workflow_yaml_path, reporter)
    gates_cfg = parse_yaml_file(quality_gates_yaml_path, reporter)
    defaults_cfg = parse_yaml_file(defaults_yaml_path, reporter)

    if workflow_cfg:
        if "version" in workflow_cfg and "workflows" in workflow_cfg and "defaults" in workflow_cfg:
            reporter.log_pass("Schema: workflow.yaml", "Has version, defaults, and workflows")
            # Verify governing roles
            for wf_name, wf_data in workflow_cfg.get("workflows", {}).items():
                if "governing_role" in wf_data:
                    reporter.log_pass(f"Workflow Governing Role: {wf_name} -> {wf_data['governing_role']}")
                else:
                    reporter.log_fail("Workflow Governing Role", f"Missing governing_role in workflow: {wf_name}", workflow_yaml_path)
        else:
            reporter.log_fail("Schema: workflow.yaml", "Missing one of required keys: version, defaults, workflows", workflow_yaml_path)

    if gates_cfg:
        expected_gates = ["requirements", "architecture", "planning", "implementation", "testing", "code_review", "final_acceptance"]
        missing_gates = [g for g in expected_gates if g not in gates_cfg]
        if not missing_gates:
            reporter.log_pass("Schema: quality-gates.yaml", "Defines all 7 standard engineering gates")
        else:
            reporter.log_fail("Schema: quality-gates.yaml", f"Missing gate definitions: {missing_gates}", quality_gates_yaml_path)

        # Verify safety boundaries (SAFE-001 to SAFE-012)
        safety_bounds = gates_cfg.get("safety_boundaries", {})
        expected_safes = [f"SAFE-{i:03d}" for i in range(1, 13)]
        missing_safes = [s for s in expected_safes if s not in safety_bounds]
        if not missing_safes:
            reporter.log_pass("Schema: quality-gates.yaml", "Defines all 12 safety boundaries (SAFE-001 to SAFE-012)")
        else:
            reporter.log_fail("Safety Boundaries Missing", f"Missing safety boundaries in quality-gates.yaml: {missing_safes}", quality_gates_yaml_path)

    if defaults_cfg:
        if "task_statuses" in defaults_cfg and "artifact_statuses" in defaults_cfg and "paths" in defaults_cfg:
            reporter.log_pass("Schema: defaults.yaml", "Has paths, artifact_statuses, and task_statuses")
        else:
            reporter.log_fail("Schema: defaults.yaml", "Missing required sections", defaults_yaml_path)

    # 4. Agent Role Specifications
    agents_dir = os.path.join(root_path, "agents")
    agent_specs = {}
    if os.path.isdir(agents_dir):
        agent_files = [f for f in os.listdir(agents_dir) if f.endswith(".toml")]
        if len(agent_files) < 6:
            reporter.log_fail("Agent Count", f"Expected at least 6 core engineering agents, found {len(agent_files)}", agents_dir)
        else:
            reporter.log_pass("Agent Count", f"Found {len(agent_files)} agent specifications")

        required_agent_keys = ["name", "display_name", "version", "role", "responsibilities", "boundaries", "skills", "quality_gates"]
        for af in sorted(agent_files):
            agent_path = os.path.join(agents_dir, af)
            data = parse_toml_file(agent_path, reporter)
            if data:
                agent_specs[data.get("name", af)] = data
                missing = [k for k in required_agent_keys if k not in data]
                if not missing:
                    reporter.log_pass(f"Agent Spec: {af}", "Contains all required keys and boundaries")
                else:
                    reporter.log_fail("Agent Spec Keys", f"Missing required keys {missing} in {af}", agent_path)

    # 5. Reusable Skills & Metadata
    skills_dir = os.path.join(root_path, "skills")
    discovered_skills = {}
    if os.path.isdir(skills_dir):
        skill_folders = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        if len(skill_folders) < 10:
            reporter.log_fail("Skill Count", f"Expected at least 10 reusable skills, found {len(skill_folders)}", skills_dir)
        else:
            reporter.log_pass("Skill Count", f"Found {len(skill_folders)} skill directories")

        for s_folder in sorted(skill_folders):
            skill_folder_path = os.path.join(skills_dir, s_folder)
            skill_md_path = os.path.join(skill_folder_path, "SKILL.md")
            frontmatter = parse_skill_frontmatter(skill_md_path, reporter)
            if frontmatter:
                skill_name = frontmatter.get("name")
                desc = frontmatter.get("description", "")
                if skill_name != s_folder:
                    reporter.log_fail("Skill Name Match", f"Frontmatter name '{skill_name}' does not match directory '{s_folder}'", skill_md_path)
                elif not desc or len(str(desc).strip()) < 10:
                    reporter.log_fail("Skill Description", "Frontmatter description is missing or too brief", skill_md_path)
                else:
                    reporter.log_pass(f"Skill Metadata: {s_folder}", f"Valid frontmatter name and description ({len(str(desc))} chars)")
                    discovered_skills[s_folder] = frontmatter

        # 5b. Validate Project Initializer Assets (Milestone 1.5)
        pi_folder = os.path.join(skills_dir, "project-initializer")
        if os.path.isdir(pi_folder):
            pi_script = os.path.join(pi_folder, "scripts", "check-project-structure.py")
            if os.path.isfile(pi_script) and os.path.getsize(pi_script) > 100:
                reporter.log_pass("Skill Script: check-project-structure.py", "Script exists and non-empty")
            else:
                reporter.log_fail("Skill Script Missing", "check-project-structure.py missing or empty", pi_script)

            pi_refs = [
                "project-detection.md",
                "context-gathering.md",
                "documentation-rules.md",
                "initialization-workflow.md",
            ]
            for ref_name in pi_refs:
                ref_path = os.path.join(pi_folder, "references", ref_name)
                if os.path.isfile(ref_path) and os.path.getsize(ref_path) > 100:
                    reporter.log_pass(f"Skill Reference: {ref_name}", "Reference guide exists and non-empty")
                else:
                    reporter.log_fail("Skill Reference Missing", f"Reference guide {ref_name} missing or empty", ref_path)

    # 6. Standard Templates
    templates_dir = os.path.join(root_path, "templates")
    expected_templates = [
        "requirement.md",
        "system-design.md",
        "plan.md",
        "task.md",
        "qa-report.md",
        "bug-report.md",
        "SKILL.md",
    ]
    if os.path.isdir(templates_dir):
        for tmpl in expected_templates:
            tmpl_path = os.path.join(templates_dir, tmpl)
            if os.path.isfile(tmpl_path) and os.path.getsize(tmpl_path) > 50:
                reporter.log_pass(f"Template: {tmpl}")
            else:
                reporter.log_fail("Template File", f"Required template missing or empty: {tmpl}", tmpl_path)

        # 6b. Project Scaffolding Templates (Milestone 1.5)
        project_templates_dir = os.path.join(templates_dir, "project")
        expected_project_templates = [
            "AGENTS.md",
            "rules.md",
            "DESIGN.md",
            "overview.md",
            "requirements.md",
            "system-design.md",
            "plan.md",
            "tech-stack.md",
            "architecture.md",
            "config.yaml",
            "project-context.md",
            "initialization-report.md",
        ]
        if os.path.isdir(project_templates_dir):
            reporter.log_pass("Directory: templates/project/")
            for p_tmpl in expected_project_templates:
                p_tmpl_path = os.path.join(project_templates_dir, p_tmpl)
                if os.path.isfile(p_tmpl_path) and os.path.getsize(p_tmpl_path) > 50:
                    reporter.log_pass(f"Project Template: {p_tmpl}")
                else:
                    reporter.log_fail("Project Template File", f"Required project template missing or empty: {p_tmpl}", p_tmpl_path)
        else:
            reporter.log_fail("Directory Structure", "Missing templates/project/ directory", project_templates_dir)

    # 7. Workflows
    workflows_dir = os.path.join(root_path, "workflows")
    expected_workflows = [
        "initialize-project.md",
        "new-feature.md",
        "validate-requirement.md",
        "design-feature.md",
        "create-plan.md",
        "implement-next.md",
        "validate-feature.md",
        "fix-bug.md",
        "feature-status.md",
    ]
    if os.path.isdir(workflows_dir):
        for wf in expected_workflows:
            wf_path = os.path.join(workflows_dir, wf)
            if os.path.isfile(wf_path) and os.path.getsize(wf_path) > 100:
                reporter.log_pass(f"Workflow: {wf}")
            else:
                reporter.log_fail("Workflow File", f"Required workflow missing or empty: {wf}", wf_path)

    # 8. Scripts & Installers
    scripts_dir = os.path.join(root_path, "scripts")
    expected_scripts = [
        "install.ps1",
        "install.sh",
        "validate-workspace.py",
    ]
    for sc in expected_scripts:
        sc_path = os.path.join(scripts_dir, sc)
        if os.path.isfile(sc_path) and os.path.getsize(sc_path) > 50:
            reporter.log_pass(f"Script: {sc}")
        else:
            reporter.log_fail("Script File", f"Expected utility script missing: {sc}", sc_path)

    # 9. System Documentation
    docs_dir = os.path.join(root_path, "docs")
    expected_docs = [
        "architecture.md",
        "installation.md",
        "workflows.md",
        "contribution-guide.md",
        "skills-standard.md",
    ]
    for doc in expected_docs:
        doc_path = os.path.join(docs_dir, doc)
        if os.path.isfile(doc_path) and os.path.getsize(doc_path) > 50:
            reporter.log_pass(f"Documentation: {doc}")
        else:
            reporter.log_fail("Documentation File", f"Expected documentation missing: {doc}", doc_path)

    # 10. JSON Schemas for Declarative Contracts (Milestone 1)
    schemas_dir = os.path.join(root_path, "schemas")
    expected_schemas = [
        "project-config.schema.json",
        "adapter-manifest.schema.json",
        "installation-manifest.schema.json",
    ]
    if os.path.isdir(schemas_dir):
        for schema_file in expected_schemas:
            schema_path = os.path.join(schemas_dir, schema_file)
            if os.path.isfile(schema_path) and os.path.getsize(schema_path) > 50:
                try:
                    with open(schema_path, "r", encoding="utf-8") as f:
                        s_data = json.load(f)
                    if "$schema" in s_data and "properties" in s_data:
                        reporter.log_pass(f"Schema JSON: {schema_file}", "Valid JSON Schema Draft-07 format")
                    else:
                        reporter.log_fail("Schema Structure", f"Schema {schema_file} missing '$schema' or 'properties'", schema_path)
                except Exception as e:
                    reporter.log_fail("Schema JSON Syntax", f"Error parsing schema {schema_file}: {e}", schema_path)
            else:
                reporter.log_fail("Schema File", f"Required schema missing or empty: {schema_file}", schema_path)
    else:
        reporter.log_fail("Directory Structure", "Missing schemas/ directory", schemas_dir)

    # 11. Cross-Reference Consistency
    if workflow_cfg and "workflows" in workflow_cfg:
        for wf_key, wf_info in workflow_cfg["workflows"].items():
            entry_point = wf_info.get("entry_point")
            if entry_point:
                resolved_ep = os.path.join(root_path, entry_point)
                if os.path.isfile(resolved_ep):
                    reporter.log_pass(f"Workflow Cross-Ref: {wf_key}", f"Points to valid file: {entry_point}")
                else:
                    reporter.log_fail("Workflow Cross-Ref", f"Workflow {wf_key} references missing entry point: {entry_point}", workflow_yaml_path)

    for agent_name, agent_data in agent_specs.items():
        skills_section = agent_data.get("skills", {})
        skills_referenced = []
        if isinstance(skills_section, dict):
            for group in skills_section.values():
                if isinstance(group, list):
                    skills_referenced.extend(group)
                elif isinstance(group, str):
                    skills_referenced.append(group)
        elif isinstance(skills_section, list):
            skills_referenced.extend(skills_section)

        for ref_entry in skills_referenced:
            # Can be "skills/<name>/SKILL.md" or "<name>"
            match = re.search(r"skills/([^/]+)", str(ref_entry))
            skill_id = match.group(1) if match else str(ref_entry)
            if skill_id in discovered_skills:
                reporter.log_pass(f"Agent Skill Ref: {agent_name} -> {skill_id}")
            else:
                reporter.log_fail("Agent Skill Cross-Ref", f"Agent '{agent_name}' references unknown skill '{ref_entry}' (parsed: '{skill_id}')", agents_dir)


def validate_target_repository(target_path, reporter):
    """Validates an application repository configured to use Dev-Team."""
    if not reporter.json_output:
        print(f"Validating Target Application Repository at: {target_path}")
        print("------------------------------------------------------------")

    if not os.path.isdir(target_path):
        reporter.log_fail("Target Directory", f"Target path is not a directory: {target_path}", target_path)
        return

    # 1. Target AGENTS.md & rules.md
    target_agents_md = os.path.join(target_path, "AGENTS.md")
    if os.path.isfile(target_agents_md):
        reporter.log_pass("Target AGENTS.md", "Target instructions file exists")
    else:
        reporter.log_fail("Target AGENTS.md", "Missing AGENTS.md operating instructions in target root", target_agents_md)

    target_rules_md = os.path.join(target_path, "rules.md")
    if os.path.isfile(target_rules_md):
        reporter.log_pass("Target rules.md", "Target coding rules file exists")
    else:
        reporter.log_warn("Target rules.md", "rules.md coding standards not found in target root", target_rules_md)

    # 2. .dev-team directory
    dev_team_dir = os.path.join(target_path, ".dev-team")
    if os.path.isdir(dev_team_dir):
        reporter.log_pass("Target .dev-team/ Directory")
    else:
        reporter.log_fail("Target .dev-team/", "Missing .dev-team directory in target repository", dev_team_dir)

    # 3. Target Configuration (.dev-team/config.yaml or project-profile.yaml)
    config_yaml_path = os.path.join(dev_team_dir, "config.yaml")
    profile_path = os.path.join(dev_team_dir, "project-profile.yaml")

    if os.path.isfile(config_yaml_path):
        cfg_data = parse_yaml_file(config_yaml_path, reporter)
        if cfg_data:
            if "version" in cfg_data and "project" in cfg_data:
                reporter.log_pass("Target Config Schema", "Valid config.yaml")
            else:
                reporter.log_fail("Target Config Schema", "Missing required keys 'version' or 'project' in config.yaml", config_yaml_path)
    elif os.path.isfile(profile_path):
        profile_data = parse_yaml_file(profile_path, reporter)
        if profile_data:
            if "version" in profile_data and "project" in profile_data:
                reporter.log_pass("Target Profile Schema", "Valid project-profile.yaml")
            else:
                reporter.log_fail("Target Profile Schema", "Missing required keys 'version' or 'project'", profile_path)
    else:
        reporter.log_warn("Target Config", "Neither config.yaml nor project-profile.yaml found in .dev-team/", dev_team_dir)

    # 4. Canonical Project Context (.dev-team/project-context.md)
    ctx_path = os.path.join(dev_team_dir, "project-context.md")
    if os.path.isfile(ctx_path) and os.path.getsize(ctx_path) > 50:
        reporter.log_pass("Target Context Store", "Canonical project-context.md exists")
    else:
        reporter.log_warn("Target Context Store", "project-context.md not found or empty", ctx_path)

    # 5. Baseline Documentation (docs/project/)
    docs_project_dir = os.path.join(target_path, "docs", "project")
    if os.path.isdir(docs_project_dir):
        reporter.log_pass("Target docs/project/ Directory")
    else:
        reporter.log_warn("Target docs/project/", "docs/project/ directory not yet established", docs_project_dir)

    # 6. features directory
    features_dir = os.path.join(dev_team_dir, "features")
    if os.path.isdir(features_dir):
        reporter.log_pass("Target features/ Directory")
        # Validate existing feature subdirectories
        feature_subdirs = [d for d in os.listdir(features_dir) if os.path.isdir(os.path.join(features_dir, d))]
        reporter.log_pass(f"Target Features Count: {len(feature_subdirs)}")
    else:
        reporter.log_warn("Target features/", ".dev-team/features directory not yet scaffolded", features_dir)


def main():
    parser = argparse.ArgumentParser(description="Deterministic Workspace Validator for Dev-Team and Target Projects")
    parser.add_argument("--root", type=str, default=None, help="Path to dev-team repository root (defaults to script parent's parent)")
    parser.add_argument("--target", type=str, default=None, help="Path to target application repository to validate target configuration")
    parser.add_argument("--verbose", "-v", action="store_true", help="Display detailed pass messages")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON result")

    args = parser.parse_args()
    reporter = ValidationReporter(verbose=args.verbose, json_output=args.json)

    if args.target:
        validate_target_repository(os.path.abspath(args.target), reporter)
    else:
        if args.root:
            root_path = os.path.abspath(args.root)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_path = os.path.abspath(os.path.join(script_dir, ".."))
        validate_dev_team_workspace(root_path, reporter)

    exit_code = reporter.print_summary()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
