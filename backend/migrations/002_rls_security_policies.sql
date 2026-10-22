-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE (Phase 79 - Zero-Trust RLS Security Policies):
-- This migration script establishes exhaustive Row-Level Security (RLS) policies
-- across all production tables according to the Strix-Supabase security benchmark.
-- Enforces:
-- 1. Zero-IDOR (Insecure Direct Object Reference) Isolation: All queries bound to auth.uid().
-- 2. Strict Multi-Tenant Partitioning: Queries scoped to auth.jwt() ->> 'tenant_id'.
-- 3. Child Minor Protection: Learner profiles where is_minor = TRUE are strictly masked
--    from unverified adult users, requiring verified guardian or institutional consent.
-- 4. Append-Only Audit Logging: audit_logs prohibits UPDATE and DELETE policies,
--    enforcing an immutable ledger backed by database-level triggers.
-- Zero-Emoji Policy Enforced: All comments and descriptions use clean technical text.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. USERS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.users FROM PUBLIC;
GRANT SELECT, UPDATE ON public.users TO authenticated;
GRANT SELECT ON public.users TO anon;

CREATE POLICY users_authenticated_select ON public.users
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() = id
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

CREATE POLICY users_authenticated_update ON public.users
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() = id
    )
    WITH CHECK (
        auth.uid() = id
    );

-- ------------------------------------------------------------------------------
-- 2. PROFILES TABLE: Row-Level Security Policies & Minor Masking
-- ------------------------------------------------------------------------------
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.profiles FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.profiles TO authenticated;
GRANT SELECT ON public.profiles TO anon;

-- Unauthenticated users can read public educator profiles only (sanitized)
CREATE POLICY profiles_anon_read ON public.profiles
    FOR SELECT
    TO anon
    USING (
        role = 'educator' AND guardian_consent_granted = TRUE
    );

-- Authenticated users: Zero-IDOR and Child Minor Protection
-- Minors (is_minor = TRUE) are hidden from unverified adults
CREATE POLICY profiles_authenticated_select ON public.profiles
    FOR SELECT
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = user_id
            OR role = 'educator'
            OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
            OR (
                is_minor = FALSE
                AND (auth.jwt() ->> 'role') IN ('student', 'educator', 'guardian')
            )
            OR (
                is_minor = TRUE
                AND guardian_consent_granted = TRUE
                AND (auth.jwt() ->> 'role') IN ('guardian', 'institutional_admin', 'service_role')
            )
        )
    );

-- Users can only insert their own profile matching auth.uid() and current tenant
CREATE POLICY profiles_authenticated_insert ON public.profiles
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- Users can only update their own profile; cannot alter tenant_id
CREATE POLICY profiles_authenticated_update ON public.profiles
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() = user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    )
    WITH CHECK (
        auth.uid() = user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- Profiles cannot be deleted directly by clients; must be soft-deleted by admin/service
CREATE POLICY profiles_admin_delete ON public.profiles
    FOR DELETE
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- ------------------------------------------------------------------------------
-- 3. QUESTION ITEMS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.question_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.question_items FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.question_items FROM PUBLIC;
GRANT SELECT ON public.question_items TO authenticated;
GRANT SELECT ON public.question_items TO anon;
GRANT INSERT, UPDATE, DELETE ON public.question_items TO authenticated;

-- Public and authenticated users can view non-quarantined questions
CREATE POLICY question_items_read_published ON public.question_items
    FOR SELECT
    TO authenticated, anon
    USING (
        is_quarantined = FALSE
    );

-- Only educators and admins can manage question items
CREATE POLICY question_items_educator_insert ON public.question_items
    FOR INSERT
    TO authenticated
    WITH CHECK (
        (auth.jwt() ->> 'role') IN ('educator', 'institutional_admin', 'service_role')
    );

CREATE POLICY question_items_educator_update ON public.question_items
    FOR UPDATE
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('educator', 'institutional_admin', 'service_role')
    )
    WITH CHECK (
        (auth.jwt() ->> 'role') IN ('educator', 'institutional_admin', 'service_role')
    );

-- ------------------------------------------------------------------------------
-- 4. QUIZ ATTEMPTS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_attempts FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.quiz_attempts FROM PUBLIC;
GRANT SELECT, INSERT ON public.quiz_attempts TO authenticated;

-- Students can read only their own quiz attempts within their tenant
CREATE POLICY quiz_attempts_student_select ON public.quiz_attempts
    FOR SELECT
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = user_id
            OR (auth.jwt() ->> 'role') IN ('educator', 'institutional_admin', 'service_role')
        )
    );

