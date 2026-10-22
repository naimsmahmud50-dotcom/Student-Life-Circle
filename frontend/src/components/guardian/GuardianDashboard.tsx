/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Guardian Trust Console & Child Digital Safety
 * TOPIC:     Apple Health Caliber Family Learning Dashboard & Privacy Boundary
 * FILE:      frontend/src/components/guardian/GuardianDashboard.tsx
 * PHASE:     Phase 108 - Guardian Trust Console & Child Digital Safety Portal
 * PURPOSE:   Provides a calm, dignified family command center:
 *            1. Non-intrusive academic telemetry (weekly study hours, subject mastery, streak).
 *            2. ASVS L2 child privacy wall guarantee (protecting private peer study chats).
 *            3. Upcoming official exam countdowns and calm, empathetic guidance.
 *            4. Strict zero-emoji compliance with tactile Lucide SVG vectors.
 * STANDARDS: ASVS L2 Minor Privacy Boundary, Zero-Intrusion Safeguards, Zero-Emoji, UI/UX Pro Max
 */

import React, { useState } from 'react';
import {
  ShieldCheck,
  Heart,
  Clock,
  Award,
  BookOpen,
  Calendar,
  CheckCircle2,
  Lock,
  Sparkles,
  Users,
  TrendingUp,
  Info,
  ChevronRight,
  EyeOff
} from 'lucide-react';

export interface SubjectMastery {
  subject: string;
  percent: number;
  status: string;
}

export interface UpcomingExam {
  title: string;
  date: string;
  days_left: number;
}

export interface ChildProfile {
  child_id: string;
  name: string;
  grade: string;
  institution: string;
  avatar_label: string;
  weekly_study_hours: number;
  study_streak_days: number;
  questions_solved_this_week: number;
  overall_mastery_percent: number;
  subject_mastery: SubjectMastery[];
  upcoming_exams: UpcomingExam[];
}

export interface GuardianDashboardProps {
  guardianName?: string;
  childrenProfiles?: ChildProfile[];
  className?: string;
}

const DEFAULT_CHILDREN: ChildProfile[] = [
  {
    child_id: 'STU_TAHSIN_01',
    name: 'তাহসিন ইসলাম',
    grade: 'HSC 2026 বিজ্ঞান বিভাগ',
    institution: 'নটর ডেম কলেজ (Notre Dame College)',
    avatar_label: 'TI',
    weekly_study_hours: 26.5,
    study_streak_days: 21,
    questions_solved_this_week: 142,
    overall_mastery_percent: 82,
    subject_mastery: [
      { subject: 'পদার্থবিজ্ঞান', percent: 84, status: 'চমৎকার' },
      { subject: 'উচ্চতর গণিত', percent: 78, status: 'সন্তোষজনক' },
      { subject: 'রসায়ন', percent: 81, status: 'ভালো' },
      { subject: 'জীববিজ্ঞান', percent: 85, status: 'চমৎকার' }
    ],
    upcoming_exams: [
      { title: 'ঢাবি ক ইউনিট মডেল টেস্ট', date: '২৫ অক্টোবর ২০২৬', days_left: 6 },
      { title: 'বুয়েট সেন্ট্রাল গ্র্যান্ড টেস্ট', date: '০২ নভেম্বর ২০২৬', days_left: 14 }
    ]
  },
  {
    child_id: 'STU_ANIKA_02',
    name: 'আনিকা ইসলাম',
    grade: 'SSC 2027',
    institution: 'ভিকারুননিসা নূন স্কুল ও কলেজ',
    avatar_label: 'AI',
    weekly_study_hours: 18.0,
    study_streak_days: 14,
    questions_solved_this_week: 95,
    overall_mastery_percent: 88,
    subject_mastery: [
      { subject: 'সাধারণ গণিত', percent: 90, status: 'অসাধারণ' },
      { subject: 'সাধারণ বিজ্ঞান', percent: 86, status: 'চমৎকার' },
      { subject: 'ইংরেজি', percent: 88, status: 'চমৎকার' }
    ],
    upcoming_exams: [
      { title: 'স্কুল মিডটার্ম মডেল মূল্যায়ন', date: '২৮ অক্টোবর ২০২৬', days_left: 9 }
    ]
  }
];

