# Spec: 10 Minute School (10MS) Reverse Engineering & Competitive Elevation

## 1. Executive Summary & Background
This specification defines the product and design elevation of **Ogrojatra** ("Student Life Circle") derived from deep reverse-engineering of Bangladesh's leading educational platform, **10 Minute School** (`https://10minuteschool.com`).

Our objective is to extract 10MS's highest-converting UX patterns, Bengali microcopy formulas, academic taxonomy, trust-building social proofs, and course/bundle card architectures, elevating Ogrojatra into a market-superior, academically dignified platform while preserving its Oxford/Cambridge visual rigor and strict zero-regression standards.

---

## 2. REA (Reverse Engineering) Key Discoveries from 10MS

### 2.1 Brand & Visual Identity Tokens
- **Primary Brand Green:** `#1CAB55` (RGB: `28, 171, 85`) — High-energy emerald green used for primary CTAs, active highlights, and success indicators.
- **Dark Ink Neutral:** `#111827` (Tailwind Gray 900) — Deep charcoal text color avoiding pure `#000000` harshness.
- **Surfaces & Borders:** `#F9FAFB` (Gray 50), `#F3F4F6` (Gray 100), `#E5E7EB` (Gray 200).
- **Urgency / Alert Red:** `#E63C3C` / `#E8001D` — Used for limited batch registration, discount tags, and live exam beacons.
- **Typography Pairing:**
  - Bengali Primary: `Anek Bangla` (with `Hind Siliguri` & `Noto Sans Bengali` fallback).
  - Latin & Numerals: `Inter` (with tabular figures for exam counters & timers).
  - Scientific Formulas: `KaTeX` (`KaTeX_Main`, `KaTeX_Math`, `KaTeX_SansSerif`).

### 2.2 Academic Segment Architecture
1. **K-12 Online Batches (ক্লাস ৬ - ১২ / এসএসসি ও এইচএসসি):**
   - Stream-based grouping: বিজ্ঞান বান্ডেল (Science Bundle), ব্যবসায় শিক্ষা ও মানবিক বান্ডেল (Business/Humanities Bundle), বাংলা-ইংরেজি-আইসিটি বান্ডেল।
   - Pedagogy Features: "সাপ্তাহিক লাইভ ক্লাস", "প্রিন্টেড মাস্টারবুক ও ক্লাস নোটস", "আনলিমিটেড MCQ প্র্যাকটিস", "হোমওয়ার্ক ও সাপ্তাহিক পরীক্ষা", "২৪ ঘণ্টা ডাউট সলভ (TenTen/SuperSolve)".
2. **University Admission (বিশ্ববিদ্যালয় ভর্তি ২০২৬):**
   - Varsity A Unit + গুচ্ছ (Science & Engineering)
   - Varsity B Unit + গুচ্ছ (Humanities & Social Sciences)
   - Varsity C Unit + গুচ্ছ (Business Studies)
   - Medical & Engineering specialized preparation tracks.
3. **Competitive Career & Job Recruitment (চাকরি প্রস্তুতি):**
   - বিসিএস প্রিলি (BCS Preliminary Course)
   - ব্যাংক জবস (Bank Jobs)
   - সরকারি চাকরি বেসিক ও প্রাথমিক সহকারী শিক্ষক নিয়োগ পরীক্ষা।
4. **Offline + Hybrid Learning Ecosystem:**
   - 5 Dedicated Offline English & Learning Hubs (উত্তরা, পান্থপথ, মিরপুর, মগবাজার, চট্টগ্রাম) with Google Maps integration and direct booking CTAs ("অফলাইন সেন্টারে ফ্রি ক্লাস করুন").
   - Offline-first catchup capability: *"পড়া চলবে ইন্টারনেট ছাড়াও"* (Downloadable lessons & offline reading notes).

