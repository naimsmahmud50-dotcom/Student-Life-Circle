# ============================================================================
# MODULE: MICRO-SCHOLARSHIP ENDOWMENT & TOKENOMICS SERVICE
# TOPIC: Corporate/Alumni Endowments, Merit-Need Composite Scoring & bKash Auto-Disbursement
# FILE: backend/app/services/scholarship_endowment_service.py
# PURPOSE: Connect underprivileged students with corporate/alumni endowment grants,
#          automated need-index calculations, and cryptographic micro-disbursements.
# STANDARDS: OWASP ASVS L2 Financial Integrity, Double-Payout Defense, Audit Ledger
# AUDIENCE: Students, Corporate Sponsors, Foundation Donors & Financial Auditors
# ============================================================================

import hashlib
import time
import uuid
import re
from typing import Dict, List, Optional, Any


class ScholarshipEndowmentService:
    """
    Enterprise Micro-Scholarship Endowment Engine.
    Powers corporate endowment grants, algorithmic need-merit scoring,
    and automated bKash/Nagad micro-disbursements with cryptographic ledgers.
    """

    CRITERIA_STEM = "UNDERPRIVILEGED_STEM"
    CRITERIA_FEMALE_TECH = "FEMALE_TECH"
    CRITERIA_MERIT = "GENERAL_MERIT"

    def __init__(self):
        self._funds: Dict[str, Dict[str, Any]] = {}
        self._applications: Dict[str, Dict[str, Any]] = {}
        self._disbursements: List[Dict[str, Any]] = []
        self._init_seed_funds()

    def _init_seed_funds(self):
        """Pre-seeds prominent corporate and alumni endowment funds in Bangladesh."""
        seeds = [
            {
                "fund_id": "fund-pathao-stem-01",
                "sponsor_id": "spn-pathao",
                "sponsor_name": "Pathao Social Foundation",
                "fund_title": "Pathao STEM Talent Endowment: Rural University Aspirants",
                "total_grant_bdt": 150000.0,
                "disbursement_per_student_bdt": 3000.0,
                "target_criteria": self.CRITERIA_STEM,
                "remaining_bdt": 138000.0,
                "awarded_count": 4,
                "status": "ACTIVE",
                "created_at": "2026-10-14T06:00:00Z"
            },
            {
                "fund_id": "fund-gp-female-02",
                "sponsor_id": "spn-gp",
                "sponsor_name": "Grameenphone Future-Leaders",
                "fund_title": "Girls in Technology & Engineering Admission Grant",
                "total_grant_bdt": 200000.0,
                "disbursement_per_student_bdt": 4000.0,
                "target_criteria": self.CRITERIA_FEMALE_TECH,
                "remaining_bdt": 184000.0,
                "awarded_count": 4,
                "status": "ACTIVE",
                "created_at": "2026-10-14T07:00:00Z"
            },
            {
                "fund_id": "fund-buet89-relief-03",
                "sponsor_id": "spn-buet-89",
                "sponsor_name": "BUET Alumni Batch 1989",
                "fund_title": "BUET Alumni Emergency Tuition & Book Relief Pool",
                "total_grant_bdt": 100000.0,
                "disbursement_per_student_bdt": 2500.0,
                "target_criteria": self.CRITERIA_MERIT,
                "remaining_bdt": 95000.0,
                "awarded_count": 2,
                "status": "ACTIVE",
                "created_at": "2026-10-14T08:00:00Z"
            }
        ]

        for f in seeds:
            self._funds[f["fund_id"]] = f

    def create_endowment_fund(
        self,
        sponsor_id: str,
        sponsor_name: str,
        fund_title: str,
        total_grant_bdt: float,
        target_criteria: str = "UNDERPRIVILEGED_STEM",
        disbursement_per_student_bdt: float = 3000.0
    ) -> Dict[str, Any]:
        """Creates a new locked corporate or philanthropic endowment fund."""
        if not sponsor_id or not sponsor_name:
            raise ValueError("Sponsor credentials cannot be empty.")
        if not fund_title or not fund_title.strip():
            raise ValueError("Fund title cannot be empty.")
        if total_grant_bdt <= 0.0:
            raise ValueError("Total grant amount must be positive.")
        if disbursement_per_student_bdt <= 0.0 or disbursement_per_student_bdt > total_grant_bdt:
            raise ValueError("Invalid per-student stipend amount.")

        fund_id = f"fund-{uuid.uuid4().hex[:10]}"
        fund_record = {
            "fund_id": fund_id,
            "sponsor_id": sponsor_id,
            "sponsor_name": sponsor_name.strip(),
            "fund_title": fund_title.strip(),
            "total_grant_bdt": round(float(total_grant_bdt), 2),
            "disbursement_per_student_bdt": round(float(disbursement_per_student_bdt), 2),
            "target_criteria": target_criteria,
            "remaining_bdt": round(float(total_grant_bdt), 2),
            "awarded_count": 0,
            "status": "ACTIVE",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        self._funds[fund_id] = fund_record
        return fund_record

    def list_endowment_funds(self, criteria: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists active endowment funds with filter capability."""
        results = []
        for f in self._funds.values():
            if f.get("status") != "ACTIVE":
                continue
            if criteria and f["target_criteria"].upper() != criteria.upper():
                continue
            summary = {
                "fund_id": f["fund_id"],
                "sponsor_name": f["sponsor_name"],
                "fund_title": f["fund_title"],
                "total_grant_bdt": f["total_grant_bdt"],
                "disbursement_per_student_bdt": f["disbursement_per_student_bdt"],
                "target_criteria": f["target_criteria"],
                "remaining_bdt": f["remaining_bdt"],
                "awarded_count": f["awarded_count"],
                "created_at": f["created_at"]
            }
            results.append(summary)
        return results

    def _compute_need_index(self, family_monthly_income_bdt: float) -> float:
        """
        Mathematical need-index function (0.0 to 100.0):
        In Bangladesh, family income <= 15,000 BDT represents acute hardship.
        """
        if family_monthly_income_bdt <= 15000.0:
            return 100.0
        elif family_monthly_income_bdt <= 30000.0:
            # Linear scaling from 100 down to 60
            deficit = family_monthly_income_bdt - 15000.0
            return round(100.0 - (deficit / 15000.0) * 40.0, 2)
        else:
            # Diminishing need down to baseline 10.0
            excess = family_monthly_income_bdt - 30000.0
            return max(10.0, round(60.0 - (excess / 30000.0) * 50.0, 2))

    def apply_for_scholarship(
        self,
        fund_id: str,
        student_id: str,
        student_name: str,
        family_monthly_income_bdt: float,
        institution_name: str,
        cat_ability_theta: float = 0.0,
        reputation_score: float = 0.0,
        bkash_number: str = "01700000000",
        statement_of_need: str = ""
    ) -> Dict[str, Any]:
        """
        Applies for a micro-scholarship with automated composite scoring.
        Formula: Composite = 0.40 * CAT_Norm + 0.30 * Rep_Norm + 0.30 * Need_Index
        """
        if fund_id not in self._funds:
            raise KeyError(f"Endowment fund {fund_id} does not exist.")

        fund = self._funds[fund_id]
        if fund["remaining_bdt"] < fund["disbursement_per_student_bdt"]:
            raise ValueError("This endowment fund has exhausted its current allocation.")

        # Phone format validation (Bangladeshi 11-digit MSISDN)
        cleaned_phone = re.sub(r"[^\d]", "", bkash_number)
        if len(cleaned_phone) != 11 or not cleaned_phone.startswith("01"):
            raise ValueError("Invalid bKash/Nagad wallet number. Must be 11-digit Bangladeshi mobile number starting with 01.")

        # Duplicate application check
        for app in self._applications.values():
            if app["fund_id"] == fund_id and app["student_id"] == student_id and app["status"] in ["APPLIED", "APPROVED", "DISBURSED"]:
                raise ValueError("You already have an active application for this endowment fund.")

        safe_income = max(0.0, float(family_monthly_income_bdt))
        # Strip potential HTML script tags from statement of need
        safe_statement = re.sub(r'<[^>]*>', '', statement_of_need).strip() if statement_of_need else ""

        need_index = self._compute_need_index(safe_income)
        cat_norm = min(100.0, max(0.0, (cat_ability_theta + 3.0) / 6.0 * 100.0))
        rep_norm = min(100.0, max(0.0, reputation_score / 10.0))

        composite_score = round(0.40 * cat_norm + 0.30 * rep_norm + 0.30 * need_index, 2)
        status = "APPROVED" if composite_score >= 65.0 else "APPLIED"

        app_id = f"app-sch-{uuid.uuid4().hex[:10]}"
        application_record = {
            "application_id": app_id,
            "fund_id": fund_id,
            "fund_title": fund["fund_title"],
            "student_id": student_id,
            "student_name": student_name,
            "institution_name": institution_name,
            "family_monthly_income_bdt": safe_income,
            "need_index": need_index,
            "cat_ability_theta": cat_ability_theta,
            "reputation_score": reputation_score,
            "composite_score": composite_score,
            "grant_amount_bdt": fund["disbursement_per_student_bdt"],
            "bkash_number": cleaned_phone,
            "statement_of_need": safe_statement,
            "status": status,
            "applied_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "disbursement_receipt": None
        }

        self._applications[app_id] = application_record
        return application_record

    def disburse_scholarship(
        self,
        application_id: str,
        disburser_id: str,
        channel: str = "BKASH_DISBURSEMENT"
    ) -> Dict[str, Any]:
        """
        Executes micro-disbursement of scholarship funds to student's mobile wallet.
        Enforces double-payout guards and updates remaining endowment pool.
        """
        if application_id not in self._applications:
            raise KeyError(f"Application {application_id} does not exist.")

        app = self._applications[application_id]
        if app["status"] == "DISBURSED":
            raise ValueError("Scholarship funds have already been disbursed for this application.")

        fund = self._funds[app["fund_id"]]
        grant_amount = app["grant_amount_bdt"]

        if fund["remaining_bdt"] < grant_amount:
            raise ValueError("Insufficient remaining endowment funds to execute disbursement.")

        # Deduct from fund safely
        fund["remaining_bdt"] = round(fund["remaining_bdt"] - grant_amount, 2)
        fund["awarded_count"] += 1

        # Cryptographic receipt
        receipt_raw = f"sch:{application_id}|std:{app['student_id']}|amt:{grant_amount}|msisdn:{app['bkash_number']}|ts:{time.time()}".encode('utf-8')
        receipt_hash = hashlib.sha256(receipt_raw).hexdigest()

        receipt = {
            "receipt_id": f"tx-sch-{receipt_hash[:14]}",
            "application_id": application_id,
            "student_id": app["student_id"],
            "recipient_name": app["student_name"],
            "bkash_number": app["bkash_number"],
            "amount_bdt": grant_amount,
            "channel": channel,
            "disburser_id": disburser_id,
            "cryptographic_hash": receipt_hash,
            "disbursed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        app["status"] = "DISBURSED"
        app["disbursement_receipt"] = receipt
        self._disbursements.append(receipt)

        return {
            "application_id": application_id,
            "status": "DISBURSED",
            "receipt": receipt,
            "fund_remaining_bdt": fund["remaining_bdt"]
        }

    def get_application_status(self, application_id: str) -> Dict[str, Any]:
        """Retrieves scholarship application details and disbursement receipt."""
        if application_id not in self._applications:
            raise KeyError(f"Application {application_id} does not exist.")
        return self._applications[application_id]


# Global singleton instance
scholarship_endowment_service = ScholarshipEndowmentService()
