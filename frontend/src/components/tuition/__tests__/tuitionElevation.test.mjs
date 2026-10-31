/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Elevation Unit & Safety Test Suite
 * TOPIC:     CareTutors Reverse Engineering Integration Verification
 * FILE:      frontend/src/components/tuition/__tests__/tuitionElevation.test.mjs
 * STANDARDS: Zero-Emoji, Production Grade, Strict Image Isolation, Data Contract Rigor
 */

import test from 'node:test';
import assert from 'node:assert/strict';

import {
  TUITION_CATEGORIES,
  TUITION_JOBS,
  VERIFIED_TUTORS,
  SALARY_BENCHMARKS,
  TUITION_FAQS,
} from '../data/tuitionElevationData.ts';

test('TC-TE-01: Tuition categories coverage and metadata completeness', () => {
  assert.ok(TUITION_CATEGORIES.length >= 8, 'Should have at least 8 tuition categories');
  const ids = TUITION_CATEGORIES.map((c) => c.id);
  assert.ok(ids.includes('bangla_medium'), 'Must include Bangla Medium');
  assert.ok(ids.includes('english_version'), 'Must include English Version');
  assert.ok(ids.includes('english_medium'), 'Must include English Medium');
  assert.ok(ids.includes('religious'), 'Must include Religious Studies');
  assert.ok(ids.includes('admission'), 'Must include Admission');
  assert.ok(ids.includes('special_child'), 'Must include Special Child Education');

  TUITION_CATEGORIES.forEach((c) => {
    assert.ok(c.nameBn.length > 3, `Category ${c.id} must have non-empty Bengali name`);
    assert.ok(c.jobsCount >= 0, `Category ${c.id} must have valid jobs count`);
  });
});

test('TC-TE-02: Tuition jobs data contract and integrity', () => {
  assert.ok(TUITION_JOBS.length >= 6, 'Should have at least 6 initial tuition jobs');

  TUITION_JOBS.forEach((job) => {
    assert.ok(job.id.startsWith('TUI-'), `Job ID ${job.id} must follow TUI-xxxx standard`);
    assert.ok(job.titleBn.length > 5, `Job ${job.id} must have title`);
    assert.ok(job.subjectsBn.length > 0, `Job ${job.id} must have at least one subject`);
    assert.ok(job.salaryAmount > 0, `Job ${job.id} must have salary amount`);
    assert.ok(['open', 'shortlisting', 'confirmed'].includes(job.status), `Job ${job.id} has invalid status`);
    assert.ok(job.daysPerWeek >= 2 && job.daysPerWeek <= 6, `Job ${job.id} must have 2-6 days/week`);
    assert.ok(job.escrowProtected === true, `Job ${job.id} must be escrow protected`);
  });
});

test('TC-TE-03: Strict Zero CareTutors Photo Asset Isolation on Tutors', () => {
  assert.ok(VERIFIED_TUTORS.length >= 4, 'Should have at least 4 verified tutors');

  VERIFIED_TUTORS.forEach((tutor) => {
    // Assert strictly NO external image URLs or scraped photos
    assert.ok(!('photoUrl' in tutor), 'Tutor must NOT contain external photo URL');
    assert.ok(!('avatarUrl' in tutor), 'Tutor must NOT contain external avatar URL');
    assert.ok(tutor.initialsBn.length > 0 && tutor.initialsBn.length <= 2, 'Must have Bengali monogram initials');
    assert.ok(tutor.accentBg.includes('bg-'), 'Must have CSS monogram background class');
    assert.ok(tutor.institutionBn.length > 2, 'Must have authentic educational institution name');
    assert.ok(tutor.verificationStatus.nidVerified === true, 'Must have NID verified');
    assert.ok(tutor.verificationStatus.academicIdVerified === true, 'Must have Academic ID verified');
    assert.ok(tutor.rating >= 4.0 && tutor.rating <= 5.0, 'Rating must be between 4.0 and 5.0');
  });
});

test('TC-TE-04: Salary benchmark formulas integrity', () => {
  assert.ok(SALARY_BENCHMARKS.length >= 8, 'Should have salary benchmark rules');

  SALARY_BENCHMARKS.forEach((rule) => {
    assert.ok(rule.minSalary > 0, 'Min salary must be positive');
    assert.ok(rule.maxSalary >= rule.minSalary, 'Max salary must be >= min salary');
    assert.ok(rule.daysPerWeek > 0, 'Days per week must be positive');
  });
});

test('TC-TE-05: Tuition FAQ coverage for both guardians and tutors', () => {
  const guardianFaqs = TUITION_FAQS.filter((f) => f.category === 'guardian');
  const tutorFaqs = TUITION_FAQS.filter((f) => f.category === 'tutor');

  assert.ok(guardianFaqs.length >= 3, 'Must have at least 3 guardian FAQs');
  assert.ok(tutorFaqs.length >= 2, 'Must have at least 2 tutor FAQs');

  TUITION_FAQS.forEach((f) => {
    assert.ok(f.questionBn.length > 10, 'FAQ question must be descriptive');
    assert.ok(f.answerBn.length > 20, 'FAQ answer must be comprehensive');
  });
});

test('TC-TE-06: All defined tuition categories have corresponding job entries', () => {
  const specificCategories = TUITION_CATEGORIES.filter((c) => c.id !== 'all');
  specificCategories.forEach((cat) => {
    const matchingJobs = TUITION_JOBS.filter((j) => j.category === cat.id);
    assert.ok(
      matchingJobs.length > 0,
      `Category ${cat.id} (${cat.nameBn}) must have at least one job in TUITION_JOBS`
    );
  });
});

