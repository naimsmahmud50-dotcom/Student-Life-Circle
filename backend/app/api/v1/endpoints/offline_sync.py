"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Offline CRDT Batch Synchronization API Endpoints
TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
FILE:      backend/app/api/v1/endpoints/offline_sync.py
PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
PURPOSE:   Exposes versioned REST API endpoints for receiving batch CRDT mutations from
           rural teacher offline stations, verifying payload integrity, reconciling
           student offline quiz attempts, and querying station sync health.
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, Distributed CRDT Semantics, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.offline_crdt_sync_service import (
    OfflineCrdtSyncService,
    offline_crdt_sync_service,
    InvalidBatchPayloadException,
    StationNotFoundException,
    OfflineSyncException,
)

router = APIRouter(prefix="/offline-sync", tags=["Offline Classroom Mesh & CRDT Sync"])


@router.post("/batch-reconcile", response_model=Dict[str, Any])
def reconcile_batch(payload: Dict[str, Any]):
    """
    Receives and reconciles a batch of CRDT mutations from an offline classroom station.
    Enforces deterministic Last-Write-Wins (LWW) and complete idempotency.
    """
    station_id = payload.get("station_id")
    batch_id = payload.get("batch_id")
    mutations = payload.get("mutations", [])
    checksum = payload.get("checksum")

    if not station_id or not batch_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: station_id or batch_id.",
        )

    try:
        return offline_crdt_sync_service.reconcile_batch(
            station_id=station_id,
            batch_id=batch_id,
            mutations=mutations,
            checksum=checksum,
        )
    except InvalidBatchPayloadException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/station/{station_id}/status", response_model=Dict[str, Any])
def get_station_status(station_id: str):
    """
    Retrieves synchronization metadata and health status for an offline station.
    """
    try:
        return offline_crdt_sync_service.get_station_status(station_id)
    except StationNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/quiz/{quiz_id}/student/{student_id}", response_model=Dict[str, str])
def get_reconciled_student_answers(quiz_id: str, student_id: str):
    """
    Returns resolved question answers for a student on a quiz.
    """
    return offline_crdt_sync_service.get_student_quiz_answers(
        quiz_id=quiz_id,
        student_id=student_id,
    )


@router.get("/audit-trail", response_model=List[Dict[str, Any]])
def get_sync_audit_trail():
    """
    Retrieves the complete audit trail of cloud batch synchronization events.
    """
    return offline_crdt_sync_service.get_sync_audit_trail()
