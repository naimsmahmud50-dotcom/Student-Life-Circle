/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic Math & Science Whiteboard Solver
 * TOPIC:     Phase 132 Interactive Canvas & Pedagogical Socratic Step Guidance
 * FILE:      frontend/src/pages/socratic/solver.tsx
 * PHASE:     Phase 132 - Real-time Socratic AI Whiteboard Solver
 * PURPOSE:   Interactive digital laboratory combining an HTML5 tactile canvas,
 *            Pencil/Ruler/Compass/Eraser instruments, KaTeX formula palette,
 *            and progressive Socratic inquiry drawer for guided STEM learning.
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Pedagogical Hint Guard
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import Link from 'next/link';
import {
  Pencil,
  Ruler,
  Compass,
  Eraser,
  RotateCcw,
  HelpCircle,
  CheckCircle2,
  ChevronRight,
  Sparkles,
  BookOpen,
  Calculator,
  Save,
  Download,
  AlertTriangle,
  Layers,
  Trash2,
  ArrowRight,
  ShieldCheck,
  Check
} from 'lucide-react';
import { AppHead } from '../../components/layout/Head';
import { Navbar } from '../../components/layout/Navbar';
import { Footer } from '../../components/layout/Footer';
import { KaTeXRenderer } from '../../components/quiz/katex-renderer';
import { toBengaliDigits } from '../../lib/i18n';

type CanvasTool = 'pencil' | 'ruler' | 'compass' | 'eraser';

interface SocraticStepDef {
  stepIndex: number;
  titleBn: string;
  conceptBn: string;
  inquiryBn: string;
  hints: string[];
  formulaLatex?: string;
  expectedKeywords: string[];
}

interface ProblemScenario {
  id: string;
  titleBn: string;
  discipline: string;
  problemStatementBn: string;
  steps: SocraticStepDef[];
}

