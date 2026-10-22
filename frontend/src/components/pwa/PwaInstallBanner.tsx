/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      frontend/src/components/pwa/PwaInstallBanner.tsx
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   Provides a refined, non-intrusive mobile install prompt with native
 *            beforeinstallprompt interception, offline benefits explanation, and dismissal memory.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import { Smartphone, Download, X } from 'lucide-react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
}

const STORAGE_KEY_DISMISSED = 'slc_pwa_install_dismissed_until';

export function PwaInstallBanner() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);
  const [isEngaged, setIsEngaged] = useState(false);

  useEffect(() => {
    // Check if dismissed recently (7 days dismissal memory)
    if (typeof window !== 'undefined') {
      const dismissedUntil = localStorage.getItem(STORAGE_KEY_DISMISSED);
      if (dismissedUntil && Date.now() < parseInt(dismissedUntil, 10)) {
        return;
      }
    }

    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Show only after meaningful engagement: scroll down or 15s session
    const handleScroll = () => {
      if (window.scrollY > 250) {
        setIsEngaged(true);
      }
    };

    const timer = setTimeout(() => {
      setIsEngaged(true);
    }, 15000);

    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('scroll', handleScroll);
      clearTimeout(timer);
    };
  }, []);

  useEffect(() => {
    if (deferredPrompt && isEngaged) {
      setIsVisible(true);
    }
  }, [deferredPrompt, isEngaged]);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    setIsInstalling(true);
    try {
      await deferredPrompt.prompt();
      const choiceResult = await deferredPrompt.userChoice;
      if (choiceResult.outcome === 'accepted') {
        setIsVisible(false);
      }
    } catch (err) {
      console.warn('[PWA Install] Error during prompt:', err);
    } finally {
      setIsInstalling(false);
      setDeferredPrompt(null);
    }
  };

  const handleDismiss = () => {
    setIsVisible(false);
    // Dismiss for 7 days
    if (typeof window !== 'undefined') {
      const cooldown = Date.now() + 7 * 24 * 60 * 60 * 1000;
      localStorage.setItem(STORAGE_KEY_DISMISSED, cooldown.toString());
    }
  };

  if (!isVisible || !deferredPrompt) {
    return null;
  }

  return (
    <aside
      aria-label="অফলাইন অ্যাপ ইনস্টলেশন ব্যানার"
      className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-md z-40 p-3 sm:p-3.5 rounded-xl bg-white dark:bg-[#181E2B] border border-[#E5E2DA] dark:border-[#273145] shadow-lg text-[#1A1A1A] dark:text-[#F5F2EB] animate-in fade-in slide-in-from-bottom-2 duration-200"
    >
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="p-2 rounded-lg bg-[#FAF8F3] dark:bg-[#202838] border border-[#E5E2DA] dark:border-[#273145] text-[#1B2A4A] dark:text-sky-400 shrink-0">
            <Smartphone className="w-4 h-4" strokeWidth={1.75} />
          </div>
          <div className="min-w-0">
            <h4 className="text-xs font-bold font-bengali text-[#1A1A1A] dark:text-[#F5F2EB] truncate flex items-center gap-1.5">
              <span>অগ্রযাত্রা অ্যাপ ইনস্টল</span>
              <span className="text-[10px] font-sans px-1 py-0.2 rounded bg-[#F5F2EB] dark:bg-slate-800 text-[#5B5B5B] dark:text-slate-300 border border-[#E5E2DA] dark:border-slate-700">
                PWA
              </span>
            </h4>
            <p className="text-[11px] text-[#5B5B5B] dark:text-slate-400 font-bengali truncate mt-0.5">
              অফলাইনে বোর্ড প্রশ্ন ও দ্রুত অ্যাক্সেস
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            onClick={handleInstallClick}
            disabled={isInstalling}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold font-bengali text-white bg-[#1B2A4A] hover:bg-[#253961] dark:bg-[#0A2540] rounded-lg shadow-xs active:translate-y-0.5 transition-all disabled:opacity-50"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isInstalling ? 'যুক্ত হচ্ছে...' : 'ইনস্টল'}</span>
          </button>
          <button
            type="button"
            onClick={handleDismiss}
            className="text-[#787878] hover:text-[#1A1A1A] dark:hover:text-white p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
            aria-label="ব্যানার বন্ধ করুন"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
