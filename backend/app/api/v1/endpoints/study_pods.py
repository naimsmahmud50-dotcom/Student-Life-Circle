"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Real-Time Study Pods & Collaborative Whiteboard Endpoints
TOPIC:     Study Pod Lifecycle, Mesh Capacity Gating & Whiteboard Delta Sync
FILE:      backend/app/api/v1/endpoints/study_pods.py
PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
PURPOSE:   Provides REST and signaling endpoints for virtual collaborative study pods.
           Enforces strict capacity gating (maximum 8 concurrent peers per pod),
           vector stroke and LaTeX formula delta synchronization, and real-time
           VAD (Voice Activity Detection) telemetry.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    status
)

router = APIRouter(prefix="/study-pods", tags=["Study Pods & Real-Time Whiteboard"])

# -----------------------------------------------------------------------------
# In-Memory Study Pod Store with strict capacity boundaries
# -----------------------------------------------------------------------------
MAX_POD_CAPACITY = 8

class StudyPodRegistry:
    """Thread-safe in-memory registry for Phase 101 Collaborative Study Pods."""

    def __init__(self):
        self._pods: Dict[str, Dict[str, Any]] = {}
        self._whiteboards: Dict[str, Dict[str, Any]] = {}
        self._telemetry: Dict[str, Dict[str, Any]] = {}
        self._seed_default_pods()

    def _seed_default_pods(self):
        seed_id = "pod-hsc-higher-math-2026"
        self._pods[seed_id] = {
            "pod_id": seed_id,
            "title": "HSC Higher Math: Calculus & Conics Problem Solving",
            "subject": "Higher Mathematics",
            "creator_id": "usr-lead-tutor-01",
            "creator_name": "Tanzir Ahmed",
            "max_capacity": MAX_POD_CAPACITY,
            "participants": [
                {
                    "user_id": "usr-lead-tutor-01",
                    "user_name": "Tanzir Ahmed",
                    "role": "tutor",
                    "joined_at": time.time() - 3600
                },
                {
                    "user_id": "usr-student-01",
                    "user_name": "Sadia Islam",
                    "role": "student",
                    "joined_at": time.time() - 1800
                }
            ],
            "created_at": time.time() - 3600,
            "status": "active"
        }
        self._whiteboards[seed_id] = {
            "strokes": [],
            "formulas": [],
            "version": 1
        }
        self._telemetry[seed_id] = {
            "usr-lead-tutor-01": {"is_speaking": False, "audio_level_db": -60.0, "last_seen": time.time()},
            "usr-student-01": {"is_speaking": False, "audio_level_db": -60.0, "last_seen": time.time()}
        }

    def list_pods(self) -> List[Dict[str, Any]]:
        return list(self._pods.values())

    def get_pod(self, pod_id: str) -> Optional[Dict[str, Any]]:
        return self._pods.get(pod_id)

    def create_pod(self, title: str, subject: str, creator_id: str, creator_name: Optional[str] = None, max_capacity: int = MAX_POD_CAPACITY) -> Dict[str, Any]:
        capped_capacity = min(max_capacity, MAX_POD_CAPACITY)
        pod_id = f"pod-{uuid.uuid4().hex[:10]}"
        pod = {
            "pod_id": pod_id,
            "title": title.strip(),
            "subject": subject.strip(),
            "creator_id": creator_id.strip(),
            "creator_name": (creator_name or "Anonymous Scholar").strip(),
            "max_capacity": capped_capacity,
            "participants": [
                {
                    "user_id": creator_id.strip(),
                    "user_name": (creator_name or "Anonymous Scholar").strip(),
                    "role": "creator",
                    "joined_at": time.time()
                }
            ],
            "created_at": time.time(),
            "status": "active"
        }
        self._pods[pod_id] = pod
        self._whiteboards[pod_id] = {"strokes": [], "formulas": [], "version": 1}
        self._telemetry[pod_id] = {
            creator_id.strip(): {"is_speaking": False, "audio_level_db": -60.0, "last_seen": time.time()}
        }
        return pod

    def join_pod(self, pod_id: str, user_id: str, user_name: str, role: str = "student") -> Dict[str, Any]:
        pod = self._pods.get(pod_id)
        if not pod:
            raise KeyError("Pod not found")

        # Check if user is already a participant (idempotent rejoin)
        for p in pod["participants"]:
            if p["user_id"] == user_id:
                return pod

        # Strict capacity gating
        if len(pod["participants"]) >= pod["max_capacity"]:
            raise ValueError(f"Pod has reached maximum capacity of {pod['max_capacity']} peers. Cannot join.")

        pod["participants"].append({
            "user_id": user_id.strip(),
            "user_name": user_name.strip(),
            "role": role.strip(),
            "joined_at": time.time()
        })
        if pod_id not in self._telemetry:
            self._telemetry[pod_id] = {}
        self._telemetry[pod_id][user_id.strip()] = {
            "is_speaking": False,
            "audio_level_db": -60.0,
            "last_seen": time.time()
        }
        return pod

    def leave_pod(self, pod_id: str, user_id: str) -> Dict[str, Any]:
        pod = self._pods.get(pod_id)
        if not pod:
            raise KeyError("Pod not found")
        pod["participants"] = [p for p in pod["participants"] if p["user_id"] != user_id]
        if pod_id in self._telemetry and user_id in self._telemetry[pod_id]:
            del self._telemetry[pod_id][user_id]
        return pod

    def get_whiteboard(self, pod_id: str) -> Dict[str, Any]:
        if pod_id not in self._whiteboards:
            self._whiteboards[pod_id] = {"strokes": [], "formulas": [], "version": 1}
        return {
            "pod_id": pod_id,
            "strokes": self._whiteboards[pod_id]["strokes"],
            "formulas": self._whiteboards[pod_id]["formulas"],
            "version": self._whiteboards[pod_id]["version"]
        }

    def append_whiteboard_delta(self, pod_id: str, delta_type: str, delta_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        wb = self._whiteboards.setdefault(pod_id, {"strokes": [], "formulas": [], "version": 1})
        wb["version"] += 1

        if delta_type == "stroke":
            wb["strokes"].append(delta_data)
        elif delta_type == "formula":
            wb["formulas"].append(delta_data)
        elif delta_type == "erase":
            stroke_id = delta_data.get("stroke_id")
            formula_id = delta_data.get("formula_id")
            if stroke_id:
                wb["strokes"] = [s for s in wb["strokes"] if s.get("stroke_id") != stroke_id]
            if formula_id:
                wb["formulas"] = [f for f in wb["formulas"] if f.get("formula_id") != formula_id]
        elif delta_type == "clear":
            wb["strokes"] = []
            wb["formulas"] = []

        return {
            "acknowledged": True,
            "pod_id": pod_id,
            "version": wb["version"],
            "total_strokes": len(wb["strokes"]),
            "total_formulas": len(wb["formulas"])
        }

    def update_telemetry(self, pod_id: str, user_id: str, is_speaking: bool, audio_level_db: float) -> Dict[str, Any]:
        tel = self._telemetry.setdefault(pod_id, {})
        tel[user_id] = {
            "is_speaking": is_speaking,
            "audio_level_db": audio_level_db,
            "last_seen": time.time()
        }
        return tel[user_id]

    def get_telemetry(self, pod_id: str) -> Dict[str, Any]:
        return {
            "pod_id": pod_id,
            "peers": self._telemetry.get(pod_id, {}),
            "timestamp": time.time()
        }


pod_registry = StudyPodRegistry()


# -----------------------------------------------------------------------------
# REST Endpoints
# -----------------------------------------------------------------------------

@router.get("", status_code=status.HTTP_200_OK)
async def list_study_pods():
    """Returns all active collaborative study pods with participant counts and capacity status."""
    pods = pod_registry.list_pods()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"pods": pods, "total": len(pods)})


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_study_pod(payload: Dict[str, Any]):
    """
    Creates a new collaborative study pod with title, subject, and max capacity (up to 8 peers).
    """
    title = payload.get("title", "").strip()
    subject = payload.get("subject", "").strip()
    creator_id = payload.get("creator_id", "").strip()
    creator_name = payload.get("creator_name", "Anonymous Scholar").strip()
    max_capacity = int(payload.get("max_capacity", MAX_POD_CAPACITY))

    if not title or not subject or not creator_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'title', 'subject', and 'creator_id' are mandatory."
        )

    pod = pod_registry.create_pod(
        title=title,
        subject=subject,
        creator_id=creator_id,
        creator_name=creator_name,
        max_capacity=max_capacity
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=pod)


