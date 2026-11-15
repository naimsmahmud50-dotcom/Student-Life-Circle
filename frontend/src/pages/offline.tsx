/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      frontend/src/pages/offline.tsx
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization (Inherits Phase 104 Android TWA & Offline Study Arena)
 * PURPOSE:   Provides an uplifting, dignified offline study arena for students
 *            traveling across rural Bangladesh without active cellular connectivity.
 *            Empowers students to browse, search, and practice cached NCTB board question
 *            papers directly from IndexedDB, submit answers to offline sync queues,
 *            and retry connectivity with tactile 3D button physics.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */

import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import {
  WifiOff,
  BookOpen,
  RefreshCw,
  CheckCircle2,
  Award,
  ArrowRight,
  ShieldCheck,
  Zap,
  Search,
  Layers,
  FileText,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { EmptyState } from '@/components/ui/empty-state';
import {
  getAllSavedBoardQuestions,
  searchSavedQuestions,
  markPaperAsRead,
  OfflineVaultStats,
  getOfflineVaultStats
} from '@/lib/offline/offline-papers-store';
import { BoardQuestionItem } from '@/components/curriculum/BoardQuestionArchiveViewer';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';
import { useTranslation, toBengaliDigits } from '@/lib/i18n';

export default function OfflinePage() {
  const { language } = useTranslation();
  const [isChecking, setIsChecking] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSubject, setSelectedSubject] = useState<string>('all');
  const [savedQuestions, setSavedQuestions] = useState<BoardQuestionItem[]>([]);
  const [expandedQuestionId, setExpandedQuestionId] = useState<string | null>(null);
  const [readQuestions, setReadQuestions] = useState<Set<string>>(new Set());
  const [vaultStats, setVaultStats] = useState<OfflineVaultStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    document.title = language === 'bn'
      ? 'অফলাইন স্টাডি এরিনা ও সংরক্ষিত বোর্ড প্রশ্ন | অগ্রযাত্রা'
      : 'Offline Study Arena & Saved Past Papers | Ogrojatra';
  }, [language]);

  // Load questions from IndexedDB on mount
  useEffect(() => {
    let isMounted = true;

    async function loadVault() {
      try {
        const [questions, stats] = await Promise.all([
          getAllSavedBoardQuestions(),
          getOfflineVaultStats()
        ]);
        if (isMounted) {
          setSavedQuestions(questions);
          setVaultStats(stats);
        }
      } catch (err) {
        console.warn('[Offline Vault] Non-fatal load error:', err);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }

    loadVault();

    return () => {
      isMounted = false;
    };
  }, []);

  // Monitor connectivity
  useEffect(() => {
    setIsOnline(typeof navigator !== 'undefined' ? navigator.onLine : false);

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleRetryConnection = () => {
    setIsChecking(true);
    setTimeout(() => {
      setIsChecking(false);
      if (typeof window !== 'undefined' && navigator.onLine) {
        window.location.reload();
      }
    }, 1000);
  };

  const handleToggleExpand = (id: string) => {
    if (expandedQuestionId === id) {
      setExpandedQuestionId(null);
    } else {
      setExpandedQuestionId(id);
      if (!readQuestions.has(id)) {
        setReadQuestions((prev) => new Set(prev).add(id));
        markPaperAsRead(id, 100).catch(() => {});
      }
    }
  };

  // Filter questions
  const filteredQuestions = useMemo(() => {
    return savedQuestions.filter((item) => {
      const matchSubject = selectedSubject === 'all' || item.subject_bn === selectedSubject;
      if (!matchSubject) return false;

      if (!searchQuery.trim()) return true;
      const q = searchQuery.toLowerCase();
      return (
        item.subject_bn.toLowerCase().includes(q) ||
        item.board_bn.toLowerCase().includes(q) ||
        item.chapter.toLowerCase().includes(q) ||
        item.stem_bn.toLowerCase().includes(q) ||
        item.year.toString().includes(q)
      );
    });
  }, [savedQuestions, selectedSubject, searchQuery]);

  return (
    <>
      <AppHead
        title={
          language === 'bn'
            ? 'অফলাইন স্টাডি এরিনা ও সংরক্ষিত বোর্ড প্রশ্ন | অগ্রযাত্রা'
            : 'Offline Study Arena & Saved Past Papers | Ogrojatra'
        }
        description={
          language === 'bn'
            ? 'ইন্টারনেট সংযোগ ছাড়াই ডিভাইসে সংরক্ষিত এনসিটিবি অনুমোদিত অফিসিয়াল বোর্ড প্রশ্ন ও KaTeX গাণিতিক সমাধান অনুশীলন করুন।'
            : 'Practice official NCTB board questions and KaTeX mathematical solutions cached securely on your device without internet.'
        }
        canonicalUrl="/offline"
        ogType="website"
      />

      <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans transition-colors duration-200">
        <Navbar currentStage={language === 'bn' ? 'এইচএসসি ও এসএসসি প্রস্তুতি (HSC & SSC)' : 'HSC & SSC Preparation'} />

        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
          {/* Unified PageHeader */}
          <PageHeader
            category={language === 'bn' ? 'অফলাইন রেসিলিয়েন্স ও লোকাল ভল্ট' : 'Offline Resilience & Local Vault'}
            title={language === 'bn' ? 'অফলাইন স্টাডি এরিনা ও বোর্ড প্রশ্ন ব্যাংক' : 'Offline Study Arena & Question Bank'}
            subtitle={
              language === 'bn'
                ? 'ইন্টারনেট সংযোগ নেই? প্রস্তুতি কিন্তু থেমে নেই! গ্রামীণ বা দূরপাল্লার যাত্রায় নেটওয়ার্ক হারিয়ে গেলেও তোমার ডিভাইসে সংরক্ষিত এনসিটিবি প্রশ্ন ও সমাধান সম্পূর্ণ প্রস্তুত।'
                : 'No internet connection? Your preparation never stops! Even during rural travel with zero network, your cached NCTB questions and solutions are completely ready.'
            }
            breadcrumbs={[
              { label: language === 'bn' ? 'নীড়পাতা' : 'Home', href: '/' },
              { label: language === 'bn' ? 'বোর্ড আর্কাইভ' : 'Board Archives', href: '/board-archives' },
              { label: language === 'bn' ? 'অফলাইন এরিনা' : 'Offline Arena' }
            ]}
            stats={[
              {
                label: language === 'bn' ? 'সংরক্ষিত প্রশ্নপত্র' : 'Saved Questions',
                value: language === 'bn' ? `${toBengaliDigits(savedQuestions.length)}টি` : `${savedQuestions.length} Items`
              },
              {
                label: language === 'bn' ? 'কভারেজ বোর্ড' : 'Covered Boards',
                value: language === 'bn' ? `${toBengaliDigits(vaultStats?.boards.length || 0)}টি` : `${vaultStats?.boards.length || 0} Boards`
              },
              {
                label: language === 'bn' ? 'সংযোগ অবস্থা' : 'Connection Status',
                value: isOnline ? (language === 'bn' ? 'অনলাইন' : 'Online') : (language === 'bn' ? 'অফলাইন' : 'Offline')
              }
            ]}
          />

          {/* Connection Status & Quick Action Controls */}
          <Card className="p-6 bg-white dark:bg-[#0F172A] border-slate-200/80 dark:border-slate-800/80 shadow-sm">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div
                  className={`p-3 rounded-2xl border ${
                    isOnline
                      ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                      : 'bg-amber-500/10 border-amber-500/20 text-amber-400'
                  }`}
                >
                  <WifiOff className="w-5 h-5 animate-pulse" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold font-bengali text-slate-900 dark:text-white text-base">
                      {isOnline
                        ? (language === 'bn' ? 'ইন্টারনেট সংযুক্ত রয়েছে' : 'Internet Connected')
                        : (language === 'bn' ? 'বর্তমানে অফলাইন মোড সক্রিয়' : 'Currently in Offline Mode')}
                    </span>
                    <span
                      className={`w-2 h-2 rounded-full ${
                        isOnline ? 'bg-emerald-400' : 'bg-amber-400 animate-ping'
                      }`}
                    />
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 font-bengali mt-0.5">
                    {isOnline
                      ? (language === 'bn'
                          ? 'সার্ভারের সাথে রিয়েল-টাইম সিঙ্ক সক্রিয়। সম্পূর্ণ পোর্টাল ব্রাউজ করতে পারেন।'
                          : 'Real-time server sync is active. You can browse the complete portal.')
                      : (language === 'bn'
                          ? 'ডিভাইসে সংরক্ষিত প্রশ্নসমূহ ব্রাউজ করুন। নতুন উত্তর দিলে ব্যাকগ্রাউন্ডে জমা থাকবে।'
                          : 'Browse questions cached on this device. New responses will be queued in the background.')}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3 w-full sm:w-auto">
                <Button
                  variant="outline"
                  onClick={handleRetryConnection}
                  disabled={isChecking}
                  className="w-full sm:w-auto"
                >
                  <RefreshCw className={`w-4 h-4 text-blue-400 ${isChecking ? 'animate-spin' : ''}`} />
                  <span>
                    {isChecking
                      ? (language === 'bn' ? 'পরীক্ষা করা হচ্ছে...' : 'Checking...')
                      : (language === 'bn' ? 'সংযোগ পরীক্ষা করুন' : 'Check Connection')}
                  </span>
                </Button>
                <Link href="/board-archives" className="w-full sm:w-auto">
                  <Button variant="oxford" className="w-full sm:w-auto shadow-[0_4px_0_0_#1D4ED8]">
                    <BookOpen className="w-4 h-4" />
                    <span>{language === 'bn' ? 'অনলাইন আর্কাইভ' : 'Online Archives'}</span>
                  </Button>
                </Link>
              </div>
            </div>
          </Card>

          {/* Search & Subject Filter Bar */}
          <div className="space-y-4">
            <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <Input
                  type="text"
                  placeholder={
                    language === 'bn'
                      ? 'সংরক্ষিত প্রশ্নের অধ্যায়, বোর্ড বা বিষয় খুঁজুন...'
                      : 'Search cached chapter, board, or subject...'
                  }
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>

              {vaultStats && vaultStats.subjects.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto pb-1">
                  <button
                    type="button"
                    onClick={() => setSelectedSubject('all')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-semibold font-bengali transition-colors ${
                      selectedSubject === 'all'
                        ? 'bg-blue-600 text-white shadow-sm'
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                    }`}
                  >
                    {language === 'bn'
                      ? `সকল বিষয় (${toBengaliDigits(savedQuestions.length)})`
                      : `All Subjects (${savedQuestions.length})`}
                  </button>
                  {vaultStats.subjects.map((sub) => (
                    <button
                      key={sub}
                      type="button"
                      onClick={() => setSelectedSubject(sub)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-semibold font-bengali whitespace-nowrap transition-colors ${
                        selectedSubject === sub
                          ? 'bg-blue-600 text-white shadow-sm'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                      }`}
                    >
                      {sub}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Offline Questions Bento Grid */}
            {filteredQuestions.length === 0 ? (
              <EmptyState
                icon={<FileText className="w-8 h-8 text-slate-400" />}
                title={language === 'bn' ? 'কোনো সংরক্ষিত প্রশ্ন পাওয়া যায়নি' : 'No Cached Questions Found'}
                description={
                  searchQuery
                    ? (language === 'bn'
                        ? `"${searchQuery}" এর সাথে মিলে এমন কোনো অফলাইন প্রশ্ন নেই।`
                        : `No offline questions matching "${searchQuery}".`)
                    : (language === 'bn'
                        ? 'ডিভাইসের ভল্টে কোনো প্রশ্ন সংরক্ষিত নেই। অনলাইন সংযোগ ফিরে এলে বোর্ড প্রশ্ন খুললে স্বয়ংক্রিয়ভাবে সংরক্ষিত হবে।'
                        : 'No questions cached in the offline vault. Questions will cache automatically once opened with an active connection.')
                }
                actionLabel={language === 'bn' ? 'অনুশীলন সেটে যান' : 'Go to Practice Sets'}
                onAction={() => {
                  window.location.href = '/practice';
                }}
              />
            ) : (
              <div className="grid grid-cols-1 gap-4">
                {filteredQuestions.map((q) => {
                  const isExpanded = expandedQuestionId === q.id;
                  const isRead = readQuestions.has(q.id);

                  return (
                    <Card
                      key={q.id}
                      className="p-5 sm:p-6 bg-white dark:bg-[#0F172A] border-slate-200/80 dark:border-slate-800/80 hover:border-blue-400/50 dark:hover:border-blue-500/40 transition-all duration-200"
                    >
                      {/* Paper Metadata Badges */}
                      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800/80 pb-3">
                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold font-bengali bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 border border-blue-200/50 dark:border-blue-800/50">
                            {q.subject_bn} ({q.paper})
                          </span>
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold font-bengali bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                            {q.board_bn} • {language === 'bn' ? toBengaliDigits(q.year) : q.year}
                          </span>
                          <span className="px-2 py-0.5 rounded-md text-[11px] font-mono text-slate-500 dark:text-slate-400">
                            {q.question_type}
                          </span>
                        </div>

                        <div className="flex items-center gap-2">
                          {isRead && (
                            <span className="inline-flex items-center gap-1 text-[11px] text-emerald-500 dark:text-emerald-400 font-bengali">
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>{language === 'bn' ? 'অনুশীলিত' : 'Completed'}</span>
                            </span>
                          )}
                          <span className="text-xs font-semibold font-bengali text-amber-600 dark:text-amber-400">
                            {language === 'bn' ? `পূর্ণমান: ${toBengaliDigits(q.marks_total)}` : `Marks: ${q.marks_total}`}
                          </span>
                        </div>
                      </div>

                      {/* Chapter Title & Stem */}
                      <div className="pt-3 space-y-2">
                        <h3 className="text-base font-bold font-bengali text-slate-900 dark:text-white flex items-center gap-2">
                          <Layers className="w-4 h-4 text-blue-500 shrink-0" />
                          <span>{q.chapter}</span>
                        </h3>

                        <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800/60 text-sm font-bengali leading-relaxed text-slate-800 dark:text-slate-200">
                          <KaTeXRenderer content={q.stem_bn} />
                        </div>
                      </div>

                      {/* Expand / Collapse Control */}
                      <div className="pt-4 flex items-center justify-between">
                        <button
                          type="button"
                          onClick={() => handleToggleExpand(q.id)}
                          className="inline-flex items-center gap-1.5 text-xs font-semibold font-bengali text-blue-600 dark:text-blue-400 hover:text-blue-500 focus:outline-none"
                        >
                          <span>
                            {isExpanded
                              ? (language === 'bn' ? 'প্রশ্ন ও সমাধান লুকান' : 'Hide Solution')
                              : (language === 'bn' ? 'উপ-প্রশ্ন ও KaTeX সমাধান দেখুন' : 'View Sub-questions & KaTeX Solution')}
                          </span>
                          {isExpanded ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )}
                        </button>

                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-mono text-slate-400">
                            ID: {q.id}
                          </span>
                        </div>
                      </div>

                      {/* Sub-questions & Detailed Solutions Accordion */}
                      {isExpanded && q.cq_sub_questions && (
                        <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800/80 space-y-4 animate-in fade-in duration-200">
                          {Object.entries(q.cq_sub_questions).map(([key, subQ]) => (
                            <div
                              key={key}
                              className="p-4 rounded-xl bg-slate-50/80 dark:bg-[#090D16] border border-slate-200/60 dark:border-slate-800 space-y-2"
                            >
                              <div className="flex items-center justify-between text-xs">
                                <span className="font-bold font-bengali text-blue-600 dark:text-blue-400">
                                  {subQ.label} {subQ.type}
                                </span>
                                <span className="font-mono text-slate-500 dark:text-slate-400">
                                  {language === 'bn' ? `নম্বর: ${toBengaliDigits(subQ.marks)}` : `Marks: ${subQ.marks}`}
                                </span>
                              </div>

                              <p className="text-sm font-semibold font-bengali text-slate-900 dark:text-white">
                                {subQ.question_bn}
                              </p>

                              <div className="pt-2 border-t border-slate-200/50 dark:border-slate-800/50">
                                <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 font-bengali">
                                  {language === 'bn' ? 'মডেল সমাধান:' : 'Model Solution:'}
                                </span>
                                <div className="text-xs sm:text-sm font-bengali text-slate-700 dark:text-slate-300 mt-1 whitespace-pre-line leading-relaxed">
                                  <KaTeXRenderer content={subQ.solution_bn} />
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </Card>
                  );
                })}
              </div>
            )}
          </div>

          {/* Offline Sync Assurance Banner */}
          <div className="p-4 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200/60 dark:border-emerald-800/40 text-left flex items-start gap-3">
            <Zap className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" strokeWidth={1.75} />
            <p className="text-xs sm:text-sm font-bengali text-emerald-900 dark:text-emerald-200 leading-relaxed">
              <span className="font-bold">
                {language === 'bn' ? 'স্বয়ংক্রিয় ব্যাকগ্রাউন্ড সিঙ্ক ও নিরাপত্তা:' : 'Automatic Background Sync & Security:'}
              </span>{' '}
              {language === 'bn'
                ? 'অফলাইনে তোমার অনুশীলন করা যেকোনো প্রশ্নের অগ্রগতি ও নোট ব্রাউজারের এনক্রিপ্টেড IndexedDB ভল্টে সংরক্ষিত থাকবে। নেটওয়ার্ক পুনঃস্থাপিত হওয়ার সাথে সাথে ডেটা ক্লাউড সার্ভারে সিঙ্ক হয়ে যাবে।'
                : 'Any progress, answers, or notes made offline remain securely encrypted within the browser IndexedDB vault and sync to cloud servers automatically upon network reconnection.'}
            </p>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
