# Tasks: Full-Site Bilingual (BN/EN) Internationalization Elevation

## Phase 1: Setup & Feature Tracking
- [x] T001: Register active feature in `.specify/feature.json` with `specs/067-full-site-bilingual-i18n-elevation`.

## Phase 2: Flagship Homepage Bilingual Implementation (`frontend/src/pages/index.tsx`)
- [x] T002: Implement dual-script BN/EN support in Section 1 (Editorial Hero, NCTB chips, stage selector chips, Call to Actions, and 4-point trust strip).
- [x] T003: Implement dual-script BN/EN support in Section 1.5 (4-in-1 Platform Disruption Grid comparing 10MS, Live MCQ, Careertutors, Bdjobs).
- [x] T004: Implement dual-script BN/EN support in Section 2 (Academic Progress, Daily Goals, Continuous Streak, and 3 Pedagogical Pillars).
- [x] T005: Implement dual-script BN/EN support in Section 3 (Curated Journey Pathways for SSC, HSC, Admission, and Career).
- [x] T006: Implement dual-script BN/EN support in Section 4 (3D STEM Virtual Labs, Physics/Chemistry experiment triggers, KaTeX formulas).
- [x] T007: Implement dual-script BN/EN support in Section 5 (National Live Challenge, localized countdown timer digits, and Socratic AI solver drawer trigger).
- [x] T008: Implement dual-script BN/EN support in Section 6 (W3C Cryptographic Proof-of-Skill Certificate showcase & QR verification card).
- [x] T009: Implement dual-script BN/EN support in Sections 6.5, 7, and 8 (Student Testimonials, Compliance & Trust Badges, and Closing Academic CTA).

## Phase 3: Quality Assurance & Verification
- [x] T010: Run static analysis with `npx tsc --noEmit` to verify zero TypeScript errors.
- [x] T011: Run backend test suites (`backend/tests/test_phase98_2_flagship_home_dashboard.py`, `backend/tests/test_phase98_1_app_shell_and_footer.py`) to confirm zero regressions.
- [x] T012: Run strict zero-emoji scanner on `frontend/src/pages/index.tsx`.

## Phase 4: Git Commit & Production Deployment
- [ ] T013: Commit changes to `main` and push to `origin/main`.
- [ ] T014: Build and deploy static export to `gh-pages` and verify live HTTP 200 response.

