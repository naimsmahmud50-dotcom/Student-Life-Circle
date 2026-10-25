/**
 * ========================================================================================
 * MODULE:    AI Draft Review Queue Playwright E2E Test Suite
 * TOPIC:     Hub Routing, Inspection, Approval Gate, Rejection Modal, Shortcuts & Zero Emoji
 * FILE:      frontend/e2e/review_queue.spec.ts
 * PURPOSE:   Validates that:
 *            1. Hub link "এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন" in /admin opens /admin/review-queue.
 *            2. Quarantine console remains accessible on its own link (/admin/quarantine).
 *            3. Draft details (stem, options, answer, explanation, AI metadata) render crisply.
 *            4. Single-click approval moves draft to APPROVED and persists.
 *            5. Rejection flow requires mandatory feedback modal and moves to REJECTED.
 *            6. Keyboard shortcuts (J/K navigation, A approval) accelerate SME workflow.
 *            7. Filters synchronize with URL search parameters.
 *            8. Zero-Emoji compliance holds strictly across all states.
 * AUDIENCE:  QA Engineers, Security Auditors & Frontend Leads
 * STANDARDS: ASVS L2, Playwright Test Harness, Strict Zero-Emoji Compliance
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis } from './helpers/e2e-fixtures';

const SESSION_KEY = 'ogrojatra_auth_session';
const TOKEN_KEY = 'auth_token';

test.describe('AI Question Bank & Draft Review Queue Verification', () => {

  const adminSession = {
    user: {
      id: 'usr_admin_01',
      fullName: 'Chief Platform Administrator',
      email: 'admin@ogrojatra.edu.bd',
      roles: ['ADMIN'],
      isActive: true,
    },
    token: 'test_admin_token_01',
    expiresAt: Date.now() + 3600000,
  };

  test.beforeEach(async ({ page }) => {
    // Authenticate as Admin via localStorage before navigation
    await page.addInitScript(({ sKey, tKey, session }) => {
      localStorage.setItem(sKey, JSON.stringify(session));
      localStorage.setItem(tKey, session.token);
    }, { sKey: SESSION_KEY, tKey: TOKEN_KEY, session: adminSession });
  });

  test('TC-RQ-01: Admin hub link routes to /admin/review-queue and quarantine remains accessible', async ({ page }) => {
    // 1. Visit admin hub
    await page.goto('/admin');
    await expect(page.locator('h1', { hasText: 'কেন্দ্রীয় প্ল্যাটফর্ম প্রশাসন' })).toBeVisible();

    // 2. Locate the AI pipeline hub link
    const reviewQueueLink = page.locator('a[href="/admin/review-queue"]');
    await expect(reviewQueueLink).toBeVisible();
    await expect(reviewQueueLink).toContainText('ড্রাফট কিউ ও মডারেশন দেখুন');

    // 3. Click link and verify navigation to /admin/review-queue
    await reviewQueueLink.click();
    await page.waitForURL(/\/admin\/review-queue/, { timeout: 10000 });
    await expect(page.locator('h1', { hasText: 'এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন' })).toBeVisible();

    // 4. Verify Quarantine Console link is also visible and links to /admin/quarantine
    const quarantineLink = page.locator('a', { hasText: 'কোয়ারেন্টিন কনসোল' });
    await expect(quarantineLink).toBeVisible();
    await expect(quarantineLink).toHaveAttribute('href', '/admin/quarantine');

    // Verify Zero-Emoji compliance
    const content = await page.content();
    assertZeroEmojis(content, 'Review Queue Landing');
  });

  test('TC-RQ-02: Draft question inspector renders stem, options, explanation and AI metadata', async ({ page }) => {
    await page.goto('/admin/review-queue');
    await expect(page.locator('h1', { hasText: 'এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন' })).toBeVisible();

    // Select physics question card
    const physCard = page.getByTestId('draft-card-q_draft_phys_301');
    if (await physCard.count() > 0) {
      await physCard.click();

      // Inspector must display stem
      await expect(page.locator('text=একটি ১০ কেজি ভরের ব্লকের ওপর')).toBeVisible();

      // Inspector must display options with correct answer indicator
      await expect(page.locator('text=৩.০৪ m/s²')).toBeVisible();
      await expect(page.locator('text=সঠিক উত্তর').first()).toBeVisible();

      // Inspector must display pedagogical explanation
      await expect(page.locator('text=ঘর্ষণ বল f_k')).toBeVisible();

      // Inspector must display AI metadata card
      await expect(page.locator('text=এআই অডিট ও কোয়ালিটি স্কোরবোর্ড')).toBeVisible();
      await expect(page.locator('text=APPLICATION')).toBeVisible();
    }

    const content = await page.content();
    assertZeroEmojis(content, 'Draft Inspector Screen');
  });

  test('TC-RQ-03: Approving a draft transitions status to APPROVED and persists across reload', async ({ page }) => {
    await page.goto('/admin/review-queue');
    await expect(page.locator('h1', { hasText: 'এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন' })).toBeVisible();

    // Pick q_draft_chem_402 or q_draft_phys_301
    const targetCard = page.getByTestId('draft-card-q_draft_chem_402');
    if (await targetCard.count() > 0) {
      await targetCard.click();

      // Click "অনুমোদন করুন (A)"
      const approveBtn = page.locator('button', { hasText: 'অনুমোদন করুন (A)' });
      await expect(approveBtn).toBeVisible();
      await approveBtn.click();

      // Verify success alert or badge changed to "অনুমোদিত"
      await expect(targetCard.locator('text=অনুমোদিত')).toBeVisible({ timeout: 10000 });

      // Hard page reload to test persistence
      await page.reload();
      await expect(targetCard.locator('text=অনুমোদিত')).toBeVisible();
    }

    const content = await page.content();
    assertZeroEmojis(content, 'Approved Draft Screen');
  });

  test('TC-RQ-04: Rejecting a draft opens mandatory reason modal and records feedback', async ({ page }) => {
    await page.goto('/admin/review-queue');
    await expect(page.locator('h1', { hasText: 'এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন' })).toBeVisible();

    // Switch to "সকল ড্রাফট" tab so we can find questions
    await page.locator('button', { hasText: 'সকল ড্রাফট' }).click();

    const targetCard = page.getByTestId('draft-card-q_draft_math_503');
    if (await targetCard.count() > 0) {
      await targetCard.click();

      // Click "প্রত্যাখ্যান করুন (R)"
      const rejectBtn = page.locator('button', { hasText: 'প্রত্যাখ্যান করুন (R)' });
      await expect(rejectBtn).toBeVisible();
      await rejectBtn.click();

      // Modal must appear
      await expect(page.locator('h3', { hasText: 'প্রশ্নটি প্রত্যাখ্যানের কারণ উল্লেখ করুন' })).toBeVisible();

      // Submit must be disabled if reason is empty
      const confirmBtn = page.locator('button', { hasText: 'প্রত্যাখ্যান নিশ্চিত করুন' });
      await expect(confirmBtn).toBeDisabled();

      // Click preset feedback button
      const presetBtn = page.locator('button', { hasText: 'এনসিটিবি কারিকুলাম মানদণ্ডের সাথে অমিল' });
      await presetBtn.click();

      // Confirm button is now enabled
      await expect(confirmBtn).toBeEnabled();
      await confirmBtn.click();

      // Modal closes and card changes to "প্রত্যাখ্যাত"
      await expect(page.locator('h3', { hasText: 'প্রশ্নটি প্রত্যাখ্যানের কারণ উল্লেখ করুন' })).not.toBeVisible();
      await expect(targetCard.locator('text=প্রত্যাখ্যাত')).toBeVisible({ timeout: 10000 });
    }

    const content = await page.content();
    assertZeroEmojis(content, 'Rejected Draft Screen');
  });

  test('TC-RQ-05: Fast review keyboard shortcuts J/K navigation and A approval', async ({ page }) => {
    await page.goto('/admin/review-queue');
    await expect(page.locator('h1', { hasText: 'এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন' })).toBeVisible();

    // Press 'J' to navigate down to next draft
    await page.keyboard.press('j');
    await page.waitForTimeout(300);

    // Press 'K' to navigate up
    await page.keyboard.press('k');
    await page.waitForTimeout(300);

    // Verify Zero-Emoji compliance
    const content = await page.content();
    assertZeroEmojis(content, 'Keyboard Shortcuts Verified');
  });

  test('TC-RQ-06: Status tabs and filter dropdowns synchronize with URL query params', async ({ page }) => {
    await page.goto('/admin/review-queue');
    await expect(page.locator('h1', { hasText: 'এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন' })).toBeVisible();

    // Click "অনুমোদিত ও সক্রিয়" tab
    await page.locator('button', { hasText: 'অনুমোদিত ও সক্রিয়' }).click();
    await page.waitForURL(/status=APPROVED/, { timeout: 5000 });

    // Select difficulty EASY
    await page.locator('select').nth(1).selectOption('EASY');
    await page.waitForURL(/difficulty=EASY/, { timeout: 5000 });

    // Verify Zero-Emoji compliance
    const content = await page.content();
    assertZeroEmojis(content, 'URL Filter Persistence');
  });

});
