# Bug Assessment: Scholarship Endowment & Technical Assessment Security Boundaries

- **Slug**: `scholarship-and-assessment-boundaries`
- **Assessed**: 2026-10-14T19:39:50Z
- **Verdict**: `valid, remediation identified`
- **Severity**: High (ASVS L2 Financial Integrity & Code Execution Sandbox)

## Summary
During the whitebox static analysis and concurrency stress audit of Phase 28 (`ScholarshipEndowmentService` and `TechnicalAssessmentService`), three critical vulnerabilities and edge cases were identified:
1. **Stored XSS via Scholarship Statement of Need**: Unsanitized HTML tags (`<script>`) in `statement_of_need` could be persisted to application records and executed in administrative audit portals.
2. **Dynamic Metaprogramming Sandbox Evasion**: Code evaluation sandbox prohibited `eval` and `os.system` but allowed indirect dynamic reflection via `getattr(builtins, ...)` and `importlib.import_module(...)`.
3. **Double-Disbursement Race Condition**: Concurrent automated payout requests could attempt multiple bKash disbursements for the same approved scholarship application.

## Files Likely to Change
- `backend/app/services/scholarship_endowment_service.py`
- `backend/app/services/technical_assessment_service.py`
- `backend/tests/test_phase28_scholarship_and_assessment.py`

## Proposed Remediation
- In `apply_for_scholarship`, sanitize `statement_of_need` by stripping HTML tags (`re.sub(r'<[^>]*>', '', statement)`) and clamp `family_monthly_income_bdt = max(0.0, ...)`.
- In `TechnicalAssessmentService`, expand `PROHIBITED_SNIPPETS` to block `getattr(`, `importlib`, `sys.modules`, `builtins`, and `rm -rf`.
- In `disburse_scholarship`, ensure strict status transition from `APPROVED` to `DISBURSED` with non-negative balance checks.
