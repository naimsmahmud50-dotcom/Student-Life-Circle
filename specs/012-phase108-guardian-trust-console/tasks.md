<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 108 Guardian Trust Console & Child Digital Safety Portal
FILE:      specs/012-phase108-guardian-trust-console/tasks.md
PHASE:     Phase 108 - Guardian Trust Console & Child Digital Safety Portal
PURPOSE:   Ordered task list tracking atomic implementation steps for child privacy wall,
           non-intrusive academic telemetry, tuition escrow releases, UI components, and test validation.
STANDARDS: ASVS L2 Minor Privacy Boundary, Zero-Intrusion Safeguards, Zero-Emoji, UI/UX Pro Max
-->

# Tasks: Phase 108 — Guardian Trust Console & Child Digital Safety Portal

## Tasks Ledger

- [x] Task 1: Implement Guardian Trust Service (`backend/app/services/guardian_trust_service.py`)
  - Aggregates non-intrusive academic telemetry (weekly study hours, subject mastery %, practice consistency)
  - Enforces strict child privacy wall blocking access to child peer chats and private notes (ASVS L2)
  - Dual-party tuition escrow milestone authorization and SMS OTP verification
  - Cryptographic SHA-256 consent audit trail generator
- [x] Task 2: Implement Guardian Dashboard Component (`frontend/src/components/guardian/GuardianDashboard.tsx`)
  - Apple Health family dashboard caliber: calm, warm slate cards, soft amber/emerald badges
  - Linked children profile cards, weekly study hours, subject mastery progress rings, upcoming exams
  - Empathetic Bengali microcopy ("সন্তানের পড়াশোনায় পাশে থাকুন স্নেহে, উদ্বেগে নয়")
  - Zero-Emoji compliance and 'Hind Siliguri' font with 1.75 line-height
- [x] Task 3: Implement Tuition Escrow Approval Card Component (`frontend/src/components/guardian/TuitionEscrowApprovalCard.tsx`)
  - Completed session progress, tutor verified credentials, student feedback overview
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`)
  - OTP confirmation dialog and cryptographic release receipt
- [x] Task 4: Mount Guardian Console REST API Endpoints (`backend/app/api/v1/endpoints/guardian_console.py`)
  - `GET /api/v1/guardian/summary`
  - `GET /api/v1/guardian/child/{child_id}/private-chat` (Strictly returns 403 Forbidden)
  - `GET /api/v1/guardian/escrow/milestones`
  - `POST /api/v1/guardian/escrow/approve`
  - Mount router in `backend/app/api/v1/router.py`
- [x] Task 5: Implement Guardian Portal Host Page (`frontend/src/pages/guardian.tsx`)
  - Unified family trust console mounting Guardian Dashboard and Tuition Escrow Approval Card
  - Integration with Navbar, Footer, and AppHead
- [x] Task 6: Implement automated verification test suite (`backend/tests/test_phase108_guardian_trust_console.py`)
  - Strict child privacy wall blocking attempts to access private peer communications (403 Forbidden)
  - Non-intrusive telemetry calculation (study hours, mastery, consistency)
  - Tuition escrow approval flow with OTP and SHA-256 audit log
  - REST API endpoint verification
  - Standardized Developer Architecture Note headers check and strict zero-emoji sweep
- [x] Task 7: Execute full regression test discovery (`python3 -m unittest discover -s backend/tests`) asserting 100% pass rate
