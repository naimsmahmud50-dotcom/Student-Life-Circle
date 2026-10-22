<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
FILE:      specs/022-phase118-curriculum-knowledge-graph/spec.md
PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
PURPOSE:   Establishes Directed Acyclic Graph (DAG) of NCTB curriculum topics,
           prerequisite dependency tracing, and 3-step dynamic remedial pathway generation.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Specification: Phase 118 — Curriculum Knowledge Graph & Dynamic Remedial Navigator

## 1. Background & Academic Context
Students struggling with higher-order concepts (such as HSC Calculus differentiation or Physics Rotational Dynamics) rarely fail because of the immediate formula; they almost always fail because of foundational prerequisite gaps in Class 9-10 Algebra, Coordinate Geometry, or Trigonometry.

Phase 118 constructs an academic **Curriculum Knowledge Graph Atlas & Dynamic Remedial Navigator**:
1. **Curriculum Directed Acyclic Graph (DAG)**:
   - Covers NCTB curriculum spanning Class 6 through HSC and University Admission.
   - Nodes represent topics/concepts with attributes: `topic_id`, `title_bn`, `title_en`, `subject`, `class_grade`, `domain`, `prerequisites` (list of prerequisite `topic_id`s), `core_formulas` (LaTeX strings), and `recommended_minutes`.
   - Strictly enforces acyclicity (DAG cycle detection).
2. **Prerequisite Dependency & Gap Tracing Engine**:
   - Traces recursive root prerequisite dependencies.
   - Detects concept gaps: Given student mastery levels ($\in [0.0, 1.0]$) across topics, flags root prerequisites below mastery threshold ($< 0.70$) that block advanced understanding.
3. **Dynamic 3-Step Remedial Pathway Generator**:
   - Synthesizes a focused 15-minute remedial trajectory for any struggling topic:
     1. **Step 1: Quick Concept Refresher** (5 mins) — Core intuition, definitions, and foundational prerequisite bridging.
     2. **Step 2: Guided Example** (5 mins) — Step-by-step solved canonical problem with sub-pixel KaTeX formula breakdowns.
     3. **Step 3: Mastery Check Drill** (5 mins) — 3 diagnostic questions with instant verification.
4. **Knowledge Graph Atlas UI**:
   - Cartographic parchment aesthetic: Oxford Academic Navy nodes (`#0A2540`) on Warm Ivory parchment (`#FAFAF8`), joined by crisp hairline connector lines (`#CBD5E1`).
   - SVG-based interactive canvas with zoom, pan, subject filtering, and mastery ring badges (Emerald for mastered $\ge 80\%$, Amber for in-progress $50-79\%$, Slate/Rose for gap $< 50\%$).
5. **Remedial Path Slide-Over Drawer**:
   - Slide-over drawer offering instant pedagogical recovery when a student makes repeated mistakes in a topic.
   - Tactile 3D button: "প্রতিকারমূলক পাঠ শুরু করো" (`shadow-[0_4px_0_0_#065F46] active:translate-y-1 active:shadow-none`).
   - Bengali typography formatted in 'Hind Siliguri' / clean sans with KaTeX mathematical formulas.

---

## 2. Functional Requirements
- **FR-118.1 (DAG Validation)**:
  - Add topic nodes and prerequisite edges.
  - Assert that cycles are detected and rejected (`CycleDetectedException`).
- **FR-118.2 (Prerequisite Tracing)**:
  - Recursive topological traversal of ancestors.
  - Return all prerequisite topics in topological dependency order.
- **FR-118.3 (Remedial Pathway Generation)**:
  - Given a target topic and student mastery profile, identify weak prerequisites and construct the structured 3-step remedial pathway.
- **FR-118.4 (Interactive Knowledge Atlas UI)**:
  - Visual topic nodes with coordinates, mastery indicators, and connected edges.
  - Pure Lucide icons, zero neon/AI cyber aesthetic.
- **FR-118.5 (Remedial Drawer UI)**:
  - Slide-over drawer with step progression, timing estimates (5 min + 5 min + 5 min = 15 min), and tactile 3D launch button.
- **FR-118.6 (Strict Zero-Emoji & Standard Header)**:
  - Zero emojis in all code, comments, docstrings, components, and tests.
  - Standardized Developer Architecture Note at the top of every file.

---

## 3. Verification Criteria
- Automated test `backend/tests/test_phase118_knowledge_graph.py` passes 100%.
- Zero-emoji sweep passes with 0 violations.
- Security sweep passes with 0 vulnerabilities.
- Global platform discover passes all 1,378+ tests with zero regressions.
