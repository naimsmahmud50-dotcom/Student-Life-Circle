"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Live Examination & Nationwide Competitive Elevation
TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
FILE:      backend/tests/test_phase142_live_mcq_elevation.py
PHASE:     Phase 142 - Live MCQ Competitive Elevation
PURPOSE:   Automated unit test suite validating Live MCQ reverse-engineered features:
           heroV2 night cosmos & aurora drift, category track selector, demo exam box (dxb),
           4-step pathway (how), 14-feature suite, interactive digital OMR simulator,
           dynamic notice board, multi-track routine matrix, subject weightage breakdown,
           mentors & Hall of Fame panel, candidate FAQ, and regression safety.
STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
"""

import os
import re
import unittest
from pathlib import Path

# Unicode Emoji regex detector
EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27ff]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u203c\u2049\u20e3\u2122\u2139\u2194-\u2199\u21a9-\u21aa\u25aa-\u25ab\u25b6\u25c0\u25fb-\u25fe]"
)

class TestPhase142LiveMcqElevation(unittest.TestCase):
    """Validates Phase 142 Live MCQ competitive elevation components and regressions."""

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.components_dir = cls.root_dir / "frontend" / "src" / "components" / "live-challenge"
        cls.pages_dir = cls.root_dir / "frontend" / "src" / "pages"
        cls.specs_dir = cls.root_dir / "specs" / "045-live-mcq-competitive-elevation"

        cls.files_to_check = [
            cls.components_dir / "LiveMcqHeroSection.tsx",
            cls.components_dir / "LiveCategoryTrackSelector.tsx",
            cls.components_dir / "LiveFreeDemoExamBox.tsx",
            cls.components_dir / "LiveHowItWorksPathway.tsx",
            cls.components_dir / "LiveMentorAndHallOfFame.tsx",
            cls.components_dir / "LiveMcqFaqAccordion.tsx",
            cls.components_dir / "LiveExamRoutineMatrix.tsx",
            cls.components_dir / "SubjectWeightageBreakdown.tsx",
            cls.components_dir / "ExamRulesProtocolModal.tsx",
            cls.components_dir / "LiveExamAnalyticsCard.tsx",
            cls.components_dir / "LiveMcqFeatureShowcase.tsx",
            cls.components_dir / "InteractiveOmrSimulator.tsx",
            cls.components_dir / "DynamicInfoNoticeBoard.tsx",
            cls.pages_dir / "live-challenge.tsx",
            cls.components_dir / "AcademicHeroMotif2D.tsx",
            cls.components_dir / "LiveChallengeEditorial.module.css",
            cls.components_dir / "detect3DCapability.ts",
            cls.components_dir / "Scene3DSlot.tsx",
            cls.components_dir / "TestHarnessScene3D.tsx",
            cls.components_dir / "AcademicArmillaryScene3D.tsx",
            cls.components_dir / "AcademicLeaderboardReveal.tsx",
            cls.specs_dir / "spec.md",
            cls.specs_dir / "plan.md",
            cls.specs_dir / "tasks.md",
        ]

    def test_01_mandatory_architecture_note_headers(self):
        """Asserts that all Phase 142 files contain the mandatory architecture note header."""
        for file_path in self.files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path} must exist.")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {file_path.name} is missing mandatory architecture note header."
            )
            self.assertIn(
                "Phase 142",
                content,
                f"File {file_path.name} must declare Phase 142 in header."
            )

    def test_02_strict_zero_emoji_compliance(self):
        """Verifies that zero unicode emojis exist across all Phase 142 files."""
        for file_path in self.files_to_check:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_REGEX.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"Emoji violation in {file_path.name}: found {matches}"
            )

    def test_03_routine_matrix_structure_and_citations(self):
        """Verifies multi-track tabs, temporal groupings, and textbook citations in LiveExamRoutineMatrix."""
        routine_file = self.components_dir / "LiveExamRoutineMatrix.tsx"
        self.assertTrue(routine_file.exists())
        content = routine_file.read_text(encoding="utf-8")

        # 5 academic tracks
        self.assertIn("hsc_science", content)
        self.assertIn("ssc_board", content)
        self.assertIn("admission", content)
        self.assertIn("olympiad", content)
        self.assertIn("bcs_job", content)

        # 3 temporal tabs
        self.assertIn("আজকের পরীক্ষা", content)
        self.assertIn("আগামীকালের রুটিন", content)
        self.assertIn("আর্কাইভ ও মেধা তালিকা", content)

        # Textbook citations and academic references
        self.assertIn("সিলেবাস রেফারেন্স:", content)
        self.assertIn("এনসিটিবি", content)
        self.assertIn("নেগেটিভ:", content)
        self.assertIn("#991B1B", content, "Negative badge must use Burgundy Crimson #991B1B.")

    def test_04_subject_weightage_breakdown_formulas(self):
        """Verifies chapter proportional distribution and marking formulas in SubjectWeightageBreakdown."""
        weightage_file = self.components_dir / "SubjectWeightageBreakdown.tsx"
        self.assertTrue(weightage_file.exists())
        content = weightage_file.read_text(encoding="utf-8")

        # Proportional chapters
        self.assertIn("নিউটোনীয় বলবিদ্যা", content)
        self.assertIn("কাজ, শক্তি ও ক্ষমতা", content)
        self.assertIn("পদার্থের গাঠনিক ধর্ম", content)

        # Marking formulas
        self.assertIn("+১.০", content, "Must declare +1.0 for correct answers.")
        self.assertIn("-০.২৫", content, "Must declare -0.25 penalty for wrong answers.")
        self.assertIn("১০.০", content, "Must declare 10.0 pass mark.")
        self.assertIn("১৮.৫+", content, "Must declare 18.5+ projected cut-off.")
        self.assertIn("#991B1B", content, "Negative formula card must feature Burgundy Crimson #991B1B.")

    def test_05_exam_rules_protocol_modal_accessibility_and_anti_cheat(self):
        """Verifies WCAG accessibility attributes and 5 core anti-cheat rules in ExamRulesProtocolModal."""
        modal_file = self.components_dir / "ExamRulesProtocolModal.tsx"
        self.assertTrue(modal_file.exists())
        content = modal_file.read_text(encoding="utf-8")

        # Accessibility
        self.assertIn('role="dialog"', content)
        self.assertIn('aria-modal="true"', content)
        self.assertIn("Escape", content, "Must handle Escape key.")

        # 5 anti-cheat and ethics rules
        self.assertIn("সার্ভার-অথরিটেটিভ টাইমার", content)
        self.assertIn("অ্যান্টি-চিট গার্ড ও ট্যাব পরিবর্তন সতর্কতা", content)
        self.assertIn("৩. নেগেটিভ মার্কিং পদ্ধতি (-০.২৫)", content)
        self.assertIn("অফলাইন বাফার ও মিলি-সেকেন্ড নেটওয়ার্ক রেজিলিয়েন্স", content)
        self.assertIn("গোপনীয়তা ও ছদ্মনাম লিডারবোর্ড", content)

    def test_06_analytics_card_and_revision_queue_toggle(self):
        """Verifies national percentiles and spaced repetition revision queue toggle in LiveExamAnalyticsCard."""
        card_file = self.components_dir / "LiveExamAnalyticsCard.tsx"
        self.assertTrue(card_file.exists())
        content = card_file.read_text(encoding="utf-8")

        self.assertIn("জাতীয় পারসেন্টাইল ও রিভিশন কিউ", content)
        self.assertIn("টপ ১% জাতীয় মেধা", content)
        self.assertIn("প্রত্যাশিত কাট-মার্ক", content)
        self.assertIn("ভুল উত্তরের স্মার্ট রিভিশন কিউ", content)

    def test_07_live_mcq_fourteen_features_suite(self):
        """Verifies all 14 elevated Live MCQ features and filter categories in LiveMcqFeatureShowcase."""
        feat_file = self.components_dir / "LiveMcqFeatureShowcase.tsx"
        self.assertTrue(feat_file.exists())
        content = feat_file.read_text(encoding="utf-8")

        # All 14 signature features
        required_features = [
            "smart_search",
            "topic_guru",
            "omr_mode",
            "vocab_booster",
            "info_vault",
            "job_admission_sol",
            "central_result",
            "quiz_master",
            "dynamic_panel",
            "wrong_unanswered",
            "central_archive",
            "offline_vault",
            "my_section",
            "multiplayer_battle"
        ]
        for feat in required_features:
            self.assertIn(feat, content, f"Feature {feat} must be defined in LiveMcqFeatureShowcase.")

        # Filter categories
        self.assertIn("সমস্ত ফিচার", content)
        self.assertIn("লাইভ পরীক্ষা ও ওএমআর", content)
        self.assertIn("স্মার্ট স্টাডি ও রিভিশন", content)
        self.assertIn("অ্যানালিটিক্স ও মেধা", content)

    def test_08_interactive_omr_simulator_mechanics(self):
        """Verifies bubble rows, negative marking calculation, and evaluation in InteractiveOmrSimulator."""
        omr_file = self.components_dir / "InteractiveOmrSimulator.tsx"
        self.assertTrue(omr_file.exists())
        content = omr_file.read_text(encoding="utf-8")

        # Bubbles and marking rules
        self.assertIn("ডিজিটাল ওএমআর শিট মোড", content)
        self.assertIn("correct * 1.0 - wrong * 0.25", content)
        self.assertIn("রিসেট শিট", content)
        self.assertIn("ওএমআর মূল্যায়ন করুন", content)

    def test_09_dynamic_notice_board(self):
        """Verifies real-time syllabus alerts and notice ticker in DynamicInfoNoticeBoard."""
        notice_file = self.components_dir / "DynamicInfoNoticeBoard.tsx"
        self.assertTrue(notice_file.exists())
        content = notice_file.read_text(encoding="utf-8")

        self.assertIn("ডাইনামিক ইনফো প্যানেল ও শিক্ষাবোর্ড নোটিশ", content)
        self.assertIn("অলিম্পিয়াড ২০২৬ পর্ব ০১", content)
        self.assertIn("এনসিটিবি", content)

    def test_10_live_challenge_page_integration_and_regression_safety(self):
        """Verifies seamless integration into live-challenge.tsx and zero regression of existing contracts."""
        page_file = self.pages_dir / "live-challenge.tsx"
        self.assertTrue(page_file.exists())
        content = page_file.read_text(encoding="utf-8")

        # Component imports & renderings
        self.assertIn("LiveMcqHeroSection", content)
        self.assertIn("LiveCategoryTrackSelector", content)
        self.assertIn("LiveFreeDemoExamBox", content)
        self.assertIn("LiveHowItWorksPathway", content)
        self.assertIn("LiveMentorAndHallOfFame", content)
        self.assertIn("LiveMcqFaqAccordion", content)
        self.assertIn("LiveExamRoutineMatrix", content)
        self.assertIn("SubjectWeightageBreakdown", content)
        self.assertIn("ExamRulesProtocolModal", content)
        self.assertIn("LiveExamAnalyticsCard", content)
        self.assertIn("LiveMcqFeatureShowcase", content)
        self.assertIn("InteractiveOmrSimulator", content)
        self.assertIn("DynamicInfoNoticeBoard", content)

        # Regressions guard - all existing tested attributes
        self.assertIn("apiClient.getLiveChallenges", content)
        self.assertIn("apiClient.getLiveLeaderboard", content)
        self.assertIn("useAuthStore", content)
        self.assertIn("animate-pulse", content)
        self.assertIn("#991B1B", content)

    def test_11_live_mcq_hero_and_track_selector(self):
        """Verifies Hero V2 cosmos aurora, 4 trust KPIs, platform ecosystem, and category selector."""
        hero_file = self.components_dir / "LiveMcqHeroSection.tsx"
        self.assertTrue(hero_file.exists())
        hero_content = hero_file.read_text(encoding="utf-8")

        # 4 trust KPIs
        self.assertIn("২৩ লাখ+", hero_content)
        self.assertIn("৭.৫ লাখ+", hero_content)
        self.assertIn("৩০ হাজার+", hero_content)
        self.assertIn("১০+ বছর", hero_content)

        # Platform ecosystem
        self.assertIn("Android", hero_content)
        self.assertIn("iOS", hero_content)
        self.assertIn("Windows", hero_content)
        self.assertIn("macOS", hero_content)

        # Required Playwright elements
        self.assertIn("সার্ভার-অথরিটেটিভ টাইমার", hero_content)
        self.assertIn("মিলি-সেকেন্ড একুরেট বাফার", hero_content)
        self.assertIn("প্রতিযোগী শিক্ষার্থী লাইভ লবিতে যুক্ত", hero_content)
        self.assertIn("পরীক্ষায় অংশগ্রহণ করুন", hero_content)

        # Category track selector
        track_file = self.components_dir / "LiveCategoryTrackSelector.tsx"
        self.assertTrue(track_file.exists())
        track_content = track_file.read_text(encoding="utf-8")
        self.assertIn("বিসিএস (BCS)", track_content)
        self.assertIn("ব্যাংক নিয়োগ (Bank)", track_content)
        self.assertIn("এইচএসসি বিজ্ঞান ও গণিত (HSC)", track_content)
        self.assertIn("বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি", track_content)
        self.assertIn("জাতীয় স্টেম অলিম্পিয়াড (Olympiad)", track_content)

    def test_12_demo_exam_pathway_and_mentors_and_faq(self):
        """Verifies demo exam specs, 4-step pathway, mentor panel, and FAQ accordion."""
        # Demo exam box
        dxb_file = self.components_dir / "LiveFreeDemoExamBox.tsx"
        self.assertTrue(dxb_file.exists())
        dxb_content = dxb_file.read_text(encoding="utf-8")
        self.assertIn("ফ্রি ডেমো", dxb_content)
        self.assertIn("২০", dxb_content)
        self.assertIn("১৫", dxb_content)
        self.assertIn("-০.২৫", dxb_content)

        # 4-step pathway
        how_file = self.components_dir / "LiveHowItWorksPathway.tsx"
        self.assertTrue(how_file.exists())
        how_content = how_file.read_text(encoding="utf-8")
        self.assertIn("০১", how_content)
        self.assertIn("০২", how_content)
        self.assertIn("০৩", how_content)
        self.assertIn("০৪", how_content)
        self.assertIn("ইনস্টল ও রেজিস্ট্রেশন", how_content)
        self.assertIn("লক্ষ্য নির্ধারণ করুন", how_content)
        self.assertIn("নিয়মিত Study ও স্মার্ট রিভিশন", how_content)
        self.assertIn("নিয়মিত লাইভ পরীক্ষা ও ওএমআর", how_content)

        # Mentors & Hall of Fame
        mentor_file = self.components_dir / "LiveMentorAndHallOfFame.tsx"
        self.assertTrue(mentor_file.exists())
        mentor_content = mentor_file.read_text(encoding="utf-8")
        self.assertIn("৪০তম বিসিএস (প্রশাসন ক্যাডার)", mentor_content)
        self.assertIn("বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (বুয়েট - সিএসই)", mentor_content)
        self.assertIn("হল অফ ফেম", mentor_content)

        # FAQ Accordion
        faq_file = self.components_dir / "LiveMcqFaqAccordion.tsx"
        self.assertTrue(faq_file.exists())
        faq_content = faq_file.read_text(encoding="utf-8")
        self.assertIn("সচরাচর জিজ্ঞাসা • FAQ", faq_content)
        self.assertIn("নেগেটিভ মার্কিং পদ্ধতি", faq_content)

    def test_13_3d_capability_detection_and_runtime_guards(self):
        """Verifies detect3DCapability module structure, constants, and defensive fallbacks."""
        cap_file = self.components_dir / "detect3DCapability.ts"
        self.assertTrue(cap_file.exists())
        cap_content = cap_file.read_text(encoding="utf-8")

        # Required storage keys and events
        self.assertIn("STORAGE_KEY_3D_DISABLED", cap_content)
        self.assertIn("ogrojatra_live_challenge_3d_disabled", cap_content)

        # 8 core capability guard reasons
        self.assertIn("LOW_DEVICE_MEMORY", cap_content)
        self.assertIn("LOW_CPU_CONCURRENCY", cap_content)
        self.assertIn("SAVE_DATA_ACTIVE", cap_content)
        self.assertIn("SLOW_NETWORK_TIER", cap_content)
        self.assertIn("PREFERS_REDUCED_MOTION", cap_content)
        self.assertIn("TAB_HIDDEN", cap_content)
        self.assertIn("USER_OPTED_OUT", cap_content)
        self.assertIn("WEBGL_UNAVAILABLE", cap_content)
        self.assertIn("BENCHMARK_STUTTER", cap_content)

        # Functions
        self.assertIn("checkStatic3DCapability", cap_content)
        self.assertIn("runFrameTimeBenchmark", cap_content)
        self.assertIn("evaluate3DCapability", cap_content)
        self.assertIn("getUser3DPreference", cap_content)
        self.assertIn("setUser3DPreference", cap_content)

    def test_14_scene_3d_slot_architecture_and_zero_cls_guarantee(self):
        """Verifies Scene3DSlot zero-CLS wrapper, dynamic chunk loading, and runtime protection."""
        slot_file = self.components_dir / "Scene3DSlot.tsx"
        self.assertTrue(slot_file.exists())
        slot_content = slot_file.read_text(encoding="utf-8")

        # Zero-CLS fallback motif
        self.assertIn("AcademicHeroMotif2D", slot_content)

        # Dynamic import / client-only SSR guard
        self.assertIn("dynamic(", slot_content)
        self.assertIn("ssr: false", slot_content)

        # Runtime protections: context lost, FPS downgrade, tab visibility, manual toggle
        self.assertIn("webglcontextlost", slot_content)
        self.assertIn("LOW_FPS_DOWNGRADE", slot_content)
        self.assertIn("visibilitychange", slot_content)
        self.assertIn("handleTogglePreference", slot_content)
        self.assertIn("Scene3DErrorBoundary", slot_content)

        # Hero section integration
        hero_file = self.components_dir / "LiveMcqHeroSection.tsx"
        hero_content = hero_file.read_text(encoding="utf-8")
        self.assertIn("Scene3DSlot", hero_content)

    def test_15_academic_armillary_scene_3d_procedural_integrity(self):
        """Verifies Three.js procedural Armillary Scene, lighting, props, and zero-leak disposal."""
        scene_file = self.components_dir / "AcademicArmillaryScene3D.tsx"
        self.assertTrue(scene_file.exists())
        scene_content = scene_file.read_text(encoding="utf-8")

        # Three.js import and procedural geometry
        self.assertIn("import * as THREE from 'three';", scene_content)
        self.assertIn("THREE.TorusGeometry", scene_content)
        self.assertIn("THREE.CylinderGeometry", scene_content)
        self.assertIn("THREE.SphereGeometry", scene_content)
        self.assertIn("THREE.BoxGeometry", scene_content)

        # Studio lighting rig
        self.assertIn("THREE.DirectionalLight", scene_content)
        self.assertIn("THREE.PointLight", scene_content)
        self.assertIn("THREE.AmbientLight", scene_content)
        self.assertIn("THREE.PCFSoftShadowMap", scene_content)

        # Props: treatises, brass stylus pen, Bangladesh marker
        self.assertIn("book1Group", scene_content)
        self.assertIn("stylusGroup", scene_content)
        self.assertIn("bangladeshMarker", scene_content)
        self.assertIn("plinthMesh", scene_content)

        # Performance & leak-free lifecycle
        self.assertIn("Math.min(window.devicePixelRatio || 1, 1.5)", scene_content)
        self.assertIn("IntersectionObserver", scene_content)
        self.assertIn("webglcontextlost", scene_content)
        self.assertIn("geometry.dispose()", scene_content)
        self.assertIn("material.dispose()", scene_content)
        self.assertIn("renderer.dispose()", scene_content)
        self.assertIn("renderer.forceContextLoss()", scene_content)

    def test_16_moments_countdown_reactivity_and_dignified_leaderboard_reveal(self):
        """Verifies real-timer 3D reactivity, waiting room beacon, and dignified Motion leaderboard reveal."""
        # 1. 3D Timer reactivity
        scene_file = self.components_dir / "AcademicArmillaryScene3D.tsx"
        scene_content = scene_file.read_text(encoding="utf-8")
        self.assertIn("timeRemainingSeconds", scene_content)
        self.assertIn("isLastMinute", scene_content)
        self.assertIn("isExamStarted", scene_content)
        self.assertIn("armillaryCenter.scale", scene_content)

        # 2. Hero waiting room beacon
        hero_file = self.components_dir / "LiveMcqHeroSection.tsx"
        hero_content = hero_file.read_text(encoding="utf-8")
        self.assertIn("লাইভ অপেক্ষা কক্ষ • Waiting Room", hero_content)
        self.assertIn("animate-pulse", hero_content)

        # 3. Motion Leaderboard reveal
        reveal_file = self.components_dir / "AcademicLeaderboardReveal.tsx"
        self.assertTrue(reveal_file.exists())
        reveal_content = reveal_file.read_text(encoding="utf-8")
        self.assertIn("LazyMotion", reveal_content)
        self.assertIn("useReducedMotion", reveal_content)
        self.assertIn("জাতীয় মেধা মূল্যায়ন ও শীর্ষ ফলাফল", reveal_content)
        self.assertIn("সর্বোচ্চ নম্বর", reveal_content)
        self.assertIn("গড় নির্ভুলতা", reveal_content)
        self.assertIn("শীর্ষ স্ট্রিক", reveal_content)


if __name__ == "__main__":
    unittest.main()
