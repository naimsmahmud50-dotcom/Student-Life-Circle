<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 120 Grand Nationwide Rollout & Public Launch Sign-off
FILE:      specs/024-phase120-grand-nationwide-rollout/spec.md
PHASE:     Phase 120 - Grand Nationwide Rollout & Public Launch Sign-off
PURPOSE:   Establishes production readiness sign-off criteria, institutional about/terms
           pages, SRE deploy script health certification, and formal attestation.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Specification: Phase 120 — Grand Nationwide Rollout & Public Launch Sign-off

## 1. Background & Mission
Phase 120 represents the final master milestone and public launch certification for **অগ্রযাত্রা (Ogrojatra) — Student Life Circle**, Bangladesh's first national unified sovereign educational operating system. Over 120 exhaustive development phases, the platform has achieved:
- Complete NCTB curriculum coverage (Classes 6-12 and University Admission).
- Real-time psychometric testing, adaptive CAT exams, handwritten script OCR grading, and Gale-Shapley college admission matching.
- Guardian trust console, offline P2P classroom mesh, and collaborative question moderation tribunals.
- Pure Academic Design System (#0A2540 Oxford Navy, #FFFFFF Pure Paper White, #FAFAF8 Warm Ivory) with a complete AI-vibe purge and 100% zero-emoji enforcement.

This phase provides:
1. **Production SRE Deploy Health Script (`deploy.sh`)**:
   - Automated `./deploy.sh health` execution certifying Nginx HTTP/3 QUIC, WebSocket readiness, zero service_role secret leaks, and security audits.
2. **Institutional Overview (`frontend/src/pages/about.tsx`)**:
   - Dignified editorial presentation of the platform's vision, NCTB alignment, pedagogical philosophy, and sovereign open architecture.
3. **Institutional Terms of Service & Privacy (`frontend/src/pages/terms.tsx`)**:
   - Scholarly privacy charter guaranteeing student data sovereignty, zero facial video proctoring, and fair dispute arbitration.
4. **National Launch Attestation (`NATIONAL_LAUNCH_ATTESTATION.md`)**:
   - Formal executive release sign-off certifying 120 phases implemented, 1,380+ tests passing, zero critical vulnerabilities, and WCAG 2.2 AAA compliance.

---

## 2. Functional Requirements
- **FR-120.1 (Production SRE Script)**:
  - `./deploy.sh health` performs rigorous automated checks:
    - Verifies Python and Node environments.
    - Runs zero-emoji sweep (`run_zero_emoji_sweep.py`).
    - Runs security sweep (`run_security_sweep.py`).
    - Verifies test discoverability and passes with exit code 0.
- **FR-120.2 (Institutional About Page)**:
  - Pure Academic Palette (#0A2540 Oxford Navy, #FAFAF8 Ivory).
  - Scholarly seals, pedagogical principles, technical architecture pillars, and governance transparency.
  - Zero emojis, 100% Lucide vector SVG icons.
- **FR-120.3 (Institutional Terms of Service)**:
  - Formal student privacy protections, proctoring integrity privacy guarantees (zero video storage), and guardian consent escrow protocols.
- **FR-120.4 (National Launch Attestation)**:
  - Comprehensive markdown attestation at repository root (`NATIONAL_LAUNCH_ATTESTATION.md`).
- **FR-120.5 (Automated Test Suite)**:
  - `backend/tests/test_phase120_grand_nationwide_rollout.py` asserts all public pages, attestation documentation, deploy script execution, and zero emojis.

---

## 3. Success Metrics
- 1,390+ automated tests passing with 0 errors and 0 failures.
- Zero-emoji sweep passes with 0 violations across 550+ files.
- Security sweep passes with 0 vulnerabilities.
