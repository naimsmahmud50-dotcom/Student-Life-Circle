/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Enterprise Role-Based Access Control (RBAC) Client Guard & Admin Security Gateway
 * TOPIC:     Dedicated Admin Security Gate, Zero-FOAC Defense & Private Link Access
 * FILE:      frontend/src/components/auth/AdminAuthGuard.tsx
 * PURPOSE:   Guards administrative routes against unauthorized and public access:
 *            - Replaces public auth redirects with a dedicated, hardened Admin Security Gate.
 *            - Enforces master password and authorized admin email/Gmail verification.
 *            - Prevents Flash of Admin Content (FOAC) via paper-press editorial skeleton.
 *            - Zero public UI leakage: /admin is accessible strictly by direct URL navigation.
 * STANDARDS: Strict TypeScript, Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial
 */

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { ShieldCheck, ShieldAlert, Lock, Home, Eye, EyeOff, AlertCircle } from 'lucide-react';
import { useAuth } from '@/lib/auth-context';
import { UserRole, ADMIN_PANEL_ROLES, hasAnyRole } from '@/lib/auth-types';

/**
 * Authorized Super Administrator Email Allowlist
 */
export const AUTHORIZED_ADMIN_EMAILS = [
  'mahmud.cse.du@gmail.com',
  'naimsmahmud50@gmail.com',
  'mahmud@ogrojatra.edu.bd',
  'admin@ogrojatra.edu.bd',
] as const;

/**
 * Master Admin Access Keys
 */
export const MASTER_ADMIN_PASSWORDS = [
  'Admin@Mahmud2026#Secure',
  'Mahmud@Admin2026!',
] as const;

export interface AdminAuthGuardProps {
  children: React.ReactNode;
  allowedRoles?: readonly UserRole[];
  /** Optional custom title for the protected section */
  sectionName?: string;
}

/**
 * Editorial Loading State preventing any Flash of Admin Content (Zero-FOAC)
 */
export const AdminAuthLoadingState: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#FAF8F3] dark:bg-[#12161F] px-4 transition-colors">
      <div className="max-w-md w-full p-8 rounded-2xl border border-[#E5E2DA] dark:border-[#273145] bg-white dark:bg-[#181E2B] shadow-xs text-center space-y-4">
        <div className="w-12 h-12 mx-auto rounded-xl bg-[#FAF8F3] dark:bg-[#1E2536] border border-[#E5E2DA] dark:border-[#273145] flex items-center justify-center">
          <Lock className="w-5 h-5 text-[#1B2A4A] dark:text-[#5A7EBA] animate-pulse" strokeWidth={1.75} />
        </div>
        <div className="space-y-1.5">
          <p className="text-xs uppercase tracking-wider text-[#B8862B] dark:text-[#D4A34B] font-semibold font-sans">
            নিরাপত্তা যাচাইকরণ
          </p>
          <h2 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
            প্রশাসনিক অনুমোদন অনুসন্ধান করা হচ্ছে...
          </h2>
          <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-sans leading-relaxed">
            আপনার অ্যাকাউন্টের নিরাপত্তা স্তর ও রোল পারমিশন যাচাই করা হচ্ছে। অনুগ্রহ করে অপেক্ষা করুন।
          </p>
        </div>
        <div className="w-24 h-1 bg-[#E5E2DA] dark:bg-[#273145] rounded-full mx-auto overflow-hidden">
          <div className="w-full h-full bg-[#1B2A4A] dark:bg-[#5A7EBA] animate-[pulse_1.2s_ease-in-out_infinite]" />
        </div>
      </div>
    </div>
  );
};

/**
 * Dedicated Admin Security Gate displayed directly at /admin when unauthenticated
 */
export interface AdminSecurityGateProps {
  switchAccountNotice?: string;
  onLogoutCurrent?: () => void;
}

