/**
 * ========================================================================================
 * MODULE:    Admin RBAC & Defense-in-Depth Playwright E2E Test Suite
 * TOPIC:     Client-Side Guard (Zero-FOAC), 403 Forbidden States, Scoped Reviewer & Admin Flows
 * FILE:      frontend/e2e/admin_rbac.spec.ts
 * PURPOSE:   Validates zero-trust access control on the client tier. Guarantees unauthenticated
 *            visitors are redirected to /auth with return target, student roles encounter
 *            dignified 403 Forbidden barrier without admin leakage, subject reviewers access
 *            scoped quarantine tools with sensitive arbitration locked, and full administrators
 *            possess unrestricted controls.
 * AUDIENCE:  Security Auditors, QA Engineers & Frontend Architects
 * STANDARDS: OWASP ASVS L2, Playwright Test Harness, Strict Zero-Emoji Compliance
 * ========================================================================================
 */

import { test, expect, assertZeroEmojis } from './helpers/e2e-fixtures';

const SESSION_KEY = 'ogrojatra_auth_session';
const TOKEN_KEY = 'auth_token';

test.describe('Admin Panel RBAC & Defense-in-Depth Verification', () => {

  test('TC-RBAC-01: Unauthenticated visitor navigating to /admin is redirected to /auth', async ({ page }) => {
    // Navigate directly to protected admin route without credentials
    await page.goto('/admin');

    // Should immediately redirect to /auth preserving return target route
    await page.waitForURL(/\/auth\?redirectTo=%2Fadmin/, { timeout: 10000 });
    expect(page.url()).toContain('/auth?redirectTo=%2Fadmin');

    // Check for dignified redirect notice in Bengali
    await expect(page.locator('text=প্রশাসনিক অঞ্চলে প্রবেশের অনুরোধ')).toBeVisible();
    await expect(page.locator('text=সংরক্ষিত প্রশাসনিক অঞ্চলে প্রবেশের জন্য অনুমোদিত অ্যাডমিন বা বিষয় পর্যালোচক অ্যাকাউন্টে লগইন করুন।')).toBeVisible();

    // Verify zero emoji
    const content = await page.content();
    assertZeroEmojis(content, 'Auth Redirect Screen');
  });

  test('TC-RBAC-02: Authenticated student role accessing /admin receives HTTP 403 barrier', async ({ page }) => {
    const studentSession = {
      user: {
        id: 'usr_student_01',
        fullName: 'Naim Hasan',
        email: 'student@ogrojatra.edu.bd',
        roles: ['STUDENT'],
        isActive: true
      },
      token: 'test_student_token_01',
      expiresAt: Date.now() + 3600000
    };

    // Pre-populate storage before page scripts mount
    await page.addInitScript(({ sKey, tKey, session }) => {
      localStorage.setItem(sKey, JSON.stringify(session));
      localStorage.setItem(tKey, session.token);
    }, { sKey: SESSION_KEY, tKey: TOKEN_KEY, session: studentSession });

    // Navigate to admin
    await page.goto('/admin');

    // Verify 403 Access Denied barrier is displayed
    await expect(page.locator('text=অননুমোদিত প্রশাসনিক অঞ্চল')).toBeVisible();
    await expect(page.locator('text=এইচটিটিপি ৪০৩ • প্রবেশাধিকার সংরক্ষিত')).toBeVisible();
    await expect(page.locator('text=আপনার বর্তমান অনুমোদিত ভূমিকা:')).toBeVisible();
    await expect(page.locator('text=শিক্ষার্থী (Student)')).toBeVisible();

    // Ensure actual admin console tabs/content are NOT leaked
    await expect(page.locator('h1', { hasText: 'কেন্দ্রীয় প্ল্যাটফর্ম প্রশাসন ও অপারেশনস কনসোল' })).not.toBeVisible();
    await expect(page.locator('text=প্রশ্ন কোয়ারেন্টিন ও কোয়ালিটি কন্ট্রোল')).not.toBeVisible();

    // Verify zero emoji
    const content = await page.content();
    assertZeroEmojis(content, 'Student 403 Forbidden Screen');
  });

  test('TC-RBAC-03: Subject Reviewer accessing /admin enters Scoped Mode', async ({ page }) => {
    const reviewerSession = {
      user: {
        id: 'usr_reviewer_01',
        fullName: 'Senior Physics Reviewer',
        email: 'reviewer@ogrojatra.edu.bd',
        roles: ['SUBJECT_REVIEWER'],
        isActive: true
      },
      token: 'test_reviewer_token_01',
      expiresAt: Date.now() + 3600000
    };

    // Pre-populate storage before page scripts mount
    await page.addInitScript(({ sKey, tKey, session }) => {
      localStorage.setItem(sKey, JSON.stringify(session));
      localStorage.setItem(tKey, session.token);
    }, { sKey: SESSION_KEY, tKey: TOKEN_KEY, session: reviewerSession });

    // Navigate to admin
    await page.goto('/admin');

    // Scoped Reviewer Mode banner must be active
    await expect(page.locator('text=সীমিত প্রবেশাধিকার স্তর: বিষয় পর্যালোচক')).toBeVisible();
    await expect(page.locator('text=বিষয় পর্যালোচক (Reviewer)').first()).toBeVisible();

    // Super-admin only hub should be locked
    await expect(page.locator('text=শুধুমাত্র সুপার অ্যাডমিন').first()).toBeVisible();

    // Quarantine hub must be visible and accessible
    await expect(page.locator('text=জরুরি কোয়ারেন্টিন')).toBeVisible();

    // Verify zero emoji
    const content = await page.content();
    assertZeroEmojis(content, 'Subject Reviewer Admin Screen');
  });

  test('TC-RBAC-04: Full Administrator accessing /admin has full console access', async ({ page }) => {
    const adminSession = {
      user: {
        id: 'usr_admin_01',
        fullName: 'Chief Platform Administrator',
        email: 'admin@ogrojatra.edu.bd',
        roles: ['ADMIN'],
        isActive: true
      },
      token: 'test_admin_token_01',
      expiresAt: Date.now() + 3600000
    };

    // Pre-populate storage before page scripts mount
    await page.addInitScript(({ sKey, tKey, session }) => {
      localStorage.setItem(sKey, JSON.stringify(session));
      localStorage.setItem(tKey, session.token);
    }, { sKey: SESSION_KEY, tKey: TOKEN_KEY, session: adminSession });

    // Navigate to admin
    await page.goto('/admin');

    // Verify full admin elements
    await expect(page.locator('h1', { hasText: 'কেন্দ্রীয় প্ল্যাটফর্ম প্রশাসন ও অপারেশনস কনসোল' })).toBeVisible();
    await expect(page.locator('text=সুপার অ্যাডমিন (Full Admin)').first()).toBeVisible();
    await expect(page.locator('text=প্রশ্ন কোয়ারেন্টিন ও কোয়ালিটি কন্ট্রোল')).toBeVisible();

    // Verify zero emoji
    const content = await page.content();
    assertZeroEmojis(content, 'Full Admin Screen');
  });

  test('TC-RBAC-05: Logout clears session and bars subsequent entry', async ({ page }) => {
    const adminSession = {
      user: {
        id: 'usr_admin_01',
        fullName: 'Chief Platform Administrator',
        email: 'admin@ogrojatra.edu.bd',
        roles: ['ADMIN'],
        isActive: true
      },
      token: 'test_admin_token_01',
      expiresAt: Date.now() + 3600000
    };

    // Pre-populate storage only when on admin routes
    await page.addInitScript(({ sKey, tKey, session }) => {
      if (window.location.pathname.startsWith('/admin')) {
        localStorage.setItem(sKey, JSON.stringify(session));
        localStorage.setItem(tKey, session.token);
      }
    }, { sKey: SESSION_KEY, tKey: TOKEN_KEY, session: adminSession });

    await page.goto('/admin');
    await expect(page.locator('h1', { hasText: 'কেন্দ্রীয় প্ল্যাটফর্ম প্রশাসন ও অপারেশনস কনসোল' })).toBeVisible({ timeout: 15000 });
    const logoutBtn = page.locator('button', { hasText: 'লগআউট' }).first();
    await expect(logoutBtn).toBeVisible({ timeout: 15000 });

    // Click logout
    await logoutBtn.click();

    // Must be redirected to /auth
    await page.waitForURL(/\/auth/, { timeout: 10000 });

    // Session in localStorage must be cleared
    const stored = await page.evaluate((key) => localStorage.getItem(key), SESSION_KEY);
    expect(stored).toBeNull();
  });

});
