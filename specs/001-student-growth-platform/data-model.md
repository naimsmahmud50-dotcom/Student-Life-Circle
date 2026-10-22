# Relational Data Model: Student Growth Platform (অগ্রযাত্রা)

**Database Engine:** PostgreSQL 16+  
**ORM / Query Layer:** Drizzle ORM / Prisma with Strict TypeScript Types  

---

## 1. Entity Relationship Overview

```
 [ users ] ──< [ user_roles ]
    │
    ├───< [ student_profiles ] ──< [ education_history ]
    │            │
    │            ├───< [ guardian_links ]
    │            ├───< [ mastery_records ]
    │            ├───< [ quiz_attempts ] ──< [ attempt_answers ]
    │            │            │
    │            │            └─── [ quiz_results ]
    │            ├───< [ student_skills ]
    │            ├───< [ student_projects ]
    │            └───< [ cv_snapshots ] ──< [ job_applications ]
    │
    ├───< [ tuition_listings ] ──< [ tuition_applications ]
    │
    └───< [ audit_logs ]

 [ curricula ] ──< [ subjects ] ──< [ topics ]
                                         │
 [ questions ] ──< [ question_versions ] ┘
                           │
                           ├───< [ question_options ]
                           └───< [ question_reports ]

 [ test_blueprints ] ──< [ live_sessions ] ──< [ session_questions ]
```

---

## 2. Core Relational Schemas

### 2.1 Identity, Users & Permissions

```sql
CREATE TYPE user_role_enum AS ENUM (
    'STUDENT', 
    'GUARDIAN', 
    'TUTOR', 
    'EMPLOYER', 
    'CONTENT_EDITOR', 
    'SUBJECT_REVIEWER', 
    'SAFETY_MODERATOR', 
    'ADMIN'
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(32) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    pseudonym VARCHAR(64) UNIQUE, -- Displayed on leaderboards for privacy
    avatar_url VARCHAR(512),
    is_phone_verified BOOLEAN DEFAULT FALSE,
    is_email_verified BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(128),
    mfa_enabled BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role user_role_enum NOT NULL,
    assigned_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    assigned_by UUID REFERENCES users(id),
    PRIMARY KEY (user_id, role)
);

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_user_sessions_lookup ON user_sessions(session_token, expires_at);
```

### 2.2 Student Profiles & Minor Consent

```sql
CREATE TYPE education_stage_enum AS ENUM (
    'PRIMARY',         -- Class 1-5
    'MIDDLE',          -- Class 6-8
    'SSC',             -- Class 9-10
    'HSC',             -- Class 11-12
    'ADMISSION',       -- University Admission Candidate
    'UNIVERSITY',      -- Undergraduate / Graduate
    'JOB_SEEKER'       -- Career & Lifelong Learner
);

CREATE TABLE student_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stage education_stage_enum NOT NULL DEFAULT 'MIDDLE',
    class_grade SMALLINT, -- e.g. 7, 10, 12
    curriculum_version VARCHAR(32) DEFAULT 'NCTB-2024',
    medium VARCHAR(16) DEFAULT 'BANGLA', -- 'BANGLA' | 'ENGLISH_VERSION'
    target_exam VARCHAR(64), -- e.g. 'DU_UNIT_A', 'BUET', 'MEDICAL'
    is_minor BOOLEAN DEFAULT TRUE,
    privacy_mode VARCHAR(16) DEFAULT 'PRIVATE', -- 'PRIVATE' | 'PSEUDONYMOUS' | 'PUBLIC_PORTFOLIO'
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE guardian_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    guardian_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    relationship VARCHAR(32) NOT NULL, -- 'FATHER', 'MOTHER', 'LEGAL_GUARDIAN'
    consent_status VARCHAR(16) DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REVOKED'
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, guardian_user_id)
);
```

### 2.3 Curricula, Subjects & Topics

```sql
CREATE TABLE curricula (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(32) UNIQUE NOT NULL, -- e.g. 'NCTB_2024'
    title VARCHAR(128) NOT NULL,
    year_established SMALLINT NOT NULL
);

CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curriculum_id UUID NOT NULL REFERENCES curricula(id),
    stage education_stage_enum NOT NULL,
    code VARCHAR(32) NOT NULL, -- e.g. 'MATH_CLASS_7'
    name_bn VARCHAR(128) NOT NULL,
    name_en VARCHAR(128) NOT NULL,
    UNIQUE(curriculum_id, stage, code)
);

CREATE TABLE topics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    chapter_number SMALLINT,
    title_bn VARCHAR(255) NOT NULL,
    title_en VARCHAR(255) NOT NULL,
    parent_topic_id UUID REFERENCES topics(id)
);
```

