/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      frontend/src/pages/_app.tsx
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   Root entrypoint wrapping all Next.js page components with PWA Service Worker lifecycle,
 *            PwaUpdateToast, PwaInstallBanner, OfflineIndicator, global theme synchronization,
 *            and the persistent Socratic AI Drawer.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import type { AppProps } from 'next/app';
import { Sparkles, WifiOff, Wifi, X } from 'lucide-react';
import { I18nProvider, useTranslation } from '@/lib/i18n';
import { SocraticTutorDrawer } from '@/components/ai/SocraticTutorDrawer';
import { PwaUpdateToast, PwaInstallBanner, OfflineIndicator } from '@/components/pwa';
import '../styles/globals.css';

interface OfflineToastState {
  show: boolean;
  status: 'offline' | 'online';
  message: string;
}

/**
 * Inner shell component residing inside I18nProvider, capable of consuming translation
 * and managing floating global widgets.
 */
function GlobalAppShell({ Component, pageProps }: AppProps) {
  const { isBengali } = useTranslation();
  const [isTutorOpen, setIsTutorOpen] = useState(false);
  const [swRegistration, setSwRegistration] = useState<ServiceWorkerRegistration | null>(null);
  const [offlineToast, setOfflineToast] = useState<OfflineToastState>({
    show: false,
    status: 'online',
    message: '',
  });

  // ---------------------------------------------------------------------------
  // 1. Service Worker Lifecycle (Runs once on mount in production)
  // ---------------------------------------------------------------------------
  useEffect(() => {
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      if (process.env.NODE_ENV === 'production') {
        const handleLoad = () => {
          navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
              setSwRegistration(registration);
            })
            .catch((err) => {
              console.warn('PWA Service Worker registration non-fatal error:', err);
            });
        };

        if (document.readyState === 'complete') {
          handleLoad();
        } else {
          window.addEventListener('load', handleLoad);
          return () => window.removeEventListener('load', handleLoad);
        }
      }
    }
  }, []);

  // ---------------------------------------------------------------------------
  // 2. Offline Connectivity Event Listeners
  // ---------------------------------------------------------------------------
  useEffect(() => {
    let timer: NodeJS.Timeout | null = null;

    const handleOffline = () => {
      setOfflineToast({
        show: true,
        status: 'offline',
        message: isBengali
          ? 'ইন্টারনেট সংযোগ বিচ্ছিন্ন। অফলাইন সিঙ্ক ও ক্যাশড কন্টেন্ট সক্রিয় রয়েছে।'
          : 'Internet disconnected. Offline sync and cached study materials are active.',
      });
    };

    const handleOnline = () => {
      setOfflineToast({
        show: true,
        status: 'online',
        message: isBengali
          ? 'ইন্টারনেট সংযোগ পুনঃস্থাপিত হয়েছে।'
          : 'Internet connection restored successfully.',
      });

      timer = setTimeout(() => {
        setOfflineToast((prev) => ({ ...prev, show: false }));
      }, 4000);
    };

    window.addEventListener('offline', handleOffline);
    window.addEventListener('online', handleOnline);

    return () => {
      if (timer) clearTimeout(timer);
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('online', handleOnline);
    };
  }, [isBengali]);

  // ---------------------------------------------------------------------------
  // 3. Global Dark / Light Theme Synchronization (Light = Default)
  // ---------------------------------------------------------------------------
  useEffect(() => {
    try {
      const savedTheme = localStorage.getItem('slc_theme');
      if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        // Light paper theme is the default
        document.documentElement.classList.remove('dark');
      }
    } catch (e) {
      // LocalStorage access non-blocking catch
    }
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-app)] text-[var(--text-main)] font-sans selection:bg-[var(--primary)] selection:text-white">
      {/* Real-time PWA Offline & Status Indicators */}
      <OfflineIndicator />
      <PwaUpdateToast registration={swRegistration} />
      <PwaInstallBanner />

      {/* Legacy Offline / Reconnection Alert Toast Banner */}
      {offlineToast.show && (
        <div
          role="status"
          aria-live="polite"
          className={`fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium shadow-md border transition-all duration-300 animate-in fade-in slide-in-from-top-4 ${
            offlineToast.status === 'offline'
              ? 'bg-[#FEF3C7] text-[#92400E] border-[#FDE68A]'
              : 'bg-[#ECFDF5] text-[#065F46] border-[#A7F3D0]'
          }`}
        >
          {offlineToast.status === 'offline' ? (
            <WifiOff className="w-4 h-4 text-[#B45309] shrink-0" />
          ) : (
            <Wifi className="w-4 h-4 text-[#065F46] shrink-0" />
          )}
          <span>{offlineToast.message}</span>
          <button
            type="button"
            onClick={() => setOfflineToast((prev) => ({ ...prev, show: false }))}
            className="ml-2 p-1 rounded-md hover:bg-black/5 text-[#5B5B5B] transition"
            aria-label="বার্তাটি বন্ধ করুন"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Main Page Component View */}
      <main className="flex-1 w-full flex flex-col">
        <Component {...pageProps} />
      </main>

      {/* Persistent Floating Socratic AI Tutor Trigger Button (Pure Academic Style) */}
      <div className="fixed bottom-6 right-6 z-40 print:hidden">
        <button
          id="global-socratic-trigger"
          type="button"
          onClick={() => setIsTutorOpen(true)}
          aria-expanded={isTutorOpen}
          aria-label={
            isBengali
              ? 'সক্রেটিক এআই টিউটর সহায়তা চালু করুন'
              : 'Open Socratic AI Learning Assistant'
          }
          className="group relative flex items-center gap-2.5 px-4 py-2.5 rounded-full bg-[#0A2540] hover:bg-[#0E3357] text-white font-medium text-xs sm:text-sm shadow-md hover:shadow-lg transition-all duration-150 border border-[#1E3A5F] focus:outline-none focus:ring-2 focus:ring-[#0A2540] min-h-[44px]"
        >
          <span className="relative flex h-2 w-2 shrink-0 rounded-full bg-emerald-400"></span>
          <Sparkles className="w-4 h-4 text-amber-300 shrink-0" />
          <span className="font-semibold tracking-wide">
            {isBengali ? 'সক্রেটিক এআই টিউটর' : 'Socratic AI Tutor'}
          </span>
        </button>
      </div>

      {/* Global Socratic AI Tutor Drawer */}
      <SocraticTutorDrawer
        isOpen={isTutorOpen}
        onClose={() => setIsTutorOpen(false)}
        subject="সাধারণ বিজ্ঞান ও গণিত"
      />
    </div>
  );
}

/**
 * Root Application Wrapper supplying the global I18nProvider context.
 */
export default function App(props: AppProps) {
  return (
    <I18nProvider>
      <GlobalAppShell {...props} />
    </I18nProvider>
  );
}