const BENCHMARK_PROBLEMS: ProblemScenario[] = [
  {
    id: 'quad_solve',
    titleBn: 'দ্বিঘাত সমীকরণের পূর্ণবর্গীয় সমাধান',
    discipline: 'উচ্চতর গণিত (বীজগণিত)',
    problemStatementBn: '2x^2 + 7x - 4 = 0 সমীকরণটিকে পূর্ণবর্গ পদ্ধতিতে সমাধান করো।',
    steps: [
      {
        stepIndex: 0,
        titleBn: 'ধাপ ১: x^2 এর সহগ অপসারণ ও সমতাকরণ',
        conceptBn: 'পূর্ণবর্গীয় গঠনে প্রথম পদের সহগকে ১ এ রূপান্তর করতে হয়।',
        inquiryBn: 'উভয়পক্ষকে কোন সংখ্যা দিয়ে ভাগ করলে x^2 এর সহগ ১ হবে?',
        hints: [
          'সমীকরণটিতে x^2 এর সাথে সহগ হিসেবে ২ রয়েছে।',
          'সম্পূর্ণ সমীকরণকে ২ দিয়ে ভাগ করে দেখুন ধ্রুবপদ ও x এর সহগ কী দাঁড়ায়।',
          'ভাগ করার পর সমীকরণটি হবে: x^2 + (7/2)x - 2 = 0।'
        ],
        formulaLatex: 'x^2 + \\frac{7}{2}x - 2 = 0',
        expectedKeywords: ['ভাগ', '২', '2', 'divide']
      },
      {
        stepIndex: 1,
        titleBn: 'ধাপ ২: ধ্রুবপদ স্থানান্তর ও মধ্যপদ বিশ্লেষণ',
        conceptBn: 'ধ্রুবপদকে ডানপক্ষে নিয়ে মধ্যপদকে 2 * x * b আকারে সাজানো।',
        inquiryBn: 'মধ্যপদ (7/2)x কে 2 * x * (b) আকারে সাজালে b এর মান কত হবে?',
        hints: [
          '2 * x * b = (7/2)x হলে b = (7/2) / 2 হবে।',
          'সুতরাং b এর মান দাঁড়াবে 7/4।',
          'বামপক্ষকে (x + 7/4)^2 বানাতে উভয়পক্ষে (7/4)^2 যোগ করতে হবে।'
        ],
        formulaLatex: 'x^2 + 2 \\cdot x \\cdot \\frac{7}{4} = 2',
        expectedKeywords: ['7/4', '3.5', 'square']
      },
      {
        stepIndex: 2,
        titleBn: 'ধাপ ৩: উভয়পক্ষে (7/4)^2 যোগ ও বর্গমূল প্রয়োগ',
        conceptBn: '(a + b)^2 গঠন করে বর্গমূল নির্ণয় ও মূলদ্বয় উন্মোচন।',
        inquiryBn: '(7/4)^2 = 49/16 উভয়পক্ষে যোগ করলে ডানপক্ষের মান কত দাঁড়ায়?',
        hints: [
          'ডানপক্ষে 2 + (49/16) যোগ করলে (32 + 49)/16 = 81/16 পাওয়া যায়।',
          'উভয়পক্ষে বর্গমূল প্রয়োগ করলে: (x + 7/4) = ± 9/4।',
          'অতএব x = (9 - 7)/4 = 1/2 অথবা x = (-9 - 7)/4 = -4।'
        ],
        formulaLatex: '\\left(x + \\frac{7}{4}\\right)^2 = \\frac{81}{16}',
        expectedKeywords: ['81/16', '49/16', '9/4', 'মূল']
      }
    ]
  },
  {
    id: 'projectile_motion',
    titleBn: 'প্রাসের গতিপথ ও সর্বোচ্চ উচ্চতা নির্ণয়',
    discipline: 'পদার্থবিজ্ঞান (গতিবিদ্যা)',
    problemStatementBn: 'আদিবেগ v_0 এবং অনুভূমিকের সাথে θ কোণে নিক্ষিপ্ত প্রাসের সর্বোচ্চ উচ্চতা (H) প্রতিপাদন করো।',
    steps: [
      {
        stepIndex: 0,
        titleBn: 'ধাপ ১: আদিবেগের উল্লম্ব উপাংশ নির্ধারণ',
        conceptBn: 'উল্লম্ব অক্ষ বরাবর অভিকর্ষীয় ত্বরণ g ক্রিয়াশীল থাকে।',
        inquiryBn: 'নিক্ষেপণ কোণ θ হলে উল্লম্ব অক্ষের আদিবেগ v_{0y} এর মান কত?',
        hints: [
          'ভেক্টরের উপাংশ সূত্র অনুযায়ী অনুভূমিক অক্ষের বেগ v_0 cos(θ)।',
          'সুতরাং উল্লম্ব অক্ষের আদিবেগ হবে v_{0y} = v_0 sin(θ)।'
        ],
        formulaLatex: 'v_{0y} = v_0 \\sin\\theta',
        expectedKeywords: ['sin', 'sine', 'v0*sin', 'সাইন']
      },
      {
        stepIndex: 1,
        titleBn: 'ধাপ ২: সর্বোচ্চ উচ্চতায় শেষবেগের শর্ত',
        conceptBn: 'সর্বোচ্চ উচ্চতার বিন্দুতে বস্তুর উল্লম্ব গতি সাময়িকভাবে থেমে যায়।',
        inquiryBn: 'সর্বোচ্চ উচ্চতার বিন্দুতে পৌঁছালে উল্লম্ব বেগ v_y এর মান কত হবে?',
        hints: [
          'বস্তু যখন চূড়ায় পৌঁছে, তখন এর ঊর্ধ্বমুখী গতি শেষ হয়ে নিম্নমুখী গতি শুরু হয়।',
          'অতএব চূড়ার বিন্দুতে উল্লম্ব শেষবেগ v_y = 0।'
        ],
        formulaLatex: 'v_y = 0',
        expectedKeywords: ['0', 'zero', 'শূন্য']
      },
      {
        stepIndex: 2,
        titleBn: 'ধাপ ৩: গতির সমীকরণ থেকে H প্রতিপাদন',
        conceptBn: 'v^2 = u^2 - 2gh সমীকরণে প্রাপ্ত মানসমূহ প্রতিস্থাপন।',
        inquiryBn: 'v_y^2 = v_{0y}^2 - 2gH সমীকরণে v_y = 0 বসালে H এর সূত্রটি কী দাঁড়ায়?',
        hints: [
          '0 = (v_0 sin θ)^2 - 2gH।',
          'পক্ষান্তর করলে পাওয়া যায়: 2gH = v_0^2 sin^2(θ)।',
          'অতএব সর্বোচ্চ উচ্চতা H = (v_0^2 sin^2 θ) / (2g)।'
        ],
        formulaLatex: 'H = \\frac{v_0^2 \\sin^2\\theta}{2g}',
        expectedKeywords: ['2g', 'sin^2', 'v0^2']
      }
    ]
  }
];

