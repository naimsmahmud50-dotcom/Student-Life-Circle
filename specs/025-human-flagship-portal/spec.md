<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Flagship Human-Centric Institutional Portal & Client Showcase
FILE:      specs/025-human-flagship-portal/spec.md
PHASE:     Phase 121 / Feature 025 - Flagship Human-Centric Institutional Portal
PURPOSE:   Establishes formal requirements for separating the public enterprise landing
           page from protected student dashboards, implementing Swiss Minimalism,
           prestigious academic typography, and world-class client presentation.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Feature Specification: Flagship Human-Centric Institutional Portal & Client Showcase

## 1. Problem Statement & Context
The previous homepage (`frontend/src/pages/index.tsx`) suffered from a fundamental architectural category error: it placed a logged-in student's internal mock dashboard (with fake personal metrics like "68% progress ring", "7-day streak", "Tanzim Hasan certificate") directly on the public root URL (`/`).

When clients, institutional evaluators, school principals, or prospective students visited `http://localhost:3000`, they were confronted with a cluttered, confusing cockpit filled with fake student numbers rather than an inspiring, prestigious national education platform. This created cognitive overload, violated `/ui-ux-pro-max` Swiss Minimalism principles, and appeared disorganized and amateurish ("vanga riksai").

## 2. Goals & Non-Goals
### Goals:
1. **Clean Separation of Concerns**: Transform `frontend/src/pages/index.tsx` into a world-class, client-facing flagship landing page, while preserving the internal student dashboard cleanly at `frontend/src/pages/dashboard.tsx`.
2. **Human-Centric Design (`/ui-ux-pro-max`)**: Apply the **Feature-Rich Showcase Pattern** with **Minimalism & Swiss Style**: generous whitespace, clear visual hierarchy, calm editorial pacing, and zero visual clutter.
3. **National Authority & Value Proposition**: Clearly articulate what the platform offers to students, parents, schools, and enterprise partners across Bangladesh.
4. **Client & Stakeholder Trust**: Prominently showcase NCTB 2015-2025 Board question archives, 3D STEM labs, Socratic AI pedagogy, zero-surveillance proctoring, and verified payment rails (bKash, Nagad, SSLCommerz).
5. **Strict Zero-Emoji & WCAG 2.2 AAA**: 100% Lucide vector SVG icons, minimum 4.5:1 text contrast, touch targets >= 44px, and full keyboard navigation.

### Non-Goals:
- Do not remove or alter existing backend APIs or test suites.
- Do not discard the student dashboard; preserve it cleanly in `frontend/src/pages/dashboard.tsx`.

## 3. User Stories
- **US-01 (Client / Institutional Evaluator)**: As an institutional decision-maker or investor, I want to immediately understand the mission, curriculum alignment, and technological excellence of the platform, so that I have absolute confidence in adopting it.
- **US-02 (Prospective Student & Parent)**: As a student or parent, I want to explore the 4 educational pathways (SSC, HSC, Admission, Career) and preview the board archives, labs, and exam hall, so that I can see the tangible value before signing up.
- **US-03 (Authenticated Student)**: As an enrolled student, I want to navigate to `/dashboard` to view my personal progress, study streak, and daily quiz recommendations without cluttering the public portal.

## 4. Acceptance Criteria
- [ ] AC-01: `frontend/src/pages/index.tsx` renders a prestigious, spacious, client-ready landing page with zero mock student personal stats on the hero.
- [ ] AC-02: Hero section features authoritative Bengali typography ("বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক ডিজিটাল শিক্ষাজীবন"), clear value proposition, and dual high-contrast tactile CTAs.
- [ ] AC-03: National scale trust bar showcases 4 key verifiable pillars (10 years of NCTB board questions, 64 districts offline P2P, zero-video privacy guarantee, 1,390 automated tests).
- [ ] AC-04: Academic Pathways section presents clean, dignified cards for SSC (9-10), HSC (11-12), Admission Hub, and Career/Tuition.
- [ ] AC-05: Interactive Feature Showcase highlights NCTB Board Archives, Digital Exam Hall, 3D STEM Labs, Socratic AI Tutor, and Merit Scholarships with live interactive previews.
- [ ] AC-06: Institutional trust & payment bar highlights bKash, Nagad, SSLCommerz, and W3C verifiable credentials.
- [ ] AC-07: The personal student learning dashboard is preserved cleanly in `frontend/src/pages/dashboard.tsx`.
- [ ] AC-08: Zero-emoji compliance (0 emoji characters in code or copy), Developer Architecture Notes, and 100% Next.js build compilation.
