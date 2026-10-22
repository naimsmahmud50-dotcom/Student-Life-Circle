"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Curriculum Knowledge Graph & Dynamic Remedial Navigator Endpoints
TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
FILE:      backend/app/api/v1/endpoints/knowledge_graph.py
PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
PURPOSE:   Exposes versioned REST API endpoints for curriculum DAG exploration,
           recursive prerequisite dependency queries, student gap identification,
           and 3-step dynamic remedial pathway synthesis.
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, Pedagogical Gap Recovery, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.curriculum_knowledge_graph_service import (
    CurriculumKnowledgeGraphService,
    curriculum_knowledge_graph_service,
    TopicNotFoundException,
    CycleDetectedException,
    KnowledgeGraphException,
)

router = APIRouter(prefix="/knowledge-graph", tags=["Curriculum Knowledge Graph & Remedial Navigator"])


@router.get("/atlas", response_model=Dict[str, Any])
def get_knowledge_graph_atlas(
    subject: Optional[str] = Query(None),
    class_grade: Optional[int] = Query(None),
):
    """
    Returns topic nodes with coordinate positioning and prerequisite edges
    for interactive SVG atlas rendering.
    """
    return curriculum_knowledge_graph_service.get_graph_snapshot(
        subject=subject,
        class_grade=class_grade,
    )


@router.get("/topics/{topic_id}", response_model=Dict[str, Any])
def get_topic_details(topic_id: str):
    """
    Retrieves full topic node metadata by topic_id.
    """
    try:
        return curriculum_knowledge_graph_service.get_topic(topic_id)
    except TopicNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/topics/{topic_id}/prerequisites", response_model=List[Dict[str, Any]])
def get_topic_prerequisites(
    topic_id: str,
    recursive: bool = Query(True),
):
    """
    Returns prerequisite topics in topological dependency order.
    """
    try:
        return curriculum_knowledge_graph_service.get_prerequisites(
            topic_id=topic_id,
            recursive=recursive,
        )
    except TopicNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/topics/{topic_id}/gaps", response_model=List[Dict[str, Any]])
def identify_topic_gaps(topic_id: str, payload: Optional[Dict[str, Any]] = None):
    """
    Identifies prerequisite topics where the student has mastery gaps (< threshold).
    """
    body = payload or {}
    student_mastery_map = body.get("student_mastery_map", {})
    threshold = float(body.get("threshold", 0.70))

    try:
        return curriculum_knowledge_graph_service.identify_prerequisite_gaps(
            topic_id=topic_id,
            student_mastery_map=student_mastery_map,
            threshold=threshold,
        )
    except TopicNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/topics/{topic_id}/remedial-pathway", response_model=Dict[str, Any])
def generate_remedial_pathway(topic_id: str, payload: Optional[Dict[str, Any]] = None):
    """
    Synthesizes a 3-step dynamic remedial pathway (15 mins) for a struggling topic.
    """
    body = payload or {}
    student_mastery_map = body.get("student_mastery_map", {})

    try:
        return curriculum_knowledge_graph_service.generate_remedial_pathway(
            topic_id=topic_id,
            student_mastery_map=student_mastery_map,
        )
    except TopicNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
