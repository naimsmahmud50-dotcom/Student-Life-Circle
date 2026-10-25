/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/LiveExamRoutineMatrix.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Multi-track daily exam routine matrix inspired by Live MCQ's core strengths,
 *            organizing live, upcoming, and archived nationwide exams with textbook citations.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Calendar,
  Clock,
  BookOpen,
  Users,
  Award,
  CheckCircle2,
  ArrowRight,
  Filter,
  FileText,
  ChevronRight,
  AlertCircle
} from 'lucide-react';

export type ExamTrackId = 'hsc_science' | 'ssc_board' | 'admission' | 'olympiad' | 'bcs_job';
export type TemporalTab = 'today' | 'tomorrow' | 'archive';

export interface ExamRoutineItem {
  id: string;
  trackId: ExamTrackId;
  temporalTab: TemporalTab;
  titleBn: string;
  titleEn: string;
  subjectBn: string;
  nctbCitationBn: string;
  examDateBn: string;
  examTimeBn: string;
  durationMinutes: number;
  totalQuestions: number;
  negativeMarkRatio: number;
  enrolledStudentsCount: number;
  status: 'live_now' | 'scheduled' | 'completed';
  passMarkPercent: number;
}

const ROUTINE_DATA: ExamRoutineItem[] = [
  // TODAY'S EXAMS
  {
    id: 'exam_today_hsc_phys',
    trackId: 'hsc_science',
    temporalTab: 'today',
    titleBn: 'পদার্থবিজ্ঞান ১ম পত্র: নিউটোনীয় বলবিদ্যা ও কাজ-শক্তি-ক্ষমতা',
    titleEn: 'HSC Physics 1st Paper: Newtonian Mechanics & Work-Energy',
    subjectBn: 'পদার্থবিজ্ঞান ১ম পত্র',
    nctbCitationBn: 'এনসিটিবি একাদশ-দ্বাদশ শ্রেণি • অধ্যায় ৪ ও ৫',
    examDateBn: 'আজকের পরীক্ষা',
    examTimeBn: 'রাত ৮:০০ টা – রাত ৮:২৫ টা',
    durationMinutes: 25,
    totalQuestions: 25,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 4850,
    status: 'live_now',
    passMarkPercent: 40
  },
  {
    id: 'exam_today_admission_math',
    trackId: 'admission',
    temporalTab: 'today',
    titleBn: 'বিশ্ববিদ্যালয় ভর্তি স্পেশাল: উচ্চতর গণিত (ক্যালকুলাস ও ম্যাট্রিক্স)',
    titleEn: 'Varsity Admission Special: Higher Math (Calculus & Matrix)',
    subjectBn: 'উচ্চতর গণিত',
    nctbCitationBn: 'বুয়েট, ঢাবি ক ও গুচ্ছ স্ট্যান্ডার্ড প্রশ্নব্যাংক',
    examDateBn: 'আজকের পরীক্ষা',
    examTimeBn: 'রাত ৯:০০ টা – রাত ৯:৪০ টা',
    durationMinutes: 40,
    totalQuestions: 40,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 6120,
    status: 'scheduled',
    passMarkPercent: 45
  },
  {
    id: 'exam_today_ssc_chem',
    trackId: 'ssc_board',
    temporalTab: 'today',
    titleBn: 'এসএসসি বিজ্ঞান ফাইনাল মডেল: রসায়ন (পদার্থের গঠন ও পর্যায় সারণি)',
    titleEn: 'SSC Chemistry Final: Structure of Matter & Periodic Table',
    subjectBn: 'রসায়ন',
    nctbCitationBn: 'এনসিটিবি ৯ম-১০ম শ্রেণি • অধ্যায় ৩ ও ৪',
    examDateBn: 'আজকের পরীক্ষা',
    examTimeBn: 'সন্ধ্যা ৭:০০ টা – সন্ধ্যা ৭:৩০ টা',
    durationMinutes: 30,
    totalQuestions: 30,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 3490,
    status: 'scheduled',
    passMarkPercent: 40
  },
  {
    id: 'exam_today_olympiad_stem',
    trackId: 'olympiad',
    temporalTab: 'today',
    titleBn: 'জাতীয় স্টেম অলিম্পিয়াড ২০২৬ - কোয়ালিফাইং রাউন্ড ০১',
    titleEn: 'National STEM Olympiad 2026 - Qualifying Round 01',
    subjectBn: 'সমন্বিত বিজ্ঞান ও গণিত',
    nctbCitationBn: 'পদার্থবিজ্ঞান, রসায়ন ও উচ্চতর গণিত সমন্বিত সিলেবাস',
    examDateBn: 'আজকের পরীক্ষা',
    examTimeBn: 'রাত ৮:০০ টা – রাত ৮:২৫ টা',
    durationMinutes: 25,
    totalQuestions: 25,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 5240,
    status: 'live_now',
    passMarkPercent: 50
  },
  {
    id: 'exam_today_bcs_math',
    trackId: 'bcs_job',
    temporalTab: 'today',
    titleBn: 'বিসিএস প্রিলিমিনারি: গাণিতিক যুক্তি ও মানসিক দক্ষতা',
    titleEn: 'BCS Preliminary: Mathematical Reasoning & Mental Ability',
    subjectBn: 'গাণিতিক যুক্তি',
    nctbCitationBn: 'বিসিএস প্রিলি বিগত ১০ বছরের প্রশ্ন ও বোর্ড সমাধান',
    examDateBn: 'আজকের পরীক্ষা',
    examTimeBn: 'রাত ৯:৩০ টা – রাত ১০:০০ টা',
    durationMinutes: 30,
    totalQuestions: 30,
    negativeMarkRatio: 0.50,
    enrolledStudentsCount: 8920,
    status: 'scheduled',
    passMarkPercent: 50
  },

  // TOMORROW'S EXAMS
  {
    id: 'exam_tmrw_hsc_chem',
    trackId: 'hsc_science',
    temporalTab: 'tomorrow',
    titleBn: 'রসায়ন ১ম পত্র: গুণগত রসায়ন ও রাসায়নিক পরিবর্তন',
    titleEn: 'HSC Chemistry 1st Paper: Qualitative Chemistry & Chemical Changes',
    subjectBn: 'রসায়ন ১ম পত্র',
    nctbCitationBn: 'এনসিটিবি একাদশ-দ্বাদশ শ্রেণি • অধ্যায় ২ ও ৪',
    examDateBn: 'আগামীকাল',
    examTimeBn: 'রাত ৮:০০ টা – রাত ৮:৩০ টা',
    durationMinutes: 30,
    totalQuestions: 30,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 3910,
    status: 'scheduled',
    passMarkPercent: 40
  },
  {
    id: 'exam_tmrw_admission_phys',
    trackId: 'admission',
    temporalTab: 'tomorrow',
    titleBn: 'মেডিকেল ও ডেন্টাল অ্যাডমিশন ফিজিক্স স্পেশাল',
    titleEn: 'Medical & Dental Admission Physics Special',
    subjectBn: 'পদার্থবিজ্ঞান',
    nctbCitationBn: 'মেডিকেল ভর্তি পরীক্ষা বিগত ২০ বছরের ট্রেন্ড বিশ্লেষণ',
    examDateBn: 'আগামীকাল',
    examTimeBn: 'রাত ৯:০০ টা – রাত ৯:৩০ টা',
    durationMinutes: 30,
    totalQuestions: 50,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 7150,
    status: 'scheduled',
    passMarkPercent: 40
  },
  {
    id: 'exam_tmrw_ssc_phys',
    trackId: 'ssc_board',
    temporalTab: 'tomorrow',
    titleBn: 'এসএসসি পদার্থবিজ্ঞান: আলো ও তড়িৎ অধ্যায়ভিত্তিক মডেল টেস্ট',
    titleEn: 'SSC Physics: Optics & Electricity Chapter Model Test',
    subjectBn: 'পদার্থবিজ্ঞান',
    nctbCitationBn: 'এনসিটিবি ৯ম-১০ম শ্রেণি • অধ্যায় ৮ ও ১১',
    examDateBn: 'আগামীকাল',
    examTimeBn: 'সন্ধ্যা ৭:৩০ টা – রাত ৮:০০ টা',
    durationMinutes: 30,
    totalQuestions: 25,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 2840,
    status: 'scheduled',
    passMarkPercent: 40
  },

  // ARCHIVED EXAMS
  {
    id: 'exam_arch_hsc_math',
    trackId: 'hsc_science',
    temporalTab: 'archive',
    titleBn: 'উচ্চতর গণিত ১ম পত্র: অন্তরীকরণ ও যৌগিক কোণের ত্রিকোণমিতি',
    titleEn: 'HSC Higher Math 1st Paper: Differentiation & Trigonometry',
    subjectBn: 'উচ্চতর গণিত ১ম পত্র',
    nctbCitationBn: 'এনসিটিবি পাঠ্যপুস্তক • অধ্যায় ৭ ও ৯',
    examDateBn: 'গতকালের পরীক্ষা',
    examTimeBn: 'সম্পন্ন হয়েছে',
    durationMinutes: 30,
    totalQuestions: 30,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 5120,
    status: 'completed',
    passMarkPercent: 40
  },
  {
    id: 'exam_arch_admission_gk',
    trackId: 'admission',
    temporalTab: 'archive',
    titleBn: 'ঢাকা বিশ্ববিদ্যালয় ক ইউনিট: রসায়ন ও পদার্থবিজ্ঞান সমন্বিত মডেল',
    titleEn: 'DU Ka Unit: Chemistry & Physics Integrated Model',
    subjectBn: 'পদার্থ ও রসায়ন',
    nctbCitationBn: 'ঢাকা বিশ্ববিদ্যালয় বিগত ৫ বছরের ক-ইউনিট প্রশ্ন',
    examDateBn: '২৩ অক্টোবর ২০২৬',
    examTimeBn: 'সম্পন্ন হয়েছে',
    durationMinutes: 45,
    totalQuestions: 50,
    negativeMarkRatio: 0.25,
    enrolledStudentsCount: 8430,
    status: 'completed',
    passMarkPercent: 45
  }
];

