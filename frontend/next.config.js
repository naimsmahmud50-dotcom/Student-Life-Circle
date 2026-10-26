/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - PRODUCTION PERFORMANCE & SECURITY CONFIGURATION:
 * MODULE:    Next.js 15+ Advanced Performance Tuning & Core Web Vitals Optimization
 * TOPIC:     Brotli Compression, AVIF/WebP Image Pipeline, Tree-Shaking & Static Cache Headers
 * FILE:      frontend/next.config.js
 * PURPOSE:   Configures Next.js production runtime for ultra-fast rendering on Bangladeshi
 *            2G/3G/4G networks. Enables Brotli compression (`compress: true`), modern AVIF/WebP
 *            image pipelines with responsive device viewports, tree-shaking via
 *            `optimizePackageImports` (for Lucide-React icon sets), strict
 *            immutable caching for static chunks, and OWASP ASVS L2 security headers.
 * AUDIENCE:  Frontend Architects, DevOps Engineers, Core Web Vitals Reviewers & Security Auditors
 * STANDARDS: Core Web Vitals (LCP < 1.2s, INP < 100ms, CLS = 0), Strict Zero-Emoji Policy
 * ========================================================================================
 */

/** @type {import('next').NextConfig} */
const nextConfig = {
  /* Standalone build output for ultra-lightweight Docker containers (< 120MB) */
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,

  /* Enable Brotli and Gzip compression across all SSR responses and static chunks */
  compress: true,

  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? { exclude: ['error', 'warn'] } : false,
  },

  /* Modern next-gen image optimization pipeline */
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [360, 412, 640, 768, 1024, 1280, 1536],
    imageSizes: [16, 32, 48, 64, 96, 128, 256],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days immutable cache
  },

  /* Aggressive module tree-shaking and package import optimization */
  experimental: {
    optimizePackageImports: [
      'lucide-react',
    ],
  },

  /* Security and Performance HTTP Response Headers */
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          ...(process.env.NODE_ENV !== 'production'
            ? [
                {
                  key: 'Clear-Site-Data',
                  value: '"cache"',
                },
              ]
            : []),
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), payment=()',
          },
        ],
      },
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, no-cache, must-revalidate, proxy-revalidate',
          },
          {
            key: 'Pragma',
            value: 'no-cache',
          },
          {
            key: 'Expires',
            value: '0',
          },
        ],
      },
      {
        source: '/sw.js',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, no-cache, must-revalidate',
          },
          {
            key: 'Clear-Site-Data',
            value: '"cache", "storage"',
          },
        ],
      },
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: process.env.NODE_ENV === 'production'
              ? 'public, max-age=31536000, immutable'
              : 'no-store, no-cache, must-revalidate',
          },
        ],
      },
      {
        source: '/manifest.json',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400, stale-while-revalidate=604800',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
