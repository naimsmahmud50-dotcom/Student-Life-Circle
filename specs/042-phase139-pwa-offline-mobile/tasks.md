# TASKS: Phase 139 — PWA, Offline Experience & Mobile Optimization

- [x] **Task 1**: Update `frontend/public/manifest.json` with theme color `#0F172A`, background `#F8FAFC`, valid icons (192, 512, maskable, SVG), standalone display, and shortcuts.
- [x] **Task 2**: Refactor `frontend/public/sw.js` with multi-tier caching (precache shell, cache-first fonts/static, stale-while-revalidate data/papers, network-first with `/offline` navigation fallback), message listener for `SKIP_WAITING`, push event listeners, and enable in production mode on localhost.
- [x] **Task 3**: Implement `frontend/src/lib/offline/offline-papers-store.ts` using `idb` to persist board question papers, offline reading lists, and sync queue.
- [x] **Task 4**: Implement PWA UI components in `frontend/src/components/pwa/`: `PwaUpdateToast.tsx`, `PwaInstallBanner.tsx`, `OfflineIndicator.tsx`, and export them via `frontend/src/components/pwa/index.ts`.
- [x] **Task 5**: Rebuild `/offline` (`frontend/src/pages/offline.tsx`) using `PageHeader`, `EmptyState`, cached papers listing, connection retry button, and offline guidance.
- [x] **Task 6**: Update `frontend/src/pages/_app.tsx` and `frontend/src/pages/_document.tsx` to handle SW registration, lifecycle prompts, offline indicators, and font preconnects.
- [x] **Task 7**: Implement automated test suite `backend/tests/test_phase139_pwa_offline.py`.
- [x] **Task 8**: Run `python3 backend/scripts/run_zero_emoji_sweep.py` asserting 0 emoji violations.
- [x] **Task 9**: Run `python3 -m unittest backend/tests/test_phase139_pwa_offline.py` verifying all Phase 139 tests pass.
- [x] **Task 10**: Run full repository test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`) verifying all 1,546 tests pass with 0 regressions.
- [x] **Task 11**: Build Next.js frontend (`npm run build`), copy static assets to standalone, restart the standalone server, and verify HTTP 200 response on `/` and `/offline`.
- [x] **Task 12**: Generate `PHASE_139_PWA_OFFLINE_REPORT.md` artifact and present final review report to the user in Bengali.
