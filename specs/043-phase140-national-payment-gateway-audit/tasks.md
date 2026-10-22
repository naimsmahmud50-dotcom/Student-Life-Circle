/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      specs/043-phase140-national-payment-gateway-audit/tasks.md
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Actionable, ordered tasks for Phase 140 implementation
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */

# Phase 140 Tasks: National Payment Gateway & Live Security Audit

- [x] **Task 1: SSLCommerz V4 Gateway Integration & Sandbox Configuration**
  - Create `backend/app/services/payment/sslcommerz_service.py` with session initiation, hash validation, and query verification.
  - Update `backend/app/services/payment/sandbox_config.py` with SSLCommerz credentials and environment toggle.
  - Update `backend/app/services/payment/__init__.py` to export new services.

- [x] **Task 2: Escrow Vault 24h Auto-Release & State-Gated Refund Engine**
  - Enhance `backend/app/services/payment/escrow_vault_service.py` to support 24-hour auto-release timers.
  - Implement automated instant refund logic for cancellations $\ge 2$ hours prior, duplicate IPNs, and timeouts.
  - Support tribunal dispute referral for active sessions.

- [x] **Task 3: Automated Hourly Reconciliation Service**
  - Create `backend/app/services/payment/reconciliation_service.py` to poll bKash, Nagad, and SSLCommerz query APIs.
  - Identify pending transactions older than 15 minutes and reconcile states.
  - Trigger auto-release for escrows with expired 24h dispute windows.
  - Append immutable records to the audit ledger.

- [x] **Task 4: Payment Endpoints & Server-Authoritative Checkout**
  - Update `backend/app/api/v1/endpoints/payments.py` with:
    - `/checkout/initiate` (server-calculated pricing, `X-Idempotency-Key` requirement)
    - `/sslcommerz/initiate` and `/ipn/sslcommerz`
    - `/escrow/{contract_id}/auto-release`
    - `/reconciliation/run`
  - Enforce OWASP ASVS Level 2 input validation and error handling.

- [x] **Task 5: Frontend Payment Modal & Tactile UI**
  - Create `frontend/src/components/payment/PaymentDrawer.tsx` supporting bKash, Nagad, and Card payments.
  - Provide server-driven checkout initiation, real-time status feedback, and digital receipt verification view.
  - Ensure Zero-Emoji compliance and Oxford Navy tactile design tokens.

- [x] **Task 6: Automated Test Suite & OWASP ASVS L2 Security Verification**
  - Implement `backend/tests/test_phase140_payment_gateway_audit.py` covering:
    - Test 01: Mandatory Architecture Note headers.
    - Test 02: Zero-Emoji compliance across files.
    - Test 03: Server-authoritative amount validation (tampered amounts rejected).
    - Test 04: Idempotency enforcement & replay protection.
    - Test 05: SSLCommerz IPN verification and session handling.
    - Test 06: bKash & Nagad gateway operations.
    - Test 07: 24h escrow auto-release state transitions.
    - Test 08: Hourly reconciliation engine execution.
    - Test 09: OWASP ASVS L2 security vectors (Rate limiting, secrets masking, SQLi/XSS defense).
    - Test 10: Endpoint integration testing across all Phase 140 API routes.

- [x] **Task 7: Regression Sweep, Build Verification & Audit Artifact**
  - Run full repository test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`: 1,556 tests passing).
  - Run Zero-Emoji sweep script (601 files certified, 0 violations).
  - Rebuild frontend (`npm run build`: 37/37 pages compiled successfully).
  - Generate `PHASE_140_PAYMENT_SECURITY_REPORT.md` artifact.
