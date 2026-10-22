"""
========================================================================================
MODULE:    Test Phase 26 Enterprise Portals, Escrow Vault & Talent Scout
TOPIC:     Unit & Integration Tests for Dual-Party Escrow, Guardian Telemetry & Recruiter Hub
FILE:      backend/tests/test_phase26_enterprise_portals_and_escrow.py
PURPOSE:   Asserts that all Phase 26 modules operate reliably with zero regressions,
           enforcing OWASP ASVS L2 financial integrity and minor privacy guards.
AUDIENCE:  QA Engineers, Security Auditors & Core Developers
========================================================================================
"""

import unittest
from backend.app.services.honorarium_escrow_service import HonorariumEscrowService
from backend.app.services.guardian_telemetry_service import GuardianTelemetryService
from backend.app.services.corporate_talent_service import CorporateTalentService

from backend.app.core.fastapi_shim import APIRouter
from backend.app.api.v1.router import api_router


class TestPhase26EnterprisePortalsAndEscrow(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Phase 26: Honorarium Escrow Vault, Guardian Telemetry & Corporate Talent Scout.
    """

    def setUp(self):
        self.escrow_service = HonorariumEscrowService()
        self.guardian_service = GuardianTelemetryService()
        self.talent_service = CorporateTalentService()

    # -------------------------------------------------------------------------
    # 1. HONORARIUM ESCROW SERVICE TESTS
    # -------------------------------------------------------------------------

    def test_create_escrow_contract_success(self):
        contract = self.escrow_service.create_escrow_contract(
            contract_id="esc_test_101",
            tuition_id="tuit_dhaka_01",
            guardian_id="g_salim_01",
            tutor_id="t_tanzim_01",
            total_bdt=10000.0,
            sessions_committed=8,
            payment_method="BKASH_ESCROW"
        )
        self.assertEqual(contract["contract_id"], "esc_test_101")
        self.assertEqual(contract["total_bdt"], 10000.0)
        self.assertEqual(contract["platform_fee_bdt"], 500.0)  # 5% of 10,000
        self.assertEqual(contract["net_tutor_bdt"], 9500.0)
        self.assertEqual(contract["per_session_rate"], 1187.5)  # 9500 / 8
        self.assertEqual(contract["state"], "ESCROW_HELD")
        self.assertTrue(len(contract["initial_tx_hash"]) == 64)

    def test_create_escrow_contract_invalid_inputs(self):
        # Negative amount
        with self.assertRaises(ValueError):
            self.escrow_service.create_escrow_contract(
                contract_id="esc_fail_1",
                tuition_id="t_01",
                guardian_id="g_01",
                tutor_id="t_01",
                total_bdt=-500.0,
                sessions_committed=4
            )
        # Zero sessions
        with self.assertRaises(ValueError):
            self.escrow_service.create_escrow_contract(
                contract_id="esc_fail_2",
                tuition_id="t_01",
                guardian_id="g_01",
                tutor_id="t_01",
                total_bdt=5000.0,
                sessions_committed=0
            )

    def test_session_logging_and_duplicate_prevention(self):
        self.escrow_service.create_escrow_contract(
            contract_id="esc_test_102",
            tuition_id="tuit_02",
            guardian_id="g_02",
            tutor_id="t_02",
            total_bdt=8000.0,
            sessions_committed=4
        )

        # Log session 1
        updated = self.escrow_service.log_session_completion(
            contract_id="esc_test_102",
            tutor_id="t_02",
            session_number=1,
            topic_covered="Calculus Derivatives",
            duration_minutes=90
        )
        self.assertEqual(updated["sessions_completed"], 1)
        self.assertEqual(updated["state"], "SESSION_LOGGED")

        # Duplicate session 1 log must fail
        with self.assertRaises(ValueError):
            self.escrow_service.log_session_completion(
                contract_id="esc_test_102",
                tutor_id="t_02",
                session_number=1,
                topic_covered="Calculus Derivatives"
            )

        # Unauthorized tutor cannot log
        with self.assertRaises(PermissionError):
            self.escrow_service.log_session_completion(
                contract_id="esc_test_102",
                tutor_id="t_malicious_attacker",
                session_number=2,
                topic_covered="Physics"
            )

    def test_milestone_funds_release_and_double_release_prevention(self):
        self.escrow_service.create_escrow_contract(
            contract_id="esc_test_103",
            tuition_id="tuit_03",
            guardian_id="g_03",
            tutor_id="t_03",
            total_bdt=4000.0,
            sessions_committed=2
        )
        # Net: 3800, rate: 1900/session
        self.escrow_service.log_session_completion(
            contract_id="esc_test_103",
            tutor_id="t_03",
            session_number=1,
            topic_covered="Algebra"
        )

        release_res = self.escrow_service.release_milestone_funds(
            contract_id="esc_test_103",
            session_number=1,
            authorizer_id="g_03"
        )
        self.assertEqual(release_res["released_bdt"], 1900.0)
        self.assertEqual(release_res["remaining_held_bdt"], 2100.0)  # 4000 - 1900

        # Attempt double-release must fail
        with self.assertRaises(ValueError):
            self.escrow_service.release_milestone_funds(
                contract_id="esc_test_103",
                session_number=1,
                authorizer_id="g_03"
            )

    def test_dispute_freeze(self):
        self.escrow_service.create_escrow_contract(
            contract_id="esc_test_104",
            tuition_id="tuit_04",
            guardian_id="g_04",
            tutor_id="t_04",
            total_bdt=5000.0,
            sessions_committed=4
        )
        self.escrow_service.log_session_completion(
            contract_id="esc_test_104",
            tutor_id="t_04",
            session_number=1,
            topic_covered="Geometry"
        )

        # Guardian raises dispute
        contract = self.escrow_service.raise_milestone_dispute(
            contract_id="esc_test_104",
            session_number=1,
            guardian_id="g_04",
            reason="Tutor arrived 45 minutes late and ended session early."
        )
        self.assertEqual(contract["state"], "DISPUTE_FROZEN")

        # Releasing funds on frozen contract must fail
        with self.assertRaises(ValueError):
            self.escrow_service.release_milestone_funds(
                contract_id="esc_test_104",
                session_number=1,
                authorizer_id="g_04"
            )

    # -------------------------------------------------------------------------
    # 2. GUARDIAN TELEMETRY SERVICE TESTS
    # -------------------------------------------------------------------------

    def test_guardian_link_and_telemetry(self):
        link = self.guardian_service.link_guardian_student(
            guardian_id="g_father_01",
            student_id="s_hasan_01",
            relationship="FATHER"
        )
        self.assertEqual(link["status"], "ACTIVE")

        telemetry = self.guardian_service.get_student_telemetry_summary(
            guardian_id="g_father_01",
            student_id="s_hasan_01"
        )
        self.assertEqual(telemetry["guardian_id"], "g_father_01")
        self.assertEqual(telemetry["student_id"], "s_hasan_01")
        self.assertGreater(telemetry["weekly_study_hours"], 0)
        self.assertFalse(telemetry["safety_lock_active"])

    def test_guardian_telemetry_idor_protection(self):
        # Unlinked guardian must be denied
        with self.assertRaises(PermissionError):
            self.guardian_service.get_student_telemetry_summary(
                guardian_id="g_unauthorized_stalker",
                student_id="s_private_student_99"
            )

    def test_guardian_safety_lock_toggle(self):
        lock_res = self.guardian_service.toggle_safety_lock(
            guardian_id="g_mother_02",
            student_id="s_child_02",
            lock_active=True,
            reason="Exam prep week; restricting outbound contact."
        )
        self.assertTrue(lock_res["safety_lock_active"])
        self.assertEqual(lock_res["status"], "SAFETY_LOCK_ENGAGED")

        # Unlock
        unlock_res = self.guardian_service.toggle_safety_lock(
            guardian_id="g_mother_02",
            student_id="s_child_02",
            lock_active=False
        )
        self.assertFalse(unlock_res["safety_lock_active"])
        self.assertEqual(unlock_res["status"], "SAFETY_LOCK_DISENGAGED")

    # -------------------------------------------------------------------------
    # 3. CORPORATE TALENT SCOUT SERVICE TESTS
    # -------------------------------------------------------------------------

    def test_talent_pool_search(self):
        # Search all
        all_cands = self.talent_service.search_talent_pool()
        self.assertGreaterEqual(len(all_cands), 4)

        # Filter by domain
        software_cands = self.talent_service.search_talent_pool(domain="Software")
        for c in software_cands:
            self.assertEqual(c["target_domain"], "Software")

        # Filter by high CAT ability (theta >= 1.7)
        top_tier = self.talent_service.search_talent_pool(min_theta=1.7)
        self.assertGreaterEqual(len(top_tier), 2)
        for c in top_tier:
            self.assertGreaterEqual(c["cat_latent_theta"], 1.7)

        # Keyword search
        buet_cands = self.talent_service.search_talent_pool(keyword="BUET")
        self.assertEqual(len(buet_cands), 1)
        self.assertEqual(buet_cands[0]["institution"], "BUET")

    def test_dispatch_interview_invitation(self):
        inv = self.talent_service.dispatch_interview_invitation(
            recruiter_id="rec_pathao_01",
            company_name="Pathao Technologies",
            candidate_id="cand_001",
            role_title="Junior Software Engineer",
            proposed_date="Next Monday 10:00 AM"
        )
        self.assertEqual(inv["candidate_name"], "Tanzim Hasan")
        self.assertEqual(inv["status"], "INVITATION_SENT")

        # Non-existent candidate must fail
        with self.assertRaises(KeyError):
            self.talent_service.dispatch_interview_invitation(
                recruiter_id="rec_pathao_01",
                company_name="Pathao",
                candidate_id="cand_fake_999",
                role_title="Developer"
            )

    def test_recruiter_shortlist(self):
        res = self.talent_service.shortlist_candidate(
            recruiter_id="rec_brainstation_01",
            candidate_id="cand_002"
        )
        self.assertEqual(res["status"], "SHORTLISTED")

        shortlist = self.talent_service.get_recruiter_shortlist("rec_brainstation_01")
        self.assertEqual(len(shortlist), 1)
        self.assertEqual(shortlist[0]["candidate_id"], "cand_002")

    # -------------------------------------------------------------------------
    # 4. REST ROUTER ENDPOINTS INTEGRATION TESTS
    # -------------------------------------------------------------------------

    async def test_router_escrow_endpoints(self):
        from backend.app.api.v1.router import (
            create_escrow_contract,
            log_escrow_session_completion,
            release_escrow_milestone_funds,
            get_escrow_contract_details,
            list_user_escrow_contracts
        )
        from backend.app.schemas.enterprise_portal_schema import (
            CreateEscrowContractRequest,
            LogSessionCompletionRequest,
            ReleaseMilestoneFundsRequest
        )

        # 1. Create contract via router
        req = CreateEscrowContractRequest(
            contract_id="esc_router_99",
            tuition_id="tuit_router_01",
            guardian_id="g_router_01",
            tutor_id="t_router_01",
            total_bdt=6000.0,
            sessions_committed=3
        )
        res = await create_escrow_contract(req)
        self.assertEqual(res["contract_id"], "esc_router_99")
        self.assertEqual(res["platform_fee_bdt"], 300.0)

        # 2. Log session via router
        log_req = LogSessionCompletionRequest(
            contract_id="esc_router_99",
            tutor_id="t_router_01",
            session_number=1,
            topic_covered="Higher Math Integration",
            duration_minutes=90
        )
        log_res = await log_escrow_session_completion(log_req)
        self.assertEqual(log_res["sessions_completed"], 1)

        # 3. Release milestone funds via router
        rel_req = ReleaseMilestoneFundsRequest(
            contract_id="esc_router_99",
            session_number=1,
            authorizer_id="g_router_01"
        )
        rel_res = await release_escrow_milestone_funds(rel_req)
        self.assertEqual(rel_res["released_bdt"], 1900.0)

        # 4. Fetch details
        details = await get_escrow_contract_details("esc_router_99")
        self.assertEqual(details["contract_id"], "esc_router_99")

        # 5. List user contracts
        user_contracts = await list_user_escrow_contracts("g_router_01")
        self.assertGreaterEqual(len(user_contracts), 1)

    async def test_router_guardian_and_talent_endpoints(self):
        from backend.app.api.v1.router import (
            get_student_guardian_telemetry,
            toggle_guardian_safety_lock,
            search_talent_candidates,
            dispatch_interview_invitation,
            shortlist_talent_candidate,
            get_recruiter_shortlist
        )
        from backend.app.schemas.enterprise_portal_schema import (
            ToggleSafetyLockRequest,
            DispatchInterviewInvitationRequest,
            ShortlistCandidateRequest
        )

        # 1. Guardian Telemetry
        telemetry = await get_student_guardian_telemetry(
            guardian_id="g_guardian_demo",
            student_id="student_default"
        )
        self.assertEqual(telemetry["student_id"], "student_default")
        self.assertGreater(telemetry["weekly_study_hours"], 0)

        # 2. Safety Lock
        lock_req = ToggleSafetyLockRequest(
            guardian_id="g_guardian_demo",
            student_id="student_default",
            lock_active=True,
            reason="Exams ongoing"
        )
        lock_res = await toggle_guardian_safety_lock(lock_req)
        self.assertTrue(lock_res["safety_lock_active"])

        # 3. Search talent
        candidates = await search_talent_candidates(domain="Software", min_theta=1.0)
        self.assertGreaterEqual(len(candidates), 1)

        # 4. Dispatch invite
        inv_req = DispatchInterviewInvitationRequest(
            recruiter_id="rec_bjobs_hr",
            company_name="Chaldal EdTech",
            candidate_id="cand_001",
            role_title="Backend Intern",
            proposed_date="Tomorrow 3 PM"
        )
        inv_res = await dispatch_interview_invitation(inv_req)
        self.assertEqual(inv_res["status"], "INVITATION_SENT")

        # 5. Shortlist
        sl_req = ShortlistCandidateRequest(
            recruiter_id="rec_bjobs_hr",
            candidate_id="cand_001"
        )
        sl_res = await shortlist_talent_candidate(sl_req)
        self.assertEqual(sl_res["status"], "SHORTLISTED")


if __name__ == "__main__":
    unittest.main()

