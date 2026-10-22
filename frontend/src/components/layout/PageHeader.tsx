/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/components/layout/PageHeader.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides a flagship-grade, consistent editorial page header banner across
 *            all sub-pages featuring ambient parchment lighting, breadcrumbs, NCTB accreditation chips,
 *            stats bento metrics, authoritative Bengali typography, and responsive action button slots.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

import React from 'react';
import Link from 'next/link';
import { ChevronRight, ShieldCheck } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

export interface PageHeaderStat {
  label: string;
  value: string;
  highlight?: boolean;
}

export interface PageHeaderProps {
  title: string;
  description?: string;
  subtitle?: string;
  category?: string;
  badgeText?: string;
  badgeIcon?: React.ReactNode;
  breadcrumbs?: BreadcrumbItem[];
  stats?: PageHeaderStat[];
  action?: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
  children?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  subtitle,
  category,
  badgeText,
  badgeIcon = <ShieldCheck className="w-4 h-4 text-[#065F46] shrink-0" />,
  breadcrumbs,
  stats,
  action,
  actions,
  className,
  children,
}) => {
  const displayDesc = description || subtitle;
  const actionSlot = actions || action;

  return (
    <section
      className={cn(
        'relative overflow-hidden pt-8 pb-10 sm:pt-12 sm:pb-14 border-b border-slate-200/80 dark:border-slate-800/80 bg-white dark:bg-slate-950',
        className
      )}
    >
      {/* Ambient Academic Parchment / Linear Glow Lighting */}
      <div className="absolute top-0 right-1/4 w-80 h-80 rounded-full bg-blue-500/5 dark:bg-blue-500/10 blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-10 w-80 h-80 rounded-full bg-emerald-500/5 dark:bg-emerald-500/10 blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-5">
        {/* Breadcrumb Navigation */}
        {breadcrumbs && breadcrumbs.length > 0 && (
          <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 font-bengali">
            {breadcrumbs.map((crumb, idx) => {
              const isLast = idx === breadcrumbs.length - 1;
              return (
                <React.Fragment key={idx}>
                  {idx > 0 && <ChevronRight className="w-3.5 h-3.5 text-slate-400 dark:text-slate-600 shrink-0" />}
                  {isLast || !crumb.href ? (
                    <span className="font-semibold text-slate-900 dark:text-white" aria-current={isLast ? 'page' : undefined}>
                      {crumb.label}
                    </span>
                  ) : (
                    <Link
                      href={crumb.href}
                      className="hover:text-slate-900 dark:hover:text-white transition-colors"
                    >
                      {crumb.label}
                    </Link>
                  )}
                </React.Fragment>
              );
            })}
          </nav>
        )}

        {/* Top Chips & Accreditation Badge */}
        {(badgeText || category) && (
          <div className="flex flex-wrap items-center gap-2">
            {badgeText && (
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FAFAF8] dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300">
                {badgeIcon}
                <span>{badgeText}</span>
              </div>
            )}
            {category && (
              <span className="text-xs font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-mono">
                {category}
              </span>
            )}
          </div>
        )}

        {/* Headline & Description with Responsive Action Slot */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-black text-[#0A2540] dark:text-white tracking-tight font-bengali leading-snug">
              {title}
            </h1>
            {displayDesc && (
              <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
                {displayDesc}
              </p>
            )}
          </div>

          {actionSlot && (
            <div className="flex items-center gap-3 shrink-0 self-start lg:self-auto">
              {actionSlot}
            </div>
          )}
        </div>

        {/* Stats Bento Grid */}
        {stats && stats.length > 0 && (
          <div className="pt-2 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-bengali">
            {stats.map((s, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-2xl bg-slate-50/80 dark:bg-slate-900/80 border border-slate-200/80 dark:border-slate-800"
              >
                <span className="text-slate-500 dark:text-slate-400 block text-[11px] mb-0.5">{s.label}</span>
                <strong className={cn("text-sm sm:text-base font-bold", s.highlight ? "text-emerald-700 dark:text-amber-400" : "text-slate-900 dark:text-white")}>
                  {s.value}
                </strong>
              </div>
            ))}
          </div>
        )}

        {children}
      </div>
    </section>
  );
};
