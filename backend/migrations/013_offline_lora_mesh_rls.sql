/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Rural Resilience & Offline SMS/LoRa Exam Synchronizer
 * TOPIC:     Phase 135 Ultra-Compressed Binary Payloads & Offline Disaster Recovery
 * FILE:      backend/migrations/013_offline_lora_mesh_rls.sql
 * PHASE:     Phase 135 - Offline LoRa & SMS-Bridge Exam Synchronizer
 * PURPOSE:   Database migration schema establishing rural_exam_packets,
 *            lora_gateway_nodes, offline_signed_answer_sheets, and
 *            reconciliation_audit_logs tables with strict Supabase RLS.
 * STANDARDS: Zero-Emoji, Disaster Resilient, Cryptographic Signatures, Low-Bandwidth
 */

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. LoRa Gateway Nodes Table
CREATE TABLE IF NOT EXISTS public.lora_gateway_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id VARCHAR(64) NOT NULL UNIQUE,
    region VARCHAR(128) NOT NULL,
    frequency_mhz NUMERIC(6, 2) NOT NULL DEFAULT 433.00,
    bandwidth_khz NUMERIC(6, 2) NOT NULL DEFAULT 125.00,
    spreading_factor VARCHAR(16) NOT NULL DEFAULT 'SF7',
    battery_percentage NUMERIC(5, 2) NOT NULL DEFAULT 100.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_heartbeat TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Rural Exam Packets Table (Encapsulating Binary Payloads)
CREATE TABLE IF NOT EXISTS public.rural_exam_packets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    packet_id VARCHAR(64) NOT NULL UNIQUE,
    student_id VARCHAR(64) NOT NULL,
    exam_id VARCHAR(64) NOT NULL,
    transport_channel VARCHAR(32) NOT NULL,
    packet_seq_num INTEGER NOT NULL DEFAULT 1,
    total_bytes INTEGER NOT NULL,
    hex_pdu TEXT NOT NULL,
    base85_pdu TEXT NOT NULL,
    crc16_checksum VARCHAR(8) NOT NULL,
    signature_hex VARCHAR(64) NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    gateway_node_id VARCHAR(64),
    rssi_dbm NUMERIC(5, 1),
    snr_db NUMERIC(5, 1),
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Offline Signed Answer Sheets Table (Decoded & Reconciled Records)
CREATE TABLE IF NOT EXISTS public.offline_signed_answer_sheets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(64) NOT NULL,
    exam_id VARCHAR(64) NOT NULL,
    packet_id VARCHAR(64) NOT NULL REFERENCES public.rural_exam_packets(packet_id) ON DELETE CASCADE,
    answers_count INTEGER NOT NULL DEFAULT 100,
    answers_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
    computed_score NUMERIC(6, 2) NOT NULL DEFAULT 0.00,
    total_marks NUMERIC(6, 2) NOT NULL DEFAULT 100.00,
    grade VARCHAR(8) NOT NULL DEFAULT 'F',
    is_duplicate BOOLEAN NOT NULL DEFAULT FALSE,
    signature_verified BOOLEAN NOT NULL DEFAULT FALSE,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_student_exam_sheet UNIQUE (student_id, exam_id)
);

-- 5. Reconciliation Audit Logs Table (Immutable Disaster Recovery Ledger)
CREATE TABLE IF NOT EXISTS public.reconciliation_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    log_id VARCHAR(64) NOT NULL UNIQUE,
    packet_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    actor_type VARCHAR(64) NOT NULL DEFAULT 'SYSTEM_GATEWAY',
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Indexes for Performance & Deduplication Lookups
CREATE INDEX IF NOT EXISTS idx_lora_nodes_region ON public.lora_gateway_nodes(region);
CREATE INDEX IF NOT EXISTS idx_rural_packets_student ON public.rural_exam_packets(student_id);
CREATE INDEX IF NOT EXISTS idx_rural_packets_exam ON public.rural_exam_packets(exam_id);
CREATE INDEX IF NOT EXISTS idx_rural_packets_transport ON public.rural_exam_packets(transport_channel);
CREATE INDEX IF NOT EXISTS idx_offline_sheets_student ON public.offline_signed_answer_sheets(student_id);
CREATE INDEX IF NOT EXISTS idx_reconciliation_packet ON public.reconciliation_audit_logs(packet_id);

-- 7. Enable and Force Row Level Security (100% RLS Enforcement)
ALTER TABLE public.lora_gateway_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lora_gateway_nodes FORCE ROW LEVEL SECURITY;

ALTER TABLE public.rural_exam_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rural_exam_packets FORCE ROW LEVEL SECURITY;

ALTER TABLE public.offline_signed_answer_sheets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.offline_signed_answer_sheets FORCE ROW LEVEL SECURITY;

ALTER TABLE public.reconciliation_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reconciliation_audit_logs FORCE ROW LEVEL SECURITY;

-- 8. Policies for LoRa Gateway Nodes
DROP POLICY IF EXISTS lora_nodes_select_policy ON public.lora_gateway_nodes;
CREATE POLICY lora_nodes_select_policy ON public.lora_gateway_nodes
    FOR SELECT
    USING (TRUE);

DROP POLICY IF EXISTS lora_nodes_admin_policy ON public.lora_gateway_nodes;
CREATE POLICY lora_nodes_admin_policy ON public.lora_gateway_nodes
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role' OR
        auth.jwt() ->> 'email' LIKE '%@edu.bd'
    );

-- 9. Policies for Rural Exam Packets (Tenant Isolation)
DROP POLICY IF EXISTS rural_packets_student_select ON public.rural_exam_packets;
CREATE POLICY rural_packets_student_select ON public.rural_exam_packets
    FOR SELECT
    USING (
        (auth.uid())::text = student_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS rural_packets_student_insert ON public.rural_exam_packets;
CREATE POLICY rural_packets_student_insert ON public.rural_exam_packets
    FOR INSERT
    WITH CHECK (
        (auth.uid())::text = student_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS rural_packets_service_all ON public.rural_exam_packets;
CREATE POLICY rural_packets_service_all ON public.rural_exam_packets
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role'
    );

-- 10. Policies for Offline Signed Answer Sheets
DROP POLICY IF EXISTS offline_sheets_student_select ON public.offline_signed_answer_sheets;
CREATE POLICY offline_sheets_student_select ON public.offline_signed_answer_sheets
    FOR SELECT
    USING (
        (auth.uid())::text = student_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS offline_sheets_service_all ON public.offline_signed_answer_sheets;
CREATE POLICY offline_sheets_service_all ON public.offline_signed_answer_sheets
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role'
    );

-- 11. Policies for Reconciliation Audit Logs (Immutable Append-Only Audit)
DROP POLICY IF EXISTS reconciliation_logs_select ON public.reconciliation_audit_logs;
CREATE POLICY reconciliation_logs_select ON public.reconciliation_audit_logs
    FOR SELECT
    USING (
        details ->> 'student_id' = (auth.uid())::text OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS reconciliation_logs_service_insert ON public.reconciliation_audit_logs;
CREATE POLICY reconciliation_logs_service_insert ON public.reconciliation_audit_logs
    FOR INSERT
    WITH CHECK (
        auth.jwt() ->> 'role' = 'service_role'
    );
