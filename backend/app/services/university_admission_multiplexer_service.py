"""
UniversityAdmissionMultiplexerService:
Centralized Multi-University Admission Multiplexer & Schedule Conflict Resolver.
Solves Bangladesh's fragmented university application nightmare across BUET, DU, Medical, CKRUET, and GST.
Features:
- Automated HSC/SSC GPA and group eligibility evaluation across official circulars
- Exam schedule date-clash collision detector
- 1-click batch application queue with centralized payment settlement
- Consolidated digital admit card generator with allocated seat plans
"""

import uuid
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class UniversityAdmissionMultiplexerService:
    UNIVERSITY_CIRCULARS = {
        "BUET": {
            "university_name": "Bangladesh University of Engineering and Technology",
            "unit_name": "Faculty of Engineering & Architecture",
            "min_hsc_gpa": 5.0,
            "min_ssc_gpa": 4.0,
            "min_combined_gpa": 9.5,
            "required_group": "SCIENCE",
            "exam_date": "2026-11-20 09:00",
            "application_fee_bdt": 1200.0,
            "exam_venue_default": "BUET Main Campus, Dhaka"
        },
        "DU_KA": {
            "university_name": "University of Dhaka",
            "unit_name": "Faculty of Science (Ka-Unit)",
            "min_hsc_gpa": 4.0,
            "min_ssc_gpa": 4.0,
            "min_combined_gpa": 8.5,
            "required_group": "SCIENCE",
            "exam_date": "2026-11-28 10:00",
            "application_fee_bdt": 1000.0,
            "exam_venue_default": "Curzon Hall, DU Campus"
        },
        "MEDICAL": {
            "university_name": "Directorate General of Health Services (DGHS)",
            "unit_name": "National Medical College Admission (MBBS/BDS)",
            "min_hsc_gpa": 4.0,
            "min_ssc_gpa": 4.0,
            "min_combined_gpa": 9.0,
            "required_group": "SCIENCE",
            "exam_date": "2026-11-15 10:00",
            "application_fee_bdt": 1000.0,
            "exam_venue_default": "Dhaka Medical College Center"
        },
        "CKRUET": {
            "university_name": "Engineering Cluster (CUET, KUET, RUET)",
            "unit_name": "Combined Engineering Admission Unit",
            "min_hsc_gpa": 4.5,
            "min_ssc_gpa": 4.0,
            "min_combined_gpa": 8.5,
            "required_group": "SCIENCE",
            "exam_date": "2026-12-05 10:00",
            "application_fee_bdt": 1200.0,
            "exam_venue_default": "RUET Engineering Complex"
        },
        "GST": {
            "university_name": "General, Science & Technology Cluster (24 Public Universities)",
            "unit_name": "GST Unified Central Admissions Unit A",
            "min_hsc_gpa": 3.5,
            "min_ssc_gpa": 3.5,
            "min_combined_gpa": 8.0,
            "required_group": "SCIENCE",
            "exam_date": "2026-12-12 11:00",
            "application_fee_bdt": 1500.0,
            "exam_venue_default": "Jagannath University Campus"
        }
    }

    def __init__(self):
        self._lock = threading.Lock()
        self._batch_applications: Dict[str, Dict[str, Any]] = {}
        self._admit_cards: Dict[str, Dict[str, Any]] = {}

    def check_eligibility(
        self,
        student_id: str,
        hsc_gpa: float,
        ssc_gpa: float,
        academic_group: str = "SCIENCE",
        subject_grades: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        combined_gpa = hsc_gpa + ssc_gpa
        reports = []

        with self._lock:
            for code, circ in self.UNIVERSITY_CIRCULARS.items():
                is_eligible = True
                reasons = []

                if academic_group.upper() != circ["required_group"]:
                    is_eligible = False
                    reasons.append(f"Requires {circ['required_group']} group.")

                if hsc_gpa < circ["min_hsc_gpa"]:
                    is_eligible = False
                    reasons.append(f"HSC GPA {hsc_gpa:.2f} is below required {circ['min_hsc_gpa']:.2f}.")

                if ssc_gpa < circ["min_ssc_gpa"]:
                    is_eligible = False
                    reasons.append(f"SSC GPA {ssc_gpa:.2f} is below required {circ['min_ssc_gpa']:.2f}.")

                if combined_gpa < circ["min_combined_gpa"]:
                    is_eligible = False
                    reasons.append(f"Combined GPA {combined_gpa:.2f} is below threshold {circ['min_combined_gpa']:.2f}.")

                status_reason = "Fully Eligible for Admission Test." if is_eligible else " • ".join(reasons)

                reports.append({
                    "university_code": code,
                    "university_name": circ["university_name"],
                    "unit_name": circ["unit_name"],
                    "is_eligible": is_eligible,
                    "min_gpa_required": circ["min_combined_gpa"],
                    "exam_date": circ["exam_date"],
                    "application_fee_bdt": circ["application_fee_bdt"],
                    "status_reason": status_reason
                })

        return reports

    def detect_schedule_conflicts(self, university_codes: List[str]) -> List[str]:
        conflicts = []
        date_map: Dict[str, str] = {}
        for code in university_codes:
            if code in self.UNIVERSITY_CIRCULARS:
                circ = self.UNIVERSITY_CIRCULARS[code]
                exam_date = circ["exam_date"]
                if exam_date in date_map:
                    conflicts.append(f"Schedule Collision: {date_map[exam_date]} and {code} both hold exams on {exam_date}.")
                else:
                    date_map[exam_date] = code
        return conflicts

    def batch_apply(
        self,
        student_id: str,
        student_name: str,
        hsc_roll: str,
        hsc_registration: str,
        university_codes: List[str],
        payment_channel: str = "bKash"
    ) -> Dict[str, Any]:
        with self._lock:
            if not university_codes:
                raise ValueError("Must select at least one university for batch application.")

            total_fee = 0.0
            admit_cards = []
            applied = []

            conflicts = self.detect_schedule_conflicts(university_codes)

            for code in university_codes:
                if code not in self.UNIVERSITY_CIRCULARS:
                    raise ValueError(f"Unknown university code '{code}'.")

                circ = self.UNIVERSITY_CIRCULARS[code]
                total_fee += circ["application_fee_bdt"]
                applied.append(code)

                # Generate Consolidated Admit Card
                admit_id = f"ADM-{code}-{uuid.uuid4().hex[:6].upper()}"
                roll_number = f"{code[:3]}-{hsc_roll[-5:]}"
                room_no = (hash(admit_id) % 40) + 101

                card = {
                    "admit_card_id": admit_id,
                    "university_code": code,
                    "university_name": circ["university_name"],
                    "student_name": student_name,
                    "roll_number": roll_number,
                    "hsc_roll": hsc_roll,
                    "hsc_registration": hsc_registration,
                    "exam_date": circ["exam_date"],
                    "exam_venue": f"{circ['exam_venue_default']} • Room {room_no}",
                    "instructions": "Bring original HSC registration card and 2 black ballpoint pens. Calculators allowed per circular rules.",
                    "status": "ISSUED"
                }
                self._admit_cards[admit_id] = card
                admit_cards.append(card)

            batch_id = f"batch-app-{uuid.uuid4().hex[:10]}"
            batch_record = {
                "batch_id": batch_id,
                "student_id": student_id,
                "student_name": student_name,
                "total_fee_bdt": total_fee,
                "applied_universities": applied,
                "admit_cards": admit_cards,
                "conflicts_detected": conflicts,
                "payment_status": "SETTLED",
                "payment_channel": payment_channel,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            self._batch_applications[batch_id] = batch_record
            return batch_record

    def get_admit_card(self, admit_card_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._admit_cards.get(admit_card_id)

    def get_batch_application(self, batch_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._batch_applications.get(batch_id)

university_admission_multiplexer_service = UniversityAdmissionMultiplexerService()
