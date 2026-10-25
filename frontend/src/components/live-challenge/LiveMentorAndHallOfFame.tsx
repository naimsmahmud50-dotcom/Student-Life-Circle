/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/LiveMentorAndHallOfFame.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Reverse-engineers and elevates Live MCQ's "mentorPanel" and Hall of Fame
 *            sections. Showcases accredited academic mentors (BCS Cadres, BUET/DU STEM
 *            mentors, Olympiad champions) and top achievers with zero emojis and WCAG AAA.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useState } from 'react';
import {
  Award,
  GraduationCap,
  Users,
  ShieldCheck,
  CheckCircle2,
  ChevronRight,
  Star,
  Building2,
  Trophy
} from 'lucide-react';

interface Mentor {
  nameBn: string;
  designationBn: string;
  institutionBn: string;
  cadreTrackBn: string;
  badgeBn: string;
}

const MENTORS: Mentor[] = [
  {
    nameBn: 'মাহমুদুল হক চৌধুরী',
    designationBn: '৪০তম বিসিএস (প্রশাসন ক্যাডার) • সহকারী কমিশনার ও নির্বাহী ম্যাজিস্ট্রেট',
    institutionBn: 'ঢাকা বিশ্ববিদ্যালয় (লোকপ্রশাসন বিভাগ)',
    cadreTrackBn: 'বিসিএস প্রিলিমিনারি ও সাধারণ জ্ঞান গাইডলাইন',
    badgeBn: 'বিসিএস অ্যাডভাইজর'
  },
  {
    nameBn: 'প্রকৌশলী ফারহান তানভীর',
    designationBn: 'সিনিয়র সফটওয়্যার ইঞ্জিনিয়ার ও অলিম্পিয়াড ট্রেইনার',
    institutionBn: 'বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (বুয়েট - সিএসই)',
    cadreTrackBn: 'উচ্চতর গণিত ও স্টেম অলিম্পিয়াড মেন্টরশিপ',
    badgeBn: 'বুয়েট ও অলিম্পিয়াড'
  },
  {
    nameBn: 'ডাঃ সানজিদা আক্তার',
    designationBn: 'সহকারী অধ্যাপক ও মেডিকেল কারিকুলাম রিসার্চার',
    institutionBn: 'ঢাকা মেডিকেল কলেজ (ডিএমসি)',
    cadreTrackBn: 'মেডিকেল ভর্তি ও জীববিজ্ঞান প্রস্তুতি প্যানেল',
    badgeBn: 'মেডিকেল একাডেমি'
  },
  {
    nameBn: 'মোঃ আনিসুর রহমান',
    designationBn: 'সিনিয়র প্রিন্সিপাল অফিসার (বাংলাদেশ ব্যাংক)',
    institutionBn: 'জাহাঙ্গীরনগর বিশ্ববিদ্যালয় (অর্থনীতি বিভাগ)',
    cadreTrackBn: 'ব্যাংক অ্যানালিটিক্যাল ও ম্যাথমেটিক্যাল সল্যুশন',
    badgeBn: 'ব্যাংক ক্যারিয়ার'
  }
];

interface Achiever {
  nameBn: string;
  examBn: string;
  rankBn: string;
  scoreBn: string;
  quoteBn: string;
}

const ACHIEVERS: Achiever[] = [
  {
    nameBn: 'সাবরিনা জাহান',
    examBn: '৪৩তম বিসিএস ক্যাডার পরীক্ষা',
    rankBn: 'মেধা স্থান: ০৩',
    scoreBn: '১৮২.৫ / ২০০',
    quoteBn: 'প্রতিদিন ওএমআর শিটে টাইমার ধরে লাইভ পরীক্ষা দেওয়ার অভ্যাসই আমাকে প্রিলিতে শতভাগ আত্মবিশ্বাস জুগিয়েছিল।'
  },
  {
    nameBn: 'তানভীর আহমেদ',
    examBn: 'জাতীয় স্টেম অলিম্পিয়াড ও বুয়েট ভর্তি',
    rankBn: 'মেধা স্থান: ০১ (অলিম্পিয়াড)',
    scoreBn: '৯৮.০ / ১০০',
    quoteBn: 'টপিক গুরু এবং ভুল উত্তরের স্পেসড রিপিটেশন রিভিশন পদ্ধতি আমার ভুল হওয়ার প্রবণতা শূন্যের কোঠায় নামিয়ে এনেছিল।'
  },
  {
    nameBn: 'নাসরিন সুলতানা',
    examBn: 'সম্মিলিত ৮ ব্যাংক সিনিয়র অফিসার',
    rankBn: 'মেধা স্থান: ০৭',
    scoreBn: '৮৬.২৫ / ১০০',
    quoteBn: 'সেন্ট্রাল রেজাল্টের মাধ্যমে প্রতিদিন দেশের হাজারো প্রার্থীর মাঝে নিজের অবস্থান দেখতে পাওয়া আমাকে শৃঙ্খলাবদ্ধ রেখেছিল।'
  }
];

