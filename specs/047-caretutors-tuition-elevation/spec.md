# Spec: CareTutors Reverse Engineering & Deep Tuition Marketplace Elevation

## 1. Executive Summary
This specification defines the deep elevation of **Ogrojatra's Tuition Marketplace** (`frontend/src/pages/tuition.tsx`), incorporating the full feature set and UX patterns reverse-engineered from Bangladesh's leading tutor matching platform, **CareTutors** (`https://caretutors.com`).

### Strict Identity & Asset Isolation Rules
- **ZERO CareTutors Branding:** The target's company name ("CareTutors"), logos, trademarks, and metadata are strictly excluded.
- **ZERO Scraped Images:** No external tutor photos or guardian pictures from CareTutors will be scraped or used. All visual identities are created using authentic procedural Scholar Monograms with university color accents and pure Lucide SVG iconography.
- **Branding Alignment:** Fully branded under **অগ্রযাত্রা ভেরিফায়েড টিউশন নেটওয়ার্ক** using our Oxford Academic Navy (`#0A2540`), Paper Ivory (`#FAF8F3`), and Academic Emerald (`#065F46`).

---

## 2. REA Discoveries from CareTutors Architecture

### 2.1 Tuition Categories & Streams
1. **Bangla Medium:** Class 1-12, SSC, HSC, Alim/Dakhil
2. **English Version (NCTB):** National Curriculum in English medium (Class 1-12)
3. **English Medium:** Cambridge (CAIE) & Edexcel (IGCSE, O-Level, A-Level)
4. **Religious Studies:** Quran recitation (Tajweed), Arabic language, Islamic Studies
5. **Admission Test:** Engineering (BUET/CKRUET), Medical, University (DU/GST), IBA
6. **Arts & Cultural:** Fine arts, drawing, guitar, vocal music, piano
7. **Language Learning:** Spoken English, IELTS, Arabic, German, French
8. **Special Child Education:** Autism, ADHD, dyslexia, personalized care
9. **University Assistance & Professional Skills:** BBA, Engineering Mathematics, Coding, Data Analysis

### 2.2 Tuition Modes
- **Home Tutoring:** One-on-one teaching at student's residence.
- **Online Tutoring:** Live interactive virtual classes anywhere across Bangladesh or abroad.
- **Group Tutoring:** 3-5 students batch study at a localized study center.
- **Package Tutoring:** Specific exam preparation crash course (e.g. 3-month HSC Physics revision).
- **Shadow Tutoring:** Daily school follow-up, homework assistance, and executive functioning support.

### 2.3 Core Operational Workflows
1. **Guardian Flow ("টিউটর প্রয়োজন? রিকোয়ারমেন্ট দিন"):**
   - Step 1: Mode & Medium selection.
   - Step 2: Class, curriculum, and specific subjects.
   - Step 3: Days per week (2-5 days), monthly salary budget, preferred tutor gender (পুরুষ/মহিলা/যেকোনো), preferred tutor institution (যেমন: বুয়েট/ঢাবি/মেডিকেল).
   - Step 4: District, Thana, specific address, guardian phone, and special requirements.
   - Outcome: Generated Job ID (e.g. `TUI-9104`), instant notification to matching verified tutors.
2. **Tutor Flow ("টিউশন খুঁজুন / জব বোর্ড"):**
   - Live job listings with detailed job card: Job ID, Class, Medium, Subjects, Area/Thana, Salary, Days/week, Gender preference, Number of applicants.
   - 1-click apply with custom cover note and trial availability.
3. **Trust & Safety Engine:**
   - 4-Tier Verification: NID, University ID, Certificate verification, Bilateral Phone Consent.
   - 2 Days Free Trial: Free trial classes for mutual compatibility check before commitment.
   - Zero Advance Scam Guarantee: Guardians pay no registration fee; tutors pay no unverified advance commission.
   - Escrow Milestone Protection: Security for tuition fees via milestone escrow.

---

## 3. Scope Lock & Non-Goals

### 3.1 Non-Goals
- Do not alter existing authentication or token validation routines.
- Do not modify existing API client fallback mechanisms (`apiClient.getTuitionListings`).
- Do not touch unrelated pages (`live-challenge.tsx`, `practice.tsx`, `admin/`).

### 3.2 In-Scope Additions
- `frontend/src/components/tuition/data/tuitionElevationData.ts`: Central typed datasets.
- `frontend/src/components/tuition/TutorRequestWizardModal.tsx`: Guardian 4-step request wizard.
- `frontend/src/components/tuition/TuitionJobBoard.tsx`: Rich job board with filters and apply modal.
- `frontend/src/components/tuition/VerifiedTutorDirectory.tsx`: Directory of verified tutors with filters and consent flow.
- `frontend/src/components/tuition/TuitionSalaryCalculator.tsx`: Interactive salary calculator.
- `frontend/src/components/tuition/TuitionTrustAndSafetySection.tsx`: Verification, trial, and escrow explanation.
- `frontend/src/components/tuition/TuitionCategoryPills.tsx`: Stream switcher.
- Update `frontend/src/pages/tuition.tsx`: Master integration with tab switcher and stats banner.

---

## 4. User Stories & Acceptance Criteria

### User Story 1 (P1 - Guardian Requests a Tutor)
*As a guardian in Dhanmondi,*  
*I want to submit my child's Class 10 Higher Math tutor requirement through a simple step-by-step wizard,*  
*So that I receive 3-5 verified tutor profiles from top universities within 24-48 hours.*

- **Acceptance Criteria:**
  - **Given** the guardian opens the request wizard,
  - **When** they fill Medium, Class, Subjects, Budget, Days/Week, and Location,
  - **Then** a verified job requirement is registered, a unique Job ID is created, and confirmation is presented without upfront fee demands.

### User Story 2 (P2 - Tutor Explores Job Board & Applies)
*As a university student looking for tuitions,*  
*I want to browse live tuition jobs by district, class, and salary,*  
*So that I can apply to relevant openings matching my academic department.*

- **Acceptance Criteria:**
  - **Given** the tutor views the Job Board tab,
  - **When** they filter by district (e.g. ঢাকা) or medium (e.g. ইংলিশ ভার্সন),
  - **Then** only matching open tuition jobs are displayed with real salary numbers and days per week.

### User Story 3 (P3 - Salary Transparency & Calculator)
*As a parent or tutor unsure of market tuition fees,*  
*I want to calculate expected tuition salary based on area, class, and days per week,*  
*So that both parties agree on a fair, standard academic remuneration.*

- **Acceptance Criteria:**
  - **Given** the user selects District: ঢাকা, Class: এইচএসসি, Medium: বাংলা মাধ্যম, Days: ৩ দিন/সপ্তাহ,
  - **Then** the calculator outputs the exact recommended monthly salary range (e.g. `৮,০০০ - ১০,৫০০ টাকা/মাস`).
