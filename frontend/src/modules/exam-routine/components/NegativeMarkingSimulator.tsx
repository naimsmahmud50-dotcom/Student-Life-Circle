/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    NegativeMarkingSimulator Component
 * TOPIC:     Interactive Negative Marking Deduction, Net Score & Merit Percentile Calculator
 * FILE:      frontend/src/modules/exam-routine/components/NegativeMarkingSimulator.tsx
 * PURPOSE:   Empowers candidates to calculate accurate net scores accounting for
 *            negative marking penalties (-0.25 / -0.50), providing predictive merit
 *            percentiles and weakness diagnostics.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji, Zero-CLS
 * ========================================================================================
 */

import React, { useState, useEffect } from 'react';
import { 
  X, 
  Calculator, 
  Award, 
  AlertTriangle, 
  TrendingUp, 
  CheckCircle2, 
  HelpCircle,
  Percent
} from 'lucide-react';
import { 
  NegativeMarkSimulationRequest, 
  NegativeMarkSimulationResponse 
} from '../types/examRoutine.types';

interface NegativeMarkingSimulatorProps {
  isOpen: boolean;
  onClose: () => void;
  onSimulate: (req: NegativeMarkSimulationRequest) => Promise<void>;
  simulationResult: NegativeMarkSimulationResponse | null;
  isSimulating: boolean;
}

