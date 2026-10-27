# Implementation Tasks: Retain Initial Dark Mode & Eliminate Theme Flash

## Phase 1: Theme Synchronization & Locking
- [x] T001: Update `frontend/src/pages/_document.tsx` to set Dark Mode as default unless explicitly saved as `'light'`.
- [x] T002: Update `frontend/src/pages/_app.tsx` to preserve Dark Mode on hydration without stripping `dark` class.
- [x] T003: Verify and synchronize `frontend/src/components/layout/Navbar.tsx` and `frontend/src/components/layout/Layout.tsx` theme toggle states.
- [x] T004: Inspect and polish Dark Mode visual hierarchy in `frontend/src/pages/index.tsx` (obsidian canvas, golden amber glows, high-contrast typography).

## Phase 2: Verification, Security & Quality Control
- [x] T005: Run TypeScript compiler check (`./frontend/node_modules/.bin/tsc --project frontend/tsconfig.json --noEmit`) to verify 0 errors.
- [x] T006: Run automated test suite (`node --experimental-strip-types --test frontend/src/data/__tests__/goeduData.test.mjs frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs`).
- [x] T007: Run Python zero-emoji audit script across modified files.
- [x] T008: Execute full production build (`npm --prefix frontend run build`).
- [x] T009: Restart server on port 3002 and verify live responses with curl.
