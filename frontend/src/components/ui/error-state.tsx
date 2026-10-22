/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/components/ui/error-state.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides high-contrast, dignified academic error boundary views with
 *            clear diagnostic messaging, retry triggers, and zero emojis.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

import React, { useState } from 'react';
import { AlertTriangle, RotateCcw, ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from './button';

export interface ErrorStateProps {
  title?: string;
  description?: string;
  error?: Error | string | null;
  onRetry?: () => void;
  retryText?: string;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'একটি অপ্রত্যাশিত ত্রুটি ঘটেছে',
  description = 'ডেটা লোড করতে বা প্রক্রিয়া সম্পন্ন করতে সমস্যা হয়েছে। অনুগ্রহ করে পুনরায় চেষ্টা করুন।',
  error,
  onRetry,
  retryText = 'পুনরায় চেষ্টা করুন (Retry)',
  className,
}) => {
  const [showDetails, setShowDetails] = useState(false);

  const errorMessage = error instanceof Error ? error.message : typeof error === 'string' ? error : null;

  return (
    <div
      role="alert"
      className={cn(
        'flex flex-col items-center justify-center text-center p-8 sm:p-12 rounded-3xl border',
        'border-red-200 dark:border-red-900/60 bg-red-50/40 dark:bg-red-950/20 space-y-4 max-w-xl mx-auto w-full',
        className
      )}
    >
      <div className="w-14 h-14 rounded-2xl bg-red-100 dark:bg-red-900/40 border border-red-200 dark:border-red-800 flex items-center justify-center text-red-600 dark:text-red-400 shadow-sm">
        <AlertTriangle className="w-7 h-7" />
      </div>

      <div className="space-y-1.5">
        <h3 className="text-base sm:text-lg font-bold text-red-900 dark:text-red-200 font-bengali">
          {title}
        </h3>
        <p className="text-xs sm:text-sm text-red-700/80 dark:text-red-300/80 font-bengali max-w-md leading-relaxed">
          {description}
        </p>
      </div>

      {errorMessage && (
        <div className="w-full text-left pt-2">
          <button
            type="button"
            onClick={() => setShowDetails(!showDetails)}
            className="text-[11px] font-mono text-red-600 dark:text-red-400 hover:underline flex items-center gap-1 mx-auto"
          >
            <span>কারিগরি বিবরণ {showDetails ? 'লুকান' : 'দেখুন'}</span>
            {showDetails ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>

          {showDetails && (
            <pre className="mt-2 p-3 rounded-xl bg-red-100/70 dark:bg-red-950/80 text-[11px] font-mono text-red-800 dark:text-red-300 overflow-x-auto border border-red-200 dark:border-red-800/80 max-h-32">
              {errorMessage}
            </pre>
          )}
        </div>
      )}

      {onRetry && (
        <div className="pt-2">
          <Button
            variant="default"
            size="md"
            onClick={onRetry}
            icon={<RotateCcw className="w-4 h-4" />}
            className="bg-red-700 hover:bg-red-800 shadow-[0_4px_0_0_#5B0F0F]"
          >
            {retryText}
          </Button>
        </div>
      )}
    </div>
  );
};
