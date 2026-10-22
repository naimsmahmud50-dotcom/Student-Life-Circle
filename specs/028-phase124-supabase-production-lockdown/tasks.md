<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 124 Supabase Production Security Lockdown & Strix Audit Tasks
FILE:      specs/028-phase124-supabase-production-lockdown/tasks.md
PHASE:     Phase 124 - Supabase Production Security Lockdown & Strix Audit
PURPOSE:   Actionable, ordered checklist for creating Migration 004, updating core validators,
           storage service, audit runner, and comprehensive test suite.
STANDARDS: Strix-Supabase Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-->

# Tasks: Feature 028 — Phase 124 Supabase Production Security Lockdown & Strix Audit

## Tasks Ledger

- [x] T001 Create `backend/migrations/004_production_supabase_lockdown.sql`
  - Include Phase 124 Developer Architecture Note header
  - Ensure `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY` on all 7 tables
  - Define strict CRUD policies with `auth.uid() = user_id`
  - Add `REVOKE UPDATE, DELETE ON public.audit_logs`
  - Add `trg_enforce_strict_audit_log_immutability` trigger
  - Ensure strict zero emojis

- [x] T002 Upgrade `backend/app/core/supabase_security_validator.py`
  - Include Phase 124 Developer Architecture Note header
  - Ensure JWT algorithm allowlist (`HS256`, `RS256`) rejecting `none`
  - Ensure audience pinning (`authenticated`, `student-life-circle-auth`, `ogrojatra-production-aud`)
  - Ensure parameter pollution defense (blocking `\x00`, newlines, carriage returns)
  - Ensure count inference defense stripping `Prefer: count=exact`
  - Ensure SQL injection and wildcard ILIKE blocking
  - Ensure strict zero emojis

- [x] T003 Upgrade `backend/app/services/storage_quarantine_service.py`
  - Include Phase 124 Developer Architecture Note header
  - Ensure private bucket designation (`student-documents`, `verified-cvs`, `escrow-receipts`, `exam-answers`, `institutional-transcripts`)
  - Enforce 15-minute (900 seconds) max TTL on signed URLs
  - Enforce headers: `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`
  - Ensure active MIME sniffing and Stored XSS quarantine (SVG, HTML, polyglots)
  - Ensure strict zero emojis

- [x] T004 Upgrade `backend/scripts/run_supabase_security_audit.py`
  - Include Phase 124 Developer Architecture Note header
  - Verify all 25 Strix attack vectors pass with 0 vulnerabilities
  - Support both `003_hardened_supabase_rls.sql` and `004_production_supabase_lockdown.sql`
  - Export audit report to `backend/reports/supabase-security-audit-report.json`
  - Ensure strict zero emojis

- [x] T005 Implement automated test `backend/tests/test_phase124_supabase_production_lockdown.py`
  - Test Developer Architecture Notes on all 5 target files
  - Test Migration 004 RLS, force RLS, user_id binding, and audit log immutability
  - Test JWT claim verification, algorithm rejection, and audience pinning
  - Test PostgREST query hardening (count inference, parameter pollution, SQL injection)
  - Test Storage bucket privacy, signed URL 900s TTL, security headers, and MIME quarantine
  - Test 25-vector Strix audit execution asserting 25/25 passed and 0 failed
  - Test strict Zero-Emoji compliance across all target files

- [x] T006 Build & Test Execution
  - Run `python3 backend/scripts/run_supabase_security_audit.py` (25/25 vectors passed)
  - Run `python3 -m unittest backend/tests/test_phase124_supabase_production_lockdown.py` (8/8 tests passed)
  - Run `python3 backend/scripts/run_zero_emoji_sweep.py` (0 violations)
  - Run master platform discovery: `python3 -m unittest discover -s backend/tests -p "test_*.py"` (1,411/1,411 tests passed)
