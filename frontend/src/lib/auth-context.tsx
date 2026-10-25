/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Enterprise Authentication Context & Reactive Session Provider
 * TOPIC:     Session Lifecycle, Multi-Tab Sync, BFCache Defense & Role Resolution
 * FILE:      frontend/src/lib/auth-context.tsx
 * PURPOSE:   Provides centralized reactive authentication state across Next.js:
 *            - Hydrates session from localStorage safely without SSR mismatch.
 *            - Automatically detects and purges expired sessions.
 *            - Listens to window 'storage' events for instant cross-tab logout synchronization.
 *            - Handles BFCache (pageshow) to prevent back-button admin leakage after logout.
 *            - Exposes strongly-typed helper methods (hasRole, hasAnyRole, login, logout).
 * STANDARDS: Strict TypeScript, WCAG 2.2 AAA, Zero-Emoji, ASVS L2 Session Management
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import {
  UserRole,
  AuthenticatedUser,
  AuthSession,
  hasAnyRole as checkHasAnyRole,
  canAccessAdminPanel as checkCanAccessAdmin,
} from './auth-types';
import { apiClient } from './api-client';

const AUTH_SESSION_STORAGE_KEY = 'ogrojatra_auth_session';
const AUTH_TOKEN_STORAGE_KEY = 'auth_token';

interface AuthContextValue {
  user: AuthenticatedUser | null;
  roles: UserRole[];
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (sessionData: { user: AuthenticatedUser; token: string; expiresInSeconds?: number }) => void;
  logout: () => void;
  hasRole: (role: UserRole) => boolean;
  hasAnyRole: (roles: readonly UserRole[]) => boolean;
  canAccessAdmin: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Validates session integrity and expiration
  const validateAndCleanSession = useCallback((): AuthSession | null => {
    if (typeof window === 'undefined') return null;

    try {
      const raw = localStorage.getItem(AUTH_SESSION_STORAGE_KEY);
      if (!raw) {
        localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
        return null;
      }

      const parsed: AuthSession = JSON.parse(raw);
      const now = Date.now();

      // Check for expiration
      if (parsed.expiresAt && now > parsed.expiresAt) {
        localStorage.removeItem(AUTH_SESSION_STORAGE_KEY);
        localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
        apiClient.setToken(null);
        return null;
      }

      // Sync apiClient token
      if (parsed.token) {
        apiClient.setToken(parsed.token);
      }

      return parsed;
    } catch (err) {
      console.error('Session deserialization error:', err);
      localStorage.removeItem(AUTH_SESSION_STORAGE_KEY);
      localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
      apiClient.setToken(null);
      return null;
    }
  }, []);

  // Initial client hydration
  useEffect(() => {
    const validSession = validateAndCleanSession();
    setSession(validSession);
    setIsLoading(false);
  }, [validateAndCleanSession]);

  // Edge Case: Cross-tab logout or token change synchronization
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === AUTH_SESSION_STORAGE_KEY || e.key === AUTH_TOKEN_STORAGE_KEY) {
        const fresh = validateAndCleanSession();
        setSession(fresh);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [validateAndCleanSession]);

  // Edge Case: BFCache / Back Button after logout handling
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handlePageShow = (event: PageTransitionEvent) => {
      if (event.persisted) {
        // Page was restored from Back-Forward Cache: re-verify session state immediately
        const fresh = validateAndCleanSession();
        setSession(fresh);
      }
    };

    window.addEventListener('pageshow', handlePageShow);
    return () => window.removeEventListener('pageshow', handlePageShow);
  }, [validateAndCleanSession]);

  // Login handler
  const login = useCallback(
    ({
      user,
      token,
      expiresInSeconds = 86400 * 7, // 7 days default
    }: {
      user: AuthenticatedUser;
      token: string;
      expiresInSeconds?: number;
    }) => {
      const now = Date.now();
      const newSession: AuthSession = {
        user,
        token,
        issuedAt: now,
        expiresAt: now + expiresInSeconds * 1000,
      };

      try {
        localStorage.setItem(AUTH_SESSION_STORAGE_KEY, JSON.stringify(newSession));
        localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, token);
      } catch (err) {
        console.error('Failed to persist session to storage:', err);
      }

      apiClient.setToken(token);
      setSession(newSession);
    },
    []
  );

  // Logout handler
  const logout = useCallback(() => {
    try {
      localStorage.removeItem(AUTH_SESSION_STORAGE_KEY);
      localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
    } catch (err) {
      console.error('Failed to clear session from storage:', err);
    }

    apiClient.setToken(null);
    setSession(null);
  }, []);

  const roles = useMemo(() => session?.user?.roles || [], [session]);
  const isAuthenticated = useMemo(() => Boolean(session && session.token), [session]);

  const hasRole = useCallback(
    (role: UserRole) => {
      return roles.includes(role);
    },
    [roles]
  );

  const hasAnyRole = useCallback(
    (targetRoles: readonly UserRole[]) => {
      return checkHasAnyRole(roles, targetRoles);
    },
    [roles]
  );

  const canAccessAdmin = useMemo(() => {
    return checkCanAccessAdmin(roles);
  }, [roles]);

  const contextValue: AuthContextValue = useMemo(
    () => ({
      user: session?.user || null,
      roles,
      token: session?.token || null,
      isAuthenticated,
      isLoading,
      login,
      logout,
      hasRole,
      hasAnyRole,
      canAccessAdmin,
    }),
    [session, roles, isAuthenticated, isLoading, login, logout, hasRole, hasAnyRole, canAccessAdmin]
  );

  return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
