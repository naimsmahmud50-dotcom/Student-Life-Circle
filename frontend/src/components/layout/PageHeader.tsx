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
 * ARCHITECTURE NOTE: Replaced legacy AI glow ambient orbs (blur-3xl) with crisp academic editorial surface borders.
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
  watermarkText?: string;
  watermarkGradient?: string;
  showGlow?: boolean;
  glowGradient?: string;
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
  watermarkText,
  watermarkGradient,
  showGlow = true,
  glowGradient,
}) => {
  const displayDesc = description || subtitle;
  const actionSlot = actions || action;

  return (
    <section
      className={cn(
        'relative pt-8 pb-10 sm:pt-12 sm:pb-14 border-b border-amber-200/60 dark:border-[#262D3D] bg-[#FFF6DD]/80 dark:bg-[#0B0F19] transition-colors overflow-hidden',
        className
      )}
    >
      {/* Background Radial Sunburst Glow (GoEdu Warm Design Language) */}
      {showGlow && (
        <div
          className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
          style={{
            height: '100%',
            minHeight: '260px',
            background:
              glowGradient ||
              'radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.45) 0%, rgba(243, 172, 8, 0.20) 45%, rgba(253, 215, 70, 0) 100%)'
          }}
          aria-hidden="true"
        />
      )}

      {/* Giant Typographic Watermark (GoEdu Signature Background Motif) */}
      {watermarkText && (
        <div
          className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
          aria-hidden="true"
        >
          <p
            className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,20vw,15rem)] uppercase tracking-wider select-none opacity-85"
            style={{
              lineHeight: 0.95,
              backgroundImage:
                watermarkGradient ||
                'linear-gradient(to bottom, rgba(243, 172, 8, 0.28) 15%, rgba(253, 215, 70, 0.02) 100%)'
            }}
          >
            {watermarkText}
          </p>
        </div>
      )}

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
                      className="hover:text-[#ED8E22] dark:hover:text-amber-300 transition-colors"
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
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] text-xs font-semibold text-[#1A1A1A] dark:text-slate-300 shadow-xs">
                {badgeIcon}
                <span>{badgeText}</span>
              </div>
            )}
            {category && (
              <span className="text-xs font-semibold uppercase tracking-wider text-[#ED8E22] dark:text-amber-400 font-sans">
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
                className="p-3.5 rounded-xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs"
              >
                <span className="text-[#787878] dark:text-slate-400 block text-[11px] mb-0.5 font-sans">{s.label}</span>
                <strong className={cn("text-sm sm:text-base font-bold", s.highlight ? "text-[#ED8E22] dark:text-amber-400" : "text-[#1B2A4A] dark:text-[#F5F2EB]")}>
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
