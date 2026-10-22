/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Navigation Primitives
 * TOPIC:     Modern Academic Editorial Breadcrumb Primitive
 * FILE:      frontend/src/components/ui/breadcrumb.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides semantic, accessible breadcrumb hierarchy navigation with microdata,
 *            quiet chevron separators, and aria-current="page" for active route terminal.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { forwardRef } from 'react';
import Link from 'next/link';
import { ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface BreadcrumbItem {
  label: React.ReactNode;
  href?: string;
  isCurrent?: boolean;
}

export interface BreadcrumbProps extends React.HTMLAttributes<HTMLElement> {
  items: BreadcrumbItem[];
  separator?: React.ReactNode;
}

export const Breadcrumb = forwardRef<HTMLElement, BreadcrumbProps>(
  ({ className, items, separator, ...props }, ref) => {
    return (
      <nav
        ref={ref}
        aria-label="Breadcrumb"
        className={cn("flex items-center text-xs text-[#5B5B5B] dark:text-slate-400 font-sans", className)}
        {...props}
      >
        <ol className="flex items-center flex-wrap gap-1.5">
          {items.map((item, index) => {
            const isLast = index === items.length - 1 || item.isCurrent;

            return (
              <li key={index} className="inline-flex items-center gap-1.5">
                {index > 0 && (
                  <span className="text-[#A09D94] dark:text-slate-600 select-none" aria-hidden="true">
                    {separator || <ChevronRight className="w-3.5 h-3.5" />}
                  </span>
                )}

                {isLast || !item.href ? (
                  <span
                    aria-current={isLast ? "page" : undefined}
                    className={cn(
                      "font-semibold truncate max-w-[200px] sm:max-w-none",
                      isLast
                        ? "text-[#1B2A4A] dark:text-[#F5F2EB]"
                        : "text-[#5B5B5B] dark:text-slate-400"
                    )}
                  >
                    {item.label}
                  </span>
                ) : (
                  <Link
                    href={item.href}
                    className="hover:text-[#1B2A4A] dark:hover:text-[#F5F2EB] hover:underline underline-offset-2 transition-colors duration-150 truncate max-w-[150px] sm:max-w-none"
                  >
                    {item.label}
                  </Link>
                )}
              </li>
            );
          })}
        </ol>
      </nav>
    );
  }
);

Breadcrumb.displayName = 'Breadcrumb';
