/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Stream & Category Filter Pills
 * TOPIC:     CareTutors Serving Categories Stream Switcher
 * FILE:      frontend/src/components/tuition/TuitionCategoryPills.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Accessible Horizontal Stream Switcher, WCAG 2.2 AAA
 */

import React, { useRef, useState, useEffect } from 'react';
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
  ChevronLeft,
  ChevronRight,
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
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState<boolean>(false);
  const [canScrollRight, setCanScrollRight] = useState<boolean>(false);

  const checkScroll = () => {
    if (scrollRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
      setCanScrollLeft(scrollLeft > 4);
      setCanScrollRight(scrollLeft + clientWidth < scrollWidth - 4);
    }
  };

  useEffect(() => {
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, []);

  const handleScroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const scrollAmount = direction === 'left' ? -280 : 280;
      scrollRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  const handlePillClick = (catId: TuitionCategoryInfo['id'], e: React.MouseEvent<HTMLButtonElement>) => {
    onSelectCategory(catId);
    e.currentTarget.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center',
    });
  };

  return (
    <div className={`relative flex items-center group ${className}`}>
      {/* Optional Left Scroll Arrow for Desktop */}
      {canScrollLeft && (
        <button
          type="button"
          onClick={() => handleScroll('left')}
          className="absolute -left-3 z-10 p-1.5 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-md text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all cursor-pointer hidden md:flex items-center justify-center active:scale-95"
          aria-label="বামে স্ক্রোল করুন"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
      )}

      {/* Main Horizontal Scroll Container with Multi-layer Scrollbar Suppression */}
      <div
        ref={scrollRef}
        onScroll={checkScroll}
        role="tablist"
        aria-label="টিউশন ক্যাটাগরি নির্বাচন"
        className="flex items-center gap-2 overflow-x-auto scroll-smooth py-1 px-0.5 no-scrollbar [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden w-full select-none"
      >
        {TUITION_CATEGORIES.map((cat) => {
          const isSelected = cat.id === selectedCategoryId;
          return (
            <button
              key={cat.id}
              role="tab"
              aria-selected={isSelected}
              onClick={(e) => handlePillClick(cat.id, e)}
              className={`flex-shrink-0 inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-150 border cursor-pointer active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0A2540] dark:focus-visible:ring-emerald-500 focus-visible:ring-offset-2 ${
                isSelected
                  ? 'bg-[#0A2540] dark:bg-emerald-800 text-white border-[#0A2540] dark:border-emerald-700 shadow-sm'
                  : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 hover:border-slate-300'
              }`}
            >
              {renderCategoryIcon(cat.iconName)}
              <span className="font-bengali whitespace-nowrap">{cat.nameBn}</span>
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

      {/* Optional Right Scroll Arrow for Desktop */}
      {canScrollRight && (
        <button
          type="button"
          onClick={() => handleScroll('right')}
          className="absolute -right-3 z-10 p-1.5 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-md text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all cursor-pointer hidden md:flex items-center justify-center active:scale-95"
          aria-label="ডানে স্ক্রোল করুন"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};
