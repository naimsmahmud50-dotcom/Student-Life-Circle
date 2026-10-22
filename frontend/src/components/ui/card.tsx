/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CORE UI PRIMITIVES:
 * MODULE:    Accessible Elevated Card Component Suite
 * TOPIC:     Subtle Border (#E2E8F0), Dual Light/Dark Theme Elevation & Zero Emoji
 * FILE:      frontend/src/components/ui/card.tsx
 * PURPOSE:   Provides clean, modern elevated cards for modules, course units, quiz questions,
 *            and telemetry monitors. Uses subtle border (#E2E8F0 / slate-800), smooth hover
 *            elevation, and structured compound components (Header, Title, Description, Content, Footer).
 * AUDIENCE:  Frontend Developers, Accessibility Testers & UI Reviewers
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA Contrast >= 4.5:1, Zero-Emoji Architecture
 * ========================================================================================
 */

import React, { forwardRef } from 'react';
import { cn } from '@/lib/utils';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, hoverable = false, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-2xl border border-[#E2E8F0] dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-sm transition-all duration-200",
        hoverable && "hover:shadow-md hover:border-slate-300 dark:hover:border-slate-700 hover:-translate-y-0.5",
        className
      )}
      {...props}
    />
  )
);
Card.displayName = "Card";

export const CardHeader = forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6 pb-3", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

export const CardTitle = forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-base sm:text-lg font-bold leading-none tracking-tight text-slate-900 dark:text-white",
      className
    )}
    {...props}
  />
));
CardTitle.displayName = "CardTitle";

export const CardDescription = forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

export const CardContent = forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-3", className)} {...props} />
));
CardContent.displayName = "CardContent";

export const CardFooter = forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0 border-t border-slate-100 dark:border-slate-800/80 mt-4", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";
