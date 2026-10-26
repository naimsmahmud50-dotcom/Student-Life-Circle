/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Master Competitive Elevation Section
 * TOPIC:     10MS Reverse Engineering Synthesis & Academic Excellence Hub
 * FILE:      frontend/src/components/competitive-elevation/CompetitiveElevationSection.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Authentic Academic Monograms, Strict Scope Lock, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { AcademicSegmentNav } from './AcademicSegmentNav';
import { AcademicBundleCard } from './AcademicBundleCard';
import { AcademicDoubtAndOfflineGrid } from './AcademicDoubtAndOfflineGrid';
import { VerifiedAchieverShowcase } from './VerifiedAchieverShowcase';
import { AcademicHelplinePill } from './AcademicHelplinePill';
import { ACADEMIC_BUNDLES, AcademicCategory } from './data/academicElevationData';
import { Compass, BookCheck, ShieldCheck } from 'lucide-react';

interface CompetitiveElevationSectionProps {
  className?: string;
  defaultCategoryId?: AcademicCategory['id'];
}

export const CompetitiveElevationSection: React.FC<CompetitiveElevationSectionProps> = ({
  className = '',
  defaultCategoryId = 'hsc_27',
}) => {
  const [selectedCategoryId, setSelectedCategoryId] = useState<AcademicCategory['id']>(defaultCategoryId);

  const filteredBundles = ACADEMIC_BUNDLES.filter(
    (bundle) => bundle.categoryId === selectedCategoryId
  );

  return (
    <section
      className={`relative w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 text-slate-900 ${className}`}
      aria-labelledby="competitive-elevation-heading"
    >
      {/* Top Academic Value Proposition (10MS Microcopy Adaptation) */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-3 shadow-xs">
          <ShieldCheck className="w-4 h-4 text-emerald-700" />
          <span>জাতীয় অলিম্পিয়াড ও বোর্ড পরীক্ষার সেরা প্ল্যাটফর্ম</span>
        </div>
        <h2
          id="competitive-elevation-heading"
          className="text-2xl sm:text-4xl font-extrabold font-serif tracking-tight text-slate-900 leading-tight"
        >
          এক জায়গায় স্কুল, কলেজ ও প্রতিযোগিতামূলক পরীক্ষার পূর্ণাঙ্গ প্রস্তুতি
        </h2>
        <p className="mt-3 text-sm sm:text-base text-slate-600 leading-relaxed font-sans">
          অনলাইনেই শেখা হোক নিজের গতিতে। লাইভ মাস্টারক্লাস, আনলিমিটেড ওএমআর মডেল টেস্ট, ২৪ ঘণ্টা ডাউট সলভ এবং ইন্টারনেট সংযোগ ছাড়াই অফলাইনে পড়ালেখা।
        </p>
      </div>

      {/* Segment Switcher */}
      <div className="mb-8">
        <AcademicSegmentNav
          selectedCategoryId={selectedCategoryId}
          onSelectCategory={(id) => setSelectedCategoryId(id)}
        />
      </div>

      {/* Filtered Course Bundles Grid */}
      <div
        id={`academic-panel-${selectedCategoryId}`}
        role="tabpanel"
        aria-labelledby={`academic-tab-${selectedCategoryId}`}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {filteredBundles.length > 0 ? (
          filteredBundles.map((bundle) => (
            <AcademicBundleCard key={bundle.id} bundle={bundle} />
          ))
        ) : (
          <div className="col-span-full py-12 text-center bg-white rounded-2xl border border-slate-200 p-6">
            <Compass className="w-10 h-10 text-slate-400 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-800 font-serif">
              এই বিভাগের নতুন সেশনের কোর্স তালিকা দ্রুত যুক্ত করা হচ্ছে
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              অন্যান্য সেশনের লাইভ কুইজ ও মডেল টেস্ট অনুশীলনে অংশ নিতে পারেন।
            </p>
          </div>
        )}
      </div>

      {/* 24/7 Socratic AI & Offline PWA Reassurance Grid */}
      <div className="mt-14 border-t border-slate-200 pt-10">
        <AcademicDoubtAndOfflineGrid />
      </div>

      {/* Verified Achievers Showcase */}
      <div className="mt-12 border-t border-slate-200 pt-10">
        <VerifiedAchieverShowcase />
      </div>

      {/* Floating 24/7 Helpline */}
      <AcademicHelplinePill shortCode="16910" />
    </section>
  );
};
export default CompetitiveElevationSection;
