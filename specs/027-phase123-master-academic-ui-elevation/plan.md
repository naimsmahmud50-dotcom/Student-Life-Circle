<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Master Academic UI & Pro Tactile Button Elevation Implementation Plan
FILE:      specs/027-phase123-master-academic-ui-elevation/plan.md
PHASE:     Phase 123 - Master Academic UI & Pro Tactile Button Elevation
PURPOSE:   Architectural blueprint and phase execution order for tactile button elevation,
           globals styling, Tailwind token harmonization, and comprehensive test suite.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
-->

# Plan: Feature 027 — Phase 123 Master Academic UI & Pro Tactile Button Elevation

## Architecture & Integration Plan

### Step 1: Design Tokens & Canvas Elevation
- **File**: `frontend/src/styles/globals.css`
- Ensure `@import` includes `Hind Siliguri`, `Plus Jakarta Sans`, `Inter`.
- Body line-height set to `1.75` for Bengali legibility.
- Define pure academic tactile button utilities:
  - `.btn-3d-oxford` with `#0A2540`, `shadow-[0_4px_0_0_#051329]`, `hover:bg-[#0E3357]`, `active:translate-y-1 active:shadow-none`.
  - `.btn-3d-emerald` with `#065F46`, `shadow-[0_4px_0_0_#033829]`, `hover:bg-[#087858]`, `active:translate-y-1 active:shadow-none`.
  - `.btn-paper-outline` with `bg-white`, `border-slate-300`, `shadow-sm`, `active:translate-y-0.5`.
- Maintain all existing navbar tokens required by `test_navbar_polish.py`.

### Step 2: Tailwind Config Harmonization
- **File**: `frontend/tailwind.config.js`
- Assert colors: `oxford`, `emerald`, `scholar`, `paper`, `ink`, `burgundy`.
- Assert font families: `sans` ('Hind Siliguri'), `display` ('Plus Jakarta Sans'), `tabular` ('Inter').
- Assert boxShadow tokens: `paper`, `tactile-oxford`, `tactile-emerald`, `tactile-pressed`.
- Strictly no glow tokens (`glow-blue`, `glow-teal`, `glow-amber`).

### Step 3: Button Primitive Upgrade
- **File**: `frontend/src/components/ui/button.tsx`
- Ensure `variantStyles`:
  - `oxford` / `default` / `primary` / `brand`: `bg-[#0A2540] text-white hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`
  - `emerald` / `academic` / `teal`: `bg-[#065F46] text-white hover:bg-[#087858] shadow-[0_4px_0_0_#033829] active:translate-y-1 active:shadow-none`
  - `paper` / `outline`: `bg-white text-slate-800 border border-slate-300 shadow-sm hover:bg-slate-50 active:translate-y-0.5 rounded-2xl`
  - `destructive` / `danger`: `bg-[#991B1B] text-white hover:bg-[#7F1D1D] shadow-[0_4px_0_0_#5B1010] active:translate-y-1 active:shadow-none`
- Min-height touch targets >= 44px on `md` and >= 36px on `sm`.
- Loading spinner using `Loader2` from `lucide-react`.

### Step 4: Page Polish
- **Files**: `frontend/src/pages/index.tsx`, `frontend/src/pages/dashboard.tsx`, `frontend/src/components/layout/Navbar.tsx`, `frontend/src/components/layout/Footer.tsx`.
- Review and refine button classes, card headers, and interactive controls to employ the tactile 3D physics.
- Confirm zero purple/indigo neon gradient cards, zero glowing borders.
- Preserve all existing anchors and semantic tags required by previous test phases.

### Step 5: Comprehensive Automated Test Suite
- **File**: `backend/tests/test_phase123_master_academic_ui.py`
- Test 1: Developer Architecture Notes in all target files.
- Test 2: Pure Academic Design Tokens in `globals.css` and `tailwind.config.js`.
- Test 3: Tactile 3D button classes in `button.tsx`, `globals.css`, and `index.tsx`.
- Test 4: Absence of neon glow, neon cyan borders, and purple gradient cards.
- Test 5: Typography rules ('Hind Siliguri', 'Plus Jakarta Sans', 'Inter').
- Test 6: Strict Zero-Emoji compliance across all target files.

### Step 6: Verification & Full Suite Discovery
- Execute `python3 -m unittest backend/tests/test_phase123_master_academic_ui.py`.
- Execute Next.js build: `npm run build`.
- Execute master discovery: `python3 -m unittest discover -s backend/tests -p "test_*.py"`.
