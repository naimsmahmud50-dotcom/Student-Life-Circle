/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/LiveMcqFeatureShowcase.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Showcases all 14 signature features reverse-engineered from Live MCQ,
 *            elevated with Oxford Navy academic dignity, zero emojis, and tactile interactions.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Search,
  BookOpen,
  CheckCircle2,
  Sparkles,
  ShieldCheck,
  FileText,
  Award,
  Layers,
  Bell,
  RotateCcw,
  Archive,
  WifiOff,
  UserCheck,
  Swords,
  ChevronRight,
  Filter,
  ArrowRight
} from 'lucide-react';

export type FeatureCategory = 'all' | 'exam_omr' | 'smart_study' | 'analytics_merit';

export interface SuiteFeature {
  id: string;
  category: 'exam_omr' | 'smart_study' | 'analytics_merit';
  tagBn: string;
  titleBn: string;
  descriptionBn: string;
  highlightBn: string;
  ctaTextBn: string;
  ctaHref: string;
  icon: React.ElementType;
  badgeColorClass: string;
}

const SUITE_FEATURES: SuiteFeature[] = [
  {
    id: 'smart_search',
    category: 'smart_study',
    tagBn: 'স্মার্ট টুল',
    titleBn: 'স্মার্ট সার্চ ও কনসেপ্ট ফাইন্ডার',
    descriptionBn: 'যেকোনো গাণিতিক সূত্র, বৈজ্ঞানিক তত্ত্ব বা টপিক লিখে এক ট্যাপেই প্রাসঙ্গিক সব বহুনির্বাচনী প্রশ্ন ও এনসিটিবি ব্যাখ্যায় পৌঁছে যান।',
    highlightBn: 'ভুল বানানেও সঠিক প্রশ্ন অনুসন্ধান',
    ctaTextBn: 'অনুসন্ধান করুন',
    ctaHref: '/practice',
    icon: Search,
    badgeColorClass: 'bg-[#0A2540] text-amber-300'
  },
  {
    id: 'topic_guru',
    category: 'smart_study',
    tagBn: 'মাইক্রো-লার্নিং',
    titleBn: 'টপিক গুরু ও চ্যাপ্টার ডিকনস্ট্রাকশন',
    descriptionBn: 'বোর্ড সিলেবাসকে ছোট ছোট সাব-টপিকে ভাগ করে মাইক্রো-প্রস্তুতি নিন এবং তাৎক্ষণিক Random Quiz জেনারেট করে নিজের দখল যাচাই করুন।',
    highlightBn: '১০০% অধ্যায়ভিত্তিক প্রস্তুতি কভারেজ',
    ctaTextBn: 'টপিক বাছুন',
    ctaHref: '/learn',
    icon: BookOpen,
    badgeColorClass: 'bg-emerald-800 text-white'
  },
  {
    id: 'omr_mode',
    category: 'exam_omr',
    tagBn: 'বাস্তব অভিজ্ঞতা',
    titleBn: 'ডিজিটাল ওএমআর শিট মোড (OMR Mode)',
    descriptionBn: 'ঘরে বসেই আসল বোর্ড ও বিশ্ববিদ্যালয় ভর্তি পরীক্ষার ওএমআর শিটের মতো ডিজিটাল বৃত্ত ভরাট করে পরীক্ষার নির্ভুল অভিজ্ঞতা অর্জন করুন।',
    highlightBn: 'স্পর্শসংবেদনশীল ওএমআর অ্যানিমেশন',
    ctaTextBn: 'ওএমআর প্র্যাকটিস',
    ctaHref: '#omr-simulator',
    icon: CheckCircle2,
    badgeColorClass: 'bg-[#0A2540] text-white'
  },
  {
    id: 'vocab_booster',
    category: 'smart_study',
    tagBn: 'ফর্মুলা ডেক',
    titleBn: 'ভোকাবুলারি ও ফর্মুলা বুস্টার প্রো',
    descriptionBn: 'পদার্থবিজ্ঞান, রসায়ন ও উচ্চতর গণিতের গুরুত্বপূর্ণ সূত্রাবলী, ধ্রুবক ও মেডিকেল-ভর্তি উপযোগী ৫২০+ বৈজ্ঞানিক পরিভাষা।',
    highlightBn: '২৬টি গ্রুপে সাজানো স্পেসড ডেক',
    ctaTextBn: 'ফর্মুলা রিভিশন',
    ctaHref: '/curriculum/lexicon',
    icon: Sparkles,
    badgeColorClass: 'bg-amber-800 text-amber-100'
  },
  {
    id: 'info_vault',
    category: 'smart_study',
    tagBn: 'প্রামাণ্য রেফারেন্স',
    titleBn: 'তথ্যকল্পদ্রুম ও বিতর্কিত প্রশ্ন সমাধান',
    descriptionBn: 'বিগত বোর্ড ও ভর্তি পরীক্ষার বিভিন্ন প্রচলিত বিভ্রান্তিমূলক প্রশ্নের এনসিটিবি পাঠ্যবই ও জাতীয় কারিকুলাম রেফারেন্সসহ নির্ভুল সমাধান।',
    highlightBn: 'বোর্ড নিরীক্ষক অনুমোদিত ব্যাখ্যা',
    ctaTextBn: 'রেফারেন্স দেখুন',
    ctaHref: '/board-archives',
    icon: ShieldCheck,
    badgeColorClass: 'bg-slate-800 text-slate-100'
  },
  {
    id: 'job_admission_sol',
    category: 'exam_omr',
    tagBn: 'প্রশ্নব্যাংক',
    titleBn: 'সেন্ট্রাল বোর্ড ও বিশ্ববিদ্যালয় ভর্তি সল্যুশন',
    descriptionBn: 'ঢাকা বিশ্ববিদ্যালয়, বুয়েট, মেডিকেল এবং বিগত ১০ বছরের সকল শিক্ষা বোর্ডের প্রশ্নপত্র অধ্যায়ভিত্তিক ফিল্টারিং ও পূর্ণাঙ্গ সল্যুশন।',
    highlightBn: 'বিগত ২০ বছরের সমাধান সংগ্রহ',
    ctaTextBn: 'প্রশ্নব্যাংক এক্সপ্লোর',
    ctaHref: '/board-archives',
    icon: FileText,
    badgeColorClass: 'bg-slate-700 text-slate-100'
  },
  {
    id: 'central_result',
    category: 'analytics_merit',
    tagBn: 'জাতীয় মেধা',
    titleBn: 'সেন্ট্রাল রেজাল্ট ও রিয়েল-টাইম মেধা তালিকা',
    descriptionBn: '৫০,০০০+ প্রতিযোগীর মাঝে আপনার জাতীয় অবস্থান, বিষয়ভিত্তিক সঠিকতা শতাংশ, পারসেন্টাইল ও সম্ভাব্য কাট-মার্কের গভীর বিশ্লেষণ।',
    highlightBn: 'রিয়েল-টাইম লাইভ লিডারবোর্ড',
    ctaTextBn: 'মেধা তালিকা দেখুন',
    ctaHref: '#central-leaderboard',
    icon: Award,
    badgeColorClass: 'bg-[#0A2540] text-amber-300'
  },
  {
    id: 'quiz_master',
    category: 'exam_omr',
    tagBn: 'কাস্টম টেস্ট',
    titleBn: 'কুইজ মাস্টার ও নিজস্ব টেস্ট জেনারেটর',
    descriptionBn: 'নিজের সময় ও দুর্বলতা অনুসারে বিষয়, নির্দিষ্ট অধ্যায় এবং প্রশ্নের সংখ্যা নির্ধারণ করে মুহূর্তেই নিজস্ব মক টেস্ট প্রস্তুত করুন।',
    highlightBn: 'সম্পূর্ণ স্বনির্ধারিত প্রশ্নকাঠামো',
    ctaTextBn: 'কুইজ তৈরি করুন',
    ctaHref: '/practice',
    icon: Layers,
    badgeColorClass: 'bg-emerald-700 text-white'
  },
  {
    id: 'dynamic_panel',
    category: 'analytics_merit',
    tagBn: 'লাইভ নোটিশ',
    titleBn: 'ডাইনামিক ইনফো প্যানেল ও বোর্ড আপডেট',
    descriptionBn: 'সকল শিক্ষা বোর্ডের রুটিন পরিবর্তন, প্রবেশপত্র নির্দেশিকা, আসন বিন্যাস ও জাতীয় অলিম্পিয়াড শিডিউল সরাসরি লাইভ প্যানেলে হালনাগাদ।',
    highlightBn: 'সরাসরি অফিসিয়াল নোটিফিকেশন',
    ctaTextBn: 'নোটিশ বোর্ড',
    ctaHref: '#notice-board',
    icon: Bell,
    badgeColorClass: 'bg-amber-900 text-amber-100'
  },
  {
    id: 'wrong_unanswered',
    category: 'smart_study',
    tagBn: 'দুর্বলতা দূরীকরণ',
    titleBn: 'ভুল ও অনুত্তরিত প্রশ্ন ব্যাংক (Wrong & Unanswered)',
    descriptionBn: 'লাইভ পরীক্ষা বা অনুশীলনে ভুল করা কিংবা উত্তর না দেওয়া প্রশ্নগুলো স্বয়ংক্রিয়ভাবে সংরক্ষিত হয়ে আপনার দুর্বলতা কাটিয়ে তুলতে সাহায্য করে।',
    highlightBn: 'স্বয়ংক্রিয় স্পেসড রিপিটিশন কিউ',
    ctaTextBn: 'রিভিশন ডেস্কে যান',
    ctaHref: '/dashboard',
    icon: RotateCcw,
    badgeColorClass: 'bg-[#991B1B] text-white'
  },
  {
    id: 'central_archive',
    category: 'exam_omr',
    tagBn: 'প্রশ্নভাণ্ডার',
    titleBn: '১০ বছরের সেন্ট্রাল আর্কাইভ ও রি-টেস্ট',
    descriptionBn: 'বিগত অনুষ্ঠিত সকল লাইভ চ্যালেঞ্জ ও অলিম্পিয়াড পরীক্ষার প্রশ্ন একসাথে সংরক্ষিত—যেকোনো সময় রি-টেস্ট দিয়ে নিজেকে ঝালিয়ে নিন।',
    highlightBn: 'সম্পূর্ণ বিনামূল্যে আনলিমিটেড এক্সেস',
    ctaTextBn: 'আর্কাইভ দেখুন',
    ctaHref: '/board-archives',
    icon: Archive,
    badgeColorClass: 'bg-slate-800 text-white'
  },
  {
    id: 'offline_vault',
    category: 'exam_omr',
    tagBn: 'নেট ছাড়া প্রস্তুতি',
    titleBn: 'অফলাইন সেকশন ও লোকাল বাফার ইঞ্জিন',
    descriptionBn: 'ইন্টারনেট ড্রপ হলেও পরীক্ষা থামবে না। আপনার ডিভাইসে স্বয়ংক্রিয়ভাবে সংরক্ষিত প্রশ্নপত্রে অফলাইনে পরীক্ষা দিন; নেট পেলেই অটো-সিঙ্ক হবে।',
    highlightBn: 'জিরো ডেটা লস গ্যারান্টি',
    ctaTextBn: 'অফলাইন মোড',
    ctaHref: '/offline',
    icon: WifiOff,
    badgeColorClass: 'bg-emerald-900 text-emerald-100'
  },
  {
    id: 'my_section',
    category: 'analytics_merit',
    tagBn: 'ব্যক্তিগত ডেস্ক',
    titleBn: 'মাই সেকশন ও পার্সোনালাইজড ট্র্যাকার',
    descriptionBn: 'শিক্ষার্থীর নিজস্ব পছন্দের সাবজেক্ট, দৈনিক স্টাডি রুটিন এবং দুর্বল অধ্যায়ের অগ্রগতি গ্রাফ নিয়ে সজ্জিত ব্যক্তিগত ড্যাশবোর্ড।',
    highlightBn: 'লক্ষ্যভিত্তিক একাডেমিক অগ্রগতি',
    ctaTextBn: 'আমার প্রোফাইল',
    ctaHref: '/dashboard',
    icon: UserCheck,
    badgeColorClass: 'bg-[#0A2540] text-slate-100'
  },
  {
    id: 'multiplayer_battle',
    category: 'exam_omr',
    tagBn: 'লাইভ ডুয়েল',
    titleBn: 'মাল্টিপ্লেয়ার স্টাডি ব্যাটল ও লাইভ পড',
    descriptionBn: 'সহপাঠী বা স্টাডি পডের বন্ধুদের সাথে সরাসরি রিয়েল-টাইম লাইভ কুইজ প্রতিযোগিতায় অংশ নিয়ে পড়াশোনাকে করুন রোমাঞ্চকর ও কার্যকর।',
    highlightBn: 'মিলিসেকেন্ড সিনক্রোনাইজড ডুয়েল',
    ctaTextBn: 'ব্যাটলে যোগ দিন',
    ctaHref: '/study-pod',
    icon: Swords,
    badgeColorClass: 'bg-purple-900 text-purple-100'
  }
];

