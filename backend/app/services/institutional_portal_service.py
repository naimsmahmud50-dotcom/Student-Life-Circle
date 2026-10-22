"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Institutional White-Label Portal & Teacher Cockpit Service
TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
FILE:      backend/app/services/institutional_portal_service.py
PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
PURPOSE:   Provides multi-tenant school/college isolation, custom subdomain routing
           (e.g., ndc.ogrojatra.edu.bd), teacher RBAC privileges, central exam scheduling,
           section gradebook administration, and statistical performance analytics.
STANDARDS: UI/UX Pro Max, Pure Academic Design, Multi-Tenant Security, Strict Zero-Emoji
========================================================================================
"""

import math
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple


class InstitutionalException(Exception):
    """Base exception for institutional portal and multi-tenant errors."""
    pass


class TenantNotFoundException(InstitutionalException):
    """Raised when an institution or subdomain cannot be resolved."""
    pass


class TenantAccessDeniedException(InstitutionalException):
    """Raised when cross-tenant access is attempted."""
    pass


class ExamSchedulingException(InstitutionalException):
    """Raised when exam authoring or publishing fails validation."""
    pass


class InstitutionalPortalService:
    """
    Core service managing multi-tenant educational institutions, teacher workflows,
    central exam scheduling, section-wide analytics, and score approvals.
    """

    EXAM_STATUS_DRAFT = "DRAFT"
    EXAM_STATUS_PUBLISHED = "PUBLISHED"
    EXAM_STATUS_COMPLETED = "COMPLETED"

    GRADE_STATUS_PENDING = "PENDING_APPROVAL"
    GRADE_STATUS_APPROVED = "GRADES_APPROVED"

    def __init__(self):
        self._institutions: Dict[str, Dict[str, Any]] = {}
        self._sections: Dict[str, Dict[str, Any]] = {}
        self._teachers: Dict[str, Dict[str, Any]] = {}
        self._exams: Dict[str, Dict[str, Any]] = {}
        self._gradebooks: Dict[str, Dict[str, Any]] = {}
        self._init_seed_institutions()

    def _init_seed_institutions(self) -> None:
        """Seeds premier institutions and default sections."""
        # 1. Notre Dame College
        self._institutions["inst-ndc-dhaka"] = {
            "institution_id": "inst-ndc-dhaka",
            "legal_name": "Notre Dame College, Dhaka",
            "name_bn": "নটর ডেম কলেজ, ঢাকা",
            "subdomain": "ndc",
            "custom_domain": "ndc.ogrojatra.edu.bd",
            "eiin_number": "108274",
            "division": "Dhaka",
            "theme_accent": "#0A2540",
            "created_at": 1729000000,
        }

        # 2. Dhaka College
        self._institutions["inst-dc-dhaka"] = {
            "institution_id": "inst-dc-dhaka",
            "legal_name": "Dhaka College",
            "name_bn": "ঢাকা কলেজ",
            "subdomain": "dc",
            "custom_domain": "dc.ogrojatra.edu.bd",
            "eiin_number": "107977",
            "division": "Dhaka",
            "theme_accent": "#065F46",
            "created_at": 1729000000,
        }

        # 3. Rajuk Uttara Model College
        self._institutions["inst-rumc-dhaka"] = {
            "institution_id": "inst-rumc-dhaka",
            "legal_name": "Rajuk Uttara Model College",
            "name_bn": "রাজউক উত্তরা মডেল কলেজ",
            "subdomain": "rumc",
            "custom_domain": "rumc.ogrojatra.edu.bd",
            "eiin_number": "108573",
            "division": "Dhaka",
            "theme_accent": "#1E3A8A",
            "created_at": 1729000000,
        }

        # Seed Teachers
        self._teachers["tch-ndc-physics-01"] = {
            "teacher_id": "tch-ndc-physics-01",
            "institution_id": "inst-ndc-dhaka",
            "full_name": "Dr. Sushanta Roy",
            "designation": "Senior Lecturer in Physics",
            "assigned_sections": ["sec-ndc-hsc26-a", "sec-ndc-hsc26-b"],
        }
        self._teachers["tch-dc-chem-01"] = {
            "teacher_id": "tch-dc-chem-01",
            "institution_id": "inst-dc-dhaka",
            "full_name": "Prof. A. K. Azad",
            "designation": "Associate Professor of Chemistry",
            "assigned_sections": ["sec-dc-hsc26-1"],
        }

        # Seed Sections
        self._sections["sec-ndc-hsc26-a"] = {
            "section_id": "sec-ndc-hsc26-a",
            "institution_id": "inst-ndc-dhaka",
            "section_name": "Section A (Science)",
            "section_name_bn": "শাখা ক (বিজ্ঞান)",
            "class_grade": 11,
            "academic_year": "2025-2026",
            "student_count": 65,
            "assigned_teacher_id": "tch-ndc-physics-01",
        }
        self._sections["sec-ndc-hsc26-b"] = {
            "section_id": "sec-ndc-hsc26-b",
            "institution_id": "inst-ndc-dhaka",
            "section_name": "Section B (Science)",
            "section_name_bn": "শাখা খ (বিজ্ঞান)",
            "class_grade": 11,
            "academic_year": "2025-2026",
            "student_count": 62,
            "assigned_teacher_id": "tch-ndc-physics-01",
        }
        self._sections["sec-dc-hsc26-1"] = {
            "section_id": "sec-dc-hsc26-1",
            "institution_id": "inst-dc-dhaka",
            "section_name": "Section 1 (Science)",
            "section_name_bn": "শাখা ০১ (বিজ্ঞান)",
            "class_grade": 11,
            "academic_year": "2025-2026",
            "student_count": 70,
            "assigned_teacher_id": "tch-dc-chem-01",
        }

        # Seed an Active Exam for NDC Section A
        now = int(time.time())
        exam_id = "exam-ndc-phys-midterm-01"
        self._exams[exam_id] = {
            "exam_id": exam_id,
            "institution_id": "inst-ndc-dhaka",
            "section_id": "sec-ndc-hsc26-a",
            "teacher_id": "tch-ndc-physics-01",
            "title_bn": "পদার্থবিজ্ঞান ১ম পত্র সেকশন মডেল টেস্ট — ১ম পর্ব",
            "title_en": "Physics 1st Paper Mid-Term Section Assessment",
            "subject": "Physics",
            "subject_bn": "পদার্থবিজ্ঞান",
            "paper": "1st",
            "duration_minutes": 60,
            "total_marks": 50,
            "due_timestamp": now + 86400 * 3,
            "status": self.EXAM_STATUS_PUBLISHED,
            "question_ids": ["nctb_hsc_phys1_dhaka_2024_cq_01", "nctb_hsc_phys_dhk_2022_mcq_01"],
            "created_at": now - 3600,
        }

        # Seed Gradebook for NDC Section A
        self._gradebooks[f"{exam_id}:sec-ndc-hsc26-a"] = {
            "exam_id": exam_id,
            "section_id": "sec-ndc-hsc26-a",
            "institution_id": "inst-ndc-dhaka",
            "status": self.GRADE_STATUS_PENDING,
            "approved_by": None,
            "approved_at": None,
            "records": [
                {
                    "student_id": "stu-ndc-101",
                    "roll_number": "101",
                    "student_name": "Tanvir Ahmed",
                    "marks_obtained": 46.5,
                    "attendance_percent": 98.0,
                    "submitted_at": now - 1800,
                    "feedback_bn": "বলবিদ্যা ও ব্যাংকিং কোণের প্রয়োগ অত্যন্ত চমৎকার হয়েছে।",
                },
                {
                    "student_id": "stu-ndc-102",
                    "roll_number": "102",
                    "student_name": "Sajid Karim",
                    "marks_obtained": 42.0,
                    "attendance_percent": 95.0,
                    "submitted_at": now - 2200,
                    "feedback_bn": "ভরবেগের সংরক্ষণশীলতার ব্যাখ্যায় আরও স্পষ্টতা প্রয়োজন।",
                },
                {
                    "student_id": "stu-ndc-103",
                    "roll_number": "103",
                    "student_name": "Abrar Fahad",
                    "marks_obtained": 48.0,
                    "attendance_percent": 100.0,
                    "submitted_at": now - 1200,
                    "feedback_bn": "নিখুঁত গাণিতিক বিশ্লেষণ ও চিত্র উপস্থাপন।",
                },
                {
                    "student_id": "stu-ndc-104",
                    "roll_number": "104",
                    "student_name": "Nafis Imtiaz",
                    "marks_obtained": 38.5,
                    "attendance_percent": 91.0,
                    "submitted_at": now - 2500,
                    "feedback_bn": "ঘর্ষণ বল ও মন্দন গণনায় অসতর্ক ভুল সংশোধন করো।",
                },
                {
                    "student_id": "stu-ndc-105",
                    "roll_number": "105",
                    "student_name": "Mahir Faysal",
                    "marks_obtained": 44.0,
                    "attendance_percent": 96.0,
                    "submitted_at": now - 1500,
                    "feedback_bn": "উচ্চতর দক্ষতা অংশে ভালো সিদ্ধান্ত দিয়েছ।",
                },
            ],
            "weak_topics": [
                {
                    "topic_name_bn": "ঘর্ষণ বল ও জড়তার ভ্রামক গণনা",
                    "accuracy_percent": 48.5,
                    "remedial_tip_bn": "সমান্তরাল অক্ষ উপপাদ্য ও লম্ব অক্ষ উপপাদ্যের পার্থক্য পুনরাবৃত্তি করুন।",
                },
                {
                    "topic_name_bn": "ব্যাংকিং কোণে নিরাপদ বেগ বিশ্লেষণ",
                    "accuracy_percent": 56.0,
                    "remedial_tip_bn": "tan(theta) = v^2/rg সূত্রের প্রয়োগ আরও অনুশীলন আবশ্যক।",
                },
            ],
        }

    def resolve_institution(self, identifier: str) -> Dict[str, Any]:
        """
        Resolves an institution by its institution_id or subdomain (e.g. 'ndc' or 'ndc.ogrojatra.edu.bd').
        """
        clean = identifier.strip().lower()

        # Check by ID
        if clean in self._institutions:
            return self._institutions[clean]

        # Check by subdomain
        for inst in self._institutions.values():
            if inst["subdomain"].lower() == clean:
                return inst
            if inst["custom_domain"].lower() == clean:
                return inst

        raise TenantNotFoundException(f"Institution tenant with identifier '{identifier}' could not be resolved.")

    def get_sections(self, institution_id: str) -> List[Dict[str, Any]]:
        """Returns all sections belonging to the verified tenant."""
        self.resolve_institution(institution_id)
        return [sec for sec in self._sections.values() if sec["institution_id"] == institution_id]

    def get_exams(self, institution_id: str, section_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns exams created within the institution scope."""
        self.resolve_institution(institution_id)
        exams = [ex for ex in self._exams.values() if ex["institution_id"] == institution_id]
        if section_id:
            exams = [ex for ex in exams if ex["section_id"] == section_id]
        return sorted(exams, key=lambda x: x["created_at"], reverse=True)

    def create_exam(
        self,
        institution_id: str,
        teacher_id: str,
        section_id: str,
        title_bn: str,
        subject: str,
        paper: str,
        duration_minutes: int,
        total_marks: int,
        due_timestamp: int,
        question_ids: List[str],
        title_en: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Authors a new model test for a specific section.
        Enforces tenant isolation and teacher verification.
        """
        inst = self.resolve_institution(institution_id)

        # Verify section belongs to institution
        section = self._sections.get(section_id)
        if not section or section["institution_id"] != institution_id:
            raise TenantAccessDeniedException(f"Section '{section_id}' does not belong to institution '{institution_id}'.")

        # Verify teacher belongs to institution
        teacher = self._teachers.get(teacher_id)
        if not teacher or teacher["institution_id"] != institution_id:
            raise TenantAccessDeniedException(f"Teacher '{teacher_id}' is not affiliated with institution '{institution_id}'.")

        exam_id = f"exam-{inst['subdomain']}-{uuid.uuid4().hex[:8]}"
        now = int(time.time())

        exam_record = {
            "exam_id": exam_id,
            "institution_id": institution_id,
            "section_id": section_id,
            "teacher_id": teacher_id,
            "title_bn": title_bn,
            "title_en": title_en or title_bn,
            "subject": subject,
            "subject_bn": subject,
            "paper": paper,
            "duration_minutes": duration_minutes,
            "total_marks": total_marks,
            "due_timestamp": due_timestamp,
            "status": self.EXAM_STATUS_DRAFT,
            "question_ids": question_ids,
            "created_at": now,
        }

        self._exams[exam_id] = exam_record
        return exam_record

    def publish_exam(self, institution_id: str, exam_id: str, teacher_id: str) -> Dict[str, Any]:
        """
        Publishes a scheduled model test ("পরীক্ষার প্রশ্ন প্রকাশ করুন").
        Transitions exam status from DRAFT to PUBLISHED.
        """
        self.resolve_institution(institution_id)
        exam = self._exams.get(exam_id)
        if not exam:
            raise ExamSchedulingException(f"Exam '{exam_id}' not found.")

        if exam["institution_id"] != institution_id:
            raise TenantAccessDeniedException("Cross-tenant exam publication attempt blocked.")

        exam["status"] = self.EXAM_STATUS_PUBLISHED
        exam["published_at"] = int(time.time())
        return exam

    def get_section_gradebook(
        self,
        institution_id: str,
        section_id: str,
        exam_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the section gradebook and marks roster with strict tenant scope.
        """
        self.resolve_institution(institution_id)
        section = self._sections.get(section_id)
        if not section or section["institution_id"] != institution_id:
            raise TenantAccessDeniedException("Cross-tenant gradebook access blocked.")

        # Find gradebook
        target_key = None
        for key, gb in self._gradebooks.items():
            if gb["institution_id"] == institution_id and gb["section_id"] == section_id:
                if not exam_id or gb["exam_id"] == exam_id:
                    target_key = key
                    break

        if not target_key:
            # Return empty template
            return {
                "institution_id": institution_id,
                "section_id": section_id,
                "exam_id": exam_id or "none",
                "status": self.GRADE_STATUS_PENDING,
                "records": [],
                "weak_topics": [],
            }

        return self._gradebooks[target_key]

    def approve_grades(
        self,
        institution_id: str,
        section_id: str,
        exam_id: str,
        teacher_id: str,
    ) -> Dict[str, Any]:
        """
        Teacher confirms and signs off section grades ("নম্বর অনুমোদন করুন").
        """
        self.resolve_institution(institution_id)
        key = f"{exam_id}:{section_id}"
        gradebook = self._gradebooks.get(key)
        if not gradebook:
            raise InstitutionalException(f"Gradebook for exam '{exam_id}' and section '{section_id}' not found.")

        if gradebook["institution_id"] != institution_id:
            raise TenantAccessDeniedException("Cross-tenant gradebook approval blocked.")

        now = int(time.time())
        gradebook["status"] = self.GRADE_STATUS_APPROVED
        gradebook["approved_by"] = teacher_id
        gradebook["approved_at"] = now
        return gradebook

    def get_section_analytics(
        self,
        institution_id: str,
        section_id: str,
        exam_id: str,
    ) -> Dict[str, Any]:
        """
        Computes section performance distribution without student public shaming:
        - examinee count
        - mean average score
        - median score
        - standard deviation (spread of understanding)
        - distribution brackets (4 tiers: <40%, 40-59%, 60-79%, 80-100%)
        - weak topic clusters with pedagogical remedial tips
        """
        self.resolve_institution(institution_id)
        key = f"{exam_id}:{section_id}"
        gradebook = self._gradebooks.get(key)
        if not gradebook:
            raise InstitutionalException(f"Gradebook data for exam '{exam_id}' not found.")

        if gradebook["institution_id"] != institution_id:
            raise TenantAccessDeniedException("Cross-tenant analytics access blocked.")

        records = gradebook.get("records", [])
        if not records:
            return {
                "total_examinees": 0,
                "average_score": 0.0,
                "median_score": 0.0,
                "standard_deviation": 0.0,
                "highest_score": 0.0,
                "lowest_score": 0.0,
                "distribution_brackets": {"tier_below_40": 0, "tier_40_59": 0, "tier_60_79": 0, "tier_80_100": 0},
                "weak_topics": [],
            }

        scores = [r["marks_obtained"] for r in records]
        n = len(scores)
        mean_score = sum(scores) / n

        # Median
        sorted_scores = sorted(scores)
        if n % 2 == 1:
            median_score = sorted_scores[n // 2]
        else:
            median_score = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2.0

        # Standard Deviation
        variance = sum((s - mean_score) ** 2 for s in scores) / n
        std_dev = math.sqrt(variance)

        # Brackets (assuming 50 total marks baseline)
        brackets = {"tier_below_40": 0, "tier_40_59": 0, "tier_60_79": 0, "tier_80_100": 0}
        for s in scores:
            pct = (s / 50.0) * 100.0
            if pct < 40:
                brackets["tier_below_40"] += 1
            elif pct < 60:
                brackets["tier_40_59"] += 1
            elif pct < 80:
                brackets["tier_60_79"] += 1
            else:
                brackets["tier_80_100"] += 1

        return {
            "total_examinees": n,
            "average_score": round(mean_score, 2),
            "median_score": round(median_score, 2),
            "standard_deviation": round(std_dev, 2),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "distribution_brackets": brackets,
            "weak_topics": gradebook.get("weak_topics", []),
        }


# Global singleton instance
institutional_portal_service = InstitutionalPortalService()
