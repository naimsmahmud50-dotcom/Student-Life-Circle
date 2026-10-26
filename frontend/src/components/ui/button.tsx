/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Radix UI Primitive Wrapper - Accessible Tactile Button Component
 * TOPIC:     Master Academic UI, Bengal Academic Editorial & Pro Tactile Button Elevation
 * FILE:      frontend/src/components/ui/button.tsx
 * PURPOSE:   Elevates every button to Duolingo/Brilliant-grade 3D physical press physics,
 *            Oxford Academic Navy palette, Forest Emerald, Paper Outline, Burgundy Crimson,
 *            inner highlights, layered shadows, square touch targets, and zero AI vibe.
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
  | 'icon'
  | 'link';

export type ButtonSize = 'sm' | 'md' | 'lg' | 'icon' | 'icon-sm';

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

  // Disciplined academic radius (rounded-lg = 8-10px), minimum touch target, smooth 120ms tactile spring press
  const baseStyles = "inline-flex items-center justify-center font-semibold rounded-lg border transition-all duration-120 ease-[cubic-bezier(0.16,1,0.3,1)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none disabled:shadow-none disabled:translate-y-0 select-none will-change-transform cursor-pointer";

  // Size specifications guaranteeing mobile touch targets (>= 44px for standard interaction)
  const sizeStyles: Record<ButtonSize, string> = {
    sm: "h-9 px-3.5 text-xs min-h-[36px]",
    md: "h-11 px-5 py-2.5 text-sm min-h-[44px]",
    lg: "h-12 px-7 py-3 text-base min-h-[48px]",
    icon: "h-11 w-11 min-h-[44px] min-w-[44px] p-0 shrink-0",
    'icon-sm': "h-9 w-9 min-h-[36px] min-w-[36px] p-0 shrink-0 text-xs",
  };

  // High-contrast, WCAG 2.2 AAA Oxford/Cambridge scholarly tactile variants with physical depth
  const variantStyles: Record<ButtonVariant, string> = {
    // Primary Oxford Navy Tactile 3D Button (3-4px physical bottom shadow, inner highlight)
    default: "bg-[#0A2540] text-white border-[#051329] hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329,0_2px_4px_rgba(10,37,64,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#051329,0_4px_8px_rgba(10,37,64,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#0A2540]",
    oxford: "bg-[#0A2540] text-white border-[#051329] hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329,0_2px_4px_rgba(10,37,64,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#051329,0_4px_8px_rgba(10,37,64,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#0A2540]",
    brand: "bg-[#0A2540] text-white border-[#051329] hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329,0_2px_4px_rgba(10,37,64,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#051329,0_4px_8px_rgba(10,37,64,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#0A2540]",
    primary: "bg-[#0A2540] text-white border-[#051329] hover:bg-[#0E3357] shadow-[0_4px_0_0_#051329,0_2px_4px_rgba(10,37,64,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#051329,0_4px_8px_rgba(10,37,64,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#0A2540]",

    // Scholarly Academic Forest Emerald Tactile 3D Button
    academic: "bg-[#065F46] text-white border-[#033829] hover:bg-[#087858] shadow-[0_4px_0_0_#033829,0_2px_4px_rgba(6,95,70,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#033829,0_4px_8px_rgba(6,95,70,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#065F46]",
    emerald: "bg-[#065F46] text-white border-[#033829] hover:bg-[#087858] shadow-[0_4px_0_0_#033829,0_2px_4px_rgba(6,95,70,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#033829,0_4px_8px_rgba(6,95,70,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#065F46]",
    teal: "bg-[#065F46] text-white border-[#033829] hover:bg-[#087858] shadow-[0_4px_0_0_#033829,0_2px_4px_rgba(6,95,70,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#033829,0_4px_8px_rgba(6,95,70,0.16),inset_0_1px_0_rgba(255,255,255,0.22)] active:translate-y-1 active:shadow-none focus-visible:ring-[#065F46]",

    // Pure Paper Outline & Secondary Tactile Buttons
    paper: "bg-[#FDFCF9] text-[#1A1A1A] border-[#E5E2DA] shadow-[0_3px_0_0_#D1CDC4,0_1px_2px_rgba(0,0,0,0.04),inset_0_1px_0_rgba(255,255,255,0.8)] hover:bg-[#F5F2EB] hover:-translate-y-0.5 hover:shadow-[0_4px_0_0_#D1CDC4,0_2px_4px_rgba(0,0,0,0.06)] dark:bg-[#171E2C] dark:text-[#F5F2EB] dark:border-[#263147] dark:shadow-[0_3px_0_0_#1F283A] active:translate-y-0.5 active:shadow-none focus-visible:ring-[#0A2540]",
    outline: "bg-[#FDFCF9] text-[#1A1A1A] border-[#E5E2DA] shadow-[0_3px_0_0_#D1CDC4,0_1px_2px_rgba(0,0,0,0.04),inset_0_1px_0_rgba(255,255,255,0.8)] hover:bg-[#F5F2EB] hover:-translate-y-0.5 hover:shadow-[0_4px_0_0_#D1CDC4,0_2px_4px_rgba(0,0,0,0.06)] dark:bg-[#171E2C] dark:text-[#F5F2EB] dark:border-[#263147] dark:shadow-[0_3px_0_0_#1F283A] active:translate-y-0.5 active:shadow-none focus-visible:ring-[#0A2540]",
    secondary: "bg-[#FDFCF9] text-[#1A1A1A] border-[#E5E2DA] shadow-[0_3px_0_0_#D1CDC4,0_1px_2px_rgba(0,0,0,0.04),inset_0_1px_0_rgba(255,255,255,0.8)] hover:bg-[#F5F2EB] hover:-translate-y-0.5 hover:shadow-[0_4px_0_0_#D1CDC4,0_2px_4px_rgba(0,0,0,0.06)] dark:bg-[#171E2C] dark:text-[#F5F2EB] dark:border-[#263147] dark:shadow-[0_3px_0_0_#1F283A] active:translate-y-0.5 active:shadow-none focus-visible:ring-[#0A2540]",

    // Tactile Icon Button
    icon: "bg-[#FDFCF9] text-[#1A1A1A] border-[#E5E2DA] shadow-[0_3px_0_0_#D1CDC4] hover:bg-[#F5F2EB] hover:-translate-y-0.5 hover:shadow-[0_4px_0_0_#D1CDC4] dark:bg-[#171E2C] dark:text-[#F5F2EB] dark:border-[#263147] dark:shadow-[0_3px_0_0_#1F283A] active:translate-y-0.5 active:shadow-none focus-visible:ring-[#0A2540]",

    // Burgundy Crimson Negative Marking & Destructive Buttons
    destructive: "bg-[#991B1B] text-white border-[#5B1010] hover:bg-[#7F1D1D] shadow-[0_4px_0_0_#5B1010,0_2px_4px_rgba(153,27,27,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#5B1010,0_4px_8px_rgba(153,27,27,0.16)] active:translate-y-1 active:shadow-none focus-visible:ring-[#991B1B]",
    danger: "bg-[#991B1B] text-white border-[#5B1010] hover:bg-[#7F1D1D] shadow-[0_4px_0_0_#5B1010,0_2px_4px_rgba(153,27,27,0.12),inset_0_1px_0_rgba(255,255,255,0.18)] hover:-translate-y-0.5 hover:shadow-[0_5px_0_0_#5B1010,0_4px_8px_rgba(153,27,27,0.16)] active:translate-y-1 active:shadow-none focus-visible:ring-[#991B1B]",

    // Scholarly Ghost & Text Link Buttons
    ghost: "bg-transparent text-[#1A1A1A] border-transparent hover:bg-[#F5F2EB] hover:text-[#0A2540] dark:text-[#F5F2EB] dark:hover:bg-[#1E2738] dark:hover:text-white active:translate-y-0.5 shadow-none focus-visible:ring-[#0A2540]",
    link: "bg-transparent text-[#0A2540] dark:text-[#F5F2EB] border-transparent hover:underline underline-offset-4 active:translate-y-0 shadow-none focus-visible:ring-[#0A2540] p-0 h-auto min-h-[44px]",
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
            <span className={cn("inline-flex items-center shrink-0", children ? "mr-2" : "")} aria-hidden="true">
              {icon}
            </span>
          )}
          {children && <span>{children}</span>}
          {icon && iconPosition === 'right' && (
            <span className={cn("inline-flex items-center shrink-0", children ? "ml-2" : "")} aria-hidden="true">
              {icon}
            </span>
          )}
        </>
      )}
    </Comp>
  );
});

Button.displayName = 'Button';
