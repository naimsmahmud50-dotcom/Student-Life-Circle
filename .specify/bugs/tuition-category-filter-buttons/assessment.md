# Bug Assessment: Tuition Category Filter Buttons & Scrollbar Defect

- **Slug**: tuition-category-filter-buttons
- **Created**: 2026-10-31T16:14:00+06:00
- **Source**: User uploaded screenshot and report regarding tuition category filter pills
- **Verdict**: valid
- **Severity**: high

## Report (summarized)

The user reported that the category filter buttons on the tuition page (`ক্যাটাগরি অনুযায়ী টিউশন ফিল্টার:`) are defective and not working properly. The uploaded screenshot shows the category pills (`সকল ক্যাটাগরি`, `বাংলা মাধ্যম`, `ইংলিশ ভার্সন`, `ইংলিশ মিডিয়াম`, `ধর্মীয় ও কুরআন শিক্ষা`, `ভর্তি পরীক্ষা প্রস্তুতি`, `ভাষা ও স্কিল...`) with an unstyled, thick native browser scrollbar across the bottom. Clicking the buttons fails to filter the jobs listing, and other buttons or features in the app must not be touched or affected.

## Symptom

1. **Ugly Native Browser Scrollbar**: The horizontal category pills container uses `no-scrollbar`, but `.no-scrollbar` utility classes were missing from `globals.css`. This causes browsers to render an unstyled, thick native scrollbar with arrows underneath the pills.
2. **Category Filter State Disconnect**: In `TuitionJobBoard.tsx`, `selectedCategory` state was initialized via `useState<string>(initialCategory)` but was never synchronized when the parent `TuitionPage` passed updated `selectedCategory` props. Consequently, clicking any category pill never updated the job board list.
3. **Missing Jobs for Categories**: Categories `arts_lang` (ভাষা ও স্কিলস) and `special_child` (স্পেশাল চাইল্ড কেয়ার) had 0 matching entries in `TUITION_JOBS`, leaving an empty screen without context.
4. **Tutor Directory Lack of Category Filtering**: In `tuition.tsx`, switching or selecting categories did not filter the `VerifiedTutorDirectory` component.

## Reproduction

1. Visit `/tuition` in any browser.
2. Observe the thick OS/browser horizontal scrollbar underneath the category pills.
3. Click on any category button such as "ইংলিশ ভার্সন 340" or "ভর্তি পরীক্ষা প্রস্তুতি 72".
4. Notice that the Job Board listing remains unchanged and does not filter to match the selected category.

## Suspected Code Paths

- `frontend/src/styles/globals.css` — Missing `.no-scrollbar` utility definition.
- `frontend/src/components/tuition/TuitionCategoryPills.tsx` — Button click handling, horizontal scroll styling and smooth scroll behavior.
- `frontend/src/components/tuition/TuitionJobBoard.tsx` — Lack of `useEffect` or direct controlled state synchronization for `initialCategory` / `selectedCategory`.
- `frontend/src/components/tuition/data/tuitionElevationData.ts` — Missing dataset samples for `arts_lang` and `special_child`.
- `frontend/src/components/tuition/VerifiedTutorDirectory.tsx` — Filter matching for selected category.
- `frontend/src/pages/tuition.tsx` — State wiring between category pills, job board, and active tabs.

## Root Cause Hypothesis

`TuitionJobBoard` treated `initialCategory` as a one-time initial state in `useState(initialCategory)` without reacting to prop updates from `TuitionPage`. Simultaneously, `.no-scrollbar` was used in `TuitionCategoryPills.tsx` without being declared in `globals.css` with `-ms-overflow-style: none; scrollbar-width: none; ::-webkit-scrollbar { display: none; }`, exposing the raw browser scrollbar. Confidence: High.

## Proposed Remediation

**Preferred**:
1. Add `.no-scrollbar` utility to `globals.css` to eliminate the ugly browser scrollbar while preserving smooth horizontal swiping/scrolling.
2. Add a `useEffect` in `TuitionJobBoard.tsx` (or bind `selectedCategory` prop) to immediately synchronize when `initialCategory` changes from the parent pills.
3. Add sample jobs for `arts_lang` and `special_child` in `tuitionElevationData.ts` so every category pill displays matching verified jobs.
4. Enable category filtering in `VerifiedTutorDirectory.tsx` via `selectedCategory` prop.
5. In `TuitionCategoryPills.tsx`, add smooth centering on click and enhanced tactile active states.
6. Guard all changes strictly within `frontend/src/components/tuition/` and `frontend/src/styles/globals.css` so no other pages, features, or buttons are disturbed.

**Files likely to change**:
- `frontend/src/styles/globals.css`
- `frontend/src/components/tuition/TuitionCategoryPills.tsx`
- `frontend/src/components/tuition/TuitionJobBoard.tsx`
- `frontend/src/components/tuition/VerifiedTutorDirectory.tsx`
- `frontend/src/components/tuition/data/tuitionElevationData.ts`
- `frontend/src/pages/tuition.tsx`

**Tests to add or update**:
- Test category pill selection in `frontend/src/components/tuition/__tests__/TuitionCategoryPills.test.tsx`

## Risks & Considerations

- Must strictly adhere to the user's requirement not to alter any other page, feature, or button.
- Must maintain strict Zero-Emoji discipline.
- Must ensure responsive touch and desktop keyboard accessibility.
