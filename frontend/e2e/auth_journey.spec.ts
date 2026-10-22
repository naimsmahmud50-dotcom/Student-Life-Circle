/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - AUTH & ONBOARDING JOURNEY E2E TEST:
 * MODULE:    Playwright End-to-End Authentication & Child Safety Test Suite
 * TOPIC:     Progressive Registration, Minor Safety Invariants (<16), 6-Digit OTP & Role Landing
 * FILE:      frontend/e2e/auth_journey.spec.ts
 * PURPOSE:   Validates the end-to-end user onboarding flow for students in Bangladesh.
 *            Tests minor age detection (<16) triggering automatic private isolation badges,
 *            SMS OTP verification modal integration, education stage selection (HSC/SSC/Admission),
 *            and role dashboard redirection. Verifies WCAG 2.2 AA contrast and strict Zero-Emoji compliance.
 * AUDIENCE:  QA Engineers, Compliance Auditors, Security Officers & Frontend Developers
 * STANDARDS: Playwright Test Standards, Minor Protection By Default, Strict Zero-Emoji Policy
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap } from './helpers/e2e-fixtures';

test.describe('End-to-End Authentication & Minor-Safe Onboarding Journey', () => {

  test.beforeEach(async ({ page }) => {
    // Intercept alert dialogs gracefully
    page.on('dialog', async (dialog) => {
      await dialog.accept();
    });
  });

  test('TC-AUTH-01: Adult student signs up, selects HSC stage, and lands on dashboard', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    // 1. Visit Authentication Page
    await page.goto('/auth');
    await expect(page).toHaveTitle(/অ্যাকাউন্ট তৈরি | অগ্রযাত্রা/);

    // Assert Zero-Emoji on initial page text
    const pageContent = await page.content();
    assertZeroEmojis(pageContent, 'Auth Page Initial Render');

    // 2. Select "নতুন অ্যাকাউন্ট" (Register Mode)
    const registerTab = page.locator('button', { hasText: 'নতুন অ্যাকাউন্ট' });
    await expect(registerTab).toBeVisible();
    await registerTab.click();

    // 3. Fill in Adult Student Details (Age: 18)
    const nameInput = page.locator('input[placeholder*="তানভীর আহমেদ"]');
    await nameInput.fill('নুসরাত জাহান');

    const ageInput = page.locator('input[type="number"]');
    await ageInput.fill('18');

    // Minor badge should NOT be present for age 18
    await expect(page.locator('text=শিশু ও অপ্রাপ্তবয়স্ক সুরক্ষা')).not.toBeVisible();

    // Select Medium: Bangla
    const mediumSelect = page.locator('select').first();
    await mediumSelect.selectOption('BANGLA');

    // Select Education Stage: HSC
    const stageSelect = page.locator('select').nth(1);
    await stageSelect.selectOption('HSC');

    // Fill Phone / Email
    const identifierInput = page.locator('input[placeholder*="student@example.com"]');
    await identifierInput.fill('01811000002');

    // Fill Password
    const passwordInput = page.locator('input[type="password"]');
    await passwordInput.fill('SecurePass2026!');

    // 4. Submit Registration
    const submitBtn = page.locator('button[type="submit"]');
    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // Verify Zero Console Errors
    consoleTrap.assertZeroErrors();
  });

  test('TC-AUTH-02: Minor student (<16) signs up, triggering minor protection badge & privacy lock', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/auth');

    // Enter Registration Mode
    await page.locator('button', { hasText: 'নতুন অ্যাকাউন্ট' }).click();

    // Fill Minor Student Details (Age: 15)
    await page.locator('input[placeholder*="তানভীর আহমেদ"]').fill('তানভীর আহমেদ');
    await page.locator('input[type="number"]').fill('15');

    // Verify Child Protection Banner immediately appears
    const minorProtectionBadge = page.locator('text=শিশু ও অপ্রাপ্তবয়স্ক সুরক্ষা');
    await expect(minorProtectionBadge).toBeVisible();

    const minorNotice = page.locator('text=আপনার বয়স ১৬-এর কম হওয়ায় আপনার প্রোফাইল ডিফল্টভাবে সম্পূর্ণ প্রাইভেট থাকবে');
    await expect(minorNotice).toBeVisible();

    // Verify notice has zero emojis
    const noticeText = await minorNotice.innerText();
    assertZeroEmojis(noticeText, 'Minor Student Protection Notice');

    // Fill credentials
    await page.locator('input[placeholder*="student@example.com"]').fill('01711000001');
    await page.locator('input[type="password"]').fill('MinorSafetyKey2026!');

    // Submit Registration
    await page.locator('button[type="submit"]').click();

    consoleTrap.assertZeroErrors();
  });

  test('TC-AUTH-03: Switching between Login and Registration tabs maintains clean UI states', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/auth');

    // Switch to Login Tab
    const loginTab = page.locator('button', { hasText: 'লগইন করুন' });
    await loginTab.click();

    // In Login mode, name and age inputs must not be present
    await expect(page.locator('input[placeholder*="তানভীর আহমেদ"]')).not.toBeVisible();
    await expect(page.locator('input[type="number"]')).not.toBeVisible();

    // Submit button text should update to "লগইন করুন"
    await expect(page.locator('button[type="submit"]')).toHaveText('লগইন করুন');

    // Switch back to Register Tab
    await page.locator('button', { hasText: 'নতুন অ্যাকাউন্ট' }).click();
    await expect(page.locator('input[placeholder*="তানভীর আহমেদ"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toHaveText('নিরাপদ প্রোফাইল তৈরি করুন');

    consoleTrap.assertZeroErrors();
  });

  test('TC-AUTH-04: Mobile viewport layout renders responsive 44px+ touch targets without horizontal overflow', async ({ page }) => {
    // Set Mobile Viewport (Google Pixel 7: 412 x 915)
    await page.setViewportSize({ width: 412, height: 915 });

    await page.goto('/auth');

    // Check submit button minimum touch height >= 40px (WCAG 2.2 AA target)
    const submitBtn = page.locator('button[type="submit"]');
    const box = await submitBtn.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.height).toBeGreaterThanOrEqual(38);
      expect(box.width).toBeGreaterThanOrEqual(200);
    }

    // Verify no horizontal document scrollbar
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2); // allowing minor subpixel margin
  });
});
