# Implementation Plan: 061-career-page-atmospheric-redesign

## 1. Architectural Strategy
The design architecture of the Career Hub is organized into discrete sectional containers, each equipped with:
- An atmospheric canvas container (`relative overflow-hidden rounded-3xl border ...`).
- A soft radial lighting aura (e.g. amber, emerald, indigo, oxford navy) set behind content with `pointer-events-none select-none z-0`.
- An ambient uppercase watermark (e.g., `CAREER`, `SECTORS`, `VACANCIES`, `PIPELINE`, `GAZETTE`, `VERIFIED`) scaled typographically to fill the width at low opacity.
- High-contrast typography with Bengali font styling (`font-bengali`) and Oxford Navy accents.
- Tactile interactive elements: 3D button press states (`shadow-[0_4px_0_0_...] active:translate-y-1 active:shadow-none`), frosted pill badges, and hover card elevation (`hover:-translate-y-0.5 hover:shadow-lg`).

## 2. Component Refactoring Breakdown
1. **`CareerSearchFilterBar.tsx`**:
   - Wrap in atmospheric ivory console with subtle amber/warm tint.
   - Refine search input with glowing amber focus ring.
   - Style filter pills with tactile active elevation.
   - Polish Hot Job and Govt Circular toggle badges.
2. **`CareerCategoryGrid.tsx`**:
   - Wrap in fresh emerald-sage atmospheric container with watermark `SECTORS` and emerald aura stop.
   - Elevate category cards with soft frosted backdrop, icon container glow, and smooth hover micro-lifts.
   - Support horizontal scroll/swiper gesture on mobile.
3. **`CareerJobBoard.tsx`**:
   - Wrap feed in dignified Oxford Navy & Ivory canvas with watermark `VACANCIES`.
   - Redesign job cards into high-craft cards with company monogram, salary highlight in emerald badge, hot job badges, and tactile apply button.
   - Modernize empty state with clean Lucide SVG icon and helpful reset CTA.
4. **`CareerATSApplicationPipeline.tsx`**:
   - Wrap in indigo-slate workspace container with watermark `PIPELINE`.
   - Elevate 5-stage stepper progress bar with illuminated step dots.
   - Elevate interview alert banner with animated live viva highlight.
5. **`GovtCircularsAndCareerGuide.tsx`**:
   - Official Circulars: Gazette seal cards with pay scale and deadline warning.
   - Salary Insights: Frosted table container with clean divider lines.
   - Career Preparation: Numbered roadmap cards.
   - FAQ: Elevated accordions with smooth chevron rotation.
6. **`frontend/src/pages/career.tsx` Tab 4**:
   - Elevate Sealed Cryptographic CV Snapshot card with digital ledger watermark `VERIFIED` and glowing SHA-256 capsule.
   - Elevate Evidence-Backed Skills grid with verified badges and demo links.

## 3. Verification Protocol
1. Static analysis: `npx tsc --noEmit` in `frontend/`.
2. Node unit tests: `node --test frontend/src/components/career/__tests__/careerElevation.test.mjs`.
3. Zero-Emoji Python audit across all modified career files.
4. Static build: `npm --prefix frontend run build:pages`.
5. Automated GitHub Pages deployment script: `bash scripts/deploy-gh-pages.sh`.
