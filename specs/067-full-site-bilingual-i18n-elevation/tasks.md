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

## Phase 5: Live Challenge Arena Bilingual Elevation (`frontend/src/pages/live-challenge.tsx` & subcomponents)
- [x] T015: Bilingual translation for `frontend/src/pages/live-challenge.tsx` (AppHead, Page header, central leaderboard card header, sidebar privacy & exam rules protocol).
- [x] T016: Bilingual translation for `frontend/src/components/live-challenge/LiveMcqHeroSection.tsx`.
- [x] T017: Bilingual translation for `frontend/src/components/live-challenge/LiveCategoryTrackSelector.tsx`.
- [x] T018: Bilingual translation for `frontend/src/components/live-challenge/DynamicInfoNoticeBoard.tsx`.
- [x] T019: Bilingual translation for `frontend/src/components/live-free/LiveFreeDemoExamBox.tsx`.
- [x] T020: Bilingual translation for `frontend/src/components/live-challenge/LiveHowItWorksPathway.tsx`.
- [x] T021: Bilingual translation for `frontend/src/components/live-challenge/SubjectWeightageBreakdown.tsx`.
- [x] T022: Bilingual translation for `frontend/src/components/live-challenge/InteractiveOmrSimulator.tsx`.
- [x] T023: Bilingual translation for `frontend/src/components/live-challenge/AcademicLeaderboardReveal.tsx`.
- [x] T024: Bilingual translation for `frontend/src/components/live-challenge/LiveExamAnalyticsCard.tsx`.
- [x] T025: Bilingual translation for `frontend/src/components/live-challenge/LiveExamRoutineMatrix.tsx`.
- [x] T026: Bilingual translation for `frontend/src/components/live-challenge/LiveMcqFeatureShowcase.tsx`.
- [x] T027: Bilingual translation for `frontend/src/components/live-challenge/LiveMentorAndHallOfFame.tsx`.
- [x] T028: Bilingual translation for `frontend/src/components/live-challenge/LiveMcqFaqAccordion.tsx`.
- [x] T029: Bilingual translation for `frontend/src/components/live-challenge/ExamRulesProtocolModal.tsx`.

## Phase 6: Quality Assurance & Live Verification
- [x] T030: Run TypeScript verification (`cd frontend && npx tsc --noEmit`).
- [x] T031: Run backend test suites (`backend/tests/test_phase98_3_unified_subpages.py`, `backend/tests/test_phase98_flagship_ui_elevation.py`, `backend/tests/test_phase95_bilingual_localization.py`).
- [x] T032: Run strict zero-emoji regex scan across all modified files.
- [x] T033: Git commit to `main`, push to `origin/main`, deploy to `gh-pages` via `scripts/deploy-gh-pages.sh --rebuild` and verify live HTTP 200.

## Phase 7: Academic Learning Hub Bilingual Elevation (`frontend/src/pages/learn.tsx`)
- [x] T034: Add `titleEn` and `summaryNotesEn` to `ChapterItem` interface and all 14 chapters in `CURATED_SUBJECTS` in `frontend/src/pages/learn.tsx`.
- [x] T035: Bilingual elevation for `AppHead`, `Navbar`, and `PageHeader` in `frontend/src/pages/learn.tsx`.
- [x] T036: Bilingual elevation for Section 1 (Level Switcher & Chapter Search Console).
- [x] T037: Bilingual elevation for Section 2 (Spaced-Repetition Revision Queue), strictly preserving tested Bengali assertions.
- [x] T038: Bilingual elevation for Section 3 (NCTB Subjects & Chapters Matrix, gauges, cards).
- [x] T039: Bilingual elevation for Section 4 (Pedagogical Roadmap) & Section 5 (Curriculum FAQs).
- [x] T040: Bilingual elevation for Chapter Editorial Notes Drawer & HLS Video Lecture Modal.
- [x] T041: Quality Assurance (TypeScript zero-error & backend test suite verification).
- [x] T042: Commit to `main`, push to `origin/main`, deploy to `gh-pages` and verify live HTTP 200 for `/learn/`.

## Phase 8: University Admission Battleground Hub Bilingual Elevation (`frontend/src/pages/admission.tsx` & subcomponents)
- [ ] T043: Bilingual elevation for `AdmissionTarget` and static data models in `frontend/src/pages/admission.tsx`.
- [ ] T044: Bilingual elevation for `AppHead`, `Navbar`, and Flagship Hero/PageHeader.
- [ ] T045: Bilingual elevation for Admission Target Blueprint Grid & Negative Marking Analytics (`target_du`, `target_buet`, `target_medical`, `-০.২৫`).
- [ ] T046: Bilingual elevation for `AdmissionCounselingMatrix.tsx` and `MigrationCascadeVisualizer.tsx`.
- [ ] T047: Bilingual elevation for Admission Calculator & FAQ Accordions.
- [ ] T048: Quality Assurance (TypeScript, Phase 98 test suite, strict zero-emoji scan).
- [ ] T049: Git commit, push to `origin/main`, rebuild & deploy to GitHub Pages, and verify live HTTP 200.

