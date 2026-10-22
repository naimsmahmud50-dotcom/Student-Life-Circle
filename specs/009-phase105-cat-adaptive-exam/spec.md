<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 105 AI Adaptive Examination & Dynamic CAT Tower
FILE:      specs/009-phase105-cat-adaptive-exam/spec.md
PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
PURPOSE:   Establishes functional specifications for psychometrically calibrated
           Computerized Adaptive Testing (CAT) based on 3-Parameter Logistic (3-PL)
           Item Response Theory (IRT), Fisher Information item selection, latent ability
           convergence, and compassionate mentor-style student evaluation.
STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
-->

# Specification: Phase 105 — AI Adaptive Examination & Dynamic CAT Tower

## Feature Directory
`specs/009-phase105-cat-adaptive-exam`

## 1. Problem Statement
Traditional static standardized exams subject all students to identical question sequences regardless of ability. For high-achieving students, excessive easy questions waste time and fail to measure ceiling potential; for struggling students, consecutive overwhelmingly difficult questions induce math anxiety, demoralization, and test fatigue. Furthermore, conventional testing platforms feature flashing red countdown timers and punitive error scores that trigger stress rather than deep cognitive mastery. 

Students in Bangladesh preparing for competitive admission (BUET, Dhaka University, Medical Colleges) and HSC board exams need an intelligent Computerized Adaptive Testing (CAT) engine that dynamically recalibrates question difficulty based on Item Response Theory (IRT 3-PL) and maximum Fisher Information, while presenting a calm, encouraging mentor-grade examination studio without panic-inducing timers.

## 2. Goals & User Stories

### US1: Psychometric 3-PL IRT Engine & Fisher Information Optimization (P1)
- As an educational psychometrician, I want the system to compute item response probability $P(\theta) = c + \frac{1-c}{1 + e^{-a(\theta - b)}}$, where $a$ is discrimination, $b$ is difficulty, and $c$ is pseudo-guessing.
- Acceptance Criteria:
  - Calculate accurate response probability and item gradients across examinee ability $\theta \in [-3.0, +3.0]$.
  - Dynamically select the next item from the calibrated question bank maximizing Fisher Information $I(\theta) = a^2 \frac{(P(\theta) - c)^2}{(1 - c)^2} \frac{1 - P(\theta)}{P(\theta)}$ to reduce standard error below 0.25 ($SE(\theta) < 0.25$).
  - Update latent ability $\theta$ after each response using Bayes/EAP or bounded Newton-Raphson MLE.
  - Map final latent ability $\theta$ to authentic HSC and admission percentile ranks.

### US2: Distraction-Free Adaptive Exam Studio (P1)
- As a student taking an adaptive exam, I want a calm, reading-focused environment with KaTeX mathematical formulas, clear option cards, and smooth question transitions without stressful countdown bars.
- Acceptance Criteria:
  - Mobile-first reading mode with crisp `Hind Siliguri` (line-height 1.8) and `Plus Jakarta Sans` for question numerals.
  - Tactile 3D button physics on option selection cards (`shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`).
  - No stressful red timers or harsh failure alerts; supportive, encouraging mentor tone throughout.
  - Zero unicode emojis; strict Lucide-React SVG vectors (`CheckCircle2`, `Compass`, `Target`, `Clock`).

### US3: Ability Convergence Graph & Visual Mastery Feedback (P1)
- As an examinee completing an adaptive test, I want to visualize my ability trajectory converging toward mastery over sequential questions.
- Acceptance Criteria:
  - HTML5 Canvas/SVG visualizer rendering the $\theta$ trajectory, confidence intervals ($\theta \pm 1.96 \cdot SE$), and national percentile mapping.
  - Emerald glow aesthetics (`#10B981`) and smooth convergence curve.

### US4: REST Endpoints for CAT Session Management (P1)
- As a client application, I need authenticated REST endpoints to initialize sessions, submit answers, receive next adaptive questions, and retrieve final diagnostic evaluations.
- Acceptance Criteria:
  - `POST /api/v1/cat/start`: Initializes session with prior ability $\theta_0 = 0.0$ and returns first diagnostic item.
  - `POST /api/v1/cat/submit-step`: Ingests student answer, updates $\theta$ and $SE(\theta)$, and selects optimal next item.
  - `GET /api/v1/cat/result`: Returns complete trajectory, final ability $\theta$, percentile rank, and subject breakdown.
