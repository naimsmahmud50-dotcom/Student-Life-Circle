/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - DESIGN SYSTEM UTILITIES:
 * FILE:      frontend/src/lib/utils.ts
 * PURPOSE:   Provides standard class name merging combining clsx and tailwind-merge (twMerge).
 *            Resolves Tailwind class conflicts dynamically and enables ergonomic conditional
 *            class compositions across all Radix UI primitive wrappers.
 * STANDARDS: UI/UX Pro Max, Zero-Emoji Architecture, TypeScript Strict Mode
 * ========================================================================================
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
