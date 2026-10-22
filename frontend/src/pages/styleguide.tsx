/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Design System Internal Style Guide & Component Gallery
 * TOPIC:     Modern Academic Editorial Component Gallery & Specification
 * FILE:      frontend/src/pages/styleguide.tsx
 * PURPOSE:   Visual verification and living specification for:
 *            - Color tokens (Paper grounds, ink levels, primary ink-blue, accent gold, flat semantics)
 *            - Modular typography scale (~1.250) in Bengali & English
 *            - Bengali conjunct ligature rendering (যুক্তাক্ষর) across font sizes with matra safety
 *            - Comprehensive Component Gallery: Button, Card, Badge, Input, Select, Checkbox,
 *              Radio, Textarea, Tabs, Accordion, Breadcrumb, Pagination, Drawer, Modal, Tooltip,
 *              Table, Skeleton, EmptyState, QuizProgress, OptionCard, ExplanationBlock, ResultSummary.
 * STANDARDS: Zero-Emoji, Zero-Neon, WCAG 2.2 AAA Contrast, Academic Monograph Style
 */

import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import {
  BookOpen,
  CheckCircle,
  AlertTriangle,
  AlertCircle,
  ArrowRight,
  ShieldCheck,
  Layers,
  Type,
  Palette,
  Maximize2,
  Copy,
  Check,
  ExternalLink,
  Search,
  Sparkles,
  FileQuestion,
  HelpCircle,
  Sliders,
  ChevronRight,
  Send,
  Eye,
  Info,
} from 'lucide-react';

import {
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardMeta,
  CardDescription,
  CardContent,
  CardFooter,
  Badge,
  DifficultyBadge,
  VerifiedBadge,
  RoleChip,
  Input,
  Select,
  Checkbox,
  Radio,
  RadioGroup,
  Textarea,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
  Breadcrumb,
  Pagination,
  Drawer,
  Tooltip,
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  Skeleton,
  CardSkeleton,
  EmptyState,
  Modal,
} from '@/components/ui';

import {
  KaTeXRenderer,
  OptionCard,
  QuizProgress,
  QuizResultSummary,
  ExplanationBlock,
} from '@/components/quiz';

interface SwatchProps {
  name: string;
  variable: string;
  hex: string;
  bgClass?: string;
  textDark?: boolean;
  contrastRatio?: string;
  wcag?: string;
  roleDescription: string;
}

