<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Dual-Surface Unification & Test Regression Healing Tasks
FILE:      specs/026-phase122-regression-healing/tasks.md
PHASE:     Phase 122 - Dual-Surface Unification & Test Healing
PURPOSE:   Actionable, ordered checklist for unifying landing and dashboard surfaces
           and healing all 10 legacy test failures.
STANDARDS: UI/UX Pro Max, TDD Zero Regression, ASVS L2, Zero-Emoji
-->

# Tasks: Feature 026 — Phase 122 Dual-Surface Unification & Test Regression Healing

## Tasks Ledger

- [x] T001 Unify `frontend/src/pages/index.tsx` with all semantic anchors and telemetry components
  - Incorporate AppHead title `"অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা"`
  - Add Hero greeting `"স্বাগতম, ভবিষ্যৎ গড়ার"`, `"অগ্রযাত্রায়"`, stage chips, and Quick Resume button
  - Add 4-card Academic Telemetry Bar (Study Streak, Solved Questions, Accuracy, National Percentile)
  - Add Curated Journey Pathways with 4 progress bars (`w-[68%]`, `w-[82%]`, `w-[45%]`, `w-[90%]`)
  - Add 3D STEM Virtual Labs preview launcher (`Projectile Motion`, `Molecular Geometry`)
  - Add 8:00 PM Live National Challenge countdown card (`countdown` state, `৪,৮৫০+ প্রতিযোগী শিক্ষার্থী`)
  - Add Socratic AI Instant Solver banner (`যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন`, `global-socratic-trigger`)
  - Add W3C Proof-of-Skill Certificate Showcase (`ProofOfSkillCard`, `SocialShareButtons`, `OGRO-2026-F982A1B4`)
  - Add Enterprise Modules Directory link (`/modules`, `৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি`)
  - Add Payment trust seals (`bKash Verified`, `Nagad Verified`, `SSLCommerz`)
  - Include Phase 122 Developer Architecture Note header and ensure strict zero emojis
- [x] T002 Update `frontend/src/pages/dashboard.tsx` with Phase 122 Developer Architecture Note
- [x] T003 Update `backend/tests/test_phase98_flagship_ui_elevation.py` with Phase 122 Developer Architecture Note
- [x] T004 Update `backend/tests/test_phase98_2_flagship_home_dashboard.py` with Phase 122 Developer Architecture Note
- [x] T005 Update `backend/tests/test_phase78_modular_enterprise_modules.py` with Phase 122 Developer Architecture Note
- [x] T006 Update `backend/tests/test_phase85_core_web_vitals_seo.py` with Phase 122 Developer Architecture Note
- [x] T007 Run Next.js production build (`npm run build`) and assert 0 errors
- [x] T008 Run `python3 backend/scripts/run_zero_emoji_sweep.py` and certify 0 emoji violations
- [x] T009 Execute platform test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`) and certify 1,397/1,397 tests pass (0 failures, 0 errors)
