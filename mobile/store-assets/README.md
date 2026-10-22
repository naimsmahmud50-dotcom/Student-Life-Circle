<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Mobile Engineering & App Store Operations
TOPIC:     Phase 104 Google Play Store Visual Assets & Listing Kit
FILE:      mobile/store-assets/README.md
PHASE:     Phase 104 - Android TWA APK & Play Store Readiness
PURPOSE:   Complete documentation of Google Play Console store listing specifications,
           visual asset requirements (512x512 App Icon, 1024x500 Feature Graphic,
           multi-form factor device screenshots), color tokens, bilingual localized
           metadata (bn-BD and en-US), and pre-submission compliance checklist.
STANDARDS: Google Play Console 2026 Guidelines, UI/UX Pro Max, Zero-Emoji
-->

# Google Play Store Visual Assets & Listing Kit

This directory contains the production-ready graphics, localized store copy, and metadata required for publishing **অগ্রযাত্রা (Student Life Circle)** to the Google Play Store under package ID `bd.edu.ogrojatra.app`.

---

## 1. Store Asset Specifications

| Asset Type | Required Dimensions | Aspect Ratio | Format | File Path |
| :--- | :--- | :--- | :--- | :--- |
| **App Icon** | 512 x 512 px | 1:1 | 32-bit PNG / SVG | `mobile/store-assets/icon_512x512.png` & `.svg` |
| **Feature Graphic** | 1024 x 500 px | 1024:500 | 24-bit PNG / SVG | `mobile/store-assets/feature_graphic_1024x500.png` & `.svg` |
| **Adaptive Icon** | 108 x 108 dp | 1:1 | Vector SVG | `mobile/store-assets/adaptive_icon.svg` |
| **Phone Screenshot** | 1080 x 1920 px | 9:16 | 24-bit SVG | `mobile/store-assets/screenshot_phone_1080x1920.svg` |
| **7-inch Tablet Screenshot** | 1200 x 1920 px | 10:16 | 24-bit SVG | `mobile/store-assets/screenshot_tablet_7inch_1200x1920.svg` |
| **10-inch Tablet Screenshot** | 1920 x 1200 px | 16:10 | 24-bit SVG | `mobile/store-assets/screenshot_tablet_10inch_1920x1200.svg` |

---

## 2. Design System & Palette Tokens

All visual assets follow the human-crafted, dignified aesthetic standards of Ogrojatra:

- **Primary Background (Midnight Slate):** `#0F172A`
- **Secondary Surface:** `#1E293B`
- **Accent Brand Blue:** `#2563EB`
- **Focus / Success Emerald:** `#10B981`
- **Warm Highlight Amber:** `#F59E0B`
- **Text & Glyph Light:** `#F8FAFC`
- **Typography:**
  - Primary Bengali: `Hind Siliguri` (curved terminals, dignified ascenders)
  - Display & Numerals: `Plus Jakarta Sans` (confident geometric clarity)

---

## 3. Bilingual Store Listing Reference (`store_listing.json`)

The definitive metadata is maintained in `mobile/store-assets/store_listing.json`. Key constraints:

### A. Bengali Locale (`bn-BD`) - Default
- **App Title (Max 30 chars):** `অগ্রযাত্রা - স্টুডেন্ট অ্যাপ` (25 chars)
- **Short Description (Max 80 chars):** `এইচএসসি, এসএসসি ও ভর্তি পরীক্ষার প্রস্তুতি ও সহায়িকা প্ল্যাটফর্ম।` (64 chars)
- **Full Description (Max 4000 chars):** Detailed NCTB curriculum coverage, Socratic AI tutor guidance, 3D STEM labs, live quiz challenges, and verified skill credentials.

### B. English Locale (`en-US`)
- **App Title (Max 30 chars):** `Ogrojatra - Student Platform` (28 chars)
- **Short Description (Max 80 chars):** `Complete academic, exam preparation & mentoring platform for students in BD.` (76 chars)
- **Full Description (Max 4000 chars):** Rigorous academic overview, step-by-step KaTeX solutions, and verifiable proof-of-skill credentials.

---

## 4. Google Play Console Compliance Checklist

1. [x] Package ID: `bd.edu.ogrojatra.app` matches TWA manifest and build scripts.
2. [x] Target SDK: 34 (Android 14+) compliant with Google Play target API requirements.
3. [x] Category: `EDUCATION`
4. [x] Content Rating: `EVERYONE`
5. [x] Privacy Policy URL: `https://ogrojatra.edu.bd/privacy` (HTTPS compliant).
6. [x] Zero-Emoji Governance: Strictly zero unicode decorative emojis in listing text and logs.
7. [x] Digital Asset Links: Verified via `frontend/public/.well-known/assetlinks.json`.
