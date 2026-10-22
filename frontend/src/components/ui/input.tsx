/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/components/ui/input.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides production-grade, accessible form input field with tactile
 *            focus rings, prefix/suffix icon slots, dark/light theme support, and WCAG 2.2 AAA contrast.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

import React, { forwardRef } from 'react';
import { cn } from '@/lib/utils';
import { AlertCircle } from 'lucide-react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  prefixIcon?: React.ReactNode;
  suffixIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      type = 'text',
      label,
      helperText,
      error,
      leftIcon,
      rightIcon,
      prefixIcon,
      suffixIcon,
      fullWidth = true,
      id,
      disabled,
      ...props
    },
    ref
  ) => {
    const iconLeft = leftIcon || prefixIcon;
    const iconRight = rightIcon || suffixIcon;
    const inputId = id || (label ? `input-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

    return (
      <div className={cn('flex flex-col space-y-1.5', fullWidth && 'w-full')}>
        {label && (
          <label
            htmlFor={inputId}
            className="text-xs font-semibold text-slate-700 dark:text-slate-300 font-bengali select-none"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center w-full">
          {iconLeft && (
            <div className="absolute left-3.5 flex items-center pointer-events-none text-slate-400 dark:text-slate-500">
              {iconLeft}
            </div>
          )}

          <input
            id={inputId}
            type={type}
            disabled={disabled}
            ref={ref}
            className={cn(
              'h-11 px-4 text-sm font-sans rounded-xl border transition-all duration-150',
              'bg-white dark:bg-slate-900/90 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500',
              'border-slate-300 dark:border-slate-800',
              'hover:border-slate-400 dark:hover:border-slate-700',
              'focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-sky-400 focus:border-transparent',
              'disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-slate-100 dark:disabled:bg-slate-800/50',
              iconLeft && 'pl-10',
              iconRight && 'pr-10',
              error && 'border-red-500 dark:border-red-500 focus:ring-red-500 dark:focus:ring-red-500',
              fullWidth && 'w-full',
              className
            )}
            aria-invalid={!!error}
            aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
            {...props}
          />

          {iconRight && (
            <div className="absolute right-3.5 flex items-center pointer-events-none text-slate-400 dark:text-slate-500">
              {iconRight}
            </div>
          )}
        </div>

        {error && (
          <div id={`${inputId}-error`} className="flex items-center gap-1.5 text-xs text-red-600 dark:text-red-400 font-medium">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {!error && helperText && (
          <p id={`${inputId}-helper`} className="text-xs text-slate-500 dark:text-slate-400 font-bengali">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
