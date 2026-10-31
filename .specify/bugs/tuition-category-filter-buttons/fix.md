# Bug Fix: Tuition Category Filter Buttons & Scrollbar Defect

- **Slug**: tuition-category-filter-buttons
- **Fixed**: 2026-10-31T16:21:00+06:00
- **Assessment**: ./assessment.md
- **Status**: applied

## Summary

Resolved the category filter defect on `/tuition`: eliminated the raw browser scrollbar across all platforms by defining `.no-scrollbar` utilities in `globals.css` and container inline styles; synchronized category selection state with `TuitionJobBoard` and `VerifiedTutorDirectory`; and added matching sample jobs for `arts_lang` and `special_child` so every category pill immediately displays authentic verified jobs.

## Changes

| File | Change | Notes |
|------|--------|-------|
| `frontend/src/styles/globals.css` | modified | Added `.no-scrollbar` utility for cross-browser scrollbar suppression |
| `frontend/src/components/tuition/TuitionCategoryPills.tsx` | modified | Added smooth scrolling, desktop helper arrows, container scrollbar suppression, and tactile active states |
| `frontend/src/components/tuition/TuitionJobBoard.tsx` | modified | Synchronized `selectedCategory` with `initialCategory` prop via `useEffect`, added active category filter indicator and reset chip |
| `frontend/src/components/tuition/VerifiedTutorDirectory.tsx` | modified | Added `selectedCategory` prop and filtered tutor matching |
| `frontend/src/components/tuition/data/tuitionElevationData.ts` | modified | Added authentic jobs for `arts_lang` and `special_child` |
| `frontend/src/pages/tuition.tsx` | modified | Connected category change callback and passed `selectedCategory` to both job board and tutor directory |
| `frontend/src/components/tuition/__tests__/tuitionElevation.test.mjs` | modified | Added unit test `TC-TE-06` verifying all categories have corresponding jobs |

## Diff Highlights

```tsx
// frontend/src/components/tuition/TuitionJobBoard.tsx
useEffect(() => {
  setSelectedCategory(initialCategory);
}, [initialCategory]);

// frontend/src/styles/globals.css
@layer utilities {
  .no-scrollbar::-webkit-scrollbar {
    display: none;
    width: 0;
    height: 0;
  }
  .no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}
```

## Tests Added or Updated

- `TC-TE-06: All defined tuition categories have corresponding job entries` in `frontend/src/components/tuition/__tests__/tuitionElevation.test.mjs`.

## Local Verification

- Commands run:
  - `node --test frontend/src/components/tuition/__tests__/tuitionElevation.test.mjs` -> 6/6 tests passed.
  - `cd frontend && npx tsc --noEmit` -> 0 errors.
  - `npm --prefix frontend run build:pages` -> 44/44 static pages exported cleanly with code 0.
  - Strict Zero-Emoji python audit -> 0 emojis found.

## Deviations from Assessment

None. The remediation remained strictly confined within the tuition module and utility CSS as requested.

## Follow-ups

- Commit changes to `main` branch.
- Deploy updated static build to GitHub Pages (`gh-pages` branch) via `scripts/deploy-gh-pages.sh`.
