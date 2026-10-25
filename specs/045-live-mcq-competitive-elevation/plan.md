/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      specs/045-live-mcq-competitive-elevation/plan.md
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Technical implementation plan for integrating Live MCQ's full design language,
 *            14-feature suite, interactive digital OMR simulator, and notice panel into Ogrojatra.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

# Implementation Plan: Phase 142 — Live MCQ Full Design & Feature Elevation

## Technical Context & Architectural Choices
- **Design System & Aesthetics**: Pure academic editorial design using Oxford Navy (`#0A2540`, `#071D33`), Paper Ivory (`#FAFAF8`, `#F5F2EB`), subtle paper borders, and academic status accents (Burgundy `#991B1B` for negative marking, Amber `#D97706`, Emerald `#059669`). Zero neon gradients, zero generic icons, zero emojis.
- **14-Feature Interactive Examination Suite (`LiveMcqFeatureShowcase.tsx`)**:
  - Filterable by 4 categories: All, Live Exam & OMR, Smart Study & Revision, Analytics & Merit.
  - Implements cards for: Smart Search, Topic Guru, Digital OMR, Vocabulary & Formula Booster, Knowledge Conflict Vault (তথ্যকল্পদ্রুম), Central Job/Board Solution, Central Result & Percentiles, Custom Quiz Master, Dynamic Info Panel, Wrong & Unanswered Revision Deck, 10-Year Central Archive, Offline Downloaded Papers, My Section Dashboard, Multiplayer Live Battle.
- **Interactive Digital OMR Simulator (`InteractiveOmrSimulator.tsx`)**:
  - Hands-on interactive OMR sheet with realistic bubble filling, tactile touch states, negative marking calculator (-0.25), and instant score breakdown.
- **Dynamic Academic Notice & Info Panel (`DynamicInfoNoticeBoard.tsx`)**:
  - Real-time ticker of official NCTB notifications, exam dates, and Olympiad schedules.
- **Multi-Track Routine Matrix (`LiveExamRoutineMatrix.tsx`)**:
  - 5 academic tracks (HSC, SSC, Admission, Olympiad, BCS/Job), 3 timeframes (Today, Tomorrow, Archive), and textbook citations.
- **Subject Weightage Breakdown (`SubjectWeightageBreakdown.tsx`)**:
  - Proportional topic bars and 4 marking formula cards.
- **Exam Rules & Anti-Cheat Protocol Modal (`ExamRulesProtocolModal.tsx`)**:
  - Accessible modal explaining server timer sync, 3-strike tab-switch detection, negative marking, and offline resilience.

## Phases of Execution
1. **Phase 1: Component Development**
   - Create `frontend/src/components/live-challenge/LiveMcqFeatureShowcase.tsx`.
   - Create `frontend/src/components/live-challenge/InteractiveOmrSimulator.tsx`.
   - Create `frontend/src/components/live-challenge/DynamicInfoNoticeBoard.tsx`.
   - Ensure existing components (`LiveExamRoutineMatrix.tsx`, `SubjectWeightageBreakdown.tsx`, `ExamRulesProtocolModal.tsx`, `LiveExamAnalyticsCard.tsx`) integrate harmoniously with visual excellence.

2. **Phase 2: Page Integration (`live-challenge.tsx`)**
   - Integrate the new components into `frontend/src/pages/live-challenge.tsx` with a world-class academic layout rhythm.
   - Maintain 100% backward compatibility with all existing test strings, IDs, and element contracts.

3. **Phase 3: Python Unit Test Suite**
   - Update `backend/tests/test_phase142_live_mcq_elevation.py` asserting all 14 features, OMR simulator mechanics, notice panel, zero emojis, and regression guards.

4. **Phase 4: Full System Verification**
   - Run `npx tsc --noEmit`.
   - Run `npm run build` and sync static assets to standalone.
   - Run `python3 backend/scripts/run_zero_emoji_sweep.py`.
   - Run all 1,593+ backend unit tests.
   - Run all 37 Playwright E2E tests.
   - Verify server startup on port 3000.
