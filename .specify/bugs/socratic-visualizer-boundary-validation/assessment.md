# Bug Assessment: Socratic Visualizer Geometry Boundary & Parameter Hardening

- **Slug**: `socratic-visualizer-boundary-validation`
- **Assessed**: 2026-10-14
- **Severity**: MEDIUM
- **Component**: `backend/app/services/math_visualizer_service.py`, `backend/app/services/socratic_tutor_service.py`

## 1. Problem Description & Root Cause
1. **Math Visualizer Non-Positive Dimensions**:
   - In `MathVisualizerService.generate_geometry_svg`, if `param_a` or `param_b` are negative or zero (e.g. `param_a = -5.0` or `0.0`), the procedural SVG generator produces inverted polygon points and nonsensical negative coordinate calculations (`points="60,260 -15,260 60,335"`).
2. **Socratic Session Student ID Sanitation**:
   - In `SocraticTutorService.start_socratic_session`, an empty or whitespace string for `student_id` is stored without fallback, causing untracked guest sessions in analytics.

## 2. Proposed Remediation
1. **In `MathVisualizerService.generate_geometry_svg`**:
   - Validate `if param_a <= 0.0 or param_b <= 0.0: return {"success": False, "message": "জ্যামিতিক বাহুর দৈর্ঘ্য অবশ্যই ০ এর চেয়ে বড় ধনাত্মক সংখ্যা হতে হবে।"}`.
2. **In `SocraticTutorService.start_socratic_session`**:
   - If `not student_id or not str(student_id).strip()`, safely fallback to `"student_anonymous"`.

## 3. Files to Change
- `backend/app/services/math_visualizer_service.py`
- `backend/app/services/socratic_tutor_service.py`

## 4. Risks & Considerations
Zero risk. Prevents corrupted SVG rendering in browser viewports and guarantees valid geometric dimensions.
