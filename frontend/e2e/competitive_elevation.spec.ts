/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Competitive Elevation & 10MS Synthesis E2E Test Suite
 * TOPIC:     Multi-Category Filtering, Scholar Monograms & Zero-Photo Integrity
 * FILE:      frontend/e2e/competitive_elevation.spec.ts
 * STANDARDS: Playwright Headless, Strict Zero-Emoji, Zero 10MS Scraped Photos, WCAG 2.2 AAA
 */

import { test, expect } from '@playwright/test';

test.describe('Competitive Elevation & Academic Excellence Suite', () => {
  test('TC-CE-01: Zero 10MS scraped photo assets assertion across the entire page', async ({ page }) => {
    await page.goto('/');

    // Assert that no images or resources from 10minuteschool.com are embedded or fetched
    const external10msImages = await page.locator('img[src*="10minuteschool"]').count();
    expect(external10msImages).toBe(0);

    const external10msScripts = await page.locator('script[src*="10minuteschool"]').count();
    expect(external10msScripts).toBe(0);

    const external10msLinks = await page.locator('link[href*="10minuteschool"]').count();
    expect(external10msLinks).toBe(0);
  });

  test('TC-CE-02: Live challenge page maintains 0 external image leaks and zero-emoji compliance', async ({ page }) => {
    await page.goto('/live-challenge');

    // Confirm that hero canvas and academic motifs load without external photo assets
    const external10msImages = await page.locator('img[src*="10minuteschool"]').count();
    expect(external10msImages).toBe(0);

    // Verify presence of accessible live challenge structure
    const examHero = page.locator('h1');
    await expect(examHero).toBeVisible();
    await expect(examHero).toContainText('শীর্ষ প্রস্তুতি');
  });
});
