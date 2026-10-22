<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 109 Corporate Talent Acquisition & Cryptographic Skill Pipeline
FILE:      specs/013-phase109-corporate-talent-pipeline/spec.md
PHASE:     Phase 109 - Corporate Talent Acquisition & Cryptographic Skill Pipeline
PURPOSE:   Establishes functional specifications for algorithmic skill-to-job matching
           using cosine vector similarity, cryptographic W3C verifiable skill credentials,
           tamper-evident sealed CV snapshots, and bilateral recruitment pipelines.
STANDARDS: W3C Verifiable Credentials, Vector Cosine Similarity, Zero-Emoji, UI/UX Pro Max
-->

# Specification: Phase 109 — Corporate Talent Acquisition & Cryptographic Skill Pipeline

## Feature Directory
`specs/013-phase109-corporate-talent-pipeline`

## 1. Problem Statement
The transition from academic excellence to high-impact corporate technology careers in Bangladesh is plagued by resume fraud, unverified credentials, and inefficient manual recruitment. Employers waste hundreds of hours screening inflated resumes, while truly talented students from top institutions (BUET, DU, SUST, IUT, DMC) struggle to prove their practical competencies in modern domains like High-Performance Computing (HPC), Machine Learning, Mathematical Modeling, and Distributed Systems.

"Student Life Circle (অগ্রযাত্রা)" requires a world-class **Corporate Talent Acquisition & Cryptographic Skill Pipeline**:
1. **Algorithmic Skill Matching:** Evaluates candidates against corporate technical requirements using normalized skill vector cosine similarity.
2. **Cryptographic Credential Verification:** Validates student skills using W3C Verifiable Credentials and sealed CV snapshots secured by SHA-256 cryptographic hashes.
3. **Bilateral Recruitment Pipeline:** Recruiter workflow tracking candidates from Sourced to Shortlisted, Technical Assessment, and Offer Issued.
4. **Linear / Stripe / Wellfound Tier Portal:** High-density, keyboard-accessible recruiter studio with tactile 3D buttons, skill radar badges, and interview dispatch.

---

## 2. Mathematical Foundation: Skill Vector Cosine Similarity

Let the job requirement vector be $\vec{J} = (j_1, j_2, \dots, j_n)$ and the candidate's verified skill profile vector be $\vec{S} = (s_1, s_2, \dots, s_n)$, where each dimension represents verified proficiency in a given domain (e.g. `Python`, `HPC`, `Next.js`, `Math Modeling`, `Rust`).

The match score is defined by cosine similarity:
$$\text{Similarity}(\vec{J}, \vec{S}) = \frac{\sum_{i=1}^n j_i \cdot s_i}{\sqrt{\sum_{i=1}^n j_i^2} \cdot \sqrt{\sum_{i=1}^n s_i^2}}$$

Candidates with $\text{Similarity} \ge 0.85$ are flagged as **High Match (উচ্চ উপযুক্ততা)**, while $0.70 \le \text{Similarity} < 0.85$ are flagged as **Strong Match (উপযুক্ত প্রার্থী)**.

---

## 3. User Stories & Acceptance Criteria

### US1: Algorithmic Skill-to-Job Matching Engine (P1)
- As a technical talent recruiter, I want candidates automatically ranked by cosine vector similarity against job requirements so I can instantly identify top engineering talent.
- Acceptance Criteria:
  - Vector cosine calculation between normalized job weights and student skill ratings.
  - Return normalized match percentage ($0\text{--}100\%$) and matched domain tags.

### US2: Cryptographic CV Snapshot & W3C Credential Verification (P1)
- As an enterprise hiring manager, I want to mathematically verify that a candidate's CV snapshot and skill credentials have not been tampered with since issuance.
- Acceptance Criteria:
  - Validates SHA-256 seal signature over candidate credentials.
  - Detects any altered grades, fake diplomas, or falsified project records.

### US3: Bilateral Recruitment Pipeline Stage Management (P1)
- As a recruiter, I want to transition candidates across structured recruitment stages: `SOURCED` $\to$ `SHORTLISTED` $\to$ `TECHNICAL_ASSESSMENT` $\to$ `OFFER_ISSUED`.
- Acceptance Criteria:
  - State machine enforcing valid sequential and rollback transitions.
  - Dispatches interview invitation with role title, CTC compensation in BDT, and interview schedule.

### US4: Linear / Stripe / Wellfound Tier Recruiter Portal UI (P1)
- As an enterprise recruiter, I want a sleek, midnight slate interface with tactile 3D buttons, search filters, and 1-click interview offer dispatch.
- Acceptance Criteria:
  - `frontend/src/components/career/CorporateRecruiterPortal.tsx`
  - `frontend/src/components/career/CandidateTalentCard.tsx`
  - `frontend/src/pages/recruiter.tsx`
  - Tactile 3D button depth (`shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`).
  - Strict Zero-Emoji compliance (pure Lucide SVG vectors: `Briefcase`, `ShieldCheck`, `Code`, `Award`, `ExternalLink`, `CheckCircle2`).

### US5: REST API & Automated Verification Suite (P1)
- As an API client, I need endpoints to search candidates, verify CV snapshots, compute match scores, and issue interview invites.
- Acceptance Criteria:
  - `GET /api/v1/talent/candidates`
  - `POST /api/v1/talent/interview/invite`
  - `POST /api/v1/talent/cv-snapshot/verify`
  - `POST /api/v1/talent/match-score`
  - Automated test suite `backend/tests/test_phase109_corporate_talent_pipeline.py` passing 100%.
