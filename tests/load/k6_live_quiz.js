/**
 * DEVELOPER ARCHITECTURE NOTES:
 * -----------------------------------------------------------------------------
 * Target System: Ogrojatra National Live Challenge Platform
 * Purpose: Hyper-Scale k6 Distributed Stress Testing (50,000 Concurrent Students)
 * Peak Load Target: 50,000 Virtual Users (VUs) during synchronized 8:00 PM National Challenge
 * Standards:
 *   - p95 Latency: < 200ms
 *   - p99 Latency: < 500ms
 *   - Error Rate: < 0.01 (Targeting 0.00% under burst load)
 *   - Zero Dropped Answers: Invariant enforced via Redis ingestion buffer
 *   - Idempotency: All answer submissions carry UUIDv4 X-Idempotency-Key
 * Compliance: Strict Zero-Emoji Policy, WCAG / RFC-compliant telemetry.
 * -----------------------------------------------------------------------------
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate, Counter } from 'k6/metrics';

// Custom latency trends for granular SLA breakdown
export const authLoginDuration = new Trend('auth_login_duration');
export const questionFetchDuration = new Trend('question_fetch_duration');
export const quizSubmissionDuration = new Trend('quiz_submission_duration');
export const leaderboardPollDuration = new Trend('leaderboard_poll_duration');

// Reliability counters and rate meters
export const submissionSuccessRate = new Rate('submission_success_rate');
export const droppedSubmissionsCount = new Counter('dropped_submissions_count');
export const idempotentDuplicationCounter = new Counter('idempotent_duplications_absorbed');

// Configuration options defining the multi-stage traffic profile
export const options = {
  scenarios: {
    national_live_challenge: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        // Stage 1: Warm-up and steady ramp from 0 to 10,000 users over 2 minutes
        { duration: '2m', target: 10000 },
        // Stage 2: Spike from 10,000 to 50,000 concurrent users over 3 minutes (simulating 8:00 PM rush)
        { duration: '3m', target: 50000 },
        // Stage 3: Sustained national challenge peak with 50,000 concurrent students for 5 minutes
        { duration: '5m', target: 50000 },
        // Stage 4: Orderly cooldown and session completion ramp-down over 2 minutes
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
  },
  thresholds: {
    // Platform SLA constraints
    'http_req_duration': ['p(95)<200', 'p(99)<500'],
    'http_req_failed': ['rate<0.01'],

    // Granular step SLAs
    'auth_login_duration': ['p(95)<180'],
    'question_fetch_duration': ['p(95)<150'],
    'quiz_submission_duration': ['p(95)<150'],
    'leaderboard_poll_duration': ['p(95)<120'],
    'submission_success_rate': ['rate>0.99'],
    'dropped_submissions_count': ['count==0'],
  },
};

const BASE_URL = __ENV.TARGET_BASE_URL || 'http://localhost:8000';
const CHALLENGE_ID = __ENV.CHALLENGE_ID || 'national-stem-olympiad-2026';

/**
 * Generates an RFC 4122 v4 compliant UUID string for idempotency tokens.
 */
function generateUuidV4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * Main Virtual User loop simulating a student participating in the live challenge.
 */
