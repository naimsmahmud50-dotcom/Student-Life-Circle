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

import React, { useState, useEffect } from 'react';
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
import { useTranslation, toBengaliDigits } from '@/lib/i18n';

export default function AchievementsPage() {
  const { language } = useTranslation();
  const isBn = language === 'bn';
  const [isShieldModalOpen, setIsShieldModalOpen] = useState<boolean>(false);
  const [currentStreak, setCurrentStreak] = useState<number>(24);
  const [availableShields, setAvailableShields] = useState<number>(2);
  const [todayXp, setTodayXp] = useState<number>(280);
  const dailyCap = 500;

  useEffect(() => {
    document.title = isBn
      ? 'অর্জন ও ডিজিটাল সনদ | অগ্রযাত্রা'
      : 'Achievements & Digital Credentials | Agragoti';
  }, [isBn]);

  const handleRecoverStreak = () => {
    setCurrentStreak((prev) => prev + 1);
  };

  const handleActivateShield = () => {
    if (availableShields > 0) {
      setAvailableShields((prev) => prev - 1);
    }
  };

  return (
    <div className={`min-h-screen bg-slate-950 text-slate-100 flex flex-col ${isBn ? 'font-bengali' : 'font-sans'}`}>
      <AppHead
        title={isBn ? "অর্জন ও ডিজিটাল সনদ | অগ্রযাত্রা" : "Achievements & Digital Credentials | Agragoti"}
        description={isBn ? "তোমার ধারাবাহিক অধ্যবসায়, বিষয়ভিত্তিক দক্ষতা এবং যাচাইকৃত অ্যাকাডেমিক সনদ পোর্টফোলিও।" : "Your continuous perseverance, subject mastery, and verified academic credentials portfolio."}
      />

      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col space-y-8">
        {/* Header Intro */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
              <Award className="w-4 h-4" strokeWidth={1.75} />
              <span>{isBn ? "মর্যাদাপূর্ণ অর্জন ও সামাজিক প্রমাণ" : "Dignified Achievements & Social Proof"}</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-display">
              {isBn ? "অ্যাকাডেমিক দক্ষতা ও ধারাবাহিকতা পোর্টফোলিও" : "Academic Mastery & Consistency Portfolio"}
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-2xl">
              {isBn
                ? "সস্তা গ্যামিফিকেশন নয়, এখানে মূল্যায়িত হয় গভীর অধ্যবসায় ও যাচাইযোগ্য জাতীয় মেধা মানদণ্ড।"
                : "Not cheap gamification, but rigorous dedication and verifiable national merit benchmarks."}
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
              <span>{isBn ? "স্ট্রিক শিল্ড পরিচালনা" : "Manage Streak Shield"}</span>
            </button>

            <Link
              href="/verify"
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all active:scale-95 shadow-md"
            >
              <ExternalLink className="w-4 h-4" strokeWidth={1.75} />
              <span>{isBn ? "সনদ যাচাই লেজার" : "Credential Ledger"}</span>
            </Link>
          </div>
        </div>

        {/* Bento Grid Top Section: Streak Radiance, Daily Anti-Burnout Cap, Overall Velocity */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Warm Amber Glowing Streak */}
          <div className="relative p-6 sm:p-7 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl flex flex-col justify-between overflow-hidden">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  {isBn ? "ধারাবাহিক অধ্যবসায় (Streak)" : "Continuous Streak"}
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-amber-950 text-amber-400 border border-amber-800/60 text-[11px] font-semibold">
                  {isBn ? "সক্রিয়" : "Active"}
                </span>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl sm:text-5xl font-extrabold text-amber-400 font-numeric tracking-tight">
                  {isBn ? toBengaliDigits(currentStreak) : currentStreak}
                </span>
                <span className="text-base text-slate-300 font-bold">{isBn ? "দিন" : "Days"}</span>
              </div>
              <p className="text-xs text-slate-400 mt-2">
                {isBn ? "সর্বোচ্চ রেকর্ড: " : "Peak Record: "}
                <strong className="text-white font-numeric">{isBn ? "৪২ দিন" : "42 Days"}</strong> {isBn ? "(টানা ৩ সপ্তাহ নিয়মিত প্রস্তুতি)" : "(3 consecutive weeks of regular study)"}
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
                <span>{isBn ? `${toBengaliDigits(availableShields)} টি ফ্রিজ শিল্ড অবশিষ্ট` : `${availableShields} Freeze Shields left`}</span>
              </span>
              <button
                type="button"
                onClick={() => setIsShieldModalOpen(true)}
                className="text-amber-400 font-semibold hover:underline"
              >
                {isBn ? "শিল্ড যোগ করুন" : "Add Shield"}
              </button>
            </div>
          </div>

          {/* Card 2: Anti-Burnout Daily XP Progress */}
          <div className="p-6 sm:p-7 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  {isBn ? "দৈনিক সীমা (Anti-Burnout Cap)" : "Daily Cap (Anti-Burnout)"}
                </span>
                <span className="px-2.5 py-0.5 rounded-full bg-blue-950 text-blue-400 border border-blue-800/60 text-[11px] font-semibold">
                  {isBn ? "মানসিক স্বাস্থ্য সুরক্ষা" : "Mental Well-being"}
                </span>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl sm:text-5xl font-extrabold text-white font-numeric tracking-tight">
                  {isBn ? toBengaliDigits(todayXp) : todayXp}
                </span>
                <span className="text-sm text-slate-400 font-numeric">/ {isBn ? toBengaliDigits(dailyCap) : dailyCap} XP</span>
              </div>

              {/* Progress bar */}
              <div className="w-full h-2.5 bg-slate-800 rounded-full mt-4 overflow-hidden">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, (todayXp / dailyCap) * 100)}%` }}
                />
              </div>
              <p className="text-xs text-slate-400 mt-2">
                {isBn
                  ? "দৈনিক লক্ষ্য অর্জিত হলে অতিরিক্ত চাপ না নিয়ে গভীর ঘুমের বিশ্রাম নেওয়া বাঞ্ছনীয়।"
                  : "Once the daily target is reached, rest and recharge without extra pressure."}
              </p>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>{isBn ? "মোট অর্জিত পয়েন্ট:" : "Total XP Earned:"}</span>
              <strong className="text-white font-numeric">{isBn ? "৮,৪৫০ XP" : "8,450 XP"}</strong>
            </div>
          </div>

          {/* Card 3: National Standing & Skill Velocity */}
          <div className="p-6 sm:p-7 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  {isBn ? "জাতীয় মেধা অবস্থান" : "National Percentile"}
                </span>
                <TrendingUp className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl sm:text-5xl font-extrabold text-emerald-400 font-numeric tracking-tight">
                  {isBn ? "৯৭.৪%" : "97.4%"}
                </span>
                <span className="text-xs text-slate-400">{isBn ? "পার্সেন্টাইল" : "Percentile"}</span>
              </div>
              <p className="text-xs text-slate-400 mt-2">
                {isBn
                  ? "বিজ্ঞান ও উচ্চতর গণিত বিভাগে সারাদেশের শীর্ষ ৩% শিক্ষার্থীদের অগ্রভাগে তোমার অবস্থান।"
                  : "You are ranked in the top 3% nationwide across Science and Higher Math disciplines."}
              </p>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>{isBn ? "যাচাইকৃত ব্যাজ:" : "Verified Badges:"}</span>
              <strong className="text-white font-numeric">{isBn ? "৩টি অর্জিত" : "3 Earned"}</strong>
            </div>
          </div>
        </div>

        {/* Verifiable Cryptographic Mastery Badges Section */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white font-display">
                {isBn ? "যাচাইযোগ্য দক্ষতা সনদ ব্যাজ (Cryptographic Badges)" : "Verifiable Skill Badges (Cryptographic Proof)"}
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                {isBn
                  ? "প্রতিটি ব্যাজ HMAC-SHA256 অ্যালগরিদমে ডিজিটাল সাক্ষরিত এবং পাবলিক লেজারে যাচাইযোগ্য।"
                  : "Each badge is HMAC-SHA256 cryptographically sealed and verifiable on public ledger."}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MasteryBadgeCard
              badgeId="badge-hsc-physics-mechanics-top3"
              title={isBn ? "এইচএসসি পদার্থবিজ্ঞান: বলবিদ্যা দক্ষতা" : "HSC Physics: Mechanics Mastery"}
              skillName="Classical Mechanics & Rotational Dynamics"
              percentileRank={97.4}
              issuingAuthority={isBn ? "জাতীয় অলিম্পিয়াড ফ্যাকাল্টি" : "National Olympiad Faculty"}
              verificationHash="a7e8b910c2d3e4f5a6b7c8d9e0f1a2b3"
              issuedDate={isBn ? "১৮ অক্টোবর ২০২৬" : "18 October 2026"}
            />

            <MasteryBadgeCard
              badgeId="badge-higher-math-calculus-top5"
              title={isBn ? "উচ্চতর গণিত: ক্যালকুলাস ও কণিক্স" : "Higher Math: Calculus & Conics"}
              skillName="Differential & Integral Calculus"
              percentileRank={95.8}
              issuingAuthority={isBn ? "বুয়েট মেন্টরশিপ কাউন্সিল" : "BUET Mentorship Council"}
              verificationHash="c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8"
              issuedDate={isBn ? "১০ অক্টোবর ২০২৬" : "10 October 2026"}
            />

            <MasteryBadgeCard
              badgeId="badge-chemistry-organic-synthesis"
              title={isBn ? "রসায়ন: জৈব রসায়ন সংশ্লেষণ" : "Chemistry: Organic Synthesis"}
              skillName="Reaction Mechanisms & Isomerism"
              percentileRank={94.2}
              issuingAuthority={isBn ? "জাতীয় পাঠ্যপুস্তক বোর্ড মানদণ্ড" : "NCTB Curriculum Standard"}
              verificationHash="f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6"
              issuedDate={isBn ? "০২ অক্টোবর ২০২৬" : "02 October 2026"}
            />
          </div>
        </section>

        {/* Milestone Timeline (Strava-caliber Milestone Progression) */}
        <section className="p-6 sm:p-8 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-2xl space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-lg font-bold text-white font-display">
                {isBn ? "শিক্ষণ মাইলস্টোন টাইমলাইন" : "Learning Milestone Timeline"}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                {isBn ? "অর্জিত লক্ষ্যের স্বচ্ছ ইতিহাস যা তোমার অধ্যবসায়ের প্রমাণ বহন করে।" : "Transparent ledger of accomplished goals reflecting your disciplined journey."}
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
                    {isBn ? "ক্যালকুলাস ও কণিক্স দক্ষতা সনদ অর্জিত (Top 5%)" : "Calculus & Conics Certificate Earned (Top 5%)"}
                  </h4>
                  <span className="text-xs text-slate-500 font-numeric">{isBn ? "১৮ অক্টোবর ২০২৬" : "18 Oct 2026"}</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  {isBn ? "টানা ২৫টি বুয়েট স্ট্যান্ডার্ড জটিল গাণিতিক সমস্যার সঠিক সমাধান সম্পন্ন।" : "Solved 25 consecutive BUET-standard advanced mathematical problems correctly."}
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
                    {isBn ? "২১ দিনের অবিচল অধ্যবসায় মাইলফলক" : "21-Day Unbroken Habit Milestone"}
                  </h4>
                  <span className="text-xs text-slate-500 font-numeric">{isBn ? "১০ অক্টোবর ২০২৬" : "10 Oct 2026"}</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  {isBn ? "একটি দিনও অপচয় না করে দৈনিক প্রস্তুতি বজায় রাখার অনন্য রেকর্ড।" : "Maintained daily active study discipline without missing a single day."}
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
                    {isBn ? "আসন্ন লক্ষ্য: জাতীয় লাইভ অলিম্পিয়াড সেমিফাইনাল" : "Upcoming Goal: National Live Olympiad Semifinal"}
                  </h4>
                  <span className="text-xs text-blue-400 font-semibold">{isBn ? "চলমান" : "In Progress"}</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  {isBn ? "পরবর্তী পর্ব আগামী শুক্রবার রাত ৮:০০ টায় অনুষ্ঠিত হবে।" : "Next session will be broadcast this Friday at 8:00 PM."}
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
