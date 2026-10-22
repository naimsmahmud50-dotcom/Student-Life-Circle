# Implementation Plan: Student Growth Platform (অগ্রযাত্রা)

**Branch:** `main`  
**Feature Dir:** `specs/001-student-growth-platform`  
**Target:** World-Class Educational & Career Companion Architecture  

---

## 1. Technical Context & Stack Justification

### Why This Technology Stack is the World's Best Choice for this Platform

Building a platform that supports millions of registered students, handles massive concurrent spikes during live nationwide quizzes, protects minor privacy, and runs smoothly on low-bandwidth mobile devices in Bangladesh demands a meticulously reasoned architecture.

```
                      [ Client Browsers / PWA (Mobile & Desktop) ]
                                            │
                                            ▼
                           [ Global Edge / CDN (Cloudflare) ]
                        (Static Assets, Edge Cache, SSL, DDoS)
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │       Next.js 15+ App Router Frontend        │
                    │   - Server Components for Instant First Load  │
                    │   - Accessible Radix Primitives + Lucide SVGs │
                    │   - PWA Offline Service Worker & Sync Queue   │
                    └───────────────────────┬───────────────────────┘
                                            │ REST / WebSocket (OpenAPI Spec)
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │       Python 3.12+ FastAPI Core Engine        │
                    │   (Clean Architecture / Domain-Driven Design) │
                    │   - Auth & Session Guard (Argon2id + JWT)     │
                    │   - Live MCQ Engine & Server-Authoritative Clocks
                    │   - Pydantic v2 Strict DTO & Contract Validation│
                    │   - AI Quality Gate & Semantic Deduplication  │
                    │   - Admission & Curriculum Engine             │
                    │   - Tuition & Job Application Service         │
                    │   - Content Review & Quarantine Ops           │
                    └───────────┬───────────────────────┬───────────┘
                                │                       │
                                ▼                       ▼
               ┌──────────────────────────────┐   ┌──────────────────────────────┐
               │    In-Memory Cache & Queue   │   │     Primary Relational DB    │
               │    (Redis 7+ / Celery / ARQ) │   │  (PostgreSQL 16+ + pgvector) │
               │  - Sub-ms Idempotent Keys    │   │  - ACID Transaction Safety   │
               │  - Pre-warmed Quiz Blueprints│   │  - Immutable Question Versions│
               │  - Live Rate Limiting        │   │  - PgBouncer Pooling         │
               │  - Background Async Workers  │   │  - Semantic Vector Similarity│
               └──────────────────────────────┘   └──────────────────────────────┘
                                                                │
                                                                ▼
                                                  ┌──────────────────────────────┐
                                                  │    Private Object Storage    │
                                                  │   (Cloudflare R2 / AWS S3)   │
                                                  │  - Signed, Time-Limited URLs │
                                                  │  - CV Snapshots, Evidence    │
                                                  └──────────────────────────────┘
```

#### 1. Frontend: Next.js 15+ (App Router) + React 19 + TypeScript + Tailwind CSS
- **Why**: 
  - **Instant First-Load on 3G/4G Networks**: Next.js Server Components pre-render learning content and public pages on the edge, sending lightweight HTML with minimal client-side JavaScript. This eliminates blank-screen waits for students on budget Android devices.
  - **Progressive Web App (PWA)**: Provides an app-like experience (installable to homescreen, offline caching of practice sets, push notifications for scheduled challenges) without forcing students to download heavy 100MB+ APKs.
  - **Type-Safe Component Architecture**: TypeScript prevents undefined property errors across complex exam state transitions and diverse curriculum data structures.
  - **Tailwind CSS + Radix UI**: Guarantees strict adherence to our design tokens, zero-runtime styling overhead, and out-of-the-box WCAG 2.2 AA accessibility (screen reader labels, focus traps, keyboard navigation).

#### 2. Backend & Intelligence Engine: Python 3.12+ with FastAPI + AsyncPG
- **Why**: 
  - **Native AI, NLP & ML Dominance**: The blueprint requires automated duplicate question detection, semantic embedding similarity (`pgvector`), NCTB curriculum ingestion, and automated explanation drafting. Python is the world's undisputed standard for these operations (`LangChain`, `PyTorch`, `sentence-transformers`, `spaCy`, `BNLP`).
  - **Ultra-High Concurrency via Async/Await**: FastAPI runs on `Starlette` and `uvloop`, achieving performance metrics on par with Go and Node.js for asynchronous I/O and database operations.
  - **Pydantic v2 Type Safety & Auto-Documentation**: High-speed Rust-powered data parsing with Pydantic ensures zero malformed data enters the system. It auto-generates interactive OpenAPI/Swagger contracts that feed directly into frontend TypeScript clients.
  - **Scientific Analytics & Spaced Repetition**: Implementing the SuperMemo SM-2 spaced repetition algorithm, question difficulty discrimination curves, and percentile rankings is native and trivial using Python's `numpy` and `scipy` ecosystem.

