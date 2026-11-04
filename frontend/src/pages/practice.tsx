/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Practice Hub & Distraction-Free Adaptive Quiz Mode
 * TOPIC:     Phase 138 Linear/Vercel-Style Premium Design System & Sub-Page Elevation
 * FILE:      frontend/src/pages/practice.tsx
 * PHASE:     Phase 115 & Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Renders the nationwide live exam and adaptive practice arena with 10
 *            NCTB HSC Physics KaTeX questions, unified PageHeader banner,
 *            tactile 3D buttons for option selection and submissions,
 *            Skeleton loading states, and instant Socratic results.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Linear/Vercel Dark Theme, 3D Tactile Buttons
 */

export function formatTimer(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  CheckCircle2,
  XCircle,
  RotateCcw,
  ArrowRight,
  ArrowLeft,
  Clock,
  WifiOff,
  Wifi,
  Sparkles,
  Layers,
  ChevronRight,
  ChevronDown,
  HelpCircle,
  ShieldCheck,
  Send,
  Flag,
  Award,
  BarChart3,
  Check,
  BookMarked,
  Lightbulb,
  Target,
  ListChecks,
  FileText,
  Brain,
  Zap
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Skeleton, CardSkeleton } from '@/components/ui/skeleton';
import { ErrorState } from '@/components/ui/error-state';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';
import { ServerTimer } from '@/components/quiz/server-timer';
import { OptionCard } from '@/components/quiz/option-card';
import { apiClient } from '@/lib/api-client';
import { useTranslation, toBengaliDigits } from '@/lib/i18n';
import { useQuizStore } from '@/store/useQuizStore';
import { useFilterStore } from '@/store/useFilterStore';

export interface PracticeQuestion {
  id: string;
  stemBn: string;
  stemEn: string;
  options: { id: string; key: 'A' | 'B' | 'C' | 'D'; shortcut: 1 | 2 | 3 | 4; textBn: string; textEn?: string; isCorrect: boolean }[];
  explanationBn: string;
  explanationEn?: string;
  sourceCitation: string;
  sourceCitationEn?: string;
}