function Swatch({
  name,
  variable,
  hex,
  textDark = false,
  contrastRatio,
  wcag,
  roleDescription,
}: SwatchProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(hex);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col border border-[var(--color-border-hairline)] rounded-[8px] overflow-hidden bg-white shadow-[var(--shadow-paper)]">
      <div
        className="h-20 w-full flex items-end justify-end p-2 relative transition-all"
        style={{ backgroundColor: hex }}
      >
        <button
          onClick={handleCopy}
          className="p-1.5 rounded bg-black/60 hover:bg-black/80 text-white transition text-xs flex items-center gap-1"
          title="কপি করুন"
          aria-label={`${name} হেক্স কোড কপি করুন`}
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Copy className="w-3.5 h-3.5" />}
        </button>
      </div>
      <div className="p-3 bg-white flex flex-col gap-1 text-xs">
        <div className="flex items-center justify-between font-semibold text-[var(--color-ink-primary)]">
          <span>{name}</span>
          <span className="font-mono text-[11px] text-[var(--color-ink-muted)]">{hex}</span>
        </div>
        <div className="font-mono text-[10px] text-[var(--color-ink-faint)] truncate" title={variable}>
          {variable}
        </div>
        <div className="text-[11px] text-[var(--color-ink-muted)] mt-1">{roleDescription}</div>
        {contrastRatio && (
          <div className="mt-2 pt-2 border-t border-[var(--color-border-subtle)] flex items-center justify-between text-[11px]">
            <span className="text-[var(--color-ink-faint)]">Contrast:</span>
            <span className="font-semibold text-emerald-800 bg-emerald-50 px-1.5 py-0.5 rounded">
              {contrastRatio} ({wcag})
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

export default function StyleGuidePage() {
  const [activeTab, setActiveTab] = useState<'all' | 'colors' | 'typography' | 'components' | 'quiz'>('all');
  const [isBengali, setIsBengali] = useState(true);
  const [buttonLoading, setButtonLoading] = useState(false);
  const [showFormErrors, setShowFormErrors] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedRadio, setSelectedRadio] = useState('physics');
  const [checkboxChecked, setCheckboxChecked] = useState(true);
  const [currentPage, setCurrentPage] = useState(3);
  const [selectedOption, setSelectedOption] = useState<string | null>('B');

  const conjuncts = [
    { glyph: 'ক্ষ', name: 'ক + ষ', example: 'শিক্ষা, পরীক্ষা, ক্ষমার্হ' },
    { glyph: 'জ্ঞ', name: 'জ + ঞ', example: 'জ্ঞান, প্রজ্ঞা, অজ্ঞাত' },
    { glyph: 'হ্ণ', name: 'হ + ণ', example: 'অপরাহ্ণ, পূর্বাহ্ণ' },
    { glyph: 'শ্রূ', name: 'শ + র + ঊ', example: 'শ্রূয়মাণ, শুশ্রূষা' },
    { glyph: 'ঙ্ক', name: 'ঙ + ক', example: 'অঙ্ক, অঙ্কন, শঙ্কা' },
    { glyph: 'ক্ট', name: 'ক + ট', example: 'ডক্টর, অক্টোবর' },
    { glyph: 'দ্ধ', name: 'দ + ধ', example: 'শুদ্ধ, বৌদ্ধ, সমৃদ্ধ' },
    { glyph: 'স্থ', name: 'স + থ', example: 'স্থান, স্বাস্থ্য, উপস্থিত' },
    { glyph: 'ব্দ', name: 'ব + দ', example: 'শব্দ, শতাব্দী, অব্দ' },
    { glyph: 'ক্র', name: 'ক + র-ফলা', example: 'ক্রমাগত, প্রক্রিয়া' },
    { glyph: 'ট্র', name: 'ট + র-ফলা', example: 'ট্র্যাক, মেট্রো, ট্রেন' },
    { glyph: 'ণ্ড', name: 'ণ + ড', example: 'কাণ্ড, পণ্ডিত, দণ্ড' },
    { glyph: 'ঞ্জ', name: 'ঞ + জ', example: 'পুঞ্জ, রঞ্জন, গঞ্জ' },
    { glyph: 'ষ্ণ', name: 'ষ + ণ', example: 'উষ্ণ, কৃষ্ণ, তৃষ্ণা' },
    { glyph: 'ত্থ', name: 'ত + থ', example: 'উত্থান, কথ্থক' },
    { glyph: 'দ্ম', name: 'দ + ম', example: 'পদ্ম, ছদ্মনাম' },
    { glyph: 'দ্ব', name: 'দ + ব', example: 'দ্বিতীয়, বিদ্বান, দ্বন্দ্ব' },
    { glyph: 'ধ্ব', name: 'ধ + ব', example: 'ধ্বনি, ধ্বংস, বিধ্বস্ত' },
  ];

  return (
    <div className="min-h-screen bg-[var(--color-paper-ground)] text-[var(--color-ink-primary)] selection:bg-[#1B2A4A] selection:text-white">
      <Head>
        <title>অগ্রযাত্রা কম্পোনেন্ট গ্যালারি ও ডিজাইন সিস্টেম (Style Guide) | Modern Academic Editorial</title>
        <meta name="description" content="অগ্রযাত্রা প্ল্যাটফর্মের প্রাতিষ্ঠানিক ডিজাইন সিস্টেম, কম্পোনেন্ট গ্যালারি ও টাইপোগ্রাফি নির্দেশিকা" />
      </Head>

      {/* Top Academic Bar */}
      <header className="border-b border-[var(--color-border-hairline)] bg-white sticky top-0 z-30 shadow-[var(--shadow-paper)]">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-[8px] bg-[#1B2A4A] text-white flex items-center justify-center font-serif text-lg font-semibold shadow-sm">
              অ
            </div>
            <div>
              <div className="font-serif text-base sm:text-lg font-semibold tracking-tight text-[#1B2A4A]">
                অগ্রযাত্রা ডিজাইন সিস্টেম ও কম্পোনেন্ট গ্যালারি
              </div>
              <div className="text-[11px] text-[var(--color-ink-muted)] uppercase tracking-wider font-sans">
                Modern Academic Editorial Standard
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setIsBengali(!isBengali)}
              className="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border border-[var(--color-border-hairline)] bg-[#FAF8F3] hover:bg-[#F5F2EB] text-[#1B2A4A] transition-colors"
            >
              <span>{isBengali ? "English View" : "বাংলা ভিউ"}</span>
            </button>

            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-ink-muted)] hover:text-[#1B2A4A] px-3 py-1.5 rounded-[6px] border border-[var(--color-border-hairline)] hover:bg-[var(--color-paper-surface-muted)] transition"
            >
              <span>{isBengali ? "ওয়েবসাইটে ফিরুন" : "Back to Site"}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-10 space-y-12">
        {/* Navigation Tabs */}
        <div className="flex items-center justify-between flex-wrap gap-4 border-b border-[var(--color-border-hairline)] pb-4">
          <div className="flex items-center gap-2 overflow-x-auto pb-1 max-w-full">
            {[
              { id: 'all', label: isBengali ? 'সম্পূর্ণ গ্যালারি' : 'All Sections' },
              { id: 'components', label: isBengali ? 'শেয়ার্ড কম্পোনেন্ট' : 'UI Components' },
              { id: 'quiz', label: isBengali ? 'কুইজ ও প্রশ্ন ইঞ্জিন' : 'Quiz & Math' },
              { id: 'colors', label: isBengali ? 'কালার টোকেন' : 'Color Tokens' },
              { id: 'typography', label: isBengali ? 'টাইপোগ্রাফি' : 'Typography' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-colors duration-150 whitespace-nowrap min-h-[40px] ${
                  activeTab === tab.id
                    ? 'bg-[#1B2A4A] text-white shadow-sm'
                    : 'bg-white border border-[var(--color-border-hairline)] text-[var(--color-ink-muted)] hover:text-[#1B2A4A] hover:bg-[#FAF8F3]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[#5B5B5B]">ইন্টারেকশন টেস্ট:</span>
            <button
              onClick={() => setButtonLoading(!buttonLoading)}
              className={`px-2.5 py-1 rounded text-xs border ${
                buttonLoading ? 'bg-amber-100 border-amber-300 text-amber-900 font-semibold' : 'bg-white border-slate-200 text-slate-700'
              }`}
            >
              Loading State {buttonLoading ? 'ON' : 'OFF'}
            </button>
            <button
              onClick={() => setShowFormErrors(!showFormErrors)}
              className={`px-2.5 py-1 rounded text-xs border ${
                showFormErrors ? 'bg-rose-100 border-rose-300 text-rose-900 font-semibold' : 'bg-white border-slate-200 text-slate-700'
              }`}
            >
              Form Errors {showFormErrors ? 'ON' : 'OFF'}
            </button>
          </div>
        </div>

        {/* SECTION: SHARED UI COMPONENTS GALLERY */}
        {(activeTab === 'all' || activeTab === 'components') && (
          <div className="space-y-12">
            {/* 1. BUTTONS */}
            <section className="space-y-5">
              <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
                <Layers className="w-5 h-5 text-[#1B2A4A]" />
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                  ১. বাটন সিস্টেম (Buttons)
                </h2>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Academic Button Variants & Interactive States</CardTitle>
                  <CardDescription>
                    Solid primary, outline secondary, text link, destructive, loading, and disabled states. Zero gradients, zero neon, guaranteed &gt;= 44px min-height.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Row 1: Main Variants */}
                  <div className="space-y-2">
                    <span className="text-xs font-semibold text-[#5B5B5B] uppercase tracking-wider block">
                      কোর ভেরিয়েন্টসমূহ (Core Variants)
                    </span>
                    <div className="flex flex-wrap items-center gap-3">
                      <Button variant="default" size="md" isLoading={buttonLoading}>
                        {isBengali ? "প্রাইমারি অ্যাকশন (Solid)" : "Primary Action"}
                      </Button>
                      <Button variant="paper" size="md" isLoading={buttonLoading}>
                        {isBengali ? "সেকেন্ডারি আউটলাইন (Outline)" : "Secondary Outline"}
                      </Button>
                      <Button variant="academic" size="md" isLoading={buttonLoading} icon={<CheckCircle className="w-4 h-4" />}>
                        {isBengali ? "একাডেমিক এমারেল্ড (Mastery)" : "Academic Mastery"}
                      </Button>
                      <Button variant="destructive" size="md" isLoading={buttonLoading} icon={<AlertTriangle className="w-4 h-4" />}>
                        {isBengali ? "নেগেটিভ মার্ক / ডিলিট" : "Destructive Action"}
                      </Button>
                      <Button variant="ghost" size="md">
                        {isBengali ? "ঘোস্ট বাটন" : "Ghost Button"}
                      </Button>
                      <Button variant="link" size="md">
                        {isBengali ? "টেক্সট লিঙ্ক বাটন →" : "Text Link Button →"}
                      </Button>
                    </div>
                  </div>

                  {/* Row 2: Sizes & States */}
                  <div className="space-y-2 pt-2 border-t border-[var(--color-border-subtle)]">
                    <span className="text-xs font-semibold text-[#5B5B5B] uppercase tracking-wider block">
                      সাইজ ও বিশেষ স্টেট (Sizes & Disabled State)
                    </span>
                    <div className="flex flex-wrap items-center gap-3">
                      <Button variant="default" size="sm">
                        Small (36px)
                      </Button>
                      <Button variant="default" size="md">
                        Standard (44px)
                      </Button>
                      <Button variant="default" size="lg">
                        Large (48px)
                      </Button>
                      <Button variant="default" size="md" disabled>
                        {isBengali ? "নিষ্ক্রিয় বাটন (Disabled)" : "Disabled State"}
                      </Button>
                      <Button variant="paper" size="md" disabled>
                        {isBengali ? "নিষ্ক্রিয় আউটলাইন" : "Disabled Outline"}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* 2. CARDS */}
            <section className="space-y-5">
              <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
                <Layers className="w-5 h-5 text-[#1B2A4A]" />
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                  ২. পেপার কার্ড সিস্টেম (Cards)
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                  <CardHeader>
                    <CardMeta>
                      <Badge variant="brand" size="sm">HSC ২০২৬</Badge>
                      <span>অধ্যায়ভিত্তিক পাঠ্যক্রম</span>
                    </CardMeta>
                    <CardTitle>পদার্থবিজ্ঞান ১ম পত্র: গতিবিদ্যা</CardTitle>
                    <CardDescription>
                      প্রক্ষেপকের পাল্লা, সর্বোচ্চ উচ্চতা এবং প্রাস সংক্রান্ত বোর্ড পরীক্ষার বিগত ১০ বছরের সৃজনশীল প্রশ্ন ও সমাধান।
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="p-3 rounded-lg bg-[#FAF8F3] border border-[#E5E2DA] text-xs">
                      <span className="font-semibold text-[#1B2A4A]">গড় নির্ভুলতা: </span>
                      <span className="text-[#0B5D3B] font-bold">৮৪.২%</span>
                    </div>
                  </CardContent>
                  <CardFooter className="justify-between">
                    <span className="text-xs text-[#5B5B5B]">১০টি সৃজনশীল অনুশীলন</span>
                    <Button variant="link" size="sm">শুরু করুন &gt;</Button>
                  </CardFooter>
                </Card>

                <Card hoverable>
                  <CardHeader>
                    <CardMeta>
                      <Badge variant="verified" size="sm">ভর্তি প্রস্তুতি</Badge>
                      <span>বুয়েট ও ঢাবি ক</span>
                    </CardMeta>
                    <CardTitle>হোভারযোগ্য এডিটোরিয়াল কার্ড (Hoverable)</CardTitle>
                    <CardDescription>
                      মাউস কার্সার রাখলে কেবল সূক্ষ্ম বর্ডার ও ব্যাকগ্রাউন্ড টোন পরিবর্তন হবে; কোনো ডিসট্রেস্টিং ৩ডি জাম্প বা গ্লো নেই।
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="p-3 rounded-lg bg-[#FAF8F3] border border-[#E5E2DA] text-xs">
                      <span className="font-semibold text-[#1B2A4A]">স্ট্যাটাস: </span>
                      <span className="text-[#B8862B] font-bold">লাইভ পরীক্ষা চালু আছে</span>
                    </div>
                  </CardContent>
                  <CardFooter className="justify-between">
                    <span className="text-xs text-[#5B5B5B]">কাট-অফ ৬০.৫ মার্ক</span>
                    <Button variant="paper" size="sm">মক টেস্ট দিন</Button>
                  </CardFooter>
                </Card>

                <Card className="bg-[#FAF8F3] border-l-4 border-l-[#1B2A4A]">
                  <CardHeader>
                    <CardMeta>
                      <Badge variant="warning" size="sm">নোটিশ বোর্ড</Badge>
                      <span>আজকের আপডেট</span>
                    </CardMeta>
                    <CardTitle>প্রাতিষ্ঠানিক ঘোষণা ও নির্দেশিকা</CardTitle>
                    <CardDescription>
                      নতুন পাঠ্যক্রম অনুযায়ী সকল বিষয়ে কুইজ ও হ্যান্ডনোট হালনাগাদ করা হয়েছে। অফলাইন অ্যাপে নতুন অধ্যায় সিঙ্ক করে নিন।
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-xs text-[#5B5B5B] leading-relaxed">
                      সিঙ্ক সংক্রান্ত যে কোনো সমস্যায় হেল্প সেন্টারে যোগাযোগ করুন।
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button variant="default" size="sm" fullWidth>
                      নোটিশ বিস্তারিত দেখুন
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </section>

            {/* 3. BADGES & CHIPS */}
            <section className="space-y-5">
              <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
                <Palette className="w-5 h-5 text-[#1B2A4A]" />
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                  ৩. ব্যাজ ও স্ট্যাটাস ট্যাগ (Badges & Chips)
                </h2>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Subdued Flat Academic Tints (Zero Neon & Zero Purple)</CardTitle>
                  <CardDescription>
                    Low-contrast semantic tints for subject domains, difficulty levels, and user roles.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <span className="text-xs font-semibold text-[#5B5B5B] uppercase tracking-wider block">
                      সিম্যান্টিক ব্যাজ টিন্ট (Semantic Badges)
                    </span>
                    <div className="flex flex-wrap items-center gap-2.5">
                      <Badge variant="brand">Oxford Navy Tint</Badge>
                      <Badge variant="success">Emerald Mastery</Badge>
                      <Badge variant="warning">Scholar Gold</Badge>
                      <Badge variant="destructive">Burgundy Alert</Badge>
                      <Badge variant="neutral">Neutral Paper</Badge>
                      <Badge variant="outline">Hairline Outline</Badge>
                    </div>
                  </div>

                  <div className="space-y-2 pt-2 border-t border-[var(--color-border-subtle)]">
                    <span className="text-xs font-semibold text-[#5B5B5B] uppercase tracking-wider block">
                      কঠিনতা ও রোল চিপ (Domain Specific Chips)
                    </span>
                    <div className="flex flex-wrap items-center gap-3">
                      <DifficultyBadge difficulty="easy" label="সহজ প্রশ্ন (Easy)" />
                      <DifficultyBadge difficulty="medium" label="মধ্যম প্রশ্ন (Medium)" />
                      <DifficultyBadge difficulty="hard" label="কঠিন প্রশ্ন (Hard)" />
                      <VerifiedBadge label="এনসিটিবি অনুমোদিত (Verified)" shield />
                      <RoleChip role="student" label="শিক্ষার্থী (Student)" />
                      <RoleChip role="guardian" label="অভিভাবক (Guardian)" />
                      <RoleChip role="teacher" label="শিক্ষক (Teacher)" />
                      <RoleChip role="admin" label="অ্যাডমিন (Admin)" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* 4. FORM PRIMITIVES */}
            <section className="space-y-5">
              <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
                <Sliders className="w-5 h-5 text-[#1B2A4A]" />
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                  ৪. ফর্ম উপাদানসমূহ (Form Inputs, Select, Checkbox, Radio, Textarea)
                </h2>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Accessible Academic Form Controls</CardTitle>
                  <CardDescription>
                    Labeled, helper text, prefix/suffix icons, inline error validation, and accessible focus outlines.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Input
                      label={isBengali ? "শিক্ষার্থীর নাম (Student Full Name)" : "Full Name"}
                      placeholder={isBengali ? "যেমন: নাঈম মাহমুদ" : "e.g. John Doe"}
                      helperText={isBengali ? "আপনার প্রাতিষ্ঠানিক সার্টিফিকেটের নাম দিন" : "Enter name as on certificate"}
                      error={showFormErrors ? (isBengali ? "নাম দেওয়া আবশ্যক" : "Name is required") : undefined}
                    />

                    <Input
                      label={isBengali ? "অনুসন্ধান করুন (Search Library)" : "Search"}
                      placeholder={isBengali ? "অধ্যায় বা বোর্ড প্রশ্ন খুঁজুন..." : "Search topics..."}
                      prefixIcon={<Search className="w-4 h-4" />}
                    />

                    <Select
                      label={isBengali ? "শিক্ষাস্তর নির্বাচন করুন (Educational Level)" : "Select Level"}
                      helperText={isBengali ? "আপনার বর্তমান শ্রেণি বা প্রস্তুতি ক্ষেত্র নির্বাচন করুন" : "Choose target syllabus"}
                      error={showFormErrors ? (isBengali ? "শিক্ষাস্তর নির্বাচন করুন" : "Please select a level") : undefined}
                      options={[
                        { value: 'ssc', label: isBengali ? 'মাধ্যমিক (SSC ৯-১০)' : 'Secondary (SSC 9-10)' },
                        { value: 'hsc', label: isBengali ? 'উচ্চ মাধ্যমিক (HSC ১১-১২)' : 'Higher Secondary (HSC 11-12)' },
                        { value: 'admission', label: isBengali ? 'বিশ্ববিদ্যালয় ভর্তি (Admission)' : 'University Admission' },
                        { value: 'career', label: isBengali ? 'টিউশন ও পেশাগত ক্যারিয়ার (Career)' : 'Career & Tuition' },
                      ]}
                    />

                    <div className="space-y-3">
                      <span className="text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] block">
                        {isBengali ? "চেকবক্স অপশন (Checkboxes)" : "Checkboxes"}
                      </span>
                      <Checkbox
                        label={isBengali ? "অফলাইন মেশ সিঙ্ক চালু রাখুন" : "Keep offline mesh sync active"}
                        helperText={isBengali ? "ইন্টারনেট না থাকলেও স্থানীয় ডিভাইসে ডেটা সংরক্ষিত হবে" : "Saves data locally without internet"}
                        checked={checkboxChecked}
                        onChange={(e) => setCheckboxChecked(e.target.checked)}
                      />
                      <Checkbox
                        label={isBengali ? "দৈনিক অনুশীলন রিমাইন্ডার গ্রহণ করুন" : "Receive daily study reminders"}
                        error={showFormErrors ? (isBengali ? "শর্তাবলি মানা আবশ্যক" : "Consent required") : undefined}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-[var(--color-border-subtle)]">
                    <RadioGroup
                      label={isBengali ? "প্রধান বিষয় নির্বাচন করুন (Radio Group)" : "Select Primary Subject"}
                      name="subject"
                      value={selectedRadio}
                      onChange={setSelectedRadio}
                      helperText={isBengali ? "আপনার নির্বাচিত বিষয়ে দৈনিক প্রশ্ন আসবে" : "Sets priority subject"}
                    >
                      <Radio value="physics" label={isBengali ? "পদার্থবিজ্ঞান (Physics)" : "Physics"} />
                      <Radio value="chemistry" label={isBengali ? "রসায়ন (Chemistry)" : "Chemistry"} />
                      <Radio value="math" label={isBengali ? "উচ্চতর গণিত (Higher Mathematics)" : "Higher Math"} />
                    </RadioGroup>

                    <Textarea
                      label={isBengali ? "প্রশ্নের সমাধান নোট বা পর্যবেক্ষণ (Study Notes)" : "Study Notes"}
                      placeholder={isBengali ? "এখানে আপনার ব্যক্তিগত সমাধান নোট লিখুন..." : "Write personal notes here..."}
                      maxLength={200}
                      showCount
                      helperText={isBengali ? "সর্বোচ্চ ২০০ অক্ষরে নোট সংরক্ষণ করুন" : "Max 200 characters"}
                      error={showFormErrors ? (isBengali ? "নোট খালি রাখা যাবে না" : "Notes cannot be empty") : undefined}
                    />
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* 5. NAVIGATION, DISCLOSURE & FEEDBACK */}
            <section className="space-y-5">
              <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
                <BookOpen className="w-5 h-5 text-[#1B2A4A]" />
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                  ৫. নেভিগেশন ও ডিসক্লোজার (Breadcrumbs, Accordion, Pagination, Modal, Drawer)
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Accordion */}
                <Card>
                  <CardHeader>
                    <CardTitle>অ্যাকর্ডিয়ন ডিসক্লোজার (Accordion)</CardTitle>
                    <CardDescription>
                      ১৫০–২০০ms গতিতে মসৃণভাবে বিস্তারিত উন্মুক্ত বা বন্ধ হয়। WAI-ARIA ডিসক্লোজার নির্দেশিকা অনুযায়ী তৈরি।
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Accordion type="single" defaultValue="item-1">
                      <AccordionItem value="item-1">
                        <AccordionTrigger>
                          ১. অফলাইন মেশ প্রযুক্তি কীভাবে কাজ করে?
                        </AccordionTrigger>
                        <AccordionContent>
                          ইন্টারনেট সংযোগ না থাকলেও ব্রাউজারের IndexedDB এবং স্থানীয় পিয়ার-টু-পিয়ার ওয়াইফাই মেশের মাধ্যমে পরীক্ষা এবং নোট সিঙ্ক হয়।
                        </AccordionContent>
                      </AccordionItem>
                      <AccordionItem value="item-2">
                        <AccordionTrigger>
                          ২. নেগেটিভ মার্কিং কীভাবে হিসাব করা হয়?
                        </AccordionTrigger>
                        <AccordionContent>
                          বিশ্ববিদ্যালয় ভর্তি পরীক্ষায় প্রতিটি ভুল উত্তরের জন্য ০.২৫ নম্বর কর্তন করা হয়, যা স্বয়ংক্রিয়ভাবে নেট স্কোরে প্রতিফলিত হয়।
                        </AccordionContent>
                      </AccordionItem>
                      <AccordionItem value="item-3">
                        <AccordionTrigger>
                          ৩. বোর্ড পরীক্ষার বিগত বছরের প্রশ্নগুলো কি যাচাইকৃত?
                        </AccordionTrigger>
                        <AccordionContent>
                          হ্যাঁ, ২০১৫ থেকে ২০২৫ পর্যন্ত সকল শিক্ষা বোর্ডের সাধারণ ও নৈর্ব্যক্তিক প্রশ্নসমূহ এনসিটিবি ও অভিজ্ঞ পরীক্ষক দ্বারা শতভাগ যাচাইকৃত।
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                  </CardContent>
                </Card>

                {/* Overlays & Modals */}
                <Card>
                  <CardHeader>
                    <CardTitle>মডাল ও ড্রয়ার কন্ট্রোল (Modal & Drawer)</CardTitle>
                    <CardDescription>
                      কোনো ভারী ব্যাকড্রপ-ব্লার ছাড়াই হালকা স্বচ্ছ শেডে ফোকাস ট্র্যাপ সহ প্যানেল প্রদর্শন।
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Breadcrumb
                      items={[
                        { label: 'হোম', href: '/' },
                        { label: 'এইচএসসি বিজ্ঞান', href: '/learn' },
                        { label: 'পদার্থবিজ্ঞান ১ম পত্র', href: '/practice' },
                        { label: 'গতিবিদ্যা', isCurrent: true },
                      ]}
                    />

                    <div className="flex flex-wrap items-center gap-3 pt-3">
                      <Button variant="default" size="md" onClick={() => setIsModalOpen(true)}>
                        মডাল ওপেন করুন (Modal)
                      </Button>
                      <Button variant="paper" size="md" onClick={() => setIsDrawerOpen(true)}>
                        স্লাইড ড্রয়ার খুলুন (Drawer)
                      </Button>
                      <Tooltip content="এটি একটি টুলটিপ নির্দেশিকা">
                        <Button variant="ghost" size="md" icon={<Info className="w-4 h-4" />}>
                          টুলটিপ টেস্ট
                        </Button>
                      </Tooltip>
                    </div>

                    <div className="pt-4 border-t border-[var(--color-border-subtle)]">
                      <span className="text-xs font-semibold text-[#5B5B5B] block mb-2">
                        পৃষ্ঠা পরিবর্তন নেভিগেশন (Pagination):
                      </span>
                      <Pagination
                        currentPage={currentPage}
                        totalPages={8}
                        onPageChange={setCurrentPage}
                        isBengali={isBengali}
                      />
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Table Primitive */}
              <Card>
                <CardHeader>
                  <CardTitle>টেক্সটবুক টেবিল (Textbook-like Table)</CardTitle>
                  <CardDescription>
                    হেয়ারলাইন রো বর্ডার (#E5E2DA), স্টিকি হেডার, এবং হালকা পেপার হোভার স্টেট।
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table stickyHeader striped>
                    <TableHeader sticky>
                      <TableRow>
                        <TableHead>বোর্ড ও সন</TableHead>
                        <TableHead>অধ্যায় ও বিষয়</TableHead>
                        <TableHead>প্রশ্ন সংখ্যা</TableHead>
                        <TableHead>গড় নির্ভুলতা</TableHead>
                        <TableHead>পদক্ষেপ</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {[
                        { board: 'ঢাকা বোর্ড ২০২৩', subject: 'পদার্থবিজ্ঞান ১ম পত্র • গতিবিদ্যা', count: '২৫টি MCQ', accuracy: '৮৬.৪%', status: 'সম্পূর্ণ' },
                        { board: 'চট্টগ্রাম বোর্ড ২০২৩', subject: 'রসায়ন ১ম পত্র • গুণগত রসায়ন', count: '২৫টি MCQ', accuracy: '৭৯.১%', status: 'চলমান' },
                        { board: 'রাজশাহী বোর্ড ২০২২', subject: 'উচ্চতর গণিত ১ম পত্র • ম্যাট্রিক্স', count: '২৫টি MCQ', accuracy: '৯১.০%', status: 'সম্পূর্ণ' },
                        { board: 'যশোর বোর্ড ২০২২', subject: 'জীববিজ্ঞান ১ম পত্র • কোষ ও এর গঠন', count: '২৫টি MCQ', accuracy: '৮৩.৫%', status: 'সম্পূর্ণ' },
                      ].map((row, idx) => (
                        <TableRow key={idx}>
                          <TableCell className="font-semibold text-[#1B2A4A]">{row.board}</TableCell>
                          <TableCell>{row.subject}</TableCell>
                          <TableCell className="font-mono text-xs">{row.count}</TableCell>
                          <TableCell className="font-bold text-[#0B5D3B]">{row.accuracy}</TableCell>
                          <TableCell>
                            <Button variant="link" size="sm">অনুশীলন &gt;</Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>

              {/* Skeleton & Empty State */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>স্কেলিটন লোডার (Skeleton Loaders)</CardTitle>
                    <CardDescription>
                      শান্ত ও মৃদু পালস অ্যানিমেশন যা পেজের লেআউট শিফট (CLS) প্রতিরোধ করে।
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-3">
                      <Skeleton variant="circular" width={48} height={48} />
                      <div className="space-y-2 flex-1">
                        <Skeleton variant="text" width="60%" height={16} />
                        <Skeleton variant="text" width="40%" height={12} />
                      </div>
                    </div>
                    <Skeleton variant="rectangular" height={80} className="w-full rounded-xl" />
                  </CardContent>
                </Card>

                <EmptyState
                  title="কোনো অনিষ্পন্ন পরীক্ষা পাওয়া যায়নি"
                  description="আপনার সকল নির্ধারিত অধ্যায়ের পরীক্ষা সফলভাবে সম্পন্ন হয়েছে। নতুন কোনো মডেল টেস্ট চালু করতে সিলেবাস ব্রাউজ করুন।"
                  actionText="নতুন অধ্যায় দেখুন"
                  onAction={() => alert('Browse curriculum clicked')}
                />
              </div>
            </section>
          </div>
        )}

        {/* SECTION: QUIZ & QUESTION ENGINE */}
        {(activeTab === 'all' || activeTab === 'quiz') && (
          <section className="space-y-6">
            <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
              <Sparkles className="w-5 h-5 text-[#1B2A4A]" />
              <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                ৬. কুইজ ও প্রশ্ন ইঞ্জিন উপাদান (Quiz UI & Mathematical KaTeX)
              </h2>
            </div>

            <div className="space-y-6">
              {/* Progress */}
              <QuizProgress
                currentQuestion={7}
                totalQuestions={25}
                timeRemaining="18:42"
                score={28}
                streak={5}
                isBengali={isBengali}
              />

              {/* Interactive Question Demonstration */}
              <Card>
                <CardHeader>
                  <CardMeta>
                    <Badge variant="brand" size="sm">ঢাকা বোর্ড ২০২৩</Badge>
                    <Badge variant="warning" size="sm">নেগেটিভ মার্কিং: ০.২৫</Badge>
                    <span>পদার্থবিজ্ঞান ১ম পত্র • ৩য় অধ্যায়</span>
                  </CardMeta>
                  <CardTitle className="text-xl sm:text-2xl pt-1">
                    <KaTeXRenderer text={String.raw`একটি ক্রিকেট বলকে ভূমির সাথে $30^\circ$ কোণে $40 \text{ m/s}$ বেগে নিক্ষেপ করা হলে এর সর্বোচ্চ উচ্চতা ($H$) কত হবে? ($g = 9.8 \text{ m/s}^2$)`} />
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="space-y-2">
                    {[
                      { key: 'A', text: String.raw`$H = 15.42 \text{ m}$` },
                      { key: 'B', text: String.raw`$H = 20.41 \text{ m}$` },
                      { key: 'C', text: String.raw`$H = 25.68 \text{ m}$` },
                      { key: 'D', text: String.raw`$H = 32.14 \text{ m}$` },
                    ].map(opt => (
                      <OptionCard
                        key={opt.key}
                        id={opt.key}
                        optionKey={opt.key as 'A' | 'B' | 'C' | 'D'}
                        textBn={opt.text}
                        isSelected={selectedOption === opt.key}
                        onSelect={(k) => setSelectedOption(k)}
                      />
                    ))}
                  </div>

                  <div className="pt-4">
                    <ExplanationBlock
                      correctOptionKey="B"
                      correctOptionText={String.raw`$H = \frac{v_0^2 \sin^2\theta}{2g} = \frac{40^2 \times \sin^2(30^\circ)}{2 \times 9.8} = \frac{1600 \times 0.25}{19.6} \approx 20.41 \text{ m}$`}
                      keyFormula={String.raw`$H = \frac{v_0^2 \sin^2\theta}{2g} \quad \text{এবং} \quad R = \frac{v_0^2 \sin 2\theta}{g}$`}
                      sourceAttribution="এনসিটিবি অনুমোদিত পাঠ্যবই, অধ্যায় ৩ (গতিবিদ্যা)"
                      explanationBn={String.raw`আমরা জানি, প্রক্ষেপকের ক্ষেত্রে সর্বোচ্চ উচ্চতার সমীকরণ $H = \frac{v_0^2 \sin^2\theta}{2g}$। এখানে আদিবেগ $v_0 = 40 \text{ m/s}$, নিক্ষেপণ কোণ $\theta = 30^\circ$, এবং অভিকর্ষজ ত্বরণ $g = 9.8 \text{ m/s}^2$। মানগুলো বসালে প্রাপ্ত মান দাঁড়ায় প্রায় $20.41 \text{ m}$।`}
                      isBengali={isBengali}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Scorecard */}
              <QuizResultSummary
                totalQuestions={25}
                correctCount={21}
                incorrectCount={3}
                unattemptedCount={1}
                negativeMarks={0.75}
                timeTaken="22 মিনিট 15 সেকেন্ড"
                isBengali={isBengali}
                onReview={() => alert('Review answers')}
                onRetry={() => alert('Retry')}
              />
            </div>
          </section>
        )}

        {/* SECTION: COLOR TOKENS */}
        {(activeTab === 'all' || activeTab === 'colors') && (
          <section id="colors" className="space-y-6">
            <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
              <Palette className="w-5 h-5 text-[#1B2A4A]" />
              <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                ৭. কালার টোকেন আর্কিটেকচার (Color Tokens)
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              <Swatch
                name="Paper Ground"
                variable="--color-paper-ground"
                hex="#FAF8F3"
                roleDescription="মেইন অ্যাপ ক্যানভাস ব্যাকগ্রাউন্ড (Warm Paper)"
                contrastRatio="15.8:1"
                wcag="AAA"
              />
              <Swatch
                name="Paper Surface"
                variable="--color-paper-surface"
                hex="#FFFFFF"
                roleDescription="কার্ড ও কন্টেইনার সারফেস"
                contrastRatio="16.5:1"
                wcag="AAA"
              />
              <Swatch
                name="Academic Navy"
                variable="--color-brand-primary"
                hex="#1B2A4A"
                textDark
                roleDescription="প্রধান প্রাতিষ্ঠানিক অ্যাকশন ও হেডিং কালার"
                contrastRatio="12.4:1"
                wcag="AAA"
              />
              <Swatch
                name="Academic Emerald"
                variable="--color-semantic-success"
                hex="#0B5D3B"
                textDark
                roleDescription="মেধাতালিকা, সঠিক উত্তর ও ভেরিফাইড ব্যাজ"
                contrastRatio="7.9:1"
                wcag="AAA"
              />
            </div>
          </section>
        )}

        {/* SECTION: TYPOGRAPHY */}
        {(activeTab === 'all' || activeTab === 'typography') && (
          <section id="typography" className="space-y-6">
            <div className="flex items-center gap-2 border-b border-[var(--color-border-hairline)] pb-3">
              <Type className="w-5 h-5 text-[#1B2A4A]" />
              <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#1B2A4A]">
                ৮. টাইপোগ্রাফি ও যুক্তাক্ষর নির্দেশিকা (Typography & Ligatures)
              </h2>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>বাংলা ও ইংরেজি টাইপ স্কেল (~১.২৫০ মেজর থার্ড)</CardTitle>
                <CardDescription>
                  মাত্ৰা সুরক্ষা সহ ১.৭৮ লাইন-হাইট এবং Noto Serif Bengali + Hind Siliguri ফন্ট সমন্বয়।
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-3xl sm:text-4xl font-serif font-bold text-[#1B2A4A]">
                  বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক ডিজিটাল শিক্ষাজীবন
                </div>
                <p className="text-base sm:text-lg text-[#5B5B5B] leading-[1.8] max-w-2xl font-sans">
                  মাধ্যমিক ও উচ্চ মাধ্যমিক থেকে বিশ্ববিদ্যালয় ভর্তি এবং পেশাগত ক্যারিয়ার—সব বিষয়ের অধ্যায়ভিত্তিক প্রাতিষ্ঠানিক পাঠ্যক্রম, বিগত ১০ বছরের নির্ভুল বোর্ড প্রশ্ন এবং ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাবরেটরি।
                </p>

                <div className="pt-4 border-t border-[var(--color-border-subtle)] space-y-2">
                  <span className="text-xs font-semibold text-[#5B5B5B] uppercase tracking-wider block">
                    জটিল বাংলা যুক্তাক্ষর রেন্ডারিং (Conjunct Glyphs):
                  </span>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
                    {conjuncts.slice(0, 12).map((item, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg border border-[#E5E2DA] bg-[#FAF8F3] text-center">
                        <span className="text-xl font-serif font-bold text-[#1B2A4A] block mb-1">{item.glyph}</span>
                        <span className="text-[10px] text-[#5B5B5B] block truncate">{item.example}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>
        )}
      </main>

      {/* Interactive Modal Instance */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="প্রাতিষ্ঠানিক কুইজ ডায়ালগ"
        description="পরীক্ষা শুরু করার পূর্বে নির্দেশিকাগুলো মনোযোগ সহকারে পড়ুন।"
        footer={
          <div className="flex items-center justify-end gap-2 w-full">
            <Button variant="paper" size="sm" onClick={() => setIsModalOpen(false)}>
              বাতিল করুন
            </Button>
            <Button variant="default" size="sm" onClick={() => setIsModalOpen(false)}>
              বুঝেছি, পরীক্ষা শুরু করুন
            </Button>
          </div>
        }
      >
        <div className="space-y-2 text-xs sm:text-sm text-[#1A1A1A] dark:text-slate-300">
          <p>১. প্রতি প্রশ্নের জন্য ৬০ সেকেন্ড সময় বরাদ্দ থাকবে।</p>
          <p>২. প্রতিটি ভুল উত্তরের জন্য ০.২৫ নেগেটিভ মার্কিং প্রযোজ্য।</p>
          <p>৩. পরীক্ষা চলাকালীন কিবোর্ডের 1-4 অথবা A-D চেপে দ্রুত উত্তর নির্বাচন করা যাবে।</p>
        </div>
      </Modal>

      {/* Interactive Drawer Instance */}
      <Drawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        title="শেখার অগ্রগতি ও সিলেবাস ওভারভিউ"
        description="আপনার বর্তমান সম্পন্নকৃত অধ্যায়সমূহ ও পরীক্ষার ফলাফল"
        footer={
          <Button variant="default" size="md" fullWidth onClick={() => setIsDrawerOpen(false)}>
            ড্রয়ার বন্ধ করুন
          </Button>
        }
      >
        <div className="space-y-4">
          <div className="p-3.5 rounded-xl bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D]">
            <span className="text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] block mb-1">
              পদার্থবিজ্ঞান ১ম পত্র
            </span>
            <div className="w-full h-2 rounded-full bg-slate-200 overflow-hidden">
              <div className="h-full bg-[#0B5D3B] rounded-full" style={{ width: '68%' }} />
            </div>
            <span className="text-[11px] text-[#5B5B5B] mt-1 block">৬৮% সিলেবাস সম্পন্ন</span>
          </div>

          <p className="text-xs text-[#5B5B5B] leading-relaxed">
            এখানে শিক্ষার্থীর বিস্তারিত অগ্রগতি, প্রতিটি অধ্যায়ের সমাধানকৃত প্রশ্ন সংখ্যা এবং রিভিশন তালিকা দেখা যাবে।
          </p>
        </div>
      </Drawer>

      {/* Footer */}
      <footer className="mt-16 border-t border-[var(--color-border-hairline)] bg-white py-8">
        <div className="max-w-6xl mx-auto px-4 text-center text-xs text-[var(--color-ink-muted)]">
          অগ্রযাত্রা এডুকেশন প্ল্যাটফর্ম · অ্যাকাডেমিক এডিটোরিয়াল ডিজাইন সিস্টেম ও কম্পোনেন্ট গ্যালারি · ২০২৬
        </div>
      </footer>
    </div>
  );
}
