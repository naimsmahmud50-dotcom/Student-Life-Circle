/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CORE UI PRIMITIVES:
 * MODULE:    Radix UI Primitive Wrapper - Accessible Badge & Chip Component
 * TOPIC:     Strict Zero-Emoji, Semantic SVG Icons, Status Pills, Dual Light/Dark Themes
 * FILE:      frontend/src/components/ui/badge.tsx
 * PURPOSE:   Provides versatile, accessible status pills, difficulty indicators, role chips,
 *            and verification badges. Replaces emojis with precise Lucide SVG vectors.
 *            Supports both Light Mode and Dark Mode with WCAG 2.2 AA compliant contrast.
 * AUDIENCE:  Frontend Developers, Accessibility Testers & UI Reviewers
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA Contrast >= 4.5:1, Zero-Emoji Architecture
 * ========================================================================================
 */

import React from 'react';
import { ShieldCheck, Check, Sparkles, User, GraduationCap, ShieldAlert } from 'lucide-react';
import { cn } from '@/lib/utils';

export type BadgeVariant = 
  | 'brand'
  | 'teal'
  | 'warning'
  | 'destructive'
  | 'danger'
  | 'neutral'
  | 'outline'
  | 'verified'
  | 'mastery'
  | 'success';

export type BadgeSize = 'sm' | 'md' | 'lg';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  size?: BadgeSize;
  icon?: React.ReactNode;
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = 'brand',
  size = 'md',
  icon,
  children,
  ...props
}) => {
  const baseStyles = "inline-flex items-center font-medium tracking-wide transition-colors select-none";

  const sizeStyles: Record<BadgeSize, string> = {
    sm: "px-2 py-0.5 rounded text-[10px] gap-1",
    md: "px-2.5 py-1 rounded-full text-xs gap-1.5",
    lg: "px-3 py-1.5 rounded-full text-sm gap-2",
  };

  const variantStyles: Record<BadgeVariant, string> = {
    brand: "bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-900",
    teal: "bg-teal-50 dark:bg-teal-950/40 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-900",
    warning: "bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-900",
    destructive: "bg-red-50 dark:bg-red-950/40 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-900",
    danger: "bg-red-50 dark:bg-red-950/40 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-900",
    neutral: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700",
    outline: "bg-transparent text-slate-800 dark:text-slate-200 border border-slate-300 dark:border-slate-700",
    verified: "bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900 font-semibold",
    mastery: "bg-purple-50 dark:bg-purple-950/40 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-900",
    success: "bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900 font-semibold",
  };

  return (
    <span
      className={cn(baseStyles, sizeStyles[size], variantStyles[variant], className)}
      {...props}
    >
      {icon && (
        <span className="inline-flex items-center shrink-0" aria-hidden="true">
          {icon}
        </span>
      )}
      <span>{children}</span>
    </span>
  );
};

// ----------------------------------------------------------------------------
// SPECIALIZED DOMAIN PRESETS
// ----------------------------------------------------------------------------

export interface DifficultyBadgeProps extends Omit<BadgeProps, 'variant' | 'icon' | 'children'> {
  difficulty: 'easy' | 'medium' | 'hard';
  label?: string;
}

export const DifficultyBadge: React.FC<DifficultyBadgeProps> = ({
  difficulty,
  label,
  className,
  ...props
}) => {
  const configs = {
    easy: {
      variant: 'teal' as const,
      text: label || 'Easy',
    },
    medium: {
      variant: 'warning' as const,
      text: label || 'Medium',
    },
    hard: {
      variant: 'destructive' as const,
      text: label || 'Hard',
    },
  };

  const config = configs[difficulty] || configs.medium;

  return (
    <Badge variant={config.variant} className={className} {...props}>
      <span className="w-1.5 h-1.5 rounded-full bg-current shrink-0" aria-hidden="true" />
      <span>{config.text}</span>
    </Badge>
  );
};

export interface VerifiedBadgeProps extends Omit<BadgeProps, 'variant' | 'icon'> {
  label?: string;
  shield?: boolean;
}

export const VerifiedBadge: React.FC<VerifiedBadgeProps> = ({
  label = 'Verified',
  shield = false,
  className,
  ...props
}) => {
  const Icon = shield ? ShieldCheck : Check;
  return (
    <Badge variant="verified" className={className} icon={<Icon className="w-3.5 h-3.5" />} {...props}>
      {label}
    </Badge>
  );
};

export interface RoleChipProps extends Omit<BadgeProps, 'variant' | 'icon' | 'children'> {
  role: 'student' | 'guardian' | 'teacher' | 'admin';
  label?: string;
}

export const RoleChip: React.FC<RoleChipProps> = ({
  role,
  label,
  className,
  ...props
}) => {
  const roleConfigs = {
    student: {
      variant: 'brand' as const,
      icon: <GraduationCap className="w-3.5 h-3.5" />,
      defaultLabel: 'Student',
    },
    guardian: {
      variant: 'teal' as const,
      icon: <User className="w-3.5 h-3.5" />,
      defaultLabel: 'Guardian',
    },
    teacher: {
      variant: 'warning' as const,
      icon: <Sparkles className="w-3.5 h-3.5" />,
      defaultLabel: 'Teacher',
    },
    admin: {
      variant: 'neutral' as const,
      icon: <ShieldAlert className="w-3.5 h-3.5" />,
      defaultLabel: 'Admin',
    },
  };

  const config = roleConfigs[role] || roleConfigs.student;

  return (
    <Badge variant={config.variant} icon={config.icon} className={className} {...props}>
      {label || config.defaultLabel}
    </Badge>
  );
};