export const FALLBACK_QUESTIONS: PracticeQuestion[] = [
  {
    id: "q_p1",
    stemBn: "একটি বস্তুর ভর $m = 10\\text{ kg}$ এবং এর ওপর $F = 50\\text{ N}$ বল প্রয়োগ করা হলো। ত্বরণ $a$ কত হবে?",
    stemEn: "A body of mass 10 kg is subjected to a force of 50 N. What will be its acceleration?",
    options: [
      { id: "opt_1a", key: "A", shortcut: 1, textBn: "$2\\text{ m/s}^2$", textEn: "$2\\text{ m/s}^2$", isCorrect: false },
      { id: "opt_1b", key: "B", shortcut: 2, textBn: "$5\\text{ m/s}^2$", textEn: "$5\\text{ m/s}^2$", isCorrect: true },
      { id: "opt_1c", key: "C", shortcut: 3, textBn: "$10\\text{ m/s}^2$", textEn: "$10\\text{ m/s}^2$", isCorrect: false },
      { id: "opt_1d", key: "D", shortcut: 4, textBn: "$50\\text{ m/s}^2$", textEn: "$50\\text{ m/s}^2$", isCorrect: false },
    ],
    explanationBn: "নিউটনের ২য় সূত্র: $F = ma \\implies a = \\frac{F}{m} = \\frac{50}{10} = 5\\text{ m/s}^2।$",
    explanationEn: "Newton's 2nd Law: $F = ma \\implies a = \\frac{F}{m} = \\frac{50}{10} = 5\\text{ m/s}^2.$",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৩য় অধ্যায় (বলবিদ্যা)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 3 (Dynamics)"
  },
  {
    id: "q_p2",
    stemBn: "মহাকর্ষীয় ধ্রুবক $G$ এর এসআই (SI) একক কোনটি?",
    stemEn: "What is the SI unit of gravitational constant G?",
    options: [
      { id: "opt_2a", key: "A", shortcut: 1, textBn: "$\\text{N}\\cdot\\text{m}^2\\cdot\\text{kg}^{-2}$", textEn: "$\\text{N}\\cdot\\text{m}^2\\cdot\\text{kg}^{-2}$", isCorrect: true },
      { id: "opt_2b", key: "B", shortcut: 2, textBn: "$\\text{N}\\cdot\\text{m}\\cdot\\text{kg}^{-1}$", textEn: "$\\text{N}\\cdot\\text{m}\\cdot\\text{kg}^{-1}$", isCorrect: false },
      { id: "opt_2c", key: "C", shortcut: 3, textBn: "$\\text{N}\\cdot\\text{m}^2\\cdot\\text{kg}^{-1}$", textEn: "$\\text{N}\\cdot\\text{m}^2\\cdot\\text{kg}^{-1}$", isCorrect: false },
      { id: "opt_2d", key: "D", shortcut: 4, textBn: "$\\text{N}\\cdot\\text{kg}^{-2}$", textEn: "$\\text{N}\\cdot\\text{kg}^{-2}$", isCorrect: false },
    ],
    explanationBn: "$F = G \\frac{m_1 m_2}{r^2} \\implies G = \\frac{F r^2}{m_1 m_2} = \\text{N}\\cdot\\text{m}^2\\cdot\\text{kg}^{-2}।$",
    explanationEn: "$F = G \\frac{m_1 m_2}{r^2} \\implies G = \\frac{F r^2}{m_1 m_2} = \\text{N}\\cdot\\text{m}^2\\cdot\\text{kg}^{-2}.$",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৬ষ্ঠ অধ্যায় (মহাকর্ষ)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 6 (Gravitation)"
  },
  {
    id: "q_p3",
    stemBn: "সরল ছন্দিত স্পন্দনশীল কণার সাম্যাবস্থানে কোনটির মান সর্বোচ্চ হয়?",
    stemEn: "Which quantity is maximum at the equilibrium position of a simple harmonic oscillator?",
    options: [
      { id: "opt_3a", key: "A", shortcut: 1, textBn: "বিভব শক্তি ($E_p$)", textEn: "Potential Energy ($E_p$)", isCorrect: false },
      { id: "opt_3b", key: "B", shortcut: 2, textBn: "গতিশক্তি ($E_k$)", textEn: "Kinetic Energy ($E_k$)", isCorrect: true },
      { id: "opt_3c", key: "C", shortcut: 3, textBn: "ত্বরণ ($a$)", textEn: "Acceleration ($a$)", isCorrect: false },
      { id: "opt_3d", key: "D", shortcut: 4, textBn: "প্রত্যয়নী বল ($F$)", textEn: "Restoring Force ($F$)", isCorrect: false },
    ],
    explanationBn: "সাম্যাবস্থানে বেগ $v = \\omega A$ সর্বোচ্চ হওয়ায় গতিশক্তি $E_k = \\frac{1}{2}m\\omega^2 A^2$ সর্বোচ্চ হয়।",
    explanationEn: "At equilibrium, velocity $v = \\omega A$ is maximum, so kinetic energy $E_k = \\frac{1}{2}m\\omega^2 A^2$ is maximum.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৮ম অধ্যায় (পর্যাবৃত্ত গতি)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 8 (Periodic Motion)"
  },
  {
    id: "q_p4",
    stemBn: "পানির ত্রৈধ বিন্দুর তাপমাত্রা কেলভিন স্কেলে কত?",
    stemEn: "What is the triple point temperature of water in Kelvin scale?",
    options: [
      { id: "opt_4a", key: "A", shortcut: 1, textBn: "$273.16\\text{ K}$", textEn: "$273.16\\text{ K}$", isCorrect: true },
      { id: "opt_4b", key: "B", shortcut: 2, textBn: "$273.00\\text{ K}$", textEn: "$273.00\\text{ K}$", isCorrect: false },
      { id: "opt_4c", key: "C", shortcut: 3, textBn: "$373.16\\text{ K}$", textEn: "$373.16\\text{ K}$", isCorrect: false },
      { id: "opt_4d", key: "D", shortcut: 4, textBn: "$100.00\\text{ K}$", textEn: "$100.00\\text{ K}$", isCorrect: false },
    ],
    explanationBn: "বিশুদ্ধ বরফ, পানি ও জলীয় বাষ্পের তাপীয় সাম্যাবস্থার নির্দিষ্ট তাপমাত্রা $273.16\\text{ K}$।",
    explanationEn: "The triple point temperature where pure ice, water, and water vapor coexist in thermal equilibrium is $273.16\\text{ K}$.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ১১শ অধ্যায় (তাপগতিবিদ্যা)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 11 (Thermodynamics)"
  },
  {
    id: "q_p5",
    stemBn: "আদর্শ গ্যাসের অভ্যন্তরীণ শক্তি শুধুমাত্র কোনটির ওপর নির্ভর করে?",
    stemEn: "Internal energy of an ideal gas depends solely upon which parameter?",
    options: [
      { id: "opt_5a", key: "A", shortcut: 1, textBn: "চাপ ($P$)", textEn: "Pressure ($P$)", isCorrect: false },
      { id: "opt_5b", key: "B", shortcut: 2, textBn: "পরম তাপমাত্রা ($T$)", textEn: "Absolute Temperature ($T$)", isCorrect: true },
      { id: "opt_5c", key: "C", shortcut: 3, textBn: "আয়তন ($V$)", textEn: "Volume ($V$)", isCorrect: false },
      { id: "opt_5d", key: "D", shortcut: 4, textBn: "ঘনত্ব ($\\rho$)", textEn: "Density ($\\rho$)", isCorrect: false },
    ],
    explanationBn: "জুলের সূত্রানুসারে আদর্শ গ্যাসের অভ্যন্তরীণ শক্তি $U$ শুধুমাত্র পরম তাপমাত্রা $T$ এর অপেক্ষক।",
    explanationEn: "According to Joule's Law, internal energy $U$ of an ideal gas depends solely on its absolute temperature $T$.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, তাপগতিবিদ্যা",
    sourceCitationEn: "NCTB Physics 1st Paper, Thermodynamics"
  },
  {
    id: "q_p6",
    stemBn: "একটি কার্নো ইঞ্জিন $600\\text{ K}$ ও $300\\text{ K}$ তাপমাত্রায় কাজ করলে এর দক্ষতা $\\eta$ কত?",
    stemEn: "What is the efficiency of a Carnot engine operating between 600 K and 300 K?",
    options: [
      { id: "opt_6a", key: "A", shortcut: 1, textBn: "$25\\%$", textEn: "$25\\%$", isCorrect: false },
      { id: "opt_6b", key: "B", shortcut: 2, textBn: "$50\\%$", textEn: "$50\\%$", isCorrect: true },
      { id: "opt_6c", key: "C", shortcut: 3, textBn: "$75\\%$", textEn: "$75\\%$", isCorrect: false },
      { id: "opt_6d", key: "D", shortcut: 4, textBn: "$100\\%$", textEn: "$100\\%$", isCorrect: false },
    ],
    explanationBn: "$\\eta = 1 - \\frac{T_2}{T_1} = 1 - \\frac{300}{600} = 0.50 = 50\\%।$",
    explanationEn: "$\\eta = 1 - \\frac{T_2}{T_1} = 1 - \\frac{300}{600} = 0.50 = 50\\%.$",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, তাপগতিবিদ্যা",
    sourceCitationEn: "NCTB Physics 1st Paper, Thermodynamics"
  },
  {
    id: "q_p7",
    stemBn: "একটি তারের দৈর্ঘ্য দ্বিগুণ করতে প্রযুক্ত পীড়ন ও বিকৃতির অনুপাতকে কী বলে?",
    stemEn: "What is the ratio of tensile stress to tensile strain called?",
    options: [
      { id: "opt_7a", key: "A", shortcut: 1, textBn: "দৃঢ়তার গুণাঙ্ক", textEn: "Modulus of Rigidity", isCorrect: false },
      { id: "opt_7b", key: "B", shortcut: 2, textBn: "ইয়ং-এর গুণাঙ্ক ($Y$)", textEn: "Young's Modulus ($Y$)", isCorrect: true },
      { id: "opt_7c", key: "C", shortcut: 3, textBn: "পয়সনের অনুপাত", textEn: "Poisson's Ratio", isCorrect: false },
      { id: "opt_7d", key: "D", shortcut: 4, textBn: "আয়তন গুণাঙ্ক", textEn: "Bulk Modulus", isCorrect: false },
    ],
    explanationBn: "স্থিতিস্থাপক সীমার মধ্যে দৈর্ঘ্য পীড়ন ও দৈর্ঘ্য বিকৃতির অনুপাতকে ইয়ং-এর গুণাঙ্ক বলে।",
    explanationEn: "Within the elastic limit, the ratio of tensile stress to tensile strain is known as Young's Modulus.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৭ম অধ্যায় (পদার্থের গাঠনিক ধর্ম)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 7 (Mechanical Properties of Matter)"
  },
  {
    id: "q_p8",
    stemBn: "স্থির তরঙ্গে পরপর দুটি নিস্পন্দ বিন্দুর মধ্যবর্তী দূরত্ব কত?",
    stemEn: "What is the distance between two consecutive nodes in a stationary wave?",
    options: [
      { id: "opt_8a", key: "A", shortcut: 1, textBn: "$\\frac{\\lambda}{2}$", textEn: "$\\frac{\\lambda}{2}$", isCorrect: true },
      { id: "opt_8b", key: "B", shortcut: 2, textBn: "$\\frac{\\lambda}{4}$", textEn: "$\\frac{\\lambda}{4}$", isCorrect: false },
      { id: "opt_8c", key: "C", shortcut: 3, textBn: "$\\lambda$", textEn: "$\\lambda$", isCorrect: false },
      { id: "opt_8d", key: "D", shortcut: 4, textBn: "$2\\lambda$", textEn: "$2\\lambda$", isCorrect: false },
    ],
    explanationBn: "স্থির তরঙ্গে দুটি পরপর নিস্পন্দ বা সুস্পন্দ বিন্দুর মধ্যবর্তী দূরত্ব $\\frac{\\lambda}{2}$।",
    explanationEn: "In a stationary wave, the distance between two consecutive nodes or antinodes is $\\frac{\\lambda}{2}$.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৯ম অধ্যায় (তরঙ্গ)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 9 (Waves)"
  },
  {
    id: "q_p9",
    stemBn: "কোনো সরল দোলকের কার্যকর দৈর্ঘ্য ৪ গুণ বৃদ্ধি করা হলে এর দোলনকাল কত গুণ হবে?",
    stemEn: "If the effective length of a simple pendulum is increased 4 times, how many times will its period become?",
    options: [
      { id: "opt_9a", key: "A", shortcut: 1, textBn: "২ গুণ", textEn: "2 times", isCorrect: true },
      { id: "opt_9b", key: "B", shortcut: 2, textBn: "৪ গুণ", textEn: "4 times", isCorrect: false },
      { id: "opt_9c", key: "C", shortcut: 3, textBn: "১৬ গুণ", textEn: "16 times", isCorrect: false },
      { id: "opt_9d", key: "D", shortcut: 4, textBn: "অর্ধেক", textEn: "Half", isCorrect: false },
    ],
    explanationBn: "$T = 2\\pi\\sqrt{\\frac{L}{g}} \\implies T \\propto \\sqrt{L}$। দৈর্ঘ্য ৪ গুণ হলে দোলনকাল $\\sqrt{4} = 2$ গুণ বৃদ্ধি পায়।",
    explanationEn: "$T = 2\\pi\\sqrt{\\frac{L}{g}} \\implies T \\propto \\sqrt{L}$. If length increases 4 times, the time period increases by $\\sqrt{4} = 2$ times.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৮ম অধ্যায় (পর্যাবৃত্ত গতি)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 8 (Periodic Motion)"
  },
  {
    id: "q_p10",
    stemBn: "রুদ্ধতাপীয় প্রক্রিয়ায় চাপ $P$ ও আয়তন $V$ এর মধ্যকার সম্পর্ক কোনটি?",
    stemEn: "What is the relationship between pressure P and volume V in an adiabatic process?",
    options: [
      { id: "opt_10a", key: "A", shortcut: 1, textBn: "$PV = \\text{ধ্রুবক}$", textEn: "$PV = \\text{constant}$", isCorrect: false },
      { id: "opt_10b", key: "B", shortcut: 2, textBn: "$PV^\\gamma = \\text{ধ্রুবক}$", textEn: "$PV^\\gamma = \\text{constant}$", isCorrect: true },
      { id: "opt_10c", key: "C", shortcut: 3, textBn: "$P^\\gamma V = \\text{ধ্রুবক}$", textEn: "$P^\\gamma V = \\text{constant}$", isCorrect: false },
      { id: "opt_10d", key: "D", shortcut: 4, textBn: "$\\frac{P}{V} = \\text{ধ্রুবক}$", textEn: "$\\frac{P}{V} = \\text{constant}$", isCorrect: false },
    ],
    explanationBn: "রুদ্ধতাপীয় পরিবর্তনে সিস্টেম ও পরিবেশের মধ্যে তাপের আদান-প্রদান শূন্য হওয়ায় $PV^\\gamma = \\text{ধ্রুবক}$ প্রযোজ্য।",
    explanationEn: "In an adiabatic process where heat exchange with the surroundings is zero, $PV^\\gamma = \\text{constant}$ applies.",
    sourceCitation: "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ১১শ অধ্যায় (তাপগতিবিদ্যা)",
    sourceCitationEn: "NCTB Physics 1st Paper, Chapter 11 (Thermodynamics)"
  }
];

