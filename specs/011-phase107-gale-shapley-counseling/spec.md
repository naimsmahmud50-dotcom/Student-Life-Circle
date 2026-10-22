<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 107 Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
FILE:      specs/011-phase107-gale-shapley-counseling/spec.md
PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
PURPOSE:   Establishes functional specifications for student-proposing deferred acceptance
           matching (Gale-Shapley), quota partitioning with automatic spillover,
           multi-stage seat migration cascade simulation, and human-crafted counseling UI.
STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
-->

# Specification: Phase 107 — Centralized Admission Counseling & Gale-Shapley Stable Matching Hub

## Feature Directory
`specs/011-phase107-gale-shapley-counseling`

## 1. Problem Statement
Every year, over 300,000 higher secondary graduates in Bangladesh navigate complex, decentralized university admission counseling processes across engineering institutes (BUET, CKET), general universities (DU, JU, RU, CU), and medical colleges (DMC, SSMC). Candidates face extreme anxiety regarding preference ordering, quota seat allocations, cut-off rank thresholds, and seat migration cycles. In traditional systems:
1. Students lack transparent, real-time feedback on how their preference ordering impacts their admission probability.
2. Seat migrations occur in opaque, slow administrative batches where candidates cannot visualize how a withdrawal in a top program cascades vacancies down the merit list.
3. Complex quotas (Freedom Fighter, District, Tribal, Special Needs) often result in vacant seats if unallocated seats fail to spill over automatically into the General merit pool.

"Student Life Circle (অগ্রযাত্রা)" requires a state-of-the-art **Centralized Admission Counseling & Gale-Shapley Stable Matching Hub** that guarantees mathematically proven stability, zero blocking pairs (no justified envy), transparent quota balancing with automatic general spillover, and multi-stage seat migration cascade simulations.

---

## 2. Core Mathematical Foundation: Gale-Shapley Deferred Acceptance

The student-proposing deferred acceptance algorithm guarantees:
1. **Stability:** No student-program pair $(s, p)$ exists such that $s$ prefers $p$ to their assigned program and $p$ prefers $s$ to any currently accepted candidate (envy-free matching).
2. **Student-Optimality:** Among all stable matchings, every student is matched to their best possible stable outcome.
3. **Strategy-Proofness for Students:** Candidates have no incentive to misreport their true preference ranking.

### Algorithmic Flow:
1. Each unassigned student proposes to their highest-ranked acceptable program that has not yet rejected them.
2. Each program tentatively holds the top $C$ candidates according to institutional priority (merit score/rank) across general and quota reserved seats, rejecting the remainder.
3. Steps 1-2 repeat until no unassigned student has any program left to propose to, or all capacity constraints are satisfied.

---

## 3. User Stories & Acceptance Criteria

### US1: Student-Proposing Gale-Shapley Matching Engine (P1)
- As an admission authority, I want a deterministic matching engine that takes thousands of candidates and university programs and produces an envy-free stable matching.
- Acceptance Criteria:
  - Supports configurable capacities and merit ranking.
  - Generates zero blocking pairs.
  - Produces detailed audit logs of rounds, proposals, tentative holds, and rejections.

### US2: Quota Partitioning & General Spillover (P1)
- As an affirmative action officer, I need quota seats (Freedom Fighter, Tribal, District, Special Needs) reserved for eligible candidates, with unfulfilled seats spilling over into the General merit pool.
- Acceptance Criteria:
  - Strict eligibility filtering by quota category.
  - Automatic spillover of unfilled quota seats to the general pool after quota round.
  - Zero wasted seats when qualifying general candidates exist.

### US3: Multi-Stage Seat Migration Cascade Simulation (P1)
- As a candidate holding a lower-preference seat, I want to simulate how subsequent rounds and seat cancellations ripple upward into vacancies in my dream program.
- Acceptance Criteria:
  - Simulates multi-round withdrawal cascading.
  - Tracks upward movement paths (e.g. `JU CSE` -> `DU CSE` -> `BUET CSE`).
  - Reports updated cut-off merit ranks per round.

### US4: Elite University Guidance Counseling Matrix UI (P1)
- As a student, I need a welcoming, dignified counseling studio to order my preferences, view admission probability meters, and explore quota options without intimidating bureaucratic tables.
- Acceptance Criteria:
  - Interactive preference ordering cards with tactile 3D buttons (`shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`).
  - Admission probability indicators (High, Moderate, Ambitious) with gentle gradients.
  - Migration cascade visualizer with step scrubber.
  - Strict Zero-Emoji compliance (Lucide SVG vectors only).
  - 'Hind Siliguri' for university programs and 'Plus Jakarta Sans' for merit ranks.

### US5: REST API & Automated Verification Suite (P1)
- As a web client, I need endpoints to run matching, simulate migration cascades, and predict admission probabilities.
- Acceptance Criteria:
  - `POST /api/v1/counseling/match`
  - `POST /api/v1/counseling/migrate-simulate`
  - `GET /api/v1/counseling/programs`
  - `POST /api/v1/counseling/predict-probability`
  - Automated test suite `backend/tests/test_phase107_gale_shapley_counseling.py` passing 100%.
