<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
FILE:      specs/021-phase117-question-bank-moderation/tasks.md
PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
PURPOSE:   Establishes multi-stage editorial state machine, dual-examiner consensus,
           emergency quarantine switch, and visual KaTeX diff tribunal.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Tasks: Phase 117 — Collaborative Question Bank Moderation & Peer-Review

## Tasks Ledger

- [x] Task 1: Implement Question Moderation Service (`backend/app/services/question_moderation_service.py`)
  - State machine: `DRAFT -> SME_REVIEW -> BOARD_MODERATED -> APPROVED -> QUARANTINED`
  - Dual-examiner blind consensus enforcement (requires 2 distinct educator approvals)
  - Emergency quarantine switch (instantly pulls question from live pools with audit log)
  - Full audit trail logging with timestamps, actors, decisions, and comments
- [x] Task 2: Build KaTeX Visual Diff Viewer Component (`frontend/src/components/moderation/KaTeXVisualDiffViewer.tsx`)
  - Side-by-side or inline view of original vs modified question text, formulas, and options
  - Hairline green highlight for additions, hairline rose highlight for deletions/modifications
  - KaTeX mathematical formula rendering integration
- [x] Task 3: Build Question Review Tribunal Component (`frontend/src/components/moderation/QuestionReviewTribunal.tsx`)
  - University press editorial boardroom aesthetic
  - Keyboard shortcuts (`A` for approve, `R` for revise, `Q` for quarantine)
  - Tactile 3D buttons: "প্রশ্ন অনুমোদন করুন" (`shadow-[0_4px_0_0_#0F766E]`) and "সংশোধনের নির্দেশ দিন"
  - Blind consensus indicator chips
- [x] Task 4: Implement REST Endpoints & Mount Router (`backend/app/api/v1/endpoints/moderation.py` and `router.py`)
  - Endpoints: create draft, submit for review, review question, emergency quarantine, get queue, get audit history
  - Mounted in `backend/app/api/v1/router.py`
- [x] Task 5: Automated Test Suite (`backend/tests/test_phase117_question_moderation.py`)
  - Assert state machine transitions and invalid transition rejections
  - Assert dual-examiner consensus requirement and self-approval block
  - Assert emergency quarantine pull and audit logging
  - Assert frontend tactile buttons, KaTeX diff highlights, and keyboard shortcuts
  - Assert Developer Architecture Notes on all Phase 117 files
- [x] Task 6: Platform Regression Discovery & Certification
  - Run zero-emoji sweep, security audit, and full platform discovery across 1,372+ tests
