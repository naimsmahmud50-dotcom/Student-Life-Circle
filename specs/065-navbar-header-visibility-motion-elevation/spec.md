# Feature Specification: Navbar Header Visibility and Motion Elevation

## 1. Overview & Objective
Elevate the main application header and navigation bar (`frontend/src/components/layout/Navbar.tsx`) to resolve critical button invisibility issues and introduce world-class motion, tactile physics, and atmospheric frosted glass aesthetics.

### Key Problems Addressed:
1. **Button Invisibility Bug:**
   - Previous inline styles `style={{ background: 'var(--navbar-primary-gradient)' }}` evaluated to `background: none;` (defined in CSS tokens), stripping button backgrounds and rendering white text directly on a light white header background.
   - Users were unable to locate the Login and Sign In / Register controls.
2. **Missing Dual-Action Clarity:**
   - Instead of a single ambiguous link, users require distinct, tactile buttons for Login (লগইন) and Sign Up / Register (নিবন্ধন / শুরু করুন).
3. **Motion & Visual Elevation:**
   - Header requires smooth 70px to 64px scroll compression with frosted glass backdrop blur.
   - Interactive dropdown menus (`Learn`, `More`) need smooth spring-inspired motion entrance (`fade-in`, `slide-in-from-top-2.5`) with hover translation on list items.
   - Language switcher `[ BN | EN ]` needs high-contrast solid active state without broken CSS token dependencies.
   - Mobile drawer must feature high-contrast dual buttons and smooth sliding drawer motion.

---

## 2. Functional Requirements

### FR-1: 100% High-Contrast Authentication Controls
- Provide TWO clearly separated authentication actions for unauthenticated visitors:
  1. **Login (লগইন):**
     - Tactile outline/ghost button with rich dark navy text `#0A2540` (light mode) and crisp slate `#F1F5F9` (dark mode).
     - Distinct `LogIn` icon with 1.75 stroke width.
     - Target route: `/auth?mode=login` (or `/auth`).
  2. **Register / Get Started (নিবন্ধন / শুরু করুন):**
     - Solid Oxford Navy flagship button (`#0A2540` light, sky-to-indigo gradient in dark mode).
     - Tactile 3D shadow `shadow-[0_3px_0_0_#051329]` with `active:translate-y-0.5 active:shadow-none`.
     - Sparkles icon (`Sparkles` in `#FBBF24` amber gold).
     - Target route: `/auth?mode=register` (or `/auth`).
- Both buttons must achieve WCAG 2.2 AAA contrast ratio (>= 7:1) against both white and dark header surfaces.

### FR-2: Language Switcher Contrast Fix
- The `[ BN | EN ]` segmented control must not rely on `--navbar-primary-gradient`.
- Active language pill receives solid `#0A2540` (light) or `#0284C7` (dark) with crisp white text.
- Inactive language pill receives muted text `#4B5563` with hover state.

### FR-3: Header Motion & Glass Atmospheric Elevation
- Sticky header container features `backdrop-blur-md bg-white/95 dark:bg-[#0E1526]/95`.
- Subtle bottom accent border (`border-b border-amber-200/50 dark:border-[#222E42]`).
- Smooth height compression from `h-[70px]` to `h-16` on scroll without layout shift.
- Mega-menu dropdowns animate with smooth micro-interactions on entrance and hover.

### FR-4: Mobile Drawer Parity & Visual Hierarchy
- Portal-mounted mobile drawer receives identical dual-action buttons (`লগইন` and `নিবন্ধন`).
- High-contrast language switcher and theme toggle at drawer footer.
- Smooth slide-in transition and backdrop blur scrim overlay.

---

## 3. Strict Scope & Quality Invariants
1. **Target File Lock:** Exclusively modify `frontend/src/components/layout/Navbar.tsx` and spec tracking files.
2. **Zero-Emoji Discipline:** Strictly zero emoji characters in all code, comments, specs, and commit messages. Pure Lucide SVG icons only.
3. **Accessibility:** Minimum 44px touch targets on mobile controls, full ARIA roles and labels, keyboard navigation support (Escape to close, Tab trapping in drawer).
