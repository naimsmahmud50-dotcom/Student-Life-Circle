/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/SubjectWeightageBreakdown.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Subject weightage distribution bar and marking formula matrix,
 *            giving students precise transparency on chapter weightage and cut-off points.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React from 'react';
import {
  BarChart3,
  Target,
  FileCheck2,
  AlertTriangle,
  Award,
  BookOpen,
  HelpCircle
} from 'lucide-react';

export interface ChapterWeightage {
  chapterBn: string;
  questionCount: number;
  percentage: number;
  colorClass: string;
}

const DEFAULT_CHAPTERS: ChapterWeightage[] = [
  { chapterBn: 'নিউটোনীয় বলবিদ্যা', questionCount: 7, percentage: 28, colorClass: 'bg-[#0A2540] text-white' },
  { chapterBn: 'কাজ, শক্তি ও ক্ষমতা', questionCount: 6, percentage: 24, colorClass: 'bg-slate-700 text-white' },
  { chapterBn: 'পদার্থের গাঠনিক ধর্ম', questionCount: 7, percentage: 28, colorClass: 'bg-amber-800 text-white' },
  { chapterBn: 'পর্যাবৃত্ত গতি ও তরঙ্গ', questionCount: 5, percentage: 20, colorClass: 'bg-emerald-800 text-white' },
];

export const SubjectWeightageBreakdown: React.FC = () => {
  return (
    <section
      aria-label="বিষয়ভিত্তিক প্রশ্ন বণ্টন ও মূল্যায়ন সূত্রাবলী"
      className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-sm space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold font-mono text-[#0A2540] dark:text-amber-300 uppercase tracking-wider">
            <BarChart3 className="w-4 h-4" />
            <span>সিলেবাস ওয়েইটেজ ও মার্কিং ম্যাট্রিক্স</span>
          </div>
          <h2 className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white mt-1">
            লাইভ পরীক্ষার প্রশ্ন বণ্টন ও কাট-মার্ক পূর্বাভাস
          </h2>
        </div>
        <span className="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-mono font-bold self-start sm:self-auto">
          মোট পূর্ণমান: ২৫ নম্বর
        </span>
      </div>

      {/* Visual Proportional Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs font-bengali text-slate-600 dark:text-slate-400">
          <span>অধ্যায়ভিত্তিক প্রশ্ন অনুপাত</span>
          <span>১০০% কভারেজ (২৫টি প্রশ্ন)</span>
        </div>

        <div className="h-4 w-full rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden flex">
          {DEFAULT_CHAPTERS.map((ch, idx) => (
            <div
              key={idx}
              style={{ width: `${ch.percentage}%` }}
              className={`${ch.colorClass} h-full transition-all`}
              title={`${ch.chapterBn}: ${ch.percentage}% (${ch.questionCount}টি প্রশ্ন)`}
            />
          ))}
        </div>

        {/* Legend */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          {DEFAULT_CHAPTERS.map((ch, idx) => (
            <div key={idx} className="p-2.5 rounded-xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-1.5 mb-1">
                <span className={`w-2.5 h-2.5 rounded-full ${ch.colorClass.split(' ')[0]}`} />
                <span className="text-xs font-bold font-bengali text-slate-800 dark:text-slate-200 truncate">
                  {ch.chapterBn}
                </span>
              </div>
              <div className="text-[11px] font-mono text-slate-500">
                {ch.questionCount} প্রশ্ন • {ch.percentage}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Marking Evaluation Formulas (4 Cards) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
        <div className="p-4 rounded-2xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/40">
          <div className="flex items-center gap-2 text-emerald-800 dark:text-emerald-300 text-xs font-bold font-bengali mb-1">
            <FileCheck2 className="w-4 h-4" />
            <span>সঠিক উত্তর</span>
          </div>
          <div className="text-xl font-black font-mono text-emerald-700 dark:text-emerald-400">
            +১.০ <span className="text-xs font-bengali font-normal">নম্বর</span>
          </div>
          <p className="text-[11px] text-emerald-700/80 dark:text-emerald-400/80 font-bengali mt-1">
            প্রতিটি নির্ভুল উত্তরের জন্য পূর্ণ ১ নম্বর যুক্ত হবে।
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-[#991B1B]/5 dark:bg-[#991B1B]/20 border border-[#991B1B]/20 dark:border-[#991B1B]/40">
          <div className="flex items-center gap-2 text-[#991B1B] dark:text-rose-300 text-xs font-bold font-bengali mb-1">
            <AlertTriangle className="w-4 h-4" />
            <span>নেগেটিভ মার্কিং</span>
          </div>
          <div className="text-xl font-black font-mono text-[#991B1B] dark:text-rose-300">
            -০.২৫ <span className="text-xs font-bengali font-normal">কর্তন</span>
          </div>
          <p className="text-[11px] text-[#991B1B]/80 dark:text-rose-300/80 font-bengali mt-1">
            ভুল উত্তরের জন্য ২৫% নম্বর কাটা যাবে।
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40">
          <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300 text-xs font-bold font-bengali mb-1">
            <Target className="w-4 h-4" />
            <span>পাস মার্ক থ্রেশহোল্ড</span>
          </div>
          <div className="text-xl font-black font-mono text-amber-800 dark:text-amber-300">
            ১০.০ <span className="text-xs font-bengali font-normal">(৪০%)</span>
          </div>
          <p className="text-[11px] text-amber-700/80 dark:text-amber-400/80 font-bengali mt-1">
            কোয়ালিফাই করার ন্যূনতম মানদণ্ড।
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-2 text-[#0A2540] dark:text-amber-300 text-xs font-bold font-bengali mb-1">
            <Award className="w-4 h-4" />
            <span>প্রত্যাশিত কাট-মার্ক</span>
          </div>
          <div className="text-xl font-black font-mono text-[#0A2540] dark:text-amber-300">
            ১৮.৫+ <span className="text-xs font-bengali font-normal">নম্বর</span>
          </div>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 font-bengali mt-1">
            শীর্ষ ৫% জাতীয় মেধা তালিকার কাট-অফ পয়েন্ট।
          </p>
        </div>
      </div>
    </section>
  );
};
