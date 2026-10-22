"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Micro-Scholarship Disbursement Vault
 * TOPIC:     Phase 133 Mobile Financial Services Gateway & Proof-of-Merit Verification
 * FILE:      backend/scholarship/disbursement_vault.py
 * PHASE:     Phase 133 - Direct-to-Mobile Scholarship Disbursement Vault
 * PURPOSE:   Provides cryptographic Proof-of-Merit verification, multi-vector
 *            anti-fraud detection (duplicate NID, multi-identity wallets),
 *            and MFS (bKash, Nagad, Rocket) merchant disbursement ledger.
 * STANDARDS: Zero-Emoji, Financial Immutable Audit, ASVS L2, Fraud Prevention
 */
"""

import hashlib
import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class ScholarshipTier(str, Enum):
    NATIONAL_GOLD = "NATIONAL_GOLD"                # BDT 15,000
    REGIONAL_DISTINCTION = "REGIONAL_DISTINCTION"  # BDT 8,000
    RURAL_EQUITY_BURSARY = "RURAL_EQUITY_BURSARY"  # BDT 5,000
    STEM_MERIT_STIPEND = "STEM_MERIT_STIPEND"      # BDT 4,000


TIER_DISBURSEMENT_AMOUNTS: Dict[ScholarshipTier, int] = {
    ScholarshipTier.NATIONAL_GOLD: 15000,
    ScholarshipTier.REGIONAL_DISTINCTION: 8000,
    ScholarshipTier.RURAL_EQUITY_BURSARY: 5000,
    ScholarshipTier.STEM_MERIT_STIPEND: 4000,
}


class MFSProvider(str, Enum):
    BKASH = "BKASH"
    NAGAD = "NAGAD"
    ROCKET = "ROCKET"


class DisbursementStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    DISBURSED = "DISBURSED"
    REJECTED = "REJECTED"
    FLAGGED_FRAUD = "FLAGGED_FRAUD"


class DuplicateNIDException(ValueError):
    """Raised when an applicant attempts to claim a stipend using an already registered NID/BRN."""
    pass


class InvalidMFSWalletException(ValueError):
    """Raised when an MFS wallet number fails Bangladeshi telecommunications MSISDN standards."""
    pass


class FraudulentClaimException(PermissionError):
    """Raised when suspicious identity-hopping, wallet collisions, or forged credentials are detected."""
    pass


class InsufficientVaultBalanceException(RuntimeError):
    """Raised when the endowment vault has insufficient liquidity to disburse stipend."""
    pass


# Recognized hard-to-reach rural districts for equity bursary weighting
RURAL_EQUITY_DISTRICTS: Set[str] = {
    "kurigram", "bandarban", "sunamganj", "panchagarh", "khagrachhari",
    "rangamati", "lalmonirhat", "barguna", "patuakhali", "gaibandha"
}


@dataclass
class ProofOfMeritRecord:
    record_id: str
    student_id: str
    nid_or_brn: str
    board_gpa: float
    district: str
    is_golden_gpa: bool = False
    olympiad_rank: Optional[int] = None
    verification_proof_hash: str = ""

    def compute_hash(self) -> str:
        raw = f"{self.student_id}:{self.nid_or_brn}:{self.board_gpa:.2f}:{self.olympiad_rank}:{self.district.lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class DisbursementTransaction:
    transaction_id: str
    application_id: str
    student_id: str
    tier: ScholarshipTier
    amount_bdt: int
    mfs_provider: MFSProvider
    wallet_msisdn: str
    idempotency_key: str
    mfs_reference: str
    transaction_hash: str
    disbursed_at: float = field(default_factory=time.time)
    status: DisbursementStatus = DisbursementStatus.DISBURSED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "application_id": self.application_id,
            "student_id": self.student_id,
            "tier": self.tier.value,
            "amount_bdt": self.amount_bdt,
            "mfs_provider": self.mfs_provider.value,
            "wallet_msisdn": self.wallet_msisdn,
            "idempotency_key": self.idempotency_key,
            "mfs_reference": self.mfs_reference,
            "transaction_hash": self.transaction_hash,
            "disbursed_at": self.disbursed_at,
            "status": self.status.value,
        }


class ProofOfMeritEvaluator:
    """
    Evaluates educational achievement credentials to determine scholarship tier and eligibility.
    """

    @classmethod
    def evaluate(cls, proof: ProofOfMeritRecord) -> Tuple[bool, Optional[ScholarshipTier], str]:
        """
        Determines eligibility and assigns highest qualifying scholarship tier.
        """
        # 1. National Gold: Olympiad National Podium (Rank 1 to 3)
        if proof.olympiad_rank is not None and 1 <= proof.olympiad_rank <= 3:
            return (
                True,
                ScholarshipTier.NATIONAL_GOLD,
                f"জাতীয় অলিম্পিয়াড র‍্যাংক {proof.olympiad_rank} অনুযায়ী জাতীয় স্বর্ণ উপবৃত্তি অনুমোদিত।"
            )

        # 2. Regional Distinction: Olympiad Rank 4-10 OR Golden GPA 5.0
        if (proof.olympiad_rank is not None and 4 <= proof.olympiad_rank <= 10) or (proof.board_gpa >= 5.0 and proof.is_golden_gpa):
            return (
                True,
                ScholarshipTier.REGIONAL_DISTINCTION,
                "আঞ্চলিক অলিম্পিয়াড মেধা বা গোল্ডেন জিপিএ ৫.০ অনুযায়ী আঞ্চলিক গৌরব উপবৃত্তি অনুমোদিত।"
            )

        # 3. Rural Equity Bursary: Hard-to-reach district and GPA >= 4.5
        if proof.district.lower().strip() in RURAL_EQUITY_DISTRICTS and proof.board_gpa >= 4.5:
            return (
                True,
                ScholarshipTier.RURAL_EQUITY_BURSARY,
                f"অনগ্রসর জেলা কোটা ({proof.district.capitalize()}) ও জিপিএ {proof.board_gpa:.2f} অনুযায়ী পল্লী সহায়তা উপবৃত্তি অনুমোদিত।"
            )

        # 4. STEM Merit Stipend: General GPA 5.0
        if proof.board_gpa >= 5.0:
            return (
                True,
                ScholarshipTier.STEM_MERIT_STIPEND,
                "বোর্ড পরীক্ষায় জিপিএ ৫.০ অর্জন অনুযায়ী সাধারণ মেধা উপবৃত্তি অনুমোদিত।"
            )

        return (
            False,
            None,
            "মেধা উপবৃত্তির ন্যূনতম যোগ্যতা পূরণ হয়নি (ন্যূনতম জিপিএ ৫.০ বা অলিম্পিয়াড মেধা আবশ্যক)।"
        )


class AntiFraudGuard:
    """
    Guards against identity synthesis, sybil duplicate claims, and wallet hijacking.
    """

    MSISDN_PATTERN = re.compile(r"^(?:\+?88)?01[3-9]\d{8}$")

    def __init__(self):
        # Tracking stores for anti-fraud validation
        self._claimed_nids: Set[str] = set()
        self._student_to_nid: Dict[str, str] = {}
        # wallet -> (student_id, nid)
        self._wallet_bindings: Dict[str, Tuple[str, str]] = {}

    @classmethod
    def normalize_and_validate_msisdn(cls, wallet_input: str) -> str:
        """
        Validates Bangladeshi MFS phone number format and returns canonical E.164 format (+8801XXXXXXXXX).
        """
        cleaned = wallet_input.strip().replace(" ", "").replace("-", "")
        if not cls.MSISDN_PATTERN.match(cleaned):
            raise InvalidMFSWalletException(
                f"Invalid MFS Wallet format: '{wallet_input}'. Must be valid Bangladeshi MSISDN (e.g. 017XXXXXXXX)."
            )

        # Canonicalize to +8801XXXXXXXXX
        if cleaned.startswith("+8801"):
            return cleaned
        elif cleaned.startswith("8801"):
            return f"+{cleaned}"
        elif cleaned.startswith("01"):
            return f"+88{cleaned}"
        return cleaned

    def assert_no_fraudulent_claim(
        self,
        student_id: str,
        nid_or_brn: str,
        wallet_msisdn: str
    ) -> None:
        """
        Asserts that the applicant is not executing duplicate, cross-account, or collided claims.
        """
        canonical_nid = nid_or_brn.strip().upper()
        canonical_wallet = self.normalize_and_validate_msisdn(wallet_msisdn)

        # 1. Duplicate NID check
        if canonical_nid in self._claimed_nids:
            raise DuplicateNIDException(
                f"Fraud Protection: NID/BRN '{canonical_nid}' has already claimed a micro-scholarship in this cycle."
            )

        # 2. Multiple student IDs claiming the same NID
        existing_nid = self._student_to_nid.get(student_id)
        if existing_nid and existing_nid != canonical_nid:
            raise FraudulentClaimException(
                f"Identity Conflict: Student '{student_id}' previously registered with different NID '{existing_nid}'."
            )

        # 3. Wallet collision check: Same wallet cannot be used by a different NID
        if canonical_wallet in self._wallet_bindings:
            bound_student, bound_nid = self._wallet_bindings[canonical_wallet]
            if bound_nid != canonical_nid or bound_student != student_id:
                raise FraudulentClaimException(
                    f"Wallet Hijacking Defense: Wallet '{canonical_wallet}' is already bound to another student/NID."
                )

    def record_claim(self, student_id: str, nid_or_brn: str, wallet_msisdn: str) -> None:
        """
        Records verified claimant to prevent future duplicate disbursements.
        """
        canonical_nid = nid_or_brn.strip().upper()
        canonical_wallet = self.normalize_and_validate_msisdn(wallet_msisdn)

        self._claimed_nids.add(canonical_nid)
        self._student_to_nid[student_id] = canonical_nid
        self._wallet_bindings[canonical_wallet] = (student_id, canonical_nid)


class MFSDisbursementGateway:
    """
    Simulates high-integrity bKash, Nagad, and Rocket merchant payout clearinghouse.
    """

    @classmethod
    def execute_payout(
        cls,
        provider: MFSProvider,
        wallet_msisdn: str,
        amount_bdt: int,
        idempotency_key: str
    ) -> Tuple[str, str]:
        """
        Executes MFS transaction and returns (mfs_reference, transaction_hash).
        """
        now = time.time()
        prefix = {
            MFSProvider.BKASH: "BKS",
            MFSProvider.NAGAD: "NGD",
            MFSProvider.ROCKET: "RKT",
        }.get(provider, "MFS")

        reference_code = f"{prefix}_{uuid.uuid4().hex[:8].upper()}"

        raw_hash_seed = f"{provider.value}:{wallet_msisdn}:{amount_bdt}:{idempotency_key}:{now:.4f}:{reference_code}"
        txn_hash = hashlib.sha256(raw_hash_seed.encode("utf-8")).hexdigest()

        return reference_code, txn_hash


class ScholarshipVaultService:
    """
    Institutional Endowment Vault Service orchestrating Proof-of-Merit verification,
    fraud checks, and immutable MFS disbursement settlement.
    """

    def __init__(self, initial_endowment_bdt: int = 5000000):
        self.total_endowment_bdt = initial_endowment_bdt
        self.disbursed_bdt = 0
        self.anti_fraud = AntiFraudGuard()
        # transaction_id -> DisbursementTransaction
        self._ledger: Dict[str, DisbursementTransaction] = {}
        # idempotency_key -> transaction_id
        self._idempotency_index: Dict[str, str] = {}

    @property
    def remaining_liquidity_bdt(self) -> int:
        return self.total_endowment_bdt - self.disbursed_bdt

    def disburse_scholarship(
        self,
        student_id: str,
        nid_or_brn: str,
        board_gpa: float,
        district: str,
        mfs_provider: MFSProvider,
        wallet_msisdn: str,
        idempotency_key: str,
        is_golden_gpa: bool = False,
        olympiad_rank: Optional[int] = None
    ) -> DisbursementTransaction:
        """
        Validates eligibility, guards against fraud, ensures idempotency, and executes disbursement.
        """
        # 1. Idempotency Check: Prevent duplicate charge on retransmission
        if idempotency_key in self._idempotency_index:
            txn_id = self._idempotency_index[idempotency_key]
            return self._ledger[txn_id]

        # 2. Anti-Fraud Assertions
        canonical_wallet = AntiFraudGuard.normalize_and_validate_msisdn(wallet_msisdn)
        self.anti_fraud.assert_no_fraudulent_claim(student_id, nid_or_brn, canonical_wallet)

        # 3. Proof-of-Merit Evaluation
        proof = ProofOfMeritRecord(
            record_id=f"pom_{uuid.uuid4().hex[:8]}",
            student_id=student_id,
            nid_or_brn=nid_or_brn,
            board_gpa=board_gpa,
            district=district,
            is_golden_gpa=is_golden_gpa,
            olympiad_rank=olympiad_rank,
        )
        proof.verification_proof_hash = proof.compute_hash()

        is_eligible, tier, explanation = ProofOfMeritEvaluator.evaluate(proof)
        if not is_eligible or tier is None:
            raise ValueError(f"Proof-of-Merit Ineligible: {explanation}")

        # 4. Vault Liquidity Check
        payout_amount = TIER_DISBURSEMENT_AMOUNTS[tier]
        if payout_amount > self.remaining_liquidity_bdt:
            raise InsufficientVaultBalanceException(
                f"Endowment Vault Liquidity Exhausted: Required {payout_amount} BDT, Available {self.remaining_liquidity_bdt} BDT."
            )

        # 5. MFS Gateway Execution
        mfs_ref, txn_hash = MFSDisbursementGateway.execute_payout(
            provider=mfs_provider,
            wallet_msisdn=canonical_wallet,
            amount_bdt=payout_amount,
            idempotency_key=idempotency_key
        )

        # 6. Immutable Ledger Commit
        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
        transaction = DisbursementTransaction(
            transaction_id=transaction_id,
            application_id=f"app_{uuid.uuid4().hex[:8]}",
            student_id=student_id,
            tier=tier,
            amount_bdt=payout_amount,
            mfs_provider=mfs_provider,
            wallet_msisdn=canonical_wallet,
            idempotency_key=idempotency_key,
            mfs_reference=mfs_ref,
            transaction_hash=txn_hash,
            disbursed_at=time.time(),
            status=DisbursementStatus.DISBURSED
        )

        self._ledger[transaction_id] = transaction
        self._idempotency_index[idempotency_key] = transaction_id
        self.disbursed_bdt += payout_amount

        # Record claimant in anti-fraud guard
        self.anti_fraud.record_claim(student_id, nid_or_brn, canonical_wallet)

        return transaction

    def get_transaction(self, transaction_id: str) -> Optional[DisbursementTransaction]:
        return self._ledger.get(transaction_id)

    def list_student_transactions(self, student_id: str) -> List[DisbursementTransaction]:
        return [t for t in self._ledger.values() if t.student_id == student_id]
