"""
========================================================================================
MODULE:    PWA Offline Sync & Network Resilience Cache Engine
TOPIC:     Offline Queue Processing, Idempotent Batch Sync & Low-Bandwidth Bundles
FILE:      backend/app/services/offline_sync_service.py
PURPOSE:   Enforces NFR-002 offline-first resilience for Bangladeshi students in
           intermittent 2G/3G connectivity environments:
           1. Offline Practice Bundle Builder: Packages lightweight question payloads
              with offline deterministic evaluation metadata.
           2. Batch Offline Replay Queue: Ingests buffered answer payloads accumulated
              during connection dropouts and processes them idempotently without loss.
AUDIENCE:  Mobile PWA Engineers, Offline Sync Specialists & AI Agents
STANDARDS: PWA Offline-First, RFC 7240 Prefer-Async, Zero-Emoji Spec
========================================================================================
"""

import hashlib
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timezone
from backend.app.core.timekeeper import ServerTimekeeper
from backend.app.services.quiz_engine import quiz_engine
from backend.app.db.seed_data import ACADEMIC_QUESTION_SEEDS


class OfflineSyncService:
    """
    Orchestrates offline practice bundle generation and batch sync replay reconciliation.
    """

    def __init__(self):
        self._synced_batches: Dict[str, Dict[str, Any]] = {}
        self._total_answers_synced: int = 0
        self._total_batches_processed: int = 0

    def generate_offline_bundle(
        self,
        class_grade: int = 8,
        subject: str = "গণিত",
        bundle_size: int = 10
    ) -> Dict[str, Any]:
        """
        Creates a lightweight, self-contained JSON bundle for offline PWA storage.
        Allows learners in remote areas to practice without continuous cellular connection.
        """
        # Filter matching questions from verified seed repository
        matching_questions = [
            q for q in ACADEMIC_QUESTION_SEEDS
            if q.get("class_grade") == class_grade or not q.get("class_grade")
        ][:bundle_size]

        sanitized_items = []
        for q in matching_questions:
            sanitized_items.append({
                "question_id": q["id"],
                "stem_bn": q["stem_bn"],
                "options": [
                    {
                        "option_id": opt["id"],
                        "option_key": opt["option_key"],
                        "text_bn": opt["option_text_bn"]
                    }
                    for opt in q["options"]
                ],
                "explanation_bn": q.get("explanation_bn", "বিশ্লেষণ উপলব্ধ রয়েছে।"),
                "cognitive_skill": q.get("cognitive_skill", "APPLICATION")
            })

        bundle_id = f"bundle_g{class_grade}_{hashlib.sha256(f'{subject}:{len(sanitized_items)}'.encode()).hexdigest()[:8]}"

        return {
            "bundle_id": bundle_id,
            "class_grade": class_grade,
            "subject": subject,
            "generated_at": ServerTimekeeper.get_server_iso_now(),
            "total_items": len(sanitized_items),
            "offline_storage_policy": "PWA_INDEXED_DB",
            "offline_version": "2.0.0",
            "questions": sanitized_items
        }

    def process_offline_sync_batch(
        self,
        student_id: str,
        attempt_id: str,
        buffered_answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Processes buffered answer saves queued in IndexedDB while learner was offline.
        Executes idempotent replay: duplicate retries are safely deduplicated.
        """
        batch_id = f"sync_batch_{len(self._synced_batches) + 1}"
        results = []
        synced_count = 0
        skipped_count = 0

        for raw_item in buffered_answers:
            if hasattr(raw_item, "model_dump"):
                item = raw_item.model_dump()
            elif isinstance(raw_item, dict):
                item = raw_item
            else:
                item = getattr(raw_item, "__dict__", {})

            qid = item.get("question_version_id")
            opt_id = item.get("selected_option_id")
            idem_key = item.get("idempotency_key")
            time_spent = item.get("time_taken_seconds", 0.0)

            if not qid or not idem_key:
                results.append({
                    "question_version_id": qid,
                    "status": "REJECTED_MISSING_FIELDS",
                    "reason": "Missing question_version_id or idempotency_key"
                })
                continue

            success, resp, reason = quiz_engine.save_answer_idempotent(
                attempt_id=attempt_id,
                user_id=student_id,
                question_version_id=qid,
                selected_option_id=opt_id,
                idempotency_key=idem_key,
                time_taken_seconds=time_spent
            )

            if success:
                if reason == "IDEMPOTENT_REPLAY":
                    skipped_count += 1
                    status_label = "DUPLICATE_IDEMPOTENT_SKIPPED"
                else:
                    synced_count += 1
                    status_label = "SYNCED_SAVED"

                results.append({
                    "question_version_id": qid,
                    "status": status_label,
                    "idempotency_key": idem_key,
                    "saved_at": resp.saved_at if resp else ServerTimekeeper.get_server_iso_now()
                })
            else:
                results.append({
                    "question_version_id": qid,
                    "status": "SYNC_FAILED",
                    "reason": reason
                })

        batch_record = {
            "batch_id": batch_id,
            "student_id": student_id,
            "attempt_id": attempt_id,
            "total_submitted": len(buffered_answers),
            "synced_count": synced_count,
            "skipped_count": skipped_count,
            "failed_count": len(buffered_answers) - (synced_count + skipped_count),
            "processed_at": ServerTimekeeper.get_server_iso_now(),
            "results": results
        }

        self._synced_batches[batch_id] = batch_record
        self._total_batches_processed += 1
        self._total_answers_synced += synced_count

        return batch_record

    def get_sync_metrics(self) -> Dict[str, Any]:
        """Returns statistics on offline PWA sync operations."""
        return {
            "total_batches_processed": self._total_batches_processed,
            "total_answers_synced": self._total_answers_synced,
            "recent_batches_count": len(self._synced_batches),
            "last_evaluated": ServerTimekeeper.get_server_iso_now()
        }


# Singleton export
offline_sync_service = OfflineSyncService()
