# Implementation Plan: Deep Pine Emerald Concentric Rings Institutional Footer

## 1. Technical Tokens & Vector Architecture

### Canvas Tokens
- **Root Background**: `bg-[#071F1A]` with `bg-gradient-to-b from-[#071F1A] via-[#0C2B24] to-[#051713]`
- **Horizon Line**: `h-[2px] bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-85`
- **Ambient Lighting**:
  - Left mint radiant glow: `radial-gradient(circle at 12% 25%, rgba(16, 185, 129, 0.35) 0%, rgba(13, 148, 136, 0.15) 45%, transparent 70%)`
  - Right emerald glow: `radial-gradient(circle at 85% 65%, rgba(5, 150, 105, 0.20) 0%, transparent 60%)`
- **Concentric Geometric Orbital Rings (SVG)**:
  Positioned `absolute right-[-100px] md:right-[-50px] top-[-50px] md:top-[-80px] w-[500px] md:w-[720px] h-[500px] md:h-[720px] pointer-events-none select-none z-0`:
  ```svg
  <svg viewBox="0 0 800 800" fill="none" className="w-full h-full" aria-hidden="true">
    <circle cx="450" cy="400" r="360" stroke="#059669" strokeWidth="48" opacity="0.18" />
    <circle cx="450" cy="400" r="260" stroke="#10B981" strokeWidth="36" opacity="0.25" />
    <circle cx="450" cy="400" r="170" stroke="#34D399" strokeWidth="24" opacity="0.20" />
    <circle cx="450" cy="400" r="90" stroke="#6EE7B7" strokeWidth="16" opacity="0.15" />
  </svg>
  ```
  Secondary subtle concentric arcs on left:
  ```svg
  <svg viewBox="0 0 400 400" fill="none" className="w-full h-full" aria-hidden="true">
    <circle cx="50" cy="350" r="220" stroke="#0D9488" strokeWidth="32" opacity="0.15" />
    <circle cx="50" cy="350" r="140" stroke="#14B8A6" strokeWidth="20" opacity="0.18" />
  </svg>
  ```

### Components Elevation
1. **Tier 1 (Accreditation Bar)**:
   - Ribbon: `bg-[#0A241E]/90 backdrop-blur-md border-b border-emerald-900/60`
   - NCTB 2026 Pill: `bg-emerald-500/15 border border-emerald-400/40 text-emerald-300`
   - Compliance Chips: `bg-[#071A15]/80 border border-emerald-900/60 text-emerald-100/90`
2. **Tier 2 (5-Column Editorial Grid)**:
   - Column 1: Frosted emerald glass card `p-6 rounded-2xl bg-[#0C2D25]/85 border border-emerald-600/30 shadow-2xl backdrop-blur-md`
   - Columns 2-5: Headings `text-emerald-200`, links `text-emerald-100/75 hover:text-white hover:translate-x-1` with interactive amber bullets
   - Tactical Hotline Chips: 16xxx, 1098, 999 with high-contrast text
3. **Tier 3 (Verified Payment Rails)**:
   - Platform: `p-6 rounded-2xl bg-[#0C2D25]/85 border border-emerald-600/35 shadow-2xl backdrop-blur-md`
   - Official SVG badges for bKash, Nagad, SSLCommerz
4. **Tier 4 (Copyright Bar)**:
   - Divider: `border-t border-emerald-900/60 pt-8`
   - WCAG 2.2 AAA live pulse indicator and dark glass policy chips
5. **Cross-Route Alignment**:
   - Apply matching Pine Emerald + Concentric Rings aesthetic to `GoEduFooter.tsx`

## 2. Verification Protocol
1. TypeScript compiler check (`./frontend/node_modules/.bin/tsc --project frontend/tsconfig.json --noEmit`).
2. Automated test suite (`node --experimental-strip-types --test frontend/src/data/__tests__/goeduData.test.mjs frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs`).
3. Python zero-emoji audit.
4. Production build (`npm --prefix frontend run build`).
5. Live curl verification on port 3002.
