# SPECIFICATION: Phase 126 — Grand Final Public Production Rollout, Edge CDN & National Attestation

## 1. Context & Objective
The final culmination of the Ogrojatra Student Growth Platform represents a nationwide, enterprise-grade educational ecosystem. Phase 126 executes the final public production rollout, edge CDN validation, DNSSEC hardening, full SSL/TLS termination, and formal ministerial attestation under the official live custom domain `https://ogrojatra.edu.bd/`.

## 2. Core Functional Requirements
1. **Cloudflare Edge CDN & DNS Architecture**:
   - Apex domain `ogrojatra.edu.bd`, canonical alias `www.ogrojatra.edu.bd`, and API endpoint `api.ogrojatra.edu.bd`.
   - DNSSEC enabled (Algorithm 13, Digest Type 2).
   - Full (Strict) SSL with TLS 1.3 minimum version 1.2, HTTP/3 (QUIC), 0-RTT, and Early Hints.
   - WAF rate limiting protecting authentication and quiz submission endpoints from brute-force floods and scraping attacks.
2. **Production Deployment & SRE Health Gates**:
   - Automated SRE health audit via `./deploy.sh health`.
   - Verification of Nginx HTTP/3 QUIC edge termination, `/ws/` WebSocket upgrade, Sentry zero-PII redaction, and PostgreSQL WAL/PITR recovery.
   - Verification of 100% table Row Level Security (RLS) across Supabase tables, zero token leaks, and zero code emojis.
3. **Formal Grand National Attestation (`GRAND_NATIONAL_ATTESTATION.md`)**:
   - Institutional sign-off documenting 100% completion across all 126 phases.
   - 1,420+ automated tests passing with zero failures and zero errors.
   - Sub-200ms p95 latency under 50,000 concurrent students load.
   - WCAG 2.2 AAA accessibility compliance, mobile-first responsiveness, and zero-emoji purity.
4. **Automated Verification Test Suite**:
   - Implement `backend/tests/test_phase126_grand_final_rollout.py` certifying all rollout criteria.
   - Execute full platform test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`) certifying 1,420+ tests pass with 0 failures and 0 errors.

## 3. Mandatory Standards
- **Zero AI Vibe**: Formal institutional prose reflecting national academic excellence.
- **Strict Zero-Emoji Policy**: Zero unicode emojis across all 560+ files. Pure Lucide SVG icons only.
- **Developer Architecture Note**: Top of all target files must declare Phase 126 headers.
