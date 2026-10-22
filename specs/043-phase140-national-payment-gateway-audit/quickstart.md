/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      specs/043-phase140-national-payment-gateway-audit/quickstart.md
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Runnable validation quickstart scenarios for Phase 140
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */

# Phase 140 Quickstart & Verification Guide

## 1. Prerequisites
- Python 3.12+ virtual environment with dependencies installed.
- Running Next.js frontend or test suite.

## 2. Test Execution
Run the dedicated Phase 140 automated test suite:
```bash
python3 -m unittest backend/tests/test_phase140_payment_gateway_audit.py -v
```

Run repository-wide regression testing:
```bash
python3 -m unittest discover -s backend/tests -p "test_*.py"
```

Run Zero-Emoji compliance check across all modified files:
```bash
python3 backend/scripts/run_zero_emoji_sweep.py
```

## 3. Validation Scenarios

### Scenario A: Server-Authoritative Amount Enforcement
1. Submit checkout initiation request with `reference_id="CRS_HSC_PHYSICS_101"` and tampered payload `amount=1.00`.
2. Confirm the server computes the price strictly from the catalog (`1500.00 BDT`) and ignores/rejects the client amount.

### Scenario B: SSLCommerz Session & IPN Verification
1. Create SSLCommerz session via `POST /api/v1/payments/sslcommerz/initiate`.
2. Submit mock IPN with forged `verify_sign` $\rightarrow$ Confirm response is HTTP 400 rejection and security log recorded.
3. Submit valid IPN with matching HMAC signature $\rightarrow$ Confirm transaction transitions to `HELD_IN_ESCROW`.

### Scenario C: 24-Hour Escrow Auto-Release
1. Create tuition escrow contract.
2. Advance simulated clock past 24 hours without disputes.
3. Trigger auto-release or run reconciliation $\rightarrow$ Confirm status transitions to `SETTLED` and tutor balance is credited.

### Scenario D: State-Gated Instant Refund
1. Cancel tuition session $\ge 2$ hours prior to scheduled start $\rightarrow$ Confirm instant refund is approved and issued.
2. Attempt cancellation after session has commenced $\rightarrow$ Confirm system rejects instant refund and instructs user to file tribunal dispute.
