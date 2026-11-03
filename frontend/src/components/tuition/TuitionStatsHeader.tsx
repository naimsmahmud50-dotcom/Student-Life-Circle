/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Live Telemetry & Metric Highlights
 * TOPIC:     CareTutors-Style Social Proof & Trust Metrics Bar
 * FILE:      frontend/src/components/tuition/TuitionStatsHeader.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, WCAG 2.2 AAA Contrast, Responsive Grid
 */

import React from 'react';
import { useTranslation } from '../../lib/i18n';
import { Users, Briefcase, Star, ShieldCheck, CheckCircle2 } from 'lucide-react';

interface TuitionStatsHeaderProps {
  className?: string;
}

export const TuitionStatsHeader: React.FC<TuitionStatsHeaderProps> = ({ className = '' }) => {
  const { isBengali } = useTranslation();

  return (
    <section className={`w-full ${className}`} aria-label={isBengali ? "টিউশন প্ল্যাটফর্ম পরিসংখ্যান" : "Tuition Platform Statistics"}>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        {/* Metric 1: Active Tutors */}
        <div className="flex items-center gap-3.5 p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs">
          <div className="w-11 h-11 rounded-xl bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 flex items-center justify-center shrink-0 border border-emerald-200 dark:border-emerald-800">
            <Users className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold font-mono text-slate-900 dark:text-white leading-none">
              {isBengali ? "১৫,০০০+" : "15,000+"}
            </div>
            <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium font-bengali">
              {isBengali ? "যাচাইকৃত সক্রিয় টিউটর" : "Verified Active Tutors"}
            </div>
          </div>
        </div>

        {/* Metric 2: Live Tuition Jobs */}
        <div className="flex items-center gap-3.5 p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs">
          <div className="w-11 h-11 rounded-xl bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-300 flex items-center justify-center shrink-0 border border-blue-200 dark:border-blue-800">
            <Briefcase className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold font-mono text-slate-900 dark:text-white leading-none">
              {isBengali ? "১,৪২০+" : "1,420+"}
            </div>
            <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium font-bengali">
              {isBengali ? "লাইভ টিউশন রিকোয়ারমেন্ট" : "Live Tuition Requirements"}
            </div>
          </div>
        </div>

        {/* Metric 3: Average Rating */}
        <div className="flex items-center gap-3.5 p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs">
          <div className="w-11 h-11 rounded-xl bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 flex items-center justify-center shrink-0 border border-amber-200 dark:border-amber-800">
            <Star className="w-5 h-5 fill-amber-500 text-amber-500" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold font-mono text-slate-900 dark:text-white leading-none flex items-center gap-1">
              <span>{isBengali ? "৪.৯" : "4.9"}</span>
              <span className="text-xs text-slate-400 font-sans">{isBengali ? "/৫" : "/5"}</span>
            </div>
            <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium font-bengali">
              {isBengali ? "গড় অভিভাবক সন্তুষ্টি" : "Average Parent Satisfaction"}
            </div>
          </div>
        </div>

        {/* Metric 4: Zero Scam / Trial */}
        <div className="flex items-center gap-3.5 p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs">
          <div className="w-11 h-11 rounded-xl bg-purple-100 dark:bg-purple-950/60 text-purple-800 dark:text-purple-300 flex items-center justify-center shrink-0 border border-purple-200 dark:border-purple-800">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold font-mono text-emerald-700 dark:text-emerald-400 leading-none">
              {isBengali ? "০ টাকা" : "BDT 0"}
            </div>
            <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 font-medium font-bengali">
              {isBengali ? "অগ্রিম ফি ও ২ দিন ফ্রি ট্রায়াল" : "Advance Fee & 2-Day Free Trial"}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
