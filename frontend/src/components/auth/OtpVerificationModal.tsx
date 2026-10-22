/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - AUTH & SECURITY UI:
 * MODULE:    SMS OTP Verification Modal Primitive
 * TOPIC:     6-Digit Auto-Focus Grid, 180s Cooldown Timer & Anti-SMS Bombing Feedback
 * FILE:      frontend/src/components/auth/OtpVerificationModal.tsx
 * PURPOSE:   Provides an accessible, human-centric modal for entering 6-digit SMS OTP
 *            codes. Enforces WCAG 2.2 AA contrast standards, >= 44px touch targets,
 *            single-digit auto-advancing input cells, countdown timer with resend rate
 *            limit notices, and strict ZERO-EMOJI compliance using Lucide SVG icons.
 * AUDIENCE:  Frontend Engineers, Security Auditors & Accessibility Reviewers
 * STANDARDS: UI/UX Pro Max, ASVS L2 Authentication, WCAG 2.2 AA
 * ========================================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  ShieldCheck, 
  Smartphone, 
  RefreshCw, 
  AlertCircle, 
  CheckCircle2, 
  X, 
  Loader2 
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export interface OtpVerificationModalProps {
  isOpen: boolean;
  phone: string;
  purpose?: string;
  onClose: () => void;
  onVerifySuccess: (result: { phone: string; user_id?: string }) => void;
  onResendOtp?: () => Promise<{ success: boolean; message?: string }>;
}

