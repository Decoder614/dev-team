# Reference: Project Documentation Mapping & Scaffolding Rules

> **Project Initializer Reference Guide**  
> Rules governing which files, templates, and configurations are generated, customized, or skipped based on target project classification.

---

## 1. Documentation Scaffolding Matrix

| Artifact Path | Flutter / Mobile | Web App (SPA/SSR) | Backend Service / API | CLI Tool | Library / SDK | Monorepo |
|---|---|---|---|---|---|---|
| `AGENTS.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `rules.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `DESIGN.md` | Mandatory | Mandatory | **Skipped** | **Skipped** | **Skipped** | Optional |
| `.dev-team/config.yaml` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `.dev-team/project-context.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `.dev-team/initialization-report.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `docs/project/overview.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `docs/project/requirements.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `docs/project/system-design.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `docs/project/plan.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `docs/project/tech-stack.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |
| `docs/project/architecture.md` | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory | Mandatory |

---

## 2. Special Generation Rules by Project Type

### 2.1 Backend Services & CLI Tools (No UI)
- **Skip `DESIGN.md`:** Do not generate `DESIGN.md`. Record the reason in `initialization-report.md`:
  > *"Skipped DESIGN.md: Target project is a backend service / CLI tool with no visual interface."*
- **Omit UI Sections in `tech-stack.md`:** Remove or mark "N/A" for UI components, state management for widgets, and client styling libraries.
- **Adjust `rules.md`:** Focus on API contracts, database migration hygiene, request validation, and error serialization instead of widget life-cycles.

### 2.2 Libraries & Reusable Packages
- **API Surface Documentation:** In `docs/project/architecture.md`, prioritize public API boundaries, export declarations, semver compliance, and minimal dependency footprints.
- **Documentation Tests:** In `tech-stack.md`, include doc-test runners or example suites.

### 2.3 Monorepos & Multi-Package Repositories
- **Root Instructions:** `AGENTS.md` acts as the umbrella orchestrator.
- **Sub-Package Context:** In `.dev-team/project-context.md`, detail the directory hierarchy (e.g. `apps/` vs `packages/`) and specify which packages have graphical UI versus shared logic.

---

## 3. Template Instantiation & Token Replacement

When instantiating templates from `templates/project/`:

1. Replace `[Project Name]` with the actual application name.
2. Replace `[YYYY-MM-DD]` with current local date.
3. Replace language and framework placeholders (`[Language]`, `[Framework]`) with detected or confirmed values.
4. Replace command placeholders with actual commands (e.g. replacing `[e.g., flutter test]` with `flutter test`).
5. **Never leave unparsed template syntax in confirmed sections:** If a value is unknown, explicitly state `Not configured yet` or `Pending architectural decision`.

---

## 4. Preservation & Non-Destructive Scaffolding Policy

When a target repository already contains files:

1. **Existing `README.md`:** Never overwrite or replace. Dev-Team uses `docs/project/overview.md` for project vision so developer READMEs remain undisturbed.
2. **Existing `AGENTS.md`:** If an `AGENTS.md` exists, inspect it:
   - If it contains Dev-Team markers, merge or refresh sections.
   - If it contains custom developer instructions, preserve developer rules at the top, and append Dev-Team operational boundaries without overwriting.
3. **Existing `docs/`:** If existing project documentation exists under other names (e.g. `docs/spec.md`), link to it from `project-context.md` instead of duplicating or overwriting.
4. **Git Safety Check:** Ensure working tree is clean or developer has acknowledged modified files before committing or creating files.

