"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bilingual Curriculum Engine & NCTB Terminology Lexicon
 * TOPIC:     Phase 136 Instant Medium Switcher & Contextual Academic Terminology
 * FILE:      backend/curriculum/lexicon_service.py
 * PHASE:     Phase 136 - Dual-Curriculum Bilingual Terminology Switcher
 * PURPOSE:   Provides bidirectional NCTB STEM terminology mapping, contextual
 *            definitions in Bengali and English, auto-glossing algorithms,
 *            and dynamic exam paper localization across Bangla & English Version tracks.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Pure Academic Design, NCTB Aligned
 */
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class AcademicMedium(str, Enum):
    BANGLA = "BANGLA"
    ENGLISH_VERSION = "ENGLISH_VERSION"
    BILINGUAL_DUAL = "BILINGUAL_DUAL"
    INLINE_ANNOTATED = "INLINE_ANNOTATED"


class CurriculumSubject(str, Enum):
    PHYSICS = "PHYSICS"
    CHEMISTRY = "CHEMISTRY"
    HIGHER_MATH = "HIGHER_MATH"
    BIOLOGY = "BIOLOGY"
    GENERAL_SCIENCE = "GENERAL_SCIENCE"


class GradeTier(str, Enum):
    SSC = "SSC"
    HSC = "HSC"
    ADMISSION = "ADMISSION"


@dataclass
class NCTBLexiconEntry:
    term_id: str
    term_en: str
    term_bn: str
    phonetic_en: str
    phonetic_bn: str
    subject: CurriculumSubject
    grade_tier: GradeTier
    definition_en: str
    definition_bn: str
    nctb_code: str
    synonyms_en: List[str] = field(default_factory=list)
    synonyms_bn: List[str] = field(default_factory=list)
    formula_latex: Optional[str] = None


@dataclass
class BilingualQuestionItem:
    question_id: str
    subject: CurriculumSubject
    grade_tier: GradeTier
    prompt_bn: str
    prompt_en: str
    options_bn: List[str]
    options_en: List[str]
    correct_index: int
    explanation_bn: str
    explanation_en: str
    matched_lexicon_ids: List[str] = field(default_factory=list)


