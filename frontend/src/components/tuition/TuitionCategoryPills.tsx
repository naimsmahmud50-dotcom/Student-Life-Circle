/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Stream & Category Filter Pills
 * TOPIC:     CareTutors Serving Categories Stream Switcher
 * FILE:      frontend/src/components/tuition/TuitionCategoryPills.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Accessible Horizontal Stream Switcher, WCAG 2.2 AAA
 */

import React from 'react';
import { TUITION_CATEGORIES, TuitionCategoryInfo } from './data/tuitionElevationData';
import {
  GraduationCap,
  BookOpen,
  Globe,
  Languages,
  Award,
  Atom,
  Palette,
  HeartHandshake,
} from 'lucide-react';

interface TuitionCategoryPillsProps {
  selectedCategoryId: TuitionCategoryInfo['id'];
  onSelectCategory: (id: TuitionCategoryInfo['id']) => void;
  className?: string;
}

const renderCategoryIcon = (iconName: TuitionCategoryInfo['iconName']) => {
  const iconProps = { className: 'w-4 h-4 shrink-0' };
  switch (iconName) {
    case 'BookOpen':
      return <BookOpen {...iconProps} />;
    case 'Globe':
      return <Globe {...iconProps} />;
    case 'Languages':
      return <Languages {...iconProps} />;
    case 'Award':
      return <Award {...iconProps} />;
    case 'Atom':
      return <Atom {...iconProps} />;
    case 'Palette':
      return <Palette {...iconProps} />;
    case 'HeartHandshake':
      return <HeartHandshake {...iconProps} />;
    default:
      return <GraduationCap {...iconProps} />;
  }
};

export const TuitionCategoryPills: React.FC<TuitionCategoryPillsProps> = ({
  selectedCategoryId,
  onSelectCategory,
  className = '',
}) => {
  return (
    <div
      role="tablist"
      aria-label="টিউশন ক্যাটাগরি নির্বাচন"
      className={`flex items-center gap-2 overflow-x-auto pb-2 pt-1 no-scrollbar ${className}`}
    >
      {TUITION_CATEGORIES.map((cat) => {
        const isSelected = cat.id === selectedCategoryId;
        return (
          <button
            key={cat.id}
            role="tab"
            aria-selected={isSelected}
            onClick={() => onSelectCategory(cat.id)}
            className={`flex-shrink-0 inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-150 border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 focus-visible:ring-offset-2 ${
              isSelected
                ? 'bg-[#0A2540] dark:bg-emerald-800 text-white border-[#0A2540] dark:border-emerald-700 shadow-sm'
                : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 hover:border-slate-300'
            }`}
          >
            {renderCategoryIcon(cat.iconName)}
            <span className="font-bengali">{cat.nameBn}</span>
            <span
              className={`text-[11px] font-mono font-bold px-1.5 py-0.2 rounded ${
                isSelected
                  ? 'bg-white/20 text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400'
              }`}
            >
              {cat.jobsCount}
            </span>
          </button>
        );
      })}
    </div>
  );
};
