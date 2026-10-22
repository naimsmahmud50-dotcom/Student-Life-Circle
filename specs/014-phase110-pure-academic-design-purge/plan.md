<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 110 Pure Academic Design System & Complete AI-Vibe Purge
FILE:      specs/014-phase110-pure-academic-design-purge/plan.md
PHASE:     Phase 110 - Pure Academic Visual Design Elevation
PURPOSE:   Purges all AI-generated neon artifacts, establishing a prestigious,
           human-crafted Oxford/Cambridge academic design system with zero emojis.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 110 — Pure Academic Design System & Complete AI-Vibe Purge

## Step 1: Design Tokens in `globals.css`
- Delete all neon radial gradients and cyber glow shadows (`--bg-radial-ambient` with neon colors, `glow-blue`, `glow-teal`, `glow-amber`).
- Set light canvas background to scholarly ivory/paper (`--bg-app: #FAFAF8`, `--bg-surface: #FFFFFF`).
- Set dark canvas background to deep ink slate (`--bg-app: #0B132B`, `--bg-surface: #111C3D`).
- Define explicit pure academic tokens:
  - `--color-oxford-navy: #0A2540`
  - `--color-academic-emerald: #065F46`
  - `--color-scholar-gold: #B45309`
  - `--color-paper-ivory: #FAFAF8`
  - `--color-ink-slate: #0B132B`
  - `--color-burgundy-crimson: #991B1B`
- Retain required legacy tokens for backward compatibility and test validation (`--text-main: #0F172A`, `--bg-app: #FAFAF8` with fallback note, Google Fonts loader with `display=swap`, `Noto Sans Bengali` fallback class, line-height 1.6 / 1.75).
- Define `.btn-3d-oxford`, `.btn-3d-emerald`, `.btn-paper-outline` utility classes.

## Step 2: Tailwind Theme Expansion in `tailwind.config.js`
- Configure `oxford: { 800: '#0E3357', 900: '#0A2540', 950: '#051329' }`.
- Configure `emerald: { 800: '#065F46', 900: '#044332' }`.
- Configure `scholar: { gold: '#B45309' }`.
- Configure `paper: { white: '#FFFFFF', ivory: '#FAFAF8' }`.
- Remove `glow-blue`, `glow-teal`, `glow-amber` box shadows; replace with authentic paper shadows and tactile depth shadows.
- Preserve backward-compatible tokens (`#0F172A`, `#2563EB`, `#0D9488`, `#D97706`, `#DC2626`, `#F8FAFC`, `Noto Sans Bengali`, `44px`).

## Step 3: Button Component Elevation in `button.tsx`
- Add variants: `oxford`, `emerald`, `academic`, `paper` alongside existing `default`, `brand`, `teal`, `destructive`, `outline`, `ghost`.
- Default to prestigious Oxford Navy 3D tactile button physics.
- Enforce strict 44px / 48px touch ergonomics, Lucide `Loader2` spinner with `animate-spin`, Radix `@radix-ui/react-slot`.

## Step 4: Component Reskinning (`Navbar.tsx`, `Footer.tsx`, `index.tsx`)
- Reskin `Navbar.tsx`:
  - Brand logo: Oxford Navy with 3D tactile feel (`bg-[#0A2540]`).
  - Active stage badge: crisp border `border-slate-200/80 dark:border-slate-800/80 bg-slate-100/80 dark:bg-slate-900/80 text-slate-800 dark:text-slate-200`.
  - Sign-in button: 3D Oxford Navy tactile button (`bg-[#0A2540] hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`).
- Reskin `Footer.tsx`:
  - Deep Ink Slate ground (`bg-[#0B132B]`).
  - Academic accents: Emerald (`#065F46`), Gold (`#B45309`), Oxford Navy.
- Reskin `index.tsx`:
  - Eradicate `bg-gradient-to-r from-blue-600 via-indigo-600 to-teal-600`.
  - Eradicate `bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950/90`.
  - Eradicate `bg-gradient-to-r from-blue-600 to-indigo-600`.
  - Replace all with tactile 3D Oxford Navy buttons, Academic Emerald badges, and crisp hairline borders (`border-slate-200/80`).

## Step 5: Test Automation & Full Platform Regression
- Create `backend/tests/test_phase110_pure_academic_design.py`.
- Run zero-emoji sweep, AST security sweep, Phase 110 unit tests, and full regression discovery.
