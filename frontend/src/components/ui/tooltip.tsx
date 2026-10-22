/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Overlay Primitives
 * TOPIC:     Modern Academic Editorial Tooltip Primitive
 * FILE:      frontend/src/components/ui/tooltip.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible tooltip component with hover and focus trigger support,
 *            role="tooltip", aria-describedby binding, and calm academic styling.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { useState, useRef, useId } from 'react';
import { cn } from '@/lib/utils';

export interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  position?: 'top' | 'bottom' | 'left' | 'right';
  className?: string;
  delay?: number;
}

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  position = 'top',
  className,
  delay = 200,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const tooltipId = useId();

  const handleMouseEnter = () => {
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  };

  const handleMouseLeave = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setIsVisible(false);
  };

  const positionClasses: Record<'top' | 'bottom' | 'left' | 'right', string> = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  return (
    <div
      className="relative inline-flex"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      {React.cloneElement(children as React.ReactElement<any>, {
        'aria-describedby': isVisible ? tooltipId : undefined,
      })}

      {isVisible && content && (
        <div
          id={tooltipId}
          role="tooltip"
          className={cn(
            "absolute z-50 px-2.5 py-1 text-xs font-medium text-white bg-[#1B2A4A] dark:bg-[#0E1526] dark:border dark:border-[#262D3D] rounded-md shadow-sm pointer-events-none whitespace-nowrap animate-in fade-in-0 duration-150",
            positionClasses[position],
            className
          )}
        >
          {content}
        </div>
      )}
    </div>
  );
};
