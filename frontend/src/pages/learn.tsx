/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Learning Hub & NCTB Curriculum Navigation
 * TOPIC:     Phase 138 Unified Premium Design System & Sub-pages Elevation
 * FILE:      frontend/src/pages/learn.tsx
 * PHASE:     Phase 115 & Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Standardized academic learning hub with flagship PageHeader,
 *            breadcrumbs, spaced-repetition queue, and tactile 3D physics.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Play,
  RotateCcw,
  Sparkles,
  ChevronRight,
  Video,
  Award,
  Layers,
  X,
  Compass,
  AlertCircle,
  GraduationCap
} from 'lucide-react';
import { AppHead, createCourseSchema } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { HlsLecturePlayer } from '@/components/video/HlsLecturePlayer';

interface ChapterItem {
  id: string;
  number: number;
  titleBn: string;
  topicCount: number;
  progressPercent: number;
  isRevised: boolean;
  videoLectureId?: string;
}

interface SubjectItem {
  id: string;
  stage: 'MIDDLE' | 'SSC' | 'HSC' | 'ADMISSION';
  titleBn: string;
  titleEn: string;
  chaptersCount: number;
  completedPercent: number;
  chapters: ChapterItem[];
}

const CURATED_SUBJECTS: SubjectItem[] = [
  {
    id: 'sub_phys_1',
    stage: 'HSC',
    titleBn: 'পদার্থবিজ্ঞান ১ম পত্র (Physics 1st Paper)',
    titleEn: 'HSC Physics Paper 1',
    chaptersCount: 10,
    completedPercent: 75,
    chapters: [
      { id: 'ch_1', number: 1, titleBn: 'ভেক্টর ও দিক রাশি', topicCount: 8, progressPercent: 100, isRevised: true, videoLectureId: 'lec_vec_01' },
      { id: 'ch_2', number: 2, titleBn: 'গতিবিদ্যা ও একমাত্রিক গতি', topicCount: 12, progressPercent: 85, isRevised: true, videoLectureId: 'lec_kin_02' },
      { id: 'ch_3', number: 3, titleBn: 'নিউটনিয়ান বলবিদ্যা ও ভরবেগ', topicCount: 14, progressPercent: 70, isRevised: false, videoLectureId: 'lec_newton_03' },
      { id: 'ch_4', number: 4, titleBn: 'কাজ, শক্তি ও ক্ষমতা', topicCount: 10, progressPercent: 45, isRevised: false, videoLectureId: 'lec_work_04' },
    ]
  },
  {
    id: 'sub_chem_1',
    stage: 'HSC',
    titleBn: 'রসায়ন ১ম পত্র (Chemistry 1st Paper)',
    titleEn: 'HSC Chemistry Paper 1',
    chaptersCount: 8,
    completedPercent: 60,
    chapters: [
      { id: 'ch_c1', number: 1, titleBn: 'গুণগত রসায়ন ও বর্ণালী', topicCount: 11, progressPercent: 90, isRevised: true, videoLectureId: 'lec_chem_01' },
      { id: 'ch_c2', number: 2, titleBn: 'পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন', topicCount: 15, progressPercent: 65, isRevised: false, videoLectureId: 'lec_chem_02' },
      { id: 'ch_c3', number: 3, titleBn: 'রাসায়নিক পরিবর্তন ও সাম্যাবস্থা', topicCount: 14, progressPercent: 30, isRevised: false, videoLectureId: 'lec_chem_03' },
    ]
  },
  {
    id: 'sub_math_1',
    stage: 'HSC',
    titleBn: 'উচ্চতর গণিত ১ম পত্র (Higher Math 1st Paper)',
    titleEn: 'HSC Higher Mathematics Paper 1',
    chaptersCount: 10,
    completedPercent: 80,
    chapters: [
      { id: 'ch_m1', number: 1, titleBn: 'ম্যাট্রিক্স ও নির্ণায়ক', topicCount: 9, progressPercent: 100, isRevised: true, videoLectureId: 'lec_mat_01' },
      { id: 'ch_m2', number: 2, titleBn: 'সরলরেখা ও স্থানাঙ্ক জ্যামিতি', topicCount: 14, progressPercent: 85, isRevised: true, videoLectureId: 'lec_line_02' },
      { id: 'ch_m3', number: 3, titleBn: 'অন্তরীকরণ ও ক্যালকুলাস', topicCount: 16, progressPercent: 60, isRevised: false, videoLectureId: 'lec_diff_03' },
    ]
  }
];

