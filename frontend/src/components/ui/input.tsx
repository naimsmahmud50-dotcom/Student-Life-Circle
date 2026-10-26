/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Accessible Form Input
 * TOPIC:     Bengal Academic Editorial & Tactile Form Controls
 * FILE:      frontend/src/components/ui/input.tsx
 * PURPOSE:   Provides production-grade, accessible form input field with subtle inner bevel,
 *            hairline borders (#E5E2DA), Oxford Navy tactile focus ring, prefix/suffix icon slots,
 *            dark/light theme support, and WCAG 2.2 AAA contrast.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Academic Editorial, 3D Tactile Physics
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
            className="text-xs font-semibold text-[#1A1A1A] dark:text-[#F5F2EB] font-bengali select-none"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center w-full">
          {iconLeft && (
            <div className="absolute left-3.5 flex items-center pointer-events-none text-[#525252] dark:text-[#A3A8B5]">
              {iconLeft}
            </div>
          )}

          <input
            id={inputId}
            type={type}
            disabled={disabled}
            ref={ref}
            className={cn(
              'h-11 px-4 text-sm font-sans rounded-lg border transition-all duration-120',
              'bg-[#FDFCF9] dark:bg-[#171E2C] text-[#1A1A1A] dark:text-[#F5F2EB] placeholder:text-[#737373] dark:placeholder:text-[#7D8494]',
              'border-[#E5E2DA] dark:border-[#263147] shadow-[inset_0_1px_2px_rgba(10,37,64,0.04)] dark:shadow-[inset_0_1px_2px_rgba(0,0,0,0.3)]',
              'hover:border-[#D1CDC4] dark:hover:border-[#384663]',
              'focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-[#6088C6] focus:border-transparent',
              'disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-[#F5F2EB] dark:disabled:bg-[#1E2738]',
              iconLeft && 'pl-10',
              iconRight && 'pr-10',
              error && 'border-[#991B1B] dark:border-[#D94545] focus:ring-[#991B1B] dark:focus:ring-[#D94545]',
              fullWidth && 'w-full',
              className
            )}
            aria-invalid={!!error}
            aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
            {...props}
          />

          {iconRight && (
            <div className="absolute right-3.5 flex items-center pointer-events-none text-[#525252] dark:text-[#A3A8B5]">
              {iconRight}
            </div>
          )}
        </div>

        {error && (
          <div id={`${inputId}-error`} className="flex items-center gap-1.5 text-xs text-[#991B1B] dark:text-[#D94545] font-medium">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {helperText && !error && (
          <p id={`${inputId}-helper`} className="text-xs text-[#525252] dark:text-[#A3A8B5]">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
