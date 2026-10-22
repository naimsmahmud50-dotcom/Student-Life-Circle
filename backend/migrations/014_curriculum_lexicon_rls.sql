/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bilingual Curriculum Engine & NCTB Terminology Lexicon
 * TOPIC:     Phase 136 Instant Medium Switcher & Contextual Academic Terminology
 * FILE:      backend/migrations/014_curriculum_lexicon_rls.sql
 * PHASE:     Phase 136 - Dual-Curriculum Bilingual Terminology Switcher
 * PURPOSE:   Database migration schema establishing nctb_lexicon_entries,
 *            bilingual_exam_templates, student_medium_preferences, and
 *            lexicon_search_logs tables with strict Supabase RLS.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Pure Academic Design, NCTB Aligned
 */

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. NCTB Terminology Lexicon Entries Table
CREATE TABLE IF NOT EXISTS public.nctb_lexicon_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    term_id VARCHAR(64) NOT NULL UNIQUE,
    term_en VARCHAR(255) NOT NULL,
    term_bn VARCHAR(255) NOT NULL,
    phonetic_en VARCHAR(128),
    phonetic_bn VARCHAR(128),
    subject VARCHAR(64) NOT NULL,
    grade_tier VARCHAR(32) NOT NULL DEFAULT 'HSC',
    definition_en TEXT NOT NULL,
    definition_bn TEXT NOT NULL,
    nctb_code VARCHAR(64) NOT NULL,
    formula_latex TEXT,
    synonyms_en JSONB NOT NULL DEFAULT '[]'::jsonb,
    synonyms_bn JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_verified BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Bilingual Exam Question Templates Table
CREATE TABLE IF NOT EXISTS public.bilingual_exam_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id VARCHAR(64) NOT NULL UNIQUE,
    subject VARCHAR(64) NOT NULL,
    grade_tier VARCHAR(32) NOT NULL DEFAULT 'HSC',
    prompt_bn TEXT NOT NULL,
    prompt_en TEXT NOT NULL,
    options_bn JSONB NOT NULL DEFAULT '[]'::jsonb,
    options_en JSONB NOT NULL DEFAULT '[]'::jsonb,
    correct_index INTEGER NOT NULL DEFAULT 0,
    explanation_bn TEXT,
    explanation_en TEXT,
    matched_lexicon_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Student Medium Preferences Table
CREATE TABLE IF NOT EXISTS public.student_medium_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(64) NOT NULL UNIQUE,
    preferred_medium VARCHAR(32) NOT NULL DEFAULT 'BANGLA',
    enable_inline_gloss BOOLEAN NOT NULL DEFAULT TRUE,
    enable_dual_column BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Lexicon Search Audit Logs Table
CREATE TABLE IF NOT EXISTS public.lexicon_search_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    log_id VARCHAR(64) NOT NULL UNIQUE,
    user_id VARCHAR(64) NOT NULL,
    search_query VARCHAR(255) NOT NULL,
    subject_filter VARCHAR(64),
    matched_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. High-Performance Search Indexes
CREATE INDEX IF NOT EXISTS idx_lexicon_term_en ON public.nctb_lexicon_entries(term_en);
CREATE INDEX IF NOT EXISTS idx_lexicon_term_bn ON public.nctb_lexicon_entries(term_bn);
CREATE INDEX IF NOT EXISTS idx_lexicon_subject ON public.nctb_lexicon_entries(subject);
CREATE INDEX IF NOT EXISTS idx_lexicon_nctb_code ON public.nctb_lexicon_entries(nctb_code);
CREATE INDEX IF NOT EXISTS idx_bilingual_questions_subj ON public.bilingual_exam_templates(subject);
CREATE INDEX IF NOT EXISTS idx_student_medium_pref ON public.student_medium_preferences(student_id);

-- 7. Enable and Force Row Level Security (100% RLS Enforcement)
ALTER TABLE public.nctb_lexicon_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nctb_lexicon_entries FORCE ROW LEVEL SECURITY;

ALTER TABLE public.bilingual_exam_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bilingual_exam_templates FORCE ROW LEVEL SECURITY;

ALTER TABLE public.student_medium_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_medium_preferences FORCE ROW LEVEL SECURITY;

ALTER TABLE public.lexicon_search_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lexicon_search_logs FORCE ROW LEVEL SECURITY;

-- 8. Policies for NCTB Lexicon Entries (Public Academic Reference)
DROP POLICY IF EXISTS lexicon_entries_select ON public.nctb_lexicon_entries;
CREATE POLICY lexicon_entries_select ON public.nctb_lexicon_entries
    FOR SELECT
    USING (TRUE);

DROP POLICY IF EXISTS lexicon_entries_admin_all ON public.nctb_lexicon_entries;
CREATE POLICY lexicon_entries_admin_all ON public.nctb_lexicon_entries
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role' OR
        auth.jwt() ->> 'email' LIKE '%@nctb.gov.bd'
    );

-- 9. Policies for Bilingual Exam Templates (Public Exam Reference)
DROP POLICY IF EXISTS exam_templates_select ON public.bilingual_exam_templates;
CREATE POLICY exam_templates_select ON public.bilingual_exam_templates
    FOR SELECT
    USING (TRUE);

DROP POLICY IF EXISTS exam_templates_admin_all ON public.bilingual_exam_templates;
CREATE POLICY exam_templates_admin_all ON public.bilingual_exam_templates
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role' OR
        auth.jwt() ->> 'email' LIKE '%@edu.bd'
    );

-- 10. Policies for Student Medium Preferences (Strict Tenant Isolation)
DROP POLICY IF EXISTS medium_pref_student_select ON public.student_medium_preferences;
CREATE POLICY medium_pref_student_select ON public.student_medium_preferences
    FOR SELECT
    USING (
        (auth.uid())::text = student_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS medium_pref_student_insert ON public.student_medium_preferences;
CREATE POLICY medium_pref_student_insert ON public.student_medium_preferences
    FOR INSERT
    WITH CHECK (
        (auth.uid())::text = student_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS medium_pref_student_update ON public.student_medium_preferences;
CREATE POLICY medium_pref_student_update ON public.student_medium_preferences
    FOR UPDATE
    USING (
        (auth.uid())::text = student_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS medium_pref_service_all ON public.student_medium_preferences;
CREATE POLICY medium_pref_service_all ON public.student_medium_preferences
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role'
    );

-- 11. Policies for Lexicon Search Logs (Tenant Privacy)
DROP POLICY IF EXISTS search_logs_student_select ON public.lexicon_search_logs;
CREATE POLICY search_logs_student_select ON public.lexicon_search_logs
    FOR SELECT
    USING (
        (auth.uid())::text = user_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS search_logs_student_insert ON public.lexicon_search_logs;
CREATE POLICY search_logs_student_insert ON public.lexicon_search_logs
    FOR INSERT
    WITH CHECK (
        (auth.uid())::text = user_id OR
        auth.jwt() ->> 'role' = 'service_role'
    );

DROP POLICY IF EXISTS search_logs_service_all ON public.lexicon_search_logs;
CREATE POLICY search_logs_service_all ON public.lexicon_search_logs
    FOR ALL
    USING (
        auth.jwt() ->> 'role' = 'service_role'
    );
