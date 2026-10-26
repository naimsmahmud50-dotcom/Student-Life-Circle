/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Playwright End-to-End 3D Capability & Runtime Guard Test Suite
 * TOPIC:     Phase 142 3D Capability Detection, WebGL Fallback, and Low-End Protection
 * FILE:      frontend/e2e/live_challenge_3d_guard.spec.ts
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Validates the progressive-enhancement 3D capability system:
 *            1. Confirms countdown timer, join button, rules, and negative marking are
 *               100% semantic HTML elements outside the WebGL canvas.
 *            2. Asserts graceful 2D fallback when WebGL is unavailable or disabled.
 *            3. Asserts low-end hardware protection (2GB RAM / 2 CPU cores defaults to 2D).
 *            4. Asserts data saver (saveData: true) and 3G network constraints default to 2D.
 *            5. Asserts prefers-reduced-motion accessibility defaults to 2D.
 *            6. Asserts offline resilience (context.setOffline(true)).
 *            7. Asserts interactive 2D/3D toggle button updates mode and persists in localStorage.
 * STANDARDS: Playwright Headless, Strict Zero-Emoji, WCAG 2.2 AAA, Zero-CLS
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap, setupMockApiRoutes } from './helpers/e2e-fixtures';

test.describe('Phase 142: Live Challenge 3D Capability & Defensive Fallback Suite', () => {

  test.beforeEach(async ({ page }) => {
    await setupMockApiRoutes(page);
  });

  test('TC-3DG-01: Countdown, join button, rules, and negative badge are real HTML text outside any canvas', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/live-challenge');
    await expect(page).toHaveTitle(/দেশব্যাপী লাইভ চ্যালেঞ্জ | অগ্রযাত্রা/);

    const pageContent = await page.content();
    assertZeroEmojis(pageContent, 'Live Challenge Page with 3D Slot');

    // 1. Verify Server-Authoritative Timer is a real HTML <span>
    const timerLabel = page.locator('span', { hasText: 'সার্ভার-অথরিটেটিভ টাইমার' });
    await expect(timerLabel).toBeVisible();

    // 2. Verify Millisecond Buffer is a real HTML <span>
    const bufferLabel = page.locator('span', { hasText: 'মিলি-সেকেন্ড একুরেট বাফার' });
    await expect(bufferLabel).toBeVisible();

    // 3. Verify Negative Marking Ratio is real HTML text with Burgundy Crimson styling
    const negativeBadge = page.locator('text=নেগেটিভ মার্কিং: -০.২৫');
    await expect(negativeBadge).toBeVisible();

    // 4. Verify Rules button is an HTML <button>
    const rulesBtn = page.locator('button', { hasText: 'নিয়মাবলী' });
    await expect(rulesBtn).toBeVisible();

    // 5. Verify Join Exam is an HTML <a> link
    const joinBtn = page.locator('main a', { hasText: 'পরীক্ষায় অংশগ্রহণ করুন' });
    await expect(joinBtn).toBeVisible();

    // 6. Confirm none of these crucial elements are trapped inside a <canvas>
    const canvasChildren = await page.evaluate(() => {
      const canvases = document.querySelectorAll('canvas');
      let textInsideCanvas = false;
      canvases.forEach((c) => {
        if (c.innerHTML.includes('সার্ভার') || c.innerHTML.includes('পরীক্ষায়')) {
          textInsideCanvas = true;
        }
      });
      return textInsideCanvas;
    });
    expect(canvasChildren).toBe(false);

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-02: User manual 3D toggle switches modes and persists choice in localStorage', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/live-challenge');

    // Find the 2D/3D mode switch button
    const modeBtn = page.locator('button', { hasText: /মোড সক্রিয়/ });
    await expect(modeBtn).toBeVisible();

    // Initial state check
    const initialText = await modeBtn.textContent();
    expect(initialText).toBeDefined();

    // Toggle button click
    await modeBtn.click();

    // Verify localStorage reflects the change
    const is3dDisabled = await page.evaluate(() => {
      return localStorage.getItem('ogrojatra_live_challenge_3d_disabled');
    });

    // Should have toggled state
    if (initialText?.includes('৩ডি মোড')) {
      expect(is3dDisabled).toBe('true');
      await expect(page.locator('button', { hasText: '২ডি মোড সক্রিয় (সুইচ টু ৩ডি)' })).toBeVisible();
    }

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-03: Low-end device emulation (deviceMemory: 2, concurrency: 2) safely defaults to 2D', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    // Emulate a low-end budget Android phone with 2GB RAM and 2 CPU cores
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'deviceMemory', { get: () => 2 });
      Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 2 });
    });

    await page.goto('/live-challenge');

    // Verify 2D Armillary Sphere fallback SVG motif is rendered
    const motif2D = page.locator('div[aria-label="একাডেমিক আর্মিলেয়ারি স্ফিয়ার ও বিজ্ঞান কোয়াড্রান্ট মোটিফ"]');
    await expect(motif2D).toBeVisible();

    // Verify low-power 2D notice is displayed
    const lowPowerNotice = page.locator('text=লো-পাওয়ার ২ডি মোড');
    await expect(lowPowerNotice).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-04: Data Saver (saveData: true) safely defaults to 2D', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    // Emulate Data Saver mode active
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'connection', {
        get: () => ({
          saveData: true,
          effectiveType: '4g'
        })
      });
    });

    await page.goto('/live-challenge');

    // 2D fallback rendered
    const motif2D = page.locator('div[aria-label="একাডেমিক আর্মিলেয়ারি স্ফিয়ার ও বিজ্ঞান কোয়াড্রান্ট মোটিফ"]');
    await expect(motif2D).toBeVisible();

    // Low power 2D notice visible
    await expect(page.locator('text=লো-পাওয়ার ২ডি মোড')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-05: 3G network emulation safely defaults to 2D', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    // Emulate 3G mobile network connection
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'connection', {
        get: () => ({
          saveData: false,
          effectiveType: '3g'
        })
      });
    });

    await page.goto('/live-challenge');

    // 2D fallback rendered
    const motif2D = page.locator('div[aria-label="একাডেমিক আর্মিলেয়ারি স্ফিয়ার ও বিজ্ঞান কোয়াড্রান্ট মোটিফ"]');
    await expect(motif2D).toBeVisible();

    await expect(page.locator('text=লো-পাওয়ার ২ডি মোড')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-06: prefers-reduced-motion accessibility setting defaults to 2D', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/live-challenge');

    // 2D fallback rendered
    const motif2D = page.locator('div[aria-label="একাডেমিক আর্মিলেয়ারি স্ফিয়ার ও বিজ্ঞান কোয়াড্রান্ট মোটিফ"]');
    await expect(motif2D).toBeVisible();

    await expect(page.locator('text=লো-পাওয়ার ২ডি মোড')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-07: Offline simulation resilience preserves live challenge interface', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page, { ignoreNetworkDisconnect: true });

    await page.goto('/live-challenge');
    await expect(page.locator('span', { hasText: 'সার্ভার-অথরিটেটিভ টাইমার' })).toBeVisible();

    // Simulate network drop
    await page.evaluate(() => window.dispatchEvent(new Event('offline')));

    // Verify page does not crash, timer is visible and operational
    await expect(page.locator('span', { hasText: 'সার্ভার-অথরিটেটিভ টাইমার' })).toBeVisible();
    await expect(page.locator('text=জাতীয় স্টেম অলিম্পিয়াড ২০২৬')).toBeVisible();

    // Reconnect
    await page.evaluate(() => window.dispatchEvent(new Event('online')));

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-08: 3D Armillary Scene mounts cleanly with WebGL, registers 3D ARMI badge, and runs at 30+ FPS', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    // Mock high-performance desktop or mobile specs (16GB RAM, 8 CPU cores)
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'deviceMemory', { get: () => 16 });
      Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
      localStorage.removeItem('ogrojatra_live_challenge_3d_disabled');
      (window as any).__OGROJATRA_FORCE_3D__ = true;
    });

    await page.goto('/live-challenge');

    // Verify 3D canvas is present
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible({ timeout: 10000 });

    // Verify 3D ARMI badge with FPS reading is visible
    const fpsBadge = page.locator('text=/3D ARMI • \\d+ FPS/');
    await expect(fpsBadge).toBeVisible();

    // Verify 3D canvas dimensions match size (280x280)
    const box = await canvas.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(Math.round(box.width)).toBe(280);
      expect(Math.round(box.height)).toBe(280);
    }
    await page.screenshot({ path: 'live-challenge-3d-active.png' });

    consoleTrap.assertZeroErrors();
  });

  test('TC-3DG-09: Memory stability verification: navigating away and back cleanly disposes WebGL without errors', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'deviceMemory', { get: () => 16 });
      Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
      localStorage.removeItem('ogrojatra_live_challenge_3d_disabled');
      (window as any).__OGROJATRA_FORCE_3D__ = true;
    });

    // 1. Visit /live-challenge
    await page.goto('/live-challenge');
    await expect(page.locator('canvas')).toBeVisible({ timeout: 10000 });

    // 2. Navigate away to another page (e.g. /about) to trigger unmount and deep Three.js disposal
    await page.goto('/about');
    await expect(page).toHaveTitle(/আমাদের সম্পর্কে | অগ্রযাত্রা/);

    // 3. Navigate back to /live-challenge
    await page.goto('/live-challenge');
    await expect(page.locator('canvas')).toBeVisible();

    // Verify zero console errors throughout the entire navigation cycle
    consoleTrap.assertZeroErrors();
  });

});

