# Feature Specification: 048-bdjobs-career-elevation
# Module: Bdjobs-Class Career & Employment Ecosystem Integration (অন্বেষণ ও কর্মসংস্থান হাব)

## 1. Overview & Context
This specification codifies the complete reverse-engineering of Bangladesh's premier job portal, Bdjobs (`https://bdjobs.com/h/`), and elevates our student/graduate platform ("Ogrojatra") with an enterprise-grade Career & Employment Hub (`/career`).

It bridges academic credentials, sealed cryptographic CV snapshots, verified skills portfolios, and real-world employment across Bangladesh (corporate, tech, NGO, government circulars, vocational, and internships).

## 2. Brand & Asset Isolation Principles (Mandatory)
- **Zero Trademark Violation:** No Bdjobs trademarks, copyrighted logos, or scraped external headshots.
- **Procedural Enterprise Branding:** Industry & corporate monograms with authentic Bangladesh institutional colors (Navy `#0A2540`, Crimson `#9E1B32`, Forest `#0F5132`, Amber `#B45309`, Slate `#1E293B`).
- **Zero-Emoji Policy:** 100% strict adherence to Lucide React SVG vector icons only. No raw Unicode emojis in code, comments, or UI.
- **Academic Palette Alignment:** Strict adherence to Phase 115 Oxford Navy `#0A2540`, tactile buttons (`active:translate-y-`, `active:shadow-none`), and zero fluorescent AI-gradients (`bg-clip-text`, `bg-gradient-to-r`).

## 3. User Stories
- **US1 (Job Seeker / Student):** As a student or fresher graduate, I want to search and filter jobs by functional category, division/district, job nature (internship, entry-level, full-time), organization type (Govt, Corporate, NGO), and salary bracket so that I can quickly find matching opportunities.
- **US2 (Job Detail & Application):** As a candidate, I want to inspect a complete Bdjobs-grade job description (responsibilities, qualifications, salary, benefits, deadline countdown) and submit an online application with my expected salary, priority note, and sealed SHA-256 CV snapshot.
- **US3 (ATS & Application Tracker):** As an applicant, I want to track my application progress across distinct stages (Applied, Under Review, Shortlisted, Interview Scheduled, Offer) with immutable tracking IDs (`OGRO-APP-XXXXX`).
- **US4 (Bdjobs Pro CV Builder):** As a jobseeker, I want an interactive CV builder with completeness percentage score, structured tabs (Personal, Academics, Skills with evidence, Work experience), and PDF-ready formatting.
- **US5 (Recruiter / Employer Suite):** As an employer, I want a 4-step job posting wizard to publish vacancies and a candidate review pipeline to shortlist or schedule interviews.
- **US6 (Govt Circulars & Career Guidance):** As a candidate preparing for BCS and government exams, I want official government job circular notifications, salary insights, and an interview preparation guide.

## 4. Acceptance Criteria
- [x] All 8 Divisions of Bangladesh and key job categories (IT, Finance, Engineering, Govt, NGO, Skills) filterable with live counts and active badge chips.
- [x] Responsive Job Board with urgency badges, salary chips, and detail modal.
- [x] Complete 4-step Employer Job Posting wizard with client-side validation.
- [x] Seamless integration with existing `career.tsx` backward-compatibility invariants (`latestSealedSnapshot`, `cvSnapshotId`, `SHORTLISTED`, `apiClient.getCareerProfile`, `animate-pulse`, `#0A2540`).
- [x] Zero emoji violations verified across the codebase.
- [x] Unit tests and Playwright E2E tests written and 100% passing.