@router.get("/{pod_id}", status_code=status.HTTP_200_OK)
async def get_study_pod(pod_id: str):
    """
    Returns pod details, current participants, and capacity availability.
    """
    pod = pod_registry.get_pod(pod_id)
    if not pod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' was not found."
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            **pod,
            "is_full": len(pod["participants"]) >= pod["max_capacity"],
            "current_capacity": len(pod["participants"])
        }
    )


@router.post("/{pod_id}/join", status_code=status.HTTP_200_OK)
async def join_study_pod(pod_id: str, payload: Dict[str, Any]):
    """
    Allows a student to enter the study pod.
    Enforces strict capacity gating: blocks joining if room capacity is at maximum (8 peers).
    """
    user_id = payload.get("user_id", "").strip()
    user_name = payload.get("user_name", "Student").strip()
    role = payload.get("role", "student").strip()

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'user_id' is mandatory."
        )

    try:
        updated_pod = pod_registry.join_pod(
            pod_id=pod_id,
            user_id=user_id,
            user_name=user_name,
            role=role
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Successfully joined study pod.",
                "pod": updated_pod,
                "current_peers": len(updated_pod["participants"])
            }
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' does not exist."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.post("/{pod_id}/leave", status_code=status.HTTP_200_OK)
async def leave_study_pod(pod_id: str, payload: Dict[str, Any]):
    """Removes a participant from the active study pod."""
    user_id = payload.get("user_id", "").strip()
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'user_id' is mandatory."
        )
    try:
        updated_pod = pod_registry.leave_pod(pod_id=pod_id, user_id=user_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Successfully left study pod.",
                "pod": updated_pod,
                "current_peers": len(updated_pod["participants"])
            }
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' does not exist."
        )


