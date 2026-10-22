/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      frontend/src/components/pwa/OfflineIndicator.tsx
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   Provides real-time network connectivity status indicator with automatic
 *            reconnection feedback and direct access to offline study materials.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { WifiOff, CheckCircle2, ArrowRight } from 'lucide-react';

export function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [showReconnectedBadge, setShowReconnectedBadge] = useState<boolean>(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    setIsOnline(navigator.onLine);

    const handleOnline = () => {
      setIsOnline(true);
      setShowReconnectedBadge(true);
      const timer = setTimeout(() => {
        setShowReconnectedBadge(false);
      }, 4000);
      return () => clearTimeout(timer);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setShowReconnectedBadge(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Offline Warning Pill
  if (!isOnline) {
    return (
      <div
        role="status"
        aria-live="assertive"
        className="fixed top-16 left-1/2 -translate-x-1/2 z-50 px-4 py-2 rounded-full bg-[#0F172A]/95 border border-amber-500/40 shadow-xl backdrop-blur-md text-amber-300 text-xs sm:text-sm font-bengali flex items-center gap-2.5 animate-in fade-in slide-in-from-top-2 duration-200"
      >
        <WifiOff className="w-4 h-4 text-amber-400 animate-pulse shrink-0" />
        <span>অফলাইন মোড সক্রিয় • সংরক্ষিত বোর্ড প্রশ্ন উপলব্ধ</span>
        <Link
          href="/offline"
          className="ml-1 inline-flex items-center gap-1 font-semibold text-amber-200 hover:text-white underline underline-offset-2"
        >
          <span>স্টাডি এরিনা</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    );
  }

  // Brief Reconnected Notification
  if (showReconnectedBadge) {
    return (
      <div
        role="status"
        aria-live="polite"
        className="fixed top-16 left-1/2 -translate-x-1/2 z-50 px-4 py-2 rounded-full bg-[#0F172A]/95 border border-emerald-500/40 shadow-xl backdrop-blur-md text-emerald-300 text-xs sm:text-sm font-bengali flex items-center gap-2 animate-in fade-in slide-in-from-top-2 duration-200"
      >
        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
        <span>ইন্টারনেট সংযোগ পুনঃস্থাপিত হয়েছে • ডেটা সিঙ্ক সম্পন্ন</span>
      </div>
    );
  }

  return null;
}
