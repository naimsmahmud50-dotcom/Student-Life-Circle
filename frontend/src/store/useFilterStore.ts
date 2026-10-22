/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CURRICULUM & SEARCH FILTER STORE:
 * MODULE:    Next.js 15+ Zustand Filter Store (useFilterStore)
 * TOPIC:     Curriculum Levels, Subject Taxonomy, Global Search & Regional Filters
 * FILE:      frontend/src/store/useFilterStore.ts
 * PURPOSE:   Maintains consistent search query parameters, curriculum stage selections (SSC,
 *            HSC, Admission), subject filtering, difficulty criteria, and regional division
 *            settings across practice tests, admission mock modules, and tuition marketplace.
 * AUDIENCE:  Filter Component Authors, Navigation Bar Search Bars & Taxonomy Engineers
 * STANDARDS: NCTB Curriculum Standards, Clean State Separation, Zero-Emoji Architecture
 * ========================================================================================
 */

import { create } from './createStore';

export type CurriculumLevel = 'ALL' | 'SSC' | 'HSC' | 'ADMISSION';
export type DifficultyLevel = 'ALL' | 'EASY' | 'MEDIUM' | 'HARD';

export interface FilterState {
  curriculumLevel: CurriculumLevel;
  subject: string;
  searchQuery: string;
  division: string;
  difficulty: DifficultyLevel;

  // Actions
  setCurriculumLevel: (level: CurriculumLevel) => void;
  setSubject: (subject: string) => void;
  setSearchQuery: (query: string) => void;
  setDivision: (division: string) => void;
  setDifficulty: (difficulty: DifficultyLevel) => void;
  resetFilters: () => void;
}

const INITIAL_FILTER_STATE = {
  curriculumLevel: 'ALL' as CurriculumLevel,
  subject: 'ALL',
  searchQuery: '',
  division: 'ALL',
  difficulty: 'ALL' as DifficultyLevel,
};

export const useFilterStore = create<FilterState>((set) => ({
  ...INITIAL_FILTER_STATE,

  setCurriculumLevel: (curriculumLevel: CurriculumLevel) => {
    set({ curriculumLevel });
  },

  setSubject: (subject: string) => {
    set({ subject });
  },

  setSearchQuery: (searchQuery: string) => {
    set({ searchQuery });
  },

  setDivision: (division: string) => {
    set({ division });
  },

  setDifficulty: (difficulty: DifficultyLevel) => {
    set({ difficulty });
  },

  resetFilters: () => {
    set({ ...INITIAL_FILTER_STATE });
  },
}));
