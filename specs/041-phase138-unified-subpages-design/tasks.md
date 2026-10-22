# TASKS: Phase 138 — Unified Premium Design for Sub-pages

- [x] **Task 1**: Implement missing design system primitives: `input.tsx`, `select.tsx`, `skeleton.tsx`, `empty-state.tsx`, `error-state.tsx` in `frontend/src/components/ui/`, and `PageHeader.tsx` in `frontend/src/components/layout/`. Export all from `frontend/src/components/ui/index.ts`.
- [x] **Task 2**: Rebuild `/practice` (`frontend/src/pages/practice.tsx`) with the unified design system, `PageHeader`, `Skeleton` loading states, `ErrorState`, and tactile 3D button physics.
- [x] **Task 3**: Rebuild `/board-archives` (`frontend/src/pages/board-archives.tsx`) linking to the global dark/light theme, `PageHeader`, unified `Input`, `Select`, `Card`, and `EmptyState`.
- [x] **Task 4**: Rebuild `/modules` (`frontend/src/pages/modules.tsx`) standardizing on `Navbar`, `Footer`, `PageHeader`, and unified design tokens.
- [x] **Task 5**: Rebuild and elevate `/learn` (`frontend/src/pages/learn.tsx`) and `/dashboard` (`frontend/src/pages/dashboard.tsx`) with consistent headers, tabs, and tactile buttons.
- [x] **Task 6**: Implement automated test suite `backend/tests/test_phase138_unified_design.py`.
- [x] **Task 7**: Run `python3 backend/scripts/run_zero_emoji_sweep.py` asserting 0 emoji violations.
- [x] **Task 8**: Run `python3 -m unittest backend/tests/test_phase138_unified_design.py` verifying all Phase 138 tests pass.
- [x] **Task 9**: Run full repository test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`) verifying all 1,537 tests pass with 0 regressions.
- [x] **Task 10**: Build Next.js frontend (`npm run build`) ensuring all static pages compile cleanly and live probe returns HTTP 200.
- [x] **Task 11**: Generate `PHASE_138_UNIFIED_SUBPAGES_DESIGN_REPORT.md` artifact and present final review report to the user in Bengali.
