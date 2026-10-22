/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Proctor Teacher Monitor Component
 * TOPIC:     Phase 116 Digital Examination Hall & Proctoring Integrity Tower
 * FILE:      frontend/src/components/exam-hall/ProctorTeacherMonitor.tsx
 * PHASE:     Phase 116 - Digital Examination Hall & Proctoring Integrity Tower
 * PURPOSE:   Provides real-time examinee roster monitoring for invigilators and teachers,
 *            tracking non-punitive integrity status bands (Exemplary, Monitored, Under Review),
 *            telemetry telemetry logs, and student answer progression with zero facial surveillance.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState, useMemo } from 'react';
import {
  Users,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertCircle,
  Search,
  Filter,
  Layers,
  Eye,
  FileCheck2,
  RefreshCw,
  X,
  ChevronRight,
  UserCheck,
  BookOpen
} from 'lucide-react';

export type IntegrityBand = 'EXEMPLARY' | 'MONITORED' | 'UNDER_REVIEW';

export interface ExamineeSessionRecord {
  session_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  answered_count: number;
  total_questions: number;
  flagged_count: number;
  tab_switches: number;
  blur_duration_seconds: number;
  audio_surges: number;
  integrity_score: number;
  integrity_band: IntegrityBand;
  status: 'ACTIVE' | 'FINALIZED';
  started_at: string;
  last_heartbeat: string;
  receipt_hash?: string;
}

export interface ProctorTeacherMonitorProps {
  examId?: string;
  examTitleBn?: string;
  institutionName?: string;
  examinees?: ExamineeSessionRecord[];
  onRefresh?: () => void;
  onFlagStudentForReview?: (sessionId: string) => void;
}

const DEFAULT_EXAMINEES: ExamineeSessionRecord[] = [
  {
    session_id: 'sess-hall-001',
    student_id: 'std-2026-042',
    student_name: 'সৌরভ আহমেদ',
    roll_number: '১০১',
    answered_count: 5,
    total_questions: 5,
    flagged_count: 1,
    tab_switches: 0,
    blur_duration_seconds: 1.2,
    audio_surges: 0,
    integrity_score: 99.0,
    integrity_band: 'EXEMPLARY',
    status: 'ACTIVE',
    started_at: '2026-10-20T10:00:00Z',
    last_heartbeat: '2026-10-20T10:35:12Z',
  },
  {
    session_id: 'sess-hall-002',
    student_id: 'std-2026-088',
    student_name: 'নুসরাত জাহান',
    roll_number: '১০২',
    answered_count: 4,
    total_questions: 5,
    flagged_count: 0,
    tab_switches: 1,
    blur_duration_seconds: 3.5,
    audio_surges: 1,
    integrity_score: 97.5,
    integrity_band: 'EXEMPLARY',
    status: 'ACTIVE',
    started_at: '2026-10-20T10:01:00Z',
    last_heartbeat: '2026-10-20T10:35:10Z',
  },
  {
    session_id: 'sess-hall-003',
    student_id: 'std-2026-105',
    student_name: 'তানভীর হাসান',
    roll_number: '১০৩',
    answered_count: 5,
    total_questions: 5,
    flagged_count: 2,
    tab_switches: 4,
    blur_duration_seconds: 18.0,
    audio_surges: 2,
    integrity_score: 82.5,
    integrity_band: 'MONITORED',
    status: 'FINALIZED',
    started_at: '2026-10-20T10:00:30Z',
    last_heartbeat: '2026-10-20T10:32:00Z',
    receipt_hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
  },
  {
    session_id: 'sess-hall-004',
    student_id: 'std-2026-119',
    student_name: 'ফারহানা ইয়াসমিন',
    roll_number: '১০৪',
    answered_count: 3,
    total_questions: 5,
    flagged_count: 1,
    tab_switches: 6,
    blur_duration_seconds: 35.5,
    audio_surges: 4,
    integrity_score: 68.0,
    integrity_band: 'UNDER_REVIEW',
    status: 'ACTIVE',
    started_at: '2026-10-20T10:02:15Z',
    last_heartbeat: '2026-10-20T10:35:05Z',
  },
];

