"""
DEVELOPER ARCHITECTURE NOTE - TEST SUITE:
Phase 77: Next.js 15+ Global State Management & Core Pages Wiring Verification
Validates 10 core architectural and integration requirements:
1. Centralized API Client Architecture: NEXT_PUBLIC_API_URL, UUID v4 Idempotency, 401/403/429 Interceptors
2. Offline Queue Resiliency: Local storage buffer, network status 0 fallback, auto-replay on reconnect
3. Zustand Authentication Store (useAuthStore): RBAC roles, minor protection protocol, privacy matrix
4. Zustand Quiz & Assessment Store (useQuizStore): Server-authoritative countdown sync, answers buffer
5. Zustand Taxonomy & Filter Store (useFilterStore): Curriculum levels (SSC/HSC/Admission), regional division
6. Practice Page Wiring (practice.tsx): /api/v1/practice/sets, useQuizStore, skeleton loader (CLS < 0.1)
7. Live Challenge Page Wiring (live-challenge.tsx): /api/v1/live-challenges, pseudonymous handles, opt-out
8. Admission Hub Page Wiring (admission.tsx): /api/v1/admission, unit selectors, negative-marking mocks
9. Tuition & Career Pages Wiring (tuition.tsx & career.tsx): Bilateral consent modal, immutable CV snapshots
10. Strict Zero-Emoji & Developer Note Governance: Complete unicode scan asserting 0 emojis and required notes
"""

import os
import re
import unittest


