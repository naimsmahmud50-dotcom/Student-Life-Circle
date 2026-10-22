<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
FILE:      specs/016-phase112-nctb-board-archives/plan.md
PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
PURPOSE:   Engineering roadmap for building the official NCTB board questions archive,
           KaTeX formula indexing, Exam/Study mode viewer, and zero-regression testing.
STANDARDS: NCTB Curriculum 2024, KaTeX Math Spec, UI/UX Pro Max, Strict Zero-Emoji
-->

# Implementation Plan: Phase 112 — Official NCTB Board Archives & KaTeX Mathematical Bank

## Step-by-Step Implementation Roadmap

1. **Step 1: Seed Data Generation (`backend/app/db/seeds/nctb_board_past_papers_2015_2025.json`)**
   - Compile authentic board papers spanning SSC and HSC across Physics, Chemistry, Higher Mathematics, Biology, and ICT from 2015 to 2025.
   - Include both Creative Questions (CQ) with 4-tier sub-questions (জ্ঞান, অনুধাবন, প্রয়োগ, উচ্চতর দক্ষতা) and MCQs.
   - Embed KaTeX LaTeX equations in Bengali context.
   - Calculate cryptographic SHA-256 content hashes.

2. **Step 2: Board Archive Backend Service (`backend/app/services/board_archive_service.py`)**
   - Implement `BoardArchiveService` with in-memory caching and sub-millisecond retrieval.
   - Implement `filter_papers(...)`, `get_paper_by_id(...)`, `get_available_facets()`, `get_curriculum_coverage_stats()`, and `verify_archive_integrity()`.

3. **Step 3: Printable Exam & Study Viewer (`frontend/src/components/curriculum/BoardQuestionArchiveViewer.tsx`)**
   - Build dual-mode viewer (Exam Mode vs Study Mode).
   - Display authentic Bangladesh board header with seal, time, and total marks.
   - KaTeX rendering with sub-pixel typography.
   - Print stylesheet integration (`@media print`).

4. **Step 4: Dedicated Explorer Page (`frontend/src/pages/board-archives.tsx`)**
   - Implement responsive page with academic Oxford Navy branding.
   - Sticky filter bar with tactile 3D buttons.
   - Seamless integration with Navbar, Footer, and internationalization.

5. **Step 5: Automated Verification Test Suite (`backend/tests/test_phase112_board_archives.py`)**
   - Verify seed schema compliance, 2015-2025 year range, zero duplicate content hashes, balanced KaTeX math delimiters, query performance, and strict zero-emoji enforcement.

6. **Step 6: Full Platform Regression Discovery**
   - Run `python3 -m unittest discover -s backend/tests` to assert 100% pass rate across all 1,340+ tests.
