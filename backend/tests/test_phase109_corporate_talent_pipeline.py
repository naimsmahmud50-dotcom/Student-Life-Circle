"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 109 Corporate Talent Acquisition & Cryptographic Skill Pipeline Tests
FILE:      backend/tests/test_phase109_corporate_talent_pipeline.py
PHASE:     Phase 109 - Corporate Talent Acquisition & Cryptographic Skill Pipeline
PURPOSE:   Asserts cosine vector similarity skill matching, tamper detection on sealed CV
           snapshots, bilateral recruitment pipeline transitions, REST API endpoints,
           and strict zero-emoji governance.
STANDARDS: W3C Verifiable Credentials, Vector Cosine Similarity, Zero-Emoji, UI/UX Pro Max
"""

import asyncio
import json
import os
import unittest
from pathlib import Path

from backend.app.services.corporate_talent_pipeline_service import (
    CorporateTalentPipelineService,
    corporate_talent_pipeline_service
)
from backend.app.api.v1.endpoints.talent_pipeline import (
    list_talent_candidates,
    dispatch_interview_invitation,
    verify_cv_snapshot_endpoint,
    calculate_custom_match_score
)
from backend.app.core.fastapi_shim import HTTPException


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is a decorative unicode emoji."""
    code = ord(char)
    return (
        0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF
    )


