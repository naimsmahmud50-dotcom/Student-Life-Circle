<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 111 Supabase Security Hardening & Zero-Trust RLS Audit
FILE:      specs/015-phase111-supabase-security-hardening/spec.md
PHASE:     Phase 111 - Supabase Security Hardening & Zero-Trust RLS Audit
PURPOSE:   Establishes zero-trust Row Level Security (RLS) enforcement, PostgREST query
           hardening, private storage quarantine with MIME-sniffing defense, and service_role
           key isolation according to the Strix-Supabase penetration benchmark.
STANDARDS: Strix-Supabase Security Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-->

# Feature Specification: Phase 111 — Supabase Security Hardening & Zero-Trust RLS Audit

## 1. Problem Statement & Motivation
Supabase platforms powered by PostgREST and PostgreSQL are exposed to critical attack surfaces if RLS policies are misconfigured, query filters allow inference via exact count hints (`Prefer: count=exact`), storage buckets allow unauthenticated public downloads or SVG/HTML stored XSS, or service role keys leak into client-side bundles.

Phase 111 systematically locks down the database schema, PostgREST access layer, and storage buckets with mathematically proven zero-trust bindings:
1. **Row Level Security (RLS) Absolute Lockdown:**
   - 100% of tables (`users`, `profiles`, `quiz_attempts`, `tuition_escrow`, `credentials`, `audit_logs`) enforce RLS.
   - Every operation (SELECT, INSERT, UPDATE, DELETE) binds strictly to `auth.uid() = user_id`.
   - Never trust client-supplied IDs in JSON payloads; server context verified via cryptographically signed JWTs.
2. **PostgREST Query Hardening:**
   - Disallow unauthorized row-count inference (`Prefer: count=exact` or wildcard `ILIKE` on protected PII).
   - Prevent cross-tenant access and parameter pollution.
3. **Storage Bucket Quarantine & MIME Sniffing Defense:**
   - Private student documents (HSC mark sheets, National ID, verified CVs) must reside in private buckets.
   - Time-limited signed URLs (15-min TTL) with mandatory security response headers:
     `Content-Disposition: attachment; filename="..."`
     `X-Content-Type-Options: nosniff`
   - Quarantine checks for SVG/HTML scripts to eliminate stored Cross-Site Scripting (XSS).
4. **Service Role Key Hygiene:**
   - Verification that `service_role` keys are strictly restricted to backend worker contexts and NEVER leaked into Next.js client builds or API error messages.

## 2. Target Deliverables
1. `backend/migrations/003_hardened_supabase_rls.sql`:
   - Hardened PostgreSQL RLS migration enforcing table lockdown, zero-IDOR policies, and append-only audit logs.
2. `backend/app/core/supabase_security_validator.py`:
   - Zero-trust token validator verifying issuer, audience (`aud=authenticated`), expiry, and principal bindings.
3. `backend/app/services/storage_quarantine_service.py`:
   - Quarantine and signed URL manager with MIME sniffing defense and 15-min TTL expiration.
4. `backend/scripts/run_supabase_security_audit.py`:
   - Automated penetration testing suite checking 20+ attack vectors (cross-tenant access, unsigned storage access, SQLi).
5. `backend/tests/test_phase111_supabase_security_hardening.py`:
   - Comprehensive automated test suite verifying all Phase 111 capabilities.
