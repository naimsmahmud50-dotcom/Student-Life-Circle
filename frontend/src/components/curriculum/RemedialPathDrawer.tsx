/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Remedial Path Drawer Component
 * TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
 * FILE:      frontend/src/components/curriculum/RemedialPathDrawer.tsx
 * PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
 * PURPOSE:   Provides slide-over pedagogical recovery drawer delivering a structured
 *            3-step remedial pathway (Refresher, Guided Example, Mastery Drill)
 *            with KaTeX mathematical equations and tactile 3D action buttons.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState } from 'react';
import {
  X,
  Clock,
  BookOpen,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Layers,
  Lightbulb,
  FileCheck2,
  ChevronRight,
  Play
} from 'lucide-react';
import { KaTeXRenderer } from '../quiz/katex-renderer';

export interface RemedialStep {
  step_number: number;
  step_name_bn: string;
  duration_minutes: number;
  pedagogy_focus: string;
  summary_bn?: string;
  formula_highlight?: string;
  problem_bn?: string;
  solution_steps?: string[];
  drill_questions_count?: number;
}

export interface RemedialPathwayData {
  target_topic_id: string;
  target_title_bn: string;
  subject: string;
  class_grade: number;
  total_duration_minutes: number;
  detected_gaps_count: number;
  primary_gap?: {
    topic_id: string;
    title_bn: string;
    class_grade: number;
    current_mastery: number;
    core_formulas?: string[];
  } | null;
  steps: RemedialStep[];
}

export interface RemedialPathDrawerProps {
  isOpen: boolean;
  topicId: string;
  onClose: () => void;
  onStartRemedialLesson?: (topicId: string) => void;
  pathwayData?: RemedialPathwayData;
}

const DEFAULT_PATHWAY: RemedialPathwayData = {
  target_topic_id: 'math-hsc-differentiation',
  target_title_bn: 'অন্তরীকরণ ও তাৎক্ষণিক পরিবর্তনের হার',
  subject: 'উচ্চতর গণিত ১ম পত্র',
  class_grade: 11,
  total_duration_minutes: 15,
  detected_gaps_count: 1,
  primary_gap: {
    topic_id: 'math-cl9-trigonometric-ratios',
    title_bn: 'ত্রিকোণমিতিক অনুপাত ও অভেদাবলী',
    class_grade: 9,
    current_mastery: 0.45,
    core_formulas: ['\\sin^2\\theta + \\cos^2\\theta = 1', '\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}'],
  },
  steps: [
    {
      step_number: 1,
      step_name_bn: 'সংক্ষিপ্ত মৌলিক ধারণা পুনশ্চরণ (Concept Refresher)',
      duration_minutes: 5,
      pedagogy_focus: 'পূর্বশর্ত ও মূল ধারণার সংযোগ',
      summary_bn: 'অন্তরীকরণ বোঝার জন্য পরিবর্তন হার এবং সীমার ($\lim$) অর্থ অনুধাবন করা আবশ্যক। এখানে শ্রেণি ৯ম ত্রিকোণমিতিক রূপান্তরসমূহের সংযোগ প্রধান চাবিকাঠি।',
      formula_highlight: 'f\'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}',
    },
    {
      step_number: 2,
      step_name_bn: 'ধাপে ধাপে নির্দেশিত সমাধান (Guided Worked Example)',
      duration_minutes: 5,
      pedagogy_focus: 'বাস্তব সমস্যার ধাপে ধাপে গাণিতিক প্রয়োগ',
      problem_bn: 'মূল নিয়মে $f(x) = \\sin x$ এর অন্তরজ নির্ণয় করো।',
      solution_steps: [
        '১. সূত্র স্থাপন: $f\'(x) = \\lim_{h \\to 0} \\frac{\\sin(x+h) - \\sin x}{h}$',
        '২. ত্রিকোণমিতিক অভেদ প্রয়োগ: $\\sin C - \\sin D = 2\\cos\\frac{C+D}{2}\\sin\\frac{C-D}{2}$',
        '৩. সীমা বিভাজন ও মান নির্ণয়: $\\lim_{h \\to 0} \\cos(x + \\frac{h}{2}) \\times \\lim_{h \\to 0} \\frac{\\sin(h/2)}{h/2} = \\cos x \\times 1 = \\cos x$',
      ],
    },
    {
      step_number: 3,
      step_name_bn: 'দক্ষতা যাচাই ড্রিল (Mastery Diagnostic Drill)',
      duration_minutes: 5,
      pedagogy_focus: '৩টি দ্রুত নির্ণায়ক প্রশ্নের মাধ্যমে দক্ষতা নিশ্চিতকরণ',
      drill_questions_count: 3,
    },
  ],
};

