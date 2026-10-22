<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
FILE:      specs/018-phase114-institutional-teacher-cockpit/plan.md
PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
PURPOSE:   Engineering roadmap for building the institutional portal service, teacher
           cockpit component, section analytics card, REST endpoints, and regression tests.
STANDARDS: UI/UX Pro Max, Pure Academic Design, Multi-Tenant Security, Strict Zero-Emoji
-->

# Implementation Plan: Phase 114 — Institutional White-Label Portal & Teacher Cockpit

## Implementation Roadmap

1. **Step 1: Institutional Portal Backend Service (`backend/app/services/institutional_portal_service.py`)**
   - Multi-tenant data structures: `institutions`, `sections`, `exams`, and `gradebooks`.
   - Seed premier Bangladeshi institutions (Notre Dame College, Dhaka College, Rajuk Uttara Model College).
   - Tenant isolation & subdomain resolver (`get_institution_by_subdomain`).
   - Exam authoring, scheduling, and publication (`publish_exam`).
   - Gradebook management and grade approval (`approve_grades`).
   - Section analytics calculator: mean, median, standard deviation, and weak topic clusters.

2. **Step 2: Section Analytics Card Component (`frontend/src/components/institution/SectionAnalyticsCard.tsx`)**
   - Pure Academic visual design with Oxford Navy and Ivory surfaces.
   - Bell curve / distribution bar visualization of score spreads without individual shaming.
   - Weak topic diagnostic cluster indicators with constructive remediation suggestions.
   - Tabular 'Inter' numbers for metrics and 'Hind Siliguri' for academic advice.

3. **Step 3: Institutional Teacher Cockpit Dashboard (`frontend/src/components/institution/InstitutionalTeacherCockpit.tsx`)**
   - High-contrast console with 4 primary tabs:
     1. Active Exams (সক্রিয় মডেল টেস্ট ও সময়সূচী)
     2. Section Grade Book (শাখার গ্রেড বুক ও নম্বর অনুমোদন)
     3. Question Paper Creator (প্রশ্নপত্র প্রণয়ন ও প্রকাশ)
     4. Student Roster (শিক্ষার্থী তালিকা ও হাজিরা)
   - Tactile 3D Oxford Navy buttons: "পরীক্ষার প্রশ্ন প্রকাশ করুন" and "নম্বর অনুমোদন করুন".
   - Pure Lucide SVG vector icons (`School`, `Users`, `GraduationCap`, `FileCheck`, `BarChart3`).

4. **Step 4: REST API Endpoints (`backend/app/api/v1/endpoints/institution.py`)**
   - `GET /institution/resolve-tenant`: Resolves subdomain or tenant ID.
   - `GET /institution/{institution_id}/sections`: List sections.
   - `GET /institution/{institution_id}/exams`: List active and past exams.
   - `POST /institution/{institution_id}/exams`: Author and schedule new exam.
   - `POST /institution/{institution_id}/exams/{exam_id}/publish`: Publish exam.
   - `GET /institution/{institution_id}/sections/{section_id}/gradebook`: Gradebook and analytics.
   - `POST /institution/{institution_id}/sections/{section_id}/approve-grades`: Approve grades.
   - Mount router into `backend/app/api/v1/router.py`.

5. **Step 5: Automated Test Suite (`backend/tests/test_phase114_institutional_teacher_cockpit.py`)**
   - Test multi-tenant isolation, exam authoring/publishing, grade calculations, weak topic aggregation, and developer architecture notes with zero emojis.

6. **Step 6: Platform Regression Discovery & Certification**
   - Run `python3 -m unittest discover -s backend/tests` to assert 100% pass rate.
   - Run security and zero-emoji sweeps.
