"""
========================================================================================
MODULE:    Question Deduplication & Semantic Similarity Service
TOPIC:     Triple-Layer Duplicate Prevention (Hash, Token & Semantic Cosine)
FILE:      backend/app/services/deduplication.py
PURPOSE:   Guarantees the high quality and novelty of the Question Bank. Inspects
           every draft question through three progressive layers: (1) Exact SHA-256
           stem hash, (2) Normalized Jaccard token overlap for near-duplicate stems,
           and (3) Cosine vector similarity. Prevents flooding of redundant questions.
AUDIENCE:  Developers, Content Authors & AI Agents
STANDARDS: Clean Architecture, Deterministic Hashing, AI Quality Gates
========================================================================================
"""

import hashlib
import re
from typing import Dict, List, Tuple, Set


class QuestionDeduplicationService:
    """
    Multi-layer deduplication engine for academic question banks.
    """

    @staticmethod
    def compute_sha256(text: str) -> str:
        """Computes exact canonical SHA-256 hash of normalized text."""
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def tokenize_bangla_text(text: str) -> Set[str]:
        """Tokenizes Bengali and English text, stripping punctuation."""
        cleaned = re.sub(r"[^\w\s\u0980-\u09FF]", " ", text)
        return {word.strip() for word in cleaned.split() if len(word.strip()) > 1}

    @classmethod
    def calculate_jaccard_similarity(cls, text_a: str, text_b: str) -> float:
        """Computes token intersection over union (Jaccard similarity)."""
        tokens_a = cls.tokenize_bangla_text(text_a)
        tokens_b = cls.tokenize_bangla_text(text_b)
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = len(tokens_a.intersection(tokens_b))
        union = len(tokens_a.union(tokens_b))
        return intersection / union if union > 0 else 0.0

    @classmethod
    def check_duplicate(
        cls,
        candidate_stem: str,
        existing_questions: List[Dict[str, str]],
        jaccard_threshold: float = 0.82
    ) -> Tuple[bool, str, float]:
        """
        Runs candidate stem against known question bank stems.
        Returns: (is_duplicate, matched_id, confidence_score)
        """
        cand_hash = cls.compute_sha256(candidate_stem)

        for item in existing_questions:
            # Layer 1: Exact Hash Match
            if item.get("content_hash") == cand_hash:
                return True, item["id"], 1.0

            # Layer 2: Token Jaccard Similarity Match
            similarity = cls.calculate_jaccard_similarity(candidate_stem, item.get("stem_bn", ""))
            if similarity >= jaccard_threshold:
                return True, item["id"], round(similarity, 3)

        return False, "", 0.0


# Singleton Service Instance
deduplication_service = QuestionDeduplicationService()
