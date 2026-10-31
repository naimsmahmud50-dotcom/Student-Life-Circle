/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerSearchFilterBar.tsx
 * PURPOSE:   Bdjobs-Style Multi-Vector Filter & Keyword Search Engine with Atmospheric Elevation
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
  ChevronDown,
  Building2,
  Compass
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
    <div className="relative overflow-hidden rounded-3xl border border-amber-200/60 dark:border-[#262D3D] bg-white/95 dark:bg-[#0B0F19]/95 backdrop-blur-md p-5 sm:p-7 shadow-xs space-y-4">
      
      {/* Subtle Warm Amber Atmospheric Halo */}
      <div
        className="absolute top-0 right-0 w-96 h-96 pointer-events-none select-none z-0"
        style={{
          background: 'radial-gradient(circle at 100% 0%, rgba(237, 142, 34, 0.12) 0%, rgba(253, 215, 70, 0.03) 55%, transparent 100%)'
        }}
        aria-hidden="true"
      />

      {/* Search Input & Primary Dropdowns */}
      <div className="relative z-10 grid grid-cols-1 md:grid-cols-12 gap-3.5">
        
        {/* Keyword Search (Title / Company / Skill) */}
        <div className="md:col-span-5 relative">
          <Search className="w-4 h-4 text-[#ED8E22] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="পদবি, কোম্পানি বা দক্ষতার নাম লিখুন (যেমন: Python, MTO, ব্র্যাক)..."
            className="w-full pl-10 pr-10 py-3 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-slate-700/80 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-[#ED8E22]/30 focus:border-[#ED8E22] shadow-xs transition"
          />
          {searchQuery && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 rounded-md transition cursor-pointer"
              aria-label="ক্লিয়ার সার্চ"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Division Dropdown */}
        <div className="md:col-span-3 relative">
          <MapPin className="w-4 h-4 text-[#0A2540] dark:text-blue-300 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <select
            value={selectedDivision}
            onChange={(e) => onDivisionChange(e.target.value)}
            className="w-full pl-10 pr-9 py-3 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-slate-700/80 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#ED8E22]/30 focus:border-[#ED8E22] appearance-none cursor-pointer shadow-xs transition"
          >
            {BANGLADESH_DIVISIONS.map((div) => (
              <option key={div.id} value={div.id}>
                {div.nameBn}
              </option>
            ))}
          </select>
          <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>

        {/* Category Dropdown */}
        <div className="md:col-span-4 relative">
          <Briefcase className="w-4 h-4 text-emerald-600 dark:text-emerald-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <select
            value={selectedCategory}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="w-full pl-10 pr-9 py-3 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-slate-700/80 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#ED8E22]/30 focus:border-[#ED8E22] appearance-none cursor-pointer shadow-xs transition"
          >
            <option value="all">সকল ক্যাটাগরি (All Categories)</option>
            {CAREER_CATEGORIES.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.nameBn} ({cat.jobCount})
              </option>
            ))}
          </select>
          <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>

      </div>

      {/* Secondary Fast-Pill Filters */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-amber-200/40 dark:border-[#262D3D]">
        
        {/* Job Nature Buttons */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-xs font-semibold text-slate-600 dark:text-slate-300 font-bengali mr-1 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-[#ED8E22]" />
            <span>কাজের ধরন:</span>
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
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bengali font-bold transition-all cursor-pointer ${
                selectedJobNature === item.id
                  ? 'bg-[#0A2540] dark:bg-amber-400 text-white dark:text-slate-950 shadow-xs ring-1 ring-[#0A2540]/30'
                  : 'bg-white dark:bg-[#121B2D] text-slate-700 dark:text-slate-300 border border-amber-200/60 dark:border-slate-700/60 hover:bg-amber-50/50 dark:hover:bg-slate-800'
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
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bengali font-bold border transition-all cursor-pointer flex items-center gap-1.5 ${
              selectedOrgType === 'GOVT'
                ? 'bg-amber-100 dark:bg-amber-950/70 text-amber-900 dark:text-amber-200 border-amber-300 dark:border-amber-700 shadow-xs'
                : 'bg-white dark:bg-[#121B2D] border-amber-200/60 dark:border-slate-700/60 text-slate-700 dark:text-slate-300 hover:bg-amber-50/50'
            }`}
          >
            <Building2 className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            <span>সরকারি সার্কুলার</span>
          </button>

          <button
            onClick={() => onOrgTypeChange(selectedOrgType === 'NGO' ? 'all' : 'NGO')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bengali font-bold border transition-all cursor-pointer flex items-center gap-1.5 ${
              selectedOrgType === 'NGO'
                ? 'bg-emerald-100 dark:bg-emerald-950/70 text-emerald-900 dark:text-emerald-200 border-emerald-300 dark:border-emerald-700 shadow-xs'
                : 'bg-white dark:bg-[#121B2D] border-amber-200/60 dark:border-slate-700/60 text-slate-700 dark:text-slate-300 hover:bg-emerald-50/50'
            }`}
          >
            <Compass className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>এনজিও</span>
          </button>

          <button
            onClick={onToggleHotJobs}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-bengali font-bold border transition-all cursor-pointer flex items-center gap-1.5 ${
              isHotJobOnly
                ? 'bg-rose-100 dark:bg-rose-950/70 text-rose-900 dark:text-rose-200 border-rose-300 dark:border-rose-700 shadow-xs'
                : 'bg-white dark:bg-[#121B2D] border-amber-200/60 dark:border-slate-700/60 text-slate-700 dark:text-slate-300 hover:bg-rose-50/50'
            }`}
          >
            <Clock className="w-3.5 h-3.5 text-rose-600 dark:text-rose-400" />
            <span>হট জবস (জরুরি)</span>
          </button>

          {hasActiveFilters && (
            <button
              onClick={onClearFilters}
              className="px-3.5 py-1.5 rounded-xl text-xs font-bengali font-bold text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/30 border border-rose-200/60 dark:border-rose-900/40 hover:bg-rose-100 dark:hover:bg-rose-950/60 transition flex items-center gap-1 cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>ফিল্টার রিসেট</span>
            </button>
          )}

        </div>

      </div>

    </div>
  );
};
