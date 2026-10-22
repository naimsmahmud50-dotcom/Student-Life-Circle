/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - ACADEMIC QUESTION CARD COMPONENT:
 * MODULE:    Quiz Interface - Full Academic Question Card
 * TOPIC:     KaTeX Mathematical Typography, Scientific Diagrams, High-Contrast Theming
 * FILE:      frontend/src/components/quiz/question-card.tsx
 * PURPOSE:   Provides an authentic, comprehensive question card for exams and practice:
 *            1. Math Formulation: Renders complex NCTB and admission equations via KaTeXRenderer.
 *            2. Diagram Inspection: Integrates ScientificDiagram with multi-touch pinch-to-zoom.
 *            3. Option Interactions: Embeds accessible OptionCard with 48px touch targets.
 *            4. Step-by-Step Derivation: Renders collapsible Bengali explanations with full
 *               mathematical derivations and source attribution.
 *            5. Dual Light/Dark Modes: Seamlessly adapts across White and Dark themes with
 *               WCAG 2.2 AA contrast compliance.
 * AUDIENCE:  Frontend Leads, UX Designers, Accessibility Reviewers & AI Agents
 * STANDARDS: UI/UX Pro Max, NCTB & Admission Blueprints, WCAG 2.2 AA, Zero-Emoji Spec
 * ========================================================================================
 */

import React, { useState } from 'react';
import { OptionCard } from './option-card';
import { KaTeXRenderer } from './katex-renderer';
import { ScientificDiagram } from './scientific-diagram';

export interface QuestionOptionItem {
  key: 'A' | 'B' | 'C' | 'D';
  text_bn: string;
  text_en?: string;
  is_correct?: boolean;
}

