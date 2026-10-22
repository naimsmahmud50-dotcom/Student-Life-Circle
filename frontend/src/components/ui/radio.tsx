/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Design System & Form Primitives
 * TOPIC:     Modern Academic Editorial Radio & RadioGroup Primitives
 * FILE:      frontend/src/components/ui/radio.tsx
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Provides accessible, high-contrast radio button group with keyboard navigation,
 *            helper text, inline error validation, and 44px touch target ergonomics.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

import React, { createContext, useContext, forwardRef } from 'react';
import { AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RadioGroupContextValue {
  name?: string;
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
}

const RadioGroupContext = createContext<RadioGroupContextValue | null>(null);

export interface RadioGroupProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'onChange'> {
  name?: string;
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
  label?: React.ReactNode;
  helperText?: React.ReactNode;
  error?: string;
  disabled?: boolean;
}

export const RadioGroup = forwardRef<HTMLDivElement, RadioGroupProps>(
  (
    {
      className,
      name,
      value: controlledValue,
      defaultValue,
      onChange,
      label,
      helperText,
      error,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const [uncontrolledValue, setUncontrolledValue] = React.useState(defaultValue || '');
    const isControlled = controlledValue !== undefined;
    const currentValue = isControlled ? controlledValue : uncontrolledValue;

    const handleChange = (newValue: string) => {
      if (!isControlled) setUncontrolledValue(newValue);
      onChange?.(newValue);
    };

    return (
      <div ref={ref} role="radiogroup" className={cn("space-y-2", className)} {...props}>
        {label && (
          <div className="text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] font-sans">
            {label}
          </div>
        )}
        <RadioGroupContext.Provider
          value={{
            name,
            value: currentValue,
            onChange: handleChange,
            disabled,
          }}
        >
          <div className="space-y-1">{children}</div>
        </RadioGroupContext.Provider>

        {error && (
          <div className="flex items-center gap-1.5 text-xs text-red-600 dark:text-red-400 font-medium pt-1">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {!error && helperText && (
          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans pt-0.5">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);
RadioGroup.displayName = 'RadioGroup';

export interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  value: string;
  label?: React.ReactNode;
  helperText?: React.ReactNode;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export const Radio = forwardRef<HTMLInputElement, RadioProps>(
  (
    {
      className,
      value,
      label,
      helperText,
      disabled: itemDisabled,
      id,
      onChange: itemOnChange,
      ...props
    },
    ref
  ) => {
    const context = useContext(RadioGroupContext);
    const disabled = itemDisabled || context?.disabled;
    const isChecked = context?.value !== undefined ? context.value === value : props.checked;
    const radioId = id || `radio-${value}-${Math.random().toString(36).substring(2, 7)}`;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      itemOnChange?.(e);
      context?.onChange?.(value);
    };

    return (
      <label
        htmlFor={radioId}
        className={cn(
          "inline-flex items-start gap-3 min-h-[44px] cursor-pointer select-none py-1.5",
          disabled && "cursor-not-allowed opacity-50",
          className
        )}
      >
        <div className="relative flex items-center justify-center shrink-0 mt-0.5">
          <input
            id={radioId}
            type="radio"
            ref={ref}
            name={context?.name}
            value={value}
            checked={isChecked}
            disabled={disabled}
            onChange={handleChange}
            className="peer sr-only"
            {...props}
          />
          <div
            className={cn(
              "w-5 h-5 rounded-full border border-[#E5E2DA] dark:border-[#262D3D] bg-white dark:bg-[#121B2D] transition-colors duration-150 flex items-center justify-center",
              "peer-focus-visible:ring-2 peer-focus-visible:ring-[#1B2A4A] dark:peer-focus-visible:ring-sky-400 peer-focus-visible:ring-offset-2",
              "peer-hover:border-[#D1CDC4] dark:peer-hover:border-[#3D475C]",
              "peer-checked:border-[#1B2A4A] dark:peer-checked:border-[#3B82F6]"
            )}
          >
            {isChecked && (
              <span className="w-2.5 h-2.5 rounded-full bg-[#1B2A4A] dark:bg-sky-400" />
            )}
          </div>
        </div>

        {(label || helperText) && (
          <div className="flex flex-col text-xs sm:text-sm">
            {label && (
              <span className="font-semibold text-[#1A1A1A] dark:text-[#F5F2EB] font-sans">
                {label}
              </span>
            )}
            {helperText && (
              <span className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans mt-0.5">
                {helperText}
              </span>
            )}
          </div>
        )}
      </label>
    );
  }
);
Radio.displayName = 'Radio';
