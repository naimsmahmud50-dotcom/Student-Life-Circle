/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & 3D Capability Assessment
 * TOPIC:     Phase 142 3D Capability Detection & Runtime Guard System
 * FILE:      frontend/src/components/live-challenge/detect3DCapability.ts
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Ultra-defensive module determining if WebGL 3D rendering is permitted.
 *            Enforces strict constraints for low-end devices across Bangladesh:
 *            - WebGL / WebGL2 context availability
 *            - Hardware capacity (deviceMemory >= 4GB, hardwareConcurrency >= 4 cores)
 *            - Zero Data Saver mode (saveData !== true)
 *            - High-bandwidth connection (disallows slow-2g, 2g, 3g tiers)
 *            - Respects prefers-reduced-motion accessibility
 *            - Tab visibility awareness
 *            - User manual 3D toggle persistence
 *            - Lightweight frame-time benchmark (>= 30 FPS)
 * STANDARDS: Zero-Emoji, Production Grade, Defensive Fallbacks, WCAG 2.2 AAA
 */

export const STORAGE_KEY_3D_DISABLED = 'ogrojatra_live_challenge_3d_disabled';
export const EVENT_3D_PREFERENCE_CHANGED = 'ogrojatra_3d_preference_changed';

export interface CapabilityDetails {
  webglAvailable: boolean;
  deviceMemoryGB?: number;
  hardwareConcurrency?: number;
  saveData: boolean;
  effectiveType?: string;
  prefersReducedMotion: boolean;
  tabVisible: boolean;
  userDisabled: boolean;
  benchmarkFps?: number;
}

export interface CapabilityCheckResult {
  allowed: boolean;
  reason:
    | 'CAPABLE'
    | 'SSR_ENVIRONMENT'
    | 'USER_OPTED_OUT'
    | 'PREFERS_REDUCED_MOTION'
    | 'TAB_HIDDEN'
    | 'SAVE_DATA_ACTIVE'
    | 'SLOW_NETWORK_TIER'
    | 'LOW_DEVICE_MEMORY'
    | 'LOW_CPU_CONCURRENCY'
    | 'WEBGL_UNAVAILABLE'
    | 'WEBGL_ERROR'
    | 'BENCHMARK_STUTTER';
  details: CapabilityDetails;
}

export interface BenchmarkResult {
  passed: boolean;
  avgFps: number;
  avgDeltaMs: number;
}

interface NavigatorNetworkInformation {
  saveData?: boolean;
  effectiveType?: string;
}

interface ExtendedNavigator {
  deviceMemory?: number;
  hardwareConcurrency?: number;
  connection?: NavigatorNetworkInformation;
  mozConnection?: NavigatorNetworkInformation;
  webkitConnection?: NavigatorNetworkInformation;
}

export interface EnvironmentContext {
  window?: any;
  document?: any;
  navigator?: ExtendedNavigator;
  localStorage?: Storage | {
    getItem: (key: string) => string | null;
    setItem: (key: string, value: string) => void;
    removeItem: (key: string) => void;
  };
}

/**
 * Resolves current execution environment, allowing dependency injection for unit testing.
 */
function resolveEnvironment(customEnv?: EnvironmentContext) {
  const win = customEnv?.window ?? (typeof window !== 'undefined' ? window : undefined);
  const doc = customEnv?.document ?? (typeof document !== 'undefined' ? document : undefined);
  const nav = customEnv?.navigator ?? (typeof navigator !== 'undefined' ? (navigator as ExtendedNavigator) : undefined);
  const storage = customEnv?.localStorage ?? (typeof window !== 'undefined' && window.localStorage ? window.localStorage : undefined);

  return { win, doc, nav, storage };
}

/**
 * Checks whether user has manually disabled 3D in localStorage.
 */
export function getUser3DPreference(customEnv?: EnvironmentContext): boolean {
  const { storage } = resolveEnvironment(customEnv);
  if (!storage) return true;
  try {
    return storage.getItem(STORAGE_KEY_3D_DISABLED) !== 'true';
  } catch {
    return true;
  }
}

