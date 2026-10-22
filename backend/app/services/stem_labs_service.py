"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    STEM Virtual Labs - 3D Simulation & Curriculum Mapping Engine
TOPIC:     Physics Projectile Mechanics, Molecular Geometry & Cellular Organelles
FILE:      backend/app/services/stem_labs_service.py
PURPOSE:   Provides scientific calculation engines and curriculum mappings for Ogrojatra
           Virtual STEM Laboratories:
           1. Projectile Motion Mechanics: Numerical trajectory solver, parameter bounds
              validation, air resistance drag models, time of flight, height, and range.
           2. 3D Molecular Geometry Catalog: Coordinates, bond lengths, hybridization
              angles, and electron orbital lobes for Methane, Benzene, Water, and Glucose.
           3. Cellular Organelles Knowledge Base: 3D spatial models and pedagogical Bengali
              summaries for Plant & Animal cell biology.
AUDIENCE:  Backend Engineers, Simulation Scientists & AI Autonomous Agents
STANDARDS: NCTB HSC Physics/Chemistry/Biology Curriculum, SI Metric System, Strict Zero-Emoji
========================================================================================
"""

import math
from typing import Dict, List, Any, Optional, Tuple


# =============================================================================
# 1. Physics Projectile Mechanics Engine
# =============================================================================
class ProjectileSimulationEngine:
    """
    Computes kinematics and aerodynamic trajectory points for projectile motion.
    Validates parameter bounds adhering to physical laws.
    """

    GRAVITY_PRESETS = {
        "earth": 9.80665,
        "moon": 1.62,
        "mars": 3.71,
        "jupiter": 24.79
    }

    @staticmethod
    def validate_parameters(
        velocity_m_s: float,
        angle_degrees: float,
        gravity_m_s2: float = 9.8,
        air_resistance_coef: float = 0.0
    ) -> Tuple[bool, Optional[str]]:
        """Validates parameter ranges to prevent unphysical calculations."""
        if not (0.0 < velocity_m_s <= 250.0):
            return False, "Velocity must be between 0.1 and 250.0 m/s."
        if not (0.0 <= angle_degrees <= 90.0):
            return False, "Angle must be between 0.0 and 90.0 degrees."
        if not (0.5 <= gravity_m_s2 <= 30.0):
            return False, "Gravity must be between 0.5 and 30.0 m/s^2."
        if not (0.0 <= air_resistance_coef <= 1.0):
            return False, "Air resistance coefficient must be between 0.0 and 1.0."
        return True, None

    @classmethod
    def calculate_ideal_metrics(
        cls,
        velocity_m_s: float,
        angle_degrees: float,
        gravity_m_s2: float = 9.8
    ) -> Dict[str, float]:
        """
        Calculates theoretical vacuum metrics using classical Newtonian equations:
        T = (2 * v0 * sin(theta)) / g
        H = (v0^2 * sin^2(theta)) / (2 * g)
        R = (v0^2 * sin(2 * theta)) / g
        """
        is_valid, err = cls.validate_parameters(velocity_m_s, angle_degrees, gravity_m_s2)
        if not is_valid:
            raise ValueError(err)

        theta_rad = math.radians(angle_degrees)
        sin_theta = math.sin(theta_rad)
        cos_theta = math.cos(theta_rad)
        sin_2theta = math.sin(2.0 * theta_rad)

        time_of_flight = (2.0 * velocity_m_s * sin_theta) / gravity_m_s2
        max_height = ((velocity_m_s ** 2) * (sin_theta ** 2)) / (2.0 * gravity_m_s2)
        max_range = ((velocity_m_s ** 2) * sin_2theta) / gravity_m_s2

        return {
            "time_of_flight_seconds": round(time_of_flight, 3),
            "max_height_meters": round(max_height, 3),
            "range_meters": round(max_range, 3),
            "vx_initial": round(velocity_m_s * cos_theta, 3),
            "vy_initial": round(velocity_m_s * sin_theta, 3)
        }

    @classmethod
    def generate_trajectory_points(
        cls,
        velocity_m_s: float,
        angle_degrees: float,
        gravity_m_s2: float = 9.8,
        air_resistance_coef: float = 0.0,
        num_samples: int = 50
    ) -> List[Dict[str, float]]:
        """
        Generates discretized 2D trajectory path (x, y, t) for canvas rendering.
        Incorporates Euler drag integration when air resistance > 0.
        """
        is_valid, err = cls.validate_parameters(velocity_m_s, angle_degrees, gravity_m_s2, air_resistance_coef)
        if not is_valid:
            raise ValueError(err)

        theta_rad = math.radians(angle_degrees)
        vx = velocity_m_s * math.cos(theta_rad)
        vy = velocity_m_s * math.sin(theta_rad)

        points = []
        dt = 0.05
        t = 0.0
        x = 0.0
        y = 0.0

        points.append({"x": 0.0, "y": 0.0, "t": 0.0, "vx": round(vx, 2), "vy": round(vy, 2)})

        max_iterations = 2000
        step = 0
        while y >= 0.0 and step < max_iterations:
            step += 1
            # Aerodynamic quadratic drag: F_drag = -k * v * v_vector
            speed = math.sqrt(vx * vx + vy * vy)
            drag_ax = -air_resistance_coef * speed * vx * 0.05
            drag_ay = -air_resistance_coef * speed * vy * 0.05

            ax = drag_ax
            ay = -gravity_m_s2 + drag_ay

            x += vx * dt
            y += vy * dt
            vx += ax * dt
            vy += ay * dt
            t += dt

            if y >= 0.0:
                points.append({
                    "x": round(x, 2),
                    "y": round(y, 2),
                    "t": round(t, 2),
                    "vx": round(vx, 2),
                    "vy": round(vy, 2)
                })

        return points


# =============================================================================
# 2. Chemistry 3D Molecular Geometry Catalog
# =============================================================================
class MolecularGeometryCatalog:
    """
    Supplies 3D atom Cartesian coordinates, chemical bonds, hybridization modes,
    and orbital geometries for chemical visualization.
    """

    MOLECULES = {
        "methane": {
            "formula": "CH4",
            "name_bn": "মিথেন",
            "name_en": "Methane",
            "geometry_bn": "চতুস্তলকীয় (Tetrahedral)",
            "hybridization": "sp3",
            "bond_angle_degrees": 109.5,
            "bond_length_angstrom": 1.09,
            "curriculum_chapter": "এইচএসসি রসায়ন ১ম পত্র: ৩য় অধ্যায় (বন্ধন ও জ্যামিতিক গঠন)",
            "atoms": [
                {"id": "C1", "element": "C", "name_bn": "কার্বন", "x": 0.0, "y": 0.0, "z": 0.0, "color": "#262626", "radius": 0.35},
                {"id": "H1", "element": "H", "name_bn": "হাইড্রোজেন", "x": 0.0, "y": 1.026, "z": 0.363, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H2", "element": "H", "name_bn": "হাইড্রোজেন", "x": -0.889, "y": -0.342, "z": 0.363, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H3", "element": "H", "name_bn": "হাইড্রোজেন", "x": 0.889, "y": -0.342, "z": 0.363, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H4", "element": "H", "name_bn": "হাইড্রোজেন", "x": 0.0, "y": 0.0, "z": -1.09, "color": "#E5E5E5", "radius": 0.22}
            ],
            "bonds": [
                {"from": "C1", "to": "H1", "type": "single"},
                {"from": "C1", "to": "H2", "type": "single"},
                {"from": "C1", "to": "H3", "type": "single"},
                {"from": "C1", "to": "H4", "type": "single"}
            ]
        },
        "water": {
            "formula": "H2O",
            "name_bn": "পানি",
            "name_en": "Water",
            "geometry_bn": "কৌণিক / V-আকৃতির (Bent)",
            "hybridization": "sp3",
            "bond_angle_degrees": 104.5,
            "bond_length_angstrom": 0.96,
            "curriculum_chapter": "এইচএসসি রসায়ন ১ম পত্র: মুক্তজোড় বিকর্ষণ ও পোলারিটি",
            "atoms": [
                {"id": "O1", "element": "O", "name_bn": "অক্সিজেন", "x": 0.0, "y": 0.0, "z": 0.0, "color": "#DC2626", "radius": 0.38},
                {"id": "H1", "element": "H", "name_bn": "হাইড্রোজেন", "x": -0.757, "y": 0.586, "z": 0.0, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H2", "element": "H", "name_bn": "হাইড্রোজেন", "x": 0.757, "y": 0.586, "z": 0.0, "color": "#E5E5E5", "radius": 0.22}
            ],
            "bonds": [
                {"from": "O1", "to": "H1", "type": "single"},
                {"from": "O1", "to": "H2", "type": "single"}
            ]
        },
        "benzene": {
            "formula": "C6H6",
            "name_bn": "বেনজিন",
            "name_en": "Benzene",
            "geometry_bn": "সমতলীয় ষড়ভুজ (Planar Hexagonal)",
            "hybridization": "sp2",
            "bond_angle_degrees": 120.0,
            "bond_length_angstrom": 1.40,
            "curriculum_chapter": "এইচএসসি রসায়ন ২য় পত্র: অ্যারোমেটিসিটি ও রেজোন্যান্স",
            "atoms": [
                # 6 Carbon ring atoms
                {"id": "C1", "element": "C", "name_bn": "কার্বন", "x": 1.40, "y": 0.0, "z": 0.0, "color": "#262626", "radius": 0.35},
                {"id": "C2", "element": "C", "name_bn": "কার্বন", "x": 0.70, "y": 1.212, "z": 0.0, "color": "#262626", "radius": 0.35},
                {"id": "C3", "element": "C", "name_bn": "কার্বন", "x": -0.70, "y": 1.212, "z": 0.0, "color": "#262626", "radius": 0.35},
                {"id": "C4", "element": "C", "name_bn": "কার্বন", "x": -1.40, "y": 0.0, "z": 0.0, "color": "#262626", "radius": 0.35},
                {"id": "C5", "element": "C", "name_bn": "কার্বন", "x": -0.70, "y": -1.212, "z": 0.0, "color": "#262626", "radius": 0.35},
                {"id": "C6", "element": "C", "name_bn": "কার্বন", "x": 0.70, "y": -1.212, "z": 0.0, "color": "#262626", "radius": 0.35},
                # 6 Hydrogens attached to ring
                {"id": "H1", "element": "H", "name_bn": "হাইড্রোজেন", "x": 2.48, "y": 0.0, "z": 0.0, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H2", "element": "H", "name_bn": "হাইড্রোজেন", "x": 1.24, "y": 2.148, "z": 0.0, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H3", "element": "H", "name_bn": "হাইড্রোজেন", "x": -1.24, "y": 2.148, "z": 0.0, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H4", "element": "H", "name_bn": "হাইড্রোজেন", "x": -2.48, "y": 0.0, "z": 0.0, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H5", "element": "H", "name_bn": "হাইড্রোজেন", "x": -1.24, "y": -2.148, "z": 0.0, "color": "#E5E5E5", "radius": 0.22},
                {"id": "H6", "element": "H", "name_bn": "হাইড্রোজেন", "x": 1.24, "y": -2.148, "z": 0.0, "color": "#E5E5E5", "radius": 0.22}
            ],
            "bonds": [
                {"from": "C1", "to": "C2", "type": "aromatic"},
                {"from": "C2", "to": "C3", "type": "aromatic"},
                {"from": "C3", "to": "C4", "type": "aromatic"},
                {"from": "C4", "to": "C5", "type": "aromatic"},
                {"from": "C5", "to": "C6", "type": "aromatic"},
                {"from": "C6", "to": "C1", "type": "aromatic"},
                {"from": "C1", "to": "H1", "type": "single"},
                {"from": "C2", "to": "H2", "type": "single"},
                {"from": "C3", "to": "H3", "type": "single"},
                {"from": "C4", "to": "H4", "type": "single"},
                {"from": "C5", "to": "H5", "type": "single"},
                {"from": "C6", "to": "H6", "type": "single"}
            ]
        },
        "glucose": {
            "formula": "C6H12O6",
            "name_bn": "ডি-গ্লুকোজ (পাইরানোজ বলয়)",
            "name_en": "D-Glucose",
            "geometry_bn": "চেয়ার কনফর্মেশন (Chair Conformation)",
            "hybridization": "sp3",
            "bond_angle_degrees": 109.5,
            "bond_length_angstrom": 1.54,
            "curriculum_chapter": "এইচএসসি রসায়ন ও জীববিজ্ঞান: বায়ো-মলিকিউল ও কার্বোহাইড্রেট",
            "atoms": [
                {"id": "C1", "element": "C", "name_bn": "কার্বন-১", "x": 1.2, "y": 0.3, "z": 0.2, "color": "#262626", "radius": 0.35},
                {"id": "C2", "element": "C", "name_bn": "কার্বন-২", "x": 0.5, "y": 1.3, "z": -0.6, "color": "#262626", "radius": 0.35},
                {"id": "C3", "element": "C", "name_bn": "কার্বন-৩", "x": -0.9, "y": 1.2, "z": -0.3, "color": "#262626", "radius": 0.35},
                {"id": "C4", "element": "C", "name_bn": "কার্বন-৪", "x": -1.3, "y": -0.2, "z": -0.1, "color": "#262626", "radius": 0.35},
                {"id": "C5", "element": "C", "name_bn": "কার্বন-৫", "x": -0.3, "y": -1.1, "z": 0.5, "color": "#262626", "radius": 0.35},
                {"id": "O5", "element": "O", "name_bn": "বলয় অক্সিজেন", "x": 0.9, "y": -0.9, "z": 0.0, "color": "#DC2626", "radius": 0.38}
            ],
            "bonds": [
                {"from": "C1", "to": "C2", "type": "single"},
                {"from": "C2", "to": "C3", "type": "single"},
                {"from": "C3", "to": "C4", "type": "single"},
                {"from": "C4", "to": "C5", "type": "single"},
                {"from": "C5", "to": "O5", "type": "single"},
                {"from": "O5", "to": "C1", "type": "single"}
            ]
        }
    }

    @classmethod
    def get_molecule(cls, molecule_id: str) -> Optional[Dict[str, Any]]:
        return cls.MOLECULES.get(molecule_id.lower())

    @classmethod
    def list_available_molecules(cls) -> List[Dict[str, Any]]:
        return [
            {
                "id": k,
                "formula": v["formula"],
                "name_bn": v["name_bn"],
                "name_en": v["name_en"],
                "geometry_bn": v["geometry_bn"],
                "hybridization": v["hybridization"],
                "bond_angle_degrees": v["bond_angle_degrees"]
            }
            for k, v in cls.MOLECULES.items()
        ]


# =============================================================================
# 3. Biology 3D Cell Structure Knowledge Base
# =============================================================================
class BiologyCellKnowledgeBase:
    """
    Cellular organelle spatial metadata and pedagogical descriptions
    aligned with NCTB HSC Biology 1st Paper, Chapter 1 (Cell & Its Structure).
    """

    ORGANELLES = {
        "mitochondria": {
            "id": "mitochondria",
            "name_bn": "মাইটোকন্ড্রিয়া",
            "name_en": "Mitochondria",
            "alias_bn": "কোষের শক্তিঘর (Powerhouse of the Cell)",
            "membrane_type_bn": "দ্বি-স্তরী লিপোপ্রোটিন ঝিল্লি (ভিতরের ঝিল্লি কৃষ্টি তৈরি করে)",
            "dimension": "0.5 - 1.0 micrometer",
            "primary_function_bn": "শ্বসনের ক্রেবস চক্র এবং অক্সিডেটিভ ফসফোরাইলেশনের মাধ্যমে উচ্চ-শক্তি সম্পন্ন এটিপি (ATP) অণু তৈরি করে।",
            "hsc_exam_note": "ঢাকা বোর্ড ২০১৯ ও চট্টগ্রাম বোর্ড ২০২১-এ মাইটোকন্ড্রিয়ার গঠন সংক্রান্ত প্রয়োগমূলক প্রশ্ন এসেছিল।",
            "color_hex": "#F59E0B"
        },
        "nucleus": {
            "id": "nucleus",
            "name_bn": "নিউক্লিয়াস",
            "name_en": "Nucleus",
            "alias_bn": "কোষের প্রাণকেন্দ্র (Control Center)",
            "membrane_type_bn": "ছিদ্রযুক্ত দ্বি-স্তরী নিউক্লিয়ার পর্দা (Nuclear Membrane)",
            "dimension": "3.0 - 10.0 micrometer",
            "primary_function_bn": "বংশগতির ধারক ও বাহক ডিএনএ (DNA) ধারণ করে এবং কোষের সমুদয় বিপাকীয় কার্যক্রম নিয়ন্ত্রণ করে।",
            "hsc_exam_note": "নিউক্লিয়ার রন্ধ্রের মাধ্যমে এমআরএনএ (mRNA) সাইটোপ্লাজমে প্রবেশ করে প্রোটিন তৈরিতে সাহায্য করে।",
            "color_hex": "#4F46E5"
        },
        "ribosome": {
            "id": "ribosome",
            "name_bn": "রাইবোজোম",
            "name_en": "Ribosome",
            "alias_bn": "প্রোটিন তৈরির কারখানা (Protein Factory)",
            "membrane_type_bn": "ঝিল্লিবিহীন (Non-membranous)",
            "dimension": "20 - 30 nanometer",
            "primary_function_bn": "মেসেঞ্জার আরএনএ (mRNA) সংকেত পাঠ করে অ্যামিনো এসিড সংযুক্তির মাধ্যমে প্রোটিন সংশ্লেষণ করে।",
            "hsc_exam_note": "আদিকোষে 70S (50S+30S) এবং প্রকৃত কোষে 80S (60S+40S) রাইবোজোম বিদ্যমান থাকে।",
            "color_hex": "#10B981"
        },
        "chloroplast": {
            "id": "chloroplast",
            "name_bn": "ক্লোরোপ্লাস্ট",
            "name_en": "Chloroplast",
            "alias_bn": "উদ্ভিদের রান্নাঘর (Photosynthetic Engine)",
            "membrane_type_bn": "দ্বি-স্তরী ঝিল্লি (থাইলাকয়েড ও গ্রানা সমৃদ্ধ)",
            "dimension": "4.0 - 6.0 micrometer",
            "primary_function_bn": "সূর্যালোক ও ক্লোরোফিল ব্যবহার করে সালোকসংশ্লেষণ প্রক্রিয়ায় কার্বন ডাই-অক্সাইড এবং পানি থেকে শর্করা ও অক্সিজেন উৎপন্ন করে।",
            "hsc_exam_note": "উদ্ভিদ কোষের একটি অনন্য বৈশিষ্ট্য; প্রাণী কোষে ক্লোরোপ্লাস্ট অনুপস্থিত থাকে।",
            "color_hex": "#16A34A"
        },
        "golgi_body": {
            "id": "golgi_body",
            "name_bn": "গলগি বডি",
            "name_en": "Golgi Apparatus",
            "alias_bn": "কোষের ট্রাফিক পুলিশ (Cellular Post Office)",
            "membrane_type_bn": "একক ঝিল্লিবেষ্টিত সিস্টার্নি ও ভেসিকল",
            "dimension": "1.0 - 3.0 micrometer",
            "primary_function_bn": "এন্ডোপ্লাজমিক রেটিকুলাম থেকে আগত প্রোটিন ও লিপিডের রাসায়নিক রূপান্তর, প্যাকেজিং ও ক্ষরণ নিশ্চিত করে।",
            "hsc_exam_note": "লাইসোজোম তৈরিতে এবং উদ্ভিদকোষের কোষপ্রাচীর গঠনে এটি বিশেষ ভূমিকা পালন করে।",
            "color_hex": "#EC4899"
        }
    }

    @classmethod
    def get_organelle(cls, organelle_id: str) -> Optional[Dict[str, Any]]:
        return cls.ORGANELLES.get(organelle_id.lower())

    @classmethod
    def list_organelles(cls) -> List[Dict[str, Any]]:
        return list(cls.ORGANELLES.values())


# =============================================================================
# 4. STEM Labs Service Façade
# =============================================================================
class STEMLabsService:
    """
    Central service facilitating virtual laboratory queries and scientific calculations.
    """

    def __init__(self):
        self.projectile = ProjectileSimulationEngine()
        self.chemistry = MolecularGeometryCatalog()
        self.biology = BiologyCellKnowledgeBase()

    def get_lab_catalog(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "physics_projectile_lab",
                "title_bn": "প্রক্ষেপকের গতি সিমুলেটর (Physics Projectile Lab)",
                "subject": "physics",
                "curriculum": "NCTB HSC পদার্থবিজ্ঞান ১ম পত্র (৩য় অধ্যায়: গতিবিদ্যা)",
                "capabilities": ["0-90 ডিগ্রি কোণ নির্বাচন", "আদিবেগ সমন্বয়", "বায়ুর বাধা সিমুলেশন", "রিয়েলটাইম প্যারাবোলা গ্রাফ"]
            },
            {
                "id": "chemistry_molecular_viewer",
                "title_bn": "৩ডি আণবিক গঠন ও অরবিটাল ভিজ্যুয়ালাইজার (Chemistry Molecular Lab)",
                "subject": "chemistry",
                "curriculum": "NCTB HSC রসায়ন ১ম পত্র (৩য় অধ্যায়: সংকরায়ন ও জ্যামিতি)",
                "capabilities": ["মিথেন/বেনজিন/পানি/গ্লুকোজ ৩ডি মডেল", "বন্ধন কোণ ও দৈর্ঘ্য পরিমাপ", "sp3/sp2 অরবিটাল লোব"]
            },
            {
                "id": "biology_cell_structure_lab",
                "title_bn": "উদ্ভিদ ও প্রাণী কোষের ত্রিমাত্রিক অঙ্গাণু ল্যাব (Biology Cell Lab)",
                "subject": "biology",
                "curriculum": "NCTB HSC জীববিজ্ঞান ১ম পত্র (১ম অধ্যায়: কোষ ও এর গঠন)",
                "capabilities": ["জুমযোগ্য সাইটোপ্লাজম", "ইন্টারেক্টিভ অঙ্গাণু নির্বাচন", "মাইটোকন্ড্রিয়া ও নিউক্লিয়াসের বাংলা সারসংক্ষেপ"]
            }
        ]


# Singleton instance
stem_labs_service = STEMLabsService()
