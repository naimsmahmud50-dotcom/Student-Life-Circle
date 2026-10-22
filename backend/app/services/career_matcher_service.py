"""
================================================================================
MODULE: Algorithmic Career Matching & Skill-to-Job Fit Engine (ক্যারিয়ার স্কিল-গ্যাপ ম্যাচিং ইঞ্জিন)
TOPIC: Skill Gap Analysis, Employability Indexing & Remediation Roadmapping
FILE: backend/app/services/career_matcher_service.py
PURPOSE: Matches a learner's verified competencies, quiz mastery records, and W3C
         credentials against real-world tech, tutoring, and assessment job profiles.
         Calculates an empirical Match Percentage (0-100%), identifies missing critical
         skills, and generates a structured Skill-Gap Bridge Roadmap with time-to-market
         sprint milestones to empower student career launching.
AUDIENCE: University Students, Fresh Graduates, Tuition Applicants, Tech Recruiters.
STANDARDS: SFIA (Skills Framework for the Information Age), NCTB Teaching Competencies.
================================================================================
"""

from typing import Any, Dict, List, Optional


class CareerMatcherService:
    """Algorithmic career fit engine evaluating candidate competencies against market roles."""

    ROLES_CATALOG: Dict[str, Dict[str, Any]] = {
        "role_python_dev": {
            "role_id": "role_python_dev",
            "title": "জুনিয়র পাইথন ব্যাকএন্ড ইঞ্জিনিয়ার (Junior Python Backend Engineer)",
            "industry": "Software & Web Development",
            "required_skills": ["Python", "FastAPI / Django", "SQL / PostgreSQL", "REST APIs", "Unit Testing"],
            "bonus_skills": ["Docker", "Redis", "CI/CD", "Security Standards"],
            "min_match_threshold": 60.0,
            "description": "স্কেলেবল ব্যাকএন্ড এপিআই তৈরি, টেস্ট-ড্রাইভেন ডেভেলপমেন্ট এবং সিকিউর ডাটাবেজ আর্কিটেকচার বাস্তবায়ন।",
        },
        "role_stem_tutor": {
            "role_id": "role_stem_tutor",
            "title": "এসটিইএম গণিত ও বিজ্ঞান মেন্টর (STEM Math & Science Mentor)",
            "industry": "Education & Academic Mentorship",
            "required_skills": ["মাধ্যমিক গণিত", "পদার্থবিজ্ঞান", "সোক্র্যাটিক পেডাগজি", "পরীক্ষা কৌশল"],
            "bonus_skills": ["ডিজিটাল প্রেজেন্টেশন", "অভিভাবক যোগাযোগ", "ক্যাট ও ব্লুপ্রিন্ট জ্ঞান"],
            "min_match_threshold": 65.0,
            "description": "৮ম-১০ম শ্রেণির শিক্ষার্থীদের গণিত ও বিজ্ঞানের জটিল বিষয় সহজ ভাষায় বোঝানো এবং পরীক্ষাভীতি দূরীকরণ।",
        },
        "role_data_analyst": {
            "role_id": "role_data_analyst",
            "title": "এডটেক ডাটা ও সাইকোমেট্রিক্স অ্যানালিস্ট (EdTech & Assessment Analyst)",
            "industry": "Data Science & Psychometrics",
            "required_skills": ["Python", "পরিসংখ্যান", "SQL", "ডাটা ভিজ্যুয়ালাইজেশন"],
            "bonus_skills": ["IRT সাইকোমেট্রিক্স", "Pandas", "মেশিন লার্নিং", "এ/বি টেস্টিং"],
            "min_match_threshold": 60.0,
            "description": "শিক্ষার্থীদের লার্নিং প্যাটার্ন, আইআরটি অ্যাবিলিটি এস্টিমেশন এবং অ্যাডাপ্টিভ টেস্ট অ্যানালিটিক্স তৈরি।",
        },
    }

    def list_target_roles(self) -> List[Dict[str, Any]]:
        """Returns list of all available industry and teaching target roles."""
        return list(self.ROLES_CATALOG.values())

    def analyze_career_fit(
        self,
        candidate_id: str,
        role_id: str,
        candidate_skills: List[str],
        verified_badges_count: int = 0,
        quiz_mastery_pct: float = 75.0,
    ) -> Dict[str, Any]:
        """Calculates match score, skill gaps, and a structured remediation bridge roadmap."""
        safe_candidate_id = candidate_id.strip() if (candidate_id and str(candidate_id).strip()) else "candidate_anonymous"
        safe_role_id = role_id.strip() if (role_id and str(role_id).strip()) else "role_python_dev"

        role = self.ROLES_CATALOG.get(safe_role_id)
        if not role:
            return {
                "success": False,
                "message": f"অননুমোদিত বা অজানা রোল আইডি: '{safe_role_id}'। সমর্থিত রোলস: {', '.join(self.ROLES_CATALOG.keys())}।",
            }

        # Normalize skill strings for resilient matching
        normalized_cand_skills = {s.strip().lower() for s in (candidate_skills or []) if s.strip()}
        
        req_skills = role["required_skills"]
        bonus_skills = role["bonus_skills"]

        matched_req: List[str] = []
        missing_req: List[str] = []

        for req in req_skills:
            if any(cand_s in req.lower() or req.lower() in cand_s for cand_s in normalized_cand_skills):
                matched_req.append(req)
            else:
                missing_req.append(req)

        matched_bonus: List[str] = []
        for bon in bonus_skills:
            if any(cand_s in bon.lower() or bon.lower() in cand_s for cand_s in normalized_cand_skills):
                matched_bonus.append(bon)

        # 1. Base Required Skill Ratio (Weight: 60%)
        req_ratio = len(matched_req) / len(req_skills) if req_skills else 1.0
        req_score = req_ratio * 60.0

        # 2. Bonus Skills & Badges Boost (Weight: 20%)
        safe_badges = max(0, min(3, int(verified_badges_count)))
        bonus_ratio = max(0.0, min(1.0, (len(matched_bonus) * 0.4) + (safe_badges * 0.2)))
        bonus_score = bonus_ratio * 20.0

        # 3. Quiz Mastery & Academic Track Record (Weight: 20%)
        safe_mastery = max(0.0, min(100.0, float(quiz_mastery_pct)))
        academic_score = (safe_mastery / 100.0) * 20.0

        total_match_pct = round(req_score + bonus_score + academic_score, 1)

        # Readiness Tier Classification
        if total_match_pct >= 85.0:
            tier_code = "READY_TIER_A+"
            tier_label = "চাকরি বা টিউশনের জন্য প্রস্তুত (মার্কেট রেডি এ+)"
        elif total_match_pct >= 70.0:
            tier_code = "COMPETENT_TIER_A"
            tier_label = "সন্তোষজনক প্রস্তুতি (স্বল্পকালীন রিভিশন সহ)"
        elif total_match_pct >= 50.0:
            tier_code = "DEVELOPING_TIER_B"
            tier_label = "উন্নতিশীল (নির্দিষ্ট স্কিল গ্যাপ পূরণের সুযোগ রয়েছে)"
        else:
            tier_code = "FOUNDATIONAL_TIER_C"
            tier_label = "প্রাথমিক পর্যায় (রোডম্যাপ অনুযায়ী প্রশিক্ষণ কাম্য)"

        # Generate Actionable Gap Remediation Roadmap
        gap_roadmap = self._generate_gap_roadmap(missing_req, role["title"])

        return {
            "success": True,
            "candidate_id": safe_candidate_id,
            "role_id": role["role_id"],
            "role_title": role["title"],
            "industry": role["industry"],
            "match_percentage": total_match_pct,
            "readiness_tier": tier_code,
            "readiness_label": tier_label,
            "matched_skills": matched_req,
            "bonus_skills_matched": matched_bonus,
            "missing_skills": missing_req,
            "estimated_sprint_weeks": max(1, len(missing_req)),
            "gap_remediation_roadmap": gap_roadmap,
        }

    def _generate_gap_roadmap(self, missing_skills: List[str], role_title: str) -> List[Dict[str, Any]]:
        """Generates sequential weekly sprint milestones to close candidate skill gaps."""
        roadmap = []
        for idx, skill in enumerate(missing_skills, start=1):
            roadmap.append({
                "sprint_week": idx,
                "target_skill": skill,
                "action": f"অগ্রযাত্রা প্ল্যাটফর্মে '{skill}' বিষয়ক অনুশীলন মডিউল ও মডেল টেস্ট সম্পন্ন করুন।",
                "milestone": f"{skill} সম্পর্কিত অন্তত ৩টি প্রজেক্ট বা লাইভ চ্যালেঞ্জে ৮০%+ স্কোর অর্জন।",
                "estimated_hours": 8,
            })

        if not roadmap:
            roadmap.append({
                "sprint_week": 1,
                "target_skill": "মক ইন্টারভিউ ও পোর্টফোলিও ফাইনাল পলিশ",
                "action": f"{role_title} রোলের জন্য এআই মক ইন্টারভিউ কোচে অংশগ্রহণ করুন এবং সিভি স্ন্যাপশট রেডি করুন।",
                "milestone": "ইন্টারভিউ কোচে ৮৫%+ স্কোর নিশ্চিতকরণ।",
                "estimated_hours": 4,
            })

        return roadmap


# Global Singleton Service
career_matcher_service = CareerMatcherService()