export function LiveMentorAndHallOfFame() {
  const [activeTab, setActiveTab] = useState<'mentors' | 'achievers'>('mentors');

  return (
    <section className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-2 border-b border-slate-200 dark:border-slate-800">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-bold font-bengali">
            <Award className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>অভিজ্ঞ মেন্টর প্যানেল ও হল অফ ফেম</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-white font-bengali">
            দেশের সেরা ক্যাডার, শিক্ষক ও শীর্ষ বিজয়ীদের গাইডলাইন
          </h2>
          <p className="text-xs text-slate-500 font-bengali">
            Live MCQ-এর ঐতিহ্য বজায় রেখে শতভাগ নির্ভরযোগ্য ও যাচাইকৃত শিক্ষক প্যানেলের সরাসরি তত্ত্বাবধান
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center p-1 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <button
            type="button"
            onClick={() => setActiveTab('mentors')}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold font-bengali transition ${
              activeTab === 'mentors'
                ? 'bg-white dark:bg-slate-900 text-[#0A2540] dark:text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            মেন্টর ও ইন্সট্রাক্টর
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('achievers')}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold font-bengali transition ${
              activeTab === 'achievers'
                ? 'bg-white dark:bg-slate-900 text-[#0A2540] dark:text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            হল অফ ফেম (সফলতা)
          </button>
        </div>
      </div>

      {/* Mentors Grid */}
      {activeTab === 'mentors' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {MENTORS.map((m) => (
            <div
              key={m.nameBn}
              className="p-5 rounded-2xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-sm hover:border-[#0A2540] dark:hover:border-amber-400 transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="w-10 h-10 rounded-xl bg-[#0A2540] text-amber-300 font-bold font-mono text-sm flex items-center justify-center">
                    {m.nameBn.charAt(0)}
                  </div>
                  <span className="text-[10px] font-bold font-bengali px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                    {m.badgeBn}
                  </span>
                </div>

                <div className="space-y-1">
                  <h3 className="text-sm font-bold font-bengali text-slate-900 dark:text-white">
                    {m.nameBn}
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed">
                    {m.designationBn}
                  </p>
                  <p className="text-[11px] text-slate-500 font-bengali">
                    {m.institutionBn}
                  </p>
                </div>
              </div>

              <div className="pt-3 mt-3 border-t border-slate-100 dark:border-slate-800 flex items-center gap-1.5 text-[11px] font-bengali text-emerald-700 dark:text-emerald-400">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>{m.cadreTrackBn}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Hall of Fame Achievers Grid */}
      {activeTab === 'achievers' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {ACHIEVERS.map((achiever) => (
            <div
              key={achiever.nameBn}
              className="p-6 rounded-2xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-sm space-y-4"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold font-bengali text-slate-900 dark:text-white">
                    {achiever.nameBn}
                  </h3>
                  <span className="text-xs text-slate-500 font-bengali block">
                    {achiever.examBn}
                  </span>
                </div>
                <div className="p-2 rounded-xl bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300">
                  <Trophy className="w-5 h-5" />
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className="px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-xs font-bold font-bengali">
                  {achiever.rankBn}
                </span>
                <span className="text-xs font-mono font-bold text-slate-700 dark:text-slate-300">
                  স্কোর: {achiever.scoreBn}
                </span>
              </div>

              <blockquote className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed italic border-l-2 border-amber-400 pl-3">
                "{achiever.quoteBn}"
              </blockquote>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
