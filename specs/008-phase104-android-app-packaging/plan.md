<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Implementation Plan
TOPIC:     Phase 104 Android TWA APK & Play Store Readiness
FILE:      specs/008-phase104-android-app-packaging/plan.md
PHASE:     Phase 104 - Android TWA APK & Play Store Readiness
PURPOSE:   Architectural blueprint detailing technical steps for TWA configuration,
           reproducible APK/AAB build routines, high-resolution Play Store assets,
           offline resilience screen, automated test suite, and regression gating.
STANDARDS: UI/UX Pro Max, Google Play Console 2026, Android 14+ (Target SDK 34), Zero-Emoji
-->

# Implementation Plan: Phase 104 — Android TWA APK & Play Store Readiness

## 1. Architecture Overview
The Android client for Ogrojatra is delivered through a high-performance Trusted Web Activity (TWA) utilizing the modern AndroidX browser library and Google Bubblewrap packaging framework. This architecture ensures instantaneous updates (PWA parity) while granting full Play Store distribution, native home launcher integration, and complete removal of browser chrome via Digital Asset Links.

```
+-------------------------------------------------------------+
|                      Google Play Store                      |
|       (Signed AAB / Target SDK 34 / 512x512 Icon / 1024x500)|
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                   Android Device (TWA Client)               |
|  - Splash Screen (Dark Midnight #0F172A, Hind Siliguri)     |
|  - Digital Asset Links: RFC 6962 handshake                  |
|  - Status Bar & Navigation Bar: #0F172A (No White Flash)   |
+------------------------------+------------------------------+
                               |
               +---------------+---------------+
               |                               |
       (Network Active)               (Network Offline)
               |                               |
               v                               v
    Ogrojatra Web App               Offline Study Arena
    (Interactive Hub)              (/offline - Cached Sets)
```

## 2. Target Deliverables & File Changes
1. `specs/008-phase104-android-app-packaging/spec.md`, `plan.md`, `tasks.md`: Spec Kit documentation.
2. `frontend/public/.well-known/assetlinks.json`: Validated Digital Asset Links with production SHA-256 fingerprints.
3. `mobile/twa-manifest.json`: Verified TWA configuration for `bd.edu.ogrojatra.app`, Target SDK 34, theme colors `#0F172A`.
4. `mobile/build_apk.sh`: Automated APK/AAB build script with Phase 104 header and zero emoji.
5. `mobile/store-assets/README.md`: Complete Google Play Store asset kit documentation.
6. `mobile/store-assets/icon_512x512.png` & `mobile/store-assets/feature_graphic_1024x500.png`: High-res PNG assets generated using PIL.
7. `frontend/src/pages/offline.tsx`: Tactile, human-crafted offline study arena.
8. `backend/tests/test_phase104_android_packaging.py`: Automated verification test suite.
9. Full regression pass asserting 1,290+ tests with 0 failures and 0 emoji.
