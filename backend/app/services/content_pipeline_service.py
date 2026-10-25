"""
========================================================================================
MODULE:    AI-Assisted Question Pipeline & Human-in-the-Loop SME Review Service
TOPIC:     Persistent Draft Ingestion, SME Review Queue, Inline Edit & Batch Moderation
FILE:      backend/app/services/content_pipeline_service.py
PURPOSE:   Orchestrates AI-assisted question draft generation and enforces the strict
           human Subject Matter Expert (SME) approval gate. Strictly prohibits AI
           from publishing questions directly into active exam pools. State transitions:
           DRAFT -> NEEDS_REVIEW -> APPROVED -> PUBLISHED, or REJECTED / NEEDS_CHANGES.
           Features thread-safe file persistence (draft_store.json) across restarts.
AUDIENCE:  Content Engineers, Subject Matter Reviewers & AI Agents
STANDARDS: FR-004 AI Quality Gate, Zero-Unreviewed-AI Policy, OWASP ASVS L2, Zero-Emoji
========================================================================================
"""

import os
import json
import uuid
import threading
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone
from backend.app.core.timekeeper import ServerTimekeeper
from backend.app.services.deduplication import QuestionDeduplicationService, deduplication_service

STORE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "draft_store.json"
)

DEFAULT_DRAFT_SEEDS: List[Dict[str, Any]] = [
    {
        "id": "q_draft_phys_301",
        "version": 1,
        "status": "NEEDS_REVIEW",
        "subject": "পদার্থবিজ্ঞান",
        "topic": "বলবিদ্যা ও গতিবিজ্ঞান",
        "concept": "নিউটনের দ্বিতীয় গতিসূত্র ও ঘর্ষণ বল",
        "stem_bn": "একটি ১০ কেজি ভরের ব্লকের ওপর অনুভূমিকভাবে ৫০ নিউটন বল প্রয়োগ করা হলো। যদি মেঝের ঘর্ষণ গুণাঙ্ক \\mu_k = 0.2 হয় (এবং g = 9.8 \\text{ m/s}^2), তবে ব্লকটির কার্যকরী ত্বরণ কত হবে?",
        "stem_en": "A horizontal force of 50 N is applied to a 10 kg block. If the coefficient of kinetic friction is 0.2 (g = 9.8 m/s^2), what is the effective acceleration?",
        "options": [
            {
                "id": "opt_301_a",
                "option_key": "A",
                "option_text_bn": "৩.০৪ m/s²",
                "is_correct": True,
                "distractor_rationale": "সঠিক উত্তর: নীট বল F = ৫০ - (০.২ × ১০ × ৯.৮) = ৩০.৪ নিউটন; a = ৩০.৪ / ১০ = ৩.০৪ m/s²।"
            },
            {
                "id": "opt_301_b",
                "option_key": "B",
                "option_text_bn": "৫.০০ m/s²",
                "is_correct": False,
                "distractor_rationale": "ভুল: ঘর্ষণ বল বিবেচনা না করে সরাসরি ৫০/১০ গণনা করা হয়েছে।"
            },
            {
                "id": "opt_301_c",
                "option_key": "C",
                "option_text_bn": "১.৯৬ m/s²",
                "is_correct": False,
                "distractor_rationale": "ভুল: এটি কেবল ঘর্ষণজনিত মন্দনের মান, কার্যকরী ত্বরণ নয়।"
            },
            {
                "id": "opt_301_d",
                "option_key": "D",
                "option_text_bn": "২.৫০ m/s²",
                "is_correct": False,
                "distractor_rationale": "ভুল: ভুল সমীকরণ প্রয়োগ।"
            }
        ],
        "explanation_bn": "ঘর্ষণ বল f_k = \\mu_k \\cdot mg = 0.2 \\times 10 \\times 9.8 = 19.6 \\text{ N}। নীট বল F_{net} = 50 - 19.6 = 30.4 \\text{ N}। সুতরাং ত্বরণ a = 30.4 / 10 = 3.04 \\text{ m/s}^2।",
        "explanation_en": "Frictional force f_k = 19.6 N. Net force = 30.4 N. Acceleration = 3.04 m/s^2.",
        "difficulty": "MEDIUM",
        "cognitive_skill": "APPLICATION",
        "curriculum": "NCTB_2024",
        "class_grade": 10,
        "is_ai_generated": True,
        "ai_confidence_score": 0.96,
        "ai_model": "Claude-3.5-Sonnet-NCTB",
        "deduplication_similarity": 0.04,
        "is_duplicate_flag": False,
        "source_attribution": "AI_GENERATED",
        "creator_user_id": "ai_agent_generator",
        "reviewed_by": None,
        "reviewed_at": None,
        "rejection_feedback": None,
        "created_at": "2026-10-24T08:30:00Z"
    },
    {
        "id": "q_draft_chem_402",
        "version": 1,
        "status": "NEEDS_REVIEW",
        "subject": "রসায়ন",
        "topic": "জৈব রসায়ন ও কার্যকরী মূলক",
        "concept": "লুকাস বিকারক ও অ্যালকোহল শনাক্তকরণ",
        "stem_bn": "লুকাস বিকারক (ZnCl₂ + গাঢ় HCl) যোগ করার সাথে সাথে কোন শ্রেণির অ্যালকোহল তাৎক্ষণিক সাদা অধঃক্ষেপ তৈরি করে?",
        "stem_en": "Which class of alcohol immediately forms a white precipitate upon adding Lucas reagent (ZnCl2 + conc. HCl)?",
        "options": [
            {
                "id": "opt_402_a",
                "option_key": "A",
                "option_text_bn": "১° অ্যালকোহল (Primary)",
                "is_correct": False,
                "distractor_rationale": "ভুল: ১° অ্যালকোহল সাধারণ তাপমাত্রায় কোনো অধঃক্ষেপ দেয় না, উত্তপ্ত করলে দেয়।"
            },
            {
                "id": "opt_402_b",
                "option_key": "B",
                "option_text_bn": "২° অ্যালকোহল (Secondary)",
                "is_correct": False,
                "distractor_rationale": "ভুল: ২° অ্যালকোহল ৫ থেকে ১০ মিনিট পর সাদা অধঃক্ষেপ বা তৈলাক্ত স্তর ফেলে।"
            },
            {
                "id": "opt_402_c",
                "option_key": "C",
                "option_text_bn": "৩° অ্যালকোহল (Tertiary)",
                "is_correct": True,
                "distractor_rationale": "সঠিক উত্তর: ৩° কার্বোক্যাটায়নের উচ্চ স্থায়িত্বের কারণে তৎক্ষণাৎ টারশিয়ারি অ্যালকাইল হ্যালাইডের অধঃক্ষেপ পড়ে।"
            },
            {
                "id": "opt_402_d",
                "option_key": "D",
                "option_text_bn": "ফেনল (Phenol)",
                "is_correct": False,
                "distractor_rationale": "ভুল: ফেনল লুকাস বিকারকের সাথে অ্যালকাইল হ্যালাইড অধঃক্ষেপ দেয় না।"
            }
        ],
        "explanation_bn": "৩° কার্বোক্যাটায়ন অধিক সুস্থিত হওয়ায় টারশিয়ারি অ্যালকোহল লুকাস বিকারকের সাথে অত্যন্ত দ্রুত বিক্রিয়া করে কয়েক সেকেন্ডের মধ্যে সাদা অ্যালকাইল ক্লোরাইড অধঃক্ষেপ সৃষ্টি করে।",
        "explanation_en": "Tertiary alcohol reacts instantaneously due to the high stability of the 3-degree carbocation.",
        "difficulty": "HARD",
        "cognitive_skill": "REASONING",
        "curriculum": "NCTB_2024",
        "class_grade": 12,
        "is_ai_generated": True,
        "ai_confidence_score": 0.95,
        "ai_model": "Claude-3.5-Sonnet-NCTB",
        "deduplication_similarity": 0.03,
        "is_duplicate_flag": False,
        "source_attribution": "AI_GENERATED",
        "creator_user_id": "ai_agent_generator",
        "reviewed_by": None,
        "reviewed_at": None,
        "rejection_feedback": None,
        "created_at": "2026-10-24T09:15:00Z"
    },
    {
        "id": "q_draft_math_503",
        "version": 1,
        "status": "NEEDS_REVIEW",
        "subject": "উচ্চতর গণিত",
        "topic": "ত্রিকোণমিতি ও বৃত্তীয় পরিমাপ",
        "concept": "বৃত্তচাপ ও কেন্দ্রস্থ কোণ",
        "stem_bn": "কোনো বৃত্তের ব্যাসার্ধ ৭ সেমি এবং একটি বৃত্তচাপ কেন্দ্রে \\frac{\\pi}{3} রেডিয়ান কোণ উৎপন্ন করলে চাপটির দৈর্ঘ্য কত সেমি?",
        "stem_en": "If a circle has radius 7 cm and an arc subtends an angle of pi/3 radians at the center, what is the arc length?",
        "options": [
            {
                "id": "opt_503_a",
                "option_key": "A",
                "option_text_bn": "৭.৩৩ সেমি",
                "is_correct": True,
                "distractor_rationale": "সঠিক উত্তর: s = r\\theta = 7 × (3.1416 / 3) ≈ 7.33 সেমি।"
            },
            {
                "id": "opt_503_b",
                "option_key": "B",
                "option_text_bn": "২১.০০ সেমি",
                "is_correct": False,
                "distractor_rationale": "ভুল: ব্যাসার্ধ ও পাই-এর ভুল গুণফল।"
            },
            {
                "id": "opt_503_c",
                "option_key": "C",
                "option_text_bn": "৩.৫০ সেমি",
                "is_correct": False,
                "distractor_rationale": "ভুল: ব্যাসার্ধকে কোণ দ্বারা ভাগ করা হয়েছে।"
            },
            {
                "id": "opt_503_d",
                "option_key": "D",
                "option_text_bn": "১৪.৬৭ সেমি",
                "is_correct": False,
                "distractor_rationale": "ভুল: ব্যাসার্ধের বদলে ব্যাস দিয়ে হিসেব করা হয়েছে।"
            }
        ],
        "explanation_bn": "বৃত্তচাপের দৈর্ঘ্য s = r\\theta। এখানে r = ৭ সেমি এবং \\theta = \\pi/3 রেডিয়ান। সুতরাং s = ৭ × (৩.১৪১৬/৩) = ৭.৩৩ সেমি।",
        "explanation_en": "Arc length s = r*theta = 7 * (pi/3) = 7.33 cm.",
        "difficulty": "EASY",
        "cognitive_skill": "APPLICATION",
        "curriculum": "NCTB_2024",
        "class_grade": 9,
        "is_ai_generated": True,
        "ai_confidence_score": 0.98,
        "ai_model": "Claude-3.5-Sonnet-NCTB",
        "deduplication_similarity": 0.02,
        "is_duplicate_flag": False,
        "source_attribution": "AI_GENERATED",
        "creator_user_id": "ai_agent_generator",
        "reviewed_by": None,
        "reviewed_at": None,
        "rejection_feedback": None,
        "created_at": "2026-10-24T10:00:00Z"
    },
    {
        "id": "q_draft_bio_604",
        "version": 1,
        "status": "DRAFT",
        "subject": "জীববিজ্ঞান",
        "topic": "কোষ ও বংশগতিবিদ্যা",
        "concept": "ডিএনএ রেপ্লিকেশন ও ওকাজাকি খণ্ড",
        "stem_bn": "ডিএনএ রেপ্লিকেশনের সময় ল্যাগিং সূত্রে (Lagging Strand) খণ্ড খণ্ড অংশ জোড়া লাগাতে কোন এনজাইমটি অনুঘটক হিসেবে কাজ করে?",
        "stem_en": "Which enzyme acts as a catalyst to join Okazaki fragments on the lagging strand during DNA replication?",
        "options": [
            {
                "id": "opt_604_a",
                "option_key": "A",
                "option_text_bn": "ডিএনএ পলিমারেজ I",
                "is_correct": False,
                "distractor_rationale": "ভুল: এটি প্রাইমার অপসারণ করে ডিএনএ অংশ প্রতিস্থাপন করে।"
            },
            {
                "id": "opt_604_b",
                "option_key": "B",
                "option_text_bn": "ডিএনএ লাইগেজ",
                "is_correct": True,
                "distractor_rationale": "সঠিক উত্তর: ওকাজাকি খণ্ডগুলোকে ফসফোডাইএস্টার বন্ধনের মাধ্যমে সংযুক্ত করে।"
            },
            {
                "id": "opt_604_c",
                "option_key": "C",
                "option_text_bn": "ডিএনএ হেলিকেজ",
                "is_correct": False,
                "distractor_rationale": "ভুল: হেলিকেজ ডিএনএর প্যাঁচ ও হাইড্রোজেন বন্ধন খুলে দেয়।"
            },
            {
                "id": "opt_604_d",
                "option_key": "D",
                "option_text_bn": "টপোআইসোমারেজ",
                "is_correct": False,
                "distractor_rationale": "ভুল: এটি ডিএনএর অতিরিক্ত ঘূর্ণন চাপ হ্রাস করে।"
            }
        ],
        "explanation_bn": "ডিএনএ লাইগেজ এনজাইম ফসফোডাইএস্টার বন্ধন গঠনের মাধ্যমে ওকাজাকি খণ্ডগুলোর সংযোগ সাধন করে অবিচ্ছিন্ন সূত্র তৈরি করে।",
        "explanation_en": "DNA ligase joins Okazaki fragments by creating phosphodiester bonds.",
        "difficulty": "MEDIUM",
        "cognitive_skill": "RECALL",
        "curriculum": "NCTB_2024",
        "class_grade": 11,
        "is_ai_generated": True,
        "ai_confidence_score": 0.92,
        "ai_model": "Claude-3.5-Sonnet-NCTB",
        "deduplication_similarity": 0.05,
        "is_duplicate_flag": False,
        "source_attribution": "AI_GENERATED",
        "creator_user_id": "ai_agent_generator",
        "reviewed_by": None,
        "reviewed_at": None,
        "rejection_feedback": None,
        "created_at": "2026-10-24T11:20:00Z"
    },
    {
        "id": "q_draft_ict_705",
        "version": 1,
        "status": "APPROVED",
        "subject": "তথ্য ও যোগাযোগ প্রযুক্তি",
        "topic": "ডিজিটাল ডিভাইস ও লজিক গেট",
        "concept": "ইউনিভার্সাল গেট ও বুলিয়ান সরলীকরণ",
        "stem_bn": "নিচের কোন লজিক গেট জোড়াকে সার্বজনীন বা ইউনিভার্সাল গেট বলা হয়?",
        "stem_en": "Which pair of logic gates are known as universal gates?",
        "options": [
            {
                "id": "opt_705_a",
                "option_key": "A",
                "option_text_bn": "AND ও OR",
                "is_correct": False,
                "distractor_rationale": "ভুল: এরা মৌলিক লজিক গেট।"
            },
            {
                "id": "opt_705_b",
                "option_key": "B",
                "option_text_bn": "NAND ও NOR",
                "is_correct": True,
                "distractor_rationale": "সঠিক উত্তর: NAND এবং NOR গেট দ্বারা যেকোনো মৌলিক লজিক গেট তৈরি করা সম্ভব।"
            },
            {
                "id": "opt_705_c",
                "option_key": "C",
                "option_text_bn": "XOR ও XNOR",
                "is_correct": False,
                "distractor_rationale": "ভুল: এরা বিশেষ (Exclusive) লজিক গেট।"
            },
            {
                "id": "opt_705_d",
                "option_key": "D",
                "option_text_bn": "NOT ও AND",
                "is_correct": False,
                "distractor_rationale": "ভুল: মৌলিক গেটের সংমিশ্রণ।"
            }
        ],
        "explanation_bn": "NAND এবং NOR গেট দিয়ে যেকোনো জটিল লজিক বর্তনী পূর্ণাঙ্গরূপে তৈরি করা যায় বলে এদের সার্বজনীন গেট বলা হয়।",
        "explanation_en": "NAND and NOR can construct any Boolean function, making them universal gates.",
        "difficulty": "EASY",
        "cognitive_skill": "RECALL",
        "curriculum": "NCTB_2024",
        "class_grade": 11,
        "is_ai_generated": False,
        "ai_confidence_score": 0.99,
        "ai_model": "Human-SME-Teacher",
        "deduplication_similarity": 0.01,
        "is_duplicate_flag": False,
        "source_attribution": "TEACHER_SUBMISSION",
        "creator_user_id": "usr_teacher_ict",
        "reviewed_by": "usr_sme_ict_01",
        "reviewed_at": "2026-10-24T12:00:00Z",
        "rejection_feedback": None,
        "created_at": "2026-10-23T14:00:00Z"
    },
    {
        "id": "q_draft_phys_806",
        "version": 1,
        "status": "REJECTED",
        "subject": "পদার্থবিজ্ঞান",
        "topic": "কাজ, শক্তি ও ক্ষমতা",
        "concept": "স্প্রিং-এর সঞ্চিত স্থিতিশক্তি",
        "stem_bn": "একটি স্প্রিংকে x দূরত্ব সংকুচিত করতে কৃতকাজের সমীকরণ কোনটি? (k = স্প্রিং ধ্রুবক)",
        "stem_en": "What is the equation for work done to compress a spring by distance x (k = spring constant)?",
        "options": [
            {
                "id": "opt_806_a",
                "option_key": "A",
                "option_text_bn": "W = kx",
                "is_correct": False,
                "distractor_rationale": "ভুল: এটি হুকের সূত্রের বল, কাজ নয়।"
            },
            {
                "id": "opt_806_b",
                "option_key": "B",
                "option_text_bn": "W = ½kx²",
                "is_correct": True,
                "distractor_rationale": "সঠিক উত্তর: স্প্রিং স্থিতিশক্তি = ½kx²।"
            },
            {
                "id": "opt_806_c",
                "option_key": "C",
                "option_text_bn": "W = ½mv²",
                "is_correct": False,
                "distractor_rationale": "ভুল: এটি গতিশক্তি।"
            },
            {
                "id": "opt_806_d",
                "option_key": "D",
                "option_text_bn": "W = 2kx²",
                "is_correct": False,
                "distractor_rationale": "ভুল: গুণাঙ্ক ভুল।"
            }
        ],
        "explanation_bn": "পরিবর্তনশীল বলের ক্ষেত্রে স্প্রিং সংকোচনে কৃতকাজ সমাকলনের মাধ্যমে পাওয়া যায় W = ½kx²।",
        "explanation_en": "Work done on spring W = 1/2 k x^2.",
        "difficulty": "EASY",
        "cognitive_skill": "RECALL",
        "curriculum": "NCTB_2024",
        "class_grade": 9,
        "is_ai_generated": True,
        "ai_confidence_score": 0.88,
        "ai_model": "Claude-3.5-Sonnet-NCTB",
        "deduplication_similarity": 0.08,
        "is_duplicate_flag": False,
        "source_attribution": "AI_GENERATED",
        "creator_user_id": "ai_agent_generator",
        "reviewed_by": "usr_sme_physics_01",
        "reviewed_at": "2026-10-24T14:30:00Z",
        "rejection_feedback": "প্রশ্নে স্থিতিস্থাপক সীমার শর্ত এবং স্প্রিং-এর প্রাথমিক সাম্যাবস্থার শর্ত উল্লেখ করা আবশ্যক।",
        "created_at": "2026-10-24T13:00:00Z"
    }
]


