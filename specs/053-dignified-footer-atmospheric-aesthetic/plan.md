# Implementation Plan: Dignified Global Footer Atmospheric Aesthetic & Watermark

## 1. Design Architecture & Token Mapping

### Palette & Atmospheric Tokens
- **Root Background**: `bg-[#FFF6DD]/95 dark:bg-[#070C18]` with top border `border-t border-amber-200/80 dark:border-[#262D3D]`.
- **Dot Matrix Grid Layer**:
  - `background-image: radial-gradient(rgba(243, 172, 8, 0.14) 1px, transparent 1px)`
  - `background-size: 24px 24px`
- **Radial Sunburst Aura**:
  - Rising upward from bottom center:
    `radial-gradient(ellipse 75% 85% at 50% 100%, rgba(255, 178, 0, 0.38) 0%, rgba(243, 172, 8, 0.15) 50%, rgba(253, 215, 70, 0) 100%)`
- **Giant Typographic Watermark**:
  - Text: `OGROJATRA`
  - Typography: `font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(4rem,22vw,16rem)] uppercase tracking-wider select-none opacity-85`
  - Gradient: `linear-gradient(to bottom, rgba(243, 172, 8, 0.22) 15%, rgba(253, 215, 70, 0.02) 100%)`
  - Placement: Absolute at bottom or centered, `pointer-events-none select-none z-0`, `aria-hidden="true"`.

### Component Structural Plan
1. **Tier 1 (Accreditation Ribbon)**:
   - Wrapper: `bg-[#FFF1C2]/90 dark:bg-[#0B132B]/90 backdrop-blur-md border-b border-amber-200/70 dark:border-amber-900/40`
   - NCTB Badge: `bg-emerald-50/80 dark:bg-emerald-950/60 border border-emerald-300/60 dark:border-emerald-700/60 text-[#065F46] dark:text-emerald-300`
   - Compliance Pills: `bg-white/70 dark:bg-[#121B2D]/70 border border-amber-200/60 dark:border-slate-800`
2. **Tier 2 (5-Column Editorial Navigation)**:
   - Outer wrapper with `relative z-10`.
   - Column 1: Encased in a warm ivory frosted card `p-5 rounded-2xl bg-white/80 dark:bg-[#121B2D]/80 border border-amber-200/70 dark:border-[#262D3D] shadow-xs`.
   - Column headers: Enhanced with crisp typography, subtle amber bottom accent indicator.
   - Interactive Links: Hover color `#ED8E22`, micro-indicators with amber hover states.
   - Contact hotline numbers: Color-coded tactile badges for `16xxx` (Oxford Navy), `1098` (Emerald), `999` (Amber).
3. **Tier 3 (Verified Payment Rails & Escrow Trust)**:
   - Dedicated frosted shelf: `p-5 rounded-2xl bg-white/85 dark:bg-[#121B2D]/85 border border-amber-200/80 dark:border-[#262D3D] shadow-xs backdrop-blur-xs flex flex-col md:flex-row items-center justify-between gap-6`.
   - High-definition official SVG merchant badges for bKash, Nagad, and SSLCommerz.
4. **Tier 4 (Copyright & Safety)**:
   - Hairline warm amber divider `border-t border-amber-200/70 dark:border-[#262D3D] pt-6`.
   - WCAG 2.2 AAA live pulse indicator, zero-emoji policy, and language indicators.
5. **GoEduFooter Alignment**:
   - `frontend/src/components/goedu/GoEduFooter.tsx`: Upgrade root to warm sunshine canvas, sunburst aura, and watermark `OGROJATRA EDU`.

## 2. Verification Protocol
1. TypeScript compilation check (`./frontend/node_modules/.bin/tsc --project frontend/tsconfig.json --noEmit`).
2. Automated test suite execution (`node --experimental-strip-types --test frontend/src/data/__tests__/goeduData.test.mjs frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs`).
3. Python zero-emoji check across modified footer files.
4. Full production build verification (`npm --prefix frontend run build`).
5. Live curl test on port 3002 across all routes.
