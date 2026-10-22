"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Official NCTB Board Question Archive API Endpoints
TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
FILE:      backend/app/api/v1/endpoints/board_archives.py
PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
PURPOSE:   REST API router exposing indexed queries, multi-criteria filtering,
           faceted metadata, and curriculum coverage statistics for official
           Bangladesh NCTB board past examination papers (2015-2025).
STANDARDS: REST OpenAPI 3.1, NCTB Curriculum 2024, KaTeX Math Spec, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.board_archive_service import board_archive_service

router = APIRouter(prefix="/board-archives", tags=["NCTB Board Archives"])


@router.get("", response_model=Dict[str, Any])
def search_board_papers(
    level: Optional[str] = Query(None, description="Curriculum Level: SSC or HSC"),
    subject: Optional[str] = Query(None, description="Subject name: Physics, Chemistry, Higher Mathematics, Biology, ICT"),
    paper: Optional[str] = Query(None, description="Paper: 1st, 2nd, Combined"),
    board: Optional[str] = Query(None, description="Board: Dhaka, Chittagong, Rajshahi, etc."),
    year: Optional[int] = Query(None, description="Examination Year: 2015 to 2025"),
    chapter: Optional[str] = Query(None, description="Chapter filter keyword"),
    question_type: Optional[str] = Query(None, description="Question Type: CQ or MCQ"),
    search_query: Optional[str] = Query(None, description="Free-text search query across stems and solutions"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Retrieves paginated and filtered official NCTB board questions."""
    return board_archive_service.filter_papers(
        level=level,
        subject=subject,
        paper=paper,
        board=board,
        year=year,
        chapter=chapter,
        question_type=question_type,
        search_query=search_query,
        limit=limit,
        offset=offset,
    )


@router.get("/facets", response_model=Dict[str, Any])
def get_board_archive_facets():
    """Returns available filtering facets: boards, years, subjects, levels, and chapters."""
    return board_archive_service.get_available_facets()


@router.get("/stats", response_model=Dict[str, Any])
def get_curriculum_coverage_stats():
    """Returns total questions count, year range, and distribution by board and subject."""
    return board_archive_service.get_curriculum_coverage_stats()


@router.get("/integrity", response_model=Dict[str, Any])
def get_archive_integrity():
    """Verifies that archive contains zero duplicate hashes and all KaTeX math delimiters balance."""
    return board_archive_service.verify_archive_integrity()


@router.get("/{paper_id}", response_model=Dict[str, Any])
def get_paper_by_id(paper_id: str):
    """Retrieves a single board examination question by ID."""
    paper = board_archive_service.get_paper_by_id(paper_id)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Board paper with ID '{paper_id}' not found."
        )
    return paper
