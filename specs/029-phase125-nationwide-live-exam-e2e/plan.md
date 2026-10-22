# IMPLEMENTATION PLAN: Phase 125 — Nationwide Live Exam & Playwright E2E Journey

## Architecture Strategy
1. **Playwright Config Hardening (`frontend/playwright.config.ts`)**:
   - Add standardized Developer Architecture Note header for Phase 125.
   - Retain all matrix viewports (Chromium, Firefox, WebKit, Pixel 7, iPhone 14) and reporter outputs (List, HTML, JSON).
   - Configure sub-second latency thresholds and headless test execution.

2. **Exam Arena & Submission Integration (`frontend/src/pages/practice.tsx`)**:
   - Provide 10 comprehensive NCTB HSC Physics questions with KaTeX equations.
   - Add a tactile 3D submit button ("খাতা জমা দিন") on completion/final question with physical bottom ledge (`shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`).
   - Add an instant score evaluation and Socratic hint breakdown modal/card upon script submission.
   - Ensure submission sends `X-Idempotency-Key` via `apiClient`.

3. **Playwright E2E Test Suite (`frontend/e2e/nationwide_exam_journey.spec.ts`)**:
   - Test TC-NAT-01: Multi-device (Desktop + Mobile Pixel 7 / iPhone 14) Student Login & OTP verification.
   - Test TC-NAT-02: Enter Live HSC Physics Challenge arena with server countdown timer.
   - Test TC-NAT-03: Solves 10 NCTB physics questions with KaTeX equations and 3D tactile button interaction.
   - Test TC-NAT-04: Network disconnection resilience (`context.setOffline(true)`), offline local buffer validation, reconnection (`context.setOffline(false)`), and answer synchronization.
   - Test TC-NAT-05: Final exam script submission ("খাতা জমা দিন") asserting `X-Idempotency-Key` header and instant result with Socratic breakdown.
   - Test TC-NAT-06: Strict Zero-Emoji and WCAG 2.2 AAA ergonomics audit across all rendered pages.

4. **K6 National Load Profile Hardening (`tests/load/k6_national_exam.js`)**:
   - Update with Phase 125 Developer Architecture Note header.
   - Confirm ramping scenario: 0 -> 15k (60s), surge -> 50k (30s), sustain 50k (5m), cool-down (60s).
   - Enforce sub-second latency SLAs (p95 < 200ms, p99 < 500ms, error rate < 1%, zero dropped submissions).
   - Enforce idempotency header (`X-Idempotency-Key`) and zero-emoji compliance.

5. **Python Verification Test (`backend/tests/test_phase125_nationwide_live_exam.py`)**:
   - Test existence and Developer Architecture Note headers on all 4 target files.
   - Validate Playwright config matrix (desktop browsers + mobile devices, reporters, timeouts).
   - Validate E2E test structure (all 6 test cases, 10 KaTeX questions, offline test, idempotency, zero-emoji).
   - Validate k6 script thresholds and stages.
   - Execute full platform test discovery certifying 1,411+ passing tests with 0 failures and 0 errors.