### 2.3 Bengali Microcopy & Copywriting Formulas
- **Value Proposition:** *"এক জায়গায় স্কুল ও কলেজের সম্পূর্ণ প্রস্তুতি!"*
- **Autonomy & Pacing:** *"অনলাইনেই শেখা হোক নিজের গতিতে!"*
- **Anti-Anxiety Reassurance:** *"ক্লাস মিস? নো ইস্যু! রেকর্ডেড ক্লাস তো আছেই।"*
- **Offline Assurance:** *"পড়া চলবে ইন্টারনেট ছাড়াও — ইন্টারনেট কানেকশন ছাড়াও ডাউনলোড করে দেখতে পারবে রেকর্ডেড ক্লাস ও ক্লাস নোটস।"*
- **24/7 Academic Support:** *"২৪ ঘণ্টা ডাউট সল্ভের জন্য তোমার সার্বক্ষণিক স্টাডি পার্টনার।"*
- **Social Proof & Verified Ranks:** Real student profiles with institutional identity (e.g. *"বীরশ্রেষ্ঠ নূর মোহাম্মদ পাবলিক কলেজ"*, *"কমর আলী হাই স্কুল"*, *"৪৫তম বিসিএস প্রিলি উত্তীর্ণ"*).

---

## 3. Scope Lock & Non-Goals

### 3.1 Strict Boundaries (DO NOT TOUCH)
- **Zero changes to existing backend APIs, authentication, payment verification, database schema, or admin RBAC.**
- **Zero changes to existing Live Challenge exam scoring (-0.25 negative marking, server time sync, anti-cheat webcam proctoring).**
- **Zero changes to existing 40+ pages unless explicitly isolated in new components.**
- **All new styles must use scoped classes or modular components to prevent global CSS pollution.**

### 3.2 In-Scope Elevation Features
1. **`AcademicSegmentNav`**: A high-efficiency segment switcher supporting HSC, SSC, Admission (Varsity/Med/Eng), and BCS/Govt Jobs.
2. **`StudyBundleCard`**: 10MS-style academic course/bundle cards featuring subject checklists, printed notes tags, mock test counts, and clear call-to-actions.
3. **`OfflineAndDoubtSolvFeatureGrid`**: Highlighting 24/7 AI Doubt-Solving and Offline-First learning with Bengali reassurance copy.
4. **`VerifiedAchieverShowcase`**: Real academic student rank cards with verified institutional badges and score breakdowns.
5. **`AcademicHelplinePill`**: A non-intrusive 24/7 scholar assistance beacon floating widget.

---

## 4. User Stories & Acceptance Criteria

### User Story 1 (P1 - Fast Academic Navigation)
*As an HSC or Admission student visiting Ogrojatra,*  
*I want to quickly filter and explore my relevant academic batch (HSC Science, Admission GST, or BCS),*  
*So that I immediately find study materials, mock tests, and live challenge schedules tailored to my curriculum.*

- **Acceptance Criteria:**
  - **Given** the user lands on the academic hub,
  - **When** they click a segment tab (e.g., "এইচএসসি ২০২৭", "ভার্সিটি এডমিশন", "বিসিএস প্রিলি"),
  - **Then** the view instantly filters corresponding subject bundles without page reload or layout shift (CLS = 0.000).

### User Story 2 (P2 - Reassuring Educational Value & Offline Proof)
*As a rural student with intermittent internet connectivity in Bangladesh,*  
*I want clear confirmation that I can download study packs and practice quizzes offline without mobile data,*  
*So that I feel confident using the platform in low-bandwidth regions.*

- **Acceptance Criteria:**
  - **Given** the user views the feature highlight grid,
  - **When** they read the offline learning card,
  - **Then** they see the prominent assurance *"পড়া চলবে ইন্টারনেট ছাড়াও"* with direct action to open the offline PWA vault.

### User Story 3 (P3 - Verified Social Proof & Peer Trust)
*As an exam candidate,*  
*I want to see real success records of senior students from reputable colleges and universities,*  
*So that I can trust the rigor and accuracy of Ogrojatra's question bank and live challenges.*

- **Acceptance Criteria:**
  - **Given** the student reviews the achiever showcase,
  - **When** cards are displayed,
  - **Then** each card showcases the student's verified college/school, exam milestone, and specific score without exaggerated marketing claims.
