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
        // Standard subtle border border-[#E2E8F0] elevated to academic hairline #E5E2DA
        "rounded-2xl border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D] text-[#1A1A1A] dark:text-[#F5F2EB] shadow-none transition-colors duration-150",
        hoverable && "hover:border-[#D1CDC4] dark:hover:border-[#3D475C] hover:bg-[#FAF8F3]/60 dark:hover:bg-[#152035]/60",
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
    className={cn("flex flex-col space-y-1.5 p-6 pb-2", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

export const CardMeta = forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center gap-2 text-xs text-[#5B5B5B] dark:text-slate-400 font-sans pb-1", className)}
    {...props}
  />
));
CardMeta.displayName = "CardMeta";

export const CardTitle = forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-base sm:text-lg font-serif font-bold leading-snug tracking-normal text-[#1B2A4A] dark:text-[#F5F2EB]",
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
    className={cn("text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-300 leading-relaxed font-sans", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

export const CardContent = forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-2", className)} {...props} />
));
CardContent.displayName = "CardContent";

export const CardFooter = forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0 border-t border-[#E5E2DA] dark:border-[#262D3D] mt-4", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";