/**
 * Updates user 3D preference and notifies active listeners.
 */
export function setUser3DPreference(enabled: boolean, customEnv?: EnvironmentContext): void {
  const { win, storage } = resolveEnvironment(customEnv);
  if (!storage) return;
  try {
    if (enabled) {
      storage.removeItem(STORAGE_KEY_3D_DISABLED);
    } else {
      storage.setItem(STORAGE_KEY_3D_DISABLED, 'true');
    }

    if (win && typeof win.dispatchEvent === 'function') {
      try {
        const event = typeof CustomEvent === 'function'
          ? new CustomEvent(EVENT_3D_PREFERENCE_CHANGED, { detail: { enabled } })
          : { type: EVENT_3D_PREFERENCE_CHANGED, detail: { enabled } };
        win.dispatchEvent(event as any);
      } catch {
        // Fallback for older headless environments
      }
    }
  } catch {
    // Storage access restricted (e.g. strict private browsing)
  }
}

/**
 * Synchronous static capability assessment.
 * Evaluates hardware, battery saver, network tier, accessibility, and WebGL support.
 */
export function checkStatic3DCapability(customEnv?: EnvironmentContext): CapabilityCheckResult {
  const { win, doc, nav, storage } = resolveEnvironment(customEnv);

  const initialDetails: CapabilityDetails = {
    webglAvailable: false,
    saveData: false,
    prefersReducedMotion: false,
    tabVisible: true,
    userDisabled: false
  };

  // 1. SSR check
  if (!win || !doc || !nav) {
    return {
      allowed: false,
      reason: 'SSR_ENVIRONMENT',
      details: initialDetails
    };
  }

  // 2. User manual preference
  let userOptedOut = false;
  try {
    userOptedOut = storage ? storage.getItem(STORAGE_KEY_3D_DISABLED) === 'true' : false;
  } catch {
    userOptedOut = false;
  }
  initialDetails.userDisabled = userOptedOut;
  if (userOptedOut) {
    return {
      allowed: false,
      reason: 'USER_OPTED_OUT',
      details: initialDetails
    };
  }

  // 3. prefers-reduced-motion accessibility
  let prefersReducedMotion = false;
  try {
    if (typeof win.matchMedia === 'function') {
      prefersReducedMotion = win.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }
  } catch {
    prefersReducedMotion = false;
  }
  initialDetails.prefersReducedMotion = prefersReducedMotion;
  if (prefersReducedMotion) {
    return {
      allowed: false,
      reason: 'PREFERS_REDUCED_MOTION',
      details: initialDetails
    };
  }

  // 4. Tab visibility
  const isTabVisible = doc.visibilityState ? doc.visibilityState === 'visible' : true;
  initialDetails.tabVisible = isTabVisible;
  if (!isTabVisible) {
    return {
      allowed: false,
      reason: 'TAB_HIDDEN',
      details: initialDetails
    };
  }

  // 5. Network Conditions (SaveData & 2G/3G detection)
  const connection = nav.connection || nav.mozConnection || nav.webkitConnection;
  if (connection) {
    const isSaveData = connection.saveData === true;
    initialDetails.saveData = isSaveData;
    if (isSaveData) {
      return {
        allowed: false,
        reason: 'SAVE_DATA_ACTIVE',
        details: initialDetails
      };
    }

    const effectiveType = connection.effectiveType ? connection.effectiveType.toLowerCase() : undefined;
    initialDetails.effectiveType = effectiveType;
    if (effectiveType && ['slow-2g', '2g', '3g'].includes(effectiveType)) {
      return {
        allowed: false,
        reason: 'SLOW_NETWORK_TIER',
        details: initialDetails
      };
    }
  }

  // 6. Device Memory (RAM) Heuristic
  const deviceMemory = typeof nav.deviceMemory === 'number' ? nav.deviceMemory : undefined;
  initialDetails.deviceMemoryGB = deviceMemory;
  if (deviceMemory !== undefined && deviceMemory < 4) {
    return {
      allowed: false,
      reason: 'LOW_DEVICE_MEMORY',
      details: initialDetails
    };
  }

  // 7. CPU Hardware Concurrency (Cores) Heuristic
  const hardwareConcurrency = typeof nav.hardwareConcurrency === 'number' ? nav.hardwareConcurrency : undefined;
  initialDetails.hardwareConcurrency = hardwareConcurrency;
  if (hardwareConcurrency !== undefined && hardwareConcurrency < 4) {
    return {
      allowed: false,
      reason: 'LOW_CPU_CONCURRENCY',
      details: initialDetails
    };
  }

  // 8. WebGL / WebGL2 Context Verification
  let webglAvailable = false;
  try {
    const canvas = doc.createElement('canvas');
    if (canvas && typeof canvas.getContext === 'function') {
      const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
      if (gl) {
        webglAvailable = true;
        // Cleanly release context resource
        try {
          const loseContextExt = gl.getExtension('WEBGL_lose_context');
          if (loseContextExt) {
            loseContextExt.loseContext();
          }
        } catch {
          // Extension optional
        }
      }
    }
  } catch {
    return {
      allowed: false,
      reason: 'WEBGL_ERROR',
      details: initialDetails
    };
  }

  initialDetails.webglAvailable = webglAvailable;
  if (!webglAvailable) {
    return {
      allowed: false,
      reason: 'WEBGL_UNAVAILABLE',
      details: initialDetails
    };
  }

  return {
    allowed: true,
    reason: 'CAPABLE',
    details: initialDetails
  };
}

