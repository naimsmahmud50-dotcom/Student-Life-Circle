/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Question Review Tribunal & Editorial Workspace Component
 * TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
 * FILE:      frontend/src/components/moderation/QuestionReviewTribunal.tsx
 * PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
 * PURPOSE:   Provides university press editorial boardroom interface for peer-review
 *            tribunals, keyboard hotkeys ('A' approve, 'R' revise, 'Q' quarantine),
 *            dual-examiner blind consensus tracking, and tactile 3D action buttons.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  BookOpen,
  Users,
  Check,
  RotateCcw,
  FileText,
  Send,
  X,
  ChevronRight,
  Filter,
  Search,
  Keyboard,
  Clock,
  Layers,
  Sparkles
} from 'lucide-react';
import { KaTeXVisualDiffViewer, DiffOption } from './KaTeXVisualDiffViewer';

export type ModerationStatus =
  | 'DRAFT'
  | 'SME_REVIEW'
  | 'BOARD_MODERATED'
  | 'APPROVED'
  | 'QUARANTINED';

export interface ReviewEntry {
  examiner_id: string;
  examiner_name: string;
  decision: 'APPROVE' | 'REVISE' | 'REJECT';
  comments: string;
  stage_at_review: string;
  timestamp: number;
}

export interface ModerationQuestionItem {
  question_id: string;
  author_id: string;
  author_name: string;
  subject: string;
  topic: string;
  class_grade: number;
  stem: string;
  options: DiffOption[];
  status: ModerationStatus;
  version: number;
  original_draft?: {
    stem: string;
    options: DiffOption[];
  };
  reviews: ReviewEntry[];
  created_at: number;
  updated_at: number;
}

export interface QuestionReviewTribunalProps {
  currentExaminerId?: string;
  currentExaminerName?: string;
  questions?: ModerationQuestionItem[];
  onApprove?: (questionId: string, comments: string) => Promise<void> | void;
  onRevise?: (questionId: string, comments: string) => Promise<void> | void;
  onQuarantine?: (questionId: string, reason: string) => Promise<void> | void;
}

const DEFAULT_QUESTIONS: ModerationQuestionItem[] = [
  {
    question_id: 'mod-q-phys-01',
    author_id: 'usr-author-01',
    author_name: 'ড. মোহাম্মদ রফিকুল ইসলাম',
    subject: 'পদার্থবিজ্ঞান ১ম পত্র',
    topic: 'নিউটনীয় বলবিদ্যা',
    class_grade: 11,
    stem: 'একটি বস্তুর ওপর প্রযুক্ত বল $F = 6t^2 + 2t$ হলে, $t = 2\\text{ s}$ সময়ে বস্তুর ভরবেগের পরিবর্তন কত? (যেখানে $t = 0$ সময়ে ভরবেগ শূন্য)',
    options: [
      { key: 'A', text: '$20\\text{ kg}\\cdot\\text{m/s}$', is_correct: true, explanation: '$\\Delta p = \\int_0^2 (6t^2 + 2t) dt = [2t^3 + t^2]_0^2 = 16 + 4 = 20$' },
      { key: 'B', text: '$16\\text{ kg}\\cdot\\text{m/s}$', is_correct: false, explanation: 'ভুল সমাকলন' },
      { key: 'C', text: '$24\\text{ kg}\\cdot\\text{m/s}$', is_correct: false, explanation: 'ভুল মান' },
      { key: 'D', text: '$12\\text{ kg}\\cdot\\text{m/s}$', is_correct: false, explanation: 'তাত্ক্ষণিক বলের সাথে বিভ্রান্তি' },
    ],
    status: 'SME_REVIEW',
    version: 1,
    original_draft: {
      stem: 'একটি বস্তুর ওপর প্রযুক্ত বল $F = 6t^2 + 2$ হলে ভরবেগ কত?',
      options: [
        { key: 'A', text: '$20\\text{ kg}\\cdot\\text{m/s}$', is_correct: true },
        { key: 'B', text: '$16\\text{ kg}\\cdot\\text{m/s}$', is_correct: false },
        { key: 'C', text: '$24\\text{ kg}\\cdot\\text{m/s}$', is_correct: false },
        { key: 'D', text: '$12\\text{ kg}\\cdot\\text{m/s}$', is_correct: false },
      ],
    },
    reviews: [],
    created_at: 1774000000,
    updated_at: 1774001800,
  },
  {
    question_id: 'mod-q-chem-02',
    author_id: 'usr-author-02',
    author_name: 'প্রফেসর আকলিমা বেগম',
    subject: 'রসায়ন ১ম পত্র',
    topic: 'গুণগত রসায়ন',
    class_grade: 11,
    stem: 'হাইড্রোজেন পরমাণুর বামার সিরিজের জন্য সর্বনিম্ন তরঙ্গদৈর্ঘ্যের ফোটনের শক্তি কত?',
    options: [
      { key: 'A', text: '$3.4\\text{ eV}$', is_correct: true, explanation: '$E = 13.6 / 2^2 = 3.4\\text{ eV}$' },
      { key: 'B', text: '$1.51\\text{ eV}$', is_correct: false, explanation: 'প্যাশ্চেন সিরিজ' },
      { key: 'C', text: '$13.6\\text{ eV}$', is_correct: false, explanation: 'লাইম্যান সিরিজ' },
      { key: 'D', text: '$0.85\\text{ eV}$', is_correct: false, explanation: 'ব্র্যাকেট সিরিজ' },
    ],
    status: 'BOARD_MODERATED',
    version: 1,
    original_draft: {
      stem: 'হাইড্রোজেনের বামার সিরিজের শক্তি কত?',
      options: [
        { key: 'A', text: '$3.4\\text{ eV}$', is_correct: true },
        { key: 'B', text: '$1.51\\text{ eV}$', is_correct: false },
      ],
    },
    reviews: [
      {
        examiner_id: 'usr-sme-01',
        examiner_name: 'ড. ফারহানা হক',
        decision: 'APPROVE',
        comments: 'পাঠ্যসূচির সাথে সংগতিপূর্ণ এবং সমীকরণ নির্ভুল।',
        stage_at_review: 'SME_REVIEW',
        timestamp: 1774002000,
      },
    ],
    created_at: 1773990000,
    updated_at: 1774002000,
  },
];

