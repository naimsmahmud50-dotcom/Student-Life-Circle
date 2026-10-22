# Bug Assessment: Predictive Analytics & Admission Engine Boundary Conditions

## 1. Problem Description
During `/speckit-analyze` boundary and consistency testing of Phase 21 (`PredictiveAnalyticsService` and `AdmissionProbabilityService`), two critical boundary inconsistencies were discovered:

### Boundary Vulnerability 1: Inconsistent Confidence Interval on Failing Subjects
In the Bangladesh National Education Board grading rules (SSC/HSC), an "F" grade (score $< 33.0\%$) in any compulsory subject results in an overall exam result of "F" (GPA 0.00). In the initial draft of `predictive_analytics_service.py`, when `has_failing_subject == True`, `expected_cgpa` was clamped to `0.00`, but `ci_upper` was calculated as `round(expected_cgpa + 1.96 * se_gpa, 2)`, yielding a non-zero upper bound (e.g., `0.20` or `0.35`). This creates a contradictory forecast where a failing student is projected to have a positive upper confidence interval for passing.

### Boundary Vulnerability 2: Opaque Imputation for Missing Admission Track Subjects
When students evaluate admission tracks (e.g., `BUET_ENG`, which requires `higher_math`, `physics`, `chemistry`) without providing grades for one or more compulsory subjects, the engine defaulted missing subjects to `50.0%` without flagging the projection as estimated. Without an explicit `missing_subjects` list and `is_partially_estimated` flag, students could mistake an imputed baseline for an accurate verified prediction.

---

## 2. Root Cause Analysis
1. In `predictive_analytics_service.py`:
   The 95% confidence interval computation did not check the `has_failing_subject` boolean flag when setting `ci_upper`.
2. In `admission_probability_service.py`:
   The `evaluate_admission_probabilities` method accumulated `missing_subjects` into an internal list but did not expose it or the boolean indicator `is_partially_estimated` in the public returned dictionary.

---

## 3. Remediation Strategy
1. **Failing Subject CI Hard-Stop**: In `predictive_analytics_service.py`, if `has_failing_subject == True`, set `ci_lower = 0.00`, `ci_upper = 0.00`, and `golden_prob_total = 0.0` with an explanatory diagnostic note in `remark_bn`.
2. **Transparent Imputation Flagging**: In `admission_probability_service.py`, expose `missing_subjects: List[str]` and `is_partially_estimated: bool` in each projection object, ensuring user-facing transparency and audit compliance.