### 2.4 Question Bank, Versioning & Review Machine

```sql
CREATE TYPE question_status_enum AS ENUM (
    'DRAFT', 
    'NEEDS_REVIEW', 
    'APPROVED', 
    'SCHEDULED', 
    'PUBLISHED', 
    'QUARANTINED', 
    'ARCHIVED'
);

CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID NOT NULL REFERENCES topics(id),
    current_version_id UUID,
    status question_status_enum DEFAULT 'DRAFT',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE question_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    version_number SMALLINT NOT NULL,
    stem_bn TEXT NOT NULL,
    stem_en TEXT,
    explanation_bn TEXT NOT NULL,
    explanation_en TEXT,
    difficulty VARCHAR(16) DEFAULT 'MEDIUM', -- 'EASY', 'MEDIUM', 'HARD'
    cognitive_skill VARCHAR(32) DEFAULT 'REASONING', -- 'RECALL', 'APPLICATION', 'REASONING'
    estimated_seconds SMALLINT DEFAULT 60,
    source_attribution VARCHAR(255), -- e.g. 'NCTB Math Book 2024, Page 42'
    content_hash CHAR(64) NOT NULL, -- SHA-256 for exact deduplication
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(question_id, version_number)
);

CREATE TABLE question_options (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_version_id UUID NOT NULL REFERENCES question_versions(id) ON DELETE CASCADE,
    option_key CHAR(1) NOT NULL, -- 'A', 'B', 'C', 'D'
    option_text_bn TEXT NOT NULL,
    option_text_en TEXT,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE question_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_version_id UUID NOT NULL REFERENCES question_versions(id),
    reported_by UUID NOT NULL REFERENCES users(id),
    issue_type VARCHAR(32) NOT NULL, -- 'WRONG_ANSWER', 'TYPO', 'AMBIGUOUS', 'OUTDATED'
    description TEXT,
    status VARCHAR(16) DEFAULT 'PENDING', -- 'PENDING', 'ACCEPTED', 'REJECTED'
    resolved_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

### 2.5 Live MCQ Sessions, Attempts & Idempotent Answers

```sql
CREATE TYPE session_mode_enum AS ENUM (
    'ANYTIME_PRACTICE', 
    'LIVE_CHALLENGE', 
    'MOCK_EXAM', 
    'MISTAKE_REPLAY'
);

CREATE TABLE test_blueprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    mode session_mode_enum NOT NULL,
    stage education_stage_enum NOT NULL,
    subject_id UUID REFERENCES subjects(id),
    total_questions SMALLINT NOT NULL,
    duration_seconds INT NOT NULL,
    negative_marking_value NUMERIC(3, 2) DEFAULT 0.00, -- e.g. 0.25
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE live_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id UUID NOT NULL REFERENCES test_blueprints(id),
    title VARCHAR(255) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    status VARCHAR(16) DEFAULT 'SCHEDULED', -- 'SCHEDULED', 'ACTIVE', 'CALCULATING', 'CLOSED'
    is_frozen BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    live_session_id UUID REFERENCES live_sessions(id),
    blueprint_id UUID NOT NULL REFERENCES test_blueprints(id),
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL, -- Server-authoritative cutoff
    submitted_at TIMESTAMPTZ,
    status VARCHAR(16) DEFAULT 'IN_PROGRESS', -- 'IN_PROGRESS', 'SUBMITTED', 'EXPIRED'
    random_seed INT NOT NULL, -- Anchors deterministic question & option order
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_quiz_attempts_user ON quiz_attempts(user_id, status);

CREATE TABLE attempt_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    question_version_id UUID NOT NULL REFERENCES question_versions(id),
    selected_option_id UUID REFERENCES question_options(id),
    idempotency_key UUID UNIQUE NOT NULL, -- Prevents duplicate write on reconnection
    saved_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    time_taken_seconds NUMERIC(5, 2),
    is_correct BOOLEAN,
    UNIQUE(attempt_id, question_version_id)
);

