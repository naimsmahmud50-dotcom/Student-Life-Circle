/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      specs/045-live-mcq-competitive-elevation/tasks.md
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Ordered, actionable tasks for implementing Live MCQ's full 14-feature suite,
 *            interactive digital OMR sheet, notice board, and elevated academic design.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

# Phase 142 Tasks: Live MCQ Competitive Elevation & Full Design System

- [x] **Task 1: 14-Feature Interactive Examination Suite (`LiveMcqFeatureShowcase.tsx`)**
  - Implement full 14-feature showcase with category tabs (All, Live Exam & OMR, Smart Study, Analytics & Merit).
  - Include cards for Smart Search, Topic Guru, Digital OMR, Vocabulary Booster, Knowledge Conflict Vault (তথ্যকল্পদ্রুম), Central Solution, Central Results, Quiz Master, Dynamic Info Panel, Wrong & Unanswered, Central Archive, Offline Section, My Section, Multiplayer Battle.

- [x] **Task 2: Interactive Digital OMR Simulator (`InteractiveOmrSimulator.tsx`)**
  - Implement interactive OMR bubble sheet with 5 sample questions, tactile filling states, negative marking calculator (-0.25), and instant feedback.

- [x] **Task 3: Dynamic Academic Notice & Info Panel (`DynamicInfoNoticeBoard.tsx`)**
  - Implement real-time notice ticker with priority tags, timestamps, and syllabus notifications.

- [x] **Task 4: Complete Live MCQ Visual Design Language & Layout Elevation**
  - Implement `LiveMcqHeroSection.tsx` (Hero V2 cosmos aurora, floating track badges, platform ecosystem, 4 trust KPIs).
  - Implement `LiveCategoryTrackSelector.tsx` (cats section with BCS, Bank, HSC STEM, Admission, Olympiad, Primary).
  - Implement `LiveFreeDemoExamBox.tsx` (dxb diagnostic exam card with 20 questions, 15m, -0.25 penalty).
  - Implement `LiveHowItWorksPathway.tsx` (how section 4-step preparation roadmap 01-04).
  - Implement `LiveMentorAndHallOfFame.tsx` (mentorPanel & tm-section with BCS cadres, BUET/DU professors).
  - Implement `LiveMcqFaqAccordion.tsx` (faq section with interactive expandable answers).
  - Harmonize all sections in `live-challenge.tsx` with refined Oxford Navy and Paper Alabaster design tokens.
  - Maintain 100% backward compatibility with all existing test strings, IDs, and element contracts.

- [x] **Task 5: Python Unit Test Suite Updates**
  - Update `backend/tests/test_phase142_live_mcq_elevation.py` asserting all 14 features, OMR simulator mechanics, notice panel, zero emojis, and regression guards (12/12 tests PASS).

- [x] **Task 6: Verification, Rebuild & E2E Validation**
  - Run `npx tsc --noEmit` -> 0 errors.
  - Run `npm run build` and sync static assets to `.next/standalone`.
  - Start standalone Next.js server on port 3000.
  - Run `python3 backend/scripts/run_zero_emoji_sweep.py` -> 649 files scanned, 0 violations.
  - Run `python3 -m unittest discover -s backend/tests -p "test_*.py"` -> 1,598 / 1,598 PASS (100%).
  - Run `npx playwright test --project=chromium` -> 37 / 37 PASS (100%).
