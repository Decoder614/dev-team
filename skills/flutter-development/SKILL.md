---
name: flutter-development
description: >-
  Reusable engineering skill for implementing approved tasks and bug fixes in Flutter and Dart
  codebases. Provides framework-agnostic architectural alignment, project inspection, Dart idiomatic
  practices, widget composition, state management adaptation (BLoC, Riverpod, Provider, etc.),
  navigation, dependency injection, data-layer patterns, error handling, testing, and deterministic
  static analysis. Emphasizes smallest useful changes, zero unsolicited refactoring, and strict
  adherence to target project conventions.
---

# Flutter Development Skill

## 1. Overview & Purpose

The **Flutter Development Skill** provides standardized procedural guidance for implementing approved tasks, tests, and bug fixes in Flutter/Dart repositories.

It enforces controlled, incremental engineering:
- Implementing one task at a time (`REQ-031`).
- Inspecting existing codebase patterns before modifying files (`REQ-032`).
- Adapting strictly to target project conventions rather than imposing dogmatic third-party libraries (`REQ-033`).
- Avoiding unsolicited refactoring and unnecessary dependencies (`REQ-034`).
- Executing deterministic verification commands and capturing evidence before marking tasks complete (`SAFE-009`, `REQ-036`, `REQ-037`).

---

## 2. When to Use

Activate this skill when:
- Executing the `implement_next` workflow (`workflows/implement-next.md`) on a Flutter codebase.
- Implementing an approved task card (`templates/task.md`) or milestone task from `plan.md`.
- Diagnosing or fixing defects in a Flutter project via the `fix_bug` workflow.
- Reviewing or updating Flutter unit tests, widget tests, or integration tests.

---

## 3. Precedence & Technology Agnosticism

### 3.1 Precedence Hierarchy
1. **Target Repository Instructions (`AGENTS.md`):** Highest authority. Project-specific rules override any generic skill recommendation (`SAFE-011`).
2. **Target Project Profile (`.dev-team/project-profile.yaml`):** Concrete commands, directory layouts, and established architectural choices.
3. **Existing Codebase Conventions:** Observed patterns in existing files (naming, formatting, folder layout, state management).
4. **This Skill (`SKILL.md`):** Reusable best practices and baseline procedural discipline.

### 3.2 Framework & Library Agnosticism
Dev-Team does **not** mandate or assume any single library stack:
- **State Management:** Adapt to whatever the project uses—BLoC/Cubit, Riverpod, Provider, Signals, MobX, or vanilla `ValueNotifier`/`StatefulWidget`. Never introduce a conflicting state library into a project.
- **Backend / Data:** Adapt to the target backend—Supabase, Firebase, REST/Dio, GraphQL, or local SQLite/Drift/Hive.
- **Routing:** Adapt to `go_router`, `auto_route`, `beamer`, or Navigator 2.0 / 1.0.
- **Dependency Injection:** Adapt to `get_it`, `injectable`, Riverpod providers, or InheritedWidgets.

---

## 4. Flutter Project Inspection

Before modifying or creating any code, perform targeted discovery (`REQ-013`, `REQ-032`):

### 4.1 Dependency & Toolchain Inspection
Read `pubspec.yaml` to identify:
- Flutter and Dart SDK version constraints (e.g., Dart 3.x with sound null safety and pattern matching).
- Active state management libraries (`flutter_bloc`, `flutter_riverpod`, `provider`, etc.).
- Network and API libraries (`http`, `dio`, `supabase_flutter`, `firebase_core`).
- Code generation tools (`build_runner`, `freezed`, `json_serializable`, `injectable_generator`).
- Testing dependencies (`mocktail`, `mockito`, `bloc_test`, `flutter_test`).

### 4.2 Linter & Style Inspection
Read `analysis_options.yaml` to identify:
- Extended rule sets (`flutter_lints`, `very_good_analysis`, or custom package rules).
- Required linter options (e.g., `prefer_const_constructors`, `avoid_print`, `unawaited_futures`).
- Strict type checking rules (`strict-casts`, `strict-inference`, `strict-raw-types`).

### 4.3 Directory Architecture Discovery
Inspect the directory structure to determine the architectural style:
- **Feature-First (Clean Architecture):** `lib/features/<feature_name>/{data, domain, presentation}/`
- **Layer-First:** `lib/{models, services, controllers/blocs, views/screens, widgets}/`
- **Shared / Core Utilities:** `lib/core/{constants, theme, utils, network, errors}/`

---

## 5. Dart Coding Practices

Follow standard Effective Dart idioms and project-specific guidelines:

