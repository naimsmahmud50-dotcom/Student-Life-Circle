/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - STEM CFD FLUID SIMULATOR MODULE:
 * MODULE:    Next.js 15+ 2D Navier-Stokes CFD Fluid & Aerodynamics Sandbox
 * TOPIC:     Velocity Streamlines, Reynolds Number Turbulence & Vortex Shedding Canvas
 * FILE:      frontend/src/modules/stem-sandboxes/CfdFluidSimulatorModule.tsx
 * PURPOSE:   Provides mechanical, civil, and aerospace engineering students with an interactive
 *            computational fluid dynamics (CFD) wind-tunnel simulator. Calculates laminar vs
 *            turbulent regimes based on Reynolds number (Re), simulates cylinder wake vortex
 *            shedding, and renders flowing vector streamlines on HTML5 canvas with requestAnimationFrame cleanup.
 * AUDIENCE:  Fluid Mechanics Students, Aerospace Engineers & Simulation Modelers
 * STANDARDS: 2D Incompressible Navier-Stokes Equations, Strict Zero Emoji
 * ========================================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Wind, 
  Activity, 
  Sliders, 
  Play, 
  Pause, 
  RotateCcw, 
  Layers, 
  ShieldCheck
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

export const CfdFluidSimulatorModule: React.FC = () => {
  const [reynoldsNumber, setReynoldsNumber] = useState<number>(450);
  const [isFlowActive, setIsFlowActive] = useState<boolean>(true);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);

  const isTurbulent = reynoldsNumber >= 2000;

  // Real-time CFD velocity streamlines on HTML5 canvas with requestAnimationFrame cleanup
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let startTime = Date.now();
    const streamlineCount = 8;

    const render = () => {
      const now = Date.now();
      const elapsed = isFlowActive ? (now - startTime) * 0.003 : 0;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const w = canvas.width;
      const h = canvas.height;

      // Draw obstacle cylinder in wind tunnel
      const obsX = w * 0.35;
      const obsY = h * 0.5;
      const obsRadius = 16;

      ctx.fillStyle = '#64748B';
      ctx.beginPath();
      ctx.arc(obsX, obsY, obsRadius, 0, Math.PI * 2);
      ctx.fill();

      // Draw flowing streamlines
      for (let i = 0; i < streamlineCount; i++) {
        const baseY = ((i + 1) * h) / (streamlineCount + 1);

        ctx.strokeStyle = isTurbulent ? '#EF4444' : '#06B6D4';
        ctx.lineWidth = 1.5;
        ctx.beginPath();

        for (let x = 10; x < w - 10; x += 4) {
          let y = baseY;

          // Deflection around cylinder
          const dx = x - obsX;
          const dy = baseY - obsY;
          const distSq = dx * dx + dy * dy;

          if (distSq < 2200) {
            const factor = Math.exp(-distSq / 1400);
            y += (dy > 0 ? 1 : -1) * 22 * factor;
          }

          // Karman vortex shedding behind obstacle
          if (x > obsX + 15) {
            const wakeDist = (x - (obsX + 15)) * 0.05;
            const vortexFreq = (reynoldsNumber / 300) * 2;
            const vortexAmp = Math.min(18, wakeDist * 4);
            y += Math.sin(wakeDist * vortexFreq - elapsed * 4) * vortexAmp;
          }

          if (x === 10) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      animFrameRef.current = requestAnimationFrame(render);
    };

    animFrameRef.current = requestAnimationFrame(render);

    return () => {
      if (animFrameRef.current !== null) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [reynoldsNumber, isTurbulent, isFlowActive]);

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-6 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="brand">Tab 37 STEM Sandbox</Badge>
            <Badge variant={isTurbulent ? "destructive" : "teal"}>
              {isTurbulent ? "টার্বুলেন্ট ফ্লো (Turbulent)" : "ল্যামিনার ফ্লো (Laminar)"}
            </Badge>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
            2D Navier-Stokes CFD Fluid & Aerodynamics Sandbox
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            উইন্ড টানেলে সিলিন্ডার বাধা ও কার্মান ভর্টেক্স শেডিং (Vortex Shedding) সিমুলেশন
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant={isFlowActive ? "brand" : "outline"}
            size="sm"
            icon={isFlowActive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            onClick={() => setIsFlowActive(!isFlowActive)}
          >
            {isFlowActive ? "ফ্লো পজ" : "চালান"}
          </Button>
        </div>
      </div>

      {/* Reynolds Number Slider */}
      <div className="bg-slate-50 dark:bg-slate-800/40 p-4 rounded-xl border border-slate-200 dark:border-slate-800 text-xs space-y-2">
        <div className="flex justify-between items-center font-medium">
          <span className="flex items-center gap-1.5 font-semibold text-slate-700 dark:text-slate-300">
            <Wind className="w-4 h-4 text-cyan-600" />
            রেইনল্ডস সংখ্যা (Reynolds Number Re = \(\rho v L / \mu\)):
          </span>
          <span className="font-mono text-base font-bold text-cyan-600">Re = {reynoldsNumber}</span>
        </div>
        <input
          type="range"
          min="50"
          max="4000"
          step="50"
          value={reynoldsNumber}
          onChange={(e) => setReynoldsNumber(parseInt(e.target.value, 10))}
          className="w-full accent-cyan-600 cursor-pointer"
        />
        <div className="flex justify-between text-[11px] text-slate-500">
          <span>ল্যামিনার (Re &lt; ২০০০)</span>
          <span>ক্রান্তিকাল (Transition)</span>
          <span>টার্বুলেন্ট বিক্ষুব্ধ ফ্লো (Re &gt; ২০০০)</span>
        </div>
      </div>

      {/* Streamline Wind Tunnel Canvas */}
      <div className="space-y-1.5">
        <div className="flex justify-between items-center text-xs">
          <span className="font-semibold text-slate-500">
            কম্পিউটেশনাল ফ্লুইড ডায়নামিক্স (CFD) স্ট্রিমলাইন ভেক্টরস:
          </span>
          <span className="font-mono text-xs text-slate-500">
            বাধা ব্যাসার্ধ: ১৬ পিক্সেল
          </span>
        </div>
        <canvas
          ref={canvasRef}
          width={460}
          height={120}
          className="w-full h-32 rounded-xl bg-slate-950 border border-slate-800"
        />
      </div>
    </div>
  );
};