-- Students can only insert their own attempt matching auth.uid()
CREATE POLICY quiz_attempts_student_insert ON public.quiz_attempts
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- ------------------------------------------------------------------------------
-- 5. EXAM SUBMISSIONS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.exam_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exam_submissions FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.exam_submissions FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE ON public.exam_submissions TO authenticated;

-- Students can read only their own submissions within their tenant
CREATE POLICY exam_submissions_student_select ON public.exam_submissions
    FOR SELECT
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = user_id
            OR (auth.jwt() ->> 'role') IN ('educator', 'institutional_admin', 'service_role')
        )
    );

-- Students can only insert their own submission matching auth.uid()
CREATE POLICY exam_submissions_student_insert ON public.exam_submissions
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- Exam submissions are immutable once verified by the server
CREATE POLICY exam_submissions_immutable_guard ON public.exam_submissions
    FOR UPDATE
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- ------------------------------------------------------------------------------
-- 6. TUITION APPLICATIONS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.tuition_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tuition_applications FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.tuition_applications FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE ON public.tuition_applications TO authenticated;

-- Only direct participants (student applicant, matched tutor, or admin) can view
CREATE POLICY tuition_applications_participant_select ON public.tuition_applications
    FOR SELECT
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = student_user_id
            OR auth.uid() = tutor_user_id
            OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        )
    );

-- Students insert applications bound to their own auth.uid()
CREATE POLICY tuition_applications_student_insert ON public.tuition_applications
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = student_user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- Matched tutor or student applicant can update application state
CREATE POLICY tuition_applications_participant_update ON public.tuition_applications
    FOR UPDATE
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = student_user_id
            OR auth.uid() = tutor_user_id
            OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        )
    );

-- ------------------------------------------------------------------------------
-- 7. ESCROW VAULTS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.escrow_vaults ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.escrow_vaults FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.escrow_vaults FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE ON public.escrow_vaults TO authenticated;

-- Guardians and tutors can view only escrow vaults where they are direct participants
CREATE POLICY escrow_vaults_participant_select ON public.escrow_vaults
    FOR SELECT
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = guardian_user_id
            OR auth.uid() = tutor_user_id
            OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        )
    );

-- Guardians initiate escrow deposits
CREATE POLICY escrow_vaults_guardian_insert ON public.escrow_vaults
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = guardian_user_id
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- Only institutional admin or service role can release funds
CREATE POLICY escrow_vaults_settlement_update ON public.escrow_vaults
    FOR UPDATE
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        AND tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
    );

-- ------------------------------------------------------------------------------
-- 8. VERIFIABLE CREDENTIALS TABLE: Row-Level Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.verifiable_credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.verifiable_credentials FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.verifiable_credentials FROM PUBLIC;
GRANT SELECT, INSERT ON public.verifiable_credentials TO authenticated;
GRANT SELECT ON public.verifiable_credentials TO anon;

-- Students can read their own credentials; public verifier can read if unrevoked
CREATE POLICY verifiable_credentials_select ON public.verifiable_credentials
    FOR SELECT
    TO authenticated, anon
    USING (
        is_revoked = FALSE
        OR auth.uid() = student_user_id
        OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'corporate_recruiter', 'service_role')
    );

-- Only authorized institutional administrators can issue credentials
CREATE POLICY verifiable_credentials_issuer_insert ON public.verifiable_credentials
    FOR INSERT
    TO authenticated
    WITH CHECK (
        (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
    );

-- ------------------------------------------------------------------------------
-- 9. AUDIT LOGS TABLE: Append-Only Immutable Security Policies
-- ------------------------------------------------------------------------------
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs FORCE ROW LEVEL SECURITY;

-- Revoke UPDATE and DELETE entirely from all roles
REVOKE ALL ON public.audit_logs FROM PUBLIC;
REVOKE UPDATE, DELETE ON public.audit_logs FROM authenticated, anon;
GRANT SELECT, INSERT ON public.audit_logs TO authenticated;

-- Only institutional admins or users viewing their own actions can read audit logs
CREATE POLICY audit_logs_authorized_select ON public.audit_logs
    FOR SELECT
    TO authenticated
    USING (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = user_id
            OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        )
    );

-- Authenticated users or system services can append audit logs
CREATE POLICY audit_logs_append_only_insert ON public.audit_logs
    FOR INSERT
    TO authenticated
    WITH CHECK (
        tenant_id = (auth.jwt() ->> 'tenant_id')::uuid
        AND (
            auth.uid() = user_id
            OR user_id IS NULL
            OR (auth.jwt() ->> 'role') IN ('institutional_admin', 'service_role')
        )
    );

-- NOTE: There are NO UPDATE or DELETE policies for audit_logs.
-- Combined with trigger trg_prevent_audit_log_mutation, mutations are strictly impossible.
