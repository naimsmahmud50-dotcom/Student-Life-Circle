/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Quiz Interface - Exam & Practice Progress Component
 * TOPIC:     Academic Exam Progress Bar, Question Counter & Bilingual Numeral Support
 * FILE:      frontend/src/components/quiz/quiz-progress.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides clean academic progress tracking for exams and practice sessions:
 *            1. Progress Bar: Smooth CSS width transition with hairline border.
 *            2. Question Counter: "প্রশ্ন ৫ / ২০" in Bengali or English.
 *            3. Score/Streak Indicators: Minimal, low-contrast status tags.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React from 'react';
import { cn } from '@/lib/utils';
import { Clock, Flame, Award } from 'lucide-react';

export interface QuizProgressProps {
  currentQuestion: number;
  totalQuestions: number;
  timeRemaining?: string;
  score?: number;
  streak?: number;
  isBengali?: boolean;
  className?: string;
}

export const QuizProgress: React.FC<QuizProgressProps> = ({
  currentQuestion,
  totalQuestions,
  timeRemaining,
  score,
  streak,
  isBengali = true,
  className,
}) => {
  const percentage = Math.min(100, Math.max(0, Math.round((currentQuestion / totalQuestions) * 100)));

  const toBengaliNumber = (num: number): string => {
    if (!isBengali) return num.toString();
    const bnDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return num.toString().split('').map(d => bnDigits[parseInt(d, 10)] || d).join('');
  };

  return (
    <div className={cn("w-full bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] rounded-xl p-4 space-y-3", className)}>
      <div className="flex items-center justify-between text-xs sm:text-sm font-sans">
        <div className="flex items-center gap-2">
          <span className="font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB]">
            {isBengali ? "প্রশ্ন" : "Question"}{" "}
            <span className="text-[#0B5D3B] dark:text-emerald-400">
              {toBengaliNumber(currentQuestion)}
            </span>{" "}
            / {toBengaliNumber(totalQuestions)}
          </span>
          <span className="text-[11px] text-[#5B5B5B] dark:text-slate-400">
            ({toBengaliNumber(percentage)}%)
          </span>
        </div>

        <div className="flex items-center gap-3 text-xs">
          {streak !== undefined && streak > 0 && (
            <div className="inline-flex items-center gap-1 text-[#B8862B] font-semibold">
              <Flame className="w-3.5 h-3.5" />
              <span>{toBengaliNumber(streak)} {isBengali ? "স্ট্রিক" : "streak"}</span>
            </div>
          )}

          {score !== undefined && (
            <div className="inline-flex items-center gap-1 text-[#0B5D3B] dark:text-emerald-400 font-semibold">
              <Award className="w-3.5 h-3.5" />
              <span>{toBengaliNumber(score)} {isBengali ? "স্কোর" : "pts"}</span>
            </div>
          )}

          {timeRemaining && (
            <div className="inline-flex items-center gap-1 text-[#5B5B5B] dark:text-slate-400 font-mono">
              <Clock className="w-3.5 h-3.5" />
              <span>{timeRemaining}</span>
            </div>
          )}
        </div>
      </div>

      {/* Progress Track */}
      <div className="w-full h-2 rounded-full bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] overflow-hidden">
        <div
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={isBengali ? "অগ্রগতি" : "Progress"}
          className="h-full bg-[#0B5D3B] dark:bg-emerald-500 rounded-full transition-all duration-200 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
