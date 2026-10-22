<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
FILE:      specs/018-phase114-institutional-teacher-cockpit/spec.md
PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
PURPOSE:   Specifies the multi-tenant white-label institutional management system,
           custom subdomain routing (e.g. ndc.ogrojatra.edu.bd), teacher RBAC controls,
           central exam scheduling, section-wide analytics, and high-contrast gradebooks.
STANDARDS: UI/UX Pro Max, Pure Academic Design, Multi-Tenant Security, Strict Zero-Emoji
-->

# Feature Specification: Phase 114 — Institutional White-Label Portal & Teacher Cockpit

## 1. Overview
The Institutional White-Label Portal & Teacher Cockpit equips schools, colleges, and madrasahs across Bangladesh (e.g. Notre Dame College, Dhaka College, Rajuk Uttara Model College, Viqarunnisa Noon School & College) with dedicated institutional administration tools. 

The system features:
- **Multi-Tenant White-Label Partitioning**: Custom subdomain support (e.g., `ndc.ogrojatra.edu.bd`, `dc.ogrojatra.edu.bd`), institutional branding, and strict tenant-scoped data isolation.
- **Teacher Role-Based Access Control (RBAC)**: Verified teacher privileges to author section-specific model tests, assign deadlines, and approve grades.
- **Section Gradebook & Analytics**: Aggregates average scores, standard deviation, and weak topic clusters without public shaming.
- **Pure Academic Visual Language**: Oxford Navy (`#0A2540`), Scholarly Gold (`#B45309`), Paper Ivory (`#FAFAF8`), generous whitespace, tabular numbers, and tactile 3D Oxford Navy buttons.

## 2. Functional Requirements
- **Tenant Management**:
  - Institutional profiles with unique `institution_id`, legal name, Bengali name, custom domain/subdomain, and active section roster.
  - Strict tenant data partitioning: Teachers and students can only access exams, sections, and gradebooks within their tenant.
- **Central Exam Authoring & Scheduling**:
  - Teachers create model tests by selecting subjects, papers, chapters, question counts, duration (minutes), and due dates.
  - Exam publishing workflow: Teachers trigger "পরীক্ষার প্রশ্ন প্রকাশ করুন" (`PUBLISHED`).
- **Section Gradebook & Score Approval**:
  - Section-level rosters with roll numbers, student names, submitted scores, and feedback.
  - Teachers approve finalized grades with "নম্বর অনুমোদন করুন" (`GRADES_APPROVED`).
- **Section Performance Analytics**:
  - Calculates mean score, median, standard deviation, and identifies weak topic clusters (e.g., "ক্যালকুলাস - যৌগিকরণ", "তড়িৎ রসায়ন") without individual public shaming.
- **Design & Typography Mandate**:
  - Zero AI vibe (no flashy neon cards, confusing gradients, or childish badges).
  - 'Hind Siliguri' for Bengali student notes; 'Inter' tabular numbers for marks and statistics.
  - Tactile 3D Oxford Navy buttons (`shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none`).
  - Zero Emoji: Pure Lucide SVG vector icons (`School`, `Users`, `GraduationCap`, `FileCheck`, `BarChart3`).
