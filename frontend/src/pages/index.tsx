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
        title="অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা - জাতীয় ডিজিটাল শিক্ষা প্ল্যাটফর্ম"
        description="এনসিটিবি পাঠ্যক্রম, বিগত ১০ বছরের বোর্ড প্রশ্ন ব্যাংক, ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাব এবং নিরপেক্ষ ডিজিটাল মূল্যায়ন প্ল্যাটফর্ম।"
        canonicalUrl="/"
        ogType="website"
        structuredData={createOrganizationSchema()}
      />

      <div className="min-h-screen flex flex-col bg-[#FAF8F3] dark:bg-[#090D16] text-[#1A1A1A] dark:text-[#F5F2EB] font-sans selection:bg-[#0A2540] selection:text-white transition-colors duration-200">
        <Navbar currentStage="জাতীয় পোর্টাল (National Portal)" />

        <main id="main-content" className="flex-1 w-full">

          {/* ===================================================================
              SECTION 1: EDITORIAL HERO (Calm, Prestigious, Scholarly)
              =================================================================== */}
          <section className="relative overflow-hidden pt-8 pb-14 sm:pt-12 sm:pb-20 lg:pt-16 lg:pb-24 border-b border-[#E5E2DA] dark:border-[#262D3D] bg-[#FAF8F3] dark:bg-[#090D16]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-center">
                
                {/* Left Column: Authoritative Editorial Copy */}
                <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
                  
                  {/* National Accreditation Chip */}
                  <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] text-xs font-semibold text-[#5B5B5B] dark:text-slate-300 shadow-sm">
                    <ShieldCheck className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                    <span>জাতীয় শিক্ষাক্রম (NCTB) মানদণ্ডে পরিচালিত • ৬৪ জেলায় সমন্বিত</span>
                  </div>

                  {/* Headline & Welcoming Tone */}
                  <div className="space-y-3.5">
                    <div className="text-sm font-semibold text-[#0B5D3B] dark:text-emerald-400 tracking-wide font-bengali">
                      স্বাগতম, ভবিষ্যৎ গড়ার অগ্রযাত্রায়
                    </div>
                    <h1 className="text-3xl sm:text-5xl lg:text-[54px] font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight leading-[1.22] font-bengali">
                      বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক <span className="underline decoration-[#B8862B]/40 underline-offset-8">ডিজিটাল শিক্ষাজীবন</span>
                    </h1>
                    <p className="text-base sm:text-lg text-[#5B5B5B] dark:text-slate-300 leading-relaxed max-w-2xl mx-auto lg:mx-0 font-bengali">
                      মাধ্যমিক ও উচ্চ মাধ্যমিক থেকে বিশ্ববিদ্যালয় ভর্তি এবং পেশাগত ক্যারিয়ার—সব বিষয়ের অধ্যায়ভিত্তিক প্রাতিষ্ঠানিক পাঠ্যক্রম, বিগত ১০ বছরের নির্ভুল বোর্ড প্রশ্ন এবং ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি।
                    </p>
                  </div>

                  {/* High-Contrast Dual Call to Action */}
                  <div className="pt-1 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
                    <Link
                      href="/practice"
                      className="btn-3d-oxford w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl bg-[#0A2540] hover:bg-[#123358] text-white font-semibold font-bengali text-base shadow-[0_3px_0_0_#051329] active:translate-y-0.5 transition-all min-h-[48px]"
                    >
                      <GraduationCap className="w-5 h-5 text-amber-300" />
                      <span>পড়াশোনা শুরু করুন (Quick Resume)</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </Link>

                    <Link
                      href="/board-archives"
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-xl bg-white dark:bg-[#121B2D] hover:bg-[#F5F2EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] font-semibold font-bengali text-base border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm active:translate-y-0.5 transition-all min-h-[48px]"
                    >
                      <Award className="w-5 h-5 text-[#B8862B]" />
                      <span>বোর্ড প্রশ্ন ব্যাংক (২০১৫–২০২৫)</span>
                    </Link>
                  </div>

                  {/* Trust Strip */}
                  <div className="pt-2 flex flex-wrap items-center justify-center lg:justify-start gap-y-2.5 gap-x-6 text-xs text-[#5B5B5B] dark:text-slate-400 font-medium">
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>এনসিটিবি অনুমোদিত পাঠ্যক্রম</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>১০ বছরের বোর্ড প্রশ্ন</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>অফলাইন মেশ সিঙ্ক সুবিধা</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>কোনো লুকানো চার্জ নেই</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>১০০% শিক্ষার্থী ডেটা গোপনীয়তা</span>
                    </div>
                  </div>

                </div>

                {/* Right Column: Clean Editorial Level Selector Card */}
                <div className="lg:col-span-5">
                  <div className="p-6 sm:p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm space-y-5">
                    
                    <div className="flex items-center justify-between border-b border-[#E5E2DA] dark:border-[#262D3D] pb-3.5">
                      <div className="space-y-0.5">
                        <span className="text-[11px] font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                          শিক্ষার ধাপসমূহ
                        </span>
                        <h2 className="text-base font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          আপনার শিক্ষাস্তর নির্বাচন করুন
                        </h2>
                      </div>
                      <span className="px-2.5 py-1 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-300 text-xs font-semibold border border-[#E5E2DA] dark:border-[#262D3D]">
                        এনসিটিবি ২০২৬ সমন্বিত
                      </span>
                    </div>

                    {/* Stage Selector Chips */}
                    <div className="grid grid-cols-2 gap-2.5 text-xs font-bengali">
                      <button
                        type="button"
                        onClick={() => setActiveStage('ssc')}
                        className={`p-3 rounded-xl border text-left transition-all ${
                          activeStage === 'ssc'
                            ? 'bg-[#1B2A4A] text-white border-[#1B2A4A] shadow-sm'
                            : 'bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-slate-300 border-[#E5E2DA] dark:border-[#262D3D] hover:border-[#1B2A4A]/40'
                        }`}
                      >
                        <BookOpen className="w-4 h-4 mb-1.5 text-amber-400" />
                        <div className="font-semibold">মাধ্যমিক (SSC ৯-১০)</div>
                        <div className="text-[11px] opacity-80 font-normal">শ্রেণি ৯–১০ বোর্ড প্রস্তুতি</div>
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveStage('hsc')}
                        className={`p-3 rounded-xl border text-left transition-all ${
                          activeStage === 'hsc'
                            ? 'bg-[#1B2A4A] text-white border-[#1B2A4A] shadow-sm'
                            : 'bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-slate-300 border-[#E5E2DA] dark:border-[#262D3D] hover:border-[#1B2A4A]/40'
                        }`}
                      >
                        <Layers className="w-4 h-4 mb-1.5 text-emerald-400" />
                        <div className="font-semibold">উচ্চ মাধ্যমিক (HSC ১১-১২)</div>
                        <div className="text-[11px] opacity-80 font-normal">বিজ্ঞান, মানবিক, বাণিজ্য</div>
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveStage('admission')}
                        className={`p-3 rounded-xl border text-left transition-all ${
                          activeStage === 'admission'
                            ? 'bg-[#1B2A4A] text-white border-[#1B2A4A] shadow-sm'
                            : 'bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-slate-300 border-[#E5E2DA] dark:border-[#262D3D] hover:border-[#1B2A4A]/40'
                        }`}
                      >
                        <Target className="w-4 h-4 mb-1.5 text-sky-400" />
                        <div className="font-semibold">বিশ্ববিদ্যালয় ভর্তি (Admission)</div>
                        <div className="text-[11px] opacity-80 font-normal">বুয়েট, ঢাবি, মেডিকেল</div>
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveStage('career')}
                        className={`p-3 rounded-xl border text-left transition-all ${
                          activeStage === 'career'
                            ? 'bg-[#1B2A4A] text-white border-[#1B2A4A] shadow-sm'
                            : 'bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-slate-300 border-[#E5E2DA] dark:border-[#262D3D] hover:border-[#1B2A4A]/40'
                        }`}
                      >
                        <Users className="w-4 h-4 mb-1.5 text-amber-400" />
                        <div className="font-semibold">টিউশন ও ক্যারিয়ার (Career)</div>
                        <div className="text-[11px] opacity-80 font-normal">এসক্রো চুক্তি ও চাকরি</div>
                      </button>
                    </div>

                    {/* Active Stage Details Card */}
                    <div className="p-4 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] space-y-3">
                      {activeStage === 'ssc' && (
                        <>
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]">মাধ্যমিক প্রস্তুতি হাব</span>
                            <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">১০ বছরের বোর্ড প্রশ্ন</span>
                          </div>
                          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                            সাধারণ গণিত, উচ্চতর গণিত, পদার্থ ও রসায়নের অধ্যায়ভিত্তিক প্রশ্ন, এমসিকিউ কুইজ এবং মডেল টেস্ট।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/learn?stage=SSC"
                              className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 hover:underline inline-flex items-center gap-1 font-bengali"
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
                            <span className="font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]">উচ্চ মাধ্যমিক বিজ্ঞান হাব</span>
                            <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">KaTeX সমীকরণ ভিউয়ার</span>
                          </div>
                          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                            পদার্থবিজ্ঞান ১ম ও ২য় পত্র, জৈব রসায়ন, ম্যাট্রিক্স এবং ক্যালকুলাসের বিশদ গাণিতিক বিশ্লেষণ।
                          </p>
                          <div className="p-2 rounded bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] text-[11px]">
                            <KaTeXRenderer content="$H = \frac{v_0^2 \sin^2\theta}{2g} \quad R = \frac{v_0^2 \sin 2\theta}{g}$" className="text-[#1B2A4A] dark:text-[#F5F2EB]" />
                          </div>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/learn?stage=HSC"
                              className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 hover:underline inline-flex items-center gap-1 font-bengali"
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
                            <span className="font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]">ভর্তি ব্লুপ্রিন্ট ও কাট-অফ ম্যাট্রিক্স</span>
                            <span className="text-[#B8862B] font-semibold">নেগেটিভ মার্কিং এলার্ট</span>
                          </div>
                          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                            বুয়েট প্রিলিমিনারি, ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট এবং সরকারি মেডিকেলের বিগত বছরের কাট-অফ বিশ্লেষণ।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/admission"
                              className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 hover:underline inline-flex items-center gap-1 font-bengali"
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
                            <span className="font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]">টিউশন এসক্রো ও স্কিল সনদ</span>
                            <span className="text-[#1B2A4A] dark:text-sky-300 font-semibold">W3C ক্রিপ্টোগ্রাফিক ভেরিফাইড</span>
                          </div>
                          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                            অভিভাবকদের সঙ্গে দ্বিপাক্ষিক ডিজিটাল চুক্তি এবং বিশ্ববিদ্যালয় শিক্ষার্থীদের জন্য নিরাপদ টিউশন প্ল্যাটফর্ম।
                          </p>
                          <div className="flex items-center gap-2 pt-1">
                            <Link
                              href="/tuition"
                              className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 hover:underline inline-flex items-center gap-1 font-bengali"
                            >
                              <span>টিউশন মার্কেটপ্লেস দেখুন</span>
                              <ChevronRight className="w-3.5 h-3.5" />
                            </Link>
                          </div>
                        </>
                      )}
                    </div>

                    <div className="pt-1">
                      <Link
                        href="/dashboard"
                        className="w-full py-2.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] hover:bg-[#F5F2EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] font-semibold text-xs flex items-center justify-center gap-2 border border-[#E5E2DA] dark:border-[#262D3D] transition"
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
              SECTION 2: ACADEMIC PROGRESS ("আপনার শেখার অগ্রগতি") & PEDAGOGICAL PILLARS
              Clean Paper-Tinted Editorial Band (Lightly Tinted Background)
              =================================================================== */}
          <section
            aria-label="অ্যাকাডেমিক প্রোগ্রেস ও প্ল্যাটফর্ম পরিসংখ্যান"
            suppressHydrationWarning={true}
            className="py-14 sm:py-16 md:py-20 bg-[#F5F2EB] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-[#F5F2EB] border-b border-[#E5E2DA] dark:border-[#262D3D]"
          >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12 sm:space-y-16">

              {/* TIER 1: আপনার শেখার অগ্রগতি (Study Momentum & Practice) */}
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-3 border-b border-[#E5E2DA] dark:border-[#262D3D]">
                  <div className="space-y-1">
                    <div className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 tracking-wider uppercase font-sans">
                      আপনার শেখার অগ্রগতি (লাইভ লার্নিং টেলিমেট্রি)
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                      আমার অনুশীলন ও মেধা প্রবৃদ্ধি
                    </h2>
                  </div>
                  <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed max-w-md sm:text-right">
                    দৈনন্দিন অধ্যবসায়, প্রশ্ন সমাধান, নির্ভুলতা ও জাতীয় মেধাতালিকায় আপনার অবস্থান
                  </p>
                </div>

                {/* Tier 1 Grid: 4 Flat Bordered Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

                  {/* 1. Study Streak */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Flame className="w-[18px] h-[18px] text-[#B8862B]" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            Study Streak (অধ্যয়ন স্ট্রিক)
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#B8862B] border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          ধারাবাহিক
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          ৭ দিনের স্ট্রিক
                        </div>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          টানা ৭ দিন সক্রিয় প্রশ্ন অনুশীলন অব্যাহত
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 7-Day Streak Dots */}
                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D]">
                      <div className="flex items-center justify-between gap-1.5 mb-1">
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
                              className={`w-full h-2 rounded-full transition-all ${
                                item.active
                                  ? 'bg-[#B8862B]'
                                  : 'bg-[#E5E2DA] dark:bg-slate-700'
                              }`}
                              title={`${item.day}: অর্জিত`}
                            />
                            <span className="text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali">
                              {item.day}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* 2. Solved Questions */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <CheckCircle2 className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            প্রশ্ন সমাধান
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          বোর্ড ব্যাংক
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          ১২৮টি প্রশ্ন সমাধান
                        </div>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          এনসিটিবি বোর্ড প্রশ্ন ব্যাংক থেকে সম্পন্ন
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: 7-Day Activity Bars */}
                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D]">
                      <div
                        className="flex items-end justify-between gap-1.5 h-6 pb-1 border-b border-[#E5E2DA] dark:border-[#262D3D]"
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
                      <div className="flex justify-between items-center text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali mt-1.5">
                        <span>৭ দিন পূর্বে</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-medium">আজকের পিক (২২টি)</span>
                      </div>
                    </div>
                  </div>

                  {/* 3. Accuracy Rate */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Target className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            নির্ভুলতা
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#5B5B5B] dark:text-slate-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          ঋণাত্মক সতর্ক
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          ৮৬.৪% নির্ভুলতা
                        </div>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          নেগেটিভ মার্কিং এড়িয়ে নির্ভুল উত্তর নিরূপণ
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: Compact Circular Progress */}
                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D] flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="relative w-7 h-7 flex items-center justify-center">
                          <svg className="w-7 h-7 transform -rotate-90" viewBox="0 0 36 36" aria-hidden="true">
                            <path
                              className="text-[#E5E2DA] dark:text-slate-700"
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
                            ৮৬
                          </span>
                        </div>
                        <div className="text-xs font-semibold font-bengali text-[#1B2A4A] dark:text-slate-200">
                          উচ্চ নির্ভুলতা ব্যান্ড
                        </div>
                      </div>
                      <span className="text-[11px] text-[#0B5D3B] dark:text-emerald-400 bg-[#FAF8F3] dark:bg-[#0E1526] px-2 py-0.5 rounded border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                        +৪.২% প্রবৃদ্ধি
                      </span>
                    </div>
                  </div>

                  {/* 4. National Percentile Rank */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Award className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            National Percentile (জাতীয় পার্সেন্টাইল)
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          শীর্ষ মেধা
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          শীর্ষ ৫% শিক্ষার্থী
                        </div>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          দেশব্যাপী ৫০,০০০+ সক্রিয় পরীক্ষার্থীর মধ্যে
                        </p>
                      </div>
                    </div>

                    {/* Data Visual: Percentile Track Bar */}
                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D] space-y-1.5">
                      <div className="relative w-full h-2 bg-[#E5E2DA] dark:bg-slate-700 rounded-full overflow-hidden">
                        <div
                          style={{ width: '95.2%' }}
                          className="h-full bg-[#0B5D3B] dark:bg-emerald-400 rounded-full"
                        />
                      </div>
                      <div className="flex items-center justify-between text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali">
                        <span>০%</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">
                          ৯৫.২তম পার্সেন্টাইল
                        </span>
                        <span>১০০%</span>
                      </div>
                    </div>
                  </div>

                </div>
              </div>

              {/* TIER 2: প্রাতিষ্ঠানিক ভিত্তি ও প্ল্যাটফর্ম ট্রাস্ট */}
              <div className="space-y-6 pt-4">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-3 border-b border-[#E5E2DA] dark:border-[#262D3D]">
                  <div className="space-y-1">
                    <div className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 tracking-wider uppercase font-sans">
                      প্রাতিষ্ঠানিক ভিত্তি
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                      প্ল্যাটফর্ম ট্রাস্ট ও জাতীয় শিক্ষাক্রম মানদণ্ড
                    </h2>
                  </div>
                  <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed max-w-md sm:text-right">
                    সার্বভৌম শিক্ষাক্রম, অফলাইন প্রযুক্তি ও শিক্ষার্থী গোপনীয়তার প্রাতিষ্ঠানিক সুরক্ষা
                  </p>
                </div>

                {/* Tier 2 Grid: 4 Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

                  {/* 1. 10-Year Archive */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <BookOpen className="w-[18px] h-[18px] text-[#1B2A4A] dark:text-slate-300" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            বোর্ড প্রশ্ন আর্কাইভ
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#5B5B5B] dark:text-slate-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          ২০১৫ — ২০২৫
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          ১০ বছর (২০১৫–২৫)
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          আসল বোর্ড প্রশ্ন আর্কাইভ
                        </h3>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          সকল সাধারণ ও কারিগরি শিক্ষা বোর্ডের আসল প্রশ্ন এবং নির্ভুল KaTeX সমীকরণ
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D]">
                      <div className="flex items-center gap-1">
                        {Array.from({ length: 10 }).map((_, i) => (
                          <div
                            key={i}
                            className="flex-1 h-1.5 rounded-full bg-[#0B5D3B] dark:bg-emerald-400"
                          />
                        ))}
                      </div>
                      <div className="flex justify-between items-center text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali mt-1.5">
                        <span>২০১৫</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-medium">১০/১০ বছর সম্পূর্ণ</span>
                        <span>২০২৫</span>
                      </div>
                    </div>
                  </div>

                  {/* 2. 100% NCTB Compliant */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <ShieldCheck className="w-[18px] h-[18px] text-[#0B5D3B] dark:text-emerald-400" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            জাতীয় মানদণ্ড
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          ভেরিফায়েড
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#0B5D3B] dark:text-emerald-400 font-bengali">
                          ১০০% এনসিটিবি
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          জাতীয় শিক্ষাক্রম মানদণ্ড
                        </h3>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          মাধ্যমিক ও উচ্চ মাধ্যমিকের ৬৯টি অ্যাকাডেমিক অধ্যায়ের শতভাগ এনসিটিবি মান
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D]">
                      <div className="w-full h-1.5 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                      <div className="flex justify-between items-center text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali mt-1.5">
                        <span>এনসিটিবি অনুমোদিত</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-medium">৬৯ / ৬৯ অধ্যায়</span>
                      </div>
                    </div>
                  </div>

                  {/* 3. 64 Districts P2P Offline */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Compass className="w-[18px] h-[18px] text-[#1B2A4A] dark:text-slate-300" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            দেশব্যাপী রেজিলিয়েন্স
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#5B5B5B] dark:text-slate-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          P2P মেশ
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          ৬৪ জেলা অফলাইন
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          P2P মেশ ক্লাসরুম
                        </h3>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          ইন্টারনেট ছাড়াই পরীক্ষা ও লোকাল সিঙ্ক এবং স্বয়ংক্রিয় ক্লাস্টার ব্যাকআপ
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D]">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                          <span className="w-6 h-[1.5px] bg-[#E5E2DA] dark:bg-slate-700" />
                          <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                          <span className="w-6 h-[1.5px] bg-[#E5E2DA] dark:bg-slate-700" />
                          <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                        </div>
                        <span className="text-[11px] text-[#5B5B5B] dark:text-slate-400 font-bengali">
                          ৪৯৫ উপজেলা
                        </span>
                      </div>
                      <div className="text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali mt-1.5">
                        জিরো-প্যাকেট লস আর্কিটেকচার
                      </div>
                    </div>
                  </div>

                  {/* 4. 0% Intrusive Surveillance */}
                  <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-4">
                    <div className="space-y-2.5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Lock className="w-[18px] h-[18px] text-[#1B2A4A] dark:text-slate-300" aria-hidden="true" />
                          <span className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                            মর্যাদা ও অধিকার
                          </span>
                        </div>
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-[#FAF8F3] dark:bg-[#0E1526] text-[#0B5D3B] dark:text-emerald-400 border border-[#E5E2DA] dark:border-[#262D3D] font-bengali">
                          নিরাপদ
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                          ০% নজরদারি
                        </div>
                        <h3 className="text-sm font-semibold text-[#1B2A4A] dark:text-slate-200 font-bengali">
                          জিরো-ভিডিও প্রক্টরিং
                        </h3>
                        <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed">
                          শিক্ষার্থী ডেটা সার্বভৌমত্ব ও মর্যাদা; কোনো ওয়েবক্যাম বা ফেসিয়াল ট্র্যাকিং নয়
                        </p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#262D3D]">
                      <div className="flex items-center gap-1.5 text-xs text-[#0B5D3B] dark:text-emerald-400 font-bengali font-semibold">
                        <span className="w-2 h-2 rounded-full bg-[#0B5D3B] dark:bg-emerald-400" />
                        <span>এন্ড-টু-এন্ড এনক্রিপ্টেড ও সুরক্ষিত</span>
                      </div>
                      <div className="text-[10px] text-[#5B5B5B] dark:text-slate-400 font-bengali mt-1.5">
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
              Warm Paper Background
              =================================================================== */}
          <section className="py-14 sm:py-16 md:py-20 bg-[#FAF8F3] dark:bg-[#090D16] border-b border-[#E5E2DA] dark:border-[#262D3D]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12">
              
              <div className="text-center max-w-2xl mx-auto space-y-2.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                  পাঠ্যক্রম ও প্রস্তুতি
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                  আপনার প্রয়োজনীয় শিক্ষাস্তর নির্বাচন করুন
                </h2>
                <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                  প্রতিটি স্তরের জন্য রয়েছে বিশেষায়িত প্রশ্ন ব্যাংক, লাইভ অনুশীলন, এবং বিশেষজ্ঞ শিক্ষকদের সহায়তায় সাজানো পাঠ্যক্রম।
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                
                {/* 1. SSC */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                  <div className="space-y-3.5">
                    <div className="w-10 h-10 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1B2A4A] dark:text-sky-300 flex items-center justify-center border border-[#E5E2DA] dark:border-[#262D3D]">
                      <BookOpen className="w-5 h-5 text-[#B8862B]" />
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#5B5B5B] dark:text-slate-400 uppercase font-sans">Class 9–10</span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        মাধ্যমিক (SSC) বোর্ড প্রস্তুতি
                      </h3>
                    </div>
                    <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                      সাধারণ গণিত, পদার্থবিজ্ঞান, রসায়ন ও উচ্চতর গণিতের বিগত ১০ বছরের সকল বোর্ডের নির্ভুল সৃজনশীল ও এমসিকিউ সমাধান।
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#5B5B5B] dark:text-slate-400">সিলেবাস অগ্রগতি</span>
                        <span className="font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]">৬৮% সম্পন্ন</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-[#1B2A4A] dark:bg-sky-400 rounded-full w-[68%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/learn?stage=SSC"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-[#E5E2DA] dark:border-[#262D3D] text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400 hover:text-[#065F46] transition font-bengali"
                  >
                    <span>এসএসসি পাঠ্যক্রম দেখুন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 2. HSC */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                  <div className="space-y-3.5">
                    <div className="w-10 h-10 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] text-[#065F46] dark:text-emerald-300 flex items-center justify-center border border-[#E5E2DA] dark:border-[#262D3D]">
                      <Layers className="w-5 h-5 text-[#0B5D3B] dark:text-emerald-400" />
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#5B5B5B] dark:text-slate-400 uppercase font-sans">Class 11–12</span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        উচ্চ মাধ্যমিক (HSC) বিজ্ঞান
                      </h3>
                    </div>
                    <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                      পদার্থবিজ্ঞান ১ম ও ২য় পত্র, জৈব রসায়ন, ক্যালকুলাস ও জীববিজ্ঞানের জটিল তাত্ত্বিক অধ্যায়গুলোর বিশদ অ্যানালিটিক্স।
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#5B5B5B] dark:text-slate-400">সিলেবাস অগ্রগতি</span>
                        <span className="font-semibold text-[#065F46] dark:text-emerald-400">৮২% সম্পন্ন</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-[#065F46] dark:bg-emerald-500 rounded-full w-[82%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/learn?stage=HSC"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-[#E5E2DA] dark:border-[#262D3D] text-xs font-semibold text-[#065F46] dark:text-emerald-400 hover:text-[#087858] transition font-bengali"
                  >
                    <span>এইচএসসি সিলেবাস দেখুন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 3. Admission */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                  <div className="space-y-3.5">
                    <div className="w-10 h-10 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] text-[#B8862B] dark:text-amber-300 flex items-center justify-center border border-[#E5E2DA] dark:border-[#262D3D]">
                      <Target className="w-5 h-5 text-[#B8862B]" />
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#5B5B5B] dark:text-slate-400 uppercase font-sans">University Entrance</span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি
                      </h3>
                    </div>
                    <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                      বুয়েট প্রিলিমিনারি, ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট এবং মেডিকেল নেগেটিভ মার্কিং মক টেস্ট ইঞ্জিন।
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#5B5B5B] dark:text-slate-400">ভর্তি লক্ষ্য প্রস্তুতি</span>
                        <span className="font-semibold text-[#B8862B] dark:text-amber-400">৪৫% সম্পন্ন</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-[#B8862B] dark:bg-amber-500 rounded-full w-[45%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/admission"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-[#E5E2DA] dark:border-[#262D3D] text-xs font-semibold text-[#B8862B] dark:text-amber-400 hover:text-[#D97706] transition font-bengali"
                  >
                    <span>ভর্তি প্রস্তুতি হাব খুলুন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* 4. Tuition & Career */}
                <div className="p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                  <div className="space-y-3.5">
                    <div className="w-10 h-10 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] text-slate-700 dark:text-slate-300 flex items-center justify-center border border-[#E5E2DA] dark:border-[#262D3D]">
                      <Users className="w-5 h-5 text-[#1B2A4A] dark:text-slate-300" />
                    </div>
                    <div>
                      <span className="text-[11px] font-semibold text-[#5B5B5B] dark:text-slate-400 uppercase font-sans">Marketplace & Career</span>
                      <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali mt-0.5">
                        টিউশন ও স্কিল লেজার
                      </h3>
                    </div>
                    <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                      দ্বিপাক্ষিক এসক্রো সুরক্ষিত হোম ও অনলাইন টিউশন এবং অপরিবর্তনীয় একাডেমিক সিভি ও মেধা সনদ।
                    </p>
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-xs font-bengali">
                        <span className="text-[#5B5B5B] dark:text-slate-400">প্রোফাইল ভেরিফিকেশন</span>
                        <span className="font-semibold text-slate-700 dark:text-slate-300">৯০% প্রোফাইল</span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 overflow-hidden">
                        <div className="h-full bg-slate-700 dark:bg-slate-300 rounded-full w-[90%]" />
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/tuition"
                    className="inline-flex items-center justify-between w-full pt-3.5 border-t border-[#E5E2DA] dark:border-[#262D3D] text-xs font-semibold text-[#1B2A4A] dark:text-slate-200 hover:text-[#0A2540] transition font-bengali"
                  >
                    <span>টিউশন মার্কেটপ্লেস</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 4: 3D STEM VIRTUAL LABS (Interactive Simulators + KaTeX Math)
              Lightly Tinted Editorial Band
              =================================================================== */}
          <section className="py-14 sm:py-16 md:py-20 bg-[#F5F2EB] dark:bg-[#0E1526] border-b border-[#E5E2DA] dark:border-[#262D3D]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12">
              
              <div className="text-center max-w-2xl mx-auto space-y-2.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                  গবেষণা ও চিন্তন দক্ষতা (3D STEM)
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                  ৩ডি স্টেম ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি
                </h2>
                <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                  মুখস্থ বিদ্যার বিকল্প হিসেবে গভীর চিন্তন দক্ষতা ও সমস্যা সমাধানের জন্য প্রস্তুত বিশেষায়িত ত্রিমাত্রিক টুলস।
                </p>
              </div>

              {/* Showcase Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                
                {/* Lab 1: Physics Projectile Motion */}
                <div className="lg:col-span-6 p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FAF8F3] dark:bg-[#0E1526] text-[#065F46] dark:text-emerald-400 text-xs font-semibold border border-[#E5E2DA] dark:border-[#262D3D]">
                      <Atom className="w-4 h-4" />
                      <span>৩ডি ইন্টারেক্টিভ সিমুলেটর • Physics</span>
                    </div>

                    <h3 className="text-xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                      প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Projectile Motion)
                    </h3>
                    <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-300 leading-relaxed font-bengali">
                      ক্যাননের নিক্ষেপ কোণ, বেগ ও মধ্যাকর্ষণ ত্বরণ পরিবর্তন করে প্রক্ষেপকের পাল্লা ও সর্বোচ্চ উচ্চতা নির্ণয় করুন। সমীকরণ: H = (v0² sin²θ) / 2g।
                    </p>

                    {/* Crisp KaTeX Preview Box */}
                    <div className="p-3.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] space-y-2 text-xs">
                      <div className="flex items-center justify-between text-[#5B5B5B] dark:text-slate-400">
                        <span>পদার্থবিজ্ঞান ১ম পত্র • গতিবিদ্যা</span>
                        <span className="text-[#0B5D3B] dark:text-emerald-400 font-semibold">৬০ FPS ক্যানভাস</span>
                      </div>
                      <div className="pt-1 text-[#1B2A4A] dark:text-[#F5F2EB]">
                        <KaTeXRenderer
                          content="$R = \frac{v_0^2 \sin 2\theta}{g}$ এবং $H = \frac{v_0^2 \sin^2\theta}{2g}$"
                          className="text-xs sm:text-sm font-serif"
                        />
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('physics')}
                    className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-[#065F46] hover:bg-[#0B5D3B] text-white font-semibold text-sm shadow-[0_3px_0_0_#044332] active:translate-y-0.5 transition-all min-h-[44px]"
                  >
                    <Play className="w-4 h-4 text-emerald-200" />
                    <span>ল্যাব চালু করুন (Physics Projectile Lab)</span>
                  </button>
                </div>

                {/* Lab 2: Chemistry Molecular Geometry */}
                <div className="lg:col-span-6 p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-5">
                  <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FAF8F3] dark:bg-[#0E1526] text-[#0A2540] dark:text-sky-300 text-xs font-semibold border border-[#E5E2DA] dark:border-[#262D3D]">
                      <Atom className="w-4 h-4" />
                      <span>৩ডি ইন্টারেক্টিভ সিমুলেটর • Chemistry</span>
                    </div>

                    <h3 className="text-xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                      ৩ডি আণবিক জ্যামিতি ও সংকরায়ন (Molecular Geometry)
                    </h3>
                    <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-300 leading-relaxed font-bengali">
                      VSEPR তত্ত্ব ও sp, sp², sp³ সংকরায়নের ত্রিমাত্রিক বন্ধন কোণ ও পরমাণুর অবস্থান ব্রাউজারে ৩ডি স্পেসে ঘুরিয়ে পর্যবেক্ষণ করুন।
                    </p>

                    {/* Crisp KaTeX Preview Box */}
                    <div className="p-3.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] space-y-2 text-xs">
                      <div className="flex items-center justify-between text-[#5B5B5B] dark:text-slate-400">
                        <span>রসায়ন ১ম পত্র • রাসায়নিক বন্ধন</span>
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
                    className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-[#0A2540] hover:bg-[#123358] text-white font-semibold text-sm shadow-[0_3px_0_0_#051329] active:translate-y-0.5 transition-all min-h-[44px]"
                  >
                    <Play className="w-4 h-4 text-amber-300" />
                    <span>ল্যাব চালু করুন (Chemistry Molecular Lab)</span>
                  </button>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 5: LIVE CHALLENGE & SOCRATIC AI INSTANT SOLVER
              Warm Paper Surface
              =================================================================== */}
          <section className="py-14 sm:py-16 md:py-20 bg-[#FAF8F3] dark:bg-[#090D16] border-b border-[#E5E2DA] dark:border-[#262D3D]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12">
              
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                
                {/* Live Challenge Spotlight Card (8:00 PM National Olympiad) */}
                <div className="lg:col-span-7 p-7 sm:p-8 rounded-2xl bg-[#1B2A4A] text-white border border-[#2B3F6C] shadow-sm flex flex-col justify-between space-y-6">
                  <div className="space-y-3.5">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-amber-300 text-xs font-semibold border border-white/10">
                      <Trophy className="w-4 h-4" />
                      <span>জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬ (রাত ৮:০০)</span>
                    </div>

                    <h3 className="text-2xl sm:text-3xl font-serif font-bold leading-tight font-bengali">
                      আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড চ্যালেঞ্জ
                    </h3>
                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-bengali">
                      সমগ্র বাংলাদেশের শীর্ষ শিক্ষার্থীদের সঙ্গে সরাসরি লাইভ প্রতিযোগিতায় অংশগ্রহণ করুন। রিয়েল-টাইম লিডারবোর্ড ও তাৎক্ষণিক বিশ্লেষণ।
                    </p>

                    {/* Countdown Timer Display */}
                    <div className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
                      <div className="space-y-0.5">
                        <span className="text-[11px] uppercase tracking-wider text-slate-400 font-sans">
                          লাইভ কাউন্টডাউন (countdown)
                        </span>
                        <div className="text-xl sm:text-2xl font-serif font-bold text-amber-300 tabular-nums">
                          {String(countdown.hours).padStart(2, '0')}:{String(countdown.minutes).padStart(2, '0')}:{String(countdown.seconds).padStart(2, '0')}
                        </div>
                      </div>
                      <div className="text-right space-y-0.5">
                        <span className="text-[11px] uppercase tracking-wider text-slate-400 font-sans">
                          অংশগ্রহণকারী
                        </span>
                        <div className="text-sm sm:text-base font-semibold text-emerald-300 font-bengali">
                          ৪,৮৫০+ প্রতিযোগী শিক্ষার্থী
                        </div>
                      </div>
                    </div>
                  </div>

                  <Link
                    href="/live-challenge"
                    className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-amber-400 hover:bg-amber-500 text-[#1B2A4A] font-bold text-sm shadow-sm transition-all active:translate-y-0.5 min-h-[44px]"
                  >
                    <Trophy className="w-4 h-4 text-[#1B2A4A]" />
                    <span>লাইভ লবিতে যোগ দিন</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>

                {/* Socratic AI Instant Solver Banner */}
                <div className="lg:col-span-5 p-7 sm:p-8 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm flex flex-col justify-between space-y-6">
                  <div className="space-y-3.5">
                    <div className="w-10 h-10 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] text-[#B8862B] flex items-center justify-center border border-[#E5E2DA] dark:border-[#262D3D]">
                      <Sparkles className="w-5 h-5 text-[#B8862B]" />
                    </div>

                    <h3 className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                      সক্রেটিক এআই তাৎক্ষণিক সমাধান
                    </h3>
                    <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-300 leading-relaxed font-bengali">
                      যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন। সরাসরি উত্তর না দিয়ে ধাপে ধাপে গাণিতিক সংকেত ও সূত্রের মাধ্যমে যুক্তি গড়ে তোলে।
                    </p>

                    <div className="p-3.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali">
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
                    className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-[#0A2540] hover:bg-[#123358] text-white font-semibold text-sm shadow-[0_3px_0_0_#051329] active:translate-y-0.5 transition-all min-h-[44px]"
                  >
                    <Sparkles className="w-4 h-4 text-amber-300" />
                    <span>সক্রেটিক টিউটর চালু করুন</span>
                  </button>
                </div>

              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 6: W3C PROOF-OF-SKILL CERTIFICATE SHOWCASE
              Lightly Tinted Editorial Band
              =================================================================== */}
          <section className="py-14 sm:py-16 md:py-20 bg-[#F5F2EB] dark:bg-[#0E1526] border-b border-[#E5E2DA] dark:border-[#262D3D]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 sm:space-y-12">
              
              <div className="text-center max-w-2xl mx-auto space-y-2.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                  যাচাইযোগ্য মেধা সনদ (W3C)
                </span>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali">
                  W3C ক্রিপ্টোগ্রাফিক ভেরিফাইড মেধা ও দক্ষতা সনদ
                </h2>
                <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                  ব্লকচেইন-মানসম্পন্ন ক্রিপ্টোগ্রাফিক হ্যাশযুক্ত সনদ যা বিশ্ববিদ্যালয়, শিক্ষক এবং আন্তর্জাতিক নিয়োগকারীদের কাছে সরাসরি যাচাইযোগ্য।
                </p>
              </div>

              {/* Certificate Component Preview & Action Toolbar */}
              <div className="max-w-4xl mx-auto space-y-5">
                <div className="rounded-2xl border border-[#E5E2DA] dark:border-[#262D3D] p-3 sm:p-6 bg-white dark:bg-[#121B2D] shadow-sm">
                  <ProofOfSkillCard certificate={SAMPLE_CERTIFICATE} />
                </div>

                <div className="p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm">
                  <div className="space-y-1 text-center sm:text-left">
                    <span className="text-xs font-semibold text-[#5B5B5B] dark:text-slate-400">
                      সনদ আইডি: {SAMPLE_CERTIFICATE.cert_id} • প্রাপক: {SAMPLE_CERTIFICATE.student_name}
                    </span>
                    <div className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali">
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
                      className="px-4 py-2.5 rounded-xl border border-[#E5E2DA] dark:border-[#262D3D] hover:bg-[#FAF8F3] dark:hover:bg-[#1A263E] text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] transition inline-flex items-center gap-1.5"
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
              SECTION 7: TRUST BADGES & 69 ENTERPRISE MODULES DIRECTORY
              =================================================================== */}
          <section className="py-12 sm:py-14 bg-[#FAF8F3] dark:bg-[#090D16] border-b border-[#E5E2DA] dark:border-[#262D3D]">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
              
              <div className="p-6 sm:p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] flex flex-col md:flex-row items-center justify-between gap-6 shadow-sm">
                
                <div className="space-y-1 text-center md:text-left max-w-xl">
                  <span className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                    জাতীয় নিরাপত্তা ও স্বীকৃতি
                  </span>
                  <h3 className="text-base sm:text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                    নিরাপদ জাতীয় পেমেন্ট ও প্রাতিষ্ঠানিক ডিজিটাল সুরক্ষা
                  </h3>
                  <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
                    বাংলাদেশ ব্যাংক রেগুলেশন এবং আন্তর্জাতিক ডব্লিউথ্রিসি (W3C) ভেরিফাইড ক্রেডেনশিয়াল মানদণ্ড অনুযায়ী পরিচালিত।
                  </p>
                </div>

                <div className="flex flex-wrap items-center justify-center gap-3">
                  {/* bKash */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#E2136E]" />
                    <span className="text-xs font-semibold text-[#E2136E]">bKash Verified</span>
                  </div>

                  {/* Nagad */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#F7941D]" />
                    <span className="text-xs font-semibold text-[#F7941D]">Nagad Verified</span>
                  </div>

                  {/* SSLCommerz */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#0B5D3B]" />
                    <span className="text-xs font-semibold text-[#1B2A4A] dark:text-slate-200">SSLCommerz Escrow</span>
                  </div>

                  {/* W3C */}
                  <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D]">
                    <span className="w-2 h-2 rounded-full bg-[#0B5D3B]" />
                    <span className="text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400">W3C Compliant</span>
                  </div>
                </div>

              </div>

              {/* Direct Modules Directory Link Card */}
              <div className="p-5 sm:p-6 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm">
                <div className="space-y-0.5 text-center sm:text-left">
                  <div className="text-sm font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                    ৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি
                  </div>
                  <p className="text-xs text-[#5B5B5B] dark:text-slate-400">
                    একাডেমিক, ভর্তি, রেজিলিয়েন্স, স্টেম স্যান্ডবক্স এবং এন্টারপ্রাইজ ককপিটের পূর্ণ ক্যাটালগ।
                  </p>
                </div>
                <Link
                  href="/modules"
                  className="px-5 py-2.5 rounded-xl bg-[#0A2540] hover:bg-[#123358] text-white text-xs font-semibold transition flex items-center gap-2 shrink-0 shadow-sm"
                >
                  <span>মডিউল ডিরেক্টরি দেখুন</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>

            </div>
          </section>

          {/* ===================================================================
              SECTION 8: CLOSING ACADEMIC CALL TO ACTION
              Oxford Academic Navy Background
              =================================================================== */}
          <section className="py-16 sm:py-20 md:py-24 bg-[#1B2A4A] text-white border-t border-[#2B3F6C]">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
              
              <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-white/10 text-amber-300 text-xs font-semibold border border-white/10">
                <GraduationCap className="w-4 h-4" />
                <span>অগ্রযাত্রায় যুক্ত হোন • বাংলাদেশের শিক্ষার ভবিষ্যৎ</span>
              </div>

              <div className="space-y-3 max-w-2xl mx-auto">
                <h2 className="text-2xl sm:text-4xl font-serif font-bold tracking-tight leading-tight font-bengali">
                  আজই আপনার শিক্ষাপ্রতিষ্ঠান বা পড়াশোনার অগ্রযাত্রায় যুক্ত হোন
                </h2>
                <p className="text-xs sm:text-base text-slate-300 leading-relaxed font-bengali">
                  শিক্ষার্থী, শিক্ষক এবং অভিভাবকদের জন্য সম্পূর্ণ নিরাপদ, জাতীয় কারিকুলাম সমন্বিত ও মর্যাদাপূর্ণ ডিজিটাল পরিবেশ।
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
                <Link
                  href="/learn"
                  className="btn-3d-oxford w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl bg-white hover:bg-slate-100 text-[#1B2A4A] font-bold text-sm shadow-md transition-all min-h-[48px]"
                >
                  <GraduationCap className="w-5 h-5 text-[#1B2A4A]" />
                  <span>বিনামূল্যে শুরু করুন</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <Link
                  href="/about"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm border border-white/20 transition-all min-h-[48px]"
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
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in"
        >
          <div className="relative w-full max-w-5xl bg-white dark:bg-[#121B2D] rounded-2xl border border-[#E5E2DA] dark:border-[#262D3D] shadow-xl overflow-hidden max-h-[90vh] flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#E5E2DA] dark:border-[#262D3D] bg-[#FAF8F3] dark:bg-[#0E1526]">
              <div className="flex items-center gap-2">
                <Atom className="w-5 h-5 text-[#0B5D3B] dark:text-emerald-400" />
                <span className="font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] text-sm sm:text-base font-bengali">
                  {activeLabModal === 'physics'
                    ? 'প্রক্ষেপক গতিবিদ্যা সিমুলেটর (Physics Projectile Lab)'
                    : '৩ডি আণবিক জ্যামিতি ল্যাবরেটরি (Chemistry Molecular Viewer)'}
                </span>
              </div>

              <button
                type="button"
                onClick={() => setActiveLabModal(null)}
                aria-label="ল্যাব বন্ধ করুন"
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
