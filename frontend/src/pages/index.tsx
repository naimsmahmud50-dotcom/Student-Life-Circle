/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Flagship Public Educational Portal & Unified Academic Command Surface
 * TOPIC:     Master Academic UI & Pro Tactile Button Elevation
 * FILE:      frontend/src/pages/index.tsx
 * PHASE:     Phase 110 - Pure Academic Visual Design Elevation & Phase 123 - Master Academic UI & Pro Tactile Button Elevation
 * PURPOSE:   Elevates every button, card, background, and header to Duolingo/Brilliant-grade
 *            3D physical press physics, Oxford Academic Navy palette, and zero AI vibe.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  GraduationCap,
  BookOpen,
  Award,
  ShieldCheck,
  Compass,
  ArrowRight,
  Layers,
  ChevronRight,
  Atom,
  Play,
  Sparkles,
  Users,
  Target,
  Trophy,
  CheckCircle2,
  Lock,
  ExternalLink,
  HelpCircle,
  FileText,
  X,
  Flame,
  Clock,
  Share2
} from 'lucide-react';
import { AppHead, createOrganizationSchema } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { ProofOfSkillCard, SocialShareButtons, CertificateData } from '@/components/certificate';
import { PhysicsProjectileLab, ChemistryMolecularViewer } from '@/components/stem-labs';
import { AcademicTelemetrySection } from '@/components/stats';
import { useTranslation } from '@/lib/i18n';

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

