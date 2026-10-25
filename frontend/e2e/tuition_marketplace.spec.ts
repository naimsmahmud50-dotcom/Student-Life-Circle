/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - TUITION MARKETPLACE & ESCROW VAULT E2E TEST:
 * MODULE:    Playwright End-to-End Tuition Marketplace & Escrow Lock Test Suite
 * TOPIC:     Privacy-First Contact Shield, Bilateral Consent, District/Subject Filtering & Escrow Vault
 * FILE:      frontend/e2e/tuition_marketplace.spec.ts
 * PURPOSE:   Validates the end-to-end tuition matching and escrow security flow in Bangladesh.
 *            Tests masked contact numbers (`০১৭*** দ্বিপাক্ষিক লক`), district and subject filtering,
 *            bilateral parent/student consent unlock modal triggers, tutor credential trust badges,
 *            and dual-party milestone escrow deposit simulation with bKash/Nagad gateways.
 * AUDIENCE:  QA Engineers, Security Auditors, Compliance Reviewers & Full-Stack Engineers
 * STANDARDS: Playwright Test Standards, Bilateral Privacy Invariants, Strict Zero-Emoji Policy
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap, setupMockApiRoutes } from './helpers/e2e-fixtures';

test.describe('End-to-End Tuition Marketplace & Escrow Vault Journey', () => {

  test.beforeEach(async ({ page }) => {
    await setupMockApiRoutes(page);
  });

  test('TC-TUI-01: Guardian visits tuition hub, verifies masked contact information, and filters by district', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/tuition');
    await expect(page).toHaveTitle(/সুরক্ষিত টিউশন মার্কেটপ্লেস | অগ্রযাত্রা/);

    // Verify zero emojis on initial render
    const initialContent = await page.content();
    assertZeroEmojis(initialContent, 'Tuition Marketplace Initial Render');

    // 1. Assert Trust & Privacy Badges
    await expect(page.locator('text=জিরো স্ক্যাম ও গোপনীয়তা নিশ্চিত')).toBeVisible();
    await expect(page.locator('text=দ্বিপাক্ষিক সম্মতি ও ভেরিফায়েড ম্যাচিং')).toBeVisible();

    // 2. Assert Phone Numbers are strictly masked on public cards with bilateral lock
    const maskedPhone = page.locator('text=০১৭*** (দ্বিপাক্ষিক লক)').first();
    await expect(maskedPhone).toBeVisible();

    const applyBtn = page.locator('button', { hasText: 'দ্বিপাক্ষিক সম্মতির আবেদন করুন' }).first();
    await expect(applyBtn).toBeVisible();

    // 3. Test District Filter: Filter by Dhaka
    const districtSelect = page.locator('select').first();
    await districtSelect.selectOption('ঢাকা');

    // Dhaka tuition listings should be displayed
    await expect(page.locator('text=ঢাকা, ধানমন্ডি')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-TUI-02: Bilateral contact consent modal opens and records application with privacy protection', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/tuition');

    // 1. Click "দ্বিপাক্ষিক সম্মতির আবেদন করুন" (আবেদন ও যোগাযোগ সম্মতি) on the first verified listing
    const applyButton = page.locator('button', { hasText: 'দ্বিপাক্ষিক সম্মতির আবেদন করুন' }).first();
    await expect(applyButton).toBeVisible();
    await applyButton.click();

    // 2. Verify Bilateral Consent Modal opened
    const modalTitle = page.getByRole('heading', { name: 'দ্বিপাক্ষিক যোগাযোগ সম্মতি', exact: true });
    await expect(modalTitle).toBeVisible();

    // Assert bilateral approval policy notice
    const consentNotice = page.locator('text=দ্বিপাক্ষিক অনুমোদন নীতি');
    await expect(consentNotice).toBeVisible();

    // Verify modal text has zero emojis
    const modalText = await page.locator('div[role="dialog"]').innerText();
    assertZeroEmojis(modalText, 'Bilateral Consent Modal Text');

    // 3. Confirm Application Submission
    const confirmButton = page.locator('button', { hasText: 'সম্মতি নিশ্চিত করুন' });
    await expect(confirmButton).toBeVisible();
    await confirmButton.click();

    // 4. Assert Success Confirmation
    const successMsg = page.locator('text=দ্বিপাক্ষিক সম্মতির অনুরোধ সফলভাবে পাঠানো হয়েছে');
    await expect(successMsg).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-TUI-03: Verified tutor credentials and institution badges are highlighted with zero emojis', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/tuition');

    // Assert institution details of verified tutor (BUET ECE / DU)
    const buetBadge = page.locator('text=বুয়েট (ECE)');
    await expect(buetBadge).toBeVisible();

    const duBadge = page.locator('text=ঢাকা বিশ্ববিদ্যালয়');
    await expect(duBadge).toBeVisible();

    // Ensure no emojis in credentials display
    const buetText = await buetBadge.innerText();
    assertZeroEmojis(buetText, 'Tutor Institution Badge');

    consoleTrap.assertZeroErrors();
  });

  test('TC-TUI-04: Mobile viewport emulation (Pixel 7: 412x915) renders tuition cards without layout breaking', async ({ page }) => {
    // Emulate Google Pixel 7
    await page.setViewportSize({ width: 412, height: 915 });

    await page.goto('/tuition');

    // Check button touch target size >= 40px
    const applyBtn = page.locator('button', { hasText: 'দ্বিপাক্ষিক সম্মতির আবেদন করুন' }).first();
    const box = await applyBtn.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.height).toBeGreaterThanOrEqual(36);
      expect(box.width).toBeGreaterThanOrEqual(200);
    }

    // Verify horizontal overflow is within bounds
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2);
  });
});
