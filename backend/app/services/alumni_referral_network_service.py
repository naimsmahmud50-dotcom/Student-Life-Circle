"""
AlumniReferralNetworkService:
Decentralized Multi-Campus Alumni Job Referral Graph & Fast-Track Gateway.
Bridges Bangladesh's entry-level talent with verified alumni at top technology
and multinational enterprises (Google, Microsoft, bKash, Pathao, Brain Station 23).
Features:
- Multi-campus alumni directory (BUET, DU, SUST, IUT, NSU, BRACU)
- Cryptographic referral token synthesis with HMAC/SHA-256 signatures
- Strict monthly alumni quota management (prevents referral spam)
- Duplicate endorsement prevention per company
- 5-stage corporate hiring lifecycle tracking
"""

import uuid
import hmac
import hashlib
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class AlumniReferralNetworkService:
    SALT = "Agrojatra_Alumni_Referral_Secret_Salt_2026"

    SEED_ALUMNI = [
        {
            "alumni_id": "alm-goog-01",
            "alumni_name": "Tanvir Rahman",
            "company": "Google",
            "role_title": "Senior Software Engineer (Cloud Infrastructure)",
            "alma_mater": "BUET",
            "department": "Computer Science & Engineering",
            "graduation_year": 2019,
            "max_monthly_referrals": 4,
            "active_referrals_count": 1
        },
        {
            "alumni_id": "alm-bkash-02",
            "alumni_name": "Sumaiya Farhana",
            "company": "bKash Limited",
            "role_title": "Lead Backend & Distributed Systems Architect",
            "alma_mater": "University of Dhaka (DU)",
            "department": "Applied Physics & Electronics",
            "graduation_year": 2020,
            "max_monthly_referrals": 5,
            "active_referrals_count": 2
        },
        {
            "alumni_id": "alm-pathao-03",
            "alumni_name": "Nabil Ahmed",
            "company": "Pathao",
            "role_title": "Principal Machine Learning Engineer",
            "alma_mater": "IUT",
            "department": "Computer Science & Engineering",
            "graduation_year": 2021,
            "max_monthly_referrals": 5,
            "active_referrals_count": 0
        },
        {
            "alumni_id": "alm-bs23-04",
            "alumni_name": "Farzana Yasmin",
            "company": "Brain Station 23",
            "role_title": "Engineering Manager (Enterprise Fintech)",
            "alma_mater": "SUST",
            "department": "Computer Science & Engineering",
            "graduation_year": 2018,
            "max_monthly_referrals": 6,
            "active_referrals_count": 3
        }
    ]

    def __init__(self):
        self._lock = threading.Lock()
        self._alumni_directory: Dict[str, Dict[str, Any]] = {
            a["alumni_id"]: dict(a) for a in self.SEED_ALUMNI
        }
        self._referrals: Dict[str, Dict[str, Any]] = {}
        self._student_company_map: Dict[str, List[str]] = {}  # student_id -> [company]

    def _generate_signature(self, alumni_id: str, student_id: str, company: str, timestamp: str) -> str:
        payload = f"{alumni_id}:{student_id}:{company}:{timestamp}"
        return hmac.new(self.SALT.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

    def get_alumni_directory(self, company_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            alumni_list = list(self._alumni_directory.values())
            if company_filter:
                f = company_filter.lower()
                return [a for a in alumni_list if f in a["company"].lower()]
            return alumni_list

    def get_alumni_by_id(self, alumni_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._alumni_directory.get(alumni_id)

    def issue_referral_endorsement(
        self,
        alumni_id: str,
        student_id: str,
        student_name: str,
        target_role: str,
        endorsement_notes: str = ""
    ) -> Dict[str, Any]:
        with self._lock:
            alumni = self._alumni_directory.get(alumni_id)
            if not alumni:
                raise ValueError(f"Alumni ID '{alumni_id}' not found in verified network.")

            # Check monthly quota
            if alumni["active_referrals_count"] >= alumni["max_monthly_referrals"]:
                raise ValueError(
                    f"Alumni {alumni['alumni_name']} has reached the monthly quota of "
                    f"{alumni['max_monthly_referrals']} referrals."
                )

            # Check duplicate referral for same company
            company = alumni["company"]
            companies_applied = self._student_company_map.get(student_id, [])
            if company in companies_applied:
                raise ValueError(f"Student '{student_id}' already holds an active referral endorsement for {company}.")

            # Synthesize referral token & HMAC
            now_iso = datetime.now(timezone.utc).isoformat()
            ref_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
            sig = self._generate_signature(alumni_id, student_id, company, now_iso)
            token = f"AGROREF|{ref_id}|{sig[:16]}"

            record = {
                "referral_id": ref_id,
                "alumni_id": alumni_id,
                "alumni_name": alumni["alumni_name"],
                "student_id": student_id,
                "student_name": student_name,
                "target_company": company,
                "target_role": target_role,
                "endorsement_notes": endorsement_notes or "Verified academic and problem-solving excellence.",
                "endorsement_token": token,
                "hmac_signature": sig,
                "status": "ISSUED",
                "created_at": now_iso
            }

            self._referrals[ref_id] = record
            alumni["active_referrals_count"] += 1
            if student_id not in self._student_company_map:
                self._student_company_map[student_id] = []
            self._student_company_map[student_id].append(company)

            return record

    def get_referral(self, referral_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._referrals.get(referral_id)

    def advance_referral_status(self, referral_id: str, next_status: str) -> Dict[str, Any]:
        with self._lock:
            ref = self._referrals.get(referral_id)
            if not ref:
                raise ValueError(f"Referral ID '{referral_id}' not found.")

            valid_statuses = ["ISSUED", "SUBMITTED", "EMPLOYER_REVIEW", "INTERVIEW_SCHEDULED", "HIRED"]
            if next_status not in valid_statuses:
                raise ValueError(f"Invalid status '{next_status}'. Must be one of {valid_statuses}")

            ref["status"] = next_status
            ref["updated_at"] = datetime.now(timezone.utc).isoformat()
            return ref

    def verify_referral_token(self, token: str) -> Dict[str, Any]:
        with self._lock:
            parts = token.strip().split("|")
            if len(parts) != 3 or parts[0] != "AGROREF":
                return {
                    "is_valid": False,
                    "status": "INVALID_FORMAT",
                    "referral": None
                }

            ref_id = parts[1]
            ref = self._referrals.get(ref_id)
            if not ref:
                return {
                    "is_valid": False,
                    "status": "NOT_FOUND",
                    "referral": None
                }

            expected_sig = self._generate_signature(
                ref["alumni_id"],
                ref["student_id"],
                ref["target_company"],
                ref["created_at"]
            )

            if expected_sig[:16] != parts[2]:
                return {
                    "is_valid": False,
                    "status": "TAMPERED_SIGNATURE",
                    "referral": None
                }

            return {
                "is_valid": True,
                "status": "AUTHENTIC",
                "referral": ref
            }


alumni_referral_network_service = AlumniReferralNetworkService()
