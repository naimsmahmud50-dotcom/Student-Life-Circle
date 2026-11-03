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

### Phase 1: Flagship Homepage (`frontend/src/pages/index.tsx`)
1. **Section 1: Editorial Hero**
   - NCTB Accreditation Chip & 3D Toggle label
   - Welcome subtitle & 4-in-1 application alternative badge
   - Main headline and secondary mission statement
   - Stage selector chips (SSC, HSC, Admission, Career)
   - Primary and outline Call-to-Action buttons
   - 4-item Trust Strip (NCTB syllabus, 10-year board questions, offline mesh sync, no hidden fees)
2. **Section 1.5: 4-in-1 Platform Disruption Grid**
   - 10 Minute School alternative (3D virtual labs vs passive video)
   - Live MCQ alternative (Cheating-proof Olympiad vs static tests)
   - Careertutors alternative (Zero commission tuition vs 50% cuts)
   - Bdjobs alternative (W3C verifiable cryptographic credentials vs paper CVs)
3. **Section 2: Academic Progress & Pedagogical Pillars**
   - Daily study goals, continuous learning streak, board syllabus completion tracker
   - 3 Pedagogical Pillars (Spaced repetition, concept mastery, doubt resolution)
4. **Section 3: Curated Journey Pathways**
   - 4 stage pathways (Secondary SSC, Higher Secondary HSC, University Admission, Professional Career)
5. **Section 4: 3D STEM Virtual Labs**
   - Physics Lab (Screw Gauge, Vernier Caliper, Pendulum)
   - Chemistry Lab (Titration, Acid-Base balance, Reaction kinetics)
6. **Section 5: Live Challenge & Socratic AI Instant Solver**
   - Live MCQ countdown timer, active participants, instant solver drawer trigger
7. **Section 6: W3C Proof-of-Skill Certificate Showcase**
   - Verifiable credential preview, cryptographic hash, QR verification
8. **Section 6.5 & 7: Testimonials, Trust Badges, & 69 Modules Directory**
   - Student success stories, ISO/OWASP compliance seals, national education directory
9. **Section 8: Closing Academic Call to Action**
   - Final join banner, registration CTA, community statistics

---

## 4. Architectural & Governance Invariants
1. **Strict Zero-Emoji Policy**: Zero emojis in all code, text dictionaries, comments, and commits.
2. **Backward Compatibility**: All Bengali string literals tested by backend suites (e.g. `backend/tests/test_phase98_2_flagship_home_dashboard.py`) must be retained directly in the code to ensure 100% test passing.
3. **Sub-Pixel Legibility**: Bengali font rules apply when `isBengali` is true; English typography defaults to `Inter` / `sans` when false.
