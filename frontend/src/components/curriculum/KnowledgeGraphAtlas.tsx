/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Curriculum Knowledge Graph Atlas Component
 * TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
 * FILE:      frontend/src/components/curriculum/KnowledgeGraphAtlas.tsx
 * PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
 * PURPOSE:   Renders an elegant cartographic academic topic map (Oxford Navy nodes
 *            on Warm Ivory parchment) with zoom/pan SVG canvas, prerequisite relationship
 *            lines, mastery ring badges, and interactive topic inspection.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState, useRef, useMemo } from 'react';
import {
  Compass,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  BookOpen,
  Layers,
  Filter,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Search,
  ChevronRight
} from 'lucide-react';
import { RemedialPathDrawer } from './RemedialPathDrawer';

export interface AtlasTopicNode {
  topic_id: string;
  title_bn: string;
  title_en: string;
  subject: string;
  class_grade: number;
  domain: string;
  core_formulas: string[];
  mastery_score: number;
  mastery_band: 'MASTERED' | 'IN_PROGRESS' | 'GAP';
  x: number;
  y: number;
}

export interface AtlasPrerequisiteEdge {
  source: string;
  target: string;
}

export interface KnowledgeGraphAtlasProps {
  nodes?: AtlasTopicNode[];
  edges?: AtlasPrerequisiteEdge[];
  onSelectTopic?: (topicId: string) => void;
}

const DEFAULT_NODES: AtlasTopicNode[] = [
  {
    topic_id: 'math-cl6-fractions',
    title_bn: 'ভগ্নাংশ ও মৌলিক পাটিগণিত',
    title_en: 'Fractions and Elementary Arithmetic',
    subject: 'সাধারণ গণিত',
    class_grade: 6,
    domain: 'পাটিগণিত',
    core_formulas: ['\\frac{a}{b} \\pm \\frac{c}{d}'],
    mastery_score: 95,
    mastery_band: 'MASTERED',
    x: 80,
    y: 120,
  },
  {
    topic_id: 'math-cl8-algebraic-identities',
    title_bn: 'বীজগণিতীয় সূত্রাবলী ও প্রয়োগ',
    title_en: 'Algebraic Formulae and Identities',
    subject: 'সাধারণ গণিত',
    class_grade: 8,
    domain: 'বীজগণিত',
    core_formulas: ['(a+b)^2 = a^2 + 2ab + b^2'],
    mastery_score: 88,
    mastery_band: 'MASTERED',
    x: 280,
    y: 120,
  },
  {
    topic_id: 'math-cl9-trigonometric-ratios',
    title_bn: 'ত্রিকোণমিতিক অনুপাত ও অভেদ',
    title_en: 'Trigonometric Ratios and Basic Identities',
    subject: 'উচ্চতর গণিত',
    class_grade: 9,
    domain: 'ত্রিকোণমিতি',
    core_formulas: ['\\sin^2\\theta + \\cos^2\\theta = 1'],
    mastery_score: 65,
    mastery_band: 'IN_PROGRESS',
    x: 500,
    y: 90,
  },
  {
    topic_id: 'math-cl10-coordinate-geometry',
    title_bn: 'স্থানাঙ্ক জ্যামিতি ও সরলরেখা',
    title_en: 'Coordinate Geometry and Slope of Lines',
    subject: 'উচ্চতর গণিত',
    class_grade: 10,
    domain: 'জ্যামিতি',
    core_formulas: ['m = \\frac{y_2 - y_1}{x_2 - x_1}'],
    mastery_score: 72,
    mastery_band: 'IN_PROGRESS',
    x: 500,
    y: 200,
  },
  {
    topic_id: 'math-hsc-functions-limits',
    title_bn: 'ফাংশন ও সীমার প্রাথমিক ধারণা',
    title_en: 'Functions and Intuition of Limits',
    subject: 'উচ্চতর গণিত ১ম পত্র',
    class_grade: 11,
    domain: 'ক্যালকুলাস',
    core_formulas: ['\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1'],
    mastery_score: 45,
    mastery_band: 'GAP',
    x: 740,
    y: 140,
  },
  {
    topic_id: 'math-hsc-differentiation',
    title_bn: 'অন্তরীকরণ ও পরিবর্তনের হার',
    title_en: 'Differentiation and Instantaneous Rates',
    subject: 'উচ্চতর গণিত ১ম পত্র',
    class_grade: 11,
    domain: 'ক্যালকুলাস',
    core_formulas: ['f\'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}'],
    mastery_score: 40,
    mastery_band: 'GAP',
    x: 980,
    y: 140,
  },
  {
    topic_id: 'phys-cl9-kinematics-motion',
    title_bn: 'একমাত্রিক গতির সমীকরণ',
    title_en: 'Kinematics and 1D Equations of Motion',
    subject: 'পদার্থবিজ্ঞান',
    class_grade: 9,
    domain: 'বলবিদ্যা',
    core_formulas: ['v = u + at', 's = ut + \\frac{1}{2}at^2'],
    mastery_score: 82,
    mastery_band: 'MASTERED',
    x: 500,
    y: 330,
  },
  {
    topic_id: 'phys-hsc-vectors-motion',
    title_bn: 'ভেক্টর রাশি ও প্রাস গতি',
    title_en: 'Vectors and Projectile Motion',
    subject: 'পদার্থবিজ্ঞান ১ম পত্র',
    class_grade: 11,
    domain: 'বলবিদ্যা',
    core_formulas: ['H = \\frac{v_0^2 \\sin^2\\theta}{2g}'],
    mastery_score: 55,
    mastery_band: 'IN_PROGRESS',
    x: 740,
    y: 330,
  },
  {
    topic_id: 'phys-hsc-newtonian-mechanics',
    title_bn: 'নিউটনীয় বলবিদ্যা ও টর্ক',
    title_en: 'Newtonian Mechanics and Torque',
    subject: 'পদার্থবিজ্ঞান ১ম পত্র',
    class_grade: 11,
    domain: 'বলবিদ্যা',
    core_formulas: ['\\tau = I\\alpha', 'L = I\\omega'],
    mastery_score: 42,
    mastery_band: 'GAP',
    x: 980,
    y: 280,
  },
];

