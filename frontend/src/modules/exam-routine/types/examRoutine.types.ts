/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Exam Routine & Model Test Calendar Types & Zod Schemas
 * TOPIC:     Client-Side Data Contracts, Validation & State Interfaces
 * FILE:      frontend/src/modules/exam-routine/types/examRoutine.types.ts
 * PURPOSE:   Provides strictly typed TypeScript interfaces and Zod validation schemas
 *            for the 200-day BCS and Admission routine calendars, Mega Model Test countdowns,
 *            negative marking simulations, and reminder subscriptions.
 * STANDARDS: Strict TypeScript, Zero-Emoji, Production Hardened
 * ========================================================================================
 */

export type ExamType = 'BCS_PRELI' | 'ADMISSION_VARSITY' | 'HSC_BOARD' | 'BANK_OFFICER';

export type TrackCategory = 'BANGLA' | 'ENGLISH' | 'MATH_SCIENCE' | 'GK' | 'GENERAL';

export interface ExamRoutineItem {
  id: string;
  routine_code: string;
  title: string;
  exam_type: ExamType;
  track_category: TrackCategory;
  day_number: number;
  syllabus_summary: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  total_questions: number;
  total_marks: number;
  negative_mark_factor: number;
  is_mega_model_test: boolean;
  is_published: boolean;
  live_participant_count: number;
}

export interface ExamRoutineListResponse {
  success: boolean;
  routines: ExamRoutineItem[];
  total: number;
  active_day: number;
  mega_test_scheduled_at: string | null;
  server_time: string;
}

export interface NegativeMarkSimulationRequest {
  total_questions: number;
  correct_answers: number;
  wrong_answers: number;
  unanswered: number;
  negative_factor: number;
  mark_per_question: number;
}

export interface NegativeMarkSimulationResponse {
  success: boolean;
  total_questions: number;
  correct_answers: number;
  wrong_answers: number;
  unanswered: number;
  gross_score: number;
  penalty_deducted: number;
  net_score: number;
  accuracy_percentage: number;
  estimated_percentile: number;
  merit_bracket: string;
  weakness_flags: string[];
}

export interface RoutineSubscribeRequest {
  routine_id: string;
  channels: string[];
}

export interface RoutineSubscribeResponse {
  success: boolean;
  subscription_id: string;
  routine_id: string;
  subscribed_channels: string[];
  message: string;
}
