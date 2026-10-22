# SPECIFICATION: Phase 129 — Multi-Dialect Regional Audio Tutoring & Voice Viva-Voce Evaluator

## 1. Executive Summary & Objective
Phase 129 introduces the Multi-Dialect Regional Audio Tutoring & Voice Viva-Voce Evaluator for the Ogrojatra student platform. This engine provides real-time acoustic oral examination evaluation aligned with NCTB practical viva-voce rubrics. It features native dialect tolerance and phonetic normalization for regional colloquial speech (Chittagong, Sylhet, Barisal, and Standard Colloquial Bengali), ensuring fair, bias-free, and supportive assessment for students across all divisions of Bangladesh.

## 2. Mandatory Architectural Standards
- **Standardized Developer Architecture Note**: Every created or modified file MUST feature the standardized block header documenting Phase 129, ASVS L2, and Privacy By Design standards.
- **Pure Academic Laboratory Visual Philosophy (Zero AI Vibe)**:
  * Formal examination audio laboratory aesthetic (British Council / National Examination Board style).
  * No glowing neon waveforms or disco audio ripples. Clean, segmented acoustic level meters and high-contrast decibel indicators.
  * Oxford Academic Navy (`#0A2540`) dominant framework, Paper White (`#FFFFFF`) cards, and Warm Paper Ivory (`#FAFAF8`) surfaces.
  * 3D tactile buttons with physical bottom ledge: `bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg`.
  * Strict Zero-Emoji Rule: 100% pure Lucide-React SVG vector icons only.

## 3. Technical Requirements

### A. Backend Dialect Adaptation & Rubric Engine (`backend/audio/viva_evaluator.py`)
1. **Dialect Normalization & Tolerance**:
   - Supports 4 major dialect modes:
     * `STANDARD_BANGLA`: Standard Colloquial Bengali (প্রমিত চলিত বাংলা).
     * `CHITTAGONG`: Chittagonian dialect (চাটগাঁইয়া কথ্যরীতি).
     * `SYLHET`: Sylheti dialect (সিলেটি কথ্যরীতি).
     * `BARISAL`: Barisali / Southern coastal dialect (বরিশাইল্যা কথ্যরীতি).
   - Phonetic and lexical normalizer converts regional speech markers into academic standard Bengali tokens without discarding contextual meaning.
2. **NCTB 4-Tier Viva-Voce Evaluation Rubric**:
   - **Conceptual Accuracy (ধারণাগত নির্ভুলতা)** - 40% (0–40 marks):
     * Validates presence of fundamental scientific principles, laws, and logical causality.
   - **Terminology & Scientific Precision (পারিভাষিক ও বৈজ্ঞানিক নির্ভুলতা)** - 30% (0–30 marks):
     * Evaluates correct usage of domain nomenclature and NCTB textbook terminology.
   - **Articulation, Fluency & Structure (বাচনিক উপস্থাপন ও কাঠামো)** - 20% (0–20 marks):
     * Assesses speech rate (WPM), structural coherence, and minimal hesitations.
   - **Dialect Accommodation & Acoustic Confidence (আঞ্চলিক বাচনিক অভিযোজন)** - 10% (0–10 marks):
     * Explicitly credits regional expressive confidence, eliminating geographic linguistic bias.
3. **Privacy by Design & Ephemeral In-Memory Buffering (ASVS L2)**:
   - Voice audio streams are processed entirely in-memory.
   - Strict 15-minute (900 seconds) TTL: Audio buffers are wiped automatically after evaluation.
   - Zero permanent voice biometrics or raw WAV/MP3 files stored on disks.
   - Zero collection of PII (names, roll numbers, or contact details).

### B. Supabase Security & RLS (`backend/migrations/007_viva_evaluator_rls.sql`)
1. **Table `viva_evaluations`**:
   - Stores rubric score breakdowns, question ID, dialect code, and calculated grade.
   - Explicit flag `audio_retained = FALSE` certifying compliance.
   - Retention expiration timestamp `expires_at = NOW() + INTERVAL '15 minutes'`.
2. **Row Level Security (RLS)**:
   - Enabled and forced on all evaluation telemetry.
   - `auth.uid() = student_id` for read/insert.
   - Immutability check prohibiting modifications to historical examination grades.

### C. Frontend Oral Exam Audio Booth (`frontend/src/pages/viva/evaluator.tsx`)
1. **Audio Laboratory Console**:
   - Dialect selector toggle with regional descriptions.
   - Microphone status monitor with real-time level gauge.
   - 3D tactile control buttons: `রেকর্ডিং শুরু করুন`, `সমাপ্ত ও মূল্যায়ন করুন`, `পুনরায় শুনুন`.
2. **NCTB Oral Evaluation Scorecard**:
   - 4 Rubric breakdown cards with marks and percentages.
   - Overall grade letter badge (A+, A, B, etc.) and qualitative feedback in Bengali & English.
   - Parallel transcript display showing spoken dialect input alongside normalized academic Bengali.

### D. Automated Verification Suite (`backend/tests/test_phase129_viva_evaluator.py`)
- Mathematical rubric scoring checks.
- Dialect normalization parity across Chittagong, Sylhet, Barisal.
- Ephemeral 15-minute buffer eviction test.
- Zero-Emoji and Developer Architecture Note compliance.
