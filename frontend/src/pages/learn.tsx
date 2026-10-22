/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Learning Hub & NCTB Curriculum Navigation
 * TOPIC:     Phase 115, Phase 138 & Modern Academic Editorial Inner Pages Elevation
 * FILE:      frontend/src/pages/learn.tsx
 * PURPOSE:   Standardized academic learning hub with flagship PageHeader,
 *            editorial breadcrumbs, spaced-repetition revision queue, chapter syllabus drawer,
 *            and tactile 3D physics.
 * STANDARDS: Modern Academic Editorial, Pure Academic Palette (#FAF8F3, #1B2A4A, #0A2540),
 *            Zero-Emoji, Zero-Neon, WCAG 2.2 AAA Contrast, 60-75ch Reading Typography
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Play,
  RotateCcw,
  Sparkles,
  ChevronRight,
  Video,
  Award,
  Layers,
  X,
  Compass,
  AlertCircle,
  GraduationCap,
  FileText,
  BookmarkCheck,
  Check,
  ExternalLink
} from 'lucide-react';
import { AppHead, createCourseSchema } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { HlsLecturePlayer } from '@/components/video/HlsLecturePlayer';
import {
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardMeta,
  CardContent,
  CardFooter,
  Badge,
  Tabs,
  TabsList,
  TabsTrigger,
  Drawer,
  Breadcrumb
} from '@/components/ui';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';

interface ChapterItem {
  id: string;
  number: number;
  titleBn: string;
  topicCount: number;
  progressPercent: number;
  isRevised: boolean;
  videoLectureId?: string;
  summaryNotes?: {
    overview: string;
    keyFormulas: string[];
    importantPoints: string[];
    textbookPage: string;
  };
}

interface SubjectItem {
  id: string;
  stage: 'MIDDLE' | 'SSC' | 'HSC' | 'ADMISSION';
  titleBn: string;
  titleEn: string;
  chaptersCount: number;
  completedPercent: number;
  chapters: ChapterItem[];
}

