/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Dignified Academic Achievements Portfolio
 * FILE:      frontend/src/pages/achievements.tsx
 * PHASE:     Phase 102 - Dignified Gamification & Verifiable Social Proof
 * PURPOSE:   Provides a Strava/Brilliant caliber academic milestone showcase:
 *            1. Global Layout: Standard sticky Navbar and dignified 4-tier Footer wrapper.
 *            2. Bento Grid Portfolio: Streak velocity, anti-burnout daily progress, and badges.
 *            3. Verifiable Social Proof: Cryptographic badge cards and QR verification.
 *            4. Empathetic Streak Shield Modal integration.
 * AUDIENCE:  Students, Guardians, Mentors, Evaluators.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA Contrast, Zero Layout Shift, Strict Zero-Emoji.
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Award,
  Flame,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Sparkles,
  Download,
  ExternalLink,
  TrendingUp,
  Calendar,
  BookOpen,
  ArrowRight,
  Shield,
  Zap,
  Target
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { StreakShieldModal } from '@/components/gamification/StreakShieldModal';
import { MasteryBadgeCard } from '@/components/gamification/MasteryBadgeCard';

export default function AchievementsPage() {
  const [isShieldModalOpen, setIsShieldModalOpen] = useState<boolean>(false);
  const [currentStreak, setCurrentStreak] = useState<number>(24);
  const [availableShields, setAvailableShields] = useState<number>(2);
  const [todayXp, setTodayXp] = useState<number>(280);
  const dailyCap = 500;

  const handleRecoverStreak = () => {
    setCurrentStreak((prev) => prev + 1);
  };

  const handleActivateShield = () => {
    if (availableShields > 0) {
      setAvailableShields((prev) => prev - 1);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali">
      <AppHead
        title="অর্জন ও ডিজিটাল সনদ | অগ্রযাত্রা"
        description="তোমার ধারাবাহিক অধ্যবসায়, বিষয়ভিত্তিক দক্ষতা এবং যাচাইকৃত অ্যাকাডেমিক সনদ পোর্টফোলিও।"
      />

      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col space-y-8">
        {/* Header Intro */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
              <Award className="w-4 h-4" strokeWidth={1.75} />
              <span>মর্যাদাপূর্ণ অর্জন ও সামাজিক প্রমাণ</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-display">
              অ্যাকাডেমিক দক্ষতা ও ধারাবাহিকতা পোর্টফোলিও
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-2xl">
              সস্তা গ্যামিফিকেশন নয়, এখানে মূল্যায়িত হয় গভীর অধ্যবসায় ও যাচাইযোগ্য জাতীয় মেধা মানদণ্ড।
            </p>
          </div>

          {/* Action: Open Streak Shield & Download Portfolio */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setIsShieldModalOpen(true)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-bold transition-all active:scale-95 shadow-sm"
            >
              <Flame className="w-4 h-4 text-amber-500 fill-amber-500/20" strokeWidth={1.75} />
              <span>স্ট্রিক শিল্ড পরিচালনা</span>
            </button>

            <Link
              href="/verify"
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all active:scale-95 shadow-md"
            >
              <ExternalLink className="w-4 h-4" strokeWidth={1.75} />
              <span>সনদ যাচাই লেজার</span>
            </Link>
          </div>
        </div>

        {/* Bento Grid Top Section: Streak Radiance, Daily Anti-Burnout Cap, Overall Velocity */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Warm Amber Glowing Streak */}
          <div className="relative p-6 sm:p-7 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl flex flex-col justify-between overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/10 rounded-full blur-3xl -mr-10 -mt-10" />
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  ধারাবাহিক অধ্যবসায় (Streak)
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-amber-950 text-amber-400 border border-amber-800/60 text-[11px] font-semibold">
                  সক্রিয়
                </span>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl sm:text-5xl font-extrabold text-amber-400 font-numeric tracking-tight">
                  {currentStreak}
                </span>
                <span className="text-base text-slate-300 font-bold">দিন</span>
              </div>
              <p className="text-xs text-slate-400 mt-2">
                সর্বোচ্চ রেকর্ড: <strong className="text-white font-numeric">৪২ দিন</strong> (টানা ৩ সপ্তাহ নিয়মিত প্রস্তুতি)
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
                <span>{availableShields} টি ফ্রিজ শিল্ড অবশিষ্ট</span>
              </span>
              <button
                type="button"
                onClick={() => setIsShieldModalOpen(true)}
                className="text-amber-400 font-semibold hover:underline"
              >
                শিল্ড যোগ করুন
              </button>
            </div>
          </div>

          {/* Card 2: Anti-Burnout Daily XP Progress */}
          <div className="p-6 sm:p-7 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  দৈনিক সীমা (Anti-Burnout Cap)
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-blue-950 text-blue-400 border border-blue-800/60 text-[11px] font-semibold">
                  মানসিক স্বাস্থ্য সুরক্ষা
                </span>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl sm:text-5xl font-extrabold text-white font-numeric tracking-tight">
                  {todayXp}
                </span>
                <span className="text-sm text-slate-400 font-numeric">/ {dailyCap} XP</span>
              </div>

              {/* Progress bar */}
              <div className="w-full h-2.5 bg-slate-800 rounded-full mt-4 overflow-hidden">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, (todayXp / dailyCap) * 100)}%` }}
                />
              </div>
              <p className="text-xs text-slate-400 mt-2">
                দৈনিক লক্ষ্য অর্জিত হলে অতিরিক্ত চাপ না নিয়ে গভীর ঘুমের বিশ্রাম নেওয়া বাঞ্ছনীয়।
              </p>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>মোট অর্জিত পয়েন্ট:</span>
              <strong className="text-white font-numeric">৮,৪৫০ XP</strong>
            </div>
          </div>

          {/* Card 3: National Standing & Skill Velocity */}
          <div className="p-6 sm:p-7 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  জাতীয় মেধা অবস্থান
                </span>
                <TrendingUp className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl sm:text-5xl font-extrabold text-emerald-400 font-numeric tracking-tight">
                  ৯৭.৪%
                </span>
                <span className="text-xs text-slate-400">পার্সেন্টাইল</span>
              </div>
              <p className="text-xs text-slate-400 mt-2">
                বিজ্ঞান ও উচ্চতর গণিত বিভাগে সারাদেশের শীর্ষ ৩% শিক্ষার্থীদের অগ্রভাগে তোমার অবস্থান।
              </p>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>যাচাইকৃত ব্যাজ:</span>
              <strong className="text-white font-numeric">৩টি অর্জিত</strong>
            </div>
          </div>
        </div>

        {/* Verifiable Cryptographic Mastery Badges Section */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white font-display">
                যাচাইযোগ্য দক্ষতা সনদ ব্যাজ (Cryptographic Badges)
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                প্রতিটি ব্যাজ HMAC-SHA256 অ্যালগরিদমে ডিজিটাল সাক্ষরিত এবং পাবলিক লেজারে যাচাইযোগ্য।
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MasteryBadgeCard
              badgeId="badge-hsc-physics-mechanics-top3"
              title="এইচএসসি পদার্থবিজ্ঞান: বলবিদ্যা দক্ষতা"
              skillName="Classical Mechanics & Rotational Dynamics"
              percentileRank={97.4}
              issuingAuthority="জাতীয় অলিম্পিয়াড ফ্যাকাল্টি"
              verificationHash="a7e8b910c2d3e4f5a6b7c8d9e0f1a2b3"
              issuedDate="১৮ অক্টোবর ২০২৬"
            />

            <MasteryBadgeCard
              badgeId="badge-higher-math-calculus-top5"
              title="উচ্চতর গণিত: ক্যালকুলাস ও কণিক্স"
              skillName="Differential & Integral Calculus"
              percentileRank={95.8}
              issuingAuthority="বুয়েট মেন্টরশিপ কাউন্সিল"
              verificationHash="c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8"
              issuedDate="১০ অক্টোবর ২০২৬"
            />

            <MasteryBadgeCard
              badgeId="badge-chemistry-organic-synthesis"
              title="রসায়ন: জৈব রসায়ন সংশ্লেষণ"
              skillName="Reaction Mechanisms & Isomerism"
              percentileRank={94.2}
              issuingAuthority="জাতীয় পাঠ্যপুস্তক বোর্ড মানদণ্ড"
              verificationHash="f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6"
              issuedDate="০২ অক্টোবর ২০২৬"
            />
          </div>
        </section>

        {/* Milestone Timeline (Strava-caliber Milestone Progression) */}
        <section className="p-6 sm:p-8 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-lg font-bold text-white font-display">
                শিক্ষণ মাইলস্টোন টাইমলাইন
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                অর্জিত লক্ষ্যের স্বচ্ছ ইতিহাস যা তোমার অধ্যবসায়ের প্রমাণ বহন করে।
              </p>
            </div>
            <Calendar className="w-5 h-5 text-slate-400" strokeWidth={1.75} />
          </div>

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-500/30">
                <CheckCircle2 className="w-4 h-4" strokeWidth={2} />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-white">
                    ক্যালকুলাস ও কণিক্স দক্ষতা সনদ অর্জিত (Top 5%)
                  </h4>
                  <span className="text-xs text-slate-500 font-numeric">১৮ অক্টোবর ২০২৬</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  টানা ২৫টি বুয়েট স্ট্যান্ডার্ড জটিল গাণিতিক সমস্যার সঠিক সমাধান সম্পন্ন।
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-500/30">
                <CheckCircle2 className="w-4 h-4" strokeWidth={2} />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-white">
                    ২১ দিনের অবিচল অধ্যবসায় মাইলফলক
                  </h4>
                  <span className="text-xs text-slate-500 font-numeric">১০ অক্টোবর ২০২৬</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  একটি দিনও অপচয় না করে দৈনিক প্রস্তুতি বজায় রাখার অনন্য রেকর্ড।
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0 border border-blue-500/30">
                <Target className="w-4 h-4" strokeWidth={2} />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-white">
                    আসন্ন লক্ষ্য: জাতীয় লাইভ অলিম্পিয়াড সেমিফাইনাল
                  </h4>
                  <span className="text-xs text-blue-400 font-semibold">চলমান</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  পরবর্তী পর্ব আগামী শুক্রবার রাত ৮:০০ টায় অনুষ্ঠিত হবে।
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />

      {/* Streak Shield Recovery Modal */}
      <StreakShieldModal
        isOpen={isShieldModalOpen}
        onClose={() => setIsShieldModalOpen(false)}
        currentStreak={currentStreak}
        availableShields={availableShields}
        isStreakAtRisk={false}
        onRecoverViaDrill={handleRecoverStreak}
        onActivateShield={handleActivateShield}
      />
    </div>
  );
}
