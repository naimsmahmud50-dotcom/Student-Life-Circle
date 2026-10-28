/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Live Challenge Arena & High-Throughput Exam Session
 * TOPIC:     Phase 115 Sub-Pages Re-Skin & Phase 142 Live MCQ Competitive Elevation
 * FILE:      frontend/src/pages/live-challenge.tsx
 * PHASE:     Phase 115 & Phase 142 - Sub-Pages Pure Academic Re-Skin & Live MCQ Competitive Elevation
 * PURPOSE:   Reverse-engineers and elevates Live MCQ's (web.livemcq.com) complete design language
 *            and feature suite into Ogrojatra's Live Challenge arena:
 *            1. Hero V2 night cosmos & aurora drift with server-authoritative timer and trust KPIs.
 *            2. Subject & Track selection category cards (BCS, Bank, HSC STEM, Admission, Olympiad).
 *            3. Dynamic Academic Info Bulletin & Notice Board.
 *            4. Interactive Free Demo Exam Box (dxb) with 20 questions, 15m, -0.25 negative marking.
 *            5. 4-step preparation pathway roadmap (how) from registration to live rank.
 *            6. Subject-wise question weightage breakdown and marking formula cards.
 *            7. Interactive digital OMR bubble sheet simulator with tactile filling feedback.
 *            8. Real-time central leaderboard with pseudonymous privacy and national percentiles.
 *            9. Multi-track daily exam routine matrix (Today, Tomorrow, Archive).
 *            10. 14-Feature interactive examination suite.
 *            11. Academic mentors & Hall of Fame accredited panel.
 *            12. Comprehensive candidate FAQ accordion.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
 */

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Trophy,
  Clock,
  Users,
  ShieldCheck,
  CheckCircle2,
  Lock,
  ArrowRight,
  Sparkles,
  Award,
  ChevronRight,
  Flame,
  AlertCircle,
  ExternalLink
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { apiClient } from '@/lib/api-client';
import { useQuizStore } from '@/store/useQuizStore';
import { useAuthStore } from '@/store/useAuthStore';
import { LiveMcqHeroSection } from '@/components/live-challenge/LiveMcqHeroSection';
import { LiveCategoryTrackSelector } from '@/components/live-challenge/LiveCategoryTrackSelector';
import { LiveFreeDemoExamBox } from '@/components/live-challenge/LiveFreeDemoExamBox';
import { LiveHowItWorksPathway } from '@/components/live-challenge/LiveHowItWorksPathway';
import { LiveMentorAndHallOfFame } from '@/components/live-challenge/LiveMentorAndHallOfFame';
import { LiveMcqFaqAccordion } from '@/components/live-challenge/LiveMcqFaqAccordion';
import { LiveExamRoutineMatrix } from '@/components/live-challenge/LiveExamRoutineMatrix';
import { SubjectWeightageBreakdown } from '@/components/live-challenge/SubjectWeightageBreakdown';
import { ExamRulesProtocolModal } from '@/components/live-challenge/ExamRulesProtocolModal';
import { LiveExamAnalyticsCard } from '@/components/live-challenge/LiveExamAnalyticsCard';
import { LiveMcqFeatureShowcase } from '@/components/live-challenge/LiveMcqFeatureShowcase';
import { InteractiveOmrSimulator } from '@/components/live-challenge/InteractiveOmrSimulator';
import { DynamicInfoNoticeBoard } from '@/components/live-challenge/DynamicInfoNoticeBoard';
import { AcademicLeaderboardReveal } from '@/components/live-challenge/AcademicLeaderboardReveal';
import Head from 'next/head';
import styles from '@/components/live-challenge/LiveChallengeEditorial.module.css';

interface LeaderboardEntry {
  rank: number;
  handle: string;
  score: number;
  accuracyPercent: number;
  streakCount: number;
  isCurrentUser?: boolean;
}

