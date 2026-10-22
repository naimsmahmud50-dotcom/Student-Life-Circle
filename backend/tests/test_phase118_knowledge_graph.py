"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Curriculum Knowledge Graph
TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
FILE:      backend/tests/test_phase118_knowledge_graph.py
PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
PURPOSE:   Automated unit and integration test suite certifying curriculum DAG cycle-free
           topological integrity, recursive prerequisite gap identification, dynamic
           3-step remedial pathway synthesis, tactile 3D styling, and zero-emoji compliance.
STANDARDS: OWASP ASVS L2, NCTB Pedagogical Standards, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import re
import unittest
from pathlib import Path

from backend.app.services.curriculum_knowledge_graph_service import (
    CurriculumKnowledgeGraphService,
    curriculum_knowledge_graph_service,
    TopicNotFoundException,
    CycleDetectedException,
)


class TestPhase118KnowledgeGraph(unittest.TestCase):
    """
    Test suite certifying Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.service_file = cls.root_dir / "backend" / "app" / "services" / "curriculum_knowledge_graph_service.py"
        cls.endpoints_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "knowledge_graph.py"
        cls.frontend_atlas = cls.root_dir / "frontend" / "src" / "components" / "curriculum" / "KnowledgeGraphAtlas.tsx"
        cls.frontend_drawer = cls.root_dir / "frontend" / "src" / "components" / "curriculum" / "RemedialPathDrawer.tsx"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def setUp(self):
        # Create a fresh isolated service instance for each test
        self.service = CurriculumKnowledgeGraphService()

    def test_01_dag_integrity_and_cycle_prevention(self):
        """Verifies DAG is acyclic and strictly catches/rejects cyclical edge additions."""
        # Initial graph must pass DAG validation
        self.service.validate_dag()

        # Add a valid child topic
        self.service.add_topic(
            topic_id="math-hsc-differential-equations",
            title_bn="অন্তরক সমীকরণ",
            title_en="Differential Equations",
            subject="উচ্চতর গণিত ১ম পত্র",
            class_grade=12,
            domain="ক্যালকুলাস",
            prerequisites=["math-hsc-differentiation", "math-hsc-integration"],
        )
        self.service.validate_dag()

        # Attempt to create a cycle: math-cl6-fractions depends on math-hsc-differential-equations
        with self.assertRaises(CycleDetectedException):
            self.service.add_topic(
                topic_id="math-cl6-fractions",
                title_bn="ভগ্নাংশ (চক্রীয় প্রচেষ্টা)",
                title_en="Cyclic Fractions",
                subject="সাধারণ গণিত",
                class_grade=6,
                domain="পাটিগণিত",
                prerequisites=["math-hsc-differential-equations"],
            )

        # Rollback check: math-cl6-fractions still has no prerequisites
        fractions_node = self.service.get_topic("math-cl6-fractions")
        self.assertEqual(fractions_node["prerequisites"], [])

        # Non-existent topic raises TopicNotFoundException
        with self.assertRaises(TopicNotFoundException):
            self.service.get_topic("non-existent-topic-id")

    def test_02_prerequisite_topological_traversal(self):
        """Verifies ancestor traversal returns prerequisites in proper topological order."""
        prereqs = self.service.get_prerequisites("math-hsc-differentiation", recursive=True)
        prereq_ids = [p["topic_id"] for p in prereqs]

        # Verify foundational ancestors are present
        self.assertIn("math-cl6-fractions", prereq_ids)
        self.assertIn("math-cl8-algebraic-identities", prereq_ids)
        self.assertIn("math-cl9-trigonometric-ratios", prereq_ids)
        self.assertIn("math-cl10-coordinate-geometry", prereq_ids)
        self.assertIn("math-hsc-functions-limits", prereq_ids)

        # In topological order: math-cl6-fractions must come before math-cl8-algebraic-identities
        idx_fractions = prereq_ids.index("math-cl6-fractions")
        idx_algebra = prereq_ids.index("math-cl8-algebraic-identities")
        idx_limits = prereq_ids.index("math-hsc-functions-limits")

        self.assertLess(idx_fractions, idx_algebra)
        self.assertLess(idx_algebra, idx_limits)

    def test_03_prerequisite_gap_identification(self):
        """Verifies prerequisite gap identification based on student mastery thresholds."""
        student_mastery = {
            "math-cl6-fractions": 0.95,
            "math-cl8-algebraic-identities": 0.85,
            "math-cl9-trigonometric-ratios": 0.40,  # Gap (< 0.70)
            "math-cl10-coordinate-geometry": 0.80,
            "math-hsc-functions-limits": 0.55,       # Gap (< 0.70)
        }

        gaps = self.service.identify_prerequisite_gaps(
            topic_id="math-hsc-differentiation",
            student_mastery_map=student_mastery,
            threshold=0.70,
        )

        gap_ids = [g["topic_id"] for g in gaps]
        self.assertIn("math-cl9-trigonometric-ratios", gap_ids)
        self.assertIn("math-hsc-functions-limits", gap_ids)
        self.assertNotIn("math-cl6-fractions", gap_ids)
        self.assertNotIn("math-cl8-algebraic-identities", gap_ids)

        trig_gap = next(g for g in gaps if g["topic_id"] == "math-cl9-trigonometric-ratios")
        self.assertEqual(trig_gap["current_mastery"], 0.40)
        self.assertEqual(trig_gap["mastery_gap"], 0.30)

    def test_04_dynamic_remedial_pathway_generation(self):
        """Verifies 3-step structured remedial pathway synthesis (5 min + 5 min + 5 min = 15 min)."""
        student_mastery = {
            "math-cl9-trigonometric-ratios": 0.45,
            "math-hsc-functions-limits": 0.50,
        }

        pathway = self.service.generate_remedial_pathway(
            topic_id="math-hsc-differentiation",
            student_mastery_map=student_mastery,
        )

        self.assertEqual(pathway["target_topic_id"], "math-hsc-differentiation")
        self.assertEqual(pathway["total_duration_minutes"], 15)
        self.assertGreaterEqual(pathway["detected_gaps_count"], 1)

        steps = pathway["steps"]
        self.assertEqual(len(steps), 3)

        # Step 1: Quick Concept Refresher (5 mins)
        self.assertEqual(steps[0]["step_number"], 1)
        self.assertEqual(steps[0]["duration_minutes"], 5)
        self.assertIn("Concept Refresher", steps[0]["step_name_bn"])
        self.assertIsNotNone(steps[0]["formula_highlight"])

        # Step 2: Guided Worked Example (5 mins)
        self.assertEqual(steps[1]["step_number"], 2)
        self.assertEqual(steps[1]["duration_minutes"], 5)
        self.assertIn("Guided Worked Example", steps[1]["step_name_bn"])
        self.assertGreater(len(steps[1]["solution_steps"]), 0)

        # Step 3: Mastery Diagnostic Drill (5 mins)
        self.assertEqual(steps[2]["step_number"], 3)
        self.assertEqual(steps[2]["duration_minutes"], 5)
        self.assertIn("Mastery Diagnostic Drill", steps[2]["step_name_bn"])
        self.assertEqual(steps[2]["drill_questions_count"], 3)

    def test_05_frontend_component_architecture_and_tactile_styling(self):
        """Verifies frontend components adhere to cartographic academic design, KaTeX, and 3D buttons."""
        self.assertTrue(self.frontend_atlas.exists(), "KnowledgeGraphAtlas.tsx must exist.")
        self.assertTrue(self.frontend_drawer.exists(), "RemedialPathDrawer.tsx must exist.")

        atlas_content = self.frontend_atlas.read_text(encoding="utf-8")
        drawer_content = self.frontend_drawer.read_text(encoding="utf-8")

        # 1. Tactile 3D button styling
        self.assertIn("shadow-[0_4px_0_0_#065F46]", drawer_content)
        self.assertIn("active:translate-y-1", drawer_content)
        self.assertIn("active:shadow-none", drawer_content)
        self.assertIn("bg-emerald-800", drawer_content)
        self.assertIn("প্রতিকারমূলক পাঠ শুরু করো", drawer_content)

        # 2. Cartographic parchment SVG canvas in Atlas
        self.assertIn("<svg", atlas_content)
        self.assertIn("academic-arrow", atlas_content)
        self.assertIn("viewBox", atlas_content)

        # 3. KaTeX Renderer formula integration
        self.assertIn("KaTeXRenderer", drawer_content)

        # 4. Pure Lucide icons
        self.assertIn("Compass", atlas_content)
        self.assertIn("ZoomIn", atlas_content)
        self.assertIn("ZoomOut", atlas_content)
        self.assertIn("RotateCcw", atlas_content)
        self.assertIn("Clock", drawer_content)
        self.assertIn("BookOpen", drawer_content)
        self.assertIn("CheckCircle2", drawer_content)
        self.assertIn("AlertCircle", drawer_content)

    def test_06_architecture_notes_and_zero_emoji_enforcement(self):
        """Verifies Developer Architecture Notes and strict zero-emoji enforcement across all Phase 118 files."""
        files_to_check = [
            self.service_file,
            self.endpoints_file,
            self.frontend_atlas,
            self.frontend_drawer,
            Path(__file__),
        ]

        for file_path in files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist.")
            content = file_path.read_text(encoding="utf-8")

            # Assert Developer Architecture Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"File {file_path.name} is missing standardized DEVELOPER ARCHITECTURE NOTE.",
            )

            # Assert zero emojis
            emoji_matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(emoji_matches),
                0,
                f"File {file_path.name} contains emoji violations: {emoji_matches}",
            )


if __name__ == "__main__":
    unittest.main()
