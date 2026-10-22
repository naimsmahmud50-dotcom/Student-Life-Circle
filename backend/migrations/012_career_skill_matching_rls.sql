-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Career Skill-to-Job Matching Radar & Recruiter Pipeline
-- TOPIC:     Phase 134 Multi-Dimensional Competency Radar & Sealed CV Applications
-- FILE:      backend/migrations/012_career_skill_matching_rls.sql
-- PHASE:     Phase 134 - Algorithmic Skill-to-Job Matching Radar
-- PURPOSE:   Database migration schema establishing corporate_job_postings,
--            student_skill_radar_profiles, sealed_job_applications, and
--            recruiter_talent_bookmarks tables with immutable CV application
--            snapshots and Supabase Row Level Security (RLS).
-- STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Immutable CV Snapshots
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Corporate Job Postings Table
CREATE TABLE IF NOT EXISTS public.corporate_job_postings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(64) NOT NULL UNIQUE,
    company_name VARCHAR(255) NOT NULL,
    title_en VARCHAR(255) NOT NULL,
    title_bn VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    required_radar JSONB NOT NULL DEFAULT '{}'::jsonb,
    salary_range_bdt VARCHAR(64) NOT NULL,
    job_type VARCHAR(64) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Student Skill Radar Profiles Table
CREATE TABLE IF NOT EXISTS public.student_skill_radar_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE,
    mathematics NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    algorithms NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    olympiads NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    communication NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    systems NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Sealed Job Applications Table (Immutable Point-in-Time Cryptographic Snapshots)
CREATE TABLE IF NOT EXISTS public.sealed_job_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    snapshot_id VARCHAR(64) NOT NULL UNIQUE,
    user_id UUID NOT NULL,
    job_id VARCHAR(64) NOT NULL REFERENCES public.corporate_job_postings(job_id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    institution VARCHAR(255) NOT NULL,
    verified_gpa NUMERIC(3,2) NOT NULL,
    olympiad_achievements JSONB NOT NULL DEFAULT '[]'::jsonb,
    radar_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    snapshot_hash VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'SUBMITTED',
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Recruiter Talent Bookmarks Table
CREATE TABLE IF NOT EXISTS public.recruiter_talent_bookmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recruiter_id UUID NOT NULL,
    candidate_id UUID NOT NULL,
    job_id VARCHAR(64) NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Sealed CV Immutability Guard: REVOKE UPDATE & DELETE
REVOKE UPDATE, DELETE ON public.sealed_job_applications FROM PUBLIC, authenticated, anon;

-- Immutability trigger function
CREATE OR REPLACE FUNCTION public.fn_block_sealed_cv_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Immutable CV Snapshot Violation: Point-in-time sealed applications cannot be modified or deleted under ASVS L2.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_block_sealed_cv_mutation ON public.sealed_job_applications;
CREATE TRIGGER trg_block_sealed_cv_mutation
BEFORE UPDATE OR DELETE ON public.sealed_job_applications
FOR EACH ROW EXECUTE FUNCTION public.fn_block_sealed_cv_mutation();

-- 7. Enable & Force Row Level Security (100% Policy Enforcement)
ALTER TABLE public.corporate_job_postings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.corporate_job_postings FORCE ROW LEVEL SECURITY;

ALTER TABLE public.student_skill_radar_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_skill_radar_profiles FORCE ROW LEVEL SECURITY;

ALTER TABLE public.sealed_job_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sealed_job_applications FORCE ROW LEVEL SECURITY;

ALTER TABLE public.recruiter_talent_bookmarks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recruiter_talent_bookmarks FORCE ROW LEVEL SECURITY;

-- 8. Row Level Security Policies: Job Postings (Public read active, service role write)
DROP POLICY IF EXISTS "Public can view active job postings" ON public.corporate_job_postings;
CREATE POLICY "Public can view active job postings"
ON public.corporate_job_postings
FOR SELECT
USING (is_active = TRUE);

DROP POLICY IF EXISTS "Service role manages job postings" ON public.corporate_job_postings;
CREATE POLICY "Service role manages job postings"
ON public.corporate_job_postings
FOR ALL
USING (auth.jwt() ->> 'role' = 'service_role');

-- 9. Row Level Security Policies: Student Radar Profiles
DROP POLICY IF EXISTS "Students manage their own skill radar" ON public.student_skill_radar_profiles;
CREATE POLICY "Students manage their own skill radar"
ON public.student_skill_radar_profiles
FOR ALL
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 10. Row Level Security Policies: Sealed Applications
DROP POLICY IF EXISTS "Students can view their own sealed applications" ON public.sealed_job_applications;
CREATE POLICY "Students can view their own sealed applications"
ON public.sealed_job_applications
FOR SELECT
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
    OR (auth.jwt() ->> 'role' = 'recruiter')
);

DROP POLICY IF EXISTS "Students can submit sealed applications" ON public.sealed_job_applications;
CREATE POLICY "Students can submit sealed applications"
ON public.sealed_job_applications
FOR INSERT
WITH CHECK (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 11. Row Level Security Policies: Recruiter Bookmarks
DROP POLICY IF EXISTS "Recruiters manage their bookmarks" ON public.recruiter_talent_bookmarks;
CREATE POLICY "Recruiters manage their bookmarks"
ON public.recruiter_talent_bookmarks
FOR ALL
USING (
    (auth.uid() = recruiter_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 12. Query Optimization & Provenance Indexes
CREATE INDEX IF NOT EXISTS idx_sealed_cv_user ON public.sealed_job_applications(user_id, applied_at DESC);
CREATE INDEX IF NOT EXISTS idx_sealed_cv_job ON public.sealed_job_applications(job_id);
CREATE INDEX IF NOT EXISTS idx_sealed_cv_hash ON public.sealed_job_applications(snapshot_hash);
CREATE INDEX IF NOT EXISTS idx_recruiter_bookmarks ON public.recruiter_talent_bookmarks(recruiter_id, job_id);
