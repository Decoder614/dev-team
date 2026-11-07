# Repository Initialization Audit Report — [Project Name]

> **Dev-Team Onboarding Audit & Scaffolding Record**  
> Comprehensive audit record of repository discovery, tech stack classification, generated files, preserved assets, and unresolved items for [Project Name].

---

## 1. Execution Summary

- **Initialization Date:** [YYYY-MM-DD HH:MM:SS]
- **Target Repository Path:** `[Target Directory Path]`
- **Repository Classification:** `[EXISTING | EMPTY | PARTIAL]`
- **Detected Project Type:** `[flutter_application | web_app | backend_service | cli_tool | monorepo | library]`
- **Total Files Scanned:** [Count]
- **Total Artifacts Generated:** [Count]
- **Total Files Preserved (Not Overwritten):** [Count]

---

## 2. Detected Manifests & Technology Stack

### 2.1 Package Manifests Detected
- [x] `pubspec.yaml` (Flutter / Dart) <!-- Check applicable -->
- [ ] `package.json` (Node.js / TypeScript / JavaScript)
- [ ] `pyproject.toml` / `requirements.txt` (Python)
- [ ] `Cargo.toml` (Rust)
- [ ] `go.mod` (Go)
- [ ] `build.gradle` / `pom.xml` (Java / Kotlin)

### 2.2 Detected Stack Components
- **Primary Language:** `[Language]`
- **Framework:** `[Framework]`
- **State Management:** `[State Library / Detected or None]`
- **Routing:** `[Routing Library / Detected or None]`
- **Dependency Injection:** `[DI Library / Detected or None]`
- **Linter / Formatter:** `[Detected config]`
- **Test Framework:** `[Detected test suite]`

---

## 3. Scaffolding & Artifact Audit

### 3.1 Generated Files Checklist
- [ ] `AGENTS.md` (Target AI agent operating instructions)
- [ ] `rules.md` (Project coding standards & architectural constraints)
- [ ] `DESIGN.md` (UI/UX design system tokens — omitted if backend/CLI)
- [ ] `.dev-team/config.yaml` (Dev-Team project configuration)
- [ ] `.dev-team/project-context.md` (Canonical central context store)
- [ ] `docs/project/overview.md` (Product vision, problem domain, personas)
- [ ] `docs/project/requirements.md` (System requirements baseline)
- [ ] `docs/project/system-design.md` (Architecture overview & subsystem design)
- [ ] `docs/project/plan.md` (Roadmap & milestone plan)
- [ ] `docs/project/tech-stack.md` (Technology profile & tool inventory)
- [ ] `docs/project/architecture.md` (Source layout & structural patterns)

### 3.2 Preserved Existing Files (Not Overwritten)
| Existing File Path | Action Taken | Rationale |
|---|---|---|
| `[e.g., README.md]` | PRESERVED | User documentation already exists |
| `[e.g., AGENTS.md]` | PRESERVED / MERGED | User customized operating instructions exist |

### 3.3 Skipped Files
| File | Reason for Skipping |
|---|---|
| `DESIGN.md` | Skipped: Project classified as backend service / CLI tool with no graphical UI |

---

## 4. Unresolved Items & Active Assumptions

> [!IMPORTANT]
> The following items require developer confirmation during subsequent engineering workflows:

1. **[Unresolved Item 1]:** [Description of question or assumption]
2. **[Unresolved Item 2]:** [Description of question or assumption]

---

## 5. Next Steps & Recommended Actions

1. Review and refine [`rules.md`](file:///rules.md) for any team-specific linting or naming preferences.
2. If UI is present, customize [`DESIGN.md`](file:///DESIGN.md) design tokens (colors, typography).
3. To begin developing a new capability, launch the new feature workflow:
   ```text
   /new-feature [Feature Name or Idea Description]
   ```

