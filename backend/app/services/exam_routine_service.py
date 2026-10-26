"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Exam Routine & Model Test Service
TOPIC:     200-Day BCS & Admission Routine Calendar, Mega Model Tests & Scoring Analytics
FILE:      backend/app/services/exam_routine_service.py
PURPOSE:   Encapsulates business logic for retrieving 200-day daily exam routines,
           synchronized Friday Mega Model Test countdown calculation, negative marking
           penalty calculations, and user reminder subscriptions.
STANDARDS: Zero-Emoji, ASVS L2, Pure Domain Logic, Comprehensive Edge Case Handling
========================================================================================
"""

from datetime import datetime, timezone, timedelta
import uuid
from typing import List, Optional, Dict, Any

from backend.app.schemas.exam_routine_schema import (
    ExamTypeEnum,
    TrackCategoryEnum,
    ExamRoutineItem,
    ExamRoutineListResponse,
    NegativeMarkSimulationRequest,
    NegativeMarkSimulationResponse,
    RoutineSubscribeRequest,
    RoutineSubscribeResponse,
)


class ExamRoutineService:
    def __init__(self):
        self._seed_routines = self._initialize_seed_routines()
        self._subscriptions: Dict[str, Dict[str, Any]] = {}

    def _initialize_seed_routines(self) -> List[ExamRoutineItem]:
        now = datetime.now(timezone.utc)
        routines = [
            # Day 1: BCS Bangla Literature
            ExamRoutineItem(
                id="rtn-bcs-001",
                routine_code="BCS-200-DAY-001",
                title="প্রাচীন ও মধ্যযুগের বাংলা সাহিত্য: চর্যাপদ ও মঙ্গলকাব্য",
                exam_type=ExamTypeEnum.BCS_PRELI,
                track_category=TrackCategoryEnum.BANGLA,
                day_number=1,
                syllabus_summary="চর্যাপদের আবিস্কার, কবি পরিচিতি, শ্রীকৃষ্ণকীর্তন, বৈষ্ণব পদাবলী ও মনসামঙ্গল কাব্য।",
                start_time=(now - timedelta(days=2)).isoformat(),
                end_time=(now + timedelta(days=28)).isoformat(),
                duration_minutes=30,
                total_questions=50,
                total_marks=50.0,
                negative_mark_factor=0.25,
                is_mega_model_test=False,
                is_published=True,
                live_participant_count=4820,
            ),
            # Day 2: BCS English Grammar
            ExamRoutineItem(
                id="rtn-bcs-002",
                routine_code="BCS-200-DAY-002",
                title="English Language: Parts of Speech, Inversion & Modifiers",
                exam_type=ExamTypeEnum.BCS_PRELI,
                track_category=TrackCategoryEnum.ENGLISH,
                day_number=2,
                syllabus_summary="Classification of nouns, adjective clauses, dangling modifiers, parallel structures.",
                start_time=(now - timedelta(days=1)).isoformat(),
                end_time=(now + timedelta(days=29)).isoformat(),
                duration_minutes=30,
                total_questions=50,
                total_marks=50.0,
                negative_mark_factor=0.25,
                is_mega_model_test=False,
                is_published=True,
                live_participant_count=5130,
            ),
            # Day 7: Weekly Friday Mega Model Test
            ExamRoutineItem(
                id="rtn-bcs-mega-001",
                routine_code="BCS-200-MEGA-001",
                title="সাপ্তাহিক মেগা মডেল টেস্ট ১: পূর্ণাঙ্গ ২০০ নম্বর প্রিলিমিনারি সিমুলেশন",
                exam_type=ExamTypeEnum.BCS_PRELI,
                track_category=TrackCategoryEnum.GENERAL,
                day_number=7,
                syllabus_summary="১ম সপ্তাহের সামগ্রিক সিলেবাস (বাংলা ৩৫, ইংরেজি ৩৫, গণিত ১৫, সাধারণ বিজ্ঞান ১৫, বাংলাদেশ ও আন্তর্জাতিক বিষয়াবলী ৬০)।",
                start_time=(now + timedelta(days=1, hours=3)).isoformat(),
                end_time=(now + timedelta(days=2, hours=3)).isoformat(),
                duration_minutes=120,
                total_questions=200,
                total_marks=200.0,
                negative_mark_factor=0.50,
                is_mega_model_test=True,
                is_published=True,
                live_participant_count=18940,
            ),
            # Admission Track 1: DU Ka Unit
            ExamRoutineItem(
                id="rtn-adm-du-001",
                routine_code="ADM-DU-KA-001",
                title="ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট: পদার্থবিজ্ঞান ১ম পত্র (ভেক্টর ও নিউটনীয় বলবিদ্যা)",
                exam_type=ExamTypeEnum.ADMISSION_VARSITY,
                track_category=TrackCategoryEnum.MATH_SCIENCE,
                day_number=1,
                syllabus_summary="ডট ও ক্রস গুণন, প্রাস, ভরবেগের সংরক্ষণশীলতা সূত্র ও সান্দ্রতা বল।",
                start_time=now.isoformat(),
                end_time=(now + timedelta(days=30)).isoformat(),
                duration_minutes=45,
                total_questions=60,
                total_marks=60.0,
                negative_mark_factor=0.25,
                is_mega_model_test=False,
                is_published=True,
                live_participant_count=6730,
            ),
            # Admission Track 2: BUET Mega Model Test
            ExamRoutineItem(
                id="rtn-adm-buet-001",
                routine_code="ADM-BUET-PRELI-001",
                title="বুয়েট প্রাক-নির্বাচনী মেগা মডেল টেস্ট: উচ্চতর গণিত ও রসায়ন সমন্বিত",
                exam_type=ExamTypeEnum.ADMISSION_VARSITY,
                track_category=TrackCategoryEnum.MATH_SCIENCE,
                day_number=7,
                syllabus_summary="ক্যালকুলাস, কোণিক, গুণগত রসায়ন এবং জারণ-বিজারণ সমীকরণ।",
                start_time=(now + timedelta(days=2)).isoformat(),
                end_time=(now + timedelta(days=3)).isoformat(),
                duration_minutes=60,
                total_questions=100,
                total_marks=100.0,
                negative_mark_factor=0.25,
                is_mega_model_test=True,
                is_published=True,
                live_participant_count=9820,
            ),
            # HSC Board Prep
            ExamRoutineItem(
                id="rtn-hsc-001",
                routine_code="HSC-BOARD-001",
                title="এইচএসসি বোর্ড স্ট্যান্ডার্ড ফাইনাল মডেল: তথ্য ও যোগাযোগ প্রযুক্তি (আইসিটি)",
                exam_type=ExamTypeEnum.HSC_BOARD,
                track_category=TrackCategoryEnum.MATH_SCIENCE,
                day_number=3,
                syllabus_summary="এইচটিএমএল ট্যাগিং, সি প্রোগ্রামিং লুপিং ও বুলিয়ান অ্যালজেব্রা।",
                start_time=now.isoformat(),
                end_time=(now + timedelta(days=15)).isoformat(),
                duration_minutes=25,
                total_questions=25,
                total_marks=25.0,
                negative_mark_factor=0.25,
                is_mega_model_test=False,
                is_published=True,
                live_participant_count=3410,
            ),
        ]
        return routines

    def get_routines(
        self,
        exam_type: Optional[ExamTypeEnum] = None,
        track_category: Optional[TrackCategoryEnum] = None,
        day_number: Optional[int] = None,
    ) -> ExamRoutineListResponse:
        filtered = self._seed_routines
        if exam_type:
            filtered = [r for r in filtered if r.exam_type == exam_type]
        if track_category:
            filtered = [r for r in filtered if r.track_category == track_category]
        if day_number:
            filtered = [r for r in filtered if r.day_number == day_number]

        # Calculate upcoming mega test timestamp
        mega_tests = [r for r in self._seed_routines if r.is_mega_model_test]
        upcoming_mega = mega_tests[0].start_time if mega_tests else None

        now_str = datetime.now(timezone.utc).isoformat()
        return ExamRoutineListResponse(
            success=True,
            routines=filtered,
            total=len(filtered),
            active_day=42, # Realistic mid-semester day
            mega_test_scheduled_at=upcoming_mega,
            server_time=now_str,
        )

    def get_routine_by_id(self, routine_id: str) -> Optional[ExamRoutineItem]:
        for routine in self._seed_routines:
            if routine.id == routine_id or routine.routine_code == routine_id:
                return routine
        return None

    def simulate_negative_marking(
        self, payload: NegativeMarkSimulationRequest
    ) -> NegativeMarkSimulationResponse:
        gross_score = round(payload.correct_answers * payload.mark_per_question, 2)
        penalty_deducted = round(payload.wrong_answers * payload.negative_factor, 2)
        net_score = max(0.0, round(gross_score - penalty_deducted, 2))

        attempted = payload.correct_answers + payload.wrong_answers
        accuracy = round((payload.correct_answers / attempted) * 100.0, 1) if attempted > 0 else 0.0

        score_ratio = net_score / (payload.total_questions * payload.mark_per_question)
        if score_ratio >= 0.80:
            estimated_percentile = round(98.0 + (score_ratio - 0.80) * 8.0, 1)
            estimated_percentile = min(99.9, estimated_percentile)
            merit_bracket = "মেধাতালিকা টপ ১% (জাতীয় ক্যাডার / শীর্ষ অনুষদ সম্ভাবনা)"
        elif score_ratio >= 0.65:
            estimated_percentile = round(88.0 + (score_ratio - 0.65) * 60.0, 1)
            merit_bracket = "নিশ্চিত ভাইভা কল ও প্রথম পছন্দ ইউনিট সম্ভাবনা"
        elif score_ratio >= 0.50:
            estimated_percentile = round(70.0 + (score_ratio - 0.50) * 100.0, 1)
            merit_bracket = "প্রতিযোগিতাপূর্ণ মধ্যম সারির ক্যাটাগরি"
        else:
            estimated_percentile = round(max(10.0, score_ratio * 120.0), 1)
            merit_bracket = "ঘন ঘন নেগেটিভ মার্কিং কমানো এবং রিভিশন প্রয়োজন"

        weakness_flags: List[str] = []
        if payload.wrong_answers > (payload.correct_answers * 0.40):
            weakness_flags.append("উচ্চ ভুল উত্তরের হার: অনুমানের উপর ভিত্তি করে উত্তর দেওয়ার প্রবণতা কমাতে হবে।")
        if penalty_deducted > 10.0:
            weakness_flags.append(f"অতিরিক্ত পেনাল্টি: ভুল উত্তরের কারণে {penalty_deducted} নম্বর কাটা গেছে।")
        if payload.unanswered > (payload.total_questions * 0.35):
            weakness_flags.append("গতি ব্যবস্থাপনা: ৩৫% এর বেশি প্রশ্ন অনুত্তরিত ছিল, সময় বণ্টন উন্নত করুন।")
        if not weakness_flags:
            weakness_flags.append("চমৎকার ব্যালেন্স: সঠিক ও নির্ভুল উত্তরের অনুপাত সন্তোষজনক।")

        return NegativeMarkSimulationResponse(
            success=True,
            total_questions=payload.total_questions,
            correct_answers=payload.correct_answers,
            wrong_answers=payload.wrong_answers,
            unanswered=payload.unanswered,
            gross_score=gross_score,
            penalty_deducted=penalty_deducted,
            net_score=net_score,
            accuracy_percentage=accuracy,
            estimated_percentile=estimated_percentile,
            merit_bracket=merit_bracket,
            weakness_flags=weakness_flags,
        )

    def subscribe_to_routine(
        self, user_id: str, payload: RoutineSubscribeRequest
    ) -> RoutineSubscribeResponse:
        routine = self.get_routine_by_id(payload.routine_id)
        sub_id = f"sub-{uuid.uuid4().hex[:12]}"
        self._subscriptions[sub_id] = {
            "subscription_id": sub_id,
            "user_id": user_id,
            "routine_id": payload.routine_id,
            "channels": payload.channels,
            "subscribed_at": datetime.now(timezone.utc).isoformat(),
        }
        title_snippet = routine.title if routine else "পরীক্ষার রুটিন"
        return RoutineSubscribeResponse(
            success=True,
            subscription_id=sub_id,
            routine_id=payload.routine_id,
            subscribed_channels=payload.channels,
            message=f"'{title_snippet}' এর জন্য নোটিফিকেশন অ্যালার্ট সফলভাবে সক্রিয় হয়েছে।",
        )


exam_routine_service = ExamRoutineService()
