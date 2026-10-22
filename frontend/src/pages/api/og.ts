/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Grand Public Production Launch & System Handover
 * TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
 * FILE:      frontend/src/pages/api/og.ts
 * PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
 * PURPOSE:   High-performance dynamic 1200x630 vector OpenGraph card generator for all 64 districts
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
 */

import type { NextApiRequest, NextApiResponse } from "next";
import { getDistrictById } from "../../lib/districts";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { district } = req.query;
  const districtKey = typeof district === "string" ? district : "dhaka";
  const districtInfo = getDistrictById(districtKey) || {
    id: "national",
    nameEn: "Bangladesh National Hub",
    nameBn: "বাংলাদেশ জাতীয় প্ল্যাটফর্ম",
    division: "Dhaka",
    activeLearners: 1250000,
    topExamStream: "এসএসসি, এইচএসসি ও ভর্তি পরীক্ষা"
  };

  const svgCard = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="630" viewBox="0 0 1200 630" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1200" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0B132B" />
      <stop offset="60%" stop-color="#090E1F" />
      <stop offset="100%" stop-color="#050811" />
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="0" x2="400" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#06B6D4" />
      <stop offset="100%" stop-color="#3B82F6" />
    </linearGradient>
    <linearGradient id="accentBorder" x1="0" y1="0" x2="1200" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1E293B" />
      <stop offset="50%" stop-color="#0284C7" />
      <stop offset="100%" stop-color="#1E293B" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bgGrad)" />
  <rect x="2" y="2" width="1196" height="626" rx="20" stroke="url(#accentBorder)" stroke-width="3" fill="none" />

  <!-- Ambient Grid Glows -->
  <circle cx="1050" cy="150" r="280" fill="#0284C7" fill-opacity="0.08" />
  <circle cx="150" cy="500" r="220" fill="#06B6D4" fill-opacity="0.05" />

  <!-- Header Banner -->
  <g transform="translate(80, 80)">
    <!-- Platform Emblem / Vector Shield -->
    <rect width="56" height="56" rx="14" fill="#0284C7" fill-opacity="0.15" stroke="#0284C7" stroke-width="2" />
    <path d="M28 14L40 19V30C40 37.5 34.5 44 28 46C21.5 44 16 37.5 16 30V19L28 14Z" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-linejoin="round" />
    <path d="M23 29L27 33L34 25" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />

    <!-- Brand Typography -->
    <text x="74" y="28" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="22" fill="#F8FAFC" letter-spacing="1">
      STUDENT LIFE CIRCLE
    </text>
    <text x="74" y="48" font-family="'Hind Siliguri', sans-serif" font-weight="600" font-size="16" fill="#38BDF8">
      অগ্রযাত্রা • বাংলাদেশের জাতীয় পরীক্ষা প্রস্তুতি ও লার্নিং প্ল্যাটফর্ম
    </text>
  </g>

  <!-- Main District Card Body -->
  <g transform="translate(80, 220)">
    <!-- Regional Pill Badge -->
    <rect width="220" height="36" rx="18" fill="#1E293B" stroke="#334155" stroke-width="1.5" />
    <circle cx="18" cy="18" r="5" fill="#10B981" />
    <text x="32" y="23" font-family="'Hind Siliguri', sans-serif" font-weight="600" font-size="14" fill="#94A3B8">
      বিভাগ: ${districtInfo.division}
    </text>

    <!-- District Name Headline in Authentic Bengali & English -->
    <text x="0" y="105" font-family="'Hind Siliguri', sans-serif" font-weight="700" font-size="64" fill="#FFFFFF">
      ${districtInfo.nameBn} জেলা
    </text>
    <text x="0" y="150" font-family="'Plus Jakarta Sans', sans-serif" font-weight="600" font-size="26" fill="#64748B" letter-spacing="0.5">
      ${districtInfo.nameEn} District Academic Hub
    </text>

    <!-- Focus Exam Stream -->
    <g transform="translate(0, 195)">
      <rect width="700" height="48" rx="12" fill="#0F172A" stroke="#1E293B" stroke-width="1.5" />
      <text x="24" y="30" font-family="'Hind Siliguri', sans-serif" font-weight="500" font-size="18" fill="#E2E8F0">
        শীর্ষ প্রস্তুতি: ${districtInfo.topExamStream}
      </text>
    </g>
  </g>

  <!-- Statistics Panel (Right Side) -->
  <g transform="translate(820, 240)">
    <rect width="300" height="190" rx="20" fill="#0F172A" stroke="#1E293B" stroke-width="2" />
    <text x="30" y="50" font-family="'Hind Siliguri', sans-serif" font-weight="600" font-size="16" fill="#94A3B8">
      নিবন্ধিত শিক্ষার্থী
    </text>
    <text x="30" y="105" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="44" fill="#38BDF8">
      ${districtInfo.activeLearners.toLocaleString()}+
    </text>
    <line x1="30" y1="125" x2="270" y2="125" stroke="#1E293B" stroke-width="1.5" />
    <text x="30" y="158" font-family="'Hind Siliguri', sans-serif" font-weight="500" font-size="14" fill="#10B981">
      সক্রিয় স্টাডি পড ও টিউটর নেটওয়ার্ক
    </text>
  </g>

  <!-- Footer Verification & Trust Bar -->
  <g transform="translate(80, 560)">
    <line x1="0" y1="0" x2="1040" y2="0" stroke="#1E293B" stroke-width="1.5" />
    <text x="0" y="30" font-family="'Hind Siliguri', sans-serif" font-weight="500" font-size="14" fill="#64748B">
      NCTB অনুমোদিত কারিকুলাম • বাংলা মিডিয়াম ও ইংলিশ ভার্সন • ২৪ ঘণ্টার ডিজিটাল এসক্রো
    </text>
    <text x="1040" y="30" text-anchor="end" font-family="'Plus Jakarta Sans', sans-serif" font-weight="600" font-size="14" fill="#38BDF8">
      studentlifecircle.com
    </text>
  </g>
</svg>`;

  res.setHeader("Content-Type", "image/svg+xml; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=86400, s-maxage=604800, stale-while-revalidate");
  return res.status(200).send(svgCard);
}
