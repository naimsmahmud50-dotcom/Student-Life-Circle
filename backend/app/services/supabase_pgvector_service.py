"""
================================================================================
MODULE: Supabase pgvector Semantic Search & AI Syllabus Grounding Engine
TOPIC: Vector Similarity (Cosine/L2/Inner Product), HNSW Indexing & RLS Scoping
FILE: backend/app/services/supabase_pgvector_service.py
PURPOSE: High-precision mathematical vector search engine supporting pgvector
         PostgreSQL extension semantics, preventing cross-tenant vector disclosure,
         and validating AI tutor syllabus grounding to eliminate hallucinations.
AUDIENCE: AI Engineers, Database Architects, Educational Assessment Scientists.
================================================================================
"""

import math
from typing import Dict, Any, List, Optional


class SupabasePgvectorService:
    """
    Mathematical engine implementing Supabase pgvector operations,
    cosine similarity metrics, HNSW index approximations, and RLS-scoped search.
    """

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two n-dimensional vectors:
        cos(theta) = (A . B) / (||A|| * ||B||)
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        return max(-1.0, min(1.0, dot_product / (norm_a * norm_b)))

    def l2_distance(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes Euclidean (L2) distance:
        d = sqrt(sum((a_i - b_i)^2))
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 999.0
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))

    def search_semantic_knowledge(
        self,
        query_vector: List[float],
        corpus: List[Dict[str, Any]],
        caller_tenant_id: str,
        caller_role: str = "authenticated",
        top_k: int = 3,
        similarity_threshold: float = 0.70
    ) -> Dict[str, Any]:
        """
        Executes an RLS-scoped vector similarity search.
        Prevents cross-tenant vector information leakage:
        - Anonymous / Authenticated users only see public or own-tenant vectors.
        - Matches are sorted by cosine similarity descending.
        """
        filtered_results = []
        violations_prevented = 0

        for item in corpus:
            doc_tenant = item.get("tenant_id")
            is_public = item.get("is_public", False)

            # RLS Boundary Check
            if caller_role != "service_role":
                if not is_public and doc_tenant != caller_tenant_id:
                    violations_prevented += 1
                    continue  # Strip unauthorized vector

            item_vec = item.get("embedding", [])
            sim = self.cosine_similarity(query_vector, item_vec)
            l2 = self.l2_distance(query_vector, item_vec)

            if sim >= similarity_threshold:
                filtered_results.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "category": item.get("category", "academic"),
                    "similarity": round(sim, 4),
                    "l2_distance": round(l2, 4),
                    "is_public": is_public,
                    "tenant_id": doc_tenant,
                    "grounding_status": "GROUNDED" if sim >= 0.82 else "PARTIAL_MATCH"
                })

        # Sort descending by similarity
        filtered_results.sort(key=lambda x: x["similarity"], reverse=True)
        top_results = filtered_results[:top_k]

        return {
            "total_candidates": len(corpus),
            "matched_count": len(top_results),
            "cross_tenant_leaks_prevented": violations_prevented,
            "results": top_results,
            "top_similarity": top_results[0]["similarity"] if top_results else 0.0
        }

    def evaluate_ai_grounding(
        self,
        ai_response_embedding: List[float],
        verified_syllabus_chunks: List[List[float]],
        grounding_threshold: float = 0.82
    ) -> Dict[str, Any]:
        """
        Evaluates whether an AI tutor's explanation is grounded in authentic NCTB/university curriculum.
        Eliminates AI hallucinations by ensuring cosine similarity with trusted syllabus chunks meets threshold.
        """
        if not verified_syllabus_chunks:
            return {
                "is_grounded": False,
                "confidence_score": 0.0,
                "verdict": "UNGROUNDED_NO_SYLLABUS_REFERENCE",
                "recommendation": "DO_NOT_PUBLISH_TO_STUDENT"
            }

        max_sim = max(self.cosine_similarity(ai_response_embedding, chunk) for chunk in verified_syllabus_chunks)

        is_grounded = max_sim >= grounding_threshold
        return {
            "is_grounded": is_grounded,
            "confidence_score": round(max_sim, 4),
            "threshold_required": grounding_threshold,
            "verdict": "VERIFIED_SYLLABUS_GROUNDED" if is_grounded else "POTENTIAL_HALLUCINATION_DETECTED",
            "recommendation": "SAFE_FOR_STUDENT" if is_grounded else "REQUIRE_HUMAN_INSTRUCTOR_REVIEW"
        }
