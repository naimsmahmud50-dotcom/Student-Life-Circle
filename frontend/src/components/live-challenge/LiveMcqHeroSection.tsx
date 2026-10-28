/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 143 - Live MCQ Exact Visual Elevation & Hero Canvas
 * FILE:      frontend/src/components/live-challenge/LiveMcqHeroSection.tsx
 * PURPOSE:   Reverse-engineers and faithfully matches the exact Live MCQ hero aesthetic:
 *            1. Deep cosmic indigo canvas with diagonal light streaks and warm amber stardust.
 *            2. Floating track pills (BCS, NTRCA, Primary, Bank, BJS) with glowing borders.
 *            3. Floating educational motifs (Graduation cap with tassel, open book, pencil).
 *            4. Central editorial typography:
 *               - Capsule badge: "সঠিক প্রস্তুতি, সহজ প্রিলি"
 *               - Dual-line headline: "ঘরে বসেই সকল প্রতিযোগিতামূলক" + fiery orange "চাকরির পূর্ণাঙ্গ প্রস্তুতি"
 *               - Candidate count subtitle with highlighted "২৪ লাখ+" badge.
 *            5. Dual CTA pill buttons: Cyan-Cobalt "৪৫তম স্পেশাল বিসিএস" + Orange "পরীক্ষা দিন".
 *            6. Multi-platform ecosystem row: Google Play, App Store, Windows, macOS, Web.
 *            7. Bottom docked frosted glass container with 4 grand KPI metrics:
 *               - ২৪ লাখ+ অ্যাপ ব্যবহারকারী
 *               - ৭.৫ লাখ+ আর্কাইভ MCQ
 *               - ৩০ হাজার+ প্রতিদিন গড় ব্যবহারকারী
 *               - ১০+ বছরের অভিজ্ঞতা
 * STANDARDS: Zero-Emoji, Pure Lucide/Inline SVG, WCAG 2.2 AAA Contrast, Port 3002 Discipline
 */

