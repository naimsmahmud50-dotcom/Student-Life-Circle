"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 104 Android TWA APK & Play Store Readiness Tests
FILE:      backend/tests/test_phase104_android_packaging.py
PHASE:     Phase 104 - Android TWA APK & Play Store Readiness
PURPOSE:   Asserts Digital Asset Links (RFC 6962) syntax, Bubblewrap TWA manifest
           (Target SDK 34, #0F172A theme), reproducible APK/AAB build outputs,
           high-res Play Store graphics kit (512x512 Icon, 1024x500 Feature Graphic),
           offline study arena page resilience, and strict zero-emoji governance.
STANDARDS: Google Play Console 2026, Android 14+ (Target SDK 34), Zero-Emoji
"""

import json
import os
import re
import unittest
from pathlib import Path
from PIL import Image


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
    """Returns True if the string contains any decorative unicode emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase104AndroidPackaging(unittest.TestCase):
    """
    Automated verification suite for Phase 104 Android TWA APK & Play Store Readiness.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.assetlinks_path = cls.repo_root / "frontend" / "public" / ".well-known" / "assetlinks.json"
        cls.twa_manifest_path = cls.repo_root / "mobile" / "twa-manifest.json"
        cls.build_script_path = cls.repo_root / "mobile" / "build_apk.sh"
        cls.store_assets_dir = cls.repo_root / "mobile" / "store-assets"
        cls.store_readme_path = cls.store_assets_dir / "README.md"
        cls.store_listing_path = cls.store_assets_dir / "store_listing.json"
        cls.icon_png_path = cls.store_assets_dir / "icon_512x512.png"
        cls.feature_png_path = cls.store_assets_dir / "feature_graphic_1024x500.png"
        cls.offline_page_path = cls.repo_root / "frontend" / "src" / "pages" / "offline.tsx"
        cls.output_dir = cls.repo_root / "mobile" / "output"

    def test_01_digital_asset_links_rfc6962_and_fingerprints(self):
        """Verifies frontend/public/.well-known/assetlinks.json schema and SHA-256 certificate fingerprints."""
        self.assertTrue(self.assetlinks_path.exists(), f"Missing assetlinks.json at {self.assetlinks_path}")

        with open(self.assetlinks_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        entry = data[0]
        self.assertIn("delegate_permission/common.handle_all_urls", entry.get("relation", []))

        target = entry.get("target", {})
        self.assertEqual(target.get("namespace"), "android_app")
        self.assertEqual(target.get("package_name"), "bd.edu.ogrojatra.app")

        fingerprints = target.get("sha256_cert_fingerprints", [])
        self.assertGreaterEqual(len(fingerprints), 1)

        # 32 pairs of uppercase hex characters separated by colons
        fp_pattern = r"^([0-9A-F]{2}:){31}[0-9A-F]{2}$"
        for fp in fingerprints:
            self.assertTrue(
                re.match(fp_pattern, fp),
                f"Fingerprint '{fp}' does not match standard 32-byte colon-separated SHA-256 format"
            )

    def test_02_bubblewrap_twa_manifest_and_android14_compliance(self):
        """Verifies mobile/twa-manifest.json Target SDK 34 and midnight slate theme colors."""
        self.assertTrue(self.twa_manifest_path.exists(), f"Missing twa-manifest.json at {self.twa_manifest_path}")

        with open(self.twa_manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("packageId"), "bd.edu.ogrojatra.app")
        self.assertEqual(manifest.get("name"), "অগ্রযাত্রা - Student Growth Platform")
        self.assertEqual(manifest.get("launcherName"), "অগ্রযাত্রা")
        self.assertEqual(manifest.get("display"), "standalone")

        # Android 14+ target SDK requirement
        self.assertGreaterEqual(manifest.get("targetSdkVersion", 0), 34)
        self.assertEqual(manifest.get("themeColor").upper(), "#0F172A")
        self.assertEqual(manifest.get("navigationColor").upper(), "#0F172A")
        self.assertIn(manifest.get("backgroundColor").upper(), ["#F8FAFC", "#0F172A"])
        self.assertGreaterEqual(manifest.get("splashScreenFadeOutDuration", 0), 300)

    def test_03_build_script_and_artifact_generation(self):
        """Verifies mobile/build_apk.sh executability and generated release / debug packaging artifacts."""
        self.assertTrue(self.build_script_path.exists())
        self.assertTrue(os.access(self.build_script_path, os.X_OK))

        with open(self.build_script_path, "r", encoding="utf-8") as f:
            script = f.read()

        self.assertIn("Phase 104", script)
        self.assertIn("app-release-bundle.aab", script)
        self.assertIn("app-release-signed.apk", script)
        self.assertIn("app-debug-unsigned.apk", script)

        # Assert output artifacts exist
        aab_path = self.output_dir / "app-release-bundle.aab"
        release_apk_path = self.output_dir / "app-release-signed.apk"
        debug_apk_path = self.output_dir / "app-debug-unsigned.apk"
        fingerprint_path = self.output_dir / "signing-fingerprint.txt"

        self.assertTrue(aab_path.exists(), "Missing app-release-bundle.aab")
        self.assertTrue(release_apk_path.exists(), "Missing app-release-signed.apk")
        self.assertTrue(debug_apk_path.exists(), "Missing app-debug-unsigned.apk")
        self.assertTrue(fingerprint_path.exists(), "Missing signing-fingerprint.txt")

        self.assertGreater(aab_path.stat().st_size, 0)
        self.assertGreater(release_apk_path.stat().st_size, 0)
        self.assertGreater(debug_apk_path.stat().st_size, 0)

    def test_04_play_store_graphics_kit_and_documentation(self):
        """Verifies high-res 512x512 Icon and 1024x500 Feature Graphic PNG dimensions and README docs."""
        self.assertTrue(self.store_readme_path.exists())
        with open(self.store_readme_path, "r", encoding="utf-8") as f:
            readme = f.read()
        self.assertIn("Phase 104", readme)
        self.assertIn("bd.edu.ogrojatra.app", readme)

        # Assert 512x512 Icon PNG
        self.assertTrue(self.icon_png_path.exists(), "Missing icon_512x512.png")
        with Image.open(self.icon_png_path) as img:
            self.assertEqual(img.size, (512, 512))

        # Assert 1024x500 Feature Graphic PNG
        self.assertTrue(self.feature_png_path.exists(), "Missing feature_graphic_1024x500.png")
        with Image.open(self.feature_png_path) as img:
            self.assertEqual(img.size, (1024, 500))

        # Assert store_listing.json metadata compliance
        with open(self.store_listing_path, "r", encoding="utf-8") as f:
            listing = json.load(f)
        self.assertIn("bn-BD", listing.get("locales", {}))
        self.assertIn("en-US", listing.get("locales", {}))

    def test_05_offline_study_arena_page_and_tactile_elements(self):
        """Verifies frontend/src/pages/offline.tsx contains inspiring Bengali copy and 3D tactile buttons."""
        self.assertTrue(self.offline_page_path.exists(), f"Missing offline.tsx at {self.offline_page_path}")

        with open(self.offline_page_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Architecture header
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)
        self.assertIn("Phase 104", content)

        # Inspiring Human Bengali Copy
        self.assertIn("ইন্টারনেট সংযোগ নেই", content)
        self.assertIn("প্রস্তুতি কিন্তু থেমে নেই", content)

        # Tactile 3D button styling
        self.assertIn("shadow-[0_4px_0_0_#1D4ED8]", content)

        # Lucide vector icons
        self.assertIn("WifiOff", content)
        self.assertIn("BookOpen", content)
        self.assertIn("RefreshCw", content)

    def test_06_developer_architecture_note_and_zero_emoji_governance(self):
        """Verifies Developer Architecture Note presence and strict zero-emoji compliance."""
        phase104_files = [
            self.build_script_path,
            self.store_readme_path,
            self.offline_page_path,
            Path(__file__)
        ]

        for file_path in phase104_files:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            self.assertIn("DEVELOPER ARCHITECTURE NOTE", text, f"Missing Architecture Note in {file_path.name}")
            self.assertIn("Phase 104", text, f"Missing Phase 104 reference in {file_path.name}")
            self.assertFalse(contains_emoji(text), f"Zero-Emoji violation detected in {file_path.name}")


if __name__ == "__main__":
    unittest.main()