@router.get("/{pod_id}/whiteboard", status_code=status.HTTP_200_OK)
async def get_whiteboard_state(pod_id: str):
    """Fetches the serialized vector stroke and LaTeX formula history for the pod whiteboard."""
    pod = pod_registry.get_pod(pod_id)
    if not pod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' does not exist."
        )
    wb = pod_registry.get_whiteboard(pod_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=wb)


@router.post("/{pod_id}/whiteboard/delta", status_code=status.HTTP_200_OK)
async def broadcast_whiteboard_delta(pod_id: str, payload: Dict[str, Any]):
    """
    Ingests and broadcasts an incremental vector stroke, LaTeX stamp, or erase delta.
    """
    pod = pod_registry.get_pod(pod_id)
    if not pod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' does not exist."
        )
    delta_type = payload.get("type", "stroke")
    delta_data = payload.get("delta", {})
    user_id = payload.get("user_id", "anonymous")

    result = pod_registry.append_whiteboard_delta(
        pod_id=pod_id,
        delta_type=delta_type,
        delta_data=delta_data,
        user_id=user_id
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/{pod_id}/telemetry", status_code=status.HTTP_200_OK)
async def get_pod_telemetry(pod_id: str):
    """
    Returns real-time voice activity detection (VAD) metrics for all active peers in the pod.
    """
    pod = pod_registry.get_pod(pod_id)
    if not pod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' does not exist."
        )
    tel = pod_registry.get_telemetry(pod_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=tel)


@router.post("/{pod_id}/telemetry", status_code=status.HTTP_200_OK)
async def update_peer_telemetry(pod_id: str, payload: Dict[str, Any]):
    """
    Updates client VAD voice activity state (speaking / dB level).
    """
    pod = pod_registry.get_pod(pod_id)
    if not pod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study pod '{pod_id}' does not exist."
        )
    user_id = payload.get("user_id", "").strip()
    is_speaking = bool(payload.get("is_speaking", False))
    audio_level_db = float(payload.get("audio_level_db", -60.0))

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'user_id' is mandatory."
        )
    updated = pod_registry.update_telemetry(pod_id, user_id, is_speaking, audio_level_db)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated)
