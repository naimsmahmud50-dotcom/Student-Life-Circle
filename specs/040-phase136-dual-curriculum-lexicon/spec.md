# SPECIFICATION: Phase 136 — Dual-Curriculum English Version / Bangla Medium Auto-Localization Switcher with NCTB Terminology Lexicon

## 1. Context & Purpose
In Bangladesh, high school (SSC) and college (HSC) students follow two distinct tracks under the National Curriculum and Textbook Board (NCTB):
- **Bangla Medium**: Taught and examined entirely in Bengali.
- **English Version**: Uses the exact same NCTB curriculum, learning outcomes, syllabus, and textbook structure, but translated into English.

Students frequently face barriers when consulting cross-medium reference books, transitioning from Bangla Medium school to English Version college (or vice-versa), and preparing for university admission tests where bilingual clarity is vital.

Phase 136 delivers an institutional-grade **Bilingual Curriculum Engine & NCTB Terminology Lexicon** that provides bidirectional terminology mapping for STEM subjects, contextual definitions in both languages, and a real-time medium switcher for examination questions (Bangla, English Version, Parallel Dual-Column, and Inline-Glossed).

---

## 2. Developer Architecture Note
Every created or modified file must include the mandatory header:
```
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bilingual Curriculum Engine & NCTB Terminology Lexicon
 * TOPIC:     Phase 136 Instant Medium Switcher & Contextual Academic Terminology
 * FILE:      [File Path]
 * PHASE:     Phase 136 - Dual-Curriculum Bilingual Terminology Switcher
 * PURPOSE:   [Architectural Purpose]
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Pure Academic Design, NCTB Aligned
 */
```

---

## 3. Core Functional Requirements

### 3.1. NCTB Science & Math Lexicon Service
1. **Curriculum Domains**:
   - Physics (পদার্থবিজ্ঞান)
   - Chemistry (রসায়ন)
   - Higher Mathematics (উচ্চতর গণিত)
   - Biology (জীববিজ্ঞান)
   - General Science & Mathematics (সাধারণ বিজ্ঞান ও গণিত)
2. **Bidirectional Mapping**:
   - Exact term in Bengali (`term_bn`, e.g. "গতিবিদ্যা", "পর্যায় সারণি", "অম্ল-ক্ষারক সাম্যাবস্থা")
   - Official NCTB English equivalent (`term_en`, e.g. "Kinematics", "Periodic Table", "Acid-Base Equilibrium")
   - Phonetic guide / Pronunciation
   - Contextual definition in Bengali (`definition_bn`)
   - Contextual definition in English (`definition_en`)
   - Official NCTB chapter code (`nctb_chapter_code`, e.g. `NCTB-PHY-C02-KINEMATICS`)
   - Grade level (`SSC`, `HSC`, `ADMISSION`)
3. **Glossary Query Engine**:
   - Search by keyword (supports both Bengali unicode search and English substring matching).
   - Filter by subject, grade level, and chapter code.
   - Exact term lookup in $O(1)$ time complexity using indexed bidirectional hash mappings.

### 3.2. Dual-Curriculum Exam Question Auto-Localization
1. **Localization Modes**:
   - `MEDIUM_BANGLA`: Native Bengali text, Bengali numerals (১, ২, ৩), and standard NCTB Bengali phrasing.
   - `MEDIUM_ENGLISH_VERSION`: Standard English Version phrasing with English numerals (1, 2, 3).
   - `MEDIUM_BILINGUAL_PARALLEL`: Synchronized side-by-side view with aligned question numbers and stimulus texts.
   - `MEDIUM_INLINE_GLOSS`: Primary medium with reciprocal technical terms embedded in non-intrusive semantic pill annotations.
2. **Auto-Glossing Algorithm**:
   - Scans arbitrary academic STEM questions, identifies matching NCTB lexicon entries, and annotates them with reciprocal translations and hoverable tooltips.

### 3.3. Database Security & Migration (`014_curriculum_lexicon_rls.sql`)
1. Four dedicated tables:
   - `public.nctb_lexicon_entries`
   - `public.bilingual_exam_templates`
   - `public.student_medium_preferences`
   - `public.lexicon_search_logs`
2. 100% Row Level Security (RLS) enforcement with `ENABLE` and `FORCE ROW LEVEL SECURITY`.
3. Tenant isolation with `auth.uid() = user_id` and service role administrative bypass.

### 3.4. Frontend Journal Console (`frontend/src/pages/curriculum/lexicon.tsx`)
1. Journal-grade aesthetics:
   - Bengali Font: `Hind Siliguri`
   - English Font: `Plus Jakarta Sans` / `Inter`
   - Color Scheme: Oxford Navy (`#0A2540`, `#051329`), NCTB Forest Emerald (`#065F46`), Academic Gold/Amber (`#B45309`), Crisp Off-white (`#F8FAFC`).
2. Mode switchers:
   - Instant 1-click medium toggle (`Bangla` $\leftrightarrow$ `English Version`).
   - Side-by-side dual-column layout toggle.
   - Inline technical term glossing toggle.
3. Interactive Searchable Lexicon Explorer with subject filtering and detailed modal/drawer cards.
4. 3D tactile push buttons (`shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`).
5. Zero-Emoji compliance (pure Lucide vector icons).

---

## 4. Verification Standards
- Zero-Emoji sweep across all created files (0 violations).
- 100% unit test coverage for Phase 136 service and models.
- Full regression check across all 1,515 existing tests (no failures, no errors).
- Next.js static build generating 37/37 pages.
- Live probe returning HTTP 200 OK for `/curriculum/lexicon`.
