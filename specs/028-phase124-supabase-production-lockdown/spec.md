<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 124 Supabase Production Security Lockdown & Strix Audit
FILE:      specs/028-phase124-supabase-production-lockdown/spec.md
PHASE:     Phase 124 - Supabase Production Security Lockdown & Strix Audit
PURPOSE:   Technical specifications for enterprise-grade Supabase hardening per Strix-Supabase
           playbook: 100% RLS lockdown, private storage buckets, secret role key isolation,
           and PostgREST enumeration defense.
STANDARDS: Strix-Supabase Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
-->

# Specification: Feature 028 — Phase 124 Supabase Production Security Lockdown & Strix Audit

## 1. Problem Statement & Mission
Educational infrastructure housing minors, national curricula, and high-stakes examination telemetry requires defense-in-depth database and API layer isolation. Supabase applications are susceptible to common attack vectors documented in the `/strix-supabase` playbook:
- Mis-scoped Row Level Security (missing UPDATE/DELETE/INSERT checks or client-supplied IDs trusted over `auth.uid()`).
- Information disclosure via PostgREST count inference (`Prefer: count=exact`) and unbounded `ILIKE` wildcard queries.
- Stored XSS and MIME sniffing in storage buckets (malicious SVG/HTML uploads).
- Exposure of `service_role` keys or `sb_secret_` tokens in client-side bundles.

Phase 124 institutes absolute zero-trust verification across database migrations, core validators, storage quarantine, and automated Strix security scanning.

## 2. Security Requirements & Attack Vectors

### Vector Category A: Row Level Security (RLS) Lockdown
- **Tables Enforced**: `public.users`, `public.profiles`, `public.student_profiles`, `public.quiz_attempts`, `public.tuition_escrow`, `public.credentials`, `public.audit_logs`.
- **Direct Binding**: All CRUD policies must strictly bind to `auth.uid() = user_id`. Client-provided IDs in request bodies must never override JWT claims.
- **Table Security**: Both `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY` must be executed to prevent role escalation.
- **Immutability Trigger**: `public.audit_logs` must have `REVOKE UPDATE, DELETE` applied and an active PostgreSQL trigger preventing modification or deletion.

### Vector Category B: Private Storage Buckets & Anti-XSS Defense
- **Bucket Isolation**: `student-documents`, `verified-cvs`, `escrow-receipts`, `exam-answers`, `institutional-transcripts` designated as strictly private.
- **Signed URL Policy**: 15-minute (900 seconds) maximum TTL on signed download URLs with HMAC-SHA256 signature verification.
- **Security Response Headers**: Every signed download must enforce:
  - `Content-Disposition: attachment; filename="..."`
  - `X-Content-Type-Options: nosniff`
- **MIME Magic Byte & XSS Quarantine**: Active binary inspection detecting SVG scripts, HTML tags, PHP code, and file magic byte mismatches.

### Vector Category C: PostgREST & RPC Protection
- **Count Inference Defense**: Strip `Prefer: count=exact` from unprivileged or anonymous requests on sensitive tables.
- **Wildcard Enumeration Defense**: Disallow unbounded wildcard ILIKE queries on identifiers, emails, and phone numbers.
- **Parameter Pollution Defense**: Block null bytes (`\x00`), CRLF sequences, and SQL injection probes (`DROP TABLE`, `UNION SELECT`).

### Vector Category D: Secret Role Key Hygiene
- Verify zero exposure of `service_role` keys or `sb_secret_` tokens in frontend code bundles.
- Ensure only `sb_publishable_` or public anon keys exist in client configurations.
