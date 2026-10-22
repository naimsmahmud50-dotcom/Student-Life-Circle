# TASKS: Phase 125 — Nationwide Live Exam & Playwright E2E Journey

- [ ] Task 1: Update `frontend/playwright.config.ts` with Phase 125 Developer Architecture Note and headless execution matrix.
- [ ] Task 2: Enhance `frontend/src/pages/practice.tsx` to include 10 HSC Physics KaTeX questions, offline buffering, tactile 3D "খাতা জমা দিন" button, and instant score with Socratic breakdown.
- [ ] Task 3: Implement `frontend/e2e/nationwide_exam_journey.spec.ts` covering Login -> OTP -> Challenge Entry -> 10 KaTeX questions -> Offline Buffer -> Reconnect -> Idempotent Submission -> Socratic Breakdown.
- [ ] Task 4: Hardened `tests/load/k6_national_exam.js` with Phase 125 Developer Architecture Note and sub-second latency thresholds.
- [ ] Task 5: Implement `backend/tests/test_phase125_nationwide_live_exam.py` validating all Phase 125 requirements.
- [ ] Task 6: Run Playwright test suite `npx playwright test e2e/nationwide_exam_journey.spec.ts`.
- [ ] Task 7: Execute zero-emoji sweep across all created/modified files.
- [ ] Task 8: Run master test discovery `python3 -m unittest discover -s backend/tests -p "test_*.py"` certifying 1,411+ tests passing.
- [ ] Task 9: Generate final certification report `PHASE_125_NATIONWIDE_LIVE_EXAM_E2E_REPORT.md`.
