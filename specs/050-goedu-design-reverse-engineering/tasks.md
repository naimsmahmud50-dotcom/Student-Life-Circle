# Actionable Tasks: 050 - GoEdu Design Reverse Engineering & Platform Adaptation

## Phase 1: Foundation & Data Architecture
- [x] T001: Create `frontend/src/data/goeduData.ts` with authentic GoEdu courses, bundle offerings, verified instructor profiles, and category metadata.
- [x] T002: Create unit tests for `goeduData.ts` in `frontend/src/data/__tests__/goeduData.test.mjs` verifying data integrity and filtering helpers.

## Phase 2: Navigation & Hero Section Components
- [x] T003: Implement `frontend/src/components/goedu/GoEduNavbar.tsx` featuring floating pill header, segmented nav links, search trigger, sliding cart drawer, profile button, dark mode toggle, and mobile drawer.
- [x] T004: Implement `frontend/src/components/goedu/GoEduHero.tsx` featuring warm sunshine hero `#FFF6DD`, radial golden sunburst, giant typographic watermark, pulsating pill badge, H1, subheadline, and pill search bar with "Let AI Recommend" button.

## Phase 3: Social Proof, Bundles & Course Grid
- [x] T005: Implement `frontend/src/components/goedu/GoEduTrustProof.tsx` with Google 5-star, Trustpilot verified 5-star `#00B67A`, and Facebook 100% recommended `#0066F5` review cards.
- [x] T006: Implement `frontend/src/components/goedu/GoEduBundleSpotlight.tsx` (`rounded-[2.5rem]` featured accelerator bundle with badges, curriculum highlights, and direct enrollment CTA).
- [x] T007: Implement `frontend/src/components/goedu/GoEduCourseGrid.tsx` with category filter pills, interactive course cards with thumbnail, level tag, duration, lessons, instructor details, ratings, and price.

## Phase 4: Trust Factors, Instructors, AI Banner & Footer
- [x] T008: Implement `frontend/src/components/goedu/GoEduInstructors.tsx` with instructor cards, photo, credential badges, and course count.
- [x] T009: Implement `frontend/src/components/goedu/GoEduTrustFactors.tsx` with 4-pillar trust grid explaining GEAC-Accredited syllabus, Socratic AI Solver, Lifetime Access, and Recognized Certificates.
- [x] T010: Implement `frontend/src/components/goedu/GoEduAIBanner.tsx` with interactive AI guidance banner connecting students to Socratic AI Tutor.
- [x] T011: Implement `frontend/src/components/goedu/GoEduFooter.tsx` with GoEdu-styled footer with accreditation note, links by category, newsletter, social links, and copyright.

## Phase 5: Page Assembly, Routing & Verification
- [x] T012: Upgrade `frontend/src/pages/index.tsx` to adopt the complete GoEdu design system layout.
- [x] T013: Create `frontend/src/pages/courses.tsx` providing a dedicated GoEdu courses catalog view.
- [x] T014: Run test suite, type-check, production build, and zero-emoji compliance audit.
