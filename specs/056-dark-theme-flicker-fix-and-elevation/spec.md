# Feature Specification: Retain Initial Dark Mode & Eliminate Theme Flash

## 1. Problem Diagnosis & Root Cause
The user reported:
> "link a click korar prtohom akta design ashe abr cole jay oi design ta maybe bettar output dibe ... prothome kon design ta ashe seitai rakho aisa ami chack dibo do it your best output"

### Root Cause Analysis:
1. **The Flash**:
   - `_document.tsx` executes an inline bootstrap script during initial HTML parsing:
     ```javascript
     var saved = localStorage.getItem('slc_theme') || localStorage.getItem('theme');
     var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
     if (saved === 'dark' || (!saved && prefersDark)) {
       document.documentElement.classList.add('dark');
     }
     ```
   - On modern OS environments with dark mode preferences, this immediately activates **Dark Mode**.
   - As a result, the user sees the Dark Mode design first.
   - However, in `_app.tsx`, client hydration executed an inconsistent `useEffect`:
     ```tsx
     if (savedTheme === 'dark') {
       document.documentElement.classList.add('dark');
     } else {
       // Light paper theme is the default
       document.documentElement.classList.remove('dark');
     }
     ```
   - When `savedTheme` was not explicitly set in `localStorage`, `_app.tsx` forcibly stripped the `dark` class from `document.documentElement`, causing the dark design to abruptly vanish ("cole jay") and snap to light theme.
2. **User Desire**:
   - The user noticed the initial dark design before the snap and determined it provides a much better aesthetic output ("oi design ta maybe bettar output dibe").
   - The user explicitly requested to identify which design appears first and lock it in permanently ("prothome kon design ta ashe seitai rakho").

## 2. Solution Requirements
- **FR-01 (Lock Initial Theme)**: Set Dark Mode as the primary default across `_document.tsx`, `_app.tsx`, `Navbar.tsx`, `Layout.tsx`, and all theme toggles.
- **FR-02 (Zero-Flicker Synchronized Bootstrapping)**: `_document.tsx` and `_app.tsx` must use identical logic so that if no explicit user preference is saved, Dark Mode remains permanently active without any FOIT (Flash of Incorrect Theme) or visual transition.
- **FR-03 (Dark Mode Polish & Elevation)**: Ensure all dark theme styles across the application have:
  - Deep obsidian & dark charcoal surfaces (`#0B0F19`, `#0F172A`, `#121B2D`).
  - Luminous golden amber accents (`#ED8E22`, `#FBBF24`).
  - High-contrast crisp typography adhering to WCAG 2.2 AAA.
  - Smooth hardware-accelerated motion via `LazyMotion` and `domAnimation`.
  - Harmonious integration with the deep pine emerald footer.
- **FR-04 (User Theme Toggle Integrity)**: If a user explicitly clicks the theme toggle to select `'light'`, that preference must be saved to `localStorage` and respected without conflicting bootstrap logic.

## 3. Strict Quality & Policy Guardrails
- **Zero-Emoji Policy**: Zero emojis anywhere in code, comments, or UI.
- **Port Discipline**: Exclusively running on port 3002.
- **Verification**: TypeScript check, 45 automated tests, production build, live curl checks.
