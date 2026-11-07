# Dev-Team Platform Adapters

This directory hosts modular platform adapters translating Dev-Team's platform-independent Agent Skills (`SKILL.md`) and workflows into platform-specific discovery paths, projection strategies, and instruction files.

## Supported & Planned Platforms
- `adapters/codex/`: OpenAI Codex CLI adapter (Reference integration)
- `adapters/claude-code/`: Anthropic Claude Code adapter
- `adapters/cursor/`: Cursor IDE adapter
- `adapters/copilot/`: GitHub Copilot adapter
- `adapters/gemini/`: Google Antigravity / Gemini CLI adapter

Each adapter provides a declarative `manifest.yaml` adhering to `schemas/adapter-manifest.schema.json` and an integration handler (`adapter.py`).

