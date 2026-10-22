<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 110 Pure Academic Design System & Complete AI-Vibe Purge
FILE:      specs/014-phase110-pure-academic-design-purge/spec.md
PHASE:     Phase 110 - Pure Academic Visual Design Elevation
PURPOSE:   Purges all AI-generated neon artifacts, establishing a prestigious,
           human-crafted Oxford/Cambridge academic design system with zero emojis.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA Contrast
-->

# Feature Specification: Phase 110 — Pure Academic Design System & Complete AI-Vibe Purge

## 1. Problem Statement & Motivation
Modern web tools and AI scaffolding generators frequently inject generic SaaS artifacts: neon cyan/indigo gradients, flashy cyber glows (`glow-blue`, `glow-teal`, `glow-amber`), radioactive purple buttons, and harsh dark-mode glass cards. For an authoritative national education ecosystem supporting students from primary school through higher education, board examinations, and corporate recruitment, such aesthetics feel artificial, childish, and distracting.

Phase 110 executes a complete, platform-wide purge of AI-vibe neon artifacts, replacing them with a prestigious, scholarly Oxford/Cambridge visual language.

## 2. Pure Academic Color Palette
1. **Primary Anchor:**
   - Deep Oxford Academic Navy (`#0A2540` / `#0F2942`) — authoritative, scholarly, calm.
2. **Canvas & Ground:**
   - Scholarly Pure Paper White (`#FFFFFF`) and Warm Ivory (`#FAFAF8`) in light mode.
   - Deep Regal Ink Slate (`#0B132B`) in dark mode.
   - NO neon radial gradients.
3. **Academic Emerald:**
   - `#065F46` / `#0D9488` for verified credentials, high accuracy, and passing grades.
4. **Scholar Gold:**
   - `#B45309` for academic honors, study streaks, and scholarship milestones.
5. **Burgundy Crimson:**
   - `#991B1B` / `#DC2626` for negative marking alerts and warnings.
6. **Hairline Architectural Rules:**
   - Crisp borders using `border-slate-200/80` or `border-[#E5E7EB]` or `border-slate-800/80`.

## 3. Tactile 3D Academic Buttons
1. **Primary Button:**
   - Deep Oxford Navy with 3D bottom depth: `bg-[#0A2540] text-white font-semibold rounded-2xl shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none hover:bg-[#0E3357] transition-all`.
2. **Secondary / Outline Button:**
   - Pure white paper card with crisp hairline border: `bg-white text-slate-800 border border-slate-300 shadow-sm hover:bg-slate-50 active:translate-y-0.5`.
3. **Emerald Academic Button:**
   - `bg-[#065F46] text-white font-semibold rounded-2xl shadow-[0_4px_0_0_#044332] active:translate-y-1 active:shadow-none hover:bg-[#087858] transition-all`.

## 4. Typography & Iconography
- Strict Bengali copy: `Hind Siliguri` (line-height 1.75).
- Latin display titles: `Plus Jakarta Sans`.
- Tabular figures / metrics: `Inter`.
- Strict Zero-Emoji Rule: 100% Lucide-React SVG vectors with 1.75px stroke width.

## 5. Scope of Impact & Target Files
- `frontend/src/styles/globals.css`
- `frontend/tailwind.config.js`
- `frontend/src/components/ui/button.tsx`
- `frontend/src/pages/index.tsx`
- `frontend/src/components/layout/Navbar.tsx`
- `frontend/src/components/layout/Footer.tsx`
- `backend/tests/test_phase110_pure_academic_design.py`
