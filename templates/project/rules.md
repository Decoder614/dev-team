# Project Coding Rules & Standards — [Project Name]

> **Target Repository Engineering Standards**  
> Coding conventions, architectural patterns, quality standards, and development guidelines for [Project Name].

---

## 1. General Principles

1. **Simplicity Over Cleverness:** Write explicit, readable, self-documenting code. Avoid unneeded abstractions and premature optimizations.
2. **Strict Type Safety:** Use strong typing throughout; avoid raw untyped escapes (e.g., `dynamic`, `any`, `Object`) unless strictly required and justified with a code comment.
3. **Immutability by Default:** Favor immutable data models, `final`/`const` declarations, and pure functions where appropriate.
4. **Single Responsibility:** Every module, class, and function must have a single, cohesive responsibility. Keep files and functions focused.

---

## 2. Code Organization & Architecture

- **Pattern:** [e.g., Clean Architecture, Feature-First, Layered, Hexagonal]
- **Layer Responsibilities:**
  - `presentation/`: UI components, screens, controllers/blocs/viewmodels. No direct database or raw network calls.
  - `domain/`: Business entities, use cases, and repository interfaces. Pure business logic independent of external frameworks.
  - `data/`: Repository implementations, API clients, local database/caching, data mappers, and DTOs.
- **Dependency Rule:** Dependencies must flow inward toward the domain layer. Higher layers depend on abstractions, not concrete implementations.
- **Dependency Injection:** [e.g., GetIt, Riverpod, InversifyJS, Spring, etc.] Register services in central composition roots; avoid ad-hoc global service instantiation.

---

## 3. Language & Framework Conventions

### 3.1 Naming Conventions
- **Files & Folders:** [e.g., `snake_case.dart` / `kebab-case.ts` / `camelCase.ts`]
- **Classes & Types:** `PascalCase`
- **Functions & Methods:** `camelCase`
- **Variables & Fields:** `camelCase`
- **Constants:** `SCREAMING_SNAKE_CASE` or `lowerCamelCase` (per language convention)
- **Interfaces / Abstractions:** [e.g., `UserRepository` or `IUserRepository`]

### 3.2 Formatting & Linting
- **Indentation:** [e.g., 2 spaces / 4 spaces]
- **Max Line Length:** [e.g., 80 / 100 / 120 characters]
- **Linter Rule Set:** Adhere strictly to the project linter configuration without adding disabling comments unless authorized.

---

## 4. Error Handling & Logging

1. **Explicit Error Types:** Define domain-specific exceptions and failure types rather than catching or throwing generic errors.
2. **No Silent Failures:** Never swallow exceptions with empty `catch` blocks. Either handle gracefully, transform, or rethrow with contextual information.
3. **Structured Logging:** Use the project logging utility (avoid raw `print` or `console.log` in production code). Include context and error objects.
4. **Safe Fallbacks:** Ensure UI states handle errors and empty states gracefully, showing meaningful feedback to users.

---

## 5. Testing Requirements

- **Unit Tests:** Mandatory for all domain use cases, data mappers, business logic, and utility functions.
- **Widget / Component Tests:** Verify UI behavior, user interactions, and visual states (loading, success, error, empty).
- **Integration Tests:** Cover critical user journeys and core API workflows.
- **Mocking:** Mock external services, network clients, and storage layers using approved mocking libraries (e.g., `mocktail`, `jest.mock`, `unittest.mock`).
- **Assertion Quality:** Test expected behavior, boundary values, and failure paths—not implementation details.

---

## 6. Git Hygiene & Commit Conventions

- **Branch Naming:** `feature/<feature-name>`, `bugfix/<bug-name>`, `chore/<chore-name>`
- **Commit Messages:** Follow Conventional Commits:
  - `feat: add user authentication flow`
  - `fix: resolve token refresh race condition`
  - `test: add unit tests for user profile repository`
  - `docs: update system design with cache strategy`
- **Atomic Commits:** Keep commits scoped to a single logical change. Do not bundle formatting, refactoring, and feature work into one commit.
- **Clean Working Tree:** Never commit generated build artifacts, temporary debug files, or `.env` files with credentials.

