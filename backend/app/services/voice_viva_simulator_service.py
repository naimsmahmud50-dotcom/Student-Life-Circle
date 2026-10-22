"""
VoiceVivaSimulatorService:
Smart Voice/Audio Viva-Voce Oral Exam & Speech Cadence Simulator.
Prepares students and candidates for BCS Cadre oral exams, BUET/IBA admission vivas,
and corporate technical interviews with real-time speech telemetry and rubric scoring.
Features:
- Category-specific oral examination sessions (BCS_ORAL, BUET_ADMISSION, TECH_BACKEND)
- Speech cadence evaluation (Words-Per-Minute WPM scoring: Optimal, Hesitant, Too Rushed)
- Response latency telemetry and cognitive retrieval delay analysis
- Precision keyword density scoring and actionable coaching rubrics
"""

import uuid
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class VoiceVivaSimulatorService:
    VIVA_QUESTION_BANK = {
        "TECH_BACKEND": [
            {
                "question_id": "viva-tech-01",
                "question_audio_prompt": "Explain how database B-Tree index structures maintain logarithmic lookup efficiency during frequent write operations.",
                "expected_keywords": ["b-tree", "node split", "balancing", "logarithmic", "o(log n)", "disk page"],
                "target_duration_sec": 30.0
            },
            {
                "question_id": "viva-tech-02",
                "question_audio_prompt": "What is the difference between concurrency and parallelism in Python, and how does the GIL affect multithreading?",
                "expected_keywords": ["gil", "global interpreter lock", "io-bound", "cpu-bound", "concurrency", "multiprocessing"],
                "target_duration_sec": 35.0
            }
        ],
        "BCS_ORAL": [
            {
                "question_id": "viva-bcs-01",
                "question_audio_prompt": "How does Bangladesh's graduation from Least Developed Country (LDC) status affect our tariff preferences under WTO rules?",
                "expected_keywords": ["ldc", "wto", "generalised scheme of preferences", "gsp", "export", "tariffs", "diversification"],
                "target_duration_sec": 45.0
            }
        ],
        "BUET_ADMISSION": [
            {
                "question_id": "viva-buet-01",
                "question_audio_prompt": "Explain why the acceleration due to gravity is maximum at the poles and minimum at the equator using rotational kinematics.",
                "expected_keywords": ["centrifugal", "rotation", "equator", "poles", "radius", "angular velocity", "omega"],
                "target_duration_sec": 30.0
            }
        ]
    }

    def __init__(self):
        self._lock = threading.Lock()
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def start_session(
        self,
        student_id: str,
        viva_category: str = "TECH_BACKEND",
        difficulty: str = "INTERMEDIATE"
    ) -> Dict[str, Any]:
        with self._lock:
            cat = viva_category.upper()
            questions = self.VIVA_QUESTION_BANK.get(cat, self.VIVA_QUESTION_BANK["TECH_BACKEND"])
            session_id = f"viva-sess-{uuid.uuid4().hex[:10]}"

            session_record = {
                "session_id": session_id,
                "student_id": student_id,
                "viva_category": cat,
                "difficulty": difficulty.upper(),
                "status": "IN_PROGRESS",
                "questions": questions,
                "evaluations": [],
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            self._sessions[session_id] = session_record
            return session_record

    def evaluate_response(
        self,
        session_id: str,
        question_id: str,
        audio_duration_seconds: float,
        transcribed_text: str,
        response_latency_seconds: float
    ) -> Dict[str, Any]:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                raise ValueError(f"Viva session '{session_id}' not found.")

            # Calculate WPM (Words Per Minute)
            words = transcribed_text.strip().split()
            word_count = len(words)
            duration_min = max(audio_duration_seconds / 60.0, 0.1)
            wpm = round(word_count / duration_min, 1)

            # Cadence rating
            if 110.0 <= wpm <= 165.0:
                cadence_rating = "OPTIMAL"
            elif wpm < 110.0:
                cadence_rating = "HESITANT"
            else:
                cadence_rating = "TOO_RUSHED"

            # Latency penalty: optimal latency is 1.0s to 3.5s
            latency_score = 100.0
            if response_latency_seconds > 3.5:
                latency_score = max(50.0, 100.0 - ((response_latency_seconds - 3.5) * 8.0))

            # Precision scoring (keyword matching)
            q_info = next((q for q in session["questions"] if q["question_id"] == question_id), None)
            expected_keys = q_info["expected_keywords"] if q_info else ["general", "analysis"]

            text_lower = transcribed_text.lower()
            matched = [k for k in expected_keys if k.lower() in text_lower]
            precision_pct = round((len(matched) / len(expected_keys)) * 100.0, 1) if expected_keys else 80.0

            # Fluency score: blend of cadence and latency
            cadence_component = 100.0 if cadence_rating == "OPTIMAL" else (78.0 if cadence_rating == "HESITANT" else 72.0)
            fluency_score = round((cadence_component * 0.6) + (latency_score * 0.4), 1)

            feedback_points = []
            if cadence_rating == "OPTIMAL":
                feedback_points.append(f"Speech cadence is well-paced ({wpm} WPM).")
            elif cadence_rating == "HESITANT":
                feedback_points.append(f"Cadence was hesitant ({wpm} WPM). Practice reducing long speech pauses.")
            else:
                feedback_points.append(f"Cadence was rushed ({wpm} WPM). Articulate complex concepts more deliberately.")

            if response_latency_seconds <= 3.5:
                feedback_points.append(f"Instant conceptual recall (Latency: {response_latency_seconds:.1f}s).")
            else:
                feedback_points.append(f"Noticeable retrieval delay ({response_latency_seconds:.1f}s before speaking).")

            feedback_points.append(f"Covered {len(matched)}/{len(expected_keys)} core technical keywords.")

            eval_record = {
                "question_id": question_id,
                "fluency_score": fluency_score,
                "precision_score": precision_pct,
                "wpm_cadence": wpm,
                "cadence_rating": cadence_rating,
                "response_latency_seconds": round(response_latency_seconds, 2),
                "matched_keywords": matched,
                "feedback": " • ".join(feedback_points)
            }

            session["evaluations"].append(eval_record)
            return eval_record

    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None

            evals = session["evaluations"]
            if not evals:
                return {
                    "session_id": session_id,
                    "student_id": session["student_id"],
                    "category": session["viva_category"],
                    "overall_score": 0.0,
                    "average_fluency": 0.0,
                    "average_latency_sec": 0.0,
                    "question_evaluations": [],
                    "status": session["status"]
                }

            avg_fluency = sum(e["fluency_score"] for e in evals) / len(evals)
            avg_precision = sum(e["precision_score"] for e in evals) / len(evals)
            avg_latency = sum(e["response_latency_seconds"] for e in evals) / len(evals)
            overall = round((avg_fluency * 0.45) + (avg_precision * 0.55), 1)

            return {
                "session_id": session_id,
                "student_id": session["student_id"],
                "category": session["viva_category"],
                "overall_score": overall,
                "average_fluency": round(avg_fluency, 1),
                "average_precision": round(avg_precision, 1),
                "average_latency_sec": round(avg_latency, 2),
                "question_evaluations": evals,
                "status": "COMPLETED" if len(evals) >= len(session["questions"]) else "IN_PROGRESS"
            }


voice_viva_simulator_service = VoiceVivaSimulatorService()
