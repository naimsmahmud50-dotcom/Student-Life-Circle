# Tasks: Flagship UI/UX Elevation & Design Unification

## Task Checklist

- [x] **T655**: [US-FOOTER-COMPONENT] Implement comprehensive, dignified platform footer in `frontend/src/components/layout/Footer.tsx` featuring NCTB curriculum accreditation, bKash/Nagad verified payment badges, quick navigation links, and child privacy disclosures.
- [x] **T656**: [US-APP-SHELL-AND-I18N] Update `frontend/src/pages/_app.tsx` to wrap the entire component tree with `I18nProvider` from `@/lib/i18n`, ensuring zero-reload language switching and persistent floating `SocraticTutorDrawer` across every route.
- [x] **T657**: [US-FLAGSHIP-HOME-DASHBOARD] Completely overhaul `frontend/src/pages/index.tsx` into an inspiring, world-class EdTech dashboard featuring:
  - Dynamic Hero Banner with quick-resume CTA and stage switcher.
  - 4-card Academic Telemetry Bar (Daily Streak, Questions Solved, Accuracy, Percentile Rank).
  - Curated Journey Pathway Cards (HSC Science, Admission Prep, Tuition, Career).
  - 3D STEM Virtual Labs Spotlight with direct interactive simulators.
  - Live Challenge Arena countdown spotlight.
  - Socratic AI instant question solver callout.
  - W3C Proof-of-Skill Certificate Showcase with 1-click social sharing.
  - Official bKash/Nagad trust & payment gateway seals.
- [x] **T658**: [US-SUB-PAGES-UNIFICATION] Unify and elevate `learn.tsx`, `practice.tsx`, `live-challenge.tsx`, `admission.tsx`, `tuition.tsx`, and `career.tsx` with the unified `Navbar`, `Footer`, sub-pixel typography, and cohesive design tokens.
- [x] **T659**: [US-TESTS-AND-VERIFICATION] Implement automated test suite in `backend/tests/test_phase98_flagship_ui_elevation.py` asserting unified layout shell, dashboard components, footer integration, zero-emoji compliance, and developer architecture notes.
- [x] **T660**: [US-MASTER-TESTS-RUN] Run full platform test discovery verifying all tests pass with 0 errors and 0 failures.

## Phase 2: World-Class Typography & Tactile Button Polish (Brilliant / Linear Caliber)

- [x] **T661**: [US-TYPOGRAPHY-FONTS] Inject 'Hind Siliguri', 'Plus Jakarta Sans', and 'Inter' alongside 'Noto Sans Bengali' in `frontend/src/pages/_document.tsx` and `frontend/src/styles/globals.css`.
- [x] **T662**: [US-TAILWIND-CONFIG] Extend `frontend/tailwind.config.js` with `fontFamily.display`, `fontFamily.bengali`, and tactile shadow tokens.
- [x] **T663**: [US-BUTTON-PRIMITIVE] Upgrade `frontend/src/components/ui/button.tsx` with Brilliant/Linear tactile physics, spring transitions, and accessible touch targets.
- [x] **T664**: [US-DASHBOARD-TYPE-POLISH] Polish typography and tactile button states across `frontend/src/pages/index.tsx`.
- [x] **T665**: [US-VERIFICATION-REGRESSION] Run full test suite (`python3 -m unittest discover -s backend/tests`) and zero-emoji sweep to guarantee 100% pass rate.

