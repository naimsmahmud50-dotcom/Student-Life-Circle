/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Radix UI Primitive Wrapper - Accessible Button Component
 * TOPIC:     Master Academic UI & Pro Tactile Button Elevation
 * FILE:      frontend/src/components/ui/button.tsx
 * PHASE:     Phase 110 - Pure Academic Visual Design Elevation & Phase 123 - Master Academic UI & Pro Tactile Button Elevation
 * PURPOSE:   Elevates every button, card, background, and header to Duolingo/Brilliant-grade
 *            3D physical press physics, Oxford Academic Navy palette, and zero AI vibe.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
 */

import React, { forwardRef } from 'react';
import { Slot } from '@radix-ui/react-slot';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export type ButtonVariant = 
  | 'default'
  | 'oxford'
  | 'academic'
  | 'emerald'
  | 'paper'
  | 'brand'
  | 'primary'
  | 'secondary'
  | 'teal'
  | 'destructive'
  | 'danger'
  | 'outline'
  | 'ghost'
  | 'link';

export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  asChild?: boolean;
  isLoading?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  className,
  variant = 'default',
  size = 'md',
  asChild = false,
  isLoading: propIsLoading,
  loading: propLoading,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  children,
  disabled,
  ...props
}, ref) => {
  const Comp = asChild ? Slot : 'button';
  const isLoading = propIsLoading ?? propLoading ?? false;

  // Base ergonomics: minimum touch targets, accessible focus ring, smooth active state with spring physics
  const baseStyles = "inline-flex items-center justify-center font-semibold rounded-2xl transition-all duration-150 ease-[cubic-bezier(0.16,1,0.3,1)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none select-none active:translate-y-1 active:shadow-none will-change-transform";

  // Size specifications guaranteeing mobile touch targets (>= 44px for standard interaction)
  const sizeStyles: Record<ButtonSize, string> = {
    sm: "h-9 px-3.5 text-xs min-h-[36px]",
    md: "h-11 px-5 py-2.5 text-sm min-h-[44px]",
    lg: "h-12 px-7 py-3 text-base min-h-[48px]",
  };

  // High-contrast, WCAG 2.2 AAA Oxford/Cambridge scholarly tactile variants
  const variantStyles: Record<ButtonVariant, string> = {
    // Primary Oxford Navy Tactile 3D Button
    default: "bg-[#0A2540] text-white hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] focus-visible:ring-[#0A2540]",
    oxford: "bg-[#0A2540] text-white hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] focus-visible:ring-[#0A2540]",
    brand: "bg-[#0A2540] text-white hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] focus-visible:ring-[#0A2540]",
    primary: "bg-[#0A2540] text-white hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329] focus-visible:ring-[#0A2540]",

    // Scholarly Academic Emerald Tactile 3D Button
    academic: "bg-[#065F46] text-white hover:bg-[#087858] shadow-[0_4px_0_0_#033829] focus-visible:ring-[#065F46]",
    emerald: "bg-[#065F46] text-white hover:bg-[#087858] shadow-[0_4px_0_0_#033829] focus-visible:ring-[#065F46]",
    teal: "bg-[#065F46] text-white hover:bg-[#087858] shadow-[0_4px_0_0_#044332] focus-visible:ring-[#065F46]",

    // Pure Paper Outline & Secondary Tactile Buttons
    paper: "bg-white text-slate-800 border border-slate-300 shadow-sm hover:bg-slate-50 dark:bg-slate-900 dark:text-slate-100 dark:border-slate-700 active:translate-y-0.5 rounded-2xl focus-visible:ring-slate-400",
    outline: "bg-white text-slate-800 border border-slate-300 shadow-sm hover:bg-slate-50 dark:bg-slate-900 dark:text-slate-100 dark:border-slate-700 active:translate-y-0.5 rounded-2xl focus-visible:ring-slate-400",
    secondary: "bg-white text-slate-800 border border-slate-300 shadow-sm hover:bg-slate-50 dark:bg-slate-900 dark:text-slate-100 dark:border-slate-700 active:translate-y-0.5 rounded-2xl focus-visible:ring-slate-400",

    // Burgundy Crimson Negative Marking & Destructive Buttons
    destructive: "bg-[#991B1B] text-white hover:bg-[#7F1D1D] shadow-[0_4px_0_0_#5B1010] focus-visible:ring-[#991B1B]",
    danger: "bg-[#991B1B] text-white hover:bg-[#7F1D1D] shadow-[0_4px_0_0_#5B1010] focus-visible:ring-[#991B1B]",

    // Scholarly Ghost & Text Link Buttons
    ghost: "bg-transparent text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100 active:translate-y-0.5 shadow-none focus-visible:ring-[#0A2540]",
    link: "bg-transparent text-[#1B2A4A] dark:text-[#F5F2EB] hover:underline underline-offset-4 active:translate-y-0 shadow-none focus-visible:ring-[#1B2A4A] p-0 h-auto min-h-[44px]",
  };

  const widthStyle = fullWidth ? "w-full" : "";

  return (
    <Comp
      ref={ref}
      disabled={disabled || isLoading}
      aria-busy={isLoading ? "true" : undefined}
      className={cn(baseStyles, sizeStyles[size], variantStyles[variant], widthStyle, className)}
      {...props}
    >
      {isLoading ? (
        <>
          <Loader2 className="w-4 h-4 mr-2 animate-spin shrink-0" aria-hidden="true" />
          <span>{children}</span>
        </>
      ) : (
        <>
          {icon && iconPosition === 'left' && (
            <span className="mr-2 inline-flex items-center shrink-0" aria-hidden="true">
              {icon}
            </span>
          )}
          <span>{children}</span>
          {icon && iconPosition === 'right' && (
            <span className="ml-2 inline-flex items-center shrink-0" aria-hidden="true">
              {icon}
            </span>
          )}
        </>
      )}
    </Comp>
  );
});

Button.displayName = 'Button';