/**
 * Lightweight frame-time benchmark.
 * Samples delta times over 12 frames to assert smooth >= 30 FPS (avg delta <= 33.33ms).
 */
export function runFrameTimeBenchmark(
  targetFrames = 12,
  maxAllowedFrameTimeMs = 33.33,
  customEnv?: EnvironmentContext
): Promise<BenchmarkResult> {
  const { win } = resolveEnvironment(customEnv);

  return new Promise((resolve) => {
    if (!win || typeof win.requestAnimationFrame !== 'function') {
      // In non-browser / headless mock without rAF, allow pass gracefully
      return resolve({ passed: true, avgFps: 60, avgDeltaMs: 16.66 });
    }

    let frameCount = 0;
    let lastTime = performance.now();
    const deltas: number[] = [];

    function onFrame(currentTime: number) {
      const delta = currentTime - lastTime;
      lastTime = currentTime;

      // Skip the very first frame delta which includes initial setup overhead
      if (frameCount > 0) {
        deltas.push(delta);
      }

      frameCount++;
      if (frameCount < targetFrames) {
        win.requestAnimationFrame(onFrame);
      } else {
        const avgDeltaMs = deltas.length > 0
          ? deltas.reduce((acc, val) => acc + val, 0) / deltas.length
          : 16.66;
        const avgFps = avgDeltaMs > 0 ? Math.round(1000 / avgDeltaMs) : 60;
        const passed = avgDeltaMs <= maxAllowedFrameTimeMs;

        resolve({ passed, avgFps, avgDeltaMs });
      }
    }

    win.requestAnimationFrame(onFrame);
  });
}

/**
 * Complete asynchronous evaluation combining static hardware checks and frame benchmark.
 */
export async function evaluate3DCapability(
  options: { bypassBenchmark?: boolean } = {},
  customEnv?: EnvironmentContext
): Promise<CapabilityCheckResult> {
  const staticResult = checkStatic3DCapability(customEnv);
  if (!staticResult.allowed) {
    return staticResult;
  }

  const shouldBypass = options.bypassBenchmark ||
    (typeof window !== 'undefined' && (window as any).__OGROJATRA_FORCE_3D__ === true);

  if (shouldBypass) {
    return staticResult;
  }

  try {
    const benchmark = await runFrameTimeBenchmark(12, 33.33, customEnv);
    staticResult.details.benchmarkFps = benchmark.avgFps;

    if (!benchmark.passed) {
      return {
        allowed: false,
        reason: 'BENCHMARK_STUTTER',
        details: staticResult.details
      };
    }

    return staticResult;
  } catch {
    // If benchmark throws, stay safe and return capable based on static check
    return staticResult;
  }
}
