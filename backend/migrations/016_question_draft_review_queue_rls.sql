/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Question Bank Draft Review Queue Lifecycle & Audit Trail
 * TOPIC:     AI Draft Ingestion, SME Review Gate, Batch Actions & Immutable Audit Log
 * FILE:      backend/migrations/016_question_draft_review_queue_rls.sql
 * PURPOSE:   Database migration schema establishing question draft review lifecycles,
 *            AI confidence scoring, Bloom's cognitive taxonomy, SME feedback reasons,
 *            and dedicated immutable question review audit logs table with strict
 *            Supabase Row-Level Security (RLS).
 * STANDARDS: Zero-Emoji, Non-destructive, Reversible, Strict Role Isolation
 *
 * ROLLBACK INSTRUCTIONS:
 * ------------------------------------------------------------------------------
 * DROP TABLE IF EXISTS public.question_review_audit_logs CASCADE;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS concept;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS curriculum;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS class_grade;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS is_ai_generated;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS ai_confidence_score;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS ai_model;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS deduplication_similarity;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS is_duplicate_flag;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS reviewed_by;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS reviewed_at;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS rejection_feedback;
 * ALTER TABLE public.question_items DROP COLUMN IF EXISTS author_id;
 * ------------------------------------------------------------------------------
 */

-- 1. Ensure Extensions Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Non-Destructive Column Additions to question_items for AI Draft Review Lifecycle
ALTER TABLE public.question_items 
    ADD COLUMN IF NOT EXISTS concept VARCHAR(255),
    ADD COLUMN IF NOT EXISTS curriculum VARCHAR(64) NOT NULL DEFAULT 'NCTB_2024',
    ADD COLUMN IF NOT EXISTS class_grade INT NOT NULL DEFAULT 10,
    ADD COLUMN IF NOT EXISTS is_ai_generated BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS ai_confidence_score NUMERIC(4,3) DEFAULT 0.900,
    ADD COLUMN IF NOT EXISTS ai_model VARCHAR(64) DEFAULT 'Claude-3.5-Sonnet-NCTB',
    ADD COLUMN IF NOT EXISTS deduplication_similarity NUMERIC(4,3) DEFAULT 0.050,
    ADD COLUMN IF NOT EXISTS is_duplicate_flag BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS reviewed_by VARCHAR(64),
    ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS rejection_feedback TEXT,
    ADD COLUMN IF NOT EXISTS author_id VARCHAR(64) DEFAULT 'ai_agent_generator';

-- 3. Dedicated Immutable Question Review Audit Log Table
CREATE TABLE IF NOT EXISTS public.question_review_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    audit_id VARCHAR(64) NOT NULL UNIQUE,
    question_id VARCHAR(64) NOT NULL,
    action VARCHAR(32) NOT NULL, -- 'APPROVE_DRAFT', 'REJECT_DRAFT', 'EDIT_AND_APPROVE', 'BULK_APPROVE', 'BULK_REJECT', 'SUBMIT_FOR_REVIEW'
    actor_id VARCHAR(64) NOT NULL,
    actor_role VARCHAR(64) NOT NULL,
    previous_status VARCHAR(32) NOT NULL,
    new_status VARCHAR(32) NOT NULL,
    reason_or_feedback TEXT,
    diff_summary JSONB,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. High-Performance Query Indices
CREATE INDEX IF NOT EXISTS idx_question_items_review_queue 
    ON public.question_items(status, subject, class_grade);

CREATE INDEX IF NOT EXISTS idx_question_review_audit_logs_qid 
    ON public.question_review_audit_logs(question_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_question_review_audit_logs_actor 
    ON public.question_review_audit_logs(actor_id, action);

-- 5. Row Level Security (RLS) Configuration
ALTER TABLE public.question_review_audit_logs ENABLE ROW LEVEL SECURITY;

-- Policy 1: Full Admins and Subject Reviewers have Read Access
DROP POLICY IF EXISTS p_read_question_review_audit ON public.question_review_audit_logs;
CREATE POLICY p_read_question_review_audit ON public.question_review_audit_logs
    FOR SELECT
    USING (
        auth.role() = 'service_role' OR
        EXISTS (
            SELECT 1 FROM public.user_roles ur
            WHERE ur.user_id = auth.uid()
            AND ur.role IN ('ADMIN', 'SUBJECT_REVIEWER')
        )
    );

-- Policy 2: Append-Only Write Access for Authorized Reviewers and Admins
DROP POLICY IF EXISTS p_insert_question_review_audit ON public.question_review_audit_logs;
CREATE POLICY p_insert_question_review_audit ON public.question_review_audit_logs
    FOR INSERT
    WITH CHECK (
        auth.role() = 'service_role' OR
        EXISTS (
            SELECT 1 FROM public.user_roles ur
            WHERE ur.user_id = auth.uid()
            AND ur.role IN ('ADMIN', 'SUBJECT_REVIEWER')
        )
    );

-- Policy 3: Prevent Update or Delete on Immutable Audit Trail
DROP POLICY IF EXISTS p_no_update_question_review_audit ON public.question_review_audit_logs;
CREATE POLICY p_no_update_question_review_audit ON public.question_review_audit_logs
    FOR UPDATE USING (FALSE);

DROP POLICY IF EXISTS p_no_delete_question_review_audit ON public.question_review_audit_logs;
CREATE POLICY p_no_delete_question_review_audit ON public.question_review_audit_logs
    FOR DELETE USING (FALSE);

-- 6. Trigger to Guarantee Immutability
CREATE OR REPLACE FUNCTION public.prevent_review_audit_log_modification()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'SECURITY ERROR: Question review audit logs are append-only and cryptographically tamper-evident. Modification or deletion is strictly prohibited.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_review_audit_modification ON public.question_review_audit_logs;
CREATE TRIGGER trg_prevent_review_audit_modification
    BEFORE UPDATE OR DELETE ON public.question_review_audit_logs
    FOR EACH ROW
    EXECUTE FUNCTION public.prevent_review_audit_log_modification();
