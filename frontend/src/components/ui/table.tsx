/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Data Display Primitives
 * TOPIC:     Modern Academic Editorial Textbook Table & List Primitives
 * FILE:      frontend/src/components/ui/table.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides textbook-like tabular presentation with hairline row borders (#E5E2DA),
 *            sticky table headers, zebra stripe options, and responsive stacked card view on mobile.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { forwardRef } from 'react';
import { cn } from '@/lib/utils';

export interface TableProps extends React.TableHTMLAttributes<HTMLTableElement> {
  stickyHeader?: boolean;
  striped?: boolean;
  responsiveStacked?: boolean;
}

export const Table = forwardRef<HTMLTableElement, TableProps>(
  ({ className, stickyHeader = false, striped = false, responsiveStacked = false, ...props }, ref) => (
    <div className={cn("w-full overflow-x-auto rounded-xl border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D]", responsiveStacked && "table-responsive-stack")}>
      <table
        ref={ref}
        className={cn(
          "w-full caption-bottom text-xs sm:text-sm font-sans border-collapse text-left",
          striped && "[&_tbody_tr:nth-child(even)]:bg-[#FAF8F3] dark:[&_tbody_tr:nth-child(even)]:bg-[#0E1526]/50",
          className
        )}
        {...props}
      />
    </div>
  )
);
Table.displayName = 'Table';

export const TableHeader = forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement> & { sticky?: boolean }
>(({ className, sticky = false, ...props }, ref) => (
  <thead
    ref={ref}
    className={cn(
      "border-b border-[#E5E2DA] dark:border-[#262D3D] bg-[#F5F2EB] dark:bg-[#0E1526] text-[#1B2A4A] dark:text-[#F5F2EB]",
      sticky && "sticky top-0 z-10",
      className
    )}
    {...props}
  />
));
TableHeader.displayName = 'TableHeader';

export const TableBody = forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("divide-y divide-[#E5E2DA] dark:divide-[#262D3D] text-[#1A1A1A] dark:text-slate-200", className)}
    {...props}
  />
));
TableBody.displayName = 'TableBody';

export const TableFooter = forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tfoot
    ref={ref}
    className={cn(
      "border-t border-[#E5E2DA] dark:border-[#262D3D] bg-[#FAF8F3] dark:bg-[#0E1526] font-semibold text-[#1B2A4A] dark:text-[#F5F2EB]",
      className
    )}
    {...props}
  />
));
TableFooter.displayName = 'TableFooter';

export const TableRow = forwardRef<
  HTMLTableRowElement,
  React.HTMLAttributes<HTMLTableRowElement>
>(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "transition-colors duration-100 hover:bg-[#FAF8F3] dark:hover:bg-[#152035]/60",
      className
    )}
    {...props}
  />
));
TableRow.displayName = 'TableRow';

export const TableHead = forwardRef<
  HTMLTableCellElement,
  React.ThHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      "h-11 px-4 text-left align-middle font-semibold text-xs text-[#1B2A4A] dark:text-[#F5F2EB] tracking-wider uppercase",
      className
    )}
    {...props}
  />
));
TableHead.displayName = 'TableHead';

export const TableCell = forwardRef<
  HTMLTableCellElement,
  React.TdHTMLAttributes<HTMLTableCellElement> & { dataLabel?: string }
>(({ className, dataLabel, children, ...props }, ref) => (
  <td
    ref={ref}
    data-label={dataLabel}
    className={cn(
      "p-4 align-middle text-xs sm:text-sm leading-relaxed",
      className
    )}
    {...props}
  >
    {children}
  </td>
));
TableCell.displayName = 'TableCell';
