<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
FILE:      specs/022-phase118-curriculum-knowledge-graph/plan.md
PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
PURPOSE:   Architectural blueprint for NCTB knowledge graph DAG, prerequisite engine,
           remedial pathway generator, SVG atlas component, and remedial drawer.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 118 — Curriculum Knowledge Graph & Dynamic Remedial Navigator

## Architectural Overview

```
 [Class 9/10 Algebra & Trig] -----> [Class 11 Limits & Functions] -----> [HSC Calculus Derivatives]
           ^                                                                      |
           |                                                                      |
   Foundation Node                                                           Target Topic
           |                                                                      |
           +----------------- Prerequisite Gap Detected --------------------------+
                                          |
                                          v
                      [3-Step Dynamic Remedial Trajectory]
                       - Step 1: Quick Concept Refresher (5 min)
                       - Step 2: Guided Worked Example (5 min)
                       - Step 3: Mastery Diagnostic Drill (5 min)
```

## Work Breakdown Structure

1. **Backend Service (`backend/app/services/curriculum_knowledge_graph_service.py`)**:
   - Class `CurriculumKnowledgeGraphService`
   - Node storage: NCTB curriculum graph with topics spanning Physics, Chemistry, Higher Math, Biology, ICT (Class 6 through HSC).
   - Prerequisite edge validations with cycle detection (Tarjan's or DFS color marking).
   - Method `get_prerequisites(topic_id, recursive=True)` returning topological ordering.
   - Method `identify_prerequisite_gaps(topic_id, student_mastery_map)`.
   - Method `generate_remedial_pathway(topic_id, student_mastery_map)`.
   - Method `get_graph_snapshot(subject=None, class_grade=None)`.

2. **Frontend Components**:
   - `frontend/src/components/curriculum/KnowledgeGraphAtlas.tsx`:
     - Interactive SVG canvas rendering nodes on cartographic parchment (`#FAFAF8`).
     - Nodes displayed with Oxford Navy ring badges (`#0A2540`), topic title, class level, and mastery percentage.
     - Prerequisite relationship edges rendered as crisp hairline connectors with directional arrows.
     - Zoom, pan, and subject/class filtering.
     - On topic node click -> opens Remedial Drawer.
   - `frontend/src/components/curriculum/RemedialPathDrawer.tsx`:
     - Slide-over drawer with 3-step breakdown (Refresher, Guided Example, Mastery Drill).
     - 5-min timing indicator for each step.
     - Sub-pixel KaTeX equation display.
     - 3D Tactile Button: "প্রতিকারমূলক পাঠ শুরু করো" (`shadow-[0_4px_0_0_#065F46] active:translate-y-1 active:shadow-none`).

3. **REST Endpoints (`backend/app/api/v1/endpoints/knowledge_graph.py`)**:
   - `GET /knowledge-graph/atlas`: Returns graph nodes and prerequisite edges.
   - `GET /knowledge-graph/topics/{topic_id}/prerequisites`: Returns prerequisite tree.
   - `POST /knowledge-graph/topics/{topic_id}/remedial-pathway`: Generates personalized 3-step recovery path.
   - Mount in `backend/app/api/v1/router.py`.

4. **Automated Verification Suite (`backend/tests/test_phase118_knowledge_graph.py`)**:
   - Test 1: DAG integrity and cycle-free validation.
   - Test 2: Prerequisite chain traversal and topological sorting.
   - Test 3: Prerequisite gap detection based on student mastery thresholds.
   - Test 4: 3-step remedial pathway generation (5 min + 5 min + 5 min).
   - Test 5: Frontend component tactile 3D button styling, KaTeX equations, and SVG map canvas.
   - Test 6: Zero-emoji compliance and standardized Developer Architecture Notes.
