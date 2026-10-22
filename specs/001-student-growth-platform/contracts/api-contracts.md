# API Contracts & Interface Definitions

**Protocol:** HTTPS / REST (v1) + WebSockets (for live session sync)  
**Authentication:** Bearer JWT / HttpOnly Secure Cookies  
**Idempotency Header:** `X-Idempotency-Key: <UUIDv4>` (required for writes/saves)  

---

## 1. Global Standard Response & Error Envelope

### Standard Success Response
```json
{
  "success": true,
  "data": {},
  "meta": {
    "server_timestamp": "2026-10-14T04:30:00.000Z",
    "request_id": "req_8f1a2b3c4d5e"
  }
}
```

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "EXPIRED_SESSION",
    "message": "The exam window has closed. Answers can no longer be recorded.",
    "details": []
  },
  "meta": {
    "server_timestamp": "2026-10-14T04:30:00.000Z",
    "request_id": "req_8f1a2b3c4d5e"
  }
}
```

---

## 2. Core API Endpoints

### 2.1 Identity & Session
#### `GET /api/v1/me`
- **Permission:** Any Authenticated User
- **Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "pseudonym": "Nirnoy_72",
    "full_name": "Mahmud Hasan",
    "roles": ["STUDENT"],
    "student_profile": {
      "stage": "HSC",
      "class_grade": 12,
      "medium": "BANGLA",
      "target_exam": "DU_UNIT_A",
      "is_minor": false
    }
  }
}
```

---

### 2.2 Practice & Anytime MCQ Engine
#### `GET /api/v1/practice/sets`
- **Query Params:** `stage=HSC&subject_id=sub_xyz&topic_id=top_123&limit=10`
- **Permission:** Student
- **Response:**
```json
{
  "success": true,
  "data": {
    "set_id": "set_98a76b5c",
    "topic_title_bn": "স্থিতিবিদ্যা ও গতিবিদ্যা",
    "question_count": 10,
    "estimated_minutes": 15,
    "has_mistakes_in_queue": true
  }
}
```

#### `POST /api/v1/quiz-attempts`
- **Permission:** Student
- **Body:**
```json
{
  "blueprint_id": "bp_4a5b6c7d",
  "live_session_id": null
}
```
- **Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "attempt_id": "att_018f2d8b-3e9a-7a55-bc12-890abcdef123",
    "started_at": "2026-10-14T04:30:00.000Z",
    "expires_at": "2026-10-14T04:45:00.000Z",
    "questions": [
      {
        "question_version_id": "qv_998877",
        "order": 1,
        "stem_bn": "একটি বস্তুর ভর ৫ কেজি এবং ত্বরণ ২ মি/সে² হলে প্রযুক্ত বল কত?",
        "options": [
          { "id": "opt_a", "key": "A", "text_bn": "১০ নিউটন" },
          { "id": "opt_b", "key": "B", "text_bn": "৭ নিউটন" },
          { "id": "opt_c", "key": "C", "text_bn": "২.৫ নিউটন" },
          { "id": "opt_d", "key": "D", "text_bn": "৩ নিউটন" }
        ]
      }
    ]
  }
}
```

#### `PUT /api/v1/quiz-attempts/:attempt_id/answers/:question_version_id`
- **Header:** `X-Idempotency-Key: <UUID>`
- **Permission:** Attempt Owner Only
- **Body:**
```json
{
  "selected_option_id": "opt_a",
  "time_taken_seconds": 12.5
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "SAVED",
    "attempt_id": "att_018f2d8b-3e9a-7a55-bc12-890abcdef123",
    "question_version_id": "qv_998877",
    "saved_at": "2026-10-14T04:30:15.120Z"
  }
}
```

#### `POST /api/v1/quiz-attempts/:attempt_id/submit`
- **Header:** `X-Idempotency-Key: <UUID>`
- **Permission:** Attempt Owner Only
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "attempt_id": "att_018f2d8b-3e9a-7a55-bc12-890abcdef123",
    "status": "SUBMITTED",
    "submitted_at": "2026-10-14T04:42:10.000Z",
    "result_release_policy": "IMMEDIATE"
  }
}
```

#### `GET /api/v1/quiz-attempts/:attempt_id/result`
- **Permission:** Attempt Owner Only
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "score": {
      "raw_score": 9.0,
      "total_questions": 10,
      "correct": 9,
      "incorrect": 1,
      "unanswered": 0,
      "time_spent_seconds": 730
    },
    "mistakes_review": [
      {
        "question_version_id": "qv_998878",
        "stem_bn": "নিচের কোনটি বলের মাত্রা?",
        "selected_option_key": "B",
        "correct_option_key": "A",
        "correct_option_text_bn": "[MLT⁻²]",
        "explanation_bn": "বল = ভর × ত্বরণ = M × LT⁻² = MLT⁻²।",
        "misconception_tag": "DIMENSIONAL_ANALYSIS"
      }
    ],
    "added_to_revision_queue": true
  }
}
```

---

### 2.3 Scheduled Live Challenge
#### `GET /api/v1/live-mcq/sessions`
- **Permission:** Public / Authenticated
- **Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "live_2026_10_18",
      "title": "HSC পদার্থবিজ্ঞান ১ম পত্র লাইভ চ্যালেঞ্জ",
      "start_time": "2026-10-18T14:00:00.000Z",
      "end_time": "2026-10-18T14:30:00.000Z",
      "duration_minutes": 25,
      "total_questions": 30,
      "status": "SCHEDULED",
      "registered_participants_count": 8420
    }
  ]
}
```

---

### 2.4 Question Reporting & Administrative Quarantine
#### `POST /api/v1/questions/:id/reports`
- **Permission:** Authenticated User (Rate limited)
- **Body:**
```json
{
  "question_version_id": "qv_998877",
  "issue_type": "WRONG_ANSWER",
  "description": "বিকল্প A এবং C উভয়ই সঠিক হতে পারে।"
}
```
- **Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "report_id": "rep_771122",
    "status": "RECEIVED",
    "message": "আপনার রিপোর্টটি পর্যালোচনার জন্য জমা হয়েছে।"
  }
}
```

#### `POST /api/v1/admin/question-versions/:id/decision`
- **Permission:** Role `SUBJECT_REVIEWER` or `ADMIN`
- **Body:**
```json
{
  "action": "QUARANTINE",
  "reason": "Report confirmed: Ambiguous stem detected. Pending new version release.",
  "recalculate_active_sessions": true
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "question_id": "q_112233",
    "new_status": "QUARANTINED",
    "affected_attempts_count": 142,
    "audit_log_id": "aud_998811"
  }
}
```
