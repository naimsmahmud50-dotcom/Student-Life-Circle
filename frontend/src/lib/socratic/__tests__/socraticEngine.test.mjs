/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic AI Engine Comprehensive Unit Test Suite
 * FILE:      frontend/src/lib/socratic/__tests__/socraticEngine.test.mjs
 * STANDARDS: Strict Zero-Emoji, Node 24 Native Test Runner, 100% Coverage
 */

import test from 'node:test';
import assert from 'node:assert/strict';

import {
  isDirectAnswerDemanded,
  scanForMisconception,
  analyzeProblemDomain,
  MISCONCEPTION_TAXONOMY,
  ZERO_ANSWER_LEAKING_REFUSAL_BN
} from '../socraticEngine.ts';

test('Socratic AI Engine - Zero-Answer Leaking Guardrail', async (t) => {
  await t.test('detects direct answer demands in Bengali', () => {
    assert.equal(isDirectAnswerDemanded('আমাকে সরাসরি উত্তর বলে দাও'), true);
    assert.equal(isDirectAnswerDemanded('পুরো অংকটা করে দাও প্লিজ'), true);
    assert.equal(isDirectAnswerDemanded('উত্তর কত হবে সরাসরি দিন'), true);
  });

  await t.test('detects direct answer demands in English', () => {
    assert.equal(isDirectAnswerDemanded('final answer please'), true);
    assert.equal(isDirectAnswerDemanded('just give me the result'), true);
    assert.equal(isDirectAnswerDemanded('solve it fully'), true);
  });

  await t.test('allows genuine inquiries and socratic questions', () => {
    assert.equal(isDirectAnswerDemanded('দ্বিঘাত সমীকরণ সমাধানের নিয়ম কী?'), false);
    assert.equal(isDirectAnswerDemanded('সর্বোচ্চ উচ্চতার চূড়ায় বেগ কত হবে?'), false);
    assert.equal(isDirectAnswerDemanded('এখানে কি মধ্যপদ ২ab যোগ করতে হবে?'), false);
  });
});

test('Socratic AI Engine - Misconception Taxonomy Scanner', async (t) => {
  await t.test('diagnoses missing middle term (a+b)^2 = a^2 + b^2', () => {
    const mis = scanForMisconception('(a+b)^2 = a^2 + b^2');
    assert.ok(mis);
    assert.equal(mis.id, 'ALGEBRA_BINOMIAL_MIDDLE_TERM');
    assert.match(mis.explanationBn, /মধ্যপদ 2ab/);
  });

  await t.test('does NOT trigger on correct algebraic binomial', () => {
    const mis = scanForMisconception('(a+b)^2 = a^2 + 2ab + b^2');
    assert.equal(mis, null);
  });

  await t.test('diagnoses projectile apex acceleration misconception', () => {
    const mis = scanForMisconception('প্রাসের সর্বোচ্চ উচ্চতায় ত্বরণ শূন্য হবে');
    assert.ok(mis);
    assert.equal(mis.id, 'PHYSICS_PROJECTILE_APEX_ACCELERATION');
    assert.match(mis.explanationBn, /অভিকর্ষজ ত্বরণ g/);
  });

  await t.test('diagnoses mass vs weight confusion', () => {
    const mis = scanForMisconception('বস্তুটির ভর ৫০ নিউটন দেওয়া আছে');
    assert.ok(mis);
    assert.equal(mis.id, 'PHYSICS_MASS_WEIGHT_CONFUSION');
  });

  await t.test('diagnoses action-reaction cancellation misconception', () => {
    const mis = scanForMisconception('ক্রিয়া ও প্রতিক্রিয়া বল পরস্পরকে বাতিল করে দেয়');
    assert.ok(mis);
    assert.equal(mis.id, 'PHYSICS_NEWTON_THIRD_LAW_CANCELLATION');
  });

  await t.test('diagnoses chemistry STP vs SATP confusion', () => {
    const mis = scanForMisconception('আদর্শ তাপমাত্রা ও চাপে মোলার আয়তন ২৪.৭৮ লিটার');
    assert.ok(mis);
    assert.equal(mis.id, 'CHEMISTRY_MOLAR_VOLUME_STP');
  });

  await t.test('diagnoses ICT hex nibble bit grouping misconception', () => {
    const mis = scanForMisconception('হেক্সাডেসিমেল সংখ্যাকে বাইনারিতে রূপান্তর করতে ৩ বিট করে সাজাতে হবে');
    assert.ok(mis);
    assert.equal(mis.id, 'ICT_HEX_BINARY_NIBBLE_GROUPING');
  });
});

test('Socratic AI Engine - Problem Domain Analysis & Scaffolding', async (t) => {
  await t.test('correctly classifies projectile motion and attaches projectile simulator', () => {
    const analysis = analyzeProblemDomain('একটি বস্তুকে অনুভূমিকের সাথে ৩০ ডিগ্রি কোণে নিক্ষিপ্ত প্রাসের সর্বোচ্চ উচ্চতা');
    assert.equal(analysis.detectedDomain, 'physics');
    assert.ok(analysis.simulators.includes('projectile'));
    assert.equal(analysis.scaffolding.length, 4);
    assert.equal(analysis.scaffolding[0].tier, 1);
    assert.equal(analysis.scaffolding[3].isTerminal, true);
  });

  await t.test('correctly classifies chemistry stoichiometry and attaches molecular simulator', () => {
    const analysis = analyzeProblemDomain('৫ মোল অ্যাসিডের সাথে ক্ষারের বিক্রিয়ায় উৎপন্ন লবণের পরিমাণ');
    assert.equal(analysis.detectedDomain, 'chemistry');
    assert.ok(analysis.simulators.includes('chemistry_molecule'));
    assert.equal(analysis.scaffolding.length, 4);
  });

  await t.test('correctly classifies higher math quadratic equations and past board exam', () => {
    const analysis = analyzeProblemDomain('2x^2 + 7x - 4 = 0 দ্বিঘাত সমীকরণটির মূল নির্ণয়');
    assert.equal(analysis.detectedDomain, 'math');
    assert.match(analysis.relevantBoardExamBn, /ঢাকা ও রাজশাহী বোর্ড/);
    assert.equal(analysis.scaffolding.length, 4);
  });
});
