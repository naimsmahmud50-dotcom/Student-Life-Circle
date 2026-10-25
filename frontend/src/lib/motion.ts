/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Motion System (Motion tokens, variants, and LazyMotion wrappers)
 * FILE:      frontend/src/lib/motion.ts
 * PURPOSE:   Provides high-performance, layout-shift-free, hardware-accelerated motion
 *            using `motion/react` with LazyMotion & domAnimation.
 * STANDARDS: 60fps+, transforms/opacity only, WCAG 2.2 prefers-reduced-motion safe, Zero-Jitter.
 */

import {
  m,
  LazyMotion,
  domAnimation,
  AnimatePresence,
  useReducedMotion,
  type Variants,
  type Transition,
} from 'motion/react';

// Re-export core motion utilities
export { m, LazyMotion, domAnimation, AnimatePresence, useReducedMotion };

/**
 * Editorial Motion Tokens
 * Restrained academic timing: standard deceleration curves, no bouncy neon physics.
 */
export const MOTION_DURATIONS = {
  fast: 0.18,       // micro-interactions, button taps
  base: 0.28,       // card hover, subtle disclosure
  deliberate: 0.42, // modal entrance, drawer slide
  measured: 0.60,   // page transition, long reveal
} as const;

export const MOTION_EASINGS = {
  // Standard academic ease: fast start, soft deliberate deceleration
  standard: [0.2, 0.0, 0.0, 1.0] as const,
  // Gentle entrance
  enter: [0.0, 0.0, 0.2, 1.0] as const,
  // Crisp exit
  exit: [0.4, 0.0, 1.0, 1.0] as const,
} as const;

export const TRANSITIONS = {
  fast: {
    duration: MOTION_DURATIONS.fast,
    ease: MOTION_EASINGS.standard,
  } as Transition,
  base: {
    duration: MOTION_DURATIONS.base,
    ease: MOTION_EASINGS.standard,
  } as Transition,
  deliberate: {
    duration: MOTION_DURATIONS.deliberate,
    ease: MOTION_EASINGS.standard,
  } as Transition,
  tactileSpring: {
    type: 'spring',
    stiffness: 450,
    damping: 35,
    mass: 0.8,
  } as Transition,
} as const;

/**
 * Hardware-Accelerated Animation Variants
 * Transform and opacity ONLY. Zero layout shift.
 */
export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: TRANSITIONS.base,
  },
  exit: {
    opacity: 0,
    transition: TRANSITIONS.fast,
  },
};

export const slideUp: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: TRANSITIONS.deliberate,
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: TRANSITIONS.fast,
  },
};

export const slideDown: Variants = {
  hidden: { opacity: 0, y: -12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: TRANSITIONS.deliberate,
  },
  exit: {
    opacity: 0,
    y: 8,
    transition: TRANSITIONS.fast,
  },
};

export const staggerContainer: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.04,
    },
  },
};

export const staggerFast: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.04,
      delayChildren: 0.02,
    },
  },
};

export const tactilePress = {
  scale: 0.985,
  transition: { duration: 0.08, ease: 'easeOut' },
};

export const tactileHover = {
  y: -2,
  transition: { duration: 0.18, ease: MOTION_EASINGS.standard },
};

/**
 * Helper to ensure complete accessibility for users who prefer reduced motion.
 * When prefersReducedMotion is true, animations degrade cleanly to simple opacity or static.
 */
export function getAccessibleVariant(
  variant: Variants,
  prefersReduced: boolean | null
): Variants {
  if (!prefersReduced) return variant;

  return {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { duration: 0.12 } },
    exit: { opacity: 0, transition: { duration: 0.08 } },
  };
}