def contains_emoji(text: str) -> bool:
    """Returns True if string contains any decorative unicode emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase109CorporateTalentPipeline(unittest.TestCase):
    """
    Automated verification suite for Phase 109 Corporate Talent Acquisition & Cryptographic Skill Pipeline.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.service_path = cls.repo_root / "backend" / "app" / "services" / "corporate_talent_pipeline_service.py"
        cls.endpoint_path = cls.repo_root / "backend" / "app" / "api" / "v1" / "endpoints" / "talent_pipeline.py"
        cls.card_path = cls.repo_root / "frontend" / "src" / "components" / "career" / "CandidateTalentCard.tsx"
        cls.portal_path = cls.repo_root / "frontend" / "src" / "components" / "career" / "CorporateRecruiterPortal.tsx"
        cls.page_path = cls.repo_root / "frontend" / "src" / "pages" / "recruiter.tsx"
        cls.tasks_path = cls.repo_root / "specs" / "013-phase109-corporate-talent-pipeline" / "tasks.md"

    def setUp(self):
        corporate_talent_pipeline_service.reset_for_testing()

    def test_01_cosine_vector_similarity_skill_matching(self):
        """Verifies cosine vector similarity mathematical precision and ranking."""
        svc = corporate_talent_pipeline_service

        # 1. Identical vectors -> 1.0 (100% match)
        v1 = {"PYTHON": 0.9, "HPC": 0.8}
        sim_identical = svc.compute_cosine_similarity(v1, v1)
        self.assertAlmostEqual(sim_identical, 1.0, places=4)

        # 2. Orthogonal vectors -> 0.0 (0% match)
        v_job = {"RUST": 1.0}
        v_cand = {"NEXTJS": 1.0}
        sim_orthogonal = svc.compute_cosine_similarity(v_job, v_cand)
        self.assertEqual(sim_orthogonal, 0.0)

        # 3. Partial overlap
        v_req = {"PYTHON": 0.9, "HPC": 0.8, "NEXTJS": 0.5}
        v_student = {"PYTHON": 0.95, "HPC": 0.90}
        sim_partial = svc.compute_cosine_similarity(v_req, v_student)
        self.assertTrue(0.80 <= sim_partial <= 0.99)

        # 4. Search candidates ranked by score
        ranked = svc.search_candidates(job_requirements={"PYTHON": 0.9, "HPC": 0.9})
        self.assertGreater(len(ranked), 0)
        self.assertIn("match_score_percent", ranked[0])
        # Ranked descending by match score
        for i in range(len(ranked) - 1):
            self.assertGreaterEqual(ranked[i]["match_score_percent"], ranked[i+1]["match_score_percent"])

    def test_02_cryptographic_sealed_cv_snapshot_tamper_detection(self):
        """Verifies HMAC-SHA256 sealed CV snapshot audit detects unapproved grade or credential alterations."""
        svc = corporate_talent_pipeline_service
        cand = svc.get_candidate("CAND_01")
        self.assertIsNotNone(cand)

        # 1. Authentic signature must pass
        valid_res = svc.verify_cv_snapshot(
            candidate_id=cand["candidate_id"],
            cgpa=cand["cgpa"],
            institution=cand["institution"],
            verified_skills=cand["verified_skills"],
            provided_signature=cand["cv_snapshot_signature"]
        )
        self.assertTrue(valid_res["is_valid"])
        self.assertFalse(valid_res["tamper_detected"])
        self.assertEqual(valid_res["w3c_status"], "VERIFIED_PROOF_OF_SKILL")

        # 2. Tampered CGPA (e.g. 3.94 -> 4.00) must be caught immediately
        tampered_res = svc.verify_cv_snapshot(
            candidate_id=cand["candidate_id"],
            cgpa=4.00,
            institution=cand["institution"],
            verified_skills=cand["verified_skills"],
            provided_signature=cand["cv_snapshot_signature"]
        )
        self.assertFalse(tampered_res["is_valid"])
        self.assertTrue(tampered_res["tamper_detected"])
        self.assertEqual(tampered_res["w3c_status"], "TAMPER_SUSPECTED")

    def test_03_recruitment_pipeline_stage_transitions(self):
        """Verifies bilateral recruitment pipeline lifecycle transitions and interview invitation dispatch."""
        svc = corporate_talent_pipeline_service
        cand_id = "CAND_01"

        # Initially SOURCED
        cand = svc.get_candidate(cand_id)
        self.assertEqual(cand["recruitment_stage"], "SOURCED")

        # Issue interview invitation
        res = svc.invite_to_interview(
            candidate_id=cand_id,
            company_name="Enosis Solutions",
            job_title="Software Engineer (Backend & HPC)",
            ctc_salary_bdt=175000,
            interview_date="2026-11-10"
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["new_stage"], "SHORTLISTED")
        self.assertIn("invitation_id", res)

        # Verify candidate stage updated in registry
        updated_cand = svc.get_candidate(cand_id)
        self.assertEqual(updated_cand["recruitment_stage"], "SHORTLISTED")

        # Verify invitation logged
        invites = svc.list_invitations()
        self.assertEqual(len(invites), 1)
        self.assertEqual(invites[0]["candidate_id"], cand_id)

    async def _test_async_endpoints(self):
        """Helper to run async endpoint unit tests."""
        def extract_content(res):
            if hasattr(res, "body"):
                return json.loads(res.body.decode("utf-8"))
            return getattr(res, "content", {})

        # 1. Candidate search endpoint
        cand_res = await list_talent_candidates(min_cgpa=3.5, university=None, skill=None, stage=None, min_match_percent=0.0)
        self.assertEqual(cand_res.status_code, 200)
        cand_data = extract_content(cand_res)
        self.assertGreaterEqual(cand_data["total"], 2)

        # 2. Match score endpoint
        score_payload = {
            "job_requirements": {"PYTHON": 0.9, "HPC": 0.8},
            "candidate_skills": {"PYTHON": 0.95, "HPC": 0.90}
        }
        score_res = await calculate_custom_match_score(score_payload)
        self.assertEqual(score_res.status_code, 200)
        score_data = extract_content(score_res)
        self.assertGreaterEqual(score_data["match_percent"], 90.0)

        # 3. CV Snapshot verify endpoint
        cand = corporate_talent_pipeline_service.get_candidate("CAND_01")
        verify_payload = {
            "candidate_id": cand["candidate_id"],
            "cgpa": cand["cgpa"],
            "institution": cand["institution"],
            "verified_skills": cand["verified_skills"],
            "signature": cand["cv_snapshot_signature"]
        }
        verify_res = await verify_cv_snapshot_endpoint(verify_payload)
        self.assertEqual(verify_res.status_code, 200)
        verify_data = extract_content(verify_res)
        self.assertTrue(verify_data["is_valid"])

        # 4. Dispatch interview invitation endpoint
        invite_payload = {
            "candidate_id": "CAND_02",
            "company_name": "Brain Station 23",
            "job_title": "Full-Stack Engineer (React & Python)",
            "ctc_salary_bdt": 160000,
            "interview_date": "2026-11-12"
        }
        invite_res = await dispatch_interview_invitation(invite_payload)
        self.assertEqual(invite_res.status_code, 200)
        invite_data = extract_content(invite_res)
        self.assertTrue(invite_data["success"])

        # 5. Invalid invite payload raises 400
        with self.assertRaises(HTTPException) as cm:
            await dispatch_interview_invitation({"candidate_id": ""})
        self.assertEqual(cm.exception.status_code, 400)

    def test_04_rest_api_endpoints_candidates_verify_invite(self):
        """Verifies Phase 109 REST API endpoints through direct async invocation."""
        asyncio.run(self._test_async_endpoints())

    def test_05_developer_architecture_note_and_strict_zero_emoji(self):
        """Verifies Developer Architecture Note headers and strict zero-emoji governance across Phase 109 files."""
        phase109_files = [
            self.service_path,
            self.endpoint_path,
            self.card_path,
            self.portal_path,
            self.page_path,
            self.tasks_path,
            Path(__file__)
        ]

        for file_path in phase109_files:
            self.assertTrue(file_path.exists(), f"File does not exist: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 109",
                content,
                f"Missing Phase 109 reference in {file_path.name}"
            )
            self.assertFalse(
                contains_emoji(content),
                f"Strict Zero-Emoji violation detected in {file_path.name}"
            )


if __name__ == "__main__":
    unittest.main()
