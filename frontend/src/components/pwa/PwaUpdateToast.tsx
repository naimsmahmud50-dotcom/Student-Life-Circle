/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      frontend/src/components/pwa/PwaUpdateToast.tsx
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   Renders a dignified, accessible update toast when a new Service Worker
 *            version is waiting, enabling one-tap instant reloading without data loss.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import { RefreshCw, Sparkles, X } from 'lucide-react';

export interface PwaUpdateToastProps {
  registration?: ServiceWorkerRegistration | null;
}

export function PwaUpdateToast({ registration }: PwaUpdateToastProps) {
  const [showToast, setShowToast] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    if (!registration) {
      return;
    }

    // Check if there is already a waiting service worker
    if (registration.waiting) {
      setShowToast(true);
    }

    // Listen for updates found during runtime
    const handleUpdateFound = () => {
      const installingWorker = registration.installing;
      if (!installingWorker) return;

      installingWorker.onstatechange = () => {
        if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
          setShowToast(true);
        }
      };
    };

    registration.addEventListener('updatefound', handleUpdateFound);

    return () => {
      registration.removeEventListener('updatefound', handleUpdateFound);
    };
  }, [registration]);

  const handleApplyUpdate = () => {
    setIsUpdating(true);
    if (registration?.waiting) {
      registration.waiting.postMessage({ type: 'SKIP_WAITING' });
    }

    // When controller changes, reload the window to run new code
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      window.location.reload();
    });

    // Fallback reload if controllerchange is already triggered
    setTimeout(() => {
      window.location.reload();
    }, 600);
  };

  const handleDismiss = () => {
    setShowToast(false);
  };

  if (!showToast) {
    return null;
  }

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed bottom-5 right-5 z-50 max-w-sm w-full p-4 rounded-2xl bg-[#0F172A] border border-slate-700/80 shadow-2xl text-slate-100 flex flex-col gap-3 animate-in fade-in slide-in-from-bottom-4 duration-200"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 shrink-0">
            <Sparkles className="w-4 h-4" strokeWidth={2} />
          </div>
          <div>
            <h4 className="text-sm font-semibold font-bengali text-white">
              অগ্রযাত্রার নতুন সংস্করণ উপলব্ধ
            </h4>
            <p className="text-xs text-slate-400 font-bengali leading-relaxed mt-0.5">
              উন্নত গতি ও নতুন একাডেমিক ফিচারের জন্য রিলোড করুন।
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={handleDismiss}
          className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          aria-label="বিজ্ঞপ্তি বন্ধ করুন"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="flex items-center justify-end gap-2 pt-1 border-t border-slate-800">
        <button
          type="button"
          onClick={handleDismiss}
          className="px-3 py-1.5 text-xs font-bengali text-slate-400 hover:text-slate-200 transition-colors"
        >
          পরে
        </button>
        <button
          type="button"
          onClick={handleApplyUpdate}
          disabled={isUpdating}
          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold font-bengali text-white bg-blue-600 hover:bg-blue-500 rounded-xl shadow-[0_2px_0_0_#1D4ED8] active:translate-y-0.5 active:shadow-none transition-all disabled:opacity-60"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isUpdating ? 'animate-spin' : ''}`} />
          <span>{isUpdating ? 'আপডেট হচ্ছে...' : 'এখনই আপডেট করুন'}</span>
        </button>
      </div>
    </div>
  );
}
