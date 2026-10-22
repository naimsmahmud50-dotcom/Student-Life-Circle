"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Offline P2P Classroom Mesh & CRDT Sync
TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
FILE:      backend/tests/test_phase119_offline_crdt_sync.py
PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
PURPOSE:   Automated unit and integration test suite certifying Lamport logical clock
           monotonicity, Last-Write-Wins (LWW) conflict-free merge determinism,
           batch reconciliation idempotency, station health tracking, and zero-emoji compliance.
STANDARDS: OWASP ASVS L2, Distributed CRDT LWW Semantics, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import re
import unittest
from pathlib import Path

from backend.app.services.offline_crdt_sync_service import (
    OfflineCrdtSyncService,
    offline_crdt_sync_service,
    InvalidBatchPayloadException,
    StationNotFoundException,
)


class TestPhase119OfflineCrdtSync(unittest.TestCase):
    """
    Test suite certifying Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.service_file = cls.root_dir / "backend" / "app" / "services" / "offline_crdt_sync_service.py"
        cls.endpoints_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "offline_sync.py"
        cls.frontend_station = cls.root_dir / "frontend" / "src" / "components" / "offline-mesh" / "OfflineClassroomStation.tsx"
        cls.frontend_ledger = cls.root_dir / "frontend" / "src" / "lib" / "offline" / "crdtMutationLedger.ts"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def setUp(self):
        # Create a fresh isolated service instance for each test
        self.service = OfflineCrdtSyncService()

    def test_01_lamport_clock_ordering_and_monotonicity(self):
        """Verifies Lamport logical clock advancement and deterministic ordering."""
        station_id = "test-station-01"
        batch_id = "test-batch-01"

        mutations = [
            {
                "mutation_id": "mut-01",
                "client_id": "peer-std-01",
                "lamport_clock": 1,
                "mutation_type": "RECORD_ANSWER",
                "payload": {
                    "quiz_id": "quiz-math-01",
                    "student_id": "std-01",
                    "question_id": "q-1",
                    "option_id": "opt-A",
                },
            },
            {
                "mutation_id": "mut-02",
                "client_id": "peer-std-01",
                "lamport_clock": 3,
                "mutation_type": "RECORD_ANSWER",
                "payload": {
                    "quiz_id": "quiz-math-01",
                    "student_id": "std-01",
                    "question_id": "q-1",
                    "option_id": "opt-B",  # Newer answer with higher Lamport clock
                },
            },
        ]

        res = self.service.reconcile_batch(station_id, batch_id, mutations)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["applied_count"], 2)

        answers = self.service.get_student_quiz_answers("quiz-math-01", "std-01")
        # opt-B must win because lamport_clock 3 > 1
        self.assertEqual(answers.get("q-1"), "opt-B")

    def test_02_crdt_lww_conflict_resolution_and_tie_breaking(self):
        """Verifies Last-Write-Wins and deterministic tie-breaking on identical clocks."""
        station_id = "test-station-02"
        batch_id = "test-batch-02"

        # Two concurrent mutations with same clock 5; tie-break lexicographically by client_id
        mutations = [
            {
                "mutation_id": "mut-tie-a",
                "client_id": "peer-alpha",
                "lamport_clock": 5,
                "mutation_type": "RECORD_ANSWER",
                "payload": {
                    "quiz_id": "quiz-phys-01",
                    "student_id": "std-02",
                    "question_id": "q-2",
                    "option_id": "opt-ALPHA",
                },
            },
            {
                "mutation_id": "mut-tie-z",
                "client_id": "peer-zeta",  # "peer-zeta" > "peer-alpha"
                "lamport_clock": 5,
                "mutation_type": "RECORD_ANSWER",
                "payload": {
                    "quiz_id": "quiz-phys-01",
                    "student_id": "std-02",
                    "question_id": "q-2",
                    "option_id": "opt-ZETA",
                },
            },
        ]

        self.service.reconcile_batch(station_id, batch_id, mutations)
        answers = self.service.get_student_quiz_answers("quiz-phys-01", "std-02")
        self.assertEqual(answers.get("q-2"), "opt-ZETA")

    def test_03_batch_reconcile_idempotency_and_checksum_verification(self):
        """Verifies batch reconciliation idempotency and duplicate deduplication."""
        station_id = "test-station-03"
        batch_id = "test-batch-03"

        mutations = [
            {
                "mutation_id": f"mut-idemp-{i}",
                "client_id": f"peer-std-{i}",
                "lamport_clock": i,
                "mutation_type": "RECORD_ANSWER",
                "payload": {
                    "quiz_id": "quiz-chem-01",
                    "student_id": f"std-{i}",
                    "question_id": "q-1",
                    "option_id": "opt-A",
                },
            }
            for i in range(1, 6)
        ]

        # First ingestion
        res1 = self.service.reconcile_batch(station_id, batch_id, mutations, checksum="chk-abc")
        self.assertEqual(res1["applied_count"], 5)
        self.assertEqual(res1["duplicate_count"], 0)

        # Second ingestion with exact same batch: 0 applied, 5 duplicates
        res2 = self.service.reconcile_batch(station_id, batch_id, mutations, checksum="chk-abc")
        self.assertEqual(res2["applied_count"], 0)
        self.assertEqual(res2["duplicate_count"], 5)

        # Missing required station_id or batch_id raises InvalidBatchPayloadException
        with self.assertRaises(InvalidBatchPayloadException):
            self.service.reconcile_batch("", "batch-x", [])

        # Audit trail must record both batches
        audit = self.service.get_sync_audit_trail()
        self.assertEqual(len(audit), 2)
        self.assertEqual(audit[0]["checksum"], "chk-abc")

    def test_04_station_status_tracking_and_querying(self):
        """Verifies station status tracking, batch counting, and unknown station handling."""
        station_id = "station-char-99"
        self.service.reconcile_batch(
            station_id=station_id,
            batch_id="batch-char-99",
            mutations=[
                {
                    "mutation_id": "mut-st-1",
                    "client_id": "peer-01",
                    "lamport_clock": 1,
                    "mutation_type": "RECORD_ANSWER",
                    "payload": {"quiz_id": "q1", "student_id": "s1", "question_id": "q1", "option_id": "o1"},
                }
            ],
        )

        status = self.service.get_station_status(station_id)
        self.assertEqual(status["station_id"], station_id)
        self.assertEqual(status["total_mutations_applied"], 1)
        self.assertEqual(status["total_batches_processed"], 1)
        self.assertEqual(status["status"], "HEALTHY")

        with self.assertRaises(StationNotFoundException):
            self.service.get_station_status("non-existent-station")

    def test_05_frontend_component_architecture_and_tactile_styling(self):
        """Verifies frontend components adhere to high-contrast utilitarian design and 3D buttons."""
        self.assertTrue(self.frontend_station.exists(), "OfflineClassroomStation.tsx must exist.")
        self.assertTrue(self.frontend_ledger.exists(), "crdtMutationLedger.ts must exist.")

        station_content = self.frontend_station.read_text(encoding="utf-8")
        ledger_content = self.frontend_ledger.read_text(encoding="utf-8")

        # 1. Tactile 3D Oxford Navy buttons
        self.assertIn("shadow-[0_4px_0_0_#061727]", station_content)
        self.assertIn("active:translate-y-1", station_content)
        self.assertIn("active:shadow-none", station_content)
        self.assertIn("bg-[#0A2540]", station_content)
        self.assertIn("লোকাল কুইজ শুরু করুন", station_content)
        self.assertIn("ক্লাউডে সিঙ্ক করুন", station_content)

        # 2. Pure Lucide vector icons
        self.assertIn("WifiOff", station_content)
        self.assertIn("Share2", station_content)
        self.assertIn("RefreshCw", station_content)
        self.assertIn("CheckCircle", station_content)
        self.assertIn("Database", station_content)
        self.assertIn("Users", station_content)

        # 3. CRDT Ledger exports and methods
        self.assertIn("CrdtMutationLedger", ledger_content)
        self.assertIn("advanceClock", ledger_content)
        self.assertIn("mergeRemoteMutations", ledger_content)
        self.assertIn("exportBatchPayload", ledger_content)

    def test_06_architecture_notes_and_zero_emoji_enforcement(self):
        """Verifies Developer Architecture Notes and strict zero-emoji enforcement across all Phase 119 files."""
        files_to_check = [
            self.service_file,
            self.endpoints_file,
            self.frontend_station,
            self.frontend_ledger,
            Path(__file__),
        ]

        for file_path in files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist.")
            content = file_path.read_text(encoding="utf-8")

            # Assert Developer Architecture Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"File {file_path.name} is missing standardized DEVELOPER ARCHITECTURE NOTE.",
            )

            # Assert zero emojis
            emoji_matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(emoji_matches),
                0,
                f"File {file_path.name} contains emoji violations: {emoji_matches}",
            )


if __name__ == "__main__":
    unittest.main()
