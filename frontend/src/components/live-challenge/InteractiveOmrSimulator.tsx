/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/InteractiveOmrSimulator.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Interactive digital OMR bubble sheet simulator directly on the page,
 *            giving students hands-on board exam tactile bubble filling experience.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Sparkles,
  Award,
  HelpCircle,
  FileCheck2
} from 'lucide-react';

interface OMRQuestion {
  id: number;
  stemBn: string;
  options: { label: string; textBn: string }[];
  correctOption: string;
}

const SAMPLE_QUESTIONS: OMRQuestion[] = [
  {
    id: 1,
    stemBn: '১. বল ও ত্বরণের সম্পর্ক নির্দেশকারী সমীকরণ কোনটি?',
    options: [
      { label: 'A', textBn: 'F = mv' },
      { label: 'B', textBn: 'F = ma' },
      { label: 'C', textBn: 'F = m/a' },
      { label: 'D', textBn: 'F = a/m' }
    ],
    correctOption: 'B'
  },
  {
    id: 2,
    stemBn: '২. কার্নো ইঞ্জিনের কর্মদক্ষতার সমীকরণ নির্দেশ করুন:',
    options: [
      { label: 'A', textBn: 'η = 1 - T2/T1' },
      { label: 'B', textBn: 'η = 1 + T2/T1' },
      { label: 'C', textBn: 'η = T1/T2' },
      { label: 'D', textBn: 'η = 1 - T1/T2' }
    ],
    correctOption: 'A'
  },
  {
    id: 3,
    stemBn: '৩. কাজ-শক্তি উপপাদ্য অনুযায়ী কৃতকাজ কিসের পরিবর্তনের সমান?',
    options: [
      { label: 'A', textBn: 'বিভব শক্তি' },
      { label: 'B', textBn: 'গতিশক্তি' },
      { label: 'C', textBn: 'ভরবেগ' },
      { label: 'D', textBn: 'ক্ষমতা' }
    ],
    correctOption: 'B'
  },
  {
    id: 4,
    stemBn: '৪. পর্যায় সারণির ৩য় পর্যায়ের ক্ষার ধাতু কোনটি?',
    options: [
      { label: 'A', textBn: 'লিথিয়াম (Li)' },
      { label: 'B', textBn: 'সোডিয়াম (Na)' },
      { label: 'C', textBn: 'পটাসিয়াম (K)' },
      { label: 'D', textBn: 'ম্যাগনেসিয়াম (Mg)' }
    ],
    correctOption: 'B'
  },
  {
    id: 5,
    stemBn: '৫. ভর-শক্তি সমতাকরণ সূত্র E = mc² এর প্রবক্তা কে?',
    options: [
      { label: 'A', textBn: 'আইজ্যাক নিউটন' },
      { label: 'B', textBn: 'ম্যাক্স প্ল্যাঙ্ক' },
      { label: 'C', textBn: 'আলবার্ট আইনস্টাইন' },
      { label: 'D', textBn: 'নীলস বোর' }
    ],
    correctOption: 'C'
  }
];

