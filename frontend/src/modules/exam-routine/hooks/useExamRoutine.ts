/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    useExamRoutine Hook
 * TOPIC:     Client Routine State, Countdown Synchronizer & Filter Controller
 * FILE:      frontend/src/modules/exam-routine/hooks/useExamRoutine.ts
 * PURPOSE:   Manages reactive state for exam routines, Friday Mega Model Test countdowns,
 *            negative marking simulator, and subscription modal interactions.
 * STANDARDS: React 18/19 Hooks, Strict TypeScript, Zero-Emoji
 * ========================================================================================
 */

import { useState, useEffect, useMemo, useCallback } from 'react';
import {
  ExamRoutineItem,
  ExamType,
  TrackCategory,
  NegativeMarkSimulationRequest,
  NegativeMarkSimulationResponse,
} from '../types/examRoutine.types';
import {
  fetchExamRoutines,
  simulateNegativeMarkingScore,
  subscribeToRoutineAlert,
} from '../services/routineApiClient';

export interface CountdownState {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  isExpired: boolean;
}

export function useExamRoutine() {
  const [routines, setRoutines] = useState<ExamRoutineItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [selectedExamType, setSelectedExamType] = useState<ExamType | 'ALL'>('ALL');
  const [selectedTrack, setSelectedTrack] = useState<TrackCategory | 'ALL'>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeDay, setActiveDay] = useState<number>(42);
  const [megaTestTime, setMegaTestTime] = useState<string | null>(null);

  // Modal states
  const [selectedRoutineForSub, setSelectedRoutineForSub] = useState<ExamRoutineItem | null>(null);
  const [isSimulatorOpen, setIsSimulatorOpen] = useState<boolean>(false);
  const [simulationResult, setSimulationResult] = useState<NegativeMarkSimulationResponse | null>(null);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);

  // Load routines
  const loadRoutines = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetchExamRoutines({
        exam_type: selectedExamType === 'ALL' ? undefined : selectedExamType,
        track_category: selectedTrack === 'ALL' ? undefined : selectedTrack,
      });
      setRoutines(res.routines);
      setActiveDay(res.active_day);
      setMegaTestTime(res.mega_test_scheduled_at);
    } catch {
      // Fallback handled in client
    } finally {
      setIsLoading(false);
    }
  }, [selectedExamType, selectedTrack]);

  useEffect(() => {
    loadRoutines();
  }, [loadRoutines]);

  // Filtered routines with search
  const filteredRoutines = useMemo(() => {
    return routines.filter((r) => {
      const matchType = selectedExamType === 'ALL' || r.exam_type === selectedExamType;
      const matchTrack = selectedTrack === 'ALL' || r.track_category === selectedTrack;
      const matchSearch =
        searchQuery.trim() === '' ||
        r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        r.syllabus_summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
        r.routine_code.toLowerCase().includes(searchQuery.toLowerCase());
      return matchType && matchTrack && matchSearch;
    });
  }, [routines, selectedExamType, selectedTrack, searchQuery]);

  // Synchronized countdown calculation
  const [countdown, setCountdown] = useState<CountdownState>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    isExpired: false,
  });

  useEffect(() => {
    if (!megaTestTime) return;

    const targetDate = new Date(megaTestTime).getTime();

    const interval = setInterval(() => {
      const now = Date.now();
      const distance = targetDate - now;

      if (distance <= 0) {
        setCountdown({ days: 0, hours: 0, minutes: 0, seconds: 0, isExpired: true });
        clearInterval(interval);
      } else {
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        setCountdown({ days, hours, minutes, seconds, isExpired: false });
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [megaTestTime]);

  // Handle Score Simulation
  const handleSimulate = async (req: NegativeMarkSimulationRequest) => {
    setIsSimulating(true);
    try {
      const res = await simulateNegativeMarkingScore(req);
      setSimulationResult(res);
    } finally {
      setIsSimulating(false);
    }
  };

  // Handle Routine Subscription
  const handleSubscribe = async (routineId: string, channels: string[]) => {
    return await subscribeToRoutineAlert({
      routine_id: routineId,
      channels,
    });
  };

  return {
    routines: filteredRoutines,
    allRoutinesCount: routines.length,
    isLoading,
    activeDay,
    countdown,
    selectedExamType,
    setSelectedExamType,
    selectedTrack,
    setSelectedTrack,
    searchQuery,
    setSearchQuery,
    selectedRoutineForSub,
    setSelectedRoutineForSub,
    isSimulatorOpen,
    setIsSimulatorOpen,
    simulationResult,
    isSimulating,
    handleSimulate,
    handleSubscribe,
    refreshRoutines: loadRoutines,
  };
}
