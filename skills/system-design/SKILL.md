---
name: system-design
description: >-
  Reusable procedural skill for designing technical architecture, component layers, data models,
  state management, API contracts, security mechanisms, and data flows for new features (system-design.md).
  Aligns feature architecture with existing project patterns discovered via project-discovery, maps designs
  to approved requirements, and identifies consequential decisions requiring developer sign-off.
  Activate when designing a feature, producing architecture specifications, or executing the design-feature workflow.
---

# System Design Skill

## 1. Overview & Purpose

This skill defines the standardized procedure for converting an approved feature requirement (`requirement.md`) into a clear, cohesive, and maintainable technical architecture specification (`system-design.md`).

The goal is to design the smallest, simplest technical solution that completely satisfies the requirements while adhering to the target project's actual technology choices, layer conventions, state management, and design patterns.

---

## 2. When to Use

Activate this skill when:
- An approved `requirement.md` exists and technical design is ready to begin.
- The `design-feature` workflow (`workflows/design-feature.md`) is executed.
- The developer asks to architect, design, or plan the technical structure of a feature (e.g., *"design the database and state model for this feature"* or *"how should we architect this feature in our Flutter app?"*).
- An existing feature architecture needs modification, restructuring, or migration.

---

## 3. Required Inputs

1. **Approved Requirement Document:** Path to approved `requirement.md` (e.g., `.dev-team/features/<feature-name>/requirement.md`).
2. **Project Profile & Context:**
   - `.dev-team/project-profile.yaml` (generated/updated via `project-discovery`).
   - Target project `AGENTS.md` for local conventions.
   - Representative codebase files illustrating existing patterns (e.g., existing models, repositories, blocs/notifiers, routes).

---

## 4. Execution Procedure

Follow these eleven sequential steps to produce a structured system design document:

### Step 1: Ingest Approved Requirements & Verify Status
1. Locate and read the target `requirement.md`.
2. Verify that document status is `APPROVED` (per `SAFE-001` and `REQ-GATE-4`).
   - If status is `DRAFT` or `IN_REVIEW`, pause and inform the developer that requirements must be approved first.
3. Extract all functional requirement IDs (`REQ-001`, `REQ-002`, ...) and non-functional requirements (`NFR-001`, ...).

### Step 2: Proportionality Assessment (Avoid Over-Engineering)
1. Evaluate feature complexity:
   - **Small Feature:** (e.g., a simple UI toggle, cosmetic enhancement, or minor validation rule). Produce a concise, streamlined design highlighting only modified components, state, and test strategy. Omit unnecessary sections (REQ-021).
   - **Medium/Large Feature:** (e.g., multi-screen workflow, new data entity, backend integration, offline cache). Produce full architectural documentation covering all relevant layers.
2. Principle: Apply the **smallest useful solution first**. Do not introduce speculative abstractions, complex design patterns, or extra layers that the existing repository does not use.

### Step 3: Run Project Discovery & Align with Existing Patterns
1. If `.dev-team/project-profile.yaml` is missing or out-of-date, invoke `skills/project-discovery/SKILL.md`.
2. Align feature design with discovered patterns:
   - Match existing directory structure (e.g., `features/<name>/` vs `lib/domain/`, `lib/presentation/`).
   - Match existing state management (BLoC, Riverpod, Provider, etc.).
   - Match existing dependency injection mechanism (GetIt, Provider, constructor injection).
   - Match existing navigation approach (GoRouter, AutoRoute, Navigator).
3. Never force an unapproved framework or architecture pattern onto the repository (REQ-014, REQ-065).

### Step 4: Layer Decomposition & Component Responsibilities
Decompose the feature into clear architectural layers aligned with the project's architecture:
1. **Presentation Layer:**
   - Screens / Views / Pages.
   - Widgets / UI components (reusing shared design system widgets).
   - ViewModels / Controllers / Blocs / Notifiers managing view state.
2. **Domain / Application Layer (if used in project):**
   - Business entities and value objects.
   - Use cases / Interactors / Domain services.
   - Failure and exception representations.
3. **Data / Infrastructure Layer:**
   - Repository interfaces and implementations.
   - Data sources (remote API clients, local databases, key-value stores).
   - Data Transfer Objects (DTOs), serialization, and deserialization models.
4. Establish bidirectional traceability: Ensure every component traces back to specific `REQ-xxx` IDs.

### Step 5: Data Flow & Reactive State Management
1. Map the operational data flow from user interaction to backend and back:
   - User action on Widget → State event / method call.
   - Controller / Bloc invokes Repository or Use Case.
   - Data source executes network or local query.
   - Result mapped to Domain Entity / View State.
   - UI reacts to state change (loading → success / error / empty).
2. Document state models:
   - Initial state, loading state, loaded state, error state.
   - Immutable state models vs reactive streams.

