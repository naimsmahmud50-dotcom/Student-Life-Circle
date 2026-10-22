# Bug Fix: CAT Numerical Stability & Blueprint Negative Percentage Guard

- **Slug**: `cat-blueprint-edge-case-hardening`
- **Fixed**: 2026-10-14
- **Component**: `backend/app/services/cat_engine_service.py`, `backend/app/services/blueprint_composer_service.py`

## 1. Summary of Changes
1. **`BlueprintComposerService`**:
   - Added validation against negative percentages in both `cognitive_distribution` and `chapter_distribution`.
2. **`CatEngineService`**:
   - Sanitized `initial_theta`: if `math.isnan(initial_theta)` or `math.isinf(initial_theta)`, safely resets to `0.0`.
   - Validated that `student_id` is provided and non-empty.
   - Validated that `selected_option_id` is provided and non-empty in `submit_cat_answer`.

## 2. Verification
Regression test suite in `backend/tests/test_phase18_cat_and_blueprint.py` verifies:
- Blueprint composition rejects negative percentage allocations.
- CAT initialization handles NaN/inf theta without failure.
- Submitting empty options is gracefully rejected.
- All 90+ tests pass with zero regressions.
