/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - AUTHENTICATION & ACCESS CONTROL STORE:
 * MODULE:    Next.js 15+ Zustand Authentication Store (useAuthStore)
 * TOPIC:     Session Management, RBAC Roles, Guardian Minor Protection, Privacy Matrix
 * FILE:      frontend/src/store/useAuthStore.ts
 * PURPOSE:   Provides centralized reactive client-side authentication state for Ogrojatra platform.
 *            Manages the active session, JWT bearer token, multi-role context (student, guardian,
 *            teacher, admin), child privacy controls (minor protection mode requiring parental consent),
 *            and fine-grained profile visibility settings. Automatically synchronizes bearer tokens
 *            with the centralized apiClient.
 * AUDIENCE:  Frontend Page Developers, Navigation Bars, Auth Guards & Security Reviewers
 * STANDARDS: OAuth 2.0 / JWT Standard, COPPA/Minor Data Safety, Zero-Emoji Architecture
 * ========================================================================================
 */

import { create } from './createStore';
import { apiClient } from '../lib/api-client';

export type UserRole = 'student' | 'guardian' | 'teacher' | 'admin';

export interface PrivacySettings {
  profileVisibility: 'public' | 'private' | 'guardians_only';
  activityStatus: boolean;
  showLeaderboardRank: boolean;
  allowPeerMessaging: boolean;
  leaderboardOptOut?: boolean;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  phoneNumber?: string;
  role: UserRole;
  isVerified: boolean;
  institution?: string;
  curriculumLevel?: 'SSC' | 'HSC' | 'ADMISSION' | 'GENERAL';
  avatarUrl?: string;
  dateOfBirth?: string;
  guardianId?: string;
}

export interface AuthState {
  user: UserProfile | null;
  role: UserRole;
  token: string | null;
  isAuthenticated: boolean;
  isMinorProtected: boolean;
  privacySettings: PrivacySettings;
  isLoading: boolean;

  // Actions
  setUser: (user: UserProfile | null) => void;
  setRole: (role: UserRole) => void;
  setToken: (token: string | null) => void;
  updatePrivacy: (settings: Partial<PrivacySettings>) => void;
  setMinorProtection: (enabled: boolean) => void;
  setIsLoading: (loading: boolean) => void;
  logout: () => void;
}

const DEFAULT_PRIVACY: PrivacySettings = {
  profileVisibility: 'guardians_only',
  activityStatus: true,
  showLeaderboardRank: true,
  allowPeerMessaging: false,
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  role: 'student',
  token: null,
  isAuthenticated: false,
  isMinorProtected: false,
  privacySettings: DEFAULT_PRIVACY,
  isLoading: false,

  setUser: (user: UserProfile | null) => {
    set((state) => {
      const isMinor = user?.dateOfBirth ? isUserMinor(user.dateOfBirth) : false;
      return {
        user,
        role: user ? user.role : state.role,
        isAuthenticated: !!user,
        isMinorProtected: isMinor,
      };
    });
  },

  setRole: (role: UserRole) => {
    set({ role });
  },

  setToken: (token: string | null) => {
    apiClient.setToken(token);
    set({
      token,
      isAuthenticated: !!token,
    });
  },

  updatePrivacy: (settings: Partial<PrivacySettings>) => {
    set((state) => ({
      privacySettings: {
        ...state.privacySettings,
        ...settings,
      },
    }));
  },

  setMinorProtection: (enabled: boolean) => {
    set({ isMinorProtected: enabled });
  },

  setIsLoading: (loading: boolean) => {
    set({ isLoading: loading });
  },

  logout: () => {
    apiClient.setToken(null);
    set({
      user: null,
      role: 'student',
      token: null,
      isAuthenticated: false,
      isMinorProtected: false,
      privacySettings: DEFAULT_PRIVACY,
      isLoading: false,
    });
  },
}));

/**
 * Calculates whether a user is under 18 years of age for minor protection protocol
 */
function isUserMinor(dobString: string): boolean {
  try {
    const dob = new Date(dobString);
    if (isNaN(dob.getTime())) return false;
    const now = new Date();
    let age = now.getFullYear() - dob.getFullYear();
    const monthDiff = now.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < dob.getDate())) {
      age--;
    }
    return age < 18;
  } catch {
    return false;
  }
}
