# Bug Fix: Predictive Analytics & Admission Engine Boundary Protection

## 1. Remediation Applied

### Fix 1: Hard-Stop Zero CI for Failing Subjects in `predictive_analytics_service.py`
When `has_failing_subject` is detected:
```python
if has_failing_subject:
    expected_cgpa = 0.00
    ci_lower = 0.00
    ci_upper = 0.00
    golden_prob_total = 0.0
```
This guarantees mathematical integrity and prevents paradoxical predictions where a student failing a core subject is forecasted to pass.

### Fix 2: Explicit Missing Subject Imputation Flagging in `admission_probability_service.py`
Exposed `missing_subjects: List[str]` and `is_partially_estimated: bool` in each track projection. When any track subject is missing:
```python
is_partially_estimated = len(missing_subjects) > 0
```
Allows UI and downstream consumers to render a caution badge warning the student that specific subject scores were imputed at 50%.

---

## 2. Verification Plan
- Unit test in `backend/tests/test_phase21_predictive_analytics.py`:
  - `test_failing_subject_forces_zero_gpa_and_ci()`
  - `test_missing_subjects_transparency_flag()`
- Full test suite run with zero regressions.