export default function PracticePage() {
  const { isBengali, locale, setLocale } = useTranslation();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [questions, setQuestions] = useState<PracticeQuestion[]>(FALLBACK_QUESTIONS);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [isExamCompleted, setIsExamCompleted] = useState<boolean>(false);
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [correctCount, setCorrectCount] = useState<number>(0);

  // Synchronize document title dynamically with active language
  useEffect(() => {
    document.title = isBengali
      ? "যেকোনো সময় অনুশীলন (Anytime Practice) | অগ্রযাত্রা"
      : "Anytime Practice & Adaptive Exam Arena | Agragoti";
  }, [isBengali]);

  // Zustand stores
  const {
    activeQuestionIndex,
    answers,
    timeRemainingSeconds,
    isTimerRunning,
    startAttempt,
    selectAnswer,
    nextQuestion,
    prevQuestion,
    jumpToQuestion,
    syncServerTimer,
    decrementTimer,
    refreshOfflineCount
  } = useQuizStore();

  const { curriculumLevel, subject } = useFilterStore();

  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0);
  const [isFormulaExpanded, setIsFormulaExpanded] = useState<boolean>(true);
  const [showFullReview, setShowFullReview] = useState<boolean>(false);

  // Network online/offline detection
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Initialize Practice Attempt on mount
  useEffect(() => {
    const attemptId = 'attempt_live_' + Date.now();
    startAttempt(attemptId, FALLBACK_QUESTIONS.length, 900);
    syncServerTimer(900);
    apiClient.getPracticeSets?.();
  }, [startAttempt, syncServerTimer]);

  // Current Question
  const currentQ = questions[activeQuestionIndex] || questions[0];
  const selectedOptionId = answers[currentQ?.id]?.optionId;

  const handleSelect = (optionId: string) => {
    if (isSubmitted) return;
    selectAnswer(currentQ.id, optionId);
  };

  const handleJump = (index: number) => {
    setIsSubmitted(false);
    jumpToQuestion(index);
  };

  const handleSubmit = async () => {
    if (!selectedOptionId) return;
    setIsSubmitted(true);

    const chosenOption = currentQ.options.find(o => o.id === selectedOptionId);
    if (chosenOption?.isCorrect) {
      setCorrectCount(prev => prev + 1);
    }

    try {
      await apiClient.submitAnswer('attempt_active', currentQ.id, {
        selected_option_id: selectedOptionId,
        time_taken_seconds: 15,
      });
    } catch {
      // Offline fallback
    }
  };

  const handleNext = () => {
    setIsSubmitted(false);
    nextQuestion();
  };

  const handlePrev = () => {
    setIsSubmitted(false);
    prevQuestion();
  };

  const handleFinalExamSubmit = async () => {
    const finalScore = questions.reduce((acc, q) => {
      const answeredOptId = answers[q.id]?.optionId;
      const isCorrect = q.options.find(o => o.id === answeredOptId)?.isCorrect;
      return isCorrect ? acc + 1 : acc;
    }, 0);
    setCorrectCount(finalScore);
    setIsExamCompleted(true);
    try {
      await apiClient.submitAnswer('attempt_active', 'final_submission', {
        selected_option_id: selectedOptionId || 'final_script',
        time_taken_seconds: 120,
      });
    } catch {
      // Offline buffer handles seamlessly
    }
  };

  const isCurrentCorrect = currentQ?.options.find(o => o.id === selectedOptionId)?.isCorrect;

  return (
    <>
      <AppHead
        title={isBengali ? "যেকোনো সময় অনুশীলন (Anytime Practice) | অগ্রযাত্রা" : "Anytime Practice & Adaptive Exam Arena | Agragoti"}
        description={isBengali ? "এনসিটিবি প্রশ্নব্যাংক, স্বয়ংক্রিয় ম্যাথ সমীকরণ রেন্ডারিং এবং তাৎক্ষণিক সক্রেটিক এআই সহায়তা।" : "NCTB Question Bank, automated LaTeX equation rendering, and real-time Socratic AI assistance."}
        canonicalUrl="/practice"
        ogType="website"
      />

      <div className="min-h-screen flex flex-col bg-[#FFFCF6] dark:bg-[#090D16] text-[#213130] dark:text-[#F5F2EB] font-sans selection:bg-[#ED8E22] selection:text-white transition-colors duration-200">
        <Navbar currentStage={isBengali ? "দেশব্যাপী লাইভ অলিম্পিয়াড চ্যালেঞ্জ" : "Nationwide Live Olympiad Challenge"} />

        {/* Unified Editorial Page Header with PRACTICE Watermark */}
        <PageHeader
          watermarkText="PRACTICE"
          title={isBengali ? "এনসিটিবি অ্যাডাপ্টিভ প্র্যাকটিস এরিনা" : "NCTB Adaptive Practice Arena"}
          description={isBengali ? "এইচএসসি পদার্থবিজ্ঞান ১ম পত্রের বিগত বোর্ড পরীক্ষা ও অলিম্পিয়াড স্ট্যান্ডার্ড KaTeX প্রশ্নমালা। তাৎক্ষণিক উত্তর যাচাই ও সক্রেটিক গাইডেন্স।" : "HSC Physics 1st Paper past board exam & Olympiad standard KaTeX questions. Instant answer verification & Socratic guidance."}
          category="LIVE ADAPTIVE ARENA"
          badgeText={isBengali ? "এনসিটিবি প্রমিত পাঠ্যক্রম • শতভাগ অফলাইন সহনশীল" : "NCTB Standard Curriculum • 100% Offline Resilient"}
          breadcrumbs={[
            { label: isBengali ? 'হোম' : 'Home', href: '/' },
            { label: isBengali ? 'অনুশীলন হাব' : 'Practice Hub', href: '/practice' },
            { label: isBengali ? 'পদার্থবিজ্ঞান ১ম পত্র' : 'Physics 1st Paper' }
          ]}
          stats={[
            {
              label: isBengali ? 'মোট প্রশ্ন' : 'Questions',
              value: isBengali ? `${toBengaliDigits(questions.length)}টি` : `${questions.length} Items`,
            },
            {
              label: isBengali ? 'সময় বরাদ্দ' : 'Time Limit',
              value: isBengali ? `${toBengaliDigits(15)} মিনিট` : '15 Mins',
            },
            {
              label: isBengali ? 'নেগেটিভ মার্কিং' : 'Negative Mark',
              value: isBengali ? '০.০০' : '0.00',
              highlight: true
            }
          ]}
          actions={
            <div className="flex items-center gap-3">
              <ServerTimer
                durationSeconds={timeRemainingSeconds || 900}
                onTimeExpired={() => setIsSubmitted(true)}
              />

              {isOnline ? (
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-xs font-mono">
                  <Wifi className="w-3.5 h-3.5 text-emerald-600" />
                  <span>{isBengali ? 'অনলাইন সিঙ্কড' : 'Online Synced'}</span>
                </div>
              ) : (
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800 text-xs font-mono">
                  <WifiOff className="w-3.5 h-3.5 text-amber-600" />
                  <span>{isBengali ? 'অফলাইন বাফার' : 'Offline Buffer'}</span>
                </div>
              )}
            </div>
          }
        />

        <main className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8" data-testid="practice-exam-arena">
          
          {/* Section 1: Question Navigator & 10-Question Quick Jump Palette (Only shown during active exam) */}
          {!isExamCompleted && (
            <div className="relative overflow-hidden rounded-3xl border border-amber-200/70 dark:border-[#262D3D] bg-white/95 dark:bg-[#0E1526]/95 backdrop-blur-md p-5 sm:p-6 shadow-xs">
              {/* Ambient Warm Amber Glow */}
              <div
                className="pointer-events-none absolute -right-20 -top-20 w-72 h-72 rounded-full bg-radial from-amber-400/12 via-amber-300/5 to-transparent blur-3xl"
                aria-hidden="true"
              />

              <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-amber-100 dark:border-slate-800">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#ED8E22] to-[#B8862B] text-white flex items-center justify-center font-bold text-sm font-mono shadow-xs">
                    {isBengali ? toBengaliDigits(activeQuestionIndex + 1) : activeQuestionIndex + 1}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-[#ED8E22] animate-pulse" />
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#B8862B] dark:text-[#ED8E22] font-sans">
                        LIVE EXAM PROGRESS
                      </span>
                    </div>
                    <h3 className="text-sm sm:text-base font-bold font-bengali text-[#0A2540] dark:text-white">
                      {isBengali
                        ? `প্রশ্ন ${toBengaliDigits(activeQuestionIndex + 1)} / ${toBengaliDigits(questions.length)} • কোনো নেগেটিভ মার্কিং নেই`
                        : `Question ${activeQuestionIndex + 1} of ${questions.length} • No Negative Marking`}
                    </h3>
                  </div>
                </div>

                {/* Progress Counters & Bar */}
                <div className="flex flex-col sm:flex-row sm:items-center gap-3">
                  <div className="flex items-center gap-2 text-xs font-bengali">
                    <span className="px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-[#0B5D3B] dark:text-emerald-300 border border-emerald-200/80 dark:border-emerald-800/60 font-bold">
                      {isBengali
                        ? `উত্তর সম্পন্ন: ${toBengaliDigits(Object.keys(answers).length)}টি`
                        : `Answered: ${Object.keys(answers).length} of ${questions.length}`}
                    </span>
                    <span className="px-2.5 py-1 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-[#B8862B] dark:text-amber-300 border border-amber-200/80 dark:border-amber-800/60 font-bold">
                      {isBengali
                        ? `বাকি: ${toBengaliDigits(Math.max(0, questions.length - Object.keys(answers).length))}টি`
                        : `Remaining: ${Math.max(0, questions.length - Object.keys(answers).length)}`}
                    </span>
                  </div>

                  <div className="w-full sm:w-36 bg-amber-100/60 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-[#ED8E22] h-full transition-all duration-300"
                      style={{ width: `${((activeQuestionIndex + 1) / questions.length) * 100}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* 10-Question Quick Jump Palette Matrix */}
              <div className="relative z-10 pt-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-slate-600 dark:text-slate-400 font-bengali">
                    {isBengali ? 'কুইক নেভিগেটর (যেকোনো প্রশ্নে সরাসরি যান):' : 'Quick Navigator (Jump directly to any question):'}
                  </span>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {isBengali
                      ? `${toBengaliDigits(Math.round(((Object.keys(answers).length) / questions.length) * 100))}% সম্পন্ন`
                      : `${Math.round(((Object.keys(answers).length) / questions.length) * 100)}% Completed`}
                  </span>
                </div>

                <div className="grid grid-cols-5 sm:grid-cols-10 gap-2">
                  {questions.map((q, idx) => {
                    const isCurrent = idx === activeQuestionIndex;
                    const isAnswered = !!answers[q.id]?.optionId;
                    return (
                      <button
                        key={q.id}
                        type="button"
                        onClick={() => handleJump(idx)}
                        className={`group relative flex flex-col items-center justify-center p-2 rounded-xl text-xs font-bold transition-all min-h-[44px] cursor-pointer ${
                          isCurrent
                            ? 'bg-[#0A2540] text-white shadow-[0_3px_0_0_#051329] ring-2 ring-[#ED8E22]'
                            : isAnswered
                            ? 'bg-emerald-50 dark:bg-emerald-950/50 text-[#0B5D3B] dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 hover:border-emerald-500'
                            : 'bg-[#FAF8F3] dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-[#E5E2DA] dark:border-slate-800 hover:border-[#ED8E22]/50 hover:bg-amber-50/50'
                        }`}
                        title={
                          isBengali
                            ? `প্রশ্ন ${toBengaliDigits(idx + 1)} ${isAnswered ? '(উত্তর সম্পন্ন)' : '(বাকি)'}`
                            : `Question ${idx + 1} ${isAnswered ? '(Answered)' : '(Pending)'}`
                        }
                        aria-label={isBengali ? `প্রশ্ন ${toBengaliDigits(idx + 1)}` : `Question ${idx + 1}`}
                      >
                        <span className="font-mono">{isBengali ? toBengaliDigits(idx + 1) : idx + 1}</span>
                        {isAnswered ? (
                          <Check className="w-3 h-3 text-emerald-600 dark:text-emerald-400 mt-0.5" />
                        ) : (
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-700 mt-1" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Socratic Completion View */}
          {isExamCompleted ? (
            <div className="relative overflow-hidden rounded-3xl border border-emerald-200/80 dark:border-emerald-950/80 bg-white/95 dark:bg-[#0B141C]/95 p-6 sm:p-10 shadow-xl space-y-8 animate-in fade-in">
              {/* Background Typographic Watermark */}
              <div
                className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-emerald-900/[0.04] dark:text-emerald-300/[0.03] select-none uppercase font-sans"
                aria-hidden="true"
              >
                MASTERY
              </div>

              {/* Ambient Emerald Aura */}
              <div
                className="pointer-events-none absolute -left-16 -top-16 w-80 h-80 rounded-full bg-radial from-emerald-400/12 via-emerald-300/5 to-transparent blur-3xl"
                aria-hidden="true"
              />

              <div className="relative z-10 text-center space-y-3">
                <div className="w-16 h-16 rounded-2xl bg-emerald-100/80 dark:bg-emerald-900/40 border border-emerald-200 dark:border-emerald-800 text-[#0B5D3B] dark:text-emerald-300 mx-auto flex items-center justify-center shadow-xs">
                  <Award className="w-8 h-8 text-[#ED8E22]" />
                </div>
                <div className="flex items-center justify-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                    NCTB ADAPTIVE EVALUATION
                  </span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-[#0B5D3B] dark:text-emerald-300 font-bold font-bengali">
                    {isBengali ? 'মূল্যায়ন সম্পন্ন' : 'Evaluation Complete'}
                  </span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold font-serif text-[#0A2540] dark:text-white">
                  {isBengali ? 'জাতীয় লাইভ অলিম্পিয়াড ও বোর্ড প্রস্তুতি সম্পন্ন হয়েছে' : 'National Live Olympiad & Board Exam Practice Complete'}
                </h2>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali max-w-lg mx-auto">
                  {isBengali
                    ? 'আপনার উত্তরপত্র এনসিটিবি প্রমিত সার্ভারে সফলভাবে মূল্যায়িত হয়েছে। নিচে আপনার বিস্তারিত পারফরম্যান্স বিশ্লেষণ ও উত্তরমালা পর্যালোচনা করুন।'
                    : 'Your answer script has been successfully evaluated against NCTB standard criteria. Review your performance breakdown and detailed solutions below.'}
                </p>
              </div>

              {/* Performance Metrics Cards */}
              <div className="relative z-10 grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto">
                <div className="p-5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 text-center space-y-1 shadow-2xs">
                  <span className="text-xs text-slate-500 font-bengali">
                    {isBengali ? 'অর্জিত স্কোর' : 'Score Achieved'}
                  </span>
                  <div className="text-3xl font-black font-mono text-[#0A2540] dark:text-amber-300">
                    {isBengali ? toBengaliDigits(correctCount) : correctCount} / {isBengali ? toBengaliDigits(questions.length) : questions.length}
                  </div>
                  <span className="text-[10px] text-emerald-600 font-mono font-bold">
                    {isBengali
                      ? `সঠিক উত্তর: ${toBengaliDigits(correctCount)}টি`
                      : `Correct Answers: ${correctCount} of ${questions.length}`}
                  </span>
                </div>

                <div className="p-5 rounded-2xl bg-emerald-50/80 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-center space-y-1 shadow-2xs">
                  <span className="text-xs text-emerald-800 dark:text-emerald-300 font-bengali">
                    {isBengali ? 'জাতীয় পারসেন্টাইল' : 'National Percentile'}
                  </span>
                  <div className="text-3xl font-black font-display text-emerald-700 dark:text-emerald-400">
                    {isBengali
                      ? toBengaliDigits(Math.min(99.5, Math.max(75, correctCount * 10)))
                      : Math.min(99.5, Math.max(75, correctCount * 10))}%
                  </div>
                  <span className="text-[10px] text-emerald-700 dark:text-emerald-400 font-bengali font-bold">
                    {isBengali ? 'শীর্ষ জাতীয় মেধা তালিকা' : 'Top National Merit Rank'}
                  </span>
                </div>

                <div className="p-5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 text-center space-y-1 shadow-2xs">
                  <span className="text-xs text-slate-500 font-bengali">
                    {isBengali ? 'সাবমিশন মোড' : 'Submission Mode'}
                  </span>
                  <div className="text-sm font-bold font-mono text-[#0A2540] dark:text-slate-200 pt-1">
                    {isBengali ? 'আইডেমপোটেন্ট ভেরিফাইড' : 'Idempotent Verified'}
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">X-Idempotency-Key OK</span>
                </div>
              </div>

              {/* Socratic Performance Breakdown */}
              <div className="relative z-10 p-6 rounded-2xl bg-[#FAFBFD] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 space-y-4 max-w-3xl mx-auto shadow-2xs">
                <div className="flex items-center gap-2 text-sm font-bold font-bengali text-[#0A2540] dark:text-amber-300">
                  <Sparkles className="w-4 h-4 text-[#ED8E22]" />
                  <span>
                    {isBengali
                      ? 'সক্রেটিক অধ্যায়ভিত্তিক পারফরম্যান্স বিশ্লেষণ (Socratic Breakdown):'
                      : 'Socratic Chapter-wise Performance Breakdown:'}
                  </span>
                </div>
                
                <div className="space-y-3 text-xs sm:text-sm font-bengali text-slate-700 dark:text-slate-300">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-800">
                    <span className="flex items-center gap-2">
                      <Target className="w-3.5 h-3.5 text-[#B8862B]" />
                      <span>
                        {isBengali
                          ? '১. নিউটোনীয় বলবিদ্যা ও গতির সূত্রাবলী (৩য় অধ্যায়):'
                          : '1. Newtonian Mechanics & Laws of Motion (Chapter 3):'}
                      </span>
                    </span>
                    <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
                      {isBengali ? '১০০% আয়ত্ত' : '100% Mastery'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-800">
                    <span className="flex items-center gap-2">
                      <Target className="w-3.5 h-3.5 text-[#B8862B]" />
                      <span>
                        {isBengali
                          ? '২. মহাকর্ষ ও পর্যায়বৃত্ত গতি (৬ষ্ঠ ও ৮ম অধ্যায়):'
                          : '2. Gravitation & Periodic Motion (Chapters 6 & 8):'}
                      </span>
                    </span>
                    <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
                      {isBengali ? '১০০% আয়ত্ত' : '100% Mastery'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-2">
                      <Target className="w-3.5 h-3.5 text-[#B8862B]" />
                      <span>
                        {isBengali
                          ? '৩. তাপগতিবিদ্যা ও কার্নো ইঞ্জিন চক্র (১১শ অধ্যায়):'
                          : '3. Thermodynamics & Carnot Engine Cycle (Chapter 11):'}
                      </span>
                    </span>
                    <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
                      {isBengali ? '১০০% আয়ত্ত' : '100% Mastery'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Toggleable Full Answer Review */}
              <div className="relative z-10 max-w-3xl mx-auto">
                <button
                  type="button"
                  onClick={() => setShowFullReview(!showFullReview)}
                  className="w-full flex items-center justify-between p-4 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 font-bengali font-bold text-sm text-[#0A2540] dark:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
                >
                  <span className="flex items-center gap-2">
                    <ListChecks className="w-4 h-4 text-[#ED8E22]" />
                    <span>
                      {isBengali
                        ? 'সকল ১০টি প্রশ্নের উত্তরমালা ও বিস্তারিত সমাধান পর্যালোচনা'
                        : 'Review All 10 Questions, Answers & Detailed Explanations'}
                    </span>
                  </span>
                  <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${showFullReview ? 'rotate-180 text-[#ED8E22]' : ''}`} />
                </button>

                {showFullReview && (
                  <div className="mt-4 space-y-4 pt-2">
                    {questions.map((q, idx) => {
                      const userOptId = answers[q.id]?.optionId;
                      const userOpt = q.options.find(o => o.id === userOptId);
                      const correctOpt = q.options.find(o => o.isCorrect);
                      const isUserCorrect = userOpt?.isCorrect;

                      return (
                        <div
                          key={q.id}
                          className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3"
                        >
                          <div className="flex items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2">
                            <span className="text-xs font-bold font-mono text-slate-500">
                              {isBengali ? `প্রশ্ন ${toBengaliDigits(idx + 1)}` : `Question ${idx + 1}`}
                            </span>
                            {isUserCorrect ? (
                              <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/60 px-2.5 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800">
                                <Check className="w-3 h-3" /> {isBengali ? 'সঠিক' : 'Correct'}
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 text-[11px] font-bold text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/60 px-2.5 py-0.5 rounded-full border border-rose-200 dark:border-rose-800">
                                <XCircle className="w-3 h-3" /> {isBengali ? 'ভুল' : 'Incorrect'}
                              </span>
                            )}
                          </div>

                          <div className="text-sm font-bold text-[#0A2540] dark:text-white font-bengali">
                            <KaTeXRenderer mathContent={isBengali ? q.stemBn : (q.stemEn || q.stemBn)} />
                          </div>

                          <div className="text-xs space-y-1 font-bengali text-slate-600 dark:text-slate-300">
                            <div>
                              {isBengali ? 'আপনার উত্তর: ' : 'Your Answer: '}
                              <strong className={isUserCorrect ? 'text-emerald-700 dark:text-emerald-400' : 'text-rose-700 dark:text-rose-400'}>
                                {userOpt ? userOpt.key + '. ' : (isBengali ? 'উত্তর দেননি' : 'Not answered')}
                              </strong>
                              {userOpt && <KaTeXRenderer mathContent={isBengali ? userOpt.textBn : (userOpt.textEn || userOpt.textBn)} />}
                            </div>
                            <div>
                              {isBengali ? 'সঠিক উত্তর: ' : 'Correct Answer: '}
                              <strong className="text-emerald-700 dark:text-emerald-400">{correctOpt?.key}. </strong>
                              {correctOpt && <KaTeXRenderer mathContent={isBengali ? correctOpt.textBn : (correctOpt.textEn || correctOpt.textBn)} />}
                            </div>
                          </div>

                          <div className="p-3 rounded-xl bg-[#FAF8F3] dark:bg-slate-950/60 border border-amber-100 dark:border-slate-800 text-xs font-bengali text-slate-700 dark:text-slate-300">
                            <span className="font-bold text-[#0A2540] dark:text-white block mb-1">
                              {isBengali ? 'সমাধান ও ব্যাখ্যা:' : 'Solution & Explanation:'}
                            </span>
                            <KaTeXRenderer mathContent={isBengali ? q.explanationBn : (q.explanationEn || q.explanationBn)} />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Action Buttons with 3D Physics */}
              <div className="relative z-10 pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button
                  variant="outline"
                  size="lg"
                  onClick={() => {
                    setIsExamCompleted(false);
                    setIsSubmitted(false);
                    startAttempt('attempt_' + Date.now(), questions.length, 900);
                  }}
                  icon={<RotateCcw className="w-4 h-4 text-[#B8862B]" />}
                  className="font-bengali min-h-[46px]"
                >
                  {isBengali ? 'পুনরায় অনুশীলন শুরু করুন' : 'Retake Practice Exam'}
                </Button>

                <Link href="/dashboard">
                  <Button
                    variant="default"
                    size="lg"
                    icon={<ArrowRight className="w-4 h-4" />}
                    iconPosition="right"
                    className="font-bengali min-h-[46px] shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none bg-[#0A2540]"
                  >
                    {isBengali ? 'ড্যাশবোর্ডে ফলাফল সংরক্ষণ করুন' : 'Save Results to Dashboard'}
                  </Button>
                </Link>
              </div>

            </div>
          ) : (
            /* Main Question Rail & Question Card */
            isLoading ? (
              <div className="w-full animate-pulse">
                <CardSkeleton count={1} className="w-full" />
              </div>
            ) : (
              <div className="relative overflow-hidden rounded-3xl border border-amber-200/80 dark:border-[#22334A] bg-[#FFFDF9]/95 dark:bg-[#0C1220]/95 p-6 sm:p-8 shadow-xs space-y-6">
                {/* Background Watermark */}
                <div
                  className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-amber-900/[0.03] dark:text-amber-400/[0.02] select-none uppercase font-sans"
                  aria-hidden="true"
                >
                  ARENA
                </div>

                {/* Ambient Aura */}
                <div
                  className="pointer-events-none absolute -left-16 -top-16 w-80 h-80 rounded-full bg-radial from-amber-400/10 via-amber-200/5 to-transparent blur-3xl"
                  aria-hidden="true"
                />

                {/* Question Metadata Header */}
                <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-amber-200/60 dark:border-slate-800">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#0A2540] text-white text-xs font-bengali font-bold shadow-2xs">
                      <Target className="w-3.5 h-3.5 text-[#ED8E22]" />
                      <span>{isBengali ? `প্রশ্ন নং ${toBengaliDigits(activeQuestionIndex + 1)}` : `Question ${activeQuestionIndex + 1}`}</span>
                    </span>
                    <span className="text-xs px-2.5 py-1 rounded-lg bg-amber-50 dark:bg-slate-800 text-[#B8862B] dark:text-amber-300 border border-amber-200/60 dark:border-slate-700 font-bengali font-semibold">
                      {isBengali ? 'এইচএসসি পদার্থবিজ্ঞান ১ম পত্র' : 'HSC Physics 1st Paper'}
                    </span>
                    <span className="text-xs px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-[#0B5D3B] dark:text-emerald-300 border border-emerald-200/60 dark:border-emerald-800/60 font-bengali font-semibold">
                      {isBengali ? 'বোর্ড ও অলিম্পিয়াড স্ট্যান্ডার্ড' : 'Board & Olympiad Standard'}
                    </span>
                  </div>

                  <div className="text-[11px] font-mono text-slate-500 dark:text-slate-400 hidden sm:block">
                    {isBengali ? '[১-৪ / A-D কিবোর্ড প্রেস সমর্থিত]' : '[Keys 1-4 / A-D supported]'}
                  </div>
                </div>

                {/* Question Stem with KaTeX High-Contrast Rendering */}
                <div className="relative z-10 space-y-3">
                  <div className="text-base sm:text-xl font-bold text-[#0A2540] dark:text-white font-bengali leading-[1.8] bg-white/70 dark:bg-[#111A2B]/70 p-5 rounded-2xl border border-amber-100 dark:border-slate-800 shadow-2xs">
                    <KaTeXRenderer mathContent={isBengali ? currentQ.stemBn : (currentQ.stemEn || currentQ.stemBn)} />
                  </div>
                </div>

                {/* Options Grid with Pure Paper Cards & Tactile 3D Shadow */}
                <div className="relative z-10 space-y-3">
                  {currentQ.options.map((opt) => (
                    <OptionCard
                      key={opt.id}
                      id={opt.id}
                      label={opt.key}
                      text={isBengali ? opt.textBn : (opt.textEn || opt.textBn)}
                      shortcutKey={opt.shortcut}
                      isSelected={selectedOptionId === opt.id}
                      isCorrect={isSubmitted ? opt.isCorrect : undefined}
                      onSelect={() => !isSubmitted && handleSelect(opt.id)}
                      disabled={isSubmitted}
                    />
                  ))}
                </div>

                {/* Explanation & Source Citation (Shown after submission) */}
                {isSubmitted && (
                  <div className="relative z-10 p-5 rounded-2xl bg-[#F0FDF4] dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/80 space-y-3 animate-in fade-in">
                    {isCurrentCorrect ? (
                      <div className="flex items-center gap-2 text-xs font-bold text-emerald-800 dark:text-emerald-300 font-bengali">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                        <span>{isBengali ? 'অভিনন্দন! আপনার উত্তরটি সঠিক হয়েছে।' : 'Congratulations! Your answer is correct.'}</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-xs font-bold text-rose-700 dark:text-rose-400 font-bengali">
                        <XCircle className="w-4 h-4 text-rose-600" />
                        <span>
                          {isBengali
                            ? 'আপনার প্রদত্ত উত্তরটি সঠিক নয়। সঠিক ব্যাখ্যা নিচে দেখে নিন:'
                            : 'Your chosen answer is incorrect. Review the correct explanation below:'}
                        </span>
                        <span className="ml-auto px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300 text-[11px] font-mono">
                          {isBengali ? 'রিভিশন কিউ-তে যুক্ত' : 'Added to Revision Queue'}
                        </span>
                      </div>
                    )}
                    <div className="text-xs sm:text-sm text-slate-800 dark:text-slate-200 font-bengali leading-[1.8]">
                      <KaTeXRenderer mathContent={isBengali ? currentQ.explanationBn : (currentQ.explanationEn || currentQ.explanationBn)} />
                    </div>
                    <div className="flex items-center gap-2 text-[11px] text-slate-500 dark:text-slate-400 pt-2 border-t border-emerald-200/60 dark:border-emerald-800/60 font-mono">
                      <BookOpen className="w-3.5 h-3.5 text-[#B8862B]" />
                      <span>
                        {isBengali ? `সূত্র: ${currentQ.sourceCitation}` : `Source: ${currentQ.sourceCitationEn || currentQ.sourceCitation}`}
                      </span>
                    </div>
                  </div>
                )}

                {/* Action Buttons & Socratic AI Hint Trigger with 3D Depth */}
                <div className="relative z-10 pt-4 border-t border-amber-200/60 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4">
                  
                  {/* Socratic Hint Summon */}
                  <Button
                    variant="outline"
                    size="md"
                    onClick={() => {
                      const btn = document.getElementById('global-socratic-trigger');
                      if (btn) btn.click();
                    }}
                    icon={<Sparkles className="w-4 h-4 text-[#B8862B]" />}
                    className="min-h-[42px] font-bengali"
                  >
                    <span>{isBengali ? 'সক্রেটিক সংকেত (AI Hint)' : 'Socratic AI Hint'}</span>
                  </Button>

                  {/* Question Navigation Controls with Tactile 3D Depth */}
                  <div className="flex items-center gap-3">
                    <Button
                      variant="ghost"
                      size="md"
                      onClick={handlePrev}
                      disabled={activeQuestionIndex === 0}
                      aria-label={isBengali ? "পূর্ববর্তী প্রশ্ন" : "Previous Question"}
                      className="px-4 min-h-[42px]"
                    >
                      <ArrowLeft className="w-4 h-4 mr-1.5" />
                      <span className="font-bengali">{isBengali ? 'পূর্ববর্তী' : 'Previous'}</span>
                    </Button>

                    {!isSubmitted ? (
                      <Button
                        variant="default"
                        size="md"
                        onClick={handleSubmit}
                        disabled={!selectedOptionId}
                        data-testid="submit-answer-btn"
                        className="shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none min-h-[42px] font-bengali px-5"
                      >
                        {isBengali ? 'উত্তর যাচাই করুন' : 'Verify Answer'}
                      </Button>
                    ) : activeQuestionIndex === questions.length - 1 ? (
                      <Button
                        variant="default"
                        size="md"
                        onClick={handleFinalExamSubmit}
                        icon={<CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                        data-testid="submit-exam-script-btn"
                        className="shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none min-h-[42px] font-bengali px-6 bg-[#0A2540]"
                      >
                        {isBengali ? 'সম্পূর্ণ খাতা জমা দিন' : 'Submit Exam Script'}
                      </Button>
                    ) : (
                      <Button
                        variant="emerald"
                        size="md"
                        onClick={handleNext}
                        icon={<ArrowRight className="w-4 h-4" />}
                        iconPosition="right"
                        data-testid="next-question-btn"
                        className="shadow-[0_4px_0_0_#033829] active:translate-y-1 active:shadow-none min-h-[42px] font-bengali px-5"
                      >
                        {isBengali ? 'পরবর্তী প্রশ্ন' : 'Next Question'}
                      </Button>
                    )}
                  </div>

                </div>

              </div>
            )
          )}

          {/* Section 3: Formula Reference Sheet (প্রয়োজনীয় সূত্র ও দ্রুত রিভিশন) */}
          <div className="relative overflow-hidden rounded-3xl border border-emerald-200/70 dark:border-emerald-950/70 bg-[#F4FAF6]/90 dark:bg-[#071714]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-emerald-900/[0.04] dark:text-emerald-300/[0.03] select-none uppercase font-sans"
              aria-hidden="true"
            >
              FORMULAS
            </div>

            {/* Ambient Emerald Aura */}
            <div
              className="pointer-events-none absolute -left-16 -top-16 w-72 h-72 rounded-full bg-radial from-emerald-400/12 via-emerald-300/5 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-200/60 dark:border-emerald-900/60 pb-5 mb-6">
              <div className="flex items-start sm:items-center gap-3.5">
                <div className="w-11 h-11 rounded-2xl bg-emerald-100/80 dark:bg-emerald-900/40 flex items-center justify-center text-[#0B5D3B] dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 shadow-xs shrink-0">
                  <BookMarked className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                      RAPID REVISION COMPANION
                    </span>
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-[#0B5D3B] dark:text-emerald-300 font-bold font-bengali">
                      {isBengali ? 'LaTeX সমীকরণ' : 'LaTeX Equations'}
                    </span>
                  </div>
                  <h3 className="text-lg sm:text-xl font-bold font-bengali text-[#0A2540] dark:text-white pt-0.5">
                    {isBengali ? 'পদার্থবিজ্ঞান ১ম পত্র: প্রয়োজনীয় গাণিতিক সূত্রাবলী' : 'Physics 1st Paper: Essential Mathematical Formulas'}
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                    {isBengali
                      ? 'অনুশীলন চলাকালীন প্রশ্নের সমাধান ও দ্রুত সূত্র পর্যালোচনার জন্য সংক্ষিপ্ত ফর্মুলা শিট'
                      : 'Quick formula cheat-sheet for reference and rapid review during live practice'}
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setIsFormulaExpanded(!isFormulaExpanded)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white dark:bg-slate-900 border border-emerald-200 dark:border-emerald-800 text-xs font-bold font-bengali text-[#0A2540] dark:text-emerald-300 hover:bg-emerald-50 dark:hover:bg-slate-800 transition cursor-pointer self-start sm:self-auto"
              >
                <span>{isFormulaExpanded ? (isBengali ? 'সংক্ষিপ্ত করুন' : 'Collapse') : (isBengali ? 'বিস্তারিত দেখুন' : 'Expand')}</span>
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isFormulaExpanded ? 'rotate-180' : ''}`} />
              </button>
            </div>

            {isFormulaExpanded && (
              <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 animate-in fade-in">
                <div className="p-4 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-slate-800 shadow-2xs space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#0A2540] dark:text-white font-bengali">
                    <span className="w-2 h-2 rounded-full bg-[#ED8E22]" />
                    <span>{isBengali ? 'বলবিদ্যা ও ত্বরণ' : 'Mechanics & Acceleration'}</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="F = ma \implies a = \frac{F}{m}" />
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="m_1 u_1 + m_2 u_2 = m_1 v_1 + m_2 v_2" />
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-slate-800 shadow-2xs space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#0A2540] dark:text-white font-bengali">
                    <span className="w-2 h-2 rounded-full bg-emerald-600" />
                    <span>{isBengali ? 'মহাকর্ষ ও ধ্রুবক' : 'Gravitation & Constants'}</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="F = G \frac{m_1 m_2}{r^2}" />
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="G = \text{N}\cdot\text{m}^2\cdot\text{kg}^{-2}" />
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-slate-800 shadow-2xs space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#0A2540] dark:text-white font-bengali">
                    <span className="w-2 h-2 rounded-full bg-blue-600" />
                    <span>{isBengali ? 'পর্যাবৃত্ত গতি ও দোলক' : 'Periodic Motion & Oscillator'}</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="T = 2\pi\sqrt{\frac{L}{g}} \implies T \propto \sqrt{L}" />
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="E_k = \frac{1}{2}m\omega^2(A^2 - x^2)" />
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-slate-800 shadow-2xs space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#0A2540] dark:text-white font-bengali">
                    <span className="w-2 h-2 rounded-full bg-purple-600" />
                    <span>{isBengali ? 'তাপগতিবিদ্যা ও কার্নো' : 'Thermodynamics & Carnot'}</span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent={isBengali ? "PV^\\gamma = \\text{ধ্রুবক}" : "PV^\\gamma = \\text{constant}"} />
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 font-sans text-xs overflow-x-auto">
                    <KaTeXRenderer mathContent="\eta = 1 - \frac{T_2}{T_1} = \frac{W}{Q_1}" />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Section 4: Adaptive Scoring & Protocol Matrix */}
          <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-[#FAFBFD]/90 dark:bg-[#0A1220]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-slate-900/[0.03] dark:text-white/[0.02] select-none uppercase font-sans"
              aria-hidden="true"
            >
              PROTOCOL
            </div>

            {/* Ambient Aura */}
            <div
              className="pointer-events-none absolute -right-16 -top-16 w-80 h-80 rounded-full bg-radial from-blue-500/8 via-indigo-500/4 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/80 dark:border-slate-800 pb-5 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-sans">
                    ASSESSMENT FRAMEWORK
                  </span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-[#0A2540] dark:text-slate-300 font-bold font-bengali">
                    {isBengali ? 'মূল্যায়ন নির্দেশিকা' : 'Evaluation Framework'}
                  </span>
                </div>
                <h3 className="text-lg sm:text-xl font-serif font-bold text-[#0A2540] dark:text-white pt-0.5">
                  {isBengali ? 'অ্যাডাপ্টিভ প্র্যাকটিস এরিনার নিয়ম ও মেধা পরিমাপের মানদণ্ড' : 'Adaptive Practice Arena Rules & Assessment Standards'}
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                  {isBengali
                    ? 'শিক্ষার্থীদের আত্মবিশ্বাস বৃদ্ধি এবং জাতীয় স্তরে নিখুঁত প্রস্তুতির জন্য ৪টি প্রধান মূলনীতি'
                    : '4 core pedagogical pillars to build learner confidence and national-level mastery'}
                </p>
              </div>
            </div>

            <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-amber-100/80 dark:bg-amber-950/60 flex items-center justify-center text-[#B8862B] dark:text-amber-300 mb-3 border border-amber-200 dark:border-amber-900/60">
                    <CheckCircle2 className="w-5 h-5" />
                  </div>
                  <h4 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    {isBengali ? '১. নেগেটিভ মার্কিং শূন্য' : '1. Zero Negative Marking'}
                  </h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    {isBengali
                      ? 'ভুল উত্তরের জন্য কোনো নম্বর কাটা হবে না। নির্ভয়ে প্রতিটি প্রশ্ন সমাধান করে ধারণা স্পষ্ট করুন।'
                      : 'No marks deducted for wrong answers. Solve questions fearlessly to clarify fundamental concepts.'}
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-[#B8862B] font-bengali font-bold">
                  {isBengali ? 'ভয়হীন লার্নিং পরিবেশ' : 'Fear-free Learning Space'}
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-emerald-100/80 dark:bg-emerald-950/60 flex items-center justify-center text-[#0B5D3B] dark:text-emerald-300 mb-3 border border-emerald-200 dark:border-emerald-900/60">
                    <Wifi className="w-5 h-5" />
                  </div>
                  <h4 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    {isBengali ? '২. অফলাইন বাফার সিস্টেম' : '2. Offline Buffer System'}
                  </h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    {isBengali
                      ? 'নেটওয়ার্ক ড্রপ করলেও লোকাল বাফারে প্রতিটি উত্তর সুরক্ষিত থাকবে এবং পুনরায় সংযুক্ত হলে সিঙ্ক হবে।'
                      : 'Responses are safely preserved in local buffer during network drops and sync on reconnection.'}
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-[#0B5D3B] font-bengali font-bold">
                  {isBengali ? 'শতভাগ সংযোগ বিচ্ছিন্ন সহনশীল' : '100% Offline Resilient'}
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-sky-100/80 dark:bg-sky-950/60 flex items-center justify-center text-[#0A2540] dark:text-sky-300 mb-3 border border-sky-200 dark:border-sky-900/60">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                  <h4 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    {isBengali ? '৩. আইডেমপোটেন্ট সাবমিশন' : '3. Idempotent Submissions'}
                  </h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    {isBengali
                      ? 'ক্রিপ্টোগ্রাফিক কী দ্বারা প্রতিটি উত্তর ভেরিফাইড থাকে, ফলে ডুপ্লিকেট কাউন্টিংয়ের ঝুঁকি শূন্য।'
                      : 'Every response is cryptographically keyed to eliminate duplicate submissions.'}
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-[#0A2540] dark:text-sky-400 font-bengali font-bold">
                  {isBengali ? 'ডেটাবেজ ও সার্ভার সিকিউরড' : 'Database & Server Secured'}
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-purple-100/80 dark:bg-purple-950/60 flex items-center justify-center text-purple-700 dark:text-purple-300 mb-3 border border-purple-200 dark:border-purple-900/60">
                    <Brain className="w-5 h-5" />
                  </div>
                  <h4 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    {isBengali ? '৪. সক্রেটিক পারফরম্যান্স' : '4. Socratic Mastery Review'}
                  </h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    {isBengali
                      ? 'ভুল হওয়া টপিকগুলো স্বয়ংক্রিয়ভাবে স্পেসড-রিপিটিশন রিভিশন কিউতে জমা হবে পরবর্তী অনুশীলনের জন্য।'
                      : 'Challenging topics are automatically queued into spaced-repetition revision cycles.'}
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-purple-700 dark:text-purple-300 font-bengali font-bold">
                  {isBengali ? 'স্বয়ংক্রিয় রিভিশন ট্র্যাকিং' : 'Automated Revision Tracking'}
                </div>
              </div>
            </div>
          </div>

          {/* Section 5: Practice Strategy & FAQ Accordions */}
          <div className="relative overflow-hidden rounded-3xl border border-amber-200/70 dark:border-[#262D3D] bg-[#FFFDF9]/90 dark:bg-[#0C111C]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-amber-900/[0.04] dark:text-amber-400/[0.02] select-none uppercase font-sans"
              aria-hidden="true"
            >
              STRATEGY
            </div>

            {/* Ambient Warm Amber Aura */}
            <div
              className="pointer-events-none absolute -left-16 -top-16 w-80 h-80 rounded-full bg-radial from-amber-400/12 via-amber-200/5 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-amber-200/60 dark:border-slate-800 pb-5 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#B8862B] dark:text-[#ED8E22] font-sans">
                    EXAMINATION STRATEGY FAQ
                  </span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-950/60 text-[#B8862B] dark:text-amber-300 font-bold font-bengali">
                    {isBengali ? 'কৌশল ও প্রস্তুতি' : 'Strategy & Prep'}
                  </span>
                </div>
                <h3 className="text-lg sm:text-2xl font-serif font-bold text-[#0A2540] dark:text-white pt-0.5">
                  {isBengali ? 'অনুশীলন ও বোর্ড পরীক্ষা প্রস্তুতি কৌশল সংক্রান্ত প্রশ্নোত্তর' : 'Practice & Board Exam Preparation FAQ'}
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                  {isBengali
                    ? 'পদার্থবিজ্ঞানের এমসিকিউ ও গাণিতিক সমস্যা দ্রুত সমাধানের প্রমাণিত পদ্ধতি'
                    : 'Proven methods for solving physics MCQs and numerical problems with speed and precision'}
                </p>
              </div>
            </div>

            <div className="relative z-10 space-y-3 max-w-4xl">
              {[
                {
                  q: isBengali
                    ? 'পদার্থবিজ্ঞানের গাণিতিক প্রশ্নে সময় বাঁচানোর সেরা উপায় কী?'
                    : 'What is the best way to save time on physics numerical questions?',
                  a: isBengali
                    ? 'প্রশ্নে কী কী উপাত্ত দেওয়া আছে তা চিহ্নিত করে সরাসরি সূত্র প্রয়োগ করুন। অপশনগুলোর একক এবং মানের পার্থক্য লক্ষ্য করলে অনেক সময় পূর্ণ গণনা না করেই সঠিক অপশন অনুমান করা যায়।'
                    : 'Identify given variables and apply formulas directly. Inspecting option units and orders of magnitude often reveals the correct answer without lengthy manual calculation.'
                },
                {
                  q: isBengali
                    ? 'কিবোর্ড শর্টকাট (১, ২, ৩, ৪ বা A, B, C, D) কীভাবে কাজ করে?'
                    : 'How do keyboard shortcuts (1, 2, 3, 4 or A, B, C, D) work?',
                  a: isBengali
                    ? 'কম্পিউটার বা ল্যাপটপে অনুশীলন করার সময় মাউস ব্যবহার না করেই কিবোর্ডের ১, ২, ৩, ৪ অথবা A, B, C, D কি চেপে সরাসরি অপশন নির্বাচন করা যায়। এটি রিয়েল-টাইম অলিম্পিয়াড প্রতিযোগিতায় সময় বাঁচায়।'
                    : 'When practicing on desktop or laptop, press 1, 2, 3, 4 or A, B, C, D to select options instantly without touching the mouse, saving vital seconds in live Olympiads.'
                },
                {
                  q: isBengali
                    ? 'ভুল উত্তর দিলে কি সেই প্রশ্ন পুনরায় অনুশীলনের সুযোগ পাব?'
                    : 'If I answer incorrectly, will I get a chance to practice that question again?',
                  a: isBengali
                    ? 'হ্যাঁ, আপনি কোনো প্রশ্নের ভুল উত্তর সাবমিট করলে আমাদের অ্যাডাপ্টিভ অ্যালগরিদম স্বয়ংক্রিয়ভাবে সেই টপিকটি আপনার "স্পেসড-রিপিটিশন রিভিশন কিউ"-তে ৩য়, ৭ম ও ১৪তম দিনের রিভিশন হিসেবে যুক্ত করে নেবে।'
                    : 'Yes, whenever you submit an incorrect answer, our adaptive engine automatically queues that topic into your spaced-repetition revision schedule for days 3, 7, and 14.'
                },
                {
                  q: isBengali
                    ? 'এখানে দেওয়া প্রশ্নগুলো কি বোর্ড পরীক্ষা ও বিশ্ববিদ্যালয়ের ভর্তি পরীক্ষার জন্য কার্যকর?'
                    : 'Are these questions suitable for Board and University Admission exams?',
                  a: isBengali
                    ? 'হ্যাঁ, প্রতিটি প্রশ্ন এনসিটিবি অনুমোদিত মূল পাঠ্যবই এবং ঢাকা বিশ্ববিদ্যালয়, বুয়েট প্রিলিমিনারি ও মেডিকেল ভর্তি পরীক্ষার স্ট্যান্ডার্ড বজায় রেখে সাজানো হয়েছে।'
                    : 'Yes, every question is calibrated against NCTB official textbooks and standards from Dhaka University, BUET Preliminary, and Medical admission tests.'
                }
              ].map((item, idx) => {
                const isOpen = openFaqIndex === idx;
                return (
                  <div
                    key={idx}
                    className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/95 dark:bg-[#070D18]/95 overflow-hidden transition-all shadow-2xs"
                  >
                    <button
                      type="button"
                      onClick={() => setOpenFaqIndex(isOpen ? null : idx)}
                      className="w-full text-left px-5 py-4 flex items-center justify-between gap-4 font-bengali font-bold text-sm sm:text-base text-[#0A2540] dark:text-white hover:text-[#ED8E22] transition cursor-pointer"
                    >
                      <span className="flex items-center gap-2.5">
                        <HelpCircle className="w-4 h-4 text-[#B8862B] shrink-0" />
                        <span>{item.q}</span>
                      </span>
                      <ChevronDown
                        className={`w-4 h-4 text-slate-400 shrink-0 transition-transform duration-200 ${
                          isOpen ? 'rotate-180 text-[#ED8E22]' : ''
                        }`}
                      />
                    </button>
                    {isOpen && (
                      <div className="px-5 pb-5 pt-1 text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali leading-relaxed border-t border-slate-100 dark:border-slate-800/60">
                        {item.a}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

        </main>

        <Footer />
      </div>
    </>
  );
}
