# ============================================================================
# MODULE: PHASE 27 VERIFICATION SUITE
# TOPIC: Peer Study Circles, WebRTC Signaling, Whiteboard & Gamified Bounty Arena
# FILE: backend/tests/test_phase27_collaborative_study_and_bounties.py
# PURPOSE: Validate end-to-end functionality, ASVS L2 security isolation,
#          concurrency race guards, and REST contracts for Phase 27.
# STANDARDS: Unittest, OWASP ASVS L2, Anti-Self-Dealing Verification
# AUDIENCE: QA Engineers, Core Backend Engineers, Security Reviewers
# ============================================================================

import unittest
from backend.app.services.study_room_service import StudyRoomCollaborationService
from backend.app.services.bounty_tribunal_service import BountyTribunalService
from backend.app.schemas.collaborative_study_schema import (
    CreateStudyRoomRequest,
    JoinStudyRoomRequest,
    WhiteboardSyncRequest,
    PomodoroSyncRequest,
    CreateBountyRequest,
    SubmitSolutionRequest,
    VerdictBountyRequest
)


class TestStudyRoomCollaborationService(unittest.TestCase):
    """Unit tests verifying synchronous peer study circle room lifecycle and whiteboard."""

    def setUp(self):
        self.service = StudyRoomCollaborationService()

    def test_create_study_room_success(self):
        room = self.service.create_study_room(
            title="DU A-Unit Physics Marathon",
            host_id="student-hassan",
            host_name="Hassan Mahmud",
            topic="Modern Physics",
            target_grade="Admission-DU",
            max_participants=12,
            is_private=False
        )
        self.assertTrue(room["room_id"].startswith("room-"))
        self.assertEqual(room["title"], "DU A-Unit Physics Marathon")
        self.assertEqual(len(room["participants"]), 1)
        self.assertEqual(room["participants"][0]["role"], "HOST")
        self.assertTrue(room["webrtc_session_token"].startswith("wrtc_sig_"))
        self.assertFalse(room["pomodoro_state"]["is_running"])

    def test_create_private_room_validation(self):
        # Missing or short passcode should raise ValueError
        with self.assertRaises(ValueError):
            self.service.create_study_room(
                title="Private Elite Group",
                host_id="student-hassan",
                host_name="Hassan Mahmud",
                topic="Chemistry",
                target_grade="HSC-2026",
                is_private=True,
                passcode="12"  # too short
            )

    def test_list_active_study_rooms(self):
        rooms = self.service.list_active_study_rooms(topic="Mathematics")
        self.assertGreaterEqual(len(rooms), 1)
        self.assertEqual(rooms[0]["topic"], "Higher Mathematics")
        self.assertIn("webrtc_session_token", self.service._rooms[rooms[0]["room_id"]])
        # Public listing masks internal passcode
        self.assertNotIn("passcode", rooms[0])

    def test_join_room_and_capacity_limits(self):
        # Create small capacity room
        room = self.service.create_study_room(
            title="Pair Study",
            host_id="host-01",
            host_name="Host One",
            topic="English",
            target_grade="SSC-2026",
            max_participants=2
        )
        room_id = room["room_id"]

        # Join 2nd participant
        join_res = self.service.join_study_room(
            room_id=room_id,
            user_id="user-02",
            user_name="User Two",
            role="PARTICIPANT"
        )
        self.assertEqual(join_res["current_participants"], 2)
        self.assertTrue(join_res["participant_token"].startswith("wrtc_sig_"))

        # 3rd participant should hit capacity limit
        with self.assertRaises(ValueError):
            self.service.join_study_room(
                room_id=room_id,
                user_id="user-03",
                user_name="User Three",
                role="PARTICIPANT"
            )

    def test_join_private_room_passcode(self):
        room = self.service.create_study_room(
            title="Olympiad Secret Study",
            host_id="host-olympiad",
            host_name="Olympiad Host",
            topic="Combinatorics",
            target_grade="Olympiad",
            is_private=True,
            passcode="IMO-PASS-2026"
        )
        room_id = room["room_id"]

        # Wrong passcode
        with self.assertRaises(PermissionError):
            self.service.join_study_room(
                room_id=room_id,
                user_id="student-guest",
                user_name="Guest Student",
                passcode="WRONG"
            )

        # Correct passcode
        res = self.service.join_study_room(
            room_id=room_id,
            user_id="student-guest",
            user_name="Guest Student",
            passcode="IMO-PASS-2026"
        )
        self.assertEqual(res["room_id"], room_id)

    def test_leave_study_room(self):
        room_id = "room-buet-math-01"
        leave_res = self.service.leave_study_room(room_id, "student-fahim-02")
        self.assertEqual(leave_res["status"], "LEFT")
        self.assertEqual(leave_res["remaining_participants"], 2)

    def test_sync_whiteboard_stroke_and_clear(self):
        room_id = "room-buet-math-01"
        # Participant strokes
        res = self.service.sync_whiteboard(
            room_id=room_id,
            user_id="student-tamim-buet",
            action="FORMULA",
            formula_latex=r"E = mc^2"
        )
        self.assertEqual(res["room_id"], room_id)
        self.assertEqual(res["stroke_entry"]["formula_latex"], r"E = mc^2")

        # Non-member stroke rejected
        with self.assertRaises(PermissionError):
            self.service.sync_whiteboard(
                room_id=room_id,
                user_id="intruder-999",
                action="STROKE"
            )

        # Clear board
        clear_res = self.service.sync_whiteboard(
            room_id=room_id,
            user_id="student-tamim-buet",
            action="CLEAR"
        )
        self.assertEqual(clear_res["action"], "CLEAR")
        self.assertEqual(clear_res["total_strokes"], 0)

    def test_observer_cannot_modify_whiteboard(self):
        room = self.service.create_study_room(
            title="Lecture Hall",
            host_id="prof-01",
            host_name="Prof Rahman",
            topic="Quantum Mechanics",
            target_grade="University"
        )
        room_id = room["room_id"]
        self.service.join_study_room(
            room_id=room_id,
            user_id="observer-student",
            user_name="Auditor Student",
            role="OBSERVER"
        )
        with self.assertRaises(PermissionError):
            self.service.sync_whiteboard(
                room_id=room_id,
                user_id="observer-student",
                action="STROKE",
                stroke_data={"tool": "pen"}
            )

    def test_formula_length_limit(self):
        room_id = "room-buet-math-01"
        huge_formula = r"\sum " * 500  # exceeds 2000 chars
        with self.assertRaises(ValueError):
            self.service.sync_whiteboard(
                room_id=room_id,
                user_id="student-tamim-buet",
                action="FORMULA",
                formula_latex=huge_formula
            )

    def test_sync_pomodoro_host_authority(self):
        room_id = "room-med-bio-02"
        # Host starts Pomodoro sprint
        res = self.service.sync_pomodoro(
            room_id=room_id,
            host_id="student-nusrat-med",
            duration_minutes=30,
            action="START"
        )
        self.assertTrue(res["pomodoro_state"]["is_running"])
        self.assertEqual(res["pomodoro_state"]["duration_minutes"], 30)

        # Non-host cannot alter sprint timer
        with self.assertRaises(PermissionError):
            self.service.sync_pomodoro(
                room_id=room_id,
                host_id="student-rafiq-03",  # participant, not host
                action="PAUSE"
            )


