/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Elevation Data Integrity & Safety Test Suite
 * TOPIC:     10MS Competitive Elevation Testing
 * FILE:      frontend/src/components/competitive-elevation/__tests__/academicElevation.test.mjs
 * STANDARDS: Zero-Emoji, Production Grade, Strict Image Isolation, Data Contract Rigor
 */

import test from 'node:test';
import assert from 'node:assert/strict';

import {
  ACADEMIC_CATEGORIES,
  ACADEMIC_BUNDLES,
  ACADEMIC_PILLAR_FEATURES,
  VERIFIED_ACHIEVERS,
} from '../data/academicElevationData.ts';

test('TC-AE-01: Academic categories coverage and Bengali labels', () => {
  assert.ok(ACADEMIC_CATEGORIES.length >= 6, 'Should have at least 6 core categories');
  const ids = ACADEMIC_CATEGORIES.map((c) => c.id);
  assert.ok(ids.includes('hsc_27'), 'Should include HSC 27');
  assert.ok(ids.includes('hsc_28'), 'Should include HSC 28');
  assert.ok(ids.includes('ssc_27'), 'Should include SSC 27');
  assert.ok(ids.includes('admission_varsity'), 'Should include Varsity Admission');
  assert.ok(ids.includes('admission_med_eng'), 'Should include Medical & BUET Engineering');
  assert.ok(ids.includes('bcs_preli'), 'Should include BCS Preliminary');

  ACADEMIC_CATEGORIES.forEach((c) => {
    assert.ok(c.labelBn.length > 3, `Category ${c.id} must have non-empty Bengali label`);
    assert.ok(c.subLabelBn.length > 3, `Category ${c.id} must have informative sub-label`);
  });
});

test('TC-AE-02: Course bundle data contract and deliverables completeness', () => {
  assert.ok(ACADEMIC_BUNDLES.length >= 6, 'Should have at least 6 academic bundles');

  ACADEMIC_BUNDLES.forEach((bundle) => {
    assert.ok(bundle.id.length > 0, 'Bundle must have an ID');
    assert.ok(bundle.titleBn.length > 5, `Bundle ${bundle.id} must have descriptive Bengali title`);
    assert.ok(bundle.subtitleBn.length > 10, `Bundle ${bundle.id} must have clear subtitle`);
    assert.ok(bundle.subjects.length > 0, `Bundle ${bundle.id} must have at least one subject`);
    assert.ok(bundle.deliverablesBn.length >= 3, `Bundle ${bundle.id} must list at least 3 deliverables`);
    assert.ok(bundle.mockTestsCount > 0, `Bundle ${bundle.id} must provide mock tests`);
    assert.ok(bundle.enrolledStudentsCount > 0, `Bundle ${bundle.id} must have student metrics`);
    assert.ok(bundle.targetUrl.startsWith('/'), `Bundle ${bundle.id} target URL must be an internal route`);
  });
});

test('TC-AE-03: Strict Zero 10MS Photo Asset Isolation on Achievers', () => {
  assert.ok(VERIFIED_ACHIEVERS.length >= 4, 'Should have at least 4 verified achievers');

  VERIFIED_ACHIEVERS.forEach((achiever) => {
    // Assert no external image URLs or 10MS scraped media
    assert.ok(!('photoUrl' in achiever), 'Achiever must NOT contain external photo URL');
    assert.ok(!('avatarUrl' in achiever), 'Achiever must NOT contain external avatar URL');
    assert.ok(achiever.initials.length > 0 && achiever.initials.length <= 3, 'Must have Bengali monogram initials');
    assert.ok(achiever.accentBg.includes('bg-'), 'Must have CSS monogram background class');
    assert.ok(achiever.institutionBn.length > 5, 'Must have authentic educational institution name');
    assert.ok(achiever.milestoneBn.length > 5, 'Must have academic milestone');
  });
});

test('TC-AE-04: Pillar features include 24/7 Socratic AI and Offline PWA reassurance', () => {
  const pillarIds = ACADEMIC_PILLAR_FEATURES.map((p) => p.id);
  assert.ok(pillarIds.includes('socratic-doubt-solve'), 'Must include 24/7 Socratic doubt solve');
  assert.ok(pillarIds.includes('offline-pwa-vault'), 'Must include offline PWA vault');
  assert.ok(pillarIds.includes('national-live-challenge'), 'Must include national live challenge');

  ACADEMIC_PILLAR_FEATURES.forEach((p) => {
    assert.ok(p.reassuranceBn.length > 5, `Pillar ${p.id} must have reassuring Bengali microcopy`);
    assert.ok(p.actionUrl.startsWith('/'), `Pillar ${p.id} must have valid internal action URL`);
  });
});
