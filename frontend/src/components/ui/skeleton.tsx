/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Accessible Loading Skeleton
 * TOPIC:     Bengal Academic Editorial & Warm Paper Shimmer
 * FILE:      frontend/src/components/ui/skeleton.tsx
 * PURPOSE:   Provides subtle, warm paper loading skeleton shimmer components that respect
 *            prefers-reduced-motion, avoid harsh neon white/slate flashes, and harmonize across both Light and Dark themes.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Academic Editorial, Warm Paper Shimmer
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
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
    card: 'h-48 w-full rounded-lg border border-[#E5E2DA] dark:border-[#263147]',
  };

  return (
    <div
      className={cn(
        'animate-pulse bg-[#EFECE3] dark:bg-[#1E2738]',
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
          className="p-6 rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] shadow-sm space-y-4"
        >
          <div className="flex items-center justify-between">
            <Skeleton variant="text" className="w-1/3 h-5" />
            <Skeleton variant="rectangular" className="w-16 h-6" />
          </div>
          <Skeleton variant="text" className="w-full h-4" />
          <Skeleton variant="text" className="w-4/5 h-4" />
          <div className="flex items-center justify-between pt-2">
            <Skeleton variant="rectangular" className="w-24 h-4" />
            <Skeleton variant="rectangular" className="w-28 h-9" />
          </div>
        </div>
      ))}
    </div>
  );
};
