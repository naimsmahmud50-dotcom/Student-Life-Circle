/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Disclosure Primitives
 * TOPIC:     Modern Academic Editorial Accordion Primitive
 * FILE:      frontend/src/components/ui/accordion.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible expandable/collapsible disclosure sections with WAI-ARIA
 *            attributes, 150-200ms calm ease-out transitions, and hairline border styling.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { createContext, useContext, useState, forwardRef } from 'react';
import { ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AccordionContextValue {
  expandedItems: string[];
  toggleItem: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

export interface AccordionProps extends React.HTMLAttributes<HTMLDivElement> {
  type?: 'single' | 'multiple';
  defaultValue?: string | string[];
  value?: string | string[];
  onValueChange?: (value: string | string[]) => void;
}

export const Accordion = forwardRef<HTMLDivElement, AccordionProps>(
  (
    {
      className,
      type = 'single',
      defaultValue,
      value: controlledValue,
      onValueChange,
      children,
      ...props
    },
    ref
  ) => {
    const [uncontrolledItems, setUncontrolledItems] = useState<string[]>(() => {
      if (defaultValue) return Array.isArray(defaultValue) ? defaultValue : [defaultValue];
      return [];
    });

    const isControlled = controlledValue !== undefined;
    const currentItems = isControlled
      ? Array.isArray(controlledValue) ? controlledValue : [controlledValue]
      : uncontrolledItems;

    const toggleItem = (id: string) => {
      let nextItems: string[];
      if (type === 'single') {
        nextItems = currentItems.includes(id) ? [] : [id];
      } else {
        nextItems = currentItems.includes(id)
          ? currentItems.filter((item) => item !== id)
          : [...currentItems, id];
      }

      if (!isControlled) setUncontrolledItems(nextItems);
      onValueChange?.(type === 'single' ? (nextItems[0] || '') : nextItems);
    };

    return (
      <AccordionContext.Provider value={{ expandedItems: currentItems, toggleItem }}>
        <div ref={ref} className={cn("divide-y divide-[#E5E2DA] dark:divide-[#262D3D] border-y border-[#E5E2DA] dark:border-[#262D3D]", className)} {...props}>
          {children}
        </div>
      </AccordionContext.Provider>
    );
  }
);
Accordion.displayName = 'Accordion';

export interface AccordionItemProps extends React.HTMLAttributes<HTMLDivElement> {
  value: string;
}

const AccordionItemContext = createContext<{ value: string; isExpanded: boolean } | null>(null);

export const AccordionItem = forwardRef<HTMLDivElement, AccordionItemProps>(
  ({ className, value, children, ...props }, ref) => {
    const context = useContext(AccordionContext);
    const isExpanded = context?.expandedItems.includes(value) ?? false;

    return (
      <AccordionItemContext.Provider value={{ value, isExpanded }}>
        <div ref={ref} className={cn("py-1", className)} {...props}>
          {children}
        </div>
      </AccordionItemContext.Provider>
    );
  }
);
AccordionItem.displayName = 'AccordionItem';

export interface AccordionTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export const AccordionTrigger = forwardRef<HTMLButtonElement, AccordionTriggerProps>(
  ({ className, children, ...props }, ref) => {
    const itemContext = useContext(AccordionItemContext);
    const accordionContext = useContext(AccordionContext);

    if (!itemContext) throw new Error('AccordionTrigger must be used inside AccordionItem');
    const { value, isExpanded } = itemContext;

    return (
      <h3>
        <button
          ref={ref}
          type="button"
          onClick={() => accordionContext?.toggleItem(value)}
          aria-expanded={isExpanded}
          aria-controls={`accordion-content-${value}`}
          className={cn(
            "flex w-full items-center justify-between py-3.5 text-left text-sm sm:text-base font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] font-serif transition-colors duration-150",
            "hover:text-[#0B5D3B] dark:hover:text-emerald-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1B2A4A] rounded-lg px-2 -mx-2 min-h-[44px]",
            className
          )}
          {...props}
        >
          <span>{children}</span>
          <ChevronDown
            className={cn(
              "w-4 h-4 shrink-0 text-[#5B5B5B] dark:text-slate-400 transition-transform duration-200 ease-out",
              isExpanded && "rotate-180 text-[#1B2A4A] dark:text-[#F5F2EB]"
            )}
            aria-hidden="true"
          />
        </button>
      </h3>
    );
  }
);
AccordionTrigger.displayName = 'AccordionTrigger';

export interface AccordionContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const AccordionContent = forwardRef<HTMLDivElement, AccordionContentProps>(
  ({ className, children, ...props }, ref) => {
    const itemContext = useContext(AccordionItemContext);
    if (!itemContext) throw new Error('AccordionContent must be used inside AccordionItem');
    const { value, isExpanded } = itemContext;

    if (!isExpanded) return null;

    return (
      <div
        ref={ref}
        id={`accordion-content-${value}`}
        role="region"
        className={cn(
          "pb-4 pt-1 text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-300 leading-relaxed font-sans animate-in fade-in-50 duration-150",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
AccordionContent.displayName = 'AccordionContent';
