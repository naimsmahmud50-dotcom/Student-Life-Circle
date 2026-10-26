/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Academic Editorial Design System
 * TOPIC:     Phase 142 Live MCQ 2D Elevation & Academic Hero Motif
 * FILE:      frontend/src/components/live-challenge/AcademicHeroMotif2D.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Vector SVG 2D academic composition: Armillary Celestial Sphere,
 *            concentric STEM planetary orbits, scholar astrolabe quadrant, and open folio.
 *            Acts as the primary 2D editorial composition and the zero-CLS fallback
 *            when 3D WebGL rendering is disabled or unavailable.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React from 'react';

interface AcademicHeroMotif2DProps {
  className?: string;
  size?: number;
}

export function AcademicHeroMotif2D({
  className = '',
  size = 380
}: AcademicHeroMotif2DProps) {
  return (
    <div
      className={`relative flex items-center justify-center select-none ${className}`}
      style={{ width: size, height: size }}
      role="img"
      aria-label="একাডেমিক আর্মিলেয়ারি স্ফিয়ার ও বিজ্ঞান কোয়াড্রান্ট মোটিফ"
    >
      <svg
        viewBox="0 0 400 400"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full drop-shadow-xl"
        preserveAspectRatio="xMidYMid meet"
      >
        <defs>
          {/* Subtle parchment and metal tones */}
          <radialGradient id="celestialCore" cx="200" cy="200" r="160" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#1E3A5F" stopOpacity="0.45" />
            <stop offset="70%" stopColor="#0A2540" stopOpacity="0.15" />
            <stop offset="100%" stopColor="#07192F" stopOpacity="0" />
          </radialGradient>

          {/* Scholar Ochre stroke gradient */}
          <linearGradient id="ochreBand" x1="60" y1="60" x2="340" y2="340" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#D97706" />
            <stop offset="50%" stopColor="#F59E0B" />
            <stop offset="100%" stopColor="#B45309" />
          </linearGradient>

          {/* Academic Steel hairline */}
          <linearGradient id="steelHairline" x1="200" y1="40" x2="200" y2="360" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#94A3B8" stopOpacity="0.6" />
            <stop offset="50%" stopColor="#CBD5E1" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#64748B" stopOpacity="0.5" />
          </linearGradient>
        </defs>

        {/* 1. Ambient Celestial Core Aura (Subtle & Academic, not neon) */}
        <circle cx="200" cy="200" r="150" fill="url(#celestialCore)" />

        {/* 2. Outer Horizon Ring with Degree Hash Marks */}
        <circle
          cx="200"
          cy="200"
          r="165"
          stroke="#475569"
          strokeWidth="1.5"
          strokeDasharray="2 6"
          opacity="0.6"
        />
        <circle
          cx="200"
          cy="200"
          r="156"
          stroke="#94A3B8"
          strokeWidth="1"
          opacity="0.4"
        />

        {/* 3. Outer Astronomical Coordinate Degree Ticks */}
        {Array.from({ length: 24 }).map((_, i) => {
          const angle = (i * 360) / 24;
          const rad = (angle * Math.PI) / 180;
          const x1 = 200 + 158 * Math.cos(rad);
          const y1 = 200 + 158 * Math.sin(rad);
          const x2 = 200 + 165 * Math.cos(rad);
          const y2 = 200 + 165 * Math.sin(rad);
          return (
            <line
              key={`tick-${i}`}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke={i % 6 === 0 ? "#F59E0B" : "#64748B"}
              strokeWidth={i % 6 === 0 ? "1.75" : "1"}
              opacity={i % 6 === 0 ? "0.9" : "0.5"}
            />
          );
        })}

        {/* 4. Solstitial Colure & Polar Meridian Rings */}
        <ellipse
          cx="200"
          cy="200"
          rx="140"
          ry="140"
          stroke="url(#steelHairline)"
          strokeWidth="1.75"
        />
        <ellipse
          cx="200"
          cy="200"
          rx="68"
          ry="140"
          stroke="#94A3B8"
          strokeWidth="1.25"
          strokeDasharray="6 4"
          opacity="0.75"
        />

        {/* 5. Tilted Ecliptic Band with Scholar Ochre Trim */}
        <g transform="rotate(-23.5 200 200)">
          <ellipse
            cx="200"
            cy="200"
            rx="144"
            ry="48"
            stroke="url(#ochreBand)"
            strokeWidth="2.25"
          />
          <ellipse
            cx="200"
            cy="200"
            rx="140"
            ry="44"
            stroke="#D97706"
            strokeWidth="0.8"
            strokeDasharray="4 4"
            opacity="0.8"
          />
          {/* Ecliptic Graduation Points */}
          <circle cx="60" cy="200" r="3" fill="#F59E0B" />
          <circle cx="340" cy="200" r="3" fill="#F59E0B" />
          <circle cx="200" cy="154" r="2.5" fill="#F59E0B" />
          <circle cx="200" cy="246" r="2.5" fill="#F59E0B" />
        </g>

        {/* 6. Celestial Equatorial Plane Ring */}
        <ellipse
          cx="200"
          cy="200"
          rx="140"
          ry="32"
          stroke="#64748B"
          strokeWidth="1.2"
          strokeDasharray="3 3"
          opacity="0.65"
        />

        {/* 7. Polar Axis Pointer with Engraved Finials */}
        <line
          x1="200"
          y1="38"
          x2="200"
          y2="362"
          stroke="#CBD5E1"
          strokeWidth="1.5"
          strokeDasharray="12 4"
        />
        {/* North Celestial Pivot Finial */}
        <polygon points="200,28 195,44 205,44" fill="#F59E0B" />
        <circle cx="200" cy="48" r="3.5" fill="#0A2540" stroke="#F59E0B" strokeWidth="1.5" />
        {/* South Celestial Pivot Finial */}
        <circle cx="200" cy="352" r="3.5" fill="#0A2540" stroke="#94A3B8" strokeWidth="1.5" />
        <polygon points="200,372 195,356 205,356" fill="#64748B" />

        {/* 8. Concentric STEM Knowledge Orbits */}
        <ellipse
          cx="200"
          cy="200"
          rx="96"
          ry="38"
          transform="rotate(35 200 200)"
          stroke="#38BDF8"
          strokeWidth="1.2"
          opacity="0.5"
        />
        <ellipse
          cx="200"
          cy="200"
          rx="96"
          ry="38"
          transform="rotate(-55 200 200)"
          stroke="#34D399"
          strokeWidth="1.2"
          opacity="0.5"
        />

        {/* 9. Central Radiant Star of Scholarship & Scientific Truth */}
        <g transform="translate(200, 200)">
          {/* Central Core Globe */}
          <circle cx="0" cy="0" r="16" fill="#0A2540" stroke="#F59E0B" strokeWidth="2" />
          <circle cx="0" cy="0" r="10" fill="#B45309" opacity="0.6" />
          <circle cx="0" cy="0" r="4" fill="#FEF3C7" />

          {/* 8-Pointed Navigator Compass Star */}
          <polygon points="0,-22 4,-8 18,-8 7,1 11,15 0,6 -11,15 -7,1 -18,-8 -4,-8" fill="#F59E0B" opacity="0.9" />
        </g>

        {/* 10. Open Scholar Folio Base (এনসিটিবি পাঠ্যপুস্তক ও পাণ্ডুলিপি রূপরেখা) */}
        <g transform="translate(130, 290)">
          {/* Left Page */}
          <path
            d="M 70 42 C 45 36, 15 42, 0 46 L 0 82 C 18 78, 48 72, 70 78 Z"
            fill="#0F243E"
            stroke="#94A3B8"
            strokeWidth="1.25"
          />
          {/* Left Page Script Lines */}
          <line x1="12" y1="56" x2="58" y2="50" stroke="#64748B" strokeWidth="1" strokeDasharray="4 2" />
          <line x1="12" y1="64" x2="58" y2="58" stroke="#64748B" strokeWidth="1" strokeDasharray="4 2" />
          <line x1="12" y1="72" x2="52" y2="66" stroke="#64748B" strokeWidth="1" strokeDasharray="4 2" />

          {/* Right Page */}
          <path
            d="M 70 42 C 95 36, 125 42, 140 46 L 140 82 C 122 78, 92 72, 70 78 Z"
            fill="#0F243E"
            stroke="#94A3B8"
            strokeWidth="1.25"
          />
          {/* Right Page Script Lines */}
          <line x1="82" y1="50" x2="128" y2="56" stroke="#64748B" strokeWidth="1" strokeDasharray="4 2" />
          <line x1="82" y1="58" x2="128" y2="64" stroke="#64748B" strokeWidth="1" strokeDasharray="4 2" />
          <line x1="88" y1="66" x2="128" y2="72" stroke="#64748B" strokeWidth="1" strokeDasharray="4 2" />

          {/* Spine Binding */}
          <line x1="70" y1="42" x2="70" y2="78" stroke="#F59E0B" strokeWidth="2" />
        </g>

        {/* 11. Subtle Archimedean Spiral Arcs & Cartesian Grid Calibration */}
        <path
          d="M 70 200 A 130 130 0 0 1 200 70"
          stroke="#475569"
          strokeWidth="0.8"
          strokeDasharray="2 4"
          opacity="0.4"
        />
        <path
          d="M 330 200 A 130 130 0 0 1 200 330"
          stroke="#475569"
          strokeWidth="0.8"
          strokeDasharray="2 4"
          opacity="0.4"
        />
      </svg>
    </div>
  );
}
