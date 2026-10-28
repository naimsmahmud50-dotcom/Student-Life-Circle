# Technical Plan: Live Challenge Full-Page Atmospheric Symphony

- **Feature Directory:** `specs/059-live-challenge-full-page-atmospheric-symphony`
- **Core Architecture:**
  - Elevate each section on `frontend/src/pages/live-challenge.tsx` to be a full-bleed edge-to-edge section with its own distinct chromatic atmospheric canvas, radial aura, typographic watermark, and frosted glass cards.
  - Refine individual components where needed for high-contrast dark-mode typography and glass borders.

---

## 1. Full-Bleed Section Container Template

Each section wrapper follows this proven architectural formula:
```tsx
<section className="relative overflow-hidden w-full bg-[CANVAS_COLOR] border-b border-[BORDER_COLOR] py-14 sm:py-20 transition-colors">
  {/* Luminous Ambient Radial Aura */}
  <div
    className="absolute inset-0 pointer-events-none select-none z-0"
    style={{
      background: 'radial-gradient(ellipse 70% 60% at 50% 50%, [COLOR_STOP_1] 0%, [COLOR_STOP_2] 45%, transparent 75%)'
    }}
    aria-hidden="true"
  />

  {/* Giant Typographic Watermark */}
  <div
    className="absolute z-0 pointer-events-none select-none w-full top-4 left-0 flex justify-center overflow-hidden"
    aria-hidden="true"
  >
    <p className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(4rem,20vw,16rem)] uppercase tracking-wider select-none opacity-20 [GRADIENT_STYLE]">
      [WATERMARK_TEXT]
    </p>
  </div>

  {/* Content Container */}
  <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ChildComponent />
  </div>
</section>
```

---

## 2. Section Token Mapping

1. **Section 2 (`LiveCategoryTrackSelector`):**
   - Canvas: `bg-[#07132B]`
   - Border: `border-sky-900/40`
   - Radial Glow: `rgba(14, 165, 233, 0.16) 0%, rgba(37, 99, 235, 0.08) 50%`
   - Watermark: `TRACKS`
2. **Section 3 (`DynamicInfoNoticeBoard`):**
   - Canvas: `bg-[#130B14]`
   - Border: `border-rose-950/50`
   - Radial Glow: `rgba(225, 29, 72, 0.16) 0%, rgba(244, 63, 94, 0.08) 50%`
   - Watermark: `BULLETIN`
3. **Section 4 (`LiveFreeDemoExamBox`):**
   - Canvas: `bg-[#0A1628]`
   - Border: `border-cyan-900/40`
   - Radial Glow: `rgba(6, 182, 212, 0.16) 0%, rgba(59, 130, 246, 0.08) 50%`
   - Watermark: `DEMO EXAM`
4. **Section 5 (`LiveHowItWorksPathway`):**
   - Canvas: `bg-[#061815]`
   - Border: `border-emerald-950/50`
   - Radial Glow: `rgba(16, 185, 129, 0.16) 0%, rgba(5, 150, 105, 0.08) 50%`
   - Watermark: `PATHWAY`
5. **Section 6 (`SubjectWeightageBreakdown`):**
   - Canvas: `bg-[#0F0B24]`
   - Border: `border-purple-950/50`
   - Radial Glow: `rgba(168, 85, 247, 0.16) 0%, rgba(139, 92, 246, 0.08) 50%`
   - Watermark: `WEIGHTAGE`
6. **Section 7 (`InteractiveOmrSimulator`):**
   - Canvas: `bg-[#0B152A]`
   - Border: `border-indigo-950/50`
   - Radial Glow: `rgba(99, 102, 241, 0.16) 0%, rgba(245, 158, 11, 0.08) 50%`
   - Watermark: `OMR SHEET`
7. **Section 8 (Leaderboard & Sidebar Cards):**
   - Canvas: `bg-[#14120C]`
   - Border: `border-amber-950/50`
   - Radial Glow: `rgba(245, 158, 11, 0.18) 0%, rgba(234, 88, 12, 0.08) 50%`
   - Watermark: `LEADERBOARD`
8. **Section 9 (`LiveExamRoutineMatrix`):**
   - Canvas: `bg-[#08181A]`
   - Border: `border-teal-950/50`
   - Radial Glow: `rgba(20, 184, 166, 0.16) 0%, rgba(14, 165, 233, 0.08) 50%`
   - Watermark: `ROUTINE`
9. **Section 10 (`LiveMcqFeatureShowcase`):**
   - Canvas: `bg-[#130A20]`
   - Border: `border-fuchsia-950/50`
   - Radial Glow: `rgba(217, 70, 239, 0.15) 0%, rgba(147, 51, 234, 0.08) 50%`
   - Watermark: `FEATURES`
10. **Section 11 (`LiveMentorAndHallOfFame`):**
    - Canvas: `bg-[#18110D]`
    - Border: `border-orange-950/50`
    - Radial Glow: `rgba(249, 115, 22, 0.16) 0%, rgba(217, 119, 6, 0.08) 50%`
    - Watermark: `MENTORS`
11. **Section 12 (`LiveMcqFaqAccordion`):**
    - Canvas: `bg-[#0D111A]`
    - Border: `border-slate-800/60`
    - Radial Glow: `rgba(100, 116, 139, 0.18) 0%, rgba(56, 189, 248, 0.08) 50%`
    - Watermark: `QUESTIONS`

---

## 3. Verification & Compliance
- Zero Emoji checks.
- TypeScript compilation verification (`tsc --noEmit`).
- Automated test suites (45/45).
- Port 3002 testing.