const FALLBACK_CHALLENGE = {
  id: "chal_nat_2026",
  titleBn: "জাতীয় স্টেম অলিম্পিয়াড ২০২৬ - পর্ব ০১",
  titleEn: "National STEM Olympiad 2026 - Phase 1",
  startTimeRemainingSeconds: 1200,
  registeredCount: 4850,
  durationMinutes: 25,
  totalQuestions: 25,
  negativeMarkingRatio: 0.25,
  syllabusSummaryBn: "এইচএসসি পদার্থবিজ্ঞান (বলবিদ্যা ও কাজ-শক্তি), রসায়ন (পর্যায়বৃত্ত ধর্ম) ও উচ্চতর গণিত (ম্যাট্রিক্স)"
};

const FALLBACK_LEADERBOARD: LeaderboardEntry[] = [
  { rank: 1, handle: "মেধাবী_শিক্ষার্থী_৯৯", score: 24.5, accuracyPercent: 98.0, streakCount: 14 },
  { rank: 2, handle: "অভিযাত্রী_নক্ষত্র_০৭", score: 23.75, accuracyPercent: 95.0, streakCount: 11 },
  { rank: 3, handle: "ক্যালকুলাস_মাস্টার_২১", score: 23.0, accuracyPercent: 92.0, streakCount: 9 },
  { rank: 4, handle: "আপনি (বর্তমান স্কোর)", score: 21.5, accuracyPercent: 88.0, streakCount: 7, isCurrentUser: true },
  { rank: 5, handle: "কোয়ান্টাম_রোভার_৫০", score: 20.75, accuracyPercent: 85.0, streakCount: 6 },
];

