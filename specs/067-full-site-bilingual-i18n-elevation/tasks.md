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
- [x] T043: Bilingual elevation for `AdmissionTarget` and static data models in `frontend/src/pages/admission.tsx`.
- [x] T044: Bilingual elevation for `AppHead`, `Navbar`, and Flagship Hero/PageHeader.
- [x] T045: Bilingual elevation for Admission Target Blueprint Grid & Negative Marking Analytics (`target_du`, `target_buet`, `target_medical`, `-০.২৫`).
- [x] T046: Bilingual elevation for `AdmissionCounselingMatrix.tsx` and `MigrationCascadeVisualizer.tsx`.
- [x] T047: Bilingual elevation for Admission Calculator & FAQ Accordions.
- [x] T048: Quality Assurance (TypeScript, Phase 98 test suite, strict zero-emoji scan).
- [x] T049: Git commit, push to `origin/main`, rebuild & deploy to GitHub Pages, and verify live HTTP 200.

## Phase 9: Tuition Match & Escrow Milestone Hub Bilingual Elevation (`frontend/src/pages/tuition.tsx` & subcomponents)
- [x] T050: Bilingual elevation for `TutorProfile` and `TuitionPost` static data models in `frontend/src/pages/tuition.tsx`.
- [x] T051: Bilingual elevation for `AppHead`, `Navbar`, and PageHeader in `frontend/src/pages/tuition.tsx`.
- [x] T052: Bilingual elevation for Thana multi-vector filter console (`selectedThana`, `ধানমন্ডি`).
- [x] T053: Bilingual elevation for Verified Teacher Cards (`isVerifiedTutor`, credentials, subjects, hourly rates).
- [x] T054: Bilingual elevation for Escrow Milestone Policy & Consent Modal (`escrowEligible`, `এসক্রো মাইলস্টোন`, `requestTuitionConsent`, `Modal`).
- [x] T055: Quality Assurance (TypeScript, test suite, strict zero-emoji scan).
- [x] T056: Git commit, push to `origin/main`, deploy to GitHub Pages, and verify live HTTP 200 for `/tuition/`.

## Phase 10: Career Pathway & Portfolio Hub Bilingual Elevation (`frontend/src/pages/career.tsx` & subcomponents)
- [x] T057: Bilingual elevation for `CareerJob`, `GovtCircular`, `SalaryBenchmark`, `CareerFaq` data structures in `careerElevationData.ts`.
- [x] T058: Bilingual elevation for `AppHead`, `Navbar`, and Flagship Header in `frontend/src/pages/career.tsx`.
- [x] T059: Bilingual elevation for `CareerStatsHeader.tsx` (Master stats telemetry & Tab navigation).
- [x] T060: Bilingual elevation for `CareerSearchFilterBar.tsx` and `CareerCategoryGrid.tsx`.
- [x] T061: Bilingual elevation for `CareerJobBoard.tsx`, `JobDetailModal.tsx`, and `JobApplyModal.tsx`.
- [x] T062: Bilingual elevation for `CareerATSApplicationPipeline.tsx` and `GovtCircularsAndCareerGuide.tsx`.
- [x] T063: Bilingual elevation for `BdjobsProCvBuilderModal.tsx` and `EmployerJobPostingWizardModal.tsx`.
- [x] T064: Bilingual elevation for Verifiable Skills & Sealed Cryptographic CV Snapshot Builder in `frontend/src/pages/career.tsx` (`latestSealedSnapshot`, `cvSnapshotId`, `SHORTLISTED`, `apiClient.getCareerProfile`, `animate-pulse`).
- [x] T065: Quality Assurance (TypeScript zero-error, backend test suite, strict zero-emoji scan).
- [x] T066: Git commit, push to `origin/main`, deploy to GitHub Pages, and verify live HTTP 200 for `/career/`.

## Phase 11: Student Authentication & Minor-Safe Onboarding Bilingual Elevation (`frontend/src/pages/auth.tsx`)
- [x] T067: Integrate `useTranslation()` hook, dynamic document title, `<Head>`, and `[BN | EN]` switcher in `frontend/src/pages/auth.tsx`.
- [x] T068: Bilingual elevation for Brand Identity & Header (`অগ্রযাত্রা` / `Agragoti`, `নিরাপদ ও দীর্ঘমেয়াদি শিক্ষার্থী প্রোফাইল` / `Secure & Lifelong Student Profile`).
- [x] T069: Bilingual elevation for Mode Switcher (`নতুন অ্যাকাউন্ট` / `New Account`, `লগইন করুন` / `Log In`).
- [x] T070: Bilingual elevation for Registration Form fields (Full Name, Age, Curriculum Medium, Education Stage options).
- [x] T071: Bilingual elevation for Minor-Safe Onboarding Alert (`শিশু ও অপ্রাপ্তবয়স্ক সুরক্ষা` / `Child & Minor Safety Guard`).
- [x] T072: Bilingual elevation for Identifier, SMS OTP Verification workflow, and Password fields.
- [x] T073: Bilingual elevation for Submit CTAs, Quick Student Demo Credential helper, Terms disclaimer, and Page Footer.
- [x] T074: Quality Assurance (TypeScript zero-error check, backend test suites, strict zero-emoji scan).
- [ ] T075: Git commit, push to `origin/main`, deploy to GitHub Pages, and verify live HTTP 200 for `/auth/`.



