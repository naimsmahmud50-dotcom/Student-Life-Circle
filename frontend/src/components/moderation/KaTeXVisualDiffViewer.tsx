/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    KaTeX Visual Diff Viewer Component
 * TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
 * FILE:      frontend/src/components/moderation/KaTeXVisualDiffViewer.tsx
 * PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
 * PURPOSE:   Provides side-by-side and unified mathematical formula diffing for
 *            editorial review committees, rendering LaTeX equations with KaTeX and
 *            highlighting additions in emerald and deletions in rose hairlines.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState } from 'react';
import {
  Columns,
  Layers,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  BookOpen,
  FileText,
  Split,
  Eye
} from 'lucide-react';
import { KaTeXRenderer } from '../quiz/katex-renderer';

export interface DiffOption {
  key: string;
  text: string;
  is_correct?: boolean;
  explanation?: string;
}

export interface KaTeXVisualDiffViewerProps {
  originalStem: string;
  revisedStem: string;
  originalOptions?: DiffOption[];
  revisedOptions?: DiffOption[];
  originalVersion?: number;
  revisedVersion?: number;
  subject?: string;
  topic?: string;
}

export const KaTeXVisualDiffViewer: React.FC<KaTeXVisualDiffViewerProps> = ({
  originalStem,
  revisedStem,
  originalOptions = [],
  revisedOptions = [],
  originalVersion = 1,
  revisedVersion = 2,
  subject = 'পদার্থবিজ্ঞান ১ম পত্র',
  topic = 'নিউটনীয় বলবিদ্যা',
}) => {
  const [viewMode, setViewMode] = useState<'SIDE_BY_SIDE' | 'UNIFIED'>('SIDE_BY_SIDE');

  const hasStemChanged = originalStem.trim() !== revisedStem.trim();

  return (
    <div className="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xs font-sans">
      {/* Diff Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            <span>{subject}</span>
            <span className="text-slate-300">•</span>
            <span>{topic}</span>
          </div>
          <h2 className="text-lg font-bold text-[#0A2540] flex items-center gap-2">
            <Split className="w-5 h-5 text-slate-600 stroke-[1.75]" />
            <span>গাণিতিক সমীকরণ ও প্রশ্নরূপ ভিজ্যুয়াল পার্থক্য (Diff)</span>
          </h2>
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center gap-1.5 p-1 bg-[#FAFAF8] border border-slate-200 rounded-2xl self-start sm:self-auto">
          <button
            onClick={() => setViewMode('SIDE_BY_SIDE')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              viewMode === 'SIDE_BY_SIDE'
                ? 'bg-[#0A2540] text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Columns className="w-3.5 h-3.5" />
            <span>পাশাপাশি তুলনা</span>
          </button>
          <button
            onClick={() => setViewMode('UNIFIED')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              viewMode === 'UNIFIED'
                ? 'bg-[#0A2540] text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>একক বিস্তারিত দৃশ্য</span>
          </button>
        </div>
      </div>

      {/* Stem Comparison */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <FileText className="w-4 h-4" />
            মূল প্রশ্ন বিবৃতি (Question Stem)
          </span>
          {hasStemChanged ? (
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-900 border border-amber-200">
              পরিমার্জন সনাক্ত হয়েছে
            </span>
          ) : (
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-50 text-slate-600 border border-slate-200">
              অপরিবর্তিত
            </span>
          )}
        </div>

        {viewMode === 'SIDE_BY_SIDE' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Original Stem Card */}
            <div className="bg-[#FAFAF8] border border-rose-200/80 rounded-2xl p-5 shadow-xs relative">
              <div className="flex items-center justify-between mb-3 pb-2 border-b border-rose-100">
                <span className="text-xs font-bold text-rose-900 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-rose-500" />
                  পূর্ববর্তী সংস্করণ (v{originalVersion}.0)
                </span>
                <span className="text-xs font-mono text-rose-700 bg-rose-50 px-2 py-0.5 rounded-md">
                  পূর্বরূপ
                </span>
              </div>
              <div className="text-sm text-slate-900 leading-relaxed">
                <KaTeXRenderer content={originalStem} />
              </div>
            </div>

            {/* Revised Stem Card */}
            <div className="bg-[#FAFAF8] border border-emerald-200/80 rounded-2xl p-5 shadow-xs relative">
              <div className="flex items-center justify-between mb-3 pb-2 border-b border-emerald-100">
                <span className="text-xs font-bold text-emerald-900 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                  সংশোধিত সংস্করণ (v{revisedVersion}.0)
                </span>
                <span className="text-xs font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md">
                  প্রস্তাবিত
                </span>
              </div>
              <div className="text-sm text-slate-900 leading-relaxed">
                <KaTeXRenderer content={revisedStem} />
              </div>
            </div>
          </div>
        ) : (
          /* Unified View */
          <div className="space-y-3">
            <div className="p-4 rounded-2xl bg-rose-50/60 border border-rose-200 text-sm text-rose-950">
              <span className="text-xs font-bold text-rose-800 uppercase block mb-1">পূর্ববর্তী খসড়া:</span>
              <KaTeXRenderer content={originalStem} />
            </div>
            <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200 text-sm text-emerald-950">
              <span className="text-xs font-bold text-emerald-800 uppercase block mb-1">সংশোধিত প্রস্তাবনা:</span>
              <KaTeXRenderer content={revisedStem} />
            </div>
          </div>
        )}
      </div>

      {/* Options Comparison Grid */}
      <div>
        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 flex items-center gap-1.5">
          <BookOpen className="w-4 h-4" />
          বিকল্প উত্তর ও ব্যাখ্যা নিরীক্ষণ (Option Comparison)
        </h3>

        <div className="space-y-3">
          {revisedOptions.map((revOpt, idx) => {
            const origOpt = originalOptions[idx] || null;
            const isModified = origOpt ? origOpt.text !== revOpt.text || origOpt.is_correct !== revOpt.is_correct : true;

            return (
              <div
                key={revOpt.key}
                className={`p-4 rounded-2xl border transition-all ${
                  isModified
                    ? 'bg-amber-50/30 border-amber-200'
                    : 'bg-[#FAFAF8] border-slate-200/80'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <div className="flex items-start gap-3 flex-1">
                    <span
                      className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-bold flex-shrink-0 ${
                        revOpt.is_correct
                          ? 'bg-emerald-700 text-white shadow-xs'
                          : 'bg-white text-slate-700 border border-slate-300'
                      }`}
                    >
                      {revOpt.key}
                    </span>

                    <div className="space-y-1.5 flex-1 text-sm">
                      <div className="text-slate-900 font-medium">
                        <KaTeXRenderer content={revOpt.text} />
                      </div>

                      {origOpt && origOpt.text !== revOpt.text && (
                        <div className="text-xs text-rose-700 bg-rose-50 px-2 py-1 rounded-lg border border-rose-100 line-through">
                          পূর্বরূপ: <KaTeXRenderer content={origOpt.text} />
                        </div>
                      )}

                      {revOpt.explanation && (
                        <div className="text-xs text-slate-500 mt-1">
                          <span className="font-semibold text-slate-700">ব্যাখ্যা: </span>
                          <KaTeXRenderer content={revOpt.explanation} />
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Badges */}
                  <div className="flex items-center gap-2 self-end sm:self-center">
                    {revOpt.is_correct && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        সঠিক উত্তর
                      </span>
                    )}
                    {isModified && (
                      <span className="px-2 py-0.5 rounded-md text-xs font-medium bg-amber-100 text-amber-900">
                        সংশোধিত
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