### 5.1 Sound Null Safety & Types
- Avoid unconditional force-unwrap (`!`) operators. Use null-aware operators (`?.`, `??`), null assertion guard clauses, or type promotion.
- Prefer explicit types over `var` for public APIs, function signatures, and class members.
- Use `final` by default for all local variables, parameters, and immutable fields.
- Leverage Dart 3 pattern matching and records for multi-return values or state destructuring:
  ```dart
  // Example pattern matching
  return switch (state) {
    ReviewLoading() => const Center(child: CircularProgressIndicator()),
    ReviewSuccess(:final reviews) => ReviewListView(reviews: reviews),
    ReviewError(:final message) => ErrorDisplay(message: message),
  };
  ```

### 5.2 Constructors & Immutability
- Add `const` constructors to immutable classes, data models, and widgets.
- Mark immutable classes with `@immutable` (from `package:meta/meta.dart`).
- Use named parameters with `required` for constructors having more than two fields.

### 5.3 Asynchronous Programming
- Always `await` asynchronous calls unless deliberately detached, in which case use `unawaited(...)` with proper documentation.
- Never let unhandled asynchronous errors escape uncaptured; wrap external calls in `try/catch` or use `Result`/`Either` monads matching project patterns.
- Always cancel stream subscriptions, timers, and controllers in `dispose()` to prevent memory leaks.

---

## 6. Widget Composition & UI Patterns

### 6.1 Small, Focused Widgets
- Break down monolithic build methods into separate, focused `StatelessWidget` classes rather than helper methods returning widgets (helper methods hinder Flutter element tree sub-tree caching and rebuild optimizations).
- Keep widget build methods pure and free of side effects (no network calls, timers, or state dispatching inside `build()`).

### 6.2 Standard Screen State Representation
Every UI screen or complex component should cleanly represent all four essential lifecycle states:
1. **Initial / Empty:** Clean empty state illustration or guidance when no data exists.
2. **Loading:** Non-blocking skeleton loaders, shimmers, or `CircularProgressIndicator`.
3. **Success / Content:** Render the active view with cached or loaded data.
4. **Error:** User-friendly message explaining the issue, paired with a retry action button.

### 6.3 Theme & Design System Conformance
- Avoid hardcoding arbitrary hex colors or pixel dimensions.
- Use the target application's design system tokens: `Theme.of(context).colorScheme`, `Theme.of(context).textTheme`, and designated spacing/padding constants.
- Respect device boundaries using `SafeArea`, responsive constraints, and scrollable wrappers for keyboard avoidance.

---

## 7. State Management Patterns (Adaptive)

Adapt to the project's established pattern. Do not mix paradigms.

### 7.1 BLoC / Cubit (`flutter_bloc`)
- Follow the unidirectional data flow: `Event -> Bloc -> State` or `Method -> Cubit -> State`.
- Define explicit, immutable states extending an abstract base class or using `freezed`.
- Use `BlocProvider` at the appropriate sub-tree level; close/dispose bloc automatically or manually.
- Use `BlocBuilder` for rebuilding widgets, `BlocListener` for one-time side-effects (navigation, snackbars), and `BlocConsumer` when both are needed.

### 7.2 Riverpod (`flutter_riverpod`)
- Use `Notifier` / `AsyncNotifier` (Riverpod 2+) or `StateNotifier` as used by the project.
- Expose typed states with `AsyncValue<T>` to handle loading, data, and error natively.
- Use `ConsumerWidget` or `ConsumerStatefulWidget`; prefer `ref.watch` in `build()` and `ref.read` in event callbacks.

### 7.3 Provider (`provider`)
- Extend `ChangeNotifier` for reactive state holders.
- Keep `notifyListeners()` calls minimal and focused.
- Consume state using `context.select` for granular rebuilds or `Consumer<T>`.

### 7.4 ValueNotifier / StatefulWidget
- For localized widget state without third-party libraries, use `ValueNotifier<T>` or private `State<MyWidget>`.
- Always dispose controllers (`TextEditingController`, `AnimationController`, `ScrollController`) in `dispose()`.

---

## 8. Routing & Navigation Patterns

- **Declarative Routers (e.g., `go_router`):**
  - Register new routes in the central router configuration file.
  - Pass parameters via path parameters, query parameters, or typed `$extra`.
  - Maintain authentication redirect guards and deep link URL consistency.
- **Named / Imperative Routes (`Navigator`):**
  - Define static route constants (e.g., `static const routeName = '/property-reviews'`).
  - Follow the existing parameter passing convention (modal arguments or constructor injection).

---

## 9. Dependency Injection & Service Locator

- **GetIt / Injectable:**
  - Register services, repositories, and blocs in the service locator registry (e.g., `injection.dart` or `locator.dart`).
  - Distinguish `registerLazySingleton` (state-less services, repositories) from `registerFactory` (transient blocs or stateful handlers).
  - Run `dart run build_runner build` if the project uses `@injectable` annotations.
