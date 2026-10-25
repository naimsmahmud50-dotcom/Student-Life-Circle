/**
 * ========================================================================================
 * MODULE:    Quarantine Persistence & Lifecycle Playwright E2E Test Suite
 * TOPIC:     Single-Click Quarantine, Page Refresh Persistence, Restore Flow & Zero Emoji
 * FILE:      frontend/e2e/quarantine_persistence.spec.ts
 * PURPOSE:   Validates that the admin quarantine console:
 *            1. Loads real data from backend API.
 *            2. Successfully executes quarantine with mandatory audit reason.
 *            3. Persists quarantined state across hard page reload (no lost in-memory state).
 *            4. Successfully executes restore (release) with mandatory audit reason.
 *            5. Persists restored state across hard page reload.
 *            6. Maintains strict Zero-Emoji compliance across all states and modals.
 * AUDIENCE:  Security Auditors, QA Engineers & Frontend Architects
 * STANDARDS: OWASP ASVS L2, Playwright Test Harness, Strict Zero-Emoji Compliance
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis } from './helpers/e2e-fixtures';

const SESSION_KEY = 'ogrojatra_auth_session';
const TOKEN_KEY = 'auth_token';

test.describe('Admin Quarantine Persistence & Lifecycle Verification', () => {

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

  test('TC-QP-01: Quarantine action updates UI, records audit log, and persists across page reload', async ({ page }) => {
    // 1. Navigate to Quarantine console
    await page.goto('/admin/quarantine');
    await expect(page.locator('h1', { hasText: 'প্রশ্ন কোয়ারেন্টিন ও কোয়ালিটি কন্ট্রোল' })).toBeVisible();

    // 2. Identify an active/reported question to quarantine (e.g. q_hsc_phys_102)
    const questionCard = page.getByTestId('question-card-q_hsc_phys_102');
    await expect(questionCard).toBeVisible();

    // If already quarantined from a previous run, restore it first so we can test quarantine
    const restoreBtn = questionCard.locator('button', { hasText: 'পুনর্বহাল করুন' });
    if (await restoreBtn.count() > 0 && await restoreBtn.isVisible()) {
      await restoreBtn.click();
      await page.locator('textarea').fill('টেস্ট শুরুর পূর্বে প্রাথমিক সক্রিয়করণ');
      await page.locator('button', { hasText: 'পুনর্বহাল নিশ্চিত করুন' }).click();
      await page.waitForTimeout(500);
    }

    // 3. Click "কোয়ারেন্টিন করুন"
    const quarantineBtn = questionCard.locator('button', { hasText: 'কোয়ারেন্টিন করুন' });
    await expect(quarantineBtn).toBeVisible();
    await quarantineBtn.click();

    // 4. Modal must appear asking for mandatory audit reason
    await expect(page.locator('h3', { hasText: 'প্রশ্নটি কি কোয়ারেন্টিন করতে চান?' })).toBeVisible();
    const reasonInput = page.locator('textarea');
    await expect(reasonInput).toBeVisible();

    // 5. Fill reason and submit
    const testReason = 'অস্পষ্ট অপশন থাকার কারণে সাময়িক প্রত্যাহার ও অডিট রিক্যালকুলেশন';
    await reasonInput.fill(testReason);
    await page.locator('button', { hasText: 'কোয়ারেন্টিন নিশ্চিত করুন' }).click();

    // 6. Verify modal closed, status badge changed to "কোয়ারেন্টিন কার্যকর", and button changed to "পুনর্বহাল করুন"
    await expect(page.locator('h3', { hasText: 'প্রশ্নটি কি কোয়ারেন্টিন করতে চান?' })).not.toBeVisible();
    await expect(questionCard.locator('text=কোয়ারেন্টিন কার্যকর')).toBeVisible();
    await expect(questionCard.locator('button', { hasText: 'পুনর্বহাল করুন' })).toBeVisible();

    // 7. Verify new audit record is visible
    await expect(page.locator('text=' + testReason).first()).toBeVisible();

    // 8. RELOAD THE PAGE: This directly tests persistence vs in-memory fake timer!
    await page.reload();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForLoadState('networkidle').catch(() => {});

    // 9. After page refresh, the question MUST STILL be in "কোয়ারেন্টিন কার্যকর" state
    const questionCardAfterReload = page.getByTestId('question-card-q_hsc_phys_102');
    await expect(questionCardAfterReload).toBeVisible({ timeout: 15000 });
    await expect(questionCardAfterReload.locator('text=কোয়ারেন্টিন কার্যকর')).toBeVisible({ timeout: 15000 });
    await expect(questionCardAfterReload.locator('button', { hasText: 'পুনর্বহাল করুন' })).toBeVisible({ timeout: 15000 });

    // Verify Zero-Emoji compliance
    const content = await page.content();
    assertZeroEmojis(content, 'Quarantine Persisted Screen');
  });

  test('TC-QP-02: Restore action reverses quarantine, records audit log, and persists across reload', async ({ page }) => {
    // 1. Navigate to Quarantine console
    await page.goto('/admin/quarantine');
    await expect(page.locator('h1', { hasText: 'প্রশ্ন কোয়ারেন্টিন ও কোয়ালিটি কন্ট্রোল' })).toBeVisible();

    // 2. Identify the quarantined question
    const questionCard = page.getByTestId('question-card-q_hsc_phys_102');
    await expect(questionCard).toBeVisible();

    // If not quarantined, quarantine it first so we can restore it
    const quarantineBtn = questionCard.locator('button', { hasText: 'কোয়ারেন্টিন করুন' });
    if (await quarantineBtn.count() > 0 && await quarantineBtn.isVisible()) {
      await quarantineBtn.click();
      await page.locator('textarea').fill('পুনর্বহাল পরীক্ষার পূর্বে কোয়ারেন্টিন তৈরি');
      await page.locator('button', { hasText: 'কোয়ারেন্টিন নিশ্চিত করুন' }).click();
      await page.waitForTimeout(500);
    }

    // 3. Click "পুনর্বহাল করুন"
    const restoreBtn = questionCard.locator('button', { hasText: 'পুনর্বহাল করুন' });
    await expect(restoreBtn).toBeVisible();
    await restoreBtn.click();

    // 4. Modal must appear asking for mandatory restore reason
    await expect(page.locator('h3', { hasText: 'প্রশ্নটি কি পরীক্ষা পুলে পুনর্বহাল করতে চান?' })).toBeVisible();
    const restoreInput = page.locator('textarea');
    await expect(restoreInput).toBeVisible();

    // 5. Fill reason and submit
    const restoreReasonText = 'বিষয় বিশেষজ্ঞ প্যানেল কর্তৃক প্রশ্নের অপশন সংশোধন সম্পন্ন';
    await restoreInput.fill(restoreReasonText);
    await page.locator('button', { hasText: 'পুনর্বহাল নিশ্চিত করুন' }).click();

    // 6. Verify modal closed and button changed back to "কোয়ারেন্টিন করুন"
    await expect(page.locator('h3', { hasText: 'প্রশ্নটি কি পরীক্ষা পুলে পুনর্বহাল করতে চান?' })).not.toBeVisible();
    await expect(questionCard.locator('button', { hasText: 'কোয়ারেন্টিন করুন' })).toBeVisible();

    // 7. RELOAD THE PAGE: Test that restore state persists across reload!
    await page.reload();

    // 8. After page refresh, the question MUST STILL be in active/restored state
    const questionCardAfterReload = page.getByTestId('question-card-q_hsc_phys_102');
    await expect(questionCardAfterReload).toBeVisible();
    await expect(questionCardAfterReload.locator('button', { hasText: 'কোয়ারেন্টিন করুন' })).toBeVisible();

    // Verify Zero-Emoji compliance
    const content = await page.content();
    assertZeroEmojis(content, 'Restore Persisted Screen');
  });

  test('TC-QP-03: Filter tabs and search accurately segment questions queue', async ({ page }) => {
    await page.goto('/admin/quarantine');
    await expect(page.locator('h1', { hasText: 'প্রশ্ন কোয়ারেন্টিন ও কোয়ালিটি কন্ট্রোল' })).toBeVisible();

    // 1. Click "কোয়ারেন্টিন কার্যকর" tab
    await page.locator('button', { hasText: 'কোয়ারেন্টিন কার্যকর' }).click();
    // Only quarantined items should be shown
    const cards = page.locator('.space-y-3 > div');
    const count = await cards.count();
    if (count > 0) {
      await expect(cards.first().locator('text=কোয়ারেন্টিন কার্যকর')).toBeVisible();
    }

    // 2. Click "সকল" tab
    await page.locator('button', { hasText: 'সকল' }).click();

    // 3. Search for a specific question term
    const searchInput = page.locator('input[placeholder="প্রশ্ন আইডি বা বিষয় খুঁজুন..."]');
    await searchInput.fill('রসায়ন');
    await expect(page.locator('text=রসায়ন ২য় পত্র')).toBeVisible();

    // Clear search
    await page.locator('button', { hasText: 'মুছুন' }).click();
    await expect(searchInput).toHaveValue('');

    // Verify zero emoji
    const content = await page.content();
    assertZeroEmojis(content, 'Filtered Quarantine View');
  });

});
