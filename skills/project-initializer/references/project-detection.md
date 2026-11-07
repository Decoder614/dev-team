# Reference: Multi-Stack Project Detection & Manifest Heuristics

> **Project Initializer Reference Guide**  
> Heuristics, manifest parsing patterns, dependency inspection rules, and architectural cues across major programming ecosystems.

---

## 1. Supported Ecosystems & Manifest Detection Matrix

| Ecosystem | Manifest File(s) | Lockfile(s) | Typical Source Dirs | Default Test Tool |
|---|---|---|---|---|
| **Flutter / Dart** | `pubspec.yaml` | `pubspec.lock` | `lib/`, `bin/` | `flutter test` |
| **Node.js / TypeScript** | `package.json`, `tsconfig.json` | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` | `src/`, `lib/`, `app/` | `npm test` / `jest` / `vitest` |
| **Python** | `pyproject.toml`, `requirements.txt`, `Pipfile` | `poetry.lock`, `Pipfile.lock` | `src/`, `<pkg_name>/` | `pytest` |
| **Rust** | `Cargo.toml` | `Cargo.lock` | `src/`, `crates/` | `cargo test` |
| **Go** | `go.mod` | `go.sum` | `cmd/`, `internal/`, `pkg/` | `go test ./...` |
| **Java / Kotlin** | `build.gradle`, `build.gradle.kts`, `pom.xml` | `gradle.lockfile` | `src/main/java`, `src/main/kotlin` | `./gradlew test` / `mvn test` |
| **.NET / C#** | `*.csproj`, `*.sln` | `packages.lock.json` | `src/`, `<ProjectName>/` | `dotnet test` |

---

## 2. Ecosystem Detection Rules

### 2.1 Flutter / Dart (`pubspec.yaml`)
1. **Framework Type:**
   - If `flutter:` section exists under `dependencies:`, classify as `flutter_application` or `flutter_package`.
   - If only `environment: sdk: >=...` without `flutter:`, classify as `dart_package` or `dart_cli`.
2. **State Management Detection:**
   - `flutter_bloc` / `bloc` $\rightarrow$ BLoC pattern
   - `flutter_riverpod` / `riverpod` $\rightarrow$ Riverpod pattern
   - `provider` $\rightarrow$ Provider pattern
   - `mobx` / `flutter_mobx` $\rightarrow$ MobX
   - `signals` $\rightarrow$ Signals
3. **Routing Detection:**
   - `go_router` $\rightarrow$ GoRouter declarative routing
   - `auto_route` $\rightarrow$ AutoRoute code-generated routing
   - `beamer` $\rightarrow$ Beamer
4. **Dependency Injection:**
   - `get_it` / `injectable` $\rightarrow$ Service Locator / DI
5. **Persistence / Local Database:**
   - `drift` $\rightarrow$ Drift SQLite ORM
   - `hive` / `hive_flutter` $\rightarrow$ Hive NoSQL
   - `isar` $\rightarrow$ Isar NoSQL
   - `shared_preferences` $\rightarrow$ Key-Value store
6. **Backend Integrations:**
   - `supabase_flutter` $\rightarrow$ Supabase
   - `firebase_core` $\rightarrow$ Firebase

### 2.2 Node.js & TypeScript (`package.json`)
1. **Framework Type:**
   - `next` $\rightarrow$ Next.js full-stack / web app
   - `react` / `react-dom` $\rightarrow$ React SPA
   - `vue` / `nuxt` $\rightarrow$ Vue / Nuxt app
   - `express` / `fastify` / `nest` $\rightarrow$ Node.js backend service
   - `@angular/core` $\rightarrow$ Angular application
2. **Language & Tooling:**
   - Presence of `typescript` or `tsconfig.json` $\rightarrow$ TypeScript
   - `scripts.lint` $\rightarrow$ ESLint / Biome
   - `scripts.test` $\rightarrow$ Jest / Vitest / Mocha
3. **State Management:**
   - `@reduxjs/toolkit` $\rightarrow$ Redux Toolkit
   - `zustand` $\rightarrow$ Zustand
   - `pinia` $\rightarrow$ Pinia (Vue)

### 2.3 Python (`pyproject.toml`, `requirements.txt`)
1. **Framework Type:**
   - `fastapi` $\rightarrow$ FastAPI backend service
   - `django` $\rightarrow$ Django full-stack web framework
   - `flask` $\rightarrow$ Flask microframework
2. **Packaging Tool:**
   - `[tool.poetry]` in `pyproject.toml` $\rightarrow$ Poetry
   - `[tool.flit]` $\rightarrow$ Flit
   - `[project]` (PEP 621) with `hatchling` or `setuptools`
3. **Linter & Type Checker:**
   - `ruff` in configuration $\rightarrow$ Ruff linter/formatter
   - `mypy` $\rightarrow$ Mypy static type analysis

### 2.4 Rust (`Cargo.toml`)
1. **Project Type:**
   - `[[bin]]` or `src/main.rs` $\rightarrow$ Rust binary / CLI tool
   - `[lib]` or `src/lib.rs` $\rightarrow$ Rust library
   - `[workspace]` $\rightarrow$ Rust monorepo
2. **Frameworks:**
   - `actix-web` / `axum` / `rocket` $\rightarrow$ Web service
   - `tokio` $\rightarrow$ Asynchronous runtime

### 2.5 Go (`go.mod`)
1. **Frameworks:**
   - `github.com/gin-gonic/gin` $\rightarrow$ Gin web service
   - `github.com/gofiber/fiber` $\rightarrow$ Fiber web service
   - `github.com/spf13/cobra` $\rightarrow$ Cobra CLI tool

### 2.6 Java / Kotlin (`build.gradle`, `pom.xml`)
1. **Frameworks:**
   - `org.springframework.boot` $\rightarrow$ Spring Boot service
   - `io.micronaut` $\rightarrow$ Micronaut service
   - `com.android.application` $\rightarrow$ Android native application

---

## 3. Directory Layout Pattern Recognition

| Pattern | Identifying Characteristics | Architecture Inferred |
|---|---|---|
| **Clean Architecture** | `domain/`, `data/`, `presentation/` or `core/` folders | Clean Architecture |
| **Feature-First** | `features/<name>/` containing local UI/data/domain | Feature-Sliced Design |
| **Layer-First** | Global `models/`, `views/`, `controllers/` | MVC / Layered |
| **Hexagonal (Ports & Adapters)** | `ports/`, `adapters/`, `domain/` | Hexagonal Architecture |
| **Monorepo** | `packages/`, `apps/`, `libs/`, `pnpm-workspace.yaml` | Monorepo |

---

## 4. Extraction Safeguards

1. **Manifest Priority:** If a lockfile exists alongside a manifest, read the lockfile for exact resolved versions, but read the manifest for declared intentions.
2. **Multi-Manifest Repositories:** When multiple manifests exist (e.g., both frontend and backend in one repository), classify the project as `monorepo` or `multi_service` and record sub-stacks under discrete service sections in `.dev-team/project-context.md`.
3. **No Guessing:** If a library is present in dependencies but not actively configured (e.g., both `provider` and `flutter_bloc` in `pubspec.yaml`), inspect `lib/` imports to determine which is primary, or prompt the developer for clarification.