const CURATED_SUBJECTS: SubjectItem[] = [
  {
    id: 'sub_phys_1',
    stage: 'HSC',
    titleBn: 'পদার্থবিজ্ঞান ১ম পত্র',
    titleEn: 'HSC Physics 1st Paper',
    chaptersCount: 10,
    completedPercent: 75,
    chapters: [
      {
        id: 'ch_1',
        number: 1,
        titleBn: 'ভেক্টর ও দিক রাশি',
        topicCount: 8,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_vec_01',
        summaryNotes: {
          overview: 'ভেক্টর রাশির যোজন, বিয়োজন, ডট গুণন ও ক্রস গুণনের মাধ্যমে দ্বিমাত্রিক ও ত্রিমাত্রিক তলে ভেক্টর বিশ্লেষণ এবং নদী-নৌকার আপেক্ষিক বেগ সংক্রান্ত সমাধান।',
          keyFormulas: [
            'লব্ধি: $R = \\sqrt{P^2 + Q^2 + 2PQ \\cos\\alpha}$',
            'ডট গুণন: $\\vec{A} \\cdot \\vec{B} = AB \\cos\\theta = A_x B_x + A_y B_y + A_z B_z$',
            'ক্রস গুণন: $|\\vec{A} \\times \\vec{B}| = AB \\sin\\theta$'
          ],
          importantPoints: [
            'দুটি ভেক্টর পরস্পর লম্ব হওয়ার শর্ত: $\\vec{A} \\cdot \\vec{B} = 0$',
            'দুটি ভেক্টর পরস্পর সমান্তরাল হওয়ার শর্ত: $\\vec{A} \\times \\vec{B} = 0$',
            'নদী ন্যূনতম সময়ে পারাপারের ক্ষেত্রে লব্ধির দিক নদীর তীরের সাথে $\\theta = 90^\\circ$ হতে হয়।'
          ],
          textbookPage: 'অধ্যায় ২, পৃষ্ঠা ৩৫–৬৮'
        }
      },
      {
        id: 'ch_2',
        number: 2,
        titleBn: 'গতিবিদ্যা ও একমাত্রিক প্রক্ষেপক',
        topicCount: 12,
        progressPercent: 85,
        isRevised: true,
        videoLectureId: 'lec_kin_02',
        summaryNotes: {
          overview: 'একমাত্রিক ও দ্বিমাত্রিক গতি, ত্বরণ, প্রক্ষেপকের গতিপথ এবং প্রাস সংক্রান্ত গাণিতিক সূত্রের প্রতিপাদন ও বাস্তবিক উদাহরণ।',
          keyFormulas: [
            'সর্বোচ্চ উচ্চতা: $H = \\frac{v_0^2 \\sin^2\\theta}{2g}$',
            'উড্ডয়ন কাল: $T = \\frac{2 v_0 \\sin\\theta}{g}$',
            'আনুভূমিক পাল্লা: $R = \\frac{v_0^2 \\sin 2\\theta}{g}$'
          ],
          importantPoints: [
            'সর্বোচ্চ আনুভূমিক পাল্লার জন্য নিক্ষেপণ কোণ $\\theta = 45^\\circ$ হতে হবে।',
            'প্রক্ষেপকের গতিপথ একটি অধিবৃত্ত (প্যারাবোলা)।'
          ],
          textbookPage: 'অধ্যায় ৩, পৃষ্ঠা ৬৯–১০২'
        }
      },
      {
        id: 'ch_3',
        number: 3,
        titleBn: 'নিউটনিয়ান বলবিদ্যা ও ঘূর্ণন গতি',
        topicCount: 14,
        progressPercent: 70,
        isRevised: false,
        videoLectureId: 'lec_newton_03',
        summaryNotes: {
          overview: 'নিউটনের গতির সূত্রসমূহ, ভরবেগের সংরক্ষণশীলতা নীতি, ঘর্ষণ বল, কেন্দ্রমুখী বল, ব্যাংকিং কোণ এবং জড়তার ভ্রামক।',
          keyFormulas: [
            'রাস্তার ব্যাংকিং কোণ: $\\tan\\theta = \\frac{v^2}{rg}$',
            'কৌণিক ভরবেগ: $L = I\\omega = mvr$',
            'ঘূর্ণন গতিশক্তি: $E_k = \\frac{1}{2} I \\omega^2$'
          ],
          importantPoints: [
            'বহিঃস্থ টর্ক শূন্য হলে কৌণিক ভরবেগ ধ্রুব থাকে ($I_1 \\omega_1 = I_2 \\omega_2$)।',
            'জড়তার ভ্রামকের সমান্তরাল ও লম্ব অক্ষ উপপাদ্য বোর্ডের অন্যতম প্রধান বর্ণনামূলক প্রশ্ন।'
          ],
          textbookPage: 'অধ্যায় ৪, পৃষ্ঠা ১০৩–১৪৬'
        }
      },
      {
        id: 'ch_4',
        number: 4,
        titleBn: 'কাজ, শক্তি ও ক্ষমতা',
        topicCount: 10,
        progressPercent: 45,
        isRevised: false,
        videoLectureId: 'lec_work_04',
        summaryNotes: {
          overview: 'পরিবর্তনশীল ও ধ্রুব বল দ্বারা কৃতকাজ, কাজ-শক্তি উপপাদ্য, স্প্রিংয়ের বিভব শক্তি, শক্তির সংরক্ষণশীলতা এবং কর্মদক্ষতা।',
          keyFormulas: [
            'কাজ: $W = \\vec{F} \\cdot \\vec{s} = F s \\cos\\theta$',
            'স্প্রিংয়ের বিভবশক্তি: $U = \\frac{1}{2} k x^2$',
            'কর্মদক্ষতা: $\\eta = \\frac{P_{\\text{out}}}{P_{\\text{in}}} \\times 100\\%$'
          ],
          importantPoints: [
            'কাজ-শক্তি উপপাদ্য: প্রযুক্ত বল দ্বারা মোট কৃতকাজ বস্তুর গতিশক্তির পরিবর্তনের সমান ($W = \\Delta K$)।',
            'অভিকর্ষ বল একটি সংরক্ষণশীল বল।'
          ],
          textbookPage: 'অধ্যায় ৫, পৃষ্ঠা ১৪৭–১৮০'
        }
      }
    ]
  },
  {
    id: 'sub_chem_1',
    stage: 'HSC',
    titleBn: 'রসায়ন ১ম পত্র',
    titleEn: 'HSC Chemistry 1st Paper',
    chaptersCount: 8,
    completedPercent: 60,
    chapters: [
      {
        id: 'ch_c1',
        number: 1,
        titleBn: 'গুণগত রসায়ন ও পরমাণুর গঠন',
        topicCount: 11,
        progressPercent: 90,
        isRevised: true,
        videoLectureId: 'lec_chem_01',
        summaryNotes: {
          overview: 'রাদারফোর্ড ও বোর পরমাণু মডেল, কোয়ান্টাম সংখ্যা, অফবাউ ও হুন্ডের নীতি, এবং দ্রাব্যতা ও দ্রাব্যতা গুণফল ($K_{sp}$)।',
          keyFormulas: [
            'রিডবার্গ সমীকরণ: $\\bar{\\nu} = \\frac{1}{\\lambda} = R_H \\left(\\frac{1}{n_1^2} - \\frac{1}{n_2^2}\\right)$',
            'ডি-ব্রগলির সমীকরণ: $\\lambda = \\frac{h}{mv}$',
            'দ্রাব্যতা গুণফল: $A_x B_y \\rightleftharpoons xA^{y+} + yB^{x-} \\implies K_{sp} = [A^{y+}]^x [B^{x-}]^y$'
          ],
          importantPoints: [
            'হুন্ডের নীতি: সমশক্তি সম্পন্ন অরবিটালে ইলেকট্রনগুলো সর্বাধিক অযুগ্ম অবস্থায় থাকবে এবং তাদের ঘূর্ণন একইমুখী হবে।',
            'অধঃক্ষেপ পড়ার শর্ত: আয়ন গুণফল ($K_{ip}$) > দ্রাব্যতা গুণফল ($K_{sp}$)।'
          ],
          textbookPage: 'অধ্যায় ২, পৃষ্ঠা ৪২–৮৮'
        }
      },
      {
        id: 'ch_c2',
        number: 2,
        titleBn: 'পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন',
        topicCount: 15,
        progressPercent: 65,
        isRevised: false,
        videoLectureId: 'lec_chem_02',
        summaryNotes: {
          overview: 'পর্যায় সারণির বিভিন্ন ব্লকের বৈশিষ্ট্য, পরমাণুর আকার, আয়নীকরণ শক্তি, তড়িৎ ঋণাত্মকতা এবং সংকরায়ন (Hybridization)।',
          keyFormulas: [
            'সংকরায়ন স্টেরিক নম্বর: $SN = \\frac{1}{2} (V + M - C + A)$'
          ],
          importantPoints: [
            'ফাজানের নীতি: ক্যাটায়নের আকার যত ছোট এবং অ্যানায়নের আকার যত বড় হবে, সমযোজী বৈশিষ্ট্য তত বৃদ্ধি পাবে।',
            'পানির অণুতে $sp^3$ সংকরায়ন হওয়া সত্ত্বেও মুক্তজোড় ইলেকট্রন থাকায় বন্ধন কোণ $104.5^\\circ$ হয়।'
          ],
          textbookPage: 'অধ্যায় ৩, পৃষ্ঠা ৮৯–১৪২'
        }
      },
      {
        id: 'ch_c3',
        number: 3,
        titleBn: 'রাসায়নিক পরিবর্তন ও সাম্যাবস্থা',
        topicCount: 14,
        progressPercent: 30,
        isRevised: false,
        videoLectureId: 'lec_chem_03',
        summaryNotes: {
          overview: 'বিক্রিয়ার হার, লা-শাতেলিয়ার নীতি, সাম্যধ্রুবক $K_p$ ও $K_c$ এর সম্পর্ক, এবং বাফার দ্রবণ ও pH গণনা।',
          keyFormulas: [
            'সাম্যধ্রুবক সম্পর্ক: $K_p = K_c (RT)^{\\Delta n}$',
            'হেন্ডারসন-হ্যাসেলবালখ সমীকরণ: $\\text{pH} = \\text{pK}_a + \\log\\frac{[\\text{Salt}]}{[\\text{Acid}]}$'
          ],
          importantPoints: [
            'লা-শাতেলিয়ার নীতি: সাম্যাবস্থায় তাপমাত্রা, চাপ বা ঘনমাত্রা পরিবর্তন করলে সাম্যাবস্থা এমনভাবে স্থানান্তরিত হবে যাতে পরিবর্তনের প্রভাব প্রশমিত হয়।'
          ],
          textbookPage: 'অধ্যায় ৪, পৃষ্ঠা ১৪৩–১৯৮'
        }
      }
    ]
  },
  {
    id: 'sub_math_1',
    stage: 'HSC',
    titleBn: 'উচ্চতর গণিত ১ম পত্র',
    titleEn: 'HSC Higher Mathematics 1st Paper',
    chaptersCount: 10,
    completedPercent: 80,
    chapters: [
      {
        id: 'ch_m1',
        number: 1,
        titleBn: 'ম্যাট্রিক্স ও নির্ণায়ক',
        topicCount: 9,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_mat_01',
        summaryNotes: {
          overview: 'ম্যাট্রিক্সের যোগ, বিয়োগ, গুণ, বিপরীত ম্যাট্রিক্স নির্ণয় এবং ক্র্যামারের নিয়মে একঘাত সমীকরণ জোট সমাধান।',
          keyFormulas: [
            'বিপরীত ম্যাট্রিক্স: $A^{-1} = \\frac{1}{|A|} \\text{adj}(A)$, যেখানে $|A| \\neq 0$',
            'ক্র্যামারের নিয়ম: $x = \\frac{D_x}{D}, \\; y = \\frac{D_y}{D}, \\; z = \\frac{D_z}{D}$'
          ],
          importantPoints: [
            'ব্যতিক্রমী ম্যাট্রিক্সের নির্ণায়কের মান শূন্য ($|A| = 0$), যার বিপরীত ম্যাট্রিক্স বিদ্যমান নয়।',
            'ম্যাট্রিক্সের গুণনের শর্ত: প্রথম ম্যাট্রিক্সের কলাম সংখ্যা = দ্বিতীয় ম্যাট্রিক্সের সারি সংখ্যা।'
          ],
          textbookPage: 'অধ্যায় ১, পৃষ্ঠা ১–৪০'
        }
      },
      {
        id: 'ch_m2',
        number: 2,
        titleBn: 'সরলরেখা ও স্থানাঙ্ক জ্যামিতি',
        topicCount: 14,
        progressPercent: 85,
        isRevised: true,
        videoLectureId: 'lec_line_02',
        summaryNotes: {
          overview: 'কার্তেসীয় ও পোলার স্থানাঙ্ক, বিন্দুর অন্তরবিভক্তিকরণ, সরলরেখার ঢাল, বিভিন্ন আকারের সমীকরণ ও মধ্যবর্তী কোণ।',
          keyFormulas: [
            'বিন্দুর দূরত্ব: $d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$',
            'সরলরেখা হতে বিন্দুর লম্বদূরত্ব: $p = \\frac{|a x_1 + b y_1 + c|}{\\sqrt{a^2 + b^2}}$',
            'দুটি সরলরেখার মধ্যবর্তী কোণ: $\\tan\\theta = \\pm \\frac{m_1 - m_2}{1 + m_1 m_2}$'
          ],
          importantPoints: [
            'পরস্পর লম্ব রেখাদ্বয়ের ঢালের গুণফল: $m_1 m_2 = -1$',
            'পরস্পর সমান্তরাল রেখাদ্বয়ের ঢাল সমান: $m_1 = m_2$'
          ],
          textbookPage: 'অধ্যায় ৩, পৃষ্ঠা ৪১–৯৪'
        }
      },
      {
        id: 'ch_m3',
        number: 3,
        titleBn: 'অন্তরীকরণ ও ক্যালকুলাস',
        topicCount: 16,
        progressPercent: 60,
        isRevised: false,
        videoLectureId: 'lec_diff_03',
        summaryNotes: {
          overview: 'ফাংশনের সীমা (Limit), মূল নিয়মে অন্তরজ নির্ণয়, পর্যায়ক্রমিক অন্তরীকরণ, স্পর্শক ও অভিলম্বের সমীকরণ এবং চরম মান (গুরুমান ও লঘুমান)।',
          keyFormulas: [
            'মূল নিয়মে অন্তরীকরণ: $\\frac{dy}{dx} = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$',
            'গুণফলের সূত্র: $\\frac{d}{dx}(uv) = u \\frac{dv}{dx} + v \\frac{du}{dx}$',
            'ভাগফলের সূত্র: $\\frac{d}{dx}\\left(\\frac{u}{v}\\right) = \\frac{v \\frac{du}{dx} - u \\frac{dv}{dx}}{v^2}$'
          ],
          importantPoints: [
            'চরম মানের প্রয়োজনীয় শর্ত: $f\'(x) = 0$',
            'লঘুমানের জন্য $f\'\'(x) > 0$ এবং গুরুমানের জন্য $f\'\'(x) < 0$।'
          ],
          textbookPage: 'অধ্যায় ৯, পৃষ্ঠা ১৯৫–২৫৪'
        }
      }
    ]
  },
  {
    id: 'sub_ssc_phys',
    stage: 'SSC',
    titleBn: 'পদার্থবিজ্ঞান (এসএসসি)',
    titleEn: 'SSC Physics',
    chaptersCount: 8,
    completedPercent: 90,
    chapters: [
      {
        id: 'ch_s_p1',
        number: 1,
        titleBn: 'ভৌত রাশি ও পরিমাপ',
        topicCount: 7,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_ssc_p01',
        summaryNotes: {
          overview: 'পরিমাপের একক, ভার্নিয়ার স্কেল, স্ক্রু গজ এবং পরিমাপে ত্রুটির বিশ্লেষণ।',
          keyFormulas: [
            'ভার্নিয়ার ধ্রুবক: $VC = \\frac{s}{n}$',
            'লঘিষ্ঠ গণন: $LC = \\frac{\\text{Pitch}}{n}$'
          ],
          importantPoints: [
            'ভার্নিয়ার স্কেলের সাহায্যে সাধারণ স্কেলের চেয়ে সূক্ষ্ম পরিমাপ নিশ্চিত করা যায়।'
          ],
          textbookPage: 'অধ্যায় ১, পৃষ্ঠা ১–২০'
        }
      },
      {
        id: 'ch_s_p2',
        number: 2,
        titleBn: 'গতি ও গতির সমীকরণ',
        topicCount: 9,
        progressPercent: 88,
        isRevised: true,
        videoLectureId: 'lec_ssc_p02',
        summaryNotes: {
          overview: 'দূরত্ব ও সরণ, দ্রুতি ও বেগ, সুষম ত্বরণ এবং গতির ৪টি মূল সমীকরণ।',
          keyFormulas: [
            '$v = u + at$',
            '$s = ut + \\frac{1}{2} at^2$',
            '$v^2 = u^2 + 2as$'
          ],
          importantPoints: [
            'মুক্তভাবে পড়ন্ত বস্তুর ক্ষেত্রে গ্যালিলিওর সূত্রসমূহ প্রযোজ্য।'
          ],
          textbookPage: 'অধ্যায় ২, পৃষ্ঠা ২১–৪৫'
        }
      }
    ]
  },
  {
    id: 'sub_ssc_math',
    stage: 'SSC',
    titleBn: 'সাধারণ গণিত (এসএসসি)',
    titleEn: 'SSC General Mathematics',
    chaptersCount: 10,
    completedPercent: 70,
    chapters: [
      {
        id: 'ch_s_m1',
        number: 1,
        titleBn: 'বাস্তব সংখ্যা ও সেট-ফাংশন',
        topicCount: 8,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_ssc_m01',
        summaryNotes: {
          overview: 'মূলদ ও অমূলদ সংখ্যা, আবৃত্ত দশমিক, সেটের সংযোগ ও ছেদ, এবং ডোমেন ও রেঞ্জ।',
          keyFormulas: [
            '$n(A \\cup B) = n(A) + n(B) - n(A \\cap B)$'
          ],
          importantPoints: [
            '$\\sqrt{2}, \\sqrt{3}, \\sqrt{5}$ একটি অমূলদ সংখ্যা সংক্রান্ত প্রমাণ বোর্ডের নিয়মিত প্রশ্ন।'
          ],
          textbookPage: 'অধ্যায় ১ ও ২, পৃষ্ঠা ১–৩৫'
        }
      },
      {
        id: 'ch_s_m2',
        number: 2,
        titleBn: 'বীজগাণিতিক রাশি ও সমীকরণ',
        topicCount: 11,
        progressPercent: 65,
        isRevised: false,
        videoLectureId: 'lec_ssc_m02',
        summaryNotes: {
          overview: 'বর্গ ও ঘনের সূত্রাবলী, উৎপাদকে বিশ্লেষণ এবং দ্বিঘাত সমীকরণের মূল নির্ণয়।',
          keyFormulas: [
            '$(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$',
            '$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$'
          ],
          importantPoints: [
            'দ্বিঘাত সমীকরণের নিশ্চায়ক $D = b^2 - 4ac \\ge 0$ হলে মূলদ্বয় বাস্তব হবে।'
          ],
          textbookPage: 'অধ্যায় ৩ ও ৪, পৃষ্ঠা ৩৬–৭৫'
        }
      }
    ]
  }
];

