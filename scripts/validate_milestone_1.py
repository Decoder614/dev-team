#!/usr/bin/env python3
"""
scripts/validate_milestone_1.py — Milestone 1 Core Foundation Verification Script

Validates the complete implementation of Milestone 1 as specified in docs/project/plan.md:
- Task M1-T01: Canonical Repository Organization (cli, adapters, schemas, etc.)
- Task M1-T02: Agent Skills Standard & Canonical Skill Directory Layout
- Task M1-T03: Standardized Templates Suite (feature deliverables & project scaffolding)
- Task M1-T04: JSON Schemas for Declarative Contracts (project-config, adapter-manifest, installation-manifest)
- Task M1-T05: Framework Policies & Quality Gates Configuration (workflow.yaml, quality-gates.yaml, defaults.yaml)

Returns:
  0 if all Milestone 1 verification checks pass
  1 if any check fails
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FAIL] Missing pyyaml. Run: pip install pyyaml")
    sys.exit(1)


def log_pass(msg):
    print(f"  [PASS] {msg}")


def log_fail(msg):
    print(f"  [FAIL] {msg}")


def validate_json_schema_minimal(data, schema, path="root"):
    """
    Lightweight, deterministic JSON schema validator supporting Draft-07 core keywords:
    type, required, properties, additionalProperties, enum, items, minLength, minimum, oneOf.
    """
    errors = []

    # 1. Type validation
    expected_type = schema.get("type")
    if expected_type:
        types = [expected_type] if isinstance(expected_type, str) else expected_type
        matched = False
        for t in types:
            if t == "object" and isinstance(data, dict):
                matched = True
            elif t == "array" and isinstance(data, list):
                matched = True
            elif t == "string" and isinstance(data, str):
                matched = True
            elif t == "integer" and isinstance(data, int) and not isinstance(data, bool):
                matched = True
            elif t == "number" and (isinstance(data, (int, float))) and not isinstance(data, bool):
                matched = True
            elif t == "boolean" and isinstance(data, bool):
                matched = True
            elif t == "null" and data is None:
                matched = True
        if not matched:
            errors.append(f"{path}: expected type {types}, got {type(data).__name__}")
            return errors

    # 2. Enum validation
    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: value '{data}' not in allowed enum {schema['enum']}")

    # 3. String constraints
    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: length {len(data)} < minLength {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], data):
            errors.append(f"{path}: string '{data}' does not match pattern '{schema['pattern']}'")

    # 4. Number constraints
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: value {data} < minimum {schema['minimum']}")

    # 5. Object constraints
    if isinstance(data, dict):
        required_keys = schema.get("required", [])
        for rk in required_keys:
            if rk not in data:
                errors.append(f"{path}: missing required property '{rk}'")

        properties = schema.get("properties", {})
        additional_allowed = schema.get("additionalProperties", True)

        for k, v in data.items():
            sub_path = f"{path}.{k}"
            if k in properties:
                sub_errs = validate_json_schema_minimal(v, properties[k], sub_path)
                errors.extend(sub_errs)
            elif additional_allowed is False:
                errors.append(f"{path}: additional property '{k}' not permitted")
            elif isinstance(additional_allowed, dict):
                sub_errs = validate_json_schema_minimal(v, additional_allowed, sub_path)
                errors.extend(sub_errs)

    # 6. Array constraints
    if isinstance(data, list) and "items" in schema:
        item_schema = schema["items"]
        for idx, item in enumerate(data):
            sub_path = f"{path}[{idx}]"
            sub_errs = validate_json_schema_minimal(item, item_schema, sub_path)
            errors.extend(sub_errs)

    # 7. oneOf constraints
    if "oneOf" in schema:
        sub_schemas = schema["oneOf"]
        passed = 0
        for s in sub_schemas:
            if len(validate_json_schema_minimal(data, s, path)) == 0:
                passed += 1
        if passed != 1:
            errors.append(f"{path}: did not match exactly one schema in oneOf (matched {passed})")

    return errors


def test_task_m1_t01(repo_root):
    print("\n--- Task M1-T01: Canonical Repository Organization ---")
    failures = 0
    required_dirs = [
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
    for d in required_dirs:
        p = os.path.join(repo_root, d)
        if os.path.isdir(p):
            log_pass(f"Canonical directory exists: {d}/")
        else:
            log_fail(f"Missing canonical directory: {d}/")
            failures += 1

    # Check adapter subdirectories
    adapters = ["codex", "claude-code", "cursor", "copilot", "gemini"]
    for ad in adapters:
        ad_p = os.path.join(repo_root, "adapters", ad)
        if os.path.isdir(ad_p):
            log_pass(f"Adapter directory exists: adapters/{ad}/")
        else:
            log_fail(f"Missing adapter directory: adapters/{ad}/")
            failures += 1

    # Check root documentation links in README.md
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    for d in required_dirs:
        if d in readme_content:
            log_pass(f"README.md references directory: {d}")
        else:
            log_fail(f"README.md does not reference directory: {d}")
            failures += 1

    return failures == 0


def test_task_m1_t02(repo_root):
    print("\n--- Task M1-T02: Agent Skills Standard & Canonical Skill Directory Layout ---")
    failures = 0

    # 1. Standard specification doc
    spec_path = os.path.join(repo_root, "docs", "skills-standard.md")
    if os.path.isfile(spec_path) and os.path.getsize(spec_path) > 200:
        log_pass("Skill specification standard doc exists: docs/skills-standard.md")
        with open(spec_path, "r", encoding="utf-8") as f:
            c = f.read()
        expected_keywords = [
            "Agent Skills Standard Specification",
            "Frontmatter Specification",
            "Markdown Body Structure",
            "Skill Resolution Hierarchy",
            "SAFE-001",
        ]
        for kw in expected_keywords:
            if kw in c:
                log_pass(f"docs/skills-standard.md contains '{kw}'")
            else:
                log_fail(f"docs/skills-standard.md missing '{kw}'")
                failures += 1
    else:
        log_fail("Missing or empty docs/skills-standard.md")
        failures += 1

    # 2. Template SKILL.md
    tmpl_path = os.path.join(repo_root, "templates", "SKILL.md")
    if os.path.isfile(tmpl_path) and os.path.getsize(tmpl_path) > 100:
        log_pass("Template SKILL.md exists: templates/SKILL.md")
        with open(tmpl_path, "r", encoding="utf-8") as f:
            c = f.read()
        if c.startswith("---") and "name:" in c and "description:" in c:
            log_pass("templates/SKILL.md contains valid YAML frontmatter header")
        else:
            log_fail("templates/SKILL.md missing standard frontmatter format")
            failures += 1
    else:
        log_fail("Missing or empty templates/SKILL.md")
        failures += 1

    # 3. Canonical skills frontmatter validation
    skills_dir = os.path.join(repo_root, "skills")
    skill_folders = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    for sf in sorted(skill_folders):
        sk_file = os.path.join(skills_dir, sf, "SKILL.md")
        if not os.path.isfile(sk_file):
            log_fail(f"Missing SKILL.md in skills/{sf}")
            failures += 1
            continue
        with open(sk_file, "r", encoding="utf-8") as f:
            txt = f.read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.DOTALL)
        if not m:
            log_fail(f"Frontmatter delimiter missing in skills/{sf}/SKILL.md")
            failures += 1
            continue
        try:
            fm = yaml.safe_load(m.group(1))
            if not isinstance(fm, dict):
                log_fail(f"Frontmatter not a dict in skills/{sf}/SKILL.md")
                failures += 1
            elif fm.get("name") != sf:
                log_fail(f"Frontmatter name '{fm.get('name')}' != '{sf}' in skills/{sf}/SKILL.md")
                failures += 1
            elif not fm.get("description") or len(str(fm.get("description")).strip()) < 15:
                log_fail(f"Frontmatter description too short in skills/{sf}/SKILL.md")
                failures += 1
            else:
                log_pass(f"Skill frontmatter valid: skills/{sf}/SKILL.md")
        except Exception as e:
            log_fail(f"YAML parsing error in skills/{sf}/SKILL.md: {e}")
            failures += 1

    return failures == 0


def test_task_m1_t03(repo_root):
    print("\n--- Task M1-T03: Standardized Templates Suite ---")
    failures = 0
    templates_dir = os.path.join(repo_root, "templates")

    # Feature templates
    feature_templates = [
        "requirement.md",
        "system-design.md",
        "plan.md",
        "task.md",
        "qa-report.md",
        "bug-report.md",
        "SKILL.md",
    ]
    for ft in feature_templates:
        p = os.path.join(templates_dir, ft)
        if os.path.isfile(p) and os.path.getsize(p) > 50:
            log_pass(f"Feature template exists: templates/{ft}")
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            # Check for template placeholders
            if re.search(r"\[.+?\]|\{\{.+?\}\}", content):
                log_pass(f"  Template variables verified in templates/{ft}")
            else:
                log_fail(f"  No template placeholder variables found in templates/{ft}")
                failures += 1
        else:
            log_fail(f"Missing feature template: templates/{ft}")
            failures += 1

    # Project templates
    project_templates_dir = os.path.join(templates_dir, "project")
    project_templates = [
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
    for pt in project_templates:
        p = os.path.join(project_templates_dir, pt)
        if os.path.isfile(p) and os.path.getsize(p) > 50:
            log_pass(f"Project template exists: templates/project/{pt}")
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            if re.search(r"\[.+?\]|\{\{.+?\}\}", content) or pt.endswith(".yaml"):
                log_pass(f"  Template variables verified in templates/project/{pt}")
            else:
                log_fail(f"  No template placeholder variables found in templates/project/{pt}")
                failures += 1
        else:
            log_fail(f"Missing project template: templates/project/{pt}")
            failures += 1

    return failures == 0


def test_task_m1_t04(repo_root):
    print("\n--- Task M1-T04: JSON Schemas for Declarative Contracts ---")
    failures = 0
    schemas_dir = os.path.join(repo_root, "schemas")

    # 1. project-config.schema.json
    cfg_schema_path = os.path.join(schemas_dir, "project-config.schema.json")
    if os.path.isfile(cfg_schema_path) and os.path.getsize(cfg_schema_path) > 100:
        log_pass("Schema exists: schemas/project-config.schema.json")
        with open(cfg_schema_path, "r", encoding="utf-8") as f:
            cfg_schema = json.load(f)

        # Validate sample project config
        sample_config = {
            "version": 1,
            "project": {
                "name": "Gotilo",
                "type": "flutter_application",
                "description": "Property management application",
            },
            "technology": {
                "primary_language": "dart",
                "framework": "flutter",
                "state_management": "bloc",
                "backend": "supabase",
            },
            "distribution": {
                "mode": "hybrid",
            },
            "skills": {
                "source": "global",
                "enabled": ["project-initializer", "flutter-development"],
            },
            "platforms": {
                "enabled": ["codex"],
            },
            "initialization": {
                "status": "completed",
                "initialized_at": "2026-11-06T12:00:00Z",
                "version": "1.1.0",
            },
        }
        errs = validate_json_schema_minimal(sample_config, cfg_schema)
        if not errs:
            log_pass("Sample project configuration validated against schemas/project-config.schema.json")
        else:
            log_fail(f"Sample project config failed schema validation: {errs}")
            failures += 1

        # Negative test case (missing required 'project' section)
        invalid_cfg = {"version": 1}
        neg_errs = validate_json_schema_minimal(invalid_cfg, cfg_schema)
        if neg_errs:
            log_pass("Negative test passed: Missing 'project' section correctly rejected")
        else:
            log_fail("Negative test failed: Schema accepted config missing 'project'")
            failures += 1
    else:
        log_fail("Missing schemas/project-config.schema.json")
        failures += 1

    # 2. adapter-manifest.schema.json
    adapter_schema_path = os.path.join(schemas_dir, "adapter-manifest.schema.json")
    if os.path.isfile(adapter_schema_path) and os.path.getsize(adapter_schema_path) > 100:
        log_pass("Schema exists: schemas/adapter-manifest.schema.json")
        with open(adapter_schema_path, "r", encoding="utf-8") as f:
            adapter_schema = json.load(f)

        sample_manifest = {
            "id": "codex",
            "name": "OpenAI Codex CLI",
            "version": "1.0.0",
            "capabilities": {
                "agent_skills": True,
                "project_instructions": True,
                "global_skills": True,
                "project_skills": True,
                "subagents": True,
                "tool_execution": True,
            },
            "locations": {
                "global_skills_dir": {
                    "windows": "$USERPROFILE/.codex/skills",
                    "unix": "~/.codex/skills",
                },
                "project_skills_dir": ".agents/skills",
                "fallback_project_skills_dir": ".codex/skills",
                "project_instructions": "AGENTS.md",
            },
            "linking": {
                "preferred_strategy": "symlink",
                "windows_fallback": "junction",
                "safe_fallback": "copy",
            },
        }
        errs = validate_json_schema_minimal(sample_manifest, adapter_schema)
        if not errs:
            log_pass("Sample adapter manifest validated against schemas/adapter-manifest.schema.json")
        else:
            log_fail(f"Sample adapter manifest failed schema validation: {errs}")
            failures += 1

        # Negative test: invalid ID format with uppercase
        invalid_manifest = dict(sample_manifest, id="Codex_Invalid")
        neg_errs = validate_json_schema_minimal(invalid_manifest, adapter_schema)
        if neg_errs:
            log_pass("Negative test passed: Invalid adapter ID correctly rejected")
        else:
            log_fail("Negative test failed: Schema accepted invalid adapter ID")
            failures += 1
    else:
        log_fail("Missing schemas/adapter-manifest.schema.json")
        failures += 1

    # 3. installation-manifest.schema.json
    install_schema_path = os.path.join(schemas_dir, "installation-manifest.schema.json")
    if os.path.isfile(install_schema_path) and os.path.getsize(install_schema_path) > 100:
        log_pass("Schema exists: schemas/installation-manifest.schema.json")
        with open(install_schema_path, "r", encoding="utf-8") as f:
            install_schema = json.load(f)

        sample_install = {
            "dev_team_version": "1.1.0",
            "installation_mode": "hybrid",
            "platform": "codex",
            "installed_at": "2026-11-06T12:00:00Z",
            "artifacts": [
                {
                    "path": ".agents/skills/project-initializer",
                    "type": "skill_projection",
                    "strategy": "symlink",
                    "source": "~/.dev-team/skills/project-initializer",
                    "source_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "managed_by_dev_team": True,
                    "user_modified": False,
                },
                {
                    "path": ".dev-team/config.yaml",
                    "type": "configuration",
                    "strategy": "managed_file",
                    "managed_by_dev_team": True,
                    "user_modified": False,
                },
            ],
        }
        errs = validate_json_schema_minimal(sample_install, install_schema)
        if not errs:
            log_pass("Sample installation manifest validated against schemas/installation-manifest.schema.json")
        else:
            log_fail(f"Sample installation manifest failed schema validation: {errs}")
            failures += 1

        # Negative test: invalid installation_mode
        invalid_install = dict(sample_install, installation_mode="unsupported_mode")
        neg_errs = validate_json_schema_minimal(invalid_install, install_schema)
        if neg_errs:
            log_pass("Negative test passed: Invalid installation_mode correctly rejected")
        else:
            log_fail("Negative test failed: Schema accepted unsupported installation_mode")
            failures += 1
    else:
        log_fail("Missing schemas/installation-manifest.schema.json")
        failures += 1

    return failures == 0


def test_task_m1_t05(repo_root):
    print("\n--- Task M1-T05: Framework Policies & Quality Gates Configuration ---")
    failures = 0
    config_dir = os.path.join(repo_root, "config")

    # 1. workflow.yaml
    wf_path = os.path.join(config_dir, "workflow.yaml")
    if os.path.isfile(wf_path):
        with open(wf_path, "r", encoding="utf-8") as f:
            wf_cfg = yaml.safe_load(f)
        log_pass("Parsed config/workflow.yaml successfully")
        workflows = wf_cfg.get("workflows", {})
        if len(workflows) >= 9:
            log_pass(f"All {len(workflows)} engineering workflows registered")
        else:
            log_fail(f"Expected at least 9 workflows, found {len(workflows)}")
            failures += 1

        for w_name, w_data in workflows.items():
            if "governing_role" in w_data:
                log_pass(f"Workflow '{w_name}' has governing_role: '{w_data['governing_role']}'")
            else:
                log_fail(f"Workflow '{w_name}' missing 'governing_role'")
                failures += 1
            if "entry_point" in w_data and os.path.isfile(os.path.join(repo_root, w_data["entry_point"])):
                log_pass(f"Workflow '{w_name}' entry_point verified: {w_data['entry_point']}")
            else:
                log_fail(f"Workflow '{w_name}' has missing entry_point: {w_data.get('entry_point')}")
                failures += 1
    else:
        log_fail("Missing config/workflow.yaml")
        failures += 1

    # 2. quality-gates.yaml
    qg_path = os.path.join(config_dir, "quality-gates.yaml")
    if os.path.isfile(qg_path):
        with open(qg_path, "r", encoding="utf-8") as f:
            qg_cfg = yaml.safe_load(f)
        log_pass("Parsed config/quality-gates.yaml successfully")

        # Check safety boundaries SAFE-001 to SAFE-012
        safety_boundaries = qg_cfg.get("safety_boundaries", {})
        for i in range(1, 13):
            s_id = f"SAFE-{i:03d}"
            if s_id in safety_boundaries:
                log_pass(f"Defined safety boundary: {s_id} ({safety_boundaries[s_id].get('title')})")
            else:
                log_fail(f"Missing safety boundary: {s_id}")
                failures += 1

        # Check standard lifecycle gates
        standard_gates = [
            "requirements",
            "architecture",
            "planning",
            "implementation",
            "testing",
            "code_review",
            "final_acceptance",
        ]
        for g in standard_gates:
            if g in qg_cfg:
                log_pass(f"Lifecycle gate configured: {g}")
            else:
                log_fail(f"Missing lifecycle gate: {g}")
                failures += 1
    else:
        log_fail("Missing config/quality-gates.yaml")
        failures += 1

    # 3. defaults.yaml
    df_path = os.path.join(config_dir, "defaults.yaml")
    if os.path.isfile(df_path):
        with open(df_path, "r", encoding="utf-8") as f:
            df_cfg = yaml.safe_load(f)
        log_pass("Parsed config/defaults.yaml successfully")

        required_paths = [
            "features_directory",
            "templates_directory",
            "agents_directory",
            "skills_directory",
            "workflows_directory",
            "schemas_directory",
            "adapters_directory",
            "cli_directory",
        ]
        paths = df_cfg.get("paths", {})
        for rp in required_paths:
            if rp in paths:
                log_pass(f"Default path defined: {rp} = {paths[rp]}")
            else:
                log_fail(f"Missing default path: {rp}")
                failures += 1

        # Check artifact and task statuses
        task_statuses = df_cfg.get("task_statuses", {}).get("allowed", [])
        expected_tasks = ["PENDING", "IN_PROGRESS", "BLOCKED", "COMPLETED", "NEEDS_REVIEW"]
        if set(expected_tasks).issubset(set(task_statuses)):
            log_pass(f"All 5 standard task statuses defined: {expected_tasks}")
        else:
            log_fail(f"Task statuses incomplete: {task_statuses}")
            failures += 1

        artifact_statuses = df_cfg.get("artifact_statuses", {}).get("allowed", [])
        expected_artifacts = ["DRAFT", "IN_REVIEW", "APPROVED", "NEEDS_REVISION", "SUPERSEDED"]
        if set(expected_artifacts).issubset(set(artifact_statuses)):
            log_pass(f"All 5 standard artifact statuses defined: {expected_artifacts}")
        else:
            log_fail(f"Artifact statuses incomplete: {artifact_statuses}")
            failures += 1
    else:
        log_fail("Missing config/defaults.yaml")
        failures += 1

    return failures == 0


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("======================================================================")
    print("        Dev-Team Milestone 1 Verification (Core Foundation)          ")
    print("======================================================================")
    print(f"Repository Root: {repo_root}")

    results = {
        "M1-T01: Canonical Repository Organization": test_task_m1_t01(repo_root),
        "M1-T02: Agent Skills Standard & Layout": test_task_m1_t02(repo_root),
        "M1-T03: Standardized Templates Suite": test_task_m1_t03(repo_root),
        "M1-T04: JSON Schemas for Declarative Contracts": test_task_m1_t04(repo_root),
        "M1-T05: Framework Policies & Quality Gates": test_task_m1_t05(repo_root),
    }

    print("\n======================================================================")
    print("                         Summary Results                              ")
    print("======================================================================")
    all_passed = True
    for task_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {task_name}")
        if not passed:
            all_passed = False

    print("======================================================================")
    if all_passed:
        print("RESULT: ALL MILESTONE 1 VERIFICATION CHECKS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("RESULT: ONE OR MORE MILESTONE 1 CHECKS FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