# Authentic NCTB STEM Benchmark Lexicon Entries
BENCHMARK_NCTB_LEXICON: List[NCTBLexiconEntry] = [
    # --- PHYSICS (পদার্থবিজ্ঞান) ---
    NCTBLexiconEntry(
        term_id="LEX-PHY-001",
        term_en="Kinematics",
        term_bn="গতিবিদ্যা",
        phonetic_en="/ˌkɪn.əˈmæt.ɪks/",
        phonetic_bn="গতিবিদ্যা",
        subject=CurriculumSubject.PHYSICS,
        grade_tier=GradeTier.HSC,
        definition_en="Branch of classical mechanics that describes the motion of points, bodies, and systems of bodies without considering the forces that cause them to move.",
        definition_bn="বলবিদ্যার যে শাখায় গতির কারণ বা বলের প্রভাব বিবেচনা না করে কেবল বস্তুর অবস্থান, সরণ, দ্রুতি, বেগ ও ত্বরণ নিয়ে সুশৃঙ্খল আলোচনা করা হয়।",
        nctb_code="NCTB-PHY-C02-KINEMATICS",
        synonyms_en=["Motion Study", "Pure Motion"],
        synonyms_bn=["গতির বিজ্ঞান"],
        formula_latex="v = u + at, \\quad s = ut + \\frac{1}{2}at^2"
    ),
    NCTBLexiconEntry(
        term_id="LEX-PHY-002",
        term_en="Periodic Motion",
        term_bn="পর্যায়বৃত্ত গতি",
        phonetic_en="/ˌpɪr.iˈɑː.dɪk ˈmoʊ.ʃən/",
        phonetic_bn="পর্যায়বৃত্ত গতি",
        subject=CurriculumSubject.PHYSICS,
        grade_tier=GradeTier.HSC,
        definition_en="Motion repeated in equal intervals of time, where a particle passes through a specific point in a definite direction at fixed periods.",
        definition_bn="কোনো গতিশীল কণার গতি যদি এমন হয় যে এটি এর গতিপথের কোনো নির্দিষ্ট বিন্দুকে নির্দিষ্ট সময় পর পর একই দিক থেকে অতিক্রম করে।",
        nctb_code="NCTB-PHY-C08-PERIODIC",
        synonyms_en=["Harmonic Motion", "Oscillatory Motion"],
        synonyms_bn=["দোলন গতি"],
        formula_latex="T = 2\\pi \\sqrt{\\frac{L}{g}}"
    ),
    NCTBLexiconEntry(
        term_id="LEX-PHY-003",
        term_en="Work-Energy Theorem",
        term_bn="কাজ-শক্তি উপপাদ্য",
        phonetic_en="/wɜːrk ˈɛn.ər.dʒi ˈθɪər.əm/",
        phonetic_bn="কাজ-শক্তি উপপাদ্য",
        subject=CurriculumSubject.PHYSICS,
        grade_tier=GradeTier.HSC,
        definition_en="The net work done by the forces on an object equals the change in its kinetic energy.",
        definition_bn="কোনো বস্তুর ওপর প্রযুক্ত নিট বল দ্বারা সম্পন্ন কাজ বস্তুটির গতিশক্তির পরিবর্তনের সমান।",
        nctb_code="NCTB-PHY-C04-WORK-ENERGY",
        synonyms_en=["Work Energy Principle"],
        synonyms_bn=["কাজ শক্তি নীতি"],
        formula_latex="W_{\\text{net}} = \\Delta K = \\frac{1}{2}mv^2 - \\frac{1}{2}mu^2"
    ),
    NCTBLexiconEntry(
        term_id="LEX-PHY-004",
        term_en="Electromagnetic Induction",
        term_bn="তাড়িৎচৌম্বক আবেশ",
        phonetic_en="/iˌlɛk.troʊ.mæɡˈnɛt.ɪk ɪnˈdʌk.ʃən/",
        phonetic_bn="তাড়িৎচৌম্বক আবেশ",
        subject=CurriculumSubject.PHYSICS,
        grade_tier=GradeTier.HSC,
        definition_en="The production of an electromotive force across an electrical conductor in a changing magnetic field.",
        definition_bn="পরিবর্তনশীল চৌম্বক ক্ষেত্রের প্রভাবে কোনো পরিবাহী কুণ্ডলীতে ক্ষণস্থায়ী তড়িৎচালক বল বা তড়িৎ প্রবাহ সৃষ্টি হওয়ার ভৌত ঘটনা।",
        nctb_code="NCTB-PHY-C11-EM-INDUCTION",
        synonyms_en=["Faraday Induction"],
        synonyms_bn=["ফ্যারাডের আবেশ"],
        formula_latex="\\varepsilon = -N \\frac{d\\Phi_B}{dt}"
    ),

    # --- CHEMISTRY (রসায়ন) ---
    NCTBLexiconEntry(
        term_id="LEX-CHE-001",
        term_en="Periodic Table",
        term_bn="পর্যায় সারণি",
        phonetic_en="/ˌpɪr.iˈɑː.dɪk ˈteɪ.bəl/",
        phonetic_bn="পর্যায় সারণি",
        subject=CurriculumSubject.CHEMISTRY,
        grade_tier=GradeTier.SSC,
        definition_en="Tabular display of chemical elements arranged by atomic number, electron configuration, and recurring chemical properties.",
        definition_bn="মৌলসমূহের ভৌত ও রাসায়নিক ধর্মের পর্যায়ক্রমিক পুনরাবৃত্তি প্রদর্শনকারী পারমাণবিক সংখ্যার ভিত্তিতে বিন্যস্ত আন্তর্জাতিক সারণি।",
        nctb_code="NCTB-CHE-C04-PERIODIC",
        synonyms_en=["Mendeleev Table", "Elemental Chart"],
        synonyms_bn=["মৌলের পর্যায় তালিকা"],
        formula_latex=None
    ),
    NCTBLexiconEntry(
        term_id="LEX-CHE-002",
        term_en="Acid-Base Equilibrium",
        term_bn="অম্ল-ক্ষারক সাম্যাবস্থা",
        phonetic_en="/ˈæs.ɪd beɪs ˌiː.kwəˈlɪb.ri.əm/",
        phonetic_bn="অম্ল-ক্ষারক সাম্যাবস্থা",
        subject=CurriculumSubject.CHEMISTRY,
        grade_tier=GradeTier.HSC,
        definition_en="State of chemical balance in a solution involving proton donation and acceptance according to Brønsted–Lowry theory.",
        definition_bn="ব্রনস্টেড-লাউরি মতবাদ অনুসারে জলীয় দ্রবণে প্রোটন দান ও গ্রহণের গতিশীল রাসায়নিক ভারসাম্য অবস্থা।",
        nctb_code="NCTB-CHE-C05-ACID-BASE",
        synonyms_en=["pH Buffer Balance"],
        synonyms_bn=["পিএইচ সাম্য"],
        formula_latex="\\text{pH} = -\\log[H^+], \\quad \\text{pH} + \\text{pOH} = 14"
    ),
    NCTBLexiconEntry(
        term_id="LEX-CHE-003",
        term_en="Redox Reaction",
        term_bn="জারণ-বিজারণ বিক্রিয়া",
        phonetic_en="/ˈriː.dɑːks riˈæk.ʃən/",
        phonetic_bn="জারণ-বিজারণ বিক্রিয়া",
        subject=CurriculumSubject.CHEMISTRY,
        grade_tier=GradeTier.SSC,
        definition_en="Chemical process involving transfer of electrons between two species, with simultaneous oxidation and reduction.",
        definition_bn="যে রাসায়নিক বিক্রিয়ায় যুগপৎভাবে এক পদার্থ ইলেকট্রন বর্জন (জারণ) করে এবং অপর পদার্থ ইলেকট্রন গ্রহণ (বিজারণ) করে।",
        nctb_code="NCTB-CHE-C07-REDOX",
        synonyms_en=["Oxidation Reduction"],
        synonyms_bn=["ইলেকট্রন স্থানান্তর বিক্রিয়া"],
        formula_latex="\\text{Oxidation: } M \\rightarrow M^{n+} + ne^-"
    ),

    # --- HIGHER MATHEMATICS (উচ্চতর গণিত) ---
    NCTBLexiconEntry(
        term_id="LEX-MAT-001",
        term_en="Differentiation",
        term_bn="অন্তরীকরণ",
        phonetic_en="/ˌdɪf.əˌrɛn.ʃiˈeɪ.ʃən/",
        phonetic_bn="অন্তরীকরণ",
        subject=CurriculumSubject.HIGHER_MATH,
        grade_tier=GradeTier.HSC,
        definition_en="Mathematical process of calculating the instantaneous rate of change of a function with respect to one of its variables.",
        definition_bn="কোনো ফাংশনের স্বাধীন চলকের অতি ক্ষুদ্র পরিবর্তনের সাপেক্ষে অধীন চলকের পরিবর্তনের তাৎক্ষণিক হার নির্ণয়ের গাণিতিক প্রক্রিয়া।",
        nctb_code="NCTB-MAT-C09-CALCULUS",
        synonyms_en=["Derivative Calculation", "Differential Calculus"],
        synonyms_bn=["ব্যবকলন"],
        formula_latex="\\frac{df}{dx} = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}"
    ),
    NCTBLexiconEntry(
        term_id="LEX-MAT-002",
        term_en="Integration",
        term_bn="সমাকলন",
        phonetic_en="/ˌɪn.tɪˈɡreɪ.ʃən/",
        phonetic_bn="সমাকলন",
        subject=CurriculumSubject.HIGHER_MATH,
        grade_tier=GradeTier.HSC,
        definition_en="Operation of finding the integral of a function, representing continuous summation and area under a curved boundary.",
        definition_bn="অন্তরীকরণের বিপরীত প্রক্রিয়া যার মাধ্যমে অবিচ্ছিন্ন যোগফল ও বক্ররেখা দ্বারা আবদ্ধ ক্ষেত্রের ক্ষেত্রফল নির্ণয় করা হয়।",
        nctb_code="NCTB-MAT-C10-INTEGRATION",
        synonyms_en=["Antiderivative", "Integral Calculus"],
        synonyms_bn=["যোগজীকরণ"],
        formula_latex="\\int x^n dx = \\frac{x^{n+1}}{n+1} + C, \\quad (n \\neq -1)"
    ),
    NCTBLexiconEntry(
        term_id="LEX-MAT-003",
        term_en="Trigonometric Ratio",
        term_bn="ত্রিকোণমিতিক অনুপাত",
        phonetic_en="/ˌtrɪɡ.ə.nəˈmɛt.rɪk ˈreɪ.ʃi.oʊ/",
        phonetic_bn="ত্রিকোণমিতিক অনুপাত",
        subject=CurriculumSubject.HIGHER_MATH,
        grade_tier=GradeTier.SSC,
        definition_en="Ratios of sides of a right-angled triangle with respect to its acute angles (sine, cosine, tangent).",
        definition_bn="সমকোণী ত্রিভুজের সূক্ষ্মকোণের সাপেক্ষে বাহুগুলোর মধ্যকার নির্দিষ্ট অনুপাত (সাইন, কোসাইন, ট্যানজেন্ট ইত্যাদি)।",
        nctb_code="NCTB-MAT-C08-TRIGONOMETRY",
        synonyms_en=["Trig Functions"],
        synonyms_bn=["ত্রিকোণমিতিক ফাংশন"],
        formula_latex="\\sin^2\\theta + \\cos^2\\theta = 1"
    ),

    # --- BIOLOGY (জীববিজ্ঞান) ---
    NCTBLexiconEntry(
        term_id="LEX-BIO-001",
        term_en="Photosynthesis",
        term_bn="সালোকসংশ্লেষণ",
        phonetic_en="/ˌfoʊ.toʊˈsɪn.θə.sɪs/",
        phonetic_bn="সালোকসংশ্লেষণ",
        subject=CurriculumSubject.BIOLOGY,
        grade_tier=GradeTier.SSC,
        definition_en="Biological process by which green plants and certain other organisms transform light energy into chemical energy in the form of glucose.",
        definition_bn="যে শারীরবৃত্তীয় প্রক্রিয়ায় সবুজ উদ্ভিদ সূর্যালোক ও ক্লোরোফিলের উপস্থিতিতে পানি ও কার্বন ডাই-অক্সাইড থেকে শর্করা জাতীয় খাদ্য তৈরি করে।",
        nctb_code="NCTB-BIO-C04-BIOENERGETICS",
        synonyms_en=["Carbon Assimilation"],
        synonyms_bn=["আলোক রাসায়নিক সংশ্লেষ"],
        formula_latex="6CO_2 + 12H_2O \\xrightarrow{\\text{Light, Chlorophyll}} C_6H_{12}O_6 + 6H_2O + 6O_2"
    ),
    NCTBLexiconEntry(
        term_id="LEX-BIO-002",
        term_en="Cellular Respiration",
        term_bn="কোষীয় শ্বসন",
        phonetic_en="/ˈsɛl.jə.lər ˌrɛs.pəˈreɪ.ʃən/",
        phonetic_bn="কোষীয় শ্বসন",
        subject=CurriculumSubject.BIOLOGY,
        grade_tier=GradeTier.HSC,
        definition_en="Metabolic pathway that breaks down glucose and produces ATP through glycolysis, Krebs cycle, and oxidative phosphorylation.",
        definition_bn="কোষীয় পর্যায়ে অক্সিজেনের উপস্থিতিতে বা অনুপস্থিতিতে গ্লুকোজ জারিত হয়ে এটিপি (ATP) রূপে রাসায়নিক শক্তি উৎপন্ন হওয়ার সামগ্রিক বিপাকীয় প্রক্রিয়া।",
        nctb_code="NCTB-BIO-C09-RESPIRATION",
        synonyms_en=["Aerobic Respiration", "Catabolic Energy Release"],
        synonyms_bn=["জীবকোষীয় শ্বসন"],
        formula_latex="C_6H_{12}O_6 + 6O_2 \\rightarrow 6CO_2 + 6H_2O + 38\\text{ ATP}"
    )
]


