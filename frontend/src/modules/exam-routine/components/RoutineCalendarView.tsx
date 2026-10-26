/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    RoutineCalendarView Component
 * TOPIC:     200-Day Timeline Calendar & Examination Cards
 * FILE:      frontend/src/modules/exam-routine/components/RoutineCalendarView.tsx
 * PURPOSE:   Renders scheduled daily exam cards with syllabus summaries, negative marking
 *            rules, participant badges, and instant subscription alert triggers.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji, Zero-CLS
 * ========================================================================================
 */

import React from 'react';
import Link from 'next/link';
import { 
  Calendar, 
  Clock, 
  Users, 
  AlertCircle, 
  Bell, 
  CheckCircle2, 
  ChevronRight,
  BookOpen,
  Award
} from 'lucide-react';
import { ExamRoutineItem } from '../types/examRoutine.types';

interface RoutineCalendarViewProps {
  routines: ExamRoutineItem[];
  isLoading: boolean;
  onSelectRoutineForSub: (routine: ExamRoutineItem) => void;
}

export const RoutineCalendarView: React.FC<RoutineCalendarViewProps> = ({
  routines,
  isLoading,
  onSelectRoutineForSub,
}) => {
  if (isLoading) {
    return (
      <div className="space-y-4" aria-busy="true" aria-label="রুটিন লোড হচ্ছে">
        {[1, 2, 3].map((n) => (
          <div
            key={n}
            className="animate-pulse rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900 h-40"
          />
        ))}
      </div>
    );
  }

  if (routines.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center dark:border-slate-800 dark:bg-slate-900">
        <Calendar className="h-10 w-10 text-slate-400 mb-3" />
        <h3 className="text-base font-semibold text-slate-800 dark:text-slate-200">
          কোনো রুটিন পাওয়া যায়নি
        </h3>
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 max-w-sm">
          আপনার নির্বাচিত ফিল্টার বা অনুসন্ধানের সাথে মিল রেখে কোনো পরীক্ষা খুঁজে পাওয়া যায়নি। অন্য ফিল্টার নির্বাচন করুন।
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4" role="feed" aria-label="দৈনিক পরীক্ষার রুটিন তালিকা">
      {routines.map((routine) => {
        const isMega = routine.is_mega_model_test;

        return (
          <article
            key={routine.id}
            className={`relative overflow-hidden rounded-xl border transition-all duration-200 ${
              isMega
                ? 'border-emerald-600/40 bg-gradient-to-r from-emerald-950/20 via-slate-900 to-slate-900 dark:border-emerald-500/50 dark:bg-slate-900/90 shadow-md'
                : 'border-slate-200 bg-white hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-slate-700 shadow-sm'
            } p-5 sm:p-6`}
          >
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
              {/* Day & Code Header */}
              <div className="space-y-2 max-w-3xl">
                <div className="flex flex-wrap items-center gap-2">
                  <span
                    className={`inline-flex items-center gap-1 rounded-md px-2.5 py-0.5 text-xs font-bold ${
                      isMega
                        ? 'bg-emerald-600 text-white'
                        : 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200'
                    }`}
                  >
                    {isMega ? <Award className="h-3 w-3" /> : <Calendar className="h-3 w-3" />}
                    <span>দিন {routine.day_number} {isMega ? '(মেগা মডেল টেস্ট)' : ''}</span>
                  </span>

                  <span className="font-mono text-[11px] text-slate-400 dark:text-slate-500">
                    {routine.routine_code}
                  </span>

                  <span className="rounded-full border border-slate-200 bg-slate-50 px-2 py-0.5 text-[10px] font-medium text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400">
                    {routine.exam_type.replace('_', ' ')}
                  </span>
                </div>

                <h3 className="text-base sm:text-lg font-serif font-bold text-slate-900 dark:text-slate-100 leading-snug">
                  {routine.title}
                </h3>

                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                  <span className="font-semibold text-slate-700 dark:text-slate-200">সিলেবাস: </span>
                  {routine.syllabus_summary}
                </p>

                {/* Meta details */}
                <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-slate-500 dark:text-slate-400">
                  <span className="flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5 text-slate-400" />
                    <span>{routine.duration_minutes} মিনিট</span>
                  </span>

                  <span className="h-3 w-px bg-slate-200 dark:bg-slate-800" />

                  <span className="flex items-center gap-1">
                    <BookOpen className="h-3.5 w-3.5 text-slate-400" />
                    <span>{routine.total_questions}টি প্রশ্ন ({routine.total_marks} নম্বর)</span>
                  </span>

                  <span className="h-3 w-px bg-slate-200 dark:bg-slate-800" />

                  <span className="flex items-center gap-1 text-amber-600 dark:text-amber-400 font-medium">
                    <AlertCircle className="h-3.5 w-3.5" />
                    <span>নেগেটিভ মার্ক: -{routine.negative_mark_factor}</span>
                  </span>

                  <span className="h-3 w-px bg-slate-200 dark:bg-slate-800" />

                  <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                    <Users className="h-3.5 w-3.5" />
                    <span>{routine.live_participant_count.toLocaleString()} অংশ নিচ্ছেন</span>
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex sm:flex-col items-center sm:items-end justify-end gap-2.5 pt-2 sm:pt-0 shrink-0">
                <button
                  type="button"
                  onClick={() => onSelectRoutineForSub(routine)}
                  className="inline-flex items-center justify-center gap-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 px-3.5 py-2 text-xs font-semibold text-slate-700 transition-colors dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                >
                  <Bell className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
                  <span>অ্যালার্ট নিন</span>
                </button>

                <Link
                  href="/live-challenge"
                  className="inline-flex items-center justify-center gap-1 rounded-lg bg-slate-900 hover:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-white transition-colors dark:bg-emerald-600 dark:hover:bg-emerald-500"
                >
                  <span>অংশগ্রহণ করুন</span>
                  <ChevronRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          </article>
        );
      })}
    </div>
  );
};