export const RemedialPathDrawer: React.FC<RemedialPathDrawerProps> = ({
  isOpen,
  topicId,
  onClose,
  onStartRemedialLesson,
  pathwayData = DEFAULT_PATHWAY,
}) => {
  const [activeStepTab, setActiveStepTab] = useState<number>(1);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden font-sans">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-[#0A2540]/30 backdrop-blur-xs transition-opacity"
      />

      {/* Slide-over panel */}
      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-xl bg-white border-l border-slate-200 shadow-2xl flex flex-col justify-between">
          {/* Top Bar */}
          <div>
            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-xs">
                  <BookOpen className="w-5 h-5 stroke-[1.75]" />
                </div>
                <div>
                  <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    <span>{pathwayData.subject}</span>
                    <span className="text-slate-300">•</span>
                    <span>শ্রেণি {pathwayData.class_grade}</span>
                  </div>
                  <h2 className="text-base font-bold text-[#0A2540] tracking-tight">
                    {pathwayData.target_title_bn}
                  </h2>
                </div>
              </div>

              <button
                onClick={onClose}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
                title="বন্ধ করুন"
                aria-label="বন্ধ করুন"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Content Body */}
            <div className="p-6 space-y-6 max-h-[calc(100vh-210px)] overflow-y-auto">
              {/* Prerequisite Gap Alert Card */}
              {pathwayData.primary_gap && (
                <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200/90 text-xs text-amber-950 space-y-1.5">
                  <div className="flex items-center gap-1.5 font-bold text-amber-900">
                    <AlertCircle className="w-4 h-4 text-amber-700" />
                    <span>চিহ্নিত পূর্বশর্ত ঘাটতি (Foundational Gap)</span>
                  </div>
                  <p className="text-slate-700 leading-relaxed">
                    এই অধ্যায়ের জটিলতা দূর করতে তোমার পূর্ববর্তী ভিত্তি{' '}
                    <strong className="text-amber-950 font-bold">
                      ‘{pathwayData.primary_gap.title_bn}’ (শ্রেণি {pathwayData.primary_gap.class_grade})
                    </strong>{' '}
                    এর পুনশ্চরণ প্রয়োজন (বর্তমান অর্জিত দক্ষতা: {Math.round(pathwayData.primary_gap.current_mastery * 100)}%)।
                  </p>
                </div>
              )}

              {/* 3-Step Remedial Overview Banner */}
              <div className="flex items-center justify-between p-4 bg-[#FAFAF8] border border-slate-200 rounded-2xl">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-emerald-700" />
                  <span className="text-xs font-bold text-slate-800">
                    ১৫ মিনিটের কার্যকর পুনরুদ্ধার পাঠ (15-Min Recovery)
                  </span>
                </div>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200">
                  ৩টি ধাপে বিন্যস্ত
                </span>
              </div>

              {/* Step Navigation Tabs */}
              <div className="grid grid-cols-3 gap-2">
                {pathwayData.steps.map((st) => (
                  <button
                    key={st.step_number}
                    onClick={() => setActiveStepTab(st.step_number)}
                    className={`p-3 rounded-2xl border text-left transition-all ${
                      activeStepTab === st.step_number
                        ? 'bg-[#0A2540] text-white border-[#0A2540] shadow-xs'
                        : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    <div className="text-[10px] uppercase font-bold opacity-75">
                      ধাপ {st.step_number} ({st.duration_minutes} মিনিট)
                    </div>
                    <div className="text-xs font-bold truncate mt-0.5">
                      {st.step_number === 1
                        ? 'মৌলিক পুনশ্চরণ'
                        : st.step_number === 2
                        ? 'নির্দেশিত সমাধান'
                        : 'দক্ষতা ড্রিল'}
                    </div>
                  </button>
                ))}
              </div>

              {/* Active Step Detailed Content Card */}
              {(() => {
                const currentStep =
                  pathwayData.steps.find((s) => s.step_number === activeStepTab) ||
                  pathwayData.steps[0];

                return (
                  <div className="bg-[#FAFAF8] border border-slate-200 rounded-2xl p-5 space-y-4">
                    <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                      <span className="text-xs font-bold text-[#0A2540] uppercase tracking-wider">
                        {currentStep.step_name_bn}
                      </span>
                      <span className="text-xs font-semibold text-slate-500 flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" /> {currentStep.duration_minutes} মিনিট
                      </span>
                    </div>

                    {/* Step 1 Content */}
                    {currentStep.step_number === 1 && (
                      <div className="space-y-3 text-sm text-slate-800 leading-relaxed">
                        <p>{currentStep.summary_bn}</p>
                        {currentStep.formula_highlight && (
                          <div className="p-3.5 bg-white border border-slate-200 rounded-xl text-center shadow-xs">
                            <span className="text-xs font-semibold text-slate-500 block mb-1">
                              প্রধান সমীকরণ ভিত্তি:
                            </span>
                            <div className="text-base text-[#0A2540]">
                              <KaTeXRenderer content={currentStep.formula_highlight} />
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Step 2 Content */}
                    {currentStep.step_number === 2 && (
                      <div className="space-y-3 text-sm text-slate-800">
                        <div className="font-semibold text-slate-900 pb-2 border-b border-slate-200">
                          {currentStep.problem_bn}
                        </div>
                        <div className="space-y-2 text-xs text-slate-700">
                          {currentStep.solution_steps?.map((stepStr, idx) => (
                            <div key={idx} className="p-2.5 bg-white border border-slate-200 rounded-xl">
                              <KaTeXRenderer content={stepStr} />
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Step 3 Content */}
                    {currentStep.step_number === 3 && (
                      <div className="space-y-3 text-xs text-slate-700">
                        <div className="p-3 bg-white border border-slate-200 rounded-xl">
                          <span className="font-bold text-slate-900 block mb-1">
                            দ্রুত নির্ণায়ক পরীক্ষা:
                          </span>
                          <span>
                            ৩টি প্রশ্ন সমাধান করে তাৎক্ষণিক ৮০% স্কোর অর্জন করলে এই অধ্যায়ের ঘাটতি দূরীভূত হবে।
                          </span>
                        </div>
                        <div className="flex items-center gap-2 text-emerald-800 font-semibold">
                          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                          <span>স্বয়ংক্রিয় প্রগ্রেস আপডেট ও মাস্টার্ড ব্যাজ প্রদান</span>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })()}
            </div>
          </div>

          {/* Bottom Tactile Action Drawer Footer */}
          <div className="p-6 border-t border-slate-200 bg-white flex items-center justify-between gap-4">
            <button
              onClick={onClose}
              className="py-3 px-4 rounded-xl border border-slate-200 text-slate-700 text-xs sm:text-sm font-semibold hover:bg-slate-50 transition-all"
            >
              পরে করবো
            </button>

            {/* 3D Tactile Emerald Action Button */}
            <button
              onClick={() => {
                if (onStartRemedialLesson) {
                  onStartRemedialLesson(pathwayData.target_topic_id);
                }
              }}
              className="flex-1 py-3 px-6 rounded-2xl bg-emerald-800 text-white text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#065F46] active:translate-y-1 active:shadow-none hover:bg-emerald-900 transition-all flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4 fill-white stroke-none" />
              <span>প্রতিকারমূলক পাঠ শুরু করো</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
