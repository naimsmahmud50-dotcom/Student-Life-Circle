/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/LiveHowItWorksPathway.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Reverse-engineers and elevates Live MCQ's "how" 4-step preparation pathway.
 *            Renders numbered cards (০১, ০২, ০৩, ০৪) describing the complete journey
 *            from registration to live exam participation and OMR evaluation with zero emojis.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React from 'react';
import {
  Smartphone,
  Compass,
  BookOpen,
  Trophy,
  ArrowRight,
  CheckCircle2,
  Layers
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

interface PathwayStep {
  numberBn: string;
  numberEn: string;
  titleBn: string;
  titleEn: string;
  descBn: string;
  descEn: string;
  badgeBn: string;
  badgeEn: string;
  icon: React.ComponentType<{ className?: string }>;
}

const STEPS: PathwayStep[] = [
  {
    numberBn: '০১',
    numberEn: '01',
    titleBn: 'ইনস্টল ও রেজিস্ট্রেশন',
    titleEn: 'Install & Quick Registration',
    descBn: 'Android, iOS, Windows, macOS এবং আধুনিক Web App — আপনার পছন্দের সব ডিভাইসেই সম্পূর্ণ ক্লাউড সিঙ্কসহ ঝামেলাহীন এক্সেস।',
    descEn: 'Seamless cloud sync across Android, iOS, Windows, macOS, and high-performance Web App.',
    badgeBn: 'মাল্টি-ডিভাইস এক্সেস',
    badgeEn: 'Multi-Device Access',
    icon: Smartphone
  },
  {
    numberBn: '০২',
    numberEn: '02',
    titleBn: 'লক্ষ্য নির্ধারণ করুন',
    titleEn: 'Select Your Target Track',
    descBn: 'বিসিএস, ব্যাংক, এইচএসসি সায়েন্স, মেডিকেল ভর্তি কিংবা জাতীয় বিজ্ঞান ও গণিত অলিম্পিয়াড — আপনার সুনির্দিষ্ট একাডেমিক সিলেবাস বেছে নিন।',
    descEn: 'Choose your specific syllabus: BCS, Bank, HSC Science, Medical Admission, or National Olympiad.',
    badgeBn: 'সুনির্দিষ্ট সিলেবাস',
    badgeEn: 'Targeted Syllabus',
    icon: Compass
  },
  {
    numberBn: '০৩',
    numberEn: '03',
    titleBn: 'নিয়মিত Study ও স্মার্ট রিভিশন',
    titleEn: 'Regular Study & Smart Revision',
    descBn: 'টপিক গুরু, বিষয়ভিত্তিক আর্কাইভ, KaTeX গাণিতিক সূত্র ও তথ্যকল্পদ্রুম ব্যবহার করে নিয়মিত প্রস্তুতি নিন এবং ভুল উত্তর স্পেসড রিপিটেশনে রিভাইজ করুন।',
    descEn: 'Prepare methodically with Topic Guru, KaTeX math formulas, verified references, and spaced repetition.',
    badgeBn: 'টপিক গুরু ও আর্কাইভ',
    badgeEn: 'Topic Guru & Archive',
    icon: BookOpen
  },
  {
    numberBn: '০৪',
    numberEn: '04',
    titleBn: 'নিয়মিত লাইভ পরীক্ষা ও ওএমআর',
    titleEn: 'Live Examination & OMR Practice',
    descBn: 'দৈনিক রুটিন অনুসারে ডিজিটাল ওএমআর শিট পূরণ করে লাইভ পরীক্ষায় অংশ নিন। পরীক্ষা শেষে জানুন জাতীয় পার্সেন্টাইল ও কাট-অফ পজিশন।',
    descEn: 'Fill digital OMR bubble sheets in synchronized live exams. Receive instant national percentile standings.',
    badgeBn: 'রিয়েল-টাইম মেধা তালিকা',
    badgeEn: 'Real-Time Merit Rank',
    icon: Trophy
  }
];

export function LiveHowItWorksPathway() {
  const { isBengali } = useTranslation();

  return (
    <section className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-3 max-w-2xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-blue-100 dark:bg-blue-950/50 border border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-300 text-xs font-bold font-bengali">
          <Layers className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
          <span>{isBengali ? '৪টি ধারাবাহিক ধাপ' : '4 Consecutive Steps'}</span>
        </div>

        <h2 className="text-xl sm:text-3xl font-bold text-white font-serif tracking-tight">
          {isBengali ? (
            <>
              অগ্রযাত্রা কীভাবে আপনার{' '}
              <span className="text-emerald-400 font-serif">
                প্রস্তুতিতে সাহায্য করবে?
              </span>
            </>
          ) : (
            <>
              How Ogrojatra{' '}
              <span className="text-emerald-400 font-serif">
                Powers Your Preparation
              </span>
            </>
          )}
        </h2>

        <p className="text-xs sm:text-sm text-slate-300 font-bengali">
          {isBengali ? 'সহজ রেজিস্ট্রেশন থেকে চূড়ান্ত জাতীয় মেধা তালিকায় অবস্থান অর্জন — ধাপে ধাপে স্বয়ংসম্পূর্ণ প্রস্তুতি' : 'From effortless registration to top national merit ranking — structured step-by-step preparation'}
        </p>
      </div>

      {/* 4 Steps Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {STEPS.map((step) => {
          const Icon = step.icon;

          return (
            <div
              key={step.numberBn}
              className="p-6 rounded-2xl bg-white/95 dark:bg-[#07241E]/85 backdrop-blur-md border border-emerald-500/25 shadow-md hover:shadow-xl hover:border-emerald-400/50 transition flex flex-col justify-between"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-3xl sm:text-4xl font-black font-mono text-emerald-700 dark:text-emerald-400">
                    {isBengali ? step.numberBn : step.numberEn}
                  </span>
                  <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-300 border border-emerald-500/20">
                    <Icon className="w-5 h-5" />
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="text-base font-bold font-bengali text-slate-900 dark:text-white">
                    {isBengali ? step.titleBn : step.titleEn}
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
                    {isBengali ? step.descBn : step.descEn}
                  </p>
                </div>
              </div>

              <div className="pt-4 mt-4 border-t border-slate-200 dark:border-emerald-900/40 flex items-center justify-between">
                <span className="text-[11px] font-bold font-bengali text-slate-500 dark:text-emerald-300/80">
                  {isBengali ? step.badgeBn : step.badgeEn}
                </span>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