const TRACKS: { id: ExamTrackId; labelBn: string; count: number }[] = [
  { id: 'hsc_science', labelBn: 'এইচএসসি বিজ্ঞান (HSC Science)', count: 3 },
  { id: 'ssc_board', labelBn: 'এসএসসি বোর্ড (SSC 9-10)', count: 2 },
  { id: 'admission', labelBn: 'বিশ্ববিদ্যালয় ভর্তি (Admission)', count: 3 },
  { id: 'olympiad', labelBn: 'জাতীয় অলিম্পিয়াড (Olympiad)', count: 1 },
  { id: 'bcs_job', labelBn: 'বিসিএস ও চাকরি (Job Solution)', count: 1 },
];

export const LiveExamRoutineMatrix: React.FC = () => {
  const [selectedTrack, setSelectedTrack] = useState<ExamTrackId>('hsc_science');
  const [activeTab, setActiveTab] = useState<TemporalTab>('today');

  const filteredExams = ROUTINE_DATA.filter((item) => {
    const matchesTrack = item.trackId === selectedTrack;
    const matchesTab = item.temporalTab === activeTab;
    return matchesTrack && matchesTab;
  });

  return (
    <section 
      aria-label="দৈনিক ও সাপ্তাহিক লাইভ পরীক্ষার রুটিন ম্যাট্রিক্স"
      className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-sm space-y-6"
    >
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold font-mono text-[#0A2540] dark:text-amber-300 uppercase tracking-wider">
            <Calendar className="w-4 h-4" />
            <span>দেশব্যাপী লাইভ পরীক্ষার সময়সূচি ও রুটিন</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-black font-bengali text-slate-900 dark:text-white mt-1">
            দৈনিক পরীক্ষার রুটিন ও সিলেবাস ম্যাট্রিক্স
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali mt-1">
            এনসিটিবি পাঠ্যবই এবং জাতীয় বোর্ড পরীক্ষার কাঠামো অনুসারে নির্ধারিত দৈনিক লাইভ ও আর্কাইভ টেস্ট।
          </p>
        </div>

        {/* Temporal Filters: Today, Tomorrow, Archive */}
        <div className="inline-flex p-1 rounded-2xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 self-start md:self-auto">
          <button
            type="button"
            onClick={() => setActiveTab('today')}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              activeTab === 'today'
                ? 'bg-[#0A2540] text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            আজকের পরীক্ষা
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('tomorrow')}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              activeTab === 'tomorrow'
                ? 'bg-[#0A2540] text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            আগামীকালের রুটিন
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('archive')}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition-all ${
              activeTab === 'archive'
                ? 'bg-[#0A2540] text-white shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            আর্কাইভ ও মেধা তালিকা
          </button>
        </div>
      </div>

      {/* Academic Track Selector Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
        {TRACKS.map((track) => (
          <button
            key={track.id}
            type="button"
            onClick={() => setSelectedTrack(track.id)}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold font-bengali whitespace-nowrap transition-all border ${
              selectedTrack === track.id
                ? 'bg-[#0A2540] text-white border-[#0A2540] shadow-sm'
                : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/60'
            }`}
          >
            <span>{track.labelBn}</span>
          </button>
        ))}
      </div>

      {/* Routine Cards Grid */}
      {filteredExams.length === 0 ? (
        <div className="p-8 text-center rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800">
          <BookOpen className="w-8 h-8 text-slate-400 mx-auto mb-2" />
          <p className="text-sm font-bold font-bengali text-slate-700 dark:text-slate-300">
            এই ক্যাটাগরিতে এই সময়ের জন্য কোনো নির্ধারিত পরীক্ষা নেই।
          </p>
          <p className="text-xs text-slate-500 font-bengali mt-1">
            অনুগ্রহ করে অন্য ক্যাটাগরি অথবা আগামীকালের রুটিন চেক করুন।
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {filteredExams.map((item) => (
            <div
              key={item.id}
              className="p-5 sm:p-6 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 hover:border-slate-400 dark:hover:border-slate-700 transition flex flex-col justify-between gap-4"
            >
              <div className="space-y-3">
                {/* Status Badges */}
                <div className="flex flex-wrap items-center gap-2">
                  {item.status === 'live_now' && (
                    <span className="px-2.5 py-0.5 rounded-full bg-emerald-600 text-white text-[11px] font-bold font-bengali flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
                      <span>লাইভ চলছে</span>
                    </span>
                  )}
                  {item.status === 'scheduled' && (
                    <span className="px-2.5 py-0.5 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-[11px] font-bold font-bengali flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      <span>নির্ধারিত</span>
                    </span>
                  )}
                  {item.status === 'completed' && (
                    <span className="px-2.5 py-0.5 rounded-full bg-amber-800 text-amber-100 text-[11px] font-bold font-bengali flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>আর্কাইভ</span>
                    </span>
                  )}
                  
                  <span className="px-2.5 py-0.5 rounded-full bg-[#991B1B]/15 text-[#991B1B] dark:text-rose-300 border border-[#991B1B]/30 text-[11px] font-mono font-bold">
                    নেগেটিভ: -{item.negativeMarkRatio.toFixed(2)}
                  </span>

                  <span className="px-2.5 py-0.5 rounded-full bg-slate-200/60 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 text-[11px] font-mono">
                    {item.totalQuestions} টি প্রশ্ন • {item.durationMinutes} মিনিট
                  </span>
                </div>

                {/* Exam Title */}
                <h3 className="text-base sm:text-lg font-bold font-bengali text-slate-900 dark:text-white leading-snug">
                  {item.titleBn}
                </h3>

                {/* NCTB Citation */}
                <div className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 flex items-start gap-2 text-xs font-bengali text-slate-600 dark:text-slate-300">
                  <BookOpen className="w-4 h-4 text-[#0A2540] dark:text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-slate-800 dark:text-slate-200">সিলেবাস রেফারেন্স: </span>
                    <span>{item.nctbCitationBn}</span>
                  </div>
                </div>

                {/* Meta details */}
                <div className="flex flex-wrap items-center gap-4 text-xs font-bengali text-slate-500 pt-1">
                  <div className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{item.examTimeBn}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Users className="w-3.5 h-3.5" />
                    <span>{item.enrolledStudentsCount.toLocaleString()} জন পরীক্ষার্থী</span>
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <div className="pt-3 border-t border-slate-200/80 dark:border-slate-800 flex items-center justify-between">
                <span className="text-[11px] font-mono text-slate-500">
                  পাস মার্ক: {item.passMarkPercent}%
                </span>

                {item.status === 'live_now' ? (
                  <Link
                    href="/practice?challenge=active"
                    className="px-5 py-2.5 rounded-xl bg-[#0A2540] text-white hover:bg-slate-800 font-bold font-bengali text-xs flex items-center gap-1.5 transition min-h-[44px]"
                  >
                    <span>টেস্টে যোগ দিন</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                ) : item.status === 'scheduled' ? (
                  <button
                    type="button"
                    onClick={() => alert('এই পরীক্ষার সিলেবাস অনুসরণে অনুশীলন শুরু করার জন্য অনুশীলন পেজে যান।')}
                    className="px-5 py-2.5 rounded-xl bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-300 dark:border-slate-600 hover:bg-slate-100 font-bold font-bengali text-xs flex items-center gap-1.5 transition min-h-[44px]"
                  >
                    <span>প্রস্তুতি নিন</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <Link
                    href="/practice?challenge=archive"
                    className="px-5 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 hover:bg-slate-200 font-bold font-bengali text-xs flex items-center gap-1.5 transition min-h-[44px]"
                  >
                    <span>প্রশ্ন ও সমাধান দেখুন</span>
                    <FileText className="w-3.5 h-3.5" />
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};
