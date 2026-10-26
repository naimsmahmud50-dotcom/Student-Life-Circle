/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    MegaModelTestCountdown Component
 * TOPIC:     Friday Mega Model Test Synchronized Countdown & Live Participant Header
 * FILE:      frontend/src/modules/exam-routine/components/MegaModelTestCountdown.tsx
 * PURPOSE:   Renders calm academic hero card for weekly synchronized Mega Model Tests,
 *            displaying live countdown ticks, participant density, and one-click alert setting.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji, Zero-CLS
 * ========================================================================================
 */

import React from 'react';
import { Clock, Users, ShieldCheck, Bell, ChevronRight, Award } from 'lucide-react';
import { CountdownState } from '../hooks/useExamRoutine';

interface MegaModelTestCountdownProps {
  countdown: CountdownState;
  onSetAlert: () => void;
  onOpenSimulator: () => void;
}

export const MegaModelTestCountdown: React.FC<MegaModelTestCountdownProps> = ({
  countdown,
  onSetAlert,
  onOpenSimulator,
}) => {
  return (
    <section 
      aria-label="শুক্রবার মেগা মডেল টেস্ট শিডিউল"
      className="relative overflow-hidden rounded-2xl border border-emerald-900/40 bg-gradient-to-br from-slate-900 via-slate-900 to-emerald-950/40 p-6 sm:p-8 text-white shadow-xl"
    >
      {/* Editorial Decorative Grid Overlay */}
      <div 
        aria-hidden="true" 
        className="pointer-events-none absolute -right-20 -top-20 h-64 w-64 rounded-full bg-emerald-500/10 blur-3xl"
      />

      <div className="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        {/* Left: Academic Title and Information */}
        <div className="max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
            <Award className="h-3.5 w-3.5" />
            <span>সাপ্তাহিক শুক্রবার মেগা মডেল টেস্ট ১</span>
          </div>

          <h2 className="text-xl sm:text-2xl lg:text-3xl font-serif font-bold tracking-tight text-slate-100">
            পূর্ণাঙ্গ ২০০ নম্বর বিসিএস প্রিলিমিনারি ও বিশ্ববিদ্যালয় ভর্তি সিমুলেশন
          </h2>

          <p className="text-sm text-slate-300 leading-relaxed font-sans">
            জাতীয় মেধাতালিকা নির্ধারণী লাইভ পরীক্ষা। নেগেটিভ মার্কিং পেনাল্টি (-০.৫০), রিয়েলটাইম পারসেন্টাইল 
            এবং পুঙ্খানুপুঙ্খ বিষয়ভিত্তিক দুর্বলতা নিরীক্ষা।
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-1 text-xs text-slate-400">
            <span className="flex items-center gap-1.5 font-medium text-emerald-400">
              <Users className="h-4 w-4" />
              <span>১৮,৯৪০+ পরীক্ষার্থী নিবন্ধিত</span>
            </span>
            <span className="h-3 w-px bg-slate-700" />
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
              <span>সার্ভার-সিনক্রোনাইজড টাইমার</span>
            </span>
            <span className="h-3 w-px bg-slate-700" />
            <span>সময়: ১২০ মিনিট | প্রশ্ন: ২০০টি</span>
          </div>
        </div>

        {/* Right: Countdown Cards & Actions */}
        <div className="flex flex-col sm:flex-row lg:flex-col items-start lg:items-end gap-4 shrink-0">
          <div className="flex items-center gap-2 font-mono" aria-label="কাউন্টডাউন সময়">
            <div className="flex flex-col items-center rounded-xl border border-slate-700/80 bg-slate-800/80 px-3 py-2 min-w-[56px] text-center shadow-inner">
              <span className="text-xl sm:text-2xl font-bold text-emerald-400">
                {String(countdown.days).padStart(2, '0')}
              </span>
              <span className="text-[10px] uppercase tracking-wider text-slate-400 font-sans">দিন</span>
            </div>
            <span className="text-slate-600 font-bold">:</span>
            <div className="flex flex-col items-center rounded-xl border border-slate-700/80 bg-slate-800/80 px-3 py-2 min-w-[56px] text-center shadow-inner">
              <span className="text-xl sm:text-2xl font-bold text-emerald-400">
                {String(countdown.hours).padStart(2, '0')}
              </span>
              <span className="text-[10px] uppercase tracking-wider text-slate-400 font-sans">ঘণ্টা</span>
            </div>
            <span className="text-slate-600 font-bold">:</span>
            <div className="flex flex-col items-center rounded-xl border border-slate-700/80 bg-slate-800/80 px-3 py-2 min-w-[56px] text-center shadow-inner">
              <span className="text-xl sm:text-2xl font-bold text-emerald-400">
                {String(countdown.minutes).padStart(2, '0')}
              </span>
              <span className="text-[10px] uppercase tracking-wider text-slate-400 font-sans">মিনিট</span>
            </div>
            <span className="text-slate-600 font-bold">:</span>
            <div className="flex flex-col items-center rounded-xl border border-slate-700/80 bg-slate-800/80 px-3 py-2 min-w-[56px] text-center shadow-inner">
              <span className="text-xl sm:text-2xl font-bold text-emerald-300">
                {String(countdown.seconds).padStart(2, '0')}
              </span>
              <span className="text-[10px] uppercase tracking-wider text-slate-400 font-sans">সেকেন্ড</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
            <button
              type="button"
              onClick={onSetAlert}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 px-4 py-2.5 text-xs sm:text-sm font-semibold text-white shadow-md transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <Bell className="h-4 w-4" />
              <span>অ্যালার্ট সেট করুন</span>
            </button>

            <button
              type="button"
              onClick={onOpenSimulator}
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-700 bg-slate-800/80 hover:bg-slate-700 px-4 py-2.5 text-xs sm:text-sm font-medium text-slate-200 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-500"
            >
              <span>স্কোর সিমুলেটর</span>
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};
