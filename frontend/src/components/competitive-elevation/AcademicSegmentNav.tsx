/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Stream Segment Navigation
 * TOPIC:     10MS-Style Fast Segment Navigation & Academic Filter
 * FILE:      frontend/src/components/competitive-elevation/AcademicSegmentNav.tsx
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Tablist, Keyboard Navigation, Tactile Physical States, Zero-CLS
 */

import React from 'react';
import { ACADEMIC_CATEGORIES, AcademicCategory } from './data/academicElevationData';
import { GraduationCap, Sparkles } from 'lucide-react';

interface AcademicSegmentNavProps {
  selectedCategoryId: string;
  onSelectCategory: (id: AcademicCategory['id']) => void;
  className?: string;
}

export const AcademicSegmentNav: React.FC<AcademicSegmentNavProps> = ({
  selectedCategoryId,
  onSelectCategory,
  className = '',
}) => {
  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let nextIndex = index;
    if (e.key === 'ArrowRight') {
      nextIndex = (index + 1) % ACADEMIC_CATEGORIES.length;
    } else if (e.key === 'ArrowLeft') {
      nextIndex = (index - 1 + ACADEMIC_CATEGORIES.length) % ACADEMIC_CATEGORIES.length;
    } else if (e.key === 'Home') {
      nextIndex = 0;
    } else if (e.key === 'End') {
      nextIndex = ACADEMIC_CATEGORIES.length - 1;
    } else {
      return;
    }
    e.preventDefault();
    onSelectCategory(ACADEMIC_CATEGORIES[nextIndex].id);
    const nextTab = document.getElementById(`academic-tab-${ACADEMIC_CATEGORIES[nextIndex].id}`);
    if (nextTab) {
      nextTab.focus();
    }
  };

  return (
    <nav
      className={`w-full ${className}`}
      aria-label="অ্যাকাডেমিক বিভাগ নির্বাচন"
    >
      <div className="flex items-center justify-between mb-3 px-1">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center border border-emerald-200">
            <GraduationCap className="w-4 h-4" />
          </div>
          <span className="text-xs sm:text-sm font-semibold tracking-wide text-slate-800 uppercase font-sans">
            অ্যাকাডেমিক স্ট্রিম ও ব্যাচ নির্বাচন
          </span>
        </div>
        <div className="hidden sm:flex items-center gap-1.5 text-xs text-emerald-700 font-medium bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
          <Sparkles className="w-3.5 h-3.5" />
          <span>নতুন সেশনের পূর্ণাঙ্গ প্রস্তুতি</span>
        </div>
      </div>

      <div
        role="tablist"
        aria-orientation="horizontal"
        className="flex items-center gap-2 overflow-x-auto pb-2 pt-1 px-1 scrollbar-thin scrollbar-thumb-slate-300 scrollbar-track-transparent no-scrollbar"
      >
        {ACADEMIC_CATEGORIES.map((cat, idx) => {
          const isSelected = cat.id === selectedCategoryId;
          return (
            <button
              key={cat.id}
              id={`academic-tab-${cat.id}`}
              role="tab"
              aria-selected={isSelected}
              aria-controls={`academic-panel-${cat.id}`}
              tabIndex={isSelected ? 0 : -1}
              onClick={() => onSelectCategory(cat.id)}
              onKeyDown={(e) => handleKeyDown(e, idx)}
              className={`flex-shrink-0 group relative flex flex-col items-start px-4 py-2.5 rounded-xl border text-left transition-all duration-150 outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 focus-visible:ring-offset-2 ${
                isSelected
                  ? 'bg-emerald-800 border-emerald-900 text-white shadow-md shadow-emerald-950/20 translate-y-[-1px]'
                  : 'bg-white border-slate-200 text-slate-800 hover:bg-slate-50 hover:border-slate-300'
              }`}
            >
              <div className="flex items-center gap-1.5 w-full justify-between">
                <span
                  className={`font-semibold text-sm sm:text-base leading-snug font-serif ${
                    isSelected ? 'text-white' : 'text-slate-900 group-hover:text-emerald-800'
                  }`}
                >
                  {cat.labelBn}
                </span>
                {cat.badgeBn && (
                  <span
                    className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded tracking-wider ${
                      isSelected
                        ? 'bg-emerald-600/60 text-emerald-100 border border-emerald-500/50'
                        : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                    }`}
                  >
                    {cat.badgeBn}
                  </span>
                )}
              </div>
              <span
                className={`text-[11px] mt-0.5 leading-tight ${
                  isSelected ? 'text-emerald-100/90' : 'text-slate-500'
                }`}
              >
                {cat.subLabelBn}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