### Step 6: Data Modeling, Database & Persistence Design
*Only applicable if feature requires data storage or backend changes (REQ-018).*
1. **Schema Design:**
   - Define table names, columns, primary keys, foreign keys, nullability, and default values.
   - Specify indexes for frequent queries or foreign key lookups.
2. **Migrations:**
   - Outline deterministic migration steps (up / down).
   - Specify migration file paths conforming to project convention (e.g., `supabase/migrations/<timestamp>_<name>.sql`).
3. **Security & Access Control:**
   - Specify Row-Level Security (RLS) policies or access rules (e.g., users can only read/write their own records).
   - Ensure foreign key constraints enforce referential integrity and cascading deletes where appropriate.

### Step 7: API Contracts & Integration Specifications
*Only applicable if feature communicates over network or with third-party APIs.*
1. Specify endpoint details:
   - Method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
   - URL path and query parameters.
   - Request payload schema (JSON).
   - Response payload schema (JSON) for 200/201, 400, 401, 403, 404, 500.
2. Specify error handling and network resilience:
   - Timeout thresholds.
   - Retry policy with exponential backoff (if idempotent).
   - Offline fallback or optimistic UI updates.

### Step 8: UI/UX & Navigation Architecture
*Only applicable for user-facing features (REQ-019).*
1. **Navigation & Routes:**
   - Route path (e.g., `/properties/:id/reviews`).
   - Navigation arguments and query parameters.
   - Deep-linking support and route guards (authentication checks).
2. **UI Hierarchy & Screen States:**
   - Component hierarchy (Parent Screen → Child Widgets).
   - Screen states: Initial, Loading (shimmer/spinner), Content, Empty (illustration/message), Error (retry prompt).
   - Shared design system token usage (colors, typography, spacing).

### Step 9: Security, Privacy & Data Protection
1. **Authentication & Authorization:**
   - Verify user identity and role permissions before executing sensitive actions.
2. **Data Sanitization & Validation:**
   - Input validation rules (boundary limits, character sets, injection prevention).
   - Output encoding.
3. **Sensitive Data Handling:**
   - Avoid storing unencrypted secrets or credentials.
   - Mark fields containing Personally Identifiable Information (PII) and define handling policy.

### Step 10: Architectural Decision Records (ADRs)
For each non-trivial technical choice:
1. Document an ADR using the standard pattern:
   - **ID & Title:** e.g., `ADR-001: Use Riverpod StateNotifier for Review Form State`.
   - **Status:** Proposed / Accepted / Rejected.
   - **Context:** Problem statement and constraints.
   - **Options Considered:** Option A vs Option B vs Option C.
   - **Decision:** Selected option.
   - **Rationale:** Why this option was chosen over alternatives.
   - **Consequences & Trade-offs:** Pros, cons, and residual risks.

### Step 11: Flag Significant Decisions for Developer Approval
1. Identify all consequential decisions:
   - New external dependencies or libraries.
   - Database schema changes or new migrations.
   - Alterations to authentication, authorization, or security posture.
   - Deviations from existing architecture patterns.
2. Mark these items prominently in the Consequential Decisions checklist of `system-design.md` (SAFE-002).

### Step 12: Produce `system-design.md`
1. Populate `templates/system-design.md` with the completed architecture.
2. Set document metadata:
   - `Status: DRAFT`
   - `Version: 1.0`
3. Save to target feature directory: `.dev-team/features/<feature-name>/system-design.md`.

---

## 5. Output Expectations

The System Design skill produces:
1. **`system-design.md`:** Complete, structured technical architecture document in `.dev-team/features/<feature-name>/system-design.md`.
2. **Consequential Decisions Summary:** Clear list of trade-offs and approvals requested from the developer.

---

## 6. Quality Checklist

- [ ] Requirements traceability: Every component traces to at least one `REQ-xxx` ID.
- [ ] Technology alignment: Matches discovered project patterns (no foreign architecture forced).
- [ ] Proportionality: Simple features have concise designs; no unnecessary abstractions.
- [ ] Database/Persistence: Schemas, indexes, constraints, migrations, and RLS clearly defined (if applicable).
- [ ] Integration & Resilience: Endpoints, error codes, and offline behavior addressed (if applicable).
- [ ] Security: Authentication, authorization, input validation, and data protection addressed.
- [ ] ADRs: Important choices documented with context, options, and trade-offs.
- [ ] Approval gate: Significant decisions explicitly flagged for developer approval (SAFE-002).

---

## 7. Safety Boundaries

- **SAFE-002:** Consequential architecture and data model decisions require explicit developer sign-off before implementation.
- **SAFE-004:** Architectural design must not silently broaden or alter approved requirements scope.
- **SAFE-005:** No secrets, credentials, or production tokens may be included in the design document.
- **SAFE-007:** No migrations may be applied to production or user databases during design.

