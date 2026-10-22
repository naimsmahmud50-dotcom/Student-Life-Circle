/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CENTRALIZED STORE EXPORTS:
 * MODULE:    Next.js 15+ Centralized Zustand State Barrel
 * TOPIC:     Unified Client State Exports & Type Re-exports
 * FILE:      frontend/src/store/index.ts
 * PURPOSE:   Provides a single entry point for all global Zustand client stores, interfaces,
 *            and the store creation factory. Enables decoupled imports across the entire
 *            component tree (e.g., `import { useAuthStore, useQuizStore } from '@/store'`).
 * AUDIENCE:  Frontend Page Developers & Architecture Engineers
 * STANDARDS: TypeScript Strict Mode, Clean Architecture, Zero-Emoji Architecture
 * ========================================================================================
 */

export * from './createStore';
export * from './useAuthStore';
export * from './useQuizStore';
export * from './useFilterStore';
