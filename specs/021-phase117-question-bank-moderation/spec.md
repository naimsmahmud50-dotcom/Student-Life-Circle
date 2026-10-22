<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
FILE:      specs/021-phase117-question-bank-moderation/spec.md
PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
PURPOSE:   Defines technical requirements for editorial state machine, dual-examiner
           blind consensus, emergency quarantine switch, and KaTeX visual diff viewer.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Specification: Phase 117 — Collaborative Question Bank Moderation & Peer-Review

## 1. Background & Context
A national-grade academic examination system cannot rely on single-editor approvals or unvetted AI generation. Questions must pass rigorous pedagogical and mathematical scrutiny through a structured editorial board before entering the active examination pool.

Phase 117 implements a collaborative moderation tribunal:
1. **Multi-Stage Editorial State Machine**:
   - `DRAFT`: Author or AI generates draft question.
   - `SME_REVIEW`: Subject Matter Expert validates curricular alignment and stem accuracy.
   - `BOARD_MODERATED`: Senior examination board reviews distractors, marks, and LaTeX equations.
   - `APPROVED`: Reached 2 independent blind reviewer approvals; live in question pool.
   - `QUARANTINED`: Suspended from all active test sessions with immutable audit logging.
2. **Dual-Examiner Blind Review Consensus**:
   - Requires $\ge 2$ distinct educators to independently submit approval decisions (`APPROVED`).
   - If an examiner requests revision (`REVISION_REQUESTED`), question reverts to `DRAFT` with structured review feedback.
   - Blind review: Reviewers cannot see each other's pending verdicts until consensus is finalized.
3. **Emergency Quarantine Switch**:
   - Instantly withdraws any live or in-review question with cryptographic audit record and rationale.
   - Syncs with `quiz_engine` quarantined registry.
4. **KaTeX Visual Diff Viewer**:
   - Side-by-side comparison of original vs. revised question stems, mathematical equations, and option choices.
   - Distinct green hairline highlights for additions and red/rose hairline highlights for deletions/modifications.
5. **Reviewer Tribunal Workspace**:
   - Sovereign editorial room aesthetic (Oxford Academic Navy `#0A2540`, Warm Ivory `#FAFAF8`, Pure Paper White `#FFFFFF`).
   - Keyboard hotkeys (`A` to approve, `R` to request revision, `Q` to trigger emergency quarantine).
   - Tactile 3D buttons:
     - "প্রশ্ন অনুমোদন করুন": Academic Emerald 3D (`shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none`)
     - "সংশোধনের নির্দেশ দিন": Paper Outline with subtle border.

---

## 2. Functional Requirements
- **FR-117.1 (Editorial State Machine)**:
  - Allowed transitions:
    - `DRAFT -> SME_REVIEW`
    - `SME_REVIEW -> BOARD_MODERATED` (upon 1st SME endorsement) or `DRAFT` (revision requested)
    - `BOARD_MODERATED -> APPROVED` (upon 2nd blind consensus endorsement) or `DRAFT` (revision requested)
    - Any state `-> QUARANTINED` (via emergency quarantine switch)
    - `QUARANTINED -> DRAFT` (if un-quarantined for remediation)
- **FR-117.2 (Dual-Examiner Blind Consensus)**:
  - A reviewer cannot approve twice for the same question.
  - Exactly 2 distinct educator approvals needed for transition from `BOARD_MODERATED` to `APPROVED`.
- **FR-117.3 (Emergency Quarantine)**:
  - Accessible to senior board invigilators/admins.
  - Requires explicit `reason` string and records timestamp, actor ID, and previous status.
- **FR-117.4 (KaTeX Visual Diff Viewer)**:
  - Compares original stem vs revised stem, showing segment-level diffs with KaTeX mathematical typography.
- **FR-117.5 (Review Tribunal UI & Hotkeys)**:
  - Event listener on window for keydown `KeyA`, `KeyR`, `KeyQ` (when not typing in textareas/inputs).
- **FR-117.6 (Zero Emoji & Standard Architecture Header)**:
  - Pure Lucide vector icons. Zero unicode emojis. Standardized Developer Architecture Note at top of all files.

---

## 3. Success Metrics & Verification
- Unit & integration tests in `backend/tests/test_phase117_question_moderation.py` pass 100%.
- Zero-emoji sweep passes with 0 violations.
- Security sweep passes with 0 vulnerabilities.
- Total platform tests reach 1,372+ passing tests.
