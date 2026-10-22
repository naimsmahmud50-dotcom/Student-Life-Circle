<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 120 Grand Nationwide Rollout & Public Launch Sign-off
FILE:      specs/024-phase120-grand-nationwide-rollout/plan.md
PHASE:     Phase 120 - Grand Nationwide Rollout & Public Launch Sign-off
PURPOSE:   Implementation plan for SRE deployment script, institutional pages,
           national launch attestation certificate, and master verification suite.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 120 — Grand Nationwide Rollout & Public Launch Sign-off

## Work Breakdown Structure

1. **Production SRE Audit Script (`deploy.sh`)**:
   - Inspect and enrich `./deploy.sh` with a comprehensive `health` command:
     - Check environment prerequisites (Python 3.10+, Node/npm).
     - Run zero-emoji compliance sweep (`python3 backend/scripts/run_zero_emoji_sweep.py`).
     - Run platform security audit sweep (`python3 backend/scripts/run_security_sweep.py`).
     - Run Supabase security audit verification (`python3 backend/scripts/run_supabase_security_audit.py`).
     - Run full test suite discovery (`python3 -m unittest discover -s backend/tests`).
     - Provide clear ASCII exit status with zero emojis.

2. **Institutional Overview Page (`frontend/src/pages/about.tsx`)**:
   - Scholarly Oxford Navy and Warm Ivory layout.
   - Core Pillars:
     - জাতীয় শিক্ষাক্রমের পূর্ণাঙ্গ রূপান্তর (Comprehensive NCTB Alignment)
     - সার্বভৌম ও গোপনীয়তা-সুরক্ষিত প্রযুক্তি (Sovereign Privacy Architecture)
     - প্রান্তিক ও দুর্যোগকালীন অন্তর্ভুক্তি (Rural LoRaWAN & Offline P2P Mesh)
     - শিক্ষাবিদ ও পিয়ার-রিভিউ ট্রাইব্যুনাল (Academic Peer-Review Tribunal)
   - Prestigious seal branding and dignified typography ('Hind Siliguri' / Inter).
   - Zero emojis! 100% Lucide vector SVG icons.

3. **Institutional Terms of Service Page (`frontend/src/pages/terms.tsx`)**:
   - Scholarly legal framework:
     - শিক্ষার্থী ডেটা সার্বভৌমত্ব ও নিরাপত্তা (Student Data Sovereignty)
     - পরীক্ষা অখণ্ডতা ও নজরদারি-মুক্ত মূল্যায়ন (Zero-Video Proctoring Guarantee)
     - টিউশন এসক্রো ও অভিভাবক ট্রাস্ট সনদ (Tuition Escrow & Guardian Trust)
     - মেধা বৃত্তি ও নিরপেক্ষ গ্রেডিং আরবিট্রেশন (Merit Scholarships & Fair Dispute Arbitration)
   - Zero emojis! 100% Lucide vector SVG icons.

4. **National Launch Attestation (`NATIONAL_LAUNCH_ATTESTATION.md`)**:
   - Formal executive release sign-off certifying 100% specification completion across all 120 phases.
   - Exact test counts, latency metrics, accessibility standards (WCAG 2.2 AAA), and architectural pillars.

5. **Automated Verification Suite (`backend/tests/test_phase120_grand_nationwide_rollout.py`)**:
   - Test 1: Production SRE health script integrity.
   - Test 2: Institutional About page content, typography, and pure Lucide icons.
   - Test 3: Institutional Terms of Service page content and privacy charters.
   - Test 4: National Launch Attestation file presence, phase count (120), and certification sections.
   - Test 5: Strict zero-emoji enforcement across all platform files.
   - Test 6: Standardized Developer Architecture Note validation.

6. **Master Discovery & SRE Health Run**:
   - Execute `./deploy.sh health`.
   - Execute full platform discovery test suite asserting 1,390+ passing tests.