#### 3. Primary Data Store: PostgreSQL 16+ (with PgBouncer connection pooling)
- **Why**:
  - **ACID Integrity for High-Stakes Exams**: When thousands of students submit answers within seconds, transactional consistency is paramount. Relational foreign keys prevent orphan submissions, duplicate score records, or broken audit trails.
  - **Immutable Versioning**: PostgreSQL easily handles immutable question versioning (`question_versions`), historical attempts, and audit logs.
  - **JSONB Flexibility for Curricula**: Enables structured querying of diverse exam blueprints (negative marking, sectional time limits, mathematical LaTeX expressions) alongside normalized relational tables.
  - **pgvector Support**: Built-in vector search for question duplicate detection and semantic recommendations without needing an expensive third-party vector database.

#### 4. Cache & Queue: Redis 7+ and BullMQ
- **Why**:
  - **Thundering Herd Protection**: Before a scheduled Live Challenge begins, question blueprints are pre-warmed into Redis. When 50,000 students click "Start" at 8:00:00 PM, requests hit Redis memory caches rather than overwhelming the PostgreSQL connection pool.
  - **Sub-Millisecond Idempotent Answer Writes**: Answers are validated against Redis token buckets and buffered through BullMQ background queues for durable batch-persistence into PostgreSQL.
  - **Server-Authoritative Ephemeral Timers**: Redis keys with strict TTLs manage session expiration, preventing any client-side clock tampering.

#### 5. Object Storage: Cloudflare R2 / AWS S3 with Time-Limited Signed URLs
- **Why**:
  - **Child & Student Privacy**: Resumes, academic certificates, and student ID verification documents are stored in private buckets. Access is granted exclusively via signed URLs expiring after 5 minutes.
  - **Zero Egress Fees**: Cloudflare R2 allows cost-predictable scaling without bandwidth penalties.

---

## 2. Live MCQ Engine: High-Concurrency & Fair Scoring Architecture

### Thundering Herd & Concurrency Management
1. **Pre-Warming**: 10 minutes prior to a scheduled Live Challenge, the backend freezes the question blueprint and caches the sanitized question payloads (without answer keys) in Redis.
2. **Deterministic Randomization**: When a student enters, the backend generates a deterministic random seed tied to `(user_id, session_id)`. Question order and option sequences are shuffled server-side to prevent screen-peeking.
3. **Server-Authoritative Clock**:
   - The test start timestamp and allowed duration are anchored to the server's NTP-synchronized clock.
   - Any client-submitted `time_taken` is treated as a telemetry hint only; actual elapsed time is strictly calculated server-side.
4. **Idempotent Answer Pipeline**:
   ```
   Client (PUT /api/v1/quiz-attempts/:id/answers/:qid)
     Header: X-Idempotency-Key: <UUIDv4>
     Payload: { option_id: "opt_xyz", client_timestamp: 1728901234 }
        │
        ▼
   Backend Idempotency Guard (Redis GETSET idempotency:<uuid>)
     ├── If key exists: Return cached 200 OK with previously recorded status.
     └── If new:
           1. Validate session is still ACTIVE and current_time <= expires_at.
           2. Save answer into Redis active attempt hash.
           3. Push async write event to BullMQ `durable-answer-writer` queue.
           4. Return HTTP 200 { status: "saved", sync_time: server_now }.
   ```
5. **Score Calculation & Result Release**:
   - While a live session is active, no correct answers or explanations are revealed to anyone.
   - Upon session close, background workers calculate scores against the frozen question version snapshot.
   - Leaderboards are computed in aggregated rank snapshots (e.g., refreshed every 30 seconds or published at session close) to prevent database read lockups.

---

## 3. Question Bank & Content Operations (The Trust Engine)

### State Machine Lifecycle
```
 [Draft] ──(Submit)──> [Needs Review] ──(SME Approve)──> [Approved] ──(Batch)──> [Scheduled]
    │                         │                                                    │
    ▼                         ▼                                                    ▼
 [Archived] <──(Deprecate)── [Quarantined] <──(Issue Reported / Flagged)───── [Published]
```