- **Provider / InheritedWidget DI:**
  - Register dependencies in the top-level or feature-level widget tree using `Provider<Service>.value`.

---

## 10. Repository & Data-Layer Patterns

### 10.1 Layer Separation
- **Data Source Layer:** Communicates with remote APIs (HTTP, Supabase, Firebase) or local storage (Hive, SQLite, SharedPreferences). Handles serialization/deserialization and raw exceptions.
- **Repository Layer:** Abstract interface in the domain layer; concrete implementation in the data layer. Translates raw API models/exceptions into clean domain entities and typed failures.
- **Domain Layer:** Pure business logic, entity models, and use cases (free of Flutter widget dependencies).

### 10.2 JSON Serialization
- Maintain consistency with existing serialization approaches:
  - If using manual parsing: Implement `factory MyModel.fromJson(Map<String, dynamic> json)` and `Map<String, dynamic> toJson()`.
  - If using `freezed` or `json_serializable`: Add `@JsonSerializable()`, run `build_runner`, and commit/validate generated `.g.dart` or `.freezed.dart` files.

---

## 11. Error Handling & Safety Boundaries

### 11.1 Failure Modeling
- Use typed failure classes (e.g., `ServerFailure`, `NetworkFailure`, `ValidationFailure`, `AuthFailure`).
- Avoid throwing unhandled raw exceptions into the presentation layer. Return failure objects or emit error states.

### 11.2 Safety Rules (SAFE-005, SAFE-007)
- **Secrets:** NEVER hardcode API keys, service role keys, authorization bearer tokens, or user passwords in Dart code (`SAFE-005`). Use environment configuration (`--dart-define`, `.env` files loaded safely).
- **Destructive Data Operations:** Never write automatic data wipes, table dropping routines, or destructive sync routines without explicit approval (`SAFE-006`, `SAFE-007`).

---

## 12. Testing Practices

Every task modifying or introducing logic must include corresponding automated tests (`REQ-025`, `REQ-036`).

### 12.1 Unit Testing
- Test domain use cases, data repositories, and state controllers in isolation.
- Use mocks (`mocktail` or `mockito`) to stub external dependencies:
  ```dart
  test('returns Review list when repository succeeds', () async {
    when(() => mockRepo.getReviews(propertyId: '123'))
        .thenAnswer((_) async => [mockReview]);

    final result = await getReviewsUseCase('123');

    expect(result, equals([mockReview]));
    verify(() => mockRepo.getReviews(propertyId: '123')).called(1);
  });
  ```

### 12.2 Widget Testing
- Test UI rendering, state transitions, user interactions, and error states.
- Wrap test widgets with necessary test harnesses (`MaterialApp`, theme, mock providers/blocs).
- Verify widget presence using finders (`find.byType`, `find.text`, `find.byKey`).

### 12.3 Test Execution Command
Run targeted tests for the modified feature rather than full repository test suites when working on a single task:
```bash
flutter test test/features/<feature_name>/path/to/test.dart
```

---

## 13. Deterministic Static Analysis & Formatting

Before considering any task implementation complete:

1. **Format Code:**
   ```bash
   dart format lib/features/<feature_name>/ test/features/<feature_name>/
   ```
2. **Run Linter / Static Analysis:**
   ```bash
   flutter analyze lib/features/<feature_name>/
   ```
   *Expected Output:* Zero issues found (`No issues found!`).
3. **Run Code Generation (if applicable):**
   ```bash
   dart run build_runner build --delete-conflicting-outputs
   ```
4. **Run Targeted Tests:**
   ```bash
   flutter test test/features/<feature_name>/
   ```
   *Expected Output:* All tests pass with exit code 0.

---

## 14. Developer Discipline Checklist

Before closing an implementation task, verify each item:

- [ ] **Single Task Scope:** Only the files specified in the approved task were modified (`REQ-031`, `REQ-035`).
- [ ] **No Unsolicited Refactoring:** Existing working code outside the task scope was left untouched (`REQ-034`).
- [ ] **Convention Conformance:** Coding style matches existing codebase conventions (`REQ-033`).
- [ ] **Deterministic Checks Executed:** Linter and tests were run and output was observed directly (`SAFE-009`, `REQ-036`).
- [ ] **Task Status Updated:** Status and evidence recorded in the task specification (`REQ-037`).
- [ ] **Clean Report:** Summary of modified files and decisions ready for developer report (`REQ-038`).
- [ ] **Halt After One Task:** Execution concludes after completing the approved task without spilling into downstream tasks (`REQ-039`).
