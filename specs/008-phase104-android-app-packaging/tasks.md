<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 104 Android TWA APK & Play Store Readiness
FILE:      specs/008-phase104-android-app-packaging/tasks.md
PHASE:     Phase 104 - Android TWA APK & Play Store Readiness
PURPOSE:   Ordered task list tracking atomic implementation steps for TWA packaging,
           build automation, store graphics kit, offline arena, and automated verification.
STANDARDS: UI/UX Pro Max, Google Play Console 2026, Android 14+ (Target SDK 34), Zero-Emoji
-->

# Tasks: Phase 104 — Android TWA APK & Play Store Readiness

## Tasks Ledger

- [x] Task 1: Update and verify Digital Asset Links (`frontend/public/.well-known/assetlinks.json`)
  - Target package: `bd.edu.ogrojatra.app`
  - Valid RFC 6962 JSON format and SHA-256 certificate fingerprints verified.
- [x] Task 2: Configure Bubblewrap TWA manifest (`mobile/twa-manifest.json`) with target SDK 34, package `bd.edu.ogrojatra.app`, and theme color `#0F172A`
  - Target SDK: 34 (Android 14+ compatible)
  - Display: standalone, Theme color: `#0F172A`, Background color: `#F8FAFC`
- [x] Task 3: Update automated build script (`mobile/build_apk.sh`) with Phase 104 Developer Architecture Note header and execute build
  - Generates `app-release-bundle.aab`, `app-release-signed.apk`, and `app-debug-unsigned.apk`
  - Extracts and verifies release fingerprint in `mobile/output/signing-fingerprint.txt`
- [x] Task 4: Generate high-resolution store PNG assets (`icon_512x512.png`, `feature_graphic_1024x500.png`) and create comprehensive documentation (`mobile/store-assets/README.md`)
  - 512x512 PNG App Icon generated and verified
  - 1024x500 PNG Feature Graphic generated and verified
  - Complete Play Store graphics kit documented with bilingual copy references
- [x] Task 5: Implement inspiring offline study arena (`frontend/src/pages/offline.tsx`) with tactile 3D buttons and zero emoji
  - Replaces generic offline errors with cached question banks for physics, math, and chemistry
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#1D4ED8]`)
  - Pure Lucide vectors and Hind Siliguri Bengali typography
- [x] Task 6: Implement automated verification test suite (`backend/tests/test_phase104_android_packaging.py`)
  - 6 comprehensive test cases asserting AssetLinks, TWA manifest, build script, PNG assets, offline page, and zero-emoji compliance.
- [x] Task 7: Execute full regression test discovery (`python3 -m unittest discover -s backend/tests`) and zero-emoji sweep, asserting 100% pass rate
  - 1,290 / 1,290 tests passing (100% success rate)
  - 482 files scanned in zero-emoji sweep: 0 violations found
