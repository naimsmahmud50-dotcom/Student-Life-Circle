/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Telemetry & National Trust Statistics Grid
 * TOPIC:     Unified Premium Dark Design System, Micro-visuals & WCAG Contrast
 * FILE:      frontend/src/components/stats/AcademicTelemetrySection.tsx
 * PHASE:     Phase 137 - World-Class Academic Telemetry Redesign (Round 2 Polish)
 * PURPOSE:   Provides Linear/Vercel/Stripe-grade dark telemetry grid with unified card
 *            design language, animated count-ups, SVG progress rings, 7-day streak pills,
 *            weekly activity sparklines, percentile slider, and zero-emoji purity.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA Contrast, Tabular Numerals, Responsive Fluidity
 */

import React, { useState, useEffect } from 'react';
import {
  Flame,
  CheckCircle2,
  Target,
  Award,
  BookOpen,
  ShieldCheck,
  Compass,
  Lock,
  Layers
} from 'lucide-react';

/**
 * Bengali numeral converter for mathematical numbers
 */
export function toBengaliNumeral(num: number | string): string {
  const bengaliDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
  return String(num).replace(/[0-9]/g, (digit) => bengaliDigits[parseInt(digit, 10)]);
}

/**
 * Hook for smooth count-up animations respecting prefers-reduced-motion
 * Defaults to target immediately on SSR so static captures are complete and non-zero
 */
function useCountUp(target: number, duration: number = 800, isDecimal: boolean = false, enabled: boolean = true): number {
  const [current, setCurrent] = useState(target);

  useEffect(() => {
    if (!enabled) return;

    if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setCurrent(target);
      return;
    }

    const startVal = Math.max(0, Math.floor(target * 0.3));
    let startTimestamp: number | null = null;
    let animationFrameId: number;

    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const rawVal = startVal + (target - startVal) * ease;
      const val = isDecimal ? Math.round(rawVal * 10) / 10 : Math.round(rawVal);
      setCurrent(val);

      if (progress < 1) {
        animationFrameId = requestAnimationFrame(step);
      } else {
        setCurrent(target);
      }
    };

    animationFrameId = requestAnimationFrame(step);
    return () => cancelAnimationFrame(animationFrameId);
  }, [target, duration, isDecimal, enabled]);

  return current;
}

/**
 * Component Props Contract
 */
export interface AcademicTelemetryProps {
  personalData?: {
    streakDays?: number;
    streakPills?: { day: string; active: boolean; isToday?: boolean }[];
    solvedCount?: number;
    weeklySolved?: number[];
    accuracyRate?: number;
    percentileTop?: number;
    percentileScore?: number;
  };
  platformData?: {
    archiveYears?: string;
    archiveSpan?: string;
    nctbCoverage?: string;
    nctbModules?: string;
    districtCount?: string;
    subDistrictCount?: string;
    privacyRate?: string;
  };
}

