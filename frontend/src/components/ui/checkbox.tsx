/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Form Primitives
 * TOPIC:     Modern Academic Editorial Checkbox Primitive
 * FILE:      frontend/src/components/ui/checkbox.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible, high-contrast checkbox control with label, helper text,
 *            inline error validation, indeterminate support, and 44px touch target ergonomics.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { forwardRef, useEffect, useRef } from 'react';
import { Check, Minus, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: React.ReactNode;
  helperText?: React.ReactNode;
  error?: string;
  indeterminate?: boolean;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  (
    {
      className,
      label,
      helperText,
      error,
      indeterminate = false,
      checked,
      disabled,
      id,
      ...props
    },
    ref
  ) => {
    const internalRef = useRef<HTMLInputElement>(null);
    const combinedRef = (node: HTMLInputElement | null) => {
      internalRef.current = node;
      if (typeof ref === 'function') ref(node);
      else if (ref) (ref as React.MutableRefObject<HTMLInputElement | null>).current = node;
    };

    useEffect(() => {
      if (internalRef.current) {
        internalRef.current.indeterminate = indeterminate;
      }
    }, [indeterminate]);

    const generatedId = id || (typeof label === 'string' ? `checkbox-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

    return (
      <div className={cn("flex flex-col space-y-1", className)}>
        <label
          htmlFor={generatedId}
          className={cn(
            "inline-flex items-start gap-3 min-h-[44px] cursor-pointer select-none py-1.5",
            disabled && "cursor-not-allowed opacity-50"
          )}
        >
          <div className="relative flex items-center justify-center shrink-0 mt-0.5">
            <input
              id={generatedId}
              type="checkbox"
              ref={combinedRef}
              checked={checked}
              disabled={disabled}
              className="peer sr-only"
              aria-invalid={!!error}
              aria-describedby={error ? `${generatedId}-error` : helperText ? `${generatedId}-helper` : undefined}
              {...props}
            />
            <div
              className={cn(
                "w-5 h-5 rounded-[6px] border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D] transition-colors duration-150 flex items-center justify-center",
                "peer-focus-visible:ring-2 peer-focus-visible:ring-[#1B2A4A] dark:peer-focus-visible:ring-sky-400 peer-focus-visible:ring-offset-2",
                "peer-hover:border-[#D1CDC4] dark:peer-hover:border-[#3D475C]",
                "peer-checked:bg-[#1B2A4A] peer-checked:border-[#1B2A4A] peer-checked:text-white dark:peer-checked:bg-[#203660] dark:peer-checked:border-[#203660]",
                error && "border-red-500 dark:border-red-500"
              )}
            >
              {indeterminate ? (
                <Minus className="w-3.5 h-3.5 text-white stroke-[2.5]" aria-hidden="true" />
              ) : checked ? (
                <Check className="w-3.5 h-3.5 text-white stroke-[2.5]" aria-hidden="true" />
              ) : null}
            </div>
          </div>

          {(label || helperText) && (
            <div className="flex flex-col text-xs sm:text-sm">
              {label && (
                <span className="font-semibold text-[#1A1A1A] dark:text-[#F5F2EB] font-sans">
                  {label}
                </span>
              )}
              {helperText && (
                <span id={`${generatedId}-helper`} className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans mt-0.5">
                  {helperText}
                </span>
              )}
            </div>
          )}
        </label>

        {error && (
          <div id={`${generatedId}-error`} className="flex items-center gap-1.5 text-xs text-red-600 dark:text-red-400 font-medium pl-8">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';
