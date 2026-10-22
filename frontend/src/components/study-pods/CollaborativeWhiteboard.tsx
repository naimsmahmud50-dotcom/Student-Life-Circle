/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Study Pods & Collaborative Classroom
 * TOPIC:     HTML5 Vector Whiteboard Canvas with KaTeX Notation Stamps
 * FILE:      frontend/src/components/study-pods/CollaborativeWhiteboard.tsx
 * PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
 * PURPOSE:   High-performance collaborative vector whiteboard with Apple Freeform
 *            floating frosted glass pill toolbar, multi-tool geometry, LaTeX formula
 *            stamping, real-time delta broadcasting, and tactile feedback.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React, { useRef, useState, useEffect, useCallback } from 'react';
import {
  PenTool,
  Highlighter,
  Eraser,
  Square,
  Circle,
  Slash,
  Sigma,
  Undo2,
  Redo2,
  Trash2,
  Download,
  Check,
  X,
  Plus,
  Move,
  Pin,
  Sparkles
} from 'lucide-react';
import { KaTeXRenderer } from '../quiz/katex-renderer';

export type WhiteboardTool =
  | 'pen'
  | 'highlighter'
  | 'eraser'
  | 'line'
  | 'rectangle'
  | 'circle'
  | 'latex';

export interface WhiteboardStroke {
  stroke_id: string;
  author_id: string;
  tool_type: WhiteboardTool;
  color: string;
  width: number;
  points: [number, number][];
  timestamp: number;
  is_erased?: boolean;
}

export interface LatexFormulaNode {
  formula_id: string;
  author_id: string;
  author_name?: string;
  latex_source: string;
  position_x: number;
  position_y: number;
  font_size: number;
  is_pinned?: boolean;
}

export interface CollaborativeWhiteboardProps {
  podId: string;
  userId: string;
  userName?: string;
  isReadOnly?: boolean;
  onDeltaBroadcast?: (type: 'stroke' | 'formula' | 'erase' | 'clear', delta: any) => void;
  className?: string;
}

const PALETTE_COLORS = [
  { name: 'Midnight', value: '#0F172A' },
  { name: 'Luminous Blue', value: '#2563EB' },
  { name: 'Mastery Teal', value: '#0D9488' },
  { name: 'Sunset Amber', value: '#D97706' },
  { name: 'Crimson', value: '#DC2626' },
  { name: 'Violet', value: '#7C3AED' }
];

const STROKE_WIDTHS = [
  { label: 'সূক্ষ্ম (Thin)', value: 2 },
  { label: 'মাঝারি (Medium)', value: 4 },
  { label: 'পুরু (Bold)', value: 8 }
];

const PRESET_FORMULAS = [
  { label: 'ক্যালকুলাস সমাকলন', code: '\\int_{a}^{b} f(x)\\,dx = F(b) - F(a)' },
  { label: 'পরাবৃত্ত (Conics)', code: 'y^2 = 4ax' },
  { label: 'ত্রিকোণমিতি অভেদ', code: '\\sin^2\\theta + \\cos^2\\theta = 1' },
  { label: 'মহাকর্ষ সূত্র', code: 'F = G\\,\\frac{m_1 m_2}{r^2}' },
  { label: 'আইনস্টাইন শক্তি সমীকরণ', code: 'E = mc^2' }
];

