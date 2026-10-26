# Technical Architecture Plan: 048-bdjobs-career-elevation
# Module: Bdjobs-Class Career & Employment Ecosystem Integration

## 1. Architectural Strategy
We construct a modular, componentized architecture under `frontend/src/components/career/` while maintaining full backward-compatibility in `frontend/src/pages/career.tsx`.

```
frontend/src/components/career/
├── data/
│   └── careerElevationData.ts        # Typed datasets: categories, locations, sample jobs, salary benchmarks, govt circulars
├── CareerStatsHeader.tsx              # Top metric ticker: 8,450+ live jobs, 1,200+ companies, govt circulars, free CV builder
├── CareerSearchFilterBar.tsx          # Keyword search, division, category, job nature, salary, and active filter chips
├── CareerCategoryGrid.tsx             # Functional & Special Skill categories with job counts
├── CareerJobBoard.tsx                 # Live job feed, sort by deadline/salary, urgent badge, detail modal & apply flow
├── JobDetailModal.tsx                 # Full Bdjobs-grade job spec: summary table, qualifications, benefits, company info
├── JobApplyModal.tsx                  # Online apply with expected salary, priority note, sealed CV snapshot
├── CareerATSApplicationPipeline.tsx   # Jobseeker tracker: Applied, Viewed, Shortlisted, Interview, Offer
├── BdjobsProCvBuilderModal.tsx        # Profile completeness gauge (85%), 5-section CV generator & print layout
├── EmployerJobPostingWizardModal.tsx  # 4-step job posting wizard for recruiters (Role, Criteria, Compensation, Review)
├── GovtCircularsAndCareerGuide.tsx    # Govt job circular archives, salary benchmarks, interview tips
└── index.ts                           # Barrel export
```

## 2. Data Models & TypeScript Interfaces
- `CareerJob`: id, title, companyName, companyLogoMonogram, companyIndustry, category, orgType, jobNature, jobLevel, vacancy, locationDistrict, locationDivision, minSalary, maxSalary, isSalaryNegotiable, deadline, publishedDate, experienceYears, educationRequirements, responsibilities, benefits, isHotJob, isEarlyAccess, applicantsCount.
- `JobApplication`: id, jobId, companyName, role, appliedDate, stage, cvSnapshotId, expectedSalary, priorityNote, interviewDetails.
- `GovtCircular`: id, title, ministryOrDepartment, totalPosts, applicationDeadline, circularPdfUrl, officialWebsite.
- `SalaryBenchmark`: industry, roleTitle, entryLevelSalary, midLevelSalary, seniorLevelSalary.

## 3. Backward Compatibility & Test Invariants
- `frontend/src/pages/career.tsx` must preserve:
  - Header: `DEVELOPER ARCHITECTURE NOTE: ... Phase 115`
  - Document Title: `দক্ষতা প্রমাণ ও ক্যারিয়ার হাব (Career Portfolio) | অগ্রযাত্রা`
  - Variables/Strings: `latestSealedSnapshot`, `cvSnapshotId`, `SHORTLISTED`, `apiClient.getCareerProfile`, `animate-pulse`, `#0A2540`, `active:translate-y-`, `active:shadow-none`.
- Zero Emoji policy: strictly Lucide icons only.

## 4. Verification Plan
- Unit tests with `node --test` for career helper functions and data consistency.
- Python zero-emoji sweep script `python3 backend/scripts/run_zero_emoji_sweep.py`.
- Playwright E2E test `frontend/e2e/career_elevation.spec.ts`.
- Next.js production build `npm --prefix frontend run build`.
- Backend regression test suite `python3 -m unittest discover -s backend/tests -p "test_*.py"`.
