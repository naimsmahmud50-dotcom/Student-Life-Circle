/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Premium Sub-Page Architecture
 * TOPIC:     Modern Academic Editorial Page Header (Zero Glow, Serif Heading)
 * FILE:      frontend/src/components/layout/PageHeader.tsx
 * PHASE:     Phase 110 - Pure Academic Visual Design Elevation & Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Provides a dignified, consistent academic editorial page header banner across
 *            all sub-pages featuring breadcrumbs, NCTB accreditation chips, flat paper backgrounds,
 *            editorial serif headings, clean stats bento metrics, and responsive action button slots.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Zero-AI Glow, Modern Academic Editorial
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
        'relative pt-8 pb-10 sm:pt-12 sm:pb-14 border-b border-[#E5E2DA] dark:border-[#273145] bg-[#FAF8F3] dark:bg-[#12161F] transition-colors',
        className
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-5">
        {/* Breadcrumb Navigation */}
        {breadcrumbs && breadcrumbs.length > 0 && (
          <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali">
            {breadcrumbs.map((crumb, idx) => {
              const isLast = idx === breadcrumbs.length - 1;
              return (
                <React.Fragment key={idx}>
                  {idx > 0 && <ChevronRight className="w-3.5 h-3.5 text-[#787878] dark:text-slate-600 shrink-0" />}
                  {isLast || !crumb.href ? (
                    <span className="font-semibold text-[#1A1A1A] dark:text-white" aria-current={isLast ? 'page' : undefined}>
                      {crumb.label}
                    </span>
                  ) : (
                    <Link
                      href={crumb.href}
                      className="hover:text-[#1A1A1A] dark:hover:text-white transition-colors"
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
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white dark:bg-[#181E2B] border border-[#E5E2DA] dark:border-[#273145] text-xs font-semibold text-[#1A1A1A] dark:text-slate-300 shadow-xs">
                {badgeIcon}
                <span>{badgeText}</span>
              </div>
            )}
            {category && (
              <span className="text-xs font-semibold uppercase tracking-wider text-[#B8862B] dark:text-[#D4AF37] font-sans">
                {category}
              </span>
            )}
          </div>
        )}

        {/* Headline & Description with Responsive Action Slot */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] tracking-tight font-bengali leading-snug">
              {title}
            </h1>
            {displayDesc && (
              <p className="text-sm sm:text-base text-[#5B5B5B] dark:text-slate-300 leading-relaxed font-sans">
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
                className="p-3.5 rounded-xl bg-white dark:bg-[#181E2B] border border-[#E5E2DA] dark:border-[#273145] shadow-xs"
              >
                <span className="text-[#787878] dark:text-slate-400 block text-[11px] mb-0.5 font-sans">{s.label}</span>
                <strong className={cn("text-sm sm:text-base font-bold", s.highlight ? "text-[#065F46] dark:text-emerald-400" : "text-[#1A1A1A] dark:text-[#F5F2EB]")}>
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
