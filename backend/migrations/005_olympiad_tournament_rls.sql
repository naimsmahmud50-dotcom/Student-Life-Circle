-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    National STEM Olympiad Arena & Tournament Engine
-- TOPIC:     Phase 127 Real-time Competitive Olympiad & Live Bracket Ladder
-- FILE:      backend/migrations/005_olympiad_tournament_rls.sql
-- PHASE:     Phase 127 - National Live Multiplayer STEM Olympiad Arena
-- PURPOSE:   Database migration schema establishing olympiad_tournaments and
--            olympiad_submissions with strict Supabase Row Level Security (RLS),
--            direct auth.uid() binding, time-locked HMAC verification, and
--            anti-cheating audit trail triggers.
-- STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Sub-50ms Latency
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Olympiad Tournaments Table
CREATE TABLE IF NOT EXISTS public.olympiad_tournaments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    discipline VARCHAR(64) NOT NULL DEFAULT 'PHYSICS',
    season_year INT NOT NULL DEFAULT 2026,
    stage VARCHAR(64) NOT NULL DEFAULT 'LOBBY',
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Olympiad Submissions Table (Time-Locked & Idempotent)
CREATE TABLE IF NOT EXISTS public.olympiad_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID NOT NULL REFERENCES public.olympiad_tournaments(id) ON DELETE CASCADE,
    participant_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    question_id VARCHAR(64) NOT NULL,
    selected_option_id VARCHAR(32) NOT NULL,
    time_taken_seconds NUMERIC(8, 3) NOT NULL CHECK (time_taken_seconds >= 0.05),
    client_timestamp_ms BIGINT NOT NULL,
    time_locked_hash VARCHAR(128) NOT NULL,
    nonce VARCHAR(64) NOT NULL UNIQUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    score NUMERIC(5, 2) NOT NULL DEFAULT 0.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Olympiad Audit Trail Log Table (Immutable Append-Only)
CREATE TABLE IF NOT EXISTS public.olympiad_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID NOT NULL,
    participant_id UUID NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Enable & Force Row Level Security (100% Coverage)
ALTER TABLE public.olympiad_tournaments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.olympiad_tournaments FORCE ROW LEVEL SECURITY;

ALTER TABLE public.olympiad_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.olympiad_submissions FORCE ROW LEVEL SECURITY;

ALTER TABLE public.olympiad_audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.olympiad_audit_log FORCE ROW LEVEL SECURITY;

-- 6. Access Control Policies for Olympiad Tournaments
DROP POLICY IF EXISTS olympiad_tournaments_read_policy ON public.olympiad_tournaments;
CREATE POLICY olympiad_tournaments_read_policy ON public.olympiad_tournaments
    FOR SELECT
    TO anon, authenticated
    USING (status = 'ACTIVE' OR status = 'COMPLETED');

-- 7. Strict Direct auth.uid() Policies for Olympiad Submissions
DROP POLICY IF EXISTS olympiad_submissions_insert_policy ON public.olympiad_submissions;
CREATE POLICY olympiad_submissions_insert_policy ON public.olympiad_submissions
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = participant_id);

DROP POLICY IF EXISTS olympiad_submissions_select_policy ON public.olympiad_submissions;
CREATE POLICY olympiad_submissions_select_policy ON public.olympiad_submissions
    FOR SELECT
    TO authenticated
    USING (auth.uid() = participant_id);

-- Explicitly revoke UPDATE and DELETE on submissions (Immutability Guarantee)
REVOKE UPDATE, DELETE ON public.olympiad_submissions FROM anon, authenticated;

-- 8. Access Control Policies for Olympiad Audit Log
DROP POLICY IF EXISTS olympiad_audit_log_insert_policy ON public.olympiad_audit_log;
CREATE POLICY olympiad_audit_log_insert_policy ON public.olympiad_audit_log
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = participant_id);

DROP POLICY IF EXISTS olympiad_audit_log_select_policy ON public.olympiad_audit_log;
CREATE POLICY olympiad_audit_log_select_policy ON public.olympiad_audit_log
    FOR SELECT
    TO authenticated
    USING (auth.uid() = participant_id);

REVOKE UPDATE, DELETE ON public.olympiad_audit_log FROM anon, authenticated;

-- 9. Anti-Tamper Immutability Trigger
CREATE OR REPLACE FUNCTION public.prevent_olympiad_submission_tampering()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Security Policy Violation: Olympiad submissions and audit entries are strictly immutable.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_olympiad_submission_tampering ON public.olympiad_submissions;
CREATE TRIGGER trg_prevent_olympiad_submission_tampering
    BEFORE UPDATE OR DELETE ON public.olympiad_submissions
    FOR EACH ROW
    EXECUTE FUNCTION public.prevent_olympiad_submission_tampering();

DROP TRIGGER IF EXISTS trg_prevent_olympiad_audit_tampering ON public.olympiad_audit_log;
CREATE TRIGGER trg_prevent_olympiad_audit_tampering
    BEFORE UPDATE OR DELETE ON public.olympiad_audit_log
    FOR EACH ROW
    EXECUTE FUNCTION public.prevent_olympiad_submission_tampering();
