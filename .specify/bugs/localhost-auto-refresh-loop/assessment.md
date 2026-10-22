# Bug Assessment: Next.js HMR Infinite Auto-Refresh Loop on Localhost

- **Slug**: localhost-auto-refresh-loop
- **Created**: 2026-10-19T13:10:00+06:00
- **Source**: User feedback ("auto refresh hote thake, bug ta pele onno code a jhamela na kore fix kore dew") and server log analysis (rapid GET / every ~230ms).
- **Verdict**: valid
- **Severity**: critical

## Forensic Evidence & Error Analysis

When accessing `http://localhost:3000/`, Google Chrome repeatedly requested `GET /` every ~230 milliseconds, generating over a thousand reload requests in dev server logs:

```text
GET / 200 in 233ms
PAYLOAD_DEBUG: {"event":"client-full-reload","stackTrace":null,"hadRuntimeError":false}
Fast Refresh had to perform a full reload.
GET / 200 in 232ms
PAYLOAD_DEBUG: {"event":"client-full-reload","stackTrace":null,"hadRuntimeError":false}
Fast Refresh had to perform a full reload.
```

## Root Cause Analysis

1. **Operator Precedence Bug in Next.js 15 Client Hot Reloader**:
   - In `next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js`, `handleSuccess` defined:
     ```javascript
     const isHotUpdate = !isFirstCompilation || window.__NEXT_DATA__.page !== '/_error' && isUpdateAvailable();
     ```
   - Because `&&` binds tighter than `||`, the condition evaluated to `true` whenever `isUpdateAvailable()` was true, even during normal on-demand entry compilation.
2. **Compilation Hash Mismatch Between Compilers**:
   - Next.js compiles `main.js` and page entries in separate compilation passes. When an on-demand entry (`pages/index.js`) compiled, the sync stats emitted a new hash.
   - `isUpdateAvailable()` evaluated `mostRecentCompilationHash !== __webpack_hash__`, which returned `true` immediately after initial mount.
3. **Missing Hot Update Chunk Treated as Catastrophic Error**:
   - `tryApplyUpdatesWebpack()` called `module.hot.check(false)`.
   - Because no files were changed on disk, the server had no `.webpack.hot-update.json` file to serve (returned 404).
   - In standard Next.js, this 404 rejected the promise into `handleApplyUpdates(err, null)`.
   - `handleApplyUpdates` treated any error or `updatedModules == null` as a fatal failure and triggered `performFullReload()`.
4. **Unthrottled `window.location.reload()` Invocation**:
   - `performFullReload` called `window.location.reload()` unconditionally without throttling or deduplication.
   - The browser reloaded within 230ms, re-executed the same cycle, and created an infinite loop.
5. **Stale Service Worker Caching in Browser Profile**:
   - The user's active Google Chrome session retained older cached Service Worker and Cache Storage instances from earlier testing, continuously replaying stale scripts.

## Proposed Remediation

1. **Defensive Patch in Next.js Hot Reloader (`hot-reloader-pages.js`)**:
   - Fix operator precedence: `!isFirstCompilation && window.__NEXT_DATA__.page !== '/_error' && isUpdateAvailable()`.
   - When `updatedModules == null` without runtime errors, dispatch `onBuildOk()` and return cleanly instead of reloading.
   - When `module.hot.check()` encounters a missing manifest (404), catch gracefully and call `onBuildOk()`.
   - Add a 5000ms rate-limit guard inside `performFullReload` to permanently prevent rapid reload loops.
2. **Automated Postinstall Script**:
   - Create `frontend/scripts/patch-next-hmr.js` and wire to `frontend/package.json` under `postinstall` so the fix is preserved across package installs.
3. **Client-Side Cache & Storage Cleanup**:
   - In `frontend/src/pages/_app.tsx`, purge any lingering `caches` on localhost mount.
   - In `frontend/next.config.js`, add `Clear-Site-Data: "cache", "storage"` on `/sw.js` for development mode.
