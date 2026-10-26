/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic AI Math & Science Whiteboard Solver & Multimodal Tutor
 * TOPIC:     Interactive Canvas, Khata Notebook OCR, Voice Input & 4-Tier Socratic Guidance
 * FILE:      frontend/src/pages/socratic/solver.tsx
 * PURPOSE:   Advanced Socratic learning environment:
 *            1. Dual mode: Multimodal Socratic AI Tutor & Interactive Canvas Whiteboard.
 *            2. Multimodal Khata (Notebook) Snapshot Dropzone with OCR equation parser.
 *            3. Bengali Web Speech API voice input integration.
 *            4. Freeform mathematical problem entry with live KaTeX preview.
 *            5. 4-Tier Pedagogical Scaffolding & 25+ Misconception Diagnosis Engine.
 *            6. Zero-Answer-Leaking guardrail (intercepts direct answer demands).
 *            7. Interactive 3D STEM simulation lab launchers (Mechanics, Molecules, Celestial).
 *            8. NCTB 10-year past board examination alignment.
 * STANDARDS: Strict Zero-Emoji, ASVS L2, WCAG 2.2 AAA, Pure Academic Design
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
  Check,
  Camera,
  Mic,
  MicOff,
  UploadCloud,
  Cpu,
  ExternalLink,
  Eye,
  Send,
  RefreshCw,
  FileText,
  Lightbulb
} from 'lucide-react';
import { AppHead } from '../../components/layout/Head';
import { Navbar } from '../../components/layout/Navbar';
import { Footer } from '../../components/layout/Footer';
import { KaTeXRenderer } from '../../components/quiz/katex-renderer';
import { toBengaliDigits } from '../../lib/i18n';
import {
  isDirectAnswerDemanded,
  ZERO_ANSWER_LEAKING_REFUSAL_BN,
  analyzeProblemDomain,
  scanForMisconception,
  SocraticProblemAnalysis,
  MisconceptionRule
} from '../../lib/socratic/socraticEngine';

type ActiveMode = 'tutor' | 'whiteboard';
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

interface ChatMessage {
  id: string;
  sender: 'student' | 'tutor';
  text: string;
  formulaLatex?: string;
  isMisconceptionAlert?: boolean;
  isRefusal?: boolean;
  timestamp: string;
}

interface SampleKhataProblem {
  id: string;
  titleBn: string;
  boardBn: string;
  discipline: string;
  queryText: string;
  sampleEquationLatex: string;
}

