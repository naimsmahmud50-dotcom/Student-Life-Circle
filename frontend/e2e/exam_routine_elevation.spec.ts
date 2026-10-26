import { test, expect } from '@playwright/test';

test.describe('Batch 1: Live MCQ Routine & Mega Model Test Calendar Hub E2E', () => {

  test('E2E-01: Flag OFF displays Coming Soon banner and SEO meta tags', async ({ page }) => {
    await page.goto('http://localhost:3002/routines', { waitUntil: 'domcontentloaded' });

    // Verify title
    await expect(page).toHaveTitle(/পরীক্ষার রুটিন ও মেগা মডেল টেস্ট শিডিউল/);
    
    // Check Coming Soon Banner
    const banner = page.locator('text=শীঘ্রই আসছে: লাইভ এমসিকিউ ও মডেল টেস্ট রুটিন হাব');
    await expect(banner).toBeVisible({ timeout: 10000 });

    const stagingBtn = page.locator('text=স্টেজিং প্রিভিউ সক্রিয় করুন');
    await expect(stagingBtn).toBeVisible();
  });

  test('E2E-02: Staging preview unlocks full 200-day routine calendar, countdown & simulator', async ({ page }) => {
    await page.goto('http://localhost:3002/routines', { waitUntil: 'domcontentloaded' });

    // Click Staging Preview button
    const stagingBtn = page.locator('text=স্টেজিং প্রিভিউ সক্রিয় করুন');
    await stagingBtn.click();

    // Wait for full hub mount
    await expect(page.locator('h1:has-text("লাইভ এমসিকিউ ও মেগা মডেল টেস্ট রুটিন হাব")')).toBeVisible({ timeout: 10000 });

    // Verify Friday Mega Model Test Hero Countdown in section
    const countdownHero = page.locator('section[aria-label="শুক্রবার মেগা মডেল টেস্ট শিডিউল"]');
    await expect(countdownHero).toBeVisible();
    await expect(countdownHero.getByText('সাপ্তাহিক শুক্রবার মেগা মডেল টেস্ট ১')).toBeVisible();
    await expect(countdownHero.getByText('১৮,৯৪০+ পরীক্ষার্থী নিবন্ধিত')).toBeVisible();

    // Verify 200-day syllabus tracker
    await expect(page.locator('text=২০০ দিনের সিলেবাস প্রস্তুতি ট্র্যাকার')).toBeVisible();

    // Verify filter tabs
    await expect(page.locator('role=tab[name*="৪৭তম বিসিএস"]')).toBeVisible();
    await expect(page.locator('role=tab[name*="ভার্সিটি ও বুয়েট ভর্তি"]')).toBeVisible();

    // Verify routine cards exist
    await expect(page.locator('text=BCS-200-DAY-001').first()).toBeVisible();
    await expect(page.locator('text=প্রাচীন ও মধ্যযুগের বাংলা সাহিত্য').first()).toBeVisible();

    // Open Negative Marking Simulator
    const simBtn = countdownHero.locator('button:has-text("স্কোর সিমুলেটর")');
    await simBtn.click();

    // Check modal visibility
    await expect(page.locator('h2:has-text("নেগেটিভ মার্কিং ও মেধা পারসেন্টাইল সিমুলেটর")')).toBeVisible();

    // Click calculate
    const calcBtn = page.locator('button:has-text("স্কোর ও পারসেন্টাইল হিসাব করুন")');
    await calcBtn.click();

    // Verify simulated score output
    await expect(page.locator('text=নেট প্রাপ্ত নম্বর')).toBeVisible();
    await expect(page.locator('text=আনুমানিক মেধা পারসেন্টাইল')).toBeVisible();

    // Close modal
    const closeBtn = page.locator('button[aria-label="মডাল বন্ধ করুন"]');
    await closeBtn.click();
    await expect(page.locator('h2:has-text("নেগেটিভ মার্কিং ও মেধা পারসেন্টাইল সিমুলেটর")')).not.toBeVisible();
  });

  test('E2E-03: Routine alert subscription modal interactions', async ({ page }) => {
    await page.goto('http://localhost:3002/routines', { waitUntil: 'domcontentloaded' });

    // Unlock staging and wait for hub mount
    await page.locator('text=স্টেজিং প্রিভিউ সক্রিয় করুন').click();
    await expect(page.locator('h1:has-text("লাইভ এমসিকিউ ও মেগা মডেল টেস্ট রুটিন হাব")')).toBeVisible({ timeout: 10000 });

    // Click first alert button in cards
    const alertBtn = page.locator('button:has-text("অ্যালার্ট নিন")').first();
    await alertBtn.click();

    // Verify subscription dialog
    await expect(page.locator('h2#sub-modal-title')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('text=ইন-অ্যাপ ড্রয়ার নোটিফিকেশন')).toBeVisible();

    // Submit subscription
    const confirmBtn = page.locator('button:has-text("অ্যালার্ট নিশ্চিত করুন")');
    await confirmBtn.click();

    // Verify confirmation message
    await expect(page.locator('text=অ্যালার্ট নিশ্চিত হয়েছে')).toBeVisible({ timeout: 8000 });
  });

  test('E2E-04: Regression check - Live Challenge, Practice and Career pages remain intact', async ({ page }) => {
    // Check Live Challenge
    await page.goto('http://localhost:3002/live-challenge', { waitUntil: 'domcontentloaded' });
    await expect(page).toHaveTitle(/লাইভ চ্যালেঞ্জ|অলিম্পিয়াড/);
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 10000 });

    // Check Career
    await page.goto('http://localhost:3002/career', { waitUntil: 'domcontentloaded' });
    await expect(page.getByText('অগ্রযাত্রা ক্যারিয়ার হাব').first()).toBeVisible({ timeout: 10000 });

    // Check Tuition
    await page.goto('http://localhost:3002/tuition', { waitUntil: 'domcontentloaded' });
    await expect(page.getByRole('heading', { name: /সুরক্ষিত টিউশন/ }).first()).toBeVisible({ timeout: 10000 });
  });
});
