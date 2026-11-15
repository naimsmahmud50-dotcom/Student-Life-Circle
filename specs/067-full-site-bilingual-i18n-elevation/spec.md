# Feature Specification: Full-Site Bilingual (BN/EN) Internationalization Elevation

## 1. Overview & Objective
Enable comprehensive, instant bilingual translation across the Student Life Circle (অগ্রযাত্রা) flagship web application. 
When the user selects **BN**, the entire site displays in authentic, academic Bengali (retaining 100% of the current text and layout).
When the user selects **EN**, the entire site displays in authoritative, natural English in the exact same positions, cards, and buttons without altering a single CSS class, grid structure, border, color, or visual element.

---

## 2. User Stories & Acceptance Criteria

### User Story 1: Seamless Instant Language Toggle
- **As a** student or visitor,
- **I want to** toggle between Bengali (**BN**) and English (**EN**) in the header or footer,
- **So that** all page content (hero, features, interactive labs, routines, cards, and buttons) instantaneously switches to my selected language without a full page reload.

#### Acceptance Criteria:
1. **Given** the user is viewing the homepage in Bengali (`locale === 'bn'`),
   **When** the user clicks **EN** in the Navbar or Footer language switcher,
   **Then** all headings, descriptions, badges, button labels, and card contents switch to English immediately.
2. **Given** the user is viewing the homepage in English (`locale === 'en'`),
   **When** the user clicks **BN**,
   **Then** all content switches back to the original authentic Bengali immediately.
3. **Given** the user sets their preference to **EN**,
   **When** they refresh the page or navigate to another page,
   **Then** the application remembers their English selection via `localStorage` and renders in English.

---

### User Story 2: 100% Visual and Layout Preservation (Zero Breakage)
- **As the** platform creator,
- **I want** the design, styling, colors, layout, animations, and card boundaries to remain 100% identical,
- **So that** changing languages does not disrupt, distort, or break any existing UI or aesthetic styling.

#### Acceptance Criteria:
1. **Given** any section or card on the homepage,
   **When** toggled between BN and EN,
   **Then** no CSS classes are modified, removed, or added other than the dynamic text content inside elements.
2. **Given** numerical counters, timestamps, or scores,
   **When** in BN, they format using authentic Bengali numerals (`০-৯`);
   **When** in EN, they format using Western Arabic numerals (`0-9`).

---

## 3. Scope & Coverage

### Phase 1: Flagship Core Routes
1. `index.tsx`: Editorial Hero, 4-in-1 Platform Comparison, 3D STEM Virtual Labs, National Live Challenge, W3C Cryptographic Certificates, Testimonials, National Directory.
2. `live-challenge.tsx`: Live MCQ Arena, Category Track Selector, OMR Simulator, Leaderboard, Routine Matrix.
3. `learn.tsx`: NCTB Curriculum Hub, Spaced Repetition Queue, Video Drawer, Subject Matrix.
4. `admission.tsx`: Battleground Hub, Target Blueprints (DU, BUET, Medical), Counseling Cascade.
5. `tuition.tsx`: Match & Escrow Milestone Hub, Verified Teacher Cards, Consent Modal.
6. `career.tsx`: Career Radar, Sealed Cryptographic CV Snapshot, ATS Application Pipeline.
7. `auth.tsx`: Minor-Safe Onboarding, SMS OTP Verification, Identifier & Password.
8. `dashboard.tsx`: Personalized Bento Grid, 3D Lab Launchers, Live Challenge Radar.
9. `practice.tsx`: Practice Exam Arena, Adaptive Quiz, Socratic AI Solver Drawer.

### Phase 2: Full-Site Comprehensive Elevation (100% of 43 Routes)
1. **Error & System Resilience**: `404.tsx` (Not Found), `500.tsx` (Server Error), `offline.tsx` (IndexedDB PWA fallback).
2. **Public & Trust**: `about.tsx` (Pedagogical Mission & Editorial Board), `terms.tsx` (Legal & Compliance Framework).
3. **Academic Simulators & Archives**: `board-archives.tsx`, `admission/predictor.tsx`, `olympiad/arena.tsx`, `socratic/solver.tsx`, `viva/evaluator.tsx`.
4. **Governance, Dispute & Financial**: `achievements.tsx`, `guardian.tsx`, `guardian/ptc.tsx`, `tribunal/disputes.tsx`, `governance/board-gateway.tsx`, `scholarship/disbursement.tsx`.
5. **Career & Corporate Infrastructure**: `career/radar.tsx`, `counseling.tsx`, `recruiter.tsx`.
6. **Decentralized & Resilient Infrastructure**: `verify/[certId].tsx` (W3C Ed25519 Certs), `adaptive-exam.tsx` (CAT Engine), `emergency-mesh.tsx` (LoRa P2P Bridge), `rural/synchronizer.tsx` (SMS Sync), `study-pod.tsx` (Collaborative Canvas).
7. **Curriculum, Courses & Schedules**: `curriculum/lexicon.tsx`, `routines/index.tsx`, `modules.tsx` (69 Modular Packages), `courses.tsx`, `academic-hub.tsx`, `grading-demo.tsx`, `styleguide.tsx`.
8. **Security & Content Administration**: `admin/index.tsx`, `admin/quarantine.tsx`, `admin/review-queue.tsx`.

---

## 4. Architectural & Governance Invariants
1. **Strict Zero-Emoji Policy**: Zero emojis in all code, text dictionaries, comments, and commits. All iconography strictly Lucide-React SVG with `strokeWidth={1.75}`.
2. **Backward Compatibility**: All Bengali string literals tested by backend suites (e.g. `BAP-140`, `CRC-16-CCITT`, `shadow-[0_4px_0_0_#051329] active:translate-y-1`, `Hind_Siliguri`, `Inter`, `toBengaliDigits`, `৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি`) must be retained verbatim in the code to ensure 100% test passing.
3. **Sub-Pixel Legibility**: Bengali typography utilizes `Hind Siliguri` font; English typography defaults to `Inter` / `sans`.
4. **Zero Layout Shift (CLS < 0.05)**: Switching language does not alter grid structures, component boundaries, card dimensions, or CSS flex arrangements.

