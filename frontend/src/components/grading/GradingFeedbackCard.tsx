/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Handwritten Script Feedback & Rubric Grading
 * TOPIC:     Affectionate Senior Teacher Script Feedback Card with Step Badges & KaTeX
 * FILE:      frontend/src/components/grading/GradingFeedbackCard.tsx
 * PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
 * PURPOSE:   Renders step-by-step exam markings with experienced educator warmth.
 *            Replaces harsh AI automated rejections with constructive margin notes,
 *            partial credit point badges, and mathematical KaTeX formula corrections.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React from 'react';
import {
  Award,
  CheckCircle2,
  AlertCircle,
  GraduationCap,
  Sparkles,
  Heart,
  CornerDownRight,
  BookOpen,
  ArrowRight
} from 'lucide-react';
import { KaTeXRenderer } from '../quiz/katex-renderer';

export interface GradingStepItem {
  step_number: number;
  title: string;
  score: number;
  max_score: number;
  teacher_note: string;
  expected_latex?: string;
  student_latex?: string;
}

export interface GradingFeedbackCardProps {
  questionTitle?: string;
  totalScore: number;
  maxScore: number;
  percentage?: number;
  steps: GradingStepItem[];
  teacherSummary: string;
  teacherName?: string;
  evaluatedAt?: string;
  onRetryDrill?: () => void;
  className?: string;
}

