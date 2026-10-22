<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 111 Supabase Security Hardening & Zero-Trust RLS Audit
FILE:      specs/015-phase111-supabase-security-hardening/plan.md
PHASE:     Phase 111 - Supabase Security Hardening & Zero-Trust RLS Audit
PURPOSE:   Establishes zero-trust Row Level Security (RLS) enforcement, PostgREST query
           hardening, private storage quarantine with MIME-sniffing defense, and service_role
           key isolation according to the Strix-Supabase penetration benchmark.
STANDARDS: Strix-Supabase Security Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-->

# Implementation Plan: Phase 111 — Supabase Security Hardening & Zero-Trust RLS Audit

## Architecture Overview
The Supabase security architecture integrates four defense rings:
1. **Database Layer (RLS)**: Enforced via PostgreSQL policies where `FORCE ROW LEVEL SECURITY` prevents table owners or standard roles from bypassing row access control. Tables reject cross-tenant reads and reject client-specified owner overrides.
2. **PostgREST Query Gatekeeper**: Validates filter syntax, sanitizes wildcard `ILIKE` patterns, blocks parameter pollution, and disallows unauthorized count enumeration.
3. **Storage Security & Anti-XSS Quarantine**: Private buckets for educational transcripts and credentials, time-bounded HMAC-SHA256 signed URLs (900s TTL), forced `Content-Disposition: attachment`, and `nosniff` headers.
4. **Key Hygiene & Zero-Leak Auditing**: Static bundle scans ensuring zero `service_role` secrets in frontend client code.

## Component Breakdown

### Step 1: SQL Migration (`backend/migrations/003_hardened_supabase_rls.sql`)
- Ensure RLS enabled and forced on `users`, `profiles`, `quiz_attempts`, `tuition_escrow`, `credentials`, `audit_logs`.
- Define policies:
  - `users`: Authenticated read/update only where `auth.uid() = id`.
  - `profiles`: Minors masked unless verified guardian; writes require `auth.uid() = user_id`.
  - `quiz_attempts`: SELECT, INSERT, UPDATE, DELETE bound to `auth.uid() = user_id`.
  - `tuition_escrow`: Only student (payer) or tutor (payee) can access; dispute status changes require verified identity.
  - `credentials`: Public can verify via valid proof hash; updates/deletions restricted.
  - `audit_logs`: INSERT permitted; UPDATE and DELETE permanently blocked.

### Step 2: Supabase Security Validator (`backend/app/core/supabase_security_validator.py`)
- `SupabaseSecurityValidator` class:
  - `validate_token(token)`: Validates JWT claims (`sub`, `aud=authenticated`, `iss`, expiration).
  - `sanitize_postgrest_query(params, headers)`: Detects parameter pollution, blocks `Prefer: count=exact` on PII, limits wildcard `ILIKE`.
  - `verify_user_binding(token, requested_user_id)`: Enforces zero trust by ensuring `token.sub == requested_user_id`.

### Step 3: Storage Quarantine Service (`backend/app/services/storage_quarantine_service.py`)
- `StorageQuarantineService` class:
  - Handles private buckets: `student-documents`, `verified-cvs`, `escrow-receipts`.
  - Inspects file payloads for dangerous MIME types (`image/svg+xml`, `text/html`, executable payloads) and quarantines suspicious files.
  - Generates time-limited signed URLs (15 min TTL = 900s) with HMAC-SHA256 signatures.
  - Returns enforced HTTP headers: `Content-Disposition: attachment; filename="..."` and `X-Content-Type-Options: nosniff`.

### Step 4: Supabase Security Audit Script (`backend/scripts/run_supabase_security_audit.py`)
- Audits 20+ attack vectors per `/strix-supabase`:
  - Cross-tenant RLS bypass
  - IDOR user parameter manipulation
  - Wildcard ILIKE count inference
  - Direct public access to private storage
  - Stored XSS SVG injection via storage
  - Next.js client bundle secret scan (ensuring `service_role` is absent from `frontend/`)
- Outputs structured JSON report in `backend/reports/supabase-security-audit-report.json`.

### Step 5: Test Automation (`backend/tests/test_phase111_supabase_security_hardening.py`)
- Unit and integration tests verifying RLS policies, token validation, query sanitization, storage quarantine, audit script, and zero-emoji compliance.
