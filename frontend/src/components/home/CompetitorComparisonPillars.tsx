/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    4-in-1 Competitor Comparison Showcase (10MS, Live MCQ, CareTutors, Bdjobs)
 * FILE:      frontend/src/components/home/CompetitorComparisonPillars.tsx
 * PURPOSE:   Boldly demonstrates to students, parents, and recruiters how Student Life Circle
 *            (অগ্রযাত্রা) decisively unifies and supersedes the 4 incumbent legacy platforms:
 *            1. 10 Minute School -> Active 3D STEM Labs & 10-Yr KaTeX Board Archive
 *            2. Live MCQ -> Sub-second Server-Synchronized Live Olympiad Arena
 *            3. CareTutors -> 0% Commission Bilateral Privacy Shield & Escrow
 *            4. Bdjobs -> Cryptographic W3C Proof-of-Skill Talent Radar
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Academic Editorial, Strict TypeScript.
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  Trophy,
  Users,
  Briefcase,
  CheckCircle2,
  XCircle,
  ShieldCheck,
  ArrowRight,
  Scale,
  Sparkles,
  Zap,
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export type CompetitorTab = '10ms' | 'livemcq' | 'caretutors' | 'bdjobs';

interface ComparisonData {
  id: CompetitorTab;
  tabLabel: string;
  competitorName: string;
  categoryTitle: { bn: string; en: string };
  ourAdvantage: { bn: string; en: string };
  ourDescription: { bn: string; en: string };
  legacyWeakness: { bn: string; en: string };
  comparisonPoints: {
    feature: { bn: string; en: string };
    competitorValue: { bn: string; en: string };
    ourValue: { bn: string; en: string };
  }[];
  ctaText: { bn: string; en: string };
  ctaLink: string;
  accentColor: string;
  icon: React.ReactNode;
}

