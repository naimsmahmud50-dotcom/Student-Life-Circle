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
  isCapabilityInquiry,
  TUTOR_CAPABILITIES_RESPONSE_BN,
  scanForMisconception,
  analyzeProblemDomain,
  findAcademicInvitation,
  resolveSocraticResponse,
  MISCONCEPTION_TAXONOMY,
  ZERO_ANSWER_LEAKING_REFUSAL_BN
} from '../socraticEngine.ts';

import {
  findPlatformKnowledge,
  formatPlatformFeatureResponse,
  PLATFORM_KNOWLEDGE_BASE
} from '../platformKnowledge.ts';

test('Socratic AI Engine - Capability Inquiry Detection', async (t) => {
  await t.test('detects Bengali and Banglish capability questions', () => {
    assert.equal(isCapabilityInquiry('tmi amk ki ki kaje help korba?'), true);
    assert.equal(isCapabilityInquiry('ki ki topic a tmi amk help korte parbe'), true);
    assert.equal(isCapabilityInquiry('তুমি আমাকে কী কী কাজে সাহায্য করবে?'), true);
    assert.equal(isCapabilityInquiry('তুমি কী করতে পারো?'), true);
    assert.equal(isCapabilityInquiry('who are you'), true);
    assert.equal(isCapabilityInquiry('what topics do you cover'), true);
  });

  await t.test('capabilities response outlines all STEM subjects and platform guidance', () => {
    assert.match(TUTOR_CAPABILITIES_RESPONSE_BN, /উচ্চতর গণিত/);
    assert.match(TUTOR_CAPABILITIES_RESPONSE_BN, /পদার্থবিজ্ঞান/);
    assert.match(TUTOR_CAPABILITIES_RESPONSE_BN, /রসায়ন/);
    assert.match(TUTOR_CAPABILITIES_RESPONSE_BN, /তথ্য ও যোগাযোগ প্রযুক্তি/);
    assert.match(TUTOR_CAPABILITIES_RESPONSE_BN, /খাতার ছবির ওটিআর/);
    assert.match(TUTOR_CAPABILITIES_RESPONSE_BN, /সাইট নেভিগেশন/);
  });
});

test('Socratic AI Engine - Academic Problem Invitation Detector', async (t) => {
  await t.test('detects math problem invitations', () => {
    const inv = findAcademicInvitation('amr akta math a problem somadhan dite parbe');
    assert.ok(inv);
    assert.equal(inv.domain, 'math');
    assert.match(inv.responseBn, /উচ্চতর গণিত/);
    assert.match(inv.responseBn, /বীজগণিত.*ক্যালকুলাস/);
  });

  await t.test('detects physics problem invitations', () => {
    const inv = findAcademicInvitation('physics a problem somadhan lagbe');
    assert.ok(inv);
    assert.equal(inv.domain, 'physics');
    assert.match(inv.responseBn, /পদার্থবিজ্ঞান/);
    assert.match(inv.responseBn, /৩ডি প্রজেক্টাইল/);
  });

  await t.test('detects chemistry problem invitations', () => {
    const inv = findAcademicInvitation('রসায়নে একটা সমস্যা সমাধান করতে পারবে?');
    assert.ok(inv);
    assert.equal(inv.domain, 'chemistry');
    assert.match(inv.responseBn, /রসায়ন|রসায়ন/);
    assert.match(inv.responseBn, /স্টয়কিওমেট্রি/);
  });

  await t.test('detects ICT problem invitations', () => {
    const inv = findAcademicInvitation('আইসিটিতে একটা সমস্যা বুঝতে পারছি না');
    assert.ok(inv);
    assert.equal(inv.domain, 'ict');
    assert.match(inv.responseBn, /আইসিটি/);
    assert.match(inv.responseBn, /বুলিয়ান বীজগণিত/);
  });

  await t.test('detects general academic invitations', () => {
    const inv = findAcademicInvitation('amr akta problem ache somadhan korte parbe');
    assert.ok(inv);
    assert.match(inv.responseBn, /(NCTB|জাতীয় শিক্ষাক্রম)/);
  });
});

