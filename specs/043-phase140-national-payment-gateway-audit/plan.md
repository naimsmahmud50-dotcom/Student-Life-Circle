/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      specs/043-phase140-national-payment-gateway-audit/plan.md
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Execution plan for multi-gateway checkout, escrow, and security lockdown
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */

# Implementation Plan: Phase 140 — National Payment Gateway & Live Security Audit

## Technical Context
- **Backend Architecture**: FastAPI, Python 3.12, Pydantic v2 data validation, HMAC-SHA256 signature verifications.
- **Gateways**:
  - bKash Merchant Checkout API (v1.2.0-beta)
  - Nagad DFS PG API (RSA-2048 encryption & signatures)
  - SSLCommerz Hosted Session V4 (Cards, Internet Banking, Mobile Banking)
- **Escrow & Refund Protocol**:
  - 24-hour dispute window auto-release fallback
  - State-gated refunds: Instant for pre-session cancellations ($\ge 2$ hours prior), duplicate IPNs, and timeouts; Tribunal arbitration for active sessions/disputes
- **Reconciliation**:
  - Hourly automated background job polling gateway query APIs for transactions pending $> 15$ minutes
- **Security Baseline**:
  - OWASP ASVS Level 2 compliance (strict input validation, rate limiting, replay defense, zero secrets in logs, server-authoritative calculations)

## Constitution & Policy Compliance
- **Zero-Emoji Policy**: Strictly enforced across all code, logs, and frontend components. Crisp Lucide icons only.
- **Mandatory File Headers**: Applied to all created and modified files.
- **Server Authority**: Client never specifies amount, currency, or payment status.

## Phases of Execution
1. **Phase 1: Gateway Core & SSLCommerz Integration**
   - Implement `backend/app/services/payment/sslcommerz_service.py`.
   - Update `sandbox_config.py` with SSLCommerz credentials and environment toggle.
2. **Phase 2: Enhanced Escrow Vault & 24h Auto-Release Engine**
   - Extend `escrow_vault_service.py` with 24-hour expiration timers and auto-settlement.
   - Implement state-gated automated instant refund logic.
3. **Phase 3: Automated Hourly Reconciliation Service**
   - Create `backend/app/services/payment/reconciliation_service.py` with automated multi-gateway status sync and audit logging.
4. **Phase 4: API Endpoints & Unified Checkout Route**
   - Update `backend/app/api/v1/endpoints/payments.py` with SSLCommerz routes, unified checkout, IPN handlers, and auto-release triggers.
   - Enforce `X-Idempotency-Key` and server price calculations.
5. **Phase 5: Frontend Payment Modal & Receipt View**
   - Build `frontend/src/components/payment/PaymentDrawer.tsx` with bKash, Nagad, and Card options.
   - Build tactile Oxford Navy design with clean Lucide icons and Bengali copy.
6. **Phase 6: Comprehensive Automated Test Suite & ASVS L2 Audit**
   - Implement `backend/tests/test_phase140_payment_gateway_audit.py`.
   - Verify all acceptance criteria and run zero-emoji sweep.
7. **Phase 7: Full Repository Discovery, Verification & Artifact Report**
   - Run complete test suite (1,555+ tests, 0 regressions).
   - Generate `PHASE_140_PAYMENT_SECURITY_REPORT.md`.
