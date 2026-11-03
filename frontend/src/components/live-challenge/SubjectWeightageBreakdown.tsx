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
import { useTranslation } from '@/lib/i18n';

export interface ChapterWeightage {
  chapterBn: string;
  chapterEn: string;
  questionCount: number;
  percentage: number;
  colorClass: string;
}

const DEFAULT_CHAPTERS: ChapterWeightage[] = [
  { chapterBn: 'নিউটোনীয় বলবিদ্যা', chapterEn: 'Newtonian Mechanics', questionCount: 7, percentage: 28, colorClass: 'bg-[#0A2540] text-white' },
  { chapterBn: 'কাজ, শক্তি ও ক্ষমতা', chapterEn: 'Work, Power & Energy', questionCount: 6, percentage: 24, colorClass: 'bg-slate-700 text-white' },
  { chapterBn: 'পদার্থের গাঠনিক ধর্ম', chapterEn: 'Structural Properties of Matter', questionCount: 7, percentage: 28, colorClass: 'bg-amber-800 text-white' },
  { chapterBn: 'পর্যাবৃত্ত গতি ও তরঙ্গ', chapterEn: 'Periodic Motion & Waves', questionCount: 5, percentage: 20, colorClass: 'bg-emerald-800 text-white' },
];

export const SubjectWeightageBreakdown: React.FC = () => {
  const { isBengali } = useTranslation();

  return (
    <div
      aria-label={isBengali ? "বিষয়ভিত্তিক প্রশ্ন বণ্টন ও মূল্যায়ন সূত্রাবলী" : "Subject-wise Question Distribution & Marking Matrix"}
      className="p-6 sm:p-8 rounded-3xl bg-white/95 dark:bg-[#160E30]/90 backdrop-blur-md border border-purple-500/25 shadow-xl space-y-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-purple-200/50 dark:border-purple-900/40">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold font-mono text-purple-600 dark:text-purple-300 uppercase tracking-wider">
            <BarChart3 className="w-4 h-4 text-purple-500 dark:text-purple-400" />
            <span>{isBengali ? 'সিলেবাস ওয়েইটেজ ও মার্কিং ম্যাট্রিক্স' : 'Syllabus Weightage & Marking Matrix'}</span>
          </div>
          <h2 className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white mt-1">
            {isBengali ? 'লাইভ পরীক্ষার প্রশ্ন বণ্টন ও কাট-মার্ক পূর্বাভাস' : 'Question Distribution & Cut-off Score Forecast'}
          </h2>
        </div>
        <span className="px-3 py-1 rounded-full bg-purple-500/10 dark:bg-purple-500/20 text-purple-700 dark:text-purple-300 border border-purple-500/30 text-xs font-mono font-bold self-start sm:self-auto">
          {isBengali ? 'মোট পূর্ণমান: ২৫ নম্বর' : 'Total Marks: 25'}
        </span>
      </div>

      {/* Visual Proportional Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs font-bengali text-slate-600 dark:text-slate-300">
          <span>{isBengali ? 'অধ্যায়ভিত্তিক প্রশ্ন অনুপাত' : 'Chapter-wise Question Ratio'}</span>
          <span className="text-purple-600 dark:text-purple-300 font-mono">
            {isBengali ? '১০০% কভারেজ (২৫টি প্রশ্ন)' : '100% Coverage (25 Questions)'}
          </span>
        </div>

        <div className="h-4 w-full rounded-full bg-slate-100 dark:bg-slate-800/80 overflow-hidden flex border border-purple-500/20">
          {DEFAULT_CHAPTERS.map((ch, idx) => (
            <div
              key={idx}
              style={{ width: `${ch.percentage}%` }}
              className={`${ch.colorClass} h-full transition-all`}
              title={`${isBengali ? ch.chapterBn : ch.chapterEn}: ${ch.percentage}% (${ch.questionCount} ${isBengali ? 'টি প্রশ্ন' : 'Questions'})`}
            />
          ))}
        </div>

        {/* Legend */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          {DEFAULT_CHAPTERS.map((ch, idx) => (
            <div key={idx} className="p-2.5 rounded-xl bg-slate-50 dark:bg-[#1C123B]/80 border border-purple-500/20">
              <div className="flex items-center gap-1.5 mb-1">
                <span className={`w-2.5 h-2.5 rounded-full ${ch.colorClass.split(' ')[0]}`} />
                <span className="text-xs font-bold font-bengali text-slate-800 dark:text-slate-200 truncate">
                  {isBengali ? ch.chapterBn : ch.chapterEn}
                </span>
              </div>
              <div className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
                {isBengali ? `${ch.questionCount} প্রশ্ন • ${ch.percentage}%` : `${ch.questionCount} Qs • ${ch.percentage}%`}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Marking Evaluation Formulas (4 Cards) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
        <div className="p-4 rounded-2xl bg-emerald-50/60 dark:bg-emerald-950/30 border border-emerald-500/30">
          <div className="flex items-center gap-2 text-emerald-800 dark:text-emerald-300 text-xs font-bold font-bengali mb-1">
            <FileCheck2 className="w-4 h-4" />
            <span>{isBengali ? 'সঠিক উত্তর' : 'Correct Answer'}</span>
          </div>
          <div className="text-xl font-black font-mono text-emerald-700 dark:text-emerald-400">
            +১.০ <span className="text-xs font-bengali font-normal">{isBengali ? 'নম্বর' : 'Marks'}</span>
          </div>
          <p className="text-[11px] text-emerald-700/80 dark:text-emerald-400/80 font-bengali mt-1">
            {isBengali ? 'প্রতিটি নির্ভুল উত্তরের জন্য পূর্ণ ১ নম্বর যুক্ত হবে।' : '1.0 full mark is awarded for each correct answer.'}
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-rose-50/60 dark:bg-rose-950/30 border border-rose-500/30">
          <div className="flex items-center gap-2 text-rose-800 dark:text-rose-300 text-xs font-bold font-bengali mb-1">
            <AlertTriangle className="w-4 h-4" />
            <span>{isBengali ? 'নেগেটিভ মার্কিং' : 'Negative Marking'}</span>
          </div>
          <div className="text-xl font-black font-mono text-rose-700 dark:text-rose-300">
            -০.২৫ <span className="text-xs font-bengali font-normal">{isBengali ? 'কর্তন' : 'Deduction'}</span>
          </div>
          <p className="text-[11px] text-rose-700/80 dark:text-rose-300/80 font-bengali mt-1">
            {isBengali ? 'ভুল উত্তরের জন্য ২৫% নম্বর কাটা যাবে।' : '25% deduction applies for each incorrect response.'}
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-amber-50/60 dark:bg-amber-950/30 border border-amber-500/30">
          <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300 text-xs font-bold font-bengali mb-1">
            <Target className="w-4 h-4" />
            <span>{isBengali ? 'পাস মার্ক থ্রেশহোল্ড' : 'Pass Threshold'}</span>
          </div>
          <div className="text-xl font-black font-mono text-amber-800 dark:text-amber-300">
            ১০.০ <span className="text-xs font-bengali font-normal">(৪০%)</span>
          </div>
          <p className="text-[11px] text-amber-700/80 dark:text-amber-400/80 font-bengali mt-1">
            {isBengali ? 'কোয়ালিফাই করার ন্যূনতম মানদণ্ড।' : 'Minimum threshold required to qualify.'}
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-purple-50/60 dark:bg-[#1F1442]/80 border border-purple-500/30">
          <div className="flex items-center gap-2 text-purple-700 dark:text-purple-300 text-xs font-bold font-bengali mb-1">
            <Award className="w-4 h-4" />
            <span>{isBengali ? 'প্রত্যাশিত কাট-মার্ক' : 'Projected Cut-off'}</span>
          </div>
          <div className="text-xl font-black font-mono text-purple-700 dark:text-purple-300">
            ১৮.৫+ <span className="text-xs font-bengali font-normal">{isBengali ? 'নম্বর' : 'Marks'}</span>
          </div>
          <p className="text-[11px] text-purple-700/80 dark:text-purple-300/80 font-bengali mt-1">
            {isBengali ? 'শীর্ষ ৫% জাতীয় মেধা তালিকার কাট-অফ পয়েন্ট।' : 'Projected cut-off for the top 5% national merit tier.'}
          </p>
        </div>
      </div>
    </div>
  );
};
