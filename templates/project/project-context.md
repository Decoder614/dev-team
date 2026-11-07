# Central Project Context Store — [Project Name]

> **Canonical Central Source of Truth**  
> Persistent repository context, confirmed technical facts, active assumptions, established conventions, and module catalog for [Project Name].  
> *Consumed and maintained by all Dev-Team skills across engineering workflows.*

---

## Document Metadata

- **Status:** APPROVED <!-- DRAFT, IN_REVIEW, APPROVED -->
- **Version:** 1.0.0
- **Last Initialized / Synchronized:** [YYYY-MM-DD HH:MM]
- **Target Repository:** `[Repository Name]`
- **Project Type:** `[flutter_application | web_app | backend_service | cli_tool | monorepo | library]`

---

## 1. Project Purpose & High-Level Summary

- **Product Name:** [Product Name]
- **Core Mission:** [1-2 sentences summarizing user value and core capabilities]
- **Target Audience:** [Primary user persona or consumer]
- **Target Platforms:** [e.g., iOS, Android, Web, Linux, macOS, Windows]

---

## 2. Confirmed Technical Facts (`CONFIRMED_FACTS`)

> [!NOTE]
> Items in this section represent verified code realities extracted deterministically from repository manifests, source inspection, or explicit developer sign-off.

### 2.1 Language & Core Framework
- **Primary Language:** `[e.g., Dart 3.x / TypeScript 5.x / Python 3.11]`
- **Primary Framework:** `[e.g., Flutter 3.24 / Next.js 14 / FastAPI]`
- **Package Manifest:** `[e.g., pubspec.yaml / package.json / pyproject.toml]`
- **Package Manager:** `[e.g., pub / pnpm / poetry]`

### 2.2 Architectural & State Primitives
- **Architectural Style:** `[e.g., Clean Architecture with feature slicing]`
- **State Management:** `[e.g., flutter_bloc / Riverpod / Redux / None]`
- **Routing & Navigation:** `[e.g., GoRouter / React Router / File-based]`
- **Dependency Injection / Service Locator:** `[e.g., GetIt / Inversify / Custom]`
- **Local Persistence:** `[e.g., Drift (SQLite) / Hive / Room / None]`
- **Remote API Client:** `[e.g., Dio / Axios / Fetch]`

### 2.3 Verification & Tooling Commands
- **Lint / Static Analysis:** `[e.g., flutter analyze / npm run lint]`
- **Unit & Component Testing:** `[e.g., flutter test / npm test]`
- **Build / Packaging:** `[e.g., flutter build apk --debug / npm run build]`

---

## 3. Active Assumptions & Open Decisions (`ACTIVE_ASSUMPTIONS`)

> [!WARNING]
> Items in this section are working hypotheses or pending architectural decisions. They MUST NOT be treated as confirmed facts until validated by the developer or proven by source code.

| ID | Category | Assumption / Open Decision | Impact / Dependent Areas | Resolution Status |
|---|---|---|---|---|
| `ASM-001` | [e.g., Backend Auth] | [e.g., Assume Supabase Auth will be used for OAuth2 login] | [Authentication flow, user model] | PENDING_VALIDATION |
| `ASM-002` | [e.g., Offline Sync] | [e.g., Assume optimistic UI updates with offline queue] | [Repository layer, sync service] | OPEN_DECISION |

---

## 4. Source Layout & Module Catalog

```text
[src/ or lib/]
├── core/                 # Shared utilities, failure types, network interceptors
├── features/             # Feature slices
│   └── [feature_a]/      # Encapsulated presentation, domain, data
└── main.[ext]            # Bootstrap and root entry point
```

| Module / Feature | Location | Responsibility & Scope | Key Dependencies |
|---|---|---|---|
| `core` | `lib/core/` | Cross-cutting error definitions, theme, HTTP clients | External SDKs |
| `[feature_a]` | `lib/features/[feature_a]/` | [Feature description] | `core` |

---

## 5. Established Conventions & Guidelines

1. **Coding Standards:** Enforced per [`rules.md`](file:///rules.md).
2. **Visual & UI Tokens:** Enforced per [`DESIGN.md`](file:///DESIGN.md) (if applicable).
3. **Safety & Approval Gates:** Enforced per [`AGENTS.md`](file:///AGENTS.md).
4. **Context Update Rule:** When a new module, dependency, or architectural pattern is approved during feature development, it must be recorded under Section 2 (`CONFIRMED_FACTS`).