export const GradingFeedbackCard: React.FC<GradingFeedbackCardProps> = ({
  questionTitle = 'প্রক্ষেপকের সর্বাধিক উচ্চতা নির্ণয়',
  totalScore = 3.0,
  maxScore = 4.0,
  percentage = 75.0,
  steps,
  teacherSummary,
  teacherName = 'ড. আহমেদ রফিক (সিনিয়র পদার্থবিজ্ঞান শিক্ষক)',
  evaluatedAt = 'আজ, বিকাল ৫:১০',
  onRetryDrill,
  className = ''
}) => {
  const defaultSteps: GradingStepItem[] = [
    {
      step_number: 1,
      title: 'সূত্র প্রয়োগ (Formula Selection)',
      score: 1.0,
      max_score: 1.0,
      teacher_note: 'চমৎকার! মূল বৈজ্ঞানিক সূত্রটি নির্ভুলভাবে নির্বাচন করেছ।',
      expected_latex: 'H = \\frac{u^2 \\sin^2\\theta}{2g}'
    },
    {
      step_number: 2,
      title: 'মান প্রতিস্থাপন (Value Substitution)',
      score: 1.0,
      max_score: 1.0,
      teacher_note: 'প্রদত্ত রাশিগুলোর মান প্রতিস্থাপন যথাযথ হয়েছে।',
      expected_latex: 'H = \\frac{40^2 \\times \\sin^2(30^\\circ)}{2 \\times 9.8}'
    },
    {
      step_number: 3,
      title: 'গাণিতিক বিশ্লেষণ (Calculation)',
      score: 0.5,
      max_score: 1.0,
      teacher_note: 'সূত্র ও মান বসানো নিখুঁত ছিল, তবে ১৬০০ × ০.২৫ = ৪০০ এর পরবর্তী ভাগে সামান্য হিসাবের বিচ্যুতি ঘটেছে। ভগ্নাংশ কাটাকাটি আরেকবার দেখে নিও।',
      expected_latex: 'H = \\frac{1600 \\times 0.25}{19.6} = \\frac{400}{19.6} \\approx 20.41'
    },
    {
      step_number: 4,
      title: 'চূড়ান্ত ফলাফল ও একক (Final Answer & Unit)',
      score: 0.5,
      max_score: 1.0,
      teacher_note: 'একক উল্লেখ ঠিক আছে (মিটার), কিন্তু আগের ধাপের হিসাবের কারণে সংখ্যায় কিছুটা অমিল হয়েছে।',
      expected_latex: 'H \\approx 20.41\\text{ m}'
    }
  ];

  const activeSteps = steps && steps.length > 0 ? steps : defaultSteps;

  return (
    <div
      className={`relative flex flex-col p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800/80 shadow-2xl space-y-6 font-bengali leading-relaxed select-none ${className}`}
    >
      {/* Top Banner: Teacher's Mark Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 dark:bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
            <GraduationCap className="w-6 h-6" strokeWidth={1.75} />
          </div>
          <div>
            <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white font-display">
              {questionTitle}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-2 mt-0.5">
              <span>{teacherName}</span>
              <span>•</span>
              <span>{evaluatedAt}</span>
            </p>
          </div>
        </div>

        {/* Tactile Score Badge with Teacher Pen Aesthetic */}
        <div className="flex items-center gap-3 self-start sm:self-auto">
          <div className="p-3 rounded-2xl bg-amber-500/10 dark:bg-amber-500/20 border border-amber-500/30 text-right">
            <span className="text-[11px] font-semibold text-amber-700 dark:text-amber-300 block uppercase tracking-wider">
              অর্জিত নম্বর
            </span>
            <div className="flex items-baseline justify-end gap-1 font-numeric">
              <span className="text-2xl sm:text-3xl font-extrabold text-amber-600 dark:text-amber-400">
                {totalScore}
              </span>
              <span className="text-sm font-bold text-slate-400">/ {maxScore}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Affectionate Teacher Handwritten Summary Note (Ruled Notepad Margin Aesthetic) */}
      <div className="relative p-5 rounded-2xl bg-[#FAF8F3] dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#24314A] space-y-2">
        <div className="flex items-center gap-2 text-xs font-bold text-blue-700 dark:text-blue-300">
          <Heart className="w-4 h-4 text-rose-500 fill-rose-500/20" strokeWidth={1.75} />
          <span>শিক্ষকের স্নেহাশিস ও মূল মন্তব্য:</span>
        </div>
        <p className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed italic pl-6">
          "{teacherSummary || 'বেশ ভালো চেষ্টা করেছ! সূত্র ও মান বসানো চমৎকার হয়েছে, তবে শেষের দিকে গণনায় সামান্য মনোযোগ দিলেই পূর্ণ ৪/৪ নম্বর অর্জন সম্ভব।'}"
        </p>
      </div>

      {/* Step-by-Step Point Rubric Breakdown */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider px-1">
          <span>ধাপভিত্তিক মার্কিং বিভাজন (Step Rubric)</span>
          <span>নম্বর</span>
        </div>

        {activeSteps.map((step) => {
          const isFullCredit = step.score >= step.max_score;
          const isPartialCredit = step.score > 0 && step.score < step.max_score;

          return (
            <div
              key={step.step_number}
              className={`p-4 rounded-2xl border transition-all ${
                isFullCredit
                  ? 'bg-slate-50/80 dark:bg-slate-800/40 border-slate-200/80 dark:border-slate-700/80'
                  : isPartialCredit
                  ? 'bg-amber-50/40 dark:bg-amber-950/20 border-amber-200/80 dark:border-amber-800/60'
                  : 'bg-rose-50/30 dark:bg-rose-950/20 border-rose-200 dark:border-rose-900/60'
              }`}
            >
              {/* Step Header with Score Badge */}
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-numeric shrink-0 ${
                      isFullCredit
                        ? 'bg-emerald-500 text-white'
                        : isPartialCredit
                        ? 'bg-amber-500 text-white'
                        : 'bg-rose-500 text-white'
                    }`}
                  >
                    {step.step_number}
                  </div>
                  <h4 className="text-sm font-bold text-slate-900 dark:text-white">
                    {step.title}
                  </h4>
                </div>

                {/* Score Chip */}
                <div
                  className={`px-2.5 py-0.5 rounded-full text-xs font-bold font-numeric ${
                    isFullCredit
                      ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                      : isPartialCredit
                      ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                      : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
                  }`}
                >
                  {step.score} / {step.max_score}
                </div>
              </div>

              {/* Teacher's gentle margin guidance note */}
              <div className="mt-2.5 flex items-start gap-2 text-xs text-slate-700 dark:text-slate-300 pl-8">
                <CornerDownRight className="w-3.5 h-3.5 text-blue-500 shrink-0 mt-0.5" strokeWidth={1.75} />
                <p>{step.teacher_note}</p>
              </div>

              {/* KaTeX Mathematical Formula Correction */}
              {step.expected_latex && (
                <div className="mt-3 ml-8 p-3 rounded-xl bg-white/90 dark:bg-slate-900/90 border border-slate-200/80 dark:border-slate-800 text-xs text-slate-900 dark:text-white shadow-sm flex items-center justify-between overflow-x-auto">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider shrink-0">
                      সঠিক সমীকরণ:
                    </span>
                    <KaTeXRenderer content={`$${step.expected_latex}$`} />
                  </div>
                  {isFullCredit && (
                    <div className="flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold shrink-0">
                      <CheckCircle2 className="w-3.5 h-3.5" strokeWidth={2} />
                      <span>নির্ভুল</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Footer Action */}
      <div className="pt-2 flex items-center justify-between border-t border-slate-100 dark:border-slate-800">
        <span className="text-xs text-slate-500 dark:text-slate-400">
          বোর্ড পরীক্ষার উত্তরপত্র মূল্যায়ন বিধিমালার সাথে ১০০% সংগতিপূর্ণ
        </span>
        {onRetryDrill && (
          <button
            type="button"
            onClick={onRetryDrill}
            className="btn-push-brand px-5 py-2 text-xs font-bold text-white bg-blue-600 rounded-xl flex items-center gap-1.5 shadow-md active:scale-95"
          >
            <span>সংশোধিত উত্তর পুনরায় জমা দিন</span>
            <ArrowRight className="w-3.5 h-3.5" strokeWidth={1.75} />
          </button>
        )}
      </div>
    </div>
  );
};
