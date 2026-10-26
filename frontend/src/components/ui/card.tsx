/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Accessible Academic Card Component Suite
 * TOPIC:     Bengal Academic Editorial & Layered Soft Paper Depth
 * FILE:      frontend/src/components/ui/card.tsx
 * PURPOSE:   Provides clean, modern elevated cards for modules, course units, quiz questions,
 *            and telemetry monitors. Uses hairline borders (#E5E2DA / #263147), soft layered
 *            paper elevation, optional tactile 3D hover lift, and disciplined 8-10px radius.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA Contrast >= 4.5:1, Zero-Emoji Architecture
 */

import React, { forwardRef } from 'react';
import { cn } from '@/lib/utils';

export type CardVariant = 'default' | 'elevated' | 'interactive' | 'muted';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  hoverable?: boolean;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', hoverable = false, ...props }, ref) => {
    const variantStyles: Record<CardVariant, string> = {
      default: "bg-[#FDFCF9] dark:bg-[#171E2C] border-[#E5E2DA] dark:border-[#263147] shadow-[0_1px_3px_rgba(10,37,64,0.05),0_1px_2px_rgba(0,0,0,0.02)]",
      elevated: "bg-[#FDFCF9] dark:bg-[#171E2C] border-[#E5E2DA] dark:border-[#263147] shadow-[0_4px_8px_-2px_rgba(10,37,64,0.06),0_2px_4px_-1px_rgba(0,0,0,0.03)]",
      interactive: "bg-[#FDFCF9] dark:bg-[#171E2C] border-[#E5E2DA] dark:border-[#263147] shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#D1CDC4,0_4px_8px_rgba(10,37,64,0.08)] active:translate-y-0.5 active:shadow-[0_1px_0_0_#D1CDC4] dark:shadow-[0_3px_0_0_#1F283A] dark:hover:shadow-[0_5px_0_0_#1F283A] cursor-pointer will-change-transform",
      muted: "bg-[#F5F2EB] dark:bg-[#1E2738] border-[#E5E2DA] dark:border-[#263147] shadow-none",
    };

    return (
      <div
        ref={ref}
        className={cn(
          "rounded-lg border text-[#1A1A1A] dark:text-[#F5F2EB] transition-all duration-150 ease-[cubic-bezier(0.16,1,0.3,1)]",
          variantStyles[variant],
          hoverable && variant !== 'interactive' && "hover:border-[#D1CDC4] dark:hover:border-[#384663] hover:bg-[#FAF8F3] dark:hover:bg-[#1E2738]/80",
          className
        )}
        {...props}
      />
    );
  }
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
    className={cn("flex items-center gap-2 text-xs text-[#525252] dark:text-[#A3A8B5] font-sans pb-1", className)}
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
      "text-base sm:text-lg font-serif font-bold leading-[1.35] tracking-normal text-[#0A2540] dark:text-[#F5F2EB]",
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
    className={cn("text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7] font-sans", className)}
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
    className={cn("flex items-center p-6 pt-2 border-t border-[#E5E2DA] dark:border-[#263147]", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";
