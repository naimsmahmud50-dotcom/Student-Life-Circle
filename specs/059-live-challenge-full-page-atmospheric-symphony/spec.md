# Feature Specification: Live Challenge Full-Page Atmospheric Design Symphony

- **Feature Directory:** `specs/059-live-challenge-full-page-atmospheric-symphony`
- **Topic:** Phase 144 - Complete Live Challenge Chromatic Section Symphony
- **Target Page:** `frontend/src/pages/live-challenge.tsx` and all child components in `frontend/src/components/live-challenge/`
- **Design DNA:** Match the deep atmospheric aesthetic of the Live MCQ Hero (dark cosmic canvas, radial glow aura, subtle watermark, frosted glass cards, high-contrast typography, zero emojis).
- **Core Directive:** Each subsequent section must have its own distinct, harmonious chromatic color personality (not identical copies), transitioning smoothly down the page.

---

## 1. Chromatic Progression Matrix

1. **Hero Section (`LiveMcqHeroSection`):** Deep Cosmic Indigo & Amber (`#080C24`, Royal Blue & Indigo Glow).
2. **Section 2 (`LiveCategoryTrackSelector`):** Royal Sapphire & Cyan Lapis (`#07132B`, Sapphire Glow `rgba(14,165,233,0.18)`, Watermark: `TRACKS`).
3. **Section 3 (`DynamicInfoNoticeBoard`):** Deep Obsidian & Crimson Alert (`#130B14`, Rose Crimson Glow `rgba(225,29,72,0.18)`, Watermark: `BULLETIN`).
4. **Section 4 (`LiveFreeDemoExamBox`):** Midnight Navy & Electric Azure (`#0A1628`, Cyan Glow `rgba(6,182,212,0.18)`, Watermark: `DEMO EXAM`).
5. **Section 5 (`LiveHowItWorksPathway`):** Deep Scholar Emerald & Mint (`#061815`, Emerald Mint Glow `rgba(16,185,129,0.18)`, Watermark: `PATHWAY`).
6. **Section 6 (`SubjectWeightageBreakdown`):** Cosmic Ultraviolet & Purple Sky (`#0F0B24`, Violet Glow `rgba(168,85,247,0.18)`, Watermark: `WEIGHTAGE`).
7. **Section 7 (`InteractiveOmrSimulator`):** Lapis Lazuli & Golden Seal (`#0B152A`, Indigo-Gold Glow `rgba(99,102,241,0.18)`, Watermark: `OMR SHEET`).
8. **Section 8 (Leaderboard & Sidebar Cards):** Deep Charcoal & Golden Arena (`#14120C`, Golden Sunburst Glow `rgba(245,158,11,0.20)`, Watermark: `LEADERBOARD`).
9. **Section 9 (`LiveExamRoutineMatrix`):** Deep Marine Teal & Oceanic Breeze (`#08181A`, Teal Glow `rgba(20,184,166,0.18)`, Watermark: `ROUTINE`).
10. **Section 10 (`LiveMcqFeatureShowcase`):** Cosmic Amethyst & Magenta (`#130A20`, Fuchsia Glow `rgba(217,70,239,0.16)`, Watermark: `FEATURES`).
11. **Section 11 (`LiveMentorAndHallOfFame`):** Warm Terracotta & Auburn Bronze (`#18110D`, Amber Glow `rgba(249,115,22,0.18)`, Watermark: `MENTORS`).
12. **Section 12 (`LiveMcqFaqAccordion`):** Deep Slate Charcoal & Starlight (`#0D111A`, Steel Blue Glow `rgba(100,116,139,0.20)`, Watermark: `QUESTIONS`).

---

## 2. Acceptance Criteria

- **AC-001 (Atmospheric Lighting & Watermark):** Every section features a full-width deep canvas container with radial glow aura and ultra-subtle typographic watermark with `aria-hidden="true"`, `select-none`, and `pointer-events-none`.
- **AC-002 (Frosted Glass Cards):** Cards use frosted glass backgrounds (`bg-white/5` or `bg-slate-900/60` with `backdrop-blur-md` and `border border-white/10`).
- **AC-003 (Harmonic Color Transitions):** Each section displays distinct accent borders, badges, and glows that seamlessly transition from section to section without visual monotony.
- **AC-004 (Full Interactive Integrity):** All tabs, demo exam question selection, timer, OMR bubbles, leaderboard filters, and routine dates remain 100% interactive and bug-free.
- **AC-005 (Quality & Policy Compliance):** 100% zero-emoji (Lucide SVG only), passing TypeScript compilation, passing test suite (45/45), and running on port 3002.
