# SPECIFICATION: Phase 125 — Nationwide Live Exam & Playwright E2E Journey

## Overview
Phase 125 delivers an end-to-end multi-viewport Playwright automated test suite certifying the full student journey during high-stakes nationwide live examinations on Ogrojatra:
1. Student Login and SMS OTP Verification modal workflow.
2. Entry into the Nationwide HSC Physics Challenge arena (`/live-challenge` -> `/practice?challenge=active`).
3. 10 authentic NCTB Physics questions with KaTeX equations solved across desktop and mobile devices.
4. Flaky connection resilience: simulated network disconnect (`context.setOffline(true)`), local answer queue buffering, and reconnect verification (`context.setOffline(false)`).
5. Tactile 3D button submission ("খাতা জমা দিন") with cryptographically verified `X-Idempotency-Key` headers.
6. Instant score evaluation and Socratic hint breakdown.
7. Strict Zero-Emoji compliance and WCAG 2.2 AAA accessibility ergonomics.

## Target Files
- `frontend/playwright.config.ts`: Multi-browser (Chromium, Firefox, WebKit) and real-world mobile viewport matrix (Pixel 7, iPhone 14) configuration with headless execution.
- `frontend/e2e/nationwide_exam_journey.spec.ts`: Complete Playwright E2E test suite covering the 7-step student journey.
- `tests/load/k6_national_exam.js`: Hyper-scale distributed load testing script validating sub-second latency SLAs (p95 < 200ms, p99 < 500ms) under 50,000 concurrent students.
- `backend/tests/test_phase125_nationwide_live_exam.py`: Automated Python test suite certifying all Phase 125 assets, configurations, and invariants.

## Non-Functional Requirements & Governance
- ZERO AI VIBE: Live exam arena must remain tranquil, high-contrast, and scholarly under peak stress.
- Tactile Buttons: Option selection and "খাতা জমা দিন" action must have physical 3D button depth (`shadow-[0_4px_0_0_...]`).
- Zero Emoji Rule: Pure Lucide SVG vector icons only.
- Developer Architecture Note at the top of all 4 target files.
- 100% test pass rate across the full platform test suite (1,411+ tests).
