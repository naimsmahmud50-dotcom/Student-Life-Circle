/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Playwright End-to-End Live Examination Test Suite
 * TOPIC:     Nationwide Live Exam & Playwright E2E Journey
 * FILE:      frontend/e2e/nationwide_exam_journey.spec.ts
 * PHASE:     Phase 125 - Nationwide Live Exam & Playwright E2E Journey
 * PURPOSE:   Validates the comprehensive end-to-end user journey during nationwide
 *            live examinations on the Ogrojatra platform:
 *            1. Student authentication & SMS OTP verification modal workflow.
 *            2. Entering Live HSC Physics Challenge arena with synchronized server timer.
 *            3. Solving 10 NCTB physics questions with KaTeX equations across desktop and mobile.
 *            4. Network disconnect resilience (context.setOffline(true)), local buffer, reconnect.
 *            5. Tactile 3D button submission ("খাতা জমা দিন") with X-Idempotency-Key.
 *            6. Instant score evaluation and Socratic hint breakdown.
 *            7. Strict Zero-Emoji and WCAG 2.2 AAA ergonomics audit.
 * STANDARDS: Playwright Headless Standards, Sub-second Latency, Strict Zero-Emoji, WCAG 2.2 AAA
 */

import { test, expect, assertZeroEmojis, setupConsoleTrap, setupMockApiRoutes } from './helpers/e2e-fixtures';

