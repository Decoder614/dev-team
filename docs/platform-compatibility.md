# Dev-Team Platform Compatibility & Adapter Guide

> **Cross-Platform AI Software Engineering**  
> Technical specification for platform adapters, skill discovery locations, instruction mappings, and capability matrices across supported AI coding platforms (Version 1.1).

---

## 1. Overview & Adapter Architecture

Dev-Team is designed from the ground up to be **independent of any single AI coding platform** (`REQ-020`, `REQ-084`). While OpenAI Codex CLI serves as our initial reference implementation, Dev-Team’s core skills and workflows are completely decoupled from proprietary platform APIs.

Platform integration is handled via **modular platform adapters** located in `adapters/<platform-id>/`. Each adapter translates canonical Dev-Team assets into the formats, discovery paths, and instruction conventions required by that specific AI platform:

```text
┌────────────────────────────────────────────────────────┐
│             Dev-Team Canonical Core Layer              │
│  - Agent Skills (skills/*/SKILL.md)                    │
│  - Standardized Templates (templates/*)                │
│  - Role Specifications (agents/*.toml)                 │
└───────────────────────────┬────────────────────────────┘
                            │
               Platform Adapter Translation
                            ▼
┌────────────────────────────────────────────────────────┐
│               Platform Adapters Layer                  │
│  ├── adapters/codex/          (OpenAI Codex CLI)       │
│  ├── adapters/claude-code/    (Anthropic Claude Code)  │
│  ├── adapters/cursor/         (Cursor IDE)             │
│  ├── adapters/copilot/        (GitHub Copilot)         │
│  └── adapters/gemini/         (Google Antigravity/CLI) │
└───────────────────────────┬────────────────────────────┘
                            │
                 Projections & Instructions
                            ▼
┌────────────────────────────────────────────────────────┐
│               Target AI Platform Discovery             │
│  - Discovery Paths (~/.codex/skills, .agents/skills)   │
│  - Instruction Files (AGENTS.md, CLAUDE.md, etc.)      │
└────────────────────────────────────────────────────────┘
```

---

## 2. Platform Capability Matrix

| Platform | Adapter ID | Status | Agent Skills (`SKILL.md`) | Global Skills | Project Skills | Root Instructions | Subagent Delegation |
|---|---|---|---|---|---|---|---|
| **OpenAI Codex CLI** | `codex` | **Reference / Tier 1** | Native | Yes (`~/.codex/skills/`) | Yes (`.agents/skills/`) | `AGENTS.md` | Yes |
| **Anthropic Claude Code** | `claude-code` | Planned (M7) | Native | Yes (`~/.claude/skills/`) | Yes (`.claude/skills/`) | `CLAUDE.md` | No |
| **Cursor IDE** | `cursor` | Planned (M7) | Adapted | No | Yes (`.cursor/skills/`) | `.cursorrules` | Limited |
| **GitHub Copilot** | `copilot` | Planned (M7) | Adapted | No | Yes (`.github/skills/`) | `.github/copilot-instructions.md` | No |
| **Google Antigravity / Gemini** | `gemini` | Planned (M7) | Native | Yes (`~/.gemini/skills/`) | Yes (`.gemini/skills/`) | `AGENTS.md` / `rules.md` | Yes |

---

## 3. Platform Discovery & Location Details

### 3.1 OpenAI Codex CLI (Reference Integration)
- **Adapter Directory:** `adapters/codex/`
- **Global Skills Directory:**
  - Windows: `$env:USERPROFILE\.codex\skills\`
  - Unix / macOS: `~/.codex/skills/`
- **Project Skills Directory:**
  - Primary: `<workspace>/.agents/skills/`
  - Fallback: `<workspace>/.codex/skills/`
- **Root Instructions:** `AGENTS.md` in repository root.
- **Skill Discovery Format:** Folders containing `SKILL.md` with YAML frontmatter.

### 3.2 Anthropic Claude Code
- **Adapter Directory:** `adapters/claude-code/`
- **Global Skills Directory:**
  - Windows: `$env:APPDATA\claude\skills\`
  - Unix / macOS: `~/.claude/skills/`
- **Project Skills Directory:** `<workspace>/.claude/skills/`
- **Root Instructions:** `CLAUDE.md` in repository root.
- **Skill Discovery Format:** Markdown instruction skills conforming to Claude Code format.

### 3.3 Cursor IDE
- **Adapter Directory:** `adapters/cursor/`
- **Global Skills Directory:** N/A (Project-scoped)
- **Project Skills Directory:** `<workspace>/.cursor/skills/`
- **Root Instructions:** `.cursorrules` or `.cursor/rules/*.mdc`
- **Skill Discovery Format:** Rules and prompt files linked into Cursor's configuration.

### 3.4 GitHub Copilot Workspace / CLI
- **Adapter Directory:** `adapters/copilot/`
- **Global Skills Directory:** N/A (Project-scoped)
- **Project Skills Directory:** `<workspace>/.github/skills/`
- **Root Instructions:** `.github/copilot-instructions.md`

### 3.5 Google Antigravity / Gemini CLI
- **Adapter Directory:** `adapters/gemini/`
- **Global Skills Directory:**
  - Windows: `$env:USERPROFILE\.gemini\antigravity\skills\`
  - Unix / macOS: `~/.gemini/antigravity/skills/`
- **Project Skills Directory:** `<workspace>/.gemini/antigravity/skills/`
- **Root Instructions:** `AGENTS.md` and `rules.md`
- **Skill Discovery Format:** `SKILL.md` with YAML frontmatter.

---

## 4. Platform Adapter Manifest Specification

Each platform adapter provides an `adapter.yaml` manifest satisfying `schemas/adapter-manifest.schema.json`:

```yaml
id: codex
name: OpenAI Codex CLI
version: 1.0.0
description: Official platform adapter for OpenAI Codex CLI.

capabilities:
  agent_skills: true
  project_instructions: true
  global_skills: true
  project_skills: true
  subagents: true
  tool_execution: true

locations:
  global_skills_dir:
    windows: "$USERPROFILE/.codex/skills"
    unix: "~/.codex/skills"
  project_skills_dir: ".agents/skills"
  fallback_project_skills_dir: ".codex/skills"
  project_instructions: "AGENTS.md"

linking:
  preferred_strategy: "symlink"
  windows_fallback: "junction"
  safe_fallback: "copy"

instruction_template: "templates/project/AGENTS.md"
```

---

## 5. Adding a New Platform Adapter

To contribute a new platform adapter to Dev-Team:
1. Create a new directory under `adapters/<platform-id>/`.
2. Author `manifest.yaml` specifying discovery paths and capabilities against `schemas/adapter-manifest.schema.json`.
3. Provide an `adapter.py` implementing the adapter interface:
   - `detect_platform()`: Detects if the platform CLI or IDE configuration is present.
   - `get_discovery_path()`: Returns the target discovery path for global and local modes.
   - `project_skills()`: Safely links or copies canonical skills into the platform's discovery path.
   - `generate_instructions()`: Emits the platform-appropriate root instruction file.
4. Add unit and integration tests under `cli/tests/test_adapters.py`.
5. Register the platform in `dev-team` CLI platform registry.

