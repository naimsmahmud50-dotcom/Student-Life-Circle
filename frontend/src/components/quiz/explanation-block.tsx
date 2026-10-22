/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Quiz Interface - Step-by-Step Explanation Component
 * TOPIC:     Academic Solution Derivation, KaTeX Formula Rendering & Textbook Reference
 * FILE:      frontend/src/components/quiz/explanation-block.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides textbook-like step-by-step solution explanations with full KaTeX
 *            mathematical typography, official board citation tags, and clean hairline layout.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React from 'react';
import { BookOpen, CheckCircle2, Bookmark } from 'lucide-react';
import { cn } from '@/lib/utils';
import { KaTeXRenderer } from './katex-renderer';

export interface ExplanationBlockProps {
  explanationBn: string;
  explanationEn?: string;
  sourceAttribution?: string;
  correctOptionKey?: string;
  correctOptionText?: string;
  keyFormula?: string;
  isBengali?: boolean;
  className?: string;
}

export const ExplanationBlock: React.FC<ExplanationBlockProps> = ({
  explanationBn,
  explanationEn,
  sourceAttribution,
  correctOptionKey,
  correctOptionText,
  keyFormula,
  isBengali = true,
  className,
}) => {
  return (
    <div
      className={cn(
        "rounded-2xl border border-[#E5E2DA] dark:border-[#262D3D] bg-[#FAF8F3] dark:bg-[#0E1526] p-5 sm:p-6 space-y-4 shadow-sm",
        className
      )}
    >
      {/* Header Deck */}
      <div className="flex items-center justify-between flex-wrap gap-2 pb-3 border-b border-[#E5E2DA] dark:border-[#262D3D]">
        <div className="inline-flex items-center gap-2 text-xs font-semibold text-[#0B5D3B] dark:text-emerald-400">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{isBengali ? "বিশদ সমাধান ও পাঠ্যবই সূত্র" : "Detailed Solution & Derivation"}</span>
        </div>

        {sourceAttribution && (
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] text-[11px] text-[#5B5B5B] dark:text-slate-400 font-sans">
            <Bookmark className="w-3 h-3 text-[#B8862B]" />
            <span>{sourceAttribution}</span>
          </div>
        )}
      </div>

      {/* Correct Option Highlight */}
      {(correctOptionKey || correctOptionText) && (
        <div className="p-3 rounded-xl bg-white dark:bg-[#121B2D] border border-[#C8E3D7] dark:border-emerald-900 text-xs sm:text-sm font-sans flex items-start gap-2.5">
          <span className="font-bold text-[#0B5D3B] dark:text-emerald-400 shrink-0">
            {isBengali ? "সঠিক উত্তর:" : "Correct Answer:"}
          </span>
          <div className="text-[#1A1A1A] dark:text-[#F5F2EB]">
            {correctOptionKey && <span className="font-bold mr-1.5">({correctOptionKey})</span>}
            {correctOptionText && <KaTeXRenderer content={correctOptionText} />}
          </div>
        </div>
      )}

      {/* Key Formula Box */}
      {keyFormula && (
        <div className="p-3.5 rounded-xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] space-y-1.5">
          <span className="text-[11px] font-semibold text-[#5B5B5B] dark:text-slate-400 uppercase tracking-wider block">
            {isBengali ? "প্রয়োজনীয় গাণিতিক সূত্র" : "Governing Equation"}
          </span>
          <div className="text-[#1B2A4A] dark:text-[#F5F2EB] pt-1">
            <KaTeXRenderer content={keyFormula} block />
          </div>
        </div>
      )}

      {/* Step by step derivation prose */}
      <div className="space-y-2 text-xs sm:text-sm text-[#1A1A1A] dark:text-slate-200 leading-relaxed font-sans">
        <KaTeXRenderer content={explanationBn} block />

        {!isBengali && explanationEn && (
          <div className="pt-2 text-xs text-[#5B5B5B] dark:text-slate-400 border-t border-[#E5E2DA] dark:border-[#262D3D]">
            <KaTeXRenderer content={explanationEn} block />
          </div>
        )}
      </div>
    </div>
  );
};
