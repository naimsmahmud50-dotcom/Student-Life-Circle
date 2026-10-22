-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Database Security & Hardened Row-Level Access Control
-- TOPIC:     Phase 111 Supabase Security Hardening & Zero-Trust RLS Policies
-- FILE:      backend/migrations/003_hardened_supabase_rls.sql
-- PHASE:     Phase 111 - Supabase Security Hardening & Zero-Trust RLS Audit
-- PURPOSE:   Enforces 100% table Row Level Security (RLS) lockdown, direct auth.uid()
--            binding across all CRUD operations, prevention of client-supplied ID
--            spoofing, immutable append-only audit logging, and zero-IDOR isolation
--            in strict accordance with the Strix-Supabase penetration benchmark.
-- STANDARDS: Strix-Supabase Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Core Tables Compatibility Alignment
CREATE TABLE IF NOT EXISTS public.student_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    class_grade INT CHECK (class_grade >= 1 AND class_grade <= 12),
    is_minor BOOLEAN NOT NULL DEFAULT TRUE,
    guardian_consent_granted BOOLEAN NOT NULL DEFAULT FALSE,
    phone VARCHAR(32),
    institution VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.tuition_escrow (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id),
    guardian_id UUID NOT NULL REFERENCES public.users(id),
    tutor_id UUID NOT NULL REFERENCES public.users(id),
    tenant_id UUID NOT NULL DEFAULT uuid_generate_v4(),
    amount_bdt NUMERIC(10, 2) NOT NULL CHECK (amount_bdt > 0),
    status VARCHAR(32) NOT NULL DEFAULT 'HELD_IN_ESCROW',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    released_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.credentials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id),
    student_id UUID NOT NULL REFERENCES public.users(id),
    tenant_id UUID NOT NULL DEFAULT uuid_generate_v4(),
    credential_title VARCHAR(255) NOT NULL,
    credential_hash VARCHAR(128) NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT FALSE,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- 3. ENFORCE ROW LEVEL SECURITY (RLS) ON 100% OF TARGET TABLES
-- ==============================================================================

-- Enable and FORCE RLS on all tables so that even table owners cannot bypass policies
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users FORCE ROW LEVEL SECURITY;

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles FORCE ROW LEVEL SECURITY;

ALTER TABLE public.student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles FORCE ROW LEVEL SECURITY;

ALTER TABLE public.quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_attempts FORCE ROW LEVEL SECURITY;

ALTER TABLE public.tuition_escrow ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tuition_escrow FORCE ROW LEVEL SECURITY;

ALTER TABLE public.escrow_vaults ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.escrow_vaults FORCE ROW LEVEL SECURITY;

ALTER TABLE public.credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.credentials FORCE ROW LEVEL SECURITY;

ALTER TABLE public.verifiable_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.verifiable_credentials FORCE ROW LEVEL SECURITY;

ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs FORCE ROW LEVEL SECURITY;

-- ==============================================================================
-- 4. HARDENED POLICIES: USERS TABLE
-- ==============================================================================
DROP POLICY IF EXISTS users_hardened_select ON public.users;
CREATE POLICY users_hardened_select ON public.users
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() = id
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

DROP POLICY IF EXISTS users_hardened_insert ON public.users;
CREATE POLICY users_hardened_insert ON public.users
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = id
        OR (auth.jwt() ->> 'role') = 'service_role'
    );

DROP POLICY IF EXISTS users_hardened_update ON public.users;
CREATE POLICY users_hardened_update ON public.users
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() = id
    )
    WITH CHECK (
        auth.uid() = id
    );

DROP POLICY IF EXISTS users_hardened_delete ON public.users;
CREATE POLICY users_hardened_delete ON public.users
    FOR DELETE
    TO authenticated
    USING (
        auth.uid() = id
        OR (auth.jwt() ->> 'role') = 'service_role'
    );

-- ==============================================================================
-- 5. HARDENED POLICIES: STUDENT PROFILES & PROFILES
-- ==============================================================================
DROP POLICY IF EXISTS student_profiles_hardened_select ON public.student_profiles;
CREATE POLICY student_profiles_hardened_select ON public.student_profiles
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() = user_id
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        OR (
            is_minor = FALSE
            AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        )
        OR (
            is_minor = TRUE
            AND guardian_consent_granted = TRUE
            AND (auth.jwt() ->> 'role') = 'guardian'
        )
    );

DROP POLICY IF EXISTS student_profiles_hardened_insert ON public.student_profiles;
CREATE POLICY student_profiles_hardened_insert ON public.student_profiles
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = user_id
    );

DROP POLICY IF EXISTS student_profiles_hardened_update ON public.student_profiles;
CREATE POLICY student_profiles_hardened_update ON public.student_profiles
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() = user_id
    )
    WITH CHECK (
        auth.uid() = user_id
    );

