-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Multi-Dialect Audio Tutoring & Voice Viva Evaluator
-- TOPIC:     Phase 129 Acoustic Dialect Adaptation & Viva-Voce Rubric Engine
-- FILE:      backend/migrations/007_viva_evaluator_rls.sql
-- PHASE:     Phase 129 - Multi-Dialect Regional Audio Tutoring
-- PURPOSE:   Database migration establishing viva_evaluations table with strict
--            Supabase Row Level Security (RLS), ASVS L2 privacy-by-design, zero
--            permanent audio storage policy, and ephemeral TTL tenancy.
-- STANDARDS: Zero-Emoji, Pure Academic Design, Privacy By Design, ASVS L2
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Viva Evaluation Telemetry Table (Zero Audio Retained)
CREATE TABLE IF NOT EXISTS public.viva_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    question_id VARCHAR(64) NOT NULL,
    dialect VARCHAR(32) NOT NULL DEFAULT 'STANDARD_BANGLA',
    total_score NUMERIC(5, 2) NOT NULL CHECK (total_score >= 0.0 AND total_score <= 100.0),
    grade_letter VARCHAR(4) NOT NULL,
    conceptual_score NUMERIC(5, 2) NOT NULL CHECK (conceptual_score >= 0.0 AND conceptual_score <= 40.0),
    terminology_score NUMERIC(5, 2) NOT NULL CHECK (terminology_score >= 0.0 AND terminology_score <= 30.0),
    articulation_score NUMERIC(5, 2) NOT NULL CHECK (articulation_score >= 0.0 AND articulation_score <= 20.0),
    dialect_score NUMERIC(5, 2) NOT NULL CHECK (dialect_score >= 0.0 AND dialect_score <= 10.0),
    audio_retained BOOLEAN NOT NULL DEFAULT FALSE CHECK (audio_retained = FALSE),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '15 minutes'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Enable & Force Row Level Security (100% Coverage)
ALTER TABLE public.viva_evaluations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.viva_evaluations FORCE ROW LEVEL SECURITY;

-- 4. RLS Policy: Insert Permission
DROP POLICY IF EXISTS "Insert viva evaluation records" ON public.viva_evaluations;
CREATE POLICY "Insert viva evaluation records"
ON public.viva_evaluations
FOR INSERT
WITH CHECK (
    (auth.uid() IS NOT NULL AND student_id = auth.uid())
    OR
    (auth.uid() IS NULL AND student_id IS NULL)
);

-- 5. RLS Policy: Select Tenancy Isolation
DROP POLICY IF EXISTS "Select own viva evaluations" ON public.viva_evaluations;
CREATE POLICY "Select own viva evaluations"
ON public.viva_evaluations
FOR SELECT
USING (
    (auth.uid() IS NOT NULL AND student_id = auth.uid())
    OR
    (auth.jwt() ->> 'role' = 'service_role')
);

-- 6. RLS Policy: Strict Immutability (Prohibiting Score Tampering)
DROP POLICY IF EXISTS "Prohibit alteration of finalized viva scores" ON public.viva_evaluations;
CREATE POLICY "Prohibit alteration of finalized viva scores"
ON public.viva_evaluations
FOR UPDATE
USING (FALSE);

-- 7. Performance & Ephemeral Eviction Indices
CREATE INDEX IF NOT EXISTS idx_viva_evaluations_student_id ON public.viva_evaluations(student_id);
CREATE INDEX IF NOT EXISTS idx_viva_evaluations_created_at ON public.viva_evaluations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_viva_evaluations_expires_at ON public.viva_evaluations(expires_at);