export const AdminSecurityGate: React.FC<AdminSecurityGateProps> = ({
  switchAccountNotice,
  onLogoutCurrent,
}) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsSubmitting(true);

    const normalizedEmail = email.trim().toLowerCase();
    const cleanPassword = password.trim();

    const isEmailValid = AUTHORIZED_ADMIN_EMAILS.some(
      (authorized) => authorized.toLowerCase() === normalizedEmail
    );
    const isPasswordValid = MASTER_ADMIN_PASSWORDS.some(
      (validPass) => validPass === cleanPassword
    );

    if (!isEmailValid || !isPasswordValid) {
      setErrorMessage(
        'ভুল অ্যাডমিন ইমেইল অথবা সিকিউর পাসওয়ার্ড! শুধুমাত্র অনুমোদিত সুপার অ্যাডমিন কনসোলে প্রবেশ করতে পারবেন।'
      );
      setIsSubmitting(false);
      return;
    }

    // Set authenticated session with full Admin & Reviewer roles
    login({
      user: {
        id: `usr_admin_${Date.now().toString(36)}`,
        email: normalizedEmail,
        fullName: 'Mahmud Hasan (সুপার অ্যাডমিন)',
        roles: [UserRole.ADMIN, UserRole.SUBJECT_REVIEWER],
      },
      token: `admin_sec_jwt_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 9)}`,
      expiresInSeconds: 86400 * 7,
    });

    setIsSubmitting(false);
  };

  return (
    <>
      <Head>
        <title>প্রশাসনিক নিরাপত্তা গেটওয়ে | অগ্রযাত্রা এডমিন</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-[#FAF8F3] dark:bg-[#0B0F19] px-4 py-12 transition-colors">
        <div className="max-w-md w-full p-6 sm:p-8 rounded-2xl border border-[#E5E2DA] dark:border-[#273145] bg-white dark:bg-[#151C2A] shadow-lg space-y-6">
          
          {/* Header */}
          <div className="text-center space-y-2 border-b border-[#E5E2DA] dark:border-[#273145] pb-5">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-[#0A2540] dark:bg-[#1E293B] border border-[#2D3A52] flex items-center justify-center text-white shadow-paper-sm">
              <ShieldCheck className="w-7 h-7 text-[#D4A34B]" strokeWidth={2} />
            </div>
            <div className="pt-2">
              <span className="text-[10px] font-bold uppercase tracking-widest text-[#B8862B] dark:text-[#D4A34B] font-sans">
                প্রশাসনিক প্রবেশদ্বার • ADMIN SECURITY GATE
              </span>
              <h1 className="text-xl sm:text-2xl font-serif font-bold text-[#0A2540] dark:text-[#F8FAFC] font-bengali">
                অগ্রযাত্রা কেন্দ্রীয় প্রশাসন
              </h1>
            </div>
            <p className="text-xs text-[#5A687D] dark:text-[#94A3B8] font-sans leading-relaxed">
              এই কনসোলটি অত্যন্ত সংবেদনশীল এবং শুধুমাত্র অনুমোদিত সুপার অ্যাডমিনের জন্য সংরক্ষিত। প্রবেশ করতে আপনার অনুমোদিত জিমেইল ও সিকিউর পাসওয়ার্ড দিন।
            </p>
          </div>

          {/* Switch Account Notice if already logged in as non-admin */}
          {switchAccountNotice && (
            <div className="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-xs text-amber-900 dark:text-amber-200 flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-amber-700 dark:text-amber-400 shrink-0 mt-0.5" strokeWidth={1.75} />
              <div className="flex-1 space-y-1">
                <p className="font-sans text-[11px] leading-relaxed">{switchAccountNotice}</p>
                {onLogoutCurrent && (
                  <button
                    type="button"
                    onClick={onLogoutCurrent}
                    className="text-[11px] font-semibold text-amber-800 dark:text-amber-300 underline underline-offset-2 hover:text-amber-950 dark:hover:text-amber-100"
                  >
                    বর্তমান সাধারণ অ্যাকাউন্ট লগআউট করুন
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Error Message */}
          {errorMessage && (
            <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 text-xs text-rose-800 dark:text-rose-200 flex items-start gap-2.5 animate-in fade-in">
              <AlertCircle className="w-4 h-4 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" strokeWidth={1.75} />
              <p className="font-sans leading-relaxed text-[11px] font-medium">{errorMessage}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#0A2540] dark:text-[#E2E8F0] block font-sans">
                অনুমোদিত জিমেইল / ইমেইল (Admin Email):
              </label>
              <input
                type="email"
                required
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="যেমন: mahmud.cse.du@gmail.com"
                className="w-full text-sm p-3 rounded-xl border border-[#E2DDD3] dark:border-[#2D3A52] bg-[#FAF8F5] dark:bg-[#0C1422] text-[#1B2A4A] dark:text-[#E2E8F0] shadow-inner-bevel focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-[#3B82F6] transition-all font-sans"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#0A2540] dark:text-[#E2E8F0] block font-sans">
                প্রশাসনিক মাস্টার পাসওয়ার্ড (Master Security Key):
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="সিকিউর অ্যাডমিন পাসওয়ার্ড"
                  className="w-full text-sm p-3 pr-10 rounded-xl border border-[#E2DDD3] dark:border-[#2D3A52] bg-[#FAF8F5] dark:bg-[#0C1422] text-[#1B2A4A] dark:text-[#E2E8F0] shadow-inner-bevel focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-[#3B82F6] transition-all font-sans"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#5A687D] dark:text-[#94A3B8] hover:text-[#0A2540] dark:hover:text-[#E8EFF8] transition-colors p-1"
                  aria-label={showPassword ? 'পাসওয়ার্ড লুকান' : 'পাসওয়ার্ড দেখুন'}
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" strokeWidth={1.75} />
                  ) : (
                    <Eye className="w-4 h-4" strokeWidth={1.75} />
                  )}
                </button>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3.5 px-4 rounded-xl bg-[#0A2540] hover:bg-[#123358] dark:bg-[#2563EB] dark:hover:bg-[#1D4ED8] text-white font-bold text-sm tracking-wide font-bengali shadow-paper-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                <Lock className="w-4 h-4 text-[#D4A34B] dark:text-white shrink-0" strokeWidth={2} />
                <span>যাচাই করুন ও প্রবেশ করুন (Verify & Access)</span>
              </button>
            </div>
          </form>

          {/* Navigation to Public Portal */}
          <div className="pt-4 border-t border-[#E5E2DA] dark:border-[#273145] text-center">
            <Link
              href="/"
              className="inline-flex items-center justify-center gap-1.5 text-xs text-[#5A687D] dark:text-[#94A3B8] hover:text-[#0A2540] dark:hover:text-[#F8FAFC] font-medium transition-colors"
            >
              <Home className="w-3.5 h-3.5 shrink-0" strokeWidth={1.75} />
              <span>মূল পাবলিক ওয়েবসাইটে ফিরে যান</span>
            </Link>
          </div>

        </div>
      </div>
    </>
  );
};

/**
 * Dignified Academic Access Denied Screen
 */
export const AdminAccessDeniedState: React.FC<{
  currentRoles: UserRole[];
  allowedRoles: readonly UserRole[];
  onLogout: () => void;
}> = ({ currentRoles, allowedRoles, onLogout }) => {
  return (
    <AdminSecurityGate
      switchAccountNotice="আপনার বর্তমান লগইনকৃত অ্যাকাউন্টে এই প্রশাসনিক বিভাগে প্রবেশের পূর্ণ অনুমতি নেই।"
      onLogoutCurrent={onLogout}
    />
  );
};

/**
 * Core Admin Route Guard Component
 */
export const AdminAuthGuard: React.FC<AdminAuthGuardProps> = ({
  children,
  allowedRoles = ADMIN_PANEL_ROLES,
}) => {
  const { isAuthenticated, isLoading, roles, logout } = useAuth();
  const [isAuthorized, setIsAuthorized] = useState<boolean>(false);

  useEffect(() => {
    if (isLoading) return;

    if (isAuthenticated) {
      const hasPermission = hasAnyRole(roles, allowedRoles);
      setIsAuthorized(hasPermission);
    } else {
      setIsAuthorized(false);
    }
  }, [isAuthenticated, isLoading, roles, allowedRoles]);

  // Prevent flash while state is hydrating
  if (isLoading) {
    return <AdminAuthLoadingState />;
  }

  // Not logged in: Show dedicated Admin Security Gate directly at /admin
  if (!isAuthenticated) {
    return <AdminSecurityGate />;
  }

  // Logged in but insufficient role permissions: Show AdminSecurityGate with account switch notice
  if (!isAuthorized) {
    return (
      <AdminSecurityGate
        switchAccountNotice="আপনার বর্তমান লগইনকৃত সাধারণ অ্যাকাউন্টে প্রশাসনিক অনুমোদন নেই। অ্যাডমিন কনসোলে প্রবেশের জন্য অনুমোদিত অ্যাডমিন জিমেইল ও পাসওয়ার্ড প্রদান করুন।"
        onLogoutCurrent={logout}
      />
    );
  }

  // Permitted: Render protected children
  return <>{children}</>;
};

/**
 * Higher Order Component (HOC) for protecting Admin Pages
 */
export function withAdminAuth<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  allowedRoles: readonly UserRole[] = ADMIN_PANEL_ROLES
) {
  const ComponentWithAdminAuth = (props: P) => {
    return (
      <AdminAuthGuard allowedRoles={allowedRoles}>
        <WrappedComponent {...props} />
      </AdminAuthGuard>
    );
  };

  ComponentWithAdminAuth.displayName = `withAdminAuth(${
    WrappedComponent.displayName || WrappedComponent.name || 'Component'
  })`;

  return ComponentWithAdminAuth;
}
