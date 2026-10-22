/**
 * ========================================================================================
 * MODULE:    Whole-Journey Evolving Progression Sidebar
 * TOPIC:     Academic Stages, Minor Safety Indicator & Lifelong Profile Stepper
 * FILE:      frontend/src/components/layout/Sidebar.tsx
 * PURPOSE:   Visualizes the learner's continuous educational journey from Class 1 to
 *            professional career without account fragmentation. Features contextual
 *            stage highlighting, minor privacy indicators, and zero-emoji status SVGs.
 * AUDIENCE:  Learners, Guardians & Educational Advisors
 * STANDARDS: UI/UX Pro Max, Single Profile Lifelong Continuity, Zero-Emoji Policy
 * ========================================================================================
 */

import React from 'react';
import Link from 'next/link';
import { 
  CheckCircle2, 
  Circle, 
  ShieldCheck, 
  Award, 
  BookMarked, 
  Compass,
  ArrowRight
} from 'lucide-react';

interface StageItem {
  id: string;
  titleBn: string;
  titleEn: string;
  status: 'COMPLETED' | 'ACTIVE' | 'UPCOMING';
  href: string;
}

interface SidebarProps {
  activeStageId?: string;
  isMinorProtected?: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeStageId = 'hsc',
  isMinorProtected = true
}) => {
  const stages: StageItem[] = [
    { id: 'primary', titleBn: 'প্রাথমিক (১ম-৫ম)', titleEn: 'Primary Education', status: 'COMPLETED', href: '/learn?stage=PRIMARY' },
    { id: 'middle', titleBn: 'মাধ্যমিক (৬ষ্ঠ-৮ম)', titleEn: 'Junior Secondary', status: 'COMPLETED', href: '/learn?stage=MIDDLE' },
    { id: 'ssc', titleBn: 'এসএসসি (৯ম-১০ম)', titleEn: 'Secondary Certificate', status: 'COMPLETED', href: '/learn?stage=SSC' },
    { id: 'hsc', titleBn: 'এইচএসসি (১১শ-১২শ)', titleEn: 'Higher Secondary', status: 'ACTIVE', href: '/learn?stage=HSC' },
    { id: 'admission', titleBn: 'বিশ্ববিদ্যালয় ভর্তি', titleEn: 'Admission Hub', status: 'UPCOMING', href: '/admission' },
    { id: 'skills', titleBn: 'স্কিল ও প্রজেক্ট', titleEn: 'University Skills', status: 'UPCOMING', href: '/career' },
    { id: 'career', titleBn: 'চাকরি ও ক্যারিয়ার', titleEn: 'Career & Jobs', status: 'UPCOMING', href: '/career' },
  ];

  return (
    <aside className="w-full lg:w-72 flex-shrink-0 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 p-5 space-y-6">
      
      {/* Title & Philosophy */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          একটি প্রোফাইল। একটি দীর্ঘযাত্রা।
        </h2>
        <p className="mt-1 text-sm font-semibold text-slate-900 dark:text-white">
          আপনার শিক্ষাজীবনের ধাপসমূহ
        </p>
      </div>

      {/* Stepper Timeline */}
      <nav aria-label="Education Journey Stages" className="space-y-1">
        {stages.map((st, idx) => {
          const isActive = st.id === activeStageId;
          const isCompleted = st.status === 'COMPLETED';

          return (
            <Link
              key={st.id}
              href={st.href}
              className={`flex items-start gap-3 p-3 rounded-xl text-sm font-medium transition min-h-touch ${
                isActive
                  ? 'bg-blue-50 dark:bg-blue-950/70 text-blue-700 dark:text-blue-300 font-bold border border-blue-200 dark:border-blue-800'
                  : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <div className="mt-0.5">
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5 text-teal-600 dark:text-teal-400" />
                ) : isActive ? (
                  <div className="relative flex items-center justify-center">
                    <span className="w-4 h-4 rounded-full bg-blue-600 dark:bg-blue-400 animate-ping absolute opacity-75"></span>
                    <Circle className="w-4 h-4 text-blue-600 dark:text-blue-400 fill-blue-600 dark:fill-blue-400" />
                  </div>
                ) : (
                  <Circle className="w-4 h-4 text-slate-300 dark:text-slate-600" />
                )}
              </div>
              <div className="flex-1">
                <div className="leading-tight">{st.titleBn}</div>
                <div className="text-[11px] text-slate-500 dark:text-slate-400 font-normal">
                  {st.titleEn}
                </div>
              </div>
              {isActive && <ArrowRight className="w-4 h-4 text-blue-600 dark:text-blue-400 self-center" />}
            </Link>
          );
        })}
      </nav>

      {/* Minor Safety Policy Card */}
      {isMinorProtected && (
        <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-2 text-teal-700 dark:text-teal-400 font-semibold text-xs mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>অপ্রাপ্তবয়স্ক সুরক্ষা সক্রিয়</span>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            অনূর্ধ্ব ১৬ বছর বয়সী শিক্ষার্থীদের ফোন নম্বর, শিক্ষা প্রতিষ্ঠান এবং ব্যক্তিগত তথ্য জনসমক্ষে সম্পূর্ণ গোপন রাখা হয়।
          </p>
        </div>
      )}

      {/* Spaced-Repetition Review CTA */}
      <div className="p-4 rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-slate-800 dark:to-slate-800/60 border border-blue-100 dark:border-slate-700">
        <div className="flex items-center gap-2 text-blue-700 dark:text-blue-400 font-semibold text-xs mb-1">
          <BookMarked className="w-4 h-4" />
          <span>ভুল উত্তর রিভিশন কিউ</span>
        </div>
        <p className="text-xs text-slate-600 dark:text-slate-400">
          আপনার পূর্বে ভুল করা ২টি প্রশ্নের ধারণা পুনরায় ঝালাই করে নিন।
        </p>
        <Link
          href="/practice?mode=MISTAKE_REPLAY"
          className="mt-3 inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline min-h-touch"
        >
          <span>রিভিশন শুরু করুন</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

    </aside>
  );
};
