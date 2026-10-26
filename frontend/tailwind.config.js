/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Next.js 15+ Tailwind CSS Production Configuration
 * TOPIC:     Master Academic UI & Pro Tactile Button Elevation
 * FILE:      frontend/tailwind.config.js
 * PHASE:     Phase 110 - Pure Academic Visual Design Elevation & Phase 123 - Master Academic UI & Pro Tactile Button Elevation
 * PURPOSE:   Elevates every button, card, background, and header to Duolingo/Brilliant-grade
 *            3D physical press physics, Oxford Academic Navy palette, and zero AI vibe.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/modules/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        ground: '#F8FAFC',
        oxford: {
          50: '#F0F4F8',
          100: '#D9E2EC',
          800: '#0E3357',
          900: '#0A2540',
          950: '#051329',
        },
        emerald: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          700: '#047857',
          800: '#065F46',
          900: '#044332',
        },
        scholar: {
          gold: '#B45309',
          light: '#FDE68A',
        },
        paper: {
          ground: '#FAF8F3',
          surface: '#FFFFFF',
          muted: '#F5F2EB',
          hover: '#EFECE3',
          white: '#FFFFFF',
          ivory: '#FAFAF8',
        },
        ink: {
          primary: '#1A1A1A',
          muted: '#5B5B5B',
          faint: '#787878',
          slate: '#0B132B',
        },
        hairline: '#E5E2DA',
        burgundy: {
          crimson: '#991B1B',
        },
        primary: {
          50: '#F8FAFC',
          100: '#F1F5F9',
          200: '#E2E8F0',
          800: '#1E293B',
          900: '#0F172A',
          950: '#020617',
        },
        brand: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          900: '#0A2540',
        },
        teal: {
          50: '#F0FDFA',
          100: '#CCFBF1',
          500: '#14B8A6',
          600: '#0D9488',
          700: '#0F766E',
        },
        mastery: {
          50: '#F0FDFA',
          100: '#CCFBF1',
          500: '#14B8A6',
          600: '#0D9488',
          700: '#0F766E',
          800: '#065F46',
        },
        amber: {
          50: '#FFFBEB',
          100: '#FEF3C7',
          500: '#F59E0B',
          600: '#D97706',
          700: '#B45309',
        },
        warning: {
          50: '#FFFBEB',
          100: '#FEF3C7',
          500: '#F59E0B',
          600: '#D97706',
          700: '#B45309',
        },
        red: {
          50: '#FEF2F2',
          100: '#FEE2E2',
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
          800: '#991B1B',
        },
        danger: {
          50: '#FEF2F2',
          100: '#FEE2E2',
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
          800: '#991B1B',
        },
      },
      fontFamily: {
        sans: ['Hind Siliguri', 'Inter', 'Noto Sans Bengali', 'system-ui', '-apple-system', 'sans-serif'],
        'serif-bengali': ['"Noto Serif Bengali"', '"Tiro Bangla"', 'serif'],
        'serif-english': ['"Source Serif 4"', 'Lora', 'Georgia', 'serif'],
        'sans-bengali': ['"Hind Siliguri"', '"Noto Sans Bengali"', 'system-ui', 'sans-serif'],
        'sans-english': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['"Noto Serif Bengali"', '"Source Serif 4"', 'Plus Jakarta Sans', 'serif'],
        bengali: ['Hind Siliguri', 'Noto Sans Bengali', 'sans-serif'],
        tabular: ['Inter', 'monospace'],
      },
      minHeight: {
        'touch': '44px',
        'touch-lg': '48px',
      },
      minWidth: {
        'touch': '44px',
        'touch-lg': '48px',
      },
      boxShadow: {
        'paper': '0 1px 3px rgba(10, 37, 64, 0.05), 0 1px 2px rgba(10, 37, 64, 0.03)',
        'paper-elevated': '0 4px 12px -2px rgba(10, 37, 64, 0.08), 0 2px 4px -1px rgba(10, 37, 64, 0.04)',
        'ambient': '0 1px 3px rgba(10, 37, 64, 0.05), 0 12px 28px -4px rgba(10, 37, 64, 0.06)',
        'ambient-lg': '0 4px 6px -1px rgba(10, 37, 64, 0.06), 0 20px 36px -4px rgba(10, 37, 64, 0.08)',
        'tactile-oxford': '0 4px 0 0 #051329',
        'tactile-emerald': '0 4px 0 0 #044332',
        'tactile-forest': '0 4px 0 0 #033829',
        'tactile-brand': '0 4px 0 0 #051329',
        'tactile-teal': '0 4px 0 0 #044332',
        'tactile-pressed': '0 0 0 0 transparent, 0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [],
};
