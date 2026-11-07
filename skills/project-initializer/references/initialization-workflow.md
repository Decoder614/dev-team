# Reference: Phase-by-Phase Initialization Workflow & Execution Checklist

> **Project Initializer Reference Guide**  
> Operational checklist, phase transitions, error recovery strategies, and resume procedures for interrupted onboarding runs.

---

## 1. Operational Checklist

Use this checklist during execution to track progress through the 6 phases:

### [ ] Phase 1: Repository Discovery
- [ ] Run `python skills/project-initializer/scripts/check-project-structure.py --path <repo_dir> --json`.
- [ ] Inspect output JSON for manifest presence, instruction files, and directory structure.
- [ ] Verify Git status (`git status`) to ensure clean working directory.

### [ ] Phase 2: Project Classification
- [ ] Determine repository classification: `EXISTING`, `EMPTY`, or `PARTIAL`.
- [ ] Identify primary project type (`flutter_application`, `web_app`, `backend_service`, `cli_tool`, `monorepo`, `library`).

### [ ] Phase 3: Context Gathering
- [ ] If `EXISTING`: Parse manifests and source files to extract confirmed facts; note any ambiguities.
- [ ] If `EMPTY`: Conduct adaptive interview across Vision, Platforms, Stack, and Quality gates.
- [ ] If `PARTIAL`: Read existing `.dev-team/` files; identify gaps.
- [ ] Partition knowledge into `CONFIRMED_FACTS` versus `ACTIVE_ASSUMPTIONS` / `OPEN_DECISIONS`.

### [ ] Phase 4: Context Validation & Approval Gate
- [ ] Present proposed project profile, detected stack, and target files list to developer.
- [ ] Explicitly ask developer for approval to create/update files.
- [ ] Await affirmative sign-off before creating any file.

### [ ] Phase 5: Documentation & Configuration Generation
- [ ] Create `.dev-team/` directory and `.dev-team/features/`.
- [ ] Create `docs/project/` directory.
- [ ] Instantiate `templates/project/config.yaml` $\rightarrow$ `.dev-team/config.yaml`.
- [ ] Instantiate `templates/project/project-context.md` $\rightarrow$ `.dev-team/project-context.md`.
- [ ] Instantiate `templates/project/AGENTS.md` $\rightarrow$ root `AGENTS.md` (preserving existing custom rules).
- [ ] Instantiate `templates/project/rules.md` $\rightarrow$ root `rules.md`.
- [ ] Instantiate `templates/project/DESIGN.md` $\rightarrow$ root `DESIGN.md` (skip if backend/CLI).
- [ ] Instantiate baseline docs in `docs/project/` (`overview.md`, `requirements.md`, `system-design.md`, `plan.md`, `tech-stack.md`, `architecture.md`).
- [ ] Replace all placeholders with confirmed project details.

### [ ] Phase 6: Verification & Audit Reporting
- [ ] Verify YAML syntax of `.dev-team/config.yaml`.
- [ ] Run cross-document consistency check (confirm paths, names, versions align).
- [ ] Instantiate `templates/project/initialization-report.md` $\rightarrow$ `.dev-team/initialization-report.md`.
- [ ] Record audit metrics (files created, preserved, skipped, and unresolved items).
- [ ] Present completion summary and handover commands to developer.

---

## 2. Resuming Interrupted Runs

If a session disconnects or is cancelled during initialization:

1. **Check for Existing Report:**
   - Inspect `.dev-team/initialization-report.md` if present.
   - If present, check the "Generated Files Checklist" to see which files were completed.
2. **Re-run Structure Checker:**
   - Run `check-project-structure.py` to get current on-disk state.
3. **Classify as `PARTIAL`:**
   - Treat the interrupted project as `PARTIAL`.
   - Never regenerate files that already exist on disk unless the developer explicitly asks to reset them.
4. **Re-enter at Phase 4:**
   - Present the delta of missing files to the developer and request confirmation to complete onboarding.

---

## 3. Post-Initialization Handoffs

Once the repository is initialized, direct the developer to one of the standard engineering workflows:

```text
Repository Onboarding Complete!
Next Recommended Steps:
1. Review generated root instructions:
   - AGENTS.md (AI operating rules)
   - rules.md (Coding standards)
   - DESIGN.md (Design tokens)
2. Review project baseline docs in docs/project/
3. Launch your first feature:
   /new-feature [Feature Name]
```

