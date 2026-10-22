-- ==============================================================================
-- DEVELOPER ARCHITECTURE NOTE:
-- MODULE:    Socratic Math & Science Whiteboard Solver
-- TOPIC:     Phase 132 Interactive Canvas & Pedagogical Socratic Step Guidance
-- FILE:      backend/migrations/010_socratic_whiteboard_rls.sql
-- PHASE:     Phase 132 - Real-time Socratic AI Whiteboard Solver
-- PURPOSE:   Database migration schema establishing socratic_whiteboard_sessions,
--            socratic_step_attempts, and socratic_saved_workbooks tables with
--            strict Supabase Row Level Security (RLS) and multi-tenant isolation.
-- STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Pedagogical Hint Guard
-- ==============================================================================

-- 1. Ensure Extension Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Socratic Whiteboard Sessions Table
CREATE TABLE IF NOT EXISTS public.socratic_whiteboard_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(64) NOT NULL UNIQUE,
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    domain VARCHAR(64) NOT NULL,
    problem_text TEXT NOT NULL,
    current_step_index INT NOT NULL DEFAULT 0,
    all_steps_completed BOOLEAN NOT NULL DEFAULT FALSE,
    stroke_buffer JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Socratic Step Attempts Table
CREATE TABLE IF NOT EXISTS public.socratic_step_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(64) NOT NULL,
    user_id UUID NOT NULL,
    step_index INT NOT NULL,
    student_submission TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    has_misconception BOOLEAN NOT NULL DEFAULT FALSE,
    remediation_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Socratic Saved Workbooks Table
CREATE TABLE IF NOT EXISTS public.socratic_saved_workbooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workbook_id VARCHAR(64) NOT NULL UNIQUE,
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(64) NOT NULL,
    canvas_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Enable & Force Row Level Security (100% Policy Enforcement)
ALTER TABLE public.socratic_whiteboard_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.socratic_whiteboard_sessions FORCE ROW LEVEL SECURITY;

ALTER TABLE public.socratic_step_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.socratic_step_attempts FORCE ROW LEVEL SECURITY;

ALTER TABLE public.socratic_saved_workbooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.socratic_saved_workbooks FORCE ROW LEVEL SECURITY;

-- 6. Row Level Security Policies: Whiteboard Sessions
DROP POLICY IF EXISTS "Users manage their own whiteboard sessions" ON public.socratic_whiteboard_sessions;
CREATE POLICY "Users manage their own whiteboard sessions"
ON public.socratic_whiteboard_sessions
FOR ALL
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 7. Row Level Security Policies: Step Attempts
DROP POLICY IF EXISTS "Users manage their own socratic step attempts" ON public.socratic_step_attempts;
CREATE POLICY "Users manage their own socratic step attempts"
ON public.socratic_step_attempts
FOR ALL
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 8. Row Level Security Policies: Saved Workbooks
DROP POLICY IF EXISTS "Users manage their own saved workbooks" ON public.socratic_saved_workbooks;
CREATE POLICY "Users manage their own saved workbooks"
ON public.socratic_saved_workbooks
FOR ALL
USING (
    (auth.uid() = user_id)
    OR (auth.jwt() ->> 'role' = 'service_role')
);

-- 9. Multi-Tenant Query Indexes
CREATE INDEX IF NOT EXISTS idx_socratic_sessions_user ON public.socratic_whiteboard_sessions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_socratic_sessions_domain ON public.socratic_whiteboard_sessions(domain);
CREATE INDEX IF NOT EXISTS idx_socratic_attempts_session ON public.socratic_step_attempts(session_id, step_index);
CREATE INDEX IF NOT EXISTS idx_socratic_workbooks_user ON public.socratic_saved_workbooks(user_id, updated_at DESC);