class TestBountyTribunalService(unittest.TestCase):
    """Unit tests verifying gamified peer bounty tribunal, anti-collusion & payout ledger."""

    def setUp(self):
        self.service = BountyTribunalService()

    def test_create_bounty_success(self):
        bounty = self.service.create_bounty(
            poster_id="student-karim",
            poster_name="Karim Ullah",
            title="Complex numbers loci in Argand plane",
            subject="Higher Mathematics",
            problem_statement="Show that |z - 1| / |z + 1| = 2 represents an Apollonian circle.",
            bounty_bdt=250.0,
            bounty_reputation_pts=60
        )
        self.assertTrue(bounty["bounty_id"].startswith("bnty-"))
        self.assertEqual(bounty["status"], "OPEN")
        self.assertEqual(bounty["bounty_bdt"], 250.0)
        self.assertEqual(bounty["bounty_reputation_pts"], 60)

    def test_create_bounty_validation_errors(self):
        with self.assertRaises(ValueError):
            self.service.create_bounty(
                poster_id="student-karim",
                poster_name="Karim Ullah",
                title="",
                subject="Math",
                problem_statement="Problem text",
                bounty_bdt=100.0
            )

        with self.assertRaises(ValueError):
            self.service.create_bounty(
                poster_id="student-karim",
                poster_name="Karim Ullah",
                title="Valid Title",
                subject="Math",
                problem_statement="Problem text",
                bounty_bdt=-50.0  # negative amount
            )

    def test_anti_self_awarding_rule(self):
        # Poster cannot submit solution to own bounty
        with self.assertRaises(PermissionError):
            self.service.submit_solution(
                bounty_id="bnty-math-buet-01",
                scholar_id="student-fahim-02",  # Poster of this seed bounty
                scholar_name="Fahim Hasan",
                explanation="Attempting to self-solve to extract bounty funds."
            )

    def test_submit_solution_success(self):
        res = self.service.submit_solution(
            bounty_id="bnty-phy-hsc-02",
            scholar_id="student-solver-01",
            scholar_name="Solver Scholar",
            explanation="Transforming the wave 4-vector K^mu through boost Lambda gives Doppler shift.",
            latex_proof=r"\omega' = \gamma \omega (1 - \beta \cos \theta)"
        )
        self.assertEqual(res["status"], "PENDING_REVIEW")
        self.assertTrue(res["solution_id"].startswith("sol-"))

    def test_duplicate_pending_solution_rejected(self):
        # First submission
        self.service.submit_solution(
            bounty_id="bnty-phy-hsc-02",
            scholar_id="student-solver-dup",
            scholar_name="Dup Scholar",
            explanation="First valid submission."
        )
        # Duplicate pending submission from same scholar
        with self.assertRaises(ValueError):
            self.service.submit_solution(
                bounty_id="bnty-phy-hsc-02",
                scholar_id="student-solver-dup",
                scholar_name="Dup Scholar",
                explanation="Second duplicate submission while first is pending."
            )

    def test_evaluate_solution_accept_and_receipt(self):
        bounty_id = "bnty-math-buet-01"
        solution_id = "sol-001"

        # Poster evaluates and accepts solution
        eval_res = self.service.evaluate_solution(
            bounty_id=bounty_id,
            solution_id=solution_id,
            evaluator_id="student-fahim-02",  # original poster
            decision="ACCEPT",
            feedback="Flawless mathematical rigor!"
        )
        self.assertEqual(eval_res["status"], "AWARDED")
        self.assertEqual(eval_res["decision"], "ACCEPTED")
        self.assertEqual(eval_res["awarded_to"]["scholar_id"], "student-tamim-buet")
        self.assertEqual(eval_res["awarded_to"]["bdt_awarded"], 500.0)

        # Cryptographic payout receipt
        receipt = eval_res["receipt"]
        self.assertTrue(receipt["receipt_id"].startswith("rcpt-"))
        self.assertEqual(len(receipt["cryptographic_hash"]), 64)

    def test_double_award_defense(self):
        bounty_id = "bnty-math-buet-01"
        solution_id = "sol-001"

        # First award succeeds
        self.service.evaluate_solution(
            bounty_id=bounty_id,
            solution_id=solution_id,
            evaluator_id="student-fahim-02",
            decision="ACCEPT"
        )

        # Second award on the same bounty must fail
        with self.assertRaises(ValueError):
            self.service.evaluate_solution(
                bounty_id=bounty_id,
                solution_id=solution_id,
                evaluator_id="student-fahim-02",
                decision="ACCEPT"
            )

    def test_unauthorized_evaluator_rejected(self):
        bounty_id = "bnty-math-buet-01"
        solution_id = "sol-001"

        with self.assertRaises(PermissionError):
            self.service.evaluate_solution(
                bounty_id=bounty_id,
                solution_id=solution_id,
                evaluator_id="random-unauthorized-student",
                decision="ACCEPT"
            )