# Benchmark Dual-Curriculum Questions for Exam Paper Rendering
BENCHMARK_BILINGUAL_QUESTIONS: List[BilingualQuestionItem] = [
    BilingualQuestionItem(
        question_id="Q-PHY-01",
        subject=CurriculumSubject.PHYSICS,
        grade_tier=GradeTier.HSC,
        prompt_bn="গতিবিদ্যা অনুসারে, কোনো বস্তুর সমত্বরণে যাত্রার ক্ষেত্রে নিচের কোন সমীকরণটি সঠিক নয়?",
        prompt_en="According to Kinematics, which of the following equations is incorrect for a body moving with uniform acceleration?",
        options_bn=[
            "v = u + at",
            "s = ut + (1/2)at^2",
            "v^2 = u^2 + 2as",
            "s = (u + v)t^2"
        ],
        options_en=[
            "v = u + at",
            "s = ut + (1/2)at^2",
            "v^2 = u^2 + 2as",
            "s = (u + v)t^2"
        ],
        correct_index=3,
        explanation_bn="সঠিক দূরত্বের সূত্র হলো s = ((u + v) / 2) * t, অতএব s = (u + v)t^2 সমীকরণটি ত্রুটিপূর্ণ।",
        explanation_en="The correct distance formula is s = ((u + v) / 2) * t; therefore, s = (u + v)t^2 is incorrect.",
        matched_lexicon_ids=["LEX-PHY-001"]
    ),
    BilingualQuestionItem(
        question_id="Q-CHE-02",
        subject=CurriculumSubject.CHEMISTRY,
        grade_tier=GradeTier.SSC,
        prompt_bn="আধুনিক পর্যায় সারণিতে পর্যায় বৃত্তাকার ধর্মের মধ্যে নিচের কোনটির মান বাম থেকে ডানে হ্রাস পায়?",
        prompt_en="In the modern Periodic Table, which of the following periodic properties decreases from left to right across a period?",
        options_bn=[
            "পারমাণবিক ব্যাসার্ধ (Atomic Radius)",
            "আয়नीकरण শক্তি (Ionization Energy)",
            "ইলেকট্রন আসক্তি (Electron Affinity)",
            "তড়িৎ ঋণাত্মকতা (Electronegativity)"
        ],
        options_en=[
            "Atomic Radius",
            "Ionization Energy",
            "Electron Affinity",
            "Electronegativity"
        ],
        correct_index=0,
        explanation_bn="একই পর্যায়ে বাম থেকে ডানে প্রোটন সংখ্যা বৃদ্ধি পাওয়ায় নিউক্লিয়াসের আকর্ষণ বৃদ্ধি পায়, ফলে পারমাণবিক ব্যাসার্ধ হ্রাস পায়।",
        explanation_en="Across a period from left to right, increasing nuclear charge pulls electrons closer, thereby decreasing the Atomic Radius.",
        matched_lexicon_ids=["LEX-CHE-001"]
    ),
    BilingualQuestionItem(
        question_id="Q-MAT-03",
        subject=CurriculumSubject.HIGHER_MATH,
        grade_tier=GradeTier.HSC,
        prompt_bn="অন্তরীকরণ প্রক্রিয়ায় d/dx (sin x) এর মান কত?",
        prompt_en="In the process of Differentiation, what is the derivative d/dx (sin x)?",
        options_bn=[
            "- cos x",
            "cos x",
            "tan x",
            "- sin x"
        ],
        options_en=[
            "- cos x",
            "cos x",
            "tan x",
            "- sin x"
        ],
        correct_index=1,
        explanation_bn="ক্যালকুলাসের স্ট্যান্ডার্ড সূত্র অনুসারে d/dx (sin x) = cos x।",
        explanation_en="By the fundamental rules of calculus, d/dx (sin x) = cos x.",
        matched_lexicon_ids=["LEX-MAT-001", "LEX-MAT-003"]
    )
]


