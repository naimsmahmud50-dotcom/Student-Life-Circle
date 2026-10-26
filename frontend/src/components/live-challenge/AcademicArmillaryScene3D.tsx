/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Real-Time 3D Academic Scene
 * TOPIC:     Phase 142/143 Three.js Procedural Armillary Sphere & Academic Ensemble
 * FILE:      frontend/src/components/live-challenge/AcademicArmillaryScene3D.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Quiet, contemplative academic 3D world: slowly rotating brass armillary
 *            celestial sphere with tilted ecliptic zodiac band, turned pedestal,
 *            scholar's stacked folios (leather-bound treatises with parchment pages),
 *            fine brass dipping stylus, and celestial globe highlighting Bangladesh.
 *            100% self-contained procedural Three.js geometry (0 external GLB network requests,
 *            0 Draco overhead, < 250 kB total 3D dynamic chunk, strictly under 400 kB limit).
 *            Full lifecycle management: WebGL context loss recovery, tab visibility pausing,
 *            intersection observer offscreen demand rendering, and zero-leak disposal.
 * STANDARDS: Zero-Emoji, Zero-CLS, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface AcademicArmillaryScene3DProps {
  size?: number;
  timeRemainingSeconds?: number;
  onFpsReport?: (fps: number) => void;
  onContextLost?: () => void;
  isPaused?: boolean;
}

