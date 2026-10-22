<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
FILE:      specs/017-phase113-scholarship-endowment-vault/spec.md
PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
PURPOSE:   Establishes national merit scholarship endowment funds, algorithmic merit-need
           composite qualification (GPA 5.0 / top 5% exam percentile + income verification),
           dual-authorization escrow release, automated bKash/Nagad B2C disbursement,
           double-spending prevention, and public cryptographic ledger auditing.
STANDARDS: OWASP ASVS L2, FinTech B2C Security, Pure Academic Design, Strict Zero-Emoji
-->

# Feature Specification: Phase 113 — National Merit Scholarship Pool & Autonomous Disbursement

## 1. Overview
The National Merit Scholarship Pool & Autonomous Disbursement system empowers deserving, underprivileged Bangladeshi students with automated, dignified educational grants. The platform combines merit evaluation (GPA 5.0 or top 5% in national mock exams) with socio-economic distress verification (monthly family income <= 15,000 BDT) and targeted district quotas (Kurigram, Sunamganj, Bandarban, Barguna, etc.).

Disbursements are governed by a dual-authorization escrow release mechanism (`academic_evaluator` + `finance_custodian`) integrated with bKash Merchant B2C Disbursement and Nagad Bulk Pay gateways. Transactions are protected by atomic idempotency keys to eliminate double-spending, and every disbursed grant is sealed into a public, tamper-evident cryptographic SHA-256 ledger while rigorously preserving student PII anonymity.

## 2. Functional Requirements
- **Merit & Need Evaluation**:
  - Academic Qualification: GPA 5.0 in SSC/HSC or >= 95th percentile in national Olympiad/mock examinations.
  - Socio-Economic Verification: Verified monthly family income <= 15,000 BDT or remote district affirmative action quota.
  - District Quota Allocations: Underserved rural regions (e.g., Kurigram, Sunamganj, Bandarban, Barguna, Lalmonirhat).
- **Dual-Authorization Escrow & Gateway Integration**:
  - Two-person rule required before fund dispatch:
    1. First signature: Academic / Merit Evaluator (`academic_evaluator`).
    2. Second signature: Financial Custodian (`finance_custodian`) or Automated Vault Service.
  - Integration with bKash Merchant B2C Disbursement and Nagad Bulk Pay APIs.
  - Atomic idempotency locking (`idempotency_key`) preventing concurrent duplicate executions or replay attacks.
- **Cryptographic Transparency & Audit**:
  - SHA-256 transaction receipt hashes binding pool ID, student token, amount, gateway reference, and dual signatures.
  - Publicly accessible, anonymized audit ledger modal (`STU-****-XXXX`) protecting minor identities.
- **Design & User Experience**:
  - Pure Academic visual language: Oxford Navy (`#0A2540`), Scholarly Gold (`#B45309`), Warm Paper Ivory (`#FAFAF8`).
  - Tactile 3D button depth: `shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none`.
  - Typography: 'Hind Siliguri' for narrative descriptions; 'Plus Jakarta Sans' for financial figures.
  - Zero-Emoji Policy: Pure Lucide SVG vector icons.
