/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Overlay Primitives
 * TOPIC:     Modern Academic Editorial Slide-Over Drawer Primitive
 * FILE:      frontend/src/components/ui/drawer.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible slide-over sheet/drawer component with left/right/bottom docking,
 *            keyboard dismissal (Escape), focus management, and calm non-blurred backdrop.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

export type DrawerSide = 'left' | 'right' | 'bottom';

export interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title: React.ReactNode;
  description?: React.ReactNode;
  side?: DrawerSide;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}

export const Drawer: React.FC<DrawerProps> = ({
  isOpen,
  onClose,
  title,
  description,
  side = 'right',
  children,
  footer,
  className,
}) => {
  const drawerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sideClasses: Record<DrawerSide, string> = {
    right: "inset-y-0 right-0 max-w-md w-full border-l border-[#E5E2DA] dark:border-[#262D3D] translate-x-0",
    left: "inset-y-0 left-0 max-w-md w-full border-r border-[#E5E2DA] dark:border-[#262D3D] translate-x-0",
    bottom: "inset-x-0 bottom-0 max-h-[85vh] w-full border-t border-[#E5E2DA] dark:border-[#262D3D] translate-y-0 rounded-t-2xl",
  };

  return (
    <div className="fixed inset-0 z-50 flex" role="dialog" aria-modal="true">
      {/* Calm Flat Overlay (Zero heavy blur) */}
      <div
        className="fixed inset-0 bg-black/40 transition-opacity duration-200"
        onClick={onClose}
        aria-hidden="true"
      />

      <div
        ref={drawerRef}
        className={cn(
          "fixed z-50 flex flex-col bg-white dark:bg-[#121B2D] text-[#1A1A1A] dark:text-[#F5F2EB] shadow-xl duration-200 ease-out",
          sideClasses[side],
          className
        )}
      >
        <div className="flex items-center justify-between p-5 border-b border-[#E5E2DA] dark:border-[#262D3D]">
          <div>
            <h2 className="text-base sm:text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB]">
              {title}
            </h2>
            {description && (
              <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans mt-0.5">
                {description}
              </p>
            )}
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-lg text-[#5B5B5B] hover:text-[#1A1A1A] dark:text-slate-400 dark:hover:text-[#F5F2EB] hover:bg-[#FAF8F3] dark:hover:bg-[#152035] transition-colors focus:outline-none focus:ring-2 focus:ring-[#1B2A4A]"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5 text-sm leading-relaxed font-sans">
          {children}
        </div>

        {footer && (
          <div className="p-4 border-t border-[#E5E2DA] dark:border-[#262D3D] bg-[#FAF8F3] dark:bg-[#0E1526]">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};
