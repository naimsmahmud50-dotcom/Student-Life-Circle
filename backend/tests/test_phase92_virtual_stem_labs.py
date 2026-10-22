"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Test Suite - 3D STEM Virtual Labs & Simulation Engine
TOPIC:     Kinematic Calculations, Molecular 3D Geometries, Cell Organelles, Zero-Emoji
FILE:      backend/tests/test_phase92_virtual_stem_labs.py
PURPOSE:   Automated verification test suite for Phase 92:
           1. STEM Virtual Lab catalog & curriculum mappings.
           2. Projectile kinematics solver, parameter bounds, trajectory coordinates.
           3. 3D Molecular geometry catalog (Methane, Benzene, Water, Glucose, sp3/sp2).
           4. Cellular organelle knowledge base (Mitochondria, Nucleus, Ribosome, Chloroplast).
           5. Frontend lab components (Physics, Chemistry, Biology, Unified Module).
           6. Strict Zero-Emoji compliance and Developer Architecture Notes.
AUDIENCE:  QA Engineers, Simulation Reviewers, STEM Curriculum Leads & AI Agents
STANDARDS: NCTB HSC Curriculum, SI Metric Standard, UI/UX Pro Max, Strict Zero-Emoji
========================================================================================
"""

import unittest
import math
import os
import re

from backend.app.services.stem_labs_service import (
    STEMLabsService,
    stem_labs_service,
    ProjectileSimulationEngine,
    MolecularGeometryCatalog,
    BiologyCellKnowledgeBase
)


class TestSTEMLabCatalogAndCurriculum(unittest.TestCase):
    """
    Tests lab catalog availability and national curriculum alignment.
    """

    def setUp(self):
        self.service = STEMLabsService()

    def test_lab_catalog_contains_three_core_sciences(self):
        catalog = self.service.get_lab_catalog()
        self.assertEqual(len(catalog), 3)

        lab_ids = [lab["id"] for lab in catalog]
        self.assertIn("physics_projectile_lab", lab_ids)
        self.assertIn("chemistry_molecular_viewer", lab_ids)
        self.assertIn("biology_cell_structure_lab", lab_ids)

        for lab in catalog:
            self.assertIn("curriculum", lab)
            self.assertIn("capabilities", lab)
            self.assertGreater(len(lab["capabilities"]), 2)


class TestProjectileSimulationEngine(unittest.TestCase):
    """
    Tests kinematic equations, parameter validation, and numerical integration.
    """

    def setUp(self):
        self.engine = ProjectileSimulationEngine()

    def test_parameter_bounds_validation(self):
        # Valid parameters
        valid, err = self.engine.validate_parameters(35.0, 45.0, 9.8, 0.0)
        self.assertTrue(valid)
        self.assertIsNone(err)

        # Invalid: Negative velocity
        valid, err = self.engine.validate_parameters(-5.0, 45.0)
        self.assertFalse(valid)
        self.assertIn("Velocity", err)

        # Invalid: Angle > 90 degrees
        valid, err = self.engine.validate_parameters(20.0, 95.0)
        self.assertFalse(valid)
        self.assertIn("Angle", err)

        # Invalid: Negative gravity
        valid, err = self.engine.validate_parameters(20.0, 45.0, -9.8)
        self.assertFalse(valid)
        self.assertIn("Gravity", err)

    def test_ideal_kinematic_calculations(self):
        # For v0 = 20 m/s, theta = 45 deg, g = 9.8 m/s^2
        metrics = self.engine.calculate_ideal_metrics(
            velocity_m_s=20.0,
            angle_degrees=45.0,
            gravity_m_s2=9.8
        )

        expected_time = (2.0 * 20.0 * math.sin(math.radians(45))) / 9.8
        expected_height = ((20.0 ** 2) * (math.sin(math.radians(45)) ** 2)) / (2.0 * 9.8)
        expected_range = ((20.0 ** 2) * math.sin(math.radians(90))) / 9.8

        self.assertAlmostEqual(metrics["time_of_flight_seconds"], round(expected_time, 3), places=2)
        self.assertAlmostEqual(metrics["max_height_meters"], round(expected_height, 3), places=2)
        self.assertAlmostEqual(metrics["range_meters"], round(expected_range, 3), places=2)

    def test_maximum_range_occurs_at_45_degrees(self):
        r_30 = self.engine.calculate_ideal_metrics(30.0, 30.0)["range_meters"]
        r_45 = self.engine.calculate_ideal_metrics(30.0, 45.0)["range_meters"]
        r_60 = self.engine.calculate_ideal_metrics(30.0, 60.0)["range_meters"]

        self.assertGreater(r_45, r_30)
        self.assertGreater(r_45, r_60)
        self.assertAlmostEqual(r_30, r_60, places=1, msg="Complementary angles (30 and 60) have identical range")

    def test_trajectory_points_generation(self):
        points = self.engine.generate_trajectory_points(
            velocity_m_s=25.0,
            angle_degrees=45.0,
            gravity_m_s2=9.8,
            air_resistance_coef=0.0
        )
        self.assertGreater(len(points), 5)
        # Starts at origin
        self.assertEqual(points[0]["x"], 0.0)
        self.assertEqual(points[0]["y"], 0.0)
        # Reaches ground
        self.assertGreaterEqual(points[-1]["x"], 30.0)


class TestMolecularGeometryCatalog(unittest.TestCase):
    """
    Tests 3D chemical coordinates, hybridization, and bond configurations.
    """

    def setUp(self):
        self.catalog = MolecularGeometryCatalog()

    def test_methane_geometry_and_hybridization(self):
        ch4 = self.catalog.get_molecule("methane")
        self.assertIsNotNone(ch4)
        self.assertEqual(ch4["formula"], "CH4")
        self.assertEqual(ch4["hybridization"], "sp3")
        self.assertEqual(ch4["bond_angle_degrees"], 109.5)
        self.assertEqual(len(ch4["atoms"]), 5, "Methane must have 1 Carbon and 4 Hydrogens")
        self.assertEqual(len(ch4["bonds"]), 4)

    def test_benzene_geometry_and_aromaticity(self):
        c6h6 = self.catalog.get_molecule("benzene")
        self.assertIsNotNone(c6h6)
        self.assertEqual(c6h6["formula"], "C6H6")
        self.assertEqual(c6h6["hybridization"], "sp2")
        self.assertEqual(c6h6["bond_angle_degrees"], 120.0)
        self.assertEqual(len(c6h6["atoms"]), 12)
        # Has aromatic ring bonds
        aromatic_bonds = [b for b in c6h6["bonds"] if b["type"] == "aromatic"]
        self.assertEqual(len(aromatic_bonds), 6)

    def test_water_and_glucose(self):
        h2o = self.catalog.get_molecule("water")
        self.assertIsNotNone(h2o)
        self.assertEqual(h2o["bond_angle_degrees"], 104.5)

        glucose = self.catalog.get_molecule("glucose")
        self.assertIsNotNone(glucose)
        self.assertIn("C6H12O6", glucose["formula"])


class TestBiologyCellKnowledgeBase(unittest.TestCase):
    """
    Tests cellular organelle descriptions and examination notes.
    """

    def setUp(self):
        self.kb = BiologyCellKnowledgeBase()

    def test_mitochondria_powerhouse_attributes(self):
        mito = self.kb.get_organelle("mitochondria")
        self.assertIsNotNone(mito)
        self.assertIn("শক্তিঘর", mito["alias_bn"])
        self.assertIn("ATP", mito["primary_function_bn"])
        self.assertIn("কৃষ্টি", mito["membrane_type_bn"])

    def test_nucleus_control_center(self):
        nuc = self.kb.get_organelle("nucleus")
        self.assertIsNotNone(nuc)
        self.assertIn("প্রাণকেন্দ্র", nuc["alias_bn"])
        self.assertIn("DNA", nuc["primary_function_bn"])

    def test_chloroplast_is_plant_specific(self):
        chloro = self.kb.get_organelle("chloroplast")
        self.assertIsNotNone(chloro)
        self.assertIn("সালোকসংশ্লেষণ", chloro["primary_function_bn"])


class TestFrontendVirtualLabComponents(unittest.TestCase):
    """
    Verifies that all frontend components exist and satisfy requirements.
    """

    LAB_COMPONENTS = [
        "frontend/src/components/stem-labs/PhysicsProjectileLab.tsx",
        "frontend/src/components/stem-labs/ChemistryMolecularViewer.tsx",
        "frontend/src/components/stem-labs/BiologyCellStructureLab.tsx",
        "frontend/src/components/stem-labs/index.ts",
        "frontend/src/modules/stem-sandboxes/VirtualStemLabsModule.tsx"
    ]

    def test_components_exist(self):
        for path in self.LAB_COMPONENTS:
            self.assertTrue(os.path.exists(path), f"Missing {path}")

    def test_physics_lab_features(self):
        with open(self.LAB_COMPONENTS[0], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)
        self.assertIn("KaTeXRenderer", content)
        self.assertIn("theoreticalFlightTime", content)
        self.assertIn("theoreticalRange", content)
        self.assertIn("webglcontextlost", content)
        self.assertIn("devicePixelRatio", content)

    def test_chemistry_lab_features(self):
        with open(self.LAB_COMPONENTS[1], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)
        self.assertIn("project3D", content)
        self.assertIn("getMeasuredDistance", content)
        self.assertIn("showOrbitalLobes", content)
        self.assertIn("webglcontextlost", content)

    def test_biology_lab_features(self):
        with open(self.LAB_COMPONENTS[2], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)
        self.assertIn("cellType", content)
        self.assertIn("plant", content)
        self.assertIn("animal", content)
        self.assertIn("selectedOrganelle", content)


class TestZeroEmojiCompliance(unittest.TestCase):
    """
    Strict Zero-Emoji Compliance across all Phase 92 files.
    """

    PHASE_92_FILES = [
        "backend/app/services/stem_labs_service.py",
        "frontend/src/components/stem-labs/PhysicsProjectileLab.tsx",
        "frontend/src/components/stem-labs/ChemistryMolecularViewer.tsx",
        "frontend/src/components/stem-labs/BiologyCellStructureLab.tsx",
        "frontend/src/components/stem-labs/index.ts",
        "frontend/src/modules/stem-sandboxes/VirtualStemLabsModule.tsx",
        "backend/tests/test_phase92_virtual_stem_labs.py"
    ]

    EMOJI_PATTERN = re.compile(
        r"[\U0001F600-\U0001F64F"  # Emoticons
        r"\U0001F300-\U0001F5FF"  # Misc symbols & pictographs
        r"\U0001F680-\U0001F6FF"  # Transport & map
        r"\U0001F700-\U0001F77F"  # Alchemical symbols
        r"\U0001F780-\U0001F7FF"  # Geometric shapes
        r"\U0001F800-\U0001F8FF"  # Supplemental arrows
        r"\U0001F900-\U0001F9FF"  # Supplemental symbols & pictographs
        r"\U0001FA00-\U0001FA6F"  # Chess symbols
        r"\U0001FA70-\U0001FAFF"  # Symbols & pictographs extended-A
        r"\U00002702-\U000027B0"  # Dingbats
        r"\U000024C2-\U0001F251"
        r"]+",
        flags=re.UNICODE
    )

    def test_strict_zero_emoji_in_phase92_files(self):
        for file_rel in self.PHASE_92_FILES:
            if not os.path.exists(file_rel):
                continue
            with open(file_rel, "r", encoding="utf-8") as f:
                content = f.read()
            match = self.EMOJI_PATTERN.search(content)
            self.assertIsNone(
                match,
                f"Strict Zero-Emoji Violation in {file_rel}: Found emoji '{match.group(0) if match else ''}'"
            )

    def test_developer_architecture_notes_presence(self):
        for file_rel in self.PHASE_92_FILES:
            if not os.path.exists(file_rel):
                continue
            with open(file_rel, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing DEVELOPER ARCHITECTURE NOTE in {file_rel}"
            )


if __name__ == "__main__":
    unittest.main()