export default function LearnPage() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedStage, setSelectedStage] = useState<'ALL' | 'SSC' | 'HSC' | 'ADMISSION'>('HSC');
  const [activeVideoLecture, setActiveVideoLecture] = useState<{ id: string; title: string } | null>(null);
  const [activeNotesChapter, setActiveNotesChapter] = useState<{ chapter: ChapterItem; subjectTitle: string } | null>(null);

  const filteredSubjects = selectedStage === 'ALL'
    ? CURATED_SUBJECTS
    : CURATED_SUBJECTS.filter((s) => s.stage === selectedStage);

  return (
    <>
      <AppHead
        title="এনসিটিবি পাঠ্যক্রম ও অধ্যায়ভিত্তিক শিক্ষা | অগ্রযাত্রা"
        description="এনসিটিবি কারিকুলাম অনুযায়ী শ্রেণিভিত্তিক অধ্যায়, ইন্টারেক্টিভ ভিডিও লেকচার ও স্পেসড-রিপিটিশন রিভিশন কিউ।"
        canonicalUrl="/learn"
        ogType="website"
        structuredData={createCourseSchema({
          name: "উচ্চ মাধ্যমিক পদার্থবিজ্ঞান ও গণিত",
          description: "এনসিটিবি কারিকুলাম ২০২৬ অনুযায়ী পদার্থবিজ্ঞান ও গণিতের সম্পূর্ণ পাঠ্যক্রম",
          educationalLevel: "Higher Secondary Certificate"
        })}
      />

      <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-[#1A1A1A] dark:text-slate-100 font-sans selection:bg-[#0A2540] selection:text-white transition-colors duration-200">
        {/* Sticky Unified Global Navigation */}
        <Navbar currentStage="পাঠ্যক্রম ও অধ্যায়ভিত্তিক লার্নিং" />

        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
          
          {/* Flagship Unified PageHeader */}
          <PageHeader
            category="এনসিটিবি অনুমোদিত ২০২৬ কারিকুলাম"
            title="পাঠ্যক্রম ও অধ্যায়ভিত্তিক শিক্ষা"
            subtitle="জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত পাঠ্যবই অনুযায়ী প্রতিটি বিষয়ের পুঙ্খানুপুঙ্খ অধ্যায়, ধারণাগত শিখনফল, বোর্ড প্রশ্নের সংকলন এবং রিভিশন গাইড।"
            breadcrumbs={[
              { label: 'নীড়পাতা', href: '/' },
              { label: 'পাঠ্যক্রম ও লার্নিং' }
            ]}
            stats={[
              { label: 'কভার্ড বিষয়', value: 'পদার্থ, রসায়ন, গণিত' },
              { label: 'মোট অধ্যায়', value: '২৮টি অধ্যায়' },
              { label: 'ভিডিও লেকচার', value: '১০০% এইচডি', highlight: true },
              { label: 'রিভিশন মেথড', value: 'স্পেসড-রিপিটিশন' }
            ]}
          />

          {/* Level Switcher: Unified Shared Tabs */}
          <div className="border-b border-[#E5E2DA] dark:border-slate-800 pb-1">
            <Tabs
              defaultValue={selectedStage}
              value={selectedStage}
              onValueChange={(val) => setSelectedStage(val as any)}
            >
              <TabsList className="bg-transparent border-none p-0 gap-2 sm:gap-4 flex-wrap">
                {[
                  { key: 'HSC', label: 'এইচএসসি (Class 11-12)' },
                  { key: 'SSC', label: 'এসএসসি (Class 9-10)' },
                  { key: 'ALL', label: 'সকল স্তর' },
                  { key: 'ADMISSION', label: 'বিশ্ববিদ্যালয় ভর্তি' },
                ].map((tab) => (
                  <TabsTrigger
                    key={tab.key}
                    value={tab.key}
                    className="data-[state=active]:bg-[#1B2A4A] data-[state=active]:text-white data-[state=active]:shadow-[0_4px_0_0_#051329] active:translate-y-1 min-h-[44px] px-4 py-2 rounded-lg font-bengali text-sm font-semibold transition-all border border-[#E5E2DA] dark:border-slate-800 hover:bg-[#FAF8F3] dark:hover:bg-slate-800"
                  >
                    {tab.label}
                  </TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
          </div>

          {/* Spaced-Repetition Revision Queue (আজকের রিভিশন কিউ) */}
          <Card className="border-[#E5E2DA] shadow-xs">
            <CardHeader className="border-b border-[#E5E2DA] pb-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-[#FEF9EE] flex items-center justify-center text-[#B8862B] border border-[#F6E6C2]">
                    <RotateCcw className="w-4 h-4" />
                  </div>
                  <div>
                    <CardTitle className="text-lg sm:text-xl font-bold font-bengali text-[#1B2A4A] dark:text-white">
                      স্পেসড-রিপিটিশন রিভিশন কিউ (আজকের রিভিশন তালিকা)
                    </CardTitle>
                    <p className="text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali pt-0.5">
                      বৈজ্ঞানিক ব্যবধানযুক্ত পুনরাবৃত্তি (SM-2 মডেল) অনুযায়ী বিস্মৃতি প্রতিরোধে আজকের পাঠগুলো অনুশীলন করুন
                    </p>
                  </div>
                </div>
                <Badge variant="warning" size="md">
                  ৩টি টপিক আজ বাকি
                </Badge>
              </div>
            </CardHeader>

            <CardContent className="pt-5">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-[#FAF8F3] dark:bg-slate-900 border border-[#E5E2DA] dark:border-slate-800 flex flex-col justify-between space-y-3">
                  <div>
                    <Badge variant="brand" size="sm" className="mb-2">পদার্থবিজ্ঞান ১ম পত্র</Badge>
                    <h3 className="text-sm font-bold text-[#1B2A4A] dark:text-white font-bengali">
                      নিউটনিয়ান বলবিদ্যা (ঘূর্ণন গতিশক্তি)
                    </h3>
                    <span className="text-[11px] text-[#B8862B] font-bengali mt-1 block">ব্যবধান: ৩য় দিন</span>
                  </div>
                  <Link
                    href="/practice?topic=newtonian_rotation"
                    className="text-xs font-semibold font-bengali text-[#1B2A4A] hover:underline flex items-center justify-between pt-2 border-t border-[#E5E2DA]/60"
                  >
                    <span>রিভিশন কুইজ শুরু করুন</span>
                    <ChevronRight className="w-4 h-4 text-[#B8862B]" />
                  </Link>
                </div>

                <div className="p-4 rounded-xl bg-[#FAF8F3] dark:bg-slate-900 border border-[#E5E2DA] dark:border-slate-800 flex flex-col justify-between space-y-3">
                  <div>
                    <Badge variant="success" size="sm" className="mb-2">রসায়ন ১ম পত্র</Badge>
                    <h3 className="text-sm font-bold text-[#1B2A4A] dark:text-white font-bengali">
                      কোয়ান্টাম সংখ্যা ও হুন্ডের নীতি
                    </h3>
                    <span className="text-[11px] text-[#B8862B] font-bengali mt-1 block">ব্যবধান: ৭ম দিন</span>
                  </div>
                  <Link
                    href="/practice?topic=quantum_hund"
                    className="text-xs font-semibold font-bengali text-[#0B5D3B] hover:underline flex items-center justify-between pt-2 border-t border-[#E5E2DA]/60"
                  >
                    <span>রিভিশন কুইজ শুরু করুন</span>
                    <ChevronRight className="w-4 h-4 text-[#0B5D3B]" />
                  </Link>
                </div>

                <div className="p-4 rounded-xl bg-[#FAF8F3] dark:bg-slate-900 border border-[#E5E2DA] dark:border-slate-800 flex flex-col justify-between space-y-3">
                  <div>
                    <Badge variant="default" size="sm" className="mb-2">উচ্চতর গণিত ১ম পত্র</Badge>
                    <h3 className="text-sm font-bold text-[#1B2A4A] dark:text-white font-bengali">
                      অন্তরীকরণ (ত্রিকোণমিতিক ডেরিভেটিভ)
                    </h3>
                    <span className="text-[11px] text-[#B8862B] font-bengali mt-1 block">ব্যবধান: ১৪তম দিন</span>
                  </div>
                  <Link
                    href="/practice?topic=calculus_trig"
                    className="text-xs font-semibold font-bengali text-[#1B2A4A] hover:underline flex items-center justify-between pt-2 border-t border-[#E5E2DA]/60"
                  >
                    <span>রিভিশন কুইজ শুরু করুন</span>
                    <ChevronRight className="w-4 h-4 text-[#1B2A4A]" />
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Subjects & Chapters Section */}
          {isLoading ? (
            <div className="space-y-6 animate-pulse">
              {[1, 2].map((i) => (
                <div key={i} className="p-8 rounded-2xl bg-white dark:bg-slate-900 border border-[#E5E2DA] space-y-4">
                  <div className="h-6 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="h-24 bg-[#FAF8F3] dark:bg-slate-800/60 rounded-xl"></div>
                    <div className="h-24 bg-[#FAF8F3] dark:bg-slate-800/60 rounded-xl"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-8">
              {filteredSubjects.map((sub) => (
                <Card key={sub.id} className="border-[#E5E2DA] overflow-hidden shadow-xs">
                  
                  {/* Subject Header with Progress Gauge */}
                  <CardHeader className="bg-[#FAF8F3] dark:bg-slate-900/60 border-b border-[#E5E2DA] p-5 sm:p-6">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <Badge variant="brand" size="sm">
                            {sub.stage}
                          </Badge>
                          <span className="text-xs text-[#5B5B5B] font-sans">
                            {sub.titleEn}
                          </span>
                        </div>
                        <CardTitle className="text-xl sm:text-2xl font-serif font-bold text-[#1B2A4A] dark:text-white">
                          {sub.titleBn}
                        </CardTitle>
                      </div>

                      {/* Circular Overall Subject Progress */}
                      <div className="flex items-center gap-3 self-start sm:self-auto">
                        <div className="relative w-12 h-12 shrink-0 flex items-center justify-center">
                          <svg className="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                            <path
                              className="text-slate-200 dark:text-slate-800"
                              strokeWidth="3.2"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                            <path
                              className="text-[#0A2540] dark:text-[#B8862B] transition-all duration-500"
                              strokeDasharray={`${sub.completedPercent}, 100`}
                              strokeWidth="3.2"
                              strokeLinecap="round"
                              stroke="currentColor"
                              fill="none"
                              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            />
                          </svg>
                          <span className="absolute text-xs font-sans font-bold text-[#1B2A4A] dark:text-white tabular-nums">
                            {sub.completedPercent}%
                          </span>
                        </div>

                        <div className="text-left text-xs">
                          <span className="block font-bold font-bengali text-[#1B2A4A] dark:text-white">মোট অগ্রগতি</span>
                          <span className="text-[#5B5B5B] font-bengali">{sub.chaptersCount} টি অধ্যায়</span>
                        </div>
                      </div>
                    </div>
                  </CardHeader>

                  {/* Chapters List */}
                  <CardContent className="p-5 sm:p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {sub.chapters.map((ch) => (
                        <div
                          key={ch.id}
                          className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-[#E5E2DA] dark:border-slate-800 hover:border-[#1B2A4A]/40 transition-all flex flex-col justify-between gap-3"
                        >
                          <div className="flex items-start gap-3 min-w-0">
                            {/* Circular Progress Gauge */}
                            <div className="relative w-10 h-10 shrink-0 flex items-center justify-center mt-0.5">
                              <svg className="w-10 h-10 -rotate-90" viewBox="0 0 36 36">
                                <path
                                  className="text-slate-200 dark:text-slate-800"
                                  strokeWidth="3"
                                  stroke="currentColor"
                                  fill="none"
                                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                />
                                <path
                                  className={ch.progressPercent === 100 ? 'text-[#0B5D3B]' : 'text-[#1B2A4A]'}
                                  strokeDasharray={`${ch.progressPercent}, 100`}
                                  strokeWidth="3"
                                  strokeLinecap="round"
                                  stroke="currentColor"
                                  fill="none"
                                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                />
                              </svg>
                              <span className="absolute text-[11px] font-sans font-bold text-[#1B2A4A] dark:text-slate-300">
                                {ch.number}
                              </span>
                            </div>

                            <div className="min-w-0 flex-1">
                              <div className="flex items-center gap-2">
                                <h3 className="text-sm font-bold font-bengali text-[#1B2A4A] dark:text-white truncate">
                                  {ch.titleBn}
                                </h3>
                                {ch.progressPercent === 100 && (
                                  <Badge variant="success" size="sm">সম্পন্ন</Badge>
                                )}
                              </div>
                              <span className="text-xs text-[#5B5B5B] font-bengali block pt-0.5">
                                {ch.topicCount} টি পাঠ • {ch.progressPercent}% সম্পন্ন
                              </span>
                            </div>
                          </div>

                          {/* Actions: Notes Drawer, Video Lecture & Practice */}
                          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-[#E5E2DA]/60">
                            {ch.summaryNotes && (
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => setActiveNotesChapter({ chapter: ch, subjectTitle: sub.titleBn })}
                                className="text-xs text-[#1B2A4A] min-h-[36px]"
                              >
                                <FileText className="w-3.5 h-3.5 mr-1 text-[#B8862B]" />
                                <span>পড়ুন ও নোটস</span>
                              </Button>
                            )}

                            <div className="flex items-center gap-2 ml-auto">
                              {ch.videoLectureId && (
                                <button
                                  type="button"
                                  onClick={() => setActiveVideoLecture({ id: ch.videoLectureId!, title: ch.titleBn })}
                                  className="p-2 rounded-lg bg-[#FAF8F3] dark:bg-slate-800 text-[#1B2A4A] hover:bg-[#1B2A4A] hover:text-white transition border border-[#E5E2DA] dark:border-slate-700 cursor-pointer min-h-[36px]"
                                  title="লেকচার ভিডিও দেখুন"
                                  aria-label={`লেকচার ভিডিও দেখুন: ${ch.titleBn}`}
                                >
                                  <Video className="w-4 h-4" />
                                </button>
                              )}

                              <Link
                                href={`/practice?chapter=${ch.id}`}
                                className="px-3.5 py-1.5 rounded-lg bg-[#0A2540] hover:bg-[#081c30] text-white font-bengali text-xs shadow-[0_3px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-1.5 min-h-[36px]"
                                title="অধ্যায় অনুশীলন করুন"
                                aria-label={`অনুশীলন করুন: ${ch.titleBn}`}
                              >
                                <Play className="w-3.5 h-3.5 text-[#B8862B]" />
                                <span>অনুশীলন</span>
                              </Link>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>

                </Card>
              ))}
            </div>
          )}

        </main>

        {/* Global Dignified Footer */}
        <Footer />
      </div>

      {/* Chapter Editorial Notes Drawer (60-75ch Textbook Reading Standard) */}
      <Drawer
        isOpen={!!activeNotesChapter}
        onClose={() => setActiveNotesChapter(null)}
        title={activeNotesChapter?.chapter.titleBn || ''}
        side="right"
      >
        {activeNotesChapter && (
          <div className="space-y-6 max-w-[70ch] leading-[1.8] text-[#1A1A1A] font-bengali text-sm sm:text-base">
            <div className="flex items-center gap-2 border-b border-[#E5E2DA] pb-3">
              <Badge variant="brand" size="sm">{activeNotesChapter.subjectTitle}</Badge>
              <Badge variant="default" size="sm">অধ্যায় {activeNotesChapter.chapter.number}</Badge>
              <span className="text-xs text-[#5B5B5B] ml-auto">
                {activeNotesChapter.chapter.summaryNotes?.textbookPage}
              </span>
            </div>

            <div>
              <h4 className="font-serif font-bold text-base text-[#1B2A4A] mb-2">
                ১. সারসংক্ষেপ ও শিখনফল
              </h4>
              <p className="text-[#333333] leading-relaxed">
                {activeNotesChapter.chapter.summaryNotes?.overview}
              </p>
            </div>

            {/* Flat Bordered Callout Box for Formulas */}
            <div className="bg-[#FAF8F3] border border-[#E5E2DA] rounded-xl p-4 sm:p-5 space-y-3">
              <div className="flex items-center gap-2 text-[#1B2A4A] font-bold text-sm">
                <BookmarkCheck className="w-4 h-4 text-[#B8862B]" />
                <span>প্রয়োজনীয় গাণিতিক সূত্রাবলী</span>
              </div>
              <div className="space-y-2 pt-1 font-sans">
                {activeNotesChapter.chapter.summaryNotes?.keyFormulas.map((f, idx) => (
                  <div key={idx} className="bg-white p-2.5 rounded-lg border border-[#E5E2DA] text-sm overflow-x-auto">
                    <KaTeXRenderer text={f} />
                  </div>
                ))}
              </div>
            </div>

            {/* Flat Bordered Callout for Exam Tips */}
            <div className="bg-[#F0F7F4] border border-[#CDE5DB] rounded-xl p-4 sm:p-5 space-y-2">
              <div className="flex items-center gap-2 text-[#0B5D3B] font-bold text-sm">
                <Check className="w-4 h-4" />
                <span>এনসিটিবি বোর্ড পরীক্ষার জন্য গুরুত্বপূর্ণ পর্যবেক্ষণ</span>
              </div>
              <ul className="space-y-1.5 list-disc list-inside text-sm text-[#065F46] leading-relaxed">
                {activeNotesChapter.chapter.summaryNotes?.importantPoints.map((pt, idx) => (
                  <li key={idx}>
                    <KaTeXRenderer text={pt} />
                  </li>
                ))}
              </ul>
            </div>

            {/* Drawer Actions */}
            <div className="pt-4 border-t border-[#E5E2DA] flex flex-wrap gap-3">
              <Link
                href={`/practice?chapter=${activeNotesChapter.chapter.id}`}
                className="flex-1"
              >
                <Button variant="primary" className="w-full">
                  <Play className="w-4 h-4 mr-1.5 text-[#B8862B]" />
                  <span>এই অধ্যায়ের বোর্ড প্রশ্ন অনুশীলন</span>
                </Button>
              </Link>

              {activeNotesChapter.chapter.videoLectureId && (
                <Button
                  variant="outline"
                  onClick={() => {
                    const vidId = activeNotesChapter.chapter.videoLectureId!;
                    const vidTitle = activeNotesChapter.chapter.titleBn;
                    setActiveNotesChapter(null);
                    setActiveVideoLecture({ id: vidId, title: vidTitle });
                  }}
                >
                  <Video className="w-4 h-4 mr-1.5 text-[#1B2A4A]" />
                  <span>ভিডিও লেকচার</span>
                </Button>
              )}
            </div>
          </div>
        )}
      </Drawer>

      {/* HLS Video Lecture Player Modal */}
      {activeVideoLecture && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 animate-in fade-in"
        >
          <div className="relative w-full max-w-4xl bg-white dark:bg-slate-900 rounded-2xl border border-[#E5E2DA] shadow-xl overflow-hidden flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#E5E2DA] bg-[#FAF8F3] dark:bg-slate-950/60">
              <div className="flex items-center gap-2">
                <Video className="w-5 h-5 text-[#1B2A4A]" />
                <span className="font-bold font-bengali text-[#1B2A4A] dark:text-white text-sm sm:text-base">
                  {activeVideoLecture.title} (HLS Adaptive Stream)
                </span>
              </div>
              <button
                type="button"
                onClick={() => setActiveVideoLecture(null)}
                aria-label="ভিডিও বন্ধ করুন"
                className="p-2 rounded-lg bg-white dark:bg-slate-800 text-[#5B5B5B] hover:text-[#1A1A1A] hover:bg-[#FAF8F3] transition border border-[#E5E2DA] cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 sm:p-6">
              <HlsLecturePlayer
                lectureId={activeVideoLecture.id}
                studentId="std_curr_user"
                titleBn={activeVideoLecture.title}
                durationSeconds={480}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