export const InteractiveOmrSimulator: React.FC = () => {
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [isEvaluated, setIsEvaluated] = useState<boolean>(false);

  const handleSelectBubble = (questionId: number, optionLabel: string) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: prev[questionId] === optionLabel ? '' : optionLabel
    }));
    setIsEvaluated(false);
  };

  const handleReset = () => {
    setSelectedAnswers({});
    setIsEvaluated(false);
  };

  const calculateScore = () => {
    let correct = 0;
    let wrong = 0;
    SAMPLE_QUESTIONS.forEach((q) => {
      const selected = selectedAnswers[q.id];
      if (selected) {
        if (selected === q.correctOption) {
          correct += 1;
        } else {
          wrong += 1;
        }
      }
    });

    const netScore = +(correct * 1.0 - wrong * 0.25).toFixed(2);
    return { correct, wrong, netScore };
  };

  const scoreResult = calculateScore();

  return (
    <div
      id="omr-simulator"
      aria-label="ইন্টারঅ্যাক্টিভ ডিজিটাল ওএমআর শিট সিমুলেটর"
      className="p-6 sm:p-8 rounded-3xl bg-white/95 dark:bg-[#0E1B33]/90 backdrop-blur-md border border-indigo-500/25 shadow-xl space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-indigo-200/50 dark:border-indigo-900/40">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold font-mono text-indigo-600 dark:text-indigo-300 uppercase tracking-wider">
            <CheckCircle2 className="w-4 h-4 text-indigo-500 dark:text-indigo-400" />
            <span>লাইভ এমসিকিউ ওএমআর ইঞ্জিন • রিয়েল-টাইম সিমুলেটর</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-black font-bengali text-slate-900 dark:text-white mt-1">
            ডিজিটাল ওএমআর শিট মোড (Interactive OMR Sheet)
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali mt-1">
            বোর্ড ও ভর্তি পরীক্ষার আসল ওএমআর বৃত্ত ভরার অভিজ্ঞতা নিন। প্রতিটি সঠিক উত্তরে +১.০ এবং ভুল উত্তরে -০.২৫ নেগেটিভ মার্কিং হিসাব হবে।
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-[#16274A] hover:bg-slate-200 dark:hover:bg-[#1E3463] text-slate-700 dark:text-slate-200 font-bold font-bengali text-xs flex items-center gap-1.5 transition min-h-[40px] border border-indigo-500/20"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>রিসেট শিট</span>
          </button>
          
          <button
            type="button"
            onClick={() => setIsEvaluated(true)}
            className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold font-bengali text-xs flex items-center gap-1.5 transition min-h-[40px] shadow-sm"
          >
            <FileCheck2 className="w-3.5 h-3.5" />
            <span>ওএমআর মূল্যায়ন করুন</span>
          </button>
        </div>
      </div>

      {/* OMR Questions & Bubble Rows */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Question Stems and Bubbles (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {SAMPLE_QUESTIONS.map((q) => {
            const userChoice = selectedAnswers[q.id];
            const isCorrect = userChoice === q.correctOption;
            const isWrong = userChoice && !isCorrect;

            return (
              <div
                key={q.id}
                className={`p-4 rounded-2xl border transition-all ${
                  isEvaluated
                    ? isCorrect
                      ? 'bg-emerald-50/60 dark:bg-emerald-950/30 border-emerald-400 dark:border-emerald-700'
                      : isWrong
                      ? 'bg-rose-50/60 dark:bg-rose-950/30 border-rose-400 dark:border-rose-700'
                      : 'bg-slate-50 dark:bg-[#071326]/80 border-slate-200 dark:border-indigo-500/20'
                    : 'bg-slate-50 dark:bg-[#071326]/80 border-slate-200 dark:border-indigo-500/20'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  {/* Stem and Options Preview */}
                  <div className="space-y-1.5 flex-1">
                    <h4 className="text-xs sm:text-sm font-bold font-bengali text-slate-900 dark:text-white">
                      {q.stemBn}
                    </h4>
                    <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs font-bengali text-slate-600 dark:text-slate-300">
                      {q.options.map((opt) => (
                        <span key={opt.label}>
                          <span className="font-mono font-bold text-slate-800 dark:text-slate-200">{opt.label})</span> {opt.textBn}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* OMR Bubbles: A, B, C, D */}
                  <div className="flex items-center gap-2 self-start sm:self-center shrink-0">
                    <span className="text-[11px] font-mono text-slate-400 mr-1">ওএমআর:</span>
                    {q.options.map((opt) => {
                      const isSelected = userChoice === opt.label;
                      const isOptionCorrect = isEvaluated && opt.label === q.correctOption;

                      return (
                        <button
                          key={opt.label}
                          type="button"
                          onClick={() => handleSelectBubble(q.id, opt.label)}
                          aria-label={`প্রশ্ন ${q.id} অপশন ${opt.label} নির্বাচন করুন`}
                          className={`w-9 h-9 rounded-full font-mono text-xs font-bold transition-all flex items-center justify-center border-2 ${
                            isSelected
                              ? 'bg-indigo-600 dark:bg-amber-400 text-white dark:text-[#0A2540] border-indigo-600 dark:border-amber-400 shadow-inner scale-95 ring-2 ring-offset-1 ring-indigo-500/30'
                              : isOptionCorrect
                              ? 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200 border-emerald-500'
                              : 'bg-white dark:bg-[#122244] text-slate-700 dark:text-slate-200 border-slate-300 dark:border-indigo-400/40 hover:border-indigo-400 dark:hover:border-amber-400'
                          }`}
                        >
                          {opt.label}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Evaluation Status Banner */}
                {isEvaluated && (
                  <div className="mt-2 pt-2 border-t border-slate-200/60 dark:border-indigo-500/20 flex items-center justify-between text-xs font-bengali">
                    {isCorrect ? (
                      <span className="text-emerald-700 dark:text-emerald-400 font-bold flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>সঠিক উত্তর! (+১.০ নম্বর)</span>
                      </span>
                    ) : isWrong ? (
                      <span className="text-rose-700 dark:text-rose-400 font-bold flex items-center gap-1">
                        <AlertTriangle className="w-3.5 h-3.5" />
                        <span>ভুল উত্তর! (-০.২৫ নেগেটিভ কর্তন) • সঠিক উত্তর: {q.correctOption}</span>
                      </span>
                    ) : (
                      <span className="text-slate-500 font-mono">
                        অনুত্তরিত (০.০ নম্বর) • সঠিক উত্তর: {q.correctOption}
                      </span>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Evaluation Summary & OMR Stats (4 cols) */}
        <div className="lg:col-span-4 p-6 rounded-2xl bg-slate-50 dark:bg-[#0A162C]/90 border border-indigo-500/25 space-y-5">
          <div className="flex items-center gap-2 pb-3 border-b border-indigo-200/50 dark:border-indigo-900/40">
            <Award className="w-4 h-4 text-amber-500 dark:text-amber-300" />
            <h3 className="text-sm font-bold font-bengali text-slate-900 dark:text-white">
              ওএমআর মূল্যায়ন পরিসংখ্যান
            </h3>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between p-2.5 rounded-xl bg-white dark:bg-[#10203D] border border-indigo-500/20">
              <span className="text-xs font-bengali text-slate-600 dark:text-slate-300">সঠিক পূরণ</span>
              <span className="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">
                {scoreResult.correct} টি (+{scoreResult.correct}.০)
              </span>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-white dark:bg-[#10203D] border border-indigo-500/20">
              <span className="text-xs font-bengali text-slate-600 dark:text-slate-300">ভুল পূরণ (পেনাল্টি)</span>
              <span className="text-xs font-mono font-bold text-rose-600 dark:text-rose-400">
                {scoreResult.wrong} টি (-{(scoreResult.wrong * 0.25).toFixed(2)})
              </span>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-white dark:bg-[#10203D] border border-indigo-500/20">
              <span className="text-xs font-bengali text-slate-600 dark:text-slate-300">অংশগ্রহণহীন</span>
              <span className="text-xs font-mono font-bold text-slate-500">
                {SAMPLE_QUESTIONS.length - (scoreResult.correct + scoreResult.wrong)} টি
              </span>
            </div>

            <div className="pt-2 border-t border-indigo-200/50 dark:border-indigo-900/40 flex items-center justify-between">
              <span className="text-xs font-bold font-bengali text-slate-900 dark:text-white">নেট প্রাপ্ত নম্বর</span>
              <span className="text-lg font-mono font-black text-indigo-600 dark:text-amber-300">
                {scoreResult.netScore} / {SAMPLE_QUESTIONS.length}.০
              </span>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-amber-500/10 dark:bg-amber-950/30 border border-amber-500/30 text-[11px] font-bengali text-amber-900 dark:text-amber-200 leading-relaxed">
            <span className="font-bold">টিপস:</span> লাইভ পরীক্ষায় পেজ পরিবর্তন করলে বা ওএমআর সময় শেষ হলে স্বয়ংক্রিয়ভাবে আপনার ভরানো বৃত্তগুলোই সার্ভারে সাবমিট হবে।
          </div>
        </div>

      </div>
    </div>
  );
};
