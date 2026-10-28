# Feature Specification: Live Challenge Hero - Exact Live MCQ Visual Elevation

- **Feature Directory:** `specs/058-live-challenge-hero-exact-livemcq-elevation`
- **Topic:** Phase 143 - Live Challenge Hero Section Elevation Matching Live MCQ Reference Screenshot
- **Target Page:** `frontend/src/pages/live-challenge.tsx` & `frontend/src/components/live-challenge/LiveMcqHeroSection.tsx`
- **Reference Asset:** User-uploaded screenshot (`media_1793149966303_08d756b3.png`)
- **Standards:** Zero-Emoji Policy, Lucide SVGs, WCAG 2.2 AAA Contrast, Responsive Layout, Port 3002 Discipline

---

## 1. Executive Summary & Vision

The user requested to transform the first section ("prothom para") of the Live Challenge page (`/live-challenge`) to precisely match the visual design language of the provided Live MCQ screenshot.
This includes:
1. Deep Cosmic Indigo Canvas with angled luminous light streaks, warm amber stardust particles, and a luminous royal blue/indigo core glow.
2. Floating glassmorphism track pills (`• BCS`, `• NTRCA`, `• Primary`, `• Bank`, `• BJS`) with glowing borders and floating educational academic icons (Mortarboard with tassel, open notebook, pencil).
3. Central Editorial Typography:
   - Top capsule badge: `• সঠিক প্রস্তুতি, সহজ প্রিলি`
   - Bold dual-tone headline: "ঘরে বসেই সকল প্রতিযোগিতামূলক" in crisp white, and "চাকরির পূর্ণাঙ্গ প্রস্তুতি" in fiery orange-amber gradient.
   - Subtitle featuring competitive exam tracks and highlighted `২৪ লাখ+` badge.
4. Dual Action CTA Pill Buttons:
   - Primary Cyan-to-Cobalt gradient pill: "৪৫তম স্পেশাল বিসিএস ও লাইভ অলিম্পিয়াড"
   - Fiery Orange-to-Amber gradient pill: "পরীক্ষা দিন"
5. Multi-Platform Ecosystem Row:
   - "অ্যাপ ইনস্টল করুন" with Google Play, App Store, Windows, macOS, and Web icons.
6. Bottom Docked Frosted Glass Container with 4 grand KPI metrics:
   - ২৪ লাখ+ অ্যাপ ব্যবহারকারী
   - ৭.৫ লাখ+ আর্কাইভ MCQ (reference-সহ ব্যাখ্যা)
   - ৩০ হাজার+ প্রতিদিন গড় ব্যবহারকারী
   - ১০+ বছরের অভিজ্ঞতা
7. Zero Code Regression:
   - Retains 100% of live exam state, countdown timer, rules modal trigger, and navigation links.

---

## 2. Acceptance Criteria

- **AC-001 (Canvas & Lighting):** Deep midnight indigo background with subtle diagonal light streaks and floating golden particles.
- **AC-002 (Floating Badges & Motifs):** 5 translucent floating pills (BCS, NTRCA, Primary, Bank, BJS) with colored halos, plus SVG educational motifs.
- **AC-003 (Typography & Copy):** Crisp white main line and fiery orange gradient second line matching the screenshot.
- **AC-004 (Dual CTAs & App Badges):** Dual gradient pill buttons and platform ecosystem row.
- **AC-005 (Docked Frosted KPI Card):** 4-column metric card with golden font-mono numbers and descriptive Bengali labels.
- **AC-006 (Live Challenge Integration):** Server-authoritative timer and rules modal trigger preserved without disruption.
- **AC-007 (Quality & Security Standards):** 100% zero-emoji, clean TypeScript compilation, passing test suite, and Strix security verification.