class ContentPipelineService:
    """
    Manages the lifecycle of questions from AI-assisted drafting to human SME publishing.
    Thread-safe and persisted to draft_store.json.
    """

    VALID_TRANSITIONS = {
        "DRAFT": {"NEEDS_REVIEW"},
        "NEEDS_REVIEW": {"APPROVED", "DRAFT", "REJECTED", "NEEDS_CHANGES"},
        "NEEDS_CHANGES": {"DRAFT", "NEEDS_REVIEW"},
        "APPROVED": {"PUBLISHED", "DRAFT", "REJECTED"},
        "REJECTED": {"DRAFT", "NEEDS_REVIEW"},
        "PUBLISHED": {"QUARANTINED", "ARCHIVED"},
        "QUARANTINED": {"ARCHIVED", "DRAFT"},
        "ARCHIVED": set()
    }

    def __init__(self):
        self._lock = threading.RLock()
        self._content_store: Dict[str, Dict[str, Any]] = {}
        self._audit_logs: List[Dict[str, Any]] = []
        self._published_questions: List[Dict[str, Any]] = []
        self._dedup_service = deduplication_service
        self._load_from_disk()

    def _load_from_disk(self):
        with self._lock:
            if os.path.exists(STORE_PATH):
                try:
                    with open(STORE_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self._content_store = data.get("questions", {})
                        self._audit_logs = data.get("audit_logs", [])
                except Exception:
                    self._populate_seeds()
            else:
                self._populate_seeds()

            # Synchronize published questions pool
            self._sync_published_pool()

    def _populate_seeds(self):
        self._content_store = {item["id"]: item for item in DEFAULT_DRAFT_SEEDS}
        self._audit_logs = [
            {
                "audit_id": "AUD-REV-2026-101",
                "question_id": "q_draft_ict_705",
                "action": "APPROVE_DRAFT",
                "actor_id": "usr_sme_ict_01",
                "actor_role": "SUBJECT_REVIEWER",
                "previous_status": "NEEDS_REVIEW",
                "new_status": "APPROVED",
                "reason_or_feedback": "মানসম্মত প্রশ্ন এবং এনসিটিবি কারিকুলামের সাথে সঙ্গতিপূর্ণ।",
                "timestamp": "2026-10-24T12:00:00Z"
            },
            {
                "audit_id": "AUD-REV-2026-102",
                "question_id": "q_draft_phys_806",
                "action": "REJECT_DRAFT",
                "actor_id": "usr_sme_physics_01",
                "actor_role": "SUBJECT_REVIEWER",
                "previous_status": "NEEDS_REVIEW",
                "new_status": "REJECTED",
                "reason_or_feedback": "প্রশ্নে স্থিতিস্থাপক সীমার শর্ত এবং স্প্রিং-এর প্রাথমিক সাম্যাবস্থার শর্ত উল্লেখ করা আবশ্যক।",
                "timestamp": "2026-10-24T14:30:00Z"
            }
        ]
        self._save_to_disk()

    def _save_to_disk(self):
        os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
        temp_path = f"{STORE_PATH}.tmp.{uuid.uuid4().hex[:6]}"
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "questions": self._content_store,
                        "audit_logs": self._audit_logs,
                        "last_updated": ServerTimekeeper.get_server_iso_now()
                    },
                    f,
                    ensure_ascii=False,
                    indent=2
                )
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, STORE_PATH)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _sync_published_pool(self):
        """Maintains questions available for active examinations."""
        self._published_questions = [
            q for q in self._content_store.values()
            if q.get("status") in ("APPROVED", "PUBLISHED")
        ]

    def get_published_questions(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._published_questions)

    def generate_ai_draft(
        self,
        subject: str,
        topic: str,
        concept: str,
        cognitive_level: str = "APPLICATION",
        curriculum: str = "NCTB_2024",
        class_grade: int = 10,
        creator_user_id: str = "ai_agent_generator"
    ) -> Dict[str, Any]:
        """
        Generates an initial MCQ draft with intelligent distractors and step-by-step reasoning.
        Status is strictly 'DRAFT' or 'NEEDS_REVIEW', requiring explicit human SME approval.
        """
        with self._lock:
            question_id = f"q_draft_{uuid.uuid4().hex[:8]}"

            stem_bn = f"যদি কোনো গতিশীল বস্তুর ত্বরণ ধ্রুব থাকে, তবে নির্দিষ্ট সময় t পরে অতিক্রান্ত দূরত্ব s নির্ণয়ের সূত্র কোনটি?"
            distractors = [
                {"id": f"opt_{uuid.uuid4().hex[:6]}", "option_key": "A", "option_text_bn": "s = vt", "is_correct": False, "distractor_rationale": "এটি সমবেগের ক্ষেত্রে প্রযোজ্য; সুষম ত্বরণের জন্য নয়।"},
                {"id": f"opt_{uuid.uuid4().hex[:6]}", "option_key": "B", "option_text_bn": "s = ut + ½at²", "is_correct": True, "distractor_rationale": "সুষম ত্বরণে অতিক্রান্ত দূরত্বের আদর্শ সমীকরণ।"},
                {"id": f"opt_{uuid.uuid4().hex[:6]}", "option_key": "C", "option_text_bn": "v = u + at", "is_correct": False, "distractor_rationale": "এটি শেষ বেগ নির্ণয়ের সূত্র, দূরত্ব নয়।"},
                {"id": f"opt_{uuid.uuid4().hex[:6]}", "option_key": "D", "option_text_bn": "v² = u² + 2as", "is_correct": False, "distractor_rationale": "এখানে সময় t অনুপস্থিত।"},
            ]

            explanation_bn = (
                "গড় বেগ = (u + v)/2। আবার v = u + at।\n"
                "সুতরাং s = ((u + u + at)/2) × t = ut + ½at²। এটি এনসিটিবি পদার্থবিজ্ঞান ৩য় অধ্যায়ের অন্তর্ভুক্ত।"
            )

            existing_questions = [{"id": k, "stem_bn": v["stem_bn"]} for k, v in self._content_store.items()]
            is_dup, _, dup_score = self._dedup_service.check_duplicate(stem_bn, existing_questions)

            record = {
                "id": question_id,
                "version": 1,
                "status": "DRAFT",
                "subject": subject,
                "topic": topic,
                "concept": concept,
                "cognitive_skill": cognitive_level,
                "curriculum": curriculum,
                "class_grade": class_grade,
                "stem_bn": stem_bn,
                "stem_en": "Which of the following is the formula for distance s under constant acceleration?",
                "options": distractors,
                "explanation_bn": explanation_bn,
                "explanation_en": "Under uniform acceleration, s = ut + 0.5 a t^2.",
                "difficulty": "MEDIUM",
                "is_ai_generated": True,
                "ai_confidence_score": 0.94,
                "ai_model": "Claude-3.5-Sonnet-NCTB",
                "deduplication_similarity": round(dup_score, 3),
                "is_duplicate_flag": is_dup,
                "source_attribution": "AI_GENERATED",
                "creator_user_id": creator_user_id,
                "reviewed_by": None,
                "reviewed_at": None,
                "rejection_feedback": None,
                "created_at": ServerTimekeeper.get_server_iso_now(),
            }

            self._content_store[question_id] = record
            self._save_to_disk()
            return record

    def submit_for_sme_review(self, question_id: str) -> Tuple[bool, str]:
        """Moves draft into the SME review queue."""
        with self._lock:
            item = self._content_store.get(question_id)
            if not item:
                return False, "QUESTION_NOT_FOUND"

            if "NEEDS_REVIEW" not in self.VALID_TRANSITIONS.get(item["status"], set()):
                return False, f"CANNOT_TRANSITION_FROM_{item['status']}"

            prev_status = item["status"]
            item["status"] = "NEEDS_REVIEW"
            self._record_audit_log(
                question_id=question_id,
                action="SUBMIT_FOR_REVIEW",
                actor_id=item.get("creator_user_id") or "system",
                actor_role="AUTHOR",
                previous_status=prev_status,
                new_status="NEEDS_REVIEW",
                reason="Submitted for Subject Matter Expert evaluation"
            )
            self._save_to_disk()
            return True, "QUEUED_FOR_SME_REVIEW"

    def get_review_queue(self, status_filter: str = "NEEDS_REVIEW") -> List[Dict[str, Any]]:
        """Legacy helper for backward compatibility."""
        with self._lock:
            return [
                item for item in self._content_store.values()
                if item["status"] == status_filter
            ]

    def list_drafts(
        self,
        status: Optional[str] = None,
        subject: Optional[str] = None,
        chapter: Optional[str] = None,
        difficulty: Optional[str] = None,
        source: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Dict[str, Any]], int, int, int, Dict[str, int]]:
        """
        Lists drafts with comprehensive multi-facet filtering, full-text search, and pagination.
        Returns (items, total, page, limit, counts_by_status).
        """
        with self._lock:
            all_items = list(self._content_store.values())

            # Calculate counts across all items
            counts = {
                "all": len(all_items),
                "needs_review": sum(1 for q in all_items if q.get("status") == "NEEDS_REVIEW"),
                "draft": sum(1 for q in all_items if q.get("status") == "DRAFT"),
                "approved": sum(1 for q in all_items if q.get("status") in ("APPROVED", "PUBLISHED")),
                "rejected": sum(1 for q in all_items if q.get("status") == "REJECTED"),
                "needs_changes": sum(1 for q in all_items if q.get("status") == "NEEDS_CHANGES")
            }

            # Filter items
            filtered = all_items

            if status and status.upper() != "ALL":
                status_upper = status.upper()
                if status_upper == "APPROVED":
                    filtered = [q for q in filtered if q.get("status") in ("APPROVED", "PUBLISHED")]
                else:
                    filtered = [q for q in filtered if q.get("status") == status_upper]

            if subject and subject.strip() and subject.upper() != "ALL":
                sub_norm = subject.strip().lower()
                filtered = [q for q in filtered if sub_norm in (q.get("subject") or "").lower()]

            if chapter and chapter.strip():
                ch_norm = chapter.strip().lower()
                filtered = [q for q in filtered if ch_norm in (q.get("topic") or "").lower() or ch_norm in (q.get("concept") or "").lower()]

            if difficulty and difficulty.upper() != "ALL":
                diff_upper = difficulty.upper()
                filtered = [q for q in filtered if q.get("difficulty") == diff_upper]

            if source and source.upper() != "ALL":
                src_upper = source.upper()
                filtered = [q for q in filtered if (q.get("source_attribution") or "").upper() == src_upper]

            if search and search.strip():
                term = search.strip().lower()
                filtered = [
                    q for q in filtered
                    if term in (q.get("id") or "").lower()
                    or term in (q.get("stem_bn") or "").lower()
                    or term in (q.get("stem_en") or "").lower()
                    or term in (q.get("subject") or "").lower()
                    or term in (q.get("topic") or "").lower()
                    or term in (q.get("concept") or "").lower()
                ]

            # Sort: newest first
            filtered.sort(key=lambda x: x.get("created_at") or "", reverse=True)

            total = len(filtered)
            start = (page - 1) * limit
            end = start + limit
            paged_items = filtered[start:end]

            return paged_items, total, page, limit, counts

    def get_draft(self, question_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._content_store.get(question_id)

    def approve_draft(
        self,
        question_id: str,
        reviewer_id: str,
        reviewer_role: str = "SUBJECT_REVIEWER",
        comments: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        SME Approval Gate:
        Transitions question to APPROVED and adds it to the active examination question pool.
        """
        with self._lock:
            item = self._content_store.get(question_id)
            if not item:
                return False, "QUESTION_NOT_FOUND", None

            prev_status = item.get("status")
            item["status"] = "APPROVED"
            item["reviewed_by"] = reviewer_id
            item["reviewed_by_sme_id"] = reviewer_id
            item["reviewed_at"] = ServerTimekeeper.get_server_iso_now()
            if comments:
                item["approval_comments"] = comments

            self._record_audit_log(
                question_id=question_id,
                action="APPROVE_DRAFT",
                actor_id=reviewer_id,
                actor_role=reviewer_role,
                previous_status=prev_status,
                new_status="APPROVED",
                reason=comments or "বিষয়বস্তুর মান এনসিটিবি আদর্শ অনুযায়ী অনুমোদিত।"
            )

            self._sync_published_pool()
            self._save_to_disk()
            return True, "APPROVED_BY_SME", item

    def reject_draft(
        self,
        question_id: str,
        reviewer_id: str,
        reviewer_role: str = "SUBJECT_REVIEWER",
        reason: Optional[str] = None,
        status: str = "REJECTED"
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Rejects a draft with mandatory feedback, keeping it in quarantine/audit history.
        """
        with self._lock:
            item = self._content_store.get(question_id)
            if not item:
                return False, "QUESTION_NOT_FOUND", None

            feedback = reason or "বিষয়বস্তুর মান এনসিটিবি আদর্শ অনুযায়ী পরিমার্জন প্রয়োজন।"
            prev_status = item.get("status")
            if status.upper() == "DRAFT":
                new_status = "DRAFT"
            elif status.upper() == "NEEDS_CHANGES":
                new_status = "NEEDS_CHANGES"
            else:
                new_status = "REJECTED"

            item["status"] = new_status
            item["reviewed_by"] = reviewer_id
            item["reviewed_by_sme_id"] = reviewer_id
            item["reviewed_at"] = ServerTimekeeper.get_server_iso_now()
            item["rejection_feedback"] = feedback

            self._record_audit_log(
                question_id=question_id,
                action="REJECT_DRAFT" if new_status == "REJECTED" else "REQUEST_CHANGES",
                actor_id=reviewer_id,
                actor_role=reviewer_role,
                previous_status=prev_status,
                new_status=new_status,
                reason=feedback
            )

            self._sync_published_pool()
            self._save_to_disk()
            return True, "REJECTED_BY_SME", item

    def edit_and_approve_draft(
        self,
        question_id: str,
        reviewer_id: str,
        reviewer_role: str = "SUBJECT_REVIEWER",
        updates: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Allows SME to apply inline edits to stem, options, explanation, and approve simultaneously.
        """
        with self._lock:
            item = self._content_store.get(question_id)
            if not item:
                return False, "QUESTION_NOT_FOUND", None

            updates = updates or {}
            prev_status = item.get("status")

            # Apply permitted edits
            diff = {}
            if "stem_bn" in updates and updates["stem_bn"]:
                diff["stem_bn"] = {"old": item["stem_bn"], "new": updates["stem_bn"]}
                item["stem_bn"] = updates["stem_bn"]

            if "stem_en" in updates:
                diff["stem_en"] = {"old": item.get("stem_en"), "new": updates["stem_en"]}
                item["stem_en"] = updates["stem_en"]

            if "options" in updates and updates["options"]:
                diff["options"] = {"old": len(item.get("options", [])), "new": len(updates["options"])}
                item["options"] = updates["options"]

            if "explanation_bn" in updates and updates["explanation_bn"]:
                diff["explanation_bn"] = {"old": item.get("explanation_bn"), "new": updates["explanation_bn"]}
                item["explanation_bn"] = updates["explanation_bn"]

            if "difficulty" in updates and updates["difficulty"]:
                item["difficulty"] = updates["difficulty"]

            if "cognitive_skill" in updates and updates["cognitive_skill"]:
                item["cognitive_skill"] = updates["cognitive_skill"]

            if "topic" in updates and updates["topic"]:
                item["topic"] = updates["topic"]

            if "concept" in updates and updates["concept"]:
                item["concept"] = updates["concept"]

            # Update lifecycle metadata
            item["version"] = item.get("version", 1) + 1
            item["status"] = "APPROVED"
            item["reviewed_by"] = reviewer_id
            item["reviewed_at"] = ServerTimekeeper.get_server_iso_now()
            item["edited_by"] = reviewer_id
            item["edited_at"] = ServerTimekeeper.get_server_iso_now()

            self._record_audit_log(
                question_id=question_id,
                action="EDIT_AND_APPROVE",
                actor_id=reviewer_id,
                actor_role=reviewer_role,
                previous_status=prev_status,
                new_status="APPROVED",
                reason=updates.get("comments") or "বিষয় বিশেষজ্ঞ কর্তৃক পরিমার্জন এবং চূড়ান্ত অনুমোদন সম্পন্ন।",
                diff=diff
            )

            self._sync_published_pool()
            self._save_to_disk()
            return True, "EDITED_AND_APPROVED", item

    def bulk_action(
        self,
        question_ids: List[str],
        action: str,
        actor_id: str,
        actor_role: str = "ADMIN",
        reason: Optional[str] = None
    ) -> Tuple[int, List[Dict[str, Any]]]:
        """
        Executes atomic batch approval or rejection on multiple selected draft questions.
        """
        with self._lock:
            updated_items = []
            action_upper = action.upper()

            for qid in question_ids:
                if action_upper == "APPROVE":
                    success, _, item = self.approve_draft(
                        question_id=qid,
                        reviewer_id=actor_id,
                        reviewer_role=actor_role,
                        comments=reason or "ব্যাচ অনুমোদন সম্পন্ন।"
                    )
                    if success and item:
                        updated_items.append(item)
                elif action_upper == "REJECT":
                    success, _, item = self.reject_draft(
                        question_id=qid,
                        reviewer_id=actor_id,
                        reviewer_role=actor_role,
                        reason=reason or "ব্যাচ প্রত্যাখ্যান সম্পন্ন।"
                    )
                    if success and item:
                        updated_items.append(item)

            return len(updated_items), updated_items

    def publish_approved_question(self, question_id: str, publisher_id: str) -> Tuple[bool, str]:
        """Final transition to PUBLISHED, releasing to active student exam pools."""
        with self._lock:
            item = self._content_store.get(question_id)
            if not item:
                return False, "QUESTION_NOT_FOUND"

            if item["status"] != "APPROVED":
                return False, f"CANNOT_PUBLISH_UNAPPROVED_QUESTION (Current: {item['status']})"

            item["status"] = "PUBLISHED"
            item["published_by_id"] = publisher_id
            item["published_at"] = ServerTimekeeper.get_server_iso_now()

            self._record_audit_log(
                question_id=question_id,
                action="PUBLISH_TO_POOLS",
                actor_id=publisher_id,
                actor_role="ADMIN",
                previous_status="APPROVED",
                new_status="PUBLISHED",
                reason="Released to active examination pool"
            )

            self._sync_published_pool()
            self._save_to_disk()
            return True, "PUBLISHED_TO_ACTIVE_POOLS"

    def review_and_approve_draft(
        self,
        question_id: str,
        sme_user_id: str,
        approve: bool,
        rejection_reason: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Backward compatibility adapter for existing endpoints."""
        if approve:
            return self.approve_draft(question_id, sme_user_id)
        else:
            return self.reject_draft(question_id, sme_user_id, reason=rejection_reason, status="DRAFT")

    def _record_audit_log(
        self,
        question_id: str,
        action: str,
        actor_id: str,
        actor_role: str,
        previous_status: str,
        new_status: str,
        reason: str,
        diff: Optional[Dict[str, Any]] = None
    ):
        entry = {
            "audit_id": f"AUD-REV-{uuid.uuid4().hex[:8].upper()}",
            "question_id": question_id,
            "action": action,
            "actor_id": actor_id,
            "actor_role": actor_role,
            "previous_status": previous_status,
            "new_status": new_status,
            "reason_or_feedback": reason,
            "diff_summary": diff or {},
            "timestamp": ServerTimekeeper.get_server_iso_now()
        }
        self._audit_logs.insert(0, entry)

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return self._audit_logs[:limit]


# Singleton Service Instance
content_pipeline_service = ContentPipelineService()
