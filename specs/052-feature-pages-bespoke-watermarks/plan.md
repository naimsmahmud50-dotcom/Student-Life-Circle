# Architecture & Implementation Plan: Bespoke Feature Background Designs

## Design Tokens & Atmospheric Palette

```
Canvas Base:        bg-[#FFFCF6] dark:bg-[#0B0F19]
Hero Sunshine:      bg-[#FFF6DD]/80 dark:bg-[#0D1527]
Sunburst Radial:    radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.45) 0%, rgba(243, 172, 8, 0.20) 45%, rgba(253, 215, 70, 0) 100%)
Watermark Text:     text-[18vw] md:text-[clamp(3.5rem,20vw,16rem)] font-black uppercase tracking-wider
Watermark Gradient: linear-gradient(to bottom, rgba(243, 172, 8, 0.28) 15%, rgba(253, 215, 70, 0.02) 100%)
Card Surfaces:      bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs
Active Accents:     #ED8E22 (primary amber), #0B5D3B (scholarly emerald), #1B2A4A (scholarly navy)
```

## Component Architecture

1. **`frontend/src/components/layout/PageHeader.tsx`:**
   - Add `watermarkText?: string`
   - Add `watermarkGradient?: string`
   - Add `showGlow?: boolean`
   - Update wrapper to warm sunshine/linen `bg-[#FFF6DD]/70 dark:bg-[#0E1726]` with bottom golden border `border-b border-amber-200/60 dark:border-[#262D3D]`.
   - Render the giant typographic watermark layer behind breadcrumbs and title.

2. **`frontend/src/pages/board-archives.tsx`:**
   - Pass `watermarkText="ARCHIVES"` to `PageHeader`.

3. **`frontend/src/pages/practice.tsx`:**
   - Pass `watermarkText="PRACTICE"` to `PageHeader`.
   - Update root background to `bg-[#FFFCF6] dark:bg-[#0B0F19]`.

4. **`frontend/src/pages/socratic/solver.tsx`:**
   - Wrap header in bespoke sunshine hero banner with watermark `SOCRATIC` and golden radial glow.
   - Update root background and cards to warm ivory with amber borders.

5. **`frontend/src/pages/live-challenge.tsx`:**
   - Add watermark `CHALLENGE` and golden stadium aura in hero area.

6. **`frontend/src/pages/tuition.tsx`:**
   - Add watermark `TUITION` and trusted scholar aura in the header section.

7. **`frontend/src/pages/career.tsx` & `CareerStatsHeader.tsx`:**
   - Add watermark `CAREER` and professional horizon aura.

8. **`frontend/src/pages/admission.tsx`:**
   - Add watermark `ADMISSION` and academic prestige golden aura.