const DEFAULT_EDGES: AtlasPrerequisiteEdge[] = [
  { source: 'math-cl6-fractions', target: 'math-cl8-algebraic-identities' },
  { source: 'math-cl8-algebraic-identities', target: 'math-cl9-trigonometric-ratios' },
  { source: 'math-cl8-algebraic-identities', target: 'math-cl10-coordinate-geometry' },
  { source: 'math-cl9-trigonometric-ratios', target: 'math-hsc-functions-limits' },
  { source: 'math-cl10-coordinate-geometry', target: 'math-hsc-functions-limits' },
  { source: 'math-hsc-functions-limits', target: 'math-hsc-differentiation' },
  { source: 'math-cl8-algebraic-identities', target: 'phys-cl9-kinematics-motion' },
  { source: 'phys-cl9-kinematics-motion', target: 'phys-hsc-vectors-motion' },
  { source: 'math-cl9-trigonometric-ratios', target: 'phys-hsc-vectors-motion' },
  { source: 'phys-hsc-vectors-motion', target: 'phys-hsc-newtonian-mechanics' },
  { source: 'math-hsc-differentiation', target: 'phys-hsc-newtonian-mechanics' },
];

export const KnowledgeGraphAtlas: React.FC<KnowledgeGraphAtlasProps> = ({
  nodes = DEFAULT_NODES,
  edges = DEFAULT_EDGES,
  onSelectTopic,
}) => {
  const [selectedSubject, setSelectedSubject] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const [selectedTopicId, setSelectedTopicId] = useState<string | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState<boolean>(false);

  // Filter nodes
  const filteredNodes = useMemo(() => {
    return nodes.filter((node) => {
      const matchesSubject =
        selectedSubject === 'ALL' ||
        (selectedSubject === 'MATH' && (node.subject.includes('গণিত') || node.subject.includes('Math'))) ||
        (selectedSubject === 'PHYSICS' && node.subject.includes('পদার্থবিজ্ঞান'));
      const matchesSearch =
        node.title_bn.toLowerCase().includes(searchQuery.toLowerCase()) ||
        node.title_en.toLowerCase().includes(searchQuery.toLowerCase()) ||
        node.domain.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesSubject && matchesSearch;
    });
  }, [nodes, selectedSubject, searchQuery]);

  const activeNodeMap = useMemo(() => {
    return new Map(filteredNodes.map((n) => [n.topic_id, n]));
  }, [filteredNodes]);

  const filteredEdges = useMemo(() => {
    return edges.filter(
      (e) => activeNodeMap.has(e.source) && activeNodeMap.has(e.target)
    );
  }, [edges, activeNodeMap]);

  const handleNodeClick = (node: AtlasTopicNode) => {
    setSelectedTopicId(node.topic_id);
    setIsDrawerOpen(true);
    if (onSelectTopic) {
      onSelectTopic(node.topic_id);
    }
  };

  const getMasteryColor = (band: AtlasTopicNode['mastery_band']) => {
    switch (band) {
      case 'MASTERED':
        return {
          stroke: '#059669', // Emerald
          fill: '#ECFDF5',
          text: 'text-emerald-800',
          badge: 'bg-emerald-50 text-emerald-800 border-emerald-200',
        };
      case 'IN_PROGRESS':
        return {
          stroke: '#D97706', // Amber
          fill: '#FFFBEB',
          text: 'text-amber-800',
          badge: 'bg-amber-50 text-amber-800 border-amber-200',
        };
      case 'GAP':
        return {
          stroke: '#E11D48', // Rose / Red
          fill: '#FFF1F2',
          text: 'text-rose-800',
          badge: 'bg-rose-50 text-rose-800 border-rose-200',
        };
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0A2540] font-sans pb-16">
      {/* Top Academic Atlas Header */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 px-4 sm:px-8 py-4 shadow-xs">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-xs">
              <Compass className="w-5 h-5 stroke-[1.75]" />
            </div>
            <div>
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <span>জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB)</span>
                <span className="text-slate-300">•</span>
                <span>জ্ঞান মানচিত্র মানচিত্রক</span>
              </div>
              <h1 className="text-lg sm:text-xl font-bold text-[#0A2540] tracking-tight">
                পাঠ্যক্রম জ্ঞান অ্যাটলাস ও গতিশীল প্রতিকারমূলক পথনির্দেশক
              </h1>
            </div>
          </div>

          {/* Controls: Subject Tabs & Zoom */}
          <div className="flex items-center gap-3 flex-wrap">
            {/* Subject Filters */}
            <div className="flex items-center gap-1 p-1 bg-[#FAFAF8] border border-slate-200 rounded-2xl text-xs font-semibold">
              <button
                onClick={() => setSelectedSubject('ALL')}
                className={`px-3 py-1.5 rounded-xl transition-all ${
                  selectedSubject === 'ALL'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                সকল বিষয়
              </button>
              <button
                onClick={() => setSelectedSubject('MATH')}
                className={`px-3 py-1.5 rounded-xl transition-all ${
                  selectedSubject === 'MATH'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                উচ্চতর গণিত
              </button>
              <button
                onClick={() => setSelectedSubject('PHYSICS')}
                className={`px-3 py-1.5 rounded-xl transition-all ${
                  selectedSubject === 'PHYSICS'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                পদার্থবিজ্ঞান
              </button>
            </div>

            {/* Zoom Controls */}
            <div className="flex items-center gap-1 p-1 bg-white border border-slate-200 rounded-xl shadow-xs">
              <button
                onClick={() => setZoomLevel((z) => Math.min(1.5, z + 0.1))}
                className="p-1.5 text-slate-600 hover:text-[#0A2540] rounded-lg"
                title="বড় করুন"
                aria-label="বড় করুন"
              >
                <ZoomIn className="w-4 h-4" />
              </button>
              <button
                onClick={() => setZoomLevel((z) => Math.max(0.7, z - 0.1))}
                className="p-1.5 text-slate-600 hover:text-[#0A2540] rounded-lg"
                title="ছোট করুন"
                aria-label="ছোট করুন"
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              <button
                onClick={() => setZoomLevel(1)}
                className="p-1.5 text-slate-600 hover:text-[#0A2540] rounded-lg"
                title="রিসেট"
                aria-label="রিসেট"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Canvas Workspace */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 space-y-6">
        {/* Search & Legend Bar */}
        <div className="bg-white border border-slate-200 rounded-3xl p-4 shadow-xs flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="টপিক বা অধ্যায়ের নাম দিয়ে অনুসন্ধান..."
              className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs text-slate-800 focus:outline-hidden focus:border-[#0A2540]"
            />
          </div>

          {/* Academic Legend */}
          <div className="flex items-center gap-4 text-xs font-semibold text-slate-600 flex-wrap">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-emerald-500 border border-emerald-600 inline-block" />
              <span>দক্ষতা অর্জিত (≥৮০%)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-amber-500 border border-amber-600 inline-block" />
              <span>চলমান অগ্রগতি (৫০-৭৯%)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-rose-500 border border-rose-600 inline-block" />
              <span>ঘাটতি চিহ্নিত (&lt;৫০%)</span>
            </div>
            <div className="flex items-center gap-1 text-slate-400">
              <ArrowRight className="w-3 h-3" />
              <span>পূর্বশর্ত সংযোগ</span>
            </div>
          </div>
        </div>

        {/* Parchment Map Canvas Box */}
        <div className="relative bg-[#FAFAF8] border border-slate-200/90 rounded-3xl shadow-sm overflow-hidden min-h-[580px] p-6">
          {/* Subtle cartographic grid lines */}
          <div className="absolute inset-0 bg-[radial-gradient(#CBD5E1_1px,transparent_1px)] [background-size:24px_24px] opacity-40 pointer-events-none" />

          {/* SVG Canvas Container */}
          <div
            className="w-full h-full overflow-auto transition-transform origin-top-left"
            style={{ transform: `scale(${zoomLevel})` }}
          >
            <svg
              className="w-[1140px] h-[520px] select-none"
              viewBox="0 0 1140 520"
              xmlns="http://www.w3.org/2000/svg"
            >
              <defs>
                {/* Clean Academic Arrowhead */}
                <marker
                  id="academic-arrow"
                  viewBox="0 0 10 10"
                  refX="18"
                  refY="5"
                  markerWidth="6"
                  markerHeight="6"
                  orient="auto-start-reverse"
                >
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#94A3B8" />
                </marker>
              </defs>

              {/* Prerequisite Edges (Crisp Hairline Lines) */}
              {filteredEdges.map((edge, idx) => {
                const src = activeNodeMap.get(edge.source);
                const tgt = activeNodeMap.get(edge.target);
                if (!src || !tgt) return null;

                // Bezier curve connector
                const dx = tgt.x - src.x;
                const dy = tgt.y - src.y;
                const pathD = `M ${src.x + 80} ${src.y + 25} C ${src.x + dx / 2} ${src.y + 25}, ${tgt.x - dx / 2} ${tgt.y + 25}, ${tgt.x} ${tgt.y + 25}`;

                return (
                  <path
                    key={`edge-${idx}`}
                    d={pathD}
                    fill="none"
                    stroke="#CBD5E1"
                    strokeWidth="1.75"
                    strokeDasharray="4 2"
                    markerEnd="url(#academic-arrow)"
                    className="transition-all hover:stroke-[#0A2540] hover:stroke-width-2"
                  />
                );
              })}

              {/* Topic Nodes */}
              {filteredNodes.map((node) => {
                const color = getMasteryColor(node.mastery_band);
                const isSelected = selectedTopicId === node.topic_id;

                return (
                  <g
                    key={node.topic_id}
                    transform={`translate(${node.x}, ${node.y})`}
                    onClick={() => handleNodeClick(node)}
                    className="cursor-pointer group"
                  >
                    {/* Outer Drop Shadow Rectangle */}
                    <rect
                      x="0"
                      y="0"
                      width="160"
                      height="54"
                      rx="14"
                      fill="#FFFFFF"
                      stroke={isSelected ? '#0A2540' : color.stroke}
                      strokeWidth={isSelected ? '2.5' : '1.75'}
                      className="filter drop-shadow-xs transition-all group-hover:drop-shadow-md"
                    />

                    {/* Mastery Ring Indicator Badge */}
                    <circle
                      cx="20"
                      cy="27"
                      r="12"
                      fill={color.fill}
                      stroke={color.stroke}
                      strokeWidth="2"
                    />
                    <text
                      x="20"
                      y="31"
                      textAnchor="middle"
                      fontSize="9"
                      fontWeight="bold"
                      fill={color.stroke}
                    >
                      {node.mastery_score}%
                    </text>

                    {/* Title Text (Bengali) */}
                    <text
                      x="40"
                      y="23"
                      fontSize="11"
                      fontWeight="bold"
                      fill="#0A2540"
                      className="group-hover:fill-[#0c2f52]"
                    >
                      {node.title_bn.length > 14
                        ? `${node.title_bn.slice(0, 13)}...`
                        : node.title_bn}
                    </text>

                    {/* Class & Domain Subtitle */}
                    <text
                      x="40"
                      y="38"
                      fontSize="9"
                      fontWeight="500"
                      fill="#64748B"
                    >
                      শ্রেণি {node.class_grade} • {node.domain}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      </main>

      {/* Slide-over Remedial Path Drawer */}
      <RemedialPathDrawer
        isOpen={isDrawerOpen}
        topicId={selectedTopicId || 'math-hsc-differentiation'}
        onClose={() => setIsDrawerOpen(false)}
      />
    </div>
  );
};
