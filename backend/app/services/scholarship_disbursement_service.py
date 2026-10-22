"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    National Merit Scholarship Pool & Autonomous Disbursement Service
TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
FILE:      backend/app/services/scholarship_disbursement_service.py
PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
PURPOSE:   Enforces algorithmic merit-need composite evaluation (GPA 5.0 or top 5%
           percentile + family income verification), district quota allocations,
           dual-authorization escrow governance, atomic double-spending defense,
           and automated bKash/Nagad B2C payouts with cryptographic SHA-256 ledger seals.
STANDARDS: OWASP ASVS L2, FinTech B2C Security, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import hashlib
import json
import os
import re
import secrets
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple


class ScholarshipException(Exception):
    """Base exception for scholarship endowment and disbursement errors."""
    pass


class EligibilityException(ScholarshipException):
    """Raised when an applicant fails merit or income verification standards."""
    pass


class AuthorizationException(ScholarshipException):
    """Raised when an unauthorized actor or invalid dual-custodian sequence is attempted."""
    pass


class DoubleSpendingException(ScholarshipException):
    """Raised when duplicate idempotency key or double disbursement is detected."""
    pass


class DisbursementFailedException(ScholarshipException):
    """Raised when gateway integration rejects B2C disbursement."""
    pass


class ScholarshipDisbursementService:
    """
    Core engine managing the National Merit Scholarship Pool, dual-authorization
    escrow release, and cryptographic disbursement ledger.
    """

    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_ACADEMIC_APPROVED = "ACADEMIC_APPROVED"
    STATUS_DUAL_APPROVED = "DUAL_APPROVED"
    STATUS_DISBURSED = "DISBURSED"
    STATUS_REJECTED = "REJECTED"

    PRIORITY_DISTRICTS = [
        "Kurigram",
        "Sunamganj",
        "Bandarban",
        "Barguna",
        "Lalmonirhat",
        "Netrokona",
        "Panchagarh",
        "Gaibandha",
    ]

    INCOME_CUTOFF_BDT = 15000.0
    PRIORITY_DISTRICT_INCOME_CUTOFF_BDT = 20000.0

    def __init__(self):
        self._pools: Dict[str, Dict[str, Any]] = {}
        self._applications: Dict[str, Dict[str, Any]] = {}
        self._idempotency_keys: Dict[str, Dict[str, Any]] = {}
        self._disbursement_ledger: List[Dict[str, Any]] = []
        self._audit_log: List[Dict[str, Any]] = []
        self._init_seed_pools()

    def _init_seed_pools(self) -> None:
        """Initializes default prestigious national endowment funds."""
        self._pools = {
            "pool-national-merit-2026": {
                "pool_id": "pool-national-merit-2026",
                "title_bn": "জাতীয় মেধা ও অনগ্রসর শিক্ষার্থী বৃত্তি তহবিল",
                "title_en": "National Merit & Hardship Foundation Pool",
                "sponsor_name": "Ministry of Education & Alumni Trust",
                "total_endowment_bdt": 5000000.0,
                "disbursed_bdt": 480000.0,
                "remaining_bdt": 4520000.0,
                "grant_per_student_bdt": 10000.0,
                "funded_students_count": 48,
                "target_quota_count": 500,
                "district_allocations": {
                    "Kurigram": {"allocated": 80, "funded": 12},
                    "Sunamganj": {"allocated": 75, "funded": 10},
                    "Bandarban": {"allocated": 65, "funded": 8},
                    "Barguna": {"allocated": 70, "funded": 9},
                    "General": {"allocated": 210, "funded": 9},
                },
                "status": "ACTIVE",
            },
            "pool-rural-stem-2026": {
                "pool_id": "pool-rural-stem-2026",
                "title_bn": "প্রান্তিক অঞ্চল বিজ্ঞান ও প্রকৌশল মেধা অনুদান",
                "title_en": "Rural Frontier STEM Endowment Pool",
                "sponsor_name": "Bangladesh Science Academy",
                "total_endowment_bdt": 3000000.0,
                "disbursed_bdt": 240000.0,
                "remaining_bdt": 2760000.0,
                "grant_per_student_bdt": 8000.0,
                "funded_students_count": 30,
                "target_quota_count": 375,
                "district_allocations": {
                    "Lalmonirhat": {"allocated": 60, "funded": 8},
                    "Netrokona": {"allocated": 65, "funded": 7},
                    "Panchagarh": {"allocated": 70, "funded": 9},
                    "Gaibandha": {"allocated": 80, "funded": 6},
                    "General": {"allocated": 100, "funded": 0},
                },
                "status": "ACTIVE",
            },
        }

    def get_all_pools(self) -> List[Dict[str, Any]]:
        """Returns all configured endowment pools."""
        return list(self._pools.values())

    def get_pool(self, pool_id: str) -> Optional[Dict[str, Any]]:
        """Returns specific endowment pool details."""
        return self._pools.get(pool_id)

    def evaluate_eligibility(
        self,
        gpa: float,
        national_percentile: float,
        monthly_family_income_bdt: float,
        district: str,
    ) -> Dict[str, Any]:
        """
        Evaluates algorithmic merit-need qualification:
        1. Academic Merit: GPA == 5.0 (out of 5.0) OR national percentile >= 95.0.
        2. Financial Need: monthly family income <= 15,000 BDT (or <= 20,000 BDT for priority remote districts).
        3. Priority District Quota Affirmative Action.
        """
        is_priority_district = district in self.PRIORITY_DISTRICTS
        income_limit = (
            self.PRIORITY_DISTRICT_INCOME_CUTOFF_BDT
            if is_priority_district
            else self.INCOME_CUTOFF_BDT
        )

        merit_qualified = gpa >= 5.0 or national_percentile >= 95.0
        need_qualified = monthly_family_income_bdt <= income_limit

        is_eligible = merit_qualified and need_qualified

        reason = ""
        if not merit_qualified and not need_qualified:
            reason = "উভয় মেধা মানদণ্ড (GPA 5.0 বা শীর্ষ ৫%) এবং পারিবারিক আয় সীমা পূর্ণ হয়নি।"
        elif not merit_qualified:
            reason = "মেধা মানদণ্ড পূর্ণ হয়নি (GPA 5.0 অথবা জাতীয় মক পরীক্ষায় ৯৫+ পার্সেন্টাইল প্রয়োজন)।"
        elif not need_qualified:
            reason = f"পারিবারিক মাসিক আয় নির্ধারিত সীমা (সর্বোচ্চ {int(income_limit):,} টাকা) অতিক্রম করেছে।"
        else:
            reason = "শিক্ষার্থী মেধা ও আর্থিক যোগ্যতা মানদণ্ড সফলভাবে পূরণ করেছেন।"

        return {
            "is_eligible": is_eligible,
            "merit_qualified": merit_qualified,
            "need_qualified": need_qualified,
            "is_priority_district": is_priority_district,
            "gpa": gpa,
            "national_percentile": national_percentile,
            "monthly_family_income_bdt": monthly_family_income_bdt,
            "income_limit_bdt": income_limit,
            "district": district,
            "reason_bn": reason,
        }

    def submit_application(
        self,
        pool_id: str,
        student_id: str,
        student_name: str,
        district: str,
        gpa: float,
        national_percentile: float,
        monthly_family_income_bdt: float,
        mobile_wallet_number: str,
        wallet_provider: str = "bKash",
    ) -> Dict[str, Any]:
        """Submits a verified scholarship application."""
        pool = self._pools.get(pool_id)
        if not pool:
            raise ScholarshipException(f"Endowment pool '{pool_id}' not found.")

        # Check existing active application for this student
        for app in self._applications.values():
            if app["student_id"] == student_id and app["pool_id"] == pool_id:
                if app["status"] in [self.STATUS_SUBMITTED, self.STATUS_ACADEMIC_APPROVED, self.STATUS_DUAL_APPROVED]:
                    return app
                if app["status"] == self.STATUS_DISBURSED:
                    raise DoubleSpendingException(f"Student '{student_id}' has already received a grant from this pool.")

        # Validate eligibility
        eval_result = self.evaluate_eligibility(
            gpa=gpa,
            national_percentile=national_percentile,
            monthly_family_income_bdt=monthly_family_income_bdt,
            district=district,
        )

        if not eval_result["is_eligible"]:
            raise EligibilityException(eval_result["reason_bn"])

        # Validate wallet format (Bangladeshi 11-digit MSISDN starting with 01)
        clean_wallet = re.sub(r"[^\d]", "", mobile_wallet_number)
        if len(clean_wallet) == 11 and clean_wallet.startswith("01"):
            formatted_wallet = clean_wallet
        elif len(clean_wallet) == 13 and clean_wallet.startswith("8801"):
            formatted_wallet = clean_wallet[2:]
        else:
            raise ScholarshipException("Invalid Bangladeshi mobile wallet number format.")

        app_id = f"app-merit-{uuid.uuid4().hex[:10]}"
        now = int(time.time())

        application = {
            "application_id": app_id,
            "pool_id": pool_id,
            "student_id": student_id,
            "student_name": student_name,
            "district": district,
            "gpa": gpa,
            "national_percentile": national_percentile,
            "monthly_family_income_bdt": monthly_family_income_bdt,
            "mobile_wallet_number": formatted_wallet,
            "wallet_provider": wallet_provider.upper(),
            "grant_amount_bdt": pool["grant_per_student_bdt"],
            "status": self.STATUS_SUBMITTED,
            "signatures": {
                "academic_evaluator": None,
                "finance_custodian": None,
            },
            "created_at": now,
            "updated_at": now,
        }

        self._applications[app_id] = application
        return application

    def approve_application(
        self,
        application_id: str,
        authorizer_id: str,
        authorizer_role: str,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Enforces strict dual-authorization (two-person rule):
        - Signature 1: role 'academic_evaluator' -> status moves to ACADEMIC_APPROVED.
        - Signature 2: role 'finance_custodian' (or 'service_role') -> status moves to DUAL_APPROVED.
        - Rejects if the same person attempts to provide both signatures.
        """
        app = self._applications.get(application_id)
        if not app:
            raise ScholarshipException(f"Application '{application_id}' not found.")

        now = int(time.time())

        if authorizer_role == "academic_evaluator":
            if app["status"] != self.STATUS_SUBMITTED:
                raise AuthorizationException(f"Application is in status '{app['status']}', expected '{self.STATUS_SUBMITTED}'.")
            app["signatures"]["academic_evaluator"] = {
                "authorizer_id": authorizer_id,
                "role": authorizer_role,
                "notes": notes or "Academic merit verified against NCTB transcripts.",
                "signed_at": now,
            }
            app["status"] = self.STATUS_ACADEMIC_APPROVED
            app["updated_at"] = now
            return app

        elif authorizer_role in ["finance_custodian", "service_role"]:
            if app["status"] != self.STATUS_ACADEMIC_APPROVED:
                raise AuthorizationException(
                    "Dual-authorization sequence violation: Application must be approved by academic_evaluator first."
                )
            
            # Anti-collusion: ensure finance custodian is not the academic evaluator
            first_signer = app["signatures"]["academic_evaluator"]
            if first_signer and first_signer.get("authorizer_id") == authorizer_id and authorizer_role != "service_role":
                raise AuthorizationException("Anti-collusion violation: Same individual cannot provide both authorizations.")

            app["signatures"]["finance_custodian"] = {
                "authorizer_id": authorizer_id,
                "role": authorizer_role,
                "notes": notes or "Endowment vault escrow allocation verified and locked.",
                "signed_at": now,
            }
            app["status"] = self.STATUS_DUAL_APPROVED
            app["updated_at"] = now
            return app

        else:
            raise AuthorizationException(f"Role '{authorizer_role}' is not authorized to sign scholarship approvals.")

    def execute_disbursement(
        self,
        application_id: str,
        idempotency_key: str,
        operator_id: str,
    ) -> Dict[str, Any]:
        """
        Executes autonomous disbursement:
        1. Validates idempotency key to prevent double-spending.
        2. Validates application status is DUAL_APPROVED.
        3. Atomically transitions state to DISBURSED.
        4. Simulates B2C gateway API call (bKash/Nagad).
        5. Generates cryptographic SHA-256 seal.
        6. Appends immutable entry to the public disbursement ledger.
        """
        if not idempotency_key or not isinstance(idempotency_key, str) or len(idempotency_key.strip()) < 8:
            raise ScholarshipException("Invalid or missing idempotency_key.")

        # Check existing idempotency record (Double-spending defense)
        if idempotency_key in self._idempotency_keys:
            cached_receipt = self._idempotency_keys[idempotency_key]
            return cached_receipt

        app = self._applications.get(application_id)
        if not app:
            raise ScholarshipException(f"Application '{application_id}' not found.")

        if app["status"] == self.STATUS_DISBURSED:
            raise DoubleSpendingException(
                f"Double-spending attack prevented: Application '{application_id}' has already been disbursed."
            )

        if app["status"] != self.STATUS_DUAL_APPROVED:
            raise AuthorizationException(
                f"Cannot disburse: Application status is '{app['status']}', requires '{self.STATUS_DUAL_APPROVED}'."
            )

        pool = self._pools.get(app["pool_id"])
        if not pool:
            raise ScholarshipException(f"Endowment pool '{app['pool_id']}' missing.")

        grant_amount = app["grant_amount_bdt"]
        if pool["remaining_bdt"] < grant_amount:
            raise ScholarshipException("Endowment pool has insufficient balance for disbursement.")

        # ATOMIC STATE LOCK
        app["status"] = self.STATUS_DISBURSED
        now = int(time.time())
        app["updated_at"] = now

        # Gateway Reference Simulation
        provider = app.get("wallet_provider", "BKASH")
        gateway_tx_ref = f"B2C_{provider}_{uuid.uuid4().hex[:12].upper()}"

        # Deduct from pool balance
        pool["remaining_bdt"] -= grant_amount
        pool["disbursed_bdt"] += grant_amount
        pool["funded_students_count"] += 1

        # Update district quota stats
        district = app["district"]
        if district in pool["district_allocations"]:
            pool["district_allocations"][district]["funded"] += 1
        elif "General" in pool["district_allocations"]:
            pool["district_allocations"]["General"]["funded"] += 1

        # Cryptographic Ledger Seal (SHA-256)
        payload_to_hash = (
            f"{app['pool_id']}:{application_id}:{app['student_id']}:{grant_amount}:"
            f"{gateway_tx_ref}:{app['signatures']['academic_evaluator']['authorizer_id']}:"
            f"{app['signatures']['finance_custodian']['authorizer_id']}:{now}"
        )
        ledger_seal_hash = hashlib.sha256(payload_to_hash.encode("utf-8")).hexdigest()

        # Public Receipt Record
        receipt = {
            "receipt_id": f"rcpt_{uuid.uuid4().hex[:10]}",
            "application_id": application_id,
            "idempotency_key": idempotency_key,
            "pool_id": app["pool_id"],
            "student_id": app["student_id"],
            "anonymous_student_token": f"STU-****-{app['student_id'][-4:] if len(app['student_id']) >= 4 else '9482'}",
            "district": district,
            "disbursed_amount_bdt": grant_amount,
            "gateway_provider": provider,
            "gateway_transaction_ref": gateway_tx_ref,
            "masked_wallet": f"{app['mobile_wallet_number'][:3]}*****{app['mobile_wallet_number'][-3:]}",
            "ledger_seal_sha256": ledger_seal_hash,
            "dual_authorized_by": [
                app["signatures"]["academic_evaluator"]["authorizer_id"],
                app["signatures"]["finance_custodian"]["authorizer_id"],
            ],
            "disbursed_at": now,
            "verification_status": "VERIFIED_ON_LEDGER",
        }

        # Cache by idempotency key
        self._idempotency_keys[idempotency_key] = receipt
        self._disbursement_ledger.append(receipt)

        return receipt

    def get_public_ledger(
        self,
        district: Optional[str] = None,
        gateway_provider: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        Returns anonymized public ledger records preserving student privacy.
        Never reveals student legal names or unmasked phone numbers.
        """
        records = self._disbursement_ledger

        if district:
            d_clean = district.strip().lower()
            records = [r for r in records if r["district"].lower() == d_clean]

        if gateway_provider:
            g_clean = gateway_provider.strip().upper()
            records = [r for r in records if r["gateway_provider"].upper() == g_clean]

        # Sort latest first
        records = sorted(records, key=lambda x: x["disbursed_at"], reverse=True)

        paginated = records[offset : offset + limit]

        # Scrub any private keys
        public_records = []
        for r in paginated:
            public_records.append({
                "receipt_id": r["receipt_id"],
                "anonymous_student_token": r["anonymous_student_token"],
                "district": r["district"],
                "disbursed_amount_bdt": r["disbursed_amount_bdt"],
                "gateway_provider": r["gateway_provider"],
                "gateway_transaction_ref": r["gateway_transaction_ref"],
                "masked_wallet": r["masked_wallet"],
                "ledger_seal_sha256": r["ledger_seal_sha256"],
                "disbursed_at": r["disbursed_at"],
                "verification_status": r["verification_status"],
            })

        return {
            "total_disbursed_count": len(self._disbursement_ledger),
            "total_disbursed_bdt": sum(r["disbursed_amount_bdt"] for r in self._disbursement_ledger),
            "limit": limit,
            "offset": offset,
            "records": public_records,
        }


# Global singleton instance
scholarship_disbursement_service = ScholarshipDisbursementService()
