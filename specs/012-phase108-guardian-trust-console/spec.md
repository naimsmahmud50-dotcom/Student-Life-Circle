<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 108 Guardian Trust Console & Child Digital Safety Portal
FILE:      specs/012-phase108-guardian-trust-console/spec.md
PHASE:     Phase 108 - Guardian Trust Console & Child Digital Safety Portal
PURPOSE:   Establishes functional specifications for non-intrusive academic telemetry,
           strict child privacy boundary guards (ASVS L2 / COPPA), dual-party tuition
           escrow release authorizations, and cryptographic consent audit logs.
STANDARDS: ASVS L2 Minor Privacy Boundary, Zero-Intrusion Safeguards, Zero-Emoji, UI/UX Pro Max
-->

# Specification: Phase 108 — Guardian Trust Console & Child Digital Safety Portal

## Feature Directory
`specs/012-phase108-guardian-trust-console`

## 1. Problem Statement
In digital education platforms across Bangladesh, guardian involvement often polarizes into two extremes: either complete disengagement (leaving guardians uninformed about milestones, upcoming exams, or tuition financial security) or invasive helicopter monitoring (tracking private messages, peer discussions, and personal reflection notes, which destroys student agency and trust). Furthermore, offline tuition arrangements frequently suffer from delayed or insecure payments, lack of attendance transparency, and dispute anxiety.

"Student Life Circle (অগ্রযাত্রা)" requires a dignified **Guardian Trust Console & Child Digital Safety Portal**:
1. **Calm, Non-Intrusive Academic Telemetry:** Guardians see high-level learning health (weekly study hours, subject mastery progress, upcoming exam calendar) without stressful micro-surveillance.
2. **Strict Child Privacy Boundary Wall (ASVS L2):** Absolute cryptographic and authorization barriers preventing guardians from reading student peer chats, private study room voice transcripts, or unshared notebook entries.
3. **Dual-Party Tuition Escrow Milestone Release:** Secure escrow holding for monthly tutor fees, released with 1-click guardian approval and SMS OTP confirmation upon tutor attendance verification.
4. **Cryptographic Consent & Audit Trail:** Immutable SHA-256 audit log tracking guardian milestone approvals and minor consent milestones.

---

## 2. User Stories & Acceptance Criteria

### US1: Non-Intrusive Academic Health Telemetry (P1)
- As a caring guardian, I want to see my child's weekly study consistency, subject progress, and upcoming exam dates in a calm, reassuring dashboard without overwhelming alarmist notifications.
- Acceptance Criteria:
  - Aggregate study hours, weekly consistency streak, and subject mastery percentages (e.g. Physics 84%, Math 78%).
  - Warm, empathetic Bengali microcopy ("সন্তানের পড়াশোনায় পাশে থাকুন স্নেহে, উদ্বেগে নয়").
  - Calm color palette (slate, soft emerald, gentle amber; zero panic-inducing red banners).

### US2: Strict Child Digital Privacy Wall (P1)
- As an adolescent student, I want guarantees that my private peer study conversations and personal notes remain confidential from my parents, fostering independent academic agency.
- Acceptance Criteria:
  - Any API request attempting to fetch peer chats, direct messages, or personal study notes via a guardian context MUST be blocked with HTTP 403 Forbidden (`CHILD_PRIVACY_BOUNDARY_ENFORCED`).
  - Clear privacy guarantee badges displayed on guardian console explaining boundary protections.

### US3: Tuition Escrow Milestone Authorization & OTP Release (P1)
- As a guardian, I want to inspect completed tutoring sessions, tutor attendance logs, and verified student feedback before releasing escrowed tuition fees via bKash/Nagad.
- Acceptance Criteria:
  - Interactive milestone card displaying completed sessions (e.g. 12 of 12 classes), verified tutor credentials, and payment amount.
  - Tactile 3D button physics: `"টিউশন ফি রিলিজ করুন"` (`shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`).
  - SMS OTP verification step for final disbursement confirmation.
  - Generates immutable cryptographic receipt (SHA-256 hash).

### US4: Guardian Trust Console UI & Mobile Responsiveness (P1)
- As a guardian accessing from a smartphone, I need an Apple Health-caliber family dashboard that is responsive, tactile, and daylight-readable.
- Acceptance Criteria:
  - `frontend/src/components/guardian/GuardianDashboard.tsx`
  - `frontend/src/components/guardian/TuitionEscrowApprovalCard.tsx`
  - `frontend/src/pages/guardian.tsx`
  - Strict Zero-Emoji compliance (Lucide SVG vectors only: `ShieldCheck`, `Heart`, `Clock`, `Award`, `Wallet`, `Lock`).
  - 'Hind Siliguri' font with comfortable 1.75 line-height.

### US5: REST API & Automated Verification Suite (P1)
- As a client app, I need secure endpoints to fetch guardian summaries and approve escrow milestones.
- Acceptance Criteria:
  - `GET /api/v1/guardian/summary`
  - `GET /api/v1/guardian/child/{child_id}/private-chat` (Strictly returns 403 Forbidden)
  - `GET /api/v1/guardian/escrow/milestones`
  - `POST /api/v1/guardian/escrow/approve`
  - Automated test suite `backend/tests/test_phase108_guardian_trust_console.py` passing 100%.
