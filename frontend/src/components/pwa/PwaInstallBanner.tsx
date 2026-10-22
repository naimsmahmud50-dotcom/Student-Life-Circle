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
import { Smartphone, Download, X, CheckCircle2 } from 'lucide-react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
}

const STORAGE_KEY_DISMISSED = 'slc_pwa_install_dismissed_until';

export function PwaInstallBanner() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);

  useEffect(() => {
    // Check if dismissed recently (e.g. within 3 days)
    if (typeof window !== 'undefined') {
      const dismissedUntil = localStorage.getItem(STORAGE_KEY_DISMISSED);
      if (dismissedUntil && Date.now() < parseInt(dismissedUntil, 10)) {
        return;
      }
    }

    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setIsVisible(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

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
    // Dismiss for 3 days
    if (typeof window !== 'undefined') {
      const cooldown = Date.now() + 3 * 24 * 60 * 60 * 1000;
      localStorage.setItem(STORAGE_KEY_DISMISSED, cooldown.toString());
    }
  };

  if (!isVisible || !deferredPrompt) {
    return null;
  }

  return (
    <aside
      aria-label="অফলাইন অ্যাপ ইনস্টলেশন ব্যানার"
      className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-md z-40 p-4 rounded-2xl bg-[#090D16] border border-blue-500/30 shadow-[0_8px_30px_rgb(0,0,0,0.6)] text-slate-100 backdrop-blur-md animate-in fade-in slide-in-from-bottom-3 duration-200"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400 shrink-0">
            <Smartphone className="w-5 h-5" strokeWidth={1.75} />
          </div>
          <div>
            <h4 className="text-sm font-bold font-bengali text-white flex items-center gap-1.5">
              <span>অগ্রযাত্রা অ্যাপ ইনস্টল করুন</span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                PWA
              </span>
            </h4>
            <p className="text-xs text-slate-400 font-bengali leading-relaxed mt-0.5">
              নেটওয়ার্ক ছাড়াই সংরক্ষিত বোর্ড প্রশ্ন ও অনুশীলন সেটে দ্রুততম প্রবেশাধিকার পান।
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleDismiss}
          className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          aria-label="ব্যানার বন্ধ করুন"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="flex items-center justify-between pt-3 mt-2 border-t border-slate-800">
        <div className="flex items-center gap-1.5 text-[11px] text-slate-400 font-bengali">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
          <span>অফলাইন ব্যাকআপ সক্রিয়</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleDismiss}
            className="px-2.5 py-1 text-xs font-bengali text-slate-400 hover:text-slate-200 transition-colors"
          >
            পরে
          </button>
          <button
            type="button"
            onClick={handleInstallClick}
            disabled={isInstalling}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold font-bengali text-white bg-blue-600 hover:bg-blue-500 rounded-xl shadow-[0_2px_0_0_#1D4ED8] active:translate-y-0.5 active:shadow-none transition-all disabled:opacity-50"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isInstalling ? 'যুক্ত হচ্ছে...' : 'হোমস্ক্রিনে যুক্ত করুন'}</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
