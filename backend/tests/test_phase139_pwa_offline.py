"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      backend/tests/test_phase139_pwa_offline.py
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file existence
 *            2. Strict Zero-Emoji compliance across all Phase 139 files
 *            3. Web App Manifest (manifest.json) validation (standalone, theme colors, icons)
 *            4. Multi-tier Workbox-grade Service Worker caching and /offline navigation fallback
 *            5. IndexedDB Board Papers Vault (offline-papers-store.ts) API integrity
 *            6. PWA UI components (PwaUpdateToast, PwaInstallBanner, OfflineIndicator)
 *            7. Elevated /offline study arena page with search and KaTeX solutions
 *            8. Root application integration in _app.tsx and _document.tsx
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */
"""

import json
import os
import re
import unittest
from pathlib import Path

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestPhase139PwaOffline(unittest.TestCase):
    """
    Automated verification suite for Phase 139 PWA, Offline Experience & Mobile Optimization.
    """

    @classmethod
    def setUpClass(cls):
        cls.phase139_files = [
            REPO_ROOT / "frontend/public/manifest.json",
            REPO_ROOT / "frontend/public/sw.js",
            REPO_ROOT / "frontend/src/lib/offline/offline-papers-store.ts",
            REPO_ROOT / "frontend/src/lib/offline/index.ts",
            REPO_ROOT / "frontend/src/components/pwa/PwaUpdateToast.tsx",
            REPO_ROOT / "frontend/src/components/pwa/PwaInstallBanner.tsx",
            REPO_ROOT / "frontend/src/components/pwa/OfflineIndicator.tsx",
            REPO_ROOT / "frontend/src/components/pwa/index.ts",
            REPO_ROOT / "frontend/src/pages/offline.tsx",
            REPO_ROOT / "frontend/src/pages/_app.tsx",
            REPO_ROOT / "frontend/src/pages/_document.tsx",
        ]

    def test_01_all_phase139_files_exist(self):
        """Verify that every Phase 139 component, library, and page file exists."""
        for file_path in self.phase139_files:
            self.assertTrue(
                file_path.exists(),
                f"Required Phase 139 file missing: {file_path}"
            )

    def test_02_strict_zero_emoji_compliance(self):
        """Enforce strict Zero-Emoji policy across all Phase 139 files."""
        violations = []
        for file_path in self.phase139_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            if matches:
                violations.append(f"{file_path.name}: found emojis {matches}")

        self.assertEqual(
            len(violations),
            0,
            f"Zero-Emoji policy violations found:\n" + "\n".join(violations),
        )

    def test_03_developer_architecture_note_headers(self):
        """Ensure standard Developer Architecture Note header is present on code files."""
        code_files = [
            f for f in self.phase139_files
            if f.suffix in [".ts", ".tsx", ".js"]
        ]
        for file_path in code_files:
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note in {file_path.name}",
            )
            self.assertIn(
                "Phase 139 - PWA, Offline Experience & Mobile Optimization",
                content,
                f"Incorrect or missing Phase 139 phase declaration in {file_path.name}",
            )

    def test_04_manifest_json_validity(self):
        """Verify Web App Manifest is valid JSON with Oxford Dark theme and required icons."""
        manifest_path = REPO_ROOT / "frontend/public/manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("display"), "standalone")
        self.assertEqual(data.get("background_color"), "#F8FAFC")
        self.assertEqual(data.get("theme_color"), "#0F172A")
        self.assertEqual(data.get("start_url"), "/")

        # Icons inspection
        icons = data.get("icons", [])
        sizes = [icon.get("sizes") for icon in icons]
        self.assertIn("192x192", sizes, "Missing 192x192 icon in manifest")
        self.assertIn("512x512", sizes, "Missing 512x512 icon in manifest")

        # Maskable icon check
        purposes = [icon.get("purpose") for icon in icons]
        self.assertIn("maskable", purposes, "Missing maskable icon in manifest")

        # Shortcuts check
        shortcuts = data.get("shortcuts", [])
        shortcut_urls = [s.get("url") for s in shortcuts]
        self.assertIn("/offline", shortcut_urls, "Missing /offline shortcut in manifest")
        self.assertIn("/board-archives", shortcut_urls, "Missing /board-archives shortcut in manifest")

    def test_05_service_worker_caching_strategies(self):
        """Verify Service Worker implementation of multi-tier caching and offline fallback."""
        sw_path = REPO_ROOT / "frontend/public/sw.js"
        content = sw_path.read_text(encoding="utf-8")

        # Cache names and versions
        self.assertIn("STATIC_CACHE", content)
        self.assertIn("PAGES_CACHE", content)
        self.assertIn("FONTS_CACHE", content)
        self.assertIn("DATA_CACHE", content)

        # Precache list
        self.assertIn("CORE_PRECACHE_URLS", content)
        self.assertIn("'/offline'", content)
        self.assertIn("'/manifest.json'", content)

        # Navigation fallback logic
        self.assertIn("request.mode === 'navigate'", content)
        self.assertIn("caches.match('/offline')", content)

        # Message listener for SKIP_WAITING
        self.assertIn("SKIP_WAITING", content)
        self.assertIn("self.skipWaiting()", content)

        # Background sync
        self.assertIn("sync", content)
        self.assertIn("TRIGGER_OFFLINE_SYNC", content)

    def test_06_indexeddb_offline_papers_store(self):
        """Verify IndexedDB past papers vault module structure and methods."""
        store_path = REPO_ROOT / "frontend/src/lib/offline/offline-papers-store.ts"
        content = store_path.read_text(encoding="utf-8")

        self.assertIn("SLC_Board_Papers_Vault", content)
        self.assertIn("saveBoardQuestionToVault", content)
        self.assertIn("saveMultipleBoardQuestions", content)
        self.assertIn("getBoardQuestionFromVault", content)
        self.assertIn("getAllSavedBoardQuestions", content)
        self.assertIn("searchSavedQuestions", content)
        self.assertIn("getOfflineVaultStats", content)
        self.assertIn("MemoryStorageFallback", content)

    def test_07_pwa_ui_components(self):
        """Verify PWA UpdateToast, InstallBanner, and OfflineIndicator components."""
        # PwaUpdateToast
        toast_content = (REPO_ROOT / "frontend/src/components/pwa/PwaUpdateToast.tsx").read_text(encoding="utf-8")
        self.assertIn("PwaUpdateToast", toast_content)
        self.assertIn("SKIP_WAITING", toast_content)
        self.assertIn("window.location.reload()", toast_content)
        self.assertIn("role=\"status\"", toast_content)

        # PwaInstallBanner
        banner_content = (REPO_ROOT / "frontend/src/components/pwa/PwaInstallBanner.tsx").read_text(encoding="utf-8")
        self.assertIn("PwaInstallBanner", banner_content)
        self.assertIn("beforeinstallprompt", banner_content)
        self.assertIn("deferredPrompt.prompt()", banner_content)

        # OfflineIndicator
        indicator_content = (REPO_ROOT / "frontend/src/components/pwa/OfflineIndicator.tsx").read_text(encoding="utf-8")
        self.assertIn("OfflineIndicator", indicator_content)
        self.assertIn("window.addEventListener('online'", indicator_content)
        self.assertIn("window.addEventListener('offline'", indicator_content)
        self.assertIn("href=\"/offline\"", indicator_content)

        # Barrel export
        barrel_content = (REPO_ROOT / "frontend/src/components/pwa/index.ts").read_text(encoding="utf-8")
        self.assertIn("PwaUpdateToast", barrel_content)
        self.assertIn("PwaInstallBanner", barrel_content)
        self.assertIn("OfflineIndicator", barrel_content)

    def test_08_offline_page_elevation(self):
        """Verify /offline page includes PageHeader, IndexedDB integration, and search."""
        offline_content = (REPO_ROOT / "frontend/src/pages/offline.tsx").read_text(encoding="utf-8")

        self.assertIn("PageHeader", offline_content)
        self.assertIn("Card", offline_content)
        self.assertIn("EmptyState", offline_content)
        self.assertIn("getAllSavedBoardQuestions", offline_content)
        self.assertIn("KaTeXRenderer", offline_content)
        self.assertIn("handleRetryConnection", offline_content)

    def test_09_root_app_and_document_integration(self):
        """Verify _app.tsx and _document.tsx integrate PWA components and resource hints."""
        app_content = (REPO_ROOT / "frontend/src/pages/_app.tsx").read_text(encoding="utf-8")
        self.assertIn("PwaUpdateToast", app_content)
        self.assertIn("PwaInstallBanner", app_content)
        self.assertIn("OfflineIndicator", app_content)
        self.assertIn("navigator.serviceWorker.register('/sw.js')", app_content)

        doc_content = (REPO_ROOT / "frontend/src/pages/_document.tsx").read_text(encoding="utf-8")
        self.assertIn("rel=\"preconnect\"", doc_content)
        self.assertIn("display=swap", doc_content)
        self.assertIn("rel=\"apple-touch-icon\"", doc_content)
        self.assertIn("content=\"#090D16\"", doc_content)


if __name__ == "__main__":
    unittest.main()
