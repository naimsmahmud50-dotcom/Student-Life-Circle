/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Quiz Interface - Result Summary Component
 * TOPIC:     Academic Exam Scorecard, Accuracy Metric & Negative Penalty Ledger
 * FILE:      frontend/src/components/quiz/quiz-result-summary.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides textbook-like exam result summary scorecard:
 *            1. Net Score & Accuracy: Highlighted percentage and rank badge.
 *            2. Question Breakdown: Correct, Incorrect, Unattempted, Negative Marks.
 *            3. Actions: Review Answers, Retry Quiz, Return to Curriculum.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React from 'react';
import { CheckCircle2, XCircle, HelpCircle, Award, RotateCcw, BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

export interface QuizResultSummaryProps {
  totalQuestions: number;
  correctCount: number;
  incorrectCount: number;
  unattemptedCount: number;
  negativeMarks?: number;
  timeTaken?: string;
  isBengali?: boolean;
  onReview?: () => void;
  onRetry?: () => void;
  onBackToCurriculum?: () => void;
  className?: string;
}

export const QuizResultSummary: React.FC<QuizResultSummaryProps> = ({
  totalQuestions,
  correctCount,
  incorrectCount,
  unattemptedCount,
  negativeMarks = 0,
  timeTaken,
  isBengali = true,
  onReview,
  onRetry,
  onBackToCurriculum,
  className,
}) => {
  const netScore = Math.max(0, correctCount - negativeMarks);
  const accuracy = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;

  const toBengaliNumber = (num: number | string): string => {
    if (!isBengali) return num.toString();
    const bnDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return num.toString().split('').map(d => bnDigits[parseInt(d, 10)] || d).join('');
  };

  return (
    <div className={cn("w-full max-w-xl mx-auto bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm", className)}>
      {/* Header Deck */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#F0F7F4] dark:bg-emerald-950/40 border border-[#C8E3D7] dark:border-emerald-900 text-xs font-semibold text-[#0B5D3B] dark:text-emerald-300">
          <Award className="w-4 h-4" />
          <span>{isBengali ? "অনুশীলন মূল্যায়ন ফলাফল" : "Assessment Complete"}</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB]">
          {isBengali ? "আপনার ফলাফল সারসংক্ষেপ" : "Performance Summary"}
        </h2>
        {timeTaken && (
          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans">
            {isBengali ? `ব্যয়িত সময়: ${timeTaken}` : `Time taken: ${timeTaken}`}
          </p>
        )}
      </div>

      {/* Main Score Bento */}
      <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D]">
        <div className="text-center p-3">
          <span className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans block mb-1">
            {isBengali ? "প্রাপ্ত নেট স্কোর" : "Net Score"}
          </span>
          <span className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB]">
            {toBengaliNumber(netScore)}
            <span className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans ml-1">/ {toBengaliNumber(totalQuestions)}</span>
          </span>
        </div>

        <div className="text-center p-3 border-l border-[#E5E2DA] dark:border-[#262D3D]">
          <span className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans block mb-1">
            {isBengali ? "নির্ভুলতার হার" : "Accuracy"}
          </span>
          <span className="text-2xl sm:text-3xl font-serif font-bold text-[#0B5D3B] dark:text-emerald-400">
            {toBengaliNumber(accuracy)}%
          </span>
        </div>
      </div>

      {/* Detailed Ledger */}
      <div className="grid grid-cols-3 gap-2.5 text-center text-xs">
        <div className="p-3 rounded-xl border border-[#C8E3D7] dark:border-emerald-900 bg-[#F0F7F4] dark:bg-emerald-950/20">
          <CheckCircle2 className="w-4 h-4 mx-auto text-[#0B5D3B] dark:text-emerald-400 mb-1" />
          <span className="text-[#5B5B5B] dark:text-slate-400 block">{isBengali ? "সঠিক" : "Correct"}</span>
          <span className="text-base font-bold text-[#0B5D3B] dark:text-emerald-300 font-sans">
            {toBengaliNumber(correctCount)}
          </span>
        </div>

        <div className="p-3 rounded-xl border border-[#F8D2D2] dark:border-red-900 bg-[#FDF2F2] dark:bg-red-950/20">
          <XCircle className="w-4 h-4 mx-auto text-[#991B1B] dark:text-red-400 mb-1" />
          <span className="text-[#5B5B5B] dark:text-slate-400 block">{isBengali ? "ভুল" : "Incorrect"}</span>
          <span className="text-base font-bold text-[#991B1B] dark:text-red-300 font-sans">
            {toBengaliNumber(incorrectCount)}
          </span>
        </div>

        <div className="p-3 rounded-xl border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D]">
          <HelpCircle className="w-4 h-4 mx-auto text-[#5B5B5B] dark:text-slate-400 mb-1" />
          <span className="text-[#5B5B5B] dark:text-slate-400 block">{isBengali ? "উত্তরহীন" : "Skipped"}</span>
          <span className="text-base font-bold text-[#1A1A1A] dark:text-[#F5F2EB] font-sans">
            {toBengaliNumber(unattemptedCount)}
          </span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        {onReview && (
          <Button
            variant="default"
            size="md"
            fullWidth
            onClick={onReview}
            icon={<BookOpen className="w-4 h-4" />}
          >
            {isBengali ? "উত্তর ও বিস্তারিত সমাধান দেখুন" : "Review Answers"}
          </Button>
        )}

        {onRetry && (
          <Button
            variant="paper"
            size="md"
            fullWidth
            onClick={onRetry}
            icon={<RotateCcw className="w-4 h-4" />}
          >
            {isBengali ? "আবার চেষ্টা করুন" : "Retry Quiz"}
          </Button>
        )}
      </div>
    </div>
  );
};