export interface QuestionCardProps {
  id: string;
  questionNumber: number;
  totalQuestions?: number;
  subject?: string;
  chapter?: string;
  stemBn: string;
  stemEn?: string;
  diagramSrc?: string;
  diagramAltBn?: string;
  options: QuestionOptionItem[];
  selectedOptionKey?: string | null;
  onSelectOption: (questionId: string, optionKey: 'A' | 'B' | 'C' | 'D') => void;
  difficulty?: 'EASY' | 'MEDIUM' | 'HARD';
  sourceAttribution?: string;
  negativeMarking?: number;
  explanationBn?: string;
  showExplanation?: boolean;
  disabled?: boolean;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  id,
  questionNumber,
  totalQuestions,
  subject,
  chapter,
  stemBn,
  stemEn,
  diagramSrc,
  diagramAltBn,
  options,
  selectedOptionKey,
  onSelectOption,
  difficulty = 'MEDIUM',
  sourceAttribution,
  negativeMarking,
  explanationBn,
  showExplanation = false,
  disabled = false
}) => {
  const [isExplanationOpen, setIsExplanationOpen] = useState(showExplanation);

  // Difficulty badge in Bengali
  const getDifficultyBadge = () => {
    switch (difficulty) {
      case 'EASY':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            সহজ
          </span>
        );
      case 'HARD':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20">
            কঠিন
          </span>
        );
      case 'MEDIUM':
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
            মধ্যম
          </span>
        );
    }
  };

  return (
    <article
      className="w-full max-w-3xl mx-auto my-6 p-5 sm:p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-subtle)] shadow-sm transition-all duration-200"
      aria-labelledby={`q-stem-${id}`}
    >
      {/* Question Header & Metadata Badges */}
      <header className="flex flex-wrap items-center justify-between gap-2.5 pb-4 mb-4 border-b border-[var(--border-subtle)]">
        <div className="flex flex-wrap items-center gap-2">
          {/* Question Index Badge */}
          <span className="inline-flex items-center justify-center px-2.5 py-1 rounded-md text-xs font-bold bg-[var(--color-brand)] text-[var(--color-brand-contrast)]">
            প্রশ্ন {questionNumber}
            {totalQuestions ? ` / ${totalQuestions}` : ''}
          </span>

          {/* Chapter / Topic Tag */}
          {chapter && (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-[var(--bg-surface-elevated)] text-[var(--text-main)] border border-[var(--border-subtle)]">
              {chapter}
            </span>
          )}

          {/* Difficulty Badge */}
          {getDifficultyBadge()}
        </div>

        <div className="flex items-center gap-2 text-xs text-[var(--text-muted)]">
          {/* Negative Marking Badge */}
          {negativeMarking && negativeMarking > 0 && (
            <span className="font-mono font-medium text-rose-500 bg-rose-500/5 px-2 py-0.5 rounded border border-rose-500/15">
              নেগেটিভ: -{negativeMarking}
            </span>
          )}

          {/* Source Board / Admission Reference */}
          {sourceAttribution && (
            <span className="italic font-normal">
              [{sourceAttribution}]
            </span>
          )}
        </div>
      </header>

      {/* Question Stem with KaTeX Equations */}
      <section className="mb-5">
        <h3
          id={`q-stem-${id}`}
          className="text-lg sm:text-xl font-medium leading-relaxed text-[var(--text-main)]"
        >
          <KaTeXRenderer content={stemBn} />
        </h3>

        {stemEn && (
          <p className="mt-1 text-sm text-[var(--text-muted)] italic">
            <KaTeXRenderer content={stemEn} />
          </p>
        )}

        {/* Optional Scientific Diagram with Pinch-to-Zoom */}
        {diagramSrc && (
          <ScientificDiagram
            src={diagramSrc}
            altTextBn={diagramAltBn || 'প্রশ্ন সংক্রান্ত বৈজ্ঞানিক চিত্র'}
          />
        )}
      </section>

      {/* Multiple-Choice Options List */}
      <section
        role="radiogroup"
        aria-label={`প্রশ্ন ${questionNumber} এর উত্তরের বিকল্পসমূহ`}
        className="space-y-2 mb-4"
      >
        {options.map((opt, index) => {
          const shortcutNum = (index + 1) as 1 | 2 | 3 | 4;
          const isSelected = selectedOptionKey === opt.key;
          return (
            <OptionCard
              key={opt.key}
              id={`${id}-opt-${opt.key}`}
              optionKey={opt.key}
              shortcutNumber={shortcutNum}
              textBn={opt.text_bn}
              textEn={opt.text_en}
              isSelected={isSelected}
              onSelect={() => onSelectOption(id, opt.key)}
              disabled={disabled}
            />
          );
        })}
      </section>

      {/* Collapsible Step-by-Step Bengali Explanation Drawer */}
      {explanationBn && (
        <section className="mt-5 pt-4 border-t border-[var(--border-subtle)]">
          <button
            type="button"
            onClick={() => setIsExplanationOpen((prev) => !prev)}
            aria-expanded={isExplanationOpen}
            className="flex items-center justify-between w-full text-left text-sm font-semibold text-[var(--color-brand)] hover:opacity-85 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--focus-ring)] rounded py-1"
          >
            <span>
              {isExplanationOpen ? 'বিস্তারিত সমাধান লুকান' : 'বিস্তারিত সমাধান ও ব্যাখ্যা দেখুন'}
            </span>
            <span className="font-mono text-xs text-[var(--text-muted)]">
              {isExplanationOpen ? '[সংকোচন করুন -]' : '[প্রসারণ করুন +]'}
            </span>
          </button>

          {isExplanationOpen && (
            <div
              className="mt-3 p-4 rounded-xl bg-[var(--bg-surface-elevated)] border border-[var(--border-subtle)] text-[var(--text-main)] text-sm sm:text-base leading-relaxed animate-fadeIn"
            >
              <div className="font-semibold text-xs tracking-wider uppercase text-[var(--text-muted)] mb-2">
                ধাপে ধাপে ব্যাখ্যা ও সূত্র:
              </div>
              <KaTeXRenderer content={explanationBn} block={true} />
            </div>
          )}
        </section>
      )}
    </article>
  );
};