### AI Quality Gate & Human Editorial Loop
- **The Golden Rule**: AI is an assistant, never an unreviewed publisher.
- **Draft Generation**: Authors may invoke AI to generate distractor options, math explanations, or test questions from NCTB curriculum outlines.
- **Deduplication Check**: Before saving, the draft runs through:
  1. Exact SHA-256 text hash check.
  2. Jaccard & Levenshtein string similarity check.
  3. Semantic cosine similarity using `pgvector` embeddings (>0.88 cosine similarity triggers duplicate warning).
- **SME Verification Gate**: Every question requires approval by a verified subject-matter expert with documented citations (e.g., textbook name, edition, page number, or board year).
- **Single-Click Quarantine & Score Re-Tally**: If students flag an answer key error during an active test, admins can immediately trigger `Quarantine`. The engine flags all affected attempts, runs an automated score reconciliation, and logs the decision to the immutable audit trail.

---

## 4. UI/UX Pro Max Design System & Strict Anti-Emoji Rules

### The Non-Negotiable Human-Centric UI Doctrine
- **Zero Emojis on Buttons & Controls**:
  - **Prohibited**: Buttons like `🚀 Start Quiz`, `🔥 Streak`, `💡 Hint`, `🏆 Leaderboard`.
  - **Mandated**: Clean, dignified typography with semantic Lucide SVG icons:
    - `<Button><Play className="w-4 h-4 mr-2" aria-hidden="true" /> অনুশীলন শুরু করুন</Button>`
    - `<Badge variant="outline"><Flame className="w-3.5 h-3.5 mr-1 text-amber-500" /> ধারাবাহিকতা: ৫ দিন</Badge>`
    - `<Button variant="ghost"><HelpCircle className="w-4 h-4 mr-2" /> ব্যাখ্যা দেখুন</Button>`
    - `<Button variant="primary"><Award className="w-4 h-4 mr-2" /> ফলাফল ও অগ্রগতি</Button>`

### Visual Identity Tokens
- **Theme**: Human, calm, academic excellence, clarity.
- **Colors**:
  - `--color-primary`: `#0F172A` (Deep Slate Navy)
  - `--color-brand`: `#2563EB` (Confident Blue)
  - `--color-mastery`: `#0D9488` (Teal - for progress & correct answers)
  - `--color-warning`: `#D97706` (Amber - for deadlines & timers under 60s)
  - `--color-danger`: `#DC2626` (Crimson - strictly for critical errors & reports)
  - `--color-surface`: `#FFFFFF`
  - `--color-background`: `#F8FAFC`
  - `--color-text-main`: `#0F172A`
  - `--color-text-muted`: `#475569`
  - `--color-border`: `#E2E8F0`
- **Typography Pairing**:
  - Bengali Text: `Noto Sans Bengali` (weights 400, 500, 600, 700). Body text 16px with 1.6 line height.
  - English & Numbers: `Inter` / `Geist Sans` with tabular figures enabled for countdown timers.
- **Responsive Touch Standards**:
  - Minimum touch targets: 44×44px (48px for quiz option cards).
  - Prominent `:focus-visible` focus rings (2px solid `#2563EB` with 2px offset).
  - Respects `prefers-reduced-motion`.

---

## 5. Security, Child Safety & Privacy Architecture (ASVS Level 2)

```
                            [ Inbound Request ]
                                    │
                                    ▼
                     [ Rate Limiter & WAF Guard ]
                   (Max 5 login/min, 60 answers/min)
                                    │
                                    ▼
                   [ Authentication & Session Check ]
                     (HttpOnly Cookie, Argon2id Hash)
                                    │
                                    ▼
                [ RBAC + ABAC Resource Ownership Guard ]
              (Is Student owner of Attempt? Is User Admin?)
                                    │
                 ┌──────────────────┴──────────────────┐
                 ▼                                     ▼
        [ Minor Privacy Guard ]               [ IDOR Prevention ]
   (Block Direct PII Exposure,             (Verify resource.user_id
    Enforce Guardian Consent)                  === auth.user_id)
                 │                                     │
                 └──────────────────┬──────────────────┘
                                    ▼
                         [ Controller / Service ]
                                    │
                                    ▼
                         [ Immutable Audit Log ]
```

1. **Authentication & Identity**:
   - Multi-factor authentication (MFA / TOTP) required for all Admin, Reviewer, and Recruiter accounts.
   - Passwords hashed using Argon2id (memory: 64MB, iterations: 3, parallelism: 1).
   - Session tokens stored exclusively in `HttpOnly`, `SameSite=Strict`, `Secure` cookies.
