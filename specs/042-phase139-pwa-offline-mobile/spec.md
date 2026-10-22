# SPECIFICATION: Phase 139 — PWA, Offline Experience & Mobile Optimization

## 1. Executive Summary & Goal
The goal of **Phase 139** is to transform "Student Life Circle" (অগ্রযাত্রা) into an ultra-fast, world-class Progressive Web Application (PWA) tailored for learners across Bangladesh, especially students in rural and low-bandwidth environments (2G/3G connectivity).

Key mandates:
1. **Sub-1s Rural First-Contentful Paint (FCP) & Largest Contentful Paint (LCP)** via preloading, font subsetting (`swap`), and aggressive edge-caching.
2. **Standard PWA Installability**: Complete `manifest.json`, high-resolution icons (192, 512, maskable, SVG), standalone display, and elegant custom installation prompt.
3. **Multi-Tier Workbox-grade Service Worker (`sw.js`)**:
   - Cache-first for fonts (`fonts.gstatic.com`), static assets, and Lucide SVG icons.
   - Stale-while-revalidate for board question papers and curriculum manifests.
   - Network-first with offline fallback (`/offline`) for all route navigations.
   - Safe localhost handling that allows full PWA offline verification in production mode.
4. **Offline Past Papers Vault via IndexedDB (`idb`)**:
   - Automatically caches opened NCTB board question papers and answers into `idb`.
   - Allows students to read question papers, practice offline, and submit answers that queue for background synchronization.
5. **Real-Time Connectivity & Lifecycle Prompts**:
   - Dignified Bengali update prompt banner: "অগ্রযাত্রার নতুন সংস্করণ উপলব্ধ • আপডেট করুন" with reload trigger.
   - Real-time offline indicator chip with zero emojis and SVG network badges.
   - Dedicated, fully-styled `/offline` fallback page containing browsable offline papers and retry action.

---

## 2. Developer Architecture Note
Every created or modified file must include the mandatory header:
```typescript
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      [File Path]
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   [Architectural Purpose]
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */
```

---

## 3. Best Tech Selection
- **Workbox-grade Native Service Worker**: Multi-tiered Cache API strategy (Precache App Shell, Cache-First for fonts/static, Stale-While-Revalidate for board question papers, Network-First with navigation fallback).
- **IndexedDB via `idb`**: Transactional, typed offline store (`slc_offline_papers_db`) for past papers, exam question caches, and offline synchronization queue.
- **PWA Lifecycle Hooks**: `beforeinstallprompt` interception for human-made install modal/banner, `waiting` Service Worker state detection with reload trigger.
- **Next.js & Browser Optimizations**: Resource hints (`dns-prefetch`, `preconnect`), font subsetting with `font-display: swap`, viewport-fit=cover, and zero-CLS page headers.

---

## 4. Architectural Components
1. `frontend/public/manifest.json`: Web app manifest with Oxford Academic Navy theme `#090D16`, icons, shortcuts, and display `standalone`.
2. `frontend/public/sw.js`: Workbox-grade Service Worker with multi-tiered caching strategies, navigation fallback, and `SKIP_WAITING` message handling.
3. `frontend/src/lib/offline/offline-papers-store.ts`: Typed IndexedDB vault (`idb`) for offline board papers, search, and reading state.
4. `frontend/src/components/pwa/PwaUpdateToast.tsx`: Non-intrusive, accessible toast notifying user when a new Service Worker is waiting.
5. `frontend/src/components/pwa/PwaInstallBanner.tsx`: Dignified install promotion banner respecting user dismissal.
6. `frontend/src/components/pwa/OfflineIndicator.tsx`: Real-time network status pill with SVG indicators and auto-reconnect sync.
7. `frontend/src/pages/offline.tsx`: Dedicated offline portal with cached papers browser, offline quick search, and reconnect button.
8. `frontend/src/pages/_app.tsx`: Integrated SW registration, lifecycle listener, and offline indicator hooks.
9. `frontend/src/pages/_document.tsx`: Resource preconnects and mobile viewport meta.
10. `backend/tests/test_phase139_pwa_offline.py`: Comprehensive test suite verifying all Phase 139 features, headers, and zero-emoji compliance.
