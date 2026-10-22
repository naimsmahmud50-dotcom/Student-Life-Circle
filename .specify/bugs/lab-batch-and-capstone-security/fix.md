# Bug Fix Specification: Physical Singularity Clamping, Zero-Leak Escrow & Milestone URL Validation

## Applied Remediations

### 1. DC Circuit Zero-Resistance Defensive Clamping & Short-Circuit Safety Flag
- In `VirtualScienceLabService.simulate_circuit`:
  - Enforced `total_resistance = max(raw_total_r, 0.001)` in series configuration.
  - In parallel configuration, clamped individual component resistance `c_val = max(c["value"], 0.001)`.
  - Conditioned short-circuit detection: if `raw_total_r < 0.05` or conductance > 1000.0, set `is_short_circuit_safe = False` and `execution_status = "WARNING_SHORT_CIRCUIT"`.
  - Eliminates all potential `ZeroDivisionError` occurrences.

### 2. Geometric Optics Focal Singularity Shield
- In `VirtualScienceLabService.trace_optics_rays`:
  - Added explicit check for `abs(u - f) < 1e-4` when `lens_type == "CONVEX"`.
  - Returns `image_nature = "AT_INFINITY"`, `image_distance_cm = None`, `magnification = None`, and `is_at_focus = True`.
  - Avoids zero-denominator division `(u - f)` in thin lens equation.

### 3. Exact Escrow Split Reconciliation with Remainder Allocation
- In `CoachingBatchPoolService._recalculate_shares`:
  - Computes `base_split = round(total_fee / n, 2)`.
  - Computes `remainder_drift = round(total_fee - (base_split * n), 2)`.
  - Adds `remainder_drift` to `shares[0]["allocated_amount_bdt"]` (lead guardian).
  - Guarantees $\sum \text{allocated\_amount\_bdt} == \text{total\_monthly\_fee\_bdt}$ down to the exact cent ($0.00$ residual).

### 4. Capstone Milestone URL Sanitization & Stage Progression Lock
- In `IndustryCapstoneService.submit_milestone`:
  - Validates `deliverables_url` against allowed protocol prefixes: `https://`, `http://`, and `git://`.
  - Enforces linear 3-stage progression: `ARCHITECTURE_PROPOSAL` -> `PROTOTYPE_DEMO` -> `FINAL_DELIVERABLES`.
  - Rejects out-of-order attempts with `ValueError` and prevents fraudulent PPO elevation.
