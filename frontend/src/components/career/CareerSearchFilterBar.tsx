/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerSearchFilterBar.tsx
 * PURPOSE:   Bdjobs-Style Multi-Vector Filter & Keyword Search Engine
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, Accessible WCAG 2.2 AAA
 */

import React from 'react';
import { 
  Search, 
  MapPin, 
  Briefcase, 
  Filter, 
  X, 
  RotateCcw,
  Clock,
  Banknote,
  Sparkles
} from 'lucide-react';
import { BANGLADESH_DIVISIONS, CAREER_CATEGORIES } from './data/careerElevationData';

interface CareerSearchFilterBarProps {
  searchQuery: string;
  onSearchChange: (val: string) => void;
  selectedDivision: string;
  onDivisionChange: (val: string) => void;
  selectedCategory: string;
  onCategoryChange: (val: string) => void;
  selectedJobNature: string;
  onJobNatureChange: (val: string) => void;
  selectedOrgType: string;
  onOrgTypeChange: (val: string) => void;
  isHotJobOnly: boolean;
  onToggleHotJobs: () => void;
  onClearFilters: () => void;
  hasActiveFilters: boolean;
}

export const CareerSearchFilterBar: React.FC<CareerSearchFilterBarProps> = ({
  searchQuery,
  onSearchChange,
  selectedDivision,
  onDivisionChange,
  selectedCategory,
  onCategoryChange,
  selectedJobNature,
  onJobNatureChange,
  selectedOrgType,
  onOrgTypeChange,
  isHotJobOnly,
  onToggleHotJobs,
  onClearFilters,
  hasActiveFilters
}) => {
  return (
    <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-sm space-y-4">
      
      {/* Search Input & Primary Dropdowns */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
        
        {/* Keyword Search (Title / Company / Skill) */}
        <div className="md:col-span-5 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="পদবি, কোম্পানি বা দক্ষতার নাম লিখুন (যেমন: Python, MTO, ব্র্যাক)..."
            className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
          />
          {searchQuery && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Division Dropdown */}
        <div className="md:col-span-3 relative">
          <MapPin className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <select
            value={selectedDivision}
            onChange={(e) => onDivisionChange(e.target.value)}
            className="w-full pl-10 pr-8 py-2.5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0A2540] appearance-none cursor-pointer"
          >
            {BANGLADESH_DIVISIONS.map((div) => (
              <option key={div.id} value={div.id}>
                {div.nameBn}
              </option>
            ))}
          </select>
        </div>

        {/* Category Dropdown */}
        <div className="md:col-span-4 relative">
          <Briefcase className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <select
            value={selectedCategory}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="w-full pl-10 pr-8 py-2.5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0A2540] appearance-none cursor-pointer"
          >
            <option value="all">সকল ক্যাটাগরি (All Categories)</option>
            {CAREER_CATEGORIES.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.nameBn} ({cat.jobCount})
              </option>
            ))}
          </select>
        </div>

      </div>

      {/* Secondary Fast-Pill Filters */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-100 dark:border-slate-800">
        
        {/* Job Nature Buttons */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-xs text-slate-500 font-bengali mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" />
            <span>ধরন:</span>
          </span>

          {[
            { id: 'all', label: 'সব' },
            { id: 'FULL_TIME', label: 'ফুল-টাইম' },
            { id: 'INTERNSHIP', label: 'ইন্টার্নশিপ ও ফ্রেশার' },
            { id: 'CONTRACTUAL', label: 'চুক্তিভিত্তিক' }
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => onJobNatureChange(item.id)}
              className={`px-3 py-1 rounded-xl text-xs font-bengali font-bold transition cursor-pointer ${
                selectedJobNature === item.id
                  ? 'bg-[#0A2540] text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* Organization Type Filters & Hot Jobs Toggle */}
        <div className="flex flex-wrap items-center gap-2">
          
          <button
            onClick={() => onOrgTypeChange(selectedOrgType === 'GOVT' ? 'all' : 'GOVT')}
            className={`px-3 py-1 rounded-xl text-xs font-bengali font-bold border transition cursor-pointer ${
              selectedOrgType === 'GOVT'
                ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-900 dark:text-amber-300 border-amber-300'
                : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50'
            }`}
          >
            সরকারি সার্কুলার
          </button>

          <button
            onClick={() => onOrgTypeChange(selectedOrgType === 'NGO' ? 'all' : 'NGO')}
            className={`px-3 py-1 rounded-xl text-xs font-bengali font-bold border transition cursor-pointer ${
              selectedOrgType === 'NGO'
                ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-900 dark:text-emerald-300 border-emerald-300'
                : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50'
            }`}
          >
            এনজিও
          </button>

          <button
            onClick={onToggleHotJobs}
            className={`px-3 py-1 rounded-xl text-xs font-bengali font-bold border transition cursor-pointer flex items-center gap-1 ${
              isHotJobOnly
                ? 'bg-rose-100 dark:bg-rose-950/60 text-rose-900 dark:text-rose-300 border-rose-300'
                : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50'
            }`}
          >
            <Clock className="w-3 h-3 text-rose-600" />
            <span>হট জবস (জরুরি)</span>
          </button>

          {hasActiveFilters && (
            <button
              onClick={onClearFilters}
              className="px-3 py-1 rounded-xl text-xs font-bengali font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition flex items-center gap-1 cursor-pointer"
            >
              <RotateCcw className="w-3 h-3" />
              <span>ফিল্টার রিসেট</span>
            </button>
          )}

        </div>

      </div>

    </div>
  );
};