export const QuestionReviewTribunal: React.FC<QuestionReviewTribunalProps> = ({
  currentExaminerId = 'usr-tribunal-examiner',
  currentExaminerName = 'ড. কায়কোবাদ রহমান',
  questions = DEFAULT_QUESTIONS,
  onApprove,
  onRevise,
  onQuarantine,
}) => {
  const [items, setItems] = useState<ModerationQuestionItem[]>(questions);
  const [selectedIndex, setSelectedIndex] = useState<number>(0);
  const [filterStage, setFilterStage] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [feedbackComment, setFeedbackComment] = useState<string>('সমীকরণ ও পাঠ্যক্রম মানসম্মত। অনুমোদনযোগ্য।');
  const [showQuarantineModal, setShowQuarantineModal] = useState<boolean>(false);
  const [quarantineReason, setQuarantineReason] = useState<string>('');

  const filteredQuestions = items.filter((q) => {
    const matchesStage = filterStage === 'ALL' || q.status === filterStage;
    const matchesSearch =
      q.question_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.topic.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.author_name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStage && matchesSearch;
  });

  const activeQuestion: ModerationQuestionItem | undefined = filteredQuestions[selectedIndex] || filteredQuestions[0];

  const handleApprove = useCallback(async () => {
    if (!activeQuestion) return;
    if (onApprove) {
      await onApprove(activeQuestion.question_id, feedbackComment);
    }
    setItems((prev) =>
      prev.map((q) => {
        if (q.question_id === activeQuestion.question_id) {
          const nextStatus = q.status === 'SME_REVIEW' ? 'BOARD_MODERATED' : 'APPROVED';
          return {
            ...q,
            status: nextStatus,
            reviews: [
              ...q.reviews,
              {
                examiner_id: currentExaminerId,
                examiner_name: currentExaminerName,
                decision: 'APPROVE',
                comments: feedbackComment,
                stage_at_review: q.status,
                timestamp: Math.floor(Date.now() / 1000),
              },
            ],
          };
        }
        return q;
      })
    );
  }, [activeQuestion, currentExaminerId, currentExaminerName, feedbackComment, onApprove]);

  const handleRevise = useCallback(async () => {
    if (!activeQuestion) return;
    if (onRevise) {
      await onRevise(activeQuestion.question_id, feedbackComment);
    }
    setItems((prev) =>
      prev.map((q) => {
        if (q.question_id === activeQuestion.question_id) {
          return {
            ...q,
            status: 'DRAFT',
            reviews: [
              ...q.reviews,
              {
                examiner_id: currentExaminerId,
                examiner_name: currentExaminerName,
                decision: 'REVISE',
                comments: feedbackComment,
                stage_at_review: q.status,
                timestamp: Math.floor(Date.now() / 1000),
              },
            ],
          };
        }
        return q;
      })
    );
  }, [activeQuestion, currentExaminerId, currentExaminerName, feedbackComment, onRevise]);

  const handleQuarantineConfirm = useCallback(async () => {
    if (!activeQuestion || !quarantineReason.trim()) return;
    if (onQuarantine) {
      await onQuarantine(activeQuestion.question_id, quarantineReason);
    }
    setItems((prev) =>
      prev.map((q) => {
        if (q.question_id === activeQuestion.question_id) {
          return {
            ...q,
            status: 'QUARANTINED',
          };
        }
        return q;
      })
    );
    setShowQuarantineModal(false);
    setQuarantineReason('');
  }, [activeQuestion, quarantineReason, onQuarantine]);

  // Global Keyboard Shortcuts (A: Approve, R: Revise, Q: Quarantine)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Do not trigger hotkeys when user is actively focused on an input or textarea
      const target = e.target as HTMLElement;
      if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')) {
        return;
      }

      if (e.key === 'a' || e.key === 'A') {
        e.preventDefault();
        handleApprove();
      } else if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        handleRevise();
      } else if (e.key === 'q' || e.key === 'Q') {
        e.preventDefault();
        setShowQuarantineModal(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleApprove, handleRevise]);

  const getStatusBadge = (status: ModerationStatus) => {
    switch (status) {
      case 'DRAFT':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            <Clock className="w-3.5 h-3.5" />
            খসড়া পর্যায়
          </span>
        );
      case 'SME_REVIEW':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-900 border border-amber-200">
            <Users className="w-3.5 h-3.5 text-amber-700" />
            ১ম পর্যায় (SME Review)
          </span>
        );
      case 'BOARD_MODERATED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-sky-50 text-sky-900 border border-sky-200">
            <ShieldCheck className="w-3.5 h-3.5 text-sky-700" />
            ২য় পর্যায় (বোর্ড নিরীক্ষণ)
          </span>
        );
      case 'APPROVED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-900 border border-emerald-200">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
            দ্বৈত ঐকমত্যে অনুমোদিত
          </span>
        );
      case 'QUARANTINED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-900 border border-rose-200">
            <AlertCircle className="w-3.5 h-3.5 text-rose-700" />
            কোয়ারেন্টিনকৃত
          </span>
        );
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0A2540] font-sans pb-16">
      {/* Top Academic Tribunal Header */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 px-4 sm:px-8 py-4 shadow-xs">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-xs">
              <BookOpen className="w-5 h-5 stroke-[1.75]" />
            </div>
            <div>
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <span>বাংলাদেশ শিক্ষা বোর্ড সমন্বিত প্রশ্ন ব্যাংক</span>
                <span className="text-slate-300">•</span>
                <span>নিরীক্ষণ ট্রাইব্যুনাল</span>
              </div>
              <h1 className="text-lg sm:text-xl font-bold text-[#0A2540] tracking-tight">
                পিয়ার-রিভিউ ও প্রশ্নপত্র পরিশোধন কনসোল
              </h1>
            </div>
          </div>

          {/* Examiner Info & Hotkey Pill */}
          <div className="flex items-center gap-3">
            <div className="hidden md:inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#FAFAF8] border border-slate-200 text-xs text-slate-600">
              <Keyboard className="w-3.5 h-3.5 text-slate-500" />
              <span>শর্টকাট: <kbd className="px-1.5 py-0.5 bg-white border border-slate-300 rounded font-mono font-bold text-slate-800">A</kbd> অনুমোদন | <kbd className="px-1.5 py-0.5 bg-white border border-slate-300 rounded font-mono font-bold text-slate-800">R</kbd> সংশোধন | <kbd className="px-1.5 py-0.5 bg-white border border-slate-300 rounded font-mono font-bold text-slate-800">Q</kbd> কোয়ারেন্টিন</span>
            </div>

            <div className="px-3.5 py-1.5 rounded-xl bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-800">
              পর্যালোচক: {currentExaminerName}
            </div>
          </div>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Moderation Queue List (4 cols) */}
        <aside className="lg:col-span-4 bg-white border border-slate-200 rounded-3xl p-5 shadow-xs sticky top-24">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-slate-500" />
              <h2 className="text-sm font-bold text-[#0A2540]">পর্যালোচনা সারি (Queue)</h2>
            </div>
            <span className="text-xs font-medium text-slate-500">
              মোট: {filteredQuestions.length} টি
            </span>
          </div>

          {/* Search Box */}
          <div className="relative mb-3">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="বিষয়, অধ্যায় বা আইডি খুঁজুন..."
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 text-xs text-slate-800 focus:outline-hidden focus:border-[#0A2540]"
            />
          </div>

          {/* Filter Tabs */}
          <div className="flex items-center gap-1 overflow-x-auto pb-2 mb-4">
            {[
              { id: 'ALL', label: 'সকল' },
              { id: 'SME_REVIEW', label: 'SME' },
              { id: 'BOARD_MODERATED', label: 'বোর্ড' },
              { id: 'APPROVED', label: 'অনুমোদিত' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setFilterStage(tab.id)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                  filterStage === tab.id
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-[#FAFAF8] text-slate-600 hover:bg-slate-100'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Question List */}
          <div className="space-y-2.5 max-h-[520px] overflow-y-auto pr-1">
            {filteredQuestions.map((q, idx) => {
              const isSelected = activeQuestion?.question_id === q.question_id;
              const approvalCount = q.reviews.filter((r) => r.decision === 'APPROVE').length;

              return (
                <button
                  key={q.question_id}
                  onClick={() => setSelectedIndex(idx)}
                  className={`w-full text-left p-3.5 rounded-2xl border transition-all ${
                    isSelected
                      ? 'bg-[#0A2540]/5 border-[#0A2540] ring-1 ring-[#0A2540]/20 shadow-xs'
                      : 'bg-[#FAFAF8] border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-bold text-[#0A2540]">{q.subject}</span>
                    <span className="text-xs text-slate-400 font-mono">v{q.version}.0</span>
                  </div>
                  <div className="text-xs text-slate-800 line-clamp-2 mb-2 font-medium">
                    {q.stem}
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-500">অনুমোদন: {approvalCount}/২</span>
                    {getStatusBadge(q.status)}
                  </div>
                </button>
              );
            })}
          </div>
        </aside>

        {/* Right: KaTeX Visual Diff & Action Panel (8 cols) */}
        <section className="lg:col-span-8 space-y-6">
          {activeQuestion ? (
            <>
              {/* Question Metadata Card */}
              <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                      {activeQuestion.question_id}
                    </span>
                    <span className="text-xs text-slate-400">•</span>
                    <span className="text-xs text-slate-600">রচয়িতা: {activeQuestion.author_name}</span>
                  </div>
                  <h3 className="text-base font-bold text-[#0A2540]">
                    {activeQuestion.subject} — {activeQuestion.topic} (শ্রেণি: {activeQuestion.class_grade}ম)
                  </h3>
                </div>

                <div className="flex items-center gap-3">
                  {getStatusBadge(activeQuestion.status)}
                  <div className="text-xs font-semibold text-slate-600 px-3 py-1 bg-[#FAFAF8] border border-slate-200 rounded-xl">
                    ঐকমত্য: {activeQuestion.reviews.filter((r) => r.decision === 'APPROVE').length} / ২ জন
                  </div>
                </div>
              </div>

              {/* KaTeX Visual Diff Viewer */}
              <KaTeXVisualDiffViewer
                originalStem={activeQuestion.original_draft?.stem || activeQuestion.stem}
                revisedStem={activeQuestion.stem}
                originalOptions={activeQuestion.original_draft?.options || activeQuestion.options}
                revisedOptions={activeQuestion.options}
                originalVersion={Math.max(1, activeQuestion.version - 1)}
                revisedVersion={activeQuestion.version}
                subject={activeQuestion.subject}
                topic={activeQuestion.topic}
              />

              {/* Existing Reviews Trail */}
              {activeQuestion.reviews.length > 0 && (
                <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    পূর্ববর্তী পর্যালোচকদের মন্তব্য (Blind Review Trail)
                  </h4>
                  <div className="space-y-3">
                    {activeQuestion.reviews.map((rev, i) => (
                      <div key={i} className="p-3.5 rounded-2xl bg-[#FAFAF8] border border-slate-200 text-xs">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-bold text-[#0A2540]">{rev.examiner_name}</span>
                          <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                            অনুমোদিত
                          </span>
                        </div>
                        <p className="text-slate-700">{rev.comments}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action & Feedback Console */}
              <div className="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xs space-y-5">
                <div>
                  <label className="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">
                    পর্যালোচনা মন্তব্য ও নির্দেশিকা (Editorial Notes)
                  </label>
                  <textarea
                    value={feedbackComment}
                    onChange={(e) => setFeedbackComment(e.target.value)}
                    rows={2}
                    className="w-full p-3.5 rounded-2xl border border-slate-200 text-sm text-slate-800 focus:outline-hidden focus:border-[#0A2540] focus:ring-1 focus:ring-[#0A2540]"
                    placeholder="প্রশ্নটির মান, সমীকরণ ও বিকল্প উত্তর সম্পর্কে আপনার মতামত লিখুন..."
                  />
                </div>

                {/* Tactile Action Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
                  <button
                    onClick={() => setShowQuarantineModal(true)}
                    className="w-full sm:w-auto py-2.5 px-4 rounded-2xl border border-rose-300 text-rose-800 bg-rose-50/80 hover:bg-rose-100 text-xs sm:text-sm font-semibold flex items-center justify-center gap-2 transition-all"
                  >
                    <AlertCircle className="w-4 h-4" />
                    <span>জরুরি কোয়ারেন্টিন (Q)</span>
                  </button>

                  <div className="flex items-center gap-3 w-full sm:w-auto">
                    {/* Paper Outline Button */}
                    <button
                      onClick={handleRevise}
                      className="flex-1 sm:flex-none py-3 px-5 rounded-2xl border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 text-xs sm:text-sm font-semibold flex items-center justify-center gap-2 transition-all shadow-xs"
                    >
                      <RotateCcw className="w-4 h-4" />
                      <span>সংশোধনের নির্দেশ দিন (R)</span>
                    </button>

                    {/* Academic Emerald 3D Tactile Button */}
                    <button
                      onClick={handleApprove}
                      className="flex-1 sm:flex-none py-3 px-6 rounded-2xl bg-emerald-700 text-white text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none hover:bg-emerald-800 transition-all flex items-center justify-center gap-2"
                    >
                      <Check className="w-4 h-4 stroke-[2.5]" />
                      <span>প্রশ্ন অনুমোদন করুন (A)</span>
                    </button>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white border border-slate-200 rounded-3xl p-12 text-center text-slate-500">
              <FileText className="w-8 h-8 mx-auto mb-3 text-slate-400" />
              <p>পর্যালোচনার জন্য কোনো প্রশ্ন নির্বাচিত নেই।</p>
            </div>
          )}
        </section>
      </main>

      {/* Emergency Quarantine Modal */}
      {showQuarantineModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0A2540]/40 p-4">
          <div className="bg-white border border-slate-200 rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
              <div className="flex items-center gap-2 text-rose-800 font-bold text-base">
                <AlertCircle className="w-5 h-5 text-rose-600" />
                <span>জরুরি কোয়ারেন্টিন নিশ্চিতকরণ</span>
              </div>
              <button
                onClick={() => setShowQuarantineModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs sm:text-sm text-slate-600 mb-4">
              কোয়ারেন্টিন সক্রিয় করলে প্রশ্নটি অবিলম্বে সমস্ত সক্রিয় পরীক্ষা ও অনুশীলন পুল থেকে প্রত্যাহার করা হবে।
            </p>

            <div className="mb-6">
              <label className="block text-xs font-bold text-slate-700 uppercase mb-2">
                কোয়ারেন্টিনের কারণ (অডিট ট্রেইলে লিপিবদ্ধ হবে):
              </label>
              <textarea
                value={quarantineReason}
                onChange={(e) => setQuarantineReason(e.target.value)}
                rows={3}
                placeholder="যেমন: সমীকরণে বৈজ্ঞানিক অসংগতি বা ভুল উত্তরমালা..."
                className="w-full p-3 rounded-xl border border-slate-200 text-xs sm:text-sm text-slate-800 focus:outline-hidden focus:border-rose-600"
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowQuarantineModal(false)}
                className="flex-1 py-2.5 px-4 rounded-xl border border-slate-200 text-slate-700 text-xs sm:text-sm font-semibold hover:bg-slate-50"
              >
                বাতিল করুন
              </button>
              <button
                onClick={handleQuarantineConfirm}
                disabled={!quarantineReason.trim()}
                className="flex-1 py-2.5 px-4 rounded-2xl bg-rose-700 text-white text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#9F1239] active:translate-y-1 active:shadow-none hover:bg-rose-800 disabled:opacity-50 disabled:pointer-events-none transition-all flex items-center justify-center gap-2"
              >
                <AlertCircle className="w-4 h-4" />
                <span>কোয়ারেন্টিন কার্যকর করুন</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
