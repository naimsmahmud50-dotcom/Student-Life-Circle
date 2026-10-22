# IMPLEMENTATION PLAN: Phase 139 — PWA, Offline Experience & Mobile Optimization

## Technical Context
- **Framework**: Next.js 14 Pages Router with standalone output (`output: 'standalone'`).
- **Styling**: Tailwind CSS with Oxford Academic Dark Palette (`#090D16`), 3D tactile buttons, Lucide React SVG icons.
- **Client Storage**: IndexedDB via `idb` with typed schemas and graceful in-memory/localStorage fallback.
- **Service Worker**: Cache API v2 with precision invalidation, multi-tier cache buckets (`slc-static-v2`, `slc-pages-v2`, `slc-data-v2`, `slc-fonts-v2`).
- **Offline Fallback**: Offline page at `/offline` served seamlessly when network drops.

## Implementation Steps
1. **Task 1: PWA Manifest & App Icons**: Update `frontend/public/manifest.json` with Oxford Navy theme `#090D16`, background `#090D16`, icons, categories, orientation, and shortcuts.
2. **Task 2: Service Worker (`sw.js`)**: Revamp `frontend/public/sw.js` with multi-tier caching (precache shell, cache-first fonts/static, stale-while-revalidate data/papers, network-first with `/offline` navigation fallback), message listener for `SKIP_WAITING`, and remove localhost suppression in production mode.
3. **Task 3: IndexedDB Past Papers Store**: Implement `frontend/src/lib/offline/offline-papers-store.ts` using `idb` to persist board question papers, offline reading lists, and offline answer submissions.
4. **Task 4: PWA UI Components**:
   - `frontend/src/components/pwa/PwaUpdateToast.tsx`
   - `frontend/src/components/pwa/PwaInstallBanner.tsx`
   - `frontend/src/components/pwa/OfflineIndicator.tsx`
5. **Task 5: Elevate `/offline` Page**: Rebuild `frontend/src/pages/offline.tsx` using `PageHeader`, `EmptyState`, cached papers listing, connection retry button, and offline guidance.
6. **Task 6: App & Document Integration**:
   - Update `frontend/src/pages/_app.tsx` to register Service Worker reliably in production, listen for `updatefound` / `waiting`, and render the PWA prompts.
   - Update `frontend/src/pages/_document.tsx` with font preconnects (`fonts.googleapis.com`, `fonts.gstatic.com`) and mobile viewport optimization.
7. **Task 7: Automated Backend Test Suite**: Implement `backend/tests/test_phase139_pwa_offline.py` covering manifest, SW logic, offline store, UI components, and headers.
8. **Task 8: Zero-Emoji Sweep & Test Execution**: Verify 0 emoji violations and ensure all 1,537+ tests pass.
9. **Task 9: Build & Standalone Deployment**: Execute `npm run build`, copy static assets, restart the standalone server, and verify HTTP 200 response on `/` and `/offline`.
10. **Task 10: Verification & Completion Report**: Generate artifact and deliver final report in Bengali.
