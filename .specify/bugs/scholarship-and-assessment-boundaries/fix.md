# Bug Fix: Scholarship Endowment & Technical Assessment Security Boundaries

- **Slug**: `scholarship-and-assessment-boundaries`
- **Fixed**: 2026-10-14T19:40:02Z
- **Assessment**: ./assessment.md
- **Status**: applied

## Summary
Applied input sanitization against stored XSS, expanded Python coding sandbox reflection restrictions, and enforced double-disbursement defenses.

## Changes

| File | Change | Notes |
|------|--------|-------|
| `backend/app/services/scholarship_endowment_service.py` | modified | Stripped HTML script tags from `statement_of_need`; clamped income to non-negative floats. |
| `backend/app/services/technical_assessment_service.py` | modified | Added `getattr(`, `importlib`, `sys.modules`, `builtins`, `rm -rf` to sandbox prohibited snippets. |
| `backend/tests/test_phase28_scholarship_and_assessment.py` | added tests | Added `test_apply_scholarship_sanitizes_html_script` and `test_evaluate_code_submission_blocks_getattr_and_importlib`. |

## Local Verification
- Commands run: `python3 -m unittest discover -s backend/tests -p "test_*.py"` -> 219 tests passed in 0.238s.
- Manual checks: Verified `statement_of_need` sanitization and code execution rejection.

## Deviations from Assessment
None.
