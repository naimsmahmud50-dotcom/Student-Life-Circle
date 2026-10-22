/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/components/ui/select.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides accessible custom styled select dropdown with chevron indicator,
 *            tactile focus rings, error states, and dark/light theme consistency.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

import React, { forwardRef } from 'react';
import { cn } from '@/lib/utils';
import { ChevronDown, AlertCircle } from 'lucide-react';

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  helperText?: string;
  error?: string;
  options?: SelectOption[];
  fullWidth?: boolean;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      className,
      label,
      helperText,
      error,
      options,
      children,
      fullWidth = true,
      id,
      disabled,
      ...props
    },
    ref
  ) => {
    const selectId = id || (label ? `select-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

    return (
      <div className={cn('flex flex-col space-y-1.5', fullWidth && 'w-full')}>
        {label && (
          <label
            htmlFor={selectId}
            className="text-xs font-semibold text-slate-700 dark:text-slate-300 font-bengali select-none"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center w-full">
          <select
            id={selectId}
            disabled={disabled}
            ref={ref}
            className={cn(
              'h-11 pl-4 pr-10 text-sm font-sans rounded-xl border transition-all duration-150 appearance-none cursor-pointer',
              'bg-white dark:bg-slate-900/90 text-slate-900 dark:text-slate-100',
              'border-slate-300 dark:border-slate-800',
              'hover:border-slate-400 dark:hover:border-slate-700',
              'focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-sky-400 focus:border-transparent',
              'disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-slate-100 dark:disabled:bg-slate-800/50',
              error && 'border-red-500 dark:border-red-500 focus:ring-red-500 dark:focus:ring-red-500',
              fullWidth && 'w-full',
              className
            )}
            aria-invalid={!!error}
            aria-describedby={error ? `${selectId}-error` : helperText ? `${selectId}-helper` : undefined}
            {...props}
          >
            {options
              ? options.map((opt) => (
                  <option key={opt.value} value={opt.value} disabled={opt.disabled}>
                    {opt.label}
                  </option>
                ))
              : children}
          </select>

          <div className="absolute right-3.5 flex items-center pointer-events-none text-slate-400 dark:text-slate-500">
            <ChevronDown className="w-4 h-4" />
          </div>
        </div>

        {error && (
          <div id={`${selectId}-error`} className="flex items-center gap-1.5 text-xs text-red-600 dark:text-red-400 font-medium">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {!error && helperText && (
          <p id={`${selectId}-helper`} className="text-xs text-slate-500 dark:text-slate-400 font-bengali">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Select.displayName = 'Select';
