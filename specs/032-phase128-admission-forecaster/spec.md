# SPECIFICATION: Phase 128 — Autonomous University Admission Cut-Off Forecaster & Rank Sigmoid Predictor

## 1. Executive Summary & Objective
Phase 128 delivers the Autonomous University Admission Cut-Off Forecaster & Rank Sigmoid Predictor for Bangladesh's premiere public universities and medical colleges. Using calibrated historical 10-year admission statistics (2015–2025), empirical cut-off thresholds, and logistic sigmoid probability modeling, this engine calculates calibrated admission probabilities, predicts merit rank ranges, checks subject-specific eligibility gates, and accounts for constitutional quota distributions without exposing or storing student Personally Identifiable Information (PII).

## 2. Mandatory Architectural Standards
- **Developer Architecture Note Header**: Every created or modified file MUST feature the standardized block header documenting Phase 128, ASVS L2, and Calibrated Probability standards.
- **Pure Academic Visual Philosophy (Zero AI Vibe)**:
  * Pure Paper Ivory (`#FAFAF8`) & Pure Paper White (`#FFFFFF`) background and card canvases.
  * Oxford Academic Navy (`#0A2540`) dominant headers, borders, and controls.
  * Academic Emerald (`#065F46`) for Safe tier probabilities ($\ge 75\%$).
  * Scholar Gold (`#B45309`) for Competitive tier probabilities ($40\% - 74\%$).
  * Deep Crimson / Slate Navy for Reach tier probabilities ($< 40\%$).
  * 3D tactile buttons with physical bottom ledge: `bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg`.
  * Strict Zero-Emoji Rule: 100% pure Lucide-React SVG vector icons only.

## 3. Mathematical & Algorithmic Formulation

### A. Sigmoid Probability Calibration
The admission probability $P(x)$ for a candidate achieving composite score $x$ is modeled using the calibrated logistic sigmoid:
$$P(x) = \frac{1}{1 + e^{-k(x - x_0)}}$$

Where:
- $x$: Student composite score calculated from weighted academic credentials (SSC/HSC GPA contribution) plus exam simulation or subject mark inputs.
- $x_0$: Target institution and unit's 10-year median cut-off threshold ($x_0 \in \mathbb{R}^+$).
- $k$: Calibration slope parameter ($k \in [0.10, 0.20]$), determined empirically from historical cut-off variance.
- Probability Tiers:
  * **Safe** (`নিরাপদ জোন`): $P(x) \ge 0.75$
  * **Competitive** (`প্রতিযোগিতাপূর্ণ জোন`): $0.40 \le P(x) < 0.75$
  * **Reach** (`চ্যালেঞ্জিং জোন`): $P(x) < 0.40$

### B. Historical Benchmarks & Units (2015–2025)
1. **BUET (Engineering)**:
   - Full Marks: 100 (Preliminary/Written scaled composite).
   - Historical Median Threshold $x_0$: $74.5$.
   - Slope $k$: $0.16$.
   - Eligibility Gate: HSC GPA 5.0, SSC GPA $\ge 4.0$, Minimum Grade Point 5.0 in Physics, Chemistry, and Higher Math.
2. **Dhaka University (DU) - Ka Unit (Science)**:
   - Full Marks: 120 (100 MCQ/Written + 20 GPA contribution).
   - Historical Median Threshold $x_0$: $68.0$.
   - Slope $k$: $0.14$.
   - Eligibility Gate: Combined SSC+HSC GPA $\ge 8.0$ (min 3.5 each), Science stream.
3. **Dhaka University (DU) - Kha Unit (Arts & Social Science)**:
   - Full Marks: 120.
   - Historical Median Threshold $x_0$: $71.0$.
   - Slope $k$: $0.14$.
   - Eligibility Gate: Combined SSC+HSC GPA $\ge 7.5$ (min 3.0 each).
4. **Dhaka University (DU) - Ga Unit (Business Studies)**:
   - Full Marks: 120.
   - Historical Median Threshold $x_0$: $73.5$.
   - Slope $k$: $0.15$.
   - Eligibility Gate: Combined SSC+HSC GPA $\ge 7.5$ (min 3.0 each).
5. **Medical Colleges (MBBS/BDS National Admission)**:
   - Full Marks: 300 (100 Written Exam + 200 GPA contribution).
   - Historical Median Threshold $x_0$: $268.5$.
   - Slope $k$: $0.12$.
   - Eligibility Gate: Combined SSC+HSC GPA $\ge 9.0$ (min 4.0 each), Biology GP $\ge 4.0$.
6. **GST Consortium (24 General & STEM Public Universities)**:
   - Full Marks: 100.
   - Historical Median Threshold $x_0$: $55.0$.
   - Slope $k$: $0.13$.
   - Eligibility Gate: Combined SSC+HSC GPA $\ge 7.0$ (min 3.0 each).

### C. Quota Modulation
Quotas dynamically adjust the effective threshold $x_0 \leftarrow x_0 - \Delta x_{\text{quota}}$:
- **General (Merit)**: $\Delta x = 0.0$
- **Freedom Fighter (মুক্তিযোদ্ধা কোটা)**: $\Delta x = 6.5$
- **Tribal / Ethnic Minority (ক্ষুদ্র নৃগোষ্ঠী)**: $\Delta x = 8.0$
- **English Medium / O/A Level (ইংরেজি মাধ্যম সমমান)**: $\Delta x = 3.0$
- **Special Needs / Physical Disability (প্রতিবন্ধী কোটা)**: $\Delta x = 7.5$

### D. Merit Rank Range Estimation
Rank range $[\text{rank}_{\min}, \text{rank}_{\max}]$ is projected using total applicant pool volume $N$ and normal quantile approximation around predicted percentile $1 - P(x)$.

## 4. Privacy, ASVS L2 & Zero PII Mandate
- No student names, national identity numbers, phone numbers, email addresses, or biometric data are ingested, processed, or persisted.
- Purely numeric academic metrics (GPA, subject grade points, raw simulation marks, target unit code, quota code) are utilized.
- All stored calculation telemetry complies with Supabase RLS isolation (`auth.uid() = user_id`).
