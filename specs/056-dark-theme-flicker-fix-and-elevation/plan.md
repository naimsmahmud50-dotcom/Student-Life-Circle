# Implementation Plan: Retain Initial Dark Mode & Eliminate Theme Flash

## 1. Technical Strategy

### Synchronizing `_document.tsx` and `_app.tsx`
1. **`_document.tsx` Bootstrap Script**:
   - Ensure the inline bootstrap script adds `class="dark"` by default unless `localStorage.getItem('slc_theme') === 'light'` or `localStorage.getItem('theme') === 'light'`.
   ```javascript
   (function() {
     try {
       var saved = localStorage.getItem('slc_theme') || localStorage.getItem('theme');
       if (saved === 'light') {
         document.documentElement.classList.remove('dark');
       } else {
         document.documentElement.classList.add('dark');
       }
     } catch (e) {}
   })();
   ```
2. **`_app.tsx` Hydration Synchronization**:
   - Update `useEffect` to match `_document.tsx`:
   ```tsx
   useEffect(() => {
     try {
       const savedTheme = localStorage.getItem('slc_theme') || localStorage.getItem('theme');
       if (savedTheme === 'light') {
         document.documentElement.classList.remove('dark');
       } else {
         // Default is Dark Mode - locks in the initial design
         document.documentElement.classList.add('dark');
       }
     } catch (e) {
       // LocalStorage access non-blocking catch
     }
   }, []);
   ```
3. **`Navbar.tsx` Theme Initial State**:
   - Default internal state is `'dark'`.
   - Update `handleToggleTheme` to cleanly write both `'slc_theme'` and `'theme'` keys.
4. **`Layout.tsx` Theme Initial State**:
   - Update default theme state to `'dark'` unless saved as `'light'`.

### Motion & Visual Polish
- Ensure `html` has `scroll-behavior: smooth` and transitions on `background-color` and `color` do not cause jarring flashes.
- Ensure all dark mode surfaces across `index.tsx`, `PageHeader.tsx`, `Footer.tsx` render with deep contrast and rich amber highlights.

## 2. Verification Protocol
1. TypeScript compilation check (`./frontend/node_modules/.bin/tsc --project frontend/tsconfig.json --noEmit`).
2. Automated test suite (`node --experimental-strip-types --test frontend/src/data/__tests__/goeduData.test.mjs frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs`).
3. Python zero-emoji audit.
4. Production build (`npm --prefix frontend run build`).
5. Live curl test on port 3002.
