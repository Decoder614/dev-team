# Reference: Context Gathering & Adaptive Interview Guide

> **Project Initializer Reference Guide**  
> Adaptive interview techniques, structured question sequences for empty repositories, and truth-preservation principles.

---

## 1. Context Gathering Philosophy

Context gathering operates on a single non-negotiable rule:
**Truth Over Assumption.**
AI assistants must never invent architecture, select frameworks silently, or hallucinate business domains. If the developer has not specified a decision, it must be either asked directly or documented as an unconfirmed assumption (`ACTIVE_ASSUMPTIONS` or `OPEN_DECISIONS`).

---

## 2. Adaptive Questionnaire for Empty Repositories

When an empty or near-empty repository is detected, conduct a focused, adaptive interview. Do not overwhelm the developer with 20 questions at once. Group inquiries into four progressive clusters:

### Cluster 1: Vision, Purpose & Audience (Mandatory)
*Goal: Understand why this project exists and who will use it.*
1. **Product Objective:** What is the primary problem this application or service solves?
2. **Target Users:** Who is the primary audience (e.g., end-consumer mobile users, internal business operators, developers via CLI)?
3. **Core Workflow:** What is the single most critical user journey or job-to-be-done?

### Cluster 2: Target Platforms & Form Factors (Mandatory)
*Goal: Determine runtime environment and platform constraints.*
1. **Platforms:** What platforms must this run on initially?
   - Mobile: iOS, Android
   - Web: Desktop web, mobile responsive
   - Desktop: macOS, Windows, Linux
   - Backend / Serverless: Docker, Kubernetes, AWS Lambda, Cloud Run
   - Terminal: Command-Line Tool (CLI)

### Cluster 3: Technical Preferences & Ecosystem (Adaptive)
*Goal: Identify preferred languages and frameworks without forcing opinions.*
1. **Language & Framework:** Do you have a preferred stack in mind? (e.g., Flutter/Dart, React/TypeScript, Python/FastAPI, Go, Rust)
   - *If developer specifies:* Record as `CONFIRMED_FACTS`.
   - *If developer is undecided:* Present 2-3 viable options with brief trade-offs, or record as `OPEN_DECISION`.
2. **Backend & Persistence:** Will this project connect to an existing backend/API, require a new database (e.g., Supabase, PostgreSQL, SQLite), or run fully standalone/local?

### Cluster 4: Quality & Process Rigor (Optional / Defaults Available)
*Goal: Configure Dev-Team approval gates and workflow preferences.*
1. **Approval Gates:** Would you like strict approval gates on Requirements, Architecture, and Plans before code is written? *(Recommended default: Enabled)*
2. **Design System:** Will this project require a dedicated UI design token specification (`DESIGN.md`)? *(Default: Yes for frontend/mobile, No for backend/CLI)*

---

## 3. Techniques for Parsing Rough Ideas into Structure

Often developers provide informal or incomplete descriptions (e.g., *"I want an app that lets dog owners track vet visits"*). Use the following decomposition technique:

1. **Extract Core Nouns (Entities):**
   - Dog / Pet (`name`, `breed`, `birthdate`)
   - Vet Visit / Record (`date`, `clinic`, `notes`, `vaccinations`, `cost`)
   - User / Owner (`auth`, `profile`)
2. **Extract Core Verbs (Use Cases):**
   - Add new pet
   - Log vet appointment
   - View immunization timeline
   - Receive upcoming vaccination reminders
3. **Isolate Technical Boundaries:**
   - Client: Mobile app (offline-first storage for clinic records)
   - Notifications: Local OS notifications or push notifications
4. **Draft Candidate Facts vs Assumptions:**
   - *Fact:* User domain is pet healthcare tracking.
   - *Assumption (to validate):* Local offline storage is preferred initially over mandatory cloud sync.

---

## 4. Fact Categorization Standard

Every piece of project knowledge must be categorized into one of three buckets:

| Category | Definition | Storage Location | Example |
|---|---|---|---|
| **CONFIRMED_FACTS** | Verified truths from manifests, existing code, or explicit developer confirmation. | Section 2 of `project-context.md` | "Language is Dart 3.5, framework is Flutter 3.24" |
| **ACTIVE_ASSUMPTIONS** | Hypotheses adopted to make progress, but not yet validated with stakeholder. | Section 3 of `project-context.md` | "Assuming local SQLite persistence before cloud sync is built" |
| **OPEN_DECISIONS** | Architectural choices intentionally deferred for subsequent design workflows. | Section 3 of `project-context.md` | "State management between BLoC and Riverpod pending evaluation" |

---

## 5. Prohibited Anti-Patterns

1. **Silent Stack Assignment:** Choosing a framework (e.g., choosing React or Flutter) without the developer's explicit confirmation or a manifest presence.
2. **Speculative Database Schema:** Writing complete 10-table relational schemas during initial onboarding of an empty repository before requirements are defined.
3. **Fictitious API Endpoints:** Inventing third-party API contracts or authentication servers that have not been discussed.

