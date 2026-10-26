/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    SyllabusCoverageBar Component
 * TOPIC:     Academic Syllabus Progress & Subject-Wise Readiness Indicators
 * FILE:      frontend/src/modules/exam-routine/components/SyllabusCoverageBar.tsx
 * PURPOSE:   Visualizes 200-day preparation syllabus coverage across key competitive
 *            subjects, flagging high-yield revision recommendations.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji
 * ========================================================================================
 */

import React from 'react';
import { BookOpen, CheckCircle, TrendingUp, AlertCircle } from 'lucide-react';

export const SyllabusCoverageBar: React.FC = () => {
  const subjects = [
    { name: 'বাংলা ভাষা ও সাহিত্য', completed: 85, color: 'bg-emerald-500' },
    { name: 'English Language', completed: 72, color: 'bg-blue-500' },
    { name: 'গাণিতিক যুক্তি ও বিজ্ঞান', completed: 90, color: 'bg-indigo-500' },
    { name: 'বাংলাদেশ ও আন্তর্জাতিক বিষয়াবলী', completed: 68, color: 'bg-amber-500' },
  ];

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900 shadow-sm space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 dark:border-slate-800">
        <div className="flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
          <h3 className="text-sm font-serif font-bold text-slate-800 dark:text-slate-200">
            ২০০ দিনের সিলেবাস প্রস্তুতি ট্র্যাকার
          </h3>
        </div>

        <span className="text-xs text-slate-500 dark:text-slate-400">
          সার্বিক অগ্রগতি: <strong className="text-emerald-600 dark:text-emerald-400">৭৮.৮%</strong>
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {subjects.map((sub, idx) => (
          <div key={idx} className="space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium text-slate-700 dark:text-slate-300">{sub.name}</span>
              <span className="font-mono font-semibold text-slate-600 dark:text-slate-400">{sub.completed}%</span>
            </div>

            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
              <div
                className={`h-full rounded-full transition-all duration-500 ${sub.color}`}
                style={{ width: `${sub.completed}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="flex items-center gap-2 rounded-lg bg-emerald-50/60 p-3 text-xs text-emerald-800 dark:bg-emerald-950/20 dark:text-emerald-300">
        <TrendingUp className="h-4 w-4 shrink-0 text-emerald-600" />
        <span>
          পরামর্শ: আপনার গণিত ও বাংলায় দক্ষতা চমৎকার। আসন্ন মেগা মডেল টেস্টের আগে বাংলাদেশ ও আন্তর্জাতিক সাধারণ জ্ঞানে আরও নজর দিন।
        </span>
      </div>
    </div>
  );
};
