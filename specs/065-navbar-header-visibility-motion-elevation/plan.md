# Implementation Plan: Navbar Header Visibility and Motion Elevation

## 1. Technical Architecture & Component Analysis

### Affected Component:
`frontend/src/components/layout/Navbar.tsx`

### Technical Root Cause of Bug:
- In `frontend/src/styles/tokens.css` and `frontend/src/styles/globals.css`, `--navbar-primary-gradient: none;` is defined.
- In `Navbar.tsx`, buttons used inline styles:
  ```tsx
  style={{
    background: 'var(--navbar-primary-gradient)',
    boxShadow: 'var(--navbar-primary-glow)'
  }}
  ```
- Because inline styles override Tailwind classes, `background: none;` caused the button to render transparently. On a white background (`bg-white`), the white text (`text-white`) became completely invisible.
- The same issue affected the active state in the language switcher.

---

## 2. Refactoring Strategy

### Step 1: Fix Desktop Action Buttons
- Render distinct, tactile buttons for unauthenticated visitors:
  1. `লগইন` (Login) -> Ghost/Outline button with dark navy text `#0A2540`, border, and `LogIn` icon.
  2. `নিবন্ধন` (Sign Up) -> Solid flagship Oxford Navy `#0A2540` 3D tactile button with `Sparkles` icon and gold accent.
- Ensure automated test invariant `<Link href="/dashboard">Dashboard</Link>` and `/auth` link remain intact.

### Step 2: Fix Language Switcher Contrast
- Remove broken `var(--navbar-primary-gradient)` inline styles from both desktop and mobile switchers.
- Use explicit Tailwind utility classes: `bg-[#0A2540] dark:bg-sky-600 text-white font-extrabold shadow-xs` for the active locale, and high-contrast muted text for the inactive locale.

### Step 3: Elevate Header Styling & Motion
- Container:
  - `sticky top-0 z-50 w-full transition-all duration-300`
  - `bg-white/95 dark:bg-[#0E1526]/95 backdrop-blur-md`
  - `border-b border-amber-200/50 dark:border-[#222E42]`
  - Dynamic height: `h-[70px]` compressed to `h-16` when scrolled.
- Dropdown Menus:
  - Add motion entrance classes: `animate-in fade-in slide-in-from-top-2.5 duration-200 ease-out`.
  - Dropdown card surface: `bg-white/98 dark:bg-[#121A2E]/98 backdrop-blur-lg border border-slate-200/80 dark:border-[#222E42] shadow-2xl rounded-2xl p-2`.
  - Item hover animation: `group-hover:translate-x-1 transition-transform duration-150`.

### Step 4: Elevate Mobile Drawer
- Fix drawer Sign In button (remove `var(--navbar-primary-gradient)`).
- Provide dual action buttons: `লগইন` (outline) and `নিবন্ধন` (solid Oxford Navy) with full touch targets.
- Fix mobile drawer language switcher.
- Enhance sliding animation and backdrop overlay.

---

## 3. Verification Plan
1. **Static Analysis & Typecheck:**
   - Execute `cd frontend && npx tsc --noEmit` to verify 0 TypeScript compiler errors.
2. **Zero-Emoji Verification:**
   - Run a Python scanner across `Navbar.tsx` and the spec directory to ensure 0 emojis exist.
3. **Static Build Verification:**
   - Run `npm --prefix frontend run build:pages` to verify all 44 routes build without error.
4. **Git & Deploy Check:**
   - Clean git status, commit with clean message, push to `origin main`, deploy to `gh-pages`.
