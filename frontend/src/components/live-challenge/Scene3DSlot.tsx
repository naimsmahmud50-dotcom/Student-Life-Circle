/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Adaptive 3D Pipeline
 * TOPIC:     Phase 142 Scene3DSlot Wrapper & Zero-CLS Dynamic Slot
 * FILE:      frontend/src/components/live-challenge/Scene3DSlot.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Universal progressive-enhancement slot for the hero composition.
 *            Guarantees:
 *            1. Zero Cumulative Layout Shift (CLS = 0.000): always reserves dimension
 *               and renders the complete, dignified 2D AcademicHeroMotif2D first.
 *            2. Client-only dynamic chunk loading (no SSR crash, separate JS bundle).
 *            3. Automatic downgrade to 2D upon:
 *               - Low-end hardware, saveData mode, 2G/3G network tiers
 *               - Runtime FPS dropping below 28 for >= 3 seconds
 *               - WebGL context loss (webglcontextlost)
 *               - React rendering error in 3D canvas (ErrorBoundary)
 *            4. Tab visibility pause to preserve battery and CPU on mobile devices.
 *            5. Accessible manual 2D/3D toggle with localStorage persistence.
 * STANDARDS: Zero-Emoji, Zero-CLS, Production Grade, WCAG 2.2 AAA, Defensive Engineering
 */

import React, { useState, useEffect, useCallback, Component, ErrorInfo, ReactNode } from 'react';
import dynamic from 'next/dynamic';
import { Sparkles, Eye, AlertCircle, RefreshCw } from 'lucide-react';
import { AcademicHeroMotif2D } from './AcademicHeroMotif2D';
import {
  evaluate3DCapability,
  getUser3DPreference,
  setUser3DPreference,
  CapabilityCheckResult,
  STORAGE_KEY_3D_DISABLED
} from './detect3DCapability';

// Client-only dynamic import of the real academic 3D scene chunk
const DynamicAcademicScene3D = dynamic(
  () => import('./AcademicArmillaryScene3D'),
  {
    ssr: false,
    loading: () => <AcademicHeroMotif2D size={280} />
  }
);

