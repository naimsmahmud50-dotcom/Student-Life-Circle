/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Course & Subject Bundle Card
 * TOPIC:     10MS-Style Tactile Educational Bundle Card with Academic Rigor
 * FILE:      frontend/src/components/competitive-elevation/AcademicBundleCard.tsx
 * STANDARDS: Zero-Emoji, Tactile Physical 3D Buttons, Pure Lucide SVGs, WCAG 2.2 AAA Contrast
 */

import React from 'react';
import Link from 'next/link';
import { AcademicBundle, AcademicSubject } from './data/academicElevationData';
import {
  Atom,
  FlaskConical,
  Calculator,
  Dna,
  BookOpen,
  Globe,
  Cpu,
  TrendingUp,
  ShieldCheck,
  CheckCircle2,
  FileText,
  Users,
  ArrowRight,
} from 'lucide-react';

interface AcademicBundleCardProps {
  bundle: AcademicBundle;
  className?: string;
}

const renderSubjectIcon = (iconName: AcademicSubject['iconName']) => {
  const iconProps = { className: 'w-3.5 h-3.5 flex-shrink-0' };
  switch (iconName) {
    case 'Atom':
      return <Atom {...iconProps} />;
    case 'FlaskConical':
      return <FlaskConical {...iconProps} />;
    case 'Calculator':
      return <Calculator {...iconProps} />;
    case 'Dna':
      return <Dna {...iconProps} />;
    case 'BookOpen':
      return <BookOpen {...iconProps} />;
    case 'Globe':
      return <Globe {...iconProps} />;
    case 'Cpu':
      return <Cpu {...iconProps} />;
    case 'TrendingUp':
      return <TrendingUp {...iconProps} />;
    case 'ShieldCheck':
      return <ShieldCheck {...iconProps} />;
    default:
      return <BookOpen {...iconProps} />;
  }
};

export const AcademicBundleCard: React.FC<AcademicBundleCardProps> = ({
  bundle,
  className = '',
}) => {
  const badgeColors = {
    emerald: 'bg-emerald-100 text-emerald-900 border-emerald-300',
    gold: 'bg-amber-100 text-amber-900 border-amber-300',
    crimson: 'bg-red-100 text-red-900 border-red-300',
  }[bundle.badgeType || 'emerald'];

  return (
    <article
      className={`relative flex flex-col justify-between bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden ${className}`}
    >
      {/* Top Banner & Header */}
      <div className="p-5 sm:p-6 border-b border-slate-100">
        <div className="flex items-center justify-between gap-2 mb-3">
          <span
            className={`inline-flex items-center text-xs font-bold px-2.5 py-0.5 rounded-full border ${badgeColors}`}
          >
            {bundle.badgeBn}
          </span>
          <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
            <Users className="w-3.5 h-3.5 text-slate-400" />
            <span>{bundle.enrolledStudentsCount.toLocaleString('bn-BD')}+ শিক্ষার্থী</span>
          </div>
        </div>

        <h3 className="text-lg sm:text-xl font-bold font-serif text-slate-900 leading-snug">
          {bundle.titleBn}
        </h3>
        <p className="mt-1 text-xs sm:text-sm text-slate-600 leading-relaxed">
          {bundle.subtitleBn}
        </p>

        {/* Subjects Checklist Pills */}
        <div className="mt-4 flex flex-wrap gap-1.5">
          {bundle.subjects.map((sub) => (
            <span
              key={sub.id}
              className="inline-flex items-center gap-1 text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded-md border border-slate-200 font-medium"
            >
              {renderSubjectIcon(sub.iconName)}
              <span>{sub.nameBn}</span>
            </span>
          ))}
        </div>
      </div>

      {/* Deliverables List (10MS Feature Mapping) */}
      <div className="p-5 sm:p-6 flex-1 flex flex-col justify-between bg-slate-50/50">
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-2.5">
            কোর্সের অন্তর্ভুক্ত বিশেষ সুবিধাসমূহ:
          </span>
          <ul className="space-y-2">
            {bundle.deliverablesBn.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-slate-700">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Deliverable Metrics & CTA Footer */}
        <div className="mt-6 pt-4 border-t border-slate-200/80 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center border border-emerald-200">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-bold text-slate-900 leading-none">
                {bundle.mockTestsCount.toLocaleString('bn-BD')}টি মডেল টেস্ট
              </div>
              <div className="text-[11px] text-slate-500 mt-0.5">
                নেগেটিভ মার্কিং সহ প্র্যাকটিস
              </div>
            </div>
          </div>

          <Link
            href={bundle.targetUrl}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-900 active:bg-emerald-950 text-white font-semibold text-xs sm:text-sm shadow-sm transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 focus-visible:ring-offset-2"
          >
            <span>{bundle.actionTextBn}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </article>
  );
};
