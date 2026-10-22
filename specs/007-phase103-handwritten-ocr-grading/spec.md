<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 103 Handwritten Script OCR & Step-by-Step Rubric Grader
FILE:      specs/007-phase103-handwritten-ocr-grading/spec.md
PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
PURPOSE:   Establishes functional specifications for automated handwritten exam script
           ingestion, multi-modal vision OCR, step-by-step NCTB rubric evaluation,
           and compassionate teacher-caliber feedback.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
-->

# Specification: Phase 103 — Handwritten Script OCR & Step-by-Step Rubric Grader

## Feature Directory
`specs/007-phase103-handwritten-ocr-grading`

## 1. Problem Statement
Traditional online examination platforms in Bangladesh are limited to multiple-choice questions (MCQs), leaving creative, descriptive, and mathematical problem-solving unchecked. When students solve physics or higher mathematics problems on paper, they write freehand Bengali steps with complex mathematical equations. Existing automated grading tools either fail to parse mixed Bengali-LaTeX script or output robotic, punitive error lists without empathetic pedagogy. Students need a compassionate, teacher-style step-by-step rubric grader that parses handwritten scripts, identifies partial credits (formula application, substitution, calculation), and provides kind pedagogical hints with KaTeX math corrections.

## 2. Goals & User Stories
### US1: Handwritten Exam Paper Capture & Preview (P1)
- As a student, I want to capture or drag-and-drop a photo of my written math/physics answer script with instant contrast enhancement preview, so that I can easily submit my paper.
- Acceptance Criteria:
  - Drag-and-drop container (`border-2 border-dashed border-blue-300 dark:border-blue-800 rounded-3xl bg-blue-50/30 hover:bg-blue-50/60 transition-all`).
  - Instant mobile-first camera capture trigger and high-contrast preview filter.
  - 3D tactile submission button ("খাতা জমা দিন") with physical depth (`shadow-[0_4px_0_0_#1D4ED8]`).

### US2: Compassionate Step-by-Step Grading Feedback (P1)
- As a student, I want to see my answer script graded like an affectionate senior teacher's marking with clear step breakdown badges and gentle margin notes.
- Acceptance Criteria:
  - Step point badges: e.g. "ধাপ ১: সূত্র প্রয়োগ — ১/১", "ধাপ ২: মান বসানো — ১/১", "ধাপ ৩: ক্যালকুলেশন — ০.৫/১".
  - Kind Bengali pedagogical guidance explaining exactly where calculation drift occurred.
  - Full KaTeX mathematical formula corrections.

### US3: Multi-Modal OCR Rubric Grader Service & API (P1)
- As an educational platform, we must evaluate student handwritten scripts against official NCTB marking rubrics with partial credit calculations.
- Acceptance Criteria:
  - Backend service `ocr_rubric_grader_service.py` evaluating formula selection, substitution, arithmetic, and units.
  - REST endpoint `POST /api/v1/grading/submit-script` and `GET /api/v1/grading/rubrics`.
  - Full automated tests in `test_phase103_handwritten_ocr_grading.py`.
