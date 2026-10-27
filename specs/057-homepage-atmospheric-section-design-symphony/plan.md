# Technical Architecture Plan: 057 - Homepage Atmospheric Section Design Symphony

## 1. Scope & Implementation Strategy
To implement the atmospheric design language across all sections without duplicating code or creating visual clutter:
- Enhance each section in `frontend/src/pages/index.tsx` and child components (`CompetitorComparisonPillars.tsx`) with:
  1. An absolute, pointer-events-none, z-0 ambient radial gradient division tailored to that section's chromatic theme.
  2. An absolute, pointer-events-none, z-0 contextual typographic watermark division styled consistently with Hero's watermark (`select-none font-black uppercase tracking-wider`).
  3. Tailored card background washes, subtle border hairline adjustments, and chip accents that match the section's color story.
  4. Ensure dark mode transitions (`dark:bg-...`, `dark:border-...`) and light mode warmth (`bg-[#FFFCF6]`, `bg-[#FFF9EB]`, etc.) remain fully responsive and contrast-safe.

---

## 2. Section Component Breakdown & Gradient Matrix

| Section | Domain / Title | Chromatic Theme | Watermark | Radial Ambient Glow Spec |
|---|---|---|---|---|
| **Sec 1.5** | Competitor Pillars | Royal Cobalt & Amber | `CAMPUS` | `radial-gradient(ellipse 70% 65% at 50% 50%, rgba(37,99,235,0.18) 0%, rgba(237,142,34,0.10) 50%, transparent 80%)` |
| **Sec 2** | Learning Telemetry | Midnight Navy & Sapphire | `PROGRESS` | `radial-gradient(ellipse 65% 75% at 50% 100%, rgba(14,165,233,0.16) 0%, rgba(37,99,235,0.08) 50%, transparent 85%)` |
| **Sec 3** | Journey Pathways | Scholar Emerald & Mint | `PATHWAYS` | `radial-gradient(ellipse 65% 80% at 50% 0%, rgba(16,185,129,0.18) 0%, rgba(5,150,105,0.08) 50%, transparent 80%)` |
| **Sec 4** | 3D STEM Labs | Cosmic Violet & Electric Sky | `LABORATORY` | `radial-gradient(ellipse 60% 85% at 50% 100%, rgba(168,85,247,0.20) 0%, rgba(126,34,206,0.10) 45%, transparent 80%)` |
| **Sec 5** | Live Challenge & Solver | Fiery Crimson & Golden Arena | `OLYMPIAD` | `radial-gradient(ellipse 65% 75% at 50% 0%, rgba(244,63,94,0.18) 0%, rgba(245,158,11,0.12) 50%, transparent 85%)` |
| **Sec 6** | W3C Proof of Skill | Lapis Lazuli & Gold Crest | `CREDENTIAL` | `radial-gradient(ellipse 70% 70% at 50% 100%, rgba(99,102,241,0.18) 0%, rgba(212,163,75,0.10) 50%, transparent 80%)` |
| **Sec 6.5** | Student Stories | Warm Terracotta & Sunset | `STORIES` | `radial-gradient(ellipse 65% 65% at 50% 50%, rgba(251,146,60,0.15) 0%, transparent 75%)` |
| **Sec 7** | Trust & Modules | Deep Marine Teal & Oceanic | `MODULES` | `radial-gradient(ellipse 70% 60% at 50% 0%, rgba(20,184,166,0.18) 0%, transparent 80%)` |
| **Sec 8** | Closing CTA | Deep Obsidian & Golden Sunburst | `EXCELLENCE` | `radial-gradient(ellipse 65% 85% at 50% 100%, rgba(255,178,0,0.30) 0%, rgba(243,172,8,0.15) 50%, transparent 100%)` |

---

## 3. Verification Protocol
1. TypeScript check (`tsc --noEmit`).
2. Automated test suite (45/45 tests passing).
3. Zero-Emoji audit across all modified components.
4. Next.js production build (`npm --prefix frontend run build`).
5. Live curl verification on port 3002.
