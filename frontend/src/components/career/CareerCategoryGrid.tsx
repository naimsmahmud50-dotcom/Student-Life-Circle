/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerCategoryGrid.tsx
 * PURPOSE:   Bdjobs-Style Functional & Special Skill Industry Grid with Atmospheric Elevation
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { 
  Code, 
  Building2, 
  Compass, 
  TrendingUp, 
  Award, 
  Users, 
  Activity, 
  BookOpen, 
  Zap, 
  Scissors, 
  Truck, 
  Utensils,
  ChevronRight,
  Layers,
  Sparkles
} from 'lucide-react';
import { CAREER_CATEGORIES, CareerCategory } from './data/careerElevationData';

interface CareerCategoryGridProps {
  selectedCategory: string;
  onSelectCategory: (catId: string) => void;
}

export const CareerCategoryGrid: React.FC<CareerCategoryGridProps> = ({
  selectedCategory,
  onSelectCategory
}) => {
  const [activeTab, setActiveTab] = useState<'functional' | 'special_skill'>('functional');

  const filteredCategories = CAREER_CATEGORIES.filter(c => c.type === activeTab);

  const getCategoryIcon = (iconName: string) => {
    switch (iconName) {
      case 'Code': return <Code className="w-5 h-5 text-blue-600 dark:text-blue-400" />;
      case 'Building2': return <Building2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />;
      case 'Compass': return <Compass className="w-5 h-5 text-amber-600 dark:text-amber-400" />;
      case 'TrendingUp': return <TrendingUp className="w-5 h-5 text-purple-600 dark:text-purple-400" />;
      case 'Award': return <Award className="w-5 h-5 text-rose-600 dark:text-rose-400" />;
      case 'Users': return <Users className="w-5 h-5 text-teal-600 dark:text-teal-400" />;
      case 'Activity': return <Activity className="w-5 h-5 text-rose-600 dark:text-rose-400" />;
      case 'BookOpen': return <BookOpen className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />;
      case 'Zap': return <Zap className="w-5 h-5 text-amber-500" />;
      case 'Scissors': return <Scissors className="w-5 h-5 text-slate-600 dark:text-slate-400" />;
      case 'Truck': return <Truck className="w-5 h-5 text-sky-600 dark:text-sky-400" />;
      case 'Utensils': return <Utensils className="w-5 h-5 text-orange-600 dark:text-orange-400" />;
      default: return <Layers className="w-5 h-5 text-emerald-700" />;
    }
  };

  return (
    <div className="relative overflow-hidden rounded-3xl border border-emerald-200/60 dark:border-emerald-950/70 bg-[#F4FAF6]/90 dark:bg-[#071714]/90 p-6 sm:p-8 shadow-xs space-y-6">
      
      {/* Fresh Emerald Atmospheric Glow Stop */}
      <div
        className="absolute bottom-0 right-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '100%',
          minHeight: '280px',
          background:
            'radial-gradient(ellipse 65% 85% at 80% 100%, rgba(16, 185, 129, 0.16) 0%, rgba(16, 185, 129, 0.05) 50%, transparent 100%)'
        }}
        aria-hidden="true"
      />

      {/* Atmospheric Typographic Watermark */}
      <div
        className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
        aria-hidden="true"
      >
        <p
          className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,13rem)] uppercase tracking-wider select-none opacity-85"
          style={{
            lineHeight: 0.95,
            backgroundImage:
              'linear-gradient(to bottom, rgba(16, 185, 129, 0.22) 15%, rgba(16, 185, 129, 0.02) 100%)'
          }}
        >
          SECTORS
        </p>
      </div>

      {/* Header and Stream Switcher */}
      <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-200/60 dark:border-emerald-900/60 pb-5">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100/90 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300/80 dark:border-emerald-800 shadow-xs">
              <Layers className="w-3.5 h-3.5 mr-1 text-emerald-600 dark:text-emerald-400" />
              ক্যারিয়ার সেক্টর ম্যাট্রিক্স
            </span>
          </div>

          <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0B251F] dark:text-[#E8F8F4]">
            শিল্প ও পেশাভিত্তিক কাজের ক্ষেত্র (Job Categories)
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
            বাংলাদেশের শীর্ষস্থানীয় সেক্টর অনুযায়ী পছন্দের ক্ষেত্রে সরাসরি নিয়োগ বিজ্ঞপ্তি ফিল্টার করুন
          </p>
        </div>

        {/* Tab Toggle Switcher */}
        <div className="inline-flex rounded-2xl bg-white/90 dark:bg-[#0B1E1A] p-1 border border-emerald-200/80 dark:border-emerald-900/70 shadow-xs">
          <button
            onClick={() => setActiveTab('functional')}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition cursor-pointer ${
              activeTab === 'functional'
                ? 'bg-emerald-800 dark:bg-emerald-400 text-white dark:text-slate-950 shadow-xs'
                : 'text-slate-600 dark:text-slate-300 hover:text-emerald-900 dark:hover:text-white'
            }`}
          >
            ফাংশনাল ক্যাটাগরি (৮)
          </button>
          <button
            onClick={() => setActiveTab('special_skill')}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition cursor-pointer ${
              activeTab === 'special_skill'
                ? 'bg-emerald-800 dark:bg-emerald-400 text-white dark:text-slate-950 shadow-xs'
                : 'text-slate-600 dark:text-slate-300 hover:text-emerald-900 dark:hover:text-white'
            }`}
          >
            স্পেশাল স্কিল্ড ও টেকনিক্যাল (৪)
          </button>
        </div>
      </div>

      {/* Grid of Categories */}
      <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {filteredCategories.map((cat) => {
          const isSelected = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => onSelectCategory(isSelected ? 'all' : cat.id)}
              className={`p-4 sm:p-5 rounded-2xl border text-left transition-all duration-200 flex flex-col justify-between group cursor-pointer backdrop-blur-xs ${
                isSelected
                  ? 'border-emerald-600 dark:border-emerald-400 bg-white dark:bg-[#0D2420] shadow-md ring-2 ring-emerald-500/20 scale-[1.01]'
                  : 'border-emerald-100/90 dark:border-emerald-900/50 bg-white/90 dark:bg-[#0B1E1A]/80 hover:border-emerald-300 dark:hover:border-emerald-700 hover:shadow-md hover:-translate-y-0.5'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3.5">
                  <div className="w-11 h-11 rounded-xl bg-emerald-50/80 dark:bg-emerald-950/60 border border-emerald-200/60 dark:border-emerald-800/60 flex items-center justify-center shadow-xs group-hover:scale-105 transition-transform">
                    {getCategoryIcon(cat.iconName)}
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-white dark:bg-[#071714] border border-emerald-200/60 dark:border-emerald-800/60 text-emerald-800 dark:text-emerald-300 shadow-xs">
                    {cat.jobCount} টি চাকরি
                  </span>
                </div>

                <h3 className="font-bold text-sm text-slate-900 dark:text-white font-bengali group-hover:text-emerald-700 dark:group-hover:text-emerald-300 transition-colors">
                  {cat.nameBn}
                </h3>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 font-bengali mt-1.5 line-clamp-2 leading-relaxed">
                  {cat.description}
                </p>
              </div>

              <div className="mt-4 pt-2.5 border-t border-emerald-100/80 dark:border-emerald-900/50 flex items-center justify-between text-xs font-bold text-emerald-800 dark:text-emerald-300 font-bengali">
                <span>{isSelected ? 'নির্বাচিত ফিল্টার (বাতিল করতে ক্লিক)' : 'বিজ্ঞপ্তি দেখুন'}</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </button>
          );
        })}
      </div>

    </div>
  );
};
