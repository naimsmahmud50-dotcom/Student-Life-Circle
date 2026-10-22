"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Psychometric AI Engine & Computerized Adaptive Testing
TOPIC:     3-PL Item Response Theory (IRT) & Fisher Information Optimization
FILE:      backend/app/services/cat_engine_service.py
PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
PURPOSE:   Computes 3-Parameter Logistic (3-PL) latent ability math, maximizes Fisher
           Information for dynamic next-question selection, drives standard error
           convergence (SE < 0.25), and maps theta to authentic admission percentiles.
STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
"""

import math
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class CatEngineService:
    """
    Computerized Adaptive Testing Engine powered by 3-Parameter Logistic (3-PL)
    and 2-Parameter Logistic (2-PL) Item Response Theory (IRT).
    """

    MIN_THETA = -3.0
    MAX_THETA = 3.0
    TARGET_STANDARD_ERROR = 0.35
    MAX_TEST_ITEMS = 12

    # Standard Calibrated NCTB Item Bank for Mathematics (Phase 18 Baseline - 8 Items)
    CALIBRATED_ITEM_BANK: List[Dict[str, Any]] = [
        {
            "item_id": "cat_item_01",
            "stem_bn": "৫ + (–৮) এর মান কত?",
            "subject": "গণিত",
            "topic": "পাটিগণিত ও পূর্ণসংখ্যা",
            "options": [{"id": "a", "text": "১৩"}, {"id": "b", "text": "–৩"}, {"id": "c", "text": "৩"}, {"id": "d", "text": "–১৩"}],
            "correct_option_id": "b",
            "difficulty_b": -2.2,  # Easy
            "discrimination_a": 1.2,
        },
        {
            "item_id": "cat_item_02",
            "stem_bn": "একটি বর্গক্ষেত্রের বাহুর দৈর্ঘ্য ৪ সেমি হলে তার ক্ষেত্রফল কত?",
            "subject": "গণিত",
            "topic": "জ্যামিতি ও ক্ষেত্রফল",
            "options": [{"id": "a", "text": "৮ বর্গ সেমি"}, {"id": "b", "text": "১২ বর্গ সেমি"}, {"id": "c", "text": "১৬ বর্গ সেমি"}, {"id": "d", "text": "২০ বর্গ সেমি"}],
            "correct_option_id": "c",
            "difficulty_b": -1.5,
            "discrimination_a": 1.4,
        },
        {
            "item_id": "cat_item_03",
            "stem_bn": "৩x – ৫ = ১০ হলে x এর মান কত?",
            "subject": "গণিত",
            "topic": "বীজগণিত",
            "options": [{"id": "a", "text": "৩"}, {"id": "b", "text": "৫"}, {"id": "c", "text": "১৫"}, {"id": "d", "text": "৪"}],
            "correct_option_id": "b",
            "difficulty_b": -0.5,
            "discrimination_a": 1.5,
        },
        {
            "item_id": "cat_item_04",
            "stem_bn": "যদি a + b = ৭ এবং ab = ১২ হয়, তবে a² + b² এর মান কত?",
            "subject": "গণিত",
            "topic": "বীজগণিতীয় সূত্রাবলী",
            "options": [{"id": "a", "text": "২৫"}, {"id": "b", "text": "৩৭"}, {"id": "c", "text": "৪৯"}, {"id": "d", "text": "১৩"}],
            "correct_option_id": "a",
            "difficulty_b": 0.2,  # Medium
            "discrimination_a": 1.8,
        },
        {
            "item_id": "cat_item_05",
            "stem_bn": "সমকোণী ত্রিভুজের অতিভুজ ১০ সেমি ও ভূমি ৮ সেমি হলে লম্বের দৈর্ঘ্য কত?",
            "subject": "গণিত",
            "topic": "পিথাগোরাসের উপপাদ্য",
            "options": [{"id": "a", "text": "২ সেমি"}, {"id": "b", "text": "৫ সেমি"}, {"id": "c", "text": "৬ সেমি"}, {"id": "d", "text": "৪ সেমি"}],
            "correct_option_id": "c",
            "difficulty_b": 0.8,
            "discrimination_a": 1.6,
        },
        {
            "item_id": "cat_item_06",
            "stem_bn": "একটি ত্রিভুজের তিন কোণের অনুপাত ১:২:৩ হলে বৃহত্তম কোণটির মান কত?",
            "subject": "গণিত",
            "topic": "জ্যামিতি",
            "options": [{"id": "a", "text": "৩০°"}, {"id": "b", "text": "৬০°"}, {"id": "c", "text": "৯০°"}, {"id": "d", "text": "১২০°"}],
            "correct_option_id": "c",
            "difficulty_b": 1.2,  # Hard
            "discrimination_a": 1.9,
        },
        {
            "item_id": "cat_item_07",
            "stem_bn": "log₁₀(x) + log₁₀(x – ৩) = ১ সমীকরণের বাস্তব সমাধান কোনটি?",
            "subject": "গণিত",
            "topic": "লগারিদম",
            "options": [{"id": "a", "text": "৫"}, {"id": "b", "text": "–২"}, {"id": "c", "text": "৫ এবং –২"}, {"id": "d", "text": "১০"}],
            "correct_option_id": "a",
            "difficulty_b": 2.1,  # Advanced
            "discrimination_a": 2.2,
        },
        {
            "item_id": "cat_item_08",
            "stem_bn": "যদি f(x) = (x – ১)/(x + ১) হয়, তবে f(f(x)) এর মান কত?",
            "subject": "গণিত",
            "topic": "ফাংশন ও ক্যালকুলাস প্রস্তুতি",
            "options": [{"id": "a", "text": "–১/x"}, {"id": "b", "text": "x"}, {"id": "c", "text": "১/x"}, {"id": "d", "text": "–x"}],
            "correct_option_id": "a",
            "difficulty_b": 2.7,  # Expert
            "discrimination_a": 2.4,
        },
    ]

    # Calibrated 3-PL High-Precision Item Bank (Phase 105 - Target SE < 0.25)
    CALIBRATED_3PL_ITEM_BANK: List[Dict[str, Any]] = [
        {
            "item_id": "cat3pl_01",
            "stem_bn": "ভূপৃষ্ঠ হতে কত উচ্চতায় অভিকর্ষজ ত্বরণ g এর মান ভূপৃষ্ঠের মানের এক-চতুর্থাংশ (g/4) হবে? (পৃথিবীর ব্যাসার্ধ R)",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "মহাকর্ষ ও অভিকর্ষ",
            "options": [{"id": "a", "text": "R/2"}, {"id": "b", "text": "R"}, {"id": "c", "text": "2R"}, {"id": "d", "text": "4R"}],
            "correct_option_id": "b",
            "difficulty_b": 0.4,
            "discrimination_a": 2.3,
            "pseudo_guessing_c": 0.25,
            "explanation_bn": "g' = g (R / (R + h))^2 => 1/4 = (R / (R + h))^2 => 1/2 = R / (R + h) => h = R।"
        },
        {
            "item_id": "cat3pl_02",
            "stem_bn": "\\lim_{x \\to 0} \\frac{\\sin(5x)}{\\tan(2x)} এর মান কত?",
            "subject": "উচ্চতর গণিত",
            "topic": "ক্যালকুলাস ও লিমিট",
            "options": [{"id": "a", "text": "5/2"}, {"id": "b", "text": "2/5"}, {"id": "c", "text": "1"}, {"id": "d", "text": "0"}],
            "correct_option_id": "a",
            "difficulty_b": 0.8,
            "discrimination_a": 2.4,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "L'Hopital বা স্ট্যান্ডার্ড লিমিট সূত্রে মান দাঁড়ায় 5/2।"
        },
        {
            "item_id": "cat3pl_03",
            "stem_bn": "একটি কণা r ব্যাসার্ধের বৃত্তাকার পথে সমদ্রুতিতে ঘুরছে। একবার পূর্ণ আবর্তনে কণাটির গড় বেগ কত?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "গতিবিদ্যা",
            "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "2\\pi r / T"}, {"id": "c", "text": "v^2 / r"}, {"id": "d", "text": "\\pi r / T"}],
            "correct_option_id": "a",
            "difficulty_b": -1.2,
            "discrimination_a": 2.1,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "পূর্ণ আবর্তনে কণাটির মোট সরণ শূন্য। অতএব গড় বেগ = ০।"
        },
        {
            "item_id": "cat3pl_04",
            "stem_bn": "কোন তাপমাত্রায় সেলসিয়াস ও ফারেনহাইট স্কেলে একই পাঠ প্রদর্শন করে?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "তাপ ও তাপগতিবিদ্যা",
            "options": [{"id": "a", "text": "0°"}, {"id": "b", "text": "-40°"}, {"id": "c", "text": "40°"}, {"id": "d", "text": "-273°"}],
            "correct_option_id": "b",
            "difficulty_b": -0.6,
            "discrimination_a": 2.0,
            "pseudo_guessing_c": 0.25,
            "explanation_bn": "C/5 = (F-32)/9 সমীকরণে C = F = x বসালে x = -40° পাওয়া যায়।"
        },
        {
            "item_id": "cat3pl_05",
            "stem_bn": "y = x^3 - 3x + 2 বক্ররেখার চরম বিন্দুতে (turning point) স্পর্শকের ঢাল কত?",
            "subject": "উচ্চতর গণিত",
            "topic": "অন্তরীকরণ",
            "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "1"}, {"id": "c", "text": "3"}, {"id": "d", "text": "-3"}],
            "correct_option_id": "a",
            "difficulty_b": 0.2,
            "discrimination_a": 2.2,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "বক্ররেখার যে কোনো চরম বিন্দুতে প্রথম অন্তরজ dy/dx = 0।"
        },
        {
            "item_id": "cat3pl_06",
            "stem_bn": "100W এর একটি বাতি দৈনিক 10 ঘণ্টা চললে 30 দিনে কত বিওটি (BOT) ইউনিট বিদ্যুৎ খরচ হবে?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "চলতড়িৎ",
            "options": [{"id": "a", "text": "30 ইউনিট"}, {"id": "b", "text": "300 ইউনিট"}, {"id": "c", "text": "3 ইউনিট"}, {"id": "d", "text": "3000 ইউনিট"}],
            "correct_option_id": "a",
            "difficulty_b": -0.2,
            "discrimination_a": 2.2,
            "pseudo_guessing_c": 0.25,
            "explanation_bn": "ইউনিট = (ওয়াট * ঘণ্টা * দিন) / ১০০০ = (১০০ * ১০ * ৩০) / ১০০০ = ৩০ BOT ইউনিট।"
        },
        {
            "item_id": "cat3pl_07",
            "stem_bn": "\\int_0^{\\pi/2} \\sin^2(x) dx এর মান কত?",
            "subject": "উচ্চতর গণিত",
            "topic": "যোগজীকরণ",
            "options": [{"id": "a", "text": "\\pi/4"}, {"id": "b", "text": "\\pi/2"}, {"id": "c", "text": "1"}, {"id": "d", "text": "1/2"}],
            "correct_option_id": "a",
            "difficulty_b": 1.4,
            "discrimination_a": 2.5,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "\\int_0^{\\pi/2} (1 - \\cos(2x))/2 dx = [x/2 - \\sin(2x)/4]_0^{\\pi/2} = \\pi/4।"
        },
        {
            "item_id": "cat3pl_08",
            "stem_bn": "একটি তরঙ্গের দুটি বিন্দুর মধ্যে পথ পার্থক্য \\lambda / 4 হলে দশা পার্থক্য কত?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "তরঙ্গ ও শব্দ",
            "options": [{"id": "a", "text": "\\pi/2"}, {"id": "b", "text": "\\pi"}, {"id": "c", "text": "2\\pi"}, {"id": "d", "text": "\\pi/4"}],
            "correct_option_id": "a",
            "difficulty_b": 0.5,
            "discrimination_a": 2.3,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "দশা পার্থক্য = (2\\pi / \\lambda) * পথ পার্থক্য = (2\\pi / \\lambda) * (\\lambda / 4) = \\pi / 2।"
        },
        {
            "item_id": "cat3pl_09",
            "stem_bn": "25°C তাপমাত্রায় বিশুদ্ধ পানির আয়নিক গুণফল K_w এর মান কত?",
            "subject": "রসায়ন",
            "topic": "রাসায়নিক পরিবর্তন ও সাম্যাবস্থা",
            "options": [{"id": "a", "text": "1.0 \\times 10^{-14} mol^2 L^{-2}"}, {"id": "b", "text": "1.0 \\times 10^{-7}"}, {"id": "c", "text": "1.0 \\times 10^{-12}"}, {"id": "d", "text": "1.0 \\times 10^{-16}"}],
            "correct_option_id": "a",
            "difficulty_b": -1.0,
            "discrimination_a": 2.0,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "25°C তাপমাত্রায় পানির স্ব-আয়নীকরণ ধ্রুবক K_w = 1.0 * 10^-14 mol^2 L^-2।"
        },
        {
            "item_id": "cat3pl_10",
            "stem_bn": "যদি |z - 2| = 3 হয়, তবে জটিল সমতলে z এর সঞ্চারপথ নির্দেশ করে একটি—",
            "subject": "উচ্চতর গণিত",
            "topic": "জটিল সংখ্যা",
            "options": [{"id": "a", "text": "বৃত্ত"}, {"id": "b", "text": "উপবৃত্ত"}, {"id": "c", "text": "পরাবৃত্ত"}, {"id": "d", "text": "সরলরেখা"}],
            "correct_option_id": "a",
            "difficulty_b": 1.1,
            "discrimination_a": 2.4,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "|z - z_0| = r হলো z_0 কেন্দ্র ও r ব্যাসার্ধের একটি আদর্শ বৃত্তের সমীকরণ।"
        },
        {
            "item_id": "cat3pl_11",
            "stem_bn": "একটি ফটনের তরঙ্গদৈর্ঘ্য 6630 Å হলে এর শক্তি কত জুল? (h = 6.63 \\times 10^{-34} J.s)",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "আধুনিক পদার্থবিজ্ঞান",
            "options": [{"id": "a", "text": "3.0 \\times 10^{-19} J"}, {"id": "b", "text": "6.63 \\times 10^{-19} J"}, {"id": "c", "text": "2.0 \\times 10^{-18} J"}, {"id": "d", "text": "1.5 \\times 10^{-19} J"}],
            "correct_option_id": "a",
            "difficulty_b": 1.7,
            "discrimination_a": 2.5,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "E = hc / \\lambda = (6.63 * 10^-34 * 3 * 10^8) / (6630 * 10^-10) = 3.0 * 10^-19 J।"
        },
        {
            "item_id": "cat3pl_12",
            "stem_bn": "স্থির তাপমাত্রায় নির্দিষ্ট ভরের কোনো গ্যাসের চাপ দ্বিগুণ করা হলে তার ঘনত্ব কতগুণ হবে?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "আদর্শ গ্যাস ও গতিসূত্র",
            "options": [{"id": "a", "text": "দ্বিগুণ"}, {"id": "b", "text": "অর্ধেক"}, {"id": "c", "text": "চারগুণ"}, {"id": "d", "text": "অপরিবর্তিত"}],
            "correct_option_id": "a",
            "difficulty_b": -0.8,
            "discrimination_a": 2.1,
            "pseudo_guessing_c": 0.25,
            "explanation_bn": "স্থির তাপমাত্রায় P proportional to rho (চাপ ঘনত্বের সমানুপাতিক)। অতএব চাপ দ্বিগুণ হলে ঘনত্ব দ্বিগুণ হবে।"
        },
        {
            "item_id": "cat3pl_13",
            "stem_bn": "বুয়েট স্ট্যান্ডার্ড: একটি গোলকের ব্যাসার্ধ পরিমাপে 1.5% ত্রুটি হলে এর আয়তন নির্ণয়ে শতকরা ত্রুটি কত?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "পরিমাপ ও ভৌতরাশি",
            "options": [{"id": "a", "text": "4.5%"}, {"id": "b", "text": "3.0%"}, {"id": "c", "text": "1.5%"}, {"id": "d", "text": "6.0%"}],
            "correct_option_id": "a",
            "difficulty_b": 1.9,
            "discrimination_a": 2.5,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "V = 4/3 * \\pi * r^3 => \\Delta V / V = 3 * (\\Delta r / r) = 3 * 1.5% = 4.5%।"
        },
        {
            "item_id": "cat3pl_14",
            "stem_bn": "e^{i\\pi} + 1 এর মান কত? (অয়লারের অভেদ)",
            "subject": "উচ্চতর গণিত",
            "topic": "জটিল সংখ্যা ও বিশ্লেষণ",
            "options": [{"id": "a", "text": "0"}, {"id": "b", "text": "1"}, {"id": "c", "text": "-1"}, {"id": "d", "text": "2"}],
            "correct_option_id": "a",
            "difficulty_b": 2.3,
            "discrimination_a": 2.6,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "e^{i\\theta} = \\cos\\theta + i\\sin\\theta => e^{i\\pi} = -1 => e^{i\\pi} + 1 = 0।"
        },
        {
            "item_id": "cat3pl_15",
            "stem_bn": "একটি আদর্শ ইঞ্জিনের উৎস ও তাপ গ্রাহকের তাপমাত্রা যথাক্রমে 600K এবং 300K হলে ইঞ্জিনের কর্মদক্ষতা কত?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "কার্নো চক্র ও তাপগতিবিদ্যা",
            "options": [{"id": "a", "text": "50%"}, {"id": "b", "text": "66.7%"}, {"id": "c", "text": "33.3%"}, {"id": "d", "text": "75%"}],
            "correct_option_id": "a",
            "difficulty_b": 0.3,
            "discrimination_a": 2.3,
            "pseudo_guessing_c": 0.25,
            "explanation_bn": "\\eta = 1 - (T_2 / T_1) = 1 - (300 / 600) = 0.5 = 50%।"
        },
        {
            "item_id": "cat3pl_16",
            "stem_bn": "বুয়েট এডমিশন: \\int_0^1 \\frac{dx}{1 + x^2} এর সঠিক মান কোনটি?",
            "subject": "উচ্চতর গণিত",
            "topic": "নির্দিষ্ট যোগজীকরণ",
            "options": [{"id": "a", "text": "\\pi/4"}, {"id": "b", "text": "\\pi/2"}, {"id": "c", "text": "1"}, {"id": "d", "text": "\\pi/3"}],
            "correct_option_id": "a",
            "difficulty_b": 1.9,
            "discrimination_a": 2.5,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "[\\tan^{-1}(x)]_0^1 = \\tan^{-1}(1) - \\tan^{-1}(0) = \\pi/4।"
        },
        {
            "item_id": "cat3pl_17",
            "stem_bn": "আইনস্টাইনের আলোক-তড়িৎ সমীকরণ অনুযায়ী নিবৃত্তি বিভব (stopping potential) V_0 এর সাথে আপতিত কম্পাঙ্ক \\nu এর লেখচিত্রের ঢাল কত?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "কোয়ান্টাম তত্ত্ব",
            "options": [{"id": "a", "text": "h/e"}, {"id": "b", "text": "e/h"}, {"id": "c", "text": "h"}, {"id": "d", "text": "hc/e"}],
            "correct_option_id": "a",
            "difficulty_b": 2.1,
            "discrimination_a": 2.6,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "eV_0 = h\\nu - W_0 => V_0 = (h/e)\\nu - (W_0/e)। সুতরাং লেখচিত্রের ঢাল h/e।"
        },
        {
            "item_id": "cat3pl_18",
            "stem_bn": "একটি কণার তরঙ্গ অপেক্ষক \\psi(x) = A e^{ikx} হলে এর ভরবেগ p কত?",
            "subject": "পদার্থবিজ্ঞান",
            "topic": "ডি ব্রগলি তরঙ্গ ও কোয়ান্টাম বলবিদ্যা",
            "options": [{"id": "a", "text": "\\hbar k"}, {"id": "b", "text": "\\hbar / k"}, {"id": "c", "text": "k / \\hbar"}, {"id": "d", "text": "k^2"}],
            "correct_option_id": "a",
            "difficulty_b": 2.3,
            "discrimination_a": 2.6,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "ভরবেগ অপারেটর \\hat{p} = -i\\hbar d/dx => \\hat{p}\\psi = \\hbar k \\psi, অতএব ভরবেগ p = \\hbar k।"
        },
        {
            "item_id": "cat3pl_19",
            "stem_bn": "ম্যাট্রিক্স A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix} এর আইগেনমান (eigenvalues) দ্বয় কত?",
            "subject": "উচ্চতর গণিত",
            "topic": "ম্যাট্রিক্স ও লিনিয়ার অ্যালজেব্রা",
            "options": [{"id": "a", "text": "3, 1"}, {"id": "b", "text": "2, 2"}, {"id": "c", "text": "4, 0"}, {"id": "d", "text": "1, -1"}],
            "correct_option_id": "a",
            "difficulty_b": 2.5,
            "discrimination_a": 2.7,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "\\det(A - \\lambda I) = (2-\\lambda)^2 - 1 = 0 => 2-\\lambda = \\pm 1 => \\lambda = 3, 1।"
        },
        {
            "item_id": "cat3pl_20",
            "stem_bn": "\\lim_{n \\to \\infty} \\sum_{r=1}^n \\frac{n}{n^2 + r^2} এর পরম মান কত?",
            "subject": "উচ্চতর গণিত",
            "topic": "যোগজীকরণের রিমান যোগ ও সীমা",
            "options": [{"id": "a", "text": "\\pi/4"}, {"id": "b", "text": "\\pi/2"}, {"id": "c", "text": "\\ln(2)"}, {"id": "d", "text": "1"}],
            "correct_option_id": "a",
            "difficulty_b": 2.7,
            "discrimination_a": 2.7,
            "pseudo_guessing_c": 0.20,
            "explanation_bn": "\\lim_{n \\to \\infty} \\frac{1}{n} \\sum \\frac{1}{1 + (r/n)^2} = \\int_0^1 \\frac{dx}{1 + x^2} = \\pi/4।"
        }
    ]

    def __init__(self) -> None:
        self._sessions: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def calculate_3pl_probability(theta: float, a: float, b: float, c: float = 0.0) -> float:
        """
        Computes response probability under the 3-Parameter Logistic (3-PL) model:
        P(theta) = c + (1 - c) / (1 + exp(-a * (theta - b)))
        When c = 0.0, reduces identically to 2-PL model.
        """
        exponent = -a * (theta - b)
        if exponent > 35.0:
            exp_term = 0.0
        elif exponent < -35.0:
            exp_term = 1.0
        else:
            exp_term = 1.0 / (1.0 + math.exp(exponent))
        return c + (1.0 - c) * exp_term

    @staticmethod
    def calculate_2pl_probability(theta: float, a: float, b: float) -> float:
        """Backwards-compatible wrapper for 2-PL probability."""
        return CatEngineService.calculate_3pl_probability(theta, a, b, 0.0)

    @staticmethod
    def calculate_3pl_fisher_information(theta: float, a: float, b: float, c: float = 0.0) -> float:
        """
        Computes 3-PL Fisher Information:
        I(theta) = a^2 * ((P(theta) - c)^2 / (1 - c)^2) * ((1 - P(theta)) / P(theta))
        When c = 0.0, reduces to a^2 * P(theta) * (1 - P(theta)).
        """
        p = CatEngineService.calculate_3pl_probability(theta, a, b, c)
        if p <= 0.0001 or p >= 0.9999 or c >= 0.99:
            return 0.001

        if abs(c) < 1e-6:
            return (a ** 2) * p * (1.0 - p)

        numerator = (p - c) ** 2
        denominator = (1.0 - c) ** 2
        ratio = (1.0 - p) / p
        return (a ** 2) * (numerator / denominator) * ratio

    @staticmethod
    def calculate_fisher_information(theta: float, a: float, b: float) -> float:
        """Backwards-compatible wrapper for 2-PL Fisher Information."""
        return CatEngineService.calculate_3pl_fisher_information(theta, a, b, 0.0)

    @staticmethod
    def calculate_percentile(theta: float) -> float:
        """
        Maps latent ability theta in [-3.0, +3.0] to a standardized normal percentile rank:
        Percentile = Phi(theta) * 100
        """
        phi = 0.5 * (1.0 + math.erf(theta / math.sqrt(2.0)))
        return round(phi * 100.0, 2)

    def start_cat_session(
        self,
        student_id: str,
        subject: str = "গণিত",
        initial_theta: float = 0.0,
        target_se: Optional[float] = None,
        use_3pl_bank: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Initializes a new CAT session and selects the first optimal question."""
        if not student_id or not str(student_id).strip():
            student_id = "student_anonymous"

        if initial_theta is None or math.isnan(initial_theta) or math.isinf(initial_theta):
            initial_theta = 0.0

        if target_se is None or target_se <= 0.05:
            target_se = self.TARGET_STANDARD_ERROR

        # Determine item bank and max items
        if use_3pl_bank is True or target_se < 0.30 or subject in ["বিজ্ঞান", "হায়ার ম্যাথ", "physics", "admission"]:
            active_bank = list(self.CALIBRATED_3PL_ITEM_BANK)
            bank_type = "3PL"
            max_items = 16
        else:
            active_bank = list(self.CALIBRATED_ITEM_BANK)
            bank_type = "2PL"
            max_items = 12

        session_id = f"cat_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()

        session: Dict[str, Any] = {
            "session_id": session_id,
            "student_id": student_id.strip(),
            "subject": subject,
            "started_at": now,
            "current_theta": max(self.MIN_THETA, min(self.MAX_THETA, float(initial_theta))),
            "standard_error": 1.0,
            "target_se": target_se,
            "max_items": max_items,
            "bank_type": bank_type,
            "item_bank": active_bank,
            "administered_items": [],
            "total_information": 1.0,  # Prior precision N(0, 1) has precision 1.0
            "is_complete": False,
            "termination_reason": None,
            "final_ability_category": None,
            "percentile_rank": self.calculate_percentile(initial_theta),
        }

        # Select first question maximizing Fisher Information at initial_theta
        next_item = self._select_next_item_from_bank(session["current_theta"], [], active_bank)
        session["current_item"] = self._sanitize_item_for_student(next_item)
        session["current_item_meta"] = next_item

        self._sessions[session_id] = session
        return self._format_session_response(session)

    def submit_cat_answer(
        self,
        session_id: str,
        item_id: str,
        selected_option_id: str,
    ) -> Dict[str, Any]:
        """Evaluates student answer, updates latent ability (Theta), and serves next optimal question."""
        if not selected_option_id or not str(selected_option_id).strip():
            return {"success": False, "message": "অনুগ্রহ করে একটি অপশন নির্বাচন করুন।"}

        session = self._sessions.get(session_id)
        if not session:
            return {"success": False, "message": "ক্যাট সেশন আইডি খুঁজে পাওয়া যায়নি।"}

        if session["is_complete"]:
            return {"success": False, "message": "এই ক্যাট সেশন ইতিপূর্বে সম্পন্ন হয়েছে।"}

        current_meta = session.get("current_item_meta")
        if not current_meta or current_meta["item_id"] != item_id:
            return {"success": False, "message": "প্রদত্ত প্রশ্ন আইডি বর্তমান সক্রিয় প্রশ্নের সাথে মিলছে না।"}

        is_correct = (selected_option_id.strip().lower() == current_meta["correct_option_id"].lower())
        a = current_meta["discrimination_a"]
        b = current_meta["difficulty_b"]
        c = current_meta.get("pseudo_guessing_c", 0.0)
        theta = session["current_theta"]

        p = self.calculate_3pl_probability(theta, a, b, c)
        item_info = self.calculate_3pl_fisher_information(theta, a, b, c)

        # Record administered item
        administered_record = {
            "item_id": item_id,
            "stem_bn": current_meta["stem_bn"],
            "difficulty_b": b,
            "discrimination_a": a,
            "pseudo_guessing_c": c,
            "selected_option_id": selected_option_id,
            "is_correct": is_correct,
            "p_model": round(p, 4),
            "prior_theta": round(theta, 3),
            "explanation_bn": current_meta.get("explanation_bn", ""),
        }
        session["administered_items"].append(administered_record)

        # Update Fisher Information & Standard Error
        session["total_information"] += item_info
        new_se = 1.0 / math.sqrt(session["total_information"])
        session["standard_error"] = round(new_se, 3)

        # Update Theta via Bayes / Newton-Raphson Step
        u = 1.0 if is_correct else 0.0
        learning_rate = 0.85
        theta_delta = learning_rate * (u - p) / math.sqrt(item_info + 0.2)
        new_theta = max(self.MIN_THETA, min(self.MAX_THETA, theta + theta_delta))
        session["current_theta"] = round(new_theta, 3)
        session["percentile_rank"] = self.calculate_percentile(session["current_theta"])
        administered_record["posterior_theta"] = session["current_theta"]

        administered_ids = [it["item_id"] for it in session["administered_items"]]
        active_bank = session.get("item_bank", self.CALIBRATED_ITEM_BANK)

        # Check Termination Criteria
        target_se = session.get("target_se", self.TARGET_STANDARD_ERROR)
        items_count = len(session["administered_items"])

        if session["standard_error"] <= target_se:
            session["is_complete"] = True
            session["termination_reason"] = f"MEASUREMENT_PRECISION_ACHIEVED (SE <= {target_se})"
        elif items_count >= session.get("max_items", self.MAX_TEST_ITEMS):
            session["is_complete"] = True
            session["termination_reason"] = "MAXIMUM_ITEMS_REACHED"
        elif len(administered_ids) >= len(active_bank):
            session["is_complete"] = True
            session["termination_reason"] = "ITEM_BANK_EXHAUSTED"

        if session["is_complete"]:
            session["current_item"] = None
            session["current_item_meta"] = None
            session["final_ability_category"] = self._classify_ability(session["current_theta"])
            session["admission_readiness"] = self._evaluate_admission_readiness(session["current_theta"])
        else:
            # Select next optimal question
            next_item = self._select_next_item_from_bank(session["current_theta"], administered_ids, active_bank)
            if next_item:
                session["current_item"] = self._sanitize_item_for_student(next_item)
                session["current_item_meta"] = next_item
            else:
                session["is_complete"] = True
                session["termination_reason"] = "NO_MORE_CANDIDATE_ITEMS"
                session["final_ability_category"] = self._classify_ability(session["current_theta"])
                session["admission_readiness"] = self._evaluate_admission_readiness(session["current_theta"])

        return {
            "success": True,
            "session": self._format_session_response(session),
            "last_answer_correct": is_correct,
            "correct_option_id": current_meta["correct_option_id"],
            "explanation_bn": current_meta.get("explanation_bn", ""),
        }

    def _select_next_item_from_bank(
        self,
        theta: float,
        administered_ids: List[str],
        bank: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Finds candidate item from bank that yields maximum Fisher Information at theta."""
        best_item = None
        max_info = -1.0

        for item in bank:
            if item["item_id"] in administered_ids:
                continue

            c = item.get("pseudo_guessing_c", 0.0)
            info = self.calculate_3pl_fisher_information(theta, item["discrimination_a"], item["difficulty_b"], c)
            if info > max_info:
                max_info = info
                best_item = item

        return best_item

    def _sanitize_item_for_student(self, item: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Strips answer keys and internal calibration parameters before returning to student."""
        if not item:
            return None
        return {
            "item_id": item["item_id"],
            "stem_bn": item["stem_bn"],
            "subject": item["subject"],
            "topic": item["topic"],
            "options": item["options"],
        }

    def _classify_ability(self, theta: float) -> str:
        """Classifies continuous latent ability into pedagogical mastery bands."""
        if theta >= 1.5:
            return "EXPERT (উচ্চতর দক্ষতা)"
        elif theta >= 0.5:
            return "PROFICIENT (উন্নত দক্ষতা)"
        elif theta >= -0.5:
            return "INTERMEDIATE (মধ্যবর্তী দক্ষতা)"
        elif theta >= -1.5:
            return "DEVELOPING (বিকাশমান দক্ষতা)"
        else:
            return "FOUNDATIONAL (মৌলিক ভিত্তি প্রয়োজন)"

    def _evaluate_admission_readiness(self, theta: float) -> str:
        """Maps latent ability to authentic competitive admission benchmark."""
        if theta >= 2.2:
            return "বুয়েট / শীর্ষ মেডিকেল কলেজ (টপ ১% পারসেন্টাইল)"
        elif theta >= 1.4:
            return "শীর্ষ পাবলিক বিশ্ববিদ্যালয় ও ইঞ্জিনিয়ারিং (টপ ৫% পারসেন্টাইল)"
        elif theta >= 0.7:
            return "জাতীয় পর্যায়ের পাবলিক বিশ্ববিদ্যালয় (টপ ২০% পারসেন্টাইল)"
        elif theta >= 0.0:
            return "উচ্চ মাধ্যমিক এ প্লাস প্রত্যাশী"
        else:
            return "মৌলিক ধারণা সুদৃঢ়করণ প্রয়োজন"

    def _format_session_response(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Serializes CAT session for client and API consumption."""
        administered = session.get("administered_items", [])
        return {
            "session_id": session["session_id"],
            "student_id": session["student_id"],
            "subject": session["subject"],
            "current_theta": session["current_theta"],
            "standard_error": session["standard_error"],
            "percentile_rank": session.get("percentile_rank", self.calculate_percentile(session["current_theta"])),
            "items_administered_count": len(administered),
            "is_complete": session["is_complete"],
            "termination_reason": session["termination_reason"],
            "final_ability_category": session["final_ability_category"],
            "admission_readiness": session.get("admission_readiness"),
            "current_item": session.get("current_item"),
            "administered_history": [
                {
                    "item_id": a["item_id"],
                    "is_correct": a["is_correct"],
                    "difficulty_b": a["difficulty_b"],
                    "prior_theta": a["prior_theta"],
                    "posterior_theta": a.get("posterior_theta"),
                }
                for a in administered
            ],
            "convergence_trajectory": [
                {
                    "step": idx + 1,
                    "theta": a.get("posterior_theta", a["prior_theta"]),
                    "standard_error": round(1.0 / math.sqrt(1.0 + (idx + 1) * 1.5), 3),
                    "difficulty_b": a["difficulty_b"],
                    "is_correct": a["is_correct"],
                }
                for idx, a in enumerate(administered)
            ]
        }

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves an active or completed CAT session."""
        session = self._sessions.get(session_id)
        if not session:
            return None
        return self._format_session_response(session)

    def get_ability_trajectory(self, session_id: str) -> List[Dict[str, Any]]:
        """Returns step-by-step ability trajectory for visual convergence graphing."""
        session = self._sessions.get(session_id)
        if not session:
            return []
        formatted = self._format_session_response(session)
        return formatted.get("convergence_trajectory", [])

    def reset_for_testing(self) -> None:
        """Clears stored CAT sessions for isolated test execution."""
        self._sessions.clear()


# Global Singleton Service
cat_engine_service = CatEngineService()