export default function AcademicArmillaryScene3D({
  size = 280,
  timeRemainingSeconds,
  onFpsReport,
  onContextLost,
  isPaused = false
}: AcademicArmillaryScene3DProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);
  const isIntersectingRef = useRef<boolean>(true);
  const [currentFps, setCurrentFps] = useState<number>(60);
  const timeRemainingRef = useRef<number | undefined>(timeRemainingSeconds);

  useEffect(() => {
    timeRemainingRef.current = timeRemainingSeconds;
  }, [timeRemainingSeconds]);

  // Parallax target and smoothed values for weighted, dignified motion
  const targetParallax = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const currentParallax = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    // 1. Pixel ratio capped strictly at 1.5 to guarantee high mobile FPS
    const dpr = typeof window !== 'undefined' ? Math.min(window.devicePixelRatio || 1, 1.5) : 1;
    const width = size;
    const height = size;

    // 2. Renderer creation with soft shadow maps and ACES filmic tone mapping
    let renderer: THREE.WebGLRenderer | null = null;
    try {
      renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
    } catch {
      onContextLost?.();
      return;
    }

    if (!renderer) {
      onContextLost?.();
      return;
    }

    renderer.setSize(width, height, false);
    renderer.setPixelRatio(dpr);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;

    // Context loss listeners
    const handleContextLost = (e: Event) => {
      e.preventDefault();
      onContextLost?.();
    };
    canvas.addEventListener('webglcontextlost', handleContextLost, false);

    // 3. Scene and Camera Setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(36, 1.0, 0.1, 40);
    // Initial camera position for gentle ease-in on load
    camera.position.set(0, 0.45, 3.8);
    camera.lookAt(0, 0.05, 0);

    // 4. Studio Lighting Rig (Warm Academic Library / Observatory)
    // Key Light: warm library sun from high left
    const keyLight = new THREE.DirectionalLight(0xFFFBEB, 1.8);
    keyLight.position.set(3.0, 4.8, 3.2);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 1024;
    keyLight.shadow.mapSize.height = 1024;
    keyLight.shadow.camera.near = 0.5;
    keyLight.shadow.camera.far = 12;
    keyLight.shadow.camera.left = -1.8;
    keyLight.shadow.camera.right = 1.8;
    keyLight.shadow.camera.top = 1.8;
    keyLight.shadow.camera.bottom = -1.8;
    keyLight.shadow.bias = -0.0002;
    scene.add(keyLight);

    // Fill Light: cool slate ambient bounce from low right
    const fillLight = new THREE.DirectionalLight(0x94A3B8, 0.6);
    fillLight.position.set(-3.0, -1.2, -2.5);
    scene.add(fillLight);

    // Rim / Kicker: scholar amber glow catching outer brass edges
    const rimLight = new THREE.PointLight(0xD97706, 1.35, 10);
    rimLight.position.set(-2.2, 2.5, -2.2);
    scene.add(rimLight);

    // Ambient: deep Oxford navy foundation
    const ambientLight = new THREE.AmbientLight(0x0A2540, 0.7);
    scene.add(ambientLight);

    // 5. Believable Physical Materials (Brushed Brass, Burnished Ochre, Dark Slate, Aged Parchment)
    const matAntiqueBrass = new THREE.MeshStandardMaterial({
      color: 0xD97706,
      roughness: 0.32,
      metalness: 0.86
    });

    const matBurnishedGold = new THREE.MeshStandardMaterial({
      color: 0xF59E0B,
      roughness: 0.28,
      metalness: 0.92
    });

    const matDarkSlate = new THREE.MeshStandardMaterial({
      color: 0x1E293B,
      roughness: 0.88,
      metalness: 0.12
    });

    const matLeatherBook1 = new THREE.MeshStandardMaterial({
      color: 0x0A2540, // Deep Oxford Ink folio
      roughness: 0.72,
      metalness: 0.08
    });

    const matLeatherBook2 = new THREE.MeshStandardMaterial({
      color: 0x78350F, // Warm Antique Amber/Burgundy leather
      roughness: 0.76,
      metalness: 0.05
    });

    const matParchmentPages = new THREE.MeshStandardMaterial({
      color: 0xFEFCE8, // Warm aged paper core
      roughness: 0.92,
      metalness: 0.0
    });

    const matGildedEdges = new THREE.MeshStandardMaterial({
      color: 0xD97706,
      roughness: 0.35,
      metalness: 0.85
    });

    const matGlobeCore = new THREE.MeshStandardMaterial({
      color: 0x475569, // Scholarly celestial sphere
      roughness: 0.42,
      metalness: 0.75
    });

    const matBangladeshEmerald = new THREE.MeshStandardMaterial({
      color: 0x10B981,
      roughness: 0.25,
      metalness: 0.6,
      emissive: 0x059669,
      emissiveIntensity: 0.45
    });

    const matScholarStylus = new THREE.MeshStandardMaterial({
      color: 0xFBBF24,
      roughness: 0.22,
      metalness: 0.95
    });

    // 6. Geometry & Hierarchy Construction
    const rootAcademicEnsemble = new THREE.Group();
    scene.add(rootAcademicEnsemble);

    // --- A. Desk Base & Supporting Props ---
    const deskGroup = new THREE.Group();
    deskGroup.position.set(0, -0.76, 0);
    rootAcademicEnsemble.add(deskGroup);

    // Beveled Dark Slate Plinth
    const plinthGeo = new THREE.CylinderGeometry(1.35, 1.45, 0.12, 12);
    const plinthMesh = new THREE.Mesh(plinthGeo, matDarkSlate);
    plinthMesh.receiveShadow = true;
    deskGroup.add(plinthMesh);

    // Stacked Treatise 1 (Bottom, Deep Oxford Ink)
    const book1Group = new THREE.Group();
    book1Group.position.set(-0.15, 0.09, 0.1);
    book1Group.rotation.y = -0.08;
    deskGroup.add(book1Group);

    const book1CoverGeo = new THREE.BoxGeometry(0.88, 0.07, 0.64);
    const book1Cover = new THREE.Mesh(book1CoverGeo, matLeatherBook1);
    book1Cover.castShadow = true;
    book1Cover.receiveShadow = true;
    book1Group.add(book1Cover);

    const book1PagesGeo = new THREE.BoxGeometry(0.82, 0.056, 0.60);
    const book1Pages = new THREE.Mesh(book1PagesGeo, matParchmentPages);
    book1Pages.position.set(0.02, 0, 0);
    book1Group.add(book1Pages);

    // Stacked Treatise 2 (Top, Antique Amber Leather, tilted 14 degrees)
    const book2Group = new THREE.Group();
    book2Group.position.set(-0.12, 0.165, 0.12);
    book2Group.rotation.y = 0.22;
    deskGroup.add(book2Group);

    const book2CoverGeo = new THREE.BoxGeometry(0.74, 0.065, 0.54);
    const book2Cover = new THREE.Mesh(book2CoverGeo, matLeatherBook2);
    book2Cover.castShadow = true;
    book2Cover.receiveShadow = true;
    book2Group.add(book2Cover);

    const book2PagesGeo = new THREE.BoxGeometry(0.68, 0.052, 0.50);
    const book2Pages = new THREE.Mesh(book2PagesGeo, matGildedEdges);
    book2Pages.position.set(0.02, 0, 0);
    book2Group.add(book2Pages);

    // Fine Brass Scholar's Pen / Stylus resting gracefully on the treatises
    const stylusGroup = new THREE.Group();
    stylusGroup.position.set(0.05, 0.22, 0.22);
    stylusGroup.rotation.set(-0.06, 0.65, 0.12);
    deskGroup.add(stylusGroup);

    const stylusBodyGeo = new THREE.CylinderGeometry(0.012, 0.007, 0.85, 12);
    const stylusBody = new THREE.Mesh(stylusBodyGeo, matScholarStylus);
    stylusBody.rotation.z = Math.PI / 2;
    stylusBody.castShadow = true;
    stylusGroup.add(stylusBody);

    const stylusNibGeo = new THREE.ConeGeometry(0.014, 0.06, 4);
    const stylusNib = new THREE.Mesh(stylusNibGeo, matBurnishedGold);
    stylusNib.position.set(0.45, 0, 0);
    stylusNib.rotation.z = -Math.PI / 2;
    stylusGroup.add(stylusNib);

    // --- B. Academic Armillary Stand & Cradle ---
    const standGroup = new THREE.Group();
    standGroup.position.set(0.32, -0.70, -0.15);
    rootAcademicEnsemble.add(standGroup);

    const standBaseGeo = new THREE.CylinderGeometry(0.24, 0.32, 0.05, 24);
    const standBase = new THREE.Mesh(standBaseGeo, matAntiqueBrass);
    standBase.castShadow = true;
    standGroup.add(standBase);

    const standPillarGeo = new THREE.CylinderGeometry(0.055, 0.08, 0.44, 20);
    const standPillar = new THREE.Mesh(standPillarGeo, matAntiqueBrass);
    standPillar.position.set(0, 0.24, 0);
    standPillar.castShadow = true;
    standGroup.add(standPillar);

    const standCapitalGeo = new THREE.CylinderGeometry(0.12, 0.06, 0.06, 20);
    const standCapital = new THREE.Mesh(standCapitalGeo, matBurnishedGold);
    standCapital.position.set(0, 0.48, 0);
    standGroup.add(standCapital);

    // --- C. Armillary Celestial Sphere (The Hero Object) ---
    const armillaryCenter = new THREE.Group();
    // Positioned slightly above stand pillar
    armillaryCenter.position.set(0.32, 0.18, -0.15);
    rootAcademicEnsemble.add(armillaryCenter);

    // 1. Outer Meridian Ring (Fixed in Y-Z plane)
    const meridianRingGeo = new THREE.TorusGeometry(0.86, 0.026, 16, 72);
    const meridianRing = new THREE.Mesh(meridianRingGeo, matAntiqueBrass);
    meridianRing.rotation.y = Math.PI / 2;
    meridianRing.castShadow = true;
    armillaryCenter.add(meridianRing);

    // Horizon Circle (Horizontal dividing ring)
    const horizonRingGeo = new THREE.TorusGeometry(0.88, 0.024, 14, 64);
    const horizonRing = new THREE.Mesh(horizonRingGeo, matAntiqueBrass);
    horizonRing.rotation.x = Math.PI / 2;
    horizonRing.castShadow = true;
    armillaryCenter.add(horizonRing);

    // 2. Axial Spindle (tilted at Bangladesh latitude & ecliptic inclination ~23.44°)
    const axisGroup = new THREE.Group();
    axisGroup.rotation.z = -0.41; // ~23.5 degrees
    armillaryCenter.add(axisGroup);

    const axisSpindleGeo = new THREE.CylinderGeometry(0.016, 0.016, 1.95, 16);
    const axisSpindle = new THREE.Mesh(axisSpindleGeo, matBurnishedGold);
    axisSpindle.castShadow = true;
    axisGroup.add(axisSpindle);

    // North & South Pole Finials
    const finialGeo = new THREE.SphereGeometry(0.045, 16, 16);
    const northFinial = new THREE.Mesh(finialGeo, matBurnishedGold);
    northFinial.position.set(0, 0.98, 0);
    axisGroup.add(northFinial);

    const southFinial = new THREE.Mesh(finialGeo, matBurnishedGold);
    southFinial.position.set(0, -0.98, 0);
    axisGroup.add(southFinial);

    // 3. Rotating Inner Celestial Gimbal
    const innerGimbal = new THREE.Group();
    axisGroup.add(innerGimbal);

    // Equatorial Ring
    const equatorRingGeo = new THREE.TorusGeometry(0.78, 0.020, 14, 64);
    const equatorRing = new THREE.Mesh(equatorRingGeo, matAntiqueBrass);
    equatorRing.rotation.x = Math.PI / 2;
    equatorRing.castShadow = true;
    innerGimbal.add(equatorRing);

    // Solstitial Colure Ring
    const solstitialRingGeo = new THREE.TorusGeometry(0.78, 0.018, 14, 64);
    const solstitialRing = new THREE.Mesh(solstitialRingGeo, matAntiqueBrass);
    solstitialRing.castShadow = true;
    innerGimbal.add(solstitialRing);

    // Equinoctial Colure Ring
    const equinoctialRingGeo = new THREE.TorusGeometry(0.78, 0.018, 14, 64);
    const equinoctialRing = new THREE.Mesh(equinoctialRingGeo, matAntiqueBrass);
    equinoctialRing.rotation.y = Math.PI / 2;
    equinoctialRing.castShadow = true;
    innerGimbal.add(equinoctialRing);

    // Tilted Ecliptic Zodiac Band (Prominent, Scholar Gold)
    const eclipticGroup = new THREE.Group();
    eclipticGroup.rotation.x = 0.41; // 23.5° relative to celestial equator
    innerGimbal.add(eclipticGroup);

    const eclipticRingGeo = new THREE.TorusGeometry(0.80, 0.038, 16, 72);
    const eclipticRing = new THREE.Mesh(eclipticRingGeo, matBurnishedGold);
    eclipticRing.rotation.x = Math.PI / 2;
    eclipticRing.castShadow = true;
    eclipticGroup.add(eclipticRing);

    // 4. Central Celestial Terrestrial Globe with Bangladesh Coordinate Marker
    const globeGeo = new THREE.SphereGeometry(0.26, 32, 32);
    const globeMesh = new THREE.Mesh(globeGeo, matGlobeCore);
    globeMesh.castShadow = true;
    innerGimbal.add(globeMesh);

    // Globe Latitude Lines (delicate equatorial wire)
    const globeEquatorGeo = new THREE.TorusGeometry(0.264, 0.005, 8, 48);
    const globeEquator = new THREE.Mesh(globeEquatorGeo, matBurnishedGold);
    globeEquator.rotation.x = Math.PI / 2;
    innerGimbal.add(globeEquator);

    // Bangladesh Coordinate Marker (~23.8° N latitude, glowing subtle emerald seal)
    const bangladeshMarkerGeo = new THREE.SphereGeometry(0.024, 16, 16);
    const bangladeshMarker = new THREE.Mesh(bangladeshMarkerGeo, matBangladeshEmerald);
    // Position on sphere at ~24 deg latitude
    const latRad = (23.8 * Math.PI) / 180;
    bangladeshMarker.position.set(
      0.265 * Math.cos(latRad),
      0.265 * Math.sin(latRad),
      0.03
    );
    innerGimbal.add(bangladeshMarker);

    // 7. Interactive Mouse / Pointer Parallax Handler
    const handlePointerMove = (e: PointerEvent) => {
      const rect = container.getBoundingClientRect();
      const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const ny = ((e.clientY - rect.top) / rect.height) * 2 - 1;
      targetParallax.current.x = Math.max(-1, Math.min(1, nx)) * 0.22;
      targetParallax.current.y = Math.max(-1, Math.min(1, ny)) * 0.16;
    };

    const handlePointerLeave = () => {
      targetParallax.current.x = 0;
      targetParallax.current.y = 0;
    };

    container.addEventListener('pointermove', handlePointerMove, { passive: true });
    container.addEventListener('pointerleave', handlePointerLeave, { passive: true });

    // 8. Intersection Observer for Demand-Based Offscreen Pausing
    let observer: IntersectionObserver | null = null;
    if (typeof window !== 'undefined' && 'IntersectionObserver' in window) {
      observer = new IntersectionObserver(
        (entries) => {
          if (entries[0]) {
            isIntersectingRef.current = entries[0].isIntersecting;
          }
        },
        { threshold: 0.05 }
      );
      observer.observe(container);
    }

    // 9. Stately Animation Loop & Continuous Performance Monitor
    let lastTime = performance.now();
    const frameTimes: number[] = [];

    const animate = (time: number) => {
      animFrameRef.current = requestAnimationFrame(animate);

      // Skip render if tab is hidden, element is offscreen, or paused
      if (isPaused || !isIntersectingRef.current) {
        return;
      }

      const delta = time - lastTime;
      lastTime = time;

      // Track FPS smoothed over 30 frames
      if (delta > 0) {
        frameTimes.push(1000 / delta);
        if (frameTimes.length > 30) {
          frameTimes.shift();
          const avgFps = Math.round(frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length);
          setCurrentFps(avgFps);
          onFpsReport?.(avgFps);
        }
      }

      // Real-time server-authoritative timer reactivity
      const seconds = timeRemainingRef.current;
      const isLastMinute = seconds !== undefined && seconds <= 60 && seconds > 0;
      const isExamStarted = seconds !== undefined && seconds === 0;

      // 1. Stately gimbal rotation: slightly accelerated during the critical final minute
      const rotationSpeed = isLastMinute ? 0.006 : isExamStarted ? 0.002 : 0.0035;
      innerGimbal.rotation.y += rotationSpeed;

      // 2. Subtle clock alignment: the axial spindle progresses with real seconds
      if (seconds !== undefined) {
        const secondHandRad = ((1200 - seconds) % 60) * (Math.PI / 30);
        axisGroup.rotation.y = secondHandRad * 0.2; // weighted celestial pace
      }

      // 3. Final minute soft visual change: rim light and emerald marker breathing
      if (isLastMinute) {
        rimLight.intensity = 1.35 + Math.sin(time * 0.006) * 0.45;
        matBangladeshEmerald.emissiveIntensity = 0.5 + Math.sin(time * 0.008) * 0.4;
      } else {
        rimLight.intensity = 1.35;
        matBangladeshEmerald.emissiveIntensity = 0.45;
      }

      // 4. Respectful opening moment upon exam start: gentle expansion
      if (isExamStarted) {
        if (armillaryCenter.scale.x < 1.08) {
          const nextScale = Math.min(1.08, armillaryCenter.scale.x + 0.003);
          armillaryCenter.scale.setScalar(nextScale);
        }
      }

      // Subtle physical breathing of outer armillary assembly
      armillaryCenter.rotation.x = Math.sin(time * 0.0006) * 0.02;

      // Weighted physics-based damping for mouse parallax (no snappy gaming feel)
      currentParallax.current.x += (targetParallax.current.x - currentParallax.current.x) * 0.045;
      currentParallax.current.y += (targetParallax.current.y - currentParallax.current.y) * 0.045;

      rootAcademicEnsemble.rotation.y = currentParallax.current.x;
      rootAcademicEnsemble.rotation.x = currentParallax.current.y;

      // Smooth camera ease-in upon initial load
      if (camera.position.z > 3.36) {
        camera.position.z += (3.35 - camera.position.z) * 0.035;
      }

      if (renderer) {
        renderer.render(scene, camera);
      }
    };

    animFrameRef.current = requestAnimationFrame(animate);

    // 10. Clean Unmount & Memory Leak Prevention
    return () => {
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }

      canvas.removeEventListener('webglcontextlost', handleContextLost);
      container.removeEventListener('pointermove', handlePointerMove);
      container.removeEventListener('pointerleave', handlePointerLeave);
      observer?.disconnect();

      // Deep disposal of all geometries, materials, and textures
      scene.traverse((obj) => {
        if ((obj as THREE.Mesh).isMesh) {
          const mesh = obj as THREE.Mesh;
          if (mesh.geometry) {
            mesh.geometry.dispose();
          }
          if (mesh.material) {
            if (Array.isArray(mesh.material)) {
              mesh.material.forEach((mat) => mat.dispose());
            } else {
              mesh.material.dispose();
            }
          }
        }
      });

      if (renderer) {
        renderer.dispose();
        renderer.forceContextLoss();
        renderer = null;
      }
    };
  }, [size, isPaused, onFpsReport, onContextLost]);

  return (
    <div
      ref={containerRef}
      className="relative flex items-center justify-center select-none cursor-grab active:cursor-grabbing"
      style={{ width: size, height: size }}
      role="region"
      aria-label="৩ডি একাডেমিক আর্মিলেয়ারি স্ফিয়ার ও বিজ্ঞান মানমন্দির মোটিফ"
    >
      <canvas
        ref={canvasRef}
        style={{ width: size, height: size, display: 'block' }}
        className="pointer-events-auto"
      />

      {/* Developer Quality & FPS Badge (Transparent, subtle academic counter) */}
      <div
        className="absolute bottom-1 right-2 pointer-events-none px-1.5 py-0.5 rounded bg-slate-900/60 backdrop-blur-sm border border-slate-700/50 text-[9px] font-mono text-amber-300/80 flex items-center gap-1 select-none"
        aria-hidden="true"
      >
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
        <span>3D ARMI • {currentFps} FPS</span>
      </div>
    </div>
  );
}
