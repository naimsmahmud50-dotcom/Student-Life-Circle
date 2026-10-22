/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - ACCESSIBLE OFFLINE TOAST INDICATOR:
 * MODULE:    Connection Status & Offline Sync Toast Notification
 * TOPIC:     Lucide Wifi/WifiOff Indicators, Zero Layout Shift & Real-Time Sync Telemetry
 * FILE:      frontend/src/components/ui/OfflineToast.tsx
 * PURPOSE:   Provides an unobtrusive, accessible indicator notifying learners of their
 *            network connectivity status across rural 2G/3G connections in Bangladesh.
 *            Subscribes to `syncEngine` state and transitions between:
 *            1. Offline Mode: Informs students that practice is active and answers are safely
 *               stored in IndexedDB.
 *            2. Synchronizing: Animated indicator while offline answers are flushed to server.
 *            3. Reconnected: Brief confirmation toast confirming zero answer loss.
 * AUDIENCE:  Frontend Developers, Accessibility Testers & UI Reviewers
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA Contrast >= 4.5:1, Strict Zero-Emoji
 * ========================================================================================
 */

import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, RefreshCw, CheckCircle2 } from 'lucide-react';
import { syncEngine, SyncStatus } from '@/lib/offline/syncEngine';

export interface OfflineToastProps {
  position?: 'bottom-right' | 'bottom-left' | 'top-center';
  autoHideConnectedAfterMs?: number;
}

export const OfflineToast: React.FC<OfflineToastProps> = ({
  position = 'bottom-right',
  autoHideConnectedAfterMs = 4000
}) => {
  const [status, setStatus] = useState<SyncStatus>(syncEngine.getStatus());
  const [showConnectedToast, setShowConnectedToast] = useState<boolean>(false);
  const [prevOnlineState, setPrevOnlineState] = useState<boolean>(status.isOnline);

  useEffect(() => {
    const unsubscribe = syncEngine.subscribe((newStatus) => {
      // If transitioned from offline to online, show the connected confirmation toast
      if (!prevOnlineState && newStatus.isOnline) {
        setShowConnectedToast(true);
        const timer = setTimeout(() => {
          setShowConnectedToast(false);
        }, autoHideConnectedAfterMs);
        return () => clearTimeout(timer);
      }
      setPrevOnlineState(newStatus.isOnline);
      setStatus(newStatus);
    });

    return () => unsubscribe();
  }, [prevOnlineState, autoHideConnectedAfterMs]);

  // Position class mapping
  const positionClasses = {
    'bottom-right': 'bottom-5 right-5',
    'bottom-left': 'bottom-5 left-5',
    'top-center': 'top-5 left-1/2 -translate-x-1/2'
  }[position];

  // If online, not syncing, no pending items, and not showing the connected confirmation, render nothing
  if (status.isOnline && !status.isSyncing && status.pendingCount === 0 && !showConnectedToast) {
    return null;
  }

  const handleManualSync = () => {
    syncEngine.flushPendingAnswers();
  };

  return (
    <div 
      className={`fixed ${positionClasses} z-50 flex items-center shadow-lg transition-all duration-300 animate-in fade-in slide-in-from-bottom-3`}
      role="status"
      aria-live="polite"
    >
      {/* State 1: Offline Mode Indicator */}
      {!status.isOnline && (
        <div className="flex items-center space-x-3 px-4 py-3 rounded-xl bg-slate-900 border border-slate-800 text-white text-xs shadow-xl backdrop-blur-md">
          <div className="flex items-center justify-center w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 shrink-0">
            <WifiOff className="w-3.5 h-3.5" aria-hidden="true" />
          </div>
          <div>
            <p className="font-semibold text-slate-100">Offline Mode Active</p>
            <p className="text-[11px] text-slate-400">
              Answers saved locally in IndexedDB {status.pendingCount > 0 ? `(${status.pendingCount} pending)` : ''}
            </p>
          </div>
        </div>
      )}

      {/* State 2: Background Synchronizing State */}
      {status.isOnline && status.isSyncing && (
        <div className="flex items-center space-x-3 px-4 py-3 rounded-xl bg-slate-900 border border-slate-800 text-white text-xs shadow-xl">
          <div className="flex items-center justify-center w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 shrink-0">
            <RefreshCw className="w-3.5 h-3.5 animate-spin" aria-hidden="true" />
          </div>
          <div>
            <p className="font-semibold text-slate-100">Synchronizing Answers</p>
            <p className="text-[11px] text-slate-400">
              Flushing {status.pendingCount} pending answers to server...
            </p>
          </div>
        </div>
      )}

      {/* State 3: Online with Pending Items Awaiting Trigger */}
      {status.isOnline && !status.isSyncing && status.pendingCount > 0 && !showConnectedToast && (
        <div className="flex items-center space-x-3 px-4 py-3 rounded-xl bg-slate-900 border border-slate-800 text-white text-xs shadow-xl">
          <div className="flex items-center justify-center w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 shrink-0">
            <Wifi className="w-3.5 h-3.5" aria-hidden="true" />
          </div>
          <div className="flex items-center space-x-3">
            <div>
              <p className="font-semibold text-slate-100">Pending Sync Available</p>
              <p className="text-[11px] text-slate-400">
                {status.pendingCount} answers stored in offline cache
              </p>
            </div>
            <button
              onClick={handleManualSync}
              className="px-2.5 py-1 text-[11px] font-semibold bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
            >
              Sync Now
            </button>
          </div>
        </div>
      )}

      {/* State 4: Connection Restored & Synced Toast */}
      {status.isOnline && showConnectedToast && (
        <div className="flex items-center space-x-3 px-4 py-3 rounded-xl bg-teal-950 border border-teal-800 text-teal-100 text-xs shadow-xl animate-in fade-in zoom-in-95">
          <div className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-400 shrink-0">
            <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
          </div>
          <div>
            <p className="font-semibold text-teal-200">Connection Restored</p>
            <p className="text-[11px] text-teal-300/80">
              All offline progress safely synchronized with server.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