export const NegativeMarkingSimulator: React.FC<NegativeMarkingSimulatorProps> = ({
  isOpen,
  onClose,
  onSimulate,
  simulationResult,
  isSimulating,
}) => {
  const [totalQuestions, setTotalQuestions] = useState<number>(100);
  const [correctAnswers, setCorrectAnswers] = useState<number>(75);
  const [wrongAnswers, setWrongAnswers] = useState<number>(15);
  const [negativeFactor, setNegativeFactor] = useState<number>(0.25);
  const [markPerQuestion, setMarkPerQuestion] = useState<number>(1.0);

  const unanswered = Math.max(0, totalQuestions - (correctAnswers + wrongAnswers));

  useEffect(() => {
    if (correctAnswers + wrongAnswers > totalQuestions) {
      setWrongAnswers(Math.max(0, totalQuestions - correctAnswers));
    }
  }, [totalQuestions, correctAnswers, wrongAnswers]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSimulate({
      total_questions: totalQuestions,
      correct_answers: correctAnswers,
      wrong_answers: wrongAnswers,
      unanswered,
      negative_factor: negativeFactor,
      mark_per_question: markPerQuestion,
    });
  };

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="simulator-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in duration-200"
    >
      <div 
        className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 shadow-2xl p-6 sm:p-8 space-y-6"
      >
        {/* Header */}
        <div className="flex items-start justify-between border-b border-slate-100 pb-4 dark:border-slate-800">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
              <Calculator className="h-4 w-4" />
              <span>অগ্রযাত্রা স্কোর ইঞ্জিন</span>
            </div>
            <h2 id="simulator-modal-title" className="text-xl font-serif font-bold text-slate-900 dark:text-slate-100">
              নেগেটিভ মার্কিং ও মেধা পারসেন্টাইল সিমুলেটর
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              ভুল উত্তরের পেনাল্টি হিসাব করে নেট স্কোর ও ঐতিহাসিক কাট-অফ পারসেন্টাইল যাচাই করুন।
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="মডাল বন্ধ করুন"
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-200 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Simulator Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Total Questions */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                মোট প্রশ্ন সংখ্যা
              </label>
              <select
                value={totalQuestions}
                onChange={(e) => setTotalQuestions(Number(e.target.value))}
                className="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 focus:ring-1 focus:ring-emerald-500"
              >
                <option value={50}>৫০টি (বিষয়ভিত্তিক দৈনিক টেস্ট)</option>
                <option value={100}>১০০টি (ভার্সিটি / বুয়েট প্রিলিমিনারি)</option>
                <option value={200}>২০০টি (বিসিএস পূর্ণাঙ্গ মডেল টেস্ট)</option>
              </select>
            </div>

            {/* Negative Factor */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                নেগেটিভ মার্কিং হার (প্রতি ভুল উত্তরে)
              </label>
              <select
                value={negativeFactor}
                onChange={(e) => setNegativeFactor(Number(e.target.value))}
                className="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 focus:ring-1 focus:ring-emerald-500"
              >
                <option value={0.25}>-০.২৫ (বিসিএস প্রিলিমিনারি ও সাধারণ ভার্সিটি)</option>
                <option value={0.50}>-০.৫০ (কঠোর মেগা মডেল টেস্ট ও মেডিকেল)</option>
                <option value={0.20}>-০.২০ (স্ট্যান্ডার্ড কোয়ালিফাইং টেস্ট)</option>
              </select>
            </div>

            {/* Correct Answers */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                সঠিক উত্তর সংখ্যা: <span className="text-emerald-600 font-bold">{correctAnswers}</span>
              </label>
              <input
                type="number"
                min={0}
                max={totalQuestions}
                value={correctAnswers}
                onChange={(e) => setCorrectAnswers(Math.min(totalQuestions, Number(e.target.value)))}
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            {/* Wrong Answers */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                ভুল উত্তর সংখ্যা: <span className="text-rose-600 font-bold">{wrongAnswers}</span>
              </label>
              <input
                type="number"
                min={0}
                max={totalQuestions - correctAnswers}
                value={wrongAnswers}
                onChange={(e) => setWrongAnswers(Math.min(totalQuestions - correctAnswers, Number(e.target.value)))}
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 focus:ring-1 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between rounded-lg bg-slate-50 p-3 text-xs text-slate-600 dark:bg-slate-800/60 dark:text-slate-300">
            <span>অনুত্তরিত প্রশ্ন: <strong className="text-slate-800 dark:text-slate-100">{unanswered}টি</strong></span>
            <span>মোট নম্বর: <strong>{totalQuestions * markPerQuestion}</strong></span>
          </div>

          <button
            type="submit"
            disabled={isSimulating}
            className="w-full rounded-lg bg-emerald-600 hover:bg-emerald-500 py-2.5 text-sm font-semibold text-white transition-colors disabled:opacity-50"
          >
            {isSimulating ? 'হিসাব করা হচ্ছে...' : 'স্কোর ও পারসেন্টাইল হিসাব করুন'}
          </button>
        </form>

        {/* Results Display */}
        {simulationResult && (
          <div className="rounded-xl border border-emerald-200 bg-emerald-50/50 p-5 dark:border-emerald-900/50 dark:bg-emerald-950/20 space-y-4 animate-in fade-in">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div className="rounded-lg bg-white p-3 border border-slate-200 dark:border-slate-800 dark:bg-slate-900">
                <span className="text-[10px] text-slate-500 uppercase font-semibold">গ্রস স্কোর</span>
                <p className="text-base font-bold text-slate-800 dark:text-slate-200">{simulationResult.gross_score}</p>
              </div>

              <div className="rounded-lg bg-white p-3 border border-slate-200 dark:border-slate-800 dark:bg-slate-900">
                <span className="text-[10px] text-rose-500 uppercase font-semibold">পেনাল্টি কর্তন</span>
                <p className="text-base font-bold text-rose-600">-{simulationResult.penalty_deducted}</p>
              </div>

              <div className="rounded-lg bg-emerald-600 p-3 text-white">
                <span className="text-[10px] uppercase font-semibold opacity-90">নেট প্রাপ্ত নম্বর</span>
                <p className="text-lg font-bold">{simulationResult.net_score}</p>
              </div>

              <div className="rounded-lg bg-white p-3 border border-slate-200 dark:border-slate-800 dark:bg-slate-900">
                <span className="text-[10px] text-emerald-600 uppercase font-semibold">সঠিকতা হার</span>
                <p className="text-base font-bold text-slate-800 dark:text-slate-200">{simulationResult.accuracy_percentage}%</p>
              </div>
            </div>

            {/* Estimated Percentile & Merit Bracket */}
            <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900 space-y-2">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 dark:text-slate-300">
                  <TrendingUp className="h-4 w-4 text-emerald-600" />
                  <span>আনুমানিক মেধা পারসেন্টাইল</span>
                </span>
                <span className="font-mono text-base font-bold text-emerald-600 dark:text-emerald-400">
                  {simulationResult.estimated_percentile}%
                </span>
              </div>

              <div className="text-xs text-slate-700 dark:text-slate-200 font-medium">
                অবস্থান ব্র্যাকেট: <span className="text-emerald-700 dark:text-emerald-300 font-bold">{simulationResult.merit_bracket}</span>
              </div>
            </div>

            {/* Strategic Weakness Flags */}
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                কৌশলগত নিরীক্ষা ও পরামর্শ:
              </span>
              <ul className="space-y-1 text-xs text-slate-600 dark:text-slate-400">
                {simulationResult.weakness_flags.map((flag, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-600 shrink-0 mt-0.5" />
                    <span>{flag}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
