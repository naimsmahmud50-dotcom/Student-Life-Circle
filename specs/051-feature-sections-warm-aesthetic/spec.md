# Functional Specification: System-Wide Warm Linen & Sunshine Aesthetic Elevation

## 1. Executive Summary
- Feature: Comprehensive aesthetic harmonization extending the GoEdu-inspired warm linen (`#FFFCF6`), sunshine canvas (`#FFF6DD`), radial golden glow, and tactile amber accents (`#ED8E22`) across every feature section and card surface.
- Target: Flagship homepage sections (Competitor Comparison, Academic Progress & Telemetry, Subject Explorer, 3D STEM Labs, Live Olympiad Arena & Socratic AI, W3C Cryptographic Proof-of-Skill, Student Stories Carousel, Trust Badges & Modules Directory) and key educational feature modules.
- Non-Goals: Zero removal or alteration of educational logic, KaTeX mathematics rendering, 3D physics/chemistry simulators, countdown timers, routing, or state machines.

## 2. User Stories
- User Story 1 (Visual Cohesion): As a student or educator exploring the portal, I want every feature section to share a warm, scholarly, and inviting aesthetic so that the entire learning experience feels cohesive, prestigious, and comfortable for long study sessions.
- User Story 2 (Feature Immersion): As an active learner inspecting Academic Progress, 3D Labs, or Live Olympiad Challenge, I want cards, badges, and progress indicators to feature subtle warm amber glows, tactile borders, and ivory surfaces rather than stark, cold grays.
- User Story 3 (Accessibility & Readability): As an exam candidate using both light and dark modes, I want WCAG 2.2 AAA contrast ratios with readable typography, clear focus states, and zero visual jank or cumulative layout shifts.

## 3. Aesthetic Specifications & Design System Tokens
- Page Canvas:
  - Light Mode: `#FFFCF6` (Warm Linen)
  - Dark Mode: `#0B0F19` (Deep Charcoal Slate)
- Hero & Highlight Bands:
  - Light Mode: `#FFF6DD` with radial golden sunburst `radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.70) 0%, rgba(243, 172, 8, 0.35) 45%, rgba(253, 215, 70, 0) 100%)`
  - Dark Mode: `#0E1526` with deep navy/amber radial glow
- Warm Card Surfaces:
  - Light Mode: Warm ivory `#FFFFFF` or `#FFFDF9` with hairline warm borders `border-amber-200/70` or `border-[#EFE9DC]`, soft amber hover glow `hover:border-[#ED8E22]/50 hover:shadow-md`
  - Dark Mode: `#121B2D` with borders `border-gray-800` or `border-amber-900/30`
- Badges & Accents:
  - Primary Accent: `#ED8E22` (Warm Tactile Amber)
  - Secondary Accents: `#0B5D3B` (Scholarly NCTB Emerald), `#1B2A4A` (Scholarly Navy), `#B8862B` (Golden Trophy Amber)
  - Pulsating Badges: `animate-pulse` with `#ED8E22` indicator dot
- Zero-Emoji Policy: 100% strict compliance. Zero emoji characters in code, comments, or UI.

## 4. Acceptance Criteria
- [ ] AC1: Section 1.5 (`CompetitorComparisonPillars`) adopts warm linen background `#FFFDF9`, warm ivory switcher tabs with amber active highlight, and warm-bordered comparison cards.
- [ ] AC2: Section 2 (`Academic Progress & Platform Trust`) replaces cold `#F5F2EB` with warm sunshine/linen `#FFF9EB`/60 and styles all 8 telemetry & trust cards with warm amber border accents.
- [ ] AC3: Section 3 (`Curated Journey Pathways` & `SubjectExplorerCarousel`) features warm ivory cards with amber hover borders and warm linen KaTeX preview boxes.
- [ ] AC4: Section 4 (`3D STEM Virtual Labs`) maintains 100% functioning interactive 3D simulations while presenting warm sunshine cards and amber tactile launch buttons.
- [ ] AC5: Section 5 (`Live Challenge & Socratic AI`) features an amber-glow synchronized countdown and warm ivory Socratic tutor banner.
- [ ] AC6: Section 6 (`W3C Certificate Showcase`) and Section 6.5 (`Student Stories Carousel`) adopt warm ivory cards with amber quotes and verified badges.
- [ ] AC7: Core feature hub pages (e.g. `/board-archives`, `/live-challenge`, `/tuition`) align with the warm linen `#FFFCF6` and amber `#ED8E22` visual design.
- [ ] AC8: Full TypeScript compilation passes with zero errors (`tsc --noEmit`).
- [ ] AC9: All unit tests (45/45) pass cleanly without regressions.
- [ ] AC10: Zero-emoji audit script confirms 0 emojis across all modified files.
- [ ] AC11: Production build (`npm run build`) finishes with exit code 0.
- [ ] AC12: Server on port 3002 responds with HTTP 200 OK.
