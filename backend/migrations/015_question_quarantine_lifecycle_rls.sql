/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Question Bank Quarantine Lifecycle & Audit Trail
 * TOPIC:     Single-Click Quarantine, Safe Release/Restore & Immutable Audit Log
 * FILE:      backend/migrations/015_question_quarantine_lifecycle_rls.sql
 * PURPOSE:   Database migration schema establishing question status lifecycles,
 *            quarantine reasons, actor attribution, affected attempt counters,
 *            and dedicated immutable question quarantine audit logs table with
 *            strict Supabase Row-Level Security (RLS).
 * STANDARDS: Zero-Emoji, Non-destructive, Reversible, Strict Role Isolation
 *
 * ROLLBACK INSTRUCTIONS:
 * ------------------------------------------------------------------------------
 * DROP TABLE IF EXISTS public.question_quarantine_audit_logs CASCADE;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS status;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS quarantine_reason;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS quarantined_by;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS quarantined_at;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS restored_by;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS restored_at;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS restore_reason;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS reports_count;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS primary_issue;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS affected_attempts_count;
 * ------------------------------------------------------------------------------
 */

-- 1. Ensure Extensions Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Non-Destructive Column Additions to question_items
ALTER TABLE public.question_items 
    ADD COLUMN IF NOT EXISTS status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    ADD COLUMN IF NOT EXISTS quarantine_reason TEXT,
    ADD COLUMN IF NOT EXISTS quarantined_by VARCHAR(64),
    ADD COLUMN IF NOT EXISTS quarantined_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS restored_by VARCHAR(64),
    ADD COLUMN IF NOT EXISTS restored_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS restore_reason TEXT,
    ADD COLUMN IF NOT EXISTS reports_count INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS primary_issue VARCHAR(255),
    ADD COLUMN IF NOT EXISTS affected_attempts_count INT NOT NULL DEFAULT 0;

-- 3. Dedicated Immutable Question Quarantine Audit Log Table
CREATE TABLE IF NOT EXISTS public.question_quarantine_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    audit_id VARCHAR(64) NOT NULL UNIQUE,
    question_id VARCHAR(64) NOT NULL,
    action VARCHAR(32) NOT NULL, -- 'QUARANTINE_QUESTION', 'RESTORE_QUESTION'
    actor_id VARCHAR(64) NOT NULL,
    actor_role VARCHAR(64) NOT NULL,
    reason TEXT NOT NULL,
    affected_attempts_count INT NOT NULL DEFAULT 0,
    recalculated BOOLEAN NOT NULL DEFAULT FALSE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. High-Performance Query Indices
CREATE INDEX IF NOT EXISTS idx_question_items_quarantine_status 
    ON public.question_items (status, is_quarantined);

CREATE INDEX IF NOT EXISTS idx_question_items_reports 
    ON public.question_items (reports_count DESC, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_quarantine_audit_question 
    ON public.question_quarantine_audit_logs (question_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_quarantine_audit_timestamp 
    ON public.question_quarantine_audit_logs (timestamp DESC);

-- 5. Row-Level Security Lockdown for question_quarantine_audit_logs
ALTER TABLE public.question_quarantine_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.question_quarantine_audit_logs FORCE ROW LEVEL SECURITY;

REVOKE ALL ON public.question_quarantine_audit_logs FROM PUBLIC;
GRANT SELECT, INSERT ON public.question_quarantine_audit_logs TO authenticated;

-- Policy: Only Admins and Subject Reviewers can view quarantine audit logs
DROP POLICY IF EXISTS quarantine_audit_logs_admin_read ON public.question_quarantine_audit_logs;
CREATE POLICY quarantine_audit_logs_admin_read ON public.question_quarantine_audit_logs
    FOR SELECT
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('admin', 'subject_reviewer', 'institutional_admin', 'service_role')
        OR (auth.jwt() -> 'app_metadata' -> 'roles') ?| ARRAY['admin', 'subject_reviewer', 'institutional_admin']
    );

-- Policy: Insert allowed for authorized reviewers and admins
DROP POLICY IF EXISTS quarantine_audit_logs_admin_insert ON public.question_quarantine_audit_logs;
CREATE POLICY quarantine_audit_logs_admin_insert ON public.question_quarantine_audit_logs
    FOR INSERT
    TO authenticated
    WITH CHECK (
        (auth.jwt() ->> 'role') IN ('admin', 'subject_reviewer', 'institutional_admin', 'service_role')
        OR (auth.jwt() -> 'app_metadata' -> 'roles') ?| ARRAY['admin', 'subject_reviewer', 'institutional_admin']
    );

-- 6. Immutability Enforcement Trigger (Strict ASVS L2 Audit Log Integrity)
CREATE OR REPLACE FUNCTION reject_quarantine_audit_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit records are strictly immutable and cannot be updated or deleted.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_quarantine_audit_mutation ON public.question_quarantine_audit_logs;
CREATE TRIGGER trg_prevent_quarantine_audit_mutation
    BEFORE UPDATE OR DELETE ON public.question_quarantine_audit_logs
    FOR EACH ROW
    EXECUTE FUNCTION reject_quarantine_audit_mutation();

-- 7. Policy Updates for question_items Table
-- Allow Admins and Subject Reviewers full SELECT visibility on all questions (including quarantined)
DROP POLICY IF EXISTS question_items_admin_select_all ON public.question_items;
CREATE POLICY question_items_admin_select_all ON public.question_items
    FOR SELECT
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('admin', 'subject_reviewer', 'institutional_admin', 'service_role')
        OR (auth.jwt() -> 'app_metadata' -> 'roles') ?| ARRAY['admin', 'subject_reviewer', 'institutional_admin']
    );

-- Allow Admins and Subject Reviewers to UPDATE quarantine and status fields on question_items
DROP POLICY IF EXISTS question_items_admin_quarantine_update ON public.question_items;
CREATE POLICY question_items_admin_quarantine_update ON public.question_items
    FOR UPDATE
    TO authenticated
    USING (
        (auth.jwt() ->> 'role') IN ('admin', 'subject_reviewer', 'institutional_admin', 'service_role')
        OR (auth.jwt() -> 'app_metadata' -> 'roles') ?| ARRAY['admin', 'subject_reviewer', 'institutional_admin']
    )
    WITH CHECK (
        (auth.jwt() ->> 'role') IN ('admin', 'subject_reviewer', 'institutional_admin', 'service_role')
        OR (auth.jwt() -> 'app_metadata' -> 'roles') ?| ARRAY['admin', 'subject_reviewer', 'institutional_admin']
    );
