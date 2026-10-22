# SPEC: Phase 132 — Real-time Socratic AI Math & Science Whiteboard Solver with Interactive Canvas

## 1. Overview
Phase 132 introduces the **Real-time Socratic AI Math & Science Whiteboard Solver**, an interactive digital laboratory combining an HTML5 tactile canvas with a pedagogical inquiry engine. Rather than functioning as a direct answer dispenser, the system employs the Socratic dialogue method to guide students through mathematical proofs, calculus derivations, Newtonian physics dynamics, and chemical stoichiometry via calibrated pedagogical hints, intermediate step verification, and misconception detection.

## 2. Architectural Pillars
1. **Developer Architecture Note Standard**: Mandatory block comment at the top of every Phase 132 file.
2. **Pedagogical Hint Guard**: Rejects instant solution dumping. Enforces a multi-tiered scaffolding model:
   - Level 1: Conceptual Orientation & Foundational Theorems
   - Level 2: Strategic Direction & Variable Decomposition
   - Level 3: Intermediate Step Inquiry & Guiding Questions
   - Level 4: Remediation on Detected Misconceptions
3. **Interactive Whiteboard Canvas**: Paper Ivory canvas (`#FAFAF8`) with drawing instruments (Pencil, Ruler, Compass/Circle tool, Eraser), KaTeX mathematical notation, and stroke persistence.
4. **ASVS L2 & Supabase Tenancy Lockdown**: Strict Row Level Security (RLS) on all whiteboard sessions, stroke buffers, and step attempt tables with `auth.uid() = user_id`.
5. **Zero-AI Vibe & Pure Academic Styling**: Oxford Academic Navy (`#0A2540`), Scholar Gold (`#B45309`), 3D tactile buttons (`shadow-[0_4px_0_0_#051329] active:translate-y-1`), and pure 1.75px Lucide vector SVG icons with 0% emojis.

## 3. Component Architecture
- `backend/socratic/__init__.py`: Package entrypoint exposing solver models and controllers.
- `backend/socratic/whiteboard_solver.py`: Socratic reasoning engine, misconception analyzer, stroke serialization validator, and pedagogical hint coordinator.
- `backend/migrations/010_socratic_whiteboard_rls.sql`: Database schema with 100% RLS enforcement.
- `frontend/src/pages/socratic/solver.tsx`: React/Next.js interactive whiteboard UI with HTML5 canvas and Socratic dialogue sidebar.
- `backend/tests/test_phase132_socratic_whiteboard.py`: Comprehensive test suite verifying all architectural invariants.
