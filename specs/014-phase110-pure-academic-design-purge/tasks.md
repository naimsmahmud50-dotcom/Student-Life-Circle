<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 110 Pure Academic Design System & Complete AI-Vibe Purge
FILE:      specs/014-phase110-pure-academic-design-purge/tasks.md
PHASE:     Phase 110 - Pure Academic Visual Design Elevation
PURPOSE:   Purges all AI-generated neon artifacts, establishing a prestigious,
           human-crafted Oxford/Cambridge academic design system with zero emojis.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA Contrast
-->

# Tasks: Phase 110 — Pure Academic Design System & Complete AI-Vibe Purge

## Tasks Ledger

- [x] Task 1: Update `frontend/src/styles/globals.css` with Pure Academic Tokens
  - Purge neon radial gradients, cyan/indigo gradients, and cyber glow drop shadows
  - Inject `--color-oxford-navy: #0A2540`, `--color-academic-emerald: #065F46`, `--color-scholar-gold: #B45309`, `--color-paper-ivory: #FAFAF8`, `--color-ink-slate: #0B132B`
  - Maintain backward compatibility tokens and Google Fonts with `display=swap`
  - Add tactile 3D button utility classes (`.btn-3d-oxford`, `.btn-3d-emerald`, `.btn-paper-outline`)
- [x] Task 2: Update `frontend/tailwind.config.js` with Oxford Academic Palette
  - Configure `oxford`, `emerald`, `scholar`, `paper` color scales
  - Replace `glow-blue`, `glow-teal`, `glow-amber` with crisp paper shadows
  - Preserve backward compatible tokens (`#0F172A`, `#2563EB`, `#0D9488`, `#D97706`, `#DC2626`, `#F8FAFC`, `Noto Sans Bengali`, `44px`)
- [x] Task 3: Elevate Button Primitive in `frontend/src/components/ui/button.tsx`
  - Implement 3D Oxford Navy tactile buttons (`shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none hover:bg-[#0E3357]`)
  - Support pure paper secondary buttons (`bg-white text-slate-800 border border-slate-300 shadow-sm hover:bg-slate-50`)
  - Maintain all existing variant names (`default`, `brand`, `teal`, `destructive`, `outline`, `ghost`) and add `oxford`, `emerald`, `academic`, `paper`
  - Ensure 44px/48px touch targets and Loader2 spinning indicator
- [x] Task 4: Elevate `frontend/src/components/layout/Navbar.tsx`
  - Eradicate flashy blue glowing headers
  - Reskin with Oxford Navy brand icon, scholarly stage badge, and tactile 3D sign-in button
  - Verify zero emojis and pure Lucide SVG vector icons
- [x] Task 5: Elevate `frontend/src/components/layout/Footer.tsx`
  - Reskin with Deep Ink Slate (`#0B132B`) and Oxford Navy accents
  - Scholarly NCTB compliance bar, verified payment badges, and zero emojis
- [x] Task 6: Reskin Bento Dashboard in `frontend/src/pages/index.tsx`
  - Eradicate AI-vibe neon gradients (`bg-gradient-to-r from-blue-600 via-indigo-600 to-teal-600`, `bg-gradient-to-r from-blue-600 to-indigo-600`, etc.)
  - Upgrade hero CTA to tactile 3D Oxford Navy button
  - Ensure crisp architectural hairline rules (`border-slate-200/80` / `border-slate-800/80`)
  - Zero-emoji scan and 'Hind Siliguri' + 'Plus Jakarta Sans' typography
- [x] Task 7: Implement Automated Test Suite `backend/tests/test_phase110_pure_academic_design.py`
  - Test absence of forbidden neon glow classes in tailwind and globals
  - Test presence of Oxford navy, academic emerald, and scholar gold design tokens
  - Test button tactile 3D physics classes
  - Test zero emoji compliance across all Phase 110 files
  - Test mandatory Developer Architecture Note headers
- [x] Task 8: Execute Full Platform Regression Discovery (`python3 -m unittest discover -s backend/tests`)
  - Verify 100% pass rate across 1,326+ test cases
