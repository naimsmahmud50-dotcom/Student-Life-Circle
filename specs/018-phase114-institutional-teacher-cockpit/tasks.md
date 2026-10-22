<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
FILE:      specs/018-phase114-institutional-teacher-cockpit/tasks.md
PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
PURPOSE:   Tracks deliverables for the multi-tenant institutional portal service,
           teacher cockpit component, section analytics card, REST endpoints, and regression tests.
STANDARDS: UI/UX Pro Max, Pure Academic Design, Multi-Tenant Security, Strict Zero-Emoji
-->

# Tasks: Phase 114 — Institutional White-Label Portal & Teacher Cockpit

## Tasks Ledger

- [x] Task 1: Implement Institutional Portal Service (`backend/app/services/institutional_portal_service.py`)
  - Multi-tenant school/college isolation with subdomain resolution (NDC, Dhaka College, Rajuk Uttara Model College)
  - Exam authoring, scheduling, and publication workflow with status transitions (DRAFT -> PUBLISHED)
  - Section gradebook retrieval and teacher score sign-off (PENDING_APPROVAL -> GRADES_APPROVED)
  - Statistical aggregation (mean, median, standard deviation $\sigma = 3.36$, 4-tier distribution brackets, weak topic clusters)
  - Strict tenant boundary security and zero emoji compliance

- [x] Task 2: Build Section Analytics Card Component (`frontend/src/components/institution/SectionAnalyticsCard.tsx`)
  - Pure Academic Oxford Navy (#0A2540) & Warm Ivory (#FAFAF8) visual language
  - Performance distribution histogram without public student ranking shaming
  - Diagnostic weak topic cluster breakdown with remedial pedagogical tips
  - Tabular Inter numbers, WCAG AAA contrast, and zero emojis

- [x] Task 3: Build Institutional Teacher Cockpit Dashboard (`frontend/src/components/institution/InstitutionalTeacherCockpit.tsx`)
  - 4-tab interface: Active Exams ("চলমান ও প্রকাশিত পরীক্ষা"), Section Grade Book ("শাখা গ্রেডবুক ও ডায়াগনস্টিক"), Question Paper Creator ("প্রশ্নপত্র সংকলন ও শিডিউলার"), Student Roster ("শিক্ষার্থী তালিকা ও হাজিরা")
  - 3D tactile Oxford Navy buttons: "পরীক্ষার প্রশ্ন প্রকাশ করুন" and "নম্বর অনুমোদন করুন" (`shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`)
  - Pure Lucide SVG icons (`School`, `Users`, `GraduationCap`, `FileCheck`, `BarChart3`)
  - Subdomain indicator (e.g. `ndc.ogrojatra.edu.bd`) and institutional EIIN badge

- [x] Task 4: Implement and Mount REST API Endpoints (`backend/app/api/v1/endpoints/institution.py`)
  - Endpoints: `GET /institution/resolve-tenant`, `GET /institution/{id}/sections`, `GET /institution/{id}/exams`, `POST /institution/{id}/exams`, `POST /institution/{id}/exams/{id}/publish`, `GET /institution/{id}/sections/{id}/gradebook`, `POST /institution/{id}/sections/{id}/approve-grades`, `GET /institution/{id}/sections/{id}/analytics/{id}`
  - Mounted router in `backend/app/api/v1/router.py`

- [x] Task 5: Implement Automated Unit & Integration Tests (`backend/tests/test_phase114_institutional_teacher_cockpit.py`)
  - Verified tenant isolation across institutions (e.g. NDC vs Dhaka College)
  - Verified teacher exam authoring and publication state transitions
  - Verified section analytics (mean 43.8, median 44.0, standard deviation 3.36, weak topics)
  - Verified Developer Architecture Notes and strict Zero-Emoji compliance (6/6 tests passing)

- [x] Task 6: Platform Regression Discovery & Certification
  - Run zero-emoji sweep: 531 files scanned, 0 violations found
  - Run security sweep: 294 files scanned, 0 critical/high/medium findings
  - Full platform regression test discovery: 1,354 / 1,354 tests passing in 5.269s (100% pass rate)
