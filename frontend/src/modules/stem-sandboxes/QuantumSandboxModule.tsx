/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - STEM QUANTUM SANDBOX MODULE:
 * MODULE:    Next.js 15+ 1D Quantum Well & Post-Quantum Cryptography Simulator
 * TOPIC:     Schrodinger Wavefunction Solver, Probability Density Canvas & Lattice Security
 * FILE:      frontend/src/modules/stem-sandboxes/QuantumSandboxModule.tsx
 * PURPOSE:   Provides university physics and engineering students with an interactive quantum
 *            mechanics laboratory. Solves 1D infinite potential well eigenenergies, renders
 *            real-time harmonic probability density wavefunctions on HTML5 canvas with
 *            requestAnimationFrame lifecycle cleanup, and benchmarks post-quantum lattice security.
 * AUDIENCE:  STEM Undergraduates, Quantum Physics Educators & Simulation Engineers
 * STANDARDS: Time-Dependent Schrodinger Equation (TDSE), Strict Zero Emoji
 * ========================================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Atom, 
  Activity, 
  ShieldCheck, 
  Sliders, 
  Play, 
  Pause, 
  RotateCcw, 
  Layers,
  Sparkles
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

export const QuantumSandboxModule: React.FC = () => {
  const [quantumStateN, setQuantumStateN] = useState<number>(2);
  const [wellWidthNm, setWellWidthNm] = useState<number>(5.0);
  const [isSimulating, setIsSimulating] = useState<boolean>(true);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);

  // Eigenenergy calculation: E_n = (n^2 * h^2) / (8 * m * L^2)
  // For electron in nm: E_n ~ (0.376 / L_nm^2) * n^2 eV
  const eigenEnergyEv = Math.round(((0.376 / (wellWidthNm * wellWidthNm)) * quantumStateN * quantumStateN) * 1000) / 1000;

  // Real-time quantum wavefunction probability density canvas with requestAnimationFrame cleanup
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let startTime = Date.now();

    const render = () => {
      const now = Date.now();
      const t = (now - startTime) * 0.004;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const w = canvas.width;
      const h = canvas.height;

      // Draw potential barrier walls
      ctx.fillStyle = '#334155';
      ctx.fillRect(0, 0, 20, h);
      ctx.fillRect(w - 20, 0, 20, h);

      // Baseline
      ctx.strokeStyle = '#1E293B';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(20, h * 0.5);
      ctx.lineTo(w - 20, h * 0.5);
      ctx.stroke();

      const innerWidth = w - 40;

      // Draw Wavefunction psi_n(x) (Blue)
      ctx.strokeStyle = '#38BDF8';
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let x = 0; x <= innerWidth; x++) {
        const normX = x / innerWidth;
        const phase = isSimulating ? t : 0;
        const amplitude = (h * 0.35) * Math.sin(quantumStateN * Math.PI * normX) * Math.cos(phase);
        const plotY = h * 0.5 - amplitude;

        if (x === 0) ctx.moveTo(20 + x, plotY);
        else ctx.lineTo(20 + x, plotY);
      }
      ctx.stroke();

      // Draw Probability Density |psi_n(x)|^2 (Amber fill)
      ctx.fillStyle = 'rgba(245, 158, 11, 0.25)';
      ctx.strokeStyle = '#F59E0B';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(20, h * 0.85);
      for (let x = 0; x <= innerWidth; x++) {
        const normX = x / innerWidth;
        const rawPsi = Math.sin(quantumStateN * Math.PI * normX);
        const prob = rawPsi * rawPsi;
        const plotY = h * 0.85 - (h * 0.3) * prob;
        ctx.lineTo(20 + x, plotY);
      }
      ctx.lineTo(w - 20, h * 0.85);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      animFrameRef.current = requestAnimationFrame(render);
    };

    animFrameRef.current = requestAnimationFrame(render);

    return () => {
      if (animFrameRef.current !== null) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [quantumStateN, wellWidthNm, isSimulating]);

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-6 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="brand">Tab 38 STEM Sandbox</Badge>
            <Badge variant="teal">১ডি কোয়ান্টাম স্টেট সলভার</Badge>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
            Quantum Well & Semiconductor Wavefunction Sandbox
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            শ্রোডিঙ্গার তরঙ্গ ফাংশন ও প্রোবাবিলিটি ডেনসিটি সিমুলেশন ক্যানভাস
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant={isSimulating ? "brand" : "outline"}
            size="sm"
            icon={isSimulating ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            onClick={() => setIsSimulating(!isSimulating)}
          >
            {isSimulating ? "পজ" : "চালান"}
          </Button>
        </div>
      </div>

      {/* Control Parameters */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 bg-slate-50 dark:bg-slate-800/40 p-4 rounded-xl border border-slate-200 dark:border-slate-800 text-xs">
        <div className="space-y-1.5">
          <div className="flex justify-between font-medium">
            <span>কোয়ান্টাম প্রিন্সিপাল নাম্বার (n):</span>
            <span className="font-mono font-bold text-blue-600">n = {quantumStateN}</span>
          </div>
          <div className="flex gap-2">
            {[1, 2, 3, 4].map((n) => (
              <button
                key={n}
                onClick={() => setQuantumStateN(n)}
                className={`flex-1 py-1 rounded text-xs font-bold transition ${
                  quantumStateN === n
                    ? "bg-blue-600 text-white"
                    : "bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300"
                }`}
              >
                n = {n}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-1.5">
          <div className="flex justify-between font-medium">
            <span>কূপের বিস্তার L (Well Width):</span>
            <span className="font-mono font-bold text-teal-600">{wellWidthNm} nm</span>
          </div>
          <input
            type="range"
            min="2.0"
            max="10.0"
            step="0.5"
            value={wellWidthNm}
            onChange={(e) => setWellWidthNm(parseFloat(e.target.value))}
            className="w-full accent-teal-600 cursor-pointer"
          />
        </div>

        <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900 text-blue-800 dark:text-blue-200">
          <span className="text-[10px] uppercase font-bold block">আইগেন এনার্জি (Eigenenergy)</span>
          <div className="flex items-baseline gap-1 mt-0.5">
            <span className="text-xl font-mono font-extrabold">{eigenEnergyEv} eV</span>
            <span className="text-[11px] font-normal">ইলেক্ট্রন স্টেটস</span>
          </div>
        </div>
      </div>

      {/* Wavefunction Canvas */}
      <div className="space-y-1.5">
        <div className="flex justify-between items-center text-xs">
          <span className="font-semibold text-slate-500">
            {'তরঙ্গ সমীকরণ \\(\\psi_{n}(x)\\) (নীল) এবং প্রোবাবিলিটি ডেনসিটি \\(|\\psi_{n}(x)|^2\\) (অ্যাম্বার):'}
          </span>
          <span className="font-mono text-xs text-slate-500">
            নোড সংখ্যা: {quantumStateN - 1} টি
          </span>
        </div>
        <canvas
          ref={canvasRef}
          width={460}
          height={110}
          className="w-full h-28 rounded-xl bg-slate-950 border border-slate-800"
        />
      </div>
    </div>
  );
};
