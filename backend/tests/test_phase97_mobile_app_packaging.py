# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 97 - Mobile Packaging & Store Assets Test):
# Comprehensive test suite validating Android Trusted Web Activity (TWA)
# configuration, Digital Asset Links (assetlinks.json), Google Play Store
# metadata, 1024x500 feature graphics, multi-device screenshots (Phone,
# 7-inch tablet, 10-inch tablet), adaptive icons, build script automation,
# and strict Zero-Emoji compliance.
#
# Standards & Verification:
# 1. Digital Asset Links: RFC 6962 / Google Digital Asset Links syntax,
#    delegating handle_all_urls to bd.edu.ogrojatra.app with SHA-256 fingerprints.
# 2. Bubblewrap TWA Manifest: Target SDK 34+ (Android 14+), themeColor #0F172A,
#    navigationColor #0F172A, standalone display.
# 3. Google Play Console Rules: App Title <= 30 chars, Short Description <= 80 chars,
#    Full Description <= 4000 chars, valid HTTPS privacy policy URL.
# 4. Store Graphics: Exact 1024x500 Feature Graphic, 1080x1920 Phone Screenshot,
#    1200x1920 7-inch Tablet, 1920x1200 10-inch Tablet, and 512x512 Icon.
# 5. Strict Zero-Emoji compliance across all configurations and build tools.
# ==============================================================================

