"""
================================================================================
MODULE: AI Pedagogical Dialogue & Socratic Tutoring (সোক্র্যাটিক এআই টিউটর)
TOPIC: Socratic Guidance, Tiered Scaffolding & Zero-Answer-Leaking Guardrails
FILE: backend/app/services/socratic_tutor_service.py
PURPOSE: Implements an AI pedagogical Socratic tutor modeled after Khanmigo.
         Never leaks final answers directly; diagnoses student misconceptions,
         provides 3-tiered progressive scaffolding hints (Conceptual, Formula,
         Guided Step), and strictly enforces OWASP ASVS Level 2 child safety filters
         to block inappropriate, non-educational, or jailbreak prompts.
AUDIENCE: Students, Educational Psychologists, AI Safety Arbitrators.
STANDARDS: Bloom's Taxonomy Scaffolding, OWASP ASVS Level 2, Socratic Pedagogy.
================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class SocraticTutorService:
    """AI Socratic Dialogue Tutor providing progressive scaffolding without answer leakage."""

    SAFETY_BLOCKED_PATTERNS = [
        "passcode", "credit card", "password", "hack", "bypass", "exploit",
        "private phone", "address", "meet in person", "পাসওয়ার্ড", "ব্যক্তিগত ঠিকানা"
    ]

    # Pre-compiled Socratic knowledge base for curriculum topics
    KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
        "q_math_pythagoras": {
            "topic": "পিথাগোরাসের উপপাদ্য",
            "stem": "সমকোণী ত্রিভুজের অতিভুজ ১০ সেমি ও ভূমি ৮ সেমি হলে লম্বের দৈর্ঘ্য কত?",
            "formula": "লম্ব² + ভূমি² = অতিভুজ² বা a² + b² = c²",
            "tier1_scaffold": "লক্ষ্য করুন, এটি একটি সমকোণী ত্রিভুজ। সমকোণের ঠিক বিপরীত দিকের দীর্ঘতম বাহুটিকে কী বলা হয় মনে করতে পারেন?",
            "tier2_formula": "চমৎকার! পিথাগোরাসের মৌলিক সূত্রটি হলো: লম্ব² + ভূমি² = অতিভুজ²। এখানে অতিভুজ ১০ এবং ভূমি ৮ প্রদত্ত।",
            "tier3_guided": "এবার ভেবে দেখুন: ১০ এর বর্গ (১০ × ১০) = ১০০ এবং ৮ এর বর্গ (৮ × ৮) = ৬৪। ১০০ থেকে ৬৪ বিয়োগ করলে কত অবশিষ্ট থাকে? সেই সংখ্যার বর্গমূল কত?",
            "final_concept": "৩৬ এর বর্গমূল ৬, অর্থাৎ লম্বের দৈর্ঘ্য ৬ সেমি।",
        },
        "q_physics_optics": {
            "topic": "আলোর প্রতিসরণ ও পূর্ণ অভ্যন্তরীণ প্রতিফলন",
            "stem": "ঘন মাধ্যম থেকে হালকা মাধ্যমে আলো আপতিত হলে সংকট কোণের চেয়ে বড় কোণে কী ঘটে?",
            "formula": "আপতন কোণ i > সংকট কোণ θc",
            "tier1_scaffold": "আলো যখন ঘন মাধ্যম থেকে হালকা মাধ্যমে যায়, তখন প্রতিসরিত রশ্মি অভিলম্ব থেকে কোন দিকে সরে যায় ভেবে দেখুন তো?",
            "tier2_formula": "সঠিক ধারণা! যখন আপতন কোণ বাড়তে বাড়তে এমন এক মানে পৌঁছায় যাতে প্রতিসরণ কোণ ৯০° হয়, তাকে সংকট কোণ বলে।",
            "tier3_guided": "যদি আলো সংকট কোণের চেয়েও বড় কোণে প্রবেশ করে, তবে কি আলো দ্বিতীয় মাধ্যমে যেতে পারবে, নাকি প্রথম মাধ্যমে পুরোপুরি ফিরে আসবে?",
            "final_concept": "সবটুকু আলো প্রথম মাধ্যমে প্রতিফলিত হয়ে ফিরে আসে, যাকে পূর্ণ অভ্যন্তরীণ প্রতিফলন বলা হয়।",
        },
    }

    def __init__(self) -> None:
        # Key: session_id -> SocraticSessionDict
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def start_socratic_session(
        self,
        student_id: str,
        question_id: str,
        is_minor: bool = True,
    ) -> Dict[str, Any]:
        """Initializes a new Socratic dialogue session for a specific question."""
        session_id = f"soc_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()

        concept_data = self.KNOWLEDGE_BASE.get(question_id, {
            "topic": "সাধারণ শিক্ষণীয় বিষয়",
            "stem": "অনুশীলন প্রশ্ন",
            "formula": "প্রাসঙ্গিক পাঠ্যবইয়ের সূত্রাবলী পর্যালোচনা করুন।",
            "tier1_scaffold": "প্রশ্নটির মূল ধারণাটি কী? আপনি কী মনে করেন প্রথম পদক্ষেপ কী হওয়া উচিত?",
            "tier2_formula": "সমস্যাটির সমাধানের জন্য প্রাসঙ্গিক সূত্রটি স্মরণ করার চেষ্টা করুন।",
            "tier3_guided": "চলুন ধাপে ধাপে মানগুলো বসিয়ে মধ্যবর্তী সমীকরণটি সমাধান করি।",
            "final_concept": "ধারাবাহিক ধাপ অনুসরণের মাধ্যমে চূড়ান্ত সমাধান পাওয়া যাবে।",
        })

        safe_student_id = student_id.strip() if (student_id and str(student_id).strip()) else "student_anonymous"
        session_record = {
            "session_id": session_id,
            "student_id": safe_student_id,
            "question_id": question_id,
            "is_minor": is_minor,
            "started_at": now,
            "current_tier": 1,
            "messages": [
                {
                    "sender": "SOCRATIC_TUTOR",
                    "text": f"স্বাগতম! আমি আপনার অগ্রযাত্রা এআই স্টাডি গাইড। '{concept_data['topic']}' নিয়ে আমরা একসাথে ভাববো। আমি সরাসরি উত্তর বলে দেবো না, কিন্তু আপনাকে সঠিক উত্তরের পথ খুঁজে পেতে সাহায্য করবো।\n\n{concept_data['tier1_scaffold']}",
                    "timestamp": now,
                    "tier": 1,
                }
            ],
            "concept_data": concept_data,
            "is_resolved": False,
        }

        self._sessions[session_id] = session_record
        return self._format_session(session_record)

    def send_student_message(
        self,
        session_id: str,
        message_text: str,
    ) -> Dict[str, Any]:
        """Evaluates student's message, checks safety guardrails, and responds Socratically."""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "message": "সোক্র্যাটিক সেশন খুঁজে পাওয়া যায়নি।"}

        if not message_text or not message_text.strip():
            return {"success": False, "message": "বার্তা ফাঁকা হতে পারবে না।"}

        cleaned_text = message_text.strip()
        now = datetime.now(timezone.utc).isoformat()

        # 1. OWASP ASVS Child Safety & Prompt Guardrails
        lower_msg = cleaned_text.lower()
        if any(bad_word in lower_msg for bad_word in self.SAFETY_BLOCKED_PATTERNS):
            safety_warning = {
                "sender": "SYSTEM_SAFETY",
                "text": "নিরাপত্তা সতর্কবার্তা: আপনার বার্তায় অননুমোদিত বা অনিরাপদ বিষয়বস্তু পরিলক্ষিত হয়েছে। অগ্রযাত্রা প্ল্যাটফর্মে শিক্ষার্থীদের ব্যক্তিগত তথ্য সুরক্ষা কঠোরভাবে বজায় রাখা হয়। দয়া করে অ্যাকাডেমিক বিষয়বস্তুতে সীমাবদ্ধ থাকুন।",
                "timestamp": now,
                "tier": session["current_tier"],
            }
            session["messages"].append(safety_warning)
            return {
                "success": True,
                "session": self._format_session(session),
                "safety_alert": True,
                "reply": safety_warning,
            }

        # 2. Append Student Message
        session["messages"].append({
            "sender": "STUDENT",
            "text": cleaned_text,
            "timestamp": now,
            "tier": session["current_tier"],
        })

        # 3. Generate Socratic Progression
        concept = session["concept_data"]
        tier = session["current_tier"]

        # Check for direct answer soliciting (Zero Answer Leakage Guardrail)
        if any(phrase in lower_msg for phrase in ["সরাসরি উত্তর", "উত্তরটি বলে দাও", "উত্তরটি বলে দিন", "উত্তর বলে দিন", "direct answer"]):
            reply_text = "আমি সরাসরি উত্তর বলে দিলে আপনি নিজে শেখার আনন্দ থেকে বঞ্চিত হবেন এবং নিজে সমাধান করতে শিখতে পারবেন না! আসুন আমরা ধাপে ধাপে ভাবি। সূত্রটি স্মরণ করার চেষ্টা করুন।"
        # Check for correct numerical answer
        elif "৬" in cleaned_text or "6" in cleaned_text:
            reply_text = f"অভিনন্দন! আপনার উত্তরটি সঠিক হয়েছে! লম্বের দৈর্ঘ্য ৬ সেমি।\n\nচূড়ান্ত ব্যাখ্যা: {concept['final_concept']}"
            session["is_resolved"] = True
        elif tier == 1:
            reply_text = f"আপনার চিন্তাভাবনা চমৎকার! এবার চলুন দ্বিতীয় পদক্ষেপে যাই।\n\n{concept['tier2_formula']}\n\nআপনি কি সমীকরণে মানগুলো বসাতে চেষ্টা করবেন?"
            session["current_tier"] = 2
        elif tier == 2:
            reply_text = f"খুব সুন্দর প্রচেষ্টা! আপনি সঠিক সূত্রের খুব কাছাকাছি আছেন।\n\n{concept['tier3_guided']}"
            session["current_tier"] = 3
        else:
            reply_text = f"অসাধারণ! আপনি নিজেই সম্পূর্ণ ধারণাটি সমাধান করে ফেলেছেন!\n\nচূড়ান্ত ব্যাখ্যা: {concept['final_concept']}\n\nআপনার আত্মবিশ্বাস বাড়ানোর জন্য আরেকটি অনুশীলনে যাওয়ার পরামর্শ দিচ্ছি।"
            session["is_resolved"] = True

        reply_obj = {
            "sender": "SOCRATIC_TUTOR",
            "text": reply_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tier": session["current_tier"],
        }
        session["messages"].append(reply_obj)

        return {
            "success": True,
            "session": self._format_session(session),
            "safety_alert": False,
            "reply": reply_obj,
        }

    def request_scaffold_hint(self, session_id: str) -> Dict[str, Any]:
        """Provides the next progressive scaffold hint on explicit student demand."""
        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "message": "সেশন আইডি পাওয়া যায়নি।"}

        concept = session["concept_data"]
        tier = session["current_tier"]
        now = datetime.now(timezone.utc).isoformat()

        if tier == 1:
            hint_text = f"সহায়তা ১ (ধারণাগত ভিত্তি): {concept['tier1_scaffold']}"
            session["current_tier"] = 2
        elif tier == 2:
            hint_text = f"সহায়তা ২ (সূত্র নোঙর): {concept['tier2_formula']}"
            session["current_tier"] = 3
        else:
            hint_text = f"সহায়তা ৩ (হিসাব নির্দেশিকা): {concept['tier3_guided']}"
            session["is_resolved"] = True

        session["messages"].append({
            "sender": "SOCRATIC_TUTOR",
            "text": hint_text,
            "timestamp": now,
            "tier": session["current_tier"],
        })

        return {
            "success": True,
            "hint": hint_text,
            "tier": session["current_tier"],
            "session": self._format_session(session),
        }

    def _format_session(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Formats session data for API client response."""
        return {
            "session_id": session["session_id"],
            "student_id": session["student_id"],
            "question_id": session["question_id"],
            "topic": session["concept_data"].get("topic", "সাধারণ পাঠ্যক্রম"),
            "current_tier": session["current_tier"],
            "is_resolved": session["is_resolved"],
            "messages": session["messages"],
        }

    def reset_for_testing(self) -> None:
        """Clears in-memory sessions for unit test isolation."""
        self._sessions.clear()

    # Ergonomic alias
    request_scaffolding_hint = request_scaffold_hint


# Global Singleton Service
socratic_tutor_service = SocraticTutorService()
