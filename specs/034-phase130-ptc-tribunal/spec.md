# SPECIFICATION: Phase 130 — Institutional Parent-Teacher Conference (PTC) Booking & Escrow Dispute Tribunal

## 1. Executive Summary & Objective
Phase 130 delivers two institutional pillars for the Ogrojatra student platform:
1. **Institutional Parent-Teacher Conference (PTC) Booking System**: A formal, conflict-free appointment booking pipeline connecting guardians and verified institutional educators with time-slot management, agenda setting, and appointment status workflows under strict zero-IDOR privacy.
2. **Escrow Dispute Tribunal & 3-Party Arbitration Engine**: A legally binding, cryptographic audit-locked arbitration engine for resolving tuition fee escrow disputes among Guardians, Tutors, and the Institutional Ombudsman with evidence hashing, hearings, and deterministic settlement payouts (full release, full refund, or structured split).

## 2. Mandatory Architectural Standards
- **Developer Architecture Note Header**: Every created or modified file MUST feature the standardized block header documenting Phase 130, Zero-IDOR, Strict Supabase RLS, and Pure Academic UI standards.
- **Pure Academic & Legal Board Visual Philosophy (Zero AI Vibe)**:
  * Formal institutional docket and tribunal bench aesthetic (Oxford / Judicial Arbitration style).
  * High-contrast Paper Ivory (`#FAFAF8`) background, Paper White (`#FFFFFF`) dockets, and Oxford Academic Navy (`#0A2540`) dominant headers and borders.
  * 3D tactile push buttons with physical depth: `bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg`.
  * Strict Zero-Emoji Rule: 100% pure Lucide-React SVG vector icons only.

## 3. Technical Requirements

### A. Escrow Dispute Tribunal (`backend/escrow/dispute_tribunal.py`)
1. **3-Party Arbitration Actors**:
   - `GUARDIAN`: Deposited funds in tuition escrow; lodges disputes for missed hours or breach of syllabus.
   - `TUTOR`: Claims completed tutoring sessions and requests fee disbursement.
   - `OMBUDSMAN`: Neutral institutional arbitrator with authority to inspect evidence and execute binding rulings.
2. **Dispute Lifecycle & State Transitions**:
   - `LODGED` $\rightarrow$ `EVIDENCE_SUBMITTED` $\rightarrow$ `HEARING_SCHEDULED` $\rightarrow$ `ARBITRATION_IN_SESSION` $\rightarrow$ `RESOLVED_RELEASE` / `RESOLVED_REFUND` / `RESOLVED_SPLIT` / `DISMISSED`.
3. **Cryptographic Evidence Hashing & Audit Trail**:
   - Every submitted evidence item (attendance logs, homework submissions, message transcripts) is hashed using SHA-256 with timestamp and submitter ID: $\text{SHA256}(\text{dispute\_id} \parallel \text{submitter\_id} \parallel \text{evidence\_content} \parallel \text{timestamp})$.
4. **Binding Settlement Execution**:
   - `RESOLVED_RELEASE`: 100% escrow funds disbursed to Tutor.
   - `RESOLVED_REFUND`: 100% escrow funds returned to Guardian.
   - `RESOLVED_SPLIT`: Custom percentage allocation (e.g. 50/50, 70/30) based on verified delivered instructional hours.
5. **Zero-IDOR Security Invariant**:
   - Any access (viewing dispute, reading evidence, submitting claims) strictly validates that `caller_id` matches `guardian_id`, `tutor_id`, or has the `OMBUDSMAN` institutional role. Unauthorized callers are rejected with `UnauthorizedDisputeAccessException`.

### B. Parent-Teacher Conference (PTC) Booking (`backend/portal/ptc_booking.py`)
1. **Time-Slot Reservation & Conflict Detection**:
   - Prevents double-booking: A teacher cannot have overlapping active appointments.
   - Buffer periods between appointments (minimum 10-minute break).
2. **Appointment Lifecycle**:
   - `REQUESTED` $\rightarrow$ `CONFIRMED` $\rightarrow$ `IN_SESSION` $\rightarrow$ `CONCLUDED` $\rightarrow$ `RESCHEDULED` / `CANCELLED`.
3. **Discussion Agenda Setting**:
   - Required agenda topics: Academic performance, exam preparation, behavioral discipline, mental well-being, or tuition roadmap.
4. **Zero-IDOR Tenancy**:
   - Only the paired Guardian and Teacher can inspect or update the appointment. Third parties receive strict unauthorized access exceptions.

### C. Supabase Security & RLS (`backend/migrations/008_ptc_and_escrow_tribunal_rls.sql`)
1. **Tables**:
   - `ptc_appointments`: Conference bookings, schedules, agendas, and mutual confirmations.
   - `escrow_disputes`: Active and settled escrow disputes, claim amounts, and rulings.
   - `dispute_evidence_logs`: Immutable hashed evidence records.
   - `tribunal_rulings`: Finalized ombudsman arbitration decisions.
2. **Row Level Security (RLS)**:
   - Enabled and forced on 100% of tables.
   - Tenancy checks: `auth.uid() = guardian_id OR auth.uid() = tutor_id OR (auth.jwt() ->> 'role' = 'ombudsman')`.

### D. Frontend Interfaces
1. **Escrow Dispute Tribunal (`frontend/src/pages/tribunal/disputes.tsx`)**:
   - Institutional case docket, evidence inspection vault, 3-party hearing status, and ombudsman settlement console with 3D tactile buttons.
2. **Guardian PTC Booking Portal (`frontend/src/pages/guardian/ptc.tsx`)**:
   - Interactive calendar time-slot booking, teacher selection, agenda composer, and active conference passes.

### E. Automated Test Suite (`backend/tests/test_phase130_dispute_tribunal.py`)
- Full test coverage of arbitration states, settlement math, PTC booking, zero-IDOR assertions, Supabase migration RLS, and zero-emoji compliance.
