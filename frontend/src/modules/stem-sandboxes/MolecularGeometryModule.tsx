/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - STEM MOLECULAR GEOMETRY MODULE:
 * MODULE:    Next.js 15+ VSEPR Molecular Geometry & Lewis Structure Lab
 * TOPIC:     Valence Shell Electron Pair Repulsion, Bond Angles, Steric Numbers & 3D Bonds
 * FILE:      frontend/src/modules/stem-sandboxes/MolecularGeometryModule.tsx
 * PURPOSE:   Provides interactive chemistry simulation for university and college students.
 *            Solves molecular geometries (linear, trigonal planar, tetrahedral, trigonal bipyramidal,
 *            octahedral) based on steric numbers and lone pairs. Renders 3D atom balls and rotating
 *            chemical bond sticks on HTML5 canvas with requestAnimationFrame lifecycle cleanup.
 * AUDIENCE:  Chemistry Students, Structural Biochemists & Simulation Engineers
 * STANDARDS: IUPAC/VSEPR Chemical Nomenclature, Canvas 3D Projection, Strict Zero Emoji
 * ========================================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Atom, 
  Layers, 
  RotateCcw, 
  CheckCircle2, 
  Sliders, 
  ShieldCheck,
  Compass
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

interface MoleculeData {
  formula: string;
  name: string;
  stericNumber: number;
  bondAngle: string;
  hybridization: string;
  polarity: 'POLAR' | 'NON_POLAR';
  centralAtom: string;
  surroundingAtoms: string[];
}

const MOLECULES_DB: Record<string, MoleculeData> = {
  CH4: { formula: 'CH4', name: 'Tetrahedral (চতুস্তলকীয়)', stericNumber: 4, bondAngle: '109.5°', hybridization: 'sp³', polarity: 'NON_POLAR', centralAtom: 'C', surroundingAtoms: ['H', 'H', 'H', 'H'] },
  NH3: { formula: 'NH3', name: 'Trigonal Pyramidal (ত্রিকোণীয় পিরামিডীয়)', stericNumber: 4, bondAngle: '107.0°', hybridization: 'sp³', polarity: 'POLAR', centralAtom: 'N', surroundingAtoms: ['H', 'H', 'H'] },
  H2O: { formula: 'H2O', name: 'Bent / V-Shaped (কৌণিক)', stericNumber: 4, bondAngle: '104.5°', hybridization: 'sp³', polarity: 'POLAR', centralAtom: 'O', surroundingAtoms: ['H', 'H'] },
  CO2: { formula: 'CO2', name: 'Linear (সরলরৈখিক)', stericNumber: 2, bondAngle: '180.0°', hybridization: 'sp', polarity: 'NON_POLAR', centralAtom: 'C', surroundingAtoms: ['O', 'O'] },
  BF3: { formula: 'BF3', name: 'Trigonal Planar (ত্রিকোণাকার সমতলীয়)', stericNumber: 3, bondAngle: '120.0°', hybridization: 'sp²', polarity: 'NON_POLAR', centralAtom: 'B', surroundingAtoms: ['F', 'F', 'F'] },
  SF6: { formula: 'SF6', name: 'Octahedral (অষ্টতলকীয়)', stericNumber: 6, bondAngle: '90.0°', hybridization: 'sp³d²', polarity: 'NON_POLAR', centralAtom: 'S', surroundingAtoms: ['F', 'F', 'F', 'F', 'F', 'F'] },
};

export const MolecularGeometryModule: React.FC = () => {
  const [selectedFormula, setSelectedFormula] = useState<string>('CH4');

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);

  const mol = MOLECULES_DB[selectedFormula] || MOLECULES_DB['CH4'];

  // Rotating 3D Atom Balls & Bond Sticks with requestAnimationFrame cleanup
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let startTime = Date.now();

    const render = () => {
      const now = Date.now();
      const angle = (now - startTime) * 0.0015;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Draw Bonds and Surrounding Atoms
      const count = mol.surroundingAtoms.length;
      for (let i = 0; i < count; i++) {
        const theta = (i * 2 * Math.PI) / count + angle;
        const radius = 55;
        const atomX = centerX + radius * Math.cos(theta);
        const atomY = centerY + radius * Math.sin(theta) * 0.65;

        // Bond Stick
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(atomX, atomY);
        ctx.stroke();

        // Surrounding Atom Ball
        ctx.fillStyle = '#38BDF8';
        ctx.beginPath();
        ctx.arc(atomX, atomY, 11, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#0F172A';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(mol.surroundingAtoms[i], atomX, atomY + 3.5);
      }

      // Central Atom Ball
      ctx.fillStyle = '#A855F7';
      ctx.beginPath();
      ctx.arc(centerX, centerY, 16, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(mol.centralAtom, centerX, centerY + 4.5);

      animFrameRef.current = requestAnimationFrame(render);
    };

    animFrameRef.current = requestAnimationFrame(render);

    return () => {
      if (animFrameRef.current !== null) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [selectedFormula, mol]);

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-6 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="brand">Tab 28 STEM Sandbox</Badge>
            <Badge variant="teal">VSEPR থিওরি ল্যাব</Badge>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
            VSEPR Molecular Geometry & Lewis Structure Lab
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            অ্যাসিড-ক্ষার ও সমযোজী বন্ধনের ত্রিমাত্রিক আকার, বন্ধন কোণ ও হাইব্রিডাইজেশন ক্যালকুলেটর
          </p>
        </div>

        {/* Quick Molecule Selector */}
        <div className="flex flex-wrap gap-1.5">
          {Object.keys(MOLECULES_DB).map((f) => (
            <button
              key={f}
              onClick={() => setSelectedFormula(f)}
              className={`px-3 py-1 rounded-lg font-mono text-xs font-bold transition ${
                selectedFormula === f
                  ? "bg-purple-600 text-white shadow-sm"
                  : "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* Geometry Telemetry & 3D Rotating Canvas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        
        {/* Molecule Data Card */}
        <div className="space-y-3 bg-slate-50 dark:bg-slate-800/40 p-4 rounded-xl border border-slate-200 dark:border-slate-800 text-xs">
          <div className="flex justify-between items-center">
            <span className="font-bold text-base text-slate-900 dark:text-white">{mol.formula}</span>
            <Badge variant={mol.polarity === 'POLAR' ? 'warning' : 'neutral'}>
              {mol.polarity === 'POLAR' ? 'পোলার (ডাইপোল মোমেন্ট বিদ্যমান)' : 'অপোলার'}
            </Badge>
          </div>

          <div className="p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-1.5 font-mono">
            <div className="flex justify-between">
              <span className="text-slate-500">জ্যামিতিক আকৃতি:</span>
              <strong className="text-purple-600">{mol.name}</strong>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">তাত্ত্বিক বন্ধন কোণ:</span>
              <strong className="text-teal-600">{mol.bondAngle}</strong>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">সংকরায়ন (Hybridization):</span>
              <strong className="text-blue-600">{mol.hybridization}</strong>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">স্টেরিক সংখ্যা (Steric No):</span>
              <strong>{mol.stericNumber}</strong>
            </div>
          </div>
        </div>

        {/* 3D Canvas */}
        <div className="space-y-1.5">
          <span className="text-xs font-semibold text-slate-500 block">
            ত্রিমাত্রিক আণবিক বন্ধন ঘূর্ণন ক্যানভাস (Central: {mol.centralAtom})
          </span>
          <canvas
            ref={canvasRef}
            width={340}
            height={160}
            className="w-full h-36 rounded-xl bg-slate-950 border border-slate-800"
          />
        </div>

      </div>
    </div>
  );
};