const COMPARISONS: ComparisonData[] = [
  {
    id: '10ms',
    tabLabel: '10 Minute School',
    competitorName: '10 Minute School',
    categoryTitle: {
      bn: 'অ্যাকাডেমিক পাঠ্যক্রম ও বিষয়ভিত্তিক প্রস্তুতি',
      en: 'Curriculum & Subject-wise Preparation'
    },
    ourAdvantage: {
      bn: 'প্যাসিভ ভিডিওর বদলে ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাব ও সক্রিয় সমাধান',
      en: 'Interactive 3D STEM Labs & Active Problem Solving over Passive Videos'
    },
    ourDescription: {
      bn: 'শুধু ভিডিও দেখা নয়; এনসিটিবি পাঠ্যক্রমের প্রতিটি অধ্যায়ের ১০ বছরের আসল বোর্ড প্রশ্ন, লাইভ KaTeX সমীকরণ ও ৩ডি সিমুলেটরে হাতে-কলমে প্র্যাকটিস।',
      en: 'Not just watching videos; practice 10-year authentic board questions, real-time KaTeX math equations, and 3D simulations across every NCTB chapter.'
    },
    legacyWeakness: {
      bn: 'একমুখী রেকর্ড করা ভিডিও লেকচার, স্ক্রিনশটভিত্তিক সূত্রের অস্পষ্ট ছবি, ইন্টারঅ্যাকশনের অভাব।',
      en: 'Passive one-way video lectures, blurry screenshot formulas, and lack of active hands-on interaction.'
    },
    comparisonPoints: [
      {
        feature: { bn: 'শেখার পদ্ধতি', en: 'Learning Method' },
        competitorValue: { bn: 'একমুখী প্যাসিভ ভিডিও দেখা', en: 'Passive video streaming' },
        ourValue: { bn: 'সক্রিয় ৩ডি সিমুলেশন ও প্রবলেম সলভিং', en: 'Active 3D simulation & problem solving' }
      },
      {
        feature: { bn: 'বোর্ড প্রশ্ন ব্যাংক', en: 'Board Question Bank' },
        competitorValue: { bn: 'সীমিত ও সাধারণ পিডিএফ', en: 'Limited generic PDFs' },
        ourValue: { bn: '১০ বছরের আসল বোর্ড প্রশ্ন (KaTeX ম্যাথ)', en: '10-Yr authentic board archive with KaTeX' }
      },
      {
        feature: { bn: 'ব্যক্তিগত টিউটর', en: 'Personal Tutor' },
        competitorValue: { bn: 'সাধারণ প্রশ্ন-উত্তর ফোরাম', en: 'Generic Q&A forums' },
        ourValue: { bn: 'সক্রেটিক এআই তাৎক্ষণিক স্টেপ-বাই-স্টেপ গাইড', en: 'Socratic AI instant step-by-step guidance' }
      },
      {
        feature: { bn: 'অফলাইন সুবিধা', en: 'Offline Access' },
        competitorValue: { bn: 'অ্যাপের ভেতর আটকে থাকা ভিডিও', en: 'In-app locked cached videos' },
        ourValue: { bn: 'P2P অফলাইন মেশ ও ব্রাউজার ক্যাশ সিঙ্ক', en: 'P2P offline mesh & browser sync' }
      },
    ],
    ctaText: {
      bn: 'বোর্ড প্রশ্ন ব্যাংক ও ৩ডি ল্যাব দেখুন',
      en: 'Explore Board Question Bank & 3D Labs'
    },
    ctaLink: '/board-archives',
    accentColor: '#1B2A4A',
    icon: <BookOpen className="w-4 h-4" />,
  },
  {
    id: 'livemcq',
    tabLabel: 'Live MCQ',
    competitorName: 'Live MCQ',
    categoryTitle: {
      bn: 'লাইভ প্রতিযোগিতা ও পরীক্ষা ইঞ্জিন',
      en: 'Live Competition & Examination Engine'
    },
    ourAdvantage: {
      bn: 'সাব-সেকেন্ড সার্ভার টাইমার ও নেগেটিভ মার্কিং নির্ভুলতা',
      en: 'Sub-Second Server Synchronization & Precision Negative Marking'
    },
    ourDescription: {
      bn: 'প্রতিদিন রাত ৮:০০ টায় সারাদেশের হাজার হাজার শিক্ষার্থীর সাথে লাইভ অলিম্পিয়াড। কোনো সার্ভার ল্যাগ নেই, রয়েছে নিখুঁত জাতীয় পার্সেন্টাইল অ্যানালিটিক্স।',
      en: 'Every night at 8:00 PM, compete live with thousands of students across the nation. Zero server latency with granular national percentile ranking.'
    },
    legacyWeakness: {
      bn: 'সাধারণ টেক্সটভিত্তিক এমসিকিউ, বড় পরীক্ষায় সার্ভার ধীরগতি, ব্যাখ্যায় তাত্ত্বিক গভীরতার ঘাটতি।',
      en: 'Plain text MCQs, server slowdowns during massive exams, and shallow theoretical explanations.'
    },
    comparisonPoints: [
      {
        feature: { bn: 'লাইভ পরীক্ষা টাইমার', en: 'Live Exam Timer' },
        competitorValue: { bn: 'ক্লায়েন্ট-সাইড আনসিঙ্ক টাইমার', en: 'Unsynchronized client timer' },
        ourValue: { bn: 'সার্ভার-সিঙ্কড জিরো-ল্যাটেন্সি কাউন্টডাউন', en: 'Server-synced zero-latency countdown' }
      },
      {
        feature: { bn: 'গাণিতিক ব্যাখ্যা', en: 'Mathematical Solutions' },
        competitorValue: { bn: 'সাধারণ টেক্সট উত্তর', en: 'Plain text answers' },
        ourValue: { bn: 'সাব-পিক্সেল KaTeX ফরম্যাটেড সমাধান', en: 'Sub-pixel KaTeX formatted solutions' }
      },
      {
        feature: { bn: 'ভুল উত্তর সংশোধন', en: 'Error Correction' },
        competitorValue: { bn: 'শুধু সঠিক উত্তর প্রদর্শন', en: 'Shows correct answer only' },
        ourValue: { bn: 'স্পেসড-রিপিটিশন রিভিশন কিউ', en: 'Spaced-repetition revision queue' }
      },
      {
        feature: { bn: 'মেধাতালিকা স্বচ্ছতা', en: 'Leaderboard Transparency' },
        competitorValue: { bn: 'সাধারণ র্যাঙ্কিং তালিকা', en: 'Generic ranking list' },
        ourValue: { bn: 'অ্যান্টি-চিট টেলিমেট্রি ও ন্যাশনাল পার্সেন্টাইল', en: 'Anti-cheat telemetry & national percentile' }
      },
    ],
    ctaText: {
      bn: 'আজকের লাইভ চ্যালেঞ্জ লবিতে প্রবেশ',
      en: 'Enter Tonight\'s Live Challenge Lobby'
    },
    ctaLink: '/live-challenge',
    accentColor: '#B8862B',
    icon: <Trophy className="w-4 h-4" />,
  },
  {
    id: 'caretutors',
    tabLabel: 'CareTutors',
    competitorName: 'CareTutors',
    categoryTitle: {
      bn: 'নিরাপদ টিউশন মার্কেটপ্লেস ও শিক্ষক যাচাই',
      en: 'Secure Tuition Marketplace & Educator Verification'
    },
    ourAdvantage: {
      bn: '৫০% কমিশনবিহীন টিউশন ও দ্বিপাক্ষিক প্রাইভেসি শিল্ড',
      en: '0% Commission Fee & Bilateral Privacy Shield'
    },
    ourDescription: {
      bn: 'শিক্ষক বা অভিভাবকদের কাছ থেকে কোনো অযৌক্তিক মধ্যস্বত্বভোগী কমিশন কাটা হয় না। এনআইডি ও বিশ্ববিদ্যালয় যাচাইকৃত প্রোফাইল এবং স্বয়ংক্রিয় এসক্রো লেনদেন।',
      en: 'Zero predatory broker commissions deducted from educators or guardians. NID & university authenticated profiles with automated escrow milestones.'
    },
    legacyWeakness: {
      bn: 'প্রথম মাসের ৫০% থেকে ৬০% বেতন কমিশন হিসেবে কেটে নেওয়া, প্রাইভেসি ফাঁসের ঝুঁকি, ম্যানুয়াল ডিসপিউট।',
      en: 'Cutting 50%–60% of the first month\'s salary as commission, risk of privacy leaks, and manual disputes.'
    },
    comparisonPoints: [
      {
        feature: { bn: 'প্ল্যাটফর্ম কমিশন ফি', en: 'Platform Commission' },
        competitorValue: { bn: 'প্রথম মাসের ৫০%–৬০% কমিশন কর্তন', en: '50%–60% first-month salary deduction' },
        ourValue: { bn: '০% অযৌক্তিক কমিশন (শিক্ষার্থীর পুরো আয় তার)', en: '0% predatory commission (tutor keeps 100%)' }
      },
      {
        feature: { bn: 'ফোন ও তথ্য সুরক্ষা', en: 'Phone & Data Privacy' },
        competitorValue: { bn: 'সরাসরি নম্বর উন্মুক্তের ঝুঁকি', en: 'Direct phone number exposure risk' },
        ourValue: { bn: 'দ্বিপাক্ষিক প্রাইভেসি শিল্ড ও মাস্কড কন্টাক্ট', en: 'Bilateral privacy shield & masked contact' }
      },
      {
        feature: { bn: 'শিক্ষক ভেরিফিকেশন', en: 'Educator Verification' },
        competitorValue: { bn: 'সাধারণ ম্যানুয়াল যাচাই', en: 'Basic manual review' },
        ourValue: { bn: 'এনআইডি ও ভার্সিটি অথেন্টিকেটেড ব্যাজ', en: 'NID & university authenticated badges' }
      },
      {
        feature: { bn: 'পেমেন্ট সুরক্ষা', en: 'Payment Security' },
        competitorValue: { bn: 'হাতে-হাতে অনিরাপদ ক্যাশ লেনদেন', en: 'Insecure cash handoffs' },
        ourValue: { bn: 'বিকাশ ও নগদ স্বয়ংক্রিয় মাইলস্টোন এসক্রো', en: 'bKash & Nagad automated milestone escrow' }
      },
    ],
    ctaText: {
      bn: 'ভেরিফাইড টিউশন মার্কেটপ্লেস খুলুন',
      en: 'Explore Verified Tuition Marketplace'
    },
    ctaLink: '/tuition',
    accentColor: '#0B5D3B',
    icon: <Users className="w-4 h-4" />,
  },
  {
    id: 'bdjobs',
    tabLabel: 'Bdjobs',
    competitorName: 'Bdjobs',
    categoryTitle: {
      bn: 'ক্যারিয়ার, ইন্টার্নশিপ ও মেধা সনদ',
      en: 'Career Readiness, Internships & Verified Credentials'
    },
    ourAdvantage: {
      bn: 'কাগজের সিভির বদলে W3C ক্রিপ্টোগ্রাফিক মেধা সনদ',
      en: 'W3C Cryptographic Credentials over Disposable Paper CVs'
    },
    ourDescription: {
      bn: 'পুরোনো রেজ্যুমে পাঠিয়ে অপেক্ষায় থাকার দিন শেষ। অগ্রযাত্রায় আপনার পরীক্ষা ও অলিম্পিয়াডের প্রতিটি স্কোর স্বয়ংক্রিয়ভাবে আন্তর্জাতিক যাচাইযোগ্য স্কিল সনদে রূপান্তরিত হয়।',
      en: 'No more sending static resumes into a black hole. At Ogrojatra, every verified exam and Olympiad performance transforms into a globally verifiable credential.'
    },
    legacyWeakness: {
      bn: 'অযাচিত বায়োডাটা ডাম্প, ভুয়া তথ্যের ছড়াছড়ি, তরুণ ফ্রেশারদের বাস্তব দক্ষতা প্রমাণের প্রাতিষ্ঠানিক অভাব।',
      en: 'Unsolicited resume spam, rampant fake claims, and zero institutional verification for fresh graduates.'
    },
    comparisonPoints: [
      {
        feature: { bn: 'দক্ষতা যাচাইয়ের পদ্ধতি', en: 'Skill Verification' },
        competitorValue: { bn: 'স্ব-লিখিত কাগুজে জীবনবৃত্তান্ত (CV)', en: 'Self-written unverified paper CV' },
        ourValue: { bn: 'W3C ক্রিপ্টোগ্রাফিক হ্যাশযুক্ত সনদ', en: 'W3C cryptographic hash credentials' }
      },
      {
        feature: { bn: 'নিয়োগকারী সংযোগ', en: 'Recruiter Connectivity' },
        competitorValue: { bn: 'বিজ্ঞাপনে হাজারো সিভির ভিড়', en: 'Lost among thousands of blind applications' },
        ourValue: { bn: 'সরাসরি রিক্রুটার ট্যালেন্ট রাডার ও ফিল্টার', en: 'Direct recruiter talent radar & filters' }
      },
      {
        feature: { bn: 'ভেরিফিকেশন স্পিড', en: 'Verification Speed' },
        competitorValue: { bn: 'ম্যানুয়াল ব্যাকগ্রাউন্ড চেক', en: 'Slow manual background checks' },
        ourValue: { bn: 'তাৎক্ষণিক কিউআর কোড ও অনলাইন ভ্যালিডেশন', en: 'Instant QR code & online validation' }
      },
      {
        feature: { bn: 'শিক্ষাজীবনের ধারাবাহিকতা', en: 'Student Journey Continuity' },
        competitorValue: { bn: 'পড়াশোনার সাথে চাকরির সংযোগহীন', en: 'Zero bridge between study and jobs' },
        ourValue: { bn: 'এসএসসি থেকে ক্যারিয়ার—এক অবিচ্ছেদ্য প্রোফাইল', en: 'SSC to Career in a single seamless profile' }
      },
    ],
    ctaText: {
      bn: 'ক্যারিয়ার ও মেধা সনদ হাব দেখুন',
      en: 'Explore Career & Credential Radar'
    },
    ctaLink: '/career',
    accentColor: '#1B2A4A',
    icon: <Briefcase className="w-4 h-4" />,
  },
];

