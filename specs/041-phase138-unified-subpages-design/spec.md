# SPECIFICATION: Phase 138 — Unified Premium Design for Sub-pages

## 1. Executive Summary & Goal
The goal of **Phase 138** is to eradicate design fragmentation across all sub-pages of "Student Life Circle" (অগ্রযাত্রা) by establishing ONE unified, shared academic design system derived from the flagship Linear/Vercel-inspired homepage. 

This brings the prestigious Oxford Academic Navy palette, 3D physical tactile button physics, deliberate typographic hierarchy, polished empty/loading/error states, and consistent page architecture across every core inner page (`/practice`, `/board-archives`, `/quiz`, `/modules`, `/learn`, `/dashboard`).

---

## 2. Developer Architecture Note
Every created or modified file must include the mandatory header:
```
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      [File Path]
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   [Architectural Purpose]
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */
```

---

## 3. Inconsistency Audit Findings

1. **Background & Color Tokens**:
   - Homepage uses `--bg-app` (`#FAFAF8` in light, `#090D16` / `#0B132B` in dark) with subtle ambient light gradients (`blur-3xl`).
   - Inner pages (such as `/practice`, `/board-archives`, `/modules`) inconsistently used hardcoded `bg-[#F9FAF9]`, `bg-slate-50/50`, or custom dark backgrounds, breaking visual continuity.
2. **Header Consistency**:
   - Homepage features an authoritative editorial hero with an accreditation chip, bold Bengali typography, and micro-trust indicators.
   - Inner pages had inconsistent header patterns: `/modules` had an inline non-standard `<header>` without the unified `Navbar`, while `/board-archives` had an ad-hoc local `theme` toggle state conflicting with the global theme.
3. **Missing Reusable Form & State Primitives**:
   - Pages lacked unified `Input`, `Select`, `Skeleton`, `EmptyState`, and `ErrorState` components, causing fragmented styling of search inputs, dropdowns, and loading placeholders.
4. **Button & Tactile Physics**:
   - Homepage uses Duolingo/Linear-grade 3D physical press physics (`shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`).
   - Several sub-pages had flat Tailwind buttons or inconsistent shadow depths.

---

## 4. Unified Design System Specification

### 4.1. Color Tokens & Theme Architecture
- **Oxford Academic Navy**: `#0A2540` (Primary Action, Brand Identity)
- **Deep Oxford Depth**: `#051329` (3D Physical Button Bottom Shadow)
- **Academic Emerald**: `#065F46` (Mastery, Verified Skills, Success States)
- **Scholar Gold / Amber**: `#B45309` (Deadlines, Honors, Accents)
- **Paper Ivory / Slate Ground**: `#FAFAF8` (Light App Ground), `#090D16` / `#0B132B` (Linear Dark App Ground)
- **Surface Elevation**: `#FFFFFF` (Light Surface), `#0F172A` / `#16203D` (Dark Elevated Surface)
- **Architectural Borders**: `#E2E8F0` / `border-slate-200/80` (Light), `#1E293B` / `border-slate-800/80` (Dark)

### 4.2. Typography Hierarchy
- **Bengali Primary**: `font-bengali` (`Hind Siliguri`, `Noto Sans Bengali`) with line-height 1.6–1.75 ensuring zero clipped conjuncts (যুক্তাক্ষর).
- **Latin Display**: `font-display` (`Plus Jakarta Sans`, `Inter`).
- **Tabular Numerals**: `tabular-numbers` (`font-mono`) for countdowns, marks, and statistics.

### 4.3. Reusable Component Suite (`components/ui`)
1. **`Button`**: 3D tactile physics, sizes (`sm`, `md`, `lg`), variants (`oxford`, `emerald`, `paper`, `outline`, `ghost`, `danger`), loading state with accessible spinner.
2. **`Card`**: Elevated surface, subtle architectural hairline border, hoverable lift effect.
3. **`Input`**: High-contrast, tactile focus ring, prefix/suffix icons, accessible error description.
4. **`Select`**: Custom accessible dropdown with chevron indicator, dark/light variants.
5. **`Badge`**: Pill chips with semantic icons (Zero-Emoji).
6. **`Modal` & `Dialog`**: Radix-based accessible modal with smooth backdrop blur and focus trap.
7. **`Tabs`**: Radix-based keyboard arrow navigation with high-contrast active indicator.
8. **`Skeleton`**: Subtle shimmer loading state respecting `prefers-reduced-motion`.
9. **`EmptyState`**: Dignified academic empty state with Lucide vector icon and call-to-action button.
10. **`ErrorState`**: Clear error presentation with retry action and error details.
11. **`PageHeader`**: Unified layout banner with ambient lighting, breadcrumbs, NCTB badge chip, and action slot.

---

## 5. Rebuilt Core Pages
- **`/practice`**: Unified practice and adaptive quiz arena utilizing `PageHeader`, `OptionCard`, `Button`, `Skeleton`, and `ErrorState`.
- **`/board-archives`**: Rebuilt with unified global theme, `PageHeader`, `Input`, `Select`, `Card`, and `EmptyState`.
- **`/modules`**: Standardized with flagship `Navbar`, `Footer`, `PageHeader`, and unified card styling.
- **`/learn`**: Upgraded with unified tabs, chapter cards, and tactile button actions.
- **`/dashboard`**: Unified student command center with consistent tokens and components.

---

## 6. Verification Criteria
- Zero console errors, zero dead code, strict TypeScript compliance.
- 100% Zero-Emoji compliance across all modified and created files.
- All backend tests continue to pass (1,525+ tests).
- Next.js production build compiles all 37/37 static pages with zero type or lint errors.
- Verified live responsiveness across 320px, 768px, 1024px, 1440px, and 1920px.
