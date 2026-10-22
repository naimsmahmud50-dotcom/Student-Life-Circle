# Bug Assessment: Study Scheduler Slot Duration Overshoot & Alert Throttling

## 1. Problem Description
During `/speckit-analyze` boundary analysis for Phase 22 (`StudySchedulerService` and `BurnoutPreventionService`), two boundary vulnerabilities were detected:

### Boundary Vulnerability 1: Active Recall Slot Duration Overshoot Under Tight Schedules
In `study_scheduler_service.py`, when a student requests a low study time allotment (e.g., `available_hours = 1.0` or `1.5` hours):
The calculation `recall_duration = max(30, total_planned_minutes - (primary_duration + sec_duration + ter_duration))` enforced an arbitrary minimum floor of `30` minutes. Consequently, for a 60-minute requested schedule, the slot durations sum to $21 + 15 + 15 + 30 = 81$ minutes ($+35\%$ overshoot of available study time). This causes schedule overflow and disrupts the student's bedtime.

### Boundary Vulnerability 2: Rapid Re-Evaluation Alert Spam in Guardian Safety Hook
In `burnout_prevention_service.py`, if an at-risk minor student triggered the `BURNOUT_RISK` tier and repeatedly checked or updated their fatigue status in a short session, a duplicate alert was appended to `_guardian_alerts` on every evaluation without deduplication.

---

## 2. Root Cause Analysis
1. Hardcoded minimum floor `max(30, ...)` ignored `total_planned_minutes` scaling when `total_planned_minutes < 180`.
2. Lack of deduplication check in `_guardian_alerts` for the same `student_id` during active session lifecycle.

---

## 3. Remediation Strategy
1. **Adaptive Slot Duration Scaling**: Scale `recall_duration` dynamically using `remaining = max(10, total_planned_minutes - sum(other_slots))` and clamp to `min(60, remaining)`.
2. **Guardian Alert Deduplication**: Check if an active unacknowledged alert already exists for the `student_id` before appending a duplicate guardian alert.