export default function SocraticWhiteboardSolverPage() {
  const [activeProblem, setActiveProblem] = useState<ProblemScenario>(BENCHMARK_PROBLEMS[0]);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [unlockedHintLevel, setUnlockedHintLevel] = useState<number>(1);
  const [studentDeduction, setStudentDeduction] = useState<string>('');
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [feedbackMessage, setFeedbackMessage] = useState<{ text: string; isError: boolean } | null>(null);

  // Whiteboard drawing tools
  const [activeTool, setActiveTool] = useState<CanvasTool>('pencil');
  const [strokeWidth, setStrokeWidth] = useState<number>(3);
  const [strokeColor, setStrokeColor] = useState<string>('#0A2540');
  const [isDrawing, setIsDrawing] = useState<boolean>(false);
  const [startPoint, setStartPoint] = useState<{ x: number; y: number } | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const snapshotRef = useRef<ImageData | null>(null);

  const currentStep = activeProblem.steps[currentStepIndex];

  // Initialize Canvas
  const setupCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Fill Paper Ivory background
    ctx.fillStyle = '#FAFAF8';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Subtle academic engineering grid pattern
    ctx.strokeStyle = '#E2E8F0';
    ctx.lineWidth = 0.5;
    const gridSize = 40;
    for (let x = 0; x < canvas.width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
  }, []);

  useEffect(() => {
    setupCanvas();
  }, [setupCanvas]);

  // Coordinate normalizer for Canvas
  const getCoordinates = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    if ('touches' in e) {
      const touch = e.touches[0];
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY
      };
    }
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  };

  const startDraw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const coords = getCoordinates(e);
    setIsDrawing(true);
    setStartPoint(coords);

    snapshotRef.current = ctx.getImageData(0, 0, canvas.width, canvas.height);

    if (activeTool === 'pencil' || activeTool === 'eraser') {
      ctx.beginPath();
      ctx.moveTo(coords.x, coords.y);
      ctx.strokeStyle = activeTool === 'eraser' ? '#FAFAF8' : strokeColor;
      ctx.lineWidth = activeTool === 'eraser' ? strokeWidth * 4 : strokeWidth;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
    }
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const coords = getCoordinates(e);

    if (activeTool === 'pencil' || activeTool === 'eraser') {
      ctx.lineTo(coords.x, coords.y);
      ctx.stroke();
    } else if (activeTool === 'ruler' && startPoint && snapshotRef.current) {
      ctx.putImageData(snapshotRef.current, 0, 0);
      ctx.beginPath();
      ctx.moveTo(startPoint.x, startPoint.y);
      ctx.lineTo(coords.x, coords.y);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = strokeWidth;
      ctx.stroke();
    } else if (activeTool === 'compass' && startPoint && snapshotRef.current) {
      ctx.putImageData(snapshotRef.current, 0, 0);
      const radius = Math.sqrt(
        Math.pow(coords.x - startPoint.x, 2) + Math.pow(coords.y - startPoint.y, 2)
      );
      ctx.beginPath();
      ctx.arc(startPoint.x, startPoint.y, radius, 0, 2 * Math.PI);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = strokeWidth;
      ctx.stroke();
    }
  };

  const stopDraw = () => {
    setIsDrawing(false);
    setStartPoint(null);
  };

  const clearCanvas = () => {
    setupCanvas();
  };

  // Socratic Hint Unlocking
  const handleUnlockHint = () => {
    if (unlockedHintLevel < currentStep.hints.length) {
      setUnlockedHintLevel(prev => prev + 1);
    }
  };

  // Misconception checker client side
  const evaluateStudentDeduction = () => {
    if (!studentDeduction.trim()) {
      setFeedbackMessage({
        text: 'অনুগ্রহ করে আপনার গাণিতিক যুক্তি বা উত্তর লিখুন।',
        isError: true
      });
      return;
    }

    const lower = studentDeduction.toLowerCase();

    // Check common misconceptions
    if (lower.includes('(a+b)^2=a^2+b^2') || lower.includes('(a+b)^2 = a^2+b^2')) {
      setFeedbackMessage({
        text: 'বিভ্রান্তি সনাক্ত হয়েছে: (a + b)^2 = a^2 + 2ab + b^2। মধ্যপদ 2ab বাদ দেওয়া যাবে না।',
        isError: true
      });
      return;
    }

    if (lower.includes('sin^2') && lower.includes('-') && lower.includes('cos^2') && lower.includes('=1')) {
      setFeedbackMessage({
        text: 'বিভ্রান্তি সনাক্ত হয়েছে: পিথাগোরাসের ত্রিকোণমিতিক অভেদ হলো sin^2(θ) + cos^2(θ) = 1।',
        isError: true
      });
      return;
    }

    // Keyword match
    const hasKeyword = currentStep.expectedKeywords.some(kw => lower.includes(kw.toLowerCase()));

    if (hasKeyword) {
      if (!completedSteps.includes(currentStepIndex)) {
        setCompletedSteps(prev => [...prev, currentStepIndex]);
      }
      setFeedbackMessage({
        text: `চমৎকার যুক্তি! ${currentStep.titleBn} সফলভাবে সম্পন্ন হয়েছে।`,
        isError: false
      });

      // Advance to next step if available
      if (currentStepIndex < activeProblem.steps.length - 1) {
        setTimeout(() => {
          setCurrentStepIndex(prev => prev + 1);
          setUnlockedHintLevel(1);
          setStudentDeduction('');
          setFeedbackMessage(null);
        }, 1200);
      }
    } else {
      setFeedbackMessage({
        text: 'আপনার যুক্তিটি সঠিক দিকের কাছাকাছি। সংকেতগুলো পুনরায় লক্ষ্য করে ধাপে ধাপে লিখুন।',
        isError: true
      });
    }
  };

  const insertMathSymbol = (sym: string) => {
    setStudentDeduction(prev => prev + sym);
  };

  const handleSelectProblem = (prob: ProblemScenario) => {
    setActiveProblem(prob);
    setCurrentStepIndex(0);
    setUnlockedHintLevel(1);
    setStudentDeduction('');
    setCompletedSteps([]);
    setFeedbackMessage(null);
    clearCanvas();
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-slate-800 flex flex-col font-sans">
      <AppHead
        title="সক্রেটিক হোয়াইটবোর্ড সলভার | Socratic AI Math & Science Whiteboard"
        description="ইন্টারঅ্যাক্টিভ এইচটিএমএল৫ ক্যানভাস ও সক্রেটিক শিক্ষাদানের মাধ্যমে ধাপে ধাপে গণিত ও বিজ্ঞান সমস্যা সমাধান।"
      />
      <Navbar />

      {/* Main Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {/* Header Breadcrumbs & Status */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-6 border-b border-slate-200">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
              <span>একাডেমিক ল্যাবরেটরি</span>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <span>সক্রেটিক গাইডেন্স ইঞ্জিন</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold text-[#0A2540] flex items-center gap-3">
              <Sparkles className="w-6 h-6 text-[#B45309]" />
              সক্রেটিক হোয়াইটবোর্ড সলভার
            </h1>
            <p className="text-sm text-slate-600 mt-1">
              সরাসরি সমাধান মুখস্থ না করে ক্লাসিক্যাল সক্রেটিক সংলাপে ধাপে ধাপে ধারণাগত যুক্তি নির্মাণ করুন।
            </p>
          </div>

          {/* Problem Selector Dropdown */}
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-slate-600">অনুশীলনের বিষয়:</span>
            <div className="flex gap-2">
              {BENCHMARK_PROBLEMS.map(p => (
                <button
                  key={p.id}
                  onClick={() => handleSelectProblem(p)}
                  className={`px-3 py-1.5 text-xs font-semibold rounded border transition-all ${
                    activeProblem.id === p.id
                      ? 'bg-[#0A2540] text-white border-[#0A2540] shadow-sm'
                      : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  {p.discipline.split(' ')[0]}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Problem Banner */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 mb-6 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="inline-block text-xs font-bold text-[#065F46] bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded uppercase tracking-wider mb-2">
                {activeProblem.discipline}
              </span>
              <h2 className="text-lg font-bold text-[#0A2540] mb-1">
                {activeProblem.titleBn}
              </h2>
              <div className="text-base text-slate-800 font-medium">
                <KaTeXRenderer content={activeProblem.problemStatementBn} />
              </div>
            </div>

            {/* Stepper Progress */}
            <div className="flex items-center gap-2 shrink-0">
              {activeProblem.steps.map((st, idx) => (
                <div key={idx} className="flex items-center">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                      completedSteps.includes(idx)
                        ? 'bg-[#065F46] text-white'
                        : idx === currentStepIndex
                        ? 'bg-[#0A2540] text-white ring-2 ring-[#B45309]'
                        : 'bg-slate-200 text-slate-600'
                    }`}
                  >
                    {completedSteps.includes(idx) ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      toBengaliDigits(idx + 1)
                    )}
                  </div>
                  {idx < activeProblem.steps.length - 1 && (
                    <div
                      className={`w-6 h-0.5 ${
                        completedSteps.includes(idx) ? 'bg-[#065F46]' : 'bg-slate-200'
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Workspace Grid: Left Canvas, Right Socratic Drawer */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Canvas: 7 Columns */}
          <div className="lg:col-span-7 flex flex-col gap-3">
            {/* Whiteboard Toolbar */}
            <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-wrap items-center justify-between gap-3 shadow-sm">
              {/* Tool Selection */}
              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={() => setActiveTool('pencil')}
                  className={`p-2 rounded border transition-all ${
                    activeTool === 'pencil'
                      ? 'bg-[#0A2540] text-white border-[#0A2540]'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                  }`}
                  title="ফ্রিহ্যান্ড পেন্সিল"
                >
                  <Pencil className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTool('ruler')}
                  className={`p-2 rounded border transition-all ${
                    activeTool === 'ruler'
                      ? 'bg-[#0A2540] text-white border-[#0A2540]'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                  }`}
                  title="সোজা রেখা ও রুলার"
                >
                  <Ruler className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTool('compass')}
                  className={`p-2 rounded border transition-all ${
                    activeTool === 'compass'
                      ? 'bg-[#0A2540] text-white border-[#0A2540]'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                  }`}
                  title="কম্পাস ও বৃত্ত"
                >
                  <Compass className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTool('eraser')}
                  className={`p-2 rounded border transition-all ${
                    activeTool === 'eraser'
                      ? 'bg-[#0A2540] text-white border-[#0A2540]'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                  }`}
                  title="ইরেজার"
                >
                  <Eraser className="w-4 h-4" />
                </button>
              </div>

              {/* Stroke Width and Color Palette */}
              <div className="flex items-center gap-2 border-l border-slate-200 pl-3">
                <span className="text-xs text-slate-500 font-medium">রং:</span>
                <div className="flex items-center gap-1.5">
                  {['#0A2540', '#B45309', '#065F46', '#991B1B'].map(c => (
                    <button
                      key={c}
                      type="button"
                      onClick={() => setStrokeColor(c)}
                      className={`w-5 h-5 rounded-full border-2 transition-transform ${
                        strokeColor === c ? 'scale-125 border-slate-900 shadow-sm' : 'border-white'
                      }`}
                      style={{ backgroundColor: c }}
                    />
                  ))}
                </div>

                <span className="text-xs text-slate-500 font-medium ml-2">বেধ:</span>
                <select
                  value={strokeWidth}
                  onChange={e => setStrokeWidth(Number(e.target.value))}
                  className="text-xs border border-slate-200 rounded px-1.5 py-1 bg-slate-50 text-slate-800"
                >
                  <option value={2}>পাতলা (২px)</option>
                  <option value={4}>মাঝারি (৪px)</option>
                  <option value={8}>পুরু (৮px)</option>
                </select>
              </div>

              {/* Canvas Clear & Reset */}
              <div className="flex items-center gap-1.5">
                <button
                  type="button"
                  onClick={clearCanvas}
                  className="p-2 text-slate-600 hover:text-red-700 hover:bg-red-50 rounded border border-slate-200 transition-colors"
                  title="ক্যানভাস পরিষ্কার করুন"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Interactive Canvas Surface */}
            <div className="relative bg-[#FAFAF8] rounded-lg border-2 border-slate-300 overflow-hidden shadow-inner flex items-center justify-center">
              <canvas
                ref={canvasRef}
                width={800}
                height={550}
                onMouseDown={startDraw}
                onMouseMove={draw}
                onMouseUp={stopDraw}
                onMouseLeave={stopDraw}
                onTouchStart={startDraw}
                onTouchMove={draw}
                onTouchEnd={stopDraw}
                className="w-full h-[520px] cursor-crosshair touch-none"
              />
              <div className="absolute bottom-2 right-3 pointer-events-none text-[10px] text-slate-400 font-mono tracking-tight">
                অক্সফোর্ড পেপার ক্যানভাস | Virtual DPI 2.0 | ASVS L2 Buffer
              </div>
            </div>
          </div>

          {/* Right Socratic Inquiry Drawer: 5 Columns */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            {/* Active Socratic Step Card */}
            <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-[#B45309] bg-amber-50 border border-amber-200 px-2.5 py-0.5 rounded">
                  সক্রেটিক অনুসন্ধান {toBengaliDigits(currentStepIndex + 1)} / {toBengaliDigits(activeProblem.steps.length)}
                </span>
                {completedSteps.includes(currentStepIndex) && (
                  <span className="flex items-center gap-1 text-xs font-semibold text-[#065F46] bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    সম্পন্ন
                  </span>
                )}
              </div>

              <h3 className="text-base font-bold text-[#0A2540] mb-1">
                {currentStep.titleBn}
              </h3>
              <p className="text-xs text-slate-600 mb-3">
                {currentStep.conceptBn}
              </p>

              {/* Inquiry Question Box */}
              <div className="bg-[#FAFAF8] border border-amber-200 rounded-lg p-3.5 mb-4">
                <div className="flex items-start gap-2.5">
                  <HelpCircle className="w-4 h-4 text-[#B45309] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 mb-1">
                      মূল প্রশ্ন:
                    </h4>
                    <p className="text-sm text-slate-800 font-medium">
                      {currentStep.inquiryBn}
                    </p>
                  </div>
                </div>
              </div>

              {/* Pedagogical Hints Accordion */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-[#0A2540]" />
                    শিক্ষণ সংকেত (Hints):
                  </span>
                  {unlockedHintLevel < currentStep.hints.length && (
                    <button
                      type="button"
                      onClick={handleUnlockHint}
                      className="text-xs font-semibold text-[#B45309] hover:underline flex items-center gap-1"
                    >
                      পরবর্তী সংকেত খুলুন (+১)
                    </button>
                  )}
                </div>

                <div className="space-y-2">
                  {currentStep.hints.slice(0, unlockedHintLevel).map((hint, hIdx) => (
                    <div
                      key={hIdx}
                      className="bg-slate-50 border border-slate-200 rounded p-2.5 text-xs text-slate-700"
                    >
                      <span className="font-bold text-[#0A2540] mr-1">
                        সংকেত {toBengaliDigits(hIdx + 1)}:
                      </span>
                      {hint}
                    </div>
                  ))}
                </div>
              </div>

              {/* Formula Blueprint if applicable */}
              {currentStep.formulaLatex && (
                <div className="bg-slate-50 border border-slate-200 rounded p-3 mb-4 text-center">
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1">
                    লক্ষ্য সমীকরণ রূপ
                  </span>
                  <KaTeXRenderer mathContent={currentStep.formulaLatex} block />
                </div>
              )}

              {/* Student Deduction Input & KaTeX Symbols Palette */}
              <div className="mb-4">
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  আপনার গাণিতিক যুক্তি / উত্তর প্রতিপাদন করুন:
                </label>

                {/* KaTeX Symbol Buttons */}
                <div className="flex flex-wrap gap-1 mb-2 bg-slate-50 p-1.5 rounded border border-slate-200">
                  {['x^2', '\\sqrt{}', '\\frac{a}{b}', '\\sin\\theta', '\\cos\\theta', '\\int', '\\pi', '\\pm', '\\Delta'].map(s => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => insertMathSymbol(s)}
                      className="px-2 py-0.5 text-xs font-mono bg-white border border-slate-300 rounded hover:bg-slate-100 text-slate-700"
                    >
                      {s}
                    </button>
                  ))}
                </div>

                <textarea
                  value={studentDeduction}
                  onChange={e => setStudentDeduction(e.target.value)}
                  placeholder="উভয়পক্ষকে ২ দিয়ে ভাগ করে x^2 এর সহগ ১ এ রূপান্তর করতে হবে..."
                  rows={3}
                  className="w-full text-xs border border-slate-300 rounded p-2.5 bg-[#FAFAF8] focus:outline-none focus:ring-1 focus:ring-[#0A2540] text-slate-800"
                />
              </div>

              {/* Feedback Alert if present */}
              {feedbackMessage && (
                <div
                  className={`p-3 rounded text-xs mb-4 flex items-start gap-2 border ${
                    feedbackMessage.isError
                      ? 'bg-amber-50 text-amber-900 border-amber-200'
                      : 'bg-emerald-50 text-emerald-900 border-emerald-200'
                  }`}
                >
                  {feedbackMessage.isError ? (
                    <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
                  ) : (
                    <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                  )}
                  <span>{feedbackMessage.text}</span>
                </div>
              )}

              {/* 3D Physical Tactile Submit Button */}
              <button
                type="button"
                onClick={evaluateStudentDeduction}
                className="w-full py-2.5 px-4 bg-[#0A2540] text-white text-xs font-bold rounded uppercase tracking-wider shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none transition-all flex items-center justify-center gap-2"
              >
                <span>ধাপের যুক্তি যাচাই করুন</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Socratic Academic Principles Footer Card */}
            <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-sm text-xs text-slate-600">
              <div className="flex items-center gap-2 font-bold text-[#0A2540] mb-1">
                <ShieldCheck className="w-4 h-4 text-[#065F46]" />
                সক্রেটিক পেডাগজি নীতি (ASVS L2)
              </div>
              <p className="text-[11px] leading-relaxed">
                প্লাটফর্মটি সরাসরি সমাধান প্রদান না করে শিক্ষার্থীকে প্রশ্নবাণের মাধ্যমে নিজস্ব বিশ্লেষণ ও অনুমানের ভুল সংশোধনে সহায়তা করে।
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
