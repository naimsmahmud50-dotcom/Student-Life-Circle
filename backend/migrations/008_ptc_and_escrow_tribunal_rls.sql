-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Parent-Teacher Conference & Escrow Dispute Tribunal
-- TOPIC:     Phase 130 Institutional Appointment & Formal Escrow Arbitration
-- FILE:      backend/migrations/008_ptc_and_escrow_tribunal_rls.sql
-- PHASE:     Phase 130 - Institutional PTC & Escrow Dispute Tribunal
-- PURPOSE:   Database migration schema establishing ptc_appointments, escrow_disputes,
--            dispute_evidence_logs, and tribunal_rulings tables with strict Supabase
--            Row Level Security (RLS), Zero-IDOR tenancy barriers, and audit indices.
-- STANDARDS: Zero-Emoji, Zero-IDOR, Strict Supabase RLS, Pure Academic UI
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Parent-Teacher Conference (PTC) Appointments Table
CREATE TABLE IF NOT EXISTS public.ptc_appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    guardian_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    teacher_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    student_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    slot_start TIMESTAMPTZ NOT NULL,
    slot_end TIMESTAMPTZ NOT NULL,
    agenda_topic VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'REQUESTED',
    meeting_passcode VARCHAR(16) NOT NULL,
    concluded_summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Escrow Disputes Table
CREATE TABLE IF NOT EXISTS public.escrow_disputes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    guardian_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    tutor_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    escrow_amount NUMERIC(10, 2) NOT NULL CHECK (escrow_amount > 0.0),
    reason_bn TEXT NOT NULL,
    reason_en TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'LODGED',
    hearing_timestamp TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Dispute Evidence Logs Table (Immutable & Cryptographically Hashed)
CREATE TABLE IF NOT EXISTS public.dispute_evidence_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES public.escrow_disputes(id) ON DELETE CASCADE,
    submitter_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    submitter_role VARCHAR(32) NOT NULL,
    title VARCHAR(255) NOT NULL,
    evidence_content TEXT NOT NULL,
    evidence_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Tribunal Rulings Table
CREATE TABLE IF NOT EXISTS public.tribunal_rulings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL UNIQUE REFERENCES public.escrow_disputes(id) ON DELETE CASCADE,
    ombudsman_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    ruling_type VARCHAR(32) NOT NULL,
    split_ratio_tutor NUMERIC(5, 4) NOT NULL,
    payout_tutor NUMERIC(10, 2) NOT NULL,
    payout_guardian NUMERIC(10, 2) NOT NULL,
    reasoning_bn TEXT NOT NULL,
    reason_en TEXT,
    ruling_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Enable & Force Row Level Security (100% Zero-IDOR Enforcement)
ALTER TABLE public.ptc_appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ptc_appointments FORCE ROW LEVEL SECURITY;

ALTER TABLE public.escrow_disputes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.escrow_disputes FORCE ROW LEVEL SECURITY;

ALTER TABLE public.dispute_evidence_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dispute_evidence_logs FORCE ROW LEVEL SECURITY;

ALTER TABLE public.tribunal_rulings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tribunal_rulings FORCE ROW LEVEL SECURITY;

-- 7. RLS Policies: PTC Appointments (Zero-IDOR: Only Guardian & Teacher have access)
DROP POLICY IF EXISTS "Parties can read own PTC appointments" ON public.ptc_appointments;
CREATE POLICY "Parties can read own PTC appointments"
ON public.ptc_appointments
FOR SELECT
USING (
    guardian_id = auth.uid()
    OR teacher_id = auth.uid()
    OR (auth.jwt() ->> 'role' = 'service_role')
);

DROP POLICY IF EXISTS "Guardians can create PTC appointments" ON public.ptc_appointments;
CREATE POLICY "Guardians can create PTC appointments"
ON public.ptc_appointments
FOR INSERT
WITH CHECK (
    guardian_id = auth.uid()
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 8. RLS Policies: Escrow Disputes
DROP POLICY IF EXISTS "Parties can read own escrow disputes" ON public.escrow_disputes;
CREATE POLICY "Parties can read own escrow disputes"
ON public.escrow_disputes
FOR SELECT
USING (
    guardian_id = auth.uid()
    OR tutor_id = auth.uid()
    OR (auth.jwt() ->> 'role' = 'ombudsman')
    OR (auth.jwt() ->> 'role' = 'service_role')
);

DROP POLICY IF EXISTS "Guardians can lodge escrow disputes" ON public.escrow_disputes;
CREATE POLICY "Guardians can lodge escrow disputes"
ON public.escrow_disputes
FOR INSERT
WITH CHECK (
    guardian_id = auth.uid()
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 9. Performance & Security Indices
CREATE INDEX IF NOT EXISTS idx_ptc_guardian_id ON public.ptc_appointments(guardian_id);
CREATE INDEX IF NOT EXISTS idx_ptc_teacher_id ON public.ptc_appointments(teacher_id);
CREATE INDEX IF NOT EXISTS idx_escrow_guardian_id ON public.escrow_disputes(guardian_id);
CREATE INDEX IF NOT EXISTS idx_escrow_tutor_id ON public.escrow_disputes(tutor_id);
CREATE INDEX IF NOT EXISTS idx_evidence_case_id ON public.dispute_evidence_logs(case_id);
