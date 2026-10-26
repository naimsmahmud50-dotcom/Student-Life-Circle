/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Client Runtime Feature Flags Configuration & React Hook
 * TOPIC:     Decoupled Feature Gating, Non-Destructive Canaries & Safe Rollouts
 * FILE:      frontend/src/config/featureFlags.ts
 * PURPOSE:   Provides runtime feature flags to govern Batch 1 (Exam Routine Hub),
 *            Batch 2 (Academic Study Archive), and Batch 3 (Circular Alert Hub).
 *            Allows silent deployment (OFF by default) and runtime activation without redeploy.
 * STANDARDS: Strict TypeScript, Zero-Emoji, Production Hardened
 * ========================================================================================
 */

export interface FeatureFlags {
  examRoutine: boolean;
  studyArchive: boolean;
  circularAlert: boolean;
}

export const DEFAULT_FEATURE_FLAGS: FeatureFlags = {
  examRoutine: process.env.NEXT_PUBLIC_FEATURE_EXAM_ROUTINE === 'true',
  studyArchive: process.env.NEXT_PUBLIC_FEATURE_STUDY_ARCHIVE === 'true',
  circularAlert: process.env.NEXT_PUBLIC_FEATURE_CIRCULAR_ALERT === 'true',
};

/**
 * Checks whether a named feature is enabled.
 * Supports localStorage override in development or QA environments:
 * e.g., localStorage.setItem('ogrojatra_ff_examRoutine', 'true')
 */
export function isFeatureEnabled(flag: keyof FeatureFlags): boolean {
  if (typeof window !== 'undefined') {
    try {
      const override = localStorage.getItem(`ogrojatra_ff_${flag}`);
      if (override !== null) {
        return override === 'true';
      }
    } catch {
      // Ignore localStorage security/privacy restrictions
    }
  }
  return DEFAULT_FEATURE_FLAGS[flag] ?? false;
}

export function useFeatureFlags(): FeatureFlags {
  // In client runtime, evaluate flags
  return {
    examRoutine: isFeatureEnabled('examRoutine'),
    studyArchive: isFeatureEnabled('studyArchive'),
    circularAlert: isFeatureEnabled('circularAlert'),
  };
}