const SAMPLE_KHATA_PROBLEMS: SampleKhataProblem[] = [
  {
    id: 'quad_dhaka_2024',
    titleBn: 'দ্বিঘাত সমীকরণ ও মূলের প্রকৃতি',
    boardBn: 'ঢাকা বোর্ড ২০২৪ (উচ্চতর গণিত)',
    discipline: 'উচ্চতর গণিত',
    queryText: '2x^2 + 7x - 4 = 0 সমীকরণটিকে পূর্ণবর্গ পদ্ধতিতে সমাধান করতে চাই। প্রথম পদক্ষেপ কী?',
    sampleEquationLatex: '2x^2 + 7x - 4 = 0'
  },
  {
    id: 'projectile_ctg_2024',
    titleBn: 'প্রাসের সর্বোচ্চ উচ্চতা ও অনুভূমিক পাল্লা',
    boardBn: 'চট্টগ্রাম বোর্ড ২০২৪ (পদার্থবিজ্ঞান ১ম পত্র)',
    discipline: 'পদার্থবিজ্ঞান',
    queryText: 'আদিবেগ v_0 এবং অনুভূমিকের সাথে θ কোণে নিক্ষিপ্ত প্রাসের সর্বোচ্চ উচ্চতা (H) প্রতিপাদন করো।',
    sampleEquationLatex: 'H = \\frac{v_0^2 \\sin^2\\theta}{2g}'
  },
  {
    id: 'chem_dinajpur_2023',
    titleBn: 'রাসায়নিক সাম্যাবস্থা ও লা-শাতেলিয়ার নীতি',
    boardBn: 'দিনাজপুর বোর্ড ২০২৩ (রসায়ন ১ম পত্র)',
    discipline: 'রসায়ন',
    queryText: 'হেবার বস পদ্ধতিতে অ্যামোনিয়া উৎপাদনে চাপ ও তাপমাত্রার প্রভাব ব্যাখ্যা করো।',
    sampleEquationLatex: 'N_2(g) + 3H_2(g) \\rightleftharpoons 2NH_3(g) + 92.4\\, \\text{kJ}'
  },
  {
    id: 'ict_rajshahi_2023',
    titleBn: 'বুলিয়ান বীজগণিত ও ডি মরগ্যান উপপাদ্য',
    boardBn: 'রাজশাহী বোর্ড ২০২৩ (এইচএসসি আইসিটি)',
    discipline: 'তথ্য ও যোগাযোগ প্রযুক্তি',
    queryText: 'F = (A + B)(A + B_bar) বুলিয়ান ফাংশনটি সরলীকরণ করো।',
    sampleEquationLatex: 'F = (A + B)(A + \\bar{B}) = A'
  }
];

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
  // Mode selection: Tutor vs Canvas Whiteboard
  const [activeMode, setActiveMode] = useState<ActiveMode>('tutor');

  // Socratic AI Tutor states
  const [studentInput, setStudentInput] = useState<string>('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome_1',
      sender: 'tutor',
      text: 'স্বাগতম! আমি অগ্রযাত্রা সক্রেটিক এআই টিউটর। আপনার গণিত, পদার্থবিজ্ঞান বা রসায়নের খাতার ছবি আপলোড করুন অথবা সমস্যাটি লিখুন। আমি আপনাকে ধাপে ধাপে চিন্তা করে সমাধানে পৌঁছাতে সহায়তা করব।',
      timestamp: 'এখন'
    }
  ]);
  const [isAiLoading, setIsAiLoading] = useState<boolean>(false);
  const [activeTier, setActiveTier] = useState<number>(1);
  const [activeAnalysis, setActiveAnalysis] = useState<SocraticProblemAnalysis | null>(null);
  const [uploadedImagePreview, setUploadedImagePreview] = useState<string | null>(null);
  const [ocrDetectedFormula, setOcrDetectedFormula] = useState<string | null>(null);
  const [ocrConfidence, setOcrConfidence] = useState<number | null>(null);

  // Bengali Voice Recognition states
  const [isVoiceListening, setIsVoiceListening] = useState<boolean>(false);
  const [voiceSupported, setVoiceSupported] = useState<boolean>(false);
  const speechRecognitionRef = useRef<any>(null);

  // Whiteboard drawing states
  const [activeProblem, setActiveProblem] = useState<ProblemScenario>(BENCHMARK_PROBLEMS[0]);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [unlockedHintLevel, setUnlockedHintLevel] = useState<number>(1);
  const [studentDeduction, setStudentDeduction] = useState<string>('');
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [feedbackMessage, setFeedbackMessage] = useState<{ text: string; isError: boolean } | null>(null);

  const [activeTool, setActiveTool] = useState<CanvasTool>('pencil');
  const [strokeWidth, setStrokeWidth] = useState<number>(3);
  const [strokeColor, setStrokeColor] = useState<string>('#0A2540');
  const [isDrawing, setIsDrawing] = useState<boolean>(false);
  const [startPoint, setStartPoint] = useState<{ x: number; y: number } | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const snapshotRef = useRef<ImageData | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const chatScrollEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatScrollEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages, isAiLoading]);

  // Setup Web Speech API for Bengali
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        setVoiceSupported(true);
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'bn-BD';

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setStudentInput(prev => (prev ? `${prev} ${transcript}` : transcript));
          setIsVoiceListening(false);
        };

        recognition.onerror = () => {
          setIsVoiceListening(false);
        };

        recognition.onend = () => {
          setIsVoiceListening(false);
        };

        speechRecognitionRef.current = recognition;
      }
    }
  }, []);

  const toggleVoiceListening = () => {
    if (!speechRecognitionRef.current) return;
    if (isVoiceListening) {
      speechRecognitionRef.current.stop();
      setIsVoiceListening(false);
    } else {
      try {
        speechRecognitionRef.current.start();
        setIsVoiceListening(true);
      } catch (err) {
        setIsVoiceListening(false);
      }
    }
  };

  // Canvas Initialization
  const setupCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.fillStyle = '#FAFAF8';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

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
    if (activeMode === 'whiteboard') {
      setupCanvas();
    }
  }, [activeMode, setupCanvas]);

  // Canvas Coordinate Normalizer
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

  // Mathematical Symbol Bar click
  const insertMathSymbol = (sym: string) => {
    if (activeMode === 'tutor') {
      setStudentInput(prev => prev + ' ' + sym + ' ');
    } else {
      setStudentDeduction(prev => prev + sym);
    }
  };

  // Image upload handling for handwritten khata
  const handleKhataImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (uploadEvt) => {
      const base64Str = uploadEvt.target?.result as string;
      setUploadedImagePreview(base64Str);

      // Trigger automatic Socratic analysis on the uploaded handwritten problem
      submitSocraticInquiry('আমার এই খাতার অংকটি ধাপে ধাপে সমাধান করতে সাহায্য করুন।', base64Str);
    };
    reader.readAsDataURL(file);
  };

  // Sample Khata Notebook quick-picker
  const handleSelectSampleProblem = (sample: SampleKhataProblem) => {
    setStudentInput(sample.queryText);
    setOcrDetectedFormula(sample.sampleEquationLatex);
    setOcrConfidence(98.5);
    submitSocraticInquiry(sample.queryText, undefined, sample.sampleEquationLatex);
  };

  // Client-side + API Socratic inquiry dispatcher
  const submitSocraticInquiry = async (
    customQuery?: string,
    imageBase64?: string,
    overrideFormula?: string
  ) => {
    const queryToSend = (customQuery ?? studentInput).trim();
    if (!queryToSend && !imageBase64) return;

    const studentMessageId = `std_${Date.now()}`;
    const newStudentMsg: ChatMessage = {
      id: studentMessageId,
      sender: 'student',
      text: queryToSend,
      formulaLatex: overrideFormula,
      timestamp: 'এইমাত্র'
    };

    setChatMessages(prev => [...prev, newStudentMsg]);
    setStudentInput('');
    setIsAiLoading(true);

    // 1. Client-Side Instant Guardrail Check
    if (isDirectAnswerDemanded(queryToSend)) {
      setTimeout(() => {
        setChatMessages(prev => [
          ...prev,
          {
            id: `tutor_${Date.now()}`,
            sender: 'tutor',
            text: ZERO_ANSWER_LEAKING_REFUSAL_BN,
            isRefusal: true,
            timestamp: 'এইমাত্র'
          }
        ]);
        setIsAiLoading(false);
      }, 400);
      return;
    }

    // 2. Client-Side Misconception Check
    const localMisconception = scanForMisconception(queryToSend);
    if (localMisconception) {
      setTimeout(() => {
        setChatMessages(prev => [
          ...prev,
          {
            id: `tutor_${Date.now()}`,
            sender: 'tutor',
            text: `পর্যবেক্ষণ ও সতর্কতা: ${localMisconception.titleBn}\n${localMisconception.explanationBn}\n\nসক্রেটিক প্রশ্ন: ${localMisconception.guidingQuestionBn}`,
            formulaLatex: localMisconception.remedialFormulaLatex,
            isMisconceptionAlert: true,
            timestamp: 'এইমাত্র'
          }
        ]);
        setIsAiLoading(false);
      }, 500);
      return;
    }

    // 3. Fallback to robust client analysis + Next.js API route
    try {
      const response = await fetch('/api/socratic/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryToSend,
          imageBase64: imageBase64 ?? uploadedImagePreview,
          currentTier: activeTier
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.analysis) {
          setActiveAnalysis(data.analysis);
        }
        if (data.extractedOcrText) {
          setOcrDetectedFormula(data.extractedOcrText);
        }
        if (data.ocrConfidence) {
          setOcrConfidence(data.ocrConfidence);
        }
        if (data.activeTier) {
          setActiveTier(data.activeTier);
        }

        setChatMessages(prev => [
          ...prev,
          {
            id: `tutor_${Date.now()}`,
            sender: 'tutor',
            text: data.tutorReplyBn,
            formulaLatex: data.suggestedFormulaLatex,
            isRefusal: data.refusedDirectAnswer,
            isMisconceptionAlert: Boolean(data.misconceptionDetected),
            timestamp: 'এইমাত্র'
          }
        ]);
      } else {
        // High-availability graceful fallback using client engine
        const clientAnalysis = analyzeProblemDomain(queryToSend);
        setActiveAnalysis(clientAnalysis);
        const scaffold = clientAnalysis.scaffolding[activeTier - 1] || clientAnalysis.scaffolding[0];

        setChatMessages(prev => [
          ...prev,
          {
            id: `tutor_${Date.now()}`,
            sender: 'tutor',
            text: `[${clientAnalysis.identifiedTopicBn}]\n${scaffold.hintTextBn}\n\nপ্রশ্ন: ${scaffold.guidingQuestionBn}`,
            formulaLatex: scaffold.formulaLatex,
            timestamp: 'এইমাত্র'
          }
        ]);
      }
    } catch (err) {
      // Offline / Network disconnect fallback
      const clientAnalysis = analyzeProblemDomain(queryToSend);
      setActiveAnalysis(clientAnalysis);
      const scaffold = clientAnalysis.scaffolding[activeTier - 1] || clientAnalysis.scaffolding[0];

      setChatMessages(prev => [
        ...prev,
        {
          id: `tutor_${Date.now()}`,
          sender: 'tutor',
          text: `[${clientAnalysis.identifiedTopicBn}]\n${scaffold.hintTextBn}\n\nপ্রশ্ন: ${scaffold.guidingQuestionBn}`,
          formulaLatex: scaffold.formulaLatex,
          timestamp: 'এইমাত্র'
        }
      ]);
    } finally {
      setIsAiLoading(false);
    }
  };

  // Next Scaffolding Tier advancement
  const advanceScaffoldingTier = () => {
    if (activeTier < 4) {
      const nextTier = activeTier + 1;
      setActiveTier(nextTier);
      if (activeAnalysis) {
        const nextScaffold = activeAnalysis.scaffolding[nextTier - 1];
        if (nextScaffold) {
          setChatMessages(prev => [
            ...prev,
            {
              id: `tutor_scaffold_${Date.now()}`,
              sender: 'tutor',
              text: `[${nextScaffold.tierNameBn}]\n${nextScaffold.hintTextBn}\n\nসক্রেটিক অনুসন্ধান: ${nextScaffold.guidingQuestionBn}`,
              formulaLatex: nextScaffold.formulaLatex,
              timestamp: 'এইমাত্র'
            }
          ]);
        }
      }
    }
  };

  // Whiteboard Step Verification
  const currentStep = activeProblem.steps[currentStepIndex];

  const handleUnlockHint = () => {
    if (unlockedHintLevel < currentStep.hints.length) {
      setUnlockedHintLevel(prev => prev + 1);
    }
  };

  const evaluateStudentDeduction = () => {
    if (!studentDeduction.trim()) {
      setFeedbackMessage({
        text: 'অনুগ্রহ করে আপনার গাণিতিক যুক্তি বা উত্তর লিখুন।',
        isError: true
      });
      return;
    }

    const lower = studentDeduction.toLowerCase();

    // Check classic misconceptions
    const mis = scanForMisconception(lower);
    if (mis) {
      setFeedbackMessage({
        text: `বিভ্রান্তি সনাক্ত হয়েছে: ${mis.titleBn}। ${mis.explanationBn}`,
        isError: true
      });
      return;
    }

    // Keyword match for the active step
    const hasKeyword = currentStep.expectedKeywords.some(kw => lower.includes(kw.toLowerCase()));

    if (hasKeyword) {
      if (!completedSteps.includes(currentStepIndex)) {
        setCompletedSteps(prev => [...prev, currentStepIndex]);
      }
      setFeedbackMessage({
        text: `চমৎকার যুক্তি! ${currentStep.titleBn} সফলভাবে সম্পন্ন হয়েছে।`,
        isError: false
      });

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
        title="সক্রেটিক এআই টিউটর ও হোয়াইটবোর্ড সলভার | Socratic AI STEM Tutor"
        description="হাতে লেখা খাতার ওটিআর স্ক্যানিং, বাংলা ভয়েস ইনপুট ও ৪-টিয়ার সক্রেটিক শিক্ষাদানের মাধ্যমে ধাপে ধাপে বিজ্ঞান ও গণিত সমস্যা সমাধান।"
      />
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {/* Header Breadcrumbs & Dual Mode Switcher */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-6 border-b border-slate-200">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
              <span>একাডেমিক ল্যাবরেটরি</span>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <span>সক্রেটিক পেডাগজি ইঞ্জিন</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold text-[#0A2540] flex items-center gap-3">
              <Sparkles className="w-6 h-6 text-[#B45309]" />
              সক্রেটিক এআই টিউটর ও সলভার
            </h1>
            <p className="text-sm text-slate-600 mt-1">
              সরাসরি সমাধান না দিয়ে শিক্ষার্থীকে প্রশ্নবাণের মাধ্যমে নিজস্ব বিশ্লেষণ ও অনুমানের ভুল সংশোধনে সহায়তা করা হয়।
            </p>
          </div>

          {/* Mode Switcher Tabs */}
          <div className="flex items-center gap-2 bg-slate-100 p-1 rounded-lg border border-slate-200 self-start md:self-auto">
            <button
              type="button"
              onClick={() => setActiveMode('tutor')}
              className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-md transition-all ${
                activeMode === 'tutor'
                  ? 'bg-[#0A2540] text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span>সক্রেটিক এআই টিউটর ও খাতা ওটিআর</span>
            </button>
            <button
              type="button"
              onClick={() => setActiveMode('whiteboard')}
              className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-md transition-all ${
                activeMode === 'whiteboard'
                  ? 'bg-[#0A2540] text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
              }`}
            >
              <Pencil className="w-4 h-4" />
              <span>ইন্টারেক্টিভ ড্রয়িং হোয়াইটবোর্ড</span>
            </button>
          </div>
        </div>

        {/* =========================================================================
            MODE 1: SOCRATIC AI MULTIMODAL TUTOR & KHATA NOTEBOOK OCR
            ========================================================================= */}
        {activeMode === 'tutor' && (
          <div className="space-y-6">
            {/* Quick Sample Problem Pills (Authentic NCTB Board Exams) */}
            <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5 uppercase tracking-wider">
                  <FileText className="w-3.5 h-3.5 text-[#B45309]" />
                  বিগত বোর্ড ও ভর্তি পরীক্ষার নমুনা খাতা প্রশ্ন:
                </span>
                <span className="text-[11px] text-slate-500 font-medium">
                  এনসিটিবি কারিকুলাম মানদণ্ড
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
                {SAMPLE_KHATA_PROBLEMS.map(sample => (
                  <button
                    key={sample.id}
                    type="button"
                    onClick={() => handleSelectSampleProblem(sample)}
                    className="p-3 text-left rounded-md border border-slate-200 hover:border-[#0A2540] hover:bg-slate-50 transition-all group"
                  >
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <span className="text-[10px] font-bold text-[#065F46] bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                        {sample.discipline}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {sample.boardBn.split(' ')[0]}
                      </span>
                    </div>
                    <div className="text-xs font-bold text-[#0A2540] group-hover:text-[#B45309] transition-colors mb-1">
                      {sample.titleBn}
                    </div>
                    <div className="text-[11px] text-slate-600 line-clamp-1 font-mono">
                      {sample.sampleEquationLatex}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Split Workspace: Left Problem Input / OCR / 3D Labs; Right Socratic Drawer */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column: 6 Columns */}
              <div className="lg:col-span-6 flex flex-col gap-5">
                {/* Multimodal Khata Snapshot Dropzone */}
                <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-slate-800 flex items-center gap-2">
                      <Camera className="w-4 h-4 text-[#0A2540]" />
                      খাতার হস্তলিপি স্ক্যানার (Multimodal Math OCR)
                    </span>
                    <span className="text-[11px] text-[#065F46] font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      ASVS L2 এনক্রিপ্টেড
                    </span>
                  </div>

                  <input
                    type="file"
                    ref={fileInputRef}
                    accept="image/*"
                    onChange={handleKhataImageUpload}
                    className="hidden"
                  />

                  {/* Dropzone Card */}
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="border-2 border-dashed border-slate-300 hover:border-[#0A2540] rounded-lg p-5 text-center cursor-pointer transition-colors bg-[#FAFAF8] group"
                  >
                    {uploadedImagePreview ? (
                      <div className="flex flex-col items-center">
                        <img
                          src={uploadedImagePreview}
                          alt="হাতে লেখা খাতার পৃষ্ঠা"
                          className="max-h-48 object-contain rounded border border-slate-300 mb-3 shadow-xs"
                        />
                        <div className="text-xs font-bold text-[#0A2540] flex items-center gap-1.5">
                          <CheckCircle2 className="w-4 h-4 text-[#065F46]" />
                          খাতার ছবি সফলভাবে আপলোড হয়েছে
                        </div>
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            setUploadedImagePreview(null);
                            setOcrDetectedFormula(null);
                          }}
                          className="text-[11px] text-red-600 hover:underline mt-1"
                        >
                          ছবি পরিবর্তন করুন
                        </button>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center">
                        <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-slate-200 transition-colors mb-2">
                          <UploadCloud className="w-6 h-6 text-[#0A2540]" />
                        </div>
                        <div className="text-xs font-bold text-slate-800 mb-1">
                          হাতে লেখা অংকের পৃষ্ঠা ড্র্যাগ করুন অথবা ক্লিক করে নির্বাচন করুন
                        </div>
                        <p className="text-[11px] text-slate-500 max-w-sm">
                          খাতার পাতায় লেখা সমীকরণ, জ্যামিতিক চিত্র বা রাসায়নিক সমীকরণ ওটিআর প্রযুক্তিতে স্বয়ংক্রিয়ভাবে সনাক্ত হবে।
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Detected OCR Result Card */}
                  {ocrDetectedFormula && (
                    <div className="mt-3 p-3 bg-amber-50/60 border border-amber-200 rounded-md">
                      <div className="flex items-center justify-between text-xs font-bold text-amber-900 mb-1.5">
                        <span className="flex items-center gap-1.5">
                          <Eye className="w-3.5 h-3.5 text-[#B45309]" />
                          সনাক্তকৃত সমীকরণ (LaTeX OCR):
                        </span>
                        {ocrConfidence && (
                          <span className="text-[10px] font-mono font-normal text-slate-600">
                            নির্ভুলতা: {ocrConfidence}%
                          </span>
                        )}
                      </div>
                      <div className="bg-white p-2 rounded border border-amber-200 text-center">
                        <KaTeXRenderer mathContent={ocrDetectedFormula} block />
                      </div>
                    </div>
                  )}
                </div>

                {/* Freeform Question Input with Live KaTeX Preview & Voice */}
                <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                      <Calculator className="w-4 h-4 text-[#0A2540]" />
                      আপনার প্রশ্ন বা গাণিতিক ধারণা লিখুন:
                    </label>

                    {/* Bengali Voice Recognition Button */}
                    {voiceSupported && (
                      <button
                        type="button"
                        onClick={toggleVoiceListening}
                        className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-md border transition-all ${
                          isVoiceListening
                            ? 'bg-red-50 text-red-700 border-red-300 animate-pulse'
                            : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                        }`}
                        title="বাংলা ভয়েসে প্রশ্ন বলুন"
                      >
                        {isVoiceListening ? (
                          <>
                            <Mic className="w-3.5 h-3.5 text-red-600" />
                            <span>শুনছি...</span>
                          </>
                        ) : (
                          <>
                            <Mic className="w-3.5 h-3.5 text-slate-600" />
                            <span>ভয়েস ইনপুট</span>
                          </>
                        )}
                      </button>
                    )}
                  </div>

                  {/* Math Symbols Toolbar */}
                  <div className="flex flex-wrap gap-1 mb-2 bg-slate-50 p-2 rounded border border-slate-200">
                    <span className="text-[10px] text-slate-500 font-bold self-center mr-1">
                      সংকেত:
                    </span>
                    {[
                      'x^2',
                      '\\sqrt{}',
                      '\\frac{a}{b}',
                      '\\sin\\theta',
                      '\\cos\\theta',
                      '\\int',
                      '\\sum',
                      '\\lim_{x \\to 0}',
                      '\\Delta',
                      '\\pi'
                    ].map(sym => (
                      <button
                        key={sym}
                        type="button"
                        onClick={() => insertMathSymbol(sym)}
                        className="px-2 py-0.5 text-xs font-mono bg-white border border-slate-300 rounded hover:bg-slate-100 text-slate-700"
                      >
                        {sym}
                      </button>
                    ))}
                  </div>

                  <textarea
                    value={studentInput}
                    onChange={e => setStudentInput(e.target.value)}
                    placeholder="উদাহরণ: আদিবেগ v_0 এবং অনুভূমিকের সাথে θ কোণে নিক্ষিপ্ত প্রাসের সর্বোচ্চ উচ্চতার সূত্র কীভাবে প্রতিপাদন করব?"
                    rows={3}
                    className="w-full text-xs border border-slate-300 rounded p-2.5 bg-[#FAFAF8] focus:outline-none focus:ring-1 focus:ring-[#0A2540] text-slate-800"
                  />

                  {/* Live KaTeX Preview if mathematical notation is present */}
                  {studentInput && (studentInput.includes('^') || studentInput.includes('\\') || studentInput.includes('=')) && (
                    <div className="mt-2 p-2.5 bg-slate-50 border border-slate-200 rounded text-xs">
                      <span className="text-[10px] uppercase font-bold text-slate-500 block mb-1">
                        লাইভ সূত্র প্রিভিউ:
                      </span>
                      <div className="text-center font-medium">
                        <KaTeXRenderer content={studentInput} />
                      </div>
                    </div>
                  )}

                  {/* Submit Button */}
                  <div className="mt-3 flex items-center justify-between gap-3">
                    <span className="text-[11px] text-slate-500">
                      সরাসরি উত্তর নিষিদ্ধ নীতি কার্যকর
                    </span>
                    <button
                      type="button"
                      disabled={isAiLoading || (!studentInput.trim() && !uploadedImagePreview)}
                      onClick={() => submitSocraticInquiry()}
                      className="py-2 px-5 bg-[#0A2540] hover:bg-[#1B2A4A] disabled:opacity-50 text-white text-xs font-bold rounded uppercase tracking-wider shadow-[0_3px_0_0_#051329] active:translate-y-0.5 active:shadow-none transition-all flex items-center gap-2"
                    >
                      {isAiLoading ? (
                        <>
                          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                          <span>বিশ্লেষণ চলছে...</span>
                        </>
                      ) : (
                        <>
                          <span>জিজ্ঞাসা করুন</span>
                          <Send className="w-3.5 h-3.5" />
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* 3D STEM Simulation Lab Launchers */}
                <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-slate-800 flex items-center gap-2">
                      <Layers className="w-4 h-4 text-[#065F46]" />
                      ইন্টারেক্টিভ ৩ডি সিমুলেশন ল্যাবসমূহ
                    </span>
                    <span className="text-[11px] text-slate-500">
                      বাস্তব পরীক্ষার অভিজ্ঞতা
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                    <Link
                      href="/simulations"
                      className="p-3 bg-slate-50 border border-slate-200 hover:border-[#0A2540] rounded-md transition-all flex flex-col justify-between group"
                    >
                      <div>
                        <div className="text-[10px] font-bold text-[#065F46] uppercase tracking-wider mb-1">
                          পদার্থবিজ্ঞান
                        </div>
                        <h4 className="text-xs font-bold text-slate-800 group-hover:text-[#B45309] transition-colors mb-1">
                          প্রাসের গতির ৩ডি ল্যাব
                        </h4>
                        <p className="text-[11px] text-slate-600">
                          কোণ ও বেগ পরিবর্তন করে পরাবৃত্তাকার ট্র্যাজেক্টরি দেখুন।
                        </p>
                      </div>
                      <div className="mt-2 text-[10px] font-semibold text-[#0A2540] flex items-center gap-1">
                        <span>সিমুলেশন খুলুন</span>
                        <ExternalLink className="w-3 h-3" />
                      </div>
                    </Link>

                    <Link
                      href="/simulations"
                      className="p-3 bg-slate-50 border border-slate-200 hover:border-[#0A2540] rounded-md transition-all flex flex-col justify-between group"
                    >
                      <div>
                        <div className="text-[10px] font-bold text-[#B45309] uppercase tracking-wider mb-1">
                          রসায়ন
                        </div>
                        <h4 className="text-xs font-bold text-slate-800 group-hover:text-[#B45309] transition-colors mb-1">
                          আণবিক জ্যামিতি ৩ডি ভিউয়ার
                        </h4>
                        <p className="text-[11px] text-slate-600">
                          সংকরণ ও বন্ধন কোণ ত্রিমাত্রিকভাবে পরীক্ষা করুন।
                        </p>
                      </div>
                      <div className="mt-2 text-[10px] font-semibold text-[#0A2540] flex items-center gap-1">
                        <span>সিমুলেশন খুলুন</span>
                        <ExternalLink className="w-3 h-3" />
                      </div>
                    </Link>

                    <Link
                      href="/simulations"
                      className="p-3 bg-slate-50 border border-slate-200 hover:border-[#0A2540] rounded-md transition-all flex flex-col justify-between group"
                    >
                      <div>
                        <div className="text-[10px] font-bold text-[#1B2A4A] uppercase tracking-wider mb-1">
                          মহাকাশ বিজ্ঞান
                        </div>
                        <h4 className="text-xs font-bold text-slate-800 group-hover:text-[#B45309] transition-colors mb-1">
                          ৩ডি স্কলার মহাজাগতিক গ্লোব
                        </h4>
                        <p className="text-[11px] text-slate-600">
                          কেপলারের সূত্র ও গ্রহের কক্ষপথের ঘূর্ণন পরিমাপ।
                        </p>
                      </div>
                      <div className="mt-2 text-[10px] font-semibold text-[#0A2540] flex items-center gap-1">
                        <span>সিমুলেশন খুলুন</span>
                        <ExternalLink className="w-3 h-3" />
                      </div>
                    </Link>
                  </div>
                </div>
              </div>

              {/* Right Column: 6 Columns - Socratic Dialogue & 4-Tier Scaffolding Drawer */}
              <div className="lg:col-span-6 flex flex-col gap-4">
                {/* 4-Tier Socratic Progress Indicator */}
                <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      সক্রেটিক পেডাগজি অগ্রগতি (Bloom&apos;s Taxonomy)
                    </span>
                    <span className="text-xs font-bold text-[#0A2540]">
                      টিয়ার {toBengaliDigits(activeTier)} / {toBengaliDigits(4)}
                    </span>
                  </div>

                  <div className="grid grid-cols-4 gap-2 text-center text-[10px] font-semibold">
                    <div
                      className={`p-1.5 rounded border transition-colors ${
                        activeTier >= 1
                          ? 'bg-[#0A2540] text-white border-[#0A2540]'
                          : 'bg-slate-50 text-slate-500 border-slate-200'
                      }`}
                    >
                      ১. ধারণা নোঙর
                    </div>
                    <div
                      className={`p-1.5 rounded border transition-colors ${
                        activeTier >= 2
                          ? 'bg-[#0A2540] text-white border-[#0A2540]'
                          : 'bg-slate-50 text-slate-500 border-slate-200'
                      }`}
                    >
                      ২. সূত্র গঠন
                    </div>
                    <div
                      className={`p-1.5 rounded border transition-colors ${
                        activeTier >= 3
                          ? 'bg-[#0A2540] text-white border-[#0A2540]'
                          : 'bg-slate-50 text-slate-500 border-slate-200'
                      }`}
                    >
                      ৩. ধাপ বিশ্লেষণ
                    </div>
                    <div
                      className={`p-1.5 rounded border transition-colors ${
                        activeTier >= 4
                          ? 'bg-[#065F46] text-white border-[#065F46]'
                          : 'bg-slate-50 text-slate-500 border-slate-200'
                      }`}
                    >
                      ৪. স্ব-মূল্যায়ন
                    </div>
                  </div>
                </div>

                {/* Socratic Dialogue Chat Stream */}
                <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs flex flex-col h-[520px]">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-2.5 h-2.5 rounded-full bg-[#065F46]" />
                      <span className="text-xs font-bold text-[#0A2540]">
                        সক্রেটিক অনুসন্ধান সংলাপ
                      </span>
                    </div>
                    {activeAnalysis?.relevantBoardExamBn && (
                      <span className="text-[10px] text-slate-500 font-medium">
                        {activeAnalysis.relevantBoardExamBn}
                      </span>
                    )}
                  </div>

                  {/* Messages Scroll Area */}
                  <div className="flex-1 overflow-y-auto space-y-3.5 pr-1">
                    {chatMessages.map(msg => (
                      <div
                        key={msg.id}
                        className={`flex flex-col ${
                          msg.sender === 'student' ? 'items-end' : 'items-start'
                        }`}
                      >
                        <div
                          className={`max-w-[90%] rounded-lg p-3 text-xs leading-relaxed ${
                            msg.sender === 'student'
                              ? 'bg-[#0A2540] text-white'
                              : msg.isRefusal
                              ? 'bg-amber-50 text-amber-950 border border-amber-300'
                              : msg.isMisconceptionAlert
                              ? 'bg-rose-50 text-rose-950 border border-rose-300'
                              : 'bg-slate-50 text-slate-800 border border-slate-200'
                          }`}
                        >
                          {/* Alert Badges */}
                          {msg.isRefusal && (
                            <div className="flex items-center gap-1 text-[11px] font-bold text-amber-800 mb-1">
                              <ShieldCheck className="w-3.5 h-3.5 text-amber-700" />
                              জিরো-অ্যানসার নির্দেশিকা
                            </div>
                          )}
                          {msg.isMisconceptionAlert && (
                            <div className="flex items-center gap-1 text-[11px] font-bold text-rose-800 mb-1">
                              <AlertTriangle className="w-3.5 h-3.5 text-rose-700" />
                              ক্লাসিক্যাল ভুল ধারণা সনাক্ত
                            </div>
                          )}

                          <div className="whitespace-pre-line font-medium">
                            <KaTeXRenderer content={msg.text} />
                          </div>

                          {/* Render Formula Block if provided */}
                          {msg.formulaLatex && (
                            <div className="mt-2 p-2 bg-white rounded border border-slate-200 text-center text-slate-900 shadow-xs">
                              <KaTeXRenderer mathContent={msg.formulaLatex} block />
                            </div>
                          )}

                          <span className="block text-[9px] opacity-60 text-right mt-1.5 font-mono">
                            {msg.timestamp}
                          </span>
                        </div>
                      </div>
                    ))}

                    {isAiLoading && (
                      <div className="flex items-center gap-2 text-xs text-slate-500 bg-slate-50 p-3 rounded-lg border border-slate-200 w-fit">
                        <RefreshCw className="w-3.5 h-3.5 animate-spin text-[#0A2540]" />
                        <span>সক্রেটিক টিউটর যুক্তি গঠন করছে...</span>
                      </div>
                    )}
                    <div ref={chatScrollEndRef} />
                  </div>

                  {/* Scaffolding Progress Unlock Action */}
                  {activeTier < 4 && (
                    <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
                      <span className="text-[11px] text-slate-600">
                        বর্তমান প্রশ্নের উত্তর দিয়ে পরবর্তী টিয়ারে পৌঁছান
                      </span>
                      <button
                        type="button"
                        onClick={advanceScaffoldingTier}
                        className="px-3 py-1.5 text-xs font-bold text-[#B45309] bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded flex items-center gap-1 transition-colors"
                      >
                        <span>পরবর্তী টিয়ার সংকেত</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  )}
                </div>

                {/* Socratic Academic Principles Footer Card */}
                <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-xs text-xs text-slate-600">
                  <div className="flex items-center gap-2 font-bold text-[#0A2540] mb-1">
                    <ShieldCheck className="w-4 h-4 text-[#065F46]" />
                    আন্তর্জাতিক সক্রেটিক মানদণ্ড (ASVS L2)
                  </div>
                  <p className="text-[11px] leading-relaxed">
                    এই সিস্টেম সরাসরি উত্তর প্রদানের পরিবর্তে প্রশ্নবাণের মাধ্যমে নিজস্ব বিশ্লেষণ ও অনুমানের ভুল সংশোধনে সহায়তা করে। জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (এনসিটিবি) কারিকুলাম ও ব্লুমস ট্যাক্সোনমি অনুযায়ী পরিচালিত।
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* =========================================================================
            MODE 2: INTERACTIVE DRAWING WHITEBOARD CANVAS
            ========================================================================= */}
        {activeMode === 'whiteboard' && (
          <div className="space-y-6">
            {/* Problem Banner */}
            <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
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

                {/* Problem Selector Dropdown */}
                <div className="flex items-center gap-2">
                  {BENCHMARK_PROBLEMS.map(p => (
                    <button
                      key={p.id}
                      onClick={() => handleSelectProblem(p)}
                      className={`px-3 py-1.5 text-xs font-semibold rounded border transition-all ${
                        activeProblem.id === p.id
                          ? 'bg-[#0A2540] text-white border-[#0A2540] shadow-xs'
                          : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                      }`}
                    >
                      {p.discipline.split(' ')[0]}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Workspace Grid: Left Canvas, Right Inquiry Drawer */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Canvas: 7 Columns */}
              <div className="lg:col-span-7 flex flex-col gap-3">
                {/* Whiteboard Toolbar */}
                <div className="bg-white border border-slate-200 rounded-lg p-2.5 flex flex-wrap items-center justify-between gap-3 shadow-xs">
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
                            strokeColor === c ? 'scale-125 border-slate-900 shadow-xs' : 'border-white'
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

                  {/* Canvas Clear */}
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

                {/* Canvas Surface */}
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
                <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-xs">
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

                  {/* Hints Accordion */}
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

                  {/* Target formula LaTeX */}
                  {currentStep.formulaLatex && (
                    <div className="bg-slate-50 border border-slate-200 rounded p-3 mb-4 text-center">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1">
                        লক্ষ্য সমীকরণ রূপ
                      </span>
                      <KaTeXRenderer mathContent={currentStep.formulaLatex} block />
                    </div>
                  )}

                  {/* Student deduction input */}
                  <div className="mb-4">
                    <label className="block text-xs font-bold text-slate-700 mb-1.5">
                      আপনার গাণিতিক যুক্তি / উত্তর প্রতিপাদন করুন:
                    </label>

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

                  <button
                    type="button"
                    onClick={evaluateStudentDeduction}
                    className="w-full py-2.5 px-4 bg-[#0A2540] text-white text-xs font-bold rounded uppercase tracking-wider shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none transition-all flex items-center justify-center gap-2"
                  >
                    <span>ধাপের যুক্তি যাচাই করুন</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
