import { test, expect } from '@playwright/test';

test.describe('Bdjobs Elevation: Career & Employment Portal End-to-End Suite', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate to Career page
    await page.goto('/career');
    await page.waitForLoadState('domcontentloaded');
  });

  test('01. Should render the platform statistics header and core counters', async ({ page }) => {
    await expect(page.locator('text=অন্বেষণ ও কর্মসংস্থান পোর্টাল')).toBeVisible();
    await expect(page.locator('text=৮,৪৫০+')).toBeVisible();
    await expect(page.locator('text=সক্রিয় চাকরির সুযোগ')).toBeVisible();
    await expect(page.locator('text=১,২০০+')).toBeVisible();
    await expect(page.locator('text=নিবন্ধিত কোম্পানি')).toBeVisible();
    await expect(page.locator('text=৫২০+')).toBeVisible();
    await expect(page.locator('text=সরকারি সার্কুলার পদ')).toBeVisible();
  });

  test('02. Should switch between Functional and Special Skill categories', async ({ page }) => {
    await expect(page.locator('h3:has-text("আইটি ও সফটওয়্যার")')).toBeVisible();
    await expect(page.locator('h3:has-text("ব্যাংক ও নন-ব্যাংক ফিন্যান্স")')).toBeVisible();

    // Switch to Special Skills
    await page.click('button:has-text("স্পেশাল স্কিল্ড ও টেকনিক্যাল")');
    await expect(page.locator('h3:has-text("ইলেকট্রিশিয়ান ও টেকনিশিয়ান")')).toBeVisible();
    await expect(page.locator('h3:has-text("গার্মেন্টস ও টেক্সটাইল টেকনিশিয়ান")')).toBeVisible();
  });

  test('03. Should filter jobs by keyword and division', async ({ page }) => {
    // Type in search box
    const searchInput = page.locator('input[placeholder*="পদবি, কোম্পানি বা দক্ষতার নাম"]');
    await searchInput.fill('BrainStation');

    await expect(page.locator('text=জুনিয়র সফটওয়্যার ইঞ্জিনিয়ার (Python / FastAPI)')).toBeVisible();

    // Clear search
    await searchInput.fill('');
    await expect(page.locator('text=ম্যানেজমেন্ট ট্রেইনি অফিসার (MTO - 2026)')).toBeVisible();
  });

  test('04. Should open Job Detail modal and inspect job specification', async ({ page }) => {
    // Click on 'বিস্তারিত' button on the first job
    const detailBtn = page.locator('[data-testid="detail-job-btn"]').first();
    await detailBtn.click();

    // Verify modal content
    await expect(page.locator('text=শিক্ষাগত যোগ্যতা ও প্রয়োজনীয় ডিগ্রি')).toBeVisible();
    await expect(page.locator('text=দায়িত্ব ও কাজের পরিধি (Responsibilities)')).toBeVisible();
    await expect(page.locator('text=মাসিক বেতন কাঠামো:')).toBeVisible();

    // Close modal
    await page.click('button:has-text("বন্ধ করুন")');
    await expect(page.locator('text=শিক্ষাগত যোগ্যতা ও প্রয়োজনীয় ডিগ্রি')).not.toBeVisible();
  });

  test('05. Should complete online application flow and generate tracking ID', async ({ page }) => {
    // Click on 'আবেদন' on the first job
    const applyBtn = page.locator('[data-testid="apply-job-btn"]').first();
    await applyBtn.click();

    await expect(page.locator('text=অনলাইন আবেদন ফর্ম')).toBeVisible();
    await expect(page.locator('text=সিলগালা ক্রিপ্টোগ্রাফিক সিভি স্ন্যাপশট সংযুক্ত')).toBeVisible();

    // Submit application
    await page.click('button:has-text("আবেদন নিশ্চিত করুন")');

    // Verify success confirmation
    await expect(page.locator('text=আবেদন সফলভাবে গৃহীত হয়েছে!')).toBeVisible();
    await expect(page.locator('text=OGRO-APP-')).toBeVisible();

    // Click finish
    await page.click('button:has-text("সম্পন্ন করুন")');
  });

  test('06. Should open Bdjobs Pro CV Builder modal and inspect 85% completeness meter', async ({ page }) => {
    // Click 'প্রফেশনাল সিভি তৈরি করুন'
    await page.click('button:has-text("প্রফেশনাল সিভি তৈরি করুন")');

    await expect(page.locator('text=অগ্রযাত্রা প্রফেশনাল সিভি বিল্ডার')).toBeVisible();
    await expect(page.locator('text=৮৫% সম্পন্ন')).toBeVisible();
    await expect(page.locator('text=বিডিজবস ফরম্যাট স্ট্যান্ডার্ড')).toBeVisible();

    // Close modal
    await page.click('button:has-text("সম্পন্ন")');
    await expect(page.locator('text=অগ্রযাত্রা প্রফেশনাল সিভি বিল্ডার')).not.toBeVisible();
  });

  test('07. Should switch to Government Circulars & Salary Insights tab', async ({ page }) => {
    await page.click('button:has-text("সরকারি সার্কুলার ও ক্যারিয়ার গাইড")');

    await expect(page.locator('text=সরকারি ও ক্যাডার সার্ভিস নিয়োগ বিজ্ঞপ্তি (Official Circulars)')).toBeVisible();
    await expect(page.locator('text=৪৮তম বিসিএস (বিশেষ) পরীক্ষা সার্কুলার ২০২৬')).toBeVisible();
    await expect(page.locator('text=শিল্প ও পদবি ভেদে গড় বেতন নির্দেশিকা (Salary Insights)')).toBeVisible();
    await expect(page.locator('text=সফটওয়্যার ও আইটি (Tech)')).toBeVisible();
  });

  test('08. Should switch to Verifiable Skills & Sealed Snapshot tab', async ({ page }) => {
    await page.click('button:has-text("প্রমাণযুক্ত স্কিল ও সিলগালা স্ন্যাপশট")');

    await expect(page.locator('text=সিলগালা ক্রিপ্টোগ্রাফিক সিভি স্ন্যাপশট বিল্ডার (SHA-256 Ledger)')).toBeVisible();
    await expect(page.locator('text=প্রমাণযুক্ত দক্ষতাসমূহ (Evidence-Backed Skills)')).toBeVisible();
    await expect(page.locator('text=Python & FastAPI Backend')).toBeVisible();

    // Mint new snapshot
    await page.click('button:has-text("নতুন সিলগালা স্ন্যাপশট তৈরি করুন")');
    await expect(page.locator('text=SNAP-2026-SHA256-')).toBeVisible();
  });

});
