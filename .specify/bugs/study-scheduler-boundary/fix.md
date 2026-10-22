# Bug Fix: Study Scheduler Slot Scaling & Guardian Alert Throttling

## 1. Remediation Applied

### Fix 1: Adaptive Recall Duration in `study_scheduler_service.py`
Replaced rigid minimum 30m floor with adaptive residual time:
```python
remaining = max(10, total_planned_minutes - (primary_duration + sec_duration + ter_duration))
recall_duration = min(60, remaining)
```
This guarantees that for any study duration (1.0h to 14.0h), total planned minutes strictly respects the student's available hours.

### Fix 2: Alert Throttling & Deduplication in `burnout_prevention_service.py`
Added stateful check so multiple evaluations within the same test or day do not duplicate alerts:
```python
already_alerted = any(a["student_id"] == student_id for a in self._guardian_alerts)
if is_minor and tier == "BURNOUT_RISK" and not already_alerted:
    self._guardian_alerts.append(...)
```

---

## 2. Verification Plan
- Unit test in `backend/tests/test_phase22_study_scheduler.py`:
  - `test_low_available_hours_slot_clamping()`
  - `test_guardian_alert_deduplication()`
- Full test suite run with zero regressions.