export const OtpVerificationModal: React.FC<OtpVerificationModalProps> = ({
  isOpen,
  phone,
  purpose = 'LOGIN',
  onClose,
  onVerifySuccess,
  onResendOtp
}) => {
  const [digits, setDigits] = useState<string[]>(['', '', '', '', '', '']);
  const [countdown, setCountdown] = useState<number>(180); // 3 minutes
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [attemptsRemaining, setAttemptsRemaining] = useState<number>(3);

  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // 180s Countdown Timer effect
  useEffect(() => {
    if (!isOpen) return;
    setCountdown(180);
    setDigits(['', '', '', '', '', '']);
    setErrorMessage(null);
    setSuccessMessage(null);

    const timer = setInterval(() => {
      setCountdown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timer);
  }, [isOpen]);

  // Focus first input on open
  useEffect(() => {
    if (isOpen && inputRefs.current[0]) {
      setTimeout(() => inputRefs.current[0]?.focus(), 100);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleDigitChange = (index: number, value: string) => {
    // Only accept numeric single digit
    const cleaned = value.replace(/\D/g, '');
    if (!cleaned) {
      const nextDigits = [...digits];
      nextDigits[index] = '';
      setDigits(nextDigits);
      return;
    }

    const char = cleaned.slice(-1);
    const nextDigits = [...digits];
    nextDigits[index] = char;
    setDigits(nextDigits);

    // Auto-advance to next input
    if (index < 5 && char) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !digits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent<HTMLInputElement>) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    if (pasted.length > 0) {
      const nextDigits = [...digits];
      for (let i = 0; i < 6; i++) {
        nextDigits[i] = pasted[i] || '';
      }
      setDigits(nextDigits);
      const focusIndex = Math.min(pasted.length, 5);
      inputRefs.current[focusIndex]?.focus();
    }
  };

  const handleVerify = async () => {
    const otpCode = digits.join('');
    if (otpCode.length < 6) {
      setErrorMessage('Please enter all 6 digits of the verification code.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const response = await fetch('/api/v1/auth-otp/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, otp: otpCode, purpose })
      });

      const data = await response.json();
      if (!response.ok) {
        setErrorMessage(data.detail || 'Verification code failed. Please check and retry.');
        if (data.attempts_remaining !== undefined) {
          setAttemptsRemaining(data.attempts_remaining);
        }
      } else {
        setSuccessMessage('Code verified successfully.');
        setTimeout(() => {
          onVerifySuccess(data);
          onClose();
        }, 600);
      }
    } catch {
      setErrorMessage('Network connection error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResend = async () => {
    if (countdown > 0) return;
    setIsLoading(true);
    setErrorMessage(null);

    try {
      if (onResendOtp) {
        const res = await onResendOtp();
        if (res.success) {
          setCountdown(180);
          setDigits(['', '', '', '', '', '']);
          setSuccessMessage('New verification code sent via SMS.');
        } else {
          setErrorMessage(res.message || 'Failed to resend code.');
        }
      } else {
        const res = await fetch('/api/v1/auth-otp/send', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ phone, purpose })
        });
        const data = await res.json();
        if (!res.ok) {
          setErrorMessage(data.detail || 'Rate limit reached. Please wait.');
        } else {
          setCountdown(180);
          setDigits(['', '', '', '', '', '']);
          setSuccessMessage('New verification code sent via SMS.');
        }
      }
    } catch {
      setErrorMessage('Failed to connect to SMS service.');
    } finally {
      setIsLoading(false);
    }
  };

  const minutes = Math.floor(countdown / 60);
  const seconds = countdown % 60;
  const timeFormatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 p-4">
      <div 
        className="w-full max-w-md rounded-2xl bg-white border border-slate-200 shadow-xl overflow-hidden transition-all duration-200 animate-in fade-in zoom-in-95"
        role="dialog"
        aria-modal="true"
        aria-labelledby="otp-dialog-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center space-x-2 text-slate-900 font-semibold text-lg">
            <ShieldCheck className="w-5 h-5 text-blue-600" aria-hidden="true" />
            <span id="otp-dialog-title">SMS Verification</span>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6">
          <div className="text-center space-y-2">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-blue-50 text-blue-600 mb-1">
              <Smartphone className="w-6 h-6" aria-hidden="true" />
            </div>
            <h3 className="text-base font-semibold text-slate-800">
              Enter 6-Digit Verification Code
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed max-w-xs mx-auto">
              A 6-digit code has been dispatched to{' '}
              <span className="font-semibold text-slate-700 font-mono">{phone}</span>
            </p>
          </div>

          {/* 6 Digit Input Grid */}
          <div className="flex justify-center space-x-2 sm:space-x-3" onPaste={handlePaste}>
            {digits.map((digit, idx) => (
              <input
                key={idx}
                ref={(el) => {
                  inputRefs.current[idx] = el;
                }}
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                maxLength={1}
                value={digit}
                onChange={(e) => handleDigitChange(idx, e.target.value)}
                onKeyDown={(e) => handleKeyDown(idx, e)}
                className="w-11 h-14 sm:w-12 sm:h-14 text-center text-xl font-bold font-mono text-slate-900 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-100 outline-none transition-all duration-150"
                aria-label={`Digit ${idx + 1}`}
              />
            ))}
          </div>

          {/* Error & Success Feedback Banners */}
          {errorMessage && (
            <div className="flex items-start space-x-2 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-500" />
              <div className="flex-1 font-medium">{errorMessage}</div>
            </div>
          )}

          {successMessage && (
            <div className="flex items-center space-x-2 p-3 rounded-lg bg-teal-50 border border-teal-200 text-teal-800 text-xs font-medium">
              <CheckCircle2 className="w-4 h-4 shrink-0 text-teal-600" />
              <span>{successMessage}</span>
            </div>
          )}

          {/* Verification Action */}
          <Button
            variant="brand"
            fullWidth
            isLoading={isLoading}
            onClick={handleVerify}
            disabled={digits.some((d) => !d) || isLoading}
            className="h-11 text-sm font-semibold shadow-sm"
          >
            Verify Code
          </Button>

          {/* Cooldown Timer & Resend Controls */}
          <div className="flex flex-col items-center justify-center space-y-2 pt-2 border-t border-slate-100 text-xs text-slate-500">
            {countdown > 0 ? (
              <p>
                Code expires in{' '}
                <span className="font-mono font-semibold text-slate-700">{timeFormatted}</span>
              </p>
            ) : (
              <div className="flex items-center space-x-1">
                <span>Did not receive code?</span>
                <button
                  onClick={handleResend}
                  disabled={isLoading}
                  className="font-semibold text-blue-600 hover:text-blue-700 inline-flex items-center space-x-1 focus:outline-none"
                >
                  <RefreshCw className="w-3 h-3" />
                  <span>Resend Code</span>
                </button>
              </div>
            )}
            <p className="text-[11px] text-slate-400">
              Anti-SMS bombing limit: Max 3 requests per 15 minutes.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
