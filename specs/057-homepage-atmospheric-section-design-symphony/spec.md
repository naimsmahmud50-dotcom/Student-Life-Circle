# Feature Specification: 057 - Homepage Atmospheric Section Design Symphony

## 1. Executive Summary & Objective
Following the user's praise for the initial Editorial Hero section's visual depth, this feature systematically elevates every single section (para) across the Ogrojatra flagship homepage (`frontend/src/pages/index.tsx` and child components). 

Every section adopts the atmospheric design language pioneered in Section 1 (bespoke ambient radial gradients, contextual typographic watermarks, frosted glass card depth, high-contrast typography, and tactile interaction) while deliberately avoiding visual monotony ("same same korba na"). Each section is given a distinct, complementary chromatic personality that flows seamlessly into the next, creating an educational color symphony.

---

## 2. Atmospheric Design Architecture (Inherited from Hero DNA)
Every homepage section must feature:
1. **Themed Atmospheric Radial Glow**: Positioned thoughtfully (bottom-center, top-center, or dual corners) to add dimensionality without compromising WCAG 2.2 AAA readability.
2. **Contextual Typographic Watermark**: Giant background headline (`text-[18vw]` to `text-[24vw]`) with subtle `linear-gradient` clip and low opacity (`0.03`–`0.07`), displaying the chapter's conceptual domain (e.g., `PROGRESS`, `PATHWAYS`, `LABORATORY`, `OLYMPIAD`, `CREDENTIAL`, `STORIES`, `MODULES`).
3. **Harmonic Chromatic Progression (Color Symphony)**:
   - **Section 1 (Hero)**: Warm Amber & Golden Sunburst (`ogrojatra`)
   - **Section 1.5 (Pillars)**: Royal Cobalt & Electric Amber (`CAMPUS`)
   - **Section 2 (Progress & Telemetry)**: Midnight Navy & Sapphire-Cyan Glow (`PROGRESS`)
   - **Section 3 (Pathways)**: Deep Scholar Emerald & Mint Glow (`PATHWAYS`)
   - **Section 4 (3D STEM Labs)**: Cosmic Violet & Ultraviolet Glow (`LABORATORY`)
   - **Section 5 (Live Challenge & Solver)**: Fiery Crimson & Golden Arena Glow (`OLYMPIAD`)
   - **Section 6 (W3C Certificates)**: Lapis Lazuli & Gold Crest Vault (`CREDENTIAL`)
   - **Section 6.5 (Student Stories)**: Warm Terracotta & Sunset Glow (`STORIES`)
   - **Section 7 (Trust & Modules)**: Deep Marine Teal & Mint Assurance (`MODULES`)
   - **Section 8 (Closing CTA)**: Deep Charcoal Slate & Golden Horizon (`EXCELLENCE`)
   - **Footer**: Harmonious Warm Slate & Celestial Orbital Hairlines
4. **Frosted Translucent Surfaces**: Glassmorphic cards with subtle hairline borders (`border-amber-200/60 dark:border-slate-700/60`), elevated shadows, and responsive tactile transitions.
5. **Zero-Emoji Policy**: Pure Lucide SVG icons only.

---

## 3. User Stories

### US-001: Chromatic Harmony Across All Sections
**As a** learner exploring the homepage,  
**I want** each section to have its own unique, beautiful atmospheric lighting and background watermark while feeling part of a cohesive journey,  
**So that** browsing the platform feels inspiring, diverse, and prestigious rather than repetitive or monotonous.

### US-002: Immersive 3D Labs & Live Challenge Visual Elevation
**As a** student interested in STEM simulations or national olympiads,  
**I want** Section 4 and Section 5 to evoke high-tech laboratory and stadium arenas through specialized ultraviolet and fiery crimson glowing atmospherics,  
**So that** I feel compelled to launch simulations and participate in live challenges.

### US-003: Cryptographic Proof & Trust Dimensionality
**As a** recruiter or guardian assessing student credentials,  
**I want** Sections 6 and 7 to radiate institutional security through deep lapis and marine teal tones with subtle watermark branding,  
**So that** verified certificates and national payment trust badges convey ultimate credibility.
