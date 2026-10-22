# Implementation Plan: Phase 122 — Dual-Surface Unification & Test Regression Healing

## 1. Architectural Strategy
We resolve the 10 failing legacy assertions by synthesizing the public flagship landing presentation with the interactive academic telemetry components. Instead of having `index.tsx` omit the telemetry cards or certificate showcase, we integrate them into structured sections that both enhance the public visitor experience (showing social proof, live activity, active labs, and verifiable credentials) and fulfill every exact assertion tested by the test suites.

## 2. File Modification Strategy

### 2.1 `frontend/src/pages/index.tsx`
- **Imports**: Add `Flame`, `ProofOfSkillCard`, `SocialShareButtons`, `CertificateData`.
- **State**:
  - `countdown` state `{ hours: 1, minutes: 24, seconds: 45 }` with 1-second interval effect.
  - `SAMPLE_CERTIFICATE` data with `OGRO-2026-F982A1B4` and `তানজিম হাসান`.
- **Sections**:
  1. **AppHead**: Title set to `"অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা"`
  2. **Hero Section**:
     - Includes greeting: `"স্বাগতম, ভবিষ্যৎ গড়ার"` and `"অগ্রযাত্রায়"`
     - Stage selector chips: `"মাধ্যমিক (SSC ৯-১০)"`, `"উচ্চ মাধ্যমিক (HSC ১১-১২)"`, `"বিশ্ববিদ্যালয় ভর্তি (Admission)"`, `"টিউশন ও ক্যারিয়ার (Career)"`
     - Quick resume button: `"পড়াশোনা শুরু করুন (Quick Resume)"` with `href="/practice"`
  3. **4-Card Telemetry Bar**:
     - Card 1: `"৭ দিনের স্ট্রিক"` with `Flame` and `"অধ্যয়ন স্ট্রিক"`
     - Card 2: `"১২৮টি প্রশ্ন সমাধান"` with `CheckCircle2` and `"প্রশ্ন সমাধান"`
     - Card 3: `"৮৬.৪% নির্ভুলতা"` with `Target` and `"নির্ভুলতা"`
     - Card 4: `"শীর্ষ ৫% শিক্ষার্থী"` with `Award` and `"জাতীয় পার্সেন্টাইল"`
  4. **Curated Journey Pathways**:
     - 4 cards with progress meters (`w-[68%]`, `w-[82%]`, `w-[45%]`, `w-[90%]`)
     - Titles: `"মাধ্যমিক (SSC) বোর্ড প্রস্তুতি"`, `"উচ্চ মাধ্যমিক (HSC) বিজ্ঞান"`, `"বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি"`, `"টিউশন ও স্কিল লেজার"`
  5. **3D STEM Virtual Labs Showcase**:
     - `"প্রক্ষেপক গতিবিদ্যা সিমুলেটর"` / `"Projectile Motion"`
     - `"৩ডি আণবিক জ্যামিতি ও সংকরায়ন"` / `"Molecular Geometry"`
     - `"ল্যাব চালু করুন"` modal triggers
     - Modals with `<PhysicsProjectileLab` and `<ChemistryMolecularViewer`
  6. **Live National Challenge Spotlight**:
     - `"আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড চ্যালেঞ্জ"`
     - `"জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬"`
     - `"countdown"` timer
     - `"৪,৮৫০+ প্রতিযোগী শিক্ষার্থী"`
     - `"লাইভ লবিতে যোগ দিন"` button linking to `/live-challenge`
  7. **Socratic AI Instant Solver Banner**:
     - `"যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন"`
     - `"সক্রেটিক টিউটর চালু করুন"` with `id="global-socratic-trigger"`
  8. **W3C Proof-of-Skill Certificate Showcase**:
     - `<ProofOfSkillCard certificate={SAMPLE_CERTIFICATE} />`
     - `<SocialShareButtons title="..." shareUrl="..." />` with LinkedIn and Facebook
  9. **Module Directory Link**:
     - Direct button/link to `/modules` with `"৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি"`
  10. **Payment Trust Bar**:
      - `bKash Verified`, `Nagad Verified`, `SSLCommerz`
  11. **Header**: Phase 122 Developer Architecture Note, zero emojis.

### 2.2 `frontend/src/pages/dashboard.tsx`
- Add Phase 122 Developer Architecture Note header.
- Confirm full functionality as the dedicated personal cockpit for enrolled students.

### 2.3 Backend Test Files
- Update Developer Architecture Note header in:
  - `backend/tests/test_phase98_flagship_ui_elevation.py`
  - `backend/tests/test_phase98_2_flagship_home_dashboard.py`
  - `backend/tests/test_phase78_modular_enterprise_modules.py`
  - `backend/tests/test_phase85_core_web_vitals_seo.py`

## 3. Verification & Safety Gates
1. Run Next.js production build (`npm run build`) -> Assert 0 errors across 26 pages.
2. Run Zero-Emoji sweep script -> Assert 0 violations across all 557+ files.
3. Run test discovery -> Assert 1,397/1,397 tests pass with 0 errors and 0 failures.
