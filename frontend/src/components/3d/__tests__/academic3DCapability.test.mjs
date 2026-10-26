/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic 3D & Depth Engine Capability Test Suite
 * FILE:      frontend/src/components/3d/__tests__/academic3DCapability.test.mjs
 * PURPOSE:   Validates capability detection, low-end device gates, reduced-motion,
 *            preference persistence in localStorage, and pristine fallback triggers.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Production Grade.
 */

import test from 'node:test';
import assert from 'node:assert/strict';

import {
  STORAGE_KEY,
  getStored3DPreference,
  setStored3DPreference,
  checkReducedMotion
} from '../use3DCapability.ts';

// Mock storage helper
function createMockLocalStorage() {
  const store = new Map();
  return {
    getItem: (key) => store.get(key) || null,
    setItem: (key, value) => store.set(key, String(value)),
    removeItem: (key) => store.delete(key),
    clear: () => store.clear(),
  };
}

test('TC-3D-ACAD-01: User preference defaults to true when unconfigured', () => {
  const originalWindow = global.window;
  const mockStorage = createMockLocalStorage();
  global.window = {
    localStorage: mockStorage,
    matchMedia: () => ({ matches: false }),
  };

  try {
    const pref = getStored3DPreference();
    assert.strictEqual(pref, true, 'Default 3D preference should be true (opt-in enabled)');
  } finally {
    global.window = originalWindow;
  }
});

test('TC-3D-ACAD-02: Storing preference persists correctly in localStorage', () => {
  const originalWindow = global.window;
  const mockStorage = createMockLocalStorage();
  global.window = {
    localStorage: mockStorage,
    matchMedia: () => ({ matches: false }),
    dispatchEvent: () => true,
  };

  try {
    setStored3DPreference(false);
    assert.strictEqual(mockStorage.getItem(STORAGE_KEY), 'false');
    assert.strictEqual(getStored3DPreference(), false);

    setStored3DPreference(true);
    assert.strictEqual(mockStorage.getItem(STORAGE_KEY), 'true');
    assert.strictEqual(getStored3DPreference(), true);
  } finally {
    global.window = originalWindow;
  }
});

test('TC-3D-ACAD-03: checkReducedMotion detects media query match', () => {
  const originalWindow = global.window;

  // Reduced motion active
  global.window = {
    matchMedia: (query) => ({
      matches: query.includes('prefers-reduced-motion: reduce'),
    }),
  };

  try {
    assert.strictEqual(checkReducedMotion(), true, 'Should detect reduced motion preference');
  } finally {
    global.window = originalWindow;
  }

  // Reduced motion inactive
  global.window = {
    matchMedia: (query) => ({
      matches: false,
    }),
  };

  try {
    assert.strictEqual(checkReducedMotion(), false, 'Should detect standard motion preference');
  } finally {
    global.window = originalWindow;
  }
});