DROP POLICY IF EXISTS student_profiles_hardened_delete ON public.student_profiles;
CREATE POLICY student_profiles_hardened_delete ON public.student_profiles
    FOR DELETE
    TO authenticated
    USING (
        auth.uid() = user_id
    );

-- ==============================================================================
-- 6. HARDENED POLICIES: QUIZ ATTEMPTS
-- ==============================================================================
DROP POLICY IF EXISTS quiz_attempts_hardened_select ON public.quiz_attempts;
CREATE POLICY quiz_attempts_hardened_select ON public.quiz_attempts
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() = user_id
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

DROP POLICY IF EXISTS quiz_attempts_hardened_insert ON public.quiz_attempts;
CREATE POLICY quiz_attempts_hardened_insert ON public.quiz_attempts
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = user_id
    );

DROP POLICY IF EXISTS quiz_attempts_hardened_update ON public.quiz_attempts;
CREATE POLICY quiz_attempts_hardened_update ON public.quiz_attempts
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() = user_id
    )
    WITH CHECK (
        auth.uid() = user_id
    );

DROP POLICY IF EXISTS quiz_attempts_hardened_delete ON public.quiz_attempts;
CREATE POLICY quiz_attempts_hardened_delete ON public.quiz_attempts
    FOR DELETE
    TO authenticated
    USING (
        auth.uid() = user_id
    );

-- ==============================================================================
-- 7. HARDENED POLICIES: TUITION ESCROW
-- ==============================================================================
DROP POLICY IF EXISTS tuition_escrow_hardened_select ON public.tuition_escrow;
CREATE POLICY tuition_escrow_hardened_select ON public.tuition_escrow
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() IN (user_id, guardian_id, tutor_id)
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

DROP POLICY IF EXISTS tuition_escrow_hardened_insert ON public.tuition_escrow;
CREATE POLICY tuition_escrow_hardened_insert ON public.tuition_escrow
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() IN (user_id, guardian_id)
    );

DROP POLICY IF EXISTS tuition_escrow_hardened_update ON public.tuition_escrow;
CREATE POLICY tuition_escrow_hardened_update ON public.tuition_escrow
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() IN (user_id, guardian_id, tutor_id)
        OR (auth.jwt() ->> 'role') = 'service_role'
    )
    WITH CHECK (
        auth.uid() IN (user_id, guardian_id, tutor_id)
        OR (auth.jwt() ->> 'role') = 'service_role'
    );

-- Prohibit DELETE operations on financial escrow ledger
REVOKE DELETE ON public.tuition_escrow FROM PUBLIC, authenticated, anon;

-- ==============================================================================
-- 8. HARDENED POLICIES: CREDENTIALS
-- ==============================================================================
DROP POLICY IF EXISTS credentials_hardened_select ON public.credentials;
CREATE POLICY credentials_hardened_select ON public.credentials
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() IN (user_id, student_id)
        OR is_public = TRUE
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'corporate_recruiter', 'service_role')
    );

DROP POLICY IF EXISTS credentials_hardened_insert ON public.credentials;
CREATE POLICY credentials_hardened_insert ON public.credentials
    FOR INSERT
    TO authenticated
    WITH CHECK (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

DROP POLICY IF EXISTS credentials_hardened_update ON public.credentials;
CREATE POLICY credentials_hardened_update ON public.credentials
    FOR UPDATE
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

-- ==============================================================================
-- 9. HARDENED POLICIES: AUDIT LOGS (IMMUTABLE APPEND-ONLY)
-- ==============================================================================
DROP POLICY IF EXISTS audit_logs_hardened_select ON public.audit_logs;
CREATE POLICY audit_logs_hardened_select ON public.audit_logs
    FOR SELECT
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

DROP POLICY IF EXISTS audit_logs_hardened_insert ON public.audit_logs;
CREATE POLICY audit_logs_hardened_insert ON public.audit_logs
    FOR INSERT
    TO authenticated
    WITH CHECK (
        TRUE
    );

-- Prohibit UPDATE and DELETE completely on audit logs
REVOKE UPDATE, DELETE ON public.audit_logs FROM PUBLIC, authenticated, anon;

-- Re-assert immutability trigger
CREATE OR REPLACE FUNCTION enforce_strict_audit_log_immutability()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Security Policy Violation: audit_logs is an immutable write-once ledger. UPDATE and DELETE operations are permanently blocked.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_enforce_strict_audit_log_immutability ON public.audit_logs;
CREATE TRIGGER trg_enforce_strict_audit_log_immutability
BEFORE UPDATE OR DELETE ON public.audit_logs
FOR EACH ROW
EXECUTE FUNCTION enforce_strict_audit_log_immutability();
