"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      backend/app/services/payment/__init__.py
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Payment services module export registry for bKash, Nagad, SSLCommerz, Escrow & Reconciliation
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */
"""

from backend.app.services.payment.bkash_service import (
    bkash_service,
    BkashMerchantCheckoutService
)
from backend.app.services.payment.nagad_service import (
    nagad_service,
    NagadPaymentService
)
from backend.app.services.payment.sslcommerz_service import (
    SSLCommerzService
)
from backend.app.services.payment.escrow_vault_service import (
    escrow_vault_service,
    TuitionMilestoneEscrowService
)
from backend.app.services.payment.reconciliation_service import (
    reconciliation_service,
    PaymentReconciliationService
)
from backend.app.services.payment.webhook_verifier import (
    webhook_security_service,
    WebhookSecurityService
)
from backend.app.services.payment.sandbox_config import (
    bkash_sandbox_config,
    nagad_sandbox_config,
    sslcommerz_sandbox_config,
    token_renewal_manager,
    TokenRenewalManager,
    BkashSandboxCredentials,
    NagadSandboxCredentials,
    SSLCommerzSandboxCredentials
)
from backend.app.services.payment.ipn_service import (
    ipn_receiver_service,
    payment_ledger,
    IPNReceiverService,
    IdempotentPaymentLedger
)

# Shared global instance of SSLCommerz
sslcommerz_service = SSLCommerzService()

__all__ = [
    "bkash_service",
    "BkashMerchantCheckoutService",
    "nagad_service",
    "NagadPaymentService",
    "sslcommerz_service",
    "SSLCommerzService",
    "escrow_vault_service",
    "TuitionMilestoneEscrowService",
    "reconciliation_service",
    "PaymentReconciliationService",
    "webhook_security_service",
    "WebhookSecurityService",
    "bkash_sandbox_config",
    "nagad_sandbox_config",
    "sslcommerz_sandbox_config",
    "token_renewal_manager",
    "TokenRenewalManager",
    "BkashSandboxCredentials",
    "NagadSandboxCredentials",
    "SSLCommerzSandboxCredentials",
    "ipn_receiver_service",
    "payment_ledger",
    "IPNReceiverService",
    "IdempotentPaymentLedger"
]
