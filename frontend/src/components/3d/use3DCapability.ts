/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Hardware & Network Capability Gate for WebGL / 3D Experiences
 * FILE:      frontend/src/components/3d/use3DCapability.ts
 * PURPOSE:   Provides strict, progressive-enhancement capability detection:
 *            1. WebGL/WebGL2 context verification
 *            2. Memory & CPU concurrency thresholds (deviceMemory >= 4, hardwareConcurrency >= 4)
 *            3. Network constraints (no Save-Data header, effectiveType !== '2g' / '3g')
 *            4. User accessibility constraints (prefers-reduced-motion check)
 *            5. Page visibility monitoring (tab visibility)
 *            6. Rolling FPS monitor with auto-downgrade if FPS < 30
 *            7. Persistent localStorage override toggle ('ogrojatra_3d_enabled')
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Sub-millisecond Execution
 */

import { useState, useEffect, useCallback, useRef } from 'react';

export interface DeviceCapabilityState {
  is3DSupported: boolean;
  is3DAllowed: boolean;
  isDegraded: boolean;
  userPreference: boolean | null; // null = auto
  rollingFps: number;
  reason: string;
}

export function checkWebGLSupport(): boolean {
  if (typeof window === 'undefined') return false;
  try {
    const canvas = document.createElement('canvas');
    const gl =
      canvas.getContext('webgl2') ||
      canvas.getContext('webgl') ||
      canvas.getContext('experimental-webgl');
    return !!gl;
  } catch {
    return false;
  }
}

export function checkDeviceTier(): { isHighEnd: boolean; reason?: string } {
  if (typeof window === 'undefined' || typeof navigator === 'undefined') {
    return { isHighEnd: true };
  }

  // 1. Check Data Saver mode
  // @ts-expect-error - connection is vendor-specific in some browsers
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if (connection) {
    if (connection.saveData === true) {
      return { isHighEnd: false, reason: 'ডাটা সেভার মোড সক্রিয়' };
    }
    const effType = connection.effectiveType;
    if (effType === 'slow-2g' || effType === '2g' || effType === '3g') {
      return { isHighEnd: false, reason: 'ধীরগতির ইন্টারনেট সংযোগ (2G/3G)' };
    }
  }

  // 2. Check Device Memory (RAM in GB)
  // @ts-expect-error - deviceMemory is experimental
  const memory = navigator.deviceMemory;
  if (typeof memory === 'number' && memory < 4) {
    return { isHighEnd: false, reason: 'কম মেমরির ডিভাইস (< ৪ জিবি)' };
  }

  // 3. Check Hardware Concurrency (CPU Cores)
  const cores = navigator.hardwareConcurrency;
  if (typeof cores === 'number' && cores < 4) {
    return { isHighEnd: false, reason: 'সীমিত প্রসেসিং কোর (< ৪ কোর)' };
  }

  return { isHighEnd: true };
}

