<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 104 Android TWA APK & Play Store Readiness
FILE:      specs/008-phase104-android-app-packaging/spec.md
PHASE:     Phase 104 - Android TWA APK & Play Store Readiness
PURPOSE:   Establishes functional specifications for Android Trusted Web Activity (TWA)
           packaging, Digital Asset Links verification, Bubblewrap manifest configuration,
           reproducible APK/AAB build automation, Google Play Store visual assets kit,
           and offline study arena resilience for students across Bangladesh.
STANDARDS: UI/UX Pro Max, Google Play Console 2026, Android 14+ (Target SDK 34), Zero-Emoji
-->

# Specification: Phase 104 — Android TWA APK & Play Store Readiness

## Feature Directory
`specs/008-phase104-android-app-packaging`

## 1. Problem Statement
Over 85% of secondary and higher secondary students in Bangladesh access online learning via Android smartphones, often on constrained 3G/4G cellular connections or intermittent transit networks (e.g. while commuting on trains or buses). A purely web-based application encounters URL bar layout shifts, browser chrome intrusions, lack of homescreen presence, and abrupt offline connection dropouts. To deliver a first-class, dignified native app experience, "Student Life Circle (অগ্রযাত্রা)" requires a Google-certified Trusted Web Activity (TWA) packaging pipeline. This unlocks full-screen immersion without browser URL bars, seamless Digital Asset Links cryptographic handshake, native Android 12+ SplashScreen transitions with zero white launch flashes, and an inspiring offline study arena with cached question sets.

## 2. Goals & User Stories

### US1: Digital Asset Links & Cryptographic Verification (P1)
- As an Android system, I must cryptographically verify that `bd.edu.ogrojatra.app` is the authorized native container for `ogrojatra.edu.bd` so that the browser URL bar is completely hidden.
- Acceptance Criteria:
  - `frontend/public/.well-known/assetlinks.json` valid RFC 6962 array with `delegate_permission/common.handle_all_urls`.
  - Target package matches `bd.edu.ogrojatra.app`.
  - Valid 32-byte uppercase colon-delimited SHA-256 certificate fingerprints configured.

### US2: Bubblewrap TWA Manifest & Android 14+ Compliance (P1)
- As a Play Store reviewer, the app manifest must comply with Android 14+ (API Level 34) standards, midnight slate status/nav bars (`#0F172A`), and standalone display.
- Acceptance Criteria:
  - `mobile/twa-manifest.json` configured with `packageId: "bd.edu.ogrojatra.app"`.
  - `targetSdkVersion >= 34`, `minSdkVersion: 24`, `display: "standalone"`.
  - `themeColor: "#0F172A"`, `navigationColor: "#0F172A"`, `splashScreenFadeOutDuration: 300`.
  - Zero-white-flash launch guaranteed by aligned theme colors.

### US3: Automated Build Pipeline (APK & AAB) (P1)
- As a DevOps engineer, I want a single automated script `mobile/build_apk.sh` to validate prerequisites, manage release keystores, and generate both Google Play Store bundle (.aab) and direct sideload APK (.apk).
- Acceptance Criteria:
  - `mobile/build_apk.sh` executable and exits with code 0.
  - Automatically extracts and verifies signing fingerprint into `mobile/output/signing-fingerprint.txt`.
  - Outputs `app-release-bundle.aab` and `app-release-signed.apk` in `mobile/output/`.

### US4: Play Store Visual Assets & Bilingual Listing Kit (P1)
- As the product marketing team, I need store-ready graphics (512x512 high-res icon, 1024x500 feature graphic, multi-device screenshots) and bilingual (Bengali & English) store listings adhering to Google Play character limits.
- Acceptance Criteria:
  - High-res PNG & SVG assets: 512x512 Icon, 1024x500 Feature Graphic.
  - Multi-form factor mockups: Phone (1080x1920), 7-inch Tablet (1200x1920), 10-inch Tablet (1920x1200).
  - `mobile/store-assets/README.md` documenting complete asset kit, colors, typography, and checklist.
  - Title <= 30 chars, Short description <= 80 chars, Full description <= 4000 chars.

### US5: Inspiring Offline Study Arena (P1)
- As a student opening the app on a train without internet connectivity, I want to see an inspiring offline study arena with cached question bank access rather than a broken dinosaur or blank white screen.
- Acceptance Criteria:
  - `frontend/src/pages/offline.tsx` rendered with warm Bengali microcopy ("ইন্টারনেট সংযোগ নেই? প্রস্তুতি কিন্তু থেমে নেই!").
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#1D4ED8]`).
  - Zero-emoji Lucide vectors (`WifiOff`, `BookOpen`, `Sparkles`, `RefreshCw`).
  - Native Hind Siliguri typography with smooth font rendering.