export const GuardianDashboard: React.FC<GuardianDashboardProps> = ({
  guardianName = 'রফিকুল ইসলাম',
  childrenProfiles = DEFAULT_CHILDREN,
  className = ''
}) => {
  const [selectedChildIndex, setSelectedChildIndex] = useState<number>(0);
  const activeChild = childrenProfiles[selectedChildIndex] || childrenProfiles[0];

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Top Empathetic Parental Banner */}
      <div className="rounded-3xl bg-slate-900/90 border border-emerald-500/30 p-6 sm:p-8 shadow-xl backdrop-blur-xl space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-800">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-xs font-mono font-medium">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>GUARDIAN TRUST & CHILD PRIVACY CONSOLE</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white font-sans flex items-center gap-2.5">
              <Heart className="w-6 h-6 text-emerald-400" />
              <span>স্বাগতম, {guardianName}</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 font-bengali leading-relaxed max-w-2xl">
              সন্তানের পড়াশোনায় পাশে থাকুন স্নেহে, উদ্বেগে নয়। এখানে আপনি সন্তানের সার্বিক পড়াশোনার ধারাবাহিকতা ও
              অগ্রগতি দেখতে পাবেন মানসিক চাপহীন শান্ত পরিবেশে।
            </p>
          </div>

          {/* Child Selector Tabs */}
          <div className="flex items-center gap-2 p-1.5 rounded-2xl bg-slate-950/80 border border-slate-800 shrink-0">
            {childrenProfiles.map((child, idx) => (
              <button
                key={child.child_id}
                type="button"
                onClick={() => setSelectedChildIndex(idx)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-sans transition-all ${
                  selectedChildIndex === idx
                    ? 'bg-emerald-700 text-white shadow-md font-semibold'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <span className="w-5 h-5 rounded-full bg-slate-800 text-[10px] flex items-center justify-center font-bold">
                  {child.avatar_label}
                </span>
                <span>{child.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Selected Child Academic Overview Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400 font-sans">
              <span>সাপ্তাহিক অধ্যয়ন</span>
              <Clock className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-white font-sans">
              {activeChild.weekly_study_hours} ঘণ্টা
            </div>
            <div className="text-[11px] text-emerald-400 font-bengali">
              স্বাস্থ্যকর ও সুষম সময় বণ্টন
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400 font-sans">
              <span>অনুশীলন ধারাবাহিকতা</span>
              <Award className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-bold text-white font-sans">
              {activeChild.study_streak_days} দিন
            </div>
            <div className="text-[11px] text-amber-300 font-bengali">
              টানা অধ্যবসায় বজায় রাখছে
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400 font-sans">
              <span>প্রশ্ন সমাধান সম্পন্ন</span>
              <BookOpen className="w-4 h-4 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-white font-sans">
              {activeChild.questions_solved_this_week} টি
            </div>
            <div className="text-[11px] text-blue-300 font-bengali">
              এই সপ্তাহে কার্যকর রিভিশন
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-400 font-sans">
              <span>গড় সিলেবাস পারদর্শিতা</span>
              <TrendingUp className="w-4 h-4 text-teal-400" />
            </div>
            <div className="text-2xl font-bold text-white font-sans">
              {activeChild.overall_mastery_percent}%
            </div>
            <div className="text-[11px] text-teal-300 font-bengali">
              লক্ষ্যমাত্রার সাথে সামঞ্জস্যপূর্ণ
            </div>
          </div>
        </div>
      </div>

      {/* Subject Mastery Progress & Upcoming Exams Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Subject Mastery Stack */}
        <div className="lg:col-span-2 rounded-3xl bg-slate-900/80 border border-slate-800 p-6 space-y-5 shadow-lg backdrop-blur-md">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h3 className="text-base font-bold text-white font-sans flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-emerald-400" />
                <span>বিষয়ভিত্তিক শিখন অগ্রগতি ({activeChild.name})</span>
              </h3>
              <p className="text-xs text-slate-400 font-bengali">
                প্রতিটি বিষয়ে বিগত মডেল টেস্ট ও কুইজের সামগ্রিক পারদর্শিতা
              </p>
            </div>
            <span className="text-xs text-slate-400 font-mono">NON-INTRUSIVE TELEMETRY</span>
          </div>

          <div className="space-y-4 pt-2">
            {activeChild.subject_mastery.map((sub) => (
              <div key={sub.subject} className="space-y-2 p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800/80">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-white font-sans">{sub.subject}</span>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-md bg-emerald-950 text-emerald-300 border border-emerald-500/30 text-[10px] font-medium font-bengali">
                      {sub.status}
                    </span>
                    <span className="font-mono font-bold text-slate-200">{sub.percent}%</span>
                  </div>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 rounded-full transition-all duration-700"
                    style={{ width: `${sub.percent}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Exam Calendar */}
        <div className="rounded-3xl bg-slate-900/80 border border-slate-800 p-6 space-y-5 shadow-lg backdrop-blur-md flex flex-col justify-between">
          <div className="space-y-4">
            <div className="space-y-1">
              <h3 className="text-base font-bold text-white font-sans flex items-center gap-2">
                <Calendar className="w-4 h-4 text-amber-400" />
                <span>আসন্ন পরীক্ষা ও মডেল টেস্ট</span>
              </h3>
              <p className="text-xs text-slate-400 font-bengali">
                সন্তানের পড়াশোনার প্রস্তুতির জন্য গুরুত্বপূর্ণ তারিখসমূহ
              </p>
            </div>

            <div className="space-y-3 pt-2">
              {activeChild.upcoming_exams.map((exam) => (
                <div
                  key={exam.title}
                  className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-white font-sans">{exam.title}</span>
                    <span className="px-2 py-0.5 rounded-md bg-amber-950 text-amber-300 border border-amber-500/30 text-[10px] font-mono">
                      {exam.days_left} দিন বাকি
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 font-bengali">
                    তারিখ: {exam.date}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Child Digital Privacy Wall Assurance Badge */}
          <div className="p-4 rounded-2xl bg-slate-950/90 border border-emerald-500/30 space-y-2 mt-4">
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 font-sans">
              <EyeOff className="w-4 h-4" />
              <span>ডিজিটাল শিশু গোপনীয়তা প্রাচীর (ASVS L2)</span>
            </div>
            <p className="text-[11px] text-slate-400 font-bengali leading-relaxed">
              সন্তানের ব্যক্তিগত সহপাঠী চ্যাট, স্টাডি পড বার্তা বা অপ্রকাশিত নোট এই ড্যাশবোর্ডে দৃশ্যমান নয়।
              আমরা শিক্ষার্থীর গোপনীয়তা ও মানসিক স্বাতন্ত্র্যকে শতভাগ সম্মান করি।
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
