import test from 'node:test';
import assert from 'node:assert/strict';
import {
  GOEDU_COURSES,
  GOEDU_BUNDLES,
  GOEDU_INSTRUCTORS,
  GOEDU_CATEGORIES,
  getCoursesByCategory,
  searchGoEduCourses
} from '../goeduData.ts';

test('GoEdu Data Architecture - Categories and Baseline Integrity', () => {
  assert.ok(GOEDU_CATEGORIES.length >= 5, 'Should have at least 5 main categories');
  assert.equal(GOEDU_CATEGORIES[0].id, 'all', 'First category should be "all"');
  assert.ok(GOEDU_COURSES.length >= 8, 'Should have at least 8 featured courses');
  assert.ok(GOEDU_BUNDLES.length >= 2, 'Should have at least 2 featured bundles');
  assert.ok(GOEDU_INSTRUCTORS.length >= 4, 'Should have at least 4 verified instructors');
});

test('GoEdu Data Architecture - Category Filtering', () => {
  const allCourses = getCoursesByCategory('all');
  assert.equal(allCourses.length, GOEDU_COURSES.length);

  const mathCourses = getCoursesByCategory('stem-math');
  assert.ok(mathCourses.length > 0);
  assert.ok(mathCourses.every(c => c.categorySlug === 'stem-math'));

  const aiCourses = getCoursesByCategory('ai-tech');
  assert.ok(aiCourses.length > 0);
  assert.ok(aiCourses.every(c => c.categorySlug === 'ai-tech'));
});

test('GoEdu Data Architecture - Search Functionality', () => {
  const calculusResults = searchGoEduCourses('calculus');
  assert.ok(calculusResults.length >= 1);
  assert.ok(calculusResults[0].title.toLowerCase().includes('calculus'));

  const bengaliResults = searchGoEduCourses('রসায়ন');
  assert.ok(bengaliResults.length >= 1);
  assert.ok(bengaliResults[0].bengaliTitle.includes('রসায়ন'));

  const instructorResults = searchGoEduCourses('Sayma');
  assert.ok(instructorResults.length >= 1);

  const emptyResults = searchGoEduCourses('');
  assert.equal(emptyResults.length, GOEDU_COURSES.length);
});

test('GoEdu Data Architecture - Course and Bundle Pricing Discipline', () => {
  for (const course of GOEDU_COURSES) {
    assert.ok(course.price > 0, `Course ${course.id} must have valid positive price`);
    if (course.discountPrice) {
      assert.ok(course.discountPrice < course.price, `Discount price must be less than regular price for course ${course.id}`);
    }
    assert.ok(course.durationMinutes > 0, `Duration must be positive for course ${course.id}`);
    assert.ok(course.totalLessons > 0, `Total lessons must be positive for course ${course.id}`);
    assert.ok(course.rating >= 4.0 && course.rating <= 5.0, `Rating must be between 4.0 and 5.0 for course ${course.id}`);
  }

  for (const bundle of GOEDU_BUNDLES) {
    assert.ok(bundle.bundlePrice < bundle.originalPrice, `Bundle ${bundle.id} must have promotional discount`);
    assert.ok(bundle.highlights.length >= 3, `Bundle ${bundle.id} must have key curriculum highlights`);
  }
});
