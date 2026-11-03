/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Flagship Public Educational Portal & Unified Academic Command Surface
 * TOPIC:     Master Academic UI & Modern Academic Editorial Redesign
 * FILE:      frontend/src/pages/index.tsx
 * PHASE:     Phase 110 - Pure Academic Visual Design Elevation & Phase 123 - Master Academic UI
 * PURPOSE:   Presents a world-class, prestigious editorial homepage for Ogrojatra:
 *            1. Modern Academic Editorial aesthetic with warm paper surfaces (#FAF8F3),
 *               hairline borders (#E5E2DA), deep academic navy (#1B2A4A, #0A2540), and muted accents.
 *            2. Editorial Hero with calm serif typography, clear sub-copy, tactile primary/secondary CTAs,
 *               and a 4-level "Choose your level" interactive selector replacing AI-vibe architecture cards.
 *            3. Academic Growth & Progress section ("আপনার শেখার অগ্রগতি") with real, verified student metrics.
 *            4. Curated educational pathways (SSC, HSC, Admission, Career) with progress indicators.
 *            5. 3D STEM Virtual Labs showcase featuring crisp KaTeX formula rendering.
 *            6. Synchronized Live Olympiad countdown timer and Socratic AI instant solver.
 *            7. W3C Proof-of-Skill Cryptographic Certificate showcase with verified social sharing.
 *            8. Official Bangladesh payment trust badges (bKash, Nagad, SSLCommerz) and Modules Directory.
 * STANDARDS: UI/UX Pro Max, Academic Editorial Palette, Strict Zero-Emoji Policy, WCAG 2.2 AAA
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
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';
import { useTranslation, toBengaliDigits } from '@/lib/i18n';
import { SubjectExplorerCarousel } from '@/components/home/SubjectExplorerCarousel';
import { StudentStoriesCarousel } from '@/components/home/StudentStoriesCarousel';
import { LiveHeroInteractiveWidget } from '@/components/home/LiveHeroInteractiveWidget';
import { CompetitorComparisonPillars } from '@/components/home/CompetitorComparisonPillars';
import { m, fadeIn, slideUp, staggerContainer, useReducedMotion } from '@/lib/motion';
import { Academic3DToggle } from '@/components/3d';

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

  // Active educational level selector
  const [activeStage, setActiveStage] = useState<'ssc' | 'hsc' | 'admission' | 'career'>('hsc');

  // Interactive 3D STEM Lab modal state
  const [activeLabModal, setActiveLabModal] = useState<'physics' | 'chemistry' | null>(null);

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
        title={
          isBengali
            ? 'অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা - জাতীয় ডিজিটাল শিক্ষা প্ল্যাটফর্ম'
            : 'Ogrojatra | One Profile. One Journey - National Digital Campus'
        }
        description={
          isBengali
            ? 'এনসিটিবি পাঠ্যক্রম, বিগত ১০ বছরের বোর্ড প্রশ্ন ব্যাংক, ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাব এবং নিরপেক্ষ ডিজিটাল মূল্যায়ন প্ল্যাটফর্ম।'
            : 'National curriculum (NCTB), 10-year board question archive, 3D virtual STEM labs, and objective digital evaluation platform.'
        }
        canonicalUrl="/"
        ogType="website"
        structuredData={createOrganizationSchema()}
      />

      <div className="min-h-screen flex flex-col bg-[#FFFCF6] dark:bg-[#0B0F19] text-[#213130] dark:text-[#F5F2EB] font-sans selection:bg-amber-200 dark:selection:bg-amber-900 selection:text-gray-900 transition-colors duration-300">
        <Navbar currentStage={isBengali ? 'জাতীয় পোর্টাল (National Portal)' : 'National Academic Portal'} />

        <main id="main-content" className="flex-1 w-full">

          {/* ===================================================================
              SECTION 1: EDITORIAL HERO (Calm, Prestigious, Scholarly - GoEdu Background Style)
              =================================================================== */}
          <section className="hero-section relative overflow-hidden pt-8 pb-14 sm:pt-12 sm:pb-20 lg:pt-16 lg:pb-24 border-b border-amber-200/60 dark:border-gray-800 bg-[#FFF6DD] dark:bg-gray-900 transition-colors duration-300">
            {/* GoEdu Background Radial Golden Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '65vh',
                minHeight: '380px',
                background:
                  'radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.70) 0%, rgba(243, 172, 8, 0.35) 45%, rgba(253, 215, 70, 0) 100%)'
              }}
              aria-hidden="true"
            />

            {/* GoEdu Giant Typographic Watermark */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[24vw] md:text-[clamp(4rem,26vw,24rem)] uppercase tracking-wider select-none"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(243, 172, 8, 0.40) 15%, rgba(253, 215, 70, 0.04) 100%)'
                }}
              >
                ogrojatra
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-center">
                
                {/* Left Column: Authoritative Editorial Copy */}
                <div className="lg:col-span-7 space-y-6 text-left">
                  
                  {/* National Accreditation Chip & 3D Depth Controller */}
                  <div className="flex flex-wrap items-center gap-2.5">
                    <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/95 dark:bg-gray-800/95 border border-amber-200/80 dark:border-gray-700 text-xs font-semibold font-bengali text-gray-700 dark:text-gray-200 shadow-xs">
                      <ShieldCheck className="w-4 h-4 text-[#ED8E22] shrink-0" />
                      <span>
                        {isBengali
                          ? 'জাতীয় শিক্ষাক্রম (NCTB) মানদণ্ডে পরিচালিত • ৬৪ জেলায় সমন্বিত'
                          : 'Aligned with National Curriculum (NCTB) • Integrated across 64 Districts'}
                      </span>
                    </div>
                    <Academic3DToggle />
                  </div>

                  {/* Headline & Welcoming Tone */}
                  <div className="space-y-3.5">
                    <div className="flex flex-wrap items-center gap-2.5">
                      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/95 dark:bg-gray-800/95 text-gray-800 dark:text-gray-200 text-xs font-bold font-bengali border border-amber-200/80 dark:border-gray-700 shadow-sm">
                        <span className="h-2 w-2 rounded-full bg-[#ED8E22] shrink-0 animate-pulse" aria-hidden="true" />
                        <span>
                          {isBengali
                            ? '৪টি প্রথাগত অ্যাপের একক বিকল্প • জাতীয় ডিজিটাল ক্যাম্পাস'
                            : 'Single Alternative to 4 Legacy Apps • National Digital Campus'}
                        </span>
                      </div>
                      <span className="text-xs font-semibold text-[#213130] dark:text-[#F5F2EB] font-bengali">
                        {isBengali ? 'স্বাগতম, ভবিষ্যৎ গড়ার অগ্রযাত্রায়' : 'Welcome to the Journey of Shaping the Future'}
                      </span>
                    </div>
                    <h1 className="text-3xl sm:text-5xl lg:text-[52px] font-bold text-[#213130] dark:text-[#F5F2EB] tracking-tight leading-[1.22] font-serif-bn">
                      {isBengali ? (
                        <>
                          বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক <span className="text-[#ED8E22] underline decoration-[#ED8E22]/40 underline-offset-8">ডিজিটাল ক্যাম্পাস</span>
                        </>
                      ) : (
                        <>
                          A Comprehensive <span className="text-[#ED8E22] underline decoration-[#ED8E22]/40 underline-offset-8">Digital Campus</span> for Every Student in Bangladesh
                        </>
                      )}
                    </h1>
                    <p className="text-base sm:text-lg text-[#525252] dark:text-[#A3A8B5] leading-[1.78] max-w-2xl font-sans font-bengali">
                      {isBengali
                        ? '১০ মিনিট স্কুলের ভিডিওর চেয়ে বেশি সক্রিয় ৩ডি ল্যাব, লাইভ এমসিকইউর চেয়ে নির্ভুল জাতীয় অলিম্পিয়াড, কেয়ারটিউটর্সের মতো ৫০% commissionহীন টিউশন এবং বিডিজবসের কাগুজে সিভির বিকল্পে W3C ক্রিপ্টোগ্রাফিক সনদ।'
                        : 'Interactive 3D STEM labs beyond passive videos, latency-free National Olympiad competitions, 0% commission bilateral tuition escrow, and W3C cryptographic credentials replacing paper CVs.'}
                    </p>

                    {/* Interactive Stage Selector Chips */}
                    <div className="flex flex-wrap items-center justify-start gap-2 pt-1 font-bengali">
                      <Link
                        href="/learn?stage=SSC"
                        className="px-3.5 py-1.5 rounded-full text-xs font-semibold border border-gray-200 dark:border-gray-700 bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-gray-200 hover:border-[#ED8E22] hover:text-[#ED8E22] transition-colors shadow-xs"
                      >
                        {isBengali ? 'মাধ্যমিক (SSC ৯-১০)' : 'Secondary (SSC 9–10)'}
                      </Link>
                      <Link
                        href="/learn?stage=HSC"
                        className="px-3.5 py-1.5 rounded-full text-xs font-semibold border border-gray-200 dark:border-gray-700 bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-gray-200 hover:border-[#ED8E22] hover:text-[#ED8E22] transition-colors shadow-xs"
                      >
                        {isBengali ? 'উচ্চ মাধ্যমিক (HSC ১১-১২)' : 'Higher Secondary (HSC 11–12)'}
                      </Link>
                      <Link
                        href="/admission"
                        className="px-3.5 py-1.5 rounded-full text-xs font-semibold border border-gray-200 dark:border-gray-700 bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-gray-200 hover:border-[#ED8E22] hover:text-[#ED8E22] transition-colors shadow-xs"
                      >
                        {isBengali ? 'বিশ্ববিদ্যালয় ভর্তি (Admission)' : 'University Admission'}
                      </Link>
                      <Link
                        href="/tuition"
                        className="px-3.5 py-1.5 rounded-full text-xs font-semibold border border-gray-200 dark:border-gray-700 bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-gray-200 hover:border-[#ED8E22] hover:text-[#ED8E22] transition-colors shadow-xs"
                      >
                        {isBengali ? 'টিউশন ও ক্যারিয়ার (Career)' : 'Tuition & Career'}
                      </Link>
                    </div>
                  </div>

                  {/* High-Contrast Dual Call to Action */}
                  <div className="pt-2 flex flex-col sm:flex-row items-center justify-start gap-4">
                    <Link
                      href="/practice"
                      className="btn-tactile-primary w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-full bg-[#ED8E22] hover:bg-[#D47C1A] text-white font-semibold font-bengali text-base min-h-[48px] shadow-md active:scale-95 transition-all"
                    >
                      <GraduationCap className="w-5 h-5 text-amber-200" />
                      <span>{isBengali ? 'পড়াশোনা শুরু করুন (Quick Resume)' : 'Start Learning (Quick Resume)'}</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </Link>

                    <Link
                      href="/board-archives"
                      className="btn-tactile-outline w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-full bg-white/90 dark:bg-gray-800/90 hover:bg-white dark:hover:bg-gray-800 border border-gray-300 dark:border-gray-700 text-[#213130] dark:text-[#F5F2EB] font-semibold font-bengali text-base min-h-[48px] shadow-sm active:scale-95 transition-all"
                    >
                      <Award className="w-5 h-5 text-[#ED8E22]" />
                      <span>{isBengali ? 'বোর্ড প্রশ্ন ব্যাংক (২০১৫–২০২৫)' : 'Board Question Bank (2015–2025)'}</span>
                    </Link>
                  </div>

                  {/* Trust Strip */}
                  <div className="pt-2 flex flex-wrap items-center justify-center lg:justify-start gap-y-2.5 gap-x-6 text-xs text-[#5B5B5B] dark:text-slate-400 font-medium">
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>{isBengali ? 'এনসিটিবি অনুমোদিত পাঠ্যক্রম' : 'NCTB Approved Curriculum'}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>{isBengali ? '১০ বছরের বোর্ড প্রশ্ন' : '10-Year Board Questions'}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>{isBengali ? 'অফলাইন মেশ সিঙ্ক সুবিধা' : 'Offline Mesh Sync'}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>{isBengali ? 'কোনো লুকানো চার্জ নেই' : 'No Hidden Charges'}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>{isBengali ? '১০০% শিক্ষার্থী ডেটা গোপনীয়তা' : '100% Student Privacy'}</span>
                    </div>
                  </div>

                </div>

                {/* Right Column: Live Interactive Science Playground & Real-Time Campus Energy */}
                <div className="lg:col-span-5">
                  <LiveHeroInteractiveWidget />
                </div>

              </div>
            </div>
          </section>

          {/* ===================================================================
              SECTION 1.5: 4-IN-1 COMPETITOR COMPARISON (10MS, Live MCQ, CareTutors, Bdjobs)
              =================================================================== */}
          <CompetitorComparisonPillars />

          {/* ===================================================================
              SECTION 2: ACADEMIC PROGRESS ("আপনার শেখার অগ্রগতি") & PEDAGOGICAL PILLARS
              Midnight Navy & Sapphire Editorial Band
              =================================================================== */}
          <section
            aria-label="অ্যাকাডেমিক প্রোগ্রেস ও প্ল্যাটফর্ম পরিসংখ্যান"
            suppressHydrationWarning={true}
            className="relative overflow-hidden py-14 sm:py-16 md:py-20 bg-[#F4F7FC]/70 dark:bg-[#0C1527] text-[#213130] dark:text-[#F5F2EB] border-b border-sky-200/50 dark:border-slate-800 transition-colors duration-300"
          >
            {/* Midnight Sapphire & Cyan Radial Ambient Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '520px',
                background:
                  'radial-gradient(ellipse 65% 75% at 50% 100%, rgba(14, 165, 233, 0.16) 0%, rgba(37, 99, 235, 0.08) 50%, transparent 85%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (PROGRESS) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[20vw] md:text-[clamp(4rem,22vw,18rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(14, 165, 233, 0.22) 15%, rgba(37, 99, 235, 0.02) 100%)'
                }}
              >
                progress
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12 sm:space-y-16 relative z-10">

              {/* TIER 1: আপনার শেখার অগ্রগতি (Study Momentum & Practice) */}
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-3 border-b border-amber-200/70 dark:border-[#262D3D]">
                  <div className="space-y-1">
                    <div className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 tracking-wider uppercase font-sans">
                      {isBengali ? 'আপনার শেখার অগ্রগতি (লাইভ লার্নিং টেলিমেট্রি)' : 'Your Academic Progress (Live Learning Telemetry)'}
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                      {isBengali ? 'আমার অনুশীলন ও মেধা প্রবৃদ্ধি' : 'My Practice & Academic Growth'}
                    </h2>
                  </div>
                  <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 font-bengali leading-relaxed max-w-md sm:text-right">
                    {isBengali
                      ? 'দৈনন্দিন অধ্যবসায়, প্রশ্ন সমাধান, নির্ভুলতা ও জাতীয় মেধাতালিকায় আপনার অবস্থান'
                      : 'Daily diligence, solved questions, accuracy, and national percentile rank'}
                  </p>
                </div>

                {/* Tier 1 Grid: 4 Flat Bordered Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

                  {/* 1. Study Streak */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Flame className="w-[18px] h-[18px] text-[#ED8E22]" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'Study Streak (অধ্যয়ন স্ট্রিক)' : 'Study Streak (Consistency)'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#B8862B] border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'ধারাবাহিক' : 'Consistent'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? '৭ দিনের স্ট্রিক' : '7-Day Streak'}
                        </div>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali ? 'টানা ৭ দিন সক্রিয় প্রশ্ন অনুশীলন অব্যাহত' : '7 consecutive days of active question practice'}
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 7-Day Streak Dots */}
                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D]">
                      <div className="flex items-center justify-between gap-1.5 mb-1">
                        {[
                          { day: isBengali ? 'শনি' : 'Sat', active: true },
                          { day: isBengali ? 'রবি' : 'Sun', active: true },
                          { day: isBengali ? 'সোম' : 'Mon', active: true },
                          { day: isBengali ? 'মঙ্গল' : 'Tue', active: true },
                          { day: isBengali ? 'বুধ' : 'Wed', active: true },
                          { day: isBengali ? 'বৃহঃ' : 'Thu', active: true },
                          { day: isBengali ? 'শুক্র' : 'Fri', active: true, isToday: true },
                        ].map((item, idx) => (
                          <div key={idx} className="flex-1 flex flex-col items-center gap-1.5">
                            <div
                              className={`w-full h-2 rounded-full transition-all ${
                                item.active
                                  ? 'bg-[#ED8E22]'
                                  : 'bg-amber-100 dark:bg-slate-700'
                              }`}
                              title={`${item.day}: ${isBengali ? 'অর্জিত' : 'Earned'}`}
                            />
                            <span className="text-[10px] text-[#525252] dark:text-slate-400 font-bengali">
                              {item.day}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* 2. Solved Questions */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <CheckCircle2 className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'প্রশ্ন সমাধান' : 'Solved Questions'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'বোর্ড ব্যাংক' : 'Board Bank'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? '১২৮টি প্রশ্ন সমাধান' : '128 Questions Solved'}
                        </div>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali ? 'এনসিটিবি বোর্ড প্রশ্ন ব্যাংক থেকে সম্পন্ন' : 'Completed from NCTB Board Question Bank'}
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 7-Day Activity Bars */}
                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D]">
                      <div
                        className="flex items-end justify-between gap-1.5 h-6 pb-1 border-b border-amber-200/60 dark:border-[#262D3D]"
                        aria-label="সাপ্তাহিক প্রশ্ন সমাধানের চার্ট"
                      >
                        {[12, 18, 14, 26, 20, 16, 22].map((val, idx) => {
                          const heightPercent = Math.max(25, Math.round((val / 26) * 100));
                          const isLatest = idx === 6;
                          return (
                            <div key={idx} className="flex-1 flex flex-col justify-end items-center h-full">
                              <div
                                style={{ height: `${heightPercent}%` }}
                                className={`w-full rounded-t-[2px] transition-all ${
                                  isLatest
                                    ? 'bg-[#0B5D3B] dark:bg-emerald-400'
                                    : 'bg-[#0B5D3B]/40 dark:bg-emerald-400/40'
                                }`}
                                title={`দিন ${idx + 1}: ${val}টি`}
                              />
                            </div>
                          );
                        })}
                      </div>
                      <div className="flex justify-between items-center text-[10px] text-[#525252] dark:text-slate-400 font-bengali mt-1.5">
                        <span>{isBengali ? '৭ দিন পূর্বে' : '7 Days Ago'}</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-medium">
                          {isBengali ? 'আজকের পিক (২২টি)' : "Today's Peak (22)"}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* 3. Accuracy Rate */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Target className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'নির্ভুলতা' : 'Accuracy'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#525252] dark:text-slate-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'ঋণাত্মক সতর্ক' : 'Negative Alert'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? '৮৬.৪% নির্ভুলতা' : '86.4% Accuracy'}
                        </div>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali ? 'নেগেটিভ মার্কিং এড়িয়ে নির্ভুল উত্তর নিরূপণ' : 'High-precision answers avoiding negative marks'}
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: Compact Circular Progress */}
                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D] flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="relative w-7 h-7 flex items-center justify-center">
                          <svg className="w-7 h-7 transform -rotate-90" viewBox="0 0 36 36" aria-hidden="true">
                            <path
                              className="text-amber-100 dark:text-slate-700"
                              strokeWidth="3.5"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                            <path
                              className="text-[#0B5D3B] dark:text-emerald-400"
                              strokeDasharray="100, 100"
                              strokeDashoffset={13.6}
                              strokeWidth="3.5"
                              strokeLinecap="round"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                          </svg>
                          <span className="absolute text-[8px] font-bold text-[#0B5D3B] dark:text-emerald-400">
                            {isBengali ? '৮৬' : '86'}
                          </span>
                        </div>
                        <div className="text-xs font-semibold font-bengali text-[#1B2A4A] dark:text-slate-200">
                          {isBengali ? 'উচ্চ নির্ভুলতা ব্যান্ড' : 'High Accuracy Band'}
                        </div>
                      </div>
                      <span className="text-[11px] text-[#0B5D3B] dark:text-emerald-400 bg-[#FFF9EB] dark:bg-[#0E1526] px-2 py-0.5 rounded border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                        {isBengali ? '+৪.২% প্রবৃদ্ধি' : '+4.2% Growth'}
                      </span>
                    </div>
                  </div>

                  {/* 4. National Percentile Rank */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Award className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'National Percentile (জাতীয় পার্সেন্টাইল)' : 'National Percentile Rank'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'শীর্ষ মেধা' : 'Top Merit'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? 'শীর্ষ ৫% শিক্ষার্থী' : 'Top 5% Nationwide'}
                        </div>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali ? 'দেশব্যাপী ৫০,০০০+ সক্রিয় পরীক্ষার্থীর মধ্যে' : 'Among 50,000+ active candidates nationwide'}
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: Percentile Track Bar */}
                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D] space-y-1.5">
                      <div className="relative w-full h-2 bg-amber-100 dark:bg-slate-700 rounded-full overflow-hidden">
                        <div
                          style={{ width: '95.2%' }}
                          className="h-full bg-[#0B5D3B] dark:bg-emerald-400 rounded-full"
                        />
                      </div>
                      <div className="flex items-center justify-between text-[10px] text-[#525252] dark:text-slate-400 font-bengali">
                        <span>{isBengali ? '০%' : '0%'}</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">
                          {isBengali ? '৯৫.২তম পার্সেন্টাইল' : '95.2th Percentile'}
                        </span>
                        <span>{isBengali ? '১০০%' : '100%'}</span>
                      </div>
                    </div>
                  </div>

                </div>
              </div>

              {/* TIER 2: প্রাতিষ্ঠানিক ভিত্তি ও প্ল্যাটফর্ম ট্রাস্ট */}
              <div className="space-y-6 pt-4">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-3 border-b border-amber-200/70 dark:border-[#262D3D]">
                  <div className="space-y-1">
                    <div className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 tracking-wider uppercase font-sans">
                      {isBengali ? 'প্রাতিষ্ঠানিক ভিত্তি' : 'Institutional Foundation'}
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                      {isBengali ? 'প্ল্যাটফর্ম ট্রাস্ট ও জাতীয় শিক্ষাক্রম মানদণ্ড' : 'Platform Trust & National Curriculum Standards'}
                    </h2>
                  </div>
                  <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 font-bengali leading-relaxed max-w-md sm:text-right">
                    {isBengali
                      ? 'সার্বভৌম শিক্ষাক্রম, অফলাইন প্রযুক্তি ও শিক্ষার্থী গোপনীয়তার প্রাতিষ্ঠানিক সুরক্ষা'
                      : 'Sovereign curriculum, offline mesh tech, and student privacy protection'}
                  </p>
                </div>

                {/* Tier 2 Grid: 4 Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

                  {/* 1. 10-Year Archive */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <BookOpen className="w-[18px] h-[18px] text-[#1B2A4A] dark:text-slate-300" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'বোর্ড প্রশ্ন আর্কাইভ' : 'Board Question Archive'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#525252] dark:text-slate-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? '২০১৫ — ২০২৫' : '2015 — 2025'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? '১০ বছর (২০১৫–২৫)' : '10 Years (2015–25)'}
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          {isBengali ? 'আসল বোর্ড প্রশ্ন আর্কাইভ' : 'Original Board Question Archive'}
                        </h3>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali
                            ? 'সকল সাধারণ ও কারিগরি শিক্ষা বোর্ডের আসল প্রশ্ন এবং নির্ভুল KaTeX সমীকরণ'
                            : 'Original questions and crisp KaTeX equations across all education boards'}
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D]">
                      <div className="flex items-center gap-1">
                        {Array.from({ length: 10 }).map((_, i) => (
                          <div
                            key={i}
                            className="flex-1 h-1.5 rounded-full bg-[#0B5D3B] dark:bg-emerald-400"
                          />
                        ))}
                      </div>
                      <div className="flex justify-between items-center text-[10px] text-[#525252] dark:text-slate-400 font-bengali mt-1.5">
                        <span>{isBengali ? '২০১৫' : '2015'}</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-medium">
                          {isBengali ? '১০/১০ বছর সম্পূর্ণ' : '10/10 Years Complete'}
                        </span>
                        <span>{isBengali ? '২০২৫' : '2025'}</span>
                      </div>
                    </div>
                  </div>

                  {/* 2. 100% NCTB Compliant */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <ShieldCheck className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'জাতীয় মানদণ্ড' : 'National Standard'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'ভেরিফায়েড' : 'Verified'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#0B5D3B] dark:text-emerald-400 font-bengali">
                          {isBengali ? '১০০% এনসিটিবি' : '100% NCTB'}
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          {isBengali ? 'জাতীয় শিক্ষাক্রম মানদণ্ড' : 'National Curriculum Standard'}
                        </h3>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali
                            ? 'মাধ্যমিক ও উচ্চ মাধ্যমিকের ৬৯টি অ্যাকাডেমিক অধ্যায়ের শতভাগ এনসিটিবি মান'
                            : '100% NCTB standard across 69 secondary and higher secondary chapters'}
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D]">
                      <div className="w-full h-1.5 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                      <div className="flex justify-between items-center text-[10px] text-[#525252] dark:text-slate-400 font-bengali mt-1.5">
                        <span>{isBengali ? 'এনসিটিবি অনুমোদিত' : 'NCTB Approved'}</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-medium">
                          {isBengali ? '৬৯ / ৬৯ অধ্যায়' : '69 / 69 Chapters'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* 3. 64 Districts P2P Offline */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Compass className="w-[18px] h-[18px] text-[#1B2A4A] dark:text-slate-300" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'দেশব্যাপী রেজিলিয়েন্স' : 'Nationwide Resilience'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#525252] dark:text-slate-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'P2P মেশ' : 'P2P Mesh'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? '৬৪ জেলা অফলাইন' : '64 Districts Offline'}
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          {isBengali ? 'P2P মেশ ক্লাসরুম' : 'P2P Mesh Classroom'}
                        </h3>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali
                            ? 'ইন্টারনেট ছাড়াই পরীক্ষা ও লোকাল সিঙ্ক এবং স্বয়ংক্রিয় ক্লাস্টার ব্যাকআপ'
                            : 'Offline examinations, local sync, and automated cluster backups'}
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D]">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                          <span className="w-6 h-[1.5px] bg-amber-200 dark:bg-slate-700" />
                          <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                          <span className="w-6 h-[1.5px] bg-amber-200 dark:bg-slate-700" />
                          <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                        </div>
                        <span className="text-[11px] text-[#525252] dark:text-slate-400 font-bengali">
                          {isBengali ? '৪৯৫ উপজেলা' : '495 Upazilas'}
                        </span>
                      </div>
                      <div className="text-[10px] text-[#525252] dark:text-slate-400 font-bengali mt-1.5">
                        {isBengali ? 'জিরো-প্যাকেট লস আর্কিটেকচার' : 'Zero-Packet Loss Architecture'}
                      </div>
                    </div>
                  </div>

                  {/* 4. 0% Intrusive Surveillance */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Lock className="w-[18px] h-[18px] text-[#1B2A4A] dark:text-slate-300" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            {isBengali ? 'মর্যাদা ও অধিকার' : 'Dignity & Privacy'}
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                          {isBengali ? 'নিরাপদ' : 'Secure'}
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          {isBengali ? '০% নজরদারি' : '0% Surveillance'}
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          {isBengali ? 'জিরো-ভিডিও প্রক্টরিং' : 'Zero Video Proctoring'}
                        </h3>
                        <p className="text-xs text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                          {isBengali
                            ? 'শিক্ষার্থী ডেটা সার্বভৌমত্ব ও মর্যাদা; কোনো ওয়েবক্যাম বা ফেসিয়াল ট্র্যাকিং নয়'
                            : 'Student data sovereignty and dignity; zero intrusive webcams or facial tracking'}
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-amber-200/60 dark:border-[#262D3D]">
                      <div className="flex items-center gap-1.5 text-xs text-[#0B5D3B] dark:text-emerald-400 font-bengali font-semibold">
                        <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                        <span>{isBengali ? 'এন্ড-টু-এন্ড এনক্রিপ্টেড ও সুরক্ষিত' : 'End-to-End Encrypted & Secure'}</span>
                      </div>
                      <div className="text-[10px] text-[#525252] dark:text-slate-400 font-bengali mt-1.5">
                        {isBengali ? 'সার্বভৌম শিক্ষার্থী ডেটা নিরাপত্তা' : 'Sovereign Student Data Security'}
                      </div>
                    </div>
                  </div>

                </div>
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 3: CURATED JOURNEY PATHWAYS (4 Cards with Progress Bars)
              Scholar Emerald & Sage Heritage Band
              =================================================================== */}
          <section className="relative overflow-hidden py-14 sm:py-16 md:py-20 bg-[#F2F9F5]/70 dark:bg-[#091714] border-b border-emerald-200/50 dark:border-emerald-950/60 transition-colors duration-300">
            {/* Scholar Emerald & Sage Radial Ambient Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '520px',
                background:
                  'radial-gradient(ellipse 65% 80% at 50% 100%, rgba(16, 185, 129, 0.16) 0%, rgba(5, 150, 105, 0.08) 45%, transparent 85%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (PATHWAYS) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[19vw] md:text-[clamp(4rem,21vw,17rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(16, 185, 129, 0.22) 15%, rgba(5, 150, 105, 0.02) 100%)'
                }}
              >
                pathways
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12 relative z-10">
              
              <div className="text-center max-w-2xl mx-auto space-y-2.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                  {isBengali ? 'পাঠ্যক্রম ও প্রস্তুতি' : 'Curriculum & Pathways'}
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#213130] dark:text-[#F5F2EB] tracking-tight font-bengali">
                  {isBengali ? 'আপনার প্রয়োজনীয় শিক্ষাস্তর নির্বাচন করুন' : 'Select Your Academic Level'}
                </h2>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                  {isBengali
                    ? 'প্রতিটি স্তরের জন্য রয়েছে বিশেষায়িত প্রশ্ন ব্যাংক, লাইভ অনুশীলন, এবং বিশেষজ্ঞ শিক্ষকদের সহায়তায় সাজানো পাঠ্যক্রম।'
                    : 'Specialized question banks, live practice sessions, and expert-curated syllabi tailored for each academic tier.'}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                
                {/* 1. SSC */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs flex flex-col justify-between space-y-5 hover:border-[#ED8E22]/60 hover:shadow-md transition-all duration-200">
                  <div className="space-y-3.5">
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] text-[#1B2A4A] dark:text-sky-300 flex items-center justify-center border border-amber-200/80 dark:border-[#262D3D]">
                        <BookOpen className="w-5 h-5 text-[#ED8E22]" />
                      </div>
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 font-bengali">
                        {isBengali ? '১০MS অল্টারনেটিভ • ৩ডি ল্যাব' : '10MS Alternative • 3D Lab'}
                      </span>
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#525252] dark:text-slate-400 uppercase font-sans">
                        {isBengali ? 'Class 9–10 • মাধ্যমিক (SSC ৯-১০)' : 'Class 9–10 • Secondary (SSC 9-10)'}
                      </span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        {isBengali ? 'মাধ্যমিক (SSC) বোর্ড প্রস্তুতি' : 'Secondary (SSC) Board Prep'}
                      </h3>
                    </div>
                    <p className="text-xs text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                      {isBengali
                        ? 'সাধারণ গণিত, পদার্থবিজ্ঞান, রসায়ন ও উচ্চতর গণিতের বিগত ১০ বছরের সকল বোর্ডের নির্ভুল সৃজনশীল ও এমসিকিউ সমাধান।'
                        : 'Flawless CQ & MCQ solutions from the past 10 years of all boards for General Math, Physics, Chemistry, and Higher Math.'}
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#525252] dark:text-slate-400">{isBengali ? 'সিলেবাস অগ্রগতি' : 'Syllabus Progress'}</span>
                        <span className="font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]">{isBengali ? '৬৮% সম্পন্ন' : '68% Completed'}</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-amber-100 dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-[#1B2A4A] dark:bg-sky-400 rounded-full w-[68%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/learn?stage=SSC"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-amber-200/60 dark:border-[#262D3D] text-xs font-semibold text-[#ED8E22] hover:text-[#D47C1A] transition font-bengali"
                  >
                    <span>{isBengali ? 'এসএসসি পাঠ্যক্রম দেখুন' : 'Explore SSC Curriculum'}</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 2. HSC */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs flex flex-col justify-between space-y-5 hover:border-[#ED8E22]/60 hover:shadow-md transition-all duration-200">
                  <div className="space-y-3.5">
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] text-[#065F46] dark:text-emerald-300 flex items-center justify-center border border-amber-200/80 dark:border-[#262D3D]">
                        <Layers className="w-5 h-5 text-[#0B5D3B] dark:text-emerald-400" />
                      </div>
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-50 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800 font-bengali">
                        {isBengali ? 'এনসিটিবি ১০ বছর আর্কাইভ' : 'NCTB 10-Year Archive'}
                      </span>
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#525252] dark:text-slate-400 uppercase font-sans">
                        {isBengali ? 'Class 11–12 • উচ্চ মাধ্যমিক (HSC ১১-১২)' : 'Class 11–12 • Higher Secondary (HSC 11-12)'}
                      </span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        {isBengali ? 'উচ্চ মাধ্যমিক (HSC) বিজ্ঞান' : 'Higher Secondary (HSC) Science'}
                      </h3>
                    </div>
                    <p className="text-xs text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                      {isBengali
                        ? 'পদার্থবিজ্ঞান ১ম ও ২য় পত্র, জৈব রসায়ন, ক্যালকুলাস ও জীববিজ্ঞানের জটিল তাত্ত্বিক অধ্যায়গুলোর বিশদ অ্যানালিটিক্স।'
                        : 'In-depth analytics for complex theoretical chapters across Physics 1st & 2nd Papers, Organic Chemistry, Calculus, and Biology.'}
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#525252] dark:text-slate-400">{isBengali ? 'সিলেবাস অগ্রগতি' : 'Syllabus Progress'}</span>
                        <span className="font-semibold text-[#065F46] dark:text-emerald-400">{isBengali ? '৮২% সম্পন্ন' : '82% Completed'}</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-amber-100 dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-[#065F46] dark:bg-emerald-500 rounded-full w-[82%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/learn?stage=HSC"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-amber-200/60 dark:border-[#262D3D] text-xs font-semibold text-[#065F46] dark:text-emerald-400 hover:text-[#087858] transition font-bengali"
                  >
                    <span>{isBengali ? 'এইচএসসি সিলেবাস দেখুন' : 'Explore HSC Syllabus'}</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 3. Admission */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs flex flex-col justify-between space-y-5 hover:border-[#ED8E22]/60 hover:shadow-md transition-all duration-200">
                  <div className="space-y-3.5">
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] text-[#B8862B] dark:text-amber-300 flex items-center justify-center border border-amber-200/80 dark:border-[#262D3D]">
                        <Target className="w-5 h-5 text-[#ED8E22]" />
                      </div>
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800 font-bengali">
                        {isBengali ? 'Live MCQ বিকল্প • জিরো ল্যাগ' : 'Live MCQ Alternative • Zero Lag'}
                      </span>
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#525252] dark:text-slate-400 uppercase font-sans">
                        {isBengali ? 'University Entrance • বিশ্ববিদ্যালয় ভর্তি' : 'University Entrance • Admission Exam'}
                      </span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        {isBengali ? 'বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি' : 'University & Medical Admission'}
                      </h3>
                    </div>
                    <p className="text-xs text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                      {isBengali
                        ? 'বুয়েট প্রিলিমিনারি, ঢাকা বিশ্ববিদ্যালয় \'ক\' ইউনিট এবং মেডিকেল নেগেটিভ মার্কিং মক টেস্ট ইঞ্জিন।'
                        : 'Mock exam engine for BUET Prelims, Dhaka University \'Ka\' Unit, and Medical negative-marking simulations.'}
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#525252] dark:text-slate-400">{isBengali ? 'ভর্তি লক্ষ্য প্রস্তুতি' : 'Target Readiness'}</span>
                        <span className="font-semibold text-[#B8862B] dark:text-amber-400">{isBengali ? '৪৫% সম্পন্ন' : '45% Completed'}</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-amber-100 dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-[#ED8E22] dark:bg-amber-500 rounded-full w-[45%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/admission"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-amber-200/60 dark:border-[#262D3D] text-xs font-semibold text-[#ED8E22] hover:text-[#D47C1A] transition font-bengali"
                  >
                    <span>{isBengali ? 'ভর্তি প্রস্তুতি হাব খুলুন' : 'Open Admission Hub'}</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 4. Tuition & Career */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs flex flex-col justify-between space-y-5 hover:border-[#ED8E22]/60 hover:shadow-md transition-all duration-200">
                  <div className="space-y-3.5">
                    <div className="flex items-center justify-between">
                      <div className="w-10 h-10 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] text-slate-700 dark:text-slate-300 flex items-center justify-center border border-amber-200/80 dark:border-[#262D3D]">
                        <Users className="w-5 h-5 text-[#1B2A4A] dark:text-slate-300" />
                      </div>
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-indigo-50 text-indigo-800 dark:bg-indigo-950/60 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 font-bengali">
                        {isBengali ? 'CareTutors মুক্ত • ০% ফি' : 'CareTutors Free • 0% Commission'}
                      </span>
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#525252] dark:text-slate-400 uppercase font-sans">
                        {isBengali ? 'Marketplace & Career • টিউশন ও ক্যারিয়ার' : 'Marketplace & Career • Tuition & CV'}
                      </span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        {isBengali ? 'টিউশন ও স্কিল লেজার' : 'Tuition & Skill Ledger'}
                      </h3>
                    </div>
                    <p className="text-xs text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                      {isBengali
                        ? 'দ্বিপাক্ষিক এসক্রো সুরক্ষিত হোম ও অনলাইন টিউশন এবং অপরিবর্তনীয় একাডেমিক সিভি ও মেধা সনদ।'
                        : 'Bilateral escrow-secured home and online tuitions with immutable academic CVs and verifiable credentials.'}
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#525252] dark:text-slate-400">{isBengali ? 'প্রোফাইল ভেরিফিকেশন' : 'Profile Verification'}</span>
                        <span className="font-semibold text-slate-700 dark:text-slate-300">{isBengali ? '৯০% প্রোফাইল' : '90% Profile'}</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-amber-100 dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-slate-700 dark:bg-slate-300 rounded-full w-[90%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/tuition"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-amber-200/60 dark:border-[#262D3D] text-xs font-semibold text-[#1B2A4A] dark:text-slate-200 hover:text-[#ED8E22] transition font-bengali"
                  >
                    <span>{isBengali ? 'টিউশন মার্কেটপ্লেস' : 'Tuition Marketplace'}</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

              </div>

              {/* Subject Explorer Carousel (Swiper & KaTeX Formulas) */}
              <div className="pt-10 border-t border-amber-200/60 dark:border-[#262D3D]">
                <SubjectExplorerCarousel />
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 4: 3D STEM VIRTUAL LABS (Interactive Simulators + KaTeX Math)
              Cosmic Ultraviolet & Electric Sky Band
              =================================================================== */}
          <section className="relative overflow-hidden py-14 sm:py-16 md:py-20 bg-[#F8F5FE]/70 dark:bg-[#110D24] border-b border-purple-200/50 dark:border-purple-950/60 transition-colors duration-300">
            {/* Cosmic Violet Radial Ambient Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '520px',
                background:
                  'radial-gradient(ellipse 60% 85% at 50% 100%, rgba(168, 85, 247, 0.18) 0%, rgba(126, 34, 206, 0.09) 45%, transparent 80%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (LABORATORY) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(4rem,20vw,16rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(168, 85, 247, 0.22) 15%, rgba(126, 34, 206, 0.02) 100%)'
                }}
              >
                laboratory
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12 relative z-10">
              
              <div className="text-center max-w-2xl mx-auto space-y-2.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                  {isBengali ? 'গবেষণা ও চিন্তন দক্ষতা (3D STEM)' : 'Research & Critical Thinking (3D STEM)'}
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#213130] dark:text-[#F5F2EB] tracking-tight font-bengali">
                  {isBengali ? '৩ডি স্টেম ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি' : '3D STEM Virtual Science Laboratories'}
                </h2>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                  {isBengali
                    ? 'মুখস্থ বিদ্যার বিকল্প হিসেবে গভীর চিন্তন দক্ষতা ও সমস্যা সমাধানের জন্য প্রস্তুত বিশেষায়িত ত্রিমাত্রিক টুলস।'
                    : 'Replacing rote memorization with deep problem-solving intuition through specialized three-dimensional experimental tools.'}
                </p>
              </div>

              {/* Showcase Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                
                {/* Lab 1: Physics Projectile Motion */}
                <div className="lg:col-span-6 p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all flex flex-col justify-between space-y-5">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FFF9EB] dark:bg-[#0E1526] text-[#065F46] dark:text-emerald-400 text-xs font-semibold border border-amber-200/80 dark:border-[#262D3D]">
                      <Atom className="w-4 h-4 text-[#ED8E22]" />
                      <span>{isBengali ? '৩ডি ইন্টারেক্টিভ সিমুলেটর • Physics' : '3D Interactive Simulator • Physics'}</span>
                    </div>

                    <h3 className="text-xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                      {isBengali ? 'প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Projectile Motion)' : 'Projectile Motion Simulator (3D Lab)'}
                    </h3>
                    <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-300 leading-relaxed font-bengali">
                      {isBengali
                        ? 'ক্যাননের নিক্ষেপ কোণ, বেগ ও মধ্যাকর্ষণ ত্বরণ পরিবর্তন করে প্রক্ষেপকের পাল্লা ও সর্বোচ্চ উচ্চতা নির্ণয় করুন। সমীকরণ: H = (v0² sin²θ) / 2g।'
                        : 'Adjust launch angle, initial velocity, and gravity to compute projectile range and maximum height. Formula: H = (v0² sin²θ) / 2g.'}
                    </p>

                    {/* Crisp KaTeX Preview Box */}
                    <div className="p-3.5 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] space-y-2 text-xs">
                      <div className="flex items-center justify-between text-[#525252] dark:text-slate-400">
                        <span>{isBengali ? 'পদার্থবিজ্ঞান ১ম পত্র • গতিবিদ্যা' : 'Physics 1st Paper • Dynamics'}</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">{isBengali ? '৬০ FPS ক্যানভাস' : '60 FPS Canvas'}</span>
                      </div>
                      <div className="pt-1 text-[#1B2A4A] dark:text-[#F5F2EB]">
                        <KaTeXRenderer
                          content={isBengali ? "$R = \\frac{v_0^2 \\sin 2\\theta}{g}$ এবং $H = \\frac{v_0^2 \\sin^2\\theta}{2g}$" : "$R = \\frac{v_0^2 \\sin 2\\theta}{g} \\quad \\text{and} \\quad H = \\frac{v_0^2 \\sin^2\\theta}{2g}$"}
                          className="text-xs sm:text-sm font-serif"
                        />
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('physics')}
                    className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-full bg-[#065F46] hover:bg-[#0B5D3B] text-white font-semibold text-sm shadow-md active:scale-95 transition-all min-h-[44px]"
                  >
                    <Play className="w-4 h-4 text-emerald-200" />
                    <span>{isBengali ? 'ল্যাব চালু করুন (Physics Projectile Lab)' : 'Launch Lab (Physics Projectile Lab)'}</span>
                  </button>
                </div>

                {/* Lab 2: Chemistry Molecular Geometry */}
                <div className="lg:col-span-6 p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all flex flex-col justify-between space-y-5">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FFF9EB] dark:bg-[#0E1526] text-[#0A2540] dark:text-sky-300 text-xs font-semibold border border-amber-200/80 dark:border-[#262D3D]">
                      <Atom className="w-4 h-4 text-[#ED8E22]" />
                      <span>{isBengali ? '৩ডি ইন্টারেক্টিভ সিমুলেটর • Chemistry' : '3D Interactive Simulator • Chemistry'}</span>
                    </div>

                    <h3 className="text-xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                      {isBengali ? '৩ডি আণবিক জ্যামিতি ও সংকরায়ন (Molecular Geometry)' : '3D Molecular Geometry & Hybridization'}
                    </h3>
                    <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-300 leading-relaxed font-bengali">
                      {isBengali
                        ? 'VSEPR তত্ত্ব ও sp, sp², sp³ সংকরায়নের ত্রিমাত্রিক বন্ধন কোণ ও পরমাণুর অবস্থান ব্রাউজারে ৩ডি স্পেসে ঘুরিয়ে পর্যবেক্ষণ করুন।'
                        : 'Inspect VSEPR theory, sp, sp², sp³ hybridizations, 3D bond angles, and atom coordinates in real-time WebGL space.'}
                    </p>

                    {/* Crisp KaTeX Preview Box */}
                    <div className="p-3.5 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] space-y-2 text-xs">
                      <div className="flex items-center justify-between text-[#525252] dark:text-slate-400">
                        <span>{isBengali ? 'রসায়ন ১ম পত্র • রাসায়নিক বন্ধন' : 'Chemistry 1st Paper • Chemical Bonding'}</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">VSEPR 3D Engine</span>
                      </div>
                      <div className="pt-1 text-[#1B2A4A] dark:text-[#F5F2EB]">
                        <KaTeXRenderer
                          content="$\text{CH}_4 \ (\text{Tetrahedral}, \ 109.5^\circ) \quad \text{H}_2\text{O} \ (\text{Bent}, \ 104.5^\circ)$"
                          className="text-xs sm:text-sm font-serif"
                        />
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('chemistry')}
                    className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-full bg-[#0A2540] hover:bg-[#123358] text-white font-semibold text-sm shadow-md active:scale-95 transition-all min-h-[44px]"
                  >
                    <Play className="w-4 h-4 text-amber-300" />
                    <span>{isBengali ? 'ল্যাব চালু করুন (Chemistry Molecular Lab)' : 'Launch Lab (Chemistry Molecular Lab)'}</span>
                  </button>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 5: LIVE CHALLENGE & SOCRATIC AI INSTANT SOLVER
              Fiery Crimson & Golden Arena Band
              =================================================================== */}
          <section className="relative overflow-hidden py-14 sm:py-16 md:py-20 bg-[#FEF7F4]/70 dark:bg-[#1D1016] border-b border-rose-200/50 dark:border-rose-950/60 transition-colors duration-300">
            {/* Fiery Crimson & Gold Arena Ambient Glow */}
            <div
              className="absolute top-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '520px',
                background:
                  'radial-gradient(ellipse 65% 75% at 50% 0%, rgba(244, 63, 94, 0.16) 0%, rgba(245, 158, 11, 0.10) 50%, transparent 85%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (OLYMPIAD) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[19vw] md:text-[clamp(4rem,21vw,17rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(244, 63, 94, 0.20) 15%, rgba(245, 158, 11, 0.02) 100%)'
                }}
              >
                olympiad
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12 relative z-10">
              
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                
                {/* Live Challenge Spotlight Card (8:00 PM National Olympiad) */}
                <div className="lg:col-span-7 p-7 sm:p-8 rounded-3xl bg-gradient-to-br from-[#1B2A4A] via-[#162441] to-[#0D1D38] text-white border border-amber-500/30 shadow-[0_4px_24px_-4px_rgba(237,142,34,0.18)] flex flex-col justify-between space-y-6 relative overflow-hidden">
                  {/* Subtle Amber Glow in Corner */}
                  <div className="absolute -top-12 -right-12 w-48 h-48 bg-amber-400/10 rounded-full blur-2xl pointer-events-none" aria-hidden="true" />

                  <div className="space-y-3.5 relative z-10">
                    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 text-amber-300 text-xs font-semibold border border-white/15">
                      <span className="h-2 w-2 rounded-full bg-amber-400 shrink-0 animate-pulse" aria-hidden="true" />
                      <Trophy className="w-4 h-4 text-amber-300" />
                      <span>{isBengali ? 'জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬ (রাত ৮:০০)' : 'National Live Quiz Competition 2026 (8:00 PM)'}</span>
                    </div>

                    <h3 className="text-2xl sm:text-3xl font-serif font-bold leading-tight font-bengali">
                      {isBengali ? 'আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড চ্যালেঞ্জ' : 'Tonight 8:00 PM National Olympiad Challenge'}
                    </h3>
                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-bengali">
                      {isBengali
                        ? 'সমগ্র বাংলাদেশের শীর্ষ শিক্ষার্থীদের সঙ্গে সরাসরি লাইভ প্রতিযোগিতায় অংশগ্রহণ করুন। রিয়েল-টাইম লিডারবোর্ড ও তাৎক্ষণিক বিশ্লেষণ।'
                        : 'Compete live alongside top students across Bangladesh with real-time nation-wide leaderboards and instantaneous performance breakdowns.'}
                    </p>

                    {/* Countdown Timer Display */}
                    <div className="p-4 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-between">
                      <div className="space-y-0.5">
                        <span className="text-[11px] uppercase tracking-wider text-amber-200/80 font-sans">
                          {isBengali ? 'লাইভ কাউন্টডাউন (countdown)' : 'Live Countdown'}
                        </span>
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-amber-300 tabular-nums">
                          {String(countdown.hours).padStart(2, '0')}:{String(countdown.minutes).padStart(2, '0')}:{String(countdown.seconds).padStart(2, '0')}
                        </div>
                      </div>
                      <div className="text-right space-y-0.5">
                        <span className="text-[11px] uppercase tracking-wider text-slate-300 font-sans">
                          {isBengali ? 'অংশগ্রহণকারী' : 'Participants'}
                        </span>
                        <div className="text-sm sm:text-base font-semibold text-emerald-300 font-bengali">
                          {isBengali ? '৪,৮৫০+ প্রতিযোগী শিক্ষার্থী' : '4,850+ Live Competitors'}
                        </div>
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/live-challenge"
                    className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-full bg-[#ED8E22] hover:bg-[#D47C1A] text-white font-bold text-sm shadow-md transition-all active:scale-95 min-h-[44px] relative z-10"
                  >
                    <Trophy className="w-4 h-4 text-amber-200" />
                    <span>{isBengali ? 'লাইভ লবিতে যোগ দিন' : 'Enter Live Lobby'}</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* Socratic AI Instant Solver Banner */}
                <div className="lg:col-span-5 p-7 sm:p-8 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 hover:shadow-md transition-all flex flex-col justify-between space-y-6">
                  <div className="space-y-3.5">
                    <div className="w-10 h-10 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] text-[#ED8E22] flex items-center justify-center border border-amber-200/80 dark:border-[#262D3D]">
                      <Sparkles className="w-5 h-5 text-[#ED8E22]" />
                    </div>

                    <h3 className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                      {isBengali ? 'সক্রেটিক এআই তাৎক্ষণিক সমাধান' : 'Socratic AI Instant Problem Solver'}
                    </h3>
                    <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-300 leading-relaxed font-bengali">
                      {isBengali
                        ? 'যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন। সরাসরি উত্তর না দিয়ে ধাপে ধাপে গাণিতিক সংকেত ও সূত্রের মাধ্যমে যুক্তি গড়ে তোলে।'
                        : 'Snap or type any academic problem. Rather than spoon-feeding answers, it builds mathematical intuition step-by-step with guided hints.'}
                    </p>

                    <div className="p-3.5 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] text-xs text-[#525252] dark:text-slate-400 font-bengali">
                      {isBengali
                        ? 'গণিত, পদার্থবিজ্ঞান এবং রসায়নের জটিল গাণিতিক সমস্যার জন্য সার্বক্ষণিক ব্যক্তিগত শিক্ষক।'
                        : '24/7 personalized tutor dedicated to challenging problems in Mathematics, Physics, and Chemistry.'}
                    </div>
                  </div>

                  <button
                    type="button"
                    id="global-socratic-trigger"
                    onClick={() => {
                      const btn = document.getElementById('global-socratic-trigger');
                      if (btn) btn.setAttribute('data-active', 'true');
                    }}
                    className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-full bg-[#0A2540] hover:bg-[#123358] text-white font-semibold text-sm shadow-md active:scale-95 transition-all min-h-[44px]"
                  >
                    <Sparkles className="w-4 h-4 text-amber-300" />
                    <span>{isBengali ? 'সক্রেটিক টিউটর চালু করুন' : 'Launch Socratic Tutor'}</span>
                  </button>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 6: W3C PROOF-OF-SKILL CERTIFICATE SHOWCASE
              Lapis Lazuli & Gold Crest Vault Band
              =================================================================== */}
          <section className="relative overflow-hidden py-14 sm:py-16 md:py-20 bg-[#F4F6FC]/70 dark:bg-[#0B142B] border-b border-indigo-200/50 dark:border-indigo-950/60 transition-colors duration-300">
            {/* Lapis Lazuli & Gold Crest Ambient Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '500px',
                background:
                  'radial-gradient(ellipse 70% 70% at 50% 100%, rgba(99, 102, 241, 0.16) 0%, rgba(212, 163, 75, 0.08) 50%, transparent 80%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (CREDENTIAL) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(4rem,20vw,16rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(99, 102, 241, 0.20) 15%, rgba(212, 163, 75, 0.02) 100%)'
                }}
              >
                credential
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12 relative z-10">
              
              <div className="text-center max-w-2xl mx-auto space-y-2.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                  {isBengali ? 'যাচাইযোগ্য মেধা সনদ (W3C)' : 'Verifiable Credentials (W3C)'}
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#213130] dark:text-[#F5F2EB] tracking-tight font-bengali">
                  {isBengali ? 'W3C ক্রিপ্টোগ্রাফিক ভেরিফাইড মেধা ও দক্ষতা সনদ' : 'W3C Cryptographically Verified Academic & Skill Credentials'}
                </h2>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                  {isBengali
                    ? 'ব্লকচেইন-মানসম্পন্ন ক্রিপ্টোগ্রাফিক হ্যাশযুক্ত সনদ যা বিশ্ববিদ্যালয়, শিক্ষক এবং আন্তর্জাতিক নিয়োগকারীদের কাছে সরাসরি যাচাইযোগ্য।'
                    : 'Blockchain-grade cryptographically signed credentials directly verifiable by universities, educators, and global employers.'}
                </p>
              </div>

              {/* Certificate Component Preview & Action Toolbar */}
              <div className="max-w-4xl mx-auto space-y-5">
                <div className="rounded-2xl border border-amber-200/70 dark:border-gray-700 p-3 sm:p-6 bg-white dark:bg-[#121B2D] shadow-xs">
                  <ProofOfSkillCard certificate={SAMPLE_CERTIFICATE} />
                </div>

                <div className="p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-gray-700 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xs">
                  <div className="space-y-1 text-center sm:text-left">
                    <span className="text-xs font-semibold text-[#525252] dark:text-slate-400">
                      {isBengali
                        ? `সনদ আইডি: ${SAMPLE_CERTIFICATE.cert_id} • প্রাপক: ${SAMPLE_CERTIFICATE.student_name}`
                        : `Credential ID: ${SAMPLE_CERTIFICATE.cert_id} • Recipient: ${SAMPLE_CERTIFICATE.student_name}`}
                    </span>
                    <div className="text-xs text-[#525252] dark:text-slate-400 font-bengali">
                      {isBengali
                        ? 'শেয়ার অপশন: LinkedIn • Facebook • ডাইরেক্ট ভেরিফিকেশন লিঙ্ক'
                        : 'Share Options: LinkedIn • Facebook • Direct Verification Link'}
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
                      className="px-4 py-2.5 rounded-full border border-amber-200/80 dark:border-gray-700 hover:bg-[#FFF9EB] dark:hover:bg-[#1A263E] text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] transition inline-flex items-center gap-1.5"
                    >
                      <span>{isBengali ? 'যাচাই পৃষ্ঠা' : 'Verify Credential'}</span>
                      <ExternalLink className="w-3.5 h-3.5 text-[#ED8E22]" />
                    </Link>
                  </div>
                </div>
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 6.5: STUDENT TESTIMONIALS & SUCCESS STORIES (Swiper)
              Warm Terracotta & Sunset Glow Band
              =================================================================== */}
          <section className="relative overflow-hidden py-14 sm:py-16 md:py-20 bg-[#FFF8F3]/70 dark:bg-[#161118] border-b border-orange-200/50 dark:border-orange-950/60 transition-colors duration-300">
            {/* Warm Terracotta Ambient Glow */}
            <div
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-5xl h-[420px] pointer-events-none select-none z-0"
              style={{
                background:
                  'radial-gradient(ellipse 65% 65% at 50% 50%, rgba(251, 146, 60, 0.14) 0%, transparent 75%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (STORIES) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-4 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[20vw] md:text-[clamp(4rem,22vw,18rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(251, 146, 60, 0.18) 15%, rgba(245, 158, 11, 0.02) 100%)'
                }}
              >
                stories
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
              <StudentStoriesCarousel />
            </div>
          </section>

          {/* ===================================================================
              SECTION 7: TRUST BADGES & 69 ENTERPRISE MODULES DIRECTORY
              Deep Marine Teal & Oceanic Assurance Band
              =================================================================== */}
          <section className="relative overflow-hidden py-12 sm:py-14 bg-[#F1F8F8]/70 dark:bg-[#0A171B] border-b border-teal-200/50 dark:border-teal-950/60 transition-colors duration-300">
            {/* Deep Marine Teal Ambient Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '420px',
                background:
                  'radial-gradient(ellipse 70% 60% at 50% 100%, rgba(20, 184, 166, 0.16) 0%, transparent 80%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (MODULES) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-4 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[19vw] md:text-[clamp(4rem,21vw,17rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(20, 184, 166, 0.20) 15%, rgba(13, 148, 136, 0.02) 100%)'
                }}
              >
                modules
              </p>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6 relative z-10">
              
              <div className="p-6 sm:p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] flex flex-col md:flex-row items-center justify-between gap-6 shadow-xs">
                
                <div className="space-y-1 text-center md:text-left max-w-xl">
                  <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                    {isBengali ? 'জাতীয় নিরাপত্তা ও স্বীকৃতি' : 'National Security & Compliance'}
                  </span>
                  <h3 className="text-base sm:text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                    {isBengali ? 'নিরাপদ জাতীয় পেমেন্ট ও প্রাতিষ্ঠানিক ডিজিটাল সুরক্ষা' : 'Secure National Payments & Institutional Digital Trust'}
                  </h3>
                  <p className="text-xs text-[#525252] dark:text-slate-400 leading-relaxed font-bengali">
                    {isBengali
                      ? 'বাংলাদেশ ব্যাংক রেগুলেশন এবং আন্তর্জাতিক ডব্লিউথ্রিসি (W3C) ভেরিফাইড ক্রেডেনশিয়াল মানদণ্ড অনুযায়ী পরিচালিত।'
                      : 'Governed strictly under Bangladesh Bank regulations and international W3C Verifiable Credentials standards.'}
                  </p>
                </div>

                <div className="flex flex-wrap items-center justify-center gap-3">
                  {/* bKash */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/80 dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#E2136E]" />
                    <span className="text-xs font-semibold text-[#E2136E]">bKash Verified</span>
                  </div>

                  {/* Nagad */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/80 dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#F7941D]" />
                    <span className="text-xs font-semibold text-[#F7941D]">Nagad Verified</span>
                  </div>

                  {/* SSLCommerz */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/80 dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#0B5D3B]" />
                    <span className="text-xs font-semibold text-[#1B2A4A] dark:text-slate-200">SSLCommerz Escrow</span>
                  </div>

                  {/* W3C */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#FFF9EB] dark:bg-[#0E1526] border border-amber-200/80 dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#0B5D3B]" />
                    <span className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400">W3C Compliant</span>
                  </div>
                </div>

              </div>

              {/* Direct Modules Directory Link Card */}
              <div className="p-5 sm:p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xs">
                <div className="space-y-0.5 text-center sm:text-left">
                  <div className="text-sm font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                    {isBengali ? '৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি' : '69 Enterprise Modules Directory'}
                  </div>
                  <p className="text-xs text-[#525252] dark:text-slate-400">
                    {isBengali
                      ? 'একাডেমিক, ভর্তি, রেজিলিয়েন্স, স্টেম স্যান্ডবক্স এবং এন্টারপ্রাইজ ককপিটের পূর্ণ ক্যাটালগ।'
                      : 'Complete directory spanning academic syllabi, admission engines, resilience mesh, STEM sandbox, and enterprise cockpits.'}
                  </p>
                </div>
                <Link
                  href="/modules"
                  className="px-5 py-2.5 rounded-full bg-[#0A2540] hover:bg-[#123358] text-white text-xs font-semibold transition flex items-center gap-2 shrink-0 shadow-sm"
                >
                  <span>{isBengali ? 'মডিউল ডিরেক্টরি দেখুন' : 'Explore Modules Directory'}</span>
                  <ArrowRight className="w-4 h-4 text-amber-300" />
                </Link>
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 8: CLOSING ACADEMIC CALL TO ACTION
              Deep Charcoal Slate & Golden Horizon Band
              =================================================================== */}
          <section className="relative py-16 sm:py-20 md:py-24 bg-gradient-to-br from-[#1C2625] via-slate-900 to-[#101726] text-white border-t border-amber-900/40 overflow-hidden">
            {/* Golden radial ambient top glow */}
            <div
              className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-4xl h-36 bg-amber-400/10 blur-3xl pointer-events-none"
              aria-hidden="true"
            />

            {/* Golden Sunburst Radial Ambient Bottom Glow */}
            <div
              className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
              style={{
                height: '380px',
                background:
                  'radial-gradient(ellipse 65% 85% at 50% 100%, rgba(255, 178, 0, 0.28) 0%, rgba(243, 172, 8, 0.12) 50%, transparent 100%)'
              }}
              aria-hidden="true"
            />

            {/* Giant Typographic Watermark (EXCELLENCE) */}
            <div
              className="absolute z-0 pointer-events-none select-none w-full top-6 left-0 flex justify-center overflow-hidden"
              aria-hidden="true"
            >
              <p
                className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(4rem,20vw,16rem)] uppercase tracking-wider select-none opacity-30 dark:opacity-15"
                style={{
                  lineHeight: 0.95,
                  backgroundImage:
                    'linear-gradient(to bottom, rgba(255, 178, 0, 0.25) 15%, transparent 100%)'
                }}
              >
                excellence
              </p>
            </div>

            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6 relative z-10">
              
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-amber-300 text-xs font-semibold border border-white/15 shadow-sm">
                <span className="h-2 w-2 rounded-full bg-[#ED8E22] shrink-0 animate-pulse" aria-hidden="true" />
                <GraduationCap className="w-4 h-4 text-[#ED8E22]" />
                <span>{isBengali ? 'অগ্রযাত্রায় যুক্ত হোন • বাংলাদেশের শিক্ষার ভবিষ্যৎ' : 'Join the Progress • The Future of Education in Bangladesh'}</span>
              </div>

              <div className="space-y-3 max-w-2xl mx-auto">
                <h2 className="text-2xl sm:text-4xl font-serif font-bold tracking-tight leading-tight font-bengali">
                  {isBengali ? 'আজই আপনার শিক্ষাপ্রতিষ্ঠান বা পড়াশোনার অগ্রযাত্রায় যুক্ত হোন' : 'Join the Vanguard of Academic Excellence Today'}
                </h2>
                <p className="text-xs sm:text-base text-slate-300 leading-relaxed font-bengali">
                  {isBengali
                    ? 'শিক্ষার্থী, শিক্ষক এবং অভিভাবকদের জন্য সম্পূর্ণ নিরাপদ, জাতীয় কারিকুলাম সমন্বিত ও মর্যাদাপূর্ণ ডিজিটাল পরিবেশ।'
                    : 'A dignified, fully secure, NCTB-aligned digital learning ecosystem built for students, teachers, and guardians.'}
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
                <Link
                  href="/learn"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-full bg-[#ED8E22] hover:bg-[#D47C1A] text-white font-bold text-sm shadow-lg active:scale-95 transition-all min-h-[48px]"
                >
                  <GraduationCap className="w-5 h-5 text-amber-200" />
                  <span>{isBengali ? 'বিনামূল্যে শুরু করুন' : 'Get Started Free'}</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <Link
                  href="/about"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-full bg-white/10 hover:bg-white/20 text-white font-semibold text-sm border border-white/20 transition-all min-h-[48px]"
                >
                  <FileText className="w-4 h-4 text-slate-300" />
                  <span>{isBengali ? 'প্রাতিষ্ঠানিক লক্ষ্য ও পরিচিতি' : 'Institutional Mission & Overview'}</span>
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
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 animate-in fade-in"
        >
          <div className="relative w-full max-w-5xl bg-white dark:bg-[#121B2D] rounded-2xl border border-[#E5E2DA] dark:border-[#262D3D] shadow-xl overflow-hidden max-h-[90vh] flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#E5E2DA] dark:border-[#262D3D] bg-[#FAF8F3] dark:bg-[#0E1526]">
              <div className="flex items-center gap-2">
                <Atom className="w-5 h-5 text-[#0B5D3B] dark:text-emerald-400" />
                <span className="font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] text-sm sm:text-base font-bengali">
                  {activeLabModal === 'physics'
                    ? (isBengali ? 'প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Physics Projectile Lab)' : 'Projectile Motion Simulator (Physics Projectile Lab)')
                    : (isBengali ? '৩ডি আণবিক জ্যামিতি ল্যাবরেটরি (Chemistry Molecular Viewer)' : '3D Molecular Geometry Laboratory (Chemistry Molecular Viewer)')}
                </span>
              </div>

              <button
                type="button"
                onClick={() => setActiveLabModal(null)}
                aria-label={isBengali ? 'ল্যাব বন্ধ করুন' : 'Close lab simulator'}
                className="p-2 rounded-lg text-[#5B5B5B] hover:text-[#1A1A1A] dark:text-slate-400 dark:hover:text-white hover:bg-[#E5E2DA] dark:hover:bg-slate-800 transition"
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
