/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Enterprise Role-Based Access Control (RBAC) Client Guard
 * TOPIC:     Zero-FOAC Protection, Academic Access Denied Presentation & Redirect Engine
 * FILE:      frontend/src/components/auth/AdminAuthGuard.tsx
 * PURPOSE:   Guards administrative routes against unauthenticated and unauthorized access:
 *            - Prevents Flash of Admin Content (FOAC) via paper-press editorial skeleton.
 *            - Enforces strict role checks (ADMIN vs SUBJECT_REVIEWER).
 *            - Preserves return path via '?redirectTo=' URL search parameter.
 *            - Dignified academic "Access Denied" state conforming to UI/UX Pro Max tokens.
 * STANDARDS: Strict TypeScript, Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial
 */

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { ShieldAlert, Lock, ArrowRight, Home, LogIn } from 'lucide-react';
import { useAuth } from '@/lib/auth-context';
import { UserRole, ADMIN_PANEL_ROLES, hasAnyRole } from '@/lib/auth-types';

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
 * Dignified Academic Access Denied Screen for Authenticated Users Lacking Sufficient Privileges
 */
export const AdminAccessDeniedState: React.FC<{
  currentRoles: UserRole[];
  allowedRoles: readonly UserRole[];
  onLogout: () => void;
}> = ({ currentRoles, allowedRoles, onLogout }) => {
  const router = useRouter();

  const formattedCurrentRoles =
    currentRoles.length > 0
      ? currentRoles.map((r) => (r === UserRole.STUDENT ? 'শিক্ষার্থী (Student)' : r)).join(', ')
      : 'সাধারণ ভিজিটর (Guest)';

  const formattedRequiredRoles = allowedRoles
    .map((r) => {
      if (r === UserRole.ADMIN) return 'সুপার অ্যাডমিন (Admin)';
      if (r === UserRole.SUBJECT_REVIEWER) return 'বিষয় পর্যালোচক (Subject Reviewer)';
      return r;
    })
    .join(' অথবা ');

  return (
    <>
      <Head>
        <title>অননুমোদিত প্রবেশাধিকার | অগ্রযাত্রা প্রশাসন</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-[#FAF8F3] dark:bg-[#12161F] px-4 py-12 transition-colors">
        <div className="max-w-lg w-full p-6 sm:p-8 rounded-2xl border border-[#E5E2DA] dark:border-[#273145] bg-white dark:bg-[#181E2B] shadow-xs space-y-6">
          <div className="flex items-center gap-3 border-b border-[#E5E2DA] dark:border-[#273145] pb-4">
            <div className="w-11 h-11 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 flex items-center justify-center shrink-0">
              <ShieldAlert className="w-5 h-5 text-rose-700 dark:text-rose-400" strokeWidth={1.75} />
            </div>
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-rose-700 dark:text-rose-400 font-sans">
                এইচটিটিপি ৪০৩ • প্রবেশাধিকার সংরক্ষিত
              </span>
              <h1 className="text-xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
                অননুমোদিত প্রশাসনিক অঞ্চল
              </h1>
            </div>
          </div>

          <div className="space-y-3 text-sm text-[#5B5B5B] dark:text-slate-300 font-sans leading-relaxed">
            <p>
              এই বিভাগটি অগ্রযাত্রার সংবেদনশীল একাডেমিক ও জাতীয় পরীক্ষা পরিচালনা কনসোল। এখানে প্রবেশের জন্য আপনার
              অ্যাকাউন্টে <strong className="text-[#1A1A1A] dark:text-white font-semibold">{formattedRequiredRoles}</strong> অনুমোদন থাকা আবশ্যক।
            </p>
            <div className="p-3.5 rounded-xl bg-[#FAF8F3] dark:bg-[#12161F] border border-[#E5E2DA] dark:border-[#273145] text-xs space-y-1">
              <div className="text-[#787878] dark:text-slate-400">আপনার বর্তমান অনুমোদিত ভূমিকা:</div>
              <div className="font-semibold text-[#1A1A1A] dark:text-[#F5F2EB]">{formattedCurrentRoles}</div>
            </div>
            <p className="text-xs text-[#787878] dark:text-slate-400">
              আপনি যদি একজন অনুমোদিত বিষয় পর্যালোচক বা বোর্ড প্রতিনিধি হয়ে থাকেন, তবে অনুগ্রহ করে সঠিক প্রাতিষ্ঠানিক
              অ্যাকাউন্ট দিয়ে পুনরায় লগইন করুন।
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
            <button
              type="button"
              onClick={() => {
                onLogout();
                router.push(`/auth?redirectTo=${encodeURIComponent(router.asPath)}`);
              }}
              className="w-full sm:w-auto flex-1 inline-flex items-center justify-center gap-2 h-11 px-5 rounded-xl bg-[#1B2A4A] hover:bg-[#121E36] text-white text-xs font-semibold shadow-xs transition-all active:translate-y-0.5"
            >
              <LogIn className="w-4 h-4 shrink-0" strokeWidth={1.75} />
              <span>অন্য অ্যাকাউন্টে লগইন</span>
            </button>

            <Link
              href="/"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 h-11 px-5 rounded-xl border border-[#E5E2DA] dark:border-[#273145] bg-white dark:bg-[#181E2B] hover:bg-[#FAF8F3] dark:hover:bg-[#252E42] text-[#1A1A1A] dark:text-[#F5F2EB] text-xs font-semibold shadow-xs transition-all"
            >
              <Home className="w-4 h-4 shrink-0" strokeWidth={1.75} />
              <span>হোমপেজে ফিরে যান</span>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

/**
 * Core Admin Route Guard Component
 */
export const AdminAuthGuard: React.FC<AdminAuthGuardProps> = ({
  children,
  allowedRoles = ADMIN_PANEL_ROLES,
}) => {
  const router = useRouter();
  const { isAuthenticated, isLoading, roles, logout } = useAuth();
  const [isAuthorized, setIsAuthorized] = useState<boolean>(false);

  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated) {
      // Unauthenticated: Immediately redirect to /auth with return target
      const returnUrl = encodeURIComponent(router.asPath);
      router.replace(`/auth?redirectTo=${returnUrl}`);
      return;
    }

    const hasPermission = hasAnyRole(roles, allowedRoles);
    setIsAuthorized(hasPermission);
  }, [isAuthenticated, isLoading, roles, allowedRoles, router]);

  // Prevent flash while state is hydrating
  if (isLoading) {
    return <AdminAuthLoadingState />;
  }

  // Not logged in: show loading while router.replace executes
  if (!isAuthenticated) {
    return <AdminAuthLoadingState />;
  }

  // Logged in but insufficient role permissions: show dignified access denied
  if (!isAuthorized) {
    return (
      <AdminAccessDeniedState
        currentRoles={roles}
        allowedRoles={allowedRoles}
        onLogout={logout}
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
