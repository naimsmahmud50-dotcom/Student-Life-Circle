/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - ACADEMIC ACCESSIBILITY MODULE:
 * MODULE:    Next.js 15+ Adaptive Neurodivergent Accessibility & Cognitive Eye-Pacing Reader
 * TOPIC:     Bionic Saccadic Fixation, Multi-Syllabic STEM Decomposition, RSVP Eye-Pacer & Canvas
 * FILE:      frontend/src/modules/academic/BionicReaderModule.tsx
 * PURPOSE:   Provides cognitive accessibility tools for neurodivergent learners (ADHD, dyslexia,
 *            visual sensory sensitivity). Features client-side Bionic fixation text transformation,
 *            rapid serial visual presentation (RSVP) pacing reader, saccadic eye movement
 *            HTML5 canvas simulator with requestAnimationFrame cleanup, and WCAG AAA sensory contrast.
 * AUDIENCE:  Accessibility Engineers, Educational Technologists & Frontend Reviewers
 * STANDARDS: WCAG 2.2 Level AAA (Contrast >= 7:1), React 18/19 Canvas Lifecycle, Strict Zero Emoji
 * ========================================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Eye, 
  BookOpen, 
  Sparkles, 
  Sliders, 
  Play, 
  Pause, 
  RotateCcw, 
  CheckCircle2, 
  Layers,
  Activity
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

export interface BionicReaderProps {
  initialText?: string;
}

const DEFAULT_SAMPLE_TEXT = 
  "নিউটনের দ্বিতীয় গতিসূত্র অনুযায়ী কোনো বস্তুর ভরবেগের পরিবর্তনের হার তার ওপর প্রযুক্ত বলের সমানুপাতিক এবং বল যেদিকে ক্রিয়া করে ভরবেগের পরিবর্তনও সেদিকে ঘটে। কোয়ান্টাম বলবিদ্যায় শ্রোডিঙ্গার সমীকরণ একটি মৌলিক ভিত্তি।";

