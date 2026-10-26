# Tasks: CareTutors-Inspired Tuition Marketplace Elevation

## Phase 1: REA & SpecKit Preparation (Complete)
- [x] T001: REA Ingestion of `https://caretutors.com` (homepage, wizard, job board, categories, trust model).
- [x] T002: Create `specs/047-caretutors-tuition-elevation/spec.md`.
- [x] T003: Create `specs/047-caretutors-tuition-elevation/plan.md`.
- [x] T004: Create `specs/047-caretutors-tuition-elevation/tasks.md`.

## Phase 2: Data Models & Components Implementation (Complete)
- [x] T005: Create `frontend/src/components/tuition/data/tuitionElevationData.ts` (Typed datasets: categories, jobs, tutors, salary calculator matrices, FAQs).
- [x] T006: Create `TuitionStatsHeader.tsx` (Live metric counter bar: Active Tutors, Live Jobs, Rating, Zero Scam).
- [x] T007: Create `TuitionCategoryPills.tsx` (8-category stream switcher with counts).
- [x] T008: Create `TutorRequestWizardModal.tsx` (4-step guardian request wizard with validation).
- [x] T009: Create `TuitionJobBoard.tsx` (Filterable tuition jobs with applicant counts and apply modal).
- [x] T010: Create `VerifiedTutorDirectory.tsx` (Directory of verified tutors with university credentials, ratings, and consent modal).
- [x] T011: Create `TuitionSalaryCalculator.tsx` (Interactive monthly salary calculator).
- [x] T012: Create `TuitionTrustAndSafetySection.tsx` (4-pillar trust model, 2 days trial, and escrow guarantee).

## Phase 3: Page Integration & Wiring (Complete)
- [x] T013: Elevate `frontend/src/pages/tuition.tsx` with unified tabs (Job Board, Verified Tutors, Request a Tutor, Salary Calculator, Safety & Policy).

## Phase 4: Verification & Security Audit (Complete)
- [x] T014: Run component unit tests (`frontend/src/components/tuition/__tests__/tuitionElevation.test.mjs`) - 5/5 passed.
- [x] T015: Run `python3 backend/scripts/run_zero_emoji_sweep.py` (Strict Zero-Emoji certification: 674 files, 0 violations).
- [x] T016: Next.js type check & production build (`npm --prefix frontend run build`) - 41/41 pages compiled.
- [x] T017: Run Playwright E2E tests (`frontend/e2e/tuition_elevation.spec.ts` & `tuition_marketplace.spec.ts`) - 9/9 passed.
- [x] T018: Run all 1,602 backend regression tests - 1,602/1,602 passed (100% green).