test('Socratic AI Engine - Platform Omniscience Knowledge Base', async (t) => {
  await t.test('has 20 platform features registered', () => {
    assert.equal(PLATFORM_KNOWLEDGE_BASE.length, 20);
  });

  await t.test('detects tuition queries and routes to /tuition', () => {
    const feature = findPlatformKnowledge('হোম টিউটর কোথায় পাব?');
    assert.ok(feature);
    assert.equal(feature.route, '/tuition');
    assert.match(feature.titleBn, /টিউটরিং|Tuition/);
  });

  await t.test('detects live challenge queries and routes to /live-challenge', () => {
    const feature = findPlatformKnowledge('লাইভ চ্যালেঞ্জ কী?');
    assert.ok(feature);
    assert.equal(feature.route, '/live-challenge');
  });

  await t.test('detects admission predictor queries and routes to /admission/predictor', () => {
    const feature = findPlatformKnowledge('এডমিশন প্রেডিক্টর কীভাবে কাজ করে?');
    assert.ok(feature);
    assert.equal(feature.route, '/admission/predictor');
  });

  await t.test('detects board archives queries and routes to /board-archives', () => {
    const feature = findPlatformKnowledge('বিগত ১০ বছরের বোর্ড প্রশ্ন কোথায় পাব?');
    assert.ok(feature);
    assert.equal(feature.route, '/board-archives');
  });

  await t.test('detects 3D simulations queries and routes to /simulations', () => {
    const feature = findPlatformKnowledge('৩ডি ল্যাব কোথায়?');
    assert.ok(feature);
    assert.equal(feature.route, '/simulations');
  });

  await t.test('formats platform guidance response with clear page link and instructions', () => {
    const feature = findPlatformKnowledge('tuition kothay pabo?');
    assert.ok(feature);
    const formatted = formatPlatformFeatureResponse(feature);
    assert.match(formatted, /পৃষ্ঠা লিঙ্ক: \/tuition/);
    assert.match(formatted, /কীভাবে ব্যবহার করবেন:/);
  });
});

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

  await t.test('correctly classifies ICT boolean algebra and logic gates', () => {
    const analysis = analyzeProblemDomain('ডি মরগ্যান উপপাদ্য অনুযায়ী বুলিয়ান সমীকরণ সরলীকরণ');
    assert.equal(analysis.detectedDomain, 'ict');
    assert.match(analysis.identifiedTopicBn, /তথ্য ও যোগাযোগ প্রযুক্তি/);
    assert.equal(analysis.scaffolding.length, 4);
  });
});

test('Socratic AI Engine - Unified resolveSocraticResponse Orchestrator', async (t) => {
  await t.test('resolves capability question', () => {
    const res = resolveSocraticResponse('ki ki topic a tmi amk help korte parbe');
    assert.equal(res.type, 'capability');
    assert.match(res.text, /উচ্চতর গণিত/);
  });

  await t.test('resolves academic problem invitation for math', () => {
    const res = resolveSocraticResponse('amr akta math a problem somadhan dite parbe');
    assert.equal(res.type, 'academic_invitation');
    assert.match(res.text, /উচ্চতর গণিত এবং সাধারণ গণিত/);
  });

  await t.test('resolves platform knowledge question', () => {
    const res = resolveSocraticResponse('হোম টিউটর কোথায় পাব?');
    assert.equal(res.type, 'platform_knowledge');
    assert.equal(res.route, '/tuition');
    assert.match(res.text, /অগ্রযাত্রা প্ল্যাটফর্ম গাইড/);
  });

  await t.test('resolves direct answer demand refusal', () => {
    const res = resolveSocraticResponse('আমাকে সরাসরি উত্তর বলে দাও');
    assert.equal(res.type, 'zero_leak_refusal');
    assert.match(res.text, /সরাসরি উত্তর মুখস্থ করায় না/);
  });

  await t.test('resolves misconception diagnosis', () => {
    const res = resolveSocraticResponse('(a+b)^2 = a^2 + b^2');
    assert.equal(res.type, 'misconception');
    assert.match(res.text, /মধ্যপদ 2ab/);
  });

  await t.test('resolves actual math equation into tier 1 scaffolding', () => {
    const res = resolveSocraticResponse('2x^2 + 7x - 4 = 0 সমীকরণটির সমাধান কীভাবে করব?');
    assert.equal(res.type, 'scaffold');
    assert.match(res.text, /উচ্চতর গণিত/);
    assert.match(res.text, /সমীকরণটির ধরন/);
  });
});
