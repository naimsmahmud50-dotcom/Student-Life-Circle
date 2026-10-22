/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - QUIZ & LIVE ASSESSMENT STORE:
 * MODULE:    Next.js 15+ Zustand Quiz & Challenge Store (useQuizStore)
 * TOPIC:     Active Question Pointer, Answer Buffering, Server-Authoritative Timer, Offline Count
 * FILE:      frontend/src/store/useQuizStore.ts
 * PURPOSE:   Coordinates reactive state for practice tests, timed mock examinations, and live
 *            competitive challenges. Keeps question indices, locally recorded response options,
 *            server-synchronized countdown timer preventing client clock skew, and monitors the
 *            offline queue for sync state in rural connectivity scenarios.
 * AUDIENCE:  Practice Arena Engineers, Live Challenge Developers & Examination Flow Testers
 * STANDARDS: Zero Layout Shift, Server-Authoritative Time Drift Correction, Zero-Emoji Architecture
 * ========================================================================================
 */

import { create } from './createStore';
import { getOfflineQueue } from '../lib/api-client';

export interface AnswerRecord {
  optionId: string;
  timeTakenSeconds: number;
  submittedAt: number;
}

export interface QuizState {
  activeAttemptId: string | null;
  activeQuestionIndex: number;
  totalQuestions: number;
  answers: Record<string, AnswerRecord>;
  timeRemainingSeconds: number;
  isTimerRunning: boolean;
  offlinePendingCount: number;
  isSubmitting: boolean;

  // Actions
  startAttempt: (attemptId: string, totalQuestions: number, initialTimeSeconds?: number) => void;
  selectAnswer: (questionId: string, optionId: string, timeTakenSeconds?: number) => void;
  nextQuestion: () => void;
  prevQuestion: () => void;
  jumpToQuestion: (index: number) => void;
  syncServerTimer: (serverSeconds: number) => void;
  decrementTimer: () => void;
  pauseTimer: () => void;
  resumeTimer: () => void;
  refreshOfflineCount: () => void;
  setIsSubmitting: (submitting: boolean) => void;
  resetQuiz: () => void;
}

export const useQuizStore = create<QuizState>((set, get) => ({
  activeAttemptId: null,
  activeQuestionIndex: 0,
  totalQuestions: 0,
  answers: {},
  timeRemainingSeconds: 0,
  isTimerRunning: false,
  offlinePendingCount: 0,
  isSubmitting: false,

  startAttempt: (attemptId: string, totalQuestions: number, initialTimeSeconds = 1800) => {
    const queue = getOfflineQueue();
    set({
      activeAttemptId: attemptId,
      activeQuestionIndex: 0,
      totalQuestions,
      answers: {},
      timeRemainingSeconds: initialTimeSeconds,
      isTimerRunning: true,
      offlinePendingCount: queue.length,
      isSubmitting: false,
    });
  },

  selectAnswer: (questionId: string, optionId: string, timeTakenSeconds = 0) => {
    set((state) => ({
      answers: {
        ...state.answers,
        [questionId]: {
          optionId,
          timeTakenSeconds,
          submittedAt: Date.now(),
        },
      },
    }));
  },

  nextQuestion: () => {
    set((state) => {
      const nextIndex = state.activeQuestionIndex + 1;
      return {
        activeQuestionIndex: nextIndex < state.totalQuestions ? nextIndex : state.activeQuestionIndex,
      };
    });
  },

  prevQuestion: () => {
    set((state) => {
      const prevIndex = state.activeQuestionIndex - 1;
      return {
        activeQuestionIndex: prevIndex >= 0 ? prevIndex : 0,
      };
    });
  },

  jumpToQuestion: (index: number) => {
    const state = get();
    if (index >= 0 && index < state.totalQuestions) {
      set({ activeQuestionIndex: index });
    }
  },

  syncServerTimer: (serverSeconds: number) => {
    // Server-authoritative timer synchronization prevents local system clock tampering
    set({
      timeRemainingSeconds: Math.max(0, serverSeconds),
      isTimerRunning: serverSeconds > 0,
    });
  },

  decrementTimer: () => {
    set((state) => {
      if (!state.isTimerRunning) return state;
      const nextTime = state.timeRemainingSeconds - 1;
      if (nextTime <= 0) {
        return {
          timeRemainingSeconds: 0,
          isTimerRunning: false,
        };
      }
      return { timeRemainingSeconds: nextTime };
    });
  },

  pauseTimer: () => {
    set({ isTimerRunning: false });
  },

  resumeTimer: () => {
    const state = get();
    if (state.timeRemainingSeconds > 0) {
      set({ isTimerRunning: true });
    }
  },

  refreshOfflineCount: () => {
    const queue = getOfflineQueue();
    set({ offlinePendingCount: queue.length });
  },

  setIsSubmitting: (submitting: boolean) => {
    set({ isSubmitting: submitting });
  },

  resetQuiz: () => {
    set({
      activeAttemptId: null,
      activeQuestionIndex: 0,
      totalQuestions: 0,
      answers: {},
      timeRemainingSeconds: 0,
      isTimerRunning: false,
      isSubmitting: false,
    });
  },
}));
