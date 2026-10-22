/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/components/ui/empty-state.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides dignified, academic empty state views with semantic Lucide SVG icons,
 *            restrained typography, and tactile call-to-action buttons.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

import React from 'react';
import Link from 'next/link';
import { FileQuestion } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from './button';

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  actionText?: string;
  actionLabel?: string;
  onAction?: () => void;
  actionHref?: string;
  actionIcon?: React.ReactNode;
  variant?: 'academic' | 'neutral' | 'archive';
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  actionText,
  actionLabel,
  onAction,
  actionHref,
  actionIcon,
  variant = 'academic',
  className,
}) => {
  const displayActionText = actionText || actionLabel;
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center text-center p-8 sm:p-12 rounded-3xl border border-dashed',
        'border-slate-300 dark:border-slate-800 bg-white/60 dark:bg-slate-900/40 space-y-4 max-w-xl mx-auto w-full',
        className
      )}
    >
      <div className="w-14 h-14 rounded-2xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 flex items-center justify-center text-[#0A2540] dark:text-sky-400 shadow-sm">
        {icon || <FileQuestion className="w-7 h-7" />}
      </div>

      <div className="space-y-1.5">
        <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white font-bengali">
          {title}
        </h3>
        {description && (
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 font-bengali max-w-md leading-relaxed">
            {description}
          </p>
        )}
      </div>

      {displayActionText && (
        <div className="pt-2">
          {actionHref ? (
            <Link href={actionHref}>
              <Button variant="default" size="md" icon={actionIcon}>
                {displayActionText}
              </Button>
            </Link>
          ) : (
            <Button variant="default" size="md" onClick={onAction} icon={actionIcon}>
              {displayActionText}
            </Button>
          )}
        </div>
      )}
    </div>
  );
};
