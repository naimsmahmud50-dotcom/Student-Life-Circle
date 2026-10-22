<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Master Academic UI & Pro Tactile Button Elevation Tasks
FILE:      specs/027-phase123-master-academic-ui-elevation/tasks.md
PHASE:     Phase 123 - Master Academic UI & Pro Tactile Button Elevation
PURPOSE:   Actionable, ordered checklist for elevating styles, buttons, layout, and test suite.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
-->

# Tasks: Feature 027 — Phase 123 Master Academic UI & Pro Tactile Button Elevation

## Tasks Ledger

- [x] T001 Elevate `frontend/src/styles/globals.css`
  - Update header with Phase 123 Developer Architecture Note
  - Ensure pure academic palette tokens (#0A2540, #FAFAF8, #FFFFFF, #065F46, #B45309, #991B1B)
  - Ensure body line-height is 1.75
  - Ensure `.btn-3d-oxford` has `shadow-[0_4px_0_0_#051329]`, `hover:bg-[#0E3357]`, `active:translate-y-1 active:shadow-none`
  - Ensure `.btn-3d-emerald` has `shadow-[0_4px_0_0_#033829]`, `hover:bg-[#087858]`, `active:translate-y-1 active:shadow-none`
  - Ensure `.btn-paper-outline` has `bg-white`, `border-slate-300`, `shadow-sm`, `active:translate-y-0.5`
  - Retain all navbar variables required by `test_navbar_polish.py`
  - Ensure strict zero emojis

- [x] T002 Elevate `frontend/tailwind.config.js`
  - Update header with Phase 123 Developer Architecture Note
  - Verify `oxford`, `emerald`, `scholar`, `paper`, `ink`, `burgundy` color tokens
  - Verify fonts: `Hind Siliguri`, `Plus Jakarta Sans`, `Inter`
  - Verify `boxShadow`: `paper`, `tactile-oxford`, `tactile-emerald`, `tactile-pressed`
  - Assert zero glow tokens (`glow-blue`, `glow-teal`, `glow-amber`)

- [x] T003 Upgrade `frontend/src/components/ui/button.tsx`
  - Update header with Phase 123 Developer Architecture Note
  - Ensure 3D tactile physics for Oxford Navy (`shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none hover:bg-[#0E3357]`)
  - Ensure 3D tactile physics for Academic Emerald (`shadow-[0_4px_0_0_#033829] active:translate-y-1 active:shadow-none hover:bg-[#087858]`)
  - Ensure tactile physics for Paper Secondary (`bg-white text-slate-800 border border-slate-300 shadow-sm active:translate-y-0.5 rounded-2xl`)
  - Ensure touch targets >= 44px on `md` and >= 36px on `sm`
  - Retain variants `'oxford'`, `'emerald'`, `'paper'`, `'default'`, `'brand'`, `'teal'`, etc.

- [x] T004 Polish `frontend/src/pages/index.tsx`
  - Update header with Phase 123 Developer Architecture Note
  - Refine hero and interactive cards with tactile 3D buttons (`btn-3d-oxford`, `btn-3d-emerald`, `btn-paper-outline`)
  - Maintain all legacy anchors and telemetry components without any purple/indigo neon gradient cards

- [x] T005 Polish `frontend/src/pages/dashboard.tsx`
  - Update header with Phase 123 Developer Architecture Note
  - Use tactile 3D Oxford and Paper buttons for action cards

- [x] T006 Polish `frontend/src/components/layout/Navbar.tsx`
  - Update header with Phase 123 Developer Architecture Note
  - Ensure all existing assertions in `test_navbar_polish.py` and `test_phase110_pure_academic_design.py` remain satisfied

- [x] T007 Polish `frontend/src/components/layout/Footer.tsx`
  - Update header with Phase 123 Developer Architecture Note
  - Maintain NCTB, ISO 27001, OWASP, and 99.9% uptime compliance bars

- [x] T008 Implement automated test `backend/tests/test_phase123_master_academic_ui.py`
  - Verify Developer Architecture Notes on all 7 target files
  - Verify Pure Academic Palette tokens and classes
  - Verify Tactile 3D button physics across `button.tsx`, `globals.css`, and `index.tsx`
  - Verify Typography standards ('Hind Siliguri', 'Plus Jakarta Sans', 'Inter')
  - Verify zero neon glow and zero purple/indigo neon classes
  - Verify 100% Zero-Emoji compliance across all target files

- [x] T009 Build & Test Execution
  - Run `python3 -m unittest backend/tests/test_phase123_master_academic_ui.py`
  - Run Next.js build: `npm run build`
  - Run Zero-Emoji sweep: `python3 backend/scripts/run_zero_emoji_sweep.py`
  - Run master platform discovery: `python3 -m unittest discover -s backend/tests -p "test_*.py"`
