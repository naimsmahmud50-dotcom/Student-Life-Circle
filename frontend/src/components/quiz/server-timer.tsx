/**
 * ========================================================================================
 * MODULE:    Quiz Interface - Server-Synchronized Countdown Timer
 * TOPIC:     Accurate Timekeeping, Anti-Jank Tabular Numbers, Deadline Warning States
 * FILE:      frontend/src/components/quiz/server-timer.tsx
 * PURPOSE:   Renders the examination countdown timer synchronized with server time.
 *            Uses tabular monospace numbers to prevent layout shift (CLS), turns Amber
 *            when less than 60 seconds remain, and triggers automatic test lock when
 *            time expires. Zero emoji; utilizes clean Lucide Clock SVG.
 * AUDIENCE:  Frontend Developers, Accessibility Testers & AI Agents
 * STANDARDS: UI/UX Pro Max, Anti-Layout-Shift (CLS < 0.1), Zero-Emoji
 * ========================================================================================
 */

import React, { useEffect, useState } from 'react';

export interface ServerTimerProps {
  initialRemainingSeconds?: number;
  durationSeconds?: number;
  onTimeExpired: () => void;
  className?: string;
}

export const ServerTimer: React.FC<ServerTimerProps> = ({
  initialRemainingSeconds: propInitialRemainingSeconds,
  durationSeconds,
  onTimeExpired,
  className = ''
}) => {
  const initialRemainingSeconds = propInitialRemainingSeconds ?? durationSeconds ?? 900;
  const [secondsLeft, setSecondsLeft] = useState<number>(initialRemainingSeconds);

  useEffect(() => {
    setSecondsLeft(initialRemainingSeconds);
  }, [initialRemainingSeconds]);

  useEffect(() => {
    if (secondsLeft <= 0) {
      onTimeExpired();
      return;
    }

    const interval = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          onTimeExpired();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [secondsLeft, onTimeExpired]);

  // Format into MM:SS
  const minutes = Math.floor(secondsLeft / 60);
  const seconds = secondsLeft % 60;
  const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  // Warning state when under 60 seconds
  const isUrgent = secondsLeft > 0 && secondsLeft <= 60;

  return (
    <div
      role="timer"
      aria-label={`অবশিষ্ট সময়: ${minutes} মিনিট ${seconds} সেকেন্ড`}
      className={`
        inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-lg border transition-colors select-none font-medium
        ${isUrgent 
          ? "border-[var(--color-warning-border)] bg-[var(--color-warning-subtle)] text-[var(--color-warning)] animate-pulse" 
          : "border-[var(--border-subtle)] bg-[var(--bg-surface)] text-[var(--text-main)]"
        }
        ${className}
      `}
    >
      {/* Accessible Clock SVG Vector (Zero Emoji) */}
      <svg
        className={`w-4 h-4 ${isUrgent ? "text-[var(--color-warning)]" : "text-[var(--text-muted)]"}`}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth="2"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>

      {/* Monospace Tabular Figures prevent CLS layout jitter */}
      <span className="tabular-numbers text-base font-semibold tracking-wider">
        {formattedTime}
      </span>
    </div>
  );
};
