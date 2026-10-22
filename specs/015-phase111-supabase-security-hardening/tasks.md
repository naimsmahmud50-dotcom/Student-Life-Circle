<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 111 Supabase Security Hardening & Zero-Trust RLS Audit
FILE:      specs/015-phase111-supabase-security-hardening/tasks.md
PHASE:     Phase 111 - Supabase Security Hardening & Zero-Trust RLS Audit
PURPOSE:   Establishes zero-trust Row Level Security (RLS) enforcement, PostgREST query
           hardening, private storage quarantine with MIME-sniffing defense, and service_role
           key isolation according to the Strix-Supabase penetration benchmark.
STANDARDS: Strix-Supabase Security Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-->

# Tasks: Phase 111 — Supabase Security Hardening & Zero-Trust RLS Audit

## Tasks Ledger

- [x] Task 1: Create Hardened Supabase RLS Migration (`backend/migrations/003_hardened_supabase_rls.sql`)
  - Enable and force RLS on 100% of tables (`users`, `profiles`, `quiz_attempts`, `tuition_escrow`, `credentials`, `audit_logs`)
  - Enforce direct `auth.uid() = user_id` binding on SELECT, INSERT, UPDATE, DELETE
  - Disallow UPDATE/DELETE on `audit_logs` table (immutable append-only)
  - Zero-emoji compliance and standardized developer architecture note
- [x] Task 2: Implement Supabase Security Validator (`backend/app/core/supabase_security_validator.py`)
  - Zero-trust JWT verification (issuer, audience `aud=authenticated`, expiry, tenant binding)
  - PostgREST query hardening (detect parameter pollution, block count inference on PII, sanitize wildcard queries)
  - Enforce zero trust on client-supplied IDs versus authenticated JWT identity
- [x] Task 3: Implement Storage Quarantine Service (`backend/app/services/storage_quarantine_service.py`)
  - Private bucket configuration for sensitive documents (mark sheets, NID, verified CVs)
  - MIME type sniffing inspection (quarantines SVG/HTML to block stored XSS)
  - Time-limited signed URL generator (15-minute TTL / 900s)
  - Enforce `Content-Disposition: attachment; filename="..."` and `X-Content-Type-Options: nosniff` headers
- [x] Task 4: Implement Supabase Security Audit Penetration Scanner (`backend/scripts/run_supabase_security_audit.py`)
  - Automated scanner checking 20+ attack vectors (cross-tenant RLS bypass, IDOR, storage access, bundle leak check)
  - Verify `service_role` key is strictly isolated from frontend client files
  - Output report to `backend/reports/supabase-security-audit-report.json`
- [x] Task 5: Implement Automated Verification Test Suite (`backend/tests/test_phase111_supabase_security_hardening.py`)
  - Validate SQL migration syntax, policies, and table security rules
  - Validate JWT verification and IDOR attack rejection in security validator
  - Validate storage quarantine, SVG XSS blocking, and signed URL generation
  - Validate zero service_role leaks in frontend files
  - Validate zero emojis and mandatory Developer Architecture Note headers
- [x] Task 6: Execute Full Platform Regression Discovery (`python3 -m unittest discover -s backend/tests`)
  - Verify 100% pass rate across 1,336 test cases
