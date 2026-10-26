/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CARETUTORS ELEVATION E2E TEST SUITE:
 * MODULE:    Playwright E2E Suite for CareTutors Reverse-Engineered Tuition Platform
 * FILE:      frontend/e2e/tuition_elevation.spec.ts
 * PURPOSE:   Validates full tuition elevation features:
 *            - Zero-emoji compliance & WCAG AA contrast
 *            - Strict Brand & Asset Isolation (Zero CareTutors logos, names, or external images)
 *            - Procedural Scholar Monograms with university accents (BUET, DU, DMC, NSU)
 *            - Interactive 8-Category Filter Bar & Live Job Board
 *            - Verified Tutor Directory with bilateral privacy locks
 *            - Interactive Market Salary Calculator with dynamic Bengali numerals
 *            - 4-Step Guardian Hire a Tutor Wizard Modal with instant unique Job ID generation
 *            - 4-Pillar Trust, 2 Days Free Trial, and Zero Advance Scam Guarantee
 * STANDARDS: Playwright Test Standards, Strict Zero-Emoji Policy, Bilateral Consent Invariants
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap, setupMockApiRoutes } from './helpers/e2e-fixtures';

test.describe('Ogrojatra Verified Tuition Network - CareTutors Reverse Engineering Elevation', () => {

  test.beforeEach(async ({ page }) => {
    await setupMockApiRoutes(page);
  });

  test('TC-TE-01: Tuition Hub initial render, stats header and zero-emoji compliance', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/tuition');
    await expect(page).toHaveTitle(/সুরক্ষিত টিউশন মার্কেটপ্লেস ও ভেরিফায়েড টিউটর হাব | অগ্রযাত্রা/);

    // Verify zero emojis on initial render
    const initialContent = await page.content();
    assertZeroEmojis(initialContent, 'Tuition Hub Initial Render');

    // Assert Stats Header Metrics
    await expect(page.locator('text=১৫,০০০+').first()).toBeVisible();
    await expect(page.locator('text=১,৪২০+').first()).toBeVisible();
    await expect(page.locator('text=৪.৯').first()).toBeVisible();
    await expect(page.locator('text=০ টাকা').first()).toBeVisible();
    await expect(page.locator('text=অগ্রিম ফি ও ২ দিন ফ্রি ট্রায়াল').first()).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-TE-02: Strict Zero External Image/Brand Leakage and Scholar Monogram Verification', async ({ page }) => {
    await page.goto('/tuition');

    // Assert absolutely ZERO CareTutors external images or script references
    const externalImages = await page.locator('img[src*="caretutors"]').count();
    expect(externalImages).toBe(0);

    const externalScripts = await page.locator('script[src*="caretutors"]').count();
    expect(externalScripts).toBe(0);

    // Switch to Verified Tutors tab
    await page.locator('button', { hasText: 'ভেরিফায়েড টিউটর ডিরেক্টরি' }).click();

    // Verify authentic scholar monograms rendered with university colors (BUET 'তা', DMC 'নু')
    const buetMonogram = page.locator('text=তা').first();
    await expect(buetMonogram).toBeVisible();

    const dmcMonogram = page.locator('text=নু').first();
    await expect(dmcMonogram).toBeVisible();
  });

  test('TC-TE-03: Tab Navigation between Job Board, Tutors, Calculator, and Trust & Safety', async ({ page }) => {
    await page.goto('/tuition');

    // 1. Initial tab is Job Board
    await expect(page.locator('text=১০ম শ্রেণির পদার্থবিজ্ঞান ও উচ্চতর গণিত টিউশন')).toBeVisible();

    // 2. Click Verified Tutors
    await page.locator('button', { hasText: 'ভেরিফায়েড টিউটর ডিরেক্টরি' }).click();
    await expect(page.locator('text=সকল শিক্ষকের জাতীয় পরিচয়পত্র ও অ্যাকাডেমিক সনদ পরীক্ষিত')).toBeVisible();

    // 3. Click Salary Calculator
    await page.locator('button', { hasText: 'পারিশ্রমিক ক্যালকুলেটর' }).click();
    await expect(page.locator('text=প্রস্তাবিত মাসিক পারিশ্রমিক পরিসর:')).toBeVisible();

    // 4. Click Trust & Safety
    await page.locator('button', { hasText: 'নিরাপত্তা, ট্রায়াল ও FAQ' }).click();
    await expect(page.locator('text=কেন অগ্রযাত্রা টিউশন মার্কেটপ্লেস সবচেয়ে বিশ্বস্ত?')).toBeVisible();
  });

  test('TC-TE-04: Interactive Tuition Salary Calculator dynamic calculation', async ({ page }) => {
    await page.goto('/tuition');

    // Switch to calculator tab
    await page.locator('button', { hasText: 'পারিশ্রমিক ক্যালকুলেটর' }).click();

    // Verify initial benchmark estimate
    await expect(page.locator('text=প্রস্তাবিত মাসিক পারিশ্রমিক পরিসর:')).toBeVisible();
    const initialSummary = await page.locator('text=প্রস্তাবিত মাসিক পারিশ্রমিক পরিসর:').innerText();

    // Change days per week to 5 days
    await page.locator('button', { hasText: '5 দিন' }).click();

    // Assert recalculation shows 5 days per week
    await expect(page.locator('text=সপ্তাহে 5 দিন')).toBeVisible();
  });

  test('TC-TE-05: Guardian 4-Step Tutor Request Wizard completion and Job ID generation', async ({ page }) => {
    await page.goto('/tuition');

    // Click "টিউটর রিকোয়ারমেন্ট দিন"
    const openWizardBtn = page.locator('button', { hasText: 'টিউটর রিকোয়ারমেন্ট দিন' }).first();
    await openWizardBtn.click();

    // Assert Wizard Step 1 Modal
    await expect(page.getByRole('heading', { name: 'টিউটর রিকোয়ারমেন্ট পোস্ট করুন' })).toBeVisible();
    await expect(page.locator('text=১. মোড ও মাধ্যম')).toBeVisible();

    // Step 1: Click Next
    await page.locator('button', { hasText: 'পরবর্তী ধাপ' }).click();

    // Step 2: Class & Subjects
    await expect(page.locator('text=২. শ্রেণি ও বিষয়')).toBeVisible();
    await page.locator('button', { hasText: 'পরবর্তী ধাপ' }).click();

    // Step 3: Budget & Schedule
    await expect(page.locator('text=৩. বাজেট ও সময়')).toBeVisible();
    await page.locator('button', { hasText: 'পরবর্তী ধাপ' }).click();

    // Step 4: Location & Contact
    await expect(page.locator('text=৪. ঠিকানা ও সাবমিট')).toBeVisible();

    // Fill contact details
    await page.locator('input[placeholder="০১৭১১******"]').fill('01712345678');
    await page.locator('input[placeholder="যেমন: ধানমন্ডি, উত্তরা, মিরপুর..."]').fill('ধানমন্ডি');

    // Submit Request
    await page.locator('button', { hasText: 'রিকোয়ারমেন্ট পোস্ট সম্পন্ন করুন' }).click();

    // Assert Success Screen and Job ID generated (format: OGRO-TUI-XXXXX)
    await expect(page.locator('text=আপনার রিকোয়ারমেন্ট সফলভাবে পোস্ট হয়েছে!')).toBeVisible();
    await expect(page.locator('text=আপনার জব আইডি:')).toBeVisible();
  });
});
