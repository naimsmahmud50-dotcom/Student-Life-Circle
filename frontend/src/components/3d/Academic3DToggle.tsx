/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic 3D & Depth Mode User Preference Toggle
 * FILE:      frontend/src/components/3d/Academic3DToggle.tsx
 * PURPOSE:   Provides an intuitive, accessible institutional toggle button:
 *            Allows students to toggle between the 3D Real-time Academic World
 *            and the calm 2D High-Contrast Layered Monograph. Persisted in localStorage.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Tactile Physics, Pure Academic Ink.
 */

import React from 'react';
import { Box, Layers, ZapOff, RefreshCw } from 'lucide-react';
import { use3DCapability } from './use3DCapability';

interface Academic3DToggleProps {
  compact?: boolean;
  className?: string;
}

export const Academic3DToggle: React.FC<Academic3DToggleProps> = ({
  compact = false,
  className = '',
}) => {
  const {
    isClient,
    is3DSupported,
    is3DAllowed,
    isDegraded,
    userPreference,
    rollingFps,
    reason,
    toggle3D,
    resetDegradation,
  } = use3DCapability();

  if (!isClient) {
    return null;
  }

  // If device doesn't support WebGL at all
  if (!is3DSupported) {
    return (
      <div
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#F5F2EB] dark:bg-[#162032] border border-[#E2DDD3] dark:border-[#263147] text-[11px] font-semibold text-[#5A687D] dark:text-[#94A3B8] ${className}`}
        title="এই ব্রাউজারে ৩ডি হার্ডওয়্যার এক্সিলারেশন সক্রিয় নয়"
      >
        <ZapOff className="w-3.5 h-3.5 text-amber-700 dark:text-amber-400" />
        <span>দ্বিমাত্রিক মোড</span>
      </div>
    );
  }

  return (
    <div className={`inline-flex items-center gap-2 ${className}`}>
      <button
        type="button"
        role="switch"
        aria-checked={is3DAllowed}
        aria-label="ত্রিমাত্রিক ৩ডি ভিজুয়ালাইজেশন নিয়ন্ত্রণ"
        onClick={toggle3D}
        title={`দৃশ্যপট মোড পরিবর্তন: ${reason} (ক্লিক করুন)`}
        className={`btn-tactile-outline inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold select-none transition-all cursor-pointer ${
          is3DAllowed
            ? 'bg-[#F0EDE6] dark:bg-[#172030] border-emerald-600/40 dark:border-emerald-500/40 text-emerald-900 dark:text-emerald-300'
            : 'bg-[#FDFCF9] dark:bg-[#111827] border-[#E5E2DA] dark:border-[#263147] text-[#5A687D] dark:text-[#94A3B8]'
        }`}
      >
        {is3DAllowed ? (
          <Box className="w-3.5 h-3.5 text-emerald-700 dark:text-emerald-400" />
        ) : (
          <Layers className="w-3.5 h-3.5 text-[#5A687D] dark:text-[#94A3B8]" />
        )}

        <span>{is3DAllowed ? '৩ডি গভীরতা: সক্রিয়' : '২ডি মোড: সক্রিয়'}</span>

        {is3DAllowed && rollingFps > 0 && !compact && (
          <span className="font-mono text-[10px] px-1.5 py-0.2 rounded bg-emerald-700/10 dark:bg-emerald-400/10 text-emerald-800 dark:text-emerald-300">
            {Math.round(rollingFps)} FPS
          </span>
        )}
      </button>

      {isDegraded && (
        <button
          type="button"
          onClick={resetDegradation}
          title="স্বয়ংক্রিয় ডাউনগ্রেড রিসেট করে পুনরায় ৩ডি চালু করুন"
          className="p-1 rounded-md text-amber-700 dark:text-amber-400 hover:bg-amber-100 dark:hover:bg-amber-950/50 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
};
