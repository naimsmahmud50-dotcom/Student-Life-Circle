/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Quiz Interface - Accessible Option Card Component
 * TOPIC:     48px Touch Target, Keyboard Binding (1-4 / A-D), Dual Light/Dark Modes
 * FILE:      frontend/src/components/quiz/option-card.tsx
 * PURPOSE:   Renders an interactive multiple-choice question option. Enforces 48px
 *            minimum touch heights for budget smartphones, accessible keyboard
 *            interaction (pressing 1, 2, 3, 4 or A, B, C, D selects the option),
 *            prominent focus rings, and clear visual state transitions across both
 *            White and Dark modes. Integrates KaTeXRenderer for mathematical formula rendering.
 * AUDIENCE:  Frontend Developers, Accessibility Reviewers & AI Agents
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA (Target Size & Focus), Zero-Emoji
 * ========================================================================================
 */

import React, { useEffect } from 'react';
import { KaTeXRenderer } from './katex-renderer';

export interface OptionCardProps {
  id?: string;
  optionKey?: 'A' | 'B' | 'C' | 'D';
  label?: 'A' | 'B' | 'C' | 'D';
  shortcutNumber?: 1 | 2 | 3 | 4;
  shortcutKey?: 1 | 2 | 3 | 4;
  textBn?: string;
  text?: string;
  textEn?: string;
  isSelected: boolean;
  isCorrect?: boolean;
  onSelect: (optionId: string) => void;
  disabled?: boolean;
}

export const OptionCard: React.FC<OptionCardProps> = ({
  id = '',
  optionKey: propOptionKey,
  label,
  shortcutNumber: propShortcutNumber,
  shortcutKey,
  textBn: propTextBn,
  text,
  textEn,
  isSelected,
  isCorrect,
  onSelect,
  disabled = false
}) => {
  const optionKey = propOptionKey ?? label ?? 'A';
  const shortcutNumber = propShortcutNumber ?? shortcutKey ?? 1;
  const textBn = propTextBn ?? text ?? '';

  // Keyboard shortcut listener for fast answering
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (disabled) return;
      // Match number key (1-4) or letter key (A-D)
      if (e.key === String(shortcutNumber) || e.key.toUpperCase() === optionKey) {
        onSelect(id);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [disabled, id, onSelect, optionKey, shortcutNumber]);

  return (
    <div
      role="button"
      aria-pressed={isSelected}
      aria-checked={isSelected}
      tabIndex={disabled ? -1 : 0}
      onClick={() => !disabled && onSelect(id)}
      onKeyDown={(e) => {
        if (!disabled && (e.key === ' ' || e.key === 'Enter')) {
          e.preventDefault();
          onSelect(id);
        }
      }}
      className={`
        group relative flex items-center justify-between p-4 my-2.5 rounded-xl border-2 transition-all duration-150 cursor-pointer select-none min-h-[52px]
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--focus-ring)] focus-visible:ring-offset-2
        ${isSelected 
          ? "border-[var(--color-brand)] bg-[var(--color-brand-subtle)] shadow-sm" 
          : "border-[var(--border-subtle)] bg-[var(--bg-surface)] hover:bg-[var(--bg-surface-elevated)] hover:border-[var(--border-strong)]"
        }
        ${disabled ? "opacity-60 cursor-not-allowed" : "active:scale-[0.99]"}
      `}
    >
      <div className="flex items-center space-x-3.5 pr-4">
        {/* Key Badge: A, B, C, D */}
        <span
          className={`
            inline-flex items-center justify-center w-8 h-8 rounded-lg text-sm font-semibold tracking-wider transition-colors
            ${isSelected 
              ? "bg-[var(--color-brand)] text-[var(--color-brand-contrast)]" 
              : "bg-[var(--bg-surface-elevated)] text-[var(--text-muted)] group-hover:text-[var(--text-main)]"
            }
          `}
        >
          {optionKey}
        </span>

        {/* Option Text */}
        <div className="flex flex-col">
          <span className={`text-base font-normal leading-relaxed ${isSelected ? "font-medium text-[var(--text-main)]" : "text-[var(--text-main)]"}`}>
            <KaTeXRenderer content={textBn} />
          </span>
          {textEn && (
            <span className="text-xs text-[var(--text-muted)] mt-0.5">
              <KaTeXRenderer content={textEn} />
            </span>
          )}
        </div>
      </div>

      {/* Keyboard Shortcut Indicator & Selection State */}
      <div className="flex items-center space-x-2">
        <span 
          title={`কীবোর্ড শর্টকাট: ${shortcutNumber}`}
          className="hidden sm:inline-block px-2 py-0.5 text-xs text-[var(--text-subtle)] bg-[var(--bg-surface-elevated)] rounded border border-[var(--border-subtle)] font-mono"
        >
          [{shortcutNumber}]
        </span>

        {/* Clean Radio Indicator SVG (Strict Zero Emoji) */}
        <div
          className={`
            w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors
            ${isSelected ? "border-[var(--color-brand)] bg-[var(--color-brand)]" : "border-[var(--border-strong)] bg-transparent"}
          `}
        >
          {isSelected && (
            <div className="w-2 h-2 rounded-full bg-white" />
          )}
        </div>
      </div>
    </div>
  );
};