export const AcademicTelemetrySection: React.FC<AcademicTelemetryProps> = ({
  personalData = {
    streakDays: 7,
    streakPills: [
      { day: 'শনি', active: true },
      { day: 'রবি', active: true },
      { day: 'সোম', active: true },
      { day: 'মঙ্গল', active: true },
      { day: 'বুধ', active: true },
      { day: 'বৃহঃ', active: true },
      { day: 'শুক্র', active: true, isToday: true },
    ],
    solvedCount: 128,
    weeklySolved: [12, 18, 14, 26, 20, 16, 22],
    accuracyRate: 86.4,
    percentileTop: 5,
    percentileScore: 95.2,
  },
  platformData = {
    archiveYears: '১০ বছর',
    archiveSpan: '২০১৫ — ২০২৫',
    nctbCoverage: '১০০%',
    nctbModules: '৬৯টি মডিউল',
    districtCount: '৬৪ জেলা',
    subDistrictCount: '৪৯৫টি উপজেলা',
    privacyRate: '০%',
  },
}) => {
  // Count-up hooks for personal telemetry
  const animatedStreak = useCountUp(personalData.streakDays ?? 7, 700, false);
  const animatedSolved = useCountUp(personalData.solvedCount ?? 128, 900, false);
  const animatedAccuracy = useCountUp(personalData.accuracyRate ?? 86.4, 1000, true);

  return (
    <section
      aria-label="অ্যাকাডেমিক প্রোগ্রেস ও প্ল্যাটফর্ম পরিসংখ্যান"
      className="py-14 sm:py-16 md:py-20 bg-[#071727] text-white border-b border-white/[0.08] relative overflow-hidden"
    >
      {/* Subtle architectural ambient background glow */}
      <div
        className="absolute inset-0 pointer-events-none opacity-30 bg-[radial-gradient(ellipse_80%_50%_at_50%_-15%,rgba(16,185,129,0.15),transparent)]"
        aria-hidden="true"
      />
      <div
        className="absolute inset-0 pointer-events-none opacity-20 bg-[radial-gradient(ellipse_70%_40%_at_50%_115%,rgba(10,37,64,0.9),transparent)]"
        aria-hidden="true"
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12 sm:space-y-14 relative z-10">

        {/* ===================================================================
            TIER 1: আমার প্রোগ্রেস (PERSONAL TELEMETRY & STUDY MOMENTUM)
            =================================================================== */}
        <div className="space-y-5">
          {/* Section Header */}
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-2 border-b border-white/[0.07]">
            <div className="space-y-1">
              <div className="inline-flex items-center gap-2 text-[11px] sm:text-[12px] font-semibold text-emerald-400 tracking-wider uppercase font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                লাইভ লার্নিং টেলিমেট্রি
              </div>
              <h2 className="text-xl sm:text-2xl md:text-3xl font-bold font-bengali text-white tracking-tight">
                আমার অনুশীলন ও মেধা প্রবৃদ্ধি
              </h2>
            </div>
            <p className="text-[13px] sm:text-sm text-slate-300 font-bengali leading-relaxed max-w-md sm:text-right">
              দৈনন্দিন অধ্যবসায়, প্রশ্ন সমাধান, নির্ভুলতা ও জাতীয় মেধাতালিকায় আপনার অবস্থান
            </p>
          </div>

          {/* Tier 1 Grid: 4 Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">

            {/* CARD 1: 7-DAY STREAK (Amber Accent) */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-amber-400/40 transition-all duration-200 flex flex-col justify-between space-y-5">
              <div className="space-y-3.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Flame className="w-[18px] h-[18px] text-amber-400 fill-amber-400/20" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      অধ্যয়ন স্ট্রিক
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/25 font-bengali">
                    ধারাবাহিক
                  </span>
                </div>

                <div className="space-y-1">
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                      {toBengaliNumeral(animatedStreak)}
                    </span>
                    <span className="text-xl font-bold text-slate-200 font-bengali">দিনের স্ট্রিক</span>
                  </div>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    টানা ৭ দিন সক্রিয় প্রশ্ন অনুশীলন অব্যাহত
                  </p>
                </div>
              </div>

              {/* Data Visual: 7-Day Streak Pills */}
              <div className="pt-3 border-t border-white/[0.07]">
                <div className="flex items-center justify-between gap-1.5 mb-1.5">
                  {(personalData.streakPills || []).map((item, idx) => (
                    <div key={idx} className="flex-1 flex flex-col items-center gap-1.5">
                      <div
                        className={`w-full h-2.5 rounded-full transition-all duration-300 ${
                          item.active
                            ? item.isToday
                              ? 'bg-amber-400'
                              : 'bg-amber-400/80'
                            : 'bg-white/10'
                        }`}
                        title={`${item.day}: ${item.active ? 'অর্জিত' : 'বাকি'}`}
                      />
                      <span className="text-[11px] font-medium text-slate-400 font-bengali">
                        {item.day}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* CARD 2: SOLVED QUESTIONS (Emerald Accent) */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-emerald-400/40 transition-all duration-200 flex flex-col justify-between space-y-5">
              <div className="space-y-3.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-[18px] h-[18px] text-emerald-400" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      প্রশ্ন সমাধান
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-emerald-400/10 text-emerald-300 border border-emerald-400/25 font-bengali">
                    বোর্ড ব্যাংক
                  </span>
                </div>

                <div className="space-y-1">
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                      {toBengaliNumeral(animatedSolved)}
                    </span>
                    <span className="text-xl font-bold text-slate-200 font-bengali">টি প্রশ্ন</span>
                  </div>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    এনসিটিবি বোর্ড প্রশ্ন ব্যাংক থেকে সম্পন্ন
                  </p>
                </div>
              </div>

              {/* Data Visual: 7-Day Weekly Activity Sparkline Bars */}
              <div className="pt-3 border-t border-white/[0.07]">
                <div
                  className="flex items-end justify-between gap-1.5 h-7 pb-1 border-b border-white/[0.08]"
                  aria-label="সাপ্তাহিক প্রশ্ন সমাধানের চার্ট"
                >
                  {(personalData.weeklySolved || [12, 18, 14, 26, 20, 16, 22]).map((val, idx) => {
                    const maxVal = Math.max(...(personalData.weeklySolved || [12, 18, 14, 26, 20, 16, 22]));
                    const heightPercent = Math.max(25, Math.round((val / maxVal) * 100));
                    const isLatest = idx === (personalData.weeklySolved || []).length - 1;
                    return (
                      <div
                        key={idx}
                        className="flex-1 flex flex-col justify-end items-center h-full group/bar"
                      >
                        <div
                          style={{ height: `${heightPercent}%` }}
                          className={`w-full rounded-t-[3px] transition-all duration-300 ${
                            isLatest
                              ? 'bg-[#0B5D3B] dark:bg-emerald-500'
                              : 'bg-[#0B5D3B]/35 dark:bg-emerald-500/35 group-hover/bar:bg-[#0B5D3B]/60 dark:group-hover/bar:bg-emerald-400/60'
                          }`}
                          title={`দিন ${toBengaliNumeral(idx + 1)}: ${toBengaliNumeral(val)}টি`}
                        />
                      </div>
                    );
                  })}
                </div>
                <div className="flex justify-between items-center text-[10px] text-slate-400 font-bengali mt-1.5">
                  <span>৭ দিন পূর্বে</span>
                  <span className="text-emerald-300 font-medium">আজকের পিক ({toBengaliNumeral(22)}টি)</span>
                </div>
              </div>
            </div>

            {/* CARD 3: ACCURACY RATE (Emerald Accent) */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-emerald-400/40 transition-all duration-200 flex flex-col justify-between space-y-5">
              <div className="space-y-3.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Target className="w-[18px] h-[18px] text-emerald-400" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      গড় নির্ভুলতা
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08] font-bengali">
                    ঋণাত্মক সতর্ক
                  </span>
                </div>

                <div className="space-y-1">
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                      {toBengaliNumeral(animatedAccuracy.toFixed(1))}
                    </span>
                    <span className="text-2xl font-black text-emerald-400 font-mono">%</span>
                  </div>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    নেগেটিভ মার্কিং এড়িয়ে নির্ভুল উত্তর নিরূপণ
                  </p>
                </div>
              </div>

              {/* Data Visual: Compact Circular Progress Ring */}
              <div className="pt-3 border-t border-white/[0.07] flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="relative w-8 h-8 flex items-center justify-center">
                    <svg className="w-8 h-8 transform -rotate-90" viewBox="0 0 36 36" aria-hidden="true">
                      <path
                        className="text-white/10"
                        strokeWidth="3.5"
                        stroke="currentColor"
                        fill="none"
                        d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      />
                      <path
                        className="text-emerald-400 transition-all duration-1000 ease-out"
                        strokeDasharray="100, 100"
                        strokeDashoffset={100 - (personalData.accuracyRate ?? 86.4)}
                        strokeWidth="3.5"
                        strokeLinecap="round"
                        stroke="currentColor"
                        fill="none"
                        d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      />
                    </svg>
                    <span className="absolute text-[8px] font-bold font-mono text-emerald-300">
                      {toBengaliNumeral(Math.round(personalData.accuracyRate ?? 86.4))}
                    </span>
                  </div>
                  <div className="text-[12px] font-semibold font-bengali text-slate-200">
                    উচ্চ নির্ভুলতা ব্যান্ড
                  </div>
                </div>
                <span className="text-[11px] font-mono text-emerald-300 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 font-bengali">
                  +৪.২% প্রবৃদ্ধি
                </span>
              </div>
            </div>

            {/* CARD 4: NATIONAL PERCENTILE (Emerald Accent) */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-emerald-400/40 transition-all duration-200 flex flex-col justify-between space-y-5">
              <div className="space-y-3.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Award className="w-[18px] h-[18px] text-emerald-400" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      জাতীয় পার্সেন্টাইল
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-emerald-400/10 text-emerald-300 border border-emerald-400/25 font-bengali">
                    শীর্ষ মেধা
                  </span>
                </div>

                <div className="space-y-1">
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl sm:text-4xl font-black text-white font-bengali tracking-tight">
                      শীর্ষ {toBengaliNumeral(personalData.percentileTop ?? 5)}%
                    </span>
                    <span className="text-lg font-bold text-slate-200 font-bengali">শিক্ষার্থী</span>
                  </div>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    দেশব্যাপী ৫০,০০০+ সক্রিয় পরীক্ষার্থীর মধ্যে
                  </p>
                </div>
              </div>

              {/* Data Visual: Percentile Track Bar with User Marker */}
              <div className="pt-3 border-t border-white/[0.07] space-y-1.5">
                <div className="relative w-full h-2.5 bg-white/10 rounded-full overflow-hidden">
                  <div
                    style={{ width: `${personalData.percentileScore ?? 95.2}%` }}
                    className="h-full bg-[#0B5D3B] dark:bg-emerald-500 rounded-full"
                  />
                </div>
                <div className="flex items-center justify-between text-[11px] text-slate-400 font-bengali">
                  <span>০%</span>
                  <span className="text-emerald-300 font-semibold font-mono">
                    {toBengaliNumeral(personalData.percentileScore ?? 95.2)}তম পার্সেন্টাইল
                  </span>
                  <span>১০০%</span>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* ===================================================================
            TIER 2: প্ল্যাটফর্ম ট্রাস্ট (NATIONAL TRUST & PEDAGOGICAL PILLARS)
            =================================================================== */}
        <div className="space-y-5 pt-2">
          {/* Section Header */}
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-2 border-b border-white/[0.07]">
            <div className="space-y-1">
              <div className="inline-flex items-center gap-2 text-[11px] sm:text-[12px] font-semibold text-slate-300 tracking-wider uppercase font-mono">
                <Layers className="w-3.5 h-3.5 text-emerald-400" aria-hidden="true" />
                প্রাতিষ্ঠানিক ভিত্তি
              </div>
              <h2 className="text-xl sm:text-2xl md:text-3xl font-bold font-bengali text-white tracking-tight">
                প্ল্যাটফর্ম ট্রাস্ট ও জাতীয় শিক্ষাক্রম মানদণ্ড
              </h2>
            </div>
            <p className="text-[13px] sm:text-sm text-slate-300 font-bengali leading-relaxed max-w-md sm:text-right">
              সার্বভৌম শিক্ষাক্রম, অফলাইন প্রযুক্তি ও শিক্ষার্থী গোপনীয়তার প্রাতিষ্ঠানিক সুরক্ষা
            </p>
          </div>

          {/* Tier 2 Grid: 4 Cards (Identical Unified Geometry) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">

            {/* CARD 5: 10-YEAR ARCHIVE (Clean Single Line Metric) */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-white/20 transition-all duration-200 flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-[18px] h-[18px] text-slate-300" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      বোর্ড প্রশ্ন আর্কাইভ
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08] font-bengali">
                    {platformData.archiveSpan || '২০১৫ — ২০২৫'}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="text-3xl sm:text-4xl font-black text-white font-bengali tracking-tight">
                    {platformData.archiveYears || '১০ বছর'}
                  </div>
                  <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                    আসল বোর্ড প্রশ্ন সমাধান
                  </h3>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    সকল সাধারণ ও কারিগরি শিক্ষা বোর্ডের মূল প্রশ্ন এবং নিখুঁত KaTeX সমীকরণ
                  </p>
                </div>
              </div>

              {/* Data Visual: 10-Segment Continuous Timeline Bar */}
              <div className="pt-3 border-t border-white/[0.07]">
                <div className="flex items-center gap-1" title="১০ বছরের অবিচ্ছিন্ন আর্কাইভ">
                  {Array.from({ length: 10 }).map((_, i) => (
                    <div
                      key={i}
                      className="flex-1 h-2 rounded-full bg-white/20 hover:bg-emerald-400 transition-colors duration-200"
                    />
                  ))}
                </div>
                <div className="flex justify-between items-center text-[10px] text-slate-400 font-bengali mt-1.5">
                  <span>২০১৫</span>
                  <span className="text-slate-300 font-medium">১০/১০ বছর সম্পূর্ণ</span>
                  <span>২০২৫</span>
                </div>
              </div>
            </div>

            {/* CARD 6: 100% NCTB COMPLIANT */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-emerald-400/40 transition-all duration-200 flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-[18px] h-[18px] text-emerald-400" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      জাতীয় মানদণ্ড
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-emerald-400/10 text-emerald-300 border border-emerald-400/25 font-bengali">
                    ভেরিফায়েড
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="text-3xl sm:text-4xl font-black text-emerald-400 font-mono tabular-nums tracking-tight">
                    {platformData.nctbCoverage || '১০০%'}
                  </div>
                  <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                    জাতীয় শিক্ষাক্রম কারিকুলাম
                  </h3>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    মাধ্যমিক ও উচ্চ মাধ্যমিকের ৬৯টি অ্যাকাডেমিক অধ্যায়ের শতভাগ এনসিটিবি মান
                  </p>
                </div>
              </div>

              {/* Data Visual: 100% Solid Emerald Progress Bar */}
              <div className="pt-3 border-t border-white/[0.07]">
                <div className="w-full h-2 rounded-full bg-emerald-400" />
                <div className="flex justify-between items-center text-[10px] text-slate-400 font-bengali mt-1.5">
                  <span>এনসিটিবি অনুমোদিত</span>
                  <span className="text-emerald-300 font-medium">৬৯ / ৬৯ অধ্যায়</span>
                </div>
              </div>
            </div>

            {/* CARD 7: 64 DISTRICTS P2P OFFLINE */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-white/20 transition-all duration-200 flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Compass className="w-[18px] h-[18px] text-slate-300" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      দেশব্যাপী রেজিলিয়েন্স
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08] font-bengali">
                    P2P মেশ
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="text-3xl sm:text-4xl font-black text-white font-bengali tracking-tight">
                    {platformData.districtCount || '৬৪ জেলা'}
                  </div>
                  <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                    অফলাইন লোকাল ক্লাসরুম
                  </h3>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    ইন্টারনেট বিচ্ছিন্নতা ও লোডশেডিংয়ে লোকাল মেশে পরীক্ষা এবং স্বয়ংক্রিয় সিঙ্ক
                  </p>
                </div>
              </div>

              {/* Data Visual: 4 Interconnected Node Mesh Link */}
              <div className="pt-3 border-t border-white/[0.07]">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                    <span className="w-8 h-[2px] bg-white/20" />
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                    <span className="w-8 h-[2px] bg-white/20" />
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                  </div>
                  <span className="text-[11px] font-mono text-slate-300 font-bengali">
                    {platformData.subDistrictCount || '৪৯৫ উপজেলা'}
                  </span>
                </div>
                <div className="text-[10px] text-slate-400 font-bengali mt-1.5">
                  জিরো-প্যাকেট লস আর্কিটেকচার
                </div>
              </div>
            </div>

            {/* CARD 8: 0% INTRUSIVE SURVEILLANCE */}
            <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-xs hover:border-white/20 transition-all duration-200 flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Lock className="w-[18px] h-[18px] text-slate-300" aria-hidden="true" />
                    <span className="text-[15px] font-medium text-slate-200 font-bengali">
                      মর্যাদা ও অধিকার
                    </span>
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08] font-bengali">
                    নিরাপদ
                  </span>
                </div>

                <div className="space-y-1.5">
                  <div className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                    {platformData.privacyRate || '০%'}
                  </div>
                  <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                    জিরো-ভিডিও প্রক্টরিং
                  </h3>
                  <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                    কোনো ওয়েবক্যাম বা ফেসিয়াল ট্র্যাকিং নয়; সম্পূর্ণ শিক্ষার্থী মর্যাদা ও গোপনীয়তা
                  </p>
                </div>
              </div>

              {/* Data Visual: End-to-End Cryptographic Security Status */}
              <div className="pt-3 border-t border-white/[0.07]">
                <div className="flex items-center gap-2 text-[11px] font-medium text-emerald-400 font-bengali">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block" />
                  <span>এন্ড-টু-এন্ড এনক্রিপ্টেড ও সুরক্ষিত</span>
                </div>
                <div className="text-[10px] text-slate-400 font-bengali mt-1.5">
                  সার্বভৌম শিক্ষার্থী ডেটা নিরাপত্তা
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
};

export default AcademicTelemetrySection;
