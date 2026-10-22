/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Navigation Primitives
 * TOPIC:     Modern Academic Editorial Pagination Primitive
 * FILE:      frontend/src/components/ui/pagination.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible pagination controls with 44px minimum touch targets,
 *            bilingual numeral support (BN/EN), ellipsis windowing, and ARIA current page semantics.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React from 'react';
import { ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface PaginationProps extends React.HTMLAttributes<HTMLElement> {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  isBengali?: boolean;
  siblingCount?: number;
}

export const Pagination: React.FC<PaginationProps> = ({
  className,
  currentPage,
  totalPages,
  onPageChange,
  isBengali = true,
  siblingCount = 1,
  ...props
}) => {
  if (totalPages <= 1) return null;

  const toBengaliNumber = (num: number): string => {
    if (!isBengali) return num.toString();
    const bnDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
    return num.toString().split('').map(d => bnDigits[parseInt(d, 10)] || d).join('');
  };

  // Generate pagination range with ellipses
  const generateRange = (): (number | 'ellipsis')[] => {
    const totalNumbers = siblingCount * 2 + 3;
    const totalBlocks = totalNumbers + 2;

    if (totalPages <= totalBlocks) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    const startPage = Math.max(2, currentPage - siblingCount);
    const endPage = Math.min(totalPages - 1, currentPage + siblingCount);

    const hasLeftSpill = startPage > 2;
    const hasRightSpill = totalPages - endPage > 1;

    const pages: (number | 'ellipsis')[] = [1];

    if (hasLeftSpill) {
      pages.push('ellipsis');
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    if (hasRightSpill) {
      pages.push('ellipsis');
    }

    pages.push(totalPages);
    return pages;
  };

  const pages = generateRange();

  return (
    <nav
      aria-label={isBengali ? "পৃষ্ঠা পরিবর্তন" : "Pagination"}
      className={cn("flex items-center justify-center gap-1 sm:gap-1.5 select-none", className)}
      {...props}
    >
      <button
        type="button"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage <= 1}
        aria-label={isBengali ? "পূর্ববর্তী পৃষ্ঠা" : "Previous page"}
        className={cn(
          "inline-flex items-center justify-center rounded-lg border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D] text-[#1B2A4A] dark:text-[#F5F2EB]",
          "h-10 px-3 min-w-[40px] sm:min-w-[44px] sm:h-11 text-xs font-semibold transition-colors duration-150",
          "hover:bg-[#FAF8F3] dark:hover:bg-[#152035] hover:border-[#D1CDC4] dark:hover:border-[#3D475C]",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1B2A4A] dark:focus-visible:ring-sky-400",
          "disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-white dark:disabled:hover:bg-[#121B2D]"
        )}
      >
        <ChevronLeft className="w-4 h-4 mr-1" />
        <span className="hidden sm:inline font-sans">{isBengali ? "পূর্ববর্তী" : "Prev"}</span>
      </button>

      <div className="flex items-center gap-1">
        {pages.map((page, index) => {
          if (page === 'ellipsis') {
            return (
              <span
                key={`ellipsis-${index}`}
                className="inline-flex items-center justify-center w-8 h-10 text-[#5B5B5B] dark:text-slate-400"
                aria-hidden="true"
              >
                <MoreHorizontal className="w-4 h-4" />
              </span>
            );
          }

          const isActive = page === currentPage;

          return (
            <button
              key={page}
              type="button"
              onClick={() => onPageChange(page)}
              aria-current={isActive ? "page" : undefined}
              aria-label={isBengali ? `পৃষ্ঠা ${toBengaliNumber(page)}` : `Page ${page}`}
              className={cn(
                "inline-flex items-center justify-center rounded-lg h-10 w-10 sm:h-11 sm:w-11 min-h-[40px] sm:min-h-[44px] text-xs sm:text-sm font-semibold transition-colors duration-150 font-sans",
                isActive
                  ? "bg-[#1B2A4A] dark:bg-[#203660] text-white border border-[#1B2A4A] dark:border-[#203660]"
                  : "border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D] text-[#1A1A1A] dark:text-[#F5F2EB] hover:bg-[#FAF8F3] dark:hover:bg-[#152035] hover:border-[#D1CDC4]",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1B2A4A] dark:focus-visible:ring-sky-400"
              )}
            >
              {toBengaliNumber(page)}
            </button>
          );
        })}
      </div>

      <button
        type="button"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage >= totalPages}
        aria-label={isBengali ? "পরবর্তী পৃষ্ঠা" : "Next page"}
        className={cn(
          "inline-flex items-center justify-center rounded-lg border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D] text-[#1B2A4A] dark:text-[#F5F2EB]",
          "h-10 px-3 min-w-[40px] sm:min-w-[44px] sm:h-11 text-xs font-semibold transition-colors duration-150",
          "hover:bg-[#FAF8F3] dark:hover:bg-[#152035] hover:border-[#D1CDC4] dark:hover:border-[#3D475C]",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1B2A4A] dark:focus-visible:ring-sky-400",
          "disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-white dark:disabled:hover:bg-[#121B2D]"
        )}
      >
        <span className="hidden sm:inline font-sans">{isBengali ? "পরবর্তী" : "Next"}</span>
        <ChevronRight className="w-4 h-4 ml-1" />
      </button>
    </nav>
  );
};
