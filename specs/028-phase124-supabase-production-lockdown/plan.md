<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 124 Supabase Production Security Lockdown & Strix Audit Implementation Plan
FILE:      specs/028-phase124-supabase-production-lockdown/plan.md
PHASE:     Phase 124 - Supabase Production Security Lockdown & Strix Audit
PURPOSE:   Architectural blueprint and phase execution order for hardened database migrations,
           zero-trust validator enhancements, storage quarantine verification, and automated Strix audit.
STANDARDS: Strix-Supabase Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-->

# Plan: Feature 028 — Phase 124 Supabase Production Security Lockdown & Strix Audit

## Architecture & Integration Plan

### Step 1: Migration 004 Creation
- **File**: `backend/migrations/004_production_supabase_lockdown.sql`
- Create idempotent production SQL migration:
  - Enforce `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY` on all 7 target tables (`users`, `profiles`, `student_profiles`, `quiz_attempts`, `tuition_escrow`, `credentials`, `audit_logs`).
  - Drop existing permissive or insecure policies.
  - Create strict per-operation policies with `auth.uid() = user_id` and tenant isolation where applicable.
  - Revoke `UPDATE` and `DELETE` on `public.audit_logs`.
  - Create immutable audit log trigger `trg_enforce_strict_audit_log_immutability`.
  - Include Phase 124 Developer Architecture Note header and strict zero emojis.

### Step 2: Supabase Security Validator Enhancement
- **File**: `backend/app/core/supabase_security_validator.py`
- Update Developer Architecture Note header to Phase 124.
- Strengthen JWT validation:
  - Strict algorithm allowlist (`HS256`, `RS256`), rejecting `none` and symmetric confusion attacks.
  - Audience pinning (`authenticated`, `student-life-circle-auth`, `ogrojatra-production-aud`).
  - Reject expired tokens and tokens with missing `sub` or `role`.
- Strengthen PostgREST query sanitization:
  - Reject parameter pollution with null bytes (`\x00`), newlines, and carriage returns.
  - Strip `Prefer: count=exact` from unprivileged queries.
  - Block SQL injection patterns (`DROP TABLE`, `UNION SELECT`, `OR 1=1`).
  - Block unbounded wildcard ILIKE probes (`%` or `%%`).
- Zero-IDOR validation binding client payload `user_id` to `auth.uid()`.

### Step 3: Storage Quarantine Service Verification
- **File**: `backend/app/services/storage_quarantine_service.py`
- Update Developer Architecture Note header to Phase 124.
- Verify private bucket designations (`student-documents`, `verified-cvs`, `escrow-receipts`, `exam-answers`, `institutional-transcripts`).
- Enforce 15-minute (900 seconds) max TTL on signed download URLs.
- Enforce security headers: `Content-Disposition: attachment; filename="..."` and `X-Content-Type-Options: nosniff`.
- Active MIME sniffing and Stored XSS defense (detecting `<script`, `svg`, polyglots, and magic byte mismatches).

### Step 4: Strix Automated Security Audit Runner
- **File**: `backend/scripts/run_supabase_security_audit.py`
- Update Developer Architecture Note header to Phase 124.
- Update migration file verification to check `004_production_supabase_lockdown.sql` (and fallback/complement `003_hardened_supabase_rls.sql`).
- Execute all 25 Strix penetration vectors and verify 100% pass rate (25/25 vectors passed, 0 failed).

### Step 5: Automated Verification Test Suite
- **File**: `backend/tests/test_phase124_supabase_production_lockdown.py`
- Test 1: Developer Architecture Notes on all 5 target files.
- Test 2: Migration 004 RLS enabled, forced, user_id policy bindings, and audit log immutability.
- Test 3: JWT claim verification, algorithm rejection, and audience pinning.
- Test 4: PostgREST query hardening (count inference, SQL injection, parameter pollution).
- Test 5: Storage bucket privacy, signed URL 900s TTL, security headers, and MIME quarantine.
- Test 6: 25-vector Strix security audit run asserting 25/25 passed and 0 failed.
- Test 7: Strict Zero-Emoji compliance across all target files.

### Step 6: Full Regression Verification
- Run `python3 -m unittest backend/tests/test_phase124_supabase_production_lockdown.py`.
- Run `python3 backend/scripts/run_supabase_security_audit.py`.
- Run master platform discovery: `python3 -m unittest discover -s backend/tests -p "test_*.py"`.