export default function LearnPage() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedStage, setSelectedStage] = useState<'ALL' | 'SSC' | 'HSC' | 'ADMISSION'>('HSC');
  const [activeVideoLecture, setActiveVideoLecture] = useState<{ id: string; title: string } | null>(null);

  const filteredSubjects = selectedStage === 'ALL'
    ? CURATED_SUBJECTS
    : CURATED_SUBJECTS.filter((s) => s.stage === selectedStage);

  return (
    <>
      <AppHead
        title="পাঠ্যক্রম ও অধ্যায়ভিত্তিক লার্নিং হাব | অগ্রযাত্রা"
        description="এনসিটিবি কারিকুলাম অনুযায়ী শ্রেণিভিত্তিক অধ্যায়, ইন্টারেক্টিভ ভিডিও লেকচার ও স্পেসড-রিপিটিশন রিভিশন কিউ।"
        canonicalUrl="/learn"
        ogType="website"
        structuredData={createCourseSchema({
          name: "উচ্চ মাধ্যমিক পদার্থবিজ্ঞান ও গণিত",
          description: "এনসিটিবি কারিকুলাম ২০২৬ অনুযায়ী পদার্থবিজ্ঞান ও গণিতের সম্পূর্ণ পাঠ্যক্রম",
          educationalLevel: "Higher Secondary Certificate"
        })}
      />

      <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans selection:bg-[#0A2540] selection:text-white transition-colors duration-200">
        {/* Sticky Unified Global Navigation */}
        <Navbar currentStage="পাঠ্যক্রম ও অধ্যায়ভিত্তিক লার্নিং" />

        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
          
          {/* Flagship Unified PageHeader */}
          <PageHeader
            category="এনসিটিবি অনুমোদিত ২০২৬ কারিকুলাম"
            title="পাঠ্যক্রম ও অধ্যায়ভিত্তিক লার্নিং হাব"
            subtitle="পর্যায়ভিত্তিক অধ্যায়, এইচডি ভিডিও লেকচার, ইন-ভিডিও ইন্টারেক্টিভ কুইজ এবং বৈজ্ঞানিক স্পেসড-রিপিটিশন রিভিশন তালিকা।"
            breadcrumbs={[
              { label: 'নীড়পাতা', href: '/' },
              { label: 'পাঠ্যক্রম ও লার্নিং' }
            ]}
            stats={[
              { label: 'কভার্ড বিষয়', value: 'পদার্থ, রসায়ন, গণিত' },
              { label: 'মোট অধ্যায়', value: '২৮টি অধ্যায়' },
              { label: 'ভিডিও লেকচার', value: '১০০% এইচডি', highlight: true },
              { label: 'রিভিশন মেথড', value: 'স্পেসড-রিপিটিশন' }
            ]}
          />

          {/* Stage Selector Chips with Tactile 3D Depth */}
          <div className="flex flex-wrap gap-2.5 pb-2">
            {[
              { key: 'ALL', label: 'সকল স্তর' },
              { key: 'SSC', label: 'এসএসসি (Class 9-10)' },
              { key: 'HSC', label: 'এইচএসসি (Class 11-12)' },
              { key: 'ADMISSION', label: 'বিশ্ববিদ্যালয় ভর্তি' },
            ].map((tab) => (
              <button
                key={tab.key}
                type="button"
                onClick={() => setSelectedStage(tab.key as any)}
                className={`px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-semibold font-bengali transition-all min-h-[44px] cursor-pointer ${
                  selectedStage === tab.key
                    ? 'bg-[#0A2540] dark:bg-amber-400 text-white dark:text-slate-950 shadow-[0_4px_0_0_#051329] dark:shadow-[0_4px_0_0_#D97706] active:translate-y-1 active:shadow-none'
                    : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Spaced-Repetition Revision Queue (আজকের রিভিশন কিউ) */}
          <div className="p-6 sm:p-7 rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <RotateCcw className="w-5 h-5 text-amber-700 dark:text-amber-400" />
                <h2 className="text-base sm:text-lg font-bold font-bengali text-slate-900 dark:text-white">
                  স্পেসড-রিপিটিশন রিভিশন কিউ (Spaced Repetition Queue)
                </h2>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                ৩টি টপিক আজ বাকি
              </span>
            </div>

            <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-[1.75]">
              বৈজ্ঞানিক SM-2 অ্যালগরিদম অনুযায়ী বিস্মৃতি প্রতিরোধে আজকের মধ্যে এই টপিকগুলো রিভিশন দেওয়া জরুরি:
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
                <div>
                  <span className="text-[10px] font-mono text-[#0A2540] dark:text-sky-400 font-bold block mb-1">পদার্থবিজ্ঞান ১ম পত্র</span>
                  <strong className="text-xs text-slate-900 dark:text-white font-bengali block">নিউটনিয়ান বলবিদ্যা (ঘূর্ণন গতিশক্তি)</strong>
                  <span className="text-[10px] text-amber-700 dark:text-amber-400 font-bengali mt-1 block">ব্যবধান: ৩য় দিন</span>
                </div>
                <Link
                  href="/practice?topic=newtonian_rotation"
                  className="mt-3 text-xs font-semibold font-bengali text-[#0A2540] dark:text-sky-400 hover:underline flex items-center justify-between"
                >
                  <span>রিভিশন কুইজ শুরু করুন</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
                <div>
                  <span className="text-[10px] font-mono text-emerald-700 dark:text-emerald-400 font-bold block mb-1">রসায়ন ১ম পত্র</span>
                  <strong className="text-xs text-slate-900 dark:text-white font-bengali block">কোয়ান্টাম সংখ্যা ও হুন্ডের নীতি</strong>
                  <span className="text-[10px] text-amber-700 dark:text-amber-400 font-bengali mt-1 block">ব্যবধান: ৭ম দিন</span>
                </div>
                <Link
                  href="/practice?topic=quantum_hund"
                  className="mt-3 text-xs font-semibold font-bengali text-emerald-700 dark:text-emerald-400 hover:underline flex items-center justify-between"
                >
                  <span>রিভিশন কুইজ শুরু করুন</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
                <div>
                  <span className="text-[10px] font-mono text-indigo-700 dark:text-indigo-400 font-bold block mb-1">উচ্চতর গণিত ১ম পত্র</span>
                  <strong className="text-xs text-slate-900 dark:text-white font-bengali block">অন্তরীকরণ (ত্রিকোণমিতিক ডেরিভেটিভ)</strong>
                  <span className="text-[10px] text-amber-700 dark:text-amber-400 font-bengali mt-1 block">ব্যবধান: ১৪তম দিন</span>
                </div>
                <Link
                  href="/practice?topic=calculus_trig"
                  className="mt-3 text-xs font-semibold font-bengali text-indigo-700 dark:text-indigo-400 hover:underline flex items-center justify-between"
                >
                  <span>রিভিশন কুইজ শুরু করুন</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </div>

          {/* Subjects & Chapters Grid with Circular Progress Indicators */}
          {isLoading ? (
            <div className="space-y-6 animate-pulse">
              {[1, 2].map((i) => (
                <div key={i} className="p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
                  <div className="h-6 bg-slate-200 dark:bg-slate-800 rounded-lg w-1/4"></div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="h-20 bg-slate-100 dark:bg-slate-800/60 rounded-2xl"></div>
                    <div className="h-20 bg-slate-100 dark:bg-slate-800/60 rounded-2xl"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-8">
              {filteredSubjects.map((sub) => (
              <div key={sub.id} className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
                
                {/* Subject Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
                  <div className="space-y-1">
                    <span className="px-2.5 py-0.5 rounded text-[11px] font-bold font-mono bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-300 dark:border-slate-700">
                      {sub.stage}
                    </span>
                    <h2 className="text-xl sm:text-2xl font-bold font-bengali text-[#0A2540] dark:text-white">
                      {sub.titleBn}
                    </h2>
                    <p className="text-xs text-slate-500 font-display">{sub.titleEn}</p>
                  </div>

                  {/* Circular Overall Subject Progress */}
                  <div className="flex items-center gap-3">
                    <div className="relative w-14 h-14 shrink-0 flex items-center justify-center">
                      <svg className="w-14 h-14 -rotate-90" viewBox="0 0 36 36">
                        <path
                          className="text-slate-200 dark:text-slate-800"
                          strokeWidth="3.5"
                          stroke="currentColor"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path
                          className="text-[#0A2540] dark:text-emerald-400 transition-all duration-500"
                          strokeDasharray={`${sub.completedPercent}, 100`}
                          strokeWidth="3.5"
                          strokeLinecap="round"
                          stroke="currentColor"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                      </svg>
                      <span className="absolute text-xs font-mono font-bold text-slate-900 dark:text-white tabular-nums">
                        {sub.completedPercent}%
                      </span>
                    </div>

                    <div className="text-left text-xs">
                      <span className="block font-bold font-bengali text-slate-900 dark:text-white">মোট অগ্রগতি</span>
                      <span className="text-slate-500 font-bengali">{sub.chaptersCount} টি অধ্যায়</span>
                    </div>
                  </div>
                </div>

                {/* Chapters List */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {sub.chapters.map((ch) => (
                    <div
                      key={ch.id}
                      className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 transition flex items-center justify-between gap-4"
                    >
                      <div className="flex items-center gap-3.5 min-w-0">
                        {/* Circular Progress Gauge */}
                        <div className="relative w-10 h-10 shrink-0 flex items-center justify-center">
                          <svg className="w-10 h-10 -rotate-90" viewBox="0 0 36 36">
                            <path
                              className="text-slate-200 dark:text-slate-800"
                              strokeWidth="3"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                            <path
                              className={ch.progressPercent === 100 ? 'text-emerald-600 dark:text-emerald-400' : 'text-[#0A2540] dark:text-sky-400'}
                              strokeDasharray={`${ch.progressPercent}, 100`}
                              strokeWidth="3"
                              strokeLinecap="round"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                          </svg>
                          <span className="absolute text-[10px] font-mono font-bold text-slate-700 dark:text-slate-300">
                            {ch.number}
                          </span>
                        </div>

                        <div className="min-w-0">
                          <h3 className="text-xs sm:text-sm font-bold font-bengali text-slate-900 dark:text-white truncate">
                            {ch.titleBn}
                          </h3>
                          <span className="text-[11px] text-slate-500 font-bengali block">
                            {ch.topicCount} টি পাঠ • {ch.progressPercent}% সম্পন্ন
                          </span>
                        </div>
                      </div>

                      {/* Video Launcher Action with 3D Tactile Styling */}
                      <div className="flex items-center gap-2 shrink-0">
                        {ch.videoLectureId && (
                          <button
                            type="button"
                            onClick={() => setActiveVideoLecture({ id: ch.videoLectureId!, title: ch.titleBn })}
                            className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-[#0A2540] dark:text-amber-300 hover:bg-[#0A2540] hover:text-white transition border border-slate-300 dark:border-slate-700 cursor-pointer"
                            title="লেকচার ভিডিও ও কুইজ দেখুন"
                            aria-label={`লেকচার ভিডিও দেখুন: ${ch.titleBn}`}
                          >
                            <Video className="w-4 h-4" />
                          </button>
                        )}
                        <Link
                          href={`/practice?chapter=${ch.id}`}
                          className="px-3.5 py-2 rounded-xl bg-[#0A2540] hover:bg-[#081c30] text-white font-bengali text-xs shadow-[0_3px_0_0_#071D33] active:translate-y-0.5 active:shadow-none transition flex items-center gap-1.5"
                          title="অধ্যায় শুরু করুন"
                          aria-label={`অনুশীলন করুন: ${ch.titleBn}`}
                        >
                          <Play className="w-3.5 h-3.5 text-amber-300" />
                          <span>শুরু করুন</span>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>

              </div>
            ))}
            </div>
          )}

        </main>

        {/* Global Dignified Footer */}
        <Footer />
      </div>

      {/* HLS Video Lecture Player Modal */}
      {activeVideoLecture && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in"
        >
          <div className="relative w-full max-w-4xl bg-white dark:bg-slate-900 rounded-3xl border-2 border-slate-300 dark:border-slate-800 shadow-2xl overflow-hidden flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60">
              <div className="flex items-center gap-2">
                <Video className="w-5 h-5 text-[#0A2540] dark:text-amber-300" />
                <span className="font-bold font-bengali text-slate-900 dark:text-white text-sm sm:text-base">
                  {activeVideoLecture.title} (HLS Adaptive Stream)
                </span>
              </div>
              <button
                type="button"
                onClick={() => setActiveVideoLecture(null)}
                aria-label="ভিডিও বন্ধ করুন"
                className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 sm:p-6">
              <HlsLecturePlayer
                lectureId={activeVideoLecture.id}
                studentId="std_curr_user"
                titleBn={activeVideoLecture.title}
                durationSeconds={480}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