CREATE TABLE quiz_results (
    attempt_id UUID PRIMARY KEY REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    total_questions SMALLINT NOT NULL,
    correct_count SMALLINT NOT NULL,
    incorrect_count SMALLINT NOT NULL,
    unanswered_count SMALLINT NOT NULL,
    raw_score NUMERIC(6, 2) NOT NULL,
    time_spent_seconds INT NOT NULL,
    rank INT,
    percentile NUMERIC(5, 2),
    calculated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

### 2.6 Spaced-Repetition Mastery Records

```sql
CREATE TABLE mastery_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    attempt_count INT DEFAULT 0,
    correct_count INT DEFAULT 0,
    last_attempted_at TIMESTAMPTZ,
    next_revision_due TIMESTAMPTZ,
    mastery_level NUMERIC(3, 2) DEFAULT 0.00, -- 0.00 to 1.00
    is_in_mistake_queue BOOLEAN DEFAULT FALSE,
    UNIQUE(student_id, topic_id)
);
CREATE INDEX idx_mastery_revision ON mastery_records(student_id, next_revision_due) WHERE is_in_mistake_queue = TRUE;
```

### 2.7 Tuition Marketplace & Contact Consent

```sql
CREATE TABLE tuition_listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_user_id UUID NOT NULL REFERENCES users(id),
    class_grade SMALLINT NOT NULL,
    curriculum VARCHAR(32) NOT NULL,
    medium VARCHAR(16) NOT NULL,
    subject VARCHAR(128) NOT NULL,
    location_district VARCHAR(64) NOT NULL,
    location_thana VARCHAR(64) NOT NULL,
    is_online BOOLEAN DEFAULT FALSE,
    salary_range_min INT,
    salary_range_max INT,
    status VARCHAR(16) DEFAULT 'PUBLISHED', -- 'DRAFT', 'PUBLISHED', 'CLOSED', 'REPORTED'
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tuition_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL REFERENCES tuition_listings(id) ON DELETE CASCADE,
    tutor_user_id UUID NOT NULL REFERENCES users(id),
    message TEXT,
    contact_consent_granted BOOLEAN DEFAULT FALSE,
    status VARCHAR(16) DEFAULT 'APPLIED', -- 'APPLIED', 'SHORTLISTED', 'ACCEPTED', 'REJECTED'
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(listing_id, tutor_user_id)
);
```

### 2.8 Portfolio, CV Snapshots & Career Applications

```sql
CREATE TABLE student_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    skill_name VARCHAR(64) NOT NULL,
    proficiency VARCHAR(16) DEFAULT 'INTERMEDIATE', -- 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'
    evidence_url VARCHAR(512), -- GitHub repo, live demo, verified certificate
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by VARCHAR(128)
);

CREATE TABLE cv_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(128) NOT NULL,
    snapshot_json JSONB NOT NULL, -- Immutable frozen data: education, skills, projects
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job_listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employer_user_id UUID NOT NULL REFERENCES users(id),
    company_name VARCHAR(128) NOT NULL,
    is_company_verified BOOLEAN DEFAULT FALSE,
    title VARCHAR(128) NOT NULL,
    work_mode VARCHAR(16) DEFAULT 'HYBRID', -- 'ONSITE', 'REMOTE', 'HYBRID'
    salary_range VARCHAR(64),
    status VARCHAR(16) DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES job_listings(id),
    candidate_user_id UUID NOT NULL REFERENCES users(id),
    cv_snapshot_id UUID NOT NULL REFERENCES cv_snapshots(id),
    stage VARCHAR(16) DEFAULT 'APPLIED', -- 'APPLIED', 'VIEWED', 'INTERVIEW', 'OFFER', 'REJECTED'
    applied_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, candidate_user_id)
);
```

### 2.9 Immutable Audit Logging

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID REFERENCES users(id),
    actor_role VARCHAR(32) NOT NULL,
    action VARCHAR(64) NOT NULL, -- e.g. 'QUARANTINE_QUESTION', 'UPDATE_ANSWER_KEY', 'CHANGE_USER_ROLE'
    entity_type VARCHAR(64) NOT NULL, -- 'QUESTION_VERSION', 'USER', 'JOB_LISTING'
    entity_id UUID NOT NULL,
    reason TEXT NOT NULL,
    payload_before JSONB,
    payload_after JSONB,
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_id, action);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
```
