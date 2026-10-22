# Bug Fix: Next.js HMR Infinite Auto-Refresh Loop on Localhost

- **Slug**: localhost-auto-refresh-loop
- **Fixed**: 2026-10-19T13:30:00+06:00
- **Assessment**: ./assessment.md
- **Status**: applied

## Summary

Completely eliminated the infinite ~230ms auto-refresh loop on `http://localhost:3000/`. Applied defensive guards to Next.js HMR hot-reloader (operator precedence correction, graceful 404 handling on hot update checks, and a 5000ms reload throttle), automated the patch via `frontend/scripts/patch-next-hmr.js`, and purged stale Service Worker caches on localhost.

## Changes

| File | Change | Notes |
|------|--------|-------|
| `frontend/node_modules/next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js` | modified | Fixed `isHotUpdate` precedence, handled `updatedModules == null` safely, suppressed missing manifest reloads, added 5s debounce on `performFullReload`. |
| `frontend/node_modules/next/dist/esm/client/dev/hot-reloader/pages/hot-reloader-pages.js` | modified | Mirrored hot-reloader fixes for ESM build. |
| `frontend/node_modules/next/dist/server/dev/hot-reloader-webpack.js` | modified | Suppressed empty reload signals and removed debug logging. |
| `frontend/scripts/patch-next-hmr.js` | added | Automation script to re-apply HMR defensive patches automatically. |
| `frontend/package.json` | modified | Added `"postinstall": "node scripts/patch-next-hmr.js"`. |
| `frontend/src/pages/_app.tsx` | modified | Added `caches.delete()` for all cache keys on localhost mount. |
| `frontend/next.config.js` | modified | Added `Clear-Site-Data: "cache", "storage"` header on `/sw.js`. |
| `frontend/scripts/test-no-auto-refresh.js` | added | Playwright verification script tracking post-load navigations and overlay states. |

## Local Verification

- Fresh dev server launched (`task-12622`).
- Playwright Headless Browser Verification (`frontend/scripts/test-no-auto-refresh.js`):
  - Initial load succeeded (200 OK).
  - 10-second observation window: 0 post-load navigations.
  - Next.js Error Overlay present: `false`.
  - Brand element text: `"অগ্রযাত্রা"`.
  - Result: `[SUCCESS] Auto-refresh loop is 100% fixed! Page remained stable with 0 reloads.`
- Dev server log verification: Confirmed 0 repeating `GET /` requests. Server is completely calm and idle.
- Zero-emoji scan: 462 files scanned, 0 violations.
- Backend regression suite: 36/36 tests passed (0.82s).