2. **Minor Protection & Consent**:
   - Accounts under digital consent age cannot publish public profiles, phone numbers, or residential addresses.
   - Guardian link protocol: Guardians receive progress summaries (study frequency, topic accuracy) but cannot view personal diary notes or private student thoughts.
   - Adult tutors cannot directly initiate unmonitored private chats with minor students; all messages flow through guardian-authorized channels.
3. **Data Minimization & CV Snapshots**:
   - Student job applications generate an immutable JSON snapshot of selected skills, education history, and portfolio links.
   - When a student later edits their active profile, the previously submitted application to an employer remains untampered as evidence.
4. **OWASP ASVS Verification**:
   - Parameterized SQL queries via ORM to completely eliminate SQL injection.
   - HTML sanitization (DOMPurify) for all user-submitted text to eliminate XSS.
   - Secure HTTP headers: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`.

---

## 6. Enterprise Admin, Moderation & Support Operations

### Administrative Separation of Concerns
| Role | Allowed Scope | Prohibited Actions |
|---|---|---|
| **Platform Admin** | System configuration, server health, staff role assignments | Cannot tamper with live test results or view unredacted student passwords |
| **Content Editor** | Draft questions, update study notes, curate reading links | Cannot publish questions to production live sessions directly |
| **Subject Reviewer** | Verify draft questions, approve answer keys, resolve reported questions | Cannot change platform financial or user authentication settings |
| **Safety Moderator** | Review reported tuition/job listings, handle spam, inspect dispute tickets | Cannot modify question bank content or answer keys |
| **Support Agent** | Respond to user account tickets, password resets, payment queries | Least privilege: No access to exam secret keys or raw database queries |

---

## 7. Delivery Roadmap & Staged Rollout

```
  Phase 1: Foundation & Specs (Week 1-2)
  ├── SpecKit Constitution, Specification, Data Models, OpenAPI Contracts
  └── UI/UX Pro Max Design System & Component Library (Zero-Emoji Policy)

  Phase 2: Platform Engine & Security (Week 3-4)
  ├── Auth System (RBAC/ABAC, Session Management, Minor Privacy Defaults)
  └── Database Schemas, Migrations & PgBouncer Setup

  Phase 3: Learning Hub & Anytime Practice MVP (Week 5-7)
  ├── Class/Curriculum Resource Catalog (Class 6-10, HSC)
  ├── Question Bank CMS (Immutable Versions, Deduplication, Review Flow)
  └── Anytime MCQ Engine (Idempotent saves, Spaced-Repetition Mistake Replay)

  Phase 4: Scheduled Live Challenge & High-Load Engine (Week 8-10)
  ├── Server-Authoritative Timer & Pre-warmed Redis Cache
  ├── Randomized Delivery & Pseudonymous Leaderboards
  └── Load Testing Burst Verification (Simulated 50,000 Concurrent Users)

  Phase 5: University Admission, Tuition & Career Portfolios (Week 11-13)
  ├── Admission Mocks (Negative Marking, DU/BUET/Medical Blueprints)
  ├── Verified Tuition Marketplace (Trust guardrails & contact consent)
  └── Skills Portfolio & Immutable CV Application Snapshots

  Phase 6: Enterprise Admin, Auditing & Launch Drill (Week 14-15)
  ├── Admin Console, Single-Click Question Quarantine, Audit Logs
  └── Disaster Recovery Rehearsal & Production Go-Live
```

---

## 8. Tri-Platform Convergence Architecture (10MS + CareTutors + Bdjobs)

The platform formally consolidates Bangladesh's three most essential educational and career sectors into a single continuous student experience:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│             STUDENT LIFE CIRCLE (AGROJATRA) UNIFIED PLATFORM                │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ 10 MINUTE SCHOOL     │ CARETUTORS           │ BDJOBS                        │
│ (Academic & Exam)    │ (Tuition & Trust)    │ (Career & Employment)         │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ • Interactive Video  │ • Live Tuition Job   │ • Verified Student Job Board  │
│   Micro-Classroom    │   Board by Region    │ • 1-Click Apply with Sealed   │
│ • In-Lecture Quiz    │ • Guardian Tuition   │   Cryptographic CV Snapshot   │
│ • CAT & IRT Testing  │   Post Wizard        │ • Real-time Application Stage │
│ • Socratic AI Tutor  │ • Bilateral Consent  │   Pipeline Tracker            │
│ • What-If Admission  │   & ASVS L2 Safety   │ • AI Mock Interview Coach     │
│   Simulator          │ • Tribunal Dispute   │ • Algorithmic Skill-to-Job    │
│ • Dual Language      │   Arbitration        │   Radar Matcher               │
│   Medium Switcher    │ • Integrity Bounties │ • Tamper-Proof SHA-256 Ledger │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

