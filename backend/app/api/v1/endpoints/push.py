# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 94 - Web Push & Guardian Notification Endpoints):
# This module exposes production REST API endpoints for W3C Web Push subscriptions,
# VAPID key distribution, scheduled retention alerts, and Guardian Messaging Bot.
# Endpoints:
# 1. GET  /push/vapid-public-key: Delivers VAPID public key for browser pushManager.
# 2. POST /push/subscribe: Registers client endpoint, p256dh, and auth keys.
# 3. POST /push/unsubscribe: Unsubscribes client endpoint.
# 4. POST /push/send: Direct custom push notification dispatch.
# 5. POST /push/scheduled/daily-quiz: Dispatches NCTB daily quiz readiness alert.
# 6. POST /push/scheduled/streak-reminder: Dispatches 5-day study streak retention alert.
# 7. POST /push/guardian/digest: Dispatches weekly academic digest to verified guardian.
# Standards: W3C Push API, RFC 8292 VAPID, Child Safety & Privacy, Zero-Emoji.
# ==============================================================================

from typing import Dict, Any, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    Query,
    status
)
from backend.app.services.notifications.web_push_service import web_push_service
from backend.app.services.notifications.guardian_bot_service import (
    guardian_bot_service,
    GuardianNotVerifiedError,
    GuardianPrivacyViolationError
)

router = APIRouter(prefix="/push", tags=["W3C Web Push & Guardian Messaging"])


@router.get("/vapid-public-key")
async def get_vapid_public_key():
    """
    Returns platform RFC 8292 VAPID uncompressed public key.
    """
    return {
        "status": "SUCCESS",
        "vapid_public_key": web_push_service.get_public_key()
    }


@router.post("/subscribe")
async def subscribe_push_client(payload: Dict[str, Any]):
    """
    Registers a browser client push subscription.
    """
    user_id = payload.get("user_id", "STD_CURRENT_USER")
    endpoint = payload.get("endpoint", "")
    keys = payload.get("keys", {})
    p256dh = keys.get("p256dh") or payload.get("p256dh", "")
    auth = keys.get("auth") or payload.get("auth", "")
    user_agent = payload.get("user_agent")

    if not endpoint or not p256dh or not auth:
        raise HTTPException(
            status_code=400,
            detail="Push subscription requires valid endpoint, p256dh, and auth parameters."
        )

    try:
        res = web_push_service.subscribe(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            user_agent=user_agent
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/unsubscribe")
async def unsubscribe_push_client(payload: Dict[str, Any]):
    """
    Unsubscribes a client endpoint from Web Push.
    """
    endpoint = payload.get("endpoint", "")
    if not endpoint:
        raise HTTPException(status_code=400, detail="Missing required endpoint parameter.")

    return web_push_service.unsubscribe(endpoint)


@router.post("/send")
async def send_direct_push_notification(payload: Dict[str, Any]):
    """
    Dispatches a custom push notification to a user's registered devices.
    """
    user_id = payload.get("user_id")
    title = payload.get("title", "Student Life Circle")
    body = payload.get("body", "নতুন শিক্ষামূলক নোটিফিকেশন")
    action_url = payload.get("action_url", "/dashboard")
    tag = payload.get("tag")

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id parameter.")

    res = web_push_service.send_push_notification(
        user_id=user_id,
        title=title,
        body=body,
        action_url=action_url,
        tag=tag
    )
    return res


@router.post("/scheduled/daily-quiz")
async def trigger_daily_quiz_reminder(payload: Dict[str, Any]):
    """
    Dispatches the daily quiz ready notification.
    Exact text: 'আজকের কুইজ প্রস্তুত: এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়'
    """
    user_id = payload.get("user_id", "STD_CURRENT_USER")
    chapter = payload.get("chapter", "এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়")

    res = web_push_service.dispatch_daily_quiz_reminder(user_id=user_id, chapter=chapter)
    return res


@router.post("/scheduled/streak-reminder")
async def trigger_streak_retention_reminder(payload: Dict[str, Any]):
    """
    Dispatches the study streak retention notification.
    Exact text: 'আপনার ৫ দিনের স্টাডি স্ট্রিক ধরে রাখতে আজকের প্র্যাকটিস সম্পন্ন করুন!'
    """
    user_id = payload.get("user_id", "STD_CURRENT_USER")
    streak_days = int(payload.get("streak_days", 5))

    res = web_push_service.dispatch_streak_reminder(user_id=user_id, streak_days=streak_days)
    return res


@router.post("/guardian/digest")
async def trigger_guardian_weekly_digest(payload: Dict[str, Any]):
    """
    Dispatches the weekly academic progress digest to a verified guardian.
    Channels: WHATSAPP, TELEGRAM.
    Enforces Child Safety & Privacy guarantees.
    """
    guardian_id = payload.get("guardian_id", "")
    student_id = payload.get("student_id", "")
    channel = payload.get("channel", "WHATSAPP")
    telegram_chat_id = payload.get("telegram_chat_id")

    if not guardian_id or not student_id:
        raise HTTPException(status_code=400, detail="Missing guardian_id or student_id parameter.")

    try:
        res = guardian_bot_service.dispatch_weekly_digest(
            guardian_id=guardian_id,
            student_id=student_id,
            channel=channel,
            telegram_chat_id=telegram_chat_id
        )
        return res
    except GuardianNotVerifiedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except GuardianPrivacyViolationError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
