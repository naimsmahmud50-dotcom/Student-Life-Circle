"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Institutional Teacher Cockpit
TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
FILE:      backend/tests/test_phase114_institutional_teacher_cockpit.py
PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
PURPOSE:   Automated unit and integration test suite certifying multi-tenant school
           isolation, custom subdomain routing, teacher exam scheduling and publishing,
           section gradebook approvals, and privacy-preserving statistical analytics.
STANDARDS: OWASP ASVS L2, Multi-Tenant Isolation, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import json
import os
import re
import unittest
from pathlib import Path

from backend.app.services.institutional_portal_service import (
    InstitutionalPortalService,
    institutional_portal_service,
    TenantNotFoundException,
    TenantAccessDeniedException,
    ExamSchedulingException,
    InstitutionalException,
)


class TestPhase114InstitutionalTeacherCockpit(unittest.TestCase):
    """
    Test suite certifying Phase 114 Institutional White-Label Portal and Teacher Cockpit.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.service_file = cls.root_dir / "backend" / "app" / "services" / "institutional_portal_service.py"
        cls.endpoints_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "institution.py"
        cls.frontend_card = cls.root_dir / "frontend" / "src" / "components" / "institution" / "SectionAnalyticsCard.tsx"
        cls.frontend_cockpit = cls.root_dir / "frontend" / "src" / "components" / "institution" / "InstitutionalTeacherCockpit.tsx"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def setUp(self):
        # Create a fresh isolated service instance for each test
        self.service = InstitutionalPortalService()

    def test_01_multi_tenant_isolation_and_subdomain_resolution(self):
        """Verifies multi-tenant school/college isolation and subdomain routing."""
        # 1. Resolve NDC by ID, subdomain, and custom domain
        inst_by_id = self.service.resolve_institution("inst-ndc-dhaka")
        self.assertEqual(inst_by_id["institution_id"], "inst-ndc-dhaka")
        self.assertEqual(inst_by_id["subdomain"], "ndc")
        self.assertEqual(inst_by_id["eiin_number"], "108274")

        inst_by_subdomain = self.service.resolve_institution("ndc")
        self.assertEqual(inst_by_subdomain["institution_id"], "inst-ndc-dhaka")

        inst_by_fqdn = self.service.resolve_institution("ndc.ogrojatra.edu.bd")
        self.assertEqual(inst_by_fqdn["institution_id"], "inst-ndc-dhaka")

        # 2. Resolve Dhaka College
        inst_dc = self.service.resolve_institution("dc")
        self.assertEqual(inst_dc["institution_id"], "inst-dc-dhaka")
        self.assertEqual(inst_dc["eiin_number"], "107977")

        # 3. Non-existent tenant resolution fails
        with self.assertRaises(TenantNotFoundException):
            self.service.resolve_institution("non-existent-college")

        # 4. Section retrieval strictly scoped to tenant
        ndc_sections = self.service.get_sections("inst-ndc-dhaka")
        self.assertEqual(len(ndc_sections), 2)
        ndc_section_ids = {s["section_id"] for s in ndc_sections}
        self.assertIn("sec-ndc-hsc26-a", ndc_section_ids)
        self.assertIn("sec-ndc-hsc26-b", ndc_section_ids)
        self.assertNotIn("sec-dc-hsc26-1", ndc_section_ids)

        dc_sections = self.service.get_sections("inst-dc-dhaka")
        self.assertEqual(len(dc_sections), 1)
        self.assertEqual(dc_sections[0]["section_id"], "sec-dc-hsc26-1")

    def test_02_teacher_exam_scheduling_and_publishing_workflow(self):
        """Verifies model test authoring, scheduling, and publication workflow."""
        # 1. Teacher creates a new section exam in DRAFT state
        exam = self.service.create_exam(
            institution_id="inst-ndc-dhaka",
            teacher_id="tch-ndc-physics-01",
            section_id="sec-ndc-hsc26-a",
            title_bn="পদার্থবিজ্ঞান ১ম পত্র অধ্যায়ভিত্তিক মূল্যায়ন",
            subject="Physics",
            paper="1st",
            duration_minutes=45,
            total_marks=50,
            due_timestamp=1730000000,
            question_ids=["nctb_cq_01", "nctb_mcq_01"],
        )
        self.assertEqual(exam["status"], self.service.EXAM_STATUS_DRAFT)
        self.assertEqual(exam["institution_id"], "inst-ndc-dhaka")
        self.assertEqual(exam["section_id"], "sec-ndc-hsc26-a")

        # 2. Cross-tenant exam creation attempt: NDC teacher trying to create exam in Dhaka College section
        with self.assertRaises(TenantAccessDeniedException):
            self.service.create_exam(
                institution_id="inst-ndc-dhaka",
                teacher_id="tch-ndc-physics-01",
                section_id="sec-dc-hsc26-1",  # belongs to Dhaka College!
                title_bn="অবৈধ অ্যাক্সেস পরীক্ষা",
                subject="Physics",
                paper="1st",
                duration_minutes=60,
                total_marks=50,
                due_timestamp=1730000000,
                question_ids=["q1"],
            )

        # 3. Publish Exam ("পরীক্ষার প্রশ্ন প্রকাশ করুন")
        published_exam = self.service.publish_exam(
            institution_id="inst-ndc-dhaka",
            exam_id=exam["exam_id"],
            teacher_id="tch-ndc-physics-01",
        )
        self.assertEqual(published_exam["status"], self.service.EXAM_STATUS_PUBLISHED)
        self.assertIn("published_at", published_exam)

        # 4. Cross-tenant publish attempt: Dhaka College cannot publish NDC exam
        with self.assertRaises(TenantAccessDeniedException):
            self.service.publish_exam(
                institution_id="inst-dc-dhaka",
                exam_id=exam["exam_id"],
                teacher_id="tch-dc-chem-01",
            )

    def test_03_section_gradebook_and_teacher_score_approval(self):
        """Verifies section gradebook marks roster retrieval and teacher approval workflow."""
        exam_id = "exam-ndc-phys-midterm-01"
        section_id = "sec-ndc-hsc26-a"

        # 1. Retrieve gradebook
        gradebook = self.service.get_section_gradebook("inst-ndc-dhaka", section_id, exam_id)
        self.assertEqual(gradebook["status"], self.service.GRADE_STATUS_PENDING)
        self.assertEqual(len(gradebook["records"]), 5)
        self.assertIsNone(gradebook["approved_by"])

        # 2. Cross-tenant gradebook access blocked
        with self.assertRaises(TenantAccessDeniedException):
            self.service.get_section_gradebook("inst-dc-dhaka", section_id, exam_id)

        # 3. Teacher confirms and signs off section grades ("নম্বর অনুমোদন করুন")
        approved_gradebook = self.service.approve_grades(
            institution_id="inst-ndc-dhaka",
            section_id=section_id,
            exam_id=exam_id,
            teacher_id="tch-ndc-physics-01",
        )
        self.assertEqual(approved_gradebook["status"], self.service.GRADE_STATUS_APPROVED)
        self.assertEqual(approved_gradebook["approved_by"], "tch-ndc-physics-01")
        self.assertIsNotNone(approved_gradebook["approved_at"])

        # 4. Cross-tenant approval blocked
        with self.assertRaises(TenantAccessDeniedException):
            self.service.approve_grades(
                institution_id="inst-dc-dhaka",
                section_id=section_id,
                exam_id=exam_id,
                teacher_id="tch-dc-chem-01",
            )

    def test_04_section_analytics_statistics_and_weak_topics(self):
        """Verifies section statistical analytics (mean, median, std dev, weak topics) without student shaming."""
        exam_id = "exam-ndc-phys-midterm-01"
        section_id = "sec-ndc-hsc26-a"

        analytics = self.service.get_section_analytics("inst-ndc-dhaka", section_id, exam_id)

        # Examinee metrics
        self.assertEqual(analytics["total_examinees"], 5)
        self.assertEqual(analytics["average_score"], 43.8)
        self.assertEqual(analytics["median_score"], 44.0)
        self.assertEqual(analytics["standard_deviation"], 3.36)
        self.assertEqual(analytics["highest_score"], 48.0)
        self.assertEqual(analytics["lowest_score"], 38.5)

        # 4 Tiers Distribution brackets
        brackets = analytics["distribution_brackets"]
        self.assertEqual(brackets["tier_80_100"], 4)
        self.assertEqual(brackets["tier_60_79"], 1)
        self.assertEqual(brackets["tier_40_59"], 0)
        self.assertEqual(brackets["tier_below_40"], 0)

        # Diagnostic weak topics
        weak_topics = analytics["weak_topics"]
        self.assertEqual(len(weak_topics), 2)
        topic_names = [wt["topic_name_bn"] for wt in weak_topics]
        self.assertIn("ঘর্ষণ বল ও জড়তার ভ্রামক গণনা", topic_names)
        self.assertIn("ব্যাংকিং কোণে নিরাপদ বেগ বিশ্লেষণ", topic_names)

        # Privacy Mandate: No public individual ranking shaming
        self.assertNotIn("rank", analytics)
        self.assertNotIn("leaderboard", analytics)

    def test_05_frontend_components_integrity_and_tactile_styling(self):
        """Verifies frontend components exist and declare tactile 3D Oxford Navy button styling."""
        self.assertTrue(self.frontend_card.exists(), "SectionAnalyticsCard.tsx must exist.")
        self.assertTrue(self.frontend_cockpit.exists(), "InstitutionalTeacherCockpit.tsx must exist.")

        card_code = self.frontend_card.read_text(encoding="utf-8")
        cockpit_code = self.frontend_cockpit.read_text(encoding="utf-8")

        # Check tactile 3D Oxford Navy buttons
        self.assertIn("shadow-[0_4px_0_0_#0A2540]", cockpit_code)
        self.assertIn("active:translate-y-1", cockpit_code)
        self.assertIn("active:shadow-none", cockpit_code)

        # Check Bengali action buttons
        self.assertIn("পরীক্ষার প্রশ্ন প্রকাশ করুন", cockpit_code)
        self.assertIn("নম্বর অনুমোদন করুন", cockpit_code)

        # Check 4-tab workflow labels
        self.assertIn("চলমান ও প্রকাশিত পরীক্ষা", cockpit_code)
        self.assertIn("শাখা গ্রেডবুক ও ডায়াগনস্টিক", cockpit_code)
        self.assertIn("প্রশ্নপত্র সংকলন ও শিডিউলার", cockpit_code)
        self.assertIn("শিক্ষার্থী তালিকা ও হাজিরা", cockpit_code)

        # Check pure Lucide SVG vector icons in cockpit and card
        self.assertIn("School", cockpit_code)
        self.assertIn("Users", cockpit_code)
        self.assertIn("GraduationCap", cockpit_code)
        self.assertIn("FileCheck", cockpit_code)
        self.assertIn("BarChart3", cockpit_code)
        self.assertIn("BarChart3", card_code)

        # Check Section Analytics Card features
        self.assertIn("গড় নম্বর (Mean)", card_code)
        self.assertIn("মধ্যমা (Median)", card_code)
        self.assertIn("পরিমিত ব্যবধান (Std Dev)", card_code)
        self.assertIn("দুর্বল বিষয় ক্লাস্টার", card_code)
        self.assertIn("গোপনীয়তা সুরক্ষিত", card_code)

    def test_06_developer_architecture_notes_and_strict_zero_emoji(self):
        """Asserts Developer Architecture Notes and strict zero-emoji compliance on all Phase 114 files."""
        target_files = [
            self.service_file,
            self.endpoints_file,
            self.frontend_card,
            self.frontend_cockpit,
            Path(__file__).resolve(),
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")

            # Check header
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {file_path.name} missing Developer Architecture Note header.",
            )

            # Check zero emojis
            matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {file_path.name} violates strict Zero Emoji policy: found {matches}",
            )


if __name__ == "__main__":
    unittest.main()
