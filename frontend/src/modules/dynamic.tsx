/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - DYNAMIC MODULE SPLITTING:
 * MODULE:    Next.js 15+ Dynamic Code Splitting & Lazy Module Loader (`next/dynamic`)
 * TOPIC:     On-Demand Module Chunking, SSR: false Isolation & Gzip Bundle < 150KB
 * FILE:      frontend/src/modules/dynamic.tsx
 * PURPOSE:   Dynamically splits heavy HTML5 Canvas, WebRTC, and Audio modules into separate
 *            client-side chunks. Keeps the initial main JavaScript bundle under 150KB gzip.
 *            Components are only loaded when selected in the dual-perspective directory or deep-linked.
 *            Provides seamless skeleton fallbacks to guarantee zero cumulative layout shift (CLS < 0.1).
 * AUDIENCE:  Web Performance Engineers, Core Web Vitals Auditors & Frontend Developers
 * STANDARDS: Next.js 15 dynamic(), React.lazy, Zero Layout Shift (CLS < 0.1), Strict Zero Emoji
 * ========================================================================================
 */

import React from 'react';
import dynamic from 'next/dynamic';

const ModuleLoadingFallback: React.FC = () => (
  <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-4 animate-pulse min-h-[300px] flex flex-col justify-center">
    <div className="flex justify-between items-center pb-3 border-b border-slate-100 dark:border-slate-800">
      <div className="h-6 w-48 bg-slate-200 dark:bg-slate-800 rounded-md" />
      <div className="h-6 w-24 bg-slate-200 dark:bg-slate-800 rounded-md" />
    </div>
    <div className="h-4 w-3/4 bg-slate-200 dark:bg-slate-800 rounded-md" />
    <div className="h-32 w-full bg-slate-100 dark:bg-slate-850 rounded-xl" />
    <div className="flex justify-end gap-2 pt-2">
      <div className="h-8 w-28 bg-slate-200 dark:bg-slate-800 rounded-lg" />
    </div>
  </div>
);

// Group 1: Academic & Cognitive
export const DynamicBionicReader = dynamic(
  () => import('./academic/BionicReaderModule').then((mod) => mod.BionicReaderModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicAdmissionMatrix = dynamic(
  () => import('./academic/AdmissionMatrixModule').then((mod) => mod.AdmissionMatrixModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicSpeechDialect = dynamic(
  () => import('./academic/SpeechDialectModule').then((mod) => mod.SpeechDialectModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

// Group 2: Resilience & Decentralized Networks
export const DynamicSatelliteLora = dynamic(
  () => import('./resilience/SatelliteLoraModule').then((mod) => mod.SatelliteLoraModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicOfflineMesh = dynamic(
  () => import('./resilience/OfflineMeshModule').then((mod) => mod.OfflineMeshModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicWebTorrentCdn = dynamic(
  () => import('./resilience/WebTorrentCdnModule').then((mod) => mod.WebTorrentCdnModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

// Group 3: STEM Sandboxes
export const DynamicQuantumSandbox = dynamic(
  () => import('./stem-sandboxes/QuantumSandboxModule').then((mod) => mod.QuantumSandboxModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicBciTelemetry = dynamic(
  () => import('./stem-sandboxes/BciTelemetryModule').then((mod) => mod.BciTelemetryModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicMolecularGeometry = dynamic(
  () => import('./stem-sandboxes/MolecularGeometryModule').then((mod) => mod.MolecularGeometryModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicCfdFluidSimulator = dynamic(
  () => import('./stem-sandboxes/CfdFluidSimulatorModule').then((mod) => mod.CfdFluidSimulatorModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

// Group 4: Enterprise Cockpit & Security
export const DynamicSupabaseCockpit = dynamic(
  () => import('./enterprise-cockpit/SupabaseCockpitModule').then((mod) => mod.SupabaseCockpitModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicShamirVault = dynamic(
  () => import('./enterprise-cockpit/ShamirVaultModule').then((mod) => mod.ShamirVaultModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DynamicCampusRaftBft = dynamic(
  () => import('./enterprise-cockpit/CampusRaftBftModule').then((mod) => mod.CampusRaftBftModule),
  { ssr: false, loading: () => <ModuleLoadingFallback /> }
);

export const DYNAMIC_MODULE_MAP: Record<string, React.ComponentType<any>> = {
  'bionic-reader': DynamicBionicReader,
  'admission-matrix': DynamicAdmissionMatrix,
  'speech-dialect-studio': DynamicSpeechDialect,
  'satellite-lora': DynamicSatelliteLora,
  'offline-mesh': DynamicOfflineMesh,
  'cdn-swarm': DynamicWebTorrentCdn,
  'quantum-sandbox': DynamicQuantumSandbox,
  'bci-telemetry': DynamicBciTelemetry,
  'molecular-geometry': DynamicMolecularGeometry,
  'cfd-fluid-simulator': DynamicCfdFluidSimulator,
  'supabase-cockpit': DynamicSupabaseCockpit,
  'shamir-vault': DynamicShamirVault,
  'campus-raft-bft': DynamicCampusRaftBft,
};
