/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Student Learning Dashboard & Personal Command Center
 * TOPIC:     Phase 138 Unified Premium Design System & Sub-pages Elevation
 * FILE:      frontend/src/pages/dashboard.tsx
 * PHASE:     Phase 123 & Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Standardized academic student dashboard with 3D tactile physics,
 *            Oxford Academic Navy palette, and unified design system tokens.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Flame,
  CheckCircle2,
  Target,
  Award,
  ArrowRight,
  BookOpen,
  Compass,
  Trophy,
  Users,
  Sparkles,
  Layers,
  ExternalLink,
  X,
  Play,
  Calendar,
  ChevronRight,
  Atom,
  Crosshair,
  AlertTriangle
} from 'lucide-react';
import { AppHead, createOrganizationSchema } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { ProofOfSkillCard, SocialShareButtons, CertificateData } from '@/components/certificate';
import { PhysicsProjectileLab, ChemistryMolecularViewer } from '@/components/stem-labs';
import { useTranslation, toBengaliDigits } from '@/lib/i18n';
import { Academic3DToggle, LazyAcademic3DScene } from '@/components/3d';

// Sample verified certificate data for W3C showcase
const SAMPLE_CERTIFICATE: CertificateData = {
  cert_id: 'OGRO-2026-F982A1B4',
  student_id: 'std_demo_7721',
  student_name: 'তানজিম হাসান (Tanzim Hasan)',
  course_title: 'উচ্চ মাধ্যমিক পদার্থবিজ্ঞান ও অ্যাডভান্সড ক্যালকুলাস',
  percentile_rank: 98.4,
  score: 98.4,
  total_score: 100,
  issue_date: '২০২৬-০৩-১৫',
  verified_skills: [
    'নিউটনিয়ান বলবিদ্যা',
    'স্থির তড়িৎ ও গতিবিদ্যা',
    'ক্যালকুলাস ডেরিভেটিভ ও ইন্টিগ্রেশন',
    'গাণিতিক মডেলিং'
  ],
  issuer_name: 'অগ্রযাত্রা জাতীয় মূল্যায়ন বোর্ড',
  institution: 'ঢাকা কলেজ / রাজশাহী কলেজ',
  signature: '3f7a8b9c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a',
  qr_url: 'https://ogrojatra.edu.bd/verify/OGRO-2026-F982A1B4',
  is_valid: true
};

