/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Institutional Teacher Cockpit & Multi-Tenant Portal Dashboard
 * TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
 * FILE:      frontend/src/components/institution/InstitutionalTeacherCockpit.tsx
 * PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
 * PURPOSE:   Provides multi-tenant school/college administration for teachers,
 *            4-tab workflow (Active Exams, Grade Book, Question Paper Creator,
 *            Student Roster), tactile 3D Oxford Navy action buttons, and
 *            section performance analytics.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState } from 'react';
import {
  School,
  Users,
  GraduationCap,
  FileCheck,
  BarChart3,
  Calendar,
  Clock,
  CheckCircle2,
  AlertCircle,
  PlusCircle,
  Send,
  BookOpen,
  ShieldCheck,
  ChevronRight,
  UserCheck,
  Layers,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { SectionAnalyticsCard, SectionAnalyticsData } from './SectionAnalyticsCard';

export interface InstitutionProfile {
  institution_id: string;
  legal_name: string;
  name_bn: string;
  subdomain: string;
  custom_domain: string;
  eiin_number: string;
  division: string;
  theme_accent: string;
}

export interface SectionSummary {
  section_id: string;
  section_name: string;
  section_name_bn: string;
  class_grade: number;
  academic_year: string;
  student_count: number;
}

export interface ExamSummary {
  exam_id: string;
  title_bn: string;
  title_en: string;
  subject: string;
  paper: string;
  duration_minutes: number;
  total_marks: number;
  due_timestamp: number;
  status: 'DRAFT' | 'PUBLISHED' | 'COMPLETED';
  question_ids: string[];
}

export interface StudentGradeRecord {
  student_id: string;
  roll_number: string;
  student_name: string;
  marks_obtained: number;
  attendance_percent: number;
  submitted_at: number;
  feedback_bn: string;
}

export interface GradebookData {
  exam_id: string;
  section_id: string;
  status: 'PENDING_APPROVAL' | 'GRADES_APPROVED';
  approved_by?: string;
  records: StudentGradeRecord[];
}

export interface InstitutionalTeacherCockpitProps {
  institution?: InstitutionProfile;
  sections?: SectionSummary[];
  activeExams?: ExamSummary[];
  gradebook?: GradebookData;
  analytics?: SectionAnalyticsData;
  teacherName?: string;
  teacherDesignation?: string;
  onPublishExam?: (examId: string) => void;
  onApproveGrades?: (examId: string, sectionId: string) => void;
  onCreateExam?: (formData: any) => void;
}

export const InstitutionalTeacherCockpit: React.FC<InstitutionalTeacherCockpitProps> = ({
  institution = {
    institution_id: 'inst-ndc-dhaka',
    legal_name: 'Notre Dame College, Dhaka',
    name_bn: 'নটর ডেম কলেজ, ঢাকা',
    subdomain: 'ndc',
    custom_domain: 'ndc.ogrojatra.edu.bd',
    eiin_number: '108274',
    division: 'Dhaka',
    theme_accent: '#0A2540'
  },
  sections = [
    {
      section_id: 'sec-ndc-hsc26-a',
      section_name: 'Section A (Science)',
      section_name_bn: 'শাখা ক (বিজ্ঞান)',
      class_grade: 11,
      academic_year: '2025-2026',
      student_count: 65
    },
    {
      section_id: 'sec-ndc-hsc26-b',
      section_name: 'Section B (Science)',
      section_name_bn: 'শাখা খ (বিজ্ঞান)',
      class_grade: 11,
      academic_year: '2025-2026',
      student_count: 62
    }
  ],
  activeExams = [
    {
      exam_id: 'exam-ndc-phys-midterm-01',
      title_bn: 'পদার্থবিজ্ঞান ১ম পত্র সেকশন মডেল টেস্ট — ১ম পর্ব',
      title_en: 'Physics 1st Paper Mid-Term Section Assessment',
      subject: 'Physics',
      paper: '1st',
      duration_minutes: 60,
      total_marks: 50,
      due_timestamp: Math.floor(Date.now() / 1000) + 86400 * 3,
      status: 'PUBLISHED',
      question_ids: ['nctb_hsc_phys1_dhaka_2024_cq_01', 'nctb_hsc_phys_dhk_2022_mcq_01']
    }
  ],
  gradebook = {
    exam_id: 'exam-ndc-phys-midterm-01',
    section_id: 'sec-ndc-hsc26-a',
    status: 'PENDING_APPROVAL',
    records: [
      {
        student_id: 'stu-ndc-101',
        roll_number: '101',
        student_name: 'Tanvir Ahmed',
        marks_obtained: 46.5,
        attendance_percent: 98.0,
        submitted_at: Math.floor(Date.now() / 1000) - 1800,
        feedback_bn: 'বলবিদ্যা ও ব্যাংকিং কোণের প্রয়োগ অত্যন্ত চমৎকার হয়েছে।'
      },
      {
        student_id: 'stu-ndc-102',
        roll_number: '102',
        student_name: 'Sajid Karim',
        marks_obtained: 42.0,
        attendance_percent: 95.0,
        submitted_at: Math.floor(Date.now() / 1000) - 2200,
        feedback_bn: 'ভরবেগের সংরক্ষণশীলতার ব্যাখ্যায় আরও স্পষ্টতা প্রয়োজন।'
      },
      {
        student_id: 'stu-ndc-103',
        roll_number: '103',
        student_name: 'Abrar Fahad',
        marks_obtained: 48.0,
        attendance_percent: 100.0,
        submitted_at: Math.floor(Date.now() / 1000) - 1200,
        feedback_bn: 'নিখুঁত গাণিতিক বিশ্লেষণ ও চিত্র উপস্থাপন।'
      },
      {
        student_id: 'stu-ndc-104',
        roll_number: '104',
        student_name: 'Nafis Imtiaz',
        marks_obtained: 38.5,
        attendance_percent: 91.0,
        submitted_at: Math.floor(Date.now() / 1000) - 2500,
        feedback_bn: 'ঘর্ষণ বল ও মন্দন গণনায় অসতর্ক ভুল সংশোধন করো।'
      },
      {
        student_id: 'stu-ndc-105',
        roll_number: '105',
        student_name: 'Mahir Faysal',
        marks_obtained: 44.0,
        attendance_percent: 96.0,
        submitted_at: Math.floor(Date.now() / 1000) - 1500,
        feedback_bn: 'উচ্চতর দক্ষতা অংশে ভালো সিদ্ধান্ত দিয়েছ।'
      }
    ]
  },
  analytics = {
    total_examinees: 5,
    average_score: 43.8,
    median_score: 44.0,
    standard_deviation: 3.36,
    highest_score: 48.0,
    lowest_score: 38.5,
    distribution_brackets: {
      tier_below_40: 0,
      tier_40_59: 0,
      tier_60_79: 1,
      tier_80_100: 4
    },
    weak_topics: [
      {
        topic_name_bn: 'ঘর্ষণ বল ও জড়তার ভ্রামক গণনা',
        accuracy_percent: 48.5,
        remedial_tip_bn: 'সমান্তরাল অক্ষ উপপাদ্য ও লম্ব অক্ষ উপপাদ্যের পার্থক্য পুনরাবৃত্তি করুন।'
      },
      {
        topic_name_bn: 'ব্যাংকিং কোণে নিরাপদ বেগ বিশ্লেষণ',
        accuracy_percent: 56.0,
        remedial_tip_bn: 'tan(theta) = v^2/rg সূত্রের প্রয়োগ আরও অনুশীলন আবশ্যক।'
      }
    ]
  },
  teacherName = 'ড. সুশান্ত রায়',
  teacherDesignation = 'সিনিয়র লেকচারার (পদার্থবিজ্ঞান)',
  onPublishExam,
  onApproveGrades,
  onCreateExam
}) => {
  const [activeTab, setActiveTab] = useState<'exams' | 'gradebook' | 'creator' | 'roster'>('exams');
  const [selectedSectionId, setSelectedSectionId] = useState<string>(sections[0]?.section_id || '');
  const [currentGradeStatus, setCurrentGradeStatus] = useState<string>(gradebook.status);
  const [examsList, setExamsList] = useState<ExamSummary[]>(activeExams);

  // Form state for Question Paper Creator
  const [examTitleBn, setExamTitleBn] = useState('');
  const [examSubject, setExamSubject] = useState('Physics');
  const [examPaper, setExamPaper] = useState('1st');
  const [examDuration, setExamDuration] = useState('60');
  const [examTotalMarks, setExamTotalMarks] = useState('50');

  const selectedSection = sections.find((s) => s.section_id === selectedSectionId) || sections[0];

  const handlePublishClick = (examId: string) => {
    setExamsList((prev) =>
      prev.map((e) => (e.exam_id === examId ? { ...e, status: 'PUBLISHED' as const } : e))
    );
    if (onPublishExam) {
      onPublishExam(examId);
    }
  };

  const handleApproveGradesClick = () => {
    setCurrentGradeStatus('GRADES_APPROVED');
    if (onApproveGrades) {
      onApproveGrades(gradebook.exam_id, selectedSectionId);
    }
  };

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!examTitleBn.trim()) return;

    const newExam: ExamSummary = {
      exam_id: `exam-${institution.subdomain}-${Date.now().toString().slice(-4)}`,
      title_bn: examTitleBn,
      title_en: `${examSubject} ${examPaper} Paper Scheduled Test`,
      subject: examSubject,
      paper: examPaper,
      duration_minutes: parseInt(examDuration) || 60,
      total_marks: parseInt(examTotalMarks) || 50,
      due_timestamp: Math.floor(Date.now() / 1000) + 86400 * 2,
      status: 'PUBLISHED',
      question_ids: ['nctb_cq_custom_01', 'nctb_mcq_custom_02']
    };

    setExamsList([newExam, ...examsList]);
    setExamTitleBn('');
    setActiveTab('exams');

    if (onCreateExam) {
      onCreateExam(newExam);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8 space-y-8 font-sans">
      
      {/* Institutional Multi-Tenant Top Bar */}
      <div className="bg-[#0A2540] text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-6 relative z-10">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center">
              <School className="w-8 h-8 text-amber-300" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-400/20 text-amber-300 border border-amber-400/30">
                  EIIN: {institution.eiin_number}
                </span>
                <span className="text-xs text-slate-300 font-mono">
                  {institution.custom_domain}
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold font-bengali tracking-tight mt-1">
                {institution.name_bn}
              </h1>
              <p className="text-xs sm:text-sm text-slate-300 font-display">
                {institution.legal_name} — প্রাতিষ্ঠানিক শিক্ষক ককপিট
              </p>
            </div>
          </div>

          {/* Teacher Profile & Section Selector */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-white/10 p-4 rounded-2xl border border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-300 text-[#0A2540] flex items-center justify-center font-bold">
                <GraduationCap className="w-6 h-6" />
              </div>
              <div>
                <div className="text-sm font-bold font-bengali text-white">
                  {teacherName}
                </div>
                <div className="text-xs text-slate-300 font-bengali">
                  {teacherDesignation}
                </div>
              </div>
            </div>

            <div className="w-full sm:w-auto">
              <select
                aria-label="অধ্যয়নরত শাখা নির্বাচন করুন"
                value={selectedSectionId}
                onChange={(e) => setSelectedSectionId(e.target.value)}
                className="w-full bg-[#071D33] text-white text-xs font-bengali px-3 py-2 rounded-xl border border-white/20 focus:outline-none focus:ring-2 focus:ring-amber-300"
              >
                {sections.map((sec) => (
                  <option key={sec.section_id} value={sec.section_id}>
                    {sec.section_name_bn} ({sec.student_count} শিক্ষার্থী)
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* 4-Tab Navigation */}
      <div className="flex flex-wrap gap-2 border-b-2 border-slate-200 dark:border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('exams')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl font-bengali text-sm font-bold transition-all ${
            activeTab === 'exams'
              ? 'bg-[#0A2540] text-white shadow-sm'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <FileCheck className="w-4 h-4" />
          চলমান ও প্রকাশিত পরীক্ষা
          <span className="px-2 py-0.5 rounded-full text-xs font-mono bg-white/20">
            {examsList.length}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('gradebook')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl font-bengali text-sm font-bold transition-all ${
            activeTab === 'gradebook'
              ? 'bg-[#0A2540] text-white shadow-sm'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <BarChart3 className="w-4 h-4" />
          শাখা গ্রেডবুক ও ডায়াগনস্টিক
          {currentGradeStatus === 'PENDING_APPROVAL' && (
            <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
          )}
        </button>

        <button
          onClick={() => setActiveTab('creator')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl font-bengali text-sm font-bold transition-all ${
            activeTab === 'creator'
              ? 'bg-[#0A2540] text-white shadow-sm'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <PlusCircle className="w-4 h-4" />
          প্রশ্নপত্র সংকলন ও শিডিউলার
        </button>

        <button
          onClick={() => setActiveTab('roster')}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-2xl font-bengali text-sm font-bold transition-all ${
            activeTab === 'roster'
              ? 'bg-[#0A2540] text-white shadow-sm'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <Users className="w-4 h-4" />
          শিক্ষার্থী তালিকা ও হাজিরা
        </button>
      </div>

      {/* TAB 1: ACTIVE EXAMS */}
      {activeTab === 'exams' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold font-bengali text-slate-900 dark:text-white">
              নির্ধারিত মডেল টেস্ট তালিকা
            </h2>
            <button
              onClick={() => setActiveTab('creator')}
              className="flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-xs font-bold font-bengali rounded-xl hover:bg-slate-200 transition-colors"
            >
              <PlusCircle className="w-4 h-4 text-[#0A2540]" />
              নতুন মডেল টেস্ট যোগ করুন
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {examsList.map((exam) => (
              <div
                key={exam.exam_id}
                className="bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold font-mono px-2.5 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                      {exam.subject} ({exam.paper} পত্র)
                    </span>
                    <span
                      className={`text-xs font-bold font-bengali px-3 py-1 rounded-full ${
                        exam.status === 'PUBLISHED'
                          ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                          : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                      }`}
                    >
                      {exam.status === 'PUBLISHED' ? 'প্রকাশিত' : 'খসড়া (Draft)'}
                    </span>
                  </div>

                  <h3 className="text-base sm:text-lg font-bold font-bengali text-slate-900 dark:text-white leading-snug">
                    {exam.title_bn}
                  </h3>
                  <p className="text-xs text-slate-500 font-display mt-0.5">
                    {exam.title_en}
                  </p>

                  <div className="grid grid-cols-3 gap-2 my-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-center">
                    <div className="p-2 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                      <div className="text-[11px] text-slate-500 font-bengali">সময়সীমা</div>
                      <div className="text-sm font-bold font-mono text-slate-800 dark:text-slate-200">
                        {exam.duration_minutes} মিনিট
                      </div>
                    </div>
                    <div className="p-2 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                      <div className="text-[11px] text-slate-500 font-bengali">পূর্ণমান</div>
                      <div className="text-sm font-bold font-mono text-slate-800 dark:text-slate-200">
                        {exam.total_marks} নম্বর
                      </div>
                    </div>
                    <div className="p-2 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                      <div className="text-[11px] text-slate-500 font-bengali">প্রশ্ন সংখ্যা</div>
                      <div className="text-sm font-bold font-mono text-slate-800 dark:text-slate-200">
                        {exam.question_ids.length} টি
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 font-mono">
                    <Clock className="w-3.5 h-3.5" />
                    জমা দেওয়ার শেষ সময়: ৩ দিন বাকি
                  </div>

                  {exam.status !== 'PUBLISHED' ? (
                    <button
                      onClick={() => handlePublishClick(exam.exam_id)}
                      className="px-5 py-2.5 bg-[#0A2540] hover:bg-[#081c30] text-white font-bengali text-xs shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none font-semibold rounded-2xl transition-all"
                    >
                      পরীক্ষার প্রশ্ন প্রকাশ করুন
                    </button>
                  ) : (
                    <span className="flex items-center gap-1 text-xs font-bold font-bengali text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 className="w-4 h-4" />
                      শিক্ষার্থীদের জন্য উন্মুক্ত
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: SECTION GRADE BOOK & ANALYTICS */}
      {activeTab === 'gradebook' && (
        <div className="space-y-8">
          {/* Section Analytics Card Integration */}
          <SectionAnalyticsCard
            analytics={analytics}
            sectionName={selectedSection.section_name_bn}
            examTitle={activeExams[0]?.title_bn}
          />

          {/* Student Marks Roster & Approval Workflow */}
          <div className="bg-white dark:bg-slate-900 border-2 border-slate-300 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-200 dark:border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider font-display">
                    সেকশন খাতা মূল্যায়ন রেজিস্টার
                  </span>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-xs font-bold font-bengali ${
                      currentGradeStatus === 'GRADES_APPROVED'
                        ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                        : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                    }`}
                  >
                    {currentGradeStatus === 'GRADES_APPROVED'
                      ? 'শিক্ষক দ্বারা নম্বর অনুমোদিত'
                      : 'অনুমোদনের অপেক্ষায়'}
                  </span>
                </div>
                <h3 className="text-xl font-bold font-bengali text-slate-900 dark:text-white mt-1">
                  শিক্ষার্থী মূল্যায়ন ও প্রাতিষ্ঠানিক নম্বরপত্র
                </h3>
              </div>

              {currentGradeStatus !== 'GRADES_APPROVED' ? (
                <button
                  onClick={handleApproveGradesClick}
                  className="px-6 py-3 bg-[#0A2540] hover:bg-[#081c30] text-white font-bengali text-sm shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none font-semibold rounded-2xl flex items-center gap-2 transition-all cursor-pointer"
                >
                  <FileCheck className="w-4 h-4 text-amber-300" />
                  নম্বর অনুমোদন করুন
                </button>
              ) : (
                <div className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-bold font-bengali">
                  <CheckCircle2 className="w-4 h-4" />
                  নম্বরপত্র সফলভাবে প্রাতিষ্ঠানিক কেন্দ্রীয় আর্কাইভে সংরক্ষিত
                </div>
              )}
            </div>

            {/* Roster Table */}
            <div className="overflow-x-auto mt-6">
              <table className="w-full text-left text-xs sm:text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 font-display">
                    <th className="py-3 px-4">রোল নং</th>
                    <th className="py-3 px-4">শিক্ষার্থীর নাম</th>
                    <th className="py-3 px-4 text-center">উপস্থিতি হার</th>
                    <th className="py-3 px-4 text-right">প্রাপ্ত নম্বর (৫০)</th>
                    <th className="py-3 px-4">শিক্ষক মন্তব্য ও ফিডব্যাক</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-sans">
                  {gradebook.records.map((rec) => (
                    <tr key={rec.student_id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                      <td className="py-3.5 px-4 font-mono font-bold text-slate-900 dark:text-white">
                        {rec.roll_number}
                      </td>
                      <td className="py-3.5 px-4 font-bengali font-semibold text-slate-800 dark:text-slate-200">
                        {rec.student_name}
                      </td>
                      <td className="py-3.5 px-4 text-center font-mono tabular-nums text-slate-600 dark:text-slate-400">
                        {rec.attendance_percent.toFixed(0)}%
                      </td>
                      <td className="py-3.5 px-4 text-right font-mono tabular-nums font-bold text-emerald-700 dark:text-emerald-400">
                        {rec.marks_obtained.toFixed(1)}
                      </td>
                      <td className="py-3.5 px-4 font-bengali text-slate-600 dark:text-slate-400 leading-relaxed max-w-xs">
                        {rec.feedback_bn}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: QUESTION PAPER CREATOR & SCHEDULER */}
      {activeTab === 'creator' && (
        <div className="bg-white dark:bg-slate-900 border-2 border-slate-300 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
          <div className="pb-6 border-b border-slate-200 dark:border-slate-800">
            <h3 className="text-xl font-bold font-bengali text-slate-900 dark:text-white">
              নতুন মডেল টেস্ট সংকলন ও প্রকাশনা
            </h3>
            <p className="text-xs text-slate-500 font-display mt-1">
              এনসিটিবি বোর্ড প্রশ্ন আর্কাইভ অথবা নিজস্ব সৃজনশীল প্রশ্ন থেকে সেকশন পরীক্ষার প্রশ্নপত্র প্রস্তুত করুন।
            </p>
          </div>

          <form onSubmit={handleCreateSubmit} className="space-y-6 mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-bold font-bengali text-slate-700 dark:text-slate-300 mb-2">
                  পরীক্ষার শিরোনাম (বাংলা)
                </label>
                <input
                  type="text"
                  required
                  value={examTitleBn}
                  onChange={(e) => setExamTitleBn(e.target.value)}
                  placeholder="উদা: পদার্থবিজ্ঞান ১ম পত্র — গতিবিদ্যা ও নিউটনিয়ান বলবিদ্যা কুইজ"
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm font-bengali focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
                />
              </div>

              <div>
                <label className="block text-xs font-bold font-bengali text-slate-700 dark:text-slate-300 mb-2">
                  বিষয় ও পত্র
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <select
                    value={examSubject}
                    onChange={(e) => setExamSubject(e.target.value)}
                    className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-sans focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
                  >
                    <option value="Physics">Physics (পদার্থবিজ্ঞান)</option>
                    <option value="Chemistry">Chemistry (রসায়ন)</option>
                    <option value="Higher Math">Higher Math (উচ্চতর গণিত)</option>
                    <option value="Biology">Biology (জীববিজ্ঞান)</option>
                  </select>

                  <select
                    value={examPaper}
                    onChange={(e) => setExamPaper(e.target.value)}
                    className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-sans focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
                  >
                    <option value="1st">1st Paper (১ম পত্র)</option>
                    <option value="2nd">2nd Paper (২য় পত্র)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold font-bengali text-slate-700 dark:text-slate-300 mb-2">
                  সময়সীমা (মিনিট)
                </label>
                <input
                  type="number"
                  min="15"
                  max="180"
                  value={examDuration}
                  onChange={(e) => setExamDuration(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
                />
              </div>

              <div>
                <label className="block text-xs font-bold font-bengali text-slate-700 dark:text-slate-300 mb-2">
                  পূর্ণমান (Marks)
                </label>
                <input
                  type="number"
                  min="10"
                  max="100"
                  value={examTotalMarks}
                  onChange={(e) => setExamTotalMarks(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
                />
              </div>
            </div>

            {/* NCTB Bank Question Selector Hint */}
            <div className="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <BookOpen className="w-5 h-5 text-[#0A2540] dark:text-amber-300" />
                <div>
                  <div className="text-xs font-bold font-bengali text-slate-900 dark:text-white">
                    এনসিটিবি বোর্ড প্রশ্ন সম্ভার সংযুক্ত
                  </div>
                  <div className="text-[11px] text-slate-500 font-display">
                    ঢাকা, চট্টগ্রাম ও রাজশাহী বোর্ডের বিগত ১০ বছরের যাচাইকৃত প্রশ্ন স্বয়ংক্রিয়ভাবে অন্তর্ভুক্ত করা হবে।
                  </div>
                </div>
              </div>
              <span className="text-xs font-mono font-bold text-slate-600 dark:text-slate-400">
                ২টি আদর্শ প্রশ্ন নির্বাচিত
              </span>
            </div>

            <div className="flex justify-end pt-4">
              <button
                type="submit"
                className="px-8 py-3 bg-[#0A2540] hover:bg-[#081c30] text-white font-bengali text-sm shadow-[0_4px_0_0_#0A2540] active:translate-y-1 active:shadow-none font-semibold rounded-2xl flex items-center gap-2 transition-all cursor-pointer"
              >
                <Send className="w-4 h-4 text-amber-300" />
                পরীক্ষার প্রশ্ন প্রকাশ করুন
              </button>
            </div>
          </form>
        </div>
      )}

      {/* TAB 4: STUDENT ROSTER & ATTENDANCE */}
      {activeTab === 'roster' && (
        <div className="bg-white dark:bg-slate-900 border-2 border-slate-300 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
          <div className="flex items-center justify-between pb-6 border-b border-slate-200 dark:border-slate-800">
            <div>
              <h3 className="text-xl font-bold font-bengali text-slate-900 dark:text-white">
                সেকশন শিক্ষার্থী তালিকা ও তথ্য
              </h3>
              <p className="text-xs text-slate-500 font-display mt-0.5">
                {selectedSection.section_name_bn} | শিক্ষাবর্ষ: {selectedSection.academic_year}
              </p>
            </div>
            <div className="flex items-center gap-2 font-mono text-xs bg-slate-100 dark:bg-slate-800 px-3 py-1.5 rounded-full">
              <Users className="w-4 h-4 text-[#0A2540]" />
              মোট শিক্ষার্থী: {selectedSection.student_count}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            {gradebook.records.map((student) => (
              <div
                key={student.student_id}
                className="p-4 bg-slate-50/70 dark:bg-slate-800/40 rounded-2xl border border-slate-200 dark:border-slate-700/80 flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-[#0A2540] text-white flex items-center justify-center font-mono font-bold text-sm">
                    {student.roll_number}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold font-bengali text-slate-900 dark:text-white">
                      {student.student_name}
                    </h4>
                    <span className="text-[11px] font-mono text-slate-500">
                      ID: {student.student_id}
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">
                    {student.attendance_percent.toFixed(0)}%
                  </div>
                  <div className="text-[10px] text-slate-400 font-bengali">
                    হাজিরা
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
