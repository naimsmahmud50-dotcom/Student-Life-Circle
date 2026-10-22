"""
========================================================================================
MODULE:    Omni-Gateway, Cross-Platform Notifications & Student Reputation Schemas
TOPIC:     Unified Search, Multi-Platform Event Dispatch & Holistic Reputation Engine
FILE:      backend/app/schemas/omni_gateway_schema.py
PURPOSE:   Provides Pydantic/BaseDTO validated data models for:
           1. Unified Omni-Search across 10MS lectures, CareTutors posts & Bdjobs roles.
           2. Real-time multi-platform push notification dispatching & unread inbox.
           3. 4-Pillar Composite Student Reputation Score (0-1000) & Daily Quests.
STANDARDS: Machine-Readable Envelopes, Strict Field Validation, OWASP ASVS L2 Audit
AUDIENCE:  Frontend Architects, API Gateway Engineers & AI Agents
========================================================================================
"""

from typing import Any, Dict, List, Optional
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(*args, **kwargs):
        return None


# ======================================================================================
# TOPIC 1: UNIFIED OMNI-SEARCH SCHEMAS
# ======================================================================================

class OmniSearchRequest(BaseModel):
    """
    Unified search query covering all platform dimensions.
    Categories: 'ALL', 'ACADEMIC_LECTURES', 'TUITIONS', 'INTERNSHIPS'
    """
    query: str
    category: str = "ALL"
    limit: int = 15


class OmniSearchResultItem(BaseModel):
    """Single normalized search result match with relevance score."""
    id: str
    category: str  # 'ACADEMIC_LECTURES', 'TUITIONS', 'INTERNSHIPS'
    title: str
    subtitle: str
    badge: str
    relevance_score: float
    action_url: str
    meta: Dict[str, Any] = {}


class OmniSearchResponse(BaseModel):
    """Unified search envelope."""
    query: str
    total_matches: int
    results: List[OmniSearchResultItem]


# ======================================================================================
# TOPIC 2: REAL-TIME NOTIFICATION GATEWAY SCHEMAS
# ======================================================================================

class NotificationDispatchRequest(BaseModel):
    """
    Event payload dispatched to a user across web push, socket, and in-app drawer.
    Categories: 'CARE_TUTORS', 'BDJOBS', 'TEN_MS', 'ACADEMIC_TRIBUNAL', 'SYSTEM'
    Priorities: 'LOW', 'NORMAL', 'HIGH', 'URGENT'
    """
    recipient_user_id: str
    category: str = "SYSTEM"
    title: str
    message: str
    priority: str = "NORMAL"
    action_link: Optional[str] = None


class NotificationRecord(BaseModel):
    """Stored notification item in user's audit inbox."""
    notification_id: str
    recipient_user_id: str
    category: str
    title: str
    message: str
    priority: str
    is_read: bool = False
    created_at: str
    action_link: Optional[str] = None


class NotificationListResponse(BaseModel):
    """User notification inbox with unread counter."""
    user_id: str
    unread_count: int
    notifications: List[NotificationRecord]


# ======================================================================================
# TOPIC 3: STUDENT REPUTATION & DAILY QUEST SCHEMAS
# ======================================================================================

class StudentReputationScoreResponse(BaseModel):
    """
    Holistic 0-1000 Composite Reputation Score across 4 pillars:
    1. Academic Mastery (35%)
    2. Tutoring Reliability (25%)
    3. Career Preparedness (25%)
    4. Community Integrity (15%)
    """
    student_id: str
    composite_score: int  # 0 to 1000
    tier: str             # 'NOVICE_SCHOLAR', 'ACADEMIC_EXPLORER', 'MASTER_MENTOR', 'EMINENCE_FELLOW'
    percentile: float     # 0.0 to 100.0%
    academic_mastery_points: int
    tutoring_reliability_points: int
    career_preparedness_points: int
    community_integrity_points: int
    radar_breakdown: Dict[str, float]
    next_tier_progress_percent: float


class DailyQuest(BaseModel):
    """Gamified daily student habit quest."""
    quest_id: str
    title: str
    description: str
    pillar: str  # 'ACADEMIC', 'TUITION', 'CAREER', 'COMMUNITY'
    target_count: int
    current_count: int
    reward_points: int
    is_completed: bool
    is_claimed: bool


class QuestClaimRequest(BaseModel):
    """Payload to claim completed quest rewards."""
    student_id: str
    quest_id: str