export const CompetitorComparisonPillars: React.FC = () => {
  const { isBengali } = useTranslation();
  const [activeTab, setActiveTab] = useState<CompetitorTab>('10ms');

  const current = COMPARISONS.find((c) => c.id === activeTab) || COMPARISONS[0];

  return (
    <section className="relative py-14 sm:py-16 md:py-20 bg-[#FAF7F2] dark:bg-[#0A1324] border-b border-amber-200/60 dark:border-slate-800 overflow-hidden transition-colors duration-300">
      {/* Royal Cobalt & Amber Radial Ambient Glow */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-5xl h-[420px] pointer-events-none select-none z-0"
        style={{
          background:
            'radial-gradient(ellipse 70% 65% at 50% 50%, rgba(37, 99, 235, 0.16) 0%, rgba(237, 142, 34, 0.08) 50%, transparent 80%)'
        }}
        aria-hidden="true"
      />

      {/* Contextual Typographic Watermark (CAMPUS) */}
      <div
        className="absolute z-0 pointer-events-none select-none w-full top-4 left-0 flex justify-center overflow-hidden"
        aria-hidden="true"
      >
        <p
          className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[20vw] md:text-[clamp(4rem,22vw,18rem)] uppercase tracking-wider select-none opacity-40 dark:opacity-20"
          style={{
            lineHeight: 0.95,
            backgroundImage:
              'linear-gradient(to bottom, rgba(37, 99, 235, 0.22) 15%, rgba(237, 142, 34, 0.02) 100%)'
          }}
        >
          campus
        </p>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10 relative z-10">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/95 dark:bg-[#121B2D] border border-amber-200/80 dark:border-[#262D3D] text-xs font-bold text-[#ED8E22] shadow-xs">
            <span className="h-2 w-2 rounded-full bg-[#ED8E22] shrink-0 animate-pulse" aria-hidden="true" />
            <Zap className="w-3.5 h-3.5 text-[#ED8E22]" />
            <span>
              {isBengali
                ? '৪টি আলাদা প্ল্যাটফর্মের বদলে একটি পূর্ণাঙ্গ ডিজিটাল ক্যাম্পাস'
                : 'One Unified Digital Campus Replacing 4 Separate Platforms'}
            </span>
          </div>

          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#213130] dark:text-[#F5F2EB] font-bengali tracking-tight">
            {isBengali
              ? 'কেন অগ্রযাত্রা প্রথাগত প্ল্যাটফর্মগুলোর চেয়ে বহুগুণ এগিয়ে?'
              : 'Why Ogrojatra Decisively Supersedes Conventional Platforms'}
          </h2>

          <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
            {isBengali
              ? 'আমরা আলাদা আলাদা প্ল্যাটফর্মের পেছনে ছোটাছুটি বন্ধ করেছি। একাডেমিক পড়াশোনা, লাইভ কুইজ, টিউশন এবং প্রথম চাকরি—সবকিছু একটি মাত্র প্রোফাইলে সমন্বিত।'
              : 'We unified the fragmented student journey. Curriculum study, live Olympiad challenges, private tuition, and career entry—all within a single profile.'}
          </p>
        </div>

        {/* 4 Interactive Switcher Tabs */}
        <div className="flex flex-wrap items-center justify-center gap-2.5 max-w-4xl mx-auto">
          {COMPARISONS.map((comp) => {
            const isActive = comp.id === activeTab;
            return (
              <button
                key={comp.id}
                type="button"
                onClick={() => setActiveTab(comp.id)}
                className={`flex items-center gap-2 px-5 py-3 rounded-2xl text-xs sm:text-sm font-bold font-bengali transition-all duration-150 border ${
                  isActive
                    ? 'bg-[#ED8E22] text-white border-[#ED8E22] shadow-[0_4px_14px_0_rgba(237,142,34,0.30)] scale-[1.02]'
                    : 'bg-white/95 dark:bg-[#121B2D] text-[#5B5B5B] dark:text-slate-300 border-amber-200/70 dark:border-[#262D3D] hover:border-[#ED8E22]/60 hover:bg-[#FFF9EB]'
                }`}
              >
                <span>{isBengali ? `বনাম ${comp.tabLabel}` : `vs ${comp.tabLabel}`}</span>
              </button>
            );
          })}
        </div>

        {/* Selected Comparison Showcase Card */}
        <div className="p-6 sm:p-8 rounded-3xl bg-[#FFF9EB]/80 dark:bg-[#121B2D] border border-amber-200/80 dark:border-[#262D3D] shadow-[0_4px_24px_-4px_rgba(237,142,34,0.08)] space-y-8">
          
          {/* Header Summary */}
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-amber-200/70 dark:border-[#262D3D]">
            <div className="space-y-1.5 max-w-2xl">
              <span className="text-xs font-bold text-[#0B5D3B] dark:text-emerald-400 uppercase tracking-wider font-sans">
                {isBengali ? current.categoryTitle.bn : current.categoryTitle.en}
              </span>
              <h3 className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                {isBengali ? current.ourAdvantage.bn : current.ourAdvantage.en}
              </h3>
              <p className="text-xs sm:text-sm text-[#525252] dark:text-slate-400 font-bengali leading-relaxed">
                {isBengali ? current.ourDescription.bn : current.ourDescription.en}
              </p>
            </div>

            <Link
              href={current.ctaLink}
              className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-full bg-[#ED8E22] hover:bg-[#D47C1A] text-white font-bold text-xs sm:text-sm font-bengali shadow-md active:scale-95 transition shrink-0 self-start lg:self-auto"
            >
              <span>{isBengali ? current.ctaText.bn : current.ctaText.en}</span>
              <ArrowRight className="w-4 h-4 text-amber-200" />
            </Link>
          </div>

          {/* Side-by-Side Comparison Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {current.comparisonPoints.map((pt, idx) => (
              <div
                key={idx}
                className="p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/50 transition-all space-y-3"
              >
                <div className="text-xs font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                  {isBengali ? pt.feature.bn : pt.feature.en}
                </div>

                <div className="space-y-2 text-xs font-bengali">
                  {/* Competitor's Limitation */}
                  <div className="flex items-start gap-2 text-[#991B1B] dark:text-rose-400 opacity-90">
                    <XCircle className="w-4 h-4 shrink-0 mt-0.5" />
                    <span><strong className="font-semibold">{current.competitorName}:</strong> {isBengali ? pt.competitorValue.bn : pt.competitorValue.en}</span>
                  </div>

                  {/* Our Superior Solution */}
                  <div className="flex items-start gap-2 text-[#0B5D3B] dark:text-emerald-400">
                    <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5" />
                    <span><strong className="font-semibold">{isBengali ? 'অগ্রযাত্রা:' : 'Ogrojatra:'}</strong> {isBengali ? pt.ourValue.bn : pt.ourValue.en}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

        </div>

      </div>
    </section>
  );
};