class NCTBLexiconService:
    """
    Core curriculum terminology index and dual-medium exam auto-localization clearinghouse.
    """

    def __init__(self, initial_entries: Optional[List[NCTBLexiconEntry]] = None):
        self._entries_by_id: Dict[str, NCTBLexiconEntry] = {}
        self._entries_by_en: Dict[str, NCTBLexiconEntry] = {}
        self._entries_by_bn: Dict[str, NCTBLexiconEntry] = {}

        seed_data = initial_entries if initial_entries is not None else BENCHMARK_NCTB_LEXICON
        for entry in seed_data:
            self.register_entry(entry)

    def register_entry(self, entry: NCTBLexiconEntry) -> None:
        """Indexes an entry across ID, English term, and Bengali term."""
        self._entries_by_id[entry.term_id] = entry
        self._entries_by_en[entry.term_en.strip().lower()] = entry
        self._entries_by_bn[entry.term_bn.strip()] = entry

    @property
    def total_entries(self) -> int:
        return len(self._entries_by_id)

    def lookup_by_id(self, term_id: str) -> Optional[NCTBLexiconEntry]:
        return self._entries_by_id.get(term_id)

    def lookup_by_term(self, term: str) -> Optional[NCTBLexiconEntry]:
        """
        Bidirectional $O(1)$ lookup for either an English or Bengali academic term.
        """
        cleaned = term.strip()
        # Check Bengali exact match
        if cleaned in self._entries_by_bn:
            return self._entries_by_bn[cleaned]

        # Check English case-insensitive match
        en_key = cleaned.lower()
        if en_key in self._entries_by_en:
            return self._entries_by_en[en_key]

        return None

    def search_entries(
        self,
        query: str = "",
        subject: Optional[CurriculumSubject] = None,
        grade_tier: Optional[GradeTier] = None,
    ) -> List[NCTBLexiconEntry]:
        """
        Filters lexicon entries by search query, subject, and grade tier.
        """
        q = query.strip().lower()
        results: List[NCTBLexiconEntry] = []

        for entry in self._entries_by_id.values():
            if subject and entry.subject != subject:
                continue
            if grade_tier and entry.grade_tier != grade_tier:
                continue

            if not q:
                results.append(entry)
                continue

            # Check matches across EN, BN, code, and definitions
            match = (
                q in entry.term_en.lower()
                or q in entry.term_bn
                or q in entry.nctb_code.lower()
                or q in entry.definition_en.lower()
                or q in entry.definition_bn
                or any(q in syn.lower() for syn in entry.synonyms_en)
                or any(q in syn for syn in entry.synonyms_bn)
            )
            if match:
                results.append(entry)

        return results

    def annotate_text_with_glossary(
        self,
        text: str,
        source_medium: AcademicMedium = AcademicMedium.BANGLA,
    ) -> str:
        """
        Scans input academic text and embeds reciprocal NCTB translations as inline gloss annotations.
        """
        annotated = text
        if source_medium == AcademicMedium.BANGLA:
            # Look for Bengali terms and append English gloss
            for bn_term, entry in self._entries_by_bn.items():
                if bn_term in annotated and f"({entry.term_en})" not in annotated:
                    pattern = re.escape(bn_term)
                    annotated = re.sub(pattern, f"{bn_term} ({entry.term_en})", annotated)
        elif source_medium == AcademicMedium.ENGLISH_VERSION:
            # Look for English terms and append Bengali gloss
            for en_term_lower, entry in self._entries_by_en.items():
                # Case-insensitive word boundary match
                pattern = re.compile(rf"\b{re.escape(entry.term_en)}\b", re.IGNORECASE)
                if pattern.search(annotated) and f"({entry.term_bn})" not in annotated:
                    annotated = pattern.sub(f"{entry.term_en} ({entry.term_bn})", annotated)

        return annotated

    def render_question(
        self,
        question: BilingualQuestionItem,
        target_medium: AcademicMedium,
    ) -> Dict[str, Any]:
        """
        Transforms a bilingual question item into the desired layout mode:
        BANGLA, ENGLISH_VERSION, BILINGUAL_DUAL, or INLINE_ANNOTATED.
        """
        if target_medium == AcademicMedium.BANGLA:
            return {
                "question_id": question.question_id,
                "medium": AcademicMedium.BANGLA.value,
                "subject": question.subject.value,
                "prompt": question.prompt_bn,
                "options": list(question.options_bn),
                "correct_index": question.correct_index,
                "explanation": question.explanation_bn,
                "secondary": None,
                "mode": "SINGLE_MEDIUM"
            }
        elif target_medium == AcademicMedium.ENGLISH_VERSION:
            return {
                "question_id": question.question_id,
                "medium": AcademicMedium.ENGLISH_VERSION.value,
                "subject": question.subject.value,
                "prompt": question.prompt_en,
                "options": list(question.options_en),
                "correct_index": question.correct_index,
                "explanation": question.explanation_en,
                "secondary": None,
                "mode": "SINGLE_MEDIUM"
            }
        elif target_medium == AcademicMedium.INLINE_ANNOTATED:
            annotated_prompt = self.annotate_text_with_glossary(question.prompt_bn, AcademicMedium.BANGLA)
            return {
                "question_id": question.question_id,
                "medium": AcademicMedium.INLINE_ANNOTATED.value,
                "subject": question.subject.value,
                "prompt": annotated_prompt,
                "options": list(question.options_bn),
                "correct_index": question.correct_index,
                "explanation": question.explanation_bn,
                "secondary": None,
                "mode": "INLINE_GLOSS"
            }
        else:  # BILINGUAL_DUAL (Side-by-side)
            return {
                "question_id": question.question_id,
                "medium": AcademicMedium.BILINGUAL_DUAL.value,
                "subject": question.subject.value,
                "prompt": question.prompt_bn,
                "options": list(question.options_bn),
                "correct_index": question.correct_index,
                "explanation": question.explanation_bn,
                "secondary": {
                    "prompt": question.prompt_en,
                    "options": list(question.options_en),
                    "explanation": question.explanation_en,
                },
                "mode": "SIDE_BY_SIDE"
            }

    def get_benchmark_questions(self) -> List[BilingualQuestionItem]:
        return list(BENCHMARK_BILINGUAL_QUESTIONS)
