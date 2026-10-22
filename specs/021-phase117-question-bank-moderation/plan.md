<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
FILE:      specs/021-phase117-question-bank-moderation/plan.md
PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
PURPOSE:   Architectural blueprint and implementation plan for question moderation service,
           visual KaTeX diff viewer, editorial tribunal workspace, REST endpoints, and tests.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 117 — Collaborative Question Bank Moderation & Peer-Review

## Architecture & Data Flow

```
                      +---------------------------------------+
                      |                 DRAFT                 |
                      +-------------------+-------------------+
                                          | submit_for_review
                                          v
                      +---------------------------------------+
                      |              SME_REVIEW               |
                      +-------------------+-------------------+
                                          | 1st Approval
                                          v
                      +---------------------------------------+
                      |            BOARD_MODERATED            |
                      +-------------------+-------------------+
                                          | 2nd Blind Approval
                                          v
                      +---------------------------------------+
                      |               APPROVED                |
                      +-------------------+-------------------+
                                          |
                      ====================+====================
                             Emergency Quarantine Switch
                                          |
                                          v
                      +---------------------------------------+
                      |              QUARANTINED              |
                      +---------------------------------------+
```

## Work Breakdown Structure

1. **Backend Service (`backend/app/services/question_moderation_service.py`)**:
   - Class `QuestionModerationService` with state transitions: `DRAFT`, `SME_REVIEW`, `BOARD_MODERATED`, `APPROVED`, `QUARANTINED`.
   - Dual-examiner consensus tracking: list of review approvals with `examiner_id`, `decision`, `comments`, `timestamp`.
   - Method `submit_for_review(question_id, actor_id)`.
   - Method `review_question(question_id, examiner_id, decision, comments)`.
   - Method `emergency_quarantine(question_id, actor_id, reason)`.
   - Method `remediate_quarantine(question_id, actor_id, remediation_notes)`.
   - Method `get_moderation_queue(filter_stage)`.
   - Method `get_question_audit_trail(question_id)`.

2. **Visual KaTeX Diff Viewer (`frontend/src/components/moderation/KaTeXVisualDiffViewer.tsx`)**:
   - Side-by-side or unified inline visual diff of original stem/equations vs modified draft.
   - Highlights:
     - Additions: Subtle green tint (`bg-emerald-50 text-emerald-950 border-emerald-300`).
     - Deletions: Subtle rose tint (`bg-rose-50 text-rose-950 border-rose-300 line-through`).
   - Integrated with `KaTeXRenderer` for mathematical formula diffing.

3. **Question Review Tribunal (`frontend/src/components/moderation/QuestionReviewTribunal.tsx`)**:
   - Editorial boardroom aesthetic: Oxford Academic Navy `#0A2540`, Pure Paper White `#FFFFFF`, Warm Ivory `#FAFAF8`.
   - Keyboard hotkeys (`A` for approve, `R` for revise, `Q` for quarantine).
   - Tactile buttons:
     - "প্রশ্ন অনুমোদন করুন" (`shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none bg-emerald-700 text-white font-semibold rounded-2xl`).
     - "সংশোধনের নির্দেশ দিন" (Paper outline button).
     - "জরুরি কোয়ারেন্টিন" (Deep rose border button).
   - Blind consensus status chip: Shows "১ম অনুমোদন সম্পন্ন (২য় পর্যালোচকের অপেক্ষায়)" or "সর্বসম্মত অনুমোদন সম্পন্ন".

4. **REST Endpoints (`backend/app/api/v1/endpoints/moderation.py`)**:
   - `POST /moderation/questions/draft`: Create a question draft.
   - `POST /moderation/questions/{question_id}/submit`: Submit draft to SME review.
   - `POST /moderation/questions/{question_id}/review`: Submit examiner review.
   - `POST /moderation/questions/{question_id}/quarantine`: Trigger emergency quarantine.
   - `GET /moderation/queue`: Retrieve filtered moderation queue.
   - `GET /moderation/questions/{question_id}/history`: Retrieve moderation audit trail.
   - Mount in `backend/app/api/v1/router.py`.

5. **Automated Verification Suite (`backend/tests/test_phase117_question_moderation.py`)**:
   - Test 1: State machine progression and validation of invalid transitions.
   - Test 2: Dual-examiner blind consensus enforcement (prevents self-approval; requires 2 distinct examiners).
   - Test 3: Emergency quarantine instant suspension and audit trail logging.
   - Test 4: Remediation and un-quarantine workflow.
   - Test 5: Frontend tactile styling, KaTeX diff highlights, and keyboard shortcuts.
   - Test 6: Zero-emoji compliance and standardized Developer Architecture Notes.