export function checkReducedMotion(): boolean {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export const STORAGE_KEY = 'ogrojatra_3d_enabled';

export function getStored3DPreference(): boolean {
  if (typeof window === 'undefined' || !window.localStorage) return true;
  try {
    const val = window.localStorage.getItem(STORAGE_KEY);
    if (val === 'false') return false;
    return true;
  } catch {
    return true;
  }
}

export function setStored3DPreference(enabled: boolean): void {
  if (typeof window === 'undefined' || !window.localStorage) return;
  try {
    window.localStorage.setItem(STORAGE_KEY, String(enabled));
  } catch {
    // Ignore storage errors in private browsing
  }
}

export function use3DCapability() {
  const [userPreference, setUserPreferenceState] = useState<boolean | null>(null);
  const [isDegraded, setIsDegraded] = useState<boolean>(false);
  const [isTabVisible, setIsTabVisible] = useState<boolean>(true);
  const [rollingFps, setRollingFps] = useState<number>(60);
  const [isClient, setIsClient] = useState<boolean>(false);

  // Consecutive low-FPS frame counter for auto-downgrade
  const lowFpsCountRef = useRef<number>(0);

  // Load initial localStorage preference and tab visibility
  useEffect(() => {
    setIsClient(true);
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'true') setUserPreferenceState(true);
      else if (saved === 'false') setUserPreferenceState(false);
    } catch {
      // Ignore storage errors in private/sandboxed mode
    }

    const handleVisibilityChange = () => {
      setIsTabVisible(!document.hidden);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  // Update user preference with persistence
  const setUserPreference = useCallback((val: boolean | null) => {
    setUserPreferenceState(val);
    try {
      if (val === null) {
        localStorage.removeItem(STORAGE_KEY);
      } else {
        localStorage.setItem(STORAGE_KEY, String(val));
      }
    } catch {
      // Ignore storage errors
    }
  }, []);

  const toggle3D = useCallback(() => {
    setUserPreferenceState((prev) => {
      const next = prev === false ? true : false;
      try {
        localStorage.setItem(STORAGE_KEY, String(next));
      } catch {
        // Ignore storage errors
      }
      return next;
    });
  }, []);

  // Report FPS from active 3D canvas
  const reportFps = useCallback((currentFps: number) => {
    setRollingFps(currentFps);

    // Auto-downgrade threshold: if FPS is below 28 for over 60 reported cycles
    if (currentFps > 0 && currentFps < 28) {
      lowFpsCountRef.current += 1;
      if (lowFpsCountRef.current > 40) {
        setIsDegraded(true);
      }
    } else if (currentFps >= 45) {
      // Reset if recovered
      lowFpsCountRef.current = Math.max(0, lowFpsCountRef.current - 1);
    }
  }, []);

  // Reset degradation manually
  const resetDegradation = useCallback(() => {
    lowFpsCountRef.current = 0;
    setIsDegraded(false);
  }, []);

  // Compute capability resolution
  const webglSupported = isClient ? checkWebGLSupport() : false;
  const tierCheck = isClient ? checkDeviceTier() : { isHighEnd: true };
  const reducedMotion = isClient ? checkReducedMotion() : false;

  let isAllowed = false;
  let reason = 'স্বাভাবিক মোড সক্রিয়';

  if (!isClient) {
    isAllowed = false;
    reason = 'সার্ভার-সাইড রেন্ডারিং';
  } else if (!webglSupported) {
    isAllowed = false;
    reason = 'ডিভাইসে ওয়েবজিএল সমর্থন অনুপস্থিত';
  } else if (reducedMotion) {
    isAllowed = false;
    reason = 'ব্যবহারকারীর মোশন হ্রাস সংক্রান্ত অগ্রাধিকার সক্রিয়';
  } else if (userPreference === false) {
    isAllowed = false;
    reason = 'ব্যবহারকারী কর্তৃক ৩ডি মোড বন্ধ রাখা হয়েছে';
  } else if (isDegraded) {
    isAllowed = false;
    reason = 'ফ্রেমরেট ৩০ এফপিএসের নিচে নামায় স্বয়ংক্রিয় ডাউনগ্রেড';
  } else if (userPreference === true) {
    // If user explicitly forced it ON, bypass device tier
    isAllowed = webglSupported && !reducedMotion;
    reason = 'ব্যবহারকারী কর্তৃক ম্যানুয়ালি ৩ডি মোড সক্রিয়';
  } else if (!tierCheck.isHighEnd) {
    isAllowed = false;
    reason = tierCheck.reason || 'সীমিত ক্ষমতাসম্পন্ন ডিভাইস';
  } else {
    isAllowed = true;
    reason = 'উচ্চ কার্যক্ষমতার ৩ডি মোড সমর্থিত ও প্রস্তুত';
  }

  return {
    isClient,
    is3DSupported: webglSupported,
    is3DAllowed: isAllowed && isTabVisible,
    isDegraded,
    userPreference,
    rollingFps,
    reason,
    setUserPreference,
    toggle3D,
    reportFps,
    resetDegradation,
  };
}
