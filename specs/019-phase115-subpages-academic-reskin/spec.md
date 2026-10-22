<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 115 Sub-Pages Academic Re-Skin & AI-Vibe Elimination
FILE:      specs/019-phase115-subpages-academic-reskin/spec.md
PHASE:     Phase 115 - Sub-Pages Pure Academic Re-Skin
PURPOSE:   Eradicates all AI-generated neon artifacts across sub-pages, enforcing
           authentic Oxford Navy and Paper Ivory human craftsmanship.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Feature Specification: Phase 115 — Sub-Pages Academic Re-Skin & AI-Vibe Elimination

## 1. Problem Statement
Previous development iterations introduced synthetic AI vibes (such as fluorescent neon gradients `bg-clip-text`, `bg-gradient-to-r from-blue-* to-indigo-*`, `glow-blue`, and casual Unicode emojis) across several primary platform sub-pages:
- `/learn`
- `/practice`
- `/live-challenge`
- `/admission`
- `/tuition`
- `/career`

These visual artifacts detract from the dignified, scholarly tone appropriate for students preparing for high-stakes examinations (HSC, SSC, BUET, Medical, Dhaka University).

## 2. Requirements & Goals
1. **Zero AI Vibe**:
   - Total elimination of `bg-clip-text`, `bg-gradient-to-r from-blue-* to-indigo-*`, and fluorescent glow classes.
   - Elimination of all Unicode emojis in favor of crisp 1.75px stroke Lucide vector icons (`BookOpen`, `Award`, `Clock`, `Compass`, `FileText`, `CheckCircle2`, `ShieldCheck`).
2. **Pure Academic Visual Language**:
   - Deep Oxford Academic Navy (`#0A2540` / `#0F2942`) for primary headings, actions, and structure.
   - Pure Paper White (`#FFFFFF`) and Warm Ivory (`#FAFAF8`) for light mode card surfaces.
   - Deep Regal Ink Slate (`#0B132B`) for dark mode surfaces.
   - Paper borders (`border-[#E5E7EB]` or `border-slate-300`).
3. **Tactile Interaction**:
   - 3D tactile bottom shadow buttons: `shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`.
4. **Typography & Math**:
   - 100% 'Hind Siliguri' for Bengali text with comfortable `leading-[1.75]`.
   - KaTeX for scientific and mathematical equations.
   - Tabular 'Inter' numbers for timers, marks, and statistics.
5. **Architectural Integrity**:
   - Developer Architecture Note at the top of every file.
   - Zero breaking changes to existing state stores or backend endpoint bindings.
   - 100% green test suite across 1,360+ tests.
