<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
FILE:      specs/022-phase118-curriculum-knowledge-graph/tasks.md
PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
PURPOSE:   Establishes Directed Acyclic Graph (DAG) topic mapping, prerequisite
           gap traversal, 3-step remedial pathway generation, and SVG atlas UI.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Tasks: Phase 118 — Curriculum Knowledge Graph & Dynamic Remedial Navigator

## Tasks Ledger

- [x] Task 1: Implement Curriculum Knowledge Graph Service (`backend/app/services/curriculum_knowledge_graph_service.py`)
  - DAG node and edge storage spanning Class 6 to HSC and Admission
  - Cycle detection validation ensuring acyclicity
  - Prerequisite dependency traversal (topological ancestor ordering)
  - Prerequisite gap identification for mastery $< 0.70$
  - Dynamic 3-step remedial pathway generator (5 min + 5 min + 5 min)
- [x] Task 2: Build Knowledge Graph Atlas Component (`frontend/src/components/curriculum/KnowledgeGraphAtlas.tsx`)
  - Interactive SVG topic map on Warm Ivory cartographic parchment
  - Oxford Navy nodes, mastery ring badges, and crisp hairline prerequisite connectors
  - Subject and class filter controls with zoom/pan capabilities
- [x] Task 3: Build Remedial Path Drawer Component (`frontend/src/components/curriculum/RemedialPathDrawer.tsx`)
  - Slide-over pedagogical drawer for instant gap recovery
  - 3-step trajectory display with 5-minute timers
  - KaTeX mathematical formula rendering
  - 3D tactile button: "প্রতিকারমূলক পাঠ শুরু করো" (`shadow-[0_4px_0_0_#065F46]`)
- [x] Task 4: Implement REST Endpoints & Mount Router (`backend/app/api/v1/endpoints/knowledge_graph.py` and `router.py`)
  - Endpoints: get atlas graph, get topic prerequisites, generate remedial pathway
  - Mount in `backend/app/api/v1/router.py`
- [x] Task 5: Automated Test Suite (`backend/tests/test_phase118_knowledge_graph.py`)
  - Assert DAG cycle detection and acyclicity
  - Assert prerequisite ancestor traversal in topological order
  - Assert gap identification and 3-step remedial pathway synthesis
  - Assert tactile 3D buttons, KaTeX formulas, and SVG rendering in frontend components
  - Assert Developer Architecture Notes and strict zero emojis across all Phase 118 files
- [x] Task 6: Platform Regression Discovery & Certification
  - Run zero-emoji sweep, security audit, and full platform discovery across 1,378+ tests
