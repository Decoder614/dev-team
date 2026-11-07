#!/usr/bin/env python3
"""
skills/project-initializer/scripts/check-project-structure.py

Deterministic structure inspector and manifest detection utility for Dev-Team onboarding.
Inspects any target directory tree using only the standard Python library (zero dependencies).

Returns:
  - Exit code 0 on successful inspection.
  - Structured JSON or human-readable summary detailing repository classification,
    detected tech stack, existing manifests, instruction files, and directory patterns.
"""

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path


# Ignored directory names for cleanliness calculation
IGNORED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    ".dart_tool",
    "build",
    "dist",
    "target",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    ".gradle",
    ".gemini",
}

# Recognized manifest files mapped to ecosystem
MANIFEST_MAP = {
    "pubspec.yaml": "Flutter / Dart",
    "package.json": "Node.js / JavaScript / TypeScript",
    "tsconfig.json": "TypeScript",
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "Pipfile": "Python",
    "setup.py": "Python",
    "Cargo.toml": "Rust",
    "go.mod": "Go",
    "build.gradle": "Java / Kotlin (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "pom.xml": "Java (Maven)",
    "Gemfile": "Ruby",
    "composer.json": "PHP",
    "Package.swift": "Swift",
}

# Recognized root instruction and metadata files
INSTRUCTION_FILES = [
    "AGENTS.md",
    "rules.md",
    "DESIGN.md",
    "CLAUDE.md",
    ".cursorrules",
    ".github/copilot-instructions.md",
    "CONTRIBUTING.md",
    "README.md",
]

# Source directory patterns
SOURCE_DIR_PATTERNS = [
    "lib",
    "src",
    "app",
    "packages",
    "cmd",
    "internal",
    "pkg",
    "crates",
    "bin",
    "test",
    "tests",
]


def inspect_directory(target_path):
    target_path = os.path.abspath(target_path)
    if not os.path.isdir(target_path):
        return {
            "error": f"Target path is not an existing directory: {target_path}",
            "classification": "UNKNOWN",
        }

    # 1. Scan root entries
    try:
        entries = os.listdir(target_path)
    except Exception as e:
        return {
            "error": f"Failed to list directory {target_path}: {e}",
            "classification": "UNKNOWN",
        }

    # Filter out ignored dirs
    meaningful_entries = [
        e for e in entries if e not in IGNORED_DIRS and not e.startswith(".git")
    ]

    # 2. Check for manifests
    detected_manifests = {}
    for manifest_name, ecosystem in MANIFEST_MAP.items():
        m_path = os.path.join(target_path, manifest_name)
        if os.path.isfile(m_path):
            detected_manifests[manifest_name] = {
                "ecosystem": ecosystem,
                "size_bytes": os.path.getsize(m_path),
            }

    # Check for .NET solution / csproj
    csproj_files = glob.glob(os.path.join(target_path, "*.csproj"))
    sln_files = glob.glob(os.path.join(target_path, "*.sln"))
    if csproj_files or sln_files:
        detected_manifests["*.csproj / *.sln"] = {
            "ecosystem": ".NET / C#",
            "files": [os.path.basename(f) for f in (csproj_files + sln_files)],
        }

    # 3. Check for root instruction files
    detected_instructions = []
    for inst_name in INSTRUCTION_FILES:
        inst_path = os.path.join(target_path, inst_name)
        if os.path.isfile(inst_path):
            detected_instructions.append(inst_name)

    # 4. Check for source directories
    detected_source_dirs = []
    for s_dir in SOURCE_DIR_PATTERNS:
        dir_full_path = os.path.join(target_path, s_dir)
        if os.path.isdir(dir_full_path):
            detected_source_dirs.append(s_dir)

    # 5. Check for Dev-Team infrastructure
    dev_team_path = os.path.join(target_path, ".dev-team")
    dev_team_status = {
        "installed": os.path.isdir(dev_team_path),
        "config_yaml": os.path.isfile(os.path.join(dev_team_path, "config.yaml")),
        "project_context_md": os.path.isfile(
            os.path.join(dev_team_path, "project-context.md")
        ),
        "initialization_report_md": os.path.isfile(
            os.path.join(dev_team_path, "initialization-report.md")
        ),
        "features_dir": os.path.isdir(os.path.join(dev_team_path, "features")),
    }

    docs_project_path = os.path.join(target_path, "docs", "project")
    docs_status = {
        "docs_project_exists": os.path.isdir(docs_project_path),
        "docs_found": [],
    }
    if docs_status["docs_project_exists"]:
        for doc_file in [
            "overview.md",
            "requirements.md",
            "system-design.md",
            "plan.md",
            "tech-stack.md",
            "architecture.md",
        ]:
            if os.path.isfile(os.path.join(docs_project_path, doc_file)):
                docs_status["docs_found"].append(doc_file)

    # 6. Extract tech stack clues
    tech_stack = extract_tech_stack_clues(target_path, detected_manifests)

    # 7. Classification logic
    classification = determine_classification(
        meaningful_entries,
        detected_manifests,
        detected_source_dirs,
        dev_team_status,
        docs_status,
    )

    return {
        "target_path": target_path,
        "classification": classification,
        "primary_project_type": tech_stack.get("project_type", "unknown"),
        "tech_stack": tech_stack,
        "manifests": detected_manifests,
        "instructions": detected_instructions,
        "source_directories": detected_source_dirs,
        "dev_team_status": dev_team_status,
        "docs_status": docs_status,
        "total_entries": len(entries),
        "meaningful_entries_count": len(meaningful_entries),
    }


