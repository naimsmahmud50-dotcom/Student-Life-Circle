/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      specs/043-phase140-national-payment-gateway-audit/research.md
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Architectural research, gateway protocols, and security lockdown decisions
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */

# Phase 140 Research & Architectural Decisions

## 1. SSLCommerz V4 Gateway Integration
- **Decision**: Integrate SSLCommerz Hosted Session v4 via `/gwprocess/v4/api.php` with direct IPN hash validation (`verify_sign`) and order validation server API query (`/validator/api/validationserverAPI.php`).
- **Rationale**: SSLCommerz is Bangladesh's premier card payment gateway (supporting Visa, Mastercard, AMEX, UnionPay, and Bangladeshi Internet Banking). Calling their server-to-server Validation API is the gold standard for verifying payment status independently of browser redirects.
- **Alternatives Considered**:
  - Relying solely on client redirect parameters: Rejected immediately as it violates OWASP ASVS L2 and PCI-DSS requirements. Malicious users could tamper with `status=VALID` in the query string.
  - Custom iFrame modal: Suboptimal compared to SSLCommerz Hosted Session redirect which isolates PCI-DSS card entry out of our application boundary.

## 2. 24-Hour Auto-Release Escrow State Machine
- **Decision**: Implement a dual-trigger escrow release mechanism. The learner or guardian can explicitly approve completion upon lesson finish. If no dispute is filed within 24 hours of scheduled completion or session logging, an automated background reconciliation engine automatically releases funds to the tutor payout ledger.
- **Rationale**: Prevents tutors' earned income from being indefinitely locked if guardians forget to click "Approve", while giving guardians a guaranteed 24-hour dispute window to report non-attendance or unsatisfactory sessions.
- **Alternatives Considered**:
  - Immediate instant payout on session end: Rejected because tutors could log fake sessions without guardians having any recourse.
  - Manual admin approval for every single payout: Does not scale beyond tens of sessions per day and introduces payment bottlenecks.

## 3. State-Gated Hybrid Refund Protocol
- **Decision**: Automated instant refunds for:
  1. Pre-session cancellations requested $\ge 2$ hours prior to scheduled start.
  2. Duplicate gateway IPNs or double-charges.
  3. Indeterminate gateway transactions that time out or fail validation.
  Tribunal adjudication required for:
  1. Cancellations made $< 2$ hours prior to scheduled start.
  2. Post-session tutor-guardian disputes.
- **Rationale**: Respects tutor preparation time while eliminating administrative overhead for straightforward, risk-free cancellations.
- **Alternatives Considered**:
  - 100% automated refunds on demand at any time: Vulnerable to abuse where a student cancels 5 minutes after a full hour-long session.
  - 100% manual refunds: Creates poor user experience for legitimate pre-session cancellations.

## 4. Hourly Automated Reconciliation Engine
- **Decision**: A background service (`PaymentReconciliationService`) running every hour to query gateway APIs for any transaction stuck in `INITIATED` or `PENDING` for $> 15$ minutes.
- **Rationale**: Bangladesh mobile financial networks (MFS) occasionally experience network timeouts or delayed IPNs due to telecom congestion. Reconciling on the hour ensures no student is charged without getting course access, and no failed transaction remains unresolved.
- **Alternatives Considered**:
  - Real-time polling per active user: Excessive API calls and rate-limit exhaustion against banking gateways.
  - Daily batch reconciliation: Too slow; students might be locked out of their mock exams for up to 24 hours.

## 5. OWASP ASVS Level 2 Security Architecture
- **Decision**:
  - Input validation with strict Pydantic models (rejecting negative amounts, non-numeric values, or non-whitelisted currencies).
  - Cryptographic verification of all incoming IPN/webhook payloads (bKash token verification, Nagad RSA signature, SSLCommerz MD5/SHA256 signature).
  - Idempotency with `X-Idempotency-Key` header and database unique constraints.
  - Secret masking in all logger formatters and exception handlers (masking phone numbers, trx IDs, passwords, and tokens).
  - Rate limiting on checkout initiation and IPN endpoints.
