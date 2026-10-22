/**
 * ========================================================================================
 * MODULE:    Theme Control - Light & Dark Mode Toggle
 * TOPIC:     White Theme / Dark Theme Switcher with Accessible Vector Icons
 * FILE:      frontend/src/components/ui/theme-toggle.tsx
 * PURPOSE:   Provides user toggle between White (Light) and Midnight Slate (Dark) modes.
 *            Toggles the '.dark' CSS class on the root HTML element, persists choice
 *            in localStorage, respects system OS preferences, and utilizes crisp
 *            Sun and Moon SVG icons (strictly zero emoji).
 * AUDIENCE:  Frontend Developers, Accessibility Testers & UI Reviewers
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA, Zero-Emoji Governance
 * ========================================================================================
 */

import React, { useEffect, useState } from 'react';

export const ThemeToggle: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [isDark, setIsDark] = useState<boolean>(false);

  useEffect(() => {
    // Check local storage or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      setIsDark(true);
      document.documentElement.classList.add('dark');
    } else {
      setIsDark(false);
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      setIsDark(false);
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
      setIsDark(true);
    }
  };

  return (
    <button
      onClick={toggleTheme}
      type="button"
      aria-label={isDark ? "হালকা মোডে পরিবর্তন করুন" : "ডার্ক মোডে পরিবর্তন করুন"}
      title={isDark ? "হালকা মোড" : "ডার্ক মোড"}
      className={`inline-flex items-center justify-center w-10 h-10 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-surface)] text-[var(--text-main)] hover:bg-[var(--bg-surface-elevated)] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--focus-ring)] select-none ${className}`}
    >
      {isDark ? (
        // Clean Sun Vector SVG (Light Mode Trigger)
        <svg
          className="w-5 h-5 text-amber-400"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ) : (
        // Clean Moon Vector SVG (Dark Mode Trigger)
        <svg
          className="w-5 h-5 text-slate-700"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      )}
    </button>
  );
};