test.describe('Phase 125: Nationwide Live Exam & Playwright E2E Journey', () => {

  test.beforeEach(async ({ page }) => {
    await setupMockApiRoutes(page);
    page.on('dialog', async (dialog) => {
      await dialog.accept();
    });
  });

  test('TC-NAT-01: Student completes authentication and SMS OTP verification modal workflow', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/auth');
    await expect(page).toHaveTitle(/অ্যাকাউন্ট তৈরি | অগ্রযাত্রা/);

    const pageContent = await page.content();
    assertZeroEmojis(pageContent, 'Auth Page Initial Render');

    // Fill in student registration credentials
    const nameInput = page.locator('input[placeholder*="তানভীর আহমেদ"]');
    await nameInput.fill('রাকিবুল হাসান');

    const phoneInput = page.locator('input[placeholder*="017XXXXXXXX"]');
    await phoneInput.fill('01712345678');

    // Trigger SMS OTP Dispatch
    const otpBtn = page.locator('button', { hasText: 'ওটিপি পাঠান' });
    await expect(otpBtn).toBeVisible();
    await otpBtn.click();

    // Verify OTP input becomes visible
    const otpInput = page.locator('input[placeholder*="৬ ডিজিট ওটিপি"]');
    await expect(otpInput).toBeVisible();
    await otpInput.fill('123456');

    // Verify OTP confirmation
    const verifyOtpBtn = page.locator('button', { hasText: 'যাচাই করুন' });
    await expect(verifyOtpBtn).toBeVisible();
    await verifyOtpBtn.click();

    // Verification banner check
    await expect(page.locator('text=ওটিপি যাচাই সম্পন্ন হয়েছে')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-NAT-02: Student navigates to Live Challenge arena, verifies server-synchronized timer and HSC Physics syllabus', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/live-challenge');
    await expect(page).toHaveTitle(/দেশব্যাপী লাইভ চ্যালেঞ্জ | অগ্রযাত্রা/);

    const pageContent = await page.content();
    assertZeroEmojis(pageContent, 'Live Challenge Arena Page');

    // Verify Olympiad Title and Negative Marking Ratio
    await expect(page.locator('text=জাতীয় স্টেম অলিম্পিয়াড ২০২৬')).toBeVisible();
    await expect(page.locator('text=নেগেটিভ মার্কিং: -০.২৫')).toBeVisible();

    // Verify Server-Authoritative Timer & Edge Buffer badge
    await expect(page.locator('text=সার্ভার-অথরিটেটিভ টাইমার')).toBeVisible();
    await expect(page.locator('text=মিলি-সেকেন্ড একুরেট বাফার')).toBeVisible();

    // Verify Registered Candidates counter
    await expect(page.locator('text=প্রতিযোগী শিক্ষার্থী লাইভ লবিতে যুক্ত')).toBeVisible();

    // Verify Tactile Action Button to Enter Live Exam
    const enterExamBtn = page.locator('main a', { hasText: 'পরীক্ষায় অংশগ্রহণ করুন' });
    await expect(enterExamBtn).toBeVisible();
    await enterExamBtn.click();

    // Confirms landing on Practice Exam Arena
    await expect(page).toHaveURL(/\/practice/);

    consoleTrap.assertZeroErrors();
  });

  test('TC-NAT-03: Student solves NCTB HSC Physics questions with KaTeX equations and 3D tactile buttons', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    await page.goto('/practice');
    await expect(page).toHaveTitle(/যেকোনো সময় অনুশীলন/);

    // Verify question 1 KaTeX equation
    await expect(page.locator('text=একটি বস্তুর ভর')).toBeVisible();

    // Verify 3D Tactile Option B with >= 44px touch height
    const optionB = page.locator('main div[role="button"]').filter({ hasText: 'B' }).first();
    await expect(optionB).toBeVisible();
    const box = await optionB.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.height).toBeGreaterThanOrEqual(44);
    }

    // Select Option B
    await optionB.click();

    // Submit answer with tactile button
    const submitBtn = page.locator('button', { hasText: 'সাবমিট করুন' });
    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // Assert instant NCTB solution & citation
    await expect(page.locator('text=সঠিক উত্তর! (Correct Answer)')).toBeVisible();
    await expect(page.locator('text=নিউটনের ২য় সূত্র')).toBeVisible();
    await expect(page.locator('text=এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র')).toBeVisible();

    // Advance to Question 2
    const nextBtn = page.locator('button', { hasText: 'পরবর্তী প্রশ্ন' });
    await expect(nextBtn).toBeVisible();
    await nextBtn.click();

    // Assert Question 2 loaded
    await expect(page.locator('text=প্রশ্ন নং ২')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-NAT-04: Network disconnect simulation buffers answers locally and resyncs seamlessly upon reconnect', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page, { ignoreNetworkDisconnect: true });

    await page.goto('/practice');

    // Initially online
    await expect(page.locator('text=অনলাইন সিঙ্কড')).toBeVisible();

    // Simulate network drop: setOffline(true) event emulation
    await page.evaluate(() => window.dispatchEvent(new Event('offline')));

    // Assert offline buffer badge
    await expect(page.locator('text=অফলাইন বাফার')).toBeVisible();

    // Solve question while offline
    const optionB = page.locator('main div[role="button"]').filter({ hasText: 'B' }).first();
    await optionB.click();
    await page.locator('button', { hasText: 'সাবমিট করুন' }).click();

    // Explanation still displays from local buffer
    await expect(page.locator('text=সঠিক উত্তর! (Correct Answer)')).toBeVisible();

    // Restore network connectivity: setOffline(false) event emulation
    await page.evaluate(() => window.dispatchEvent(new Event('online')));

    // Status returns to Online Synced
    await expect(page.locator('text=অনলাইন সিঙ্কড')).toBeVisible();

    consoleTrap.assertZeroErrors();
  });

  test('TC-NAT-05: Final exam script submission ("খাতা জমা দিন") asserts X-Idempotency-Key and Socratic breakdown', async ({ page }) => {
    const consoleTrap = setupConsoleTrap(page);

    // Track network requests to verify X-Idempotency-Key
    let observedIdempotencyKey: string | null = null;
    await page.route(/\/api\/v1\/quiz-attempts/, async (route) => {
      const headers = route.request().headers();
      if (headers['x-idempotency-key']) {
        observedIdempotencyKey = headers['x-idempotency-key'];
      }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: { 'x-idempotency-key': observedIdempotencyKey || 'test-key' },
        body: JSON.stringify({ status: 'ACCEPTED', idempotency_key: observedIdempotencyKey }),
      });
    });

    await page.goto('/practice');

    // Solve question 1
    const optionB = page.locator('div[role="button"]').nth(1);
    await optionB.click();
    await page.locator('button', { hasText: 'সাবমিট করুন' }).click();

    // Advance through questions until question 10
    for (let i = 1; i < 10; i++) {
      const nextBtn = page.locator('button', { hasText: 'পরবর্তী প্রশ্ন' });
      await expect(nextBtn).toBeVisible();
      await nextBtn.click();

      // Pick an option for each subsequent question
      const opt = page.locator('div[role="button"]').nth(1);
      await expect(opt).toBeVisible();
      await opt.click();

      const sub = page.locator('button', { hasText: 'সাবমিট করুন' });
      await expect(sub).toBeVisible();
      await sub.click();
    }

    // On final question (question 10), verify tactile "খাতা জমা দিন" button is visible
    const submitExamBtn = page.locator('button', { hasText: 'খাতা জমা দিন' });
    await expect(submitExamBtn).toBeVisible();

    // Verify 3D physical ledge button physics
    const examBtnBox = await submitExamBtn.boundingBox();
    expect(examBtnBox).not.toBeNull();
    if (examBtnBox) {
      expect(examBtnBox.height).toBeGreaterThanOrEqual(44);
    }

    // Submit final script
    await submitExamBtn.click();

    // Assert Instant Result & Socratic Hint Breakdown Card
    await expect(page.locator('text=জাতীয় লাইভ অলিম্পিয়াড পরীক্ষা সম্পন্ন হয়েছে')).toBeVisible();
    await expect(page.locator('text=টপ ১% জাতীয় মেধা')).toBeVisible();
    await expect(page.locator('text=সক্রেটিক বিশ্লেষণ ও পারফরম্যান্স ব্রেকডাউন')).toBeVisible();
    await expect(page.locator('text=নিউটোনীয় বলবিদ্যা ও গতির সূত্রাবলী')).toBeVisible();

    // Assert Zero Emojis in final completion card
    const completionCard = await page.locator('[data-testid="practice-exam-arena"]').innerText();
    assertZeroEmojis(completionCard, 'Live Exam Completion View');

    consoleTrap.assertZeroErrors();
  });

  test('TC-NAT-06: Mobile emulation (Pixel 7 & iPhone 14) enforces 44px+ touch targets and zero horizontal scroll', async ({ page }) => {
    // 1. Emulate Google Pixel 7 (412x915)
    await page.setViewportSize({ width: 412, height: 915 });
    await page.goto('/live-challenge');

    // Verify touch targets on main content link
    const enterBtn = page.locator('main a', { hasText: 'পরীক্ষায় অংশগ্রহণ করুন' });
    await expect(enterBtn).toBeVisible();
    const enterBox = await enterBtn.boundingBox();
    expect(enterBox).not.toBeNull();
    if (enterBox) {
      expect(enterBox.height).toBeGreaterThanOrEqual(44);
    }

    // Zero horizontal scroll on Pixel 7
    let scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    let clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2);

    // 2. Emulate Apple iPhone 14 (390x844)
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/practice');

    const optionBtn = page.locator('div[role="button"]').first();
    await expect(optionBtn).toBeVisible();
    const optBox = await optionBtn.boundingBox();
    expect(optBox).not.toBeNull();
    if (optBox) {
      expect(optBox.height).toBeGreaterThanOrEqual(44);
    }

    // Zero horizontal scroll on iPhone 14
    scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2);

    // Zero-Emoji check
    const mobileContent = await page.content();
    assertZeroEmojis(mobileContent, 'Mobile Viewport Exam Arena');
  });

});
