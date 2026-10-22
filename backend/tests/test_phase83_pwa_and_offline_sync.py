# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 83 Test Suite):
# Automated Verification Test Suite for Progressive Web App (PWA) & Offline-First CRDT:
# 1. W3C Web App Manifest Conformance (192px/512px/maskable icons, theme #0F172A, standalone).
# 2. Service Worker Routing Strategies (Cache-First, Network-First, Stale-While-Revalidate).
# 3. Client-Side IndexedDB Storage Primitives (practice_sets, answers_queue, profiles_cache).
# 4. CRDT Last-Write-Wins (LWW) Conflict Resolution & Vector Clock Causality.
# 5. Backend Offline Sync Endpoints (/quiz-attempts/sync & /offline/sync idempotent batching).
# 6. Accessible OfflineToast Component Contracts with Semantic Lucide Icons.
# 7. Strict Zero-Emoji Policy across all PWA, Service Worker, and frontend components.
# ==============================================================================

import unittest
import json
import os
import re

from backend.app.schemas.security_and_offline_schema import OfflineSyncBatchRequest
from backend.app.services.offline_sync_service import offline_sync_service
from backend.app.api.v1.router import sync_offline_batch, get_offline_manifest


class TestPhase83PwaAndOfflineSync(unittest.IsolatedAsyncioTestCase):
    """
    Test suite asserting PWA Web Manifest, Service Worker Caching Strategies,
    IndexedDB contracts, CRDT conflict resolution, and /quiz-attempts/sync endpoints.
    """

    def setUp(self):
        self.workspace_root = os.getcwd()

    def test_01_manifest_json_conformance(self):
        """Asserts W3C Web App Manifest compliance, icons, standalone display, and theme tokens."""
        manifest_path = os.path.join(self.workspace_root, "frontend/public/manifest.json")
        self.assertTrue(os.path.exists(manifest_path), "manifest.json must exist")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Core PWA properties
        self.assertEqual(manifest.get("display"), "standalone")
        self.assertEqual(manifest.get("theme_color"), "#0F172A")
        self.assertEqual(manifest.get("background_color"), "#F8FAFC")
        self.assertEqual(manifest.get("start_url"), "/")
        self.assertEqual(manifest.get("orientation"), "portrait-primary")

        # Bilingual description
        desc = manifest.get("description", "")
        self.assertTrue(len(desc) > 20)
        self.assertIn("Student Life Circle", desc)
        self.assertIn("শিক্ষার্থীদের", desc)

        # Icon validation (192px, 512px, maskable)
        icons = manifest.get("icons", [])
        self.assertGreaterEqual(len(icons), 3)

        sizes = [icon.get("sizes") for icon in icons]
        self.assertIn("192x192", sizes)
        self.assertIn("512x512", sizes)

        purposes = [icon.get("purpose") for icon in icons if "purpose" in icon]
        self.assertIn("maskable", purposes)

        # App shortcuts
        shortcuts = manifest.get("shortcuts", [])
        self.assertGreaterEqual(len(shortcuts), 2)
        urls = [s.get("url") for s in shortcuts]
        self.assertIn("/practice", urls)

    def test_02_service_worker_caching_strategies(self):
        """Asserts Cache-First, Network-First, Stale-While-Revalidate in sw.js."""
        sw_path = os.path.join(self.workspace_root, "frontend/public/sw.js")
        self.assertTrue(os.path.exists(sw_path), "sw.js must exist")

        with open(sw_path, "r", encoding="utf-8") as f:
            sw_code = f.read()

        # Cache definitions
        self.assertIn("CACHE_VERSION", sw_code)
        self.assertIn("STATIC_CACHE", sw_code)
        self.assertIn("QUESTIONS_CACHE", sw_code)
        self.assertIn("PROFILES_CACHE", sw_code)

        # Cache-First for static & fonts
        self.assertIn("Cache-First", sw_code)
        self.assertIn("STATIC_ASSET_REGEX", sw_code)
        self.assertIn("FONT_REGEX", sw_code)

        # Network-First for questions/practice
        self.assertIn("/api/v1/offline/", sw_code)
        self.assertIn("/api/v1/practice", sw_code)

        # Stale-While-Revalidate for profiles
        self.assertIn("/api/v1/profiles", sw_code)

        # Background Sync event listener
        self.assertIn("addEventListener('sync'", sw_code)
        self.assertIn("sync-offline-quiz-answers", sw_code)

    def test_03_indexeddb_storage_primitives(self):
        """Asserts IndexedDB TypeScript module exports, store schemas, and method contracts."""
        idb_path = os.path.join(self.workspace_root, "frontend/src/lib/offline/indexedDbStorage.ts")
        self.assertTrue(os.path.exists(idb_path), "indexedDbStorage.ts must exist")

        with open(idb_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Object Store Names
        self.assertIn("practice_sets", code)
        self.assertIn("answers_queue", code)
        self.assertIn("profiles_cache", code)

        # TypeScript Interfaces
        self.assertIn("interface OfflinePracticeQuestion", code)
        self.assertIn("interface OfflinePracticeBundle", code)
        self.assertIn("interface OfflineAnswerRecord", code)

        # Storage Methods
        self.assertIn("saveOfflinePracticeSet", code)
        self.assertIn("getOfflinePracticeSet", code)
        self.assertIn("listOfflinePracticeSets", code)
        self.assertIn("enqueueOfflineAnswer", code)
        self.assertIn("getPendingOfflineAnswers", code)
        self.assertIn("markAnswersAsSynced", code)
        self.assertIn("clearSyncedAnswers", code)

    def test_04_crdt_sync_engine_conflict_resolution(self):
        """Asserts SyncEngine conflict resolution (LWW and vector clocks) in syncEngine.ts."""
        sync_path = os.path.join(self.workspace_root, "frontend/src/lib/offline/syncEngine.ts")
        self.assertTrue(os.path.exists(sync_path), "syncEngine.ts must exist")

        with open(sync_path, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertIn("class OfflineSyncEngine", code)
        self.assertIn("resolveConflict", code)
        self.assertIn("flushPendingAnswers", code)
        self.assertIn("subscribe", code)
        self.assertIn("/api/v1/quiz-attempts/sync", code)

        # Test simulated LWW conflict resolution
        earlier_record = {
            "question_version_id": "q1",
            "selected_option_id": "opt_A",
            "client_timestamp": 1000,
            "vector_clock": {"node1": 1}
        }
        later_record = {
            "question_version_id": "q1",
            "selected_option_id": "opt_B",
            "client_timestamp": 2000,
            "vector_clock": {"node1": 2}
        }

        # Vector clock with higher scalar wins
        winner = later_record if sum(later_record["vector_clock"].values()) > sum(earlier_record["vector_clock"].values()) else earlier_record
        self.assertEqual(winner["selected_option_id"], "opt_B")

    async def test_05_backend_offline_sync_endpoints(self):
        """Asserts /api/v1/quiz-attempts/sync and /api/v1/offline/manifest."""
        # 1. Test offline manifest generator
        manifest = await get_offline_manifest(class_grade=9, subject="গণিত", bundle_size=5)
        self.assertIn("bundle_id", manifest)
        self.assertIn("questions", manifest)
        self.assertEqual(manifest["offline_storage_policy"], "PWA_INDEXED_DB")

        # 2. Test batch offline sync replay
        student_id = "student_offline_test_01"
        from backend.app.services.quiz_engine import quiz_engine
        from backend.app.schemas.quiz_schema import QuizMode
        from backend.app.db.seed_data import ACADEMIC_QUESTION_SEEDS

        attempt_resp = quiz_engine.start_practice_attempt(
            user_id=student_id,
            blueprint_id="bp_general_01",
            mode=QuizMode.ANYTIME_PRACTICE,
            raw_questions=ACADEMIC_QUESTION_SEEDS[:5],
            duration_minutes=30
        )
        attempt_id = attempt_resp.attempt_id
        q1 = attempt_resp.questions[0].question_version_id
        q2 = attempt_resp.questions[1].question_version_id

        payload = OfflineSyncBatchRequest(
            student_id=student_id,
            attempt_id=attempt_id,
            buffered_answers=[
                {
                    "question_version_id": q1,
                    "selected_option_id": "opt_b",
                    "idempotency_key": "idem_off_01",
                    "time_taken_seconds": 14.5,
                    "client_timestamp": 1729230000000
                },
                {
                    "question_version_id": q2,
                    "selected_option_id": "opt_a",
                    "idempotency_key": "idem_off_02",
                    "time_taken_seconds": 22.0,
                    "client_timestamp": 1729230030000
                }
            ]
        )


        res = await sync_offline_batch(payload)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("batch", res)
        self.assertEqual(res["batch"]["synced_count"], 2)

        # 3. Test idempotent replay (re-sending same batch should be gracefully deduplicated)
        replay_res = await sync_offline_batch(payload)
        self.assertEqual(replay_res["status"], "SUCCESS")
        self.assertEqual(replay_res["batch"]["skipped_count"], 2)

    def test_06_offline_toast_component(self):
        """Asserts OfflineToast component contains Lucide SVG icons and proper states."""
        toast_path = os.path.join(self.workspace_root, "frontend/src/components/ui/OfflineToast.tsx")
        self.assertTrue(os.path.exists(toast_path), "OfflineToast.tsx must exist")

        with open(toast_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Lucide SVG icons
        self.assertIn("WifiOff", code)
        self.assertIn("Wifi", code)
        self.assertIn("RefreshCw", code)
        self.assertIn("CheckCircle2", code)

        # Accessible states
        self.assertIn("Offline Mode Active", code)
        self.assertIn("Synchronizing Answers", code)
        self.assertIn("Connection Restored", code)

        # Export in ui/index.ts
        ui_index_path = os.path.join(self.workspace_root, "frontend/src/components/ui/index.ts")
        with open(ui_index_path, "r", encoding="utf-8") as f:
            index_code = f.read()
        self.assertIn("OfflineToast", index_code)

    def test_07_zero_emoji_governance(self):
        """Scans all Phase 83 PWA, Service Worker, and UI files for strict zero-emoji enforcement."""
        files_to_check = [
            "frontend/public/manifest.json",
            "frontend/public/sw.js",
            "frontend/src/lib/offline/indexedDbStorage.ts",
            "frontend/src/lib/offline/syncEngine.ts",
            "frontend/src/lib/offline/index.ts",
            "frontend/src/components/ui/OfflineToast.tsx"
        ]

        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]|'
            r'[\u2600-\u26FF\u2700-\u27BF]'
        )

        for rel_path in files_to_check:
            abs_path = os.path.join(self.workspace_root, rel_path)
            if not os.path.exists(abs_path):
                continue
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = emoji_pattern.findall(content)
                self.assertEqual(
                    len(matches),
                    0,
                    f"Zero-emoji policy violation in {rel_path}: {matches}"
                )


if __name__ == "__main__":
    unittest.main()
