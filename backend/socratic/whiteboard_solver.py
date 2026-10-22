"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic Math & Science Whiteboard Solver
 * TOPIC:     Phase 132 Interactive Canvas & Pedagogical Socratic Step Guidance
 * FILE:      backend/socratic/whiteboard_solver.py
 * PHASE:     Phase 132 - Real-time Socratic AI Whiteboard Solver
 * PURPOSE:   Provides pedagogical Socratic inquiry generation, progressive hint
 *            gating without answer leaking, mathematical/scientific misconception
 *            detection, and whiteboard stroke coordinate buffering.
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Pedagogical Hint Guard
 */
"""

import math
import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ProblemDomain(str, Enum):
    ALGEBRA = "ALGEBRA"
    CALCULUS = "CALCULUS"
    GEOMETRY = "GEOMETRY"
    TRIGONOMETRY = "TRIGONOMETRY"
    MECHANICS = "MECHANICS"
    ELECTROMAGNETISM = "ELECTROMAGNETISM"
    CHEMISTRY = "CHEMISTRY"


class HintLevel(int, Enum):
    LEVEL_1_CONCEPTUAL = 1
    LEVEL_2_STRATEGIC = 2
    LEVEL_3_GUIDING_QUESTION = 3
    LEVEL_4_STEP_EVALUATION = 4


class DrawingToolType(str, Enum):
    PENCIL = "PENCIL"
    RULER = "RULER"
    COMPASS = "COMPASS"
    ERASER = "ERASER"
    MATH_TEXT = "MATH_TEXT"


class DirectAnswerLeakedException(ValueError):
    """Raised when a hint or response attempts to dump the final answer prematurely."""
    pass


class InvalidStrokeCoordinateException(ValueError):
    """Raised when stroke coordinates are non-finite, negative, or beyond canvas boundaries."""
    pass


class UnauthorizedSessionAccessException(PermissionError):
    """Raised when a student attempts to access a whiteboard session belonging to another user."""
    pass


@dataclass
class Point2D:
    x: float
    y: float
    pressure: float = 1.0

    def is_valid(self, max_x: float = 2000.0, max_y: float = 2000.0) -> bool:
        if not (math.isfinite(self.x) and math.isfinite(self.y) and math.isfinite(self.pressure)):
            return False
        if self.x < 0.0 or self.y < 0.0 or self.x > max_x or self.y > max_y:
            return False
        if self.pressure < 0.0 or self.pressure > 1.0:
            return False
        return True


@dataclass
class DrawingStroke:
    stroke_id: str
    tool: DrawingToolType
    color_hex: str
    width: float
    points: List[Point2D]
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stroke_id": self.stroke_id,
            "tool": self.tool.value,
            "color_hex": self.color_hex,
            "width": self.width,
            "points": [{"x": p.x, "y": p.y, "pressure": p.pressure} for p in self.points],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DrawingStroke":
        points = [
            Point2D(x=float(p["x"]), y=float(p["y"]), pressure=float(p.get("pressure", 1.0)))
            for p in data.get("points", [])
        ]
        return cls(
            stroke_id=data["stroke_id"],
            tool=DrawingToolType(data["tool"]),
            color_hex=data.get("color_hex", "#0A2540"),
            width=float(data.get("width", 2.0)),
            points=points,
            created_at=float(data.get("created_at", time.time())),
        )


@dataclass
class SocraticStep:
    step_index: int
    title: str
    concept_bengali: str
    inquiry_question: str
    pedagogical_hints: List[str]
    revealed_hint_level: int = 1
    is_completed: bool = False
    katex_formula: Optional[str] = None
    expected_concept_keywords: List[str] = field(default_factory=list)


@dataclass
class SocraticProblemSession:
    session_id: str
    student_id: str
    title: str
    problem_text: str
    domain: ProblemDomain
    steps: List[SocraticStep]
    strokes: List[DrawingStroke] = field(default_factory=list)
    current_step_index: int = 0
    final_solution_revealed: bool = False
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def is_all_steps_completed(self) -> bool:
        return all(s.is_completed for s in self.steps)


class PedagogicalHintGuard:
    """
    Guards pedagogical integrity by ensuring solutions are not directly leaked.
    Requires progressive hint unlocking and conceptual scaffolding.
    """

    DIRECT_ANSWER_PATTERNS = [
        re.compile(r"(?:সরাসরি উত্তর|চূড়ান্ত সমাধান|final answer|the answer is|x\s*=\s*[-+]?\d+)", re.IGNORECASE),
        re.compile(r"(?:অতএব উত্তর হলো|সুতরাং নির্ণেয় মান)", re.IGNORECASE),
    ]

    @classmethod
    def assert_no_direct_answer_leak(cls, hint_text: str, is_final_step: bool = False) -> None:
        """
        Validates that hint text does not leak the terminal answer prematurely.
        """
        if not is_final_step:
            for pattern in cls.DIRECT_ANSWER_PATTERNS:
                if pattern.search(hint_text):
                    raise DirectAnswerLeakedException(
                        f"Pedagogical Violation: Hint attempted to leak direct answer without scaffolding: '{hint_text}'"
                    )

    @classmethod
    def validate_hint_request(cls, current_level: int, requested_level: int) -> bool:
        """
        Enforces sequential hint unlocking (Level 1 -> Level 2 -> Level 3 -> Level 4).
        Cannot skip ahead without encountering intermediate inquiry.
        """
        if requested_level < 1 or requested_level > 4:
            return False
        if requested_level > current_level + 1:
            return False
        return True


class MisconceptionDetector:
    """
    Identifies common cognitive traps and misconceptions in student mathematical & scientific derivations.
    """

    MISCONCEPTION_RULES = [
        {
            "id": "FRESHMAN_EXPONENT_TRAP",
            "domain": ProblemDomain.ALGEBRA,
            "pattern": re.compile(r"\(\s*[a-zA-Z]\s*\+\s*[a-zA-Z]\s*\)\s*\^\s*2\s*=\s*[a-zA-Z]\^2\s*\+\s*[a-zA-Z]\^2", re.IGNORECASE),
            "negative_pattern": None,
            "title_bn": "বীজগণিতীয় দ্বিপদী বিস্তৃতিতে মধ্যপদের বিভ্রান্তি",
            "remediation_bn": "(a + b)^2 এর বিস্তৃতিতে 2ab পদটি বিদ্যমান থাকে। সুতরাং (a + b)^2 = a^2 + 2ab + b^2।",
            "remediation_en": "Remember the binomial expansion (a + b)^2 = a^2 + 2ab + b^2, requiring the middle 2ab term.",
        },
        {
            "id": "TRIG_PYTHAGOREAN_CONFUSION",
            "domain": ProblemDomain.TRIGONOMETRY,
            "pattern": re.compile(r"sin\^2\s*([a-zA-Z]|\\theta)\s*-\s*cos\^2\s*([a-zA-Z]|\\theta)\s*=\s*1", re.IGNORECASE),
            "negative_pattern": None,
            "title_bn": "ত্রিকোণমিতিক পিথাগোরাস অভেদে চিহ্নের ভুল",
            "remediation_bn": "পিথাগোরাসের মূল অভেদ হলো sin^2(θ) + cos^2(θ) = 1। বিয়োগ চিহ্ন কেবল cos^2(θ) - sin^2(θ) = cos(2θ) এর ক্ষেত্রে প্রযোজ্য।",
            "remediation_en": "The Pythagorean identity is sin^2(θ) + cos^2(θ) = 1 with addition, not subtraction.",
        },
        {
            "id": "CALCULUS_MISSING_CONSTANT",
            "domain": ProblemDomain.CALCULUS,
            "pattern": re.compile(r"(?:\\int|int).*=", re.IGNORECASE),
            "negative_pattern": re.compile(r"\+\s*[cC]\b", re.IGNORECASE),
            "title_bn": "অনির্দিষ্ট যোগজে ধ্রুবক (C) বাদ পড়া",
            "remediation_bn": "যেহেতু এটি অনির্দিষ্ট যোগজ (indefinite integral), সমাধান শেষে সমাকলন ধ্রুবক '+ C' যুক্ত করতে হয়।",
            "remediation_en": "An indefinite integral always requires an arbitrary integration constant '+ C'.",
        },
        {
            "id": "DERIVATIVE_COSINE_SIGN",
            "domain": ProblemDomain.CALCULUS,
            "pattern": re.compile(r"d/dx\s*\(?\s*cos\s*\(?x\)?\s*\)?\s*=\s*sin\s*\(?x\)?", re.IGNORECASE),
            "negative_pattern": None,
            "title_bn": "কোসাইনের অন্তরজে ঋণাত্মক চিহ্নের ভুল",
            "remediation_bn": "কোসাইনের অন্তরীকরণ করলে ঋণাত্মক সাইন পাওয়া যায়: d/dx(cos x) = -sin x।",
            "remediation_en": "The derivative of cos(x) is negative: d/dx(cos x) = -sin(x).",
        },
        {
            "id": "NEWTON_THIRD_LAW_PAIR",
            "domain": ProblemDomain.MECHANICS,
            "pattern": re.compile(r"(?:action\s*and\s*reaction\s*cancel|ক্রিয়া\s*ও\s*প্রতিক্রিয়া\s*পরস্পরকে\s*বাতিল\s*করে)", re.IGNORECASE),
            "negative_pattern": None,
            "title_bn": "নিউটনের তৃতীয় সূত্রের ক্রিয়া-প্রতিক্রিয়া জোড় বিভ্রান্তি",
            "remediation_bn": "ক্রিয়া ও প্রতিক্রিয়া বল সর্বদা দুটি ভিন্ন বস্তুর উপর কাজ করে, তাই তারা একে অপরকে বাতিল করে না।",
            "remediation_en": "Action and reaction forces act on two entirely different bodies, so they never cancel each other out.",
        },
    ]

    @classmethod
    def evaluate_expression(cls, domain: ProblemDomain, student_input: str) -> Optional[Dict[str, Any]]:
        """
        Scans student's mathematical expression or step argument for known misconceptions.
        """
        for rule in cls.MISCONCEPTION_RULES:
            if rule["domain"] == domain:
                if rule["pattern"].search(student_input):
                    neg = rule.get("negative_pattern")
                    if neg and neg.search(student_input):
                        continue
                    return {
                        "has_misconception": True,
                        "rule_id": rule["id"],
                        "title_bn": rule["title_bn"],
                        "remediation_bn": rule["remediation_bn"],
                        "remediation_en": rule["remediation_en"],
                    }
        return None


class DrawingStrokeBuffer:
    """
    Maintains and validates freehand strokes, ruler measurements, and compass arcs.
    """

    MAX_STROKES_PER_SESSION = 5000
    CANVAS_WIDTH = 2000.0
    CANVAS_HEIGHT = 2000.0

    @classmethod
    def validate_and_append_stroke(
        cls,
        existing_strokes: List[DrawingStroke],
        new_stroke: DrawingStroke
    ) -> List[DrawingStroke]:
        """
        Validates coordinate limits and points integrity before adding to in-memory session buffer.
        """
        if len(existing_strokes) >= cls.MAX_STROKES_PER_SESSION:
            raise OverflowError(f"Stroke buffer capacity exceeded ({cls.MAX_STROKES_PER_SESSION} strokes).")

        if not new_stroke.points:
            raise InvalidStrokeCoordinateException("Stroke must contain at least one Point2D coordinate.")

        for pt in new_stroke.points:
            if not pt.is_valid(cls.CANVAS_WIDTH, cls.CANVAS_HEIGHT):
                raise InvalidStrokeCoordinateException(
                    f"Coordinate ({pt.x}, {pt.y}) exceeds canvas bounds [0, {cls.CANVAS_WIDTH}] or is non-finite."
                )

        updated = list(existing_strokes)
        updated.append(new_stroke)
        return updated

    @classmethod
    def calculate_bounding_box(cls, strokes: List[DrawingStroke]) -> Tuple[float, float, float, float]:
        """
        Computes (min_x, min_y, max_x, max_y) across all points in stroke collection.
        """
        if not strokes:
            return (0.0, 0.0, 0.0, 0.0)

        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for s in strokes:
            for p in s.points:
                if p.x < min_x:
                    min_x = p.x
                if p.y < min_y:
                    min_y = p.y
                if p.x > max_x:
                    max_x = p.x
                if p.y > max_y:
                    max_y = p.y

        if min_x == float("inf"):
            return (0.0, 0.0, 0.0, 0.0)

        return (min_x, min_y, max_x, max_y)


class SocraticWhiteboardSolver:
    """
    Central controller managing student whiteboard sessions, progressive hints, and step validation.
    """

    STANDARD_CURRICULUM_PROBLEMS: Dict[str, Dict[str, Any]] = {
        "prob_quad_01": {
            "title": "দ্বিঘাত সমীকরণের পূর্ণবর্গীয় সমাধান",
            "domain": ProblemDomain.ALGEBRA,
            "problem_text": "2x^2 + 7x - 4 = 0 সমীকরণটি পূর্ণবর্গ পদ্ধতিতে সমাধান করো।",
            "steps": [
                {
                    "step_index": 0,
                    "title": "ধাপ ১: x^2 এর সহগ অপসারণ ও সমতাকরণ",
                    "concept_bengali": "পূর্ণবর্গীয় গঠনে প্রথম পদের সহগকে ১ এ রূপান্তর করতে হয়।",
                    "inquiry_question": "উভয়পক্ষকে কোন সংখ্যা দিয়ে ভাগ করলে x^2 এর সহগ ১ হবে?",
                    "pedagogical_hints": [
                        "সমীকরণটিতে x^2 এর সাথে সহগ হিসেবে ২ রয়েছে।",
                        "সম্পূর্ণ সমীকরণকে ২ দিয়ে ভাগ করে দেখুন ধ্রুবপদ ও x এর সহগ কী দাঁড়ায়।",
                        "তাহলে সমীকরণটি হবে: x^2 + (7/2)x - 2 = 0।",
                    ],
                    "katex_formula": "x^2 + \\frac{7}{2}x - 2 = 0",
                    "expected_concept_keywords": ["ভাগ", "divide", "2"],
                },
                {
                    "step_index": 1,
                    "title": "ধাপ ২: ধ্রুবপদ স্থানান্তর ও মধ্যপদ বিশ্লেষণ",
                    "concept_bengali": "ধ্রুবপদকে ডানপক্ষে নিয়ে মধ্যপদকে 2 * x * b আকারে সাজানো।",
                    "inquiry_question": "মধ্যপদ (7/2)x কে 2 * x * (b) আকারে লিখলে b এর মান কত হবে?",
                    "pedagogical_hints": [
                        "2 * x * b = (7/2)x হতে হলে b = (7/2) / 2 হতে হবে।",
                        "সুতরাং b এর মান দাঁড়াবে 7/4।",
                        "উভয়পক্ষে কত যোগ করলে বামপক্ষটি (x + b)^2 হবে?",
                    ],
                    "katex_formula": "x^2 + 2 \\cdot x \\cdot \\frac{7}{4} = 2",
                    "expected_concept_keywords": ["7/4", "3.5", "square"],
                },
                {
                    "step_index": 2,
                    "title": "ধাপ ৩: উভয়পক্ষে (b)^2 যোগ ও বর্গমূল",
                    "concept_bengali": "(a + b)^2 গঠন করে বর্গমূল নির্ণয়।",
                    "inquiry_question": "(7/4)^2 এর মান কত এবং উভয়পক্ষে তা যোগ করলে ডানপক্ষের মান কত হয়?",
                    "pedagogical_hints": [
                        "(7/4)^2 হলো 49/16।",
                        "ডানপক্ষে 2 + (49/16) যোগ করলে (32 + 49)/16 = 81/16 পাওয়া যায়।",
                        "এবার উভয়পক্ষে বর্গমূল প্রয়োগ করে x এর দুটি সমাধান নির্ণয় করুন।",
                    ],
                    "katex_formula": "\\left(x + \\frac{7}{4}\\right)^2 = \\frac{81}{16}",
                    "expected_concept_keywords": ["81/16", "49/16", "root"],
                },
            ]
        },
        "prob_proj_02": {
            "title": "প্রাসের গতিপথের সর্বোচ্চ উচ্চতা ও সমীকরণ",
            "domain": ProblemDomain.MECHANICS,
            "problem_text": "ভূমি থেকে v_0 আদিবেগে θ কোণে নিক্ষিপ্ত প্রাসের সর্বোচ্চ উচ্চতা (H) প্রতিপাদন করো।",
            "steps": [
                {
                    "step_index": 0,
                    "title": "ধাপ ১: আদিবেগের উল্লম্ব উপাংশ নির্ণয়",
                    "concept_bengali": "গতির সমীকরণে উল্লম্ব অক্ষের গতি বিবেচনা করা।",
                    "inquiry_question": "নিক্ষেপণ কোণ θ হলে উল্লম্ব দিকের আদিবেগ v_{0y} কত হবে?",
                    "pedagogical_hints": [
                        "ভেক্টরের উপাংশ সূত্র স্মরণ করো: উল্লম্ব দিক হলো উলম্ব কোণের সাইন উপাংশ।",
                        "v_{0y} = v_0 \\sin\\theta।",
                    ],
                    "katex_formula": "v_{0y} = v_0 \\sin\\theta",
                    "expected_concept_keywords": ["sin", "sine", "v0*sin"],
                },
                {
                    "step_index": 1,
                    "title": "ধাপ ২: সর্বোচ্চ উচ্চতায় শেষবেগের শর্ত",
                    "concept_bengali": "সর্বোচ্চ উচ্চতার বিন্দুতে উল্লম্ব বেগের বৈশিষ্ট্য।",
                    "inquiry_question": "সর্বোচ্চ উচ্চতায় পৌঁছালে বস্তুর উল্লম্ব বেগ v_y কত হয়?",
                    "pedagogical_hints": [
                        "যখন বস্তু শীর্ষে পৌঁছায়, তখন এটি ঊর্ধ্বমুখী গতি থেকে নিম্নমুখী গতিতে রূপ নেয়।",
                        "সেই মুহূর্তে উল্লম্ব বেগ ক্ষণিকের জন্য শূন্য হয়, অর্থাৎ v_y = 0।",
                    ],
                    "katex_formula": "v_y = 0",
                    "expected_concept_keywords": ["0", "zero", "শূন্য"],
                },
                {
                    "step_index": 2,
                    "title": "ধাপ ৩: গতিবিদ্যার সমীকরণ প্রয়োগ ও প্রতিপাদন",
                    "concept_bengali": "v^2 = u^2 - 2gh সমীকরণে মান বসানো।",
                    "inquiry_question": "v_y^2 = v_{0y}^2 - 2gH সমীকরণে v_y = 0 বসালে H এর সূত্র কী দাঁড়ায়?",
                    "pedagogical_hints": [
                        "0 = (v_0 \\sin\\theta)^2 - 2gH।",
                        "2gH = v_0^2 \\sin^2\\theta পক্ষান্তর করো।",
                        "তাহলে সর্বোচ্চ উচ্চতা H = (v_0^2 \\sin^2\\theta) / (2g)।",
                    ],
                    "katex_formula": "H = \\frac{v_0^2 \\sin^2\\theta}{2g}",
                    "expected_concept_keywords": ["2g", "v0^2", "sin^2"],
                },
            ]
        }
    }

    def __init__(self):
        # In-memory store: session_id -> SocraticProblemSession
        self._sessions: Dict[str, SocraticProblemSession] = {}

    def create_session(
        self,
        student_id: str,
        problem_key: Optional[str] = "prob_quad_01",
        custom_problem_text: Optional[str] = None,
        custom_domain: Optional[ProblemDomain] = None
    ) -> SocraticProblemSession:
        """
        Creates and registers a new Socratic whiteboard session.
        """
        session_id = f"socr_{uuid.uuid4().hex[:12]}"

        if problem_key and problem_key in self.STANDARD_CURRICULUM_PROBLEMS:
            prob_def = self.STANDARD_CURRICULUM_PROBLEMS[problem_key]
            steps = [
                SocraticStep(
                    step_index=s["step_index"],
                    title=s["title"],
                    concept_bengali=s["concept_bengali"],
                    inquiry_question=s["inquiry_question"],
                    pedagogical_hints=s["pedagogical_hints"],
                    katex_formula=s.get("katex_formula"),
                    expected_concept_keywords=s.get("expected_concept_keywords", []),
                )
                for s in prob_def["steps"]
            ]
            session = SocraticProblemSession(
                session_id=session_id,
                student_id=student_id,
                title=prob_def["title"],
                problem_text=prob_def["problem_text"],
                domain=prob_def["domain"],
                steps=steps,
            )
        else:
            # Custom problem fallback
            domain = custom_domain or ProblemDomain.ALGEBRA
            problem_text = custom_problem_text or "সমস্যাটি ধাপে ধাপে বিশ্লেষণ করো।"
            default_step = SocraticStep(
                step_index=0,
                title="ধাপ ১: প্রদত্ত তথ্য ও সমস্যা বিশ্লেষণ",
                concept_bengali="সমস্যার চলক ও শর্তসমূহ চিহ্নিত করা।",
                inquiry_question="সমস্যাটিতে মূল উপপাদ্য বা সূত্র কোনটি প্রযোজ্য?",
                pedagogical_hints=[
                    "প্রদত্ত সমীকরণ বা তথ্যের চলকগুলো পৃথক করো।",
                    "সম্পর্কিত মৌলিক গাণিতিক নিয়মটি স্মরণে আনো।",
                ],
                expected_concept_keywords=["চলক", "variable", "formula"],
            )
            session = SocraticProblemSession(
                session_id=session_id,
                student_id=student_id,
                title="কাস্টম সক্রেটিক বিশ্লেষণ",
                problem_text=problem_text,
                domain=domain,
                steps=[default_step],
            )

        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str, student_id: str) -> SocraticProblemSession:
        """
        Retrieves session ensuring zero-IDOR multi-tenant isolation.
        """
        session = self._sessions.get(session_id)
        if not session:
            raise KeyError(f"Socratic session '{session_id}' not found.")
        if session.student_id != student_id:
            raise UnauthorizedSessionAccessException(
                f"IDOR Protection: Student '{student_id}' cannot access session '{session_id}'."
            )
        return session

    def unlock_next_hint(self, session_id: str, student_id: str) -> SocraticStep:
        """
        Unlocks the next progressive pedagogical hint for the current step without answer leaking.
        """
        session = self.get_session(session_id, student_id)
        current_step = session.steps[session.current_step_index]

        if current_step.revealed_hint_level < len(current_step.pedagogical_hints):
            current_step.revealed_hint_level += 1

        # Check hint guard
        active_hint = current_step.pedagogical_hints[current_step.revealed_hint_level - 1]
        is_last_step = (session.current_step_index == len(session.steps) - 1)
        PedagogicalHintGuard.assert_no_direct_answer_leak(active_hint, is_final_step=is_last_step)

        session.updated_at = time.time()
        return current_step

    def submit_step_response(
        self,
        session_id: str,
        student_id: str,
        student_response: str
    ) -> Dict[str, Any]:
        """
        Evaluates student's answer or deduction for the active step.
        """
        session = self.get_session(session_id, student_id)
        current_step = session.steps[session.current_step_index]

        # 1. Check for misconceptions first
        misconception = MisconceptionDetector.evaluate_expression(session.domain, student_response)
        if misconception and misconception.get("has_misconception"):
            return {
                "step_index": current_step.step_index,
                "is_correct": False,
                "has_misconception": True,
                "feedback_bn": misconception["remediation_bn"],
                "feedback_en": misconception["remediation_en"],
                "step_completed": False,
            }

        # 2. Check for expected keywords or algebraic indicators
        matched = False
        lowered_response = student_response.lower()
        if not current_step.expected_concept_keywords:
            matched = True
        else:
            for kw in current_step.expected_concept_keywords:
                if kw.lower() in lowered_response:
                    matched = True
                    break

        if matched:
            current_step.is_completed = True
            is_all_done = session.is_all_steps_completed()

            # Advance current step index if more steps exist
            if not is_all_done and session.current_step_index < len(session.steps) - 1:
                session.current_step_index += 1

            session.updated_at = time.time()
            return {
                "step_index": current_step.step_index,
                "is_correct": True,
                "has_misconception": False,
                "feedback_bn": f"চমৎকার! {current_step.title} সম্পন্ন হয়েছে।",
                "feedback_en": f"Correct deduction for {current_step.title}.",
                "step_completed": True,
                "all_steps_completed": is_all_done,
                "next_step_index": session.current_step_index,
            }
        else:
            return {
                "step_index": current_step.step_index,
                "is_correct": False,
                "has_misconception": False,
                "feedback_bn": "আপনার উত্তরের যুক্তিটি আরও স্পষ্ট করুন বা সক্রেটিক সংকেতটি পুনরায় লক্ষ্য করুন।",
                "feedback_en": "Refine your step derivation or inspect the pedagogical hint.",
                "step_completed": False,
                "all_steps_completed": False,
            }

    def append_stroke(
        self,
        session_id: str,
        student_id: str,
        stroke: DrawingStroke
    ) -> List[DrawingStroke]:
        """
        Appends a validated stroke to the student's canvas buffer.
        """
        session = self.get_session(session_id, student_id)
        session.strokes = DrawingStrokeBuffer.validate_and_append_stroke(session.strokes, stroke)
        session.updated_at = time.time()
        return session.strokes
