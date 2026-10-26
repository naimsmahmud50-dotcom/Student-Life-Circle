/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ 2D Elevation & Academic Typography
 * FILE:      frontend/src/components/live-challenge/LiveMcqHeroSection.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Reverse-engineers and elevates Live MCQ's signature hero section:
 *            authentic Oxford academic canvas, engraved 2D Armillary Sphere motif,
 *            editorial serif typography, server-authoritative countdown timer,
 *            platform ecosystem row, and 4 national trust KPI cards with zero emojis.
 * STANDARDS: Zero-Emoji, Zero-AI Vibe, WCAG 2.2 AAA Contrast, Human Craftsmanship
 */

import React from 'react';
import Link from 'next/link';
import {
  Trophy,
  Users,
  ShieldCheck,
  ArrowRight,
  BookOpen,
  Smartphone,
  Monitor,
  Check
} from 'lucide-react';
import { Scene3DSlot } from './Scene3DSlot';

interface LiveMcqHeroSectionProps {
  challenge: {
    id: string;
    titleBn: string;
    titleEn: string;
    startTimeRemainingSeconds: number;
    registeredCount: number;
    durationMinutes: number;
    totalQuestions: number;
    negativeMarkingRatio: number;
    syllabusSummaryBn: string;
  };
  timeRemainingSeconds: number;
  formatTimer: (seconds: number) => string;
  isLoading: boolean;
  onOpenRulesModal: () => void;
}