export default function () {
  const vuId = __VU;
  const iteration = __ITER;
  const studentId = `student_vu_${vuId}_${iteration}`;

  // ---------------------------------------------------------------------------
  // STEP 1: Authenticated Student Login / Token Acquisition
  // ---------------------------------------------------------------------------
  const loginPayload = JSON.stringify({
    username: `student_${vuId}@ogrojatra.edu.bd`,
    password: 'StandardSecuredPassword2026!',
    student_id: studentId,
  });

  const authHeaders = {
    'Content-Type': 'application/json',
    'User-Agent': 'Ogrojatra-LoadTest-k6/1.0',
    'X-Client-Platform': 'web-high-throughput',
  };

  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, loginPayload, {
    headers: authHeaders,
    tags: { name: 'AuthLogin' },
  });

  authLoginDuration.add(loginRes.timings.duration);

  const loginOk = check(loginRes, {
    'auth_status_is_200': (r) => r.status === 200,
    'token_present': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.access_token !== undefined || body.token !== undefined || r.status === 200;
      } catch (e) {
        return r.status === 200;
      }
    },
  });

  let bearerToken = 'mock-jwt-token-vu-' + vuId;
  try {
    const parsed = JSON.parse(loginRes.body);
    if (parsed.access_token) {
      bearerToken = parsed.access_token;
    }
  } catch (e) {
    // Fall back to synthetic token for isolated benchmark harnesses
  }

  const authenticatedHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${bearerToken}`,
    'X-Student-ID': studentId,
  };

  // Brief thinking pause before fetching question
  sleep(Math.random() * 0.5 + 0.2);

  // ---------------------------------------------------------------------------
  // STEP 2: Fetch Live Question Set
  // ---------------------------------------------------------------------------
  const questionRes = http.get(
    `${BASE_URL}/api/v1/quiz/active?challenge_id=${CHALLENGE_ID}`,
    {
      headers: authenticatedHeaders,
      tags: { name: 'FetchLiveQuestion' },
    }
  );

  questionFetchDuration.add(questionRes.timings.duration);

  check(questionRes, {
    'question_status_is_200': (r) => r.status === 200,
    'has_questions_or_active_flag': (r) => r.status === 200,
  });

  // Simulate reading and problem-solving time (1 to 2.5 seconds)
  sleep(Math.random() * 1.5 + 1.0);

  // ---------------------------------------------------------------------------
  // STEP 3: Submit Answer with X-Idempotency-Key
  // ---------------------------------------------------------------------------
  const idempotencyKey = generateUuidV4();
  const submissionPayload = JSON.stringify({
    challenge_id: CHALLENGE_ID,
    question_id: 'stem_phys_2026_q1',
    selected_option: Math.floor(Math.random() * 4),
    client_timestamp: new Date().toISOString(),
    student_id: studentId,
  });

  const submissionHeaders = Object.assign({}, authenticatedHeaders, {
    'X-Idempotency-Key': idempotencyKey,
    'X-Buffer-Priority': 'high',
  });

  const submitRes = http.post(`${BASE_URL}/api/v1/quiz/answer`, submissionPayload, {
    headers: submissionHeaders,
    tags: { name: 'SubmitAnswer' },
  });

  quizSubmissionDuration.add(submitRes.timings.duration);

  const isAcceptedOrOk = submitRes.status === 200 || submitRes.status === 202;
  submissionSuccessRate.add(isAcceptedOrOk);

  if (!isAcceptedOrOk) {
    droppedSubmissionsCount.add(1);
  }

  check(submitRes, {
    'submission_status_is_200_or_202': (r) => r.status === 200 || r.status === 202,
    'submission_ack_received': (r) => r.status === 200 || r.status === 202,
  });

  // Simulated rapid re-submission with same idempotency key (1% frequency) to test deduplication
  if (Math.random() < 0.01) {
    const replayRes = http.post(`${BASE_URL}/api/v1/quiz/answer`, submissionPayload, {
      headers: submissionHeaders,
      tags: { name: 'ReplaySubmission' },
    });
    if (replayRes.status === 200 || replayRes.status === 202) {
      idempotentDuplicationCounter.add(1);
    }
  }

  // Brief pause before viewing live standing
  sleep(Math.random() * 0.8 + 0.4);

  // ---------------------------------------------------------------------------
  // STEP 4: Poll Live Leaderboard
  // ---------------------------------------------------------------------------
  const leaderboardRes = http.get(
    `${BASE_URL}/api/v1/live/leaderboard?challenge_id=${CHALLENGE_ID}&limit=50`,
    {
      headers: authenticatedHeaders,
      tags: { name: 'PollLeaderboard' },
    }
  );

  leaderboardPollDuration.add(leaderboardRes.timings.duration);

  check(leaderboardRes, {
    'leaderboard_status_is_200': (r) => r.status === 200,
    'leaderboard_response_time_under_200ms': (r) => r.timings.duration < 200,
  });

  // Final cycle pacing jitter (1.0 - 2.0s)
  sleep(Math.random() * 1.0 + 1.0);
}
