/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      specs/045-live-mcq-competitive-elevation/spec.md
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Defines requirements, user stories, and acceptance criteria for
 *            integrating Live MCQ's full design language and 14 core features into
 *            Ogrojatra's Live Challenge arena with world-class human craftsmanship.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

# SPECIFICATION: Phase 142 — Live MCQ Competitive Elevation & Full Design System

## 1. Executive Summary & Goal
The goal of **Phase 142** is to elevate Ogrojatra's Live Challenge platform (`/live-challenge`) beyond Bangladesh's leading exam-prep platforms (specifically `web.livemcq.com`), adopting their visual hierarchy, layout rhythms, and 14 signature features—while strictly eliminating all AI-vibe neon gradients, generic icons, and clutter. The result is an authentic, human-crafted academic examination hub utilizing Oxford Navy (`#0A2540`), Deep Ink (`#071D33`), Paper Ivory (`#FAFAF8`, `#F5F2EB`), Academic Amber (`#D97706`), Emerald (`#059669`), and Burgundy Crimson (`#991B1B`), paired with KaTeX mathematical typography, interactive digital OMR simulation, and millisecond-synchronized edge timers.

---

## 2. Developer Architecture Note
Every created or modified file must include the mandatory header:
```typescript
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      [File Path]
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   [Architectural Purpose]
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */
```

---

## 3. User Stories & Acceptance Criteria

### User Story 1 (P1): Multi-Track Daily Exam Routine Matrix
**As a** student preparing for HSC, SSC, Admission, or Olympiads,  
**I want** to browse today's live exams, tomorrow's scheduled topics with textbook syllabus citations, and past archived exams across multiple educational tracks,  
**So that** I can structure my daily revision according to a transparent academic schedule.

- **Scenario 1.1**: Student selects from 5 distinct tracks: HSC Science (এইচএসসি বিজ্ঞান), SSC Board (এসএসসি বোর্ড প্রস্তুতি), University Admission (বিশ্ববিদ্যালয় ভর্তি), STEM Olympiad (জাতীয় অলিম্পিয়াড), and BCS/Govt Job (বিসিএস ও চাকরি প্রস্তুতি).
- **Scenario 1.2**: For each exam card, the system displays the exact NCTB syllabus reference, total questions, exam duration in minutes, negative marking ratio (-0.25 in Burgundy Crimson `#991B1B`), and total enrolled candidate count.
- **Scenario 1.3**: Exams scheduled for today feature active status badges and direct CTA entry; tomorrow's exams feature preparation countdowns and topic previews; past exams feature result and merit-list access.

### User Story 2 (P1): Subject-Wise Question Weightage Breakdown
**As a** serious candidate taking high-stakes competitive examinations,  
**I want** to see an interactive pre-exam topic distribution and mark allocation breakdown,  
**So that** I understand the proportional weight of each chapter and pass mark requirements before starting.

- **Scenario 2.1**: The exam lobby presents an interactive breakdown bar indicating the percentage of questions allocated per chapter (e.g. গতিবিদ্যা 28%, কাজ-শক্তি 24%, মহাকর্ষ 20%, পদার্থের গাঠনিক ধর্ম 28%).
- **Scenario 2.2**: Displays mark formulas: Positive mark per question (+1.0), Negative marking penalty (-0.25 in Burgundy Crimson `#991B1B`), minimum qualifying pass mark (40%), and projected cut-off score.

### User Story 3 (P1): Examination Ethics & Anti-Cheat Protocol Modal
**As a** test administrator and student seeking a fair testing environment,  
**I want** unambiguous proctoring and exam ethics guidelines readily accessible before entering the test hall,  
**So that** academic integrity, anti-cheat tab-switching guards, and submission policies are clearly understood.

- **Scenario 3.1**: Clicking "পরীক্ষার নিয়মাবলী ও নিরাপত্তা" opens a modal explaining the server-authoritative timer, negative marking penalty formula, 3-strike tab-switching detection guard, offline sync buffer, and pseudonymous leaderboard privacy.
- **Scenario 3.2**: Modal conforms to WCAG 2.2 AAA keyboard navigation (Escape to close, Tab focus trapping) and touch target sizes (>= 44px).

### User Story 4 (P1): 14-Feature Interactive Examination Suite
**As a** student comparing Ogrojatra with Live MCQ,  
**I want** to explore all 14 elevated capabilities inspired by Live MCQ's flagship features (Smart Search, Topic Guru, Digital OMR, Vocabulary Booster, Knowledge Conflict Vault, Job & Board Solution, Central Result, Custom Quiz Master, Dynamic Info Panel, Wrong & Unanswered Revision Deck, 10-Year Central Archive, Offline Downloaded Papers, My Section Dashboard, Multiplayer Live Battle),  
**So that** I have a complete, cohesive, and superior exam-prep ecosystem without needing any paid subscriptions.

- **Scenario 4.1**: Renders an interactive 14-feature grid with categorical filter tabs: "সমস্ত ফিচার", "লাইভ পরীক্ষা ও ওএমআর", "স্মার্ট স্টাডি ও রিভিশন", and "অ্যানালিটিক্স ও মেধা তালিকা".
- **Scenario 4.2**: Each card displays a category badge, clear Bengali title, educational explanation, key highlight metric, and direct action trigger.

### User Story 5 (P1): Interactive Digital OMR Sheet Simulator
**As a** student practicing for official board exams and admissions,  
**I want** to test and experience the digital OMR bubble filling mode directly inside the Live Challenge lobby,  
**So that** I can practice filling bubbles under realistic exam conditions with tactile feedback and instant scoring.

- **Scenario 5.1**: Students can click round bubble options (A, B, C, D / ক, খ, গ, ঘ) for 5 interactive sample questions.
- **Scenario 5.2**: Bubbles fill with rich Oxford Navy ink, calculate real-time scores with negative marking (-0.25), and display instant evaluation.

### User Story 6 (P1): Dynamic Academic Notice & Info Panel
**As a** candidate staying updated with national schedules,  
**I want** a live academic notice board displaying real-time syllabus announcements, exam date changes, and NCTB updates,  
**So that** I never miss an important examination deadline.

- **Scenario 6.1**: Renders an academic notice ticker with priority tags ("জরুরি নোটিশ", "সিলেবাস আপডেট", "রেজাল্ট প্রকাশ") and timestamps.

### User Story 7 (P1): Strict Regression Safety & Zero-Emoji Enforcement
**As a** system engineer and auditor,  
**I want** all pre-existing tests (1,593 backend unit tests, 37 Playwright E2E tests, zero-emoji sweeps) to continue passing with 100% success,  
**So that** zero regressions occur across the platform.
