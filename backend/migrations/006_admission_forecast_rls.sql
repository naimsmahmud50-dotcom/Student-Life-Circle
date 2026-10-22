-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    University Admission Forecaster & Sigmoid Rank Predictor
-- TOPIC:     Phase 128 Statistical Cut-Off Engine & Admission Probability Calibration
-- FILE:      backend/migrations/006_admission_forecast_rls.sql
-- PHASE:     Phase 128 - Autonomous Admission Cut-Off Forecaster
-- PURPOSE:   Database migration establishing admission_prediction_logs table with
--            strict Supabase Row Level Security (RLS), ASVS L2 zero-PII storage,
--            direct auth.uid() tenancy isolation, and query acceleration indices.
-- STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Calibrated Probability
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Admission Prediction Logs Table (Zero-PII Academic Analytics)
CREATE TABLE IF NOT EXISTS public.admission_prediction_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    target_institution VARCHAR(64) NOT NULL,
    unit VARCHAR(32) NOT NULL,
    quota VARCHAR(32) NOT NULL DEFAULT 'GENERAL',
    ssc_gpa NUMERIC(4, 2) NOT NULL CHECK (ssc_gpa >= 0.0 AND ssc_gpa <= 5.0),
    hsc_gpa NUMERIC(4, 2) NOT NULL CHECK (hsc_gpa >= 0.0 AND hsc_gpa <= 5.0),
    composite_score NUMERIC(6, 2) NOT NULL CHECK (composite_score >= 0.0),
    calibrated_probability NUMERIC(6, 4) NOT NULL CHECK (calibrated_probability >= 0.0 AND calibrated_probability <= 1.0),
    tier VARCHAR(32) NOT NULL CHECK (tier IN ('SAFE', 'COMPETITIVE', 'REACH', 'INELIGIBLE')),
    rank_range_min INT NOT NULL CHECK (rank_range_min >= 1),
    rank_range_max INT NOT NULL CHECK (rank_range_max >= rank_range_min),
    is_eligible BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Enable & Force Row Level Security (100% Coverage)
ALTER TABLE public.admission_prediction_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.admission_prediction_logs FORCE ROW LEVEL SECURITY;

-- 4. RLS Policy: Insert Permission
-- Authenticated students insert records with their verified auth.uid(); anonymous students insert with user_id NULL.
DROP POLICY IF EXISTS "Insert admission prediction records" ON public.admission_prediction_logs;
CREATE POLICY "Insert admission prediction records"
ON public.admission_prediction_logs
FOR INSERT
WITH CHECK (
    (auth.uid() IS NOT NULL AND user_id = auth.uid())
    OR
    (auth.uid() IS NULL AND user_id IS NULL)
);

-- 5. RLS Policy: Select Tenancy Isolation
-- Authenticated students can inspect only their own prediction telemetry.
DROP POLICY IF EXISTS "Select own prediction records" ON public.admission_prediction_logs;
CREATE POLICY "Select own prediction records"
ON public.admission_prediction_logs
FOR SELECT
USING (
    (auth.uid() IS NOT NULL AND user_id = auth.uid())
    OR
    (auth.jwt() ->> 'role' = 'service_role')
);

-- 6. RLS Policy: Strict Immutability (Zero In-Place Updates)
DROP POLICY IF EXISTS "Prevent in-place modification of forecast telemetry" ON public.admission_prediction_logs;
CREATE POLICY "Prevent in-place modification of forecast telemetry"
ON public.admission_prediction_logs
FOR UPDATE
USING (FALSE);

-- 7. Performance & Analytics Query Optimization Indices
CREATE INDEX IF NOT EXISTS idx_admission_logs_user_id ON public.admission_prediction_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_admission_logs_unit_tier ON public.admission_prediction_logs(unit, tier);
CREATE INDEX IF NOT EXISTS idx_admission_logs_created_at ON public.admission_prediction_logs(created_at DESC);