export default function FlagshipLandingPage() {
  const { isBengali, t } = useTranslation();

  // Active showcase stage
  const [activeStage, setActiveStage] = useState<'ssc' | 'hsc' | 'admission' | 'career'>('hsc');

  // Interactive 3D STEM Lab modal state
  const [activeLabModal, setActiveLabModal] = useState<'physics' | 'chemistry' | null>(null);

  // Active STEM tab in showcase
  const [activeStemTab, setActiveStemTab] = useState<'physics' | 'chemistry'>('physics');

  // Live Challenge Countdown timer state (hours, minutes, seconds)
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
        title="অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা - জাতীয় ডিজিটাল শিক্ষা প্ল্যাটফর্ম"
        description="এনসিটিবি পাঠ্যক্রম, বিগত ১০ বছরের বোর্ড প্রশ্ন ব্যাংক, ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাব এবং নিরপেক্ষ ডিজিটাল মূল্যায়ন প্ল্যাটফর্ম।"
        canonicalUrl="/"
        ogType="website"
        structuredData={createOrganizationSchema()}
      />

      <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans selection:bg-[#0A2540] selection:text-white transition-colors duration-200">
        <Navbar currentStage="জাতীয় পোর্টাল (National Portal)" />

        <main className="flex-1 w-full">

          {/* ===================================================================
              SECTION 1: FLAGSHIP EDITORIAL HERO (Prestigious, Spacious, Human)
              =================================================================== */}
          <section className="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28 border-b border-slate-200/80 dark:border-slate-800/80 bg-white dark:bg-slate-950">
            {/* Ambient Academic Parchment Lighting */}
            <div className="absolute top-0 right-1/4 w-96 h-96 rounded-full bg-blue-500/5 dark:bg-blue-500/10 blur-3xl pointer-events-none" />
            <div className="absolute bottom-0 left-10 w-96 h-96 rounded-full bg-emerald-500/5 dark:bg-emerald-500/10 blur-3xl pointer-events-none" />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
                
                {/* Left Column: Authoritative Editorial Copy */}
                <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
                  
                  {/* National Accreditation Chip */}
                  <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#FAFAF8] dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300">
                    <ShieldCheck className="w-4 h-4 text-[#065F46] shrink-0" />
                    <span>জাতীয় শিক্ষাক্রম (NCTB) মানদণ্ডে পরিচালিত • ৬৪ জেলায় সমন্বিত</span>
                  </div>

                  {/* Headline & Welcoming Tone */}
                  <div className="space-y-4">
                    <div className="text-sm font-bold text-[#0A2540] dark:text-sky-400 font-bengali">
                      স্বাগতম, ভবিষ্যৎ গড়ার অগ্রযাত্রায়
                    </div>
                    <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black text-[#0A2540] dark:text-white tracking-tight leading-[1.18] font-bengali">
                      বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক <span className="underline decoration-[#B45309]/30 underline-offset-8">ডিজিটাল শিক্ষাজীবন</span>
                    </h1>
                    <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl mx-auto lg:mx-0 font-bengali">
                      মাধ্যমিক ও উচ্চ মাধ্যমিক থেকে বিশ্ববিদ্যালয় ভর্তি এবং পেশাগত ক্যারিয়ার—সব বিষয়ের অধ্যায়ভিত্তিক প্রাতিষ্ঠানিক পাঠ্যক্রম, বিগত ১০ বছরের নির্ভুল বোর্ড প্রশ্ন এবং ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি।
                    </p>
                  </div>

                  {/* High-Contrast Dual Call to Action */}
                  <div className="pt-2 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
                    <Link
                      href="/practice"
                      className="btn-3d-oxford w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl bg-[#0A2540] hover:bg-[#0E3357] text-white font-bold font-bengali text-base shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none transition-all min-h-[52px]"
                    >
                      <GraduationCap className="w-5 h-5 text-amber-300" />
                      <span>পড়াশোনা শুরু করুন (Quick Resume)</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </Link>

                    <Link
                      href="/board-archives"
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-4 rounded-2xl bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-800 dark:text-slate-200 font-bold font-bengali text-base border border-slate-300 dark:border-slate-700 shadow-sm active:translate-y-0.5 transition-all min-h-[52px]"
                    >
                      <Award className="w-5 h-5 text-[#B45309]" />
                      <span>বোর্ড প্রশ্ন ব্যাংক (২০১৫–২০২৫)</span>
                    </Link>
                  </div>

                  {/* Micro Trust Indicators */}
                  <div className="pt-4 flex flex-wrap items-center justify-center lg:justify-start gap-6 text-xs text-slate-500 dark:text-slate-400 font-medium">
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span>কোনো লুকানো চার্জ নেই</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span>১০০% শিক্ষার্থী ডেটা গোপনীয়তা</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span>অফলাইন মেশ সিঙ্ক সুবিধা</span>
                    </div>
                  </div>

                </div>

                {/* Right Column: Live Academic Stage Preview Console */}
                <div className="lg:col-span-5">
                  <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xl shadow-slate-200/50 dark:shadow-none space-y-6">
                    
                    <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
                      <div className="space-y-0.5">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 font-mono">
                          PLATFORM ARCHITECTURE
                        </span>
                        <h3 className="text-base font-bold text-[#0A2540] dark:text-white font-bengali">
                          শিক্ষার সার্বিক ৪টি ধাপ
                        </h3>
                      </div>
                      <span className="px-2.5 py-1 rounded-md bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 text-xs font-bold font-mono">
                        NCTB 2026 Ready
                      </span>
                    </div>

                    {/* Stage Selector Chips */}
                    <div className="grid grid-cols-2 gap-2 text-xs font-bold font-bengali">
                      <button
                        type="button"
                        onClick={() => setActiveStage('ssc')}
                        className={`p-3 rounded-xl border text-left transition ${
                          activeStage === 'ssc'
                            ? 'bg-[#0A2540] text-white border-[#0A2540]'
                            : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <BookOpen className="w-4 h-4 mb-1.5" />
                        <div>মাধ্যমিক (SSC ৯-১০)</div>
                        <div className="text-[10px] font-normal opacity-80">শ্রেণি ৯–১০ বোর্ড প্রস্তুতি</div>
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveStage('hsc')}
                        className={`p-3 rounded-xl border text-left transition ${
                          activeStage === 'hsc'
                            ? 'bg-[#0A2540] text-white border-[#0A2540]'
                            : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <Layers className="w-4 h-4 mb-1.5" />
                        <div>উচ্চ মাধ্যমিক (HSC ১১-১২)</div>
                        <div className="text-[10px] font-normal opacity-80">বিজ্ঞান, মানবিক, বাণিজ্য</div>
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveStage('admission')}
                        className={`p-3 rounded-xl border text-left transition ${
                          activeStage === 'admission'
                            ? 'bg-[#0A2540] text-white border-[#0A2540]'
                            : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <Target className="w-4 h-4 mb-1.5" />
                        <div>বিশ্ববিদ্যালয় ভর্তি (Admission)</div>
                        <div className="text-[10px] font-normal opacity-80">বুয়েট, ঢাবি, মেডিকেল</div>
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveStage('career')}
                        className={`p-3 rounded-xl border text-left transition ${
                          activeStage === 'career'
                            ? 'bg-[#0A2540] text-white border-[#0A2540]'
                            : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                        }`}
                      >
                        <Users className="w-4 h-4 mb-1.5" />
                        <div>টিউশন ও ক্যারিয়ার (Career)</div>
                        <div className="text-[10px] font-normal opacity-80">এসক্রো চুক্তি ও চাকরি</div>
                      </button>
                    </div>

                    {/* Active Stage Details Card */}
                    <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-200/80 dark:border-slate-800 space-y-3">
                      {activeStage === 'ssc' && (
                        <>
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-bold text-slate-800 dark:text-slate-200">মাধ্যমিক প্রস্তুতি হাব</span>
                            <span className="font-mono text-emerald-600 font-bold">১০ বছরের বোর্ড প্রশ্ন</span>
                          </div>
                          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                            সাধারণ গণিত, উচ্চতর গণিত, পদার্থ ও রসায়নের অধ্যায়ভিত্তিক প্রশ্ন, এমসিকিউ কুইজ এবং মডেল টেস্ট।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/learn?stage=SSC"
                              className="text-xs font-bold text-[#0A2540] dark:text-sky-400 hover:underline inline-flex items-center gap-1 font-bengali"
                            >
                              <span>মাধ্যমিক সিলেবাস এক্সপ্লোর করুন</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </Link>
                          </div>
                        </>
                      )}

                      {activeStage === 'hsc' && (
                        <>
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-bold text-slate-800 dark:text-slate-200">উচ্চ মাধ্যমিক বিজ্ঞান হাব</span>
                            <span className="font-mono text-emerald-600 font-bold">KaTeX সমীকরণ ভিউয়ার</span>
                          </div>
                          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                            পদার্থবিজ্ঞান ১ম ও ২য় পত্র, জৈব রসায়ন, ম্যাট্রিক্স এবং ক্যালকুলাসের বিশদ গাণিতিক বিশ্লেষণ।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/learn?stage=HSC"
                              className="text-xs font-bold text-[#0A2540] dark:text-sky-400 hover:underline inline-flex items-center gap-1 font-bengali"
                            >
                              <span>উচ্চ মাধ্যমিক কোর্স দেখুন</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </Link>
                          </div>
                        </>
                      )}

                      {activeStage === 'admission' && (
                        <>
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-bold text-slate-800 dark:text-slate-200">ভর্তি ব্লুপ্রিন্ট ও কাট-অফ ম্যাট্রিক্স</span>
                            <span className="font-mono text-amber-600 font-bold">নেগেটিভ মার্কিং এলার্ট</span>
                          </div>
                          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                            বুয়েট প্রিলিমিনারি, ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট এবং সরকারি মেডিকেলের বিগত বছরের কাট-অফ বিশ্লেষণ।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/admission"
                              className="text-xs font-bold text-[#0A2540] dark:text-sky-400 hover:underline inline-flex items-center gap-1 font-bengali"
                            >
                              <span>ভর্তি প্রস্তুতি হাব খুলুন</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </Link>
                          </div>
                        </>
                      )}

                      {activeStage === 'career' && (
                        <>
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-bold text-slate-800 dark:text-slate-200">টিউশন এসক্রো ও স্কিল সনদ</span>
                            <span className="font-mono text-blue-600 font-bold">W3C ক্রিপ্টোগ্রাফিক ভেরিফাইড</span>
                          </div>
                          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                            অভিভাবকদের সঙ্গে দ্বিপাক্ষিক ডিজিটাল চুক্তি এবং বিশ্ববিদ্যালয় শিক্ষার্থীদের জন্য নিরাপদ টিউশন প্ল্যাটফর্ম।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/tuition"
                              className="text-xs font-bold text-[#0A2540] dark:text-sky-400 hover:underline inline-flex items-center gap-1 font-bengali"
                            >
                              <span>টিউশন মার্কেটপ্লেস দেখুন</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </Link>
                          </div>
                        </>
                      )}
                    </div>

                    <div className="pt-2">
                      <Link
                        href="/dashboard"
                        className="w-full py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-xs flex items-center justify-center gap-2 transition"
                      >
                        <span>শিক্ষার্থী পোর্টাল ও ড্যাশবোর্ডে প্রবেশ</span>
                        <ChevronRight className="w-4 h-4" />
                      </Link>
                    </div>

                  </div>
                </div>

              </div>
            </div>
          </section>

          {/* ===================================================================
              SECTION 2: 4-CARD ACADEMIC TELEMETRY GRID & NATIONAL TRUST STRIP
              Linear/Vercel/Stripe-grade Unified Dark Telemetry System
              =================================================================== */}
          <section
            aria-label="অ্যাকাডেমিক প্রোগ্রেস ও প্ল্যাটফর্ম পরিসংখ্যান"
            suppressHydrationWarning={true}
            className="py-14 sm:py-16 md:py-20 bg-[#071727] text-white border-b border-white/[0.08] relative overflow-hidden"
          >
            {/* Ambient Background Glow */}
            <div
              className="absolute inset-0 pointer-events-none opacity-30 bg-[radial-gradient(ellipse_80%_50%_at_50%_-15%,rgba(16,185,129,0.15),transparent)]"
              aria-hidden="true"
            />
            <div
              className="absolute inset-0 pointer-events-none opacity-20 bg-[radial-gradient(ellipse_70%_40%_at_50%_115%,rgba(10,37,64,0.9),transparent)]"
              aria-hidden="true"
            />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12 sm:space-y-14 relative z-10">

              {/* TIER 1: আমার প্রোগ্রেস (PERSONAL TELEMETRY & STUDY MOMENTUM) */}
              <div className="space-y-5">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-2 border-b border-white/[0.07]">
                  <div className="space-y-1">
                    <div className="inline-flex items-center gap-2 text-[11px] sm:text-[12px] font-semibold text-emerald-400 tracking-wider uppercase font-mono">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" />
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

                  {/* 1. Study Streak */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-amber-400/40 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-5">
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
                        <div className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                          ৭ দিনের স্ট্রিক
                        </div>
                        <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                          টানা ৭ দিন সক্রিয় প্রশ্ন অনুশীলন অব্যাহত
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 7-Day Streak Pills */}
                    <div className="pt-3 border-t border-white/[0.07]">
                      <div className="flex items-center justify-between gap-1.5 mb-1.5">
                        {[
                          { day: 'শনি', active: true },
                          { day: 'রবি', active: true },
                          { day: 'সোম', active: true },
                          { day: 'মঙ্গল', active: true },
                          { day: 'বুধ', active: true },
                          { day: 'বৃহঃ', active: true },
                          { day: 'শুক্র', active: true, isToday: true },
                        ].map((item, idx) => (
                          <div key={idx} className="flex-1 flex flex-col items-center gap-1.5">
                            <div
                              className={`w-full h-2.5 rounded-full transition-all duration-300 ${
                                item.active
                                  ? item.isToday
                                    ? 'bg-amber-400 shadow-[0_0_10px_rgba(251,191,36,0.7)]'
                                    : 'bg-amber-400/80 shadow-[0_0_4px_rgba(251,191,36,0.3)]'
                                  : 'bg-white/10'
                              }`}
                              title={`${item.day}: অর্জিত`}
                            />
                            <span className="text-[11px] font-medium text-slate-400 font-bengali">
                              {item.day}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* 2. Solved Questions */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-emerald-400/40 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-5">
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
                        <div className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                          ১২৮টি প্রশ্ন সমাধান
                        </div>
                        <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                          এনসিটিবি বোর্ড প্রশ্ন ব্যাংক থেকে সম্পন্ন
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 7-Day Activity Sparkline Bars */}
                    <div className="pt-3 border-t border-white/[0.07]">
                      <div
                        className="flex items-end justify-between gap-1.5 h-7 pb-1 border-b border-white/[0.08]"
                        aria-label="সাপ্তাহিক প্রশ্ন সমাধানের চার্ট"
                      >
                        {[12, 18, 14, 26, 20, 16, 22].map((val, idx) => {
                          const heightPercent = Math.max(25, Math.round((val / 26) * 100));
                          const isLatest = idx === 6;
                          return (
                            <div
                              key={idx}
                              className="flex-1 flex flex-col justify-end items-center h-full group/bar"
                            >
                              <div
                                style={{ height: `${heightPercent}%` }}
                                className={`w-full rounded-t-[3px] transition-all duration-300 ${
                                  isLatest
                                    ? 'bg-gradient-to-t from-emerald-500 to-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]'
                                    : 'bg-emerald-500/35 group-hover/bar:bg-emerald-400/60'
                                }`}
                                title={`দিন ${idx + 1}: ${val}টি`}
                              />
                            </div>
                          );
                        })}
                      </div>
                      <div className="flex justify-between items-center text-[10px] text-slate-400 font-bengali mt-1.5">
                        <span>৭ দিন পূর্বে</span>
                        <span className="text-emerald-300 font-medium">আজকের পিক (২২টি)</span>
                      </div>
                    </div>
                  </div>

                  {/* 3. Accuracy Rate */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-emerald-400/40 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-5">
                    <div className="space-y-3.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Target className="w-[18px] h-[18px] text-emerald-400" aria-hidden="true" />
                          <span className="text-[15px] font-medium text-slate-200 font-bengali">
                            নির্ভুলতা
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08] font-bengali">
                          ঋণাত্মক সতর্ক
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-3xl sm:text-4xl font-black text-white font-mono tabular-nums tracking-tight">
                          ৮৬.৪% নির্ভুলতা
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
                              strokeDashoffset={13.6}
                              strokeWidth="3.5"
                              strokeLinecap="round"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                          </svg>
                          <span className="absolute text-[8px] font-bold font-mono text-emerald-300">
                            ৮৬
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

                  {/* 4. National Percentile Rank */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-emerald-400/40 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-5">
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
                        <div className="text-3xl sm:text-4xl font-black text-white font-bengali tracking-tight">
                          শীর্ষ ৫% শিক্ষার্থী
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
                          style={{ width: '95.2%' }}
                          className="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 rounded-full shadow-[0_0_8px_rgba(52,211,153,0.5)]"
                        />
                      </div>
                      <div className="flex items-center justify-between text-[11px] text-slate-400 font-bengali">
                        <span>০%</span>
                        <span className="text-emerald-300 font-semibold font-mono">
                          ৯৫.২তম পার্সেন্টাইল
                        </span>
                        <span>১০০%</span>
                      </div>
                    </div>
                  </div>

                </div>
              </div>

              {/* TIER 2: প্ল্যাটফর্ম ট্রাস্ট (NATIONAL TRUST & PEDAGOGICAL PILLARS) */}
              <div className="space-y-5 pt-2">
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

                  {/* 5. 10-Year Archive */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-white/20 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-4">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <BookOpen className="w-[18px] h-[18px] text-slate-300" aria-hidden="true" />
                          <span className="text-[15px] font-medium text-slate-200 font-bengali">
                            বোর্ড প্রশ্ন আর্কাইভ
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-white/[0.06] text-slate-300 border border-white/[0.08] font-bengali">
                          ২০১৫ — ২০২৫
                        </span>
                      </div>

                      <div className="space-y-1.5">
                        <div className="text-3xl sm:text-4xl font-black text-white font-bengali tracking-tight">
                          ১০ বছর (২০১৫–২৫)
                        </div>
                        <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                          আসল বোর্ড প্রশ্ন আর্কাইভ
                        </h3>
                        <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                          সকল সাধারণ ও কারিগরি শিক্ষা বোর্ডের আসল প্রশ্ন এবং নির্ভুল KaTeX সমীকরণ
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

                  {/* 6. 100% NCTB Compliant */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-emerald-400/40 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-4">
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
                          ১০০% এনসিটিবি
                        </div>
                        <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                          জাতীয় শিক্ষাক্রম মানদণ্ড
                        </h3>
                        <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                          মাধ্যমিক ও উচ্চ মাধ্যমিকের ৬৯টি অ্যাকাডেমিক অধ্যায়ের শতভাগ এনসিটিবি মান
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 100% Solid Emerald Progress Bar */}
                    <div className="pt-3 border-t border-white/[0.07]">
                      <div className="w-full h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]" />
                      <div className="flex justify-between items-center text-[10px] text-slate-400 font-bengali mt-1.5">
                        <span>এনসিটিবি অনুমোদিত</span>
                        <span className="text-emerald-300 font-medium">৬৯ / ৬৯ অধ্যায়</span>
                      </div>
                    </div>
                  </div>

                  {/* 7. 64 Districts P2P Offline */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-white/20 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-4">
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
                          ৬৪ জেলা অফলাইন
                        </div>
                        <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                          P2P মেশ ক্লাসরুম
                        </h3>
                        <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                          ইন্টারনেট ছাড়াই পরীক্ষা ও লোকাল সিঙ্ক এবং স্বয়ংক্রিয় ক্লাস্টার ব্যাকআপ
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 4 Interconnected Node Mesh Link */}
                    <div className="pt-3 border-t border-white/[0.07]">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1.5">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" />
                          <span className="w-8 h-[2px] bg-white/20" />
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" />
                          <span className="w-8 h-[2px] bg-white/20" />
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" />
                        </div>
                        <span className="text-[11px] font-mono text-slate-300 font-bengali">
                          ৪৯৫ উপজেলা
                        </span>
                      </div>
                      <div className="text-[10px] text-slate-400 font-bengali mt-1.5">
                        জিরো-প্যাকেট লস আর্কিটেকচার
                      </div>
                    </div>
                  </div>

                  {/* 8. 0% Intrusive Surveillance */}
                  <div className="group p-6 rounded-2xl bg-[#0A1E34]/85 border border-white/[0.09] shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08),0_4px_20px_rgba(0,0,0,0.3)] hover:border-white/20 hover:-translate-y-1 hover:shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_12px_32px_rgba(0,0,0,0.5)] transition-all duration-200 flex flex-col justify-between space-y-4">
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
                          ০% নজরদারি
                        </div>
                        <h3 className="text-[15px] font-semibold text-white font-bengali leading-snug">
                          জিরো-ভিডিও প্রক্টরিং
                        </h3>
                        <p className="text-[13px] text-slate-300 font-bengali leading-relaxed">
                          শিক্ষার্থী ডেটা সার্বভৌমত্ব ও মর্যাদা; কোনো ওয়েবক্যাম বা ফেসিয়াল ট্র্যাকিং নয়
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: End-to-End Cryptographic Security Status */}
                    <div className="pt-3 border-t border-white/[0.07]">
                      <div className="flex items-center gap-2 text-[11px] font-medium text-emerald-400 font-bengali">
                        <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)] inline-block" />
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

          {/* ===================================================================
              SECTION 3: CURATED JOURNEY PATHWAYS (4 Cards with Progress Bars)
              =================================================================== */}
          <section className="py-16 md:py-24 bg-[#FAFAF8] dark:bg-[#090D16]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
              
              <div className="text-center max-w-3xl mx-auto space-y-3">
                <span className="text-xs font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-mono">
                  STRUCTURED CURRICULUM
                </span>
                <h2 className="text-3xl sm:text-4xl font-black text-[#0A2540] dark:text-white tracking-tight font-bengali">
                  আপনার প্রয়োজনীয় শিক্ষাস্তর নির্বাচন করুন
                </h2>
                <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                  প্রতিটি স্তরের জন্য রয়েছে বিশেষায়িত প্রশ্ন ব্যাংক, লাইভ অনুশীলন, এবং বিশেষজ্ঞ শিক্ষকদের সহায়তায় সাজানো পাঠ্যক্রম।
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                
                {/* 1. SSC */}
                <div className="p-7 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="w-12 h-12 rounded-2xl bg-blue-50 dark:bg-blue-950/60 text-[#0A2540] dark:text-sky-300 flex items-center justify-center border border-blue-200 dark:border-blue-800">
                      <BookOpen className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-[11px] font-bold text-slate-400 uppercase font-mono">Class 9–10</span>
                      <h3 className="text-xl font-bold text-[#0A2540] dark:text-white font-bengali mt-0.5">
                        মাধ্যমিক (SSC) বোর্ড প্রস্তুতি
                      </h3>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                      সাধারণ গণিত, পদার্থবিজ্ঞান, রসায়ন ও উচ্চতর গণিতের বিগত ১০ বছরের সকল বোর্ডের নির্ভুল সৃজনশীল ও এমসিকিউ সমাধান।
                    </p>
                    {/* Progress Bar */}
                    <div className="space-y-1.5 pt-2">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="text-slate-500">সিলেবাস অগ্রগতি</span>
                        <span className="font-bold text-[#0A2540] dark:text-sky-400">৬৮% সম্পন্ন</span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                        <div className="h-full bg-[#0A2540] dark:bg-sky-500 rounded-full w-[68%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/learn?stage=SSC"
                    className="inline-flex items-center justify-between w-full pt-4 border-t border-slate-100 dark:border-slate-800 text-xs font-bold text-[#0A2540] dark:text-sky-400 hover:text-[#0E3357] transition"
                  >
                    <span>এসএসসি পাঠ্যক্রম দেখুন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 2. HSC */}
                <div className="p-7 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="w-12 h-12 rounded-2xl bg-emerald-50 dark:bg-emerald-950/60 text-[#065F46] dark:text-emerald-300 flex items-center justify-center border border-emerald-200 dark:border-emerald-800">
                      <Layers className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-[11px] font-bold text-slate-400 uppercase font-mono">Class 11–12</span>
                      <h3 className="text-xl font-bold text-[#0A2540] dark:text-white font-bengali mt-0.5">
                        উচ্চ মাধ্যমিক (HSC) বিজ্ঞান
                      </h3>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                      পদার্থবিজ্ঞান ১ম ও ২য় পত্র, জৈব রসায়ন, ক্যালকুলাস ও জীববিজ্ঞানের জটিল তাত্ত্বিক অধ্যায়গুলোর বিশদ অ্যানালিটিক্স।
                    </p>
                    {/* Progress Bar */}
                    <div className="space-y-1.5 pt-2">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="text-slate-500">সিলেবাস অগ্রগতি</span>
                        <span className="font-bold text-[#065F46] dark:text-emerald-400">৮২% সম্পন্ন</span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                        <div className="h-full bg-[#065F46] dark:bg-emerald-500 rounded-full w-[82%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/learn?stage=HSC"
                    className="inline-flex items-center justify-between w-full pt-4 border-t border-slate-100 dark:border-slate-800 text-xs font-bold text-[#065F46] dark:text-emerald-400 hover:text-[#087858] transition"
                  >
                    <span>এইচএসসি সিলেবাস দেখুন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 3. Admission */}
                <div className="p-7 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="w-12 h-12 rounded-2xl bg-amber-50 dark:bg-amber-950/60 text-[#B45309] dark:text-amber-300 flex items-center justify-center border border-amber-200 dark:border-amber-800">
                      <Target className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-[11px] font-bold text-slate-400 uppercase font-mono">University Entrance</span>
                      <h3 className="text-xl font-bold text-[#0A2540] dark:text-white font-bengali mt-0.5">
                        বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি
                      </h3>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                      বুয়েট প্রিলিমিনারি, ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট এবং মেডিকেল নেগেটিভ মার্কিং মক টেস্ট ইঞ্জিন।
                    </p>
                    {/* Progress Bar */}
                    <div className="space-y-1.5 pt-2">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="text-slate-500">ভর্তি লক্ষ্য প্রস্তুতি</span>
                        <span className="font-bold text-[#B45309] dark:text-amber-400">৪৫% সম্পন্ন</span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                        <div className="h-full bg-[#B45309] dark:bg-amber-500 rounded-full w-[45%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/admission"
                    className="inline-flex items-center justify-between w-full pt-4 border-t border-slate-100 dark:border-slate-800 text-xs font-bold text-[#B45309] dark:text-amber-400 hover:text-[#D97706] transition"
                  >
                    <span>ভর্তি প্রস্তুতি হাব খুলুন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 4. Tuition & Career */}
                <div className="p-7 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center border border-slate-200 dark:border-slate-700">
                      <Users className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-[11px] font-bold text-slate-400 uppercase font-mono">Marketplace & Career</span>
                      <h3 className="text-xl font-bold text-[#0A2540] dark:text-white font-bengali mt-0.5">
                        টিউশন ও স্কিল লেজার
                      </h3>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                      দ্বিপাক্ষিক এসক্রো সুরক্ষিত হোম ও অনলাইন টিউশন এবং অপরিবর্তনীয় একাডেমিক সিভি ও মেধা সনদ।
                    </p>
                    {/* Progress Bar */}
                    <div className="space-y-1.5 pt-2">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="text-slate-500">প্রোফাইল ভেরিফিকেশন</span>
                        <span className="font-bold text-slate-700 dark:text-slate-300">৯০% প্রোফাইল</span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                        <div className="h-full bg-slate-700 dark:bg-slate-300 rounded-full w-[90%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/tuition"
                    className="inline-flex items-center justify-between w-full pt-4 border-t border-slate-100 dark:border-slate-800 text-xs font-bold text-slate-800 dark:text-slate-200 hover:text-[#0A2540] transition"
                  >
                    <span>টিউশন মার্কেটপ্লেস</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 4: 3D STEM VIRTUAL LABS SHOWCASE (Interactive Simulators)
              =================================================================== */}
          <section className="py-16 md:py-24 bg-white dark:bg-slate-950 border-y border-slate-200/80 dark:border-slate-800/80">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
              
              <div className="text-center max-w-3xl mx-auto space-y-3">
                <span className="text-xs font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-mono">
                  INNOVATION & PEDAGOGY
                </span>
                <h2 className="text-3xl sm:text-4xl font-black text-[#0A2540] dark:text-white tracking-tight font-bengali">
                  ৩ডি স্টেম ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি
                </h2>
                <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                  মুখস্থ বিদ্যার বিকল্প হিসেবে গভীর চিন্তন দক্ষতা ও সমস্যা সমাধানের জন্য প্রস্তুত বিশেষায়িত ত্রিমাত্রিক টুলস।
                </p>
              </div>

              {/* Showcase Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
                
                {/* Lab 1: Physics Projectile Motion */}
                <div className="lg:col-span-6 p-8 rounded-3xl bg-[#FAFAF8] dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 dark:bg-teal-950/60 text-[#065F46] text-xs font-bold border border-teal-200 dark:border-teal-800">
                      <Atom className="w-4 h-4" />
                      <span>৩ডি ইন্টারেক্টিভ সিমুলেটর • Physics</span>
                    </div>

                    <h3 className="text-2xl font-black text-[#0A2540] dark:text-white font-bengali">
                      প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Projectile Motion)
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
                      ক্যাননের নিক্ষেপ কোণ, বেগ ও মধ্যাকর্ষণ ত্বরণ পরিবর্তন করে প্রক্ষেপকের পাল্লা ও সর্বোচ্চ উচ্চতা নির্ণয় করুন। সমীকরণ: H = (v0² sin²θ) / 2g।
                    </p>

                    <div className="p-4 rounded-2xl bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-2 text-xs">
                      <div className="flex items-center justify-between text-slate-500 font-mono">
                        <span>পদার্থবিজ্ঞান ১ম পত্র • গতিবিদ্যা</span>
                        <span className="text-emerald-600 font-bold">৬০ FPS ক্যানভাস</span>
                      </div>
                      <div className="font-mono text-slate-800 dark:text-slate-200 font-semibold">
                        Projectile Motion: R = (v0² sin 2θ) / g
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('physics')}
                    className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-[#065F46] hover:bg-[#087858] text-white font-bold text-sm shadow-[0_4px_0_0_#044332] active:translate-y-1 active:shadow-none transition-all"
                  >
                    <Play className="w-4 h-4 text-emerald-200" />
                    <span>ল্যাব চালু করুন (Physics Projectile Lab)</span>
                  </button>
                </div>

                {/* Lab 2: Chemistry Molecular Geometry */}
                <div className="lg:col-span-6 p-8 rounded-3xl bg-[#FAFAF8] dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 text-[#0A2540] dark:text-sky-300 text-xs font-bold border border-blue-200 dark:border-blue-800">
                      <Atom className="w-4 h-4" />
                      <span>৩ডি ইন্টারেক্টিভ সিমুলেটর • Chemistry</span>
                    </div>

                    <h3 className="text-2xl font-black text-[#0A2540] dark:text-white font-bengali">
                      ৩ডি আণবিক জ্যামিতি ও সংকরায়ন (Molecular Geometry)
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
                      VSEPR তত্ত্ব ও sp, sp², sp³ সংকরায়নের ত্রিমাত্রিক বন্ধন কোণ ও পরমাণুর অবস্থান ব্রাউজারে ৩ডি স্পেসে ঘুরিয়ে পর্যবেক্ষণ করুন।
                    </p>

                    <div className="p-4 rounded-2xl bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-2 text-xs">
                      <div className="flex items-center justify-between text-slate-500 font-mono">
                        <span>রসায়ন ১ম পত্র • রাসায়নিক বন্ধন</span>
                        <span className="text-sky-600 font-bold">VSEPR 3D Engine</span>
                      </div>
                      <div className="font-mono text-slate-800 dark:text-slate-200 font-semibold">
                        Molecular Geometry: CH4 (Tetrahedral, 109.5°)
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('chemistry')}
                    className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-[#0A2540] hover:bg-[#0E3357] text-white font-bold text-sm shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none transition-all"
                  >
                    <Play className="w-4 h-4 text-amber-300" />
                    <span>ল্যাব চালু করুন (Chemistry Molecular Lab)</span>
                  </button>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 5: LIVE CHALLENGE SPOTLIGHT & SOCRATIC AI INSTANT SOLVER
              =================================================================== */}
          <section className="py-16 md:py-24 bg-[#FAFAF8] dark:bg-[#090D16]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
              
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
                
                {/* Live Challenge Spotlight Card (8:00 PM National Olympiad) */}
                <div className="lg:col-span-7 p-8 rounded-3xl bg-gradient-to-br from-[#0A2540] to-[#0E3357] text-white border border-slate-700 shadow-xl flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-amber-300 text-xs font-semibold backdrop-blur-sm border border-white/10">
                      <Trophy className="w-4 h-4" />
                      <span>জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬</span>
                    </div>

                    <h3 className="text-2xl sm:text-3xl font-black font-bengali leading-tight">
                      আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড চ্যালেঞ্জ
                    </h3>
                    <p className="text-sm text-slate-300 leading-relaxed font-bengali">
                      সমগ্র বাংলাদেশের শীর্ষ শিক্ষার্থীদের সঙ্গে সরাসরি লাইভ প্রতিযোগিতায় অংশগ্রহণ করুন। রিয়েল-টাইম লিডারবোর্ড ও তাৎক্ষণিক বিশ্লেষণ।
                    </p>

                    {/* Countdown Timer Display */}
                    <div className="p-4 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-between">
                      <div className="space-y-0.5">
                        <span className="text-[11px] uppercase tracking-wider text-slate-400 font-mono">
                          লাইভ কাউন্টডাউন (countdown)
                        </span>
                        <div className="text-xl sm:text-2xl font-black font-mono text-amber-300 tabular-nums">
                          {String(countdown.hours).padStart(2, '0')}:{String(countdown.minutes).padStart(2, '0')}:{String(countdown.seconds).padStart(2, '0')}
                        </div>
                      </div>
                      <div className="text-right space-y-0.5">
                        <span className="text-[11px] uppercase tracking-wider text-slate-400 font-mono">
                          অংশগ্রহণকারী
                        </span>
                        <div className="text-base font-bold text-emerald-300 font-bengali">
                          ৪,৮৫০+ প্রতিযোগী শিক্ষার্থী
                        </div>
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/live-challenge"
                    className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl bg-amber-400 hover:bg-amber-500 text-[#0A2540] font-black text-sm shadow-md transition-all active:translate-y-0.5"
                  >
                    <Trophy className="w-4 h-4 text-[#0A2540]" />
                    <span>লাইভ লবিতে যোগ দিন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* Socratic AI Instant Solver Banner */}
                <div className="lg:col-span-5 p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-6">
                  <div className="space-y-4">
                    <div className="w-12 h-12 rounded-2xl bg-amber-50 dark:bg-amber-950/60 text-[#B45309] dark:text-amber-300 flex items-center justify-center border border-amber-200 dark:border-amber-800">
                      <Sparkles className="w-6 h-6" />
                    </div>

                    <h3 className="text-2xl font-black text-[#0A2540] dark:text-white font-bengali">
                      সক্রেটিক এআই তাৎক্ষণিক সমাধান
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
                      যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন। সরাসরি উত্তর না দিয়ে ধাপে ধাপে গাণিতিক সংকেত ও সূত্রের মাধ্যমে যুক্তি গড়ে তোলে।
                    </p>

                    <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 font-bengali">
                      গণিত, পদার্থবিজ্ঞান এবং রসায়নের জটিল গাণিতিক সমস্যার জন্য সার্বক্ষণিক ব্যক্তিগত শিক্ষক।
                    </div>
                  </div>

                  <button
                    type="button"
                    id="global-socratic-trigger"
                    onClick={() => {
                      const btn = document.getElementById('global-socratic-trigger');
                      if (btn) btn.setAttribute('data-active', 'true');
                    }}
                    className="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-2xl bg-[#0A2540] hover:bg-[#0E3357] text-white font-bold text-sm shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none transition-all"
                  >
                    <Sparkles className="w-4 h-4 text-amber-300" />
                    <span>সক্রেটিক টিউটর চালু করুন</span>
                  </button>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 6: W3C PROOF-OF-SKILL CERTIFICATE SHOWCASE & SOCIAL SHARING
              =================================================================== */}
          <section className="py-16 md:py-24 bg-white dark:bg-slate-950 border-y border-slate-200/80 dark:border-slate-800/80">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
              
              <div className="text-center max-w-3xl mx-auto space-y-3">
                <span className="text-xs font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-mono">
                  VERIFIABLE CREDENTIALS
                </span>
                <h2 className="text-3xl sm:text-4xl font-black text-[#0A2540] dark:text-white tracking-tight font-bengali">
                  W3C ক্রিপ্টোগ্রাফিক ভেরিফাইড মেধা ও দক্ষতা সনদ
                </h2>
                <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                  ব্লকচেইন-মানসম্পন্ন ক্রিপ্টোগ্রাফিক হ্যাশযুক্ত সনদ যা বিশ্ববিদ্যালয়, শিক্ষক এবং আন্তর্জাতিক নিয়োগকারীদের কাছে সরাসরি যাচাইযোগ্য।
                </p>
              </div>

              {/* Certificate Component Preview & Action Toolbar */}
              <div className="max-w-4xl mx-auto space-y-6">
                <div className="rounded-3xl border border-slate-200/90 dark:border-slate-800 p-2 sm:p-6 bg-[#FAFAF8] dark:bg-slate-900 shadow-lg">
                  <ProofOfSkillCard certificate={SAMPLE_CERTIFICATE} />
                </div>

                <div className="p-6 rounded-2xl bg-[#FAFAF8] dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="space-y-1 text-center sm:text-left">
                    <span className="text-xs font-mono font-bold text-slate-500">
                      সনদ আইডি: {SAMPLE_CERTIFICATE.cert_id} • প্রাপক: {SAMPLE_CERTIFICATE.student_name}
                    </span>
                    <div className="text-xs text-slate-600 dark:text-slate-400">
                      শেয়ার অপশন: LinkedIn • Facebook • ডাইরেক্ট ভেরিফিকেশন লিঙ্ক
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <SocialShareButtons
                      certId={SAMPLE_CERTIFICATE.cert_id}
                      studentName={SAMPLE_CERTIFICATE.student_name}
                      courseTitle={SAMPLE_CERTIFICATE.course_title}
                      verifyUrl={`https://ogrojatra.edu.bd/verify/${SAMPLE_CERTIFICATE.cert_id}`}
                    />

                    <Link
                      href={`/verify/${SAMPLE_CERTIFICATE.cert_id}`}
                      className="px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-300 transition inline-flex items-center gap-1.5"
                    >
                      <span>যাচাই পৃষ্ঠা</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 7: ENTERPRISE MODULES DIRECTORY & NATIONAL RECOGNITION
              =================================================================== */}
          <section className="py-12 bg-[#FAFAF8] dark:bg-[#090D16] border-b border-slate-200/80 dark:border-slate-800/80">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
              
              <div className="p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 flex flex-col md:flex-row items-center justify-between gap-8 shadow-sm">
                
                <div className="space-y-1 text-center md:text-left max-w-xl">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 font-mono">
                    NATIONAL RECOGNITION & SECURITY
                  </h4>
                  <h3 className="text-lg font-bold text-[#0A2540] dark:text-white font-bengali">
                    নিরাপদ জাতীয় পেমেন্ট ও প্রাতিষ্ঠানিক ডিজিটাল সুরক্ষা
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed font-bengali">
                    বাংলাদেশ ব্যাংক রেগুলেশন এবং আন্তর্জাতিক ডব্লিউথ্রিসি (W3C) ভেরিফাইড ক্রেডেনশিয়াল মানদণ্ড অনুযায়ী পরিচালিত।
                  </p>
                </div>

                <div className="flex flex-wrap items-center justify-center gap-3">
                  {/* bKash */}
                  <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                    <span className="w-2.5 h-2.5 rounded-full bg-pink-500" />
                    <span className="text-xs font-mono font-bold text-pink-600 dark:text-pink-400">bKash Verified</span>
                  </div>

                  {/* Nagad */}
                  <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                    <span className="w-2.5 h-2.5 rounded-full bg-orange-500" />
                    <span className="text-xs font-mono font-bold text-orange-600 dark:text-orange-400">Nagad Verified</span>
                  </div>

                  {/* SSLCommerz */}
                  <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                    <span className="w-2.5 h-2.5 rounded-full bg-blue-600" />
                    <span className="text-xs font-mono font-bold text-blue-600 dark:text-blue-400">SSLCommerz Escrow</span>
                  </div>

                  {/* W3C */}
                  <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                    <span className="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">W3C Compliant</span>
                  </div>
                </div>

              </div>

              {/* Direct Modules Directory Link Card */}
              <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="space-y-0.5 text-center sm:text-left">
                  <div className="text-sm font-bold text-[#0A2540] dark:text-white font-bengali">
                    ৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি
                  </div>
                  <p className="text-xs text-slate-500">
                    একাডেমিক, ভর্তি, রেজিলিয়েন্স, স্টেম স্যান্ডবক্স এবং এন্টারপ্রাইজ ককপিটের পূর্ণ ক্যাটালগ।
                  </p>
                </div>
                <Link
                  href="/modules"
                  className="px-5 py-2.5 rounded-xl bg-[#0A2540] hover:bg-[#0E3357] text-white text-xs font-bold transition flex items-center gap-2 shrink-0"
                >
                  <span>মডিউল ডিরেক্টরি দেখুন</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 8: HIGH-IMPACT CLOSING CALL TO ACTION
              =================================================================== */}\
          <section className="py-20 md:py-28 bg-[#0A2540] text-white relative overflow-hidden">
            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8 relative z-10">
              
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-amber-300 text-xs font-semibold backdrop-blur-sm border border-white/10">
                <GraduationCap className="w-4 h-4" />
                <span>অগ্রযাত্রায় যুক্ত হোন • বাংলাদেশের শিক্ষার ভবিষ্যৎ</span>
              </div>

              <div className="space-y-4 max-w-3xl mx-auto">
                <h2 className="text-3xl sm:text-5xl font-black tracking-tight leading-tight font-bengali">
                  আজই আপনার শিক্ষাপ্রতিষ্ঠান বা পড়াশোনার অগ্রযাত্রায় যুক্ত হোন
                </h2>
                <p className="text-base sm:text-lg text-slate-300 leading-relaxed font-bengali">
                  শিক্ষার্থী, শিক্ষক এবং অভিভাবকদের জন্য সম্পূর্ণ নিরাপদ, জাতীয় কারিকুলাম সমন্বিত ও মর্যাদাপূর্ণ ডিজিটাল পরিবেশ।
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <Link
                  href="/learn"
                  className="btn-3d-oxford w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl bg-white hover:bg-slate-100 text-[#0A2540] font-black text-base shadow-lg transition-all min-h-[52px]"
                >
                  <GraduationCap className="w-5 h-5 text-[#0A2540]" />
                  <span>বিনামূল্যে শুরু করুন</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <Link
                  href="/about"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl bg-white/10 hover:bg-white/20 text-white font-bold text-base border border-white/20 transition-all min-h-[52px]"
                >
                  <FileText className="w-4 h-4 text-slate-300" />
                  <span>প্রাতিষ্ঠানিক লক্ষ্য ও পরিচিতি</span>
                </Link>
              </div>

            </div>
          </section>

        </main>

        <Footer />
      </div>

      {/* Interactive 3D STEM Lab Modals */}
      {activeLabModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in"
        >
          <div className="relative w-full max-w-5xl bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60">
              <div className="flex items-center gap-2">
                <Atom className="w-5 h-5 text-teal-400" />
                <span className="font-bold text-white text-sm sm:text-base font-bengali">
                  {activeLabModal === 'physics'
                    ? 'প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Physics Projectile Lab)'
                    : '৩ডি আণবিক জ্যামিতি ল্যাবরেটরি (Chemistry Molecular Viewer)'}
                </span>
              </div>

              <button
                type="button"
                onClick={() => setActiveLabModal(null)}
                aria-label="ল্যাব বন্ধ করুন"
                className="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 sm:p-6 overflow-y-auto flex-1">
              {activeLabModal === 'physics' ? (
                <PhysicsProjectileLab />
              ) : (
                <ChemistryMolecularViewer />
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
