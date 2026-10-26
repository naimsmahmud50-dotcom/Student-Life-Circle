/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & 3D Capability Assessment
 * TOPIC:     Phase 142 3D Capability Detection & Runtime Guard Test Suite
 * FILE:      frontend/src/components/live-challenge/__tests__/detect3DCapability.test.mjs
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Unit test suite testing 3D capability evaluation under all constraints:
 *            low deviceMemory, low hardwareConcurrency, saveData, 2G/3G network,
 *            prefers-reduced-motion, hidden tab, user opt-out, missing WebGL, and benchmark stutter.
 * STANDARDS: Zero-Emoji, Production Grade, TDD Red-Green, Human Craftsmanship
 */

import test from 'node:test';
import assert from 'node:assert/strict';

// Import target module
import {
  checkStatic3DCapability,
  STORAGE_KEY_3D_DISABLED,
  evaluate3DCapability,
  getUser3DPreference,
  setUser3DPreference
} from '../detect3DCapability.ts';

// Mock environment helper
function createMockEnvironment(overrides = {}) {
  const defaultNavigator = {
    deviceMemory: 8,
    hardwareConcurrency: 8,
    connection: {
      saveData: false,
      effectiveType: '4g'
    }
  };

  const defaultWindow = {
    matchMedia: (query) => ({
      matches: query.includes('prefers-reduced-motion: reduce') ? false : false
    }),
    requestAnimationFrame: (cb) => setTimeout(() => cb(Date.now()), 16),
    cancelAnimationFrame: (id) => clearTimeout(id)
  };

  const defaultDocument = {
    visibilityState: 'visible',
    createElement: (tag) => {
      if (tag === 'canvas') {
        return {
          getContext: (type) => {
            if (type === 'webgl2' || type === 'webgl') {
              return {
                getExtension: () => null
              };
            }
            return null;
          }
        };
      }
      return {};
    }
  };

  const storageMap = new Map();
  const defaultLocalStorage = {
    getItem: (key) => storageMap.get(key) || null,
    setItem: (key, val) => storageMap.set(key, String(val)),
    removeItem: (key) => storageMap.delete(key),
    clear: () => storageMap.clear()
  };

  return {
    window: { ...defaultWindow, ...(overrides.window || {}) },
    document: { ...defaultDocument, ...(overrides.document || {}) },
    navigator: {
      ...defaultNavigator,
      ...(overrides.navigator || {}),
      connection: {
        ...defaultNavigator.connection,
        ...((overrides.navigator && overrides.navigator.connection) || {})
      }
    },
    localStorage: overrides.localStorage || defaultLocalStorage
  };
}

test('TC-3D-01: Low device memory (< 4GB) disables 3D safely', () => {
  const env = createMockEnvironment({
    navigator: { deviceMemory: 2 }
  });
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'LOW_DEVICE_MEMORY');
  assert.strictEqual(res.details.deviceMemoryGB, 2);
});

test('TC-3D-02: Low CPU concurrency (< 4 cores) disables 3D safely', () => {
  const env = createMockEnvironment({
    navigator: { hardwareConcurrency: 2 }
  });
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'LOW_CPU_CONCURRENCY');
  assert.strictEqual(res.details.hardwareConcurrency, 2);
});

test('TC-3D-03: Data Saver active (saveData: true) disables 3D', () => {
  const env = createMockEnvironment({
    navigator: { connection: { saveData: true, effectiveType: '4g' } }
  });
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'SAVE_DATA_ACTIVE');
  assert.strictEqual(res.details.saveData, true);
});

test('TC-3D-04: Slow network tiers (2G/3G/slow-2g) disable 3D', () => {
  for (const tier of ['2g', '3g', 'slow-2g']) {
    const env = createMockEnvironment({
      navigator: { connection: { saveData: false, effectiveType: tier } }
    });
    const res = checkStatic3DCapability(env);
    assert.strictEqual(res.allowed, false, `Tier ${tier} must be disallowed`);
    assert.strictEqual(res.reason, 'SLOW_NETWORK_TIER');
    assert.strictEqual(res.details.effectiveType, tier);
  }
});

