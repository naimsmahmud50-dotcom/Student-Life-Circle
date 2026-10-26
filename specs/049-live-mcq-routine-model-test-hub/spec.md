# Spec: 049 - Live MCQ Routine & Mega Model Test Calendar Hub (লাইভ এমসিকিউ ও মডেল টেস্ট রুটিন হাব)

## 1. Problem Statement & Context
Bangladeshi competitive exam candidates (47th BCS Preliminary, Dhaka University & Varsity Admission, HSC Board) require a disciplined, day-by-day exam routine calendar with synchronized nation-wide Mega Model Tests. Currently, students face unstructured preparation without clear timeline projections, synchronized countdown timers, or realistic negative marking percentile calculations.

## 2. Goals & User Stories
- **P1: 200-Day Daily Routine Calendar**: As a student, I want to view a 200-day structured exam syllabus calendar with dates, subjects, topics, and question counts so that I can prepare systematically.
- **P1: Friday Mega Model Test Hub**: As an examinee, I want to participate in weekly synchronized Friday Mega Model Tests with a live countdown timer and live participant indicator.
- **P1: Automated Negative Marking & Percentile Distribution**: As a candidate, I want to calculate my net score with negative marking penalty (+1.0 / -0.25, -0.50) and view estimated merit percentile and rank projection.
- **P2: Routine Reminder Subscriptions**: As a user, I want to subscribe to routine reminders (In-app, Push) for specific exams so I never miss a model test.
- **P2: Weakness Breakdown & Syllabus Coverage**: As a student, I want to see subject-wise syllabus coverage bars and topic-level weakness flags.

## 3. Non-Goals
- Real-time WebRTC 3D multi-user avatars (reserved for `/live-challenge` 3D arena).
- Modifying core payment or subscription billing tables (free academic routine with optional push alerts).

## 4. Acceptance Criteria
1. Route `/routines` renders the modern academic routine calendar, countdown header, and filter tabs behind `FEATURE_EXAM_ROUTINE`.
2. When the feature flag is `false`, `/routines` gracefully renders the calm "শীঘ্রই আসছে - অগ্রযাত্রা শিডিউলার" banner.
3. Backend endpoints `/api/v1/routines` return routine lists, details, score simulation, and subscription status.
4. Database migration `017_exam_routine_and_model_test_rls.sql` is strictly additive with full rollback commands.
5. All 1,602 existing backend tests continue passing with zero regressions.
6. Zero emojis; WCAG 2.2 AAA compliant; responsive on mobile (360px), tablet (768px), and desktop (1440px).
