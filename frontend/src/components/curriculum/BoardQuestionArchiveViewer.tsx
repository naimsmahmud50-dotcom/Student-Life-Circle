/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Official NCTB Board Question Paper Archive & KaTeX Equation Viewer
 * TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
 * FILE:      frontend/src/components/curriculum/BoardQuestionArchiveViewer.tsx
 * PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
 * PURPOSE:   Renders authentic, prestigious Bangladesh NCTB board question papers
 *            with sub-pixel KaTeX math rendering, dual Exam/Study modes, printable
 *            booklet layout, authentic board seals, and tactile Oxford Navy styling.
 * STANDARDS: NCTB Curriculum 2024, KaTeX Math Spec, UI/UX Pro Max, Strict Zero-Emoji
 */

import React, { useState, useMemo } from 'react';
import {
  BookOpen,
  Award,
  CheckCircle,
  FileText,
  Printer,
  Eye,
  EyeOff,
  Filter,
  Search,
  CheckCircle2,
  HelpCircle,
  RotateCcw,
  Sparkles,
  Layers,
  ChevronDown,
  ChevronUp,
  Download
} from 'lucide-react';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';
import { EmptyState } from '@/components/ui/empty-state';
import { BoardYearSwiper } from './BoardYearSwiper';

export interface CQSubQuestion {
  label: string;
  type: string;
  marks: number;
  question_bn: string;
  solution_bn: string;
  rubric_bn: string;
}

export interface MCQOption {
  key: string;
  text_bn: string;
  is_correct: boolean;
}

export interface BoardQuestionItem {
  id: string;
  level: 'SSC' | 'HSC';
  subject: string;
  subject_bn: string;
  paper: string;
  board: string;
  board_bn: string;
  year: number;
  chapter: string;
  question_type: 'CQ' | 'MCQ';
  stem_bn: string;
  cq_sub_questions?: {
    ka: CQSubQuestion;
    kha: CQSubQuestion;
    ga: CQSubQuestion;
    gha: CQSubQuestion;
  };
  options?: MCQOption[];
  correct_option_key?: string;
  explanation_bn?: string;
  marks_total: number;
  content_hash: string;
}

export interface BoardQuestionArchiveViewerProps {
  initialQuestions: BoardQuestionItem[];
}