interface ErrorBoundaryProps {
  fallback: ReactNode;
  onError?: (error: Error) => void;
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

class Scene3DErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

interface Scene3DSlotProps {
  size?: number;
  timeRemainingSeconds?: number;
  className?: string;
}

export function Scene3DSlot({
  size = 280,
  timeRemainingSeconds,
  className = ''
}: Scene3DSlotProps) {
  const [mounted, setMounted] = useState<boolean>(false);
  const [is3DAllowed, setIs3DAllowed] = useState<boolean>(false);
  const [capabilityResult, setCapabilityResult] = useState<CapabilityCheckResult | null>(null);
  const [user3DEnabled, setUser3DEnabled] = useState<boolean>(true);
  const [downgradedTo2D, setDowngradedTo2D] = useState<boolean>(false);
  const [downgradeReason, setDowngradeReason] = useState<string | null>(null);
  const [isTabHidden, setIsTabHidden] = useState<boolean>(false);
  const [lowFpsStreak, setLowFpsStreak] = useState<number>(0);

  // Initialize and run capability evaluation on mount
  useEffect(() => {
    setMounted(true);
    const pref = getUser3DPreference();
    setUser3DEnabled(pref);

    if (!pref) {
      setIs3DAllowed(false);
      return;
    }

    let isSubscribed = true;
    async function checkCapabilities() {
      const result = await evaluate3DCapability();
      if (isSubscribed) {
        setCapabilityResult(result);
        setIs3DAllowed(result.allowed);
        if (!result.allowed) {
          setDowngradeReason(result.reason);
        }
      }
    }

    checkCapabilities();

    return () => {
      isSubscribed = false;
    };
  }, []);

  // Listen for tab visibility changes to pause 3D animation
  useEffect(() => {
    if (typeof document === 'undefined') return;

    const handleVisibilityChange = () => {
      const hidden = document.visibilityState === 'hidden';
      setIsTabHidden(hidden);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  // Manual 2D / 3D toggle
  const handleTogglePreference = useCallback(() => {
    const nextState = !user3DEnabled;
    setUser3DEnabled(nextState);
    setUser3DPreference(nextState);

    if (!nextState) {
      setIs3DAllowed(false);
      setDowngradedTo2D(false);
      setDowngradeReason('USER_DISABLED');
    } else {
      setDowngradedTo2D(false);
      setDowngradeReason(null);
      setLowFpsStreak(0);
      // Re-evaluate capability
      evaluate3DCapability().then((result) => {
        setCapabilityResult(result);
        setIs3DAllowed(result.allowed);
        if (!result.allowed) {
          setDowngradeReason(result.reason);
        }
      });
    }
  }, [user3DEnabled]);

  // Handle WebGL context loss: instant safe downgrade to 2D
  const handleContextLost = useCallback(() => {
    setDowngradedTo2D(true);
    setDowngradeReason('WEBGL_CONTEXT_LOST');
  }, []);

  // Continuous runtime FPS monitor: auto-downgrade if FPS < 28 for 3 consecutive measurements
  const handleFpsReport = useCallback((fps: number) => {
    if (fps < 28) {
      setLowFpsStreak((prev) => {
        const next = prev + 1;
        if (next >= 3) {
          setDowngradedTo2D(true);
          setDowngradeReason('LOW_FPS_DOWNGRADE');
        }
        return next;
      });
    } else {
      setLowFpsStreak(0);
    }
  }, []);

  // Error boundary catch
  const handleSceneCrash = useCallback((error: Error) => {
    setDowngradedTo2D(true);
    setDowngradeReason('SCENE_RENDER_ERROR');
  }, []);

  const shouldRender3D = mounted && is3DAllowed && user3DEnabled && !downgradedTo2D;

  return (
    <div
      className={`relative flex flex-col items-center justify-center ${className}`}
      style={{ width: size, minHeight: size }}
    >
      {/* 
        Zero Cumulative Layout Shift (CLS = 0.000) Canvas Slot.
        Always reserves exact dimensions and renders AcademicHeroMotif2D first.
      */}
      <div
        className="relative flex items-center justify-center rounded-3xl overflow-hidden"
        style={{ width: size, height: size }}
      >
        {shouldRender3D ? (
          <Scene3DErrorBoundary
            fallback={<AcademicHeroMotif2D size={size} />}
            onError={handleSceneCrash}
          >
            <DynamicAcademicScene3D
              size={size}
              timeRemainingSeconds={timeRemainingSeconds}
              isPaused={isTabHidden}
              onFpsReport={handleFpsReport}
              onContextLost={handleContextLost}
            />
          </Scene3DErrorBoundary>
        ) : (
          <AcademicHeroMotif2D size={size} />
        )}
      </div>

      {/* 
        Accessible 2D/3D Mode Controller Button
        Gives students full autonomy and transparent performance feedback
      */}
      {mounted && (
        <div className="mt-2.5 flex items-center gap-2">
          <button
            type="button"
            onClick={handleTogglePreference}
            aria-pressed={shouldRender3D}
            aria-label={shouldRender3D ? '৩ডি অ্যানিমেশন বন্ধ করে ২ডি মোড চালু করুন' : '৩ডি গ্রাফিক্স চালু করুন'}
            className="px-3 py-1 rounded-full bg-[#0A2540] hover:bg-[#0E3559] border border-[#1E3A5F] text-[11px] font-bengali font-bold text-slate-300 hover:text-amber-300 transition flex items-center gap-1.5 shadow-sm active:translate-y-0.5"
          >
            {shouldRender3D ? (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block animate-pulse" />
                <span>৩ডি মোড সক্রিয় (সুইচ টু ২ডি)</span>
              </>
            ) : (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-slate-500 inline-block" />
                <span>২ডি মোড সক্রিয় (সুইচ টু ৩ডি)</span>
              </>
            )}
          </button>

          {/* Performance notice when 3D is auto-downgraded or restricted */}
          {!shouldRender3D && downgradeReason && downgradeReason !== 'USER_DISABLED' && (
            <span
              title={`ডিভাইসের স্থায়িত্ব ও ব্যাটারি সুরক্ষায় ২ডি মোড সক্রিয় (${downgradeReason})`}
              className="text-[10px] text-slate-400 font-mono flex items-center gap-1"
            >
              <AlertCircle className="w-3 h-3 text-amber-400" />
              <span>লো-পাওয়ার ২ডি মোড</span>
            </span>
          )}
        </div>
      )}
    </div>
  );
}
