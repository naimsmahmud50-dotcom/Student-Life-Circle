<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 116 Digital Examination Hall & Proctoring Integrity Tower
FILE:      specs/020-phase116-digital-exam-hall-proctoring/plan.md
PHASE:     Phase 116 - Digital Examination Hall & Proctoring Integrity Tower
PURPOSE:   Establishes serene, privacy-preserving digital examination desk, teacher
           integrity monitor, and cryptographic submission receipt verification.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 116 — Digital Examination Hall & Proctoring Integrity Tower

## Component & Service Architecture

### 1. `backend/app/services/proctoring_integrity_service.py`
- In-memory thread-safe registry of active examination hall sessions.
- Session Lifecycle:
  * `initialize_exam_session(session_id, student_id, student_name, exam_id)`
  * `record_telemetry_event(session_id, event_type, value, metadata)`
  * `calculate_integrity_score(session_id) -> float`
  * `finalize_exam_submission(session_id, answers) -> Dict[str, Any]`
- Cryptographic Receipt:
  * Produces an immutable receipt payload:
    `receipt_hash = sha256(f"{session_id}:{student_id}:{exam_id}:{final_score}:{timestamp}:{secret_salt}".encode()).hexdigest()`
- Privacy Guarantee: Zero video or facial biometric processing. Only heuristic event metadata.

### 2. `frontend/src/components/exam-hall/DigitalExamDesk.tsx`
- Fullscreen distraction-free desk layout with serene paper aesthetic (`bg-[#FAFAF8] dark:bg-[#0B132B]`).
- Question navigation rail with answered, flagged, and unanswered chips.
- Calm emerald integrity badge: `"পরীক্ষা অখণ্ডতা সক্রিয়"`.
- Auto-save indicator: `"স্বয়ংক্রিয় সংরক্ষণ সম্পন্ন"`.
- Tactile 3D Oxford Navy buttons: `"উত্তর নিশ্চিত করুন"` and `"পরীক্ষা সমাপ্ত করুন"`.

### 3. `frontend/src/components/exam-hall/ProctorTeacherMonitor.tsx`
- Real-time teacher view monitoring student examinees.
- Roster cards displaying student roll, answered count, active timer, and integrity category:
  * `অখণ্ডতা অক্ষুণ্ণ (90-100)` (Emerald)
  * `পর্যবেক্ষণাধীন (70-89)` (Amber)
  * `পুনঃযাচাই প্রয়োজন (<70)` (Rose)
- Dignified layout with zero punitive alarms.

### 4. `backend/app/api/v1/endpoints/exam_hall.py`
- `POST /exam-hall/sessions/start`: Initializes an exam desk session.
- `POST /exam-hall/sessions/{session_id}/telemetry`: Logs telemetry heuristic events (tab switch, blur, audio surge).
- `POST /exam-hall/sessions/{session_id}/finalize`: Submits and seals exam with cryptographic receipt.
- `GET /exam-hall/sessions/{session_id}/status`: Fetches live session status & integrity telemetry.
- `GET /exam-hall/proctor/{exam_id}/roster`: Proctor live teacher monitor feed.
- Mount router in `backend/app/api/v1/router.py`.

### 5. Automated Verification
- `backend/tests/test_phase116_digital_exam_hall.py`:
  * Telemetry logging and integrity score deduction formula.
  * SHA-256 seal integrity and tamper resistance.
  * Teacher roster retrieval.
  * Frontend components tactile styling & zero emoji.
  * Developer architecture notes.
- Platform regression discovery: 1,366+ tests passing.
