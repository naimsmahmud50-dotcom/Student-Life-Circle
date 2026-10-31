# Feature Specification: 064-practice-arena-atmospheric-redesign

## 1. Problem Statement & User Request
The user uploaded a screenshot of the Practice Hub page (`frontend/src/pages/practice.tsx`, URL: `/practice`), noting:
> "prothom page a dekho akta design ache but nicher pera gulate kno design nai tmr akhn kaj tmr joto designing skill ache sob gula designing skill kaje lagiye uporer para design copy na kore dhara thik rekhe sundor akta design kore dew /design /ui-styling /ui-ux-pro-max agula kaje llagaw amon joto designing skill ache sob skill kaje lagaw do it your best version onno kno code a jhaemla korba na karon tmk tmr path diye dewya hoiche sei path ai design korba /speckit"

### Core Deficiencies in Existing Lower Sections:
1. Below the rich `PageHeader`, the Question Status Counter and Question Card are plain, minimalist boxes lacking atmospheric visual depth, glow, or typographic hierarchy.
2. No interactive Question Palette/Navigator: Students have no quick visual overview of all 10 questions (which are answered, pending, or active).
3. No academic reference tools: No formula quick-sheet for the active physics chapters.
4. No methodology/protocol explanation: Lacks clarity on scoring rules, offline buffering, and idempotency guarantees.
5. No strategic guidance or FAQ accordions addressing exam time management and equation memorization.
6. The completion view lacks high-impact celebratory visualization and detailed answer review.

---

## 2. Goals & Non-Goals
### Goals:
- Transform the lower sections of `frontend/src/pages/practice.tsx` to match the flagship atmospheric caliber and chromatic harmony of `PageHeader`.
- Introduce an interactive 10-Question Navigator Palette with real-time answered/pending state indicators and 1-click jump functionality (`jumpToQuestion`).
- Elevate the Core Question Arena with atmospheric glow, watermark (`ARENA`), chapter tags, difficulty pill, KaTeX math rendering, and keyboard shortcuts guide.
- Add a Formula Reference Sheet container (`FORMULAS`) covering Newtonian mechanics, gravitation, simple harmonic motion, and thermodynamics.
- Add an Examination Protocol & Marking Criteria container (`PROTOCOL`).
- Add a Board Strategy & Practice FAQ accordion container (`STRATEGY`).
- Elevate the Exam Completion View (`MASTERY`) with metric cards and full answer review capability.
- Strictly maintain Zero-Emoji compliance (pure Lucide SVG icons only).
- Strictly isolate all changes to `frontend/src/pages/practice.tsx` and specification files.

### Non-Goals:
- Modifying any global state models, backend endpoints, or unrelated pages.
- Modifying `useQuizStore.ts` or `option-card.tsx` (all existing APIs and props are leveraged directly).

---

## 3. User Stories
- **P1 - Interactive Question Palette:** As a student taking a timed practice set, I want a 10-question visual matrix so that I can see my progress, know which questions are answered, and jump between questions instantly.
- **P2 - Atmospheric Question Arena:** As a candidate preparing for board and olympiad exams, I want a beautifully styled question card with clear math rendering, keyboard shortcuts, and tactile action buttons so that practice feels immersive and focused.
- **P3 - Formula Reference Companion:** As a student solving physics numericals, I want a quick-reference formula sheet on the same page so that I can review key equations during practice.
- **P4 - Strategy & Protocol Guidance:** As an examinee, I want clear instructions on scoring, offline auto-sync, and board MCQ answering techniques.
- **P5 - Detailed Result Mastery Review:** When I submit my script, I want to see my score, accuracy, national percentile, and question-by-question breakdown.
