# Implementation Plan: Dignified Oxford Midnight Institutional Footer

## 1. Technical Architecture & Component Structure

### Color Palette Tokens (Oxford Midnight)
- **Base Canvas**: `bg-[#060D1A]` with deep gradient overlay `bg-gradient-to-b from-[#081224] via-[#060D1A] to-[#040812]`
- **Horizon Transition**: Top edge featuring a dual-tone glowing line:
  `<div className="w-full h-[2px] bg-gradient-to-r from-transparent via-[#ED8E22] to-transparent opacity-80" />`
- **Celestial Dot Matrix**:
  `background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px); background-size: 32px 32px;`
- **Aurora Glow**:
  `radial-gradient(ellipse 70% 45% at 50% 0%, rgba(30, 58, 138, 0.32) 0%, transparent 100%)`
  and bottom warm ember:
  `radial-gradient(ellipse 50% 25% at 50% 100%, rgba(237, 142, 34, 0.10) 0%, transparent 100%)`
- **Architectural Watermark**:
  Subtle architectural outline text `NATIONAL REPOSITORY` or `STUDENT LIFE CIRCLE` in `text-white/[0.025]`, `pointer-events-none select-none z-0`.

### Component Plan for `Footer.tsx`
1. **Horizon Line**: Amber glowing gradient hairline at top.
2. **Tier 1 (Accreditation Bar)**:
   - Container: `bg-[#0A1628]/95 border-b border-slate-800/80 px-4 sm:px-6 lg:px-8 py-3.5`
   - NCTB 2026 Pill: `bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-semibold`
   - ISO 27001, OWASP, WCAG pills: `bg-slate-900/80 border border-slate-800 text-slate-300 shadow-sm`
3. **Tier 2 (Editorial Navigation)**:
   - Column 1 (Brand & Mission): Dark glass frosted container `bg-[#0D1D35]/80 border border-slate-700/60 shadow-xl backdrop-blur-md p-6 rounded-2xl space-y-4`
   - Column 2-5: Headings in `text-xs font-bold uppercase tracking-wider text-white font-sans`, link items in `text-slate-400 hover:text-white transition-all flex items-center gap-2 py-1.5 group`, with interactive bullet `group-hover:bg-[#ED8E22] group-hover:scale-125`.
   - Contact Helpdesk: Tactical dark glass chips for hotline numbers with high contrast.
4. **Tier 3 (Verified Payment Rails)**:
   - Wide frosted dark glass platform: `bg-[#0D1D35]/90 border border-slate-700/70 shadow-xl backdrop-blur-md p-6 rounded-2xl`
   - Verified badges for bKash, Nagad, SSLCommerz with crisp high-contrast styling and glowing border hover states.
5. **Tier 4 (Copyright Bar)**:
   - Subtle border divider `border-t border-slate-800/90 pt-6`
   - WCAG 2.2 AAA badge with live pulse indicator and dark glass policy chips.

### Component Plan for `GoEduFooter.tsx`
- Refactor to match the Oxford Midnight canvas, celestial dot matrix, and dark glass styling for unified cross-route elegance.

## 2. Verification Protocol
1. TypeScript check with `./frontend/node_modules/.bin/tsc --project frontend/tsconfig.json --noEmit`.
2. Automated test suite execution (`node --experimental-strip-types --test frontend/src/data/__tests__/goeduData.test.mjs frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs`).
3. Python zero-emoji audit across all updated files.
4. Full production build (`npm --prefix frontend run build`).
5. Live curl verification on port 3002.
