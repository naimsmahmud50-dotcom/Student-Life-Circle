/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Lazy-Loaded Progressive 3D Academic Scene Container
 * FILE:      frontend/src/components/3d/LazyAcademic3DScene.tsx
 * PURPOSE:   Master progressive enhancement wrapper for academic 3D scenes:
 *            1. Client-only dynamic chunk import with Suspense + Error Boundary.
 *            2. Capability Gate: Never loads Three.js chunk if device is low-end,
 *               save-data is active, connection is 2G/3G, or user prefers reduced motion.
 *            3. Zero CLS: Exactly preserved dimensions and aspect ratio.
 *            4. Optional ParallaxDepthContainer wrapping for weighted physical presence.
 *            5. Integrated Academic3DToggle controller.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Sub-400KB Chunk, Zero CLS.
 */

import React, { Suspense } from 'react';
import dynamic from 'next/dynamic';
import { use3DCapability } from './use3DCapability';
import { AcademicPristine2DFallback } from './AcademicPristine2DFallback';
import { Academic3DErrorBoundary } from './Academic3DErrorBoundary';
import { ParallaxDepthContainer } from './ParallaxDepthContainer';
import { Academic3DToggle } from './Academic3DToggle';

// Dynamic client-only chunk for Three.js scene
const AcademicScholarGlobe3D = dynamic(
  () => import('./AcademicScholarGlobe3D'),
  {
    ssr: false,
    loading: () => <AcademicPristine2DFallback size={280} />,
  }
);

interface LazyAcademic3DSceneProps {
  size?: number;
  className?: string;
  showToggle?: boolean;
  enableParallax?: boolean;
  badgeLabel?: string;
}

export const LazyAcademic3DScene: React.FC<LazyAcademic3DSceneProps> = ({
  size = 280,
  className = '',
  showToggle = true,
  enableParallax = true,
  badgeLabel,
}) => {
  const {
    isClient,
    is3DAllowed,
    reportFps,
    toggle3D,
    setUserPreference,
  } = use3DCapability();

  // If SSR or capability gate disallows 3D, render pristine 2D fallback with zero CLS
  const renderFallback = (
    <AcademicPristine2DFallback
      size={size}
      badgeLabel={badgeLabel}
    />
  );

  return (
    <div className={`relative flex flex-col items-center gap-3 ${className}`}>
      <ParallaxDepthContainer
        disabled={!enableParallax || !is3DAllowed}
        maxTiltDegrees={3.5}
        maxTranslatePx={8}
      >
        <div
          style={{ width: size, height: size }}
          className="relative flex items-center justify-center rounded-2xl overflow-hidden bg-[#FAF8F5] dark:bg-[#0E1524] border border-[#E5E2DA] dark:border-[#263147] shadow-paper-md"
        >
          {isClient && is3DAllowed ? (
            <Academic3DErrorBoundary
              size={size}
              fallback={renderFallback}
              onError={() => {
                // If WebGL runtime fails, downgrade gracefully
                setUserPreference(false);
              }}
            >
              <Suspense fallback={renderFallback}>
                <AcademicScholarGlobe3D
                  size={size}
                  onFpsReport={reportFps}
                  onContextLost={() => {
                    setUserPreference(false);
                  }}
                />
              </Suspense>
            </Academic3DErrorBoundary>
          ) : (
            renderFallback
          )}
        </div>
      </ParallaxDepthContainer>

      {/* Accessible Control Bar Below Scene */}
      {showToggle && (
        <div className="flex items-center justify-between w-full max-w-[280px] px-1">
          <Academic3DToggle compact />
          <span className="text-[10px] font-mono text-[#5A687D] dark:text-[#94A3B8]">
            এনসিটিবি ২০২৬
          </span>
        </div>
      )}
    </div>
  );
};
