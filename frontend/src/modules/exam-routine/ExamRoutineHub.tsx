/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    ExamRoutineHub Container Component
 * TOPIC:     Comprehensive 200-Day BCS & Admission Routine Calendar Hub
 * FILE:      frontend/src/modules/exam-routine/ExamRoutineHub.tsx
 * PURPOSE:   Coordinates routine calendar view, Friday Mega Model Test countdown,
 *            negative marking simulations, and reminder alert subscriptions.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji, Zero-CLS
 * ========================================================================================
 */

import React from 'react';
import Head from 'next/head';
import { Calendar, RefreshCw } from 'lucide-react';
import { useExamRoutine } from './hooks/useExamRoutine';
import { MegaModelTestCountdown } from './components/MegaModelTestCountdown';
import { RoutineFilterTabs } from './components/RoutineFilterTabs';
import { RoutineCalendarView } from './components/RoutineCalendarView';
import { SyllabusCoverageBar } from './components/SyllabusCoverageBar';
import { NegativeMarkingSimulator } from './components/NegativeMarkingSimulator';
import { RoutineSubscriptionModal } from './components/RoutineSubscriptionModal';

export const ExamRoutineHub: React.FC = () => {
  const {
    routines,
    allRoutinesCount,
    isLoading,
    activeDay,
    countdown,
    selectedExamType,
    setSelectedExamType,
    selectedTrack,
    setSelectedTrack,
    searchQuery,
    setSearchQuery,
    selectedRoutineForSub,
    setSelectedRoutineForSub,
    isSimulatorOpen,
    setIsSimulatorOpen,
    simulationResult,
    isSimulating,
    handleSimulate,
    handleSubscribe,
    refreshRoutines,
  } = useExamRoutine();

  return (
    <>
      <Head>
        <title>পরীক্ষার রুটিন ও মেগা মডেল টেস্ট শিডিউল | অগ্রযাত্রা</title>
        <meta
          name="description"
          content="৪৭তম বিসিএস প্রিলিমিনারি ২০০ দিনের দৈনিক রুটিন এবং বিশ্ববিদ্যালয় ভর্তি মেগা মডেল টেস্ট শিডিউল ক্যালেন্ডার।"
        />
      </Head>

      <div className="min-h-screen bg-slate-50/50 py-8 px-4 sm:px-6 lg:px-8 dark:bg-slate-950 transition-colors">
        <div className="mx-auto max-w-7xl space-y-8">
          {/* Main Title & Breadcrumb Header */}
          <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-5 dark:border-slate-800">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                <Calendar className="h-4 w-4" />
                <span>অগ্রযাত্রা একাডেমিক শিডিউলার</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-serif font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
                লাইভ এমসিকিউ ও মেগা মডেল টেস্ট রুটিন হাব
              </h1>
              <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
                ২০০ দিনের ধারাবাহিক রোডম্যাপ, শুক্রবারের পূর্ণাঙ্গ সিমুলেশন ও সঠিক নেগেটিভ মার্কিং নিরীক্ষা।
              </p>
            </div>

            <button
              type="button"
              onClick={refreshRoutines}
              disabled={isLoading}
              className="inline-flex items-center gap-1.5 self-start sm:self-auto rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isLoading ? 'animate-spin text-emerald-600' : ''}`} />
              <span>রুটিন রিফ্রেশ</span>
            </button>
          </header>

          {/* 1. Friday Mega Model Test Hero Countdown */}
          <MegaModelTestCountdown
            countdown={countdown}
            onSetAlert={() => {
              const megaRoutine = routines.find((r) => r.is_mega_model_test) || routines[0];
              if (megaRoutine) setSelectedRoutineForSub(megaRoutine);
            }}
            onOpenSimulator={() => setIsSimulatorOpen(true)}
          />

          {/* 2. Syllabus Coverage Progress Bar */}
          <SyllabusCoverageBar />

          {/* 3. Filter Tabs & Live Search */}
          <RoutineFilterTabs
            selectedExamType={selectedExamType}
            onSelectExamType={setSelectedExamType}
            selectedTrack={selectedTrack}
            onSelectTrack={setSelectedTrack}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            activeDay={activeDay}
            totalFiltered={routines.length}
          />

          {/* 4. Calendar Timeline Routine Cards */}
          <RoutineCalendarView
            routines={routines}
            isLoading={isLoading}
            onSelectRoutineForSub={(routine) => setSelectedRoutineForSub(routine)}
          />
        </div>
      </div>

      {/* Negative Marking Simulator Modal */}
      <NegativeMarkingSimulator
        isOpen={isSimulatorOpen}
        onClose={() => setIsSimulatorOpen(false)}
        onSimulate={handleSimulate}
        simulationResult={simulationResult}
        isSimulating={isSimulating}
      />

      {/* Routine Subscription Modal */}
      <RoutineSubscriptionModal
        routine={selectedRoutineForSub}
        onClose={() => setSelectedRoutineForSub(null)}
        onSubscribe={handleSubscribe}
      />
    </>
  );
};
