<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
FILE:      specs/016-phase112-nctb-board-archives/tasks.md
PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
PURPOSE:   Tracks deliverables for the authentic NCTB board question paper archive,
           KaTeX mathematical bank, dual-mode examination viewer, and automated test suite.
STANDARDS: NCTB Curriculum 2024, KaTeX Math Spec, UI/UX Pro Max, Strict Zero-Emoji
-->

# Tasks: Phase 112 — Official NCTB Board Archives & KaTeX Mathematical Bank

## Tasks Ledger

- [x] Task 1: Generate NCTB Board Past Papers Seed Data (`backend/app/db/seeds/nctb_board_past_papers_2015_2025.json`)
  - Cover SSC and HSC Physics, Chemistry, Higher Math, Biology, and ICT from 2015 to 2025 across all boards
  - Creative Questions (CQ) with 4-tier sub-questions and marking schemes
  - Multiple Choice Questions (MCQ) with 4 options and detailed KaTeX explanations
  - Zero duplicate content hashes and balanced LaTeX delimiters
- [x] Task 2: Implement Board Archive Service (`backend/app/services/board_archive_service.py`)
  - Sub-millisecond indexed query engine with caching
  - Multi-attribute filtering (board, year, subject, paper, chapter, type, query)
  - Facet extraction and curriculum coverage analytics
  - Archive integrity validator
- [x] Task 3: Build Printable Exam Paper & Solution Viewer (`frontend/src/components/curriculum/BoardQuestionArchiveViewer.tsx`)
  - Authentic Bangladesh board examination paper aesthetics (Oxford Navy, ivory canvas, official header)
  - Exam Mode (answers hidden, printable) vs Study Mode (step-by-step KaTeX solutions, rubrics)
  - Sub-pixel KaTeX LaTeX formula rendering
  - Tactile 3D Oxford Navy button depth
- [x] Task 4: Create Board Archives Explorer Page (`frontend/src/pages/board-archives.tsx`)
  - Global Navbar & Footer integration
  - Interactive board and subject filter chips
  - Curriculum coverage stats bento card
- [x] Task 5: Implement Automated Unit & Integration Tests (`backend/tests/test_phase112_board_archives.py`)
  - Verify seed data integrity, 2015-2025 year range, and zero duplicate hashes
  - Verify KaTeX formula syntax and balanced delimiters
  - Verify filter performance and facet analytics
  - Verify Developer Architecture Notes and strict Zero-Emoji compliance
- [x] Task 6: Platform Regression Discovery & Certification
  - Run full platform test suite (`python3 -m unittest discover -s backend/tests`)
  - Run security and zero-emoji sweeps
