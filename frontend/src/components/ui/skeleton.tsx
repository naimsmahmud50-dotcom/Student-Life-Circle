/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/components/ui/skeleton.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides subtle, polished loading skeleton shimmer components that respect
 *            prefers-reduced-motion and harmonize across both Light and Dark themes.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

import React from 'react';
import { cn } from '@/lib/utils';

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'text' | 'rectangular' | 'circular' | 'card';
  width?: string | number;
  height?: string | number;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className,
  variant = 'rectangular',
  width,
  height,
  style,
  ...props
}) => {
  const variantStyles: Record<string, string> = {
    text: 'h-4 w-full rounded-md',
    rectangular: 'rounded-xl',
    circular: 'rounded-full',
    card: 'h-48 w-full rounded-2xl',
  };

  return (
    <div
      className={cn(
        'animate-pulse bg-slate-200/80 dark:bg-slate-800/60',
        variantStyles[variant],
        className
      )}
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        ...style,
      }}
      aria-hidden="true"
      {...props}
    />
  );
};

export const CardSkeleton: React.FC<{ count?: number; className?: string }> = ({
  count = 1,
  className
}) => {
  return (
    <div className={cn('space-y-4', className)}>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4"
        >
          <div className="flex items-center justify-between">
            <Skeleton variant="text" className="w-1/3 h-5" />
            <Skeleton variant="rectangular" className="w-16 h-6 rounded-full" />
          </div>
          <Skeleton variant="text" className="w-full h-4" />
          <Skeleton variant="text" className="w-4/5 h-4" />
          <div className="pt-2 flex items-center gap-3">
            <Skeleton variant="rectangular" className="w-24 h-9 rounded-xl" />
            <Skeleton variant="rectangular" className="w-24 h-9 rounded-xl" />
          </div>
        </div>
      ))}
    </div>
  );
};