import React from 'react';
import Link from 'next/link';
import {
  Trophy,
  Users,
  ShieldCheck,
  ArrowRight,
  BookOpen,
  Award,
  FileText,
  CheckCircle2,
  Globe,
  MousePointer,
  GraduationCap,
  Sparkles,
  FileEdit
} from 'lucide-react';

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
    <section className="relative overflow-hidden w-full bg-[#080C24] text-white pt-10 pb-16 sm:pt-14 sm:pb-20 border-b border-[#1E294B] shadow-2xl selection:bg-[#FF8A00] selection:text-white">
      
      {/* 1. Deep Cosmic Indigo Background & Lighting System */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden" aria-hidden="true">
        {/* Core Multi-Stop Indigo/Cosmic Gradient */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 75% 65% at 50% 32%, rgba(37, 99, 235, 0.28) 0%, rgba(99, 102, 241, 0.16) 42%, rgba(8, 12, 36, 0.95) 85%)'
          }}
        />

        {/* Diagonal Luminous Sheer Light Streaks */}
        <svg
          className="absolute inset-0 w-full h-full opacity-25"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="livemcqStreak" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.45" />
              <stop offset="35%" stopColor="#60A5FA" stopOpacity="0.25" />
              <stop offset="70%" stopColor="#818CF8" stopOpacity="0.08" />
              <stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
            </linearGradient>
          </defs>
          <line x1="18%" y1="-10%" x2="10%" y2="110%" stroke="url(#livemcqStreak)" strokeWidth="1.5" />
          <line x1="38%" y1="-10%" x2="26%" y2="110%" stroke="url(#livemcqStreak)" strokeWidth="2.5" />
          <line x1="56%" y1="-10%" x2="44%" y2="110%" stroke="url(#livemcqStreak)" strokeWidth="1.8" />
          <line x1="78%" y1="-10%" x2="65%" y2="110%" stroke="url(#livemcqStreak)" strokeWidth="2.2" />
          <line x1="92%" y1="-10%" x2="80%" y2="110%" stroke="url(#livemcqStreak)" strokeWidth="1.2" />
        </svg>

        {/* Scattered Warm Golden Stardust Embers */}
        <div className="absolute top-16 left-[12%] w-1.5 h-1.5 rounded-full bg-amber-400/50 blur-[0.5px] animate-pulse" />
        <div className="absolute top-28 left-[24%] w-1 h-1 rounded-full bg-amber-300/40 blur-[0.3px]" />
        <div className="absolute top-44 left-[8%] w-2 h-2 rounded-full bg-amber-400/40 blur-[0.7px]" />
        <div className="absolute top-20 right-[15%] w-1.5 h-1.5 rounded-full bg-amber-300/60 blur-[0.5px] animate-pulse" />
        <div className="absolute top-36 right-[28%] w-1 h-1 rounded-full bg-amber-400/40 blur-[0.3px]" />
        <div className="absolute top-52 right-[10%] w-2 h-2 rounded-full bg-amber-400/40 blur-[0.7px]" />
        <div className="absolute bottom-24 left-[20%] w-1.5 h-1.5 rounded-full bg-amber-400/40 blur-[0.5px]" />
        <div className="absolute bottom-32 right-[22%] w-1.5 h-1.5 rounded-full bg-amber-300/50 blur-[0.5px]" />
      </div>

      {/* 2. Floating Peripheral Track Badges & Academic Motifs */}
      <div className="absolute inset-0 pointer-events-none select-none max-w-7xl mx-auto px-4 overflow-hidden" aria-hidden="true">
        
        {/* Floating 3D Graduation Cap (Upper Left) */}
        <div className="absolute top-8 left-4 sm:left-12 lg:left-16 transform -rotate-12 opacity-85">
          <svg width="72" height="72" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            {/* Cap Diamond Top */}
            <polygon points="50,15 90,32 50,49 10,32" fill="#F59E0B" opacity="0.95" />
            <polygon points="50,18 86,32 50,46 14,32" fill="#D97706" />
            {/* Skullcap / Base */}
            <path d="M26,38 L26,58 C26,68 74,68 74,58 L74,38" fill="#B45309" opacity="0.9" />
            {/* Button */}
            <circle cx="50" cy="32" r="3.5" fill="#FEF3C7" />
            {/* Tassel Cord & Brush */}
            <path d="M50,32 Q68,40 76,54" stroke="#FEF3C7" strokeWidth="2.5" fill="none" strokeLinecap="round" />
            <circle cx="76" cy="54" r="2.5" fill="#FDE68A" />
            <path d="M74,54 L72,70 L80,70 L78,54 Z" fill="#FDE68A" />
          </svg>
        </div>

        {/* Floating Track Pill: BCS (Left) */}
        <div className="absolute top-36 left-2 sm:left-8 lg:left-12 hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#1C1738]/80 border border-purple-400/40 text-purple-200 text-xs font-bold shadow-[0_0_20px_rgba(168,85,247,0.3)] backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-purple-400 inline-block" />
          <span>BCS</span>
        </div>

        {/* Floating Track Pill: NTRCA (Lower Left) */}
        <div className="absolute bottom-40 left-4 sm:left-10 lg:left-16 hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#1C1738]/80 border border-purple-400/40 text-purple-200 text-xs font-bold shadow-[0_0_20px_rgba(168,85,247,0.3)] backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-purple-400 inline-block" />
          <span>NTRCA</span>
        </div>

        {/* Open Book Motif (Lower Left) */}
        <div className="absolute bottom-12 left-6 sm:left-16 lg:left-24 transform -rotate-6 opacity-35">
          <svg width="60" height="48" viewBox="0 0 60 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M6 38C14 36 24 37 30 42C36 37 46 36 54 38V10C46 8 36 9 30 14C24 9 14 8 6 10V38Z" stroke="#F59E0B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M30 14V42" stroke="#F59E0B" strokeWidth="2" strokeLinecap="round" />
            <line x1="12" y1="18" x2="24" y2="18" stroke="#F59E0B" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="12" y1="24" x2="22" y2="24" stroke="#F59E0B" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="36" y1="18" x2="48" y2="18" stroke="#F59E0B" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="38" y1="24" x2="48" y2="24" stroke="#F59E0B" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </div>

        {/* Floating Track Pill: Primary (Top Right) */}
        <div className="absolute top-20 right-4 sm:right-12 lg:right-24 hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#0F2642]/80 border border-sky-400/40 text-sky-200 text-xs font-bold shadow-[0_0_20px_rgba(56,189,248,0.3)] backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-sky-400 inline-block" />
          <span>Primary</span>
        </div>

        {/* Floating Track Pill: Bank (Middle Right) */}
        <div className="absolute top-44 right-2 sm:right-6 lg:right-12 hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#0E322D]/80 border border-emerald-400/40 text-emerald-200 text-xs font-bold shadow-[0_0_20px_rgba(52,211,153,0.3)] backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block" />
          <span>Bank</span>
        </div>

        {/* Floating Track Pill: BJS (Lower Right) */}
        <div className="absolute bottom-44 right-4 sm:right-10 lg:right-16 hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#322710]/80 border border-amber-400/40 text-amber-200 text-xs font-bold shadow-[0_0_20px_rgba(251,191,36,0.3)] backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-amber-400 inline-block" />
          <span>BJS</span>
        </div>

        {/* Tilted Pencil Motif (Lower Right) */}
        <div className="absolute bottom-10 right-6 sm:right-16 lg:right-28 transform rotate-45 opacity-35">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 40L14 38L36 16L30 10L8 32L8 40Z" stroke="#F59E0B" strokeWidth="2" strokeLinejoin="round" />
            <path d="M30 10L36 16" stroke="#F59E0B" strokeWidth="2" />
            <path d="M8 40L12 34" stroke="#F59E0B" strokeWidth="2" />
          </svg>
        </div>

      </div>

      {/* 3. Central Hero Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
        
        {/* Top Capsule Badge: সঠিক প্রস্তুতি, সহজ প্রিলি */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#161C3D]/90 border border-indigo-400/30 text-indigo-200 text-xs font-medium backdrop-blur-sm shadow-md">
          <span className="w-2 h-2 rounded-full bg-indigo-400 inline-block animate-pulse" />
          <span className="font-bengali">সঠিক প্রস্তুতি, সহজ প্রিলি</span>
        </div>

        {/* Majestic Dual-Line Headline */}
        <div className="space-y-1">
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black text-white font-serif tracking-tight leading-[1.25]">
            ঘরে বসেই সকল প্রতিযোগিতামূলক
          </h1>
          <h2 className="text-3xl sm:text-5xl lg:text-6xl font-black font-serif tracking-tight leading-[1.25] bg-gradient-to-r from-[#FF5722] via-[#FF8A00] to-[#FFA000] bg-clip-text text-transparent">
            চাকরির পূর্ণাঙ্গ প্রস্তুতি
          </h2>
        </div>

        {/* Explanatory Subtitle with Highlighted 24 Lakh+ Tag */}
        <p className="text-xs sm:text-sm lg:text-base text-slate-300 font-bengali leading-relaxed max-w-3xl mx-auto">
          বিসিএস, ব্যাংক, প্রাইমারি, NTRCA, ৯ম-২০তম গ্রেড, বার কাউন্সিল, বিজেএস-সহ সকল
          প্রতিযোগিতামূলক পরীক্ষার প্রস্তুতিতে ২০১৭ সাল থেকে দেশের প্রথম ও সর্ববৃহৎ প্ল্যাটফর্ম Live MCQ™
          এখন <span className="inline-block px-2.5 py-0.5 rounded-md bg-[#182348] border border-white/20 text-white font-bold text-xs sm:text-sm shadow-inner">২৪ লাখ+</span> চাকরিপ্রার্থীর আস্থার নাম।
        </p>

        {/* Dual Primary Action CTA Pill Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          
          {/* Button 1: Left Cyan-to-Cobalt Gradient Pill */}
          <Link
            href="/practice?challenge=active"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-full bg-gradient-to-r from-[#0284C7] via-[#0284C7] to-[#2563EB] hover:from-[#0369A1] hover:to-[#1D4ED8] text-white font-bold font-bengali text-sm shadow-[0_6px_25px_rgba(2,132,199,0.35)] transition-all transform active:scale-95"
          >
            <GraduationCap className="w-4 h-4 text-white" />
            <span>৪৫তম স্পেশাল বিসিএস</span>
          </Link>

          {/* Button 2: Right Orange-to-Coral Gradient Pill */}
          <Link
            href="/practice?challenge=active"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-full bg-gradient-to-r from-[#E65100] via-[#F57C00] to-[#FF9800] hover:from-[#BF360C] hover:to-[#E65100] text-white font-bold font-bengali text-sm shadow-[0_6px_25px_rgba(245,124,0,0.35)] transition-all transform active:scale-95"
          >
            <FileEdit className="w-4 h-4 text-white" />
            <span>পরীক্ষা দিন</span>
          </Link>

        </div>

        {/* Integrated Active Live Exam Room Bar (Zero Regression on Countdown & Rules) */}
        <div className="flex flex-wrap items-center justify-center gap-3 pt-1">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#0D1535]/90 border border-amber-400/30 text-xs font-mono font-bold text-amber-300 shadow-inner">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>সার্ভার-অথরিটেটিভ টাইমার: {formatTimer(timeRemainingSeconds || 1200)}</span>
            <span className="text-slate-500">•</span>
            <span className="text-rose-300">নেগেটিভ: -০.২৫</span>
          </div>

          <button
            type="button"
            onClick={onOpenRulesModal}
            className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-bold text-slate-300 transition"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>পরীক্ষার নিয়মাবলী</span>
          </button>
        </div>

        {/* Platform App Store Row: অ্যাপ ইনস্টল করুন */}
        <div className="pt-4 space-y-3">
          <span className="text-[#FF8A00] font-bold text-xs uppercase tracking-wider font-bengali block">
            অ্যাপ ইনস্টল করুন
          </span>

          <div className="flex items-center justify-center gap-4 text-white">
            {/* Google Play */}
            <a
              href="https://play.google.com"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Google Play Store"
              className="p-2 rounded-xl bg-white/5 hover:bg-white/15 border border-white/10 transition transform hover:-translate-y-0.5"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
                <path d="M3.6 1.8L13.8 12L3.6 22.2C3.3 22 3 21.6 3 21V3C3 2.4 3.3 2 3.6 1.8Z" fill="#2196F3" />
                <path d="M17.3 8.5L13.8 12L17.3 15.5L20.8 13.5C21.7 13 21.7 12 20.8 11.5L17.3 8.5Z" fill="#FFC107" />
                <path d="M13.8 12L3.6 1.8C4 1.5 4.5 1.5 5 1.8L17.3 8.5L13.8 12Z" fill="#4CAF50" />
                <path d="M13.8 12L17.3 15.5L5 22.2C4.5 22.5 4 22.5 3.6 22.2L13.8 12Z" fill="#F44336" />
              </svg>
            </a>

            {/* Apple App Store */}
            <a
              href="https://apple.com/app-store"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Apple App Store"
              className="p-2 rounded-xl bg-white/5 hover:bg-white/15 border border-white/10 transition transform hover:-translate-y-0.5"
            >
              <svg className="w-5 h-5 fill-current text-white" viewBox="0 0 24 24">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.63-.77 1.06-1.85.94-2.93-.93.04-2.07.62-2.73 1.39-.58.67-1.09 1.76-.95 2.82 1.05.08 2.11-.51 2.74-1.28" />
              </svg>
            </a>

            {/* Windows Store */}
            <a
              href="https://microsoft.com/store"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Windows Store"
              className="p-2 rounded-xl bg-white/5 hover:bg-white/15 border border-white/10 transition transform hover:-translate-y-0.5"
            >
              <svg className="w-5 h-5 fill-[#00ADEF]" viewBox="0 0 24 24">
                <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.951-1.751" />
              </svg>
            </a>

            {/* macOS / Mac */}
            <a
              href="https://apple.com/macos"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="macOS App"
              className="p-2 rounded-xl bg-white/5 hover:bg-white/15 border border-white/10 transition transform hover:-translate-y-0.5"
            >
              <svg className="w-5 h-5 fill-current text-[#38BDF8]" viewBox="0 0 24 24">
                <path d="M21 4H3C1.9 4 1 4.9 1 6V18C1 19.1 1.9 20 3 20H21C22.1 20 23 19.1 23 18V6C23 4.9 22.1 4 21 4ZM7.5 9C8.33 9 9 9.67 9 10.5C9 11.33 8.33 12 7.5 12C6.67 12 6 11.33 6 10.5C6 9.67 6.67 9 7.5 9ZM16.5 9C17.33 9 18 9.67 18 10.5C18 11.33 17.33 12 16.5 12C15.67 12 15 11.33 15 10.5C15 9.67 15.67 9 16.5 9ZM16 15.5C15.17 16.43 13.72 17 12 17C10.28 17 8.83 16.43 8 15.5L9.5 14C9.9 14.5 10.84 15 12 15C13.16 15 14.1 14.5 14.5 14L16 15.5Z" />
              </svg>
            </a>

            {/* Web Browser Access */}
            <a
              href="#demo-exam"
              aria-label="Web Browser Platform"
              className="p-2 rounded-xl bg-white/5 hover:bg-white/15 border border-white/10 transition transform hover:-translate-y-0.5 flex items-center justify-center text-sky-400"
            >
              <div className="relative">
                <Globe className="w-5 h-5 text-sky-400" />
                <MousePointer className="w-3 h-3 text-white absolute -bottom-1 -right-1" />
              </div>
            </a>
          </div>
        </div>

        {/* 4. Bottom Docked Frosted Glass KPI Container */}
        <div className="pt-4">
          <div className="rounded-3xl bg-[#0D1535]/85 backdrop-blur-xl border border-white/10 shadow-[0_12px_40px_rgba(0,0,0,0.5)] p-6 sm:p-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-white/5">
              
              {/* Metric 1: অ্যাপ ব্যবহারকারী */}
              <div className="space-y-2 pt-4 md:pt-0">
                <div className="w-10 h-10 rounded-full bg-amber-500/10 border border-amber-400/30 flex items-center justify-center mx-auto text-amber-400 shadow-sm">
                  <Users className="w-5 h-5 text-amber-400" />
                </div>
                <div className="text-2xl sm:text-3xl font-black font-mono text-[#FFB300] tracking-tight">
                  ২৪ লাখ+
                </div>
                <div className="text-xs text-slate-300 font-bengali">
                  অ্যাপ ব্যবহারকারী
                </div>
              </div>

              {/* Metric 2: আর্কাইভ MCQ */}
              <div className="space-y-2 pt-4 md:pt-0 md:pl-6">
                <div className="w-10 h-10 rounded-full bg-amber-500/10 border border-amber-400/30 flex items-center justify-center mx-auto text-amber-400 shadow-sm">
                  <FileText className="w-5 h-5 text-amber-400" />
                </div>
                <div className="text-2xl sm:text-3xl font-black font-mono text-[#FFB300] tracking-tight">
                  ৭.৫ লাখ+
                </div>
                <div className="text-xs text-slate-300 font-bengali">
                  আর্কাইভ MCQ (reference-সহ ব্যাখ্যা)
                </div>
              </div>

              {/* Metric 3: প্রতিদিন গড় ব্যবহারকারী */}
              <div className="space-y-2 pt-4 md:pt-0 md:pl-6">
                <div className="w-10 h-10 rounded-full bg-amber-500/10 border border-amber-400/30 flex items-center justify-center mx-auto text-amber-400 shadow-sm">
                  <Users className="w-5 h-5 text-amber-400" />
                </div>
                <div className="text-2xl sm:text-3xl font-black font-mono text-[#FFB300] tracking-tight">
                  ৩০ হাজার+
                </div>
                <div className="text-xs text-slate-300 font-bengali">
                  প্রতিদিন গড় ব্যবহারকারী
                </div>
              </div>

              {/* Metric 4: বছরের অভিজ্ঞতা */}
              <div className="space-y-2 pt-4 md:pt-0 md:pl-6">
                <div className="w-10 h-10 rounded-full bg-amber-500/10 border border-amber-400/30 flex items-center justify-center mx-auto text-amber-400 shadow-sm">
                  <Award className="w-5 h-5 text-amber-400" />
                </div>
                <div className="text-2xl sm:text-3xl font-black font-mono text-[#FFB300] tracking-tight">
                  ১০+
                </div>
                <div className="text-xs text-slate-300 font-bengali">
                  বছরের অভিজ্ঞতা
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>

    </section>
  );
}
