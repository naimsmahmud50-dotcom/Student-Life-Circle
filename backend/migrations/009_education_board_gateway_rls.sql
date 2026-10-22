-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Ministry Accreditation & National Curriculum API Gateway
-- TOPIC:     Phase 131 National Education Board Webhook Clearinghouse & Ed25519 Signatures
-- FILE:      backend/migrations/009_education_board_gateway_rls.sql
-- PHASE:     Phase 131 - National Curriculum Accreditation API Gateway
-- PURPOSE:   Database migration schema establishing board_accreditation_nodes,
--            board_webhook_events, verifiable_credentials_batch, and gateway_audit_logs
--            tables with strict Supabase Row Level Security (RLS) and audit indices.
-- STANDARDS: Zero-Emoji, ASVS L2, Ed25519 Cryptographic Signatures, Rate Limiting
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Board Accreditation Nodes Table
CREATE TABLE IF NOT EXISTS public.board_accreditation_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_code VARCHAR(32) NOT NULL UNIQUE,
    name_bn VARCHAR(255) NOT NULL,
    name_en VARCHAR(255) NOT NULL,
    endpoint_url VARCHAR(255) NOT NULL,
    public_key_hex VARCHAR(128) NOT NULL,
    whitelisted_cidrs JSONB NOT NULL DEFAULT '[]'::jsonb,
    rate_limit_rpm INT NOT NULL DEFAULT 60,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Board Webhook Events Table (Cryptographically Verified)
CREATE TABLE IF NOT EXISTS public.board_webhook_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_board VARCHAR(32) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    signature_hex VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PROCESSED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Verifiable Credentials Batch Table (W3C Standard)
CREATE TABLE IF NOT EXISTS public.verifiable_credentials_batch (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id VARCHAR(64) NOT NULL UNIQUE,
    issuing_board VARCHAR(32) NOT NULL,
    credential_type VARCHAR(64) NOT NULL,
    total_credentials INT NOT NULL DEFAULT 0,
    verified_credentials INT NOT NULL DEFAULT 0,
    raw_vc_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Gateway Security Audit Logs Table (Append-Only)
CREATE TABLE IF NOT EXISTS public.gateway_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_code VARCHAR(32) NOT NULL,
    client_ip VARCHAR(64) NOT NULL,
    action VARCHAR(64) NOT NULL,
    is_authorized BOOLEAN NOT NULL,
    signature_verified BOOLEAN NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Enable & Force Row Level Security (100% Policy Enforcement)
ALTER TABLE public.board_accreditation_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.board_accreditation_nodes FORCE ROW LEVEL SECURITY;

ALTER TABLE public.board_webhook_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.board_webhook_events FORCE ROW LEVEL SECURITY;

ALTER TABLE public.verifiable_credentials_batch ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.verifiable_credentials_batch FORCE ROW LEVEL SECURITY;

ALTER TABLE public.gateway_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gateway_audit_logs FORCE ROW LEVEL SECURITY;

-- 7. RLS Policy: Ministry Admin & Service Role Clearance
DROP POLICY IF EXISTS "Service role & Ministry admin node access" ON public.board_accreditation_nodes;
CREATE POLICY "Service role & Ministry admin node access"
ON public.board_accreditation_nodes
FOR ALL
USING (
    (auth.jwt() ->> 'role' = 'service_role')
    OR (auth.jwt() ->> 'role' = 'ministry_admin')
);

DROP POLICY IF EXISTS "Service role & Ministry admin webhook access" ON public.board_webhook_events;
CREATE POLICY "Service role & Ministry admin webhook access"
ON public.board_webhook_events
FOR ALL
USING (
    (auth.jwt() ->> 'role' = 'service_role')
    OR (auth.jwt() ->> 'role' = 'ministry_admin')
);

DROP POLICY IF EXISTS "Service role & Ministry admin credentials access" ON public.verifiable_credentials_batch;
CREATE POLICY "Service role & Ministry admin credentials access"
ON public.verifiable_credentials_batch
FOR ALL
USING (
    (auth.jwt() ->> 'role' = 'service_role')
    OR (auth.jwt() ->> 'role' = 'ministry_admin')
);

DROP POLICY IF EXISTS "Service role & Ministry admin audit logs access" ON public.gateway_audit_logs;
CREATE POLICY "Service role & Ministry admin audit logs access"
ON public.gateway_audit_logs
FOR ALL
USING (
    (auth.jwt() ->> 'role' = 'service_role')
    OR (auth.jwt() ->> 'role' = 'ministry_admin')
);

-- 8. High-Performance Query Acceleration Indices
CREATE INDEX IF NOT EXISTS idx_board_nodes_code ON public.board_accreditation_nodes(node_code);
CREATE INDEX IF NOT EXISTS idx_board_webhook_events_source ON public.board_webhook_events(source_board);
CREATE INDEX IF NOT EXISTS idx_board_webhook_created_at ON public.board_webhook_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_gateway_audit_created_at ON public.gateway_audit_logs(created_at DESC);
