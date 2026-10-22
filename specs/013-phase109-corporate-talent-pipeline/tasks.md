<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 109 Corporate Talent Acquisition & Cryptographic Skill Pipeline
FILE:      specs/013-phase109-corporate-talent-pipeline/tasks.md
PHASE:     Phase 109 - Corporate Talent Acquisition & Cryptographic Skill Pipeline
PURPOSE:   Ordered task list tracking atomic implementation steps for cosine vector
           skill matching, W3C verifiable credentials, sealed CV verification, recruitment pipelines, and test validation.
STANDARDS: W3C Verifiable Credentials, Vector Cosine Similarity, Zero-Emoji, UI/UX Pro Max
-->

# Tasks: Phase 109 — Corporate Talent Acquisition & Cryptographic Skill Pipeline

## Tasks Ledger

- [x] Task 1: Implement Corporate Talent Pipeline Service (`backend/app/services/corporate_talent_pipeline_service.py`)
  - Algorithmic skill-to-job matching with cosine vector similarity across standardized taxonomy
  - Cryptographic W3C verifiable skill credential validation and tamper-evident sealed CV snapshot hashing
  - Bilateral recruitment pipeline state machine (`SOURCED` -> `SHORTLISTED` -> `TECHNICAL_ASSESSMENT` -> `OFFER_ISSUED`)
  - Recruiter candidate discovery registry with university, CGPA, and skill ratings
- [x] Task 2: Implement Candidate Talent Card Component (`frontend/src/components/career/CandidateTalentCard.tsx`)
  - Linear / Stripe / Wellfound tier candidate card with skill radar tags and match percentage pill
  - Verified W3C Proof-of-Skill Certificate seal and GitHub/project external links
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`)
  - 1-click interview offer scheduling modal with role title, CTC salary in BDT, and interview date
- [x] Task 3: Implement Corporate Recruiter Portal Component (`frontend/src/components/career/CorporateRecruiterPortal.tsx`)
  - High-density candidate discovery grid with university filters (BUET, DU, SUST, etc.)
  - Minimum CGPA slider and verified skill chip filters (Python, Next.js, HPC, Math Modeling, Rust)
  - Recruitment stage tabs and candidate count statistics
  - Zero-Emoji compliance and 'Plus Jakarta Sans' + 'Hind Siliguri' typography
- [x] Task 4: Mount Talent Pipeline REST API Endpoints (`backend/app/api/v1/endpoints/talent_pipeline.py`)
  - `GET /api/v1/talent/candidates`
  - `POST /api/v1/talent/interview/invite`
  - `POST /api/v1/talent/cv-snapshot/verify`
  - `POST /api/v1/talent/match-score`
  - Mount router in `backend/app/api/v1/router.py`
- [x] Task 5: Implement Recruiter Studio Host Page (`frontend/src/pages/recruiter.tsx`)
  - Unified enterprise talent acquisition console mounting Recruiter Portal and Candidate Talent Card
  - Integration with Navbar, Footer, and AppHead
- [x] Task 6: Implement automated verification test suite (`backend/tests/test_phase109_corporate_talent_pipeline.py`)
  - Algorithmic skill-to-job cosine vector similarity math
  - Tamper detection on modified CV snapshots (invalid signature rejection)
  - Recruitment pipeline stage transitions and interview offer dispatch
  - REST API endpoint verification
  - Standardized Developer Architecture Note headers check and strict zero-emoji sweep
- [x] Task 7: Execute full regression test discovery (`python3 -m unittest discover -s backend/tests`) asserting 100% pass rate