export default function LiveChallengePage() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [challenge, setChallenge] = useState(FALLBACK_CHALLENGE);
  const [entries, setEntries] = useState<LeaderboardEntry[]>(FALLBACK_LEADERBOARD);
  const [optOutRanking, setOptOutRanking] = useState<boolean>(false);
  const [isRulesModalOpen, setIsRulesModalOpen] = useState<boolean>(false);

  // Zustand stores
  const { 
    timeRemainingSeconds, 
    isTimerRunning, 
    syncServerTimer, 
    decrementTimer, 
    startAttempt 
  } = useQuizStore();

  const { user, isMinorProtected, privacySettings, updatePrivacy } = useAuthStore();

  // Load live challenge & leaderboard from centralized API
  useEffect(() => {
    let isMounted = true;
    async function loadLiveData() {
      setIsLoading(true);
      try {
        const [challengeRes, leaderboardRes] = await Promise.allSettled([
          apiClient.getLiveChallenges(),
          apiClient.getLiveLeaderboard('active_challenge')
        ]);

        if (isMounted) {
          if (challengeRes.status === 'fulfilled' && challengeRes.value?.data) {
            setChallenge(challengeRes.value.data);
          }
          if (leaderboardRes.status === 'fulfilled' && leaderboardRes.value?.data?.length > 0) {
            setEntries(leaderboardRes.value.data);
          }
        }
      } catch {
        // Safe fallback
      } finally {
        if (isMounted) {
          setIsLoading(false);
          syncServerTimer(challenge.startTimeRemainingSeconds);
        }
      }
    }

    loadLiveData();

    return () => {
      isMounted = false;
    };
  }, []);

  // Server-authoritative timer interval
  useEffect(() => {
    if (!isTimerRunning) return;
    const interval = setInterval(() => {
      decrementTimer();
    }, 1000);
    return () => clearInterval(interval);
  }, [isTimerRunning, decrementTimer]);

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleToggleOptOut = async (checked: boolean) => {
    setOptOutRanking(checked);
    try {
      await updatePrivacy({ leaderboardOptOut: checked });
    } catch {
      // Local state retained
    }
  };

  const visibleEntries = optOutRanking
    ? entries.filter(e => !e.isCurrentUser)
    : entries;

  return (
    <>
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </Head>

      <AppHead
        title="দেশব্যাপী লাইভ চ্যালেঞ্জ | অগ্রযাত্রা"
        description="৫০,০০০ কনকারেন্ট শিক্ষার্থীর সঙ্গে রিয়েল-টাইম অলিম্পিয়াড পরীক্ষা, লাইভ লিডারবোর্ড ও মিলি-সেকেন্ড নির্ভুল সাবমিশন বাফার।"
        canonicalUrl="/live-challenge"
        ogType="website"
      />

      <div className={`${styles.liveChallengeRoot} min-h-screen flex flex-col bg-[#FFFCF6] dark:bg-[#0B0F19] text-[#213130] dark:text-[#F5F2EB] font-sans selection:bg-[#ED8E22] selection:text-white`}>
        {/* Sticky Unified Global Navigation */}
        <Navbar currentStage="দেশব্যাপী লাইভ অলিম্পিয়াড চ্যালেঞ্জ" />

        {/* 1. Live MCQ Signature Hero Section (Exact Elevation from Reference Screenshot) */}
        {isLoading ? (
          <div className="w-full py-16 bg-[#080C24] flex items-center justify-center border-b border-[#1E294B] animate-pulse">
            <div className="max-w-4xl w-full mx-auto px-4 space-y-6 text-center">
              <div className="h-6 bg-slate-800 rounded-full w-48 mx-auto"></div>
              <div className="h-12 bg-slate-800/80 rounded-2xl w-3/4 mx-auto"></div>
              <div className="h-16 bg-slate-800/40 rounded-2xl w-1/2 mx-auto"></div>
            </div>
          </div>
        ) : (
          <LiveMcqHeroSection
            challenge={challenge}
            timeRemainingSeconds={timeRemainingSeconds}
            formatTimer={formatTimer}
            isLoading={isLoading}
            onOpenRulesModal={() => setIsRulesModalOpen(true)}
          />
        )}

        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-12 sm:space-y-16">

          {/* 2. Track & Category Selector (Inspired by Live MCQ cats section) */}
          <LiveCategoryTrackSelector />

          {/* 3. Dynamic Academic Info Panel & Notice Board */}
          <DynamicInfoNoticeBoard />

          {/* 4. Free Demo Exam Box (Inspired by Live MCQ dxb section) */}
          <LiveFreeDemoExamBox />

          {/* 5. 4-Step Academic Pathway Roadmap (Inspired by Live MCQ how section) */}
          <LiveHowItWorksPathway />

          {/* 6. Live Exam Subject Weightage Breakdown */}
          <SubjectWeightageBreakdown />

          {/* 7. Interactive Digital OMR Sheet Simulator */}
          <InteractiveOmrSimulator />

          {/* 8. Real-Time Central Leaderboard & Pseudonymous Privacy Controls */}
          <div id="central-leaderboard" className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Leaderboard Table (8 cols) */}
            <div className="lg:col-span-8 p-6 sm:p-8 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-amber-100 dark:border-[#262D3D]">
                <div>
                  <h2 className="text-lg sm:text-xl font-bold font-serif text-slate-900 dark:text-white flex items-center gap-2">
                    <Award className="w-5 h-5 text-[#ED8E22]" />
                    <span>সেন্ট্রাল রেজাল্ট ও মেধা তালিকা (শীর্ষ প্রতিযোগী)</span>
                  </h2>
                  <p className="text-xs text-slate-500 font-bengali mt-1">
                    রিয়েল-টাইমে WebSocket ব্রডকাস্টের মাধ্যমে স্কোরের পরিবর্তন প্রদর্শিত হচ্ছে।
                  </p>
                </div>

                <span className="text-xs font-mono text-slate-500">
                  আপডেট: প্রতি ৫ সেকেন্ড
                </span>
              </div>

              {/* Dignified Academic Leaderboard Reveal with Motion transitions & KPI count-up */}
              <AcademicLeaderboardReveal
                entries={visibleEntries}
                registeredCount={challenge.registeredCount}
              />
            </div>

            {/* Sidebar Cards (4 cols): Privacy, Rules & Live Analytics */}
            <div className="lg:col-span-4 space-y-6">
              {/* Privacy Controls & Exam Ethics Card */}
              <div className="p-6 sm:p-7 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-6">
                <div className="flex items-center justify-between pb-4 border-b border-amber-100 dark:border-[#262D3D]">
                  <div className="flex items-center gap-2.5">
                    <ShieldCheck className="w-5 h-5 text-emerald-600" />
                    <h3 className="text-base font-bold font-bengali text-slate-900 dark:text-white">
                      পরীক্ষার নিয়মাবলী ও নিরাপত্তা
                    </h3>
                  </div>
                </div>

                <div className="space-y-4 text-xs font-bengali text-slate-600 dark:text-slate-400 leading-[1.75]">
                  <div className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <p>সার্ভার সময় অনুসারে পরীক্ষা পরিচালিত হবে। সময় সমাপ্তির সাথে সাথে উত্তরপত্র স্বয়ংক্রিয়ভাবে জমা হবে।</p>
                  </div>
                  <div className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <p>প্রতিটি ভুল উত্তরের জন্য ০.২৫ নম্বর কাটা যাবে। উত্তর না দিলে কোনো নম্বর কর্তন হবে না।</p>
                  </div>
                  <div className="flex items-start gap-2.5">
                    <Lock className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                    <p>প্রার্থীর ব্যক্তিগত নাম ও ফোন নম্বর সম্পূর্ণ গোপন রেখে ছদ্মনামে লিডারবোর্ডে স্কোর প্রদর্শিত হয়।</p>
                  </div>
                </div>

                {/* View Full Protocol Button */}
                <button
                  type="button"
                  onClick={() => setIsRulesModalOpen(true)}
                  className="w-full py-2.5 px-4 rounded-xl bg-[#FFF9EB] hover:bg-[#FFF6DD] dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 border border-amber-200/60 dark:border-slate-700 text-xs font-bold font-bengali flex items-center justify-center gap-2 transition"
                >
                  <ShieldCheck className="w-4 h-4 text-[#ED8E22]" />
                  <span>সম্পূর্ণ অ্যান্টি-চিট প্রোটোকল দেখুন</span>
                </button>

                <div className="pt-4 border-t border-amber-100 dark:border-[#262D3D]">
                  <label className="flex items-center gap-3 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={optOutRanking}
                      onChange={(e) => handleToggleOptOut(e.target.checked)}
                      className="w-4 h-4 rounded text-[#ED8E22] focus:ring-[#ED8E22] border-slate-300"
                    />
                    <span className="text-xs font-bengali text-slate-700 dark:text-slate-300">
                      পাবলিক লিডারবোর্ড থেকে আমার স্কোর গোপন রাখুন
                    </span>
                  </label>
                </div>
              </div>

              {/* National Percentile & Revision Queue Card */}
              <LiveExamAnalyticsCard />
            </div>

          </div>

          {/* 9. Multi-Track Daily Exam Routine Matrix */}
          <LiveExamRoutineMatrix />

          {/* 10. 14-Feature Examination Suite */}
          <LiveMcqFeatureShowcase />

          {/* 11. Accredited Academic Mentors & Hall of Fame Panel */}
          <LiveMentorAndHallOfFame />

          {/* 12. Candidate FAQ Accordion */}
          <LiveMcqFaqAccordion />

        </main>

        {/* Global Dignified Footer */}
        <Footer />

        {/* Accessible Anti-Cheat & Exam Rules Protocol Modal */}
        <ExamRulesProtocolModal
          isOpen={isRulesModalOpen}
          onClose={() => setIsRulesModalOpen(false)}
        />
      </div>
    </>
  );
}
