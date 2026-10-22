/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      specs/043-phase140-national-payment-gateway-audit/data-model.md
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Data models, entity schemas, and state transitions for Phase 140
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */

# Phase 140 Data Models & Schemas

## 1. Entities

### `PaymentTransaction`
Represents an authoritative financial payment attempt on the platform.
- `transaction_id`: `str` (UUIDv4)
- `idempotency_key`: `str` (UUID or unique client token, enforced unique)
- `user_id`: `str` (Student or Guardian initiating payment)
- `gateway`: `Literal["BKASH", "NAGAD", "SSLCOMMERZ"]`
- `gateway_txn_id`: `Optional[str]` (Gateway reference e.g. TRXID, val_id)
- `server_amount_bdt`: `float` (Authoritative fee computed by system, e.g. 1500.00)
- `currency`: `Literal["BDT"]`
- `purpose`: `str` (e.g. `TUITION_ESCROW`, `EXAM_PACKAGE`, `MENTORSHIP`)
- `reference_id`: `str` (Target course/tuition contract ID)
- `status`: `Literal["INITIATED", "HELD_IN_ESCROW", "SETTLED", "REFUNDED", "DISPUTED", "FAILED"]`
- `created_at`: `str` (ISO-8601 UTC timestamp)
- `updated_at`: `str` (ISO-8601 UTC timestamp)

### `EscrowContract`
Represents a locked tuition fund held until milestone completion or 24-hour auto-release.
- `contract_id`: `str` (Unique identifier, e.g. `ESC_...`)
- `guardian_id`: `str`
- `tutor_id`: `str`
- `amount_bdt`: `float`
- `platform_fee_bdt`: `float` (5% platform fee)
- `net_payout_bdt`: `float` (95% net to tutor)
- `status`: `Literal["PENDING_DEPOSIT", "HELD_IN_ESCROW", "SESSION_LOGGED", "SETTLED", "DISPUTED", "REFUNDED"]`
- `sessions_agreed`: `int`
- `sessions_completed`: `int`
- `scheduled_completion_at`: `str` (ISO-8601 UTC)
- `auto_release_at`: `str` (ISO-8601 UTC, exactly 24 hours after session logged/scheduled completion)
- `dispute_reason`: `Optional[str]`
- `disputed_by`: `Optional[str]`
- `disputed_at`: `Optional[str]`

### `PaymentAuditLedgerEntry`
Immutable audit log entry for every payment state change.
- `entry_id`: `str` (UUIDv4)
- `transaction_id`: `str`
- `action`: `str` (e.g. `INITIATED`, `IPN_RECEIVED`, `ESCROW_LOCKED`, `AUTO_RELEASED_24H`, `REFUNDED_INSTANT`, `DISPUTE_FILED`)
- `actor_id`: `str` (`SYSTEM`, `USER`, `GATEWAY_WEBHOOK`, `ADMIN_TRIBUNAL`)
- `details`: `dict` (Sanitized payload, no passwords, no full card numbers, no CVVs)
- `recorded_at`: `str` (ISO-8601 UTC)

---

## 2. State Machine Transitions

```
[INITIATED]
   │
   ├── Gateway Success Callback / IPN Verified ────────► [HELD_IN_ESCROW]
   │                                                            │
   │                                  ┌─────────────────────────┴────────────────────────┐
   │                                  ▼                                                  ▼
   │                         Guardian Manual Sign-off                         24h Window Elapses (No Dispute)
   │                                  │                                                  │
   │                                  └─────────────────────────┬────────────────────────┘
   │                                                            ▼
   │                                                        [SETTLED]
   │                                                      (Tutor Paid)
   │
   ├── Pre-Session Cancellation (>= 2h) ───────────────────► [REFUNDED]
   │   OR Duplicate IPN / Timeout Auto-Refund
   │
   ├── Disagreement / Abuse Flagged ──────────────────────► [DISPUTED]
   │                                                            │
   │                                                Administrative Tribunal
   │                                                            │
   │                                           ┌────────────────┴────────────────┐
   │                                           ▼                                 ▼
   │                                       [SETTLED]                         [REFUNDED]
   │
   └── Payment Rejected / Cancelled by User ───────────────► [FAILED]
```
