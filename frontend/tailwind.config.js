/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Next.js 15+ Tailwind CSS Production Configuration
 * TOPIC:     Master Academic UI & Bengal Academic Editorial Design System
 * FILE:      frontend/tailwind.config.js
 * PURPOSE:   Configures theme extension for:
 *            - Semantic academic colors (Oxford Navy, Forest Emerald, Scholar Gold, Burgundy Crimson)
 *            - Warm Paper ground (#FAF8F3) and surfaces (#FDFCF9 / #171E2C)
 *            - Disciplined radius scale (6-12px, zero pill card abuse)
 *            - Tactile 3D physical shadows and layered soft paper elevations
 *            - Z-index tokens and typography pairings
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
        ground: '#FAF8F3',
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
          700: '#087858',
          800: '#065F46',
          900: '#044332',
          950: '#033829',
        },
        scholar: {
          gold: '#B45309',
          hover: '#92400E',
          depth: '#78350F',
          light: '#FEF9EE',
          border: '#F5E5C4',
        },
        paper: {
          ground: '#FAF8F3',
          surface: '#FDFCF9',
          muted: '#F5F2EB',
          hover: '#EFECE3',
          inset: '#F2EFE8',
          white: '#FDFCF9',
          ivory: '#FAF8F3',
        },
        ink: {
          primary: '#1A1A1A',
          muted: '#525252',
          faint: '#737373',
          slate: '#0B132B',
          inverse: '#FDFCF9',
        },
        hairline: '#E5E2DA',
        burgundy: {
          crimson: '#991B1B',
          hover: '#7F1D1D',
          depth: '#5B1010',
          tint: '#FDF2F2',
          border: '#F8D2D2',
        },
        primary: {
          50: '#F0F4F8',
          100: '#D9E2EC',
          200: '#B8C9DC',
          800: '#0E3357',
          900: '#0A2540',
          950: '#051329',
        },
        brand: {
          50: '#EEF2F6',
          100: '#D9E2EC',
          500: '#1B2A4A',
          600: '#121E36',
          700: '#0E3357',
          900: '#0A2540',
        },
        teal: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          500: '#065F46',
          600: '#087858',
          700: '#044332',
        },
        mastery: {
          50: '#F0F7F4',
          100: '#C8E3D7',
          500: '#0B5D3B',
          600: '#065F46',
          700: '#087858',
          800: '#033829',
        },
        amber: {
          50: '#FEF9EE',
          100: '#F5E5C4',
          500: '#D97706',
          600: '#B45309',
          700: '#92400E',
        },
        warning: {
          50: '#FEF9EE',
          100: '#F5E5C4',
          500: '#D97706',
          600: '#B45309',
          700: '#78350F',
        },
        red: {
          50: '#FDF2F2',
          100: '#F8D2D2',
          500: '#EF4444',
          600: '#DC2626',
          700: '#B91C1C',
          800: '#991B1B',
        },
        danger: {
          50: '#FDF2F2',
          100: '#F8D2D2',
          500: '#991B1B',
          600: '#7F1D1D',
          700: '#5B1010',
          800: '#450A0A',
        },
      },
      borderRadius: {
        xs: '4px',
        sm: '6px',
        md: '8px',
        lg: '10px',
        xl: '12px',
        '2xl': '16px',
      },
      fontFamily: {
        sans: ['Hind Siliguri', 'Inter', 'Noto Sans Bengali', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        'serif-bengali': ['"Noto Serif Bengali"', '"Tiro Bangla"', '"Source Serif 4"', 'Georgia', 'serif'],
        'serif-english': ['"Source Serif 4"', 'Lora', 'Georgia', '"Times New Roman"', 'serif'],
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
        'paper-xs': '0 1px 2px rgba(10, 37, 64, 0.04)',
        'paper-sm': '0 1px 3px rgba(10, 37, 64, 0.05), 0 1px 2px rgba(0, 0, 0, 0.02)',
        'paper-md': '0 4px 8px -2px rgba(10, 37, 64, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
        'paper-lg': '0 10px 20px -3px rgba(10, 37, 64, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04)',
        'paper-xl': '0 20px 25px -5px rgba(10, 37, 64, 0.10), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
        'paper': '0 1px 3px rgba(10, 37, 64, 0.05), 0 1px 2px rgba(0, 0, 0, 0.02)',
        'paper-elevated': '0 4px 8px -2px rgba(10, 37, 64, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
        'ambient': '0 1px 3px rgba(10, 37, 64, 0.05), 0 1px 2px rgba(0, 0, 0, 0.02)',
        'ambient-lg': '0 4px 8px -2px rgba(10, 37, 64, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
        'tactile-oxford': '0 4px 0 0 #051329, 0 2px 4px rgba(10, 37, 64, 0.12)',
        'tactile-emerald': '0 4px 0 0 #033829, 0 2px 4px rgba(6, 95, 70, 0.12)',
        'tactile-forest': '0 4px 0 0 #033829, 0 2px 4px rgba(6, 95, 70, 0.12)',
        'tactile-gold': '0 4px 0 0 #78350F, 0 2px 4px rgba(180, 83, 9, 0.12)',
        'tactile-danger': '0 4px 0 0 #5B1010, 0 2px 4px rgba(153, 27, 27, 0.12)',
        'tactile-outline': '0 3px 0 0 #D1CDC4, 0 1px 2px rgba(0, 0, 0, 0.04)',
        'tactile-pressed': '0 0 0 0 transparent',
      },
      zIndex: {
        dropdown: '50',
        sticky: '100',
        overlay: '200',
        modal: '300',
        popover: '400',
        toast: '500',
        tooltip: '600',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'academic': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'press': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
    },
  },
  plugins: [],
};
