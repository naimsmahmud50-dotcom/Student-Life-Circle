# Implementation Tasks: Bespoke Feature Background Designs & Giant Watermarks

## Phase 1: Core Layout & Sub-Page Foundation
- [x] T001: Elevate `frontend/src/components/layout/PageHeader.tsx` with `watermarkText`, `glowGradient`, and warm sunshine canvas.
- [x] T002: Elevate `frontend/src/pages/board-archives.tsx` with watermark `ARCHIVES` via PageHeader.
- [x] T003: Elevate `frontend/src/pages/practice.tsx` with watermark `PRACTICE` via PageHeader and warm linen canvas.

## Phase 2: Flagship Feature Pages Custom Atmospheric Heroes
- [x] T004: Elevate `frontend/src/pages/socratic/solver.tsx` with bespoke atmospheric hero banner, watermark `SOCRATIC`, radial glow, and warm ivory cards.
- [x] T005: Elevate `frontend/src/pages/live-challenge.tsx` with watermark `CHALLENGE` and golden stadium aura.
- [x] T006: Elevate `frontend/src/pages/tuition.tsx` with watermark `TUITION` and trusted scholar golden aura.
- [x] T007: Elevate `frontend/src/components/career/CareerStatsHeader.tsx` and `frontend/src/pages/career.tsx` with watermark `CAREER` and horizon glow.
- [x] T008: Elevate `frontend/src/pages/admission.tsx` with watermark `ADMISSION` and university prestige aura.

## Phase 3: Verification, Security & Quality Control
- [x] T009: Run TypeScript check (`./frontend/node_modules/.bin/tsc --project frontend/tsconfig.json --noEmit`) to ensure zero errors.
- [x] T010: Run test suite (`node --experimental-strip-types --test frontend/src/data/__tests__/goeduData.test.mjs frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs`).
- [x] T011: Run zero-emoji audit script across all modified files.
- [x] T012: Execute production build (`npm --prefix frontend run build`).
- [x] T013: Verify live server response on port 3002 across all elevated routes with curl.
