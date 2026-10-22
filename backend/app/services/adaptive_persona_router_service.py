"""
Phase 60: Adaptive Persona Router Service.
Synthesizes role-tailored dashboards, navigation priorities, and accessibility profiles
for Students, Educators, Guardians, Institutional Admins, and Corporate Recruiters.
"""

from typing import Dict, Any, List, Optional


class AdaptivePersonaRouterService:
    """
    Persona configuration authority dynamically shaping workspace UI,
    priority navigation tabs, and operational shortcuts.
    """

    PERSONA_PROFILES: Dict[str, Dict[str, Any]] = {
        "student": {
            "role_display_title": "Academic Scholar & Career Explorer",
            "primary_navigation_tabs": [
                "practice",
                "interactive-preview",
                "molecular-geometry",
                "tuition-matching",
                "verifiable-credentials-zkp",
                "edge-video-streamer"
            ],
            "dashboard_kpis": [
                {"label": "Daily Study Streak", "value": "18 Days", "status": "positive"},
                {"label": "Practice Accuracy", "value": "89.4%", "status": "positive"},
                {"label": "ZKP Credentials", "value": "2 Active", "status": "neutral"},
                {"label": "Tuition Match Rate", "value": "94.0%", "status": "positive"}
            ],
            "quick_action_shortcuts": [
                {"action_id": "start_practice", "title": "Launch Rapid MCQ Practice", "target_tab": "practice"},
                {"action_id": "view_lecture", "title": "Watch 144p Micro-Lecture", "target_tab": "edge-video-streamer"},
                {"action_id": "share_zkp", "title": "Share ZKP Grade to Bdjobs", "target_tab": "verifiable-credentials-zkp"}
            ]
        },
        "educator": {
            "role_display_title": "Certified Master Educator & Examiner",
            "primary_navigation_tabs": [
                "practice",
                "coaching-batch-pool",
                "voice-viva-simulator",
                "syllabus-atlas",
                "multi-llm-injection-shield"
            ],
            "dashboard_kpis": [
                {"label": "Active Batches", "value": "4 Batches", "status": "positive"},
                {"label": "Submissions Graded", "value": "342 Quizzes", "status": "positive"},
                {"label": "Question Bank", "value": "128 Items", "status": "positive"},
                {"label": "Student Retention", "value": "96.5%", "status": "positive"}
            ],
            "quick_action_shortcuts": [
                {"action_id": "author_quiz", "title": "Publish New Chapter Quiz", "target_tab": "practice"},
                {"action_id": "conduct_viva", "title": "Conductor Live Voice Viva", "target_tab": "voice-viva-simulator"},
                {"action_id": "check_llm", "title": "Grade Essays with Claude", "target_tab": "multi-llm-injection-shield"}
            ]
        },
        "guardian": {
            "role_display_title": "Student Guardian & Academic Sponsor",
            "primary_navigation_tabs": [
                "tuition-matching",
                "coaching-batch-pool",
                "interactive-preview"
            ],
            "dashboard_kpis": [
                {"label": "Attendance Rate", "value": "98.2%", "status": "positive"},
                {"label": "Verified Tuition", "value": "24 Hours", "status": "positive"},
                {"label": "Escrow Wallet BDT", "value": "4,500 BDT", "status": "neutral"},
                {"label": "Monthly Improvement", "value": "+14.5%", "status": "positive"}
            ],
            "quick_action_shortcuts": [
                {"action_id": "pay_escrow", "title": "Release Tutor Payment (bKash)", "target_tab": "tuition-matching"},
                {"action_id": "view_report", "title": "View Weekly Report Card", "target_tab": "interactive-preview"},
                {"action_id": "message_mentor", "title": "Contact Head Mentor", "target_tab": "coaching-batch-pool"}
            ]
        },
        "institutional_admin": {
            "role_display_title": "University Registrar & Security Officer",
            "primary_navigation_tabs": [
                "migration-drift-index",
                "verifiable-credentials-zkp",
                "multi-llm-injection-shield",
                "tenant-merkle-cdc",
                "presence-rls-privacy"
            ],
            "dashboard_kpis": [
                {"label": "Database Lock Time", "value": "0.00s", "status": "positive"},
                {"label": "W3C Credentials", "value": "1,420 Issued", "status": "positive"},
                {"label": "RLS Policy Coverage", "value": "100.0%", "status": "positive"},
                {"label": "Zero-Trust Breaches", "value": "0 Intercepted", "status": "positive"}
            ],
            "quick_action_shortcuts": [
                {"action_id": "verify_drift", "title": "Verify Schema Drift Parity", "target_tab": "migration-drift-index"},
                {"action_id": "issue_degree", "title": "Issue W3C VC Certificate", "target_tab": "verifiable-credentials-zkp"},
                {"action_id": "audit_llm", "title": "Inspect Canary Trap Logs", "target_tab": "multi-llm-injection-shield"}
            ]
        },
        "corporate_recruiter": {
            "role_display_title": "Talent Acquisition & Technical Recruiter",
            "primary_navigation_tabs": [
                "verifiable-credentials-zkp",
                "industry-capstone",
                "tuition-matching"
            ],
            "dashboard_kpis": [
                {"label": "Verified Engineers", "value": "64 Profiles", "status": "positive"},
                {"label": "ZKP Proofs Verified", "value": "100%", "status": "positive"},
                {"label": "Average Screening Time", "value": "1.2 Days", "status": "positive"},
                {"label": "Shortlisted Hires", "value": "12 Candidates", "status": "positive"}
            ],
            "quick_action_shortcuts": [
                {"action_id": "filter_zkp", "title": "Filter Candidates (CGPA >= 3.50)", "target_tab": "verifiable-credentials-zkp"},
                {"action_id": "verify_sig", "title": "Audit Ed25519 Signatures", "target_tab": "verifiable-credentials-zkp"},
                {"action_id": "view_capstones", "title": "Inspect Industry Capstones", "target_tab": "industry-capstone"}
            ]
        }
    }

    def route_persona(
        self,
        user_role: str,
        device_tier: str = "desktop",
        preferred_theme: str = "auto"
    ) -> Dict[str, Any]:
        """
        Synthesizes personalized UI parameters, prioritized tabs, and shortcuts.
        """
        role_key = user_role.lower().strip()
        profile = self.PERSONA_PROFILES.get(role_key, self.PERSONA_PROFILES["student"])

        is_low_bandwidth = device_tier == "mobile_low_bandwidth"

        accessibility = {
            "high_contrast_mode": False,
            "font_scaling_factor": 1.0,
            "low_bandwidth_optimized": is_low_bandwidth,
            "brotli_compression_level": 11 if is_low_bandwidth else 6,
            "reduced_motion": is_low_bandwidth,
            "touch_target_min_px": 44
        }

        return {
            "user_role": role_key,
            "role_display_title": profile["role_display_title"],
            "primary_navigation_tabs": profile["primary_navigation_tabs"],
            "dashboard_kpis": profile["dashboard_kpis"],
            "quick_action_shortcuts": profile["quick_action_shortcuts"],
            "accessibility_parameters": accessibility
        }