class TestPhase77GlobalStateAndPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        cls.frontend_dir = os.path.join(cls.base_dir, 'frontend')
        cls.lib_dir = os.path.join(cls.frontend_dir, 'src/lib')
        cls.store_dir = os.path.join(cls.frontend_dir, 'src/store')
        cls.pages_dir = os.path.join(cls.frontend_dir, 'src/pages')

    def test_api_client_architecture(self):
        """Verify centralized API client implements UUID v4 idempotency, headers, and error interceptors."""
        client_path = os.path.join(self.lib_dir, 'api-client.ts')
        self.assertTrue(os.path.exists(client_path), "api-client.ts must exist.")

        with open(client_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Config & UUID v4
        self.assertIn("NEXT_PUBLIC_API_URL", content, "NEXT_PUBLIC_API_URL must be configured.")
        self.assertIn("generateUUID", content, "UUID v4 generator must be defined.")
        self.assertIn("X-Idempotency-Key", content, "X-Idempotency-Key header must be attached.")

        # Interceptors
        self.assertIn("response.status === 401", content, "401 unauthorized interceptor must exist.")
        self.assertIn("response.status === 403", content, "403 forbidden interceptor must exist.")
        self.assertIn("response.status === 429", content, "429 rate-limit interceptor must exist.")
        self.assertIn("Retry-After", content, "Retry-After header parsing must be supported.")

        # Token handling
        self.assertIn("Bearer", content, "Authorization Bearer token injection must exist.")
        self.assertIn("setToken", content, "setToken method must be exposed.")

    def test_offline_queue_resiliency(self):
        """Verify offline queue buffering, localStorage persistence, and auto-replay logic."""
        client_path = os.path.join(self.lib_dir, 'api-client.ts')
        with open(client_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("OfflineAnswerItem", content, "OfflineAnswerItem interface must be defined.")
        self.assertIn("getOfflineQueue", content, "getOfflineQueue helper must be defined.")
        self.assertIn("saveOfflineQueue", content, "saveOfflineQueue helper must be defined.")
        self.assertIn("replayPendingAnswers", content, "replayPendingAnswers method must be implemented.")
        self.assertIn("window.addEventListener('online'", content, "Online event listener must auto-replay.")

    def test_use_auth_store(self):
        """Verify useAuthStore manages roles, token sync, and child minor-protection protocol."""
        store_path = os.path.join(self.store_dir, 'useAuthStore.ts')
        self.assertTrue(os.path.exists(store_path), "useAuthStore.ts must exist.")

        with open(store_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("useAuthStore", content, "useAuthStore must be defined.")
        self.assertIn("'student' | 'guardian' | 'teacher' | 'admin'", content, "All RBAC roles must be supported.")
        self.assertIn("isMinorProtected", content, "Minor protection flag must exist.")
        self.assertIn("privacySettings", content, "Privacy settings interface must exist.")
        self.assertIn("apiClient.setToken", content, "Store must synchronize token with apiClient.")
        self.assertIn("isUserMinor", content, "Under-18 age detector for minor protection must exist.")

    def test_use_quiz_store(self):
        """Verify useQuizStore implements server-authoritative timer and answer buffering."""
        store_path = os.path.join(self.store_dir, 'useQuizStore.ts')
        self.assertTrue(os.path.exists(store_path), "useQuizStore.ts must exist.")

        with open(store_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("useQuizStore", content, "useQuizStore must be defined.")
        self.assertIn("activeQuestionIndex", content, "activeQuestionIndex must be tracked.")
        self.assertIn("answers", content, "Answers buffer must be maintained.")
        self.assertIn("timeRemainingSeconds", content, "Countdown timer must be maintained.")
        self.assertIn("syncServerTimer", content, "Server-authoritative timer sync method must exist.")
        self.assertIn("decrementTimer", content, "Timer decrement method must exist.")
        self.assertIn("offlinePendingCount", content, "Offline pending queue count must be tracked.")

    def test_use_filter_store(self):
        """Verify useFilterStore manages curriculum levels and search parameters."""
        store_path = os.path.join(self.store_dir, 'useFilterStore.ts')
        self.assertTrue(os.path.exists(store_path), "useFilterStore.ts must exist.")

        with open(store_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("useFilterStore", content, "useFilterStore must be defined.")
        self.assertIn("'ALL' | 'SSC' | 'HSC' | 'ADMISSION'", content, "Curriculum levels must match NCTB hierarchy.")
        self.assertIn("searchQuery", content, "Global search query must be supported.")
        self.assertIn("division", content, "Division filter must be supported.")
        self.assertIn("resetFilters", content, "resetFilters action must exist.")

    def test_practice_page_wiring(self):
        """Verify practice.tsx wires useQuizStore, apiClient, and skeleton loading state."""
        page_path = os.path.join(self.pages_dir, 'practice.tsx')
        self.assertTrue(os.path.exists(page_path), "practice.tsx must exist.")

        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("apiClient.getPracticeSets", content, "practice.tsx must call apiClient.getPracticeSets.")
        self.assertIn("useQuizStore", content, "practice.tsx must use useQuizStore.")
        self.assertIn("useFilterStore", content, "practice.tsx must use useFilterStore.")
        self.assertIn("animate-pulse", content, "practice.tsx must provide skeleton loading state.")
        self.assertIn("formatTimer", content, "Countdown timer must be formatted.")
        self.assertIn("WifiOff", content, "Offline indicator icon must be handled.")

    def test_live_challenge_page_wiring(self):
        """Verify live-challenge.tsx connects to live endpoints with pseudonymous privacy."""
        page_path = os.path.join(self.pages_dir, 'live-challenge.tsx')
        self.assertTrue(os.path.exists(page_path), "live-challenge.tsx must exist.")

        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("apiClient.getLiveChallenges", content, "live-challenge.tsx must call getLiveChallenges.")
        self.assertIn("apiClient.getLiveLeaderboard", content, "live-challenge.tsx must call getLiveLeaderboard.")
        self.assertIn("optOutRanking", content, "Mental health opt-out toggle must exist.")
        self.assertIn("useAuthStore", content, "live-challenge.tsx must use useAuthStore.")
        self.assertIn("animate-pulse", content, "live-challenge.tsx must provide skeleton loading state.")

    def test_admission_page_wiring(self):
        """Verify admission.tsx connects to admission tests and negative marking blueprints."""
        page_path = os.path.join(self.pages_dir, 'admission.tsx')
        self.assertTrue(os.path.exists(page_path), "admission.tsx must exist.")

        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("apiClient.getAdmissionTests", content, "admission.tsx must call getAdmissionTests.")
        self.assertIn("useFilterStore", content, "admission.tsx must use useFilterStore.")
        self.assertIn("negativeMarking", content, "Negative marking blueprint details must be displayed.")
        self.assertIn("animate-pulse", content, "admission.tsx must provide skeleton loading state.")

    def test_tuition_and_career_pages_wiring(self):
        """Verify tuition.tsx and career.tsx wire bilateral consent and immutable CV snapshots."""
        tuition_path = os.path.join(self.pages_dir, 'tuition.tsx')
        career_path = os.path.join(self.pages_dir, 'career.tsx')

        self.assertTrue(os.path.exists(tuition_path), "tuition.tsx must exist.")
        self.assertTrue(os.path.exists(career_path), "career.tsx must exist.")

        with open(tuition_path, 'r', encoding='utf-8') as f:
            t_content = f.read()
        self.assertIn("apiClient.getTuitions", t_content, "tuition.tsx must call getTuitions.")
        self.assertIn("requestTuitionConsent", t_content, "tuition.tsx must call requestTuitionConsent.")
        self.assertIn("Modal", t_content, "tuition.tsx must use Radix Modal wrapper.")
        self.assertIn("animate-pulse", t_content, "tuition.tsx must provide skeleton loading state.")

        with open(career_path, 'r', encoding='utf-8') as f:
            c_content = f.read()
        self.assertIn("apiClient.getCareerProfile", c_content, "career.tsx must call getCareerProfile.")
        self.assertIn("cvSnapshotId", c_content, "career.tsx must display immutable CV snapshot hashes.")
        self.assertIn("animate-pulse", c_content, "career.tsx must provide skeleton loading state.")

    def test_developer_notes_and_zero_emoji_governance(self):
        """Verify every created/updated file has a Developer Architecture Note and 0 emojis."""
        files_to_check = [
            os.path.join(self.lib_dir, 'api-client.ts'),
            os.path.join(self.store_dir, 'createStore.ts'),
            os.path.join(self.store_dir, 'useAuthStore.ts'),
            os.path.join(self.store_dir, 'useQuizStore.ts'),
            os.path.join(self.store_dir, 'useFilterStore.ts'),
            os.path.join(self.store_dir, 'index.ts'),
            os.path.join(self.pages_dir, 'practice.tsx'),
            os.path.join(self.pages_dir, 'live-challenge.tsx'),
            os.path.join(self.pages_dir, 'admission.tsx'),
            os.path.join(self.pages_dir, 'tuition.tsx'),
            os.path.join(self.pages_dir, 'career.tsx'),
        ]

        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

        for filepath in files_to_check:
            self.assertTrue(os.path.exists(filepath), f"File {filepath} must exist.")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verify Developer Architecture Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content[:600],
                f"File {os.path.basename(filepath)} must start with a prominent DEVELOPER ARCHITECTURE NOTE."
            )

            # Verify Strict Zero-Emoji Policy
            matches = emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {os.path.basename(filepath)} contains forbidden emojis: {matches}"
            )


if __name__ == '__main__':
    unittest.main()
