/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live MCQ & Mega Model Test Routine Calendar Hub
 * TOPIC:     Synchronized Routine Schedule, Mega Model Tests & Notification Subscriptions
 * FILE:      backend/migrations/017_exam_routine_and_model_test_rls.sql
 * PURPOSE:   Database migration schema establishing 200-day BCS and Admission routine schedules,
 *            synchronized Friday mega model test countdowns, negative marking penalty configurations,
 *            and user subscription alerts with strict Supabase Row-Level Security (RLS).
 * STANDARDS: Zero-Emoji, Non-destructive, Reversible, Strict Role Isolation, ASVS L2
 *
 * ROLLBACK INSTRUCTIONS:
 * ------------------------------------------------------------------------------
 * DROP TABLE IF EXISTS public.routine_subscriptions CASCADE;
 * DROP TABLE IF EXISTS public.exam_routines CASCADE;
 * ------------------------------------------------------------------------------
 */

-- 1. Ensure Extensions Availability
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Dedicated Table: Exam Routines Schedule
CREATE TABLE IF NOT EXISTS public.exam_routines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    routine_code VARCHAR(64) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    exam_type VARCHAR(64) NOT NULL, -- 'BCS_PRELI', 'ADMISSION_VARSITY', 'HSC_BOARD', 'BANK_OFFICER'
    track_category VARCHAR(64) NOT NULL DEFAULT 'GENERAL', -- 'BANGLA', 'ENGLISH', 'MATH_SCIENCE', 'GK', 'GENERAL'
    day_number INT NOT NULL DEFAULT 1,
    syllabus_summary TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    duration_minutes INT NOT NULL DEFAULT 60,
    total_questions INT NOT NULL DEFAULT 100,
    total_marks NUMERIC(6,2) NOT NULL DEFAULT 100.00,
    negative_mark_factor NUMERIC(3,2) NOT NULL DEFAULT 0.25,
    is_mega_model_test BOOLEAN NOT NULL DEFAULT FALSE,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    live_participant_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Dedicated Table: Routine Subscriptions & User Reminders
CREATE TABLE IF NOT EXISTS public.routine_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    routine_id UUID NOT NULL REFERENCES public.exam_routines(id) ON DELETE CASCADE,
    reminder_channels JSONB NOT NULL DEFAULT '["IN_APP", "PUSH"]'::jsonb,
    subscribed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_routine_user_subscription UNIQUE(user_id, routine_id)
);

-- 4. High-Performance Indexing
CREATE INDEX IF NOT EXISTS idx_exam_routines_schedule ON public.exam_routines(start_time, is_published);
CREATE INDEX IF NOT EXISTS idx_exam_routines_type ON public.exam_routines(exam_type, day_number);
CREATE INDEX IF NOT EXISTS idx_routine_subscriptions_user ON public.routine_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_routine_subscriptions_routine ON public.routine_subscriptions(routine_id);

-- 5. Row-Level Security (RLS) Lockdown
ALTER TABLE public.exam_routines ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exam_routines FORCE ROW LEVEL SECURITY;

ALTER TABLE public.routine_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.routine_subscriptions FORCE ROW LEVEL SECURITY;

-- 6. RLS Policies: Public & Student Read Access
DROP POLICY IF EXISTS "Public Read Published Routines" ON public.exam_routines;
CREATE POLICY "Public Read Published Routines" ON public.exam_routines
    FOR SELECT USING (is_published = true);

-- 7. RLS Policies: User Subscription Management
DROP POLICY IF EXISTS "User Routine Subscriptions Select" ON public.routine_subscriptions;
CREATE POLICY "User Routine Subscriptions Select" ON public.routine_subscriptions
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "User Routine Subscriptions Insert" ON public.routine_subscriptions;
CREATE POLICY "User Routine Subscriptions Insert" ON public.routine_subscriptions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "User Routine Subscriptions Delete" ON public.routine_subscriptions;
CREATE POLICY "User Routine Subscriptions Delete" ON public.routine_subscriptions
    FOR DELETE USING (auth.uid() = user_id);

-- 8. RLS Policies: Admin & Reviewer Full Access
DROP POLICY IF EXISTS "Admin Full Access Routines" ON public.exam_routines;
CREATE POLICY "Admin Full Access Routines" ON public.exam_routines
    FOR ALL USING (auth.jwt() ->> 'role' IN ('admin', 'reviewer'));

DROP POLICY IF EXISTS "Admin Full Access Subscriptions" ON public.routine_subscriptions;
CREATE POLICY "Admin Full Access Subscriptions" ON public.routine_subscriptions
    FOR ALL USING (auth.jwt() ->> 'role' IN ('admin', 'reviewer'));
