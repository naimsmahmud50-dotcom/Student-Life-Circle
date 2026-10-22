/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CORE UI PRIMITIVES:
 * MODULE:    Accessible Status Notification Toast Suite
 * TOPIC:     Strict Zero-Emoji, Semantic SVG Icons (Success, Warning, Error, Offline), WAI-ARIA
 * FILE:      frontend/src/components/ui/toast.tsx
 * PURPOSE:   Provides production-grade toast notifications across the entire application.
 *            Supports success, warning, error, info, and offline network state notifications.
 *            Employs exclusively Lucide SVG icons, WAI-ARIA live region announcements,
 *            smooth entrance/exit animations, and auto-dismiss timers.
 * AUDIENCE:  Frontend Developers, Accessibility Testers & UI Reviewers
 * STANDARDS: UI/UX Pro Max, WAI-ARIA Live Regions, Zero-Emoji Architecture
 * ========================================================================================
 */

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { 
  CheckCircle2, 
  AlertTriangle, 
  AlertCircle, 
  Info, 
  WifiOff, 
  X 
} from 'lucide-react';
import { cn } from '@/lib/utils';

export type ToastType = 'success' | 'warning' | 'error' | 'info' | 'offline';

export interface ToastItem {
  id: string;
  type: ToastType;
  title: string;
  description?: string;
  duration?: number;
}

interface ToastContextValue {
  toasts: ToastItem[];
  addToast: (toast: Omit<ToastItem, 'id'>) => string;
  removeToast: (id: string) => void;
  success: (title: string, description?: string) => string;
  warning: (title: string, description?: string) => string;
  error: (title: string, description?: string) => string;
  info: (title: string, description?: string) => string;
  offline: (title?: string, description?: string) => string;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const addToast = useCallback((toast: Omit<ToastItem, 'id'>) => {
    const id = 'toast_' + Math.random().toString(36).substring(2, 9);
    const newToast: ToastItem = { ...toast, id };
    setToasts((prev) => [...prev, newToast]);

    const duration = toast.duration ?? 4000;
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
    return id;
  }, [removeToast]);

  const success = useCallback((title: string, description?: string) => {
    return addToast({ type: 'success', title, description });
  }, [addToast]);

  const warning = useCallback((title: string, description?: string) => {
    return addToast({ type: 'warning', title, description });
  }, [addToast]);

  const error = useCallback((title: string, description?: string) => {
    return addToast({ type: 'error', title, description, duration: 6000 });
  }, [addToast]);

  const info = useCallback((title: string, description?: string) => {
    return addToast({ type: 'info', title, description });
  }, [addToast]);

  const offline = useCallback((title = 'Network Offline', description = 'Working in local CRDT offline mode. Mutations buffered.') => {
    return addToast({ type: 'offline', title, description, duration: 5000 });
  }, [addToast]);

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast, success, warning, error, info, offline }}>
      {children}
      <ToastContainer toasts={toasts} onDismiss={removeToast} />
    </ToastContext.Provider>
  );
};

export function useToast(): ToastContextValue {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

interface ToastContainerProps {
  toasts: ToastItem[];
  onDismiss: (id: string) => void;
}

export const ToastContainer: React.FC<ToastContainerProps> = ({ toasts, onDismiss }) => {
  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      className="fixed bottom-4 right-4 z-[9999] flex flex-col space-y-2 max-w-sm w-full pointer-events-none p-2 sm:p-0"
    >
      {toasts.map((toast) => (
        <ToastCard key={toast.id} toast={toast} onDismiss={() => onDismiss(toast.id)} />
      ))}
    </div>
  );
};

interface ToastCardProps {
  toast: ToastItem;
  onDismiss: () => void;
}

export const ToastCard: React.FC<ToastCardProps> = ({ toast, onDismiss }) => {
  const typeConfigs = {
    success: {
      icon: CheckCircle2,
      iconColor: 'text-emerald-600 dark:text-emerald-400',
      bgColor: 'bg-emerald-50/90 dark:bg-emerald-950/80',
      borderColor: 'border-emerald-200 dark:border-emerald-900',
      titleColor: 'text-emerald-950 dark:text-emerald-100',
    },
    warning: {
      icon: AlertTriangle,
      iconColor: 'text-amber-600 dark:text-amber-400',
      bgColor: 'bg-amber-50/90 dark:bg-amber-950/80',
      borderColor: 'border-amber-200 dark:border-amber-900',
      titleColor: 'text-amber-950 dark:text-amber-100',
    },
    error: {
      icon: AlertCircle,
      iconColor: 'text-red-600 dark:text-red-400',
      bgColor: 'bg-red-50/90 dark:bg-red-950/80',
      borderColor: 'border-red-200 dark:border-red-900',
      titleColor: 'text-red-950 dark:text-red-100',
    },
    info: {
      icon: Info,
      iconColor: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-50/90 dark:bg-blue-950/80',
      borderColor: 'border-blue-200 dark:border-blue-900',
      titleColor: 'text-blue-950 dark:text-blue-100',
    },
    offline: {
      icon: WifiOff,
      iconColor: 'text-slate-600 dark:text-slate-400',
      bgColor: 'bg-slate-100/90 dark:bg-slate-900/90',
      borderColor: 'border-slate-300 dark:border-slate-700',
      titleColor: 'text-slate-900 dark:text-slate-100',
    },
  };

  const config = typeConfigs[toast.type] || typeConfigs.info;
  const IconComponent = config.icon;

  return (
    <div
      role={toast.type === 'error' ? 'alert' : 'status'}
      className={cn(
        "pointer-events-auto flex items-start gap-3 p-4 rounded-xl border shadow-lg backdrop-blur-md transition-all duration-200 animate-in slide-in-from-bottom-2 fade-in",
        config.bgColor,
        config.borderColor
      )}
    >
      <IconComponent className={cn("w-5 h-5 shrink-0 mt-0.5", config.iconColor)} aria-hidden="true" />
      <div className="flex-1 space-y-0.5">
        <div className={cn("text-xs sm:text-sm font-bold", config.titleColor)}>
          {toast.title}
        </div>
        {toast.description && (
          <div className="text-[11px] sm:text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
            {toast.description}
          </div>
        )}
      </div>
      <button
        onClick={onDismiss}
        className="p-1 rounded-md text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0"
        aria-label="Dismiss notification"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