test('TC-3D-05: prefers-reduced-motion disables 3D animation', () => {
  const env = createMockEnvironment({
    window: {
      matchMedia: (query) => ({
        matches: query.includes('prefers-reduced-motion')
      })
    }
  });
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'PREFERS_REDUCED_MOTION');
  assert.strictEqual(res.details.prefersReducedMotion, true);
});

test('TC-3D-06: Hidden tab (document.visibilityState === "hidden") disables 3D', () => {
  const env = createMockEnvironment({
    document: { visibilityState: 'hidden' }
  });
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'TAB_HIDDEN');
  assert.strictEqual(res.details.tabVisible, false);
});

test('TC-3D-07: User manual opt-out in localStorage disables 3D', () => {
  const env = createMockEnvironment();
  env.localStorage.setItem(STORAGE_KEY_3D_DISABLED, 'true');
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'USER_OPTED_OUT');
  assert.strictEqual(res.details.userDisabled, true);
});

test('TC-3D-08: Missing WebGL context safely defaults to 2D', () => {
  const env = createMockEnvironment({
    document: {
      createElement: (tag) => {
        if (tag === 'canvas') {
          return { getContext: () => null };
        }
        return {};
      }
    }
  });
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'WEBGL_UNAVAILABLE');
  assert.strictEqual(res.details.webglAvailable, false);
});

test('TC-3D-09: All capability conditions met allows 3D', () => {
  const env = createMockEnvironment();
  const res = checkStatic3DCapability(env);
  assert.strictEqual(res.allowed, true);
  assert.strictEqual(res.reason, 'CAPABLE');
});

test('TC-3D-10: User preference toggle persists and reads correctly', () => {
  const env = createMockEnvironment();
  assert.strictEqual(getUser3DPreference(env), true);

  setUser3DPreference(false, env);
  assert.strictEqual(getUser3DPreference(env), false);
  assert.strictEqual(env.localStorage.getItem(STORAGE_KEY_3D_DISABLED), 'true');

  setUser3DPreference(true, env);
  assert.strictEqual(getUser3DPreference(env), true);
  assert.strictEqual(env.localStorage.getItem(STORAGE_KEY_3D_DISABLED), null);
});

test('TC-3D-11: Frame benchmark stutter (< 30 FPS) fails capability evaluation', async () => {
  // Mock rAF that runs at 20 FPS (delta 50ms)
  let simulatedTime = 1000;
  const env = createMockEnvironment({
    window: {
      requestAnimationFrame: (cb) => {
        simulatedTime += 50; // 50ms per frame = 20 FPS
        setTimeout(() => cb(simulatedTime), 5);
      }
    }
  });

  const res = await evaluate3DCapability({}, env);
  assert.strictEqual(res.allowed, false);
  assert.strictEqual(res.reason, 'BENCHMARK_STUTTER');
  assert.ok(res.details.benchmarkFps !== undefined && res.details.benchmarkFps < 30);
});

test('TC-3D-12: Smooth frame benchmark (>= 30 FPS) passes capability evaluation', async () => {
  // Mock rAF that runs at 60 FPS (delta ~16.6ms)
  let simulatedTime = 1000;
  const env = createMockEnvironment({
    window: {
      requestAnimationFrame: (cb) => {
        simulatedTime += 16.6;
        setTimeout(() => cb(simulatedTime), 5);
      }
    }
  });

  const res = await evaluate3DCapability({}, env);
  assert.strictEqual(res.allowed, true);
  assert.strictEqual(res.reason, 'CAPABLE');
  assert.ok(res.details.benchmarkFps !== undefined && res.details.benchmarkFps >= 30);
});