export const ProctorTeacherMonitor: React.FC<ProctorTeacherMonitorProps> = ({
  examId = 'exam-phy-hsc-2026',
  examTitleBn = 'উচ্চমাধ্যমিক পদার্থবিজ্ঞান ১ম পত্র — চুড়ান্ত পরীক্ষা',
  institutionName = 'ঢাকা রেসিডেনসিয়াল মডেল কলেজ',
  examinees = DEFAULT_EXAMINEES,
  onRefresh,
  onFlagStudentForReview,
}) => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [filterBand, setFilterBand] = useState<string>('ALL');
  const [selectedExaminee, setSelectedExaminee] = useState<ExamineeSessionRecord | null>(null);

  // Filtered List
  const filteredExaminees = useMemo(() => {
    return examinees.filter((ex) => {
      const matchesSearch =
        ex.student_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ex.roll_number.includes(searchQuery) ||
        ex.student_id.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesBand =
        filterBand === 'ALL' ||
        (filterBand === 'EXEMPLARY' && ex.integrity_band === 'EXEMPLARY') ||
        (filterBand === 'MONITORED' && ex.integrity_band === 'MONITORED') ||
        (filterBand === 'UNDER_REVIEW' && ex.integrity_band === 'UNDER_REVIEW');

      return matchesSearch && matchesBand;
    });
  }, [examinees, searchQuery, filterBand]);

  // Aggregate Metrics
  const totalCount = examinees.length;
  const activeCount = examinees.filter((e) => e.status === 'ACTIVE').length;
  const finalizedCount = examinees.filter((e) => e.status === 'FINALIZED').length;
  const avgIntegrity =
    totalCount > 0
      ? (examinees.reduce((acc, curr) => acc + curr.integrity_score, 0) / totalCount).toFixed(1)
      : '100.0';

  const getBandBadge = (band: IntegrityBand) => {
    switch (band) {
      case 'EXEMPLARY':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 stroke-[1.75]" />
            অখণ্ডতা অক্ষুণ্ণ
          </span>
        );
      case 'MONITORED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200">
            <Clock className="w-3.5 h-3.5 text-amber-600 stroke-[1.75]" />
            পর্যবেক্ষণাধীন
          </span>
        );
      case 'UNDER_REVIEW':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-300">
            <AlertCircle className="w-3.5 h-3.5 text-slate-600 stroke-[1.75]" />
            পুনঃযাচাই প্রয়োজন
          </span>
        );
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0A2540] font-sans pb-16">
      {/* Top Academic Proctor Bar */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 px-4 sm:px-8 py-4 shadow-xs">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">
              <span>{institutionName}</span>
              <span className="text-slate-300">•</span>
              <span>পরীক্ষা কোড: {examId}</span>
            </div>
            <h1 className="text-lg sm:text-xl font-bold text-[#0A2540] tracking-tight">
              {examTitleBn} — পরিদর্শক কন্ট্রোল টাওয়ার
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold shadow-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>সরাসরি নিরীক্ষণ সক্রিয়</span>
            </div>

            <button
              onClick={onRefresh}
              className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:text-[#0A2540] hover:bg-slate-50 transition-colors"
              title="রিফ্রেশ করুন"
              aria-label="রিফ্রেশ করুন"
            >
              <RefreshCw className="w-4 h-4 stroke-[1.75]" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        {/* Metric Cards Grid */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">মোট পরীক্ষার্থী</span>
              <Users className="w-4 h-4 text-slate-400" />
            </div>
            <div className="text-2xl font-bold text-[#0A2540]">{totalCount} জন</div>
            <span className="text-xs text-slate-500 mt-1 block">অনুমোদিত রোল তালিকা</span>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">পরীক্ষা প্রদানরত</span>
              <Clock className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl font-bold text-emerald-700">{activeCount} জন</div>
            <span className="text-xs text-slate-500 mt-1 block">বর্তমান লাইভ ডেস্ক সেশন</span>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">সমাপ্তকৃত পরীক্ষা</span>
              <CheckCircle2 className="w-4 h-4 text-slate-600" />
            </div>
            <div className="text-2xl font-bold text-[#0A2540]">{finalizedCount} জন</div>
            <span className="text-xs text-slate-500 mt-1 block">ক্রিপ্টোগ্রাফিক সিল নিবন্ধিত</span>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">গড় অখণ্ডতা সূচক</span>
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl font-bold text-[#0A2540]">{avgIntegrity}%</div>
            <span className="text-xs text-slate-500 mt-1 block">ক্লায়েন্ট হিউরিস্টিক স্কোর</span>
          </div>
        </section>

        {/* Filter & Search Bar */}
        <section className="bg-white border border-slate-200 rounded-3xl p-5 shadow-xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          {/* Search Field */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="পরীক্ষার্থীর নাম, রোল নম্বর বা শিক্ষার্থী আইডি দিয়ে খুঁজুন..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm text-slate-800 focus:outline-hidden focus:border-[#0A2540] focus:ring-1 focus:ring-[#0A2540]"
            />
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
            {[
              { id: 'ALL', label: 'সকল পরীক্ষার্থী' },
              { id: 'EXEMPLARY', label: 'অখণ্ডতা অক্ষুণ্ণ (≥৯০)' },
              { id: 'MONITORED', label: 'পর্যবেক্ষণাধীন (৭০-৮৯)' },
              { id: 'UNDER_REVIEW', label: 'পুনঃযাচাই প্রয়োজন (<৭০)' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setFilterBand(tab.id)}
                className={`px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                  filterBand === tab.id
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-[#FAFAF8] text-slate-600 border border-slate-200 hover:border-slate-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </section>

        {/* Examinee Roster Table */}
        <section className="bg-white border border-slate-200 rounded-3xl shadow-xs overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-slate-500" />
              <h2 className="text-base font-bold text-[#0A2540]">পরীক্ষার্থী তালিকা ও লাইভ পর্যবেক্ষণ</h2>
            </div>
            <span className="text-xs font-medium text-slate-500">
              প্রদর্শিত: {filteredExaminees.length} জন
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-[#FAFAF8] text-xs font-semibold text-slate-500 uppercase border-b border-slate-100">
                <tr>
                  <th className="px-6 py-3.5">রোল ও নাম</th>
                  <th className="px-6 py-3.5">অগ্রগতি</th>
                  <th className="px-6 py-3.5">চিহ্নিত প্রশ্ন</th>
                  <th className="px-6 py-3.5">ট্যাব / ব্লার সময়</th>
                  <th className="px-6 py-3.5">অখণ্ডতা স্কোর</th>
                  <th className="px-6 py-3.5">মর্যাদা ব্যান্ড</th>
                  <th className="px-6 py-3.5 text-right">কার্যক্রম</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredExaminees.map((ex) => (
                  <tr key={ex.session_id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-[#0A2540]">{ex.student_name}</div>
                      <div className="text-xs text-slate-500">রোল: {ex.roll_number} • আইডি: {ex.student_id}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-slate-800">
                          {ex.answered_count} / {ex.total_questions}
                        </span>
                        <span className="text-xs text-slate-400">
                          ({Math.round((ex.answered_count / ex.total_questions) * 100)}%)
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-600">
                      {ex.flagged_count > 0 ? (
                        <span className="px-2.5 py-0.5 rounded-lg bg-amber-50 text-amber-800 text-xs font-semibold border border-amber-200">
                          {ex.flagged_count} টি চিহ্নিত
                        </span>
                      ) : (
                        <span className="text-xs text-slate-400">০</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-xs text-slate-600">
                      <div>ট্যাব সুইচ: <span className="font-semibold">{ex.tab_switches} বার</span></div>
                      <div>ব্লার সময়: <span className="font-semibold">{ex.blur_duration_seconds} সে.</span></div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-base font-bold text-[#0A2540]">{ex.integrity_score}%</span>
                    </td>
                    <td className="px-6 py-4">
                      {getBandBadge(ex.integrity_band)}
                    </td>
                    <td className="px-6 py-4 text-right">
                      {/* Tactile 3D Oxford Navy Inspect Button */}
                      <button
                        onClick={() => setSelectedExaminee(ex)}
                        className="py-1.5 px-3 rounded-xl bg-[#0A2540] text-white text-xs font-semibold shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none hover:bg-[#0d2f50] transition-all inline-flex items-center gap-1.5"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>নিরীক্ষণ</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>

      {/* Examinee Telemetry Audit Modal */}
      {selectedExaminee && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0A2540]/40 p-4">
          <div className="bg-white border border-slate-200 rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl relative">
            <button
              onClick={() => setSelectedExaminee(null)}
              className="absolute top-6 right-6 p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
              title="বন্ধ করুন"
              aria-label="বন্ধ করুন"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
              <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-xs">
                <UserCheck className="w-6 h-6 stroke-[1.75]" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-[#0A2540]">{selectedExaminee.student_name}</h3>
                <p className="text-xs text-slate-500">
                  রোল: {selectedExaminee.roll_number} • আইডি: {selectedExaminee.student_id} • সেশন: {selectedExaminee.session_id}
                </p>
              </div>
            </div>

            <div className="space-y-4 mb-6 text-sm">
              <div className="grid grid-cols-2 gap-3 p-4 bg-[#FAFAF8] border border-slate-200 rounded-2xl">
                <div>
                  <span className="text-xs text-slate-500 block uppercase">অখণ্ডতা সূচক</span>
                  <span className="text-xl font-bold text-[#0A2540]">{selectedExaminee.integrity_score}%</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block uppercase">মর্যাদা ব্যান্ড</span>
                  <div className="mt-1">{getBandBadge(selectedExaminee.integrity_band)}</div>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block uppercase">উত্তর সম্পন্ন</span>
                  <span className="text-sm font-semibold text-slate-800">
                    {selectedExaminee.answered_count} / {selectedExaminee.total_questions} টি
                  </span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block uppercase">চিহ্নিত প্রশ্ন</span>
                  <span className="text-sm font-semibold text-slate-800">
                    {selectedExaminee.flagged_count} টি
                  </span>
                </div>
              </div>

              {/* Heuristic Audit Summary */}
              <div className="border border-slate-200 rounded-2xl p-4">
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                  ক্লায়েন্ট হিউরিস্টিক অডিট পর্যবেক্ষণ (শূন্য বায়োমেট্রিক রেকর্ড)
                </h4>
                <ul className="text-xs text-slate-600 space-y-2">
                  <li className="flex justify-between">
                    <span>ট্যাব পরিবর্তনের সংখ্যা:</span>
                    <span className="font-semibold text-slate-800">{selectedExaminee.tab_switches} বার</span>
                  </li>
                  <li className="flex justify-between">
                    <span>উইন্ডো ব্লার সময়কাল:</span>
                    <span className="font-semibold text-slate-800">{selectedExaminee.blur_duration_seconds} সেকেন্ড</span>
                  </li>
                  <li className="flex justify-between">
                    <span>শব্দ মাত্রা সীমার ঊর্ধ্বগতি:</span>
                    <span className="font-semibold text-slate-800">{selectedExaminee.audio_surges} বার</span>
                  </li>
                </ul>
              </div>

              {selectedExaminee.receipt_hash && (
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs">
                  <span className="font-semibold text-emerald-800 block mb-1">
                    SHA-256 ক্রিপ্টোগ্রাফিক রিসিট নিশ্চিতকরণ:
                  </span>
                  <span className="font-mono text-emerald-950 break-all select-all">
                    {selectedExaminee.receipt_hash}
                  </span>
                </div>
              )}
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setSelectedExaminee(null)}
                className="flex-1 py-2.5 px-4 rounded-xl border border-slate-200 text-slate-700 text-xs sm:text-sm font-semibold hover:bg-slate-50 transition-all"
              >
                বন্ধ করুন
              </button>
              <button
                onClick={() => {
                  if (onFlagStudentForReview) {
                    onFlagStudentForReview(selectedExaminee.session_id);
                  }
                  setSelectedExaminee(null);
                }}
                className="flex-1 py-2.5 px-4 rounded-2xl bg-[#0A2540] text-white text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none hover:bg-[#0d2f50] transition-all"
              >
                অধিবেশন অনুমোদন করুন
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
