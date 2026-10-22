-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Micro-Scholarship Disbursement Vault
-- TOPIC:     Phase 133 Mobile Financial Services Gateway & Proof-of-Merit Verification
-- FILE:      backend/migrations/011_scholarship_disbursement_rls.sql
-- PHASE:     Phase 133 - Direct-to-Mobile Scholarship Disbursement Vault
-- PURPOSE:   Database migration schema establishing scholarship_endowment_vaults,
--            micro_scholarship_applications, mfs_disbursement_ledger, and
--            scholarship_fraud_audit_logs tables with strict financial immutability
--            and Supabase Row Level Security (RLS).
-- STANDARDS: Zero-Emoji, Financial Immutable Audit, ASVS L2, Fraud Prevention
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Scholarship Endowment Vaults Table
CREATE TABLE IF NOT EXISTS public.scholarship_endowment_vaults (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vault_code VARCHAR(32) NOT NULL UNIQUE,
    name_bn VARCHAR(255) NOT NULL,
    name_en VARCHAR(255) NOT NULL,
    total_fund_bdt NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    disbursed_fund_bdt NUMERIC(14,2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Micro-Scholarship Applications Table
CREATE TABLE IF NOT EXISTS public.micro_scholarship_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id VARCHAR(64) NOT NULL UNIQUE,
    user_id UUID NOT NULL,
    nid_or_brn VARCHAR(32) NOT NULL,
    district VARCHAR(64) NOT NULL,
    board_gpa NUMERIC(3,2) NOT NULL,
    olympiad_rank INT,
    tier VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    verification_proof_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. MFS Disbursement Ledger Table (Immutable Financial Records)
CREATE TABLE IF NOT EXISTS public.mfs_disbursement_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id VARCHAR(64) NOT NULL UNIQUE,
    application_id VARCHAR(64) NOT NULL,
    user_id UUID NOT NULL,
    amount_bdt NUMERIC(10,2) NOT NULL,
    mfs_provider VARCHAR(16) NOT NULL,
    wallet_msisdn VARCHAR(20) NOT NULL,
    idempotency_key VARCHAR(64) NOT NULL UNIQUE,
    mfs_reference VARCHAR(64) NOT NULL,
    transaction_hash VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'DISBURSED',
    disbursed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Scholarship Fraud Audit Logs Table (Append-Only)
CREATE TABLE IF NOT EXISTS public.scholarship_fraud_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    flagged_nid VARCHAR(32),
    flagged_wallet VARCHAR(20),
    violation_type VARCHAR(64) NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Financial Ledger Immutability Guard: REVOKE UPDATE & DELETE
REVOKE UPDATE, DELETE ON public.mfs_disbursement_ledger FROM PUBLIC, authenticated, anon;
REVOKE UPDATE, DELETE ON public.scholarship_fraud_audit_logs FROM PUBLIC, authenticated, anon;

-- Immutability trigger function
CREATE OR REPLACE FUNCTION public.fn_block_mfs_ledger_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Financial Immutability Violation: Modifications to MFS Disbursement Ledger are strictly prohibited under ASVS L2.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_block_mfs_ledger_mutation ON public.mfs_disbursement_ledger;
CREATE TRIGGER trg_block_mfs_ledger_mutation
BEFORE UPDATE OR DELETE ON public.mfs_disbursement_ledger
FOR EACH ROW EXECUTE FUNCTION public.fn_block_mfs_ledger_mutation();

-- 7. Enable & Force Row Level Security (100% Policy Enforcement)
ALTER TABLE public.scholarship_endowment_vaults ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scholarship_endowment_vaults FORCE ROW LEVEL SECURITY;

ALTER TABLE public.micro_scholarship_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.micro_scholarship_applications FORCE ROW LEVEL SECURITY;

ALTER TABLE public.mfs_disbursement_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mfs_disbursement_ledger FORCE ROW LEVEL SECURITY;

ALTER TABLE public.scholarship_fraud_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scholarship_fraud_audit_logs FORCE ROW LEVEL SECURITY;

-- 8. Row Level Security Policies: Endowment Vaults (Public read active, service role write)
DROP POLICY IF EXISTS "Anyone can view active endowment vaults" ON public.scholarship_endowment_vaults;
CREATE POLICY "Anyone can view active endowment vaults"
ON public.scholarship_endowment_vaults
FOR SELECT
USING (is_active = TRUE);

DROP POLICY IF EXISTS "Service role manages endowment vaults" ON public.scholarship_endowment_vaults;
CREATE POLICY "Service role manages endowment vaults"
ON public.scholarship_endowment_vaults
FOR ALL
USING (auth.jwt() ->> 'role' = 'service_role');

-- 9. Row Level Security Policies: Applications
DROP POLICY IF EXISTS "Users manage their own scholarship applications" ON public.micro_scholarship_applications;
CREATE POLICY "Users manage their own scholarship applications"
ON public.micro_scholarship_applications
FOR ALL
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 10. Row Level Security Policies: MFS Disbursement Ledger
DROP POLICY IF EXISTS "Users can only view their own disbursements" ON public.mfs_disbursement_ledger;
CREATE POLICY "Users can only view their own disbursements"
ON public.mfs_disbursement_ledger
FOR SELECT
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

DROP POLICY IF EXISTS "Service role inserts disbursements" ON public.mfs_disbursement_ledger;
CREATE POLICY "Service role inserts disbursements"
ON public.mfs_disbursement_ledger
FOR INSERT
WITH CHECK (auth.jwt() ->> 'role' = 'service_role');

-- 11. Row Level Security Policies: Fraud Audit Logs
DROP POLICY IF EXISTS "Service role manages fraud audit logs" ON public.scholarship_fraud_audit_logs;
CREATE POLICY "Service role manages fraud audit logs"
ON public.scholarship_fraud_audit_logs
FOR ALL
USING (auth.jwt() ->> 'role' = 'service_role');

-- 12. Query Optimization & Fraud Defense Indexes
CREATE INDEX IF NOT EXISTS idx_micro_apps_user ON public.micro_scholarship_applications(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_micro_apps_nid ON public.micro_scholarship_applications(nid_or_brn);
CREATE INDEX IF NOT EXISTS idx_mfs_ledger_user ON public.mfs_disbursement_ledger(user_id, disbursed_at DESC);
CREATE INDEX IF NOT EXISTS idx_mfs_ledger_wallet ON public.mfs_disbursement_ledger(wallet_msisdn);
CREATE INDEX IF NOT EXISTS idx_mfs_ledger_idemp ON public.mfs_disbursement_ledger(idempotency_key);
