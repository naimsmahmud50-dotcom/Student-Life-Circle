# SPEC: Phase 134 — Algorithmic Skill-to-Job Matching Radar & Recruiter Headhunting Pipeline

## 1. Overview
Phase 134 introduces the **Algorithmic Skill-to-Job Matching Radar & Recruiter Headhunting Pipeline**, a dignified academic recruitment system connecting verified student talents with top technology companies, corporate enterprises, and high-growth startups in Bangladesh. The module computes a multi-dimensional competency radar (Mathematics & Analytics, Coding & Algorithms, Olympiad Problem Solving, Communication, and Systems Architecture) and matches students to vacancies using vector cosine percentile alignment. Upon application, the system generates an immutable, cryptographically sealed CV snapshot anchored by SHA-256 hashes to guarantee provenance for recruiters.

## 2. Architectural Pillars
1. **Developer Architecture Note Standard**: Mandatory block comment on every created/modified file.
2. **Multi-Dimensional Competency Radar Algorithm**:
   - Computes normalized scores $[0, 100]$ across 5 dimensions using weighted student achievements:
     - $S_{\text{math}}$: Board Math GPA, Olympiad Math Score
     - $S_{\text{algo}}$: Practice module scores, Olympiad Informatics rank
     - $S_{\text{olympiad}}$: National & Regional STEM Olympiad achievements
     - $S_{\text{comm}}$: Viva-voce verbal scores, technical writeups
     - $S_{\text{systems}}$: Project submissions and lab simulations
   - Vector similarity matching: Computes cosine percentile alignment between candidate vector $\vec{C}$ and job profile vector $\vec{J}$.
3. **Immutable Sealed CV Snapshot Engine**:
   - Generates point-in-time cryptographic snapshots of student credentials and radar metrics at application moment.
   - Enforces SHA-256 provenance hashing and tamper detection.
4. **Supabase Migration 012 with 100% RLS & Immutability**:
   - Strict `REVOKE UPDATE, DELETE ON public.sealed_job_applications` under ASVS L2.
   - Multi-tenant isolation ensuring candidates and recruiters access only authorized dockets.
5. **Academic Recruiting Aesthetic**:
   - Oxford Academic Navy (`#0A2540`), Academic Emerald (`#065F46`), Scholar Gold (`#B45309`), Paper White (`#FAFAF8`).
   - Pure SVG 5-axis Radar Polygon Chart.
   - 3D physical tactile push buttons and pure Lucide vector icons with 0% emojis.

## 3. File Inventory
- `backend/career/__init__.py`: Package exports for skill matching and sealed CV snapshots.
- `backend/career/skill_matcher.py`: Core logic for radar calculation, job profile cosine matching, and sealed CV generation.
- `backend/migrations/012_career_skill_matching_rls.sql`: Database schema with immutable application ledger and RLS.
- `frontend/src/pages/career/radar.tsx`: Interactive radar dashboard with SVG chart, job vacancy cards, and sealed CV submission.
- `backend/tests/test_phase134_skill_matcher.py`: Automated test suite.
