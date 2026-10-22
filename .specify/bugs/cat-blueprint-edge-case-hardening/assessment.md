# Bug Assessment: CAT Numerical Stability & Blueprint Negative Percentage Guard

- **Slug**: `cat-blueprint-edge-case-hardening`
- **Assessed**: 2026-10-14
- **Severity**: MEDIUM
- **Component**: `backend/app/services/cat_engine_service.py`, `backend/app/services/blueprint_composer_service.py`

## 1. Problem Description & Root Cause
1. **Blueprint Negative Percentage Invariant Violation**:
   - In `BlueprintComposerService.compose_blueprint`, the sum of percentages is checked (`abs(sum - 100.0) <= 1.0`), but individual percentage values are not checked for negativity. If a caller inputs `{"knowledge": -20.0, "comprehension": 120.0}`, the sum is 100%, but negative questions cannot exist.
2. **CAT Engine Theta NaN/Inf Input Hardening**:
   - In `CatEngineService.start_cat_session`, if `initial_theta` is `float('nan')` or `float('inf')`, clamping with `min/max` can propagate `nan` into all future IRT calculations, breaking `math.exp` and Fisher Information calculations.
3. **Empty Option Submission in CAT**:
   - In `CatEngineService.submit_cat_answer`, submitting an empty string `""` for `selected_option_id` should return a clear validation error rather than marking it as an unhandled option.

## 2. Proposed Remediation
1. **In `BlueprintComposerService.compose_blueprint`**:
   - Guard: `if any(v < 0.0 for v in cognitive_distribution.values()) or any(v < 0.0 for v in chapter_distribution.values()): return {"success": False, "message": "কোনো শতকরা হার ঋণাত্মক হতে পারবে না।"}`.
2. **In `CatEngineService.start_cat_session`**:
   - Check `if math.isnan(initial_theta) or math.isinf(initial_theta): initial_theta = 0.0`.
   - Validate that `student_id` is a non-empty string.
3. **In `CatEngineService.submit_cat_answer`**:
   - Validate that `selected_option_id` is non-empty.

## 3. Files to Change
- `backend/app/services/cat_engine_service.py`
- `backend/app/services/blueprint_composer_service.py`

## 4. Risks & Considerations
Zero risk. Strengthens mathematical consistency, protects IRT engine from numerical poisoning, and guarantees valid exam blueprints.
