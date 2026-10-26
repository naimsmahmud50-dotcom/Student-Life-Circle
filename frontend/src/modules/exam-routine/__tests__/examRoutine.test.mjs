import { test, describe } from 'node:test';
import assert from 'node:assert';
import { INITIAL_EXAM_ROUTINES } from '../data/examRoutineData.ts';
import { DEFAULT_FEATURE_FLAGS, isFeatureEnabled } from '../../../config/featureFlags.ts';

describe('Live MCQ Routine & Mega Model Test: Client Module Integrity Suite', () => {

  test('T001: Initial routines dataset has 200-day BCS, Admission, and Mega Model Tests', () => {
    assert.strictEqual(INITIAL_EXAM_ROUTINES.length >= 6, true, 'Must have at least 6 seed routines');
    
    const bcsRoutines = INITIAL_EXAM_ROUTINES.filter(r => r.exam_type === 'BCS_PRELI');
    const admissionRoutines = INITIAL_EXAM_ROUTINES.filter(r => r.exam_type === 'ADMISSION_VARSITY');
    const megaTests = INITIAL_EXAM_ROUTINES.filter(r => r.is_mega_model_test);

    assert.ok(bcsRoutines.length >= 4, 'Must have at least 4 BCS routines');
    assert.ok(admissionRoutines.length >= 2, 'Must have at least 2 admission routines');
    assert.ok(megaTests.length >= 2, 'Must have at least 2 mega model tests');

    for (const routine of INITIAL_EXAM_ROUTINES) {
      assert.ok(routine.id.length > 0, 'Routine must have an ID');
      assert.ok(routine.title.length > 0, 'Routine must have a Bengali title');
      assert.ok(routine.syllabus_summary.length > 0, 'Routine must have a syllabus summary');
      assert.ok(routine.duration_minutes > 0, 'Duration must be positive');
      assert.ok(routine.total_questions > 0, 'Questions must be positive');
      assert.ok(routine.negative_mark_factor > 0, 'Negative mark factor must be set');
    }
  });

  test('T002: Mega model tests have higher question counts and realistic durations', () => {
    const mega = INITIAL_EXAM_ROUTINES.find(r => r.is_mega_model_test && r.exam_type === 'BCS_PRELI');
    assert.ok(mega, 'Must have a BCS Mega Model Test');
    assert.strictEqual(mega.total_questions, 200);
    assert.strictEqual(mega.duration_minutes, 120);
    assert.strictEqual(mega.negative_mark_factor, 0.50);
  });

  test('T003: Negative marking logic satisfies precision and penalty bounds', () => {
    // Test pure formula: Gross = Correct * 1.0, Penalty = Wrong * 0.25, Net = Max(0, Gross - Penalty)
    const simulate = (correct, wrong, negativeFactor = 0.25) => {
      const gross = correct * 1.0;
      const penalty = wrong * negativeFactor;
      const net = Math.max(0, Math.round((gross - penalty) * 100) / 100);
      return { gross, penalty, net };
    };

    const res1 = simulate(80, 15, 0.25);
    assert.strictEqual(res1.gross, 80.0);
    assert.strictEqual(res1.penalty, 3.75);
    assert.strictEqual(res1.net, 76.25);

    const res2 = simulate(10, 50, 0.25);
    assert.strictEqual(res2.gross, 10.0);
    assert.strictEqual(res2.penalty, 12.5);
    assert.strictEqual(res2.net, 0); // Net cannot fall below zero
  });

  test('T004: Feature flags default to disabled (OFF) in production', () => {
    assert.strictEqual(DEFAULT_FEATURE_FLAGS.examRoutine, false);
    assert.strictEqual(DEFAULT_FEATURE_FLAGS.studyArchive, false);
    assert.strictEqual(DEFAULT_FEATURE_FLAGS.circularAlert, false);
  });
});
