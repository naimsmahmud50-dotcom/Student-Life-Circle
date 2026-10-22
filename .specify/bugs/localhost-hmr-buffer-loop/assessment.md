# Bug Assessment: Localhost HMR Buffering Loop & Dev Server Unresponsiveness

- **Slug**: localhost-hmr-buffer-loop
- **Created**: 2026-10-19T11:48:00+06:00
- **Updated**: 2026-10-19T12:12:00+06:00
- **Source**: 
  - Screencast video 1: `/home/mahmud-hasan/Videos/Screencasts/error/Screencast From 2026-10-19 11-37-16.webm`
  - Screencast video 2: `/home/mahmud-hasan/Videos/Screencasts/Screencast From 2026-10-19 11-50-14.webm`
  - User error screenshot: `media_1792389679458_bb6255ad.png`
- **Verdict**: valid
- **Severity**: critical

## Forensic Evidence & Error Analysis

The user screenshot (`media_1792389679458_bb6255ad.png`) and screencast 2 captured the exact Next.js 15 dev overlay:

```text
Recoverable Error:
Hydration failed because the server rendered text didn't match the client.
> <span suppressHydrationWarning className="font-bold text-lg leading-tight tracking-tight text-slate-900 dark:text-w...">
+ header.brand_title
- "অগ্রযাত্রা"
src/components/layout/Navbar.tsx (76:17) @ Navbar
```

Notice the top right badge: `🔴 Next.js 15.5.28 (outdated) Webpack`.

## Suspected Code Paths & Root Cause

1. **Hydration Asynchrony on `t('header.brand_title')`**:
   - `Navbar.tsx` relied on `t('header.brand_title')` from `useTranslation()`.
   - On the server, `t()` returned `"অগ্রযাত্রা"`.
   - On the client during the initial hydration pass before provider synchronization, or when running cached JS chunks from disk, `t()` returned the raw dot-notated fallback string `'header.brand_title'`.
   - In Next.js 15, any text mismatch inside a Client Component triggers `Hydration failed because the server rendered text didn't match the client`.
2. **Fast Refresh Error Overlay Persistence**:
   - Once Next.js mounts the full-screen error modal, it flags the client compilation as `(outdated)` and traps the viewport in an active error state until dismissed or hard-reloaded.
3. **PWA Service Worker & Disk Chunk Caching**:
   - Old service worker and HTTP disk caches continued serving obsolete webpack chunks, creating an infinite reload and unstyling cycle.

## Remediation Plan

1. **Eliminate Dynamic Token Lookups in `Navbar.tsx`**:
   - Replace all `t('header.brand_title')`, `t('nav.*')`, `t('header.*')` calls in `Navbar.tsx` with deterministic `{isBengali ? 'অগ্রযাত্রা' : 'Ogrojatra'}` and `{isBengali ? ... : ...}` ternaries.
   - This physically eliminates `header.brand_title` from ever existing or being emitted in `Navbar.tsx`.
2. **Add `Clear-Site-Data` in `next.config.js`**:
   - Instruct Chrome to automatically purge all Service Workers and storage for `/sw.js` and development assets.
   - Enforce `Cache-Control: no-cache, no-store, must-revalidate` for all static assets in dev mode.
3. **Built-in Fallbacks in `i18n.ts`**:
   - Provide static `BUILTIN_FALLBACKS` so `t()` never returns raw keys under any circumstance.
4. **Automated Verification**:
   - Inspect DOM and verify `data-error="false"`, `Hydration failed = False`, and 0 console errors in headless browser.