export const CollaborativeWhiteboard: React.FC<CollaborativeWhiteboardProps> = ({
  podId,
  userId,
  userName = 'Student Scholar',
  isReadOnly = false,
  onDeltaBroadcast,
  className = ''
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  // Whiteboard drawing states
  const [activeTool, setActiveTool] = useState<WhiteboardTool>('pen');
  const [currentColor, setCurrentColor] = useState<string>('#2563EB');
  const [currentWidth, setCurrentWidth] = useState<number>(3);

  // History & Delta stacks
  const [strokes, setStrokes] = useState<WhiteboardStroke[]>([]);
  const [undoneStrokes, setUndoneStrokes] = useState<WhiteboardStroke[]>([]);
  const [formulas, setFormulas] = useState<LatexFormulaNode[]>([]);

  // Drag / Drawing ephemeral state
  const [isDrawing, setIsDrawing] = useState<boolean>(false);
  const [currentStroke, setCurrentStroke] = useState<[number, number][]>([]);

  // LaTeX Modal State
  const [isLatexModalOpen, setIsLatexModalOpen] = useState<boolean>(false);
  const [latexInput, setLatexInput] = useState<string>('\\int_{0}^{\\infty} e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}');
  const [draggingFormulaId, setDraggingFormulaId] = useState<string | null>(null);
  const [dragOffset, setDragOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  // Redraw complete canvas
  const redrawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw grid background for engineering / mathematical precision
    ctx.save();
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.15)';
    ctx.lineWidth = 1;
    const gridSize = 32;
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
    ctx.restore();

    // Render all active strokes
    strokes.forEach((stroke) => {
      if (stroke.is_erased || stroke.points.length === 0) return;

      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      if (stroke.tool_type === 'highlighter') {
        ctx.globalAlpha = 0.35;
        ctx.strokeStyle = stroke.color;
        ctx.lineWidth = stroke.width * 4;
      } else {
        ctx.globalAlpha = 1.0;
        ctx.strokeStyle = stroke.color;
        ctx.lineWidth = stroke.width;
      }

      if (stroke.tool_type === 'rectangle' && stroke.points.length >= 2) {
        const [start, end] = [stroke.points[0], stroke.points[stroke.points.length - 1]];
        const width = end[0] - start[0];
        const height = end[1] - start[1];
        ctx.strokeRect(start[0], start[1], width, height);
      } else if (stroke.tool_type === 'circle' && stroke.points.length >= 2) {
        const [start, end] = [stroke.points[0], stroke.points[stroke.points.length - 1]];
        const rx = Math.abs(end[0] - start[0]) / 2;
        const ry = Math.abs(end[1] - start[1]) / 2;
        const cx = Math.min(start[0], end[0]) + rx;
        const cy = Math.min(start[1], end[1]) + ry;
        ctx.beginPath();
        ctx.ellipse(cx, cy, rx, ry, 0, 0, 2 * Math.PI);
        ctx.stroke();
      } else if (stroke.tool_type === 'line' && stroke.points.length >= 2) {
        const [start, end] = [stroke.points[0], stroke.points[stroke.points.length - 1]];
        ctx.beginPath();
        ctx.moveTo(start[0], start[1]);
        ctx.lineTo(end[0], end[1]);
        ctx.stroke();
      } else {
        // Freehand pen or highlighter
        ctx.beginPath();
        ctx.moveTo(stroke.points[0][0], stroke.points[0][1]);
        for (let i = 1; i < stroke.points.length; i++) {
          const pt = stroke.points[i];
          ctx.lineTo(pt[0], pt[1]);
        }
        ctx.stroke();
      }
      ctx.restore();
    });

    // Render ephemeral in-progress stroke
    if (currentStroke.length > 0) {
      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      if (activeTool === 'highlighter') {
        ctx.globalAlpha = 0.35;
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = currentWidth * 4;
      } else {
        ctx.globalAlpha = 1.0;
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = currentWidth;
      }

      if (activeTool === 'rectangle' && currentStroke.length >= 2) {
        const [start, end] = [currentStroke[0], currentStroke[currentStroke.length - 1]];
        ctx.strokeRect(start[0], start[1], end[0] - start[0], end[1] - start[1]);
      } else if (activeTool === 'circle' && currentStroke.length >= 2) {
        const [start, end] = [currentStroke[0], currentStroke[currentStroke.length - 1]];
        const rx = Math.abs(end[0] - start[0]) / 2;
        const ry = Math.abs(end[1] - start[1]) / 2;
        const cx = Math.min(start[0], end[0]) + rx;
        const cy = Math.min(start[1], end[1]) + ry;
        ctx.beginPath();
        ctx.ellipse(cx, cy, rx, ry, 0, 0, 2 * Math.PI);
        ctx.stroke();
      } else if (activeTool === 'line' && currentStroke.length >= 2) {
        const [start, end] = [currentStroke[0], currentStroke[currentStroke.length - 1]];
        ctx.beginPath();
        ctx.moveTo(start[0], start[1]);
        ctx.lineTo(end[0], end[1]);
        ctx.stroke();
      } else {
        ctx.beginPath();
        ctx.moveTo(currentStroke[0][0], currentStroke[0][1]);
        for (let i = 1; i < currentStroke.length; i++) {
          ctx.lineTo(currentStroke[i][0], currentStroke[i][1]);
        }
        ctx.stroke();
      }
      ctx.restore();
    }
  }, [strokes, currentStroke, activeTool, currentColor, currentWidth]);

  // Adjust canvas dimensions to parent container with devicePixelRatio
  useEffect(() => {
    const handleResize = () => {
      const canvas = canvasRef.current;
      const container = containerRef.current;
      if (!canvas || !container) return;

      const rect = container.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;

      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;

      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.scale(dpr, dpr);
      }
      redrawCanvas();
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [redrawCanvas]);

  // Redraw when strokes change
  useEffect(() => {
    redrawCanvas();
  }, [redrawCanvas]);

  // Fetch initial whiteboard state from backend
  useEffect(() => {
    let isMounted = true;
    async function loadWhiteboardState() {
      try {
        const res = await fetch(`/api/v1/study-pods/${podId}/whiteboard`);
        if (res.ok) {
          const data = await res.json();
          if (isMounted) {
            if (data.strokes && Array.isArray(data.strokes)) {
              setStrokes(data.strokes);
            }
            if (data.formulas && Array.isArray(data.formulas)) {
              setFormulas(data.formulas);
            }
          }
        }
      } catch (err) {
        // Fallback gracefully in offline / initial state
      }
    }
    loadWhiteboardState();
    return () => {
      isMounted = false;
    };
  }, [podId]);

  // Coordinate normalizer
  const getCanvasCoords = (e: React.PointerEvent<HTMLCanvasElement>): [number, number] => {
    const canvas = canvasRef.current;
    if (!canvas) return [0, 0];
    const rect = canvas.getBoundingClientRect();
    return [e.clientX - rect.left, e.clientY - rect.top];
  };

  // Pointer Events for Drawing
  const handlePointerDown = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (isReadOnly) return;
    const coords = getCanvasCoords(e);

    if (activeTool === 'eraser') {
      // Find stroke closest to eraser point (hit test)
      const eraserRadius = 16;
      const hitStrokeIndex = strokes.findIndex((s) => {
        return s.points.some(
          (pt) => Math.hypot(pt[0] - coords[0], pt[1] - coords[1]) <= eraserRadius
        );
      });
      if (hitStrokeIndex !== -1) {
        const erased = strokes[hitStrokeIndex];
        const nextStrokes = strokes.filter((_, idx) => idx !== hitStrokeIndex);
        setStrokes(nextStrokes);
        onDeltaBroadcast?.('erase', { stroke_id: erased.stroke_id });
      }
      return;
    }

    if (activeTool === 'latex') {
      setIsLatexModalOpen(true);
      return;
    }

    setIsDrawing(true);
    setCurrentStroke([coords]);
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawing || isReadOnly) return;
    const coords = getCanvasCoords(e);

    if (activeTool === 'rectangle' || activeTool === 'circle' || activeTool === 'line') {
      // For geometric shapes: start point + current cursor end point
      setCurrentStroke((prev) => (prev.length > 0 ? [prev[0], coords] : [coords]));
    } else {
      // Freehand drawing: append coordinate point
      setCurrentStroke((prev) => [...prev, coords]);
    }
  };

  const handlePointerUp = () => {
    if (!isDrawing || isReadOnly) return;
    setIsDrawing(false);

    if (currentStroke.length > 0) {
      const newStroke: WhiteboardStroke = {
        stroke_id: `stroke-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
        author_id: userId,
        tool_type: activeTool,
        color: currentColor,
        width: currentWidth,
        points: currentStroke,
        timestamp: Date.now()
      };

      setStrokes((prev) => [...prev, newStroke]);
      setUndoneStrokes([]);
      setCurrentStroke([]);

      onDeltaBroadcast?.('stroke', newStroke);
    }
  };

  // Undo / Redo
  const handleUndo = () => {
    if (strokes.length === 0) return;
    const last = strokes[strokes.length - 1];
    setStrokes((prev) => prev.slice(0, -1));
    setUndoneStrokes((prev) => [...prev, last]);
    onDeltaBroadcast?.('erase', { stroke_id: last.stroke_id });
  };

  const handleRedo = () => {
    if (undoneStrokes.length === 0) return;
    const toRestore = undoneStrokes[undoneStrokes.length - 1];
    setUndoneStrokes((prev) => prev.slice(0, -1));
    setStrokes((prev) => [...prev, toRestore]);
    onDeltaBroadcast?.('stroke', toRestore);
  };

  const handleClear = () => {
    if (strokes.length === 0 && formulas.length === 0) return;
    if (window.confirm('আপনি কি সম্পূর্ণ ক্যানভাস পরিষ্কার করতে চান?')) {
      setStrokes([]);
      setFormulas([]);
      setUndoneStrokes([]);
      onDeltaBroadcast?.('clear', {});
    }
  };

  // Download snapshot
  const handleDownload = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const dataUrl = canvas.toDataURL('image/png');
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = `ogrojatra-whiteboard-${podId}-${Date.now()}.png`;
    a.click();
  };

  // Insert LaTeX Formula Node
  const handleInsertFormula = () => {
    if (!latexInput.trim()) return;
    const node: LatexFormulaNode = {
      formula_id: `formula-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
      author_id: userId,
      author_name: userName,
      latex_source: latexInput.trim(),
      position_x: 80,
      position_y: 80 + formulas.length * 50,
      font_size: 18,
      is_pinned: false
    };

    setFormulas((prev) => [...prev, node]);
    setIsLatexModalOpen(false);
    onDeltaBroadcast?.('formula', node);
  };

  const handleDeleteFormula = (formulaId: string) => {
    setFormulas((prev) => prev.filter((f) => f.formula_id !== formulaId));
    onDeltaBroadcast?.('erase', { formula_id: formulaId });
  };

  const handleTogglePinFormula = (formulaId: string) => {
    setFormulas((prev) =>
      prev.map((f) =>
        f.formula_id === formulaId ? { ...f, is_pinned: !f.is_pinned } : f
      )
    );
  };

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full min-h-[540px] bg-slate-50 dark:bg-slate-950 overflow-hidden select-none font-bengali rounded-3xl border border-slate-200/80 dark:border-slate-800/80 shadow-ambient ${className}`}
    >
      {/* HTML5 Canvas */}
      <canvas
        ref={canvasRef}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerCancel={handlePointerUp}
        className="absolute inset-0 w-full h-full cursor-crosshair touch-none"
      />

      {/* Rendered Interactive LaTeX Formula Nodes */}
      {formulas.map((formula) => (
        <div
          key={formula.formula_id}
          style={{
            left: `${formula.position_x}px`,
            top: `${formula.position_y}px`
          }}
          className={`absolute z-20 group p-3 rounded-2xl bg-white dark:bg-slate-900 border ${
            formula.is_pinned
              ? 'border-amber-400/80 shadow-md ring-2 ring-amber-400/20'
              : 'border-slate-200/80 dark:border-slate-700/80 shadow-lg'
          } transition-all duration-150`}
        >
          {/* Controls bar on hover */}
          <div className="flex items-center justify-between gap-3 mb-1.5 opacity-90 text-xs text-slate-500">
            <span className="font-semibold text-slate-700 dark:text-slate-300">
              {formula.author_name || 'গণিত সূত্র'}
            </span>
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => handleTogglePinFormula(formula.formula_id)}
                className={`p-1 rounded-lg transition-colors ${
                  formula.is_pinned
                    ? 'text-amber-500 bg-amber-50 dark:bg-amber-950/40'
                    : 'hover:text-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
                title={formula.is_pinned ? 'পিন খোলা' : 'পিন করুন'}
              >
                <Pin className="w-3.5 h-3.5" strokeWidth={1.75} />
              </button>
              {!formula.is_pinned && (
                <button
                  type="button"
                  onClick={() => handleDeleteFormula(formula.formula_id)}
                  className="p-1 rounded-lg hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors"
                  title="মুছে ফেলুন"
                >
                  <X className="w-3.5 h-3.5" strokeWidth={1.75} />
                </button>
              )}
            </div>
          </div>

          {/* KaTeX Math View */}
          <div className="text-slate-900 dark:text-white px-1 py-0.5">
            <KaTeXRenderer content={`$$${formula.latex_source}$$`} block />
          </div>
        </div>
      ))}

      {/* Academic Floating Pill Toolbar */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-30 flex items-center gap-2 px-4 py-2 rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl">
        {/* Tool Selector Buttons */}
        <div className="flex items-center gap-1 pr-2 border-r border-slate-200 dark:border-slate-700">
          <button
            type="button"
            onClick={() => setActiveTool('pen')}
            className={`p-2 rounded-full transition-all active:scale-95 ${
              activeTool === 'pen'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="কলম (Pen)"
          >
            <PenTool className="w-4 h-4" strokeWidth={1.75} />
          </button>

          <button
            type="button"
            onClick={() => setActiveTool('highlighter')}
            className={`p-2 rounded-full transition-all active:scale-95 ${
              activeTool === 'highlighter'
                ? 'bg-amber-500 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="হাইলাইটার (Highlighter)"
          >
            <Highlighter className="w-4 h-4" strokeWidth={1.75} />
          </button>

          <button
            type="button"
            onClick={() => setActiveTool('line')}
            className={`p-2 rounded-full transition-all active:scale-95 ${
              activeTool === 'line'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="সরলরেখা (Line)"
          >
            <Slash className="w-4 h-4" strokeWidth={1.75} />
          </button>

          <button
            type="button"
            onClick={() => setActiveTool('rectangle')}
            className={`p-2 rounded-full transition-all active:scale-95 ${
              activeTool === 'rectangle'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="আয়াতক্ষেত্র (Rectangle)"
          >
            <Square className="w-4 h-4" strokeWidth={1.75} />
          </button>

          <button
            type="button"
            onClick={() => setActiveTool('circle')}
            className={`p-2 rounded-full transition-all active:scale-95 ${
              activeTool === 'circle'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="বৃত্ত (Circle)"
          >
            <Circle className="w-4 h-4" strokeWidth={1.75} />
          </button>

          <button
            type="button"
            onClick={() => setActiveTool('eraser')}
            className={`p-2 rounded-full transition-all active:scale-95 ${
              activeTool === 'eraser'
                ? 'bg-rose-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="ইরেজার (Eraser)"
          >
            <Eraser className="w-4 h-4" strokeWidth={1.75} />
          </button>

          <button
            type="button"
            onClick={() => {
              setActiveTool('latex');
              setIsLatexModalOpen(true);
            }}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-full transition-all active:scale-95 text-xs font-semibold ${
              activeTool === 'latex'
                ? 'bg-emerald-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
            title="গণিত সূত্র যুক্ত করুন (LaTeX)"
          >
            <Sigma className="w-4 h-4" strokeWidth={1.75} />
            <span className="hidden sm:inline">সূত্র (LaTeX)</span>
          </button>
        </div>

        {/* Color Swatches */}
        <div className="flex items-center gap-1.5 px-2 border-r border-slate-200 dark:border-slate-700">
          {PALETTE_COLORS.map((c) => (
            <button
              key={c.value}
              type="button"
              onClick={() => setCurrentColor(c.value)}
              style={{ backgroundColor: c.value }}
              className={`w-5 h-5 rounded-full transition-transform active:scale-90 ${
                currentColor === c.value
                  ? 'ring-2 ring-offset-2 ring-blue-500 scale-110 shadow-sm'
                  : 'hover:scale-105 opacity-90'
              }`}
              title={c.name}
            />
          ))}
        </div>

        {/* Stroke Width Selector */}
        <div className="hidden md:flex items-center gap-1 px-2 border-r border-slate-200 dark:border-slate-700">
          {STROKE_WIDTHS.map((w) => (
            <button
              key={w.value}
              type="button"
              onClick={() => setCurrentWidth(w.value)}
              className={`px-2 py-1 text-xs font-medium rounded-lg transition-colors ${
                currentWidth === w.value
                  ? 'bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-white font-semibold'
                  : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              {w.value}px
            </button>
          ))}
        </div>

        {/* Action Controls: Undo, Redo, Clear, Download */}
        <div className="flex items-center gap-1 pl-1">
          <button
            type="button"
            onClick={handleUndo}
            disabled={strokes.length === 0}
            className="p-2 rounded-full text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            title="পূর্বাবস্থায় ফেরান (Undo)"
          >
            <Undo2 className="w-4 h-4" strokeWidth={1.75} />
          </button>
          <button
            type="button"
            onClick={handleRedo}
            disabled={undoneStrokes.length === 0}
            className="p-2 rounded-full text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            title="পুনরায় করুন (Redo)"
          >
            <Redo2 className="w-4 h-4" strokeWidth={1.75} />
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="p-2 rounded-full text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-all"
            title="ক্যানভাস মুছুন (Clear)"
          >
            <Trash2 className="w-4 h-4" strokeWidth={1.75} />
          </button>
          <button
            type="button"
            onClick={handleDownload}
            className="p-2 rounded-full text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-950/30 transition-all"
            title="চিত্র সংরক্ষণ করুন (Download PNG)"
          >
            <Download className="w-4 h-4" strokeWidth={1.75} />
          </button>
        </div>
      </div>

      {/* LaTeX Formula Stamp Modal */}
      {isLatexModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 animate-in fade-in">
          <div className="w-full max-w-lg p-6 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-950 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                  <Sigma className="w-4 h-4" strokeWidth={1.75} />
                </div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  গাণিতিক সূত্র স্ট্যাম্প (LaTeX Math Stamp)
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setIsLatexModalOpen(false)}
                className="p-1 rounded-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-5 h-5" strokeWidth={1.75} />
              </button>
            </div>

            {/* Quick Presets */}
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                সহজ প্রিসেট (Quick Presets)
              </span>
              <div className="flex flex-wrap gap-1.5">
                {PRESET_FORMULAS.map((preset) => (
                  <button
                    key={preset.label}
                    type="button"
                    onClick={() => setLatexInput(preset.code)}
                    className="px-3 py-1.5 text-xs font-semibold rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-blue-600 hover:text-white dark:hover:bg-blue-600 dark:hover:text-white transition-all shadow-sm active:scale-95"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Input textarea */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-600 dark:text-slate-400">
                LaTeX কোড লিখুন:
              </label>
              <textarea
                value={latexInput}
                onChange={(e) => setLatexInput(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 text-sm font-mono rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-900 dark:text-slate-100"
                placeholder="উদাহরণ: \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
              />
            </div>

            {/* Live KaTeX Preview */}
            <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200/80 dark:border-slate-800/80 min-h-[70px] flex items-center justify-center text-slate-900 dark:text-white">
              <KaTeXRenderer content={`$$${latexInput}$$`} block />
            </div>

            {/* Action Buttons */}
            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setIsLatexModalOpen(false)}
                className="px-4 py-2 text-sm font-semibold rounded-2xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
              >
                বাতিল করুন
              </button>
              <button
                type="button"
                onClick={handleInsertFormula}
                className="btn-push-brand px-5 py-2 text-sm font-semibold text-white bg-blue-600 rounded-2xl flex items-center gap-1.5 shadow-md active:scale-95"
              >
                <Plus className="w-4 h-4" strokeWidth={1.75} />
                ক্যানভাসে যুক্ত করুন
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
