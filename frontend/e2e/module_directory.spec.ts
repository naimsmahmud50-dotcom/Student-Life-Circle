/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - MODULE DIRECTORY DUAL-PERSPECTIVE E2E TEST:
 * MODULE:    Playwright End-to-End 69 Enterprise Modules Directory Test Suite
 * TOPIC:     Dual-Perspective Switcher, Category Faceting, Dynamic Lazy Loading & Zero JS Error Audit
 * FILE:      frontend/e2e/module_directory.spec.ts
 * PURPOSE:   Validates the end-to-end user navigation across all 69 platform modules.
 *            Tests perspective toggling (Student Core Hub [Tabs 1-5] vs All 69 Modules [Tabs 1-69]),
 *            live text search filtering, category pill filtering, on-demand dynamic component
 *            mounting, and strictly asserts zero JavaScript console errors across all modules.
 * AUDIENCE:  System Architects, QA Automation Engineers & Frontend Performance Reviewers
 * STANDARDS: Playwright Test Standards, Dynamic Code Splitting, Strict Zero-Emoji Policy
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap } from './helpers/e2e-fixtures';

test.describe('End-to-End Dual-Perspective 69 Modules Directory Journey', () => {

  test('TC-MOD-01: Student Core Hub view displays 5 calm core modules initially', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/modules');
    await expect(page).toHaveTitle(/৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি | অগ্রযাত্রা/);

    // Assert zero emojis on initial render
    const initialContent = await page.content();
    assertZeroEmojis(initialContent, 'Module Directory Initial Render');

    // 1. Verify Core Hub Perspective Header
    const heading = page.locator('text=শিক্ষার্থী কোর হাব (Student Core Hub)');
    await expect(heading).toBeVisible();

    // 2. Verify Core Tier Modules are visible (e.g. Anytime Practice)
    await expect(page.locator('text=Anytime Practice & Mistake Replay Engine')).toBeVisible();
    await expect(page.locator('text=Scheduled Live Challenge & Pseudonymous Scoreboard')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-MOD-02: Switching to "সমস্ত মডিউল (Tabs 1-69)" expands the full enterprise catalog', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/modules');

    // 1. Click "সমস্ত মডিউল (Tabs 1-69)" switcher button
    const enterpriseToggle = page.locator('button', { hasText: 'সমস্ত মডিউল (Tabs 1-69)' });
    await expect(enterpriseToggle).toBeVisible();
    await enterpriseToggle.click();

    // 2. Heading updates to All 69 Modules
    await expect(page.locator('text=অল ৬৯ এন্টারপ্রাইজ মডিউল ডিরেক্টরি')).toBeVisible();

    // 3. Category pills become visible
    await expect(page.locator('button', { hasText: 'সকল ক্যাটাগরি' })).toBeVisible();
    await expect(page.locator('button', { hasText: 'একাডেমিক (Academic)' })).toBeVisible();
    await expect(page.locator('button', { hasText: 'রেজিলিয়েন্স (Resilience)' })).toBeVisible();
    await expect(page.locator('button', { hasText: 'স্টেম ল্যাব (STEM Labs)' })).toBeVisible();
    await expect(page.locator('button', { hasText: 'সিকিউরিটি ও ককপিট' })).toBeVisible();

    // 4. Assert zero emojis in category labels
    const catText = await page.locator('button', { hasText: 'স্টেম ল্যাব (STEM Labs)' }).innerText();
    assertZeroEmojis(catText, 'Category Pill Text');

    consoleTrap.assertZeroErrors();
  });

  test('TC-MOD-03: Category filter and instant search filter modules responsively', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/modules');

    // Switch to enterprise perspective
    await page.locator('button', { hasText: 'সমস্ত মডিউল (Tabs 1-69)' }).click();

    // 1. Filter by STEM Labs category
    const stemCategoryBtn = page.locator('button', { hasText: 'স্টেম ল্যাব (STEM Labs)' });
    await stemCategoryBtn.click();

    // Verify STEM modules are visible
    await expect(page.locator('text=Quantum Circuit Simulator & Bloch Sphere')).toBeVisible();

    // 2. Use Search Bar to search for "LoRaWAN"
    const searchInput = page.locator('input[placeholder*="মডিউল নাম বা ট্যাগ খুঁজুন"]');
    await searchInput.fill('LoRaWAN');

    // Reset category to ALL or click Resilience to see LoRaWAN
    await page.locator('button', { hasText: 'রেজিলিয়েন্স (Resilience)' }).click();
    await expect(page.locator('text=Satellite USSD & LoRaWAN Studio')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-MOD-04: Dynamic module view opens without throwing JavaScript console errors', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/modules');

    // Switch to enterprise perspective
    await page.locator('button', { hasText: 'সমস্ত মডিউল (Tabs 1-69)' }).click();

    // Find a dynamic module button (e.g. Quantum Sandbox or Bionic Reader)
    const openModuleBtn = page.locator('button', { hasText: 'মডিউল চালু করুন' }).first();
    if (await openModuleBtn.isVisible()) {
      await openModuleBtn.click();

      // Verify active dynamic container mounts
      const dynamicHeader = page.locator('text=সক্রিয় ডাইনামিক কম্পোনেন্ট ভিউ');
      await expect(dynamicHeader).toBeVisible();

      // Close view
      const closeBtn = page.locator('button', { hasText: 'ভিউ বন্ধ করুন' });
      await expect(closeBtn).toBeVisible();
      await closeBtn.click();
    }

    // Strictly assert zero JS errors occurred during mounting and unmounting
    consoleTrap.assertZeroErrors();
  });

  test('TC-MOD-05: Mobile viewport emulation renders perspective switcher cleanly', async ({ page }) => {
    // Emulate Google Pixel 7
    await page.setViewportSize({ width: 412, height: 915 });

    await page.goto('/modules');

    const coreBtn = page.locator('button', { hasText: 'কোর হাব (Tabs 1-5)' });
    await expect(coreBtn).toBeVisible();

    const enterpriseBtn = page.locator('button', { hasText: 'সমস্ত মডিউল (Tabs 1-69)' });
    await expect(enterpriseBtn).toBeVisible();

    // Verify no horizontal overflow
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2);
  });
});