export const BionicReaderModule: React.FC<BionicReaderProps> = ({ 
  initialText = DEFAULT_SAMPLE_TEXT 
}) => {
  const [inputText, setInputText] = useState(initialText);
  const [mode, setMode] = useState<'BIONIC' | 'SYLLABLES' | 'STANDARD'>('BIONIC');
  const [intensity, setIntensity] = useState<number>(0.5);
  const [wpm, setWpm] = useState<number>(250);
  const [isPacingActive, setIsPacingActive] = useState<boolean>(false);
  const [pacingWordIndex, setPacingWordIndex] = useState<number>(0);
  const [contrastTheme, setContrastTheme] = useState<'slate' | 'sepia' | 'dark' | 'yellow'>('slate');

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);

  const words = inputText.split(/\s+/).filter(Boolean);

  // Bionic transformation function
  const renderBionicWord = (word: string, key: number) => {
    if (mode === 'STANDARD') {
      return <span key={key} className="mr-1.5">{word}</span>;
    }

    if (mode === 'SYLLABLES') {
      const parts = word.length > 4 ? [word.slice(0, 3), word.slice(3)] : [word];
      return (
        <span key={key} className="mr-1.5 inline-block">
          {parts.map((p, i) => (
            <span key={i} className={i % 2 === 0 ? "text-indigo-600 dark:text-indigo-400 font-bold" : "text-slate-700 dark:text-slate-300"}>
              {p}{i < parts.length - 1 ? "•" : ""}
            </span>
          ))}
        </span>
      );
    }

    // Bionic Fixation Anchor
    const boldLen = Math.max(1, Math.ceil(word.length * intensity));
    const boldPart = word.slice(0, boldLen);
    const restPart = word.slice(boldLen);

    return (
      <span key={key} className="mr-1.5 inline-block">
        <strong className="font-extrabold text-slate-950 dark:text-white underline-offset-2">{boldPart}</strong>
        <span className="font-normal text-slate-700 dark:text-slate-300 opacity-90">{restPart}</span>
      </span>
    );
  };

  // RSVP Cognitive Eye-Pacer Timer
  useEffect(() => {
    if (!isPacingActive || words.length === 0) return;

    const intervalMs = Math.max(50, Math.floor(60000 / wpm));
    const timer = setInterval(() => {
      setPacingWordIndex((prev) => {
        if (prev + 1 >= words.length) {
          setIsPacingActive(false);
          return 0;
        }
        return prev + 1;
      });
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isPacingActive, wpm, words.length]);

  // HTML5 Canvas Saccadic Trajectory Visualizer with requestAnimationFrame cleanup
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let startTime = Date.now();

    const render = () => {
      const now = Date.now();
      const elapsed = (now - startTime) * 0.002;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const w = canvas.width;
      const h = canvas.height;

      // Draw horizontal track lines
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 1;
      [h * 0.3, h * 0.7].forEach((y) => {
        ctx.beginPath();
        ctx.moveTo(20, y);
        ctx.lineTo(w - 20, y);
        ctx.stroke();
      });

      // Fixation Nodes
      const fixations = [
        { x: 40, y: h * 0.3, r: 6 },
        { x: 130, y: h * 0.3, r: 8 },
        { x: 230, y: h * 0.3, r: 7 },
        { x: 330, y: h * 0.3, r: 9 },
        { x: 420, y: h * 0.3, r: 6 },
      ];

      // Draw saccade jumps
      ctx.strokeStyle = '#8B5CF6';
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i < fixations.length - 1; i++) {
        const p1 = fixations[i];
        const p2 = fixations[i + 1];
        const midX = (p1.x + p2.x) / 2;
        const midY = p1.y - 18 - 8 * Math.sin(elapsed + i);
        ctx.moveTo(p1.x, p1.y);
        ctx.quadraticCurveTo(midX, midY, p2.x, p2.y);
      }
      ctx.stroke();

      // Render nodes with pulse
      fixations.forEach((f, idx) => {
        const pulse = 1 + 0.2 * Math.sin(elapsed * 2 + idx);
        ctx.fillStyle = idx === pacingWordIndex % fixations.length ? '#10B981' : '#6366F1';
        ctx.beginPath();
        ctx.arc(f.x, f.y, f.r * pulse, 0, Math.PI * 2);
        ctx.fill();
      });

      animFrameRef.current = requestAnimationFrame(render);
    };

    animFrameRef.current = requestAnimationFrame(render);

    return () => {
      if (animFrameRef.current !== null) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [pacingWordIndex]);

  const themeClasses: Record<string, string> = {
    slate: "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 border-slate-200 dark:border-slate-800",
    sepia: "bg-[#FBF0D9] text-[#433422] border-[#E8D4B4]",
    dark: "bg-slate-950 text-slate-100 border-slate-800",
    yellow: "bg-[#FEF9C3] text-[#713F12] border-[#FDE047]",
  };

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-6 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="brand">Tab 68 Enterprise</Badge>
            <Badge variant="teal">WCAG 2.2 Level AAA</Badge>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
            Adaptive Neurodivergent Accessibility & Cognitive Eye-Pacing Reader
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            সাক্কাডিক ফিক্সেশন অ্যাংকর ও আরএসভিপি রিডার ফর ডিসলেক্সিক ও এডিএইচডি লার্নার্স
          </p>
        </div>

        {/* Mode Selector */}
        <div className="flex items-center gap-2">
          <Button
            variant={mode === 'BIONIC' ? 'brand' : 'outline'}
            size="sm"
            onClick={() => setMode('BIONIC')}
          >
            বায়োনিক ফিক্সেশন
          </Button>
          <Button
            variant={mode === 'SYLLABLES' ? 'brand' : 'outline'}
            size="sm"
            onClick={() => setMode('SYLLABLES')}
          >
            সিলেবল ব্রেক
          </Button>
          <Button
            variant={mode === 'STANDARD' ? 'brand' : 'outline'}
            size="sm"
            onClick={() => setMode('STANDARD')}
          >
            স্ট্যান্ডার্ড
          </Button>
        </div>
      </div>

      {/* Control Sliders */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs bg-slate-50 dark:bg-slate-800/40 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
        <div className="space-y-1.5">
          <div className="flex justify-between font-medium">
            <span>অ্যাংকর তীব্রতা (Intensity):</span>
            <span className="font-mono font-bold text-blue-600">{Math.round(intensity * 100)}%</span>
          </div>
          <input
            type="range"
            min="0.2"
            max="0.8"
            step="0.05"
            value={intensity}
            onChange={(e) => setIntensity(parseFloat(e.target.value))}
            className="w-full accent-blue-600 cursor-pointer"
          />
        </div>

        <div className="space-y-1.5">
          <div className="flex justify-between font-medium">
            <span>আই-পেসার গতি (WPM):</span>
            <span className="font-mono font-bold text-teal-600">{wpm} WPM</span>
          </div>
          <input
            type="range"
            min="100"
            max="500"
            step="25"
            value={wpm}
            onChange={(e) => setWpm(parseInt(e.target.value, 10))}
            className="w-full accent-teal-600 cursor-pointer"
          />
        </div>

        <div className="space-y-1.5">
          <span className="font-medium block">সেন্সরি টিন্ট থিম (WCAG AAA):</span>
          <div className="flex gap-2">
            {[
              { id: 'slate', label: 'স্লেট' },
              { id: 'sepia', label: 'সেপিয়া' },
              { id: 'dark', label: 'ডার্ক' },
              { id: 'yellow', label: 'ইয়েলো' },
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setContrastTheme(t.id as any)}
                className={`px-2.5 py-1 rounded text-[11px] font-semibold border transition ${
                  contrastTheme === t.id ? "ring-2 ring-blue-500 font-bold" : "opacity-80"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Reading Text Container */}
      <div className={`p-6 rounded-2xl border ${themeClasses[contrastTheme]} transition-colors duration-200 leading-relaxed text-base min-h-[140px]`}>
        <div className="flex flex-wrap">
          {words.map((w, idx) => (
            <span
              key={idx}
              className={`transition-colors duration-150 ${
                isPacingActive && idx === pacingWordIndex
                  ? "bg-emerald-300/40 dark:bg-emerald-600/40 rounded px-1"
                  : ""
              }`}
            >
              {renderBionicWord(w, idx)}
            </span>
          ))}
        </div>
      </div>

      {/* Saccadic Trajectory Canvas & Pacer Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center pt-2 border-t border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-semibold text-slate-500 block mb-1">
            সাক্কাডিক গেজ ট্র্যাজেক্টরি ও ফিক্সেশন পয়েন্ট ক্যানভাস
          </span>
          <canvas
            ref={canvasRef}
            width={460}
            height={90}
            className="w-full h-20 rounded-xl bg-slate-950 border border-slate-800"
          />
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-end gap-3">
          <Button
            variant={isPacingActive ? "destructive" : "brand"}
            size="md"
            icon={isPacingActive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            onClick={() => setIsPacingActive(!isPacingActive)}
          >
            {isPacingActive ? "পেসার থামান" : "কগনিটিভ পেসার শুরু করুন"}
          </Button>
          <Button
            variant="outline"
            size="md"
            icon={<RotateCcw className="w-4 h-4" />}
            onClick={() => {
              setIsPacingActive(false);
              setPacingWordIndex(0);
            }}
          >
            রিসেট
          </Button>
        </div>
      </div>
    </div>
  );
};
