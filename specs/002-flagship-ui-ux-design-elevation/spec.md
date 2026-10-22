# Specification: Flagship UI/UX Design Elevation & Unified Experience

## Feature Directory
`specs/002-flagship-ui-ux-design-elevation`

## 1. Problem Statement
Across Phases 1 to 97, the platform built comprehensive backend services, psychometrics, AI streaming, virtual labs, cryptographic proof-of-skills, and 1,190 passing automated tests. However, the frontend pages (`index.tsx`, `learn.tsx`, `practice.tsx`, etc.) were developed as individual modular prototypes with fragmented headers, inconsistent layouts, missing global state providers, and wireframe-like aesthetics.

When an end user opens `localhost:3000`, the experience feels like an unfinished, patchwork product ("ভাঙা রিকশার মতো") rather than an elite, unified, world-class EdTech platform like 10 Minute School, Khan Academy, or Linear.

## 2. Goals & Non-Goals
### Goals:
- Transform the platform frontend into a visually stunning, cohesive, world-class educational hub.
- Unify all pages under a shared, responsive layout shell: global `I18nProvider`, sticky `Navbar` with `[BN | EN]` language toggle, persistent `SocraticTutorDrawer` floating assistant, and dignified footer.
- Overhaul the flagship Home Dashboard (`index.tsx`) with personalized academic telemetry (streak, accuracy, questions solved), quick-resume cards, 3D STEM labs launcher, live challenge countdown, and verified proof-of-skill certificate showcase.
- Ensure 100% WCAG 2.2 AAA contrast, sub-pixel Noto Sans Bengali typography, 48px touch targets, and strict Zero-Emoji policy with Lucide vector icons.
- Ensure all 97 phases of functionality are seamlessly accessible from the UI with zero broken links or dummy placeholders.

### Non-Goals:
- Rewriting backend API services or altering database schemas (all 1,190 backend tests must remain passing).
- Introducing decorative emojis or childish gamification animations.

---

## 3. User Stories & Priority Matrix

### [P1] Unified Application Shell & Global Providers
- **As a** student navigating between learning, practice, live challenge, and admission modules,
- **I want** a consistent header, navigation bar, language switcher, and floating Socratic AI tutor across every single page,
- **So that** I never experience abrupt layout shifts, broken navigation, or missing tools.

### [P1] Flagship Home Dashboard Overhaul (`index.tsx`)
- **As a** student landing on the home page,
- **I want** to see an inspiring, modern dashboard displaying my active study streak, recent curriculum progress, live challenge alerts, 3D STEM labs preview, and verified achievements,
- **So that** I immediately feel motivated and know the exact next step in my academic journey.

### [P2] Curriculum & Subject Explorer Elevation (`learn.tsx`)
- **As a** secondary or higher secondary student,
- **I want** an intuitive, visual subject catalog with progress rings, chapter breakdown, video lecture integration, and mistake revision queues,
- **So that** I can study systematically without cognitive overload.

### [P2] Anytime Practice & Exam Simulation Elevation (`practice.tsx`)
- **As an** admission candidate,
- **I want** a distraction-free, high-contrast quiz interface with KaTeX math rendering, timer, option selection, Socratic hint drawer, and instant explanation breakdown,
- **So that** my practice sessions simulate authentic exam conditions.

### [P3] Proof-of-Skill & Trust Integration
- **As an** ambitious student,
- **I want** my verified certificates, bKash/Nagad fee receipts, and skill cards to be proudly displayed and 1-click shareable to LinkedIn and Facebook,
- **So that** I can build my academic portfolio for university and career opportunities.

---

## 4. Visual Design System & UI Tokens
- **Theme Ground**: Slate `#F8FAFC` (Light) / Midnight Slate `#090D16` (Dark)
- **Primary Cards & Surfaces**: Clean White `#FFFFFF` (Light) / Deep Slate `#0F172A` (Dark)
- **Brand Primary**: Royal Blue `#2563EB` (Light) / Luminous Blue `#3B82F6` (Dark)
- **Mastery & Verified**: Emerald / Teal `#0D9488` (Light) / Bright Teal `#14B8A6` (Dark)
- **Alert & Streak**: Warm Amber `#D97706` (Light) / `#F59E0B` (Dark)
- **Typography**: `Noto Sans Bengali` for Bengali copy, `Inter` for numbers and Latin labels
- **Touch Ergonomics**: Minimum 48px touch targets, full keyboard accessibility, zero CLS.
