-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE (Phase 79 - Core Database Schema):
-- This migration script establishes the production PostgreSQL / Supabase schema
-- for the Student Life Circle educational platform. It defines enterprise schemas
-- for authentication, learner profiles, question banks, quiz attempts, tuition
-- applications, financial escrow vaults, verifiable credentials, and immutable
-- append-only audit logs. All tables enforce UUID primary keys, relational
-- integrity, and OWASP ASVS Level 2 child-safety data structures.
-- Zero-Emoji Policy Enforced: All comments and descriptions use clean technical text.
-- ==============================================================================

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Core Enumerations
DO $$ BEGIN
    CREATE TYPE user_role_enum AS ENUM (
        'student',
        'educator',
        'guardian',
        'institutional_admin',
        'corporate_recruiter',
        'service_role'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE quiz_difficulty_band AS ENUM (
        'FOUNDATION',
        'INTERMEDIATE',
        'ADVANCED',
        'OLYMPIAD'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Core Users Table (Supabase Auth / Public Federation)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    role user_role_enum NOT NULL DEFAULT 'student',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Student & User Profiles
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'student',
    class_grade INT CHECK (class_grade >= 1 AND class_grade <= 12),
    curriculum VARCHAR(64) NOT NULL DEFAULT 'NCTB',
    is_minor BOOLEAN NOT NULL DEFAULT TRUE,
    guardian_consent_granted BOOLEAN NOT NULL DEFAULT FALSE,
    phone VARCHAR(32),
    institution VARCHAR(255),
    district VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Question Bank & Cognitive Items
CREATE TABLE IF NOT EXISTS public.question_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject VARCHAR(128) NOT NULL,
    topic VARCHAR(128) NOT NULL,
    stem_text_bn TEXT NOT NULL,
    stem_text_en TEXT,
    difficulty quiz_difficulty_band NOT NULL DEFAULT 'INTERMEDIATE',
    options JSONB NOT NULL,
    correct_option_key VARCHAR(8) NOT NULL,
    explanation_bn TEXT NOT NULL,
    is_quarantined BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Student Quiz Attempts (Active Session Records)
CREATE TABLE IF NOT EXISTS public.quiz_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL,
    quiz_id VARCHAR(64) NOT NULL,
    score NUMERIC(6, 2) NOT NULL DEFAULT 0.0,
    total_questions INT NOT NULL DEFAULT 0,
    correct_answers INT NOT NULL DEFAULT 0,
    time_spent_seconds INT NOT NULL DEFAULT 0,
    answers_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_verified BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Student Exam Submissions & Formal Attempt Records (Backward Compatibility)
CREATE TABLE IF NOT EXISTS public.exam_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL,
    quiz_blueprint_id VARCHAR(64) NOT NULL,
    answers_payload JSONB NOT NULL,
    raw_score NUMERIC(6, 2) NOT NULL DEFAULT 0.0,
    accuracy_percentage NUMERIC(5, 2) NOT NULL DEFAULT 0.0,
    is_server_verified BOOLEAN NOT NULL DEFAULT TRUE,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Tuition Applications & Marketplace Matchings
CREATE TABLE IF NOT EXISTS public.tuition_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    tutor_user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    tenant_id UUID NOT NULL,
    subject VARCHAR(128) NOT NULL,
    grade_level VARCHAR(32) NOT NULL,
    budget_bdt NUMERIC(10, 2) NOT NULL DEFAULT 0.0,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    guardian_phone VARCHAR(32),
    message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 9. Tuition Matching & Financial Escrow Vaults
CREATE TABLE IF NOT EXISTS public.escrow_vaults (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    guardian_user_id UUID NOT NULL REFERENCES public.users(id),
    tutor_user_id UUID NOT NULL REFERENCES public.users(id),
    tenant_id UUID NOT NULL,
    amount_bdt NUMERIC(10, 2) NOT NULL CHECK (amount_bdt > 0),
    status VARCHAR(32) NOT NULL DEFAULT 'HELD_IN_ESCROW',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    released_at TIMESTAMPTZ
);

-- 10. W3C Verifiable Academic Credentials
CREATE TABLE IF NOT EXISTS public.verifiable_credentials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_user_id UUID NOT NULL REFERENCES public.users(id),
    institution_did VARCHAR(255) NOT NULL,
    credential_type VARCHAR(64) NOT NULL,
    ed25519_signature TEXT NOT NULL,
    claims_payload JSONB NOT NULL,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. Immutable Append-Only Audit Logs
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL,
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    action VARCHAR(64) NOT NULL,
    entity_type VARCHAR(64) NOT NULL,
    entity_id VARCHAR(128) NOT NULL,
    metadata_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 12. Database-Level Immutability Trigger for Audit Logs
CREATE OR REPLACE FUNCTION reject_audit_log_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Security Violation: Audit logs are strictly immutable and append-only. UPDATE and DELETE operations are prohibited at database level.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_audit_log_mutation ON public.audit_logs;
CREATE TRIGGER trg_prevent_audit_log_mutation
BEFORE UPDATE OR DELETE ON public.audit_logs
FOR EACH ROW
EXECUTE FUNCTION reject_audit_log_mutation();

-- 13. High-Performance Foreign Key & Filtering Indices
CREATE INDEX IF NOT EXISTS idx_profiles_user_tenant ON public.profiles (user_id, tenant_id);
CREATE INDEX IF NOT EXISTS idx_profiles_minor_privacy ON public.profiles (is_minor, guardian_consent_granted);
CREATE INDEX IF NOT EXISTS idx_question_items_subject ON public.question_items (subject, is_quarantined);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user ON public.quiz_attempts (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_exam_submissions_user ON public.exam_submissions (user_id, submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_tuition_student ON public.tuition_applications (student_user_id, tenant_id);
CREATE INDEX IF NOT EXISTS idx_escrow_vaults_participants ON public.escrow_vaults (guardian_user_id, tutor_user_id);
CREATE INDEX IF NOT EXISTS idx_verifiable_credentials_student ON public.verifiable_credentials (student_user_id, is_revoked);
CREATE INDEX IF NOT EXISTS idx_audit_logs_tenant_ts ON public.audit_logs (tenant_id, timestamp DESC);
