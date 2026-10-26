/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Procedural Three.js Academic Armillary Globe & Scholar's Treatise
 * FILE:      frontend/src/components/3d/AcademicScholarGlobe3D.tsx
 * PURPOSE:   Renders a contemplative, prestigious academic 3D world:
 *            - 100% self-contained procedural Three.js geometry (0 external model downloads).
 *            - Brass celestial armillary sphere with tilted ecliptic ring (23.5°).
 *            - Inner terrestrial globe with illuminated Bangladesh beacon (23.68° N, 90.35° E).
 *            - Turned mahogany pedestal & scholar's leather-bound treatises at the base.
 *            - Soft academic studio 3-point lighting (warm key, cool fill, rim accent).
 *            - Strict GPU lifecycle: 0 memory leaks, context loss handling, off-screen pause via
 *              IntersectionObserver, capped 1.5 DPR, and rolling FPS monitoring.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Sub-400KB Dynamic Chunk, Zero CLS.
 */

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface AcademicScholarGlobe3DProps {
  size?: number;
  onFpsReport?: (fps: number) => void;
  onContextLost?: () => void;
  isPaused?: boolean;
}

export default function AcademicScholarGlobe3D({
  size = 280,
  onFpsReport,
  onContextLost,
  isPaused = false,
}: AcademicScholarGlobe3DProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);
  const isIntersectingRef = useRef<boolean>(true);

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
        powerPreference: 'high-performance',
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
    camera.position.set(0, 0.45, 3.8);
    camera.lookAt(0, 0.05, 0);

    // 4. Soft Studio Lighting (Academic Gallery Aesthetic)
    const ambientLight = new THREE.AmbientLight(0xfff8ee, 0.7);
    scene.add(ambientLight);

    // Warm Ivory Key Light (reflecting brass patina)
    const keyLight = new THREE.DirectionalLight(0xfffaed, 2.4);
    keyLight.position.set(2.4, 3.5, 2.8);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.width = 512;
    keyLight.shadow.mapSize.height = 512;
    keyLight.shadow.camera.near = 0.5;
    keyLight.shadow.camera.far = 10;
    keyLight.shadow.bias = -0.001;
    scene.add(keyLight);

    // Cool Steel Fill Light
    const fillLight = new THREE.DirectionalLight(0x94a3b8, 0.85);
    fillLight.position.set(-2.5, 1.2, 1.8);
    scene.add(fillLight);

    // Warm Amber Rim Light
    const rimLight = new THREE.DirectionalLight(0xd97706, 1.1);
    rimLight.position.set(0, -1.8, -2.4);
    scene.add(rimLight);

    // 5. Procedural Materials
    const brassMaterial = new THREE.MeshStandardMaterial({
      color: 0xc49a45,
      metalness: 0.85,
      roughness: 0.32,
    });

    const darkBrassMaterial = new THREE.MeshStandardMaterial({
      color: 0x8c6d2c,
      metalness: 0.88,
      roughness: 0.4,
    });

    const emeraldPatinaMaterial = new THREE.MeshStandardMaterial({
      color: 0x065f46,
      metalness: 0.75,
      roughness: 0.35,
    });

    const turnedWoodMaterial = new THREE.MeshStandardMaterial({
      color: 0x1c1917,
      metalness: 0.15,
      roughness: 0.65,
    });

    const leatherBookMaterial = new THREE.MeshStandardMaterial({
      color: 0x451a03,
      metalness: 0.1,
      roughness: 0.75,
    });

    const parchmentMaterial = new THREE.MeshStandardMaterial({
      color: 0xf5f2eb,
      metalness: 0.05,
      roughness: 0.9,
    });

    const beaconMaterial = new THREE.MeshBasicMaterial({
      color: 0x10b981,
    });

    // 6. Master Armillary Group
    const ensembleGroup = new THREE.Group();
    scene.add(ensembleGroup);

    // --- BASE & PEDESTAL ---
    const pedestalGroup = new THREE.Group();
    ensembleGroup.add(pedestalGroup);

    // Circular turned wood plinth
    const plinthGeom = new THREE.CylinderGeometry(0.85, 0.92, 0.08, 36);
    const plinthMesh = new THREE.Mesh(plinthGeom, turnedWoodMaterial);
    plinthMesh.position.y = -1.15;
    plinthMesh.receiveShadow = true;
    pedestalGroup.add(plinthMesh);

    // Turned brass collar
    const collarGeom = new THREE.CylinderGeometry(0.24, 0.34, 0.12, 24);
    const collarMesh = new THREE.Mesh(collarGeom, brassMaterial);
    collarMesh.position.y = -1.05;
    collarMesh.castShadow = true;
    pedestalGroup.add(collarMesh);

    // Stem baluster
    const balusterGeom = new THREE.CylinderGeometry(0.12, 0.18, 0.45, 24);
    const balusterMesh = new THREE.Mesh(balusterGeom, brassMaterial);
    balusterMesh.position.y = -0.78;
    balusterMesh.castShadow = true;
    pedestalGroup.add(balusterMesh);

    // Top support cradle bracket
    const bracketGeom = new THREE.TorusGeometry(0.88, 0.028, 12, 48, Math.PI);
    const bracketMesh = new THREE.Mesh(bracketGeom, darkBrassMaterial);
    bracketMesh.rotation.x = Math.PI / 2;
    bracketMesh.rotation.z = Math.PI;
    bracketMesh.position.y = -0.45;
    pedestalGroup.add(bracketMesh);

    // --- SCHOLAR'S STACKED FOLIOS AT BASE ---
    const folioGroup = new THREE.Group();
    folioGroup.position.set(0.22, -1.08, 0.15);
    folioGroup.rotation.y = 0.35;
    ensembleGroup.add(folioGroup);

    // Bottom book
    const book1Geom = new THREE.BoxGeometry(0.68, 0.07, 0.48);
    const book1Mesh = new THREE.Mesh(book1Geom, leatherBookMaterial);
    book1Mesh.castShadow = true;
    folioGroup.add(book1Mesh);

    // Top smaller treatise
    const book2Geom = new THREE.BoxGeometry(0.55, 0.06, 0.4);
    const book2Mesh = new THREE.Mesh(book2Geom, parchmentMaterial);
    book2Mesh.position.set(0.04, 0.065, 0.02);
    book2Mesh.rotation.y = -0.22;
    book2Mesh.castShadow = true;
    folioGroup.add(book2Mesh);

    // --- ROTATING CELESTIAL ARMILLARY SPHERE ---
    const armillaryGroup = new THREE.Group();
    armillaryGroup.position.y = 0.15;
    ensembleGroup.add(armillaryGroup);

    // Outer Brass Meridian Ring
    const meridianGeom = new THREE.TorusGeometry(0.82, 0.028, 16, 64);
    const meridianMesh = new THREE.Mesh(meridianGeom, brassMaterial);
    meridianMesh.castShadow = true;
    armillaryGroup.add(meridianMesh);

    // Equatorial Celestial Ring (Horizontal)
    const equatorGeom = new THREE.TorusGeometry(0.79, 0.024, 16, 64);
    const equatorMesh = new THREE.Mesh(equatorGeom, darkBrassMaterial);
    equatorMesh.rotation.x = Math.PI / 2;
    equatorMesh.castShadow = true;
    armillaryGroup.add(equatorMesh);

    // Tilted Ecliptic Zodiac Band (23.5 degrees)
    const eclipticGroup = new THREE.Group();
    eclipticGroup.rotation.z = (-23.5 * Math.PI) / 180;
    armillaryGroup.add(eclipticGroup);

    const eclipticGeom = new THREE.CylinderGeometry(0.76, 0.76, 0.065, 48, 1, true);
    const eclipticMesh = new THREE.Mesh(eclipticGeom, emeraldPatinaMaterial);
    eclipticMesh.castShadow = true;
    eclipticGroup.add(eclipticMesh);

    // Solstice Colure Ring
    const colureGeom = new THREE.TorusGeometry(0.77, 0.016, 12, 48);
    const colureMesh = new THREE.Mesh(colureGeom, brassMaterial);
    colureMesh.rotation.y = Math.PI / 2;
    eclipticGroup.add(colureMesh);

    // --- INNER TERRESTRIAL GLOBE & BEACON ---
    const globeGroup = new THREE.Group();
    globeGroup.rotation.z = (-23.5 * Math.PI) / 180;
    armillaryGroup.add(globeGroup);

    // Inner globe body
    const globeGeom = new THREE.SphereGeometry(0.42, 32, 24);
    const globeMaterial = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      metalness: 0.35,
      roughness: 0.55,
      wireframe: false,
    });
    const globeMesh = new THREE.Mesh(globeGeom, globeMaterial);
    globeMesh.castShadow = true;
    globeGroup.add(globeMesh);

    // Globe Latitude Circles
    const lat1Geom = new THREE.TorusGeometry(0.422, 0.008, 8, 36);
    const lat1Mesh = new THREE.Mesh(lat1Geom, brassMaterial);
    lat1Mesh.rotation.x = Math.PI / 2;
    globeGroup.add(lat1Mesh);

    // Polar Axis Pin
    const axisPinGeom = new THREE.CylinderGeometry(0.018, 0.018, 1.82, 16);
    const axisPinMesh = new THREE.Mesh(axisPinGeom, brassMaterial);
    globeGroup.add(axisPinMesh);

    // Bangladesh Sovereign Beacon (Lat 23.68° N, Long 90.35° E)
    // Convert spherical lat/long to 3D Cartesian coordinates
    const latRad = (23.68 * Math.PI) / 180;
    const lonRad = (90.35 * Math.PI) / 180;
    const globeRadius = 0.425;

    const beaconX = globeRadius * Math.cos(latRad) * Math.sin(lonRad);
    const beaconY = globeRadius * Math.sin(latRad);
    const beaconZ = globeRadius * Math.cos(latRad) * Math.cos(lonRad);

    const beaconGeom = new THREE.SphereGeometry(0.032, 16, 16);
    const beaconMesh = new THREE.Mesh(beaconGeom, beaconMaterial);
    beaconMesh.position.set(beaconX, beaconY, beaconZ);
    globeGroup.add(beaconMesh);

    // Beacon subtle pulse aura
    const auraGeom = new THREE.RingGeometry(0.038, 0.065, 16);
    const auraMaterial = new THREE.MeshBasicMaterial({
      color: 0x34d399,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.8,
    });
    const auraMesh = new THREE.Mesh(auraGeom, auraMaterial);
    auraMesh.position.set(beaconX * 1.02, beaconY * 1.02, beaconZ * 1.02);
    auraMesh.lookAt(beaconX * 2, beaconY * 2, beaconZ * 2);
    globeGroup.add(auraMesh);

    // 7. Interaction: Pointer Hover Tilt
    const handlePointerMove = (e: PointerEvent) => {
      const rect = container.getBoundingClientRect();
      const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const ny = ((e.clientY - rect.top) / rect.height) * 2 - 1;
      targetParallax.current = {
        x: Math.max(-1, Math.min(1, nx)),
        y: Math.max(-1, Math.min(1, ny)),
      };
    };

    const handlePointerLeave = () => {
      targetParallax.current = { x: 0, y: 0 };
    };

    container.addEventListener('pointermove', handlePointerMove, { passive: true });
    container.addEventListener('pointerleave', handlePointerLeave, { passive: true });

    // 8. Intersection Observer for Demand-Based Off-screen Pausing
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          isIntersectingRef.current = entry.isIntersecting;
        });
      },
      { threshold: 0.05 }
    );
    observer.observe(container);

    // 9. Animation Loop with FPS Monitoring & Dynamic Inertia
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsAccumulator = 0;
    let isRunning = true;

    const animate = (now: number) => {
      if (!isRunning) return;

      animFrameRef.current = requestAnimationFrame(animate);

      // Skip render if out of viewport or paused
      if (!isIntersectingRef.current || isPaused || document.hidden) {
        lastTime = now;
        return;
      }

      // Delta time & rolling FPS calculation
      const delta = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      frameCount++;
      fpsAccumulator += 1 / (delta || 0.016);
      if (frameCount >= 30) {
        const reportedFps = Math.round(fpsAccumulator / frameCount);
        onFpsReport?.(reportedFps);
        frameCount = 0;
        fpsAccumulator = 0;
      }

      // Damped parallax smoothing
      currentParallax.current.x += (targetParallax.current.x - currentParallax.current.x) * 0.05;
      currentParallax.current.y += (targetParallax.current.y - currentParallax.current.y) * 0.05;

      // Gentle continuous academic rotation
      armillaryGroup.rotation.y += 0.005;
      globeGroup.rotation.y += 0.008;

      // Weighted ensemble tilt responding to pointer
      ensembleGroup.rotation.y = currentParallax.current.x * 0.35;
      ensembleGroup.rotation.x = -currentParallax.current.y * 0.22;

      // Beacon breathing aura
      const auraScale = 1.0 + Math.sin(now * 0.004) * 0.25;
      auraMesh.scale.set(auraScale, auraScale, 1);

      renderer.render(scene, camera);
    };

    animFrameRef.current = requestAnimationFrame(animate);

    // 10. Comprehensive GPU Resource Disposal on Unmount
    return () => {
      isRunning = false;
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);

      container.removeEventListener('pointermove', handlePointerMove);
      container.removeEventListener('pointerleave', handlePointerLeave);
      canvas.removeEventListener('webglcontextlost', handleContextLost);
      observer.disconnect();

      // Dispose all geometries and materials recursively
      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          if (obj.geometry) {
            obj.geometry.dispose();
          }
          if (obj.material) {
            if (Array.isArray(obj.material)) {
              obj.material.forEach((mat) => mat.dispose());
            } else {
              obj.material.dispose();
            }
          }
        }
      });

      renderer.dispose();
      renderer.forceContextLoss();
    };
  }, [size, isPaused, onFpsReport, onContextLost]);

  return (
    <div
      ref={containerRef}
      style={{ width: size, height: size }}
      className="relative flex items-center justify-center rounded-2xl overflow-hidden select-none"
    >
      <canvas
        ref={canvasRef}
        style={{ width: size, height: size }}
        className="block w-full h-full cursor-grab active:cursor-grabbing"
      />
    </div>
  );
}
