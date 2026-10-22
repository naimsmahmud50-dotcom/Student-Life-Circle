/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Form Primitives
 * TOPIC:     Modern Academic Editorial Textarea Primitive
 * FILE:      frontend/src/components/ui/textarea.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible, multi-line text input with label, helper text,
 *            character count indicator, inline error validation, and high contrast.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { forwardRef, useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: React.ReactNode;
  helperText?: React.ReactNode;
  error?: string;
  showCount?: boolean;
  fullWidth?: boolean;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      className,
      label,
      helperText,
      error,
      showCount = false,
      maxLength,
      fullWidth = true,
      id,
      disabled,
      value,
      defaultValue,
      onChange,
      rows = 4,
      ...props
    },
    ref
  ) => {
    const [currentLength, setCurrentLength] = useState<number>(() => {
      if (typeof value === 'string') return value.length;
      if (typeof defaultValue === 'string') return defaultValue.length;
      return 0;
    });

    const textareaId = id || (typeof label === 'string' ? `textarea-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      setCurrentLength(e.target.value.length);
      onChange?.(e);
    };

    return (
      <div className={cn("flex flex-col space-y-1.5", fullWidth && "w-full", className)}>
        <div className="flex items-center justify-between">
          {label && (
            <label
              htmlFor={textareaId}
              className="text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] font-sans select-none"
            >
              {label}
            </label>
          )}

          {showCount && maxLength && (
            <span className="text-[11px] text-[#5B5B5B] dark:text-slate-400 font-sans">
              {currentLength} / {maxLength}
            </span>
          )}
        </div>

        <textarea
          id={textareaId}
          ref={ref}
          disabled={disabled}
          rows={rows}
          maxLength={maxLength}
          value={value}
          defaultValue={defaultValue}
          onChange={handleChange}
          className={cn(
            "p-3.5 text-sm font-sans rounded-xl border transition-all duration-150 resize-y",
            "bg-white dark:bg-[#121B2D] text-[#1A1A1A] dark:text-[#F5F2EB] placeholder:text-[#787878] dark:placeholder:text-slate-500",
            "border-[#E5E2DA] dark:border-[#262D3D]",
            "hover:border-[#D1CDC4] dark:hover:border-[#3D475C]",
            "focus:outline-none focus:ring-2 focus:ring-[#1B2A4A] dark:focus:ring-sky-400 focus:border-transparent",
            "disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-[#FAF8F3] dark:disabled:bg-[#0E1526]",
            error && "border-red-500 dark:border-red-500 focus:ring-red-500 dark:focus:ring-red-500",
            fullWidth && "w-full"
          )}
          aria-invalid={!!error}
          aria-describedby={error ? `${textareaId}-error` : helperText ? `${textareaId}-helper` : undefined}
          {...props}
        />

        {error && (
          <div id={`${textareaId}-error`} className="flex items-center gap-1.5 text-xs text-red-600 dark:text-red-400 font-medium">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {!error && helperText && (
          <p id={`${textareaId}-helper`} className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';
