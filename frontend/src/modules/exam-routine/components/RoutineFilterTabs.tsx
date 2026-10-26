/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    RoutineFilterTabs Component
 * TOPIC:     Academic Exam Track Filter, Subject Selector & Routine Search Bar
 * FILE:      frontend/src/modules/exam-routine/components/RoutineFilterTabs.tsx
 * PURPOSE:   Provides seamless switching between 200-day BCS routines, varsity admissions,
 *            HSC board preps, and subject tracks with live search query filtering.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji
 * ========================================================================================
 */

import React from 'react';
import { Search, Calendar, Filter } from 'lucide-react';
import { ExamType, TrackCategory } from '../types/examRoutine.types';

interface RoutineFilterTabsProps {
  selectedExamType: ExamType | 'ALL';
  onSelectExamType: (type: ExamType | 'ALL') => void;
  selectedTrack: TrackCategory | 'ALL';
  onSelectTrack: (track: TrackCategory | 'ALL') => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  activeDay: number;
  totalFiltered: number;
}

export const RoutineFilterTabs: React.FC<RoutineFilterTabsProps> = ({
  selectedExamType,
  onSelectExamType,
  selectedTrack,
  onSelectTrack,
  searchQuery,
  onSearchChange,
  activeDay,
  totalFiltered,
}) => {
  const examTabs: { id: ExamType | 'ALL'; label: string }[] = [
    { id: 'ALL', label: 'সব পরীক্ষা' },
    { id: 'BCS_PRELI', label: '৪৭তম বিসিএস (২০০ দিন)' },
    { id: 'ADMISSION_VARSITY', label: 'ভার্সিটি ও বুয়েট ভর্তি' },
    { id: 'HSC_BOARD', label: 'এইচএসসি ফাইনাল মডেল' },
  ];

  const trackTabs: { id: TrackCategory | 'ALL'; label: string }[] = [
    { id: 'ALL', label: 'সকল বিষয়' },
    { id: 'BANGLA', label: 'বাংলা ভাষা ও সাহিত্য' },
    { id: 'ENGLISH', label: 'English Language' },
    { id: 'MATH_SCIENCE', label: 'গণিত ও বিজ্ঞান' },
    { id: 'GK', label: 'বাংলাদেশ ও আন্তর্জাতিক' },
  ];

  return (
    <div className="space-y-4 rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      {/* Primary Exam Type Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4 dark:border-slate-800/80">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none" role="tablist">
          {examTabs.map((tab) => {
            const isActive = selectedExamType === tab.id;
            return (
              <button
                key={tab.id}
                role="tab"
                aria-selected={isActive}
                onClick={() => onSelectExamType(tab.id)}
                className={`whitespace-nowrap rounded-lg px-3.5 py-2 text-xs sm:text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-slate-900 text-white shadow-sm dark:bg-emerald-600 dark:text-white'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Current Active Day Badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 shrink-0 self-start sm:self-auto">
          <Calendar className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
          <span>চলতি পর্ব: দিন {activeDay} / ২০০</span>
        </div>
      </div>

      {/* Secondary Track Filters & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
        {/* Track Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 scrollbar-none">
          <span className="flex items-center gap-1 text-xs font-medium text-slate-500 dark:text-slate-400 mr-1 shrink-0">
            <Filter className="h-3.5 w-3.5" />
            <span>ট্র্যাক:</span>
          </span>
          {trackTabs.map((tab) => {
            const isActive = selectedTrack === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onSelectTrack(tab.id)}
                className={`whitespace-nowrap rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
                  isActive
                    ? 'border border-emerald-600/30 bg-emerald-50 text-emerald-700 font-semibold dark:border-emerald-500/40 dark:bg-emerald-950/40 dark:text-emerald-300'
                    : 'border border-transparent text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Live Search Input */}
        <div className="relative w-full md:w-72 shrink-0">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="বিষয় বা অধ্যায়ের নাম খুঁজুন..."
            className="w-full rounded-lg border border-slate-200 bg-slate-50 pl-9 pr-4 py-1.5 text-xs sm:text-sm text-slate-900 placeholder-slate-400 focus:border-emerald-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-emerald-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:placeholder-slate-500"
          />
        </div>
      </div>

      <div className="text-[11px] text-slate-500 dark:text-slate-400 pt-1">
        মোট {totalFiltered}টি পরীক্ষার রুটিন প্রদর্শিত হচ্ছে
      </div>
    </div>
  );
};
