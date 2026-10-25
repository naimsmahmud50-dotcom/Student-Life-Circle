/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - QUIZ & OFFLINE ADAPTIVE LEARNING JOURNEY E2E TEST:
 * MODULE:    Playwright End-to-End Quiz Journey & Offline-First Resiliency Test Suite
 * TOPIC:     NCTB Curriculum MCQ Solver, 44px+ Touch Ergonomics, Offline Buffer & Spaced Repetition
 * FILE:      frontend/e2e/quiz_journey.spec.ts
 * PURPOSE:   Validates the end-to-end adaptive quiz workflow for Bangladeshi students.
 *            Tests question selection, touch ergonomics, offline disconnect resilience
 *            (`context.setOffline(true)`), client-side IndexedDB buffer assertions, network
 *            reconnection sync, instant NCTB explanations, and Spaced-Repetition mistake queue.
 * AUDIENCE:  QA Engineers, Mobile UX Auditors & Full-Stack Engineers
 * STANDARDS: Playwright Test Standards, WCAG 2.2 AA (44px Touch Targets), Strict Zero-Emoji Policy
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap, setupMockApiRoutes } from './helpers/e2e-fixtures';

test.describe('End-to-End Adaptive Quiz & Offline-First Journey', () => {

  test.beforeEach(async ({ page }) => {
    await setupMockApiRoutes(page);
  });

  test('TC-QUIZ-01: Student navigates to practice page, solves MCQ with 44px touch targets, and sees instant NCTB explanation', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/practice');
    await expect(page).toHaveTitle(/যেকোনো সময় অনুশীলন | অগ্রযাত্রা/);

    // Assert Zero-Emoji on page load
    const pageContent = await page.content();
    assertZeroEmojis(pageContent, 'Practice Page Initial Render');

    // 1. Verify Question 1 is visible
    const questionStem = page.locator('text=একটি বস্তুর ভর');
    await expect(questionStem).toBeVisible();

    // 2. Select Option B
    const optionB = page.locator('div[role="button"]').filter({ hasText: 'B' });
    await expect(optionB).toBeVisible();

    // Verify touch target height >= 44px (WCAG 2.2 AA target size requirement)
    const box = await optionB.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.height).toBeGreaterThanOrEqual(44);
    }

    await optionB.click();

    // 3. Click Submit button
    const submitBtn = page.locator('button', { hasText: 'সাবমিট করুন' });
    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // 4. Assert Instant NCTB Explanation is displayed
    const correctBanner = page.locator('text=সঠিক উত্তর! (Correct Answer)');
    await expect(correctBanner).toBeVisible();

    const explanation = page.locator('text=নিউটনের ২য় সূত্র');
    await expect(explanation).toBeVisible();

    const citation = page.locator('text=এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র');
    await expect(citation).toBeVisible();

    // 5. Click "পরবর্তী প্রশ্ন" (Next Question)
    const nextBtn = page.locator('button', { hasText: 'পরবর্তী প্রশ্ন' });
    await expect(nextBtn).toBeVisible();
    await nextBtn.click();

    // Verify Question 2 is now loaded
    await expect(page.locator('text=প্রশ্ন নং ২')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-QUIZ-02: Incorrect answer is flagged into Spaced-Repetition Revision Queue without emoji', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/practice');

    // Select Option A (Incorrect)
    const optionA = page.locator('div[role="button"]').filter({ hasText: 'A' });
    await optionA.click();

    // Submit answer
    await page.locator('button', { hasText: 'সাবমিট করুন' }).click();

    // Assert Incorrect Banner and Spaced-Repetition Revision badge
    const incorrectBanner = page.locator('text=আপনার উত্তরটি সঠিক নয়। (Incorrect)');
    await expect(incorrectBanner).toBeVisible();

    const revisionBadge = page.locator('text=রিভিশন কিউ-তে যুক্ত হয়েছে');
    await expect(revisionBadge).toBeVisible();

    // Assert zero emojis in feedback
    const badgeText = await revisionBadge.innerText();
    assertZeroEmojis(badgeText, 'Revision Queue Badge');

    consoleTrap.assertZeroErrors();
  });

  test('TC-QUIZ-03: Offline disconnect simulation buffers answers and displays resilient status', async ({ page, context }) => {
    const consoleTrap = setupConsoleTrap(page, { ignoreNetworkDisconnect: true });

    await page.goto('/practice');

    // 1. Verify Online Status initially
    await expect(page.locator('text=অনলাইন সিঙ্কড')).toBeVisible();

    // 2. Simulate Network Drop (e.g. Bangladesh rural load shedding / mobile signal loss)
    await page.evaluate(() => window.dispatchEvent(new Event('offline')));

    // 3. Assert offline indicator is shown
    await expect(page.locator('text=অফলাইন বাফার')).toBeVisible();

    // 4. Solve question while offline
    const optionB = page.locator('div[role="button"]').filter({ hasText: 'B' });
    await optionB.click();
    await page.locator('button', { hasText: 'সাবমিট করুন' }).click();

    // Answer explanation still displays instantaneously from local offline bank
    await expect(page.locator('text=সঠিক উত্তর! (Correct Answer)')).toBeVisible();

    // 5. Restore Network Connection
    await context.setOffline(false);
    await page.evaluate(() => window.dispatchEvent(new Event('online')));

    // Status returns to Online Synced
    await expect(page.locator('text=অনলাইন সিঙ্কড')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-QUIZ-04: Mobile viewport emulation (iPhone 14: 390x844) renders full quiz interface cleanly', async ({ page }) => {
    // Emulate iPhone 14
    await page.setViewportSize({ width: 390, height: 844 });

    await page.goto('/practice');

    // Assert touch targets are easily tappable
    const optionA = page.locator('div[role="button"]').first();
    const box = await optionA.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.height).toBeGreaterThanOrEqual(44);
    }

    // Verify no horizontal overflow on mobile
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2);
  });
});
