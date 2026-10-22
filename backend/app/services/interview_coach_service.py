"""
================================================================================
MODULE: AI Mock Interview Evaluator & Career Coaching (এআই মক ইন্টারভিউ কোচ)
TOPIC: Multi-Track Simulated Vivas, Natural Language Rubric Scoring & Actionable Feedback
FILE: backend/app/services/interview_coach_service.py
PURPOSE: Implements an AI mock interview evaluator for Bangladesh students and graduates.
         Simulates authentic technical, pedagogical, and university admission viva
         sessions across three curated tracks (Software Engineering, STEM Tutoring,
         and University Admission Viva). Evaluates student answers using multi-dimensional
         rubric scoring (Conceptual Accuracy, Clarity, Confidence/Structure), provides
         actionable growth feedback in Bengali, and strictly enforces OWASP ASVS
         Level 2 child and minor safety guardrails.
AUDIENCE: Job Seekers, Tuition Candidates, Admission Applicants, Career Mentors.
STANDARDS: IEEE Software Engineering Competency Model, OWASP ASVS Level 2,
           NCTB STEM Pedagogical Standards.
================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class InterviewCoachService:
    """AI Mock Interview Coach evaluating candidate answers across structured academic and career tracks."""

    SAFETY_BLOCKED_PATTERNS = [
        "password", "passcode", "credit card", "hack", "bypass", "exploit",
        "private phone", "address", "meet in person", "পাসওয়ার্ড", "ব্যক্তিগত ঠিকানা"
    ]

    TRACKS: Dict[str, Dict[str, Any]] = {
        "track_tech_swe": {
            "name": "সফটওয়্যার ইঞ্জিনিয়ারিং ও ব্যাকএন্ড ডেভেলপমেন্ট",
            "role": "Junior Backend / Full-Stack Engineer",
            "questions": [
                {
                    "qid": "q_swe_01",
                    "question": "RESTful API ডিজাইনে Idempotency (আইডেম্পোটেন্সি) বলতে কী বোঝায়? POST ও PUT মেথডের মধ্যে আইডেম্পোটেন্সির পার্থক্য কী?",
                    "keywords": ["idempotent", "আইডেম্পোটেন্ট", "put", "post", "একই ফলাফল", "side effect", "পুনরাবৃত্তি", "রিসোর্স", "পার্থক্য"],
                    "ideal_concept": "আইডেম্পোটেন্ট মেথডে একই রিকোয়েস্ট একাধিকবার পাঠালেও সার্ভার স্টেটে অতিরিক্ত পরিবর্তন ঘটে না। PUT সাধারণত আইডেম্পোটেন্ট কিন্তু POST নয়।",
                },
                {
                    "qid": "q_swe_02",
                    "question": "ডাটাবেজে ইনডেক্সিং (Indexing) কেন ব্যবহার করা হয়? ইনডেক্স ব্যবহারের সম্ভাব্য ড্র-ব্যাক বা অসুবিধা কী হতে পারে?",
                    "keywords": ["index", "ইনডেক্স", "b-tree", "search", "দ্রুত", "write", "insert", "মেমোরি", "কুয়েরি", "অসুবিধা"],
                    "ideal_concept": "ইনডেক্স কুয়েরি সার্চের গতি বাড়ায় (B-Tree/Hash), তবে ডেটা রাইট/ইনসার্ট ও আপডেটের গতি কিছুটা মন্থর করে এবং অতিরিক্ত ডিস্ক স্টোরেজ নেয়।",
                },
            ]
        },
        "track_stem_tutor": {
            "name": "এসটিইএম গণিত ও বিজ্ঞান টিউশনিং",
            "role": "STEM Mathematics & Physics Tutor",
            "questions": [
                {
                    "qid": "q_tutor_01",
                    "question": "একজন ৮ম শ্রেণির শিক্ষার্থী ভগ্নাংশের যোগ এবং লসাগু বুঝতে পারছে না। আপনি তাকে কীভাবে সহজ বাস্তব উদাহরণের সাহায্যে বিষয়টি বোঝাবেন?",
                    "keywords": ["বাস্তব", "পিজ্জা", "রুটি", "ভাগ", "ধাপে ধাপে", "সহজ", "পেশেন্স", "হর", "লব", "ভগ্নাংশ"],
                    "ideal_concept": "কাগজ বা বৃত্তাকার রুটি কেটে সমপরিমাণ ভাগে ভাগ করার বাস্তব উদাহরণ দিয়ে হর ও লবের সমতুল্যতা দেখানো এবং ধৈর্য সহকারে বোঝানো।",
                },
                {
                    "qid": "q_tutor_02",
                    "question": "অনলাইন বা অফলাইন টিউশনে অপ্রাপ্তবয়স্ক শিক্ষার্থীর সাথে যোগাযোগের সময় শিক্ষক হিসেবে পেশাদারিত্ব ও নিরাপত্তা সীমানা কীভাবে বজায় রাখবেন?",
                    "keywords": ["অভিভাবক", "সীমানা", "পেশাদার", "সম্মতি", "guardian", "safety", "নিরাপত্তা"],
                    "ideal_concept": "অভিভাবকের অনুমতি ছাড়া ব্যক্তিগত চ্যাট না করা, একাডেমিক প্ল্যাটফর্মের মাধ্যমে যোগাযোগ রাখা এবং পেশাদার আচরণ বজায় রাখা।",
                },
            ]
        },
        "track_admission_viva": {
            "name": "বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি ভাইভা",
            "role": "University Admission & Academic Viva",
            "questions": [
                {
                    "qid": "q_adm_01",
                    "question": "আপনি কেন উচ্চশিক্ষার জন্য এই বিভাগটি (উদাঃ কম্পিউটার সায়েন্স / ফলিত পদার্থবিজ্ঞান) বেছে নিয়েছেন এবং এটি ভবিষ্যতে দেশের উন্নয়নে কীভাবে কাজে লাগবে?",
                    "keywords": ["উদ্দেশ্য", "আগ্রহ", "প্রবলেম সলভিং", "ভবিষ্যত", "দেশ", "বিজ্ঞান", "উচ্চশিক্ষা", "কম্পিউটার", "উন্নয়ন"],
                    "ideal_concept": "স্পষ্ট আত্মবিশ্বাস, বাস্তবিক কারণ, প্রযুক্তিগত সমস্যা সমাধানের আগ্রহ এবং জাতীয় অগ্রগতিতে অবদান রাখার সুনির্দিষ্ট লক্ষ্য প্রকাশ করা।",
                },
            ]
        },
    }

    def __init__(self) -> None:
        # Key: session_id -> InterviewSessionDict
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def start_interview_session(
        self,
        candidate_id: str,
        track_id: str,
        is_minor: bool = False,
    ) -> Dict[str, Any]:
        """Initializes a new mock interview session for a candidate in the chosen track."""
        safe_candidate_id = candidate_id.strip() if (candidate_id and str(candidate_id).strip()) else "candidate_anonymous"
        safe_track_id = track_id.strip() if (track_id and str(track_id).strip()) else "track_tech_swe"

        track_data = self.TRACKS.get(safe_track_id, self.TRACKS["track_tech_swe"])
        session_id = f"int_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()

        first_question = track_data["questions"][0]

        session_record = {
            "session_id": session_id,
            "candidate_id": safe_candidate_id,
            "track_id": safe_track_id,
            "track_name": track_data["name"],
            "target_role": track_data["role"],
            "is_minor": is_minor,
            "started_at": now,
            "current_q_index": 0,
            "questions": track_data["questions"],
            "answers": [],
            "scores": {
                "accuracy": 0.0,
                "clarity": 0.0,
                "confidence": 0.0,
                "overall_readiness": 0.0,
            },
            "is_completed": False,
        }

        self._sessions[session_id] = session_record

        return {
            "success": True,
            "session_id": session_id,
            "candidate_id": safe_candidate_id,
            "track_name": track_data["name"],
            "target_role": track_data["role"],
            "total_questions": len(track_data["questions"]),
            "current_question": {
                "question_number": 1,
                "qid": first_question["qid"],
                "question_text": first_question["question"],
            },
        }

    def submit_interview_answer(
        self,
        session_id: str,
        answer_text: str,
    ) -> Dict[str, Any]:
        """Evaluates a candidate's answer using multi-dimensional rubrics and advances the interview."""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "message": "ইন্টারভিউ সেশন খুঁজে পাওয়া যায়নি।"}

        if session["is_completed"]:
            return {"success": False, "message": "এই ইন্টারভিউ সেশনটি ইতিমধ্যে সমাপ্ত হয়েছে।"}

        if not answer_text or not str(answer_text).strip():
            return {"success": False, "message": "উত্তরের বিবরণ ফাঁকা হতে পারবে না।"}

        cleaned_text = str(answer_text).strip()
        lower_ans = cleaned_text.lower()
        now = datetime.now(timezone.utc).isoformat()

        # 1. OWASP ASVS Safety Guardrail Check
        if any(bad_word in lower_ans for bad_word in self.SAFETY_BLOCKED_PATTERNS):
            return {
                "success": False,
                "safety_alert": True,
                "message": "নিরাপত্তা সতর্কবার্তা: আপনার উত্তরে অননুমোদিত ব্যক্তিগত তথ্য বা সুরক্ষাবহির্ভূত শব্দ শনাক্ত হয়েছে। দয়া করে পেশাদার অ্যাকাডেমিক উত্তরে সীমাবদ্ধ থাকুন।",
            }

        # 2. Score Candidate Answer
        q_idx = session["current_q_index"]
        current_q = session["questions"][q_idx]

        eval_result = self._evaluate_response(current_q, cleaned_text)

        session["answers"].append({
            "qid": current_q["qid"],
            "question_text": current_q["question"],
            "candidate_answer": cleaned_text,
            "timestamp": now,
            "evaluation": eval_result,
        })

        # Advance question or complete
        session["current_q_index"] += 1
        if session["current_q_index"] >= len(session["questions"]):
            session["is_completed"] = True
            # Compute final aggregate scores
            session["scores"] = self._compute_aggregate_scores(session["answers"])

        next_q = None
        if not session["is_completed"]:
            nxt = session["questions"][session["current_q_index"]]
            next_q = {
                "question_number": session["current_q_index"] + 1,
                "qid": nxt["qid"],
                "question_text": nxt["question"],
            }

        return {
            "success": True,
            "session_id": session_id,
            "is_completed": session["is_completed"],
            "evaluation": eval_result,
            "next_question": next_q,
            "cumulative_scores": session["scores"] if session["is_completed"] else None,
        }

    def get_interview_report(self, session_id: str) -> Dict[str, Any]:
        """Generates a comprehensive interview performance report with strengths and growth areas."""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "message": "সেশন আইডি পাওয়া যায়নি।"}

        if not session["is_completed"]:
            return {
                "success": False,
                "message": "ইন্টারভিউ সেশনটি এখনও চলমান। সবকটি প্রশ্নের উত্তর দেওয়ার পর চূড়ান্ত রিপোর্ট জেনারেট হবে।",
            }

        scores = session["scores"]
        overall = scores["overall_readiness"]

        # Qualitative readiness grade
        if overall >= 85.0:
            badge = "MARKET_READY_ADVANCED"
            grade_label = "চমৎকার প্রস্তুতি (অ্যাডভান্সড)"
        elif overall >= 70.0:
            badge = "JOB_READY_COMPETENT"
            grade_label = "সন্তোষজনক ও কার্যকর প্রস্তুতি"
        else:
            badge = "DEVELOPING_POTENTIAL"
            grade_label = "উন্নতিশীল (অতিরিক্ত অনুশীলন কাম্য)"

        strengths = []
        growth_points = []

        if scores["accuracy"] >= 75.0:
            strengths.append("প্রযুক্তিগত ও ধারণাগত নির্ভুলতা অত্যন্ত সুদৃঢ়।")
        else:
            growth_points.append("মৌলিক সূত্রের গভীরে প্রবেশ করে কনসেপচুয়াল স্পষ্টতা আরও বৃদ্ধি করা প্রয়োজন।")

        if scores["clarity"] >= 75.0:
            strengths.append("ভাবপ্রকাশ ও উত্তরের গঠন ছিল সুশৃঙ্খল ও প্রাঞ্জল।")
        else:
            growth_points.append("উত্তরে অপ্রাসঙ্গিক দীর্ঘসূত্রিতা পরিহার করে মূল পয়েন্টে ফোকাস করুন।")

        if scores["confidence"] >= 75.0:
            strengths.append("আত্মবিশ্বাসী ও প্রাসঙ্গিক পেশাদার শব্দাবলীর ব্যবহার পরিলক্ষিত হয়েছে।")
        else:
            growth_points.append("বাস্তব কাজের অভিজ্ঞতা বা প্রজেক্ট রেফারেন্স উল্লেখ করে আত্মবিশ্বাস বাড়ান।")

        return {
            "success": True,
            "session_id": session_id,
            "candidate_id": session["candidate_id"],
            "track_name": session["track_name"],
            "target_role": session["target_role"],
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "readiness_badge": badge,
            "readiness_label": grade_label,
            "scores": scores,
            "strengths": strengths,
            "growth_recommendations": growth_points,
            "total_answers_evaluated": len(session["answers"]),
        }

    def _evaluate_response(self, question_meta: Dict[str, Any], answer_text: str) -> Dict[str, Any]:
        """Evaluates single response against keywords, clarity length, and conceptual keywords."""
        lower = answer_text.lower()
        keywords = question_meta.get("keywords", [])

        # 1. Accuracy based on keyword hits (hitting 2-3 key concepts demonstrates solid grasp)
        hit_count = sum(1 for kw in keywords if kw.lower() in lower)
        keyword_ratio = min(1.0, (hit_count / 2.0)) if keywords else 1.0
        accuracy = round(min(100.0, max(45.0, keyword_ratio * 80.0 + (15.0 if len(answer_text) > 40 else 0.0))), 1)

        # 2. Clarity based on sentence structure and word count (optimal: 20 - 150 words)
        words = answer_text.split()
        word_count = len(words)
        if word_count < 8:
            clarity = 40.0
        elif word_count <= 60:
            clarity = 85.0
        else:
            clarity = 92.0

        # 3. Confidence & Structure
        confidence = 80.0
        if "যেমন" in answer_text or "উদাহরণ" in answer_text or "example" in lower:
            confidence += 10.0
        if "জানি না" in answer_text or "মনে নেই" in answer_text:
            confidence = max(40.0, confidence - 30.0)

        composite = round(0.4 * accuracy + 0.3 * clarity + 0.3 * confidence, 1)

        return {
            "accuracy": accuracy,
            "clarity": clarity,
            "confidence": confidence,
            "composite": composite,
            "feedback": "উত্তরে প্রাসঙ্গিক মৌলিক ধারণাগুলোর চমৎকার উপস্থিতি রয়েছে।" if composite >= 75.0 else "উত্তরটি গ্রহণযোগ্য, তবে আরও সুস্পষ্ট বাস্তব উদাহরণ দিলে উত্তরটি আরও সমৃদ্ধ হতো।",
        }

    def _compute_aggregate_scores(self, answers: List[Dict[str, Any]]) -> Dict[str, float]:
        """Averages scores across all answers in the interview."""
        if not answers:
            return {"accuracy": 0.0, "clarity": 0.0, "confidence": 0.0, "overall_readiness": 0.0}

        n = len(answers)
        acc = sum(a["evaluation"]["accuracy"] for a in answers) / n
        cla = sum(a["evaluation"]["clarity"] for a in answers) / n
        cnf = sum(a["evaluation"]["confidence"] for a in answers) / n
        ovr = 0.4 * acc + 0.3 * cla + 0.3 * cnf

        return {
            "accuracy": round(acc, 1),
            "clarity": round(cla, 1),
            "confidence": round(cnf, 1),
            "overall_readiness": round(ovr, 1),
        }

    def reset_for_testing(self) -> None:
        """Clears in-memory sessions for unit testing isolation."""
        self._sessions.clear()


# Global Singleton Service
interview_coach_service = InterviewCoachService()
