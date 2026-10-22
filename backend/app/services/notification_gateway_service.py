"""
========================================================================================
MODULE:    Real-Time Cross-Platform Notification Gateway
TOPIC:     Event Dispatch, Web Push, In-App Drawer & Bilateral Consent Alerts
FILE:      backend/app/services/notification_gateway_service.py
PURPOSE:   Dispatches real-time events across 10MS, CareTutors, and Bdjobs:
           1. In-lecture checkpoint achievements & streak milestones.
           2. CareTutors tuition application shortlists, guardian approvals & bilateral releases.
           3. Bdjobs hiring pipeline stage updates (Interview scheduled, Offer released).
           4. ASVS L2 security and audit warnings.
STANDARDS: Non-Blocking Event Routing, Unread Indexing, Priority-Based Escalation
AUDIENCE:  Real-time Systems Engineers, Mobile Architects & AI Agents
========================================================================================
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class NotificationGatewayService:
    """
    Enterprise Notification Gateway managing unified push notifications
    and user audit drawers across the tripartite platform.
    """

    PRIORITY_LOW = "LOW"
    PRIORITY_NORMAL = "NORMAL"
    PRIORITY_HIGH = "HIGH"
    PRIORITY_URGENT = "URGENT"

    CATEGORY_10MS = "TEN_MS"
    CATEGORY_CARETUTORS = "CARE_TUTORS"
    CATEGORY_BDJOBS = "BDJOBS"
    CATEGORY_TRIBUNAL = "ACADEMIC_TRIBUNAL"
    CATEGORY_SYSTEM = "SYSTEM"

    def __init__(self):
        # user_id -> list of notification dicts
        self._inbox: Dict[str, List[Dict[str, Any]]] = {}
        self._seed_default_notifications()

    def _seed_default_notifications(self):
        """Pre-seeds standard benchmark notifications for demo student accounts."""
        demo_user = "student_demo_01"
        self._inbox[demo_user] = [
            {
                "notification_id": "notif_001",
                "recipient_user_id": demo_user,
                "category": self.CATEGORY_BDJOBS,
                "title": "Interview Invitation Received",
                "message": "Brain Station 23 reviewed your Sealed CV Snapshot (100% skill match) and scheduled a Technical Viva.",
                "priority": self.PRIORITY_URGENT,
                "is_read": False,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "action_link": "#tab-career"
            },
            {
                "notification_id": "notif_002",
                "recipient_user_id": demo_user,
                "category": self.CATEGORY_CARETUTORS,
                "title": "Guardian Approved Your Shortlist",
                "message": "Guardian for Class 9 Physics (Dhanmondi) approved your tuition bid. Bilateral consent pending your acceptance.",
                "priority": self.PRIORITY_HIGH,
                "is_read": False,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "action_link": "#tab-tuition"
            },
            {
                "notification_id": "notif_003",
                "recipient_user_id": demo_user,
                "category": self.CATEGORY_10MS,
                "title": "Checkpoint Milestone Unlocked",
                "message": "You correctly answered the in-lecture quiz for Unitary Method & Velocity (+100 Mastery Points).",
                "priority": self.PRIORITY_NORMAL,
                "is_read": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "action_link": "#tab-practice"
            }
        ]

    # ----------------------------------------------------------------------------------
    # TOPIC: EVENT DISPATCHING & INBOX RECORDING
    # ----------------------------------------------------------------------------------

    def dispatch_notification(
        self,
        recipient_user_id: str,
        category: str,
        title: str,
        message: str,
        priority: str = "NORMAL",
        action_link: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches a new notification to a recipient's inbox and simulates real-time broadcast.
        """
        clean_user = (recipient_user_id or "").strip()
        if not clean_user:
            return {
                "success": False,
                "error_code": "INVALID_RECIPIENT_USER_ID",
                "message": "Recipient user ID cannot be blank."
            }

        if not (title or "").strip():
            return {
                "success": False,
                "error_code": "EMPTY_NOTIFICATION_TITLE",
                "message": "Notification title cannot be blank."
            }

        if not (message or "").strip():
            return {
                "success": False,
                "error_code": "EMPTY_NOTIFICATION_MESSAGE",
                "message": "Notification message cannot be blank."
            }

        user_list = self._inbox.setdefault(clean_user, [])
        notif_id = f"notif_{int(datetime.now(timezone.utc).timestamp())}_{len(user_list) + 1}"
        record = {
            "notification_id": notif_id,
            "recipient_user_id": clean_user,
            "category": category,
            "title": title.strip(),
            "message": message.strip(),
            "priority": priority,
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "action_link": action_link
        }
        # Prepend to list for reverse-chronological order
        user_list.insert(0, record)

        return {
            "success": True,
            "notification": record,
            "message": f"Notification '{notif_id}' dispatched successfully to user '{clean_user}'."
        }

    # ----------------------------------------------------------------------------------
    # TOPIC: RETRIEVAL & UNREAD TRACKING
    # ----------------------------------------------------------------------------------

    def get_user_notifications(
        self,
        user_id: str,
        only_unread: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves user's notification drawer with dynamic unread counter.
        """
        user_list = self._inbox.get(user_id, [])
        unread_count = sum(1 for n in user_list if not n["is_read"])

        if only_unread:
            filtered = [n for n in user_list if not n["is_read"]]
        else:
            filtered = list(user_list)

        return {
            "success": True,
            "user_id": user_id,
            "unread_count": unread_count,
            "total_count": len(user_list),
            "notifications": filtered
        }

    def mark_as_read(
        self,
        notification_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Marks an individual notification as read."""
        user_list = self._inbox.get(user_id, [])
        item = next((n for n in user_list if n["notification_id"] == notification_id), None)
        if not item:
            return {
                "success": False,
                "error_code": "NOTIFICATION_NOT_FOUND",
                "message": f"Notification '{notification_id}' not found in inbox."
            }

        item["is_read"] = True
        unread_count = sum(1 for n in user_list if not n["is_read"])
        return {
            "success": True,
            "notification_id": notification_id,
            "is_read": True,
            "unread_count": unread_count,
            "message": "Notification marked as read."
        }

    def mark_all_as_read(self, user_id: str) -> Dict[str, Any]:
        """Marks all notifications in user's inbox as read."""
        user_list = self._inbox.get(user_id, [])
        for n in user_list:
            n["is_read"] = True

        return {
            "success": True,
            "user_id": user_id,
            "marked_count": len(user_list),
            "unread_count": 0,
            "message": "All notifications marked as read."
        }


# Singleton instance
notification_gateway_service = NotificationGatewayService()
