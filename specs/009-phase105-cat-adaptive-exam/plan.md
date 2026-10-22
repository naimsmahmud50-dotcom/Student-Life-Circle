<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Implementation Plan
TOPIC:     Phase 105 AI Adaptive Examination & Dynamic CAT Tower
FILE:      specs/009-phase105-cat-adaptive-exam/plan.md
PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
PURPOSE:   Architectural blueprint detailing technical steps for Item Response Theory
           (3-PL) mathematical modeling, Fisher Information item selection, adaptive exam
           studio UI components, convergence visualization, REST API endpoints, and test verification.
STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
-->

# Implementation Plan: Phase 105 — AI Adaptive Examination & Dynamic CAT Tower

## 1. Technical Architecture & Mathematical Foundation

### A. 3-Parameter Logistic (3-PL) Model
The probability of examinee with latent ability $\theta$ answering item $i$ correctly:
$$P_i(\theta) = c_i + \frac{1 - c_i}{1 + e^{-a_i (\theta - b_i)}}$$
Where:
- $a_i > 0$: Item discrimination parameter (slope of item characteristic curve).
- $b_i \in [-3.0, +3.0]$: Item difficulty parameter (ability required for 50% chance above guessing).
- $c_i \in [0.0, 0.25]$: Pseudo-guessing parameter (chance of guessing correctly).
- $\theta \in [-3.0, +3.0]$: Examinee's current estimated latent ability.

### B. Fisher Information & Standard Error Convergence
Item Fisher Information:
$$I_i(\theta) = a_i^2 \frac{(P_i(\theta) - c_i)^2}{(1 - c_i)^2} \frac{1 - P_i(\theta)}{P_i(\theta)}$$
Test Information Function after $k$ administered items:
$$I(\theta) = \sum_{j=1}^k I_{i_j}(\theta)$$
Standard Error of Ability Estimation:
$$SE(\theta) = \frac{1}{\sqrt{\sum_{j=1}^k I_{i_j}(\theta) + \sigma_{prior}^{-2}}}$$
The engine selects unadministered item $i^*$ maximizing $I_i(\hat{\theta})$ until stopping criteria ($SE(\theta) < 0.25$ or maximum steps $N_{max} = 15$) is met.

### C. Latent Ability Updating
Using Bayesian EAP (Expected A Posteriori) with standard normal prior $\theta \sim \mathcal{N}(0, 1)$ or bounded Newton-Raphson maximum likelihood with score function:
$$\frac{\partial \ln L}{\partial \theta} = \sum_{j=1}^k \frac{u_j - P_j(\theta)}{P_j(\theta) (1 - P_j(\theta))} P_j'(\theta)$$

---

## 2. Component Blueprint

```
+--------------------------------------------------------------+
|                   AdaptiveExamStudio.tsx                     |
|  - Distraction-Free Reading Mode (Hind Siliguri, line 1.8)  |
|  - KaTeX Mathematical Formula Parsing                       |
|  - 3D Tactile Option Cards (shadow-[0_4px_0_0_#1D4ED8])     |
|  - Gentle Mentor Status Indicator (Zero Emoji, Lucide SVG)   |
+------------------------------+-------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                 AbilityConvergenceGraph.tsx                  |
|  - HTML5 Canvas/SVG Trajectory Visualizer                   |
|  - Theta Convergence Curve + Emerald Glow (#10B981)          |
|  - Confidence Intervals (Theta +/- 1.96 * SE)                |
+------------------------------+-------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|              REST API: adaptive_exam.py                      |
|  - POST /api/v1/cat/start                                    |
|  - POST /api/v1/cat/submit-step                              |
|  - GET  /api/v1/cat/result                                   |
+------------------------------+-------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|             CatEngineService (cat_engine_service.py)         |
|  - 3-PL IRT Probability & Fisher Information Matrix          |
|  - Optimal Item Selection (Max Info at Theta)                |
|  - Standard Error Minimization (Target SE < 0.25)            |
|  - National HSC / BUET Percentile Rank Mapping               |
+--------------------------------------------------------------+
```

---

## 3. Implementation Steps & Targets
1. `backend/app/services/cat_engine_service.py`: Complete IRT 3-PL logic, question catalog with calibrated $(a, b, c)$ parameters, Bayesian EAP ability updating, and percentile mapping.
2. `frontend/src/components/adaptive-exam/AbilityConvergenceGraph.tsx`: SVG/Canvas component rendering convergence path, confidence bounds, and difficulty step markers.
3. `frontend/src/components/adaptive-exam/AdaptiveExamStudio.tsx`: Mobile-responsive studio with KaTeX math formulas, 3D tactile buttons, and supportive mentor microcopy.
4. `backend/app/api/v1/endpoints/adaptive_exam.py`: Fast and typed REST endpoints mounted to FastAPI `api_router`.
5. `backend/tests/test_phase105_cat_adaptive_exam.py`: Unit tests asserting 3-PL math, Fisher Information maximization, session state transitions, zero-emoji compliance, and architecture note headers.
6. Full test suite execution ensuring 1,300+ tests pass cleanly.
