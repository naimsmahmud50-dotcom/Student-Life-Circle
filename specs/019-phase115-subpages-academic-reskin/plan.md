<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 115 Sub-Pages Academic Re-Skin & AI-Vibe Elimination
FILE:      specs/019-phase115-subpages-academic-reskin/plan.md
PHASE:     Phase 115 - Sub-Pages Pure Academic Re-Skin
PURPOSE:   Eradicates all AI-generated neon artifacts across sub-pages, enforcing
           authentic Oxford Navy and Paper Ivory human craftsmanship.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 115 — Sub-Pages Academic Re-Skin & AI-Vibe Elimination

## Architecture & Re-Skin Strategy

### 1. `frontend/src/pages/learn.tsx`
- Curated subject chapter cards (Physics, Chemistry, Higher Math, Biology).
- Circular academic progress meters with calm slate/emerald tracks.
- Tactile 3D Oxford Navy study buttons ("অধ্যায় শুরু করুন").
- Pure Lucide icons (`BookOpen`, `Compass`, `Clock`, `Sparkles`, `CheckCircle2`).

### 2. `frontend/src/pages/practice.tsx`
- Distraction-free, high-contrast academic examination desk.
- Pure Paper White (`#FFFFFF`) question cards and option selectors with tactile bottom shadows.
- KaTeX mathematical and physical equations rendering.
- Bengali explanation drawer with clean typography.

### 3. `frontend/src/pages/live-challenge.tsx`
- Calm, dignified live countdown examination hall.
- Millisecond-accurate answer buffer with tabular Inter numerals.
- Burgundy Crimson negative marking indicators (`#991B1B`).
- Tactile answer submission buttons.

### 4. `frontend/src/pages/admission.tsx`
- Authentic university admission unit cards:
  * BUET Engineering Unit
  * Armed Forces / Government Medical College Unit
  * Dhaka University Ka Unit (Science)
  * GST Integrated Universities Unit
- Negative-marking badges in Burgundy Crimson (`#991B1B`).
- Tactile 3D buttons ("মডেল টেস্টে অংশ নিন").

### 5. `frontend/src/pages/tuition.tsx` & `career.tsx`
- `tuition.tsx`: Verified guardian escrow badges, academic subject criteria, physical location tags, tactile tuition matching buttons.
- `career.tsx`: Cryptographically sealed CV snapshot builder, industry verified skills tags, verified recruiter pipeline, zero generic job board fluff.

### 6. Automated Testing & Verification
- `backend/tests/test_phase115_subpages_academic_reskin.py`:
  * Asserts zero forbidden classes (`bg-clip-text`, `bg-gradient-to-r from-blue-`, `glow-blue`).
  * Asserts strict zero emojis across all 6 pages.
  * Asserts presence of Developer Architecture Notes.
  * Asserts 3D tactile button styling.
  * Platform regression test: 1,360+ tests passing.
