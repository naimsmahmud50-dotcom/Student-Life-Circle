<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Implementation Plan
TOPIC:     Technical Architecture for Handwritten Script OCR & Step-by-Step Rubric Grader
FILE:      specs/007-phase103-handwritten-ocr-grading/plan.md
PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
PURPOSE:   Architectural blueprint for handwritten image preprocessing, vision OCR integration,
           NCTB 4-step rubric grading algorithm, and affectionate teacher feedback UI.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
-->

# Technical Plan: Phase 103 Handwritten Script OCR & Step-by-Step Rubric Grader

## 1. Architectural Architecture
- **OCR Rubric Grader Service (`backend/app/services/ocr_rubric_grader_service.py`)**:
  - Implements multi-modal script evaluation against standard NCTB step rubrics:
    1. Step 1: Formula Identification & Principle (`সূত্র বা নীতি প্রয়োগ` - 1.0 mark)
    2. Step 2: Given Variable Substitution (`প্রদত্ত মান প্রতিস্থাপন` - 1.0 mark)
    3. Step 3: Arithmetic & Algebraic Calculation (`গাণিতিক বিশ্লেষণ ও হিসাব` - 1.0 mark)
    4. Step 4: Final Numerical Value & SI Units (`চূড়ান্ত উত্তর ও সঠিক একক` - 1.0 mark)
  - Calculates partial credit scores and flags minor slips with constructive guidance.
  - Normalizes Bengali-English mixed mathematical handwriting into LaTeX syntax.
- **REST Endpoints (`backend/app/api/v1/endpoints/grading.py`)**:
  - `POST /api/v1/grading/submit-script`: Ingests base64 or multipart image, evaluates against rubric, returns step breakdown.
  - `GET /api/v1/grading/rubrics`: Lists standard NCTB rubrics for Physics, Chemistry, and Higher Math.
- **Frontend Components**:
  - `HandwrittenUploadModal.tsx`: Mobile-first camera snapshot, drag-and-drop zone (`border-2 border-dashed border-blue-300 dark:border-blue-800 rounded-3xl bg-blue-50/30`), contrast slider/preview, and tactile submit button.
  - `GradingFeedbackCard.tsx`: Experienced teacher-style marking card with step badges, affectionate margin notes, and KaTeX corrections.
- **Automated Verification**:
  - `backend/tests/test_phase103_handwritten_ocr_grading.py`: Asserts step-scoring math, Bengali normalization, API response contracts, architecture headers, and zero-emoji compliance.

## 2. Directory Layout & Key Files
- `frontend/src/components/grading/HandwrittenUploadModal.tsx`
- `frontend/src/components/grading/GradingFeedbackCard.tsx`
- `backend/app/services/ocr_rubric_grader_service.py`
- `backend/app/api/v1/endpoints/grading.py`
- `backend/tests/test_phase103_handwritten_ocr_grading.py`