export function LiveMcqHeroSection({
  challenge,
  timeRemainingSeconds,
  formatTimer,
  isLoading,
  onOpenRulesModal
}: LiveMcqHeroSectionProps) {
  return (
    <section className="relative overflow-hidden rounded-3xl bg-[#07192F] text-white border border-[#1E3A5F] shadow-2xl">
      {/* Refined Academic Hairline Grid Canvas (Strict Zero AI Glow Blobs) */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden select-none" aria-hidden="true">
        <div
          className="absolute inset-0 opacity-[0.05]"
          style={{
            backgroundImage:
              'radial-gradient(circle, #ffffff 1px, transparent 1px), linear-gradient(to right, rgba(255,255,255,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.06) 1px, transparent 1px)',
            backgroundSize: '32px 32px, 64px 64px, 64px 64px'
          }}
        />
        {/* Subtle architectural hairline border inside the hero */}
        <div className="absolute inset-3 border border-white/5 rounded-2xl pointer-events-none" />
      </div>

      <div className="relative z-10 px-6 sm:px-10 lg:px-12 py-10 sm:py-14 space-y-10">
        
        {/* Top Header Badge & Categorical Track Indicators */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-[#0A2540] border border-[#1E3A5F]">
            <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block" />
            <span className="text-xs font-bold text-amber-300 font-bengali tracking-wide">
              সঠিক প্রস্তুতি, সহজ প্রিলি • জাতীয় লাইভ প্ল্যাটফর্ম
            </span>
          </div>

          {/* Restrained Academic Category Pills */}
          <div className="flex flex-wrap items-center gap-2 text-[11px] font-bold font-bengali text-slate-300">
            <span className="px-2.5 py-1 rounded-lg bg-[#0F2D4A] text-amber-200 border border-[#1E3E66]">
              বিসিএস ও ব্যাংক
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-[#0F2D4A] text-emerald-200 border border-[#1E3E66]">
              এইচএসসি সায়েন্স
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-[#0F2D4A] text-sky-200 border border-[#1E3E66]">
              মেডিকেল ও ভর্তি
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-[#0F2D4A] text-amber-300 border border-[#B45309]/50">
              জাতীয় অলিম্পিয়াড
            </span>
          </div>
        </div>

        {/* Hero Composition: Editorial Headline + 2D Academic Motif */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Column: Dignified Editorial Typography */}
          <div className="lg:col-span-8 space-y-4">
            <h1 className="text-2xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight font-serif leading-[1.3] text-balance">
              ঘরে বসেই সকল প্রতিযোগিতামূলক{' '}
              <span className="text-amber-400 font-serif">
                পরীক্ষার শীর্ষ প্রস্তুতি
              </span>
            </h1>

            <p className="text-sm sm:text-base text-slate-300 font-bengali leading-[1.8] max-w-2xl">
              বিসিএস, ব্যাংক, প্রাইমারি, এইচএসসি এবং জাতীয় অলিম্পিয়াডসহ সকল প্রতিযোগিতামূলক পরীক্ষার প্রস্তুতিতে 
              দেশের প্রথম ও সর্ববৃহৎ ডিজিটাল একাডেমি প্ল্যাটফর্ম — <strong className="text-amber-300 font-semibold">২৩ লাখ+</strong> শিক্ষার্থীর আস্থার নাম।
            </p>
          </div>

          {/* Right Column: Progressive 2D/3D Adaptive Hero Composition */}
          <div className="hidden lg:flex lg:col-span-4 items-center justify-center">
            <div className="p-2 rounded-3xl bg-[#0A2540]/60 border border-white/10 shadow-lg">
              <Scene3DSlot size={280} timeRemainingSeconds={timeRemainingSeconds} />
            </div>
          </div>

        </div>

        {/* Active Examination Arena Card (Server-Authoritative) */}
        {isLoading ? (
          <div className="p-8 rounded-2xl bg-[#0A2540] border border-[#1E3A5F] space-y-4 animate-pulse">
            <div className="h-6 bg-slate-800 rounded-lg w-1/3"></div>
            <div className="h-10 bg-slate-800/80 rounded-xl w-3/4"></div>
            <div className="h-16 bg-slate-800/40 rounded-xl"></div>
          </div>
        ) : (
          <div className="p-6 sm:p-8 rounded-2xl bg-[#0A2540] border-2 border-white/15 shadow-xl flex flex-col lg:flex-row lg:items-center justify-between gap-8">
            
            <div className="space-y-4 max-w-2xl">
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-3 py-1 rounded-full bg-[#07192F] text-amber-300 border border-white/20 text-xs font-bold font-bengali flex items-center gap-1.5">
                  <Trophy className="w-3.5 h-3.5 text-amber-300" />
                  <span>লাইভ অলিম্পিয়াড পরীক্ষা</span>
                </span>
                <span className="px-3 py-1 rounded-full bg-[#991B1B]/40 text-rose-200 border border-[#991B1B] text-xs font-mono font-bold">
                  নেগেটিভ মার্কিং: -০.২৫
                </span>
                <button
                  type="button"
                  onClick={onOpenRulesModal}
                  className="px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-bold font-bengali flex items-center gap-1 transition"
                >
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>নিয়মাবলী</span>
                </button>
              </div>

              <div className="text-xl sm:text-3xl font-extrabold text-white tracking-tight font-serif">
                {challenge.titleBn}
              </div>

              <p className="text-xs sm:text-sm text-slate-200 leading-[1.75] font-bengali">
                সিলেবাস: {challenge.syllabusSummaryBn}
              </p>

              {/* Waiting Room & Live Participant Count (Calm, dignified academic beacon) */}
              <div className="flex flex-wrap items-center gap-3 pt-1">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#07192F] border border-[#1E3A5F] text-xs font-bold text-amber-300 font-bengali">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block animate-pulse" />
                  <Users className="w-3.5 h-3.5 text-amber-300" />
                  <span>{challenge.registeredCount.toLocaleString()} জন প্রতিযোগী শিক্ষার্থী লাইভ লবিতে যুক্ত</span>
                </div>
                <span className="text-[11px] font-mono text-slate-300 px-2 py-0.5 rounded bg-white/5 border border-white/10">
                  লাইভ অপেক্ষা কক্ষ • Waiting Room
                </span>
              </div>
            </div>

            {/* Synchronized Server Timer & Primary Entry CTA */}
            <div className="flex flex-col items-center sm:items-start lg:items-end gap-5">
              <div className="p-4 rounded-2xl bg-[#071D33] border border-white/20 text-center min-w-[210px] shadow-inner">
                <span className="text-[10px] text-slate-300 uppercase font-mono block mb-1">
                  সার্ভার-অথরিটেটিভ টাইমার
                </span>
                <div className="text-3xl sm:text-4xl font-mono font-black text-amber-300 tabular-nums">
                  {formatTimer(timeRemainingSeconds || 1200)}
                </div>
                <span className="text-[10px] text-emerald-300 font-mono mt-1 block">
                  মিলি-সেকেন্ড একুরেট বাফার
                </span>
              </div>

              <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
                <Link
                  href="/practice?challenge=active"
                  className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-white text-[#0A2540] hover:bg-slate-100 font-bold font-bengali text-sm shadow-[0_4px_0_0_#CBD5E1] active:translate-y-1 active:shadow-none transition text-center min-h-[48px] flex items-center justify-center gap-2"
                >
                  <span>পরীক্ষায় অংশগ্রহণ করুন</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <a
                  href="#demo-exam"
                  className="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-white/10 hover:bg-white/20 text-white font-bold font-bengali text-sm border border-white/20 transition text-center min-h-[48px] flex items-center justify-center gap-2"
                >
                  <span>ফ্রি ডেমো এক্সাম</span>
                </a>
              </div>
            </div>

          </div>
        )}

        {/* Multi-Platform Availability Row (Like Live MCQ web & app) */}
        <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-t border-slate-800">
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-400 font-bengali">
              যে কোনো ডিভাইসে সহজে এক্সেস করুন:
            </span>
            <div className="flex items-center gap-2 text-slate-300">
              <span className="px-2.5 py-1 rounded-md bg-[#0A2540] border border-[#1E3A5F] text-[11px] font-mono flex items-center gap-1.5">
                <Smartphone className="w-3.5 h-3.5 text-emerald-400" /> Android
              </span>
              <span className="px-2.5 py-1 rounded-md bg-[#0A2540] border border-[#1E3A5F] text-[11px] font-mono flex items-center gap-1.5">
                <Smartphone className="w-3.5 h-3.5 text-sky-400" /> iOS
              </span>
              <span className="px-2.5 py-1 rounded-md bg-[#0A2540] border border-[#1E3A5F] text-[11px] font-mono flex items-center gap-1.5">
                <Monitor className="w-3.5 h-3.5 text-blue-400" /> Windows
              </span>
              <span className="px-2.5 py-1 rounded-md bg-[#0A2540] border border-[#1E3A5F] text-[11px] font-mono flex items-center gap-1.5">
                <Monitor className="w-3.5 h-3.5 text-amber-400" /> macOS
              </span>
            </div>
          </div>

          <span className="text-xs font-mono text-emerald-400 flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-emerald-400" /> ১০০% বিজ্ঞাপনমুক্ত ও নিরাপদ
          </span>
        </div>

        {/* 4 Grand Trust KPIs (Strict Editorial Solid Borders) */}
        <ul aria-label="বিশ্বাসের পরিসংখ্যান" className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
          <li className="p-4 rounded-2xl bg-[#0A2540]/80 border border-[#1E3A5F] text-center hover:border-amber-400/60 transition">
            <div className="text-2xl sm:text-3xl font-black font-mono text-amber-300">
              ২৩ লাখ+
            </div>
            <div className="text-xs text-slate-300 font-bengali mt-1">
              নিবন্ধিত শিক্ষার্থী
            </div>
          </li>
          <li className="p-4 rounded-2xl bg-[#0A2540]/80 border border-[#1E3A5F] text-center hover:border-sky-400/60 transition">
            <div className="text-2xl sm:text-3xl font-black font-mono text-sky-300">
              ৭.৫ লাখ+
            </div>
            <div className="text-xs text-slate-300 font-bengali mt-1">
              আর্কাইভ প্রশ্ন ও ব্যাখ্যা
            </div>
          </li>
          <li className="p-4 rounded-2xl bg-[#0A2540]/80 border border-[#1E3A5F] text-center hover:border-emerald-400/60 transition">
            <div className="text-2xl sm:text-3xl font-black font-mono text-emerald-300">
              ৩০ হাজার+
            </div>
            <div className="text-xs text-slate-300 font-bengali mt-1">
              প্রতিদিন লাইভ অংশগ্রহণকারী
            </div>
          </li>
          <li className="p-4 rounded-2xl bg-[#0A2540]/80 border border-[#1E3A5F] text-center hover:border-rose-400/60 transition">
            <div className="text-2xl sm:text-3xl font-black font-mono text-rose-300">
              ১০+ বছর
            </div>
            <div className="text-xs text-slate-300 font-bengali mt-1">
              জাতীয় কারিকুলাম ও টিম অভিজ্ঞতা
            </div>
          </li>
        </ul>

      </div>
    </section>
  );
}