export const BoardQuestionArchiveViewer: React.FC<BoardQuestionArchiveViewerProps> = ({
  initialQuestions
}) => {
  const [mode, setMode] = useState<'exam' | 'study'>('study');
  const [selectedLevel, setSelectedLevel] = useState<string>('all');
  const [selectedSubject, setSelectedSubject] = useState<string>('all');
  const [selectedBoard, setSelectedBoard] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  // MCQ state in Exam Mode
  const [userSelectedOptions, setUserSelectedOptions] = useState<Record<string, string>>({});
  
  // Expand/collapse individual solutions
  const [expandedSolutions, setExpandedSolutions] = useState<Record<string, boolean>>({});

  // Filter questions based on state
  const filteredQuestions = useMemo(() => {
    return initialQuestions.filter((item) => {
      if (selectedLevel !== 'all' && item.level !== selectedLevel) return false;
      if (selectedSubject !== 'all' && item.subject !== selectedSubject) return false;
      if (selectedBoard !== 'all' && item.board !== selectedBoard) return false;
      if (selectedYear !== 'all' && item.year.toString() !== selectedYear) return false;
      if (selectedType !== 'all' && item.question_type !== selectedType) return false;
      
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase().trim();
        const inStem = item.stem_bn.toLowerCase().includes(query);
        const inChapter = item.chapter.toLowerCase().includes(query);
        const inBoard = item.board_bn.toLowerCase().includes(query);
        const inSubject = item.subject_bn.toLowerCase().includes(query);
        return inStem || inChapter || inBoard || inSubject;
      }
      return true;
    });
  }, [initialQuestions, selectedLevel, selectedSubject, selectedBoard, selectedYear, selectedType, searchQuery]);

  const toggleSolution = (id: string) => {
    setExpandedSolutions((prev) => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const handleOptionSelect = (questionId: string, optionKey: string) => {
    setUserSelectedOptions((prev) => ({
      ...prev,
      [questionId]: optionKey
    }));
  };

  const handlePrint = () => {
    window.print();
  };

  const handleResetFilters = () => {
    setSelectedLevel('all');
    setSelectedSubject('all');
    setSelectedBoard('all');
    setSelectedYear('all');
    setSelectedType('all');
    setSearchQuery('');
  };

  // Distinct facet arrays
  const boards = [
    { key: 'all', label_bn: 'সকল বোর্ড' },
    { key: 'Dhaka', label_bn: 'ঢাকা' },
    { key: 'Chittagong', label_bn: 'চট্টগ্রাম' },
    { key: 'Rajshahi', label_bn: 'রাজশাহী' },
    { key: 'Comilla', label_bn: 'কুমিল্লা' },
    { key: 'Sylhet', label_bn: 'সিলেট' },
    { key: 'Barisal', label_bn: 'বরিশাল' },
    { key: 'Dinajpur', label_bn: 'দিনাজপুর' },
    { key: 'Jessore', label_bn: 'যশোর' },
    { key: 'Mymensingh', label_bn: 'ময়মনসিংহ' }
  ];

  const years = ['all', '2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015'];

  const subjects = [
    { key: 'all', label_bn: 'সকল বিষয়' },
    { key: 'Physics', label_bn: 'পদার্থবিজ্ঞান' },
    { key: 'Chemistry', label_bn: 'রসায়ন' },
    { key: 'Higher Mathematics', label_bn: 'উচ্চতর গণিত' },
    { key: 'Biology', label_bn: 'জীববিজ্ঞান' },
    { key: 'Information & Communication Technology', label_bn: 'তথ্য ও যোগাযোগ প্রযুক্তি' }
  ];

  return (
    <div className="w-full">
      {/* =========================================================================
          CONTROL & FILTER BAR (Hidden during @media print)
         ========================================================================= */}
      <section className="print:hidden mb-8 space-y-6">
        {/* Top Action Bar */}
        <div className="bg-white dark:bg-[#0F172A] p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3 w-full md:w-auto">
            <div className="w-10 h-10 rounded-xl bg-[#0A2540] text-white flex items-center justify-center shadow-sm">
              <BookOpen className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white font-bengali text-lg leading-snug">
                বোর্ড প্রশ্ন আর্কাইভ ফিল্টার
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-bengali">
                মোট পাওয়া গেছে: <span className="font-bold text-[#0A2540] dark:text-amber-400">{filteredQuestions.length}</span> টি প্রশ্ন
              </p>
            </div>
          </div>

          {/* Mode Switcher & Print Button */}
          <div className="flex items-center gap-3 w-full md:w-auto justify-end">
            {/* Mode Switcher */}
            <div className="inline-flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
              <button
                type="button"
                onClick={() => setMode('study')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-bengali transition-all duration-150 flex items-center gap-1.5 ${
                  mode === 'study'
                    ? 'bg-[#0A2540] text-white shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <Eye className="w-3.5 h-3.5" />
                <span>সমাধান ও ব্যাখ্যা</span>
              </button>
              <button
                type="button"
                onClick={() => setMode('exam')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-bengali transition-all duration-150 flex items-center gap-1.5 ${
                  mode === 'exam'
                    ? 'bg-[#0A2540] text-white shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <EyeOff className="w-3.5 h-3.5" />
                <span>পরীক্ষা মোড (উত্তর গোপন)</span>
              </button>
            </div>

            {/* Print Trigger */}
            <button
              type="button"
              onClick={handlePrint}
              className="px-4 py-2 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-600 rounded-xl text-xs font-semibold font-bengali flex items-center gap-2 shadow-[0_2px_0_0_#CBD5E1] active:translate-y-0.5 active:shadow-none transition-all"
            >
              <Printer className="w-4 h-4 text-[#0A2540] dark:text-amber-400" />
              <span className="hidden sm:inline">প্রশ্নপত্র প্রিন্ট করুন</span>
            </button>
          </div>
        </div>

        {/* Touch-Friendly Swiper Horizontal Year & Board Selector */}
        <BoardYearSwiper
          years={years}
          selectedYear={selectedYear}
          onSelectYear={setSelectedYear}
          boards={boards}
          selectedBoard={selectedBoard}
          onSelectBoard={setSelectedBoard}
        />

        {/* Search & Multi-Criteria Selectors */}
        <div className="bg-white dark:bg-[#0F172A] p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 shadow-sm space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {/* Search Input */}
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="প্রশ্ন, অধ্যায় বা টপিক খুঁজুন..."
                className="w-full pl-9 pr-3 py-2 text-xs font-bengali bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-amber-400 text-slate-900 dark:text-white placeholder-slate-400"
              />
            </div>

            {/* Level Selector */}
            <select
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value)}
              className="w-full px-3 py-2 text-xs font-bengali bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-amber-400 text-slate-900 dark:text-white"
            >
              <option value="all">সকল স্তর (SSC ও HSC)</option>
              <option value="HSC">এইচএসসি (HSC)</option>
              <option value="SSC">এসএসসি (SSC)</option>
            </select>

            {/* Subject Selector */}
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full px-3 py-2 text-xs font-bengali bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-amber-400 text-slate-900 dark:text-white"
            >
              {subjects.map((s) => (
                <option key={s.key} value={s.key}>
                  {s.label_bn}
                </option>
              ))}
            </select>

            {/* Year Selector */}
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
              className="w-full px-3 py-2 text-xs font-bengali bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-amber-400 text-slate-900 dark:text-white"
            >
              {years.map((y) => (
                <option key={y} value={y}>
                  {y === 'all' ? 'সকল সাল (২০১৫-২০২৫)' : `${y} সাল`}
                </option>
              ))}
            </select>
          </div>

          {/* Board Selector Chips */}
          <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center gap-1.5">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mr-1">
              বোর্ড:
            </span>
            {boards.map((b) => (
              <button
                key={b.key}
                type="button"
                onClick={() => setSelectedBoard(b.key)}
                className={`px-2.5 py-1 rounded-lg text-xs font-bengali transition-all duration-100 ${
                  selectedBoard === b.key
                    ? 'bg-[#0A2540] text-white font-semibold shadow-[0_2px_0_0_#051329]'
                    : 'bg-slate-100 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                }`}
              >
                {b.label_bn}
              </button>
            ))}

            {/* Question Type Filter Chips */}
            <div className="ml-auto flex items-center gap-1">
              {['all', 'CQ', 'MCQ'].map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setSelectedType(t)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-bengali font-semibold transition-all duration-100 ${
                    selectedType === t
                      ? 'bg-amber-600 text-white shadow-[0_2px_0_0_#B45309]'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
                  }`}
                >
                  {t === 'all' ? 'সকল ধরন' : t === 'CQ' ? 'সৃজনশীল (CQ)' : 'বহুনির্বাচনি (MCQ)'}
                </button>
              ))}

              <button
                type="button"
                onClick={handleResetFilters}
                className="px-2 py-1 text-xs text-slate-500 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400 font-bengali flex items-center gap-1 ml-2"
                title="ফিল্টার রিসেট করুন"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">রিসেট</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          AUTHENTIC NCTB EXAMINATION PAPER LAYOUT (Visible in Web & Print)
         ========================================================================= */}
      <div className="bg-[#FAFAF8] dark:bg-[#0B132B] border-2 border-slate-300 dark:border-slate-700/80 rounded-3xl p-6 sm:p-10 shadow-lg relative overflow-hidden print:p-0 print:border-none print:shadow-none print:bg-white text-slate-900 dark:text-slate-100">
        
        {/* Authentic Board Paper Header Banner */}
        <header className="border-b-2 border-slate-800 dark:border-slate-200 pb-6 mb-8 text-center relative">
          {/* Authentic Vector Seal Emblem */}
          <div className="flex justify-center mb-3">
            <div className="w-16 h-16 rounded-full border-2 border-[#0A2540] dark:border-amber-400 flex items-center justify-center p-1 bg-white dark:bg-slate-900 shadow-sm">
              <div className="w-full h-full rounded-full border border-dashed border-[#0A2540] dark:border-amber-400 flex flex-col items-center justify-center text-center">
                <Award className="w-6 h-6 text-[#0A2540] dark:text-amber-400" />
                <span className="text-[8px] font-bold tracking-tighter text-[#0A2540] dark:text-amber-300 uppercase font-display">
                  NCTB
                </span>
              </div>
            </div>
          </div>

          <h2 className="text-xl sm:text-2xl font-bold font-bengali text-slate-900 dark:text-white tracking-wide">
            {selectedBoard === 'all'
              ? 'মাধ্যমিক ও উচ্চ মাধ্যমিক শিক্ষা বোর্ড'
              : `মাধ্যমিক ও উচ্চ মাধ্যমিক শিক্ষা বোর্ড, ${boards.find((b) => b.key === selectedBoard)?.label_bn || selectedBoard}`}
          </h2>
          <p className="text-sm font-semibold font-bengali text-slate-700 dark:text-slate-300 mt-1">
            {selectedLevel === 'SSC'
              ? 'মাধ্যমিক স্কুল সার্টিফিকেট পরীক্ষা (SSC)'
              : selectedLevel === 'HSC'
              ? 'উচ্চ মাধ্যমিক সার্টিফিকেট পরীক্ষা (HSC)'
              : 'অফিসিয়াল বোর্ড সমাপনী পরীক্ষা আর্কাইভ'}
            {selectedYear !== 'all' ? ` — ${selectedYear}` : ' (২০১৫-২০২৫)'}
          </p>

          <div className="mt-3 flex flex-wrap items-center justify-center gap-x-6 gap-y-1 text-xs font-semibold font-bengali text-slate-600 dark:text-slate-400">
            <span>
              বিষয়:{' '}
              <strong className="text-slate-900 dark:text-white">
                {selectedSubject === 'all' ? 'বিজ্ঞান ও মানবিক বিভাগ' : subjects.find((s) => s.key === selectedSubject)?.label_bn}
              </strong>
            </span>
            <span className="hidden sm:inline">|</span>
            <span>সময়: ২ ঘণ্টা ৩০ মিনিট (সৃজনশীল) / ২৫ মিনিট (MCQ)</span>
            <span className="hidden sm:inline">|</span>
            <span>পূর্ণমান: ৫০ / ২৫</span>
          </div>

          {/* NCTB Formal Student Direction Note */}
          <div className="mt-4 pt-3 border-t border-slate-300 dark:border-slate-700 flex items-center justify-between text-[11px] font-bengali italic text-slate-600 dark:text-slate-400">
            <span>[বিশেষ দ্রষ্টব্য: ডান পাশের সংখ্যা প্রশ্নের পূর্ণমান জ্ঞাপন করে।]</span>
            <span>নথি সংকলন: অগ্রযাত্রা একাডেমিক সেল</span>
          </div>
        </header>

        {/* =========================================================================
            QUESTIONS STREAM
           ========================================================================= */}
        {filteredQuestions.length === 0 ? (
          <EmptyState
            variant="academic"
            title="কোনো প্রশ্ন পাওয়া যায়নি"
            description="আপনার নির্বাচিত ফিল্টারে কোনো সংরক্ষিত প্রশ্ন নেই। ফিল্টার রিসেট করে আবার চেষ্টা করুন।"
            actionLabel="সকল ফিল্টার রিসেট করুন"
            onAction={handleResetFilters}
          />
        ) : (
          <div className="space-y-10">
            {filteredQuestions.map((q, index) => {
              const isSolutionOpen = mode === 'study' || expandedSolutions[q.id];

              return (
                <article
                  key={q.id}
                  id={q.id}
                  className="pb-8 border-b border-slate-200 dark:border-slate-800 last:border-b-0 space-y-4 break-inside-avoid"
                >
                  {/* Question Meta Badge Bar */}
                  <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-bengali text-slate-500 dark:text-slate-400">
                    <div className="flex items-center gap-2">
                      <span className="w-7 h-7 rounded-lg bg-[#0A2540] text-white flex items-center justify-center font-bold text-xs font-display">
                        {index + 1}
                      </span>
                      <span className="px-2.5 py-0.5 rounded-md bg-slate-200/80 dark:bg-slate-800 font-semibold text-slate-800 dark:text-slate-200">
                        {q.board_bn} {q.year}
                      </span>
                      <span className="px-2 py-0.5 rounded-md bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 font-medium">
                        {q.subject_bn} ({q.paper} পত্র)
                      </span>
                      <span className="text-slate-400 hidden sm:inline">•</span>
                      <span className="text-slate-600 dark:text-slate-400 hidden sm:inline">
                        অধ্যায়: {q.chapter}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-700 dark:text-slate-300">
                        [পূর্ণমান: {q.marks_total}]
                      </span>
                      {mode === 'exam' && (
                        <button
                          type="button"
                          onClick={() => toggleSolution(q.id)}
                          className="print:hidden text-xs text-[#0A2540] dark:text-amber-400 hover:underline flex items-center gap-1 font-semibold ml-2"
                        >
                          {isSolutionOpen ? (
                            <>
                              <ChevronUp className="w-3.5 h-3.5" />
                              <span>সমাধান বন্ধ</span>
                            </>
                          ) : (
                            <>
                              <ChevronDown className="w-3.5 h-3.5" />
                              <span>সমাধান দেখুন</span>
                            </>
                          )}
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Question Stem / Context with KaTeX Formulas */}
                  <div className="bg-white/70 dark:bg-slate-900/50 p-4 sm:p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800 text-slate-800 dark:text-slate-100 leading-relaxed font-bengali text-sm sm:text-base">
                    <KaTeXRenderer content={q.stem_bn} />
                  </div>

                  {/* -------------------------------------------------------------
                      CASE A: CREATIVE QUESTION (CQ - ৪ স্তরীয় সৃজনশীল প্রশ্ন)
                     ------------------------------------------------------------- */}
                  {q.question_type === 'CQ' && q.cq_sub_questions && (
                    <div className="space-y-4 pl-2 sm:pl-4">
                      {(['ka', 'kha', 'ga', 'gha'] as const).map((partKey) => {
                        const sub = q.cq_sub_questions![partKey];
                        return (
                          <div key={partKey} className="space-y-2">
                            {/* Sub-question Header & Text */}
                            <div className="flex items-start justify-between gap-3 font-bengali text-sm sm:text-base">
                              <div className="flex items-start gap-2 text-slate-900 dark:text-white">
                                <span className="font-bold text-[#0A2540] dark:text-amber-400 min-w-[24px]">
                                  {sub.label}
                                </span>
                                <div className="leading-relaxed">
                                  <KaTeXRenderer content={sub.question_bn} />
                                </div>
                              </div>
                              <span className="font-bold text-slate-600 dark:text-slate-400 text-xs min-w-[20px] text-right">
                                {sub.marks}
                              </span>
                            </div>

                            {/* Step-by-step Solution in Study Mode */}
                            {isSolutionOpen && (
                              <div className="ml-6 sm:ml-8 mt-2 p-4 rounded-xl bg-amber-50/60 dark:bg-slate-900/90 border border-amber-200/70 dark:border-slate-800 text-xs sm:text-sm font-bengali space-y-2">
                                <div className="flex items-center justify-between text-[11px] font-semibold text-amber-900 dark:text-amber-300">
                                  <span className="flex items-center gap-1.5">
                                    <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                                    <span>অফিসিয়াল সমাধান ({sub.type})</span>
                                  </span>
                                  <span className="px-2 py-0.5 rounded bg-amber-200/60 dark:bg-amber-950/80 text-amber-900 dark:text-amber-200 font-display">
                                    মান বণ্টন: {sub.rubric_bn}
                                  </span>
                                </div>
                                <div className="text-slate-800 dark:text-slate-200 leading-relaxed font-bengali whitespace-pre-line">
                                  <KaTeXRenderer content={sub.solution_bn} />
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* -------------------------------------------------------------
                      CASE B: MULTIPLE CHOICE QUESTION (MCQ - বহুনির্বাচনি প্রশ্ন)
                     ------------------------------------------------------------- */}
                  {q.question_type === 'MCQ' && q.options && (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                        {q.options.map((opt) => {
                          const isSelected = userSelectedOptions[q.id] === opt.key;
                          const showCorrect = isSolutionOpen && opt.is_correct;
                          const showWrong = isSolutionOpen && isSelected && !opt.is_correct;

                          return (
                            <button
                              key={opt.key}
                              type="button"
                              onClick={() => handleOptionSelect(q.id, opt.key)}
                              className={`p-3 rounded-xl border text-left font-bengali text-xs sm:text-sm flex items-center justify-between gap-3 transition-all ${
                                showCorrect
                                  ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-500 text-emerald-950 dark:text-emerald-100 font-semibold'
                                  : showWrong
                                  ? 'bg-red-50 dark:bg-red-950/40 border-red-400 text-red-900 dark:text-red-200'
                                  : isSelected
                                  ? 'bg-blue-50 dark:bg-blue-950/40 border-[#0A2540] dark:border-blue-400 text-[#0A2540] dark:text-white font-semibold'
                                  : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:border-slate-400'
                              }`}
                            >
                              <div className="flex items-center gap-2.5">
                                <span
                                  className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                                    showCorrect
                                      ? 'bg-emerald-600 text-white'
                                      : isSelected
                                      ? 'bg-[#0A2540] text-white'
                                      : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                                  }`}
                                >
                                  {opt.key}
                                </span>
                                <div>
                                  <KaTeXRenderer content={opt.text_bn} />
                                </div>
                              </div>
                              {showCorrect && <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />}
                            </button>
                          );
                        })}
                      </div>

                      {/* Detailed MCQ Step-by-Step KaTeX Explanation */}
                      {isSolutionOpen && q.explanation_bn && (
                        <div className="p-4 rounded-xl bg-emerald-50/50 dark:bg-slate-900/90 border border-emerald-200/70 dark:border-slate-800 text-xs sm:text-sm font-bengali space-y-1.5">
                          <div className="flex items-center gap-1.5 font-bold text-emerald-900 dark:text-emerald-300">
                            <CheckCircle className="w-4 h-4 text-emerald-600" />
                            <span>সঠিক উত্তর: ({q.correct_option_key}) | ব্যাখ্যা ও বিশ্লেষণ</span>
                          </div>
                          <div className="text-slate-700 dark:text-slate-300 leading-relaxed">
                            <KaTeXRenderer content={q.explanation_bn} />
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Cryptographic Content Verification Footnote */}
                  <div className="pt-2 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                    <span>ID: {q.id}</span>
                    <span>SHA-256: {q.content_hash} (NCTB Verified)</span>
                  </div>
                </article>
              );
            })}
          </div>
        )}

        {/* Examination Paper Footer */}
        <footer className="mt-12 pt-6 border-t-2 border-slate-800 dark:border-slate-200 flex flex-col sm:flex-row items-center justify-between text-xs font-bengali text-slate-500 gap-2 text-center sm:text-left">
          <span>জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত পাঠ্যক্রম অনুযায়ী মুদ্রিত</span>
          <span className="font-display font-semibold">Ogrojatra Digital Examination Archives &copy; 2026</span>
        </footer>
      </div>
    </div>
  );
};
