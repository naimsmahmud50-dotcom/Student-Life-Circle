/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic 24/7 Doubt-Solve & Offline Learning Grid
 * TOPIC:     10MS Reassurance & Offline-First Value Proposition
 * FILE:      frontend/src/components/competitive-elevation/AcademicDoubtAndOfflineGrid.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, High-Contrast Reassurance Badges, WCAG 2.2 AAA
 */

import React from 'react';
import Link from 'next/link';
import { ACADEMIC_PILLAR_FEATURES, AcademicPillarFeature } from './data/academicElevationData';
import {
  Sparkles,
  WifiOff,
  Trophy,
  BookMarked,
  Headphones,
  Layers,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';

interface AcademicDoubtAndOfflineGridProps {
  className?: string;
}

const renderPillarIcon = (name: AcademicPillarFeature['iconName']) => {
  const iconProps = { className: 'w-5 h-5 text-emerald-800' };
  switch (name) {
    case 'Sparkles':
      return <Sparkles {...iconProps} />;
    case 'WifiOff':
      return <WifiOff {...iconProps} />;
    case 'Trophy':
      return <Trophy {...iconProps} />;
    case 'BookMarked':
      return <BookMarked {...iconProps} />;
    case 'Headphones':
      return <Headphones {...iconProps} />;
    case 'Layers':
      return <Layers {...iconProps} />;
    default:
      return <ShieldCheck {...iconProps} />;
  }
};

export const AcademicDoubtAndOfflineGrid: React.FC<AcademicDoubtAndOfflineGridProps> = ({
  className = '',
}) => {
  return (
    <section className={`w-full py-8 ${className}`} aria-labelledby="academic-pillars-heading">
      <div className="text-center max-w-2xl mx-auto mb-8 px-4">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-200 uppercase tracking-wider">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>শিক্ষা ও পরীক্ষার পূর্ণাঙ্গ নিশ্চয়তা</span>
        </span>
        <h2
          id="academic-pillars-heading"
          className="mt-3 text-2xl sm:text-3xl font-bold font-serif text-slate-900 leading-tight"
        >
          অনলাইনে ও অফলাইনে পড়াশোনা চলুক নিরবচ্ছিন্ন
        </h2>
        <p className="mt-2 text-sm sm:text-base text-slate-600 leading-relaxed">
          দেশের যেকোনো প্রান্ত থেকে কম ব্যান্ডউইথ বা ইন্টারনেট সংযোগ ছাড়াই সর্বোচ্চ মানের শিক্ষা সবার কাছে পৌঁছে দেওয়ার অঙ্গীকার।
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 px-1">
        {ACADEMIC_PILLAR_FEATURES.map((pillar) => (
          <div
            key={pillar.id}
            className="flex flex-col justify-between p-6 rounded-2xl bg-white border border-slate-200 shadow-sm hover:shadow-md transition-shadow duration-200"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-4">
                <div className="w-10 h-10 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center">
                  {renderPillarIcon(pillar.iconName)}
                </div>
                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                  {pillar.badgeBn}
                </span>
              </div>

              <h3 className="text-lg sm:text-xl font-bold font-serif text-slate-900">
                {pillar.titleBn}
              </h3>
              <div className="text-xs sm:text-sm font-semibold text-emerald-800 mt-0.5">
                {pillar.subtitleBn}
              </div>

              <p className="mt-2.5 text-xs sm:text-sm text-slate-600 leading-relaxed">
                {pillar.descriptionBn}
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
              <span className="text-xs font-medium text-slate-500 italic">
                {pillar.reassuranceBn}
              </span>
              <Link
                href={pillar.actionUrl}
                className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-emerald-800 hover:text-emerald-950 transition-colors"
              >
                <span>{pillar.actionLabelBn}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
