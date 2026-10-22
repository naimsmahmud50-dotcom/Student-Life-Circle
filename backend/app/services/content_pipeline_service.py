"""
========================================================================================
MODULE:    AI-Assisted Question Pipeline & Human-in-the-Loop SME Review Service
TOPIC:     Distractor Generation, Deduplication Check & Content Approval State Machine
FILE:      backend/app/services/content_pipeline_service.py
PURPOSE:   Orchestrates AI-assisted question draft generation and enforces the strict
           human Subject Matter Expert (SME) approval gate. Strictly prohibits AI
           from publishing questions directly into active exam pools. State transitions:
           DRAFT -> NEEDS_REVIEW -> APPROVED -> PUBLISHED.
AUDIENCE:  Content Engineers, Subject Matter Reviewers & AI Agents
STANDARDS: FR-004 AI Quality Gate, Zero-Unreviewed-AI Policy, OWASP ASVS L2
========================================================================================
"""

import uuid
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone
from backend.app.core.timekeeper import ServerTimekeeper
from backend.app.services.deduplication import QuestionDeduplicationService, deduplication_service


class ContentPipelineService:
    """
    Manages the lifecycle of questions from AI-assisted drafting to human SME publishing.
    """

    VALID_TRANSITIONS = {
        "DRAFT": {"NEEDS_REVIEW"},
        "NEEDS_REVIEW": {"APPROVED", "DRAFT"},  # SME can approve or reject back to draft
        "APPROVED": {"PUBLISHED", "DRAFT"},    # Publisher can release or revoke
        "PUBLISHED": {"QUARANTINED", "ARCHIVED"},
        "QUARANTINED": {"ARCHIVED", "DRAFT"},
        "ARCHIVED": set()
    }

    def __init__(self):
        self._content_store: Dict[str, Dict[str, Any]] = {}
        self._dedup_service = deduplication_service

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
        Status is ALWAYS 'DRAFT', requiring explicit human SME approval.
        """
        question_id = f"q_draft_{uuid.uuid4().hex[:8]}"

        # Sample AI-generated question structure aligned with NCTB
        stem_bn = f"যদি কোনো গতিশীল বস্তুর ত্বরণ ধ্রুব থাকে, তবে নির্দিষ্ট সময় t পরে অতিক্রান্ত দূরত্ব s নির্ণয়ের সূত্র কোনটি?"
        correct_option_text = "s = ut + ½at²"
        distractors = [
            {"option_key": "A", "option_text_bn": "s = vt", "is_correct": False, "distractor_rationale": "এটি সমবেগের ক্ষেত্রে প্রযোজ্য; সুষম ত্বরণের জন্য নয়।"},
            {"option_key": "B", "option_text_bn": "s = ut + ½at²", "is_correct": True, "distractor_rationale": "সুষম ত্বরণে অতিক্রান্ত দূরত্বের আদর্শ সমীকরণ।"},
            {"option_key": "C", "option_text_bn": "v = u + at", "is_correct": False, "distractor_rationale": "এটি শেষ বেগ নির্ণয়ের সূত্র, দূরত্ব নয়।"},
            {"option_key": "D", "option_text_bn": "v² = u² + 2as", "is_correct": False, "distractor_rationale": "এখানে সময় t অনুপস্থিত।"},
        ]

        explanation_bn = (
            "গড় বেগ = (u + v)/2। আবার v = u + at।\n"
            "সুতরাং s = ((u + u + at)/2) × t = ut + ½at²। এটি এনসিটিবি পদার্থবিজ্ঞান ৩য় অধ্যায়ের অন্তর্ভুক্ত।"
        )

        # Triple-layer deduplication check before queuing
        existing_questions = [{"id": k, "stem_bn": v["stem_bn"]} for k, v in self._content_store.items()]
        is_dup, _, dup_score = self._dedup_service.check_duplicate(stem_bn, existing_questions)

        record = {
            "id": question_id,
            "version": 1,
            "status": "DRAFT",
            "subject": subject,
            "topic": topic,
            "concept": concept,
            "cognitive_level": cognitive_level,
            "curriculum": curriculum,
            "class_grade": class_grade,
            "stem_bn": stem_bn,
            "options": distractors,
            "explanation_bn": explanation_bn,
            "is_ai_generated": True,
            "ai_confidence_score": 0.94,
            "deduplication_similarity": round(dup_score, 3),
            "is_duplicate_flag": is_dup,
            "creator_user_id": creator_user_id,
            "reviewed_by_sme_id": None,
            "reviewed_at": None,
            "published_at": None,
            "created_at": ServerTimekeeper.get_server_iso_now(),
        }

        self._content_store[question_id] = record
        return record

    def submit_for_sme_review(self, question_id: str) -> Tuple[bool, str]:
        """Moves draft into the SME review queue."""
        item = self._content_store.get(question_id)
        if not item:
            return False, "QUESTION_NOT_FOUND"

        if "NEEDS_REVIEW" not in self.VALID_TRANSITIONS.get(item["status"], set()):
            return False, f"CANNOT_TRANSITION_FROM_{item['status']}"

        item["status"] = "NEEDS_REVIEW"
        return True, "QUEUED_FOR_SME_REVIEW"

    def get_review_queue(self, status_filter: str = "NEEDS_REVIEW") -> List[Dict[str, Any]]:
        """Lists items waiting for human Subject Matter Expert (SME) evaluation."""
        return [
            item for item in self._content_store.values()
            if item["status"] == status_filter
        ]

    def review_and_approve_draft(
        self,
        question_id: str,
        sme_user_id: str,
        approve: bool,
        rejection_reason: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Human Subject Matter Expert gate:
        - If approve=True: Status becomes 'APPROVED' (ready to publish).
        - If approve=False: Status returns to 'DRAFT' with feedback.
        """
        item = self._content_store.get(question_id)
        if not item:
            return False, "QUESTION_NOT_FOUND", None

        if item["status"] != "NEEDS_REVIEW":
            return False, f"QUESTION_NOT_IN_REVIEW_QUEUE (Current: {item['status']})", None

        if approve:
            item["status"] = "APPROVED"
            item["reviewed_by_sme_id"] = sme_user_id
            item["reviewed_at"] = ServerTimekeeper.get_server_iso_now()
            return True, "APPROVED_BY_SME", item
        else:
            item["status"] = "DRAFT"
            item["rejection_feedback"] = rejection_reason or "বিষয়বস্তুর মান এনসিটিবি আদর্শ অনুযায়ী পরিমার্জন প্রয়োজন।"
            return True, "REJECTED_BACK_TO_DRAFT", item

    def publish_approved_question(self, question_id: str, publisher_id: str) -> Tuple[bool, str]:
        """Final transition to PUBLISHED, making it available to student exams."""
        item = self._content_store.get(question_id)
        if not item:
            return False, "QUESTION_NOT_FOUND"

        if item["status"] != "APPROVED":
            return False, f"CANNOT_PUBLISH_UNAPPROVED_QUESTION (Current: {item['status']})"

        item["status"] = "PUBLISHED"
        item["published_by_id"] = publisher_id
        item["published_at"] = ServerTimekeeper.get_server_iso_now()
        return True, "PUBLISHED_TO_ACTIVE_POOLS"

    def list_drafts(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all items in content store with optional status filtering."""
        if status:
            return [item for item in self._content_store.values() if item.get("status") == status]
        return list(self._content_store.values())


# Singleton Service Instance
content_pipeline_service = ContentPipelineService()
