<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
FILE:      specs/016-phase112-nctb-board-archives/spec.md
PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
PURPOSE:   Specifies the authentic archive of Bangladesh NCTB board past examination papers
           (2015-2025) covering SSC and HSC Physics, Chemistry, Higher Math, Biology, and ICT
           with step-by-step KaTeX mathematical solutions, Exam/Study modes, and tactile UI.
STANDARDS: NCTB Curriculum 2024, KaTeX Math Spec, UI/UX Pro Max, Strict Zero-Emoji
-->

# Feature Specification: Phase 112 — Official NCTB Board Archives & KaTeX Mathematical Bank

## 1. Objective
Provide Bangladeshi students with an authentic, prestigious digital archive of official NCTB Secondary School Certificate (SSC) and Higher Secondary Certificate (HSC) board examination questions spanning 2015 to 2025 across all boards (Dhaka, Chittagong, Rajshahi, Barisal, Sylhet, Comilla, Dinajpur, Jessore, Mymensingh, and Madrasah). The archive features:
- Pixel-perfect KaTeX LaTeX math and scientific chemical equation rendering.
- Authentic examination booklet layout modeled after physical Bangladesh board question papers (ivory paper canvas, Oxford Navy typography, watermark seal aesthetic).
- Dual Modes: **Exam Mode** (timed printable practice, hidden solutions) and **Study Mode** (full step-by-step derivations, marking rubrics, examiner notes).
- Ultra-fast indexed search and filtering by board, year, subject, paper (1st/2nd), and chapter.

## 2. Requirements & Acceptance Criteria
- **Curriculum Coverage**:
  - Educational levels: SSC and HSC.
  - Subjects: Physics (পদার্থবিজ্ঞান), Chemistry (রসায়ন), Higher Mathematics (উচ্চতর গণিত), Biology (জীববিজ্ঞান), Information & Communication Technology (তথ্য ও যোগাযোগ প্রযুক্তি).
  - Years: 2015 to 2025 inclusive.
  - Question Types: Creative Questions (CQ - সৃজনশীল) and Multiple Choice Questions (MCQ - বহুনির্বাচনি).
- **Mathematical Integrity**:
  - 100% LaTeX formulas parsed via `$..$` (inline) and `$$..$$` (display equations).
  - Balanced delimiters with zero raw syntax leak or rendering artifact.
- **Deduplication & Integrity**:
  - Every question item must contain a unique cryptographic SHA-256 content hash.
- **Academic Aesthetic**:
  - Strictly zero AI vibes (no flashy neons, cyan/purple glows, or gamified clutter).
  - Scholarly palette: Deep Oxford Academic Navy (`#0A2540`), Pure Paper White (`#FFFFFF`), Warm Ivory (`#FAFAF8`), and Regal Ink Slate (`#0B132B`).
  - Tactile 3D Oxford Navy button depth: `shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none`.
- **Zero Emoji Compliance**:
  - Pure Lucide SVG icons (`BookOpen`, `Award`, `CheckCircle`, `FileText`, `Printer`, `Eye`, `Layers`).

## 3. Architecture & Target Files
1. `backend/app/db/seeds/nctb_board_past_papers_2015_2025.json`: Structured board questions database.
2. `backend/app/services/board_archive_service.py`: High-performance query and filter service with caching.
3. `frontend/src/components/curriculum/BoardQuestionArchiveViewer.tsx`: Interactive examination paper component.
4. `frontend/src/pages/board-archives.tsx`: Dedicated public archive explorer page.
5. `backend/tests/test_phase112_board_archives.py`: Automated test suite certifying data integrity, KaTeX validity, and zero regressions.