class TestPhase27RestEndpoints(unittest.IsolatedAsyncioTestCase):
    """Integration tests verifying Section 26 REST API routing in router.py."""

    async def test_create_and_list_study_rooms_endpoint(self):
        from backend.app.api.v1.router import create_study_room, list_study_rooms

        req = CreateStudyRoomRequest(
            title="Medical Rapid MCQs",
            host_id="student-dr-01",
            host_name="Dr Aspirant",
            topic="Human Anatomy",
            target_grade="Admission-Medical",
            max_participants=6
        )
        res = await create_study_room(req)
        self.assertEqual(res["title"], "Medical Rapid MCQs")

        rooms = await list_study_rooms(topic="Anatomy")
        self.assertGreaterEqual(len(rooms), 1)

    async def test_bounties_create_and_submit_solution_endpoint(self):
        from backend.app.api.v1.router import (
            create_bounty,
            submit_bounty_solution,
            evaluate_bounty_solution
        )

        bounty_req = CreateBountyRequest(
            poster_id="student-asker-01",
            poster_name="Asker One",
            title="Thermodynamics Carnot Cycle Efficiency",
            subject="Physics",
            problem_statement="Derive efficiency eta = 1 - T_C / T_H using entropy integral.",
            bounty_bdt=300.0,
            bounty_reputation_pts=80
        )
        bounty = await create_bounty(bounty_req)
        bounty_id = bounty["bounty_id"]

        sol_req = SubmitSolutionRequest(
            bounty_id=bounty_id,
            scholar_id="student-solver-99",
            scholar_name="Solver Ninety-Nine",
            explanation="Along reversible adiabatic legs dS=0, along isothermal legs Q/T is constant.",
            latex_proof=r"\eta = 1 - \frac{T_C}{T_H}"
        )
        sol = await submit_bounty_solution(sol_req)
        solution_id = sol["solution_id"]

        verdict_req = VerdictBountyRequest(
            bounty_id=bounty_id,
            evaluator_id="student-asker-01",
            decision="ACCEPT",
            feedback="Accurate entropy derivation!"
        )
        verdict = await evaluate_bounty_solution(solution_id=solution_id, payload=verdict_req)
        self.assertEqual(verdict["decision"], "ACCEPTED")
        self.assertEqual(verdict["status"], "AWARDED")


if __name__ == "__main__":
    unittest.main()
