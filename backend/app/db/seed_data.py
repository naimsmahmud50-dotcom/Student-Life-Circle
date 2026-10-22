"""
========================================================================================
MODULE:    Academic Seed Data & Curriculum Registry
TOPIC:     NCTB Curriculum 2024, Class 7, SSC, HSC & University Admission Blueprints
FILE:      backend/app/db/seed_data.py
PURPOSE:   Supplies verified academic starter seeds for the Student Growth Platform.
           Includes NCTB curriculum hierarchies (Class 7, SSC, HSC), authentic
           subjects, chapters, verified question records with step-by-step Bengali
           explanations, and University Admission exam blueprints (DU Unit-A,
           BUET, Medical) with official negative marking rules (-0.25).
AUDIENCE:  Database Seeders, Integration Testers & AI Agents
STANDARDS: NCTB Alignment, Authentic Academic Bangla, Clean Architecture
========================================================================================
"""

from typing import Dict, List, Any
from backend.app.schemas.quiz_schema import QuizMode


CURRICULUM_SEEDS = [
    {
        "code": "NCTB_2024",
        "title": "জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (এনসিটিবি) ২০২৪",
        "year_established": 2024
    }
]

SUBJECT_SEEDS = [
    # Middle School (Class 7)
    {"code": "MATH_7", "stage": "MIDDLE", "name_bn": "গণিত", "name_en": "Mathematics"},
    {"code": "ENG_7", "stage": "MIDDLE", "name_bn": "ইংরেজি ব্যাকরণ", "name_en": "English Grammar"},
    {"code": "BAN_7", "stage": "MIDDLE", "name_bn": "বাংলা", "name_en": "Bangla"},
    {"code": "GK_7", "stage": "MIDDLE", "name_bn": "সাধারণ জ্ঞান", "name_en": "General Knowledge"},
    
    # SSC (Class 9-10)
    {"code": "SSC_PHYS", "stage": "SSC", "name_bn": "পদার্থবিজ্ঞান", "name_en": "Physics"},
    {"code": "SSC_CHEM", "stage": "SSC", "name_bn": "রসায়ন", "name_en": "Chemistry"},
    {"code": "SSC_HMATH", "stage": "SSC", "name_bn": "উচ্চতর গণিত", "name_en": "Higher Mathematics"},
    
    # HSC (Class 11-12)
    {"code": "HSC_PHYS_1", "stage": "HSC", "name_bn": "পদার্থবিজ্ঞান ১ম পত্র", "name_en": "Physics 1st Paper"},
    {"code": "HSC_CHEM_1", "stage": "HSC", "name_bn": "রসায়ন ১ম পত্র", "name_en": "Chemistry 1st Paper"},
    {"code": "HSC_MATH_1", "stage": "HSC", "name_bn": "উচ্চতর গণিত ১ম পত্র", "name_en": "Higher Math 1st Paper"},
    {"code": "HSC_BIO_1", "stage": "HSC", "name_bn": "জীববিজ্ঞান ১ম পত্র", "name_en": "Biology 1st Paper"},
    {"code": "HSC_ICT", "stage": "HSC", "name_bn": "তথ্য ও যোগাযোগ প্রযুক্তি", "name_en": "ICT"}
]

# Admission Exam Blueprints
ADMISSION_BLUEPRINTS = [
    {
        "id": "bp_du_unit_a",
        "title": "ঢাকা বিশ্ববিদ্যালয় ক-ইউনিট পূর্ণাঙ্গ মডেল টেস্ট",
        "mode": QuizMode.MOCK_EXAM,
        "stage": "ADMISSION",
        "total_questions": 60,
        "duration_seconds": 2700,  # 45 minutes
        "negative_marking_value": 0.25,
        "description": "পদার্থবিজ্ঞান, রসায়ন, গণিত ও জীববিজ্ঞানের উপর সমন্বিত টেস্ট।"
    },
    {
        "id": "bp_medical_mbbs",
        "title": "মেডিকেল ভর্তি পরীক্ষা (MBBS) প্রস্তুতি টেস্ট",
        "mode": QuizMode.MOCK_EXAM,
        "stage": "ADMISSION",
        "total_questions": 100,
        "duration_seconds": 3600,  # 60 minutes
        "negative_marking_value": 0.25,
        "description": "জীববিজ্ঞান (৩০), রসায়ন (২৫), পদার্থ (২০), ইংরেজি (১৫) ও সাধারণ জ্ঞান (১০)।"
    },
    {
        "id": "bp_buet_preli",
        "title": "বুয়েট প্রিলিমিনারি প্র্যাকটিস টেস্ট",
        "mode": QuizMode.MOCK_EXAM,
        "stage": "ADMISSION",
        "total_questions": 100,
        "duration_seconds": 3600,
        "negative_marking_value": 0.25,
        "description": "পদার্থ, রসায়ন এবং গণিতের উচ্চতর সমস্যা ও দ্রুত সমাধান।"
    }
]

