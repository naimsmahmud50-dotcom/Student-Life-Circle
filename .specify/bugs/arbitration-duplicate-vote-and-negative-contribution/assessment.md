# Bug Assessment: Arbitration Duplicate Vote Guard & Study Circle Negative Contribution

- **Slug**: `arbitration-duplicate-vote-and-negative-contribution`
- **Assessed**: 2026-10-14
- **Severity**: HIGH
- **Component**: `backend/app/services/arbitration_service.py`, `backend/app/services/study_circle_service.py`

## 1. Problem Description & Root Cause
1. **Arbitration Tribunal Duplicate SME Voting & Deadlock Handling**:
   - In `ArbitrationTribunalService.cast_sme_vote`, the service does not check whether `sme_id` has already cast a vote in `case["votes"]`. A single SME could submit votes multiple times, potentially altering their verdict or tampering with the deliberation audit trail.
   - In `_finalize_tribunal_ruling`, if a 3-way split occurs (1 CORRECT_KEY, 1 QUARANTINE, 1 DISMISS), `max(verdict_counts.items(), key=lambda x: x[1])` picks an arbitrary verdict with count 1, violating the $\ge 2$ majority quorum rule.
   - An invalid verdict string (e.g. arbitrary text) is not guarded against.

2. **Study Circle Negative/Zero Question Contribution**:
   - In `StudyCircleService.contribute_questions`, non-positive integers (`questions_solved <= 0`) are directly added to `member["contributed_questions"]` and `goal["completed_questions"]`, which can corrupt group goal metrics and streak achievements.

## 2. Proposed Remediation
1. **In `ArbitrationTribunalService.cast_sme_vote`**:
   - Validate that `verdict` is in `{"CORRECT_KEY", "QUARANTINE", "DISMISS"}`.
   - Guard against duplicate voting: if `sme_id in case["votes"]`, return `{"success": False, "message": "এই বিশেষজ্ঞ বিচারক ইতিমধ্যে এই মামলায় ভোট প্রদান করেছেন।"}`.
   - In `_finalize_tribunal_ruling`, ensure a true majority ($\ge 2$ votes) exists. If there is a 1-1-1 deadlock, set status to `DISMISSED` with the ruling: "কোনো মতামতে সংখ্যাগরিষ্ঠতা (কমপক্ষে ২ ভোট) অর্জিত না হওয়ায় প্রশ্ন অপরিবর্তিত রেখে অভিযোগ খারিজ করা হলো।"

2. **In `StudyCircleService.contribute_questions`**:
   - Guard: `if questions_solved <= 0: return {"success": False, "message": "অনুশীলন সংখ্যা অবশ্যই ১ বা তার বেশি হতে হবে।"}`.

## 3. Files to Change
- `backend/app/services/arbitration_service.py`
- `backend/app/services/study_circle_service.py`

## 4. Risks & Considerations
Zero negative impact. Hardens consensus integrity, maintains mathematical consistency of group progress, and prevents tampering.
