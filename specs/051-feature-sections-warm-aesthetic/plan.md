# Technical Architecture Plan: Feature Sections Warm Aesthetic

## 1. Architectural Strategy
- Layer: Visual UI Design, Theming, Component Layout, Design System Tokens.
- Approach: Non-destructive styling elevation using Tailwind utility tokens, CSS variables, and consistent warm color palettes.
- Target Components & Files:
  1. `frontend/src/pages/index.tsx`: Main educational portal containing all 10 feature sections.
  2. `frontend/src/components/home/CompetitorComparisonPillars.tsx`: 4-in-1 platform comparison.
  3. `frontend/src/components/home/SubjectExplorerCarousel.tsx`: Touch-friendly Swiper carousel with KaTeX formula previews.
  4. `frontend/src/components/home/StudentStoriesCarousel.tsx`: Swiper testimonial carousel.
  5. `frontend/src/pages/board-archives.tsx`: 10-year NCTB board questions archive.
  6. `frontend/src/pages/live-challenge.tsx`: Live Olympiad arena & real-time leaderboard.
  7. `frontend/src/pages/tuition.tsx`: 0% commission tuition marketplace.

## 2. Design Token System & Palette Mapping
- Backgrounds:
  - Surface Main: `bg-[#FFFCF6] dark:bg-[#0B0F19]`
  - Surface Tint Warm: `bg-[#FFF9EB]/60 dark:bg-[#0E1526]`
  - Surface Sunshine Glow: `bg-[#FFF6DD] dark:bg-[#121B2D]`
  - Card Ivory: `bg-white dark:bg-[#121B2D]`
- Borders & Dividers:
  - Card Hairline: `border border-amber-200/70 dark:border-[#262D3D]`
  - Hover State: `hover:border-[#ED8E22]/60 dark:hover:border-amber-500/40`
  - Subtle Divider: `border-b border-amber-200/60 dark:border-gray-800`
- Accents:
  - Primary CTA & Focus: `#ED8E22` (Warm Amber), hover `#D47C1A`
  - Secondary Badges: `bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border-amber-200/80`
  - Pulse Indicators: `bg-[#ED8E22]`
- Shadows:
  - Card Soft: `shadow-[0_4px_20px_-4px_rgba(237,142,34,0.08)]`

## 3. Security & Quality Guardrails
- Verification gates:
  - Strix SAST check & counterevidence validation.
  - Zero-emoji scan.
  - Strict TypeScript check (`tsc --noEmit`).
  - Unit test verification (`node --test`).
  - Next.js production build (`npm run build`).
  - Health check curl against `http://localhost:3002/`.
