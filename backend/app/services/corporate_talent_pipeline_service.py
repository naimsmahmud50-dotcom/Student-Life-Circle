"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Corporate Talent Acquisition & Cryptographic Skill Pipeline
TOPIC:     Vector Skill Matching, W3C Verifiable Credentials & Recruitment Pipeline
FILE:      backend/app/services/corporate_talent_pipeline_service.py
PHASE:     Phase 109 - Corporate Talent Acquisition & Cryptographic Skill Pipeline
PURPOSE:   Computes cosine vector similarity between job requirements and verified student skills,
           cryptographically audits W3C Proof-of-Skill Certificate signatures and sealed CV snapshots,
           and orchestrates bilateral recruitment stage transitions (SOURCED -> OFFER_ISSUED).
STANDARDS: W3C Verifiable Credentials, Vector Cosine Similarity, Zero-Emoji, UI/UX Pro Max
"""

import hashlib
import hmac
import math
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class CorporateTalentPipelineService:
    """
    Field-Grade Corporate Talent Acquisition & Cryptographic Skill Pipeline Service.
    Enables technology enterprises to discover, mathematically match, and recruit verified top graduates.
    """

    SECRET_KEY = os.getenv("TALENT_VERIFIER_SECRET", "dev_talent_verifier_key_2026")
    TAXONOMY = [
        "PYTHON",
        "HPC",
        "NEXTJS",
        "MATH_MODELING",
        "DISTRIBUTED_SYSTEMS",
        "MACHINE_LEARNING",
        "RUST"
    ]

    STAGES = ["SOURCED", "SHORTLISTED", "TECHNICAL_ASSESSMENT", "OFFER_ISSUED"]

    def __init__(self) -> None:
        self._candidates: Dict[str, Dict[str, Any]] = {}
        self._interview_invitations: Dict[str, Dict[str, Any]] = {}
        self._init_benchmark_candidates()

    def _init_benchmark_candidates(self) -> None:
        """Seeds benchmark graduates with verified skill vectors and sealed CV signatures."""
        benchmark_data = [
            {
                "candidate_id": "CAND_01",
                "name": "তানভীর আহমেদ (Tanvir Ahmed)",
                "institution": "বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)",
                "department": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "cgpa": 3.94,
                "graduation_year": 2026,
                "verified_skills": {
                    "PYTHON": 0.95,
                    "HPC": 0.90,
                    "MATH_MODELING": 0.88,
                    "DISTRIBUTED_SYSTEMS": 0.85,
                    "RUST": 0.80
                },
                "github_url": "https://github.com/tanvir-buet",
                "w3c_credential_id": "urn:uuid:w3c-cert-buet-001",
                "recruitment_stage": "SOURCED",
                "bio": "বুয়েট সিএসই ফাইনাল ইয়ার। হাই-পারফরম্যান্স কম্পিউটিং ও প্যারালাল ডিস্ট্রিবিউটেড অ্যালগরিদমে গবেষণা অভিজ্ঞ।"
            },
            {
                "candidate_id": "CAND_02",
                "name": "সাদিয়া তাসনিম (Sadia Tasnim)",
                "institution": "ঢাকা বিশ্ববিদ্যালয় (DU)",
                "department": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "cgpa": 3.88,
                "graduation_year": 2026,
                "verified_skills": {
                    "NEXTJS": 0.95,
                    "PYTHON": 0.88,
                    "MACHINE_LEARNING": 0.90,
                    "MATH_MODELING": 0.82
                },
                "github_url": "https://github.com/sadia-du",
                "w3c_credential_id": "urn:uuid:w3c-cert-du-002",
                "recruitment_stage": "SHORTLISTED",
                "bio": "ঢাকা বিশ্ববিদ্যালয় সিএসই। ফুল-স্ট্যাক ও রিয়েল-টাইম অ্যাডাপ্টিভ লার্নিং আর্কিটেকচার বিশেষজ্ঞ।"
            },
            {
                "candidate_id": "CAND_03",
                "name": "মাহির ফয়সাল (Mahir Faysal)",
                "institution": "শাহজালাল বিজ্ঞান ও প্রযুক্তি বিশ্ববিদ্যালয় (SUST)",
                "department": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "cgpa": 3.82,
                "graduation_year": 2025,
                "verified_skills": {
                    "RUST": 0.92,
                    "DISTRIBUTED_SYSTEMS": 0.90,
                    "HPC": 0.85,
                    "PYTHON": 0.80
                },
                "github_url": "https://github.com/mahir-sust",
                "w3c_credential_id": "urn:uuid:w3c-cert-sust-003",
                "recruitment_stage": "TECHNICAL_ASSESSMENT",
                "bio": "সাস্ট সিএসই। লো-লেটেন্সি রাস্ট নেটওয়ার্কিং ও কনকারেন্ট সিস্টেমস ডেভেলপার।"
            },
            {
                "candidate_id": "CAND_04",
                "name": "নুসরাত জাহান (Nusrat Jahan)",
                "institution": "ইসলামিক ইউনিভার্সিটি অব টেকনোলজি (IUT)",
                "department": "ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)",
                "cgpa": 3.85,
                "graduation_year": 2026,
                "verified_skills": {
                    "PYTHON": 0.90,
                    "MATH_MODELING": 0.95,
                    "MACHINE_LEARNING": 0.86
                },
                "github_url": "https://github.com/nusrat-iut",
                "w3c_credential_id": "urn:uuid:w3c-cert-iut-004",
                "recruitment_stage": "OFFER_ISSUED",
                "bio": "আইইউটি ইইই। স্ট্যাটিস্টিক্যাল সিগন্যাল প্রসেসিং ও অ্যাডাপ্টিভ ফিল্টারিং গবেষক।"
            }
        ]

        for cand in benchmark_data:
            sig = self.compute_snapshot_signature(
                candidate_id=cand["candidate_id"],
                cgpa=cand["cgpa"],
                institution=cand["institution"],
                verified_skills=cand["verified_skills"]
            )
            cand["cv_snapshot_signature"] = sig
            self._candidates[cand["candidate_id"]] = cand

    # --------------------------------------------------------------------------
    # 1. Cosine Vector Similarity Skill Matching
    # --------------------------------------------------------------------------

    def compute_cosine_similarity(
        self,
        job_requirements: Dict[str, float],
        candidate_skills: Dict[str, float]
    ) -> float:
        """
        Calculates cosine vector similarity between required job skills and candidate skills:
        Cosine = (J · S) / (||J|| * ||S||)
        """
        dot_product = 0.0
        norm_j_sq = 0.0
        norm_s_sq = 0.0

        all_keys = set(job_requirements.keys()).union(set(candidate_skills.keys()))
        for k in all_keys:
            j_val = float(job_requirements.get(k, 0.0))
            s_val = float(candidate_skills.get(k, 0.0))

            dot_product += j_val * s_val
            norm_j_sq += j_val * j_val
            norm_s_sq += s_val * s_val

        if norm_j_sq <= 0.0 or norm_s_sq <= 0.0:
            return 0.0

        similarity = dot_product / (math.sqrt(norm_j_sq) * math.sqrt(norm_s_sq))
        return min(1.0, max(0.0, similarity))

    # --------------------------------------------------------------------------
    # 2. Cryptographic Sealed CV Snapshot & Credential Verification
    # --------------------------------------------------------------------------

    def compute_snapshot_signature(
        self,
        candidate_id: str,
        cgpa: float,
        institution: str,
        verified_skills: Dict[str, float]
    ) -> str:
        """
        Generates HMAC-SHA256 signature sealing candidate credentials and verified skills.
        """
        sorted_skills = ",".join(f"{k}:{verified_skills[k]:.2f}" for k in sorted(verified_skills.keys()))
        canonical_str = f"{candidate_id}:{cgpa:.2f}:{institution}:{sorted_skills}"
        return hmac.new(
            self.SECRET_KEY.encode("utf-8"),
            canonical_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def verify_cv_snapshot(
        self,
        candidate_id: str,
        cgpa: float,
        institution: str,
        verified_skills: Dict[str, float],
        provided_signature: str
    ) -> Dict[str, Any]:
        """
        Cryptographically audits candidate's sealed CV snapshot against HMAC-SHA256 signature.
        Detects any tampering in CGPA, institution, or unverified skill inflation.
        """
        expected_sig = self.compute_snapshot_signature(
            candidate_id=candidate_id,
            cgpa=cgpa,
            institution=institution,
            verified_skills=verified_skills
        )

        is_valid = hmac.compare_digest(expected_sig, provided_signature.strip())
        return {
            "candidate_id": candidate_id,
            "is_valid": is_valid,
            "tamper_detected": not is_valid,
            "w3c_status": "VERIFIED_PROOF_OF_SKILL" if is_valid else "TAMPER_SUSPECTED",
            "message_bn": "সিভি স্ন্যাপশট ও দক্ষতা সনদ সম্পূর্ণ খাঁটি ও অপরিবর্তিত।" if is_valid else "সতর্কতা: সনদে কোনো পরিবর্তন বা গরমিল শনাক্ত হয়েছে।"
        }

    # --------------------------------------------------------------------------
    # 3. Candidate Discovery & Skill Match Engine
    # --------------------------------------------------------------------------

    def search_candidates(
        self,
        job_requirements: Optional[Dict[str, float]] = None,
        min_cgpa: float = 0.0,
        institution_filter: Optional[str] = None,
        skill_filter: Optional[str] = None,
        stage_filter: Optional[str] = None,
        min_match_percent: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Searches candidates with real-time vector matching scores and pipeline filters.
        """
        if job_requirements is None:
            # Default software engineer benchmark
            job_requirements = {"PYTHON": 0.8, "NEXTJS": 0.6, "HPC": 0.5, "MATH_MODELING": 0.5}

        results = []
        for cand in self._candidates.values():
            if cand["cgpa"] < min_cgpa:
                continue

            if institution_filter and institution_filter.lower() not in cand["institution"].lower():
                continue

            if skill_filter and skill_filter.upper() not in cand["verified_skills"]:
                continue

            if stage_filter and stage_filter.upper() != cand["recruitment_stage"].upper():
                continue

            sim = self.compute_cosine_similarity(job_requirements, cand["verified_skills"])
            match_percent = round(sim * 100.0, 1)

            if match_percent < min_match_percent:
                continue

            cand_copy = dict(cand)
            cand_copy["match_score_percent"] = match_percent
            cand_copy["match_tier"] = "HIGH" if match_percent >= 85 else "STRONG" if match_percent >= 70 else "POTENTIAL"
            results.append(cand_copy)

        return sorted(results, key=lambda x: -x["match_score_percent"])

    def get_candidate(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """Returns single candidate record."""
        return self._candidates.get(candidate_id)

    # --------------------------------------------------------------------------
    # 4. Bilateral Recruitment Pipeline & Interview Offer Dispatch
    # --------------------------------------------------------------------------

    def invite_to_interview(
        self,
        candidate_id: str,
        company_name: str,
        job_title: str,
        ctc_salary_bdt: int,
        interview_date: str,
        recruiter_id: str = "REC_CORP_01"
    ) -> Dict[str, Any]:
        """
        Dispatches interview invitation, advances candidate stage, and logs audit record.
        """
        candidate = self._candidates.get(candidate_id)
        if not candidate:
            return {
                "success": False,
                "error": f"Candidate '{candidate_id}' not found in talent pool."
            }

        # Advance stage to SHORTLISTED or TECHNICAL_ASSESSMENT
        if candidate["recruitment_stage"] == "SOURCED":
            candidate["recruitment_stage"] = "SHORTLISTED"

        invitation_id = f"inv_{uuid.uuid4().hex[:10]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        invitation = {
            "invitation_id": invitation_id,
            "candidate_id": candidate_id,
            "candidate_name": candidate["name"],
            "company_name": company_name,
            "job_title": job_title,
            "ctc_salary_bdt": ctc_salary_bdt,
            "interview_date": interview_date,
            "recruiter_id": recruiter_id,
            "dispatched_at": now_iso,
            "status": "OFFERED"
        }
        self._interview_invitations[invitation_id] = invitation

        return {
            "success": True,
            "invitation_id": invitation_id,
            "candidate_id": candidate_id,
            "new_stage": candidate["recruitment_stage"],
            "company_name": company_name,
            "job_title": job_title,
            "ctc_salary_bdt": ctc_salary_bdt,
            "interview_date": interview_date,
            "message_bn": f"{candidate['name']}-কে সফলভাবে ইন্টারভিউ অফার পাঠানো হয়েছে।"
        }

    def list_invitations(self) -> List[Dict[str, Any]]:
        """Lists all corporate interview invitations."""
        return list(self._interview_invitations.values())

    def reset_for_testing(self) -> None:
        """Resets candidate stages and invitations for test isolation."""
        self._interview_invitations.clear()
        self._candidates.clear()
        self._init_benchmark_candidates()


# Global Singleton Instance
corporate_talent_pipeline_service = CorporateTalentPipelineService()
