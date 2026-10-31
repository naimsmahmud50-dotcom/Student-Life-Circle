# Feature Specification: 063-curriculum-learn-page-atmospheric-redesign

## 1. Executive Summary & Problem Statement
The NCTB Curriculum & Chapter-wise Learning Page (`frontend/src/pages/learn.tsx`) features a flagship `PageHeader` banner with warm amber background, editorial breadcrumbs, category chip, and 4 metric cards. However, the subsequent lower sections (Stage switcher tabs, Spaced-repetition revision queue, Subject chapters listing) are currently rendered using flat cards with thin borders and zero atmospheric lighting, depth, or thematic visual storytelling.

The user has instructed:
"prothom paray design ache baki para gula design nai akhn tmr kaj holo tmi path khuje paciho onno kno path a jhamela na kore akdom jei path tmi khuje paich sei path ar design ta tmi nicher para gula uporer sathe thik rekhe design kore felo tbe mne rekho akdom copy paste design jate na hoy akkhere obossoi sotorko thakba best design diba ,, design korar time tmi tmr sokol skill jmn /design /ui-styling /ui-ux-pro-max joto designing skilll ache sob skill kaje lagiye kaj suru kore dibe akta bisoy note kore felo tmk jei path dewya hoilo sei path betito proyojon chara onno kno path a hat diba na onno kno code nosto korba na tmi mne rakhba tmr kaj jeita dewya hoiche sudhu sei kaj ta tmi kroba onno kothaw onno code a jhamela korba na.."

## 2. Goals & Non-Goals
### Goals
1. **Atmospheric Aesthetic Continuity:** Elevate the lower sections of `frontend/src/pages/learn.tsx` with tailored radial lighting, thematic typographic watermarks, frosted glass containers, tactile 3D buttons, and refined micro-interactions.
2. **Distinct Themed Sections:**
   - **PageHeader Elevation:** Add signature watermark `CURRICULUM` to the top hero.
   - **Level Switcher & Search Console:** Frosted ivory and warm amber console with stage pills and keyword chapter search.
   - **Spaced-Repetition Revision Queue (`REVISION`):** Sage-emerald container with watermark `REVISION`, SM-2 algorithm badge, pulse remaining indicator, and elevated revision cards.
   - **NCTB Subjects & Chapter Matrix (`SYLLABUS`):** Oxford Navy and ivory canvas with watermark `SYLLABUS`, subject progress gauges, circular chapter progress rings, and tactile 3D action buttons.
   - **Board Exam Pedagogical Roadmap (`GUIDELINES`):** Golden-amber container with watermark `GUIDELINES` containing 4 strategic study cards.
   - **Curriculum FAQ Accordion (`ACADEMIC`):** Oxford Midnight container with watermark `ACADEMIC` answering syllabus update, offline study, and CQ answering techniques.
3. **Strict Zero-Emoji Discipline:** Pure Lucide SVG icons only. No emoji characters anywhere in code, commits, or responses.
4. **Strict Scope Lock:** Modify exclusively `frontend/src/pages/learn.tsx`. Do not touch any other pages or buttons.
5. **Zero TypeScript Errors & 100% Production Build:** Ensure `npx tsc --noEmit` and `npm --prefix frontend run build:pages` succeed with zero errors.

### Non-Goals
- No backend API route modifications.
- No changes to any files outside `frontend/src/pages/learn.tsx`.