def determine_classification(
    meaningful_entries, manifests, source_dirs, dev_team_status, docs_status
):
    # Empty if 0 meaningful entries or only default bootstrap files
    bootstrap_files = {"README.md", ".gitignore", "LICENSE", "LICENCE"}
    non_bootstrap = [e for e in meaningful_entries if e not in bootstrap_files]

    if len(meaningful_entries) == 0 or len(non_bootstrap) == 0:
        return "EMPTY"

    has_manifests = len(manifests) > 0
    has_source = len(source_dirs) > 0
    has_dev_team = dev_team_status["installed"]

    if has_manifests and has_source:
        if has_dev_team and dev_team_status["project_context_md"] and len(docs_status["docs_found"]) >= 4:
            return "EXISTING"
        elif has_dev_team:
            return "PARTIAL"
        return "EXISTING"

    if has_manifests or has_source or has_dev_team:
        return "PARTIAL"

    return "EXISTING"


def extract_tech_stack_clues(target_path, manifests):
    stack = {
        "languages": [],
        "frameworks": [],
        "ecosystems": [],
        "project_type": "unknown",
        "state_management": None,
        "routing": None,
        "database": None,
    }

    # Flutter / Dart analysis
    if "pubspec.yaml" in manifests:
        stack["ecosystems"].append("Flutter / Dart")
        stack["languages"].append("Dart")
        pubspec_path = os.path.join(target_path, "pubspec.yaml")
        try:
            with open(pubspec_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "flutter:" in content:
                stack["frameworks"].append("Flutter")
                stack["project_type"] = "flutter_application"
            else:
                stack["project_type"] = "dart_package"

            # Check for common flutter libraries
            if re.search(r"\bflutter_bloc\b|\bbloc\b", content):
                stack["state_management"] = "BLoC"
            elif re.search(r"\bflutter_riverpod\b|\briverpod\b", content):
                stack["state_management"] = "Riverpod"
            elif re.search(r"\bprovider\b", content):
                stack["state_management"] = "Provider"

            if re.search(r"\bgo_router\b", content):
                stack["routing"] = "GoRouter"
            elif re.search(r"\bauto_route\b", content):
                stack["routing"] = "AutoRoute"

            if re.search(r"\bsupabase_flutter\b", content):
                stack["database"] = "Supabase"
            elif re.search(r"\bdrift\b", content):
                stack["database"] = "Drift (SQLite)"
            elif re.search(r"\bhive\b", content):
                stack["database"] = "Hive"
        except Exception:
            pass

    # Node.js / TypeScript analysis
    if "package.json" in manifests:
        stack["ecosystems"].append("Node.js")
        pkg_path = os.path.join(target_path, "package.json")
        try:
            with open(pkg_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            deps = data.get("dependencies", {})
            dev_deps = data.get("devDependencies", {})
            all_deps = {**deps, **dev_deps}

            if "typescript" in all_deps or "tsconfig.json" in manifests:
                stack["languages"].append("TypeScript")
            else:
                stack["languages"].append("JavaScript")

            if "next" in all_deps:
                stack["frameworks"].append("Next.js")
                stack["project_type"] = "web_app"
            elif "react" in all_deps:
                stack["frameworks"].append("React")
                stack["project_type"] = "web_app"
            elif "vue" in all_deps:
                stack["frameworks"].append("Vue")
                stack["project_type"] = "web_app"
            elif "express" in all_deps or "fastify" in all_deps or "nest" in all_deps:
                stack["frameworks"].append("Express / Node Backend")
                stack["project_type"] = "backend_service"

            if "@reduxjs/toolkit" in all_deps:
                stack["state_management"] = "Redux Toolkit"
            elif "zustand" in all_deps:
                stack["state_management"] = "Zustand"
        except Exception:
            pass

    # Python analysis
    if "pyproject.toml" in manifests or "requirements.txt" in manifests:
        stack["ecosystems"].append("Python")
        stack["languages"].append("Python")
        req_path = os.path.join(target_path, "requirements.txt")
        pyproject_path = os.path.join(target_path, "pyproject.toml")
        combined_text = ""
        for p in (req_path, pyproject_path):
            if os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        combined_text += f.read() + "\n"
                except Exception:
                    pass

        if "fastapi" in combined_text.lower():
            stack["frameworks"].append("FastAPI")
            stack["project_type"] = "backend_service"
        elif "django" in combined_text.lower():
            stack["frameworks"].append("Django")
            stack["project_type"] = "web_app"
        elif "flask" in combined_text.lower():
            stack["frameworks"].append("Flask")
            stack["project_type"] = "backend_service"

    # Rust analysis
    if "Cargo.toml" in manifests:
        stack["ecosystems"].append("Rust")
        stack["languages"].append("Rust")
        stack["project_type"] = "cli_tool"

    # Go analysis
    if "go.mod" in manifests:
        stack["ecosystems"].append("Go")
        stack["languages"].append("Go")
        stack["project_type"] = "backend_service"

    # Clean duplicates
    stack["languages"] = sorted(list(set(stack["languages"])))
    stack["frameworks"] = sorted(list(set(stack["frameworks"])))
    stack["ecosystems"] = sorted(list(set(stack["ecosystems"])))

    return stack


def main():
    parser = argparse.ArgumentParser(
        description="Inspect project structure, manifests, and classify repository for Dev-Team."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Target repository path (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=True,
        help="Output results in JSON format (default: True)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print human-readable summary instead of raw JSON",
    )

    args = parser.parse_args()
    report = inspect_directory(args.path)

    if args.summary:
        print("============================================================")
        print("Dev-Team Repository Structure Inspection Report")
        print("============================================================")
        print(f"Target Path:         {report.get('target_path')}")
        print(f"Classification:      {report.get('classification')}")
        print(f"Primary Project Type: {report.get('primary_project_type')}")
        print(f"Detected Languages:  {', '.join(report.get('tech_stack', {}).get('languages', [])) or 'None'}")
        print(f"Detected Frameworks: {', '.join(report.get('tech_stack', {}).get('frameworks', [])) or 'None'}")
        print(f"Manifests Found:     {', '.join(report.get('manifests', {}).keys()) or 'None'}")
        print(f"Instructions Found:  {', '.join(report.get('instructions', [])) or 'None'}")
        print(f"Source Directories:  {', '.join(report.get('source_directories', [])) or 'None'}")
        print(f"Dev-Team Installed:  {report.get('dev_team_status', {}).get('installed')}")
        print("============================================================")
    else:
        print(json.dumps(report, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()

