import { test, describe } from 'node:test';
import assert from 'node:assert';
import { 
  CAREER_CATEGORIES, 
  BANGLADESH_DIVISIONS, 
  VERIFIED_CAREER_JOBS, 
  GOVT_CIRCULAR_ARCHIVES, 
  SALARY_BENCHMARKS, 
  CAREER_PORTAL_FAQS 
} from '../data/careerElevationData.ts';

describe('Bdjobs Elevation: Career Data Model & Integrity Suite', () => {

  test('T001: Category dataset contains both functional and special skills categories', () => {
    assert.strictEqual(CAREER_CATEGORIES.length >= 12, true, 'Must have at least 12 categories');
    const functional = CAREER_CATEGORIES.filter(c => c.type === 'functional');
    const skills = CAREER_CATEGORIES.filter(c => c.type === 'special_skill');
    
    assert.strictEqual(functional.length >= 8, true, 'Must have at least 8 functional categories');
    assert.strictEqual(skills.length >= 4, true, 'Must have at least 4 special skill categories');

    for (const cat of CAREER_CATEGORIES) {
      assert.ok(cat.nameBn.length > 0, 'Category must have a valid Bengali name');
      assert.ok(cat.jobCount > 0, 'Category job count must be positive');
      assert.ok(cat.iconName.length > 0, 'Category must have an icon name');
    }
  });

  test('T002: Bangladesh divisions taxonomy covers all 8 administrative divisions', () => {
    const divisionIds = BANGLADESH_DIVISIONS.map(d => d.id);
    const expected = ['dhaka', 'chattogram', 'rajshahi', 'khulna', 'barishal', 'sylhet', 'rangpur', 'mymensingh'];
    
    for (const exp of expected) {
      assert.ok(divisionIds.includes(exp), `Missing division: ${exp}`);
    }

    for (const div of BANGLADESH_DIVISIONS) {
      assert.ok(div.districts.length > 0, `Division ${div.id} must have districts defined`);
    }
  });

  test('T003: Verified jobs feed has valid salary ranges, deadlines, and requirements', () => {
    assert.strictEqual(VERIFIED_CAREER_JOBS.length >= 8, true, 'Must have at least 8 verified jobs');

    for (const job of VERIFIED_CAREER_JOBS) {
      assert.ok(job.id.startsWith('JOB-BD-'), `Job ID must follow convention: ${job.id}`);
      assert.ok(job.minSalary <= job.maxSalary, `Job ${job.id} minSalary must be <= maxSalary`);
      assert.ok(job.vacancy >= 1, `Job ${job.id} must have at least 1 vacancy`);
      assert.ok(job.educationRequirements.length > 0, `Job ${job.id} must have educational requirements`);
      assert.ok(job.responsibilities.length > 0, `Job ${job.id} must have responsibilities`);
      assert.ok(job.benefits.length > 0, `Job ${job.id} must specify benefits`);
    }
  });

  test('T004: Official government circular archives cover key national institutions', () => {
    assert.strictEqual(GOVT_CIRCULAR_ARCHIVES.length >= 4, true, 'Must have at least 4 govt circulars');

    for (const circ of GOVT_CIRCULAR_ARCHIVES) {
      assert.ok(circ.totalPosts > 0, `Circular ${circ.id} must have positive post count`);
      assert.ok(circ.officialRef.length > 0, `Circular ${circ.id} must have official reference`);
      assert.ok(circ.gradePayScale.length > 0, `Circular ${circ.id} must state pay scale`);
    }
  });

  test('T005: Salary benchmarks and FAQs are populated with authentic Bangladeshi market data', () => {
    assert.strictEqual(SALARY_BENCHMARKS.length >= 5, true, 'Must cover at least 5 industries');
    assert.strictEqual(CAREER_PORTAL_FAQS.length >= 4, true, 'Must have at least 4 FAQs');

    for (const bench of SALARY_BENCHMARKS) {
      assert.ok(bench.entryLevelSalary.includes('টাকা'), 'Salary benchmark must be formatted in Taka');
      assert.ok(bench.midLevelSalary.includes('টাকা'), 'Salary benchmark must be formatted in Taka');
      assert.ok(bench.seniorLevelSalary.includes('টাকা'), 'Salary benchmark must be formatted in Taka');
    }
  });

});
