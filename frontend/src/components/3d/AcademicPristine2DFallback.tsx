/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Pristine 2D Layered Academic Monograph & Armillary Graphic
 * FILE:      frontend/src/components/3d/AcademicPristine2DFallback.tsx
 * PURPOSE:   Provides an exquisitely crafted 2D vector fallback matching the 3D scene:
 *            - Completely identical bounding box and aspect ratio (Zero CLS).
 *            - Layered SVG celestial meridian, ecliptic zodiac angle, and latitude rings.
 *            - Bangladesh celestial beacon coordinate indicator (23.68° N, 90.35° E).
 *            - Warm parchment and Oxford navy ink palette.
 *            - Zero WebGL overhead, instantaneous SSR and low-end device rendering.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Zero-CLS Architecture.
 */

import React from 'react';

interface AcademicPristine2DFallbackProps {
  size?: number;
  className?: string;
  badgeLabel?: string;
}

export const AcademicPristine2DFallback: React.FC<AcademicPristine2DFallbackProps> = ({
  size = 280,
  className = '',
  badgeLabel = 'একাডেমিক মনোগ্রাফ ও মহাজাগতিক গ্লোব',
}) => {
  return (
    <div
      style={{ width: size, height: size }}
      className={`relative flex items-center justify-center rounded-2xl bg-[#F6F4EE] dark:bg-[#101826] border border-[#E2DDD3] dark:border-[#263147] shadow-paper-sm overflow-hidden select-none ${className}`}
      aria-label="একাডেমিক গোলক ও মহাজাগতিক পরিমাপক নকশা"
    >
      {/* Background Subtle Ruled Astrolabe Grid */}
      <svg
        className="absolute inset-0 w-full h-full opacity-40 dark:opacity-25 pointer-events-none"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 280 280"
        fill="none"
      >
        <circle cx="140" cy="140" r="120" stroke="currentColor" strokeWidth="0.75" strokeDasharray="3 3" className="text-[#0A2540] dark:text-[#A8B7D8]" />
        <circle cx="140" cy="140" r="95" stroke="currentColor" strokeWidth="0.75" className="text-[#0A2540] dark:text-[#A8B7D8]" />
        <circle cx="140" cy="140" r="65" stroke="currentColor" strokeWidth="0.5" strokeDasharray="2 2" className="text-[#0A2540] dark:text-[#A8B7D8]" />
        <line x1="20" y1="140" x2="260" y2="140" stroke="currentColor" strokeWidth="0.75" className="text-[#0A2540] dark:text-[#A8B7D8]" />
        <line x1="140" y1="20" x2="140" y2="260" stroke="currentColor" strokeWidth="0.75" className="text-[#0A2540] dark:text-[#A8B7D8]" />
        
        {/* Tilted Ecliptic Axis Line (23.5 degrees) */}
        <line x1="45" y1="235" x2="235" y2="45" stroke="currentColor" strokeWidth="1" strokeDasharray="4 2" className="text-emerald-800 dark:text-emerald-400" />
      </svg>

      {/* Layered Celestial Armillary Vector */}
      <svg
        className="w-[85%] h-[85%] relative z-10 transition-transform duration-500 ease-out"
        viewBox="0 0 240 240"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Turned Pedestal Base */}
        <path
          d="M80 216 L160 216 C160 210 152 206 145 204 L145 185 C145 182 142 180 140 180 C138 180 135 182 135 185 L135 204 C128 206 120 210 120 216 Z"
          fill="#0A2540"
          className="dark:fill-[#1B2A4A]"
        />
        <rect x="70" y="216" width="100" height="8" rx="3" fill="#0A2540" className="dark:fill-[#1B2A4A]" />

        {/* Scholar's Stacked Folio Treatises at Base */}
        <path
          d="M75 198 L165 198 L160 206 L70 206 Z"
          fill="#8B5A2B"
          stroke="#5C3A1E"
          strokeWidth="0.75"
        />
        <path
          d="M78 200 L162 200 L158 204 L74 204 Z"
          fill="#FAF8F3"
          className="dark:fill-[#E2DDD3]"
        />

        {/* Outer Brass Meridian Ring */}
        <circle
          cx="120"
          cy="110"
          r="75"
          stroke="#0A2540"
          strokeWidth="4"
          className="dark:stroke-[#A8B7D8]"
        />
        <circle
          cx="120"
          cy="110"
          r="71"
          stroke="#B48234"
          strokeWidth="1.25"
        />

        {/* Equatorial Celestial Ring (Elliptical) */}
        <ellipse
          cx="120"
          cy="110"
          rx="72"
          ry="24"
          stroke="#B48234"
          strokeWidth="2.5"
          strokeDasharray="1 0"
        />

        {/* Tilted Ecliptic Solstice Band */}
        <g transform="rotate(-23.5 120 110)">
          <ellipse
            cx="120"
            cy="110"
            rx="70"
            ry="20"
            stroke="#065F46"
            strokeWidth="3"
            className="dark:stroke-emerald-400"
          />
        </g>

        {/* Inner Terrestrial Sphere */}
        <circle
          cx="120"
          cy="110"
          r="38"
          fill="#F0EDE6"
          stroke="#0A2540"
          strokeWidth="1.5"
          className="dark:fill-[#172030] dark:stroke-[#A8B7D8]"
        />

        {/* Sphere Latitude/Longitude Curves */}
        <ellipse cx="120" cy="110" rx="38" ry="14" stroke="#0A2540" strokeWidth="0.75" className="dark:stroke-[#CBD5E1]" />
        <ellipse cx="120" cy="110" rx="14" ry="38" stroke="#0A2540" strokeWidth="0.75" className="dark:stroke-[#CBD5E1]" />

        {/* Sovereign Bangladesh Coordinate Beacon (23.68° N, 90.35° E) */}
        <g transform="translate(136, 96)">
          <circle cx="0" cy="0" r="4.5" fill="#065F46" className="dark:fill-emerald-400 animate-ping opacity-75" />
          <circle cx="0" cy="0" r="3" fill="#065F46" className="dark:fill-emerald-400" />
          <circle cx="0" cy="0" r="1" fill="#FFFFFF" />
        </g>
      </svg>

      {/* Institutional Metadata Pill */}
      <div className="absolute bottom-2.5 inset-x-3 flex items-center justify-between text-[10px] font-mono font-bold text-[#0A2540] dark:text-[#E8EFF8] bg-[#FAF8F5]/90 dark:bg-[#0C1422]/90 backdrop-blur-xs px-2.5 py-1 rounded-md border border-[#E2DDD3] dark:border-[#263147] z-20">
        <span>২৩°৪১′ উত্তর</span>
        <span className="text-emerald-700 dark:text-emerald-400">৯০°২১′ পূর্ব</span>
      </div>
    </div>
  );
};
