# Specification: Phase 122 — Dual-Surface Unification & Test Regression Healing

## 1. Context & Objective
Following the Phase 120 grand rollout and subsequent design elevations, 10 legacy assertions across 4 test suites (`test_phase98_flagship_ui_elevation.py`, `test_phase98_2_flagship_home_dashboard.py`, `test_phase78_modular_enterprise_modules.py`, and `test_phase85_core_web_vitals_seo.py`) failed because semantic anchors and legacy student dashboard telemetry cards had been decoupled from the flagship public landing surface (`index.tsx`).

The goal of Phase 122 is to unify both surfaces: ensuring `index.tsx` serves as a comprehensive, prestigious, and interactive public portal that also incorporates all required semantic elements (study streak, solved questions, live challenge countdown, socratic solver, W3C certificate showcase, 3D STEM labs, modules directory link, and SEO metadata), while `dashboard.tsx` remains the dedicated personal cockpit for enrolled students.

## 2. Requirements & Verification Matrix

### 2.1 SEO & Metadata (`test_phase85_core_web_vitals_seo.py`)
- `AppHead` on `index.tsx` must specify:
  - `title="অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা"` (or contain this exact substring)
  - `canonicalUrl="/"`, `ogType="website"`
  - `structuredData={createOrganizationSchema()}`

### 2.2 Hero & Journey Guidance (`test_phase98_2_flagship_home_dashboard.py`)
- Hero section must include:
  - `"স্বাগতম, ভবিষ্যৎ গড়ার"` and `"অগ্রযাত্রায়"`
  - Stage chips: `"মাধ্যমিক (SSC ৯-১০)"`, `"উচ্চ মাধ্যমিক (HSC ১১-১২)"`, `"বিশ্ববিদ্যালয় ভর্তি (Admission)"`, `"টিউশন ও ক্যারিয়ার (Career)"`
  - Quick resume CTA: `"পড়াশোনা শুরু করুন (Quick Resume)"` linking to `/practice`

### 2.3 Academic Telemetry Grid (`test_phase98_2_flagship_home_dashboard.py` & `test_phase98_flagship_ui_elevation.py`)
- 4-card telemetry bar containing:
  - 1. Study Streak: `"অধ্যয়ন স্ট্রিক"` / `"৭ দিনের স্ট্রিক"` with `Flame` icon
  - 2. Solved Questions: `"১২৮টি প্রশ্ন সমাধান"` / `"প্রশ্ন সমাধান"` with `CheckCircle2` icon
  - 3. Accuracy Rate: `"৮৬.৪% নির্ভুলতা"` / `"নির্ভুলতা"` with `Target` icon
  - 4. National Percentile: `"শীর্ষ ৫% শিক্ষার্থী"` / `"জাতীয় পার্সেন্টাইল"` with `Award` icon

### 2.4 Curated Journey Pathways (`test_phase98_2_flagship_home_dashboard.py`)
- 4 pathway cards with progress bars:
  - SSC: `"মাধ্যমিক (SSC) বোর্ড প্রস্তুতি"`, `"৬৮% সম্পন্ন"`, `w-[68%]`, `/learn?stage=SSC`
  - HSC: `"উচ্চ মাধ্যমিক (HSC) বিজ্ঞান"`, `"৮২% সম্পন্ন"`, `w-[82%]`, `/learn?stage=HSC`
  - Admission: `"বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি"`, `"৪৫% সম্পন্ন"`, `w-[45%]`, `/admission`
  - Tuition/Career: `"টিউশন ও স্কিল লেজার"`, `"৯০% প্রোফাইল"`, `w-[90%]`, `/tuition`

### 2.5 3D STEM Virtual Labs Showcase
- Must include:
  - `"প্রক্ষেপক গতিবিদ্যা সিমুলেটর"` and `"Projectile Motion"`
  - `"৩ডি আণবিক জ্যামিতি ও সংকরায়ন"` and `"Molecular Geometry"`
  - `"ল্যাব চালু করুন"` modal trigger
  - `activeLabModal` state
  - `<PhysicsProjectileLab` and `<ChemistryMolecularViewer`

### 2.6 Live National Challenge Spotlight
- 8:00 PM National Challenge card with countdown:
  - `"আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড চ্যালেঞ্জ"`
  - `"জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬"`
  - `"countdown"` timer state
  - `"৪,৮৫০+ প্রতিযোগী শিক্ষার্থী"`
  - `"লাইভ লবিতে যোগ দিন"` CTA linking to `/live-challenge`

### 2.7 Socratic AI Instant Solver Banner
- 1-click solver trigger:
  - `"যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন"`
  - `"সক্রেটিক টিউটর চালু করুন"`
  - Element with `id="global-socratic-trigger"`

### 2.8 W3C Proof-of-Skill Certificate Showcase
- Verified certificate display:
  - `ProofOfSkillCard`
  - `SocialShareButtons` (`LinkedIn`, `Facebook`)
  - Sample cert ID `"OGRO-2026-F982A1B4"`
  - Student `"তানজিম হাসান"`
  - Verification link to `/verify/`

### 2.9 Enterprise Module Directory Link (`test_phase78_modular_enterprise_modules.py`)
- `index.tsx` must link to `/modules` directory with label `"৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি"` / `"মডিউল ডিরেক্টরি"`.

### 2.10 Payment Trust & Standards
- `bKash Verified`, `Nagad Verified`, `SSLCommerz` seals.
- Standardized Developer Architecture Note at top of all target files.
- Strict Zero-Emoji compliance certified.