export default function StudentDashboardPage() {
  const { isBengali, t } = useTranslation();

  // Academic stage chip filter state
  const [selectedStage, setSelectedStage] = useState<'ssc' | 'hsc' | 'admission' | 'career'>('hsc');

  // Interactive 3D STEM Lab modal state
  const [activeLabModal, setActiveLabModal] = useState<'physics' | 'chemistry' | 'astronomy' | null>(null);

  // Active lab tab preview state
  const [activeLabTab, setActiveLabTab] = useState<'physics' | 'chemistry'>('physics');

  // Live Challenge Countdown timer state
  const [countdown, setCountdown] = useState({ hours: 1, minutes: 24, seconds: 45 });

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev.seconds > 0) {
          return { ...prev, seconds: prev.seconds - 1 };
        } else if (prev.minutes > 0) {
          return { ...prev, minutes: 59, seconds: 59 };
        } else if (prev.hours > 0) {
          return { hours: prev.hours - 1, minutes: 59, seconds: 59 };
        }
        return { hours: 0, minutes: 0, seconds: 0 };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <>
      <AppHead
        title={isBengali ? "শিক্ষার্থী ড্যাশবোর্ড | অগ্রযাত্রা" : "Student Dashboard | Agragoti"}
        description={
          isBengali
            ? "আপনার সাপ্তাহিক অধ্যয়ন লক্ষ্য, জাতীয় অলিম্পিয়াড প্রস্তুতি ও ব্যক্তিগত প্রগ্রেস ট্র্যাকার।"
            : "Your weekly study goals, national Olympiad preparation, and personal progress tracker."
        }
        canonicalUrl="/dashboard"
        ogType="website"
        structuredData={createOrganizationSchema()}
      />

      <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans selection:bg-[#0A2540] selection:text-white transition-colors duration-200">
        <Navbar currentStage={isBengali ? "এইচএসসি বিজ্ঞান (HSC Science)" : "HSC Science"} />

        <main className="flex-1 w-full pb-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-10 space-y-8 sm:space-y-10">

            {/* Breadcrumb & Greeting */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-bengali">
                  {isBengali ? "ব্যক্তিগত শিক্ষার্থী ড্যাশবোর্ড" : "Personal Student Dashboard"}
                </span>
                <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight font-bengali">
                  {isBengali ? "স্বাগতম, তানজিম হাসান" : "Welcome, Tanzim Hasan"}
                </h1>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <Academic3DToggle />
                <Link
                  href="/learn"
                  className="btn-3d-oxford px-5 py-2.5 rounded-2xl bg-[#0A2540] text-white text-xs font-semibold hover:bg-[#0E3357] transition shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none font-bengali"
                >
                  {isBengali ? "আজকের পাঠে যান" : "Go to Today's Lesson"}
                </Link>
                <Link
                  href="/practice"
                  className="btn-paper-outline px-5 py-2.5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs font-semibold text-slate-800 dark:text-slate-200 hover:bg-slate-50 transition shadow-sm active:translate-y-0.5 font-bengali"
                >
                  {isBengali ? "কুইজ প্র্যাকটিস" : "Quiz Practice"}
                </Link>
              </div>
            </div>

            {/* TIER 1: ASYMMETRICAL BENTO HERO & REAL-TIME LIVE RADAR */}
            <div className="grid grid-cols-12 gap-6 lg:gap-8 items-stretch">
              
              {/* PRIMARY BENTO HERO CARD */}
              <div className="col-span-12 lg:col-span-8 p-6 sm:p-8 lg:p-10 rounded-3xl bg-white dark:bg-slate-900/90 border border-slate-200/70 dark:border-slate-800/80 shadow-ambient dark:shadow-ambient-lg relative overflow-hidden flex flex-col justify-between">
                <div className="relative z-10 space-y-6">
                  
                  {/* Accreditation & Standard Badges */}
                  <div className="flex flex-wrap items-center gap-2.5">
                    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 dark:bg-slate-800/80 border border-slate-200/80 dark:border-slate-700/80 text-xs font-semibold text-slate-700 dark:text-slate-300 font-bengali">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                      <span>{isBengali ? "এনসিটিবি ২০২৬ মানদণ্ড • সক্রিয় শিক্ষণ সেশন" : "NCTB 2026 Standards • Active Learning Session"}</span>
                    </div>

                    <Link
                      href="/modules"
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 text-xs font-bold text-blue-700 dark:text-blue-300 hover:bg-blue-100 transition font-bengali"
                    >
                      <Layers className="w-3.5 h-3.5" />
                      <span>{isBengali ? "মডিউল ডিরেক্টরি" : "Module Directory"}</span>
                    </Link>
                  </div>

                  {/* Goal Prompt */}
                  <div className="space-y-3 max-w-2xl">
                    <h2 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white font-bengali">
                      {isBengali ? "আজকে তোমার লক্ষ্য কতটুকু এগোলো?" : "How far did your goals advance today?"}
                    </h2>
                    <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
                      {isBengali
                        ? "তোমার এইচএসসি পদার্থবিজ্ঞান ও উচ্চতর গণিতের অধ্যয়ন পরিকল্পনা নির্ধারিত সময় অনুযায়ী চলমান রয়েছে।"
                        : "Your HSC Physics and Higher Mathematics study plan is currently on track according to schedule."}
                    </p>
                  </div>

                  {/* Stage Selector Pills */}
                  <div>
                    <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 font-bengali">
                      {isBengali ? "বর্তমান কারিকুলাম লেভেল:" : "Current Curriculum Level:"}
                    </div>
                    <div className="flex flex-wrap items-center gap-2 sm:gap-3">
                      <button
                        type="button"
                        onClick={() => setSelectedStage('ssc')}
                        className={`px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-semibold font-bengali min-h-[44px] flex items-center gap-2 transition cursor-pointer ${
                          selectedStage === 'ssc'
                            ? 'bg-[#0A2540] text-white shadow-[0_3px_0_0_#051329]'
                            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <BookOpen className="w-4 h-4" />
                        <span>{isBengali ? "মাধ্যমিক (SSC ৯-১০)" : "Secondary (SSC 9-10)"}</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => setSelectedStage('hsc')}
                        className={`px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-semibold font-bengali min-h-[44px] flex items-center gap-2 transition cursor-pointer ${
                          selectedStage === 'hsc'
                            ? 'bg-[#0A2540] text-white shadow-[0_3px_0_0_#051329]'
                            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <Layers className="w-4 h-4" />
                        <span>{isBengali ? "উচ্চ মাধ্যমিক (HSC ১১-১২)" : "Higher Secondary (HSC 11-12)"}</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => setSelectedStage('admission')}
                        className={`px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-semibold font-bengali min-h-[44px] flex items-center gap-2 transition cursor-pointer ${
                          selectedStage === 'admission'
                            ? 'bg-[#0A2540] text-white shadow-[0_3px_0_0_#051329]'
                            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <Target className="w-4 h-4" />
                        <span>{isBengali ? "বিশ্ববিদ্যালয় ভর্তি (Admission)" : "University Admission"}</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => setSelectedStage('career')}
                        className={`px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-semibold font-bengali min-h-[44px] flex items-center gap-2 transition cursor-pointer ${
                          selectedStage === 'career'
                            ? 'bg-[#0A2540] text-white shadow-[0_3px_0_0_#051329]'
                            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <Users className="w-4 h-4" />
                        <span>{isBengali ? "টিউশন ও ক্যারিয়ার (Career)" : "Tuition & Career"}</span>
                      </button>
                    </div>
                  </div>

                </div>

                {/* Bottom Row: Goal Progress Ring & Quick Resume */}
                <div className="relative z-10 mt-8 pt-6 border-t border-slate-200/70 dark:border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-6">
                  
                  <div className="flex items-center gap-4 w-full sm:w-auto">
                    <div className="relative w-16 h-16 shrink-0 flex items-center justify-center">
                      <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 80 80">
                        <circle
                          cx="40"
                          cy="40"
                          r="32"
                          stroke="currentColor"
                          strokeWidth="6"
                          className="text-slate-100 dark:text-slate-800"
                          fill="transparent"
                        />
                        <circle
                          cx="40"
                          cy="40"
                          r="32"
                          stroke="currentColor"
                          strokeWidth="6"
                          className="text-blue-600 dark:text-blue-500"
                          fill="transparent"
                          strokeDasharray="201.06"
                          strokeDashoffset="64.34"
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                        <span className="text-xs font-mono font-bold text-slate-900 dark:text-white leading-none">
                          {isBengali ? "৬৮%" : "68%"}
                        </span>
                      </div>
                    </div>

                    <div className="space-y-0.5">
                      <span className="text-xs font-bold text-slate-900 dark:text-white block font-bengali">
                        {isBengali ? "সাপ্তাহিক শিখন লক্ষ্যমাত্রা" : "Weekly Learning Target"}
                      </span>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 font-bengali">
                        {isBengali
                          ? "১২/১৮টি অধ্যায় সম্পন্ন • আজ আর মাত্র ২টি কুইজ বাকি"
                          : "12/18 Chapters Completed • Only 2 Quizzes Remaining Today"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
                    <Link
                      href="/practice"
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-2xl bg-[#0A2540] hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none text-white font-semibold font-bengali text-sm min-h-[48px] transition-all"
                    >
                      <span>{isBengali ? "পড়াশোনা শুরু করুন (Quick Resume)" : "Start Learning (Quick Resume)"}</span>
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>

                </div>

              </div>

              {/* REAL-TIME LIVE CHALLENGE RADAR CARD */}
              <div className="col-span-12 lg:col-span-4 p-6 sm:p-8 rounded-3xl bg-[#0F172A] text-white border border-slate-800/80 shadow-ambient-lg relative overflow-hidden flex flex-col justify-between">
                <div className="relative z-10 space-y-4">
                  
                  <div className="flex items-center justify-between">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-xs font-semibold text-amber-400">
                      <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                      </span>
                      <span>{isBengali ? "আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড" : "Tonight's 8:00 PM National Olympiad"}</span>
                    </div>

                    <Trophy className="w-5 h-5 text-amber-400 shrink-0" />
                  </div>

                  <div>
                    <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight leading-tight font-bengali">
                      {isBengali ? "জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬" : "National Live Quiz Competition 2026"}
                    </h2>
                    <p className="text-xs text-slate-300 mt-2 leading-relaxed font-bengali">
                      {isBengali
                        ? "বাংলাদেশব্যাপী শিক্ষার্থীদের সঙ্গে রিয়েল-টাইম মেধার লড়াই। নেগেটিভ মার্কিং সহ লাইভ লিডারবোর্ড।"
                        : "Real-time intellectual contest with students across Bangladesh. Live leaderboard with negative marking."}
                    </p>
                  </div>

                  {/* Countdown Timer */}
                  <div className="pt-2">
                    <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2">
                      {isBengali ? "প্রতিযোগিতা শুরু হতে বাকি:" : "Competition starts in:"}
                    </div>

                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div className="p-3 rounded-2xl bg-slate-950/90 border border-slate-800/80">
                        <span className="text-2xl sm:text-3xl font-mono font-black text-white tabular-nums">
                          {isBengali ? toBengaliDigits(String(countdown.hours).padStart(2, '0')) : String(countdown.hours).padStart(2, '0')}
                        </span>
                        <span className="block text-[10px] text-slate-400 uppercase font-bold mt-0.5 font-bengali">{isBengali ? "ঘণ্টা" : "Hours"}</span>
                      </div>

                      <div className="p-3 rounded-2xl bg-slate-950/90 border border-slate-800/80">
                        <span className="text-2xl sm:text-3xl font-mono font-black text-amber-400 tabular-nums">
                          {isBengali ? toBengaliDigits(String(countdown.minutes).padStart(2, '0')) : String(countdown.minutes).padStart(2, '0')}
                        </span>
                        <span className="block text-[10px] text-slate-400 uppercase font-bold mt-0.5 font-bengali">{isBengali ? "মিনিট" : "Minutes"}</span>
                      </div>

                      <div className="p-3 rounded-2xl bg-slate-950/90 border border-slate-800/80">
                        <span className="text-2xl sm:text-3xl font-mono font-black text-teal-400 tabular-nums">
                          {isBengali ? toBengaliDigits(String(countdown.seconds).padStart(2, '0')) : String(countdown.seconds).padStart(2, '0')}
                        </span>
                        <span className="block text-[10px] text-slate-400 uppercase font-bold mt-0.5 font-bengali">{isBengali ? "সেকেন্ড" : "Seconds"}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-xs font-medium text-emerald-400 pt-1">
                    <Users className="w-4 h-4 shrink-0" />
                    <span>{isBengali ? "৪,৮৫০+ প্রতিযোগী শিক্ষার্থী লবিতে যুক্ত হয়েছে" : "4,850+ Competitor Students Joined in Lobby"}</span>
                  </div>

                </div>

                <div className="relative z-10 pt-6 mt-4 border-t border-slate-800/80">
                  <Link
                    href="/live-challenge"
                    className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-[#B45309] hover:bg-[#D97706] shadow-[0_4px_0_0_#78350F] active:translate-y-1 active:shadow-none text-white font-bold font-bengali text-sm min-h-[48px] transition-all"
                  >
                    <Trophy className="w-4 h-4 text-amber-200" />
                    <span>{isBengali ? "লাইভ লবিতে যোগ দিন" : "Join Live Lobby"}</span>
                  </Link>
                </div>

              </div>

            </div>

            {/* TIER 2: 4-TIER METRIC PILL RIBBON */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
              
              <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/70 dark:border-slate-800/80 shadow-ambient">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    {isBengali ? "অধ্যয়ন স্ট্রিক" : "Study Streak"}
                  </span>
                  <div className="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center border border-amber-500/20">
                    <Flame className="w-5 h-5" />
                  </div>
                </div>
                <div className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight mb-1">
                  {isBengali ? "৭ দিনের স্ট্রিক" : "7-Day Streak"}
                </div>
                <p className="text-xs text-amber-600 dark:text-amber-400 font-medium">
                  {isBengali ? "টানা ৭ দিন শেখার ধারাবাহিকতা" : "7 Consecutive Days of Consistent Learning"}
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/70 dark:border-slate-800/80 shadow-ambient">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    {isBengali ? "সমাধানকৃত প্রশ্ন" : "Solved Questions"}
                  </span>
                  <div className="w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center border border-emerald-500/20">
                    <CheckCircle2 className="w-5 h-5" />
                  </div>
                </div>
                <div className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight mb-1">
                  {isBengali ? "১২৮টি প্রশ্ন সমাধান" : "128 Questions Solved"}
                </div>
                <p className="text-xs text-slate-500">
                  {isBengali ? "পদার্থবিজ্ঞান ও উচ্চতর গণিত" : "Physics & Higher Mathematics"}
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/70 dark:border-slate-800/80 shadow-ambient">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    {isBengali ? "নির্ভুলতা হার" : "Accuracy Rate"}
                  </span>
                  <div className="w-9 h-9 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center border border-blue-500/20">
                    <Target className="w-5 h-5" />
                  </div>
                </div>
                <div className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight mb-1">
                  {isBengali ? "৮৬.৪% নির্ভুলতা" : "86.4% Accuracy"}
                </div>
                <p className="text-xs text-slate-500">
                  {isBengali ? "সাপ্তাহিক প্রবৃদ্ধি +৪.২%" : "Weekly Growth +4.2%"}
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/70 dark:border-slate-800/80 shadow-ambient">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    {isBengali ? "জাতীয় পার্সেন্টাইল" : "National Percentile"}
                  </span>
                  <div className="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center border border-amber-500/20">
                    <Award className="w-5 h-5" />
                  </div>
                </div>
                <div className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight mb-1">
                  {isBengali ? "শীর্ষ ৫% শিক্ষার্থী" : "Top 5% Students"}
                </div>
                <p className="text-xs text-slate-500">
                  {isBengali ? "৯৫.২তম পার্সেন্টাইল" : "95.2th Percentile"}
                </p>
              </div>

            </div>

            {/* TIER 3: STEM VIRTUAL LABS */}
            <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/70 dark:border-slate-800/80 shadow-ambient flex flex-col sm:flex-row items-center justify-between gap-6">
              <div className="space-y-2">
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-teal-50 dark:bg-teal-950/60 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-800">
                  <Atom className="w-4 h-4 text-teal-600" />
                  <span>{isBengali ? "৩ডি স্টেম ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি" : "3D STEM Virtual Science Laboratory"}</span>
                </div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                  {isBengali ? "ইন্টারেক্টিভ পদার্থ, রসায়ন ও জ্যোতির্বিদ্যা সিমুলেশন" : "Interactive Physics, Chemistry & Astronomy Simulation"}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  {isBengali ? "প্রক্ষেপক গতি, ত্রিমাত্রিক আণবিক মডেল ও জ্যোতির্বৈজ্ঞানিক গ্লোব সরাসরি ব্রাউজারে এক্সপ্লোর করুন।" : "Explore projectile motion, 3D molecular models and celestial globe directly in your browser."}
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={() => setActiveLabModal('physics')}
                  className="px-5 py-3 rounded-2xl bg-[#065F46] hover:bg-[#087858] text-white font-bold text-xs shadow-[0_3px_0_0_#044332] active:translate-y-0.5 transition"
                >
                  {isBengali ? "পদার্থবিজ্ঞান ল্যাব" : "Physics Lab"}
                </button>
                <button
                  type="button"
                  onClick={() => setActiveLabModal('chemistry')}
                  className="px-5 py-3 rounded-2xl bg-[#0A2540] hover:bg-[#0E3357] text-white font-bold text-xs shadow-[0_3px_0_0_#051329] active:translate-y-0.5 transition"
                >
                  {isBengali ? "রসায়ন আণবিক ল্যাব" : "Chemistry Molecular Lab"}
                </button>
                <button
                  type="button"
                  onClick={() => setActiveLabModal('astronomy')}
                  className="px-5 py-3 rounded-2xl bg-[#1E293B] hover:bg-[#334155] text-white font-bold text-xs shadow-[0_3px_0_0_#0F172A] active:translate-y-0.5 transition flex items-center gap-2"
                >
                  <Compass className="w-4 h-4 text-sky-400" />
                  <span>{isBengali ? "জ্যোতির্বিদ্যা ল্যাব (3D)" : "Astronomy Lab (3D)"}</span>
                </button>
              </div>
            </div>

          </div>
        </main>

        <Footer />
      </div>

      {/* Interactive 3D STEM Lab Modals */}
      {activeLabModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 animate-in fade-in"
        >
          <div className="relative w-full max-w-5xl bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60">
              <div className="flex items-center gap-2">
                <Atom className="w-5 h-5 text-teal-400" />
                <span className="font-bold text-white text-sm sm:text-base font-bengali">
                  {activeLabModal === 'physics'
                    ? (isBengali ? 'প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Physics Projectile Lab)' : 'Physics Projectile Motion Simulator (Physics Projectile Lab)')
                    : activeLabModal === 'chemistry'
                    ? (isBengali ? '৩ডি আণবিক জ্যামিতি ল্যাবরেটরি (Chemistry Molecular Viewer)' : '3D Molecular Geometry Laboratory (Chemistry Molecular Viewer)')
                    : (isBengali ? '৩ডি স্কলার গ্লোব ও জ্যোতির্বিদ্যা ল্যাব (Scholar Celestial Globe Lab)' : '3D Scholar Globe & Astronomy Lab (Scholar Celestial Globe Lab)')}
                </span>
              </div>

              <button
                type="button"
                onClick={() => setActiveLabModal(null)}
                aria-label={isBengali ? "ল্যাব বন্ধ করুন" : "Close Lab"}
                className="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 sm:p-6 overflow-y-auto flex-1">
              {activeLabModal === 'physics' ? (
                <PhysicsProjectileLab />
              ) : activeLabModal === 'chemistry' ? (
                <ChemistryMolecularViewer />
              ) : (
                <div className="flex flex-col items-center justify-center py-6 px-4 bg-slate-950/40 rounded-2xl border border-slate-800/80">
                  <div className="max-w-xl text-center space-y-2 mb-6">
                    <span className="text-[11px] font-mono uppercase tracking-widest text-teal-400 font-semibold">
                      {isBengali ? "একাডেমিক ৩ডি অবজারভেটরি" : "Academic 3D Observatory"}
                    </span>
                    <h4 className="text-lg font-bold text-white font-bengali">
                      {isBengali ? "অগ্রযাত্রা স্কলার আর্সিলারি স্ফিয়ার ও ভৌগোলিক অক্ষ" : "Agragoti Scholar Armillary Sphere & Terrestrial Axis"}
                    </h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      {isBengali ? "২৩.৫° অক্ষীয় হেলে থাকা সৌরক্রান্তীয় গোলক এবং বাংলাদেশের স্থানাঙ্ক (২৩.৬৮° উত্তর, ৯০.৩৫° পূর্ব) পর্যবেক্ষণ করুন। মাউস বা স্পর্শ দ্বারা ৩ডি কোণ পরিবর্তন করা যায়।" : "Observe the 23.5° axially tilted ecliptic sphere and coordinates of Bangladesh (23.68° N, 90.35° E). Rotate 3D perspectives using mouse or touch controls."}
                    </p>
                  </div>
                  <LazyAcademic3DScene size={320} showToggle={true} enableParallax={true} />
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
