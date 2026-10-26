/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerCategoryGrid.tsx
 * PURPOSE:   Bdjobs-Style Functional & Special Skill Industry Grid with Live Job Counts
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
  Layers
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
      case 'Award': return <Award className="w-5 h-5 text-red-600 dark:text-red-400" />;
      case 'Users': return <Users className="w-5 h-5 text-teal-600 dark:text-teal-400" />;
      case 'Activity': return <Activity className="w-5 h-5 text-rose-600 dark:text-rose-400" />;
      case 'BookOpen': return <BookOpen className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />;
      case 'Zap': return <Zap className="w-5 h-5 text-amber-500" />;
      case 'Scissors': return <Scissors className="w-5 h-5 text-slate-600 dark:text-slate-400" />;
      case 'Truck': return <Truck className="w-5 h-5 text-sky-600 dark:text-sky-400" />;
      case 'Utensils': return <Utensils className="w-5 h-5 text-orange-600 dark:text-orange-400" />;
      default: return <Layers className="w-5 h-5 text-[#0A2540]" />;
    }
  };

  return (
    <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm space-y-5">
      
      {/* Header and Stream Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold flex items-center gap-2 font-bengali text-[#0A2540] dark:text-white">
            <Layers className="w-5 h-5 text-[#0A2540] dark:text-amber-300" />
            <span>শিল্প ও পেশাভিত্তিক কাজের ক্ষেত্র (Job Categories)</span>
          </h2>
          <p className="text-xs text-slate-500 font-bengali mt-1">
            বাংলাদেশের শীর্ষস্থানীয় সেক্টর অনুযায়ী পছন্দের ক্ষেত্রে সরাসরি নিয়োগ খুঁজুন
          </p>
        </div>

        <div className="inline-flex rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 p-1 border border-slate-200 dark:border-slate-800">
          <button
            onClick={() => setActiveTab('functional')}
            className={`px-4 py-1.5 rounded-xl text-xs font-bold font-bengali transition cursor-pointer ${
              activeTab === 'functional'
                ? 'bg-[#0A2540] text-white shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            ফাংশনাল ক্যাটাগরি (৮)
          </button>
          <button
            onClick={() => setActiveTab('special_skill')}
            className={`px-4 py-1.5 rounded-xl text-xs font-bold font-bengali transition cursor-pointer ${
              activeTab === 'special_skill'
                ? 'bg-[#0A2540] text-white shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            স্পেশাল স্কিল্ড ও টেকনিক্যাল (৪)
          </button>
        </div>
      </div>

      {/* Grid of Categories */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {filteredCategories.map((cat) => {
          const isSelected = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => onSelectCategory(isSelected ? 'all' : cat.id)}
              className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between group cursor-pointer ${
                isSelected
                  ? 'border-[#0A2540] dark:border-amber-400 bg-slate-50 dark:bg-slate-800/80 shadow-xs'
                  : 'border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/40 hover:border-slate-300 dark:hover:border-slate-700'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="w-10 h-10 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center shadow-xs">
                    {getCategoryIcon(cat.iconName)}
                  </div>
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-mono font-bold bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300">
                    {cat.jobCount} টি চাকরি
                  </span>
                </div>

                <h3 className="font-bold text-sm text-slate-900 dark:text-white font-bengali group-hover:text-[#0A2540] dark:group-hover:text-amber-300 transition-colors">
                  {cat.nameBn}
                </h3>
                <p className="text-[11px] text-slate-500 font-bengali mt-1 line-clamp-2 leading-relaxed">
                  {cat.description}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between text-xs font-semibold text-[#0A2540] dark:text-amber-300 font-bengali">
                <span>বিজ্ঞপ্তি দেখুন</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </button>
          );
        })}
      </div>

    </div>
  );
};
