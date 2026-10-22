<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Task Breakdown
TOPIC:     Phase 103 Sequenced Implementation Tasks
FILE:      specs/007-phase103-handwritten-ocr-grading/tasks.md
PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
PURPOSE:   Tracks step-by-step implementation for handwritten script upload modal,
           teacher-style grading feedback card, OCR rubric service, endpoints, and tests.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
-->

# Tasks: Phase 103 Handwritten Script OCR & Step-by-Step Rubric Grader

## Task Checklist

- [x] **T723**: [US3] Implement `backend/app/services/ocr_rubric_grader_service.py` with NCTB 4-step marking rubrics, partial credit calculations, and Bengali OCR normalization.
- [x] **T724**: [US3] Implement `backend/app/api/v1/endpoints/grading.py` and mount in `router.py` with script submission and rubric listing endpoints.
- [x] **T725**: [US1] Build `frontend/src/components/grading/HandwrittenUploadModal.tsx` with mobile-first camera capture, drag-and-drop dashed container, contrast preview, and tactile submit button.
- [x] **T726**: [US2] Build `frontend/src/components/grading/GradingFeedbackCard.tsx` with teacher handwritten marking aesthetic, step point badges, kind margin notes, and KaTeX corrections.
- [x] **T727**: [US4] Implement automated verification test in `backend/tests/test_phase103_handwritten_ocr_grading.py` asserting rubric mathematics, Bengali OCR handling, and API response contracts.
- [x] **T728**: [US4] Execute full platform test discovery (`python3 -m unittest discover -s backend/tests`) asserting 1,284+ passing tests and zero-emoji compliance.