export const LiveMcqFeatureShowcase: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<FeatureCategory>('all');

  const filteredFeatures = SUITE_FEATURES.filter((feat) => {
    if (selectedCategory === 'all') return true;
    return feat.category === selectedCategory;
  });

  return (
    <div
      aria-label="অগ্রযাত্রা এক্সামিনেশন স্যুট"
      className="p-6 sm:p-10 rounded-3xl bg-white/95 dark:bg-[#1A0C2C]/90 backdrop-blur-md border border-fuchsia-500/25 shadow-xl space-y-8"
    >
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-fuchsia-200/50 dark:border-fuchsia-900/40">
        <div className="space-y-2 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-fuchsia-500/10 dark:bg-fuchsia-500/20 border border-fuchsia-500/30 text-fuchsia-600 dark:text-fuchsia-300 text-xs font-mono font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5 text-fuchsia-500" />
            <span>অগ্রযাত্রা এক্সামিনেশন স্যুট • ১৪টি ফ্ল্যাগশিপ ফিচার</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-black font-bengali text-slate-900 dark:text-white tracking-tight">
            লাইভ এমসিকিউ-এর সকল আধুনিক শক্তি, এবার সম্পূর্ণ উন্মুক্ত ও উন্নত
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
            স্মার্ট সার্চ, ডিজিটাল ওএমআর শিট, টপিক গুরু, অফলাইন বাফার থেকে শুরু করে তথ্যকল্পদ্রুম—শিক্ষার্থীদের পরীক্ষার পূর্ণাঙ্গ প্রস্তুতি নিশ্চিত করতে প্রস্তুত এক সমন্বিত একাডেমিক পরিবেশ।
          </p>
        </div>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-2xl bg-slate-100 dark:bg-[#10071C] border border-fuchsia-500/25">
          <button
            type="button"
            onClick={() => setSelectedCategory('all')}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              selectedCategory === 'all'
                ? 'bg-fuchsia-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-fuchsia-200 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            সমস্ত ফিচার (১৪)
          </button>
          <button
            type="button"
            onClick={() => setSelectedCategory('exam_omr')}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              selectedCategory === 'exam_omr'
                ? 'bg-fuchsia-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-fuchsia-200 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            লাইভ পরীক্ষা ও ওএমআর
          </button>
          <button
            type="button"
            onClick={() => setSelectedCategory('smart_study')}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              selectedCategory === 'smart_study'
                ? 'bg-fuchsia-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-fuchsia-200 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            স্মার্ট স্টাডি ও রিভিশন
          </button>
          <button
            type="button"
            onClick={() => setSelectedCategory('analytics_merit')}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              selectedCategory === 'analytics_merit'
                ? 'bg-fuchsia-600 text-white shadow-sm'
                : 'text-slate-600 dark:text-fuchsia-200 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            অ্যানালিটিক্স ও মেধা
          </button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredFeatures.map((feat) => {
          const Icon = feat.icon;
          return (
            <div
              key={feat.id}
              className="p-6 rounded-2xl bg-white/95 dark:bg-[#10071C]/90 border border-fuchsia-500/20 hover:border-fuchsia-500/50 transition flex flex-col justify-between gap-5 group shadow-sm"
            >
              <div className="space-y-3">
                {/* Header Badge & Icon */}
                <div className="flex items-center justify-between gap-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-[#200D38] border border-fuchsia-500/30 flex items-center justify-center text-fuchsia-600 dark:text-fuchsia-300 group-hover:scale-105 transition-transform shadow-xs">
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold font-bengali ${feat.badgeColorClass}`}>
                    {feat.tagBn}
                  </span>
                </div>

                {/* Title */}
                <h3 className="text-base font-bold font-bengali text-slate-900 dark:text-white leading-snug">
                  {feat.titleBn}
                </h3>

                {/* Description */}
                <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
                  {feat.descriptionBn}
                </p>
              </div>

              {/* Highlight and CTA */}
              <div className="pt-3 border-t border-fuchsia-200/40 dark:border-fuchsia-900/30 flex items-center justify-between gap-2">
                <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400 truncate">
                  {feat.highlightBn}
                </span>

                <Link
                  href={feat.ctaHref}
                  className="px-3.5 py-1.5 rounded-lg bg-slate-100 dark:bg-[#200D38] text-fuchsia-700 dark:text-fuchsia-300 border border-fuchsia-500/30 hover:bg-fuchsia-600 hover:text-white dark:hover:bg-fuchsia-500 dark:hover:text-white font-bold font-bengali text-xs flex items-center gap-1 transition whitespace-nowrap min-h-[36px]"
                >
                  <span>{feat.ctaTextBn}</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
