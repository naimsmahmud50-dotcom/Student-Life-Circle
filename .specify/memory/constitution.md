# Student Growth Platform (অগ্রযাত্রা) - Engineering Constitution

## 1. Core Principles & Philosophy
- **One Profile, Lifelong Journey**: A single unified account that scales seamlessly from Primary school (Class 1-5) to Secondary (SSC), Higher Secondary (HSC), University Admission, Skill Development, Tuition Marketplace, and Job/Career.
- **Contextual Guidance (Not a Giant Menu)**: The platform surfaces the single next most helpful action based on the learner's current grade, immediate goal, and privacy settings.
- **Learning Before Ranking**: Leaderboards provide healthy motivation without shame. No public shaming, no "fail/unfit" negative labeling, and strictly no pay-to-win advantage.
- **Verified Means Specific**: Nothing is badged as "verified" unless an exact document, institution, or identity credential has been checked. The scope of verification must always be visible.
- **AI as Assistant, Never Sovereign Editor**: AI may draft questions, study summaries, and explanations, but NO AI-generated question enters live competitions or formal admission mocks without human subject-matter expert review and source citation.
- **Scale by Evidence**: Stateless application instances, server-side authoritative state, idempotent answer pipelines, buffered queues, and measured load testing before premature sharding.

## 2. UI/UX Pro Max & Visual Design Governance
- **Human-Centric & Dignified Design**: The UI must feel welcoming, calm, focused, and respectful. Avoid frantic gamification, excessive neon/glassmorphism, flashing banners, or childish confetti bursts.
- **STRICT ZERO-EMOJI & NO-AI-BADGE POLICY ON BUTTONS & UI**:
  - **No emojis** (e.g., 🚀, 🔥, 🏆, 💡) shall be used as icons inside buttons, badges, headings, cards, or navigation tabs.
  - **Professional Vector Icons Only**: Use crisp, accessible, semantic SVG icons (Lucide Icons / Heroicons) with proper `aria-hidden="true"` or accessible labels.
  - Buttons must display clean, dignified human microcopy (e.g., "অনুশীলন শুরু করুন", "পরবর্তী প্রশ্ন", "সাবমিট করুন", "রিভিশন কিউ").
- **Visual Identity & Color Palette**:
  - Primary / Trust: Deep Navy Blue (`#0F172A` / `#1E293B` / `#1E40AF`)
  - Learning Progress & Mastery: Refined Teal / Cyan (`#0D9488` / `#0284C7`)
  - Warning & Deadlines: Warm Amber (`#D97706` / `#F59E0B`)
  - Critical Danger / Error: Dedicated Red (`#DC2626`) reserved strictly for actual risk/errors.
  - Neutral / Ground: Slate Warm White (`#F8FAFC` / `#FFFFFF`) with crisp 4.5:1 WCAG 2.2 AA contrast.
- **Typography**:
  - Primary Bengali Font: `Noto Sans Bengali` (balanced line-height 1.6, minimum 16px body on web).
  - Primary Latin/Numerical Font: `Inter` or `Geist Sans` for tabular numerals in countdown timers, scores, and mathematical symbols.
- **Mobile-First & Low-Bandwidth Optimizations**:
  - Optimized for 3G/4G network latencies common in Bangladesh.
  - Minimum touch targets: 44×44px with 8px+ spacing.
  - Zero Cumulative Layout Shift (CLS < 0.1), skeleton loaders, and graceful offline/retry states.

## 3. Technology Stack & Architectural Standards
- **Optimal Polyglot / Best-of-Breed Architecture**:
  - **Web Frontend & UI**: Next.js 15+ (App Router, React 19, TypeScript, Tailwind CSS, Radix UI Primitives, Lucide Icons, PWA).
  - **Backend API & Core Engine**: **Python 3.12+ with FastAPI** (High-concurrency Async/Await with `uvloop` + `asyncpg`, Pydantic v2 strict data validation, Clean Architecture / Domain-Driven Design).
  - **AI, NLP & Intelligence Engine**: **Python** (Sentence-Transformers, pgvector, LangChain, Bengali NLP, NumPy/SciPy for psychometric scoring and Spaced Repetition).
  - **Primary Relational Store**: PostgreSQL 16+ (ACID transactional guarantees, `pgvector` extension for semantic question deduplication, connection pooling via PgBouncer).
  - **In-Memory Cache & Message Broker**: Redis 7+ with Celery / ARQ for reliable background task processing and server-authoritative timer locks.
  - **Secure Object Storage**: Cloudflare R2 / AWS S3 with signed, time-limited private URLs for CVs, verification docs, and test materials.
- **Idempotency & Server Authority**:
  - Every answer save, quiz start, submission, and payment action MUST require an idempotent request key (`X-Idempotency-Key`).
  - The server is the SOLE authority on timers, scoring, and question ordering. Client-side clocks are completely untrusted.

## 4. Security, Privacy & Child Protection (ASVS Level 2)
- **Minor Protection & Consent**:
  - Children under legal digital consent age default to private profiles.
  - No direct messaging between unverified adults and minors.
  - Guardian-linked views require explicit student age-policy compliance; guardians cannot inspect private personal thoughts or non-academic spaces without mutual consent.
- **Authorization & Data Isolation**:
  - Role-Based Access Control (RBAC) paired with Attribute-Based Access Control (ABAC).
  - Zero IDOR tolerance: Every request validates entity ownership (`user_id === resource.owner_id`).
  - Sensitive PII (phone, exact home address, guardian contact) is never exposed in public listings or search engines.
  - Candidates share an explicit "CV snapshot" per job application; updating a general profile does not mutate previously submitted snapshots.
- **Audit & Anti-Abuse**:
  - Immutable audit logs for all administrative decisions, question modifications, answer key updates, and score re-tallies.
  - Rate limiting on authentication, question submission, and reporting endpoints.