# Authentic Question Seeds
ACADEMIC_QUESTION_SEEDS: List[Dict[str, Any]] = [
    # Question 1: HSC Physics - Newton's Laws
    {
        "id": "q_phys_newton_01",
        "subject_code": "HSC_PHYS_1",
        "chapter": "গতিবিদ্যা ও বলবিদ্যা",
        "stem_bn": "একটি স্থির বস্তুর ওপর ২০ নিউটন বল ৫ সেকেন্ড যাবত কাজ করলে বস্তুর ভরবেগের পরিবর্তন কত হবে?",
        "options": [
            {"id": "opt_pn1_a", "option_key": "A", "option_text_bn": "৪ কেজি মি/সে", "is_correct": False},
            {"id": "opt_pn1_b", "option_key": "B", "option_text_bn": "১০০ কেজি মি/সে", "is_correct": True},
            {"id": "opt_pn1_c", "option_key": "C", "option_text_bn": "২৫ কেজি মি/সে", "is_correct": False},
            {"id": "opt_pn1_d", "option_key": "D", "option_text_bn": "০.২৫ কেজি মি/সে", "is_correct": False},
        ],
        "explanation_bn": "বলের ঘাত = ভরবেগের পরিবর্তন (Δp) = বল (F) × সময় (t) = ২০ × ৫ = ১০০ কেজি মি/সে।",
        "cognitive_skill": "APPLICATION",
        "source_attribution": "এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৩য় অধ্যায়, পৃষ্ঠা ৮৮"
    },
    # Question 2: HSC Chemistry - Orbitals
    {
        "id": "q_chem_orbital_02",
        "subject_code": "HSC_CHEM_1",
        "chapter": "গুণগত রসায়ন",
        "stem_bn": "প্রধান কোয়ান্টাম সংখ্যা n = ৩ হলে সর্বোচ্চ কয়টি ইলেকট্রন ধারণ সম্ভব?",
        "options": [
            {"id": "opt_co2_a", "option_key": "A", "option_text_bn": "৮ টি", "is_correct": False},
            {"id": "opt_co2_b", "option_key": "B", "option_text_bn": "১৮ টি", "is_correct": True},
            {"id": "opt_co2_c", "option_key": "C", "option_text_bn": "৩২ টি", "is_correct": False},
            {"id": "opt_co2_d", "option_key": "D", "option_text_bn": "২ টি", "is_correct": False},
        ],
        "explanation_bn": "একটি প্রধান শক্তিস্তরে সর্বোচ্চ ইলেকট্রন ধারণক্ষমতার সূত্র হলো ২n²। n = ৩ হলে ২ × ৩² = ২ × ৯ = ১৮ টি।",
        "cognitive_skill": "REASONING",
        "source_attribution": "এনসিটিবি রসায়ন ১ম পত্র, ২য় অধ্যায়, পৃষ্ঠা ৪৫"
    },
    # Question 3: DU Admission - Higher Math Limits
    {
        "id": "q_math_limit_03",
        "subject_code": "HSC_MATH_1",
        "chapter": "অন্তরীকরণ (Calculus)",
        "stem_bn": "lim (x → 0) [sin(5x) / x] এর মান কত?",
        "options": [
            {"id": "opt_ml3_a", "option_key": "A", "option_text_bn": "১", "is_correct": False},
            {"id": "opt_ml3_b", "option_key": "B", "option_text_bn": "৫", "is_correct": True},
            {"id": "opt_ml3_c", "option_key": "C", "option_text_bn": "০", "is_correct": False},
            {"id": "opt_ml3_d", "option_key": "D", "option_text_bn": "১/৫", "is_correct": False},
        ],
        "explanation_bn": "lim (x → 0) [sin(5x) / (5x)] × ৫ = ১ × ৫ = ৫।",
        "cognitive_skill": "APPLICATION",
        "source_attribution": "ঢাকা বিশ্ববিদ্যালয় ক-ইউনিট পূর্ববর্তী ভর্তি পরীক্ষা"
    }
]
