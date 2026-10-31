# Implementation Plan: 063-curriculum-learn-page-atmospheric-redesign

## 1. Architectural Strategy
We elevate `frontend/src/pages/learn.tsx` by:
1. Adding `watermarkText="CURRICULUM"` to the top `PageHeader`.
2. Encapsulating the Level Switcher in an atmospheric Frosted Ivory & Amber search console (`relative overflow-hidden rounded-3xl border border-amber-200/60 dark:border-[#262D3D] ...`) with real-time chapter search.
3. Transforming the Spaced-Repetition Revision Queue into an atmospheric Sage-Emerald container with typographic watermark `REVISION` and elevated revision cards.
4. Elevating the Subjects and Chapters section into an Oxford Navy atmospheric canvas with typographic watermark `SYLLABUS`, high-craft subject cards, circular chapter gauge, and 3D tactile buttons.
5. Introducing an atmospheric pedagogical guidelines container (`GUIDELINES`) with 4 study strategies.
6. Introducing an atmospheric curriculum FAQ accordion container (`ACADEMIC`).
7. Preserving the Chapter Editorial Notes Drawer (`KaTeXRenderer`) and HLS Video Lecture Player modal.

## 2. Verification Protocol
1. TypeScript compilation: `npx tsc --noEmit` in `frontend/`.
2. Python Zero-Emoji audit on `frontend/src/pages/learn.tsx` and spec files.
3. Production static page build: `npm --prefix frontend run build:pages`.
4. Git commit and GitHub Pages deployment: `bash scripts/deploy-gh-pages.sh`.