import unittest
import os
import re
import json
from pathlib import Path


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is an emoji."""
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
    """Returns True if the string contains any emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase97MobileAppPackaging(unittest.TestCase):
    """
    Test suite for Phase 97: Android TWA APK Packaging & App Store Assets.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.assetlinks_path = cls.repo_root / "frontend" / "public" / ".well-known" / "assetlinks.json"
        cls.twa_manifest_path = cls.repo_root / "mobile" / "twa-manifest.json"
        cls.build_script_path = cls.repo_root / "mobile" / "build_apk.sh"
        cls.store_listing_path = cls.repo_root / "mobile" / "store-assets" / "store_listing.json"
        cls.feature_graphic_path = cls.repo_root / "mobile" / "store-assets" / "feature_graphic_1024x500.svg"
        cls.phone_ss_path = cls.repo_root / "mobile" / "store-assets" / "screenshot_phone_1080x1920.svg"
        cls.tab7_ss_path = cls.repo_root / "mobile" / "store-assets" / "screenshot_tablet_7inch_1200x1920.svg"
        cls.tab10_ss_path = cls.repo_root / "mobile" / "store-assets" / "screenshot_tablet_10inch_1920x1200.svg"
        cls.icon_512_path = cls.repo_root / "mobile" / "store-assets" / "icon_512x512.svg"
        cls.adaptive_icon_path = cls.repo_root / "mobile" / "store-assets" / "adaptive_icon.svg"
        cls.output_dir = cls.repo_root / "mobile" / "output"

    def test_01_digital_asset_links_syntax_and_schema(self):
        """Verifies frontend/public/.well-known/assetlinks.json syntax and Google TWA requirements."""
        self.assertTrue(self.assetlinks_path.exists(), f"Missing assetlinks.json at {self.assetlinks_path}")

        with open(self.assetlinks_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, list, "assetlinks.json must be a JSON array")
        self.assertGreaterEqual(len(data), 1, "assetlinks.json must contain at least one entry")

        entry = data[0]
        self.assertIn("delegate_permission/common.handle_all_urls", entry.get("relation", []))

        target = entry.get("target", {})
        self.assertEqual(target.get("namespace"), "android_app")
        self.assertEqual(target.get("package_name"), "bd.edu.ogrojatra.app")

        fingerprints = target.get("sha256_cert_fingerprints", [])
        self.assertGreaterEqual(len(fingerprints), 1)

        # Validate fingerprint regex: 32 pairs of uppercase hex characters separated by colons
        fp_pattern = r"^([0-9A-F]{2}:){31}[0-9A-F]{2}$"
        for fp in fingerprints:
            self.assertTrue(
                re.match(fp_pattern, fp),
                f"Fingerprint '{fp}' does not match standard 32-byte colon-separated SHA-256 format"
            )

    def test_02_bubblewrap_twa_manifest_compliance(self):
        """Verifies mobile/twa-manifest.json compliance with Android 14+ (Target SDK 34) guidelines."""
        self.assertTrue(self.twa_manifest_path.exists(), f"Missing twa-manifest.json at {self.twa_manifest_path}")

        with open(self.twa_manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("packageId"), "bd.edu.ogrojatra.app")
        self.assertEqual(manifest.get("host"), "ogrojatra.edu.bd")
        self.assertIn("অগ্রযাত্রা", manifest.get("name", ""))
        self.assertEqual(manifest.get("launcherName"), "অগ্রযাত্রা")

        # Android 14+ target SDK assertion
        target_sdk = manifest.get("targetSdkVersion")
        self.assertIsInstance(target_sdk, int)
        self.assertGreaterEqual(target_sdk, 34, "Target SDK must be 34 or higher for Android 14+ compliance")

        # Status bar and navigation bar color matching
        self.assertEqual(manifest.get("themeColor").upper(), "#0F172A")
        self.assertEqual(manifest.get("navigationColor").upper(), "#0F172A")
        self.assertIn(manifest.get("backgroundColor").upper(), ["#0F172A", "#F8FAFC"])
        self.assertEqual(manifest.get("display"), "standalone")

        # Adaptive icon links
        adaptive = manifest.get("adaptiveIcons", {})
        self.assertIn("roundIconUrl", adaptive)
        self.assertIn("squircleIconUrl", adaptive)

    def test_03_build_script_executability_and_pipeline(self):
        """Verifies mobile/build_apk.sh is executable and contains necessary verification routines."""
        self.assertTrue(self.build_script_path.exists(), f"Missing build_apk.sh at {self.build_script_path}")
        self.assertTrue(os.access(self.build_script_path, os.X_OK), "build_apk.sh must be executable (chmod +x)")

        with open(self.build_script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # Check required build logic symbols
        self.assertIn("assetlinks.json", script_content)
        self.assertIn("twa-manifest.json", script_content)
        self.assertIn("app-release-bundle.aab", script_content)
        self.assertIn("app-release-signed.apk", script_content)
        self.assertIn("signing-fingerprint.txt", script_content)

    def test_04_play_store_listing_metadata_requirements(self):
        """Verifies mobile/store-assets/store_listing.json strictly obeys Google Play Store character limits."""
        self.assertTrue(self.store_listing_path.exists(), f"Missing store_listing.json at {self.store_listing_path}")

        with open(self.store_listing_path, "r", encoding="utf-8") as f:
            listing = json.load(f)

        self.assertEqual(listing.get("category"), "EDUCATION")
        self.assertEqual(listing.get("package_name"), "bd.edu.ogrojatra.app")
        self.assertTrue(listing.get("privacy_policy_url", "").startswith("https://"))

        locales = listing.get("locales", {})
        self.assertIn("bn-BD", locales, "Must contain Bengali store listing")
        self.assertIn("en-US", locales, "Must contain English store listing")

        for loc_key, loc_data in locales.items():
            title = loc_data.get("title", "")
            short_desc = loc_data.get("short_description", "")
            full_desc = loc_data.get("full_description", "")

            # Google Play Console strict constraints:
            # Title: maximum 30 characters
            self.assertLessEqual(
                len(title), 30,
                f"Title for {loc_key} exceeds 30 characters: '{title}' ({len(title)} chars)"
            )
            # Short description: maximum 80 characters
            self.assertLessEqual(
                len(short_desc), 80,
                f"Short description for {loc_key} exceeds 80 characters: '{short_desc}' ({len(short_desc)} chars)"
            )
            # Full description: maximum 4000 characters and non-empty
            self.assertLessEqual(len(full_desc), 4000)
            self.assertGreaterEqual(len(full_desc), 100)

    def test_05_feature_graphic_dimensions_and_svg_structure(self):
        """Verifies feature_graphic_1024x500.svg has exact 1024x500 dimensions."""
        self.assertTrue(self.feature_graphic_path.exists())

        with open(self.feature_graphic_path, "r", encoding="utf-8") as f:
            svg = f.read()

        self.assertIn('width="1024"', svg)
        self.assertIn('height="500"', svg)
        self.assertIn('viewBox="0 0 1024 500"', svg)
        self.assertIn("অগ্রযাত্রা | OGROJATRA", svg)

    def test_06_screenshots_dimensions_and_device_targets(self):
        """Verifies phone, 7-inch tablet, and 10-inch tablet screenshots meet Google Play dimension specs."""
        # Phone: 1080x1920
        with open(self.phone_ss_path, "r", encoding="utf-8") as f:
            phone_svg = f.read()
        self.assertIn('width="1080"', phone_svg)
        self.assertIn('height="1920"', phone_svg)
        self.assertIn('viewBox="0 0 1080 1920"', phone_svg)

        # 7-inch Tablet: 1200x1920
        with open(self.tab7_ss_path, "r", encoding="utf-8") as f:
            tab7_svg = f.read()
        self.assertIn('width="1200"', tab7_svg)
        self.assertIn('height="1920"', tab7_svg)
        self.assertIn('viewBox="0 0 1200 1920"', tab7_svg)

        # 10-inch Tablet: 1920x1200
        with open(self.tab10_ss_path, "r", encoding="utf-8") as f:
            tab10_svg = f.read()
        self.assertIn('width="1920"', tab10_svg)
        self.assertIn('height="1200"', tab10_svg)
        self.assertIn('viewBox="0 0 1920 1200"', tab10_svg)

    def test_07_app_icon_and_adaptive_launcher_assets(self):
        """Verifies 512x512 app icon and 108x108 adaptive icon dimensions."""
        with open(self.icon_512_path, "r", encoding="utf-8") as f:
            icon_svg = f.read()
        self.assertIn('width="512"', icon_svg)
        self.assertIn('height="512"', icon_svg)

        with open(self.adaptive_icon_path, "r", encoding="utf-8") as f:
            adaptive_svg = f.read()
        self.assertIn('width="108"', adaptive_svg)
        self.assertIn('height="108"', adaptive_svg)

    def test_08_output_artifacts_and_signing_fingerprints(self):
        """Verifies release APK, AAB bundle, and fingerprint text files generated by build pipeline."""
        apk_file = self.output_dir / "app-release-signed.apk"
        aab_file = self.output_dir / "app-release-bundle.aab"
        fp_file = self.output_dir / "signing-fingerprint.txt"

        self.assertTrue(apk_file.exists(), "Release APK must exist in mobile/output/")
        self.assertTrue(aab_file.exists(), "Release AAB must exist in mobile/output/")
        self.assertTrue(fp_file.exists(), "Signing fingerprint file must exist in mobile/output/")

        self.assertGreater(apk_file.stat().st_size, 0)
        self.assertGreater(aab_file.stat().st_size, 0)

        with open(fp_file, "r", encoding="utf-8") as f:
            fp_content = f.read().strip()
        self.assertIn("3B:4E:91:8C:72:A5:10:9F:88:2E:3D:4C:5B:6A:7F:80:91:A2:B3:C4:D5:E6:F7:08:19:2A:3B:4C:5D:6E:7F:80", fp_content)

    def test_09_strict_zero_emoji_in_mobile_and_store_assets(self):
        """Validates that no decorative emojis are present in any Phase 97 files."""
        files_to_scan = [
            self.assetlinks_path,
            self.twa_manifest_path,
            self.build_script_path,
            self.store_listing_path,
            self.feature_graphic_path,
            self.phone_ss_path,
            self.tab7_ss_path,
            self.tab10_ss_path,
            self.icon_512_path,
            self.adaptive_icon_path,
            Path(__file__)
        ]

        for file_path in files_to_scan:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertFalse(
                contains_emoji(content),
                f"Strict Zero-Emoji violation detected in {file_path.name}"
            )

    def test_10_developer_architecture_notes_presence(self):
        """Verifies Developer Architecture Notes exist in key files."""
        files_to_check = [
            self.build_script_path,
            Path(__file__)
        ]

        for file_path in files_to_check:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(
                "DEVELOPER ARCHITECTURE NOTE" in content,
                f"Developer Architecture Note missing from {file_path.name}"
            )


if __name__ == "__main__":
    unittest.main()
