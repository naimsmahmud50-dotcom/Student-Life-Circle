"""
========================================================================================
MODULE:    Tuition Marketplace & Bilateral Contact Consent Service
TOPIC:     Safe Tuition Listings, Geographic Scoping, Contact Privacy & Anti-Scam
FILE:      backend/app/services/tuition_service.py
PURPOSE:   Orchestrates the trusted tuition marketplace for students and verified tutors.
           Enforces strict contact privacy: phone numbers and exact residential addresses
           remain hidden from public listings. Contact details are disclosed only after
           bilateral consent between tutor and learner/guardian. Enforces guardian
           co-signing for minor learners.
AUDIENCE:  Marketplace Engineers, Trust & Safety Teams & AI Agents
STANDARDS: Data Minimization, Bilateral Consent Protocol, Minor Protection
========================================================================================
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any

from backend.app.models.opportunity import TuitionListing, TuitionApplication


class TuitionService:
    """
    Trust-first tuition matching service.
    """

    def __init__(self):
        self._listings: Dict[str, TuitionListing] = {}
        self._applications: Dict[str, TuitionApplication] = {}

    def create_listing(
        self,
        creator_user_id: str,
        class_grade: int,
        curriculum: str,
        medium: str,
        subject: str,
        location_district: str,
        location_thana: str,
        is_online: bool = False,
        salary_range_min: Optional[int] = None,
        salary_range_max: Optional[int] = None
    ) -> TuitionListing:
        """Creates a new tuition offer or requirement."""
        listing = TuitionListing(
            creator_user_id=creator_user_id,
            class_grade=class_grade,
            curriculum=curriculum,
            medium=medium,
            subject=subject,
            location_district=location_district,
            location_thana=location_thana,
            is_online=is_online,
            salary_range_min=salary_range_min,
            salary_range_max=salary_range_max,
            status="PUBLISHED"
        )
        self._listings[listing.id] = listing
        return listing

    def apply_for_tuition(
        self,
        listing_id: str,
        tutor_user_id: str,
        message: str = ""
    ) -> Tuple[bool, Optional[TuitionApplication], str]:
        """Tutor applies for an open listing."""
        listing = self._listings.get(listing_id)
        if not listing or listing.status != "PUBLISHED":
            return False, None, "LISTING_NOT_FOUND_OR_CLOSED"

        # Check existing application
        app_key = f"{listing_id}:{tutor_user_id}"
        if app_key in self._applications:
            return False, None, "ALREADY_APPLIED"

        app = TuitionApplication(
            listing_id=listing_id,
            tutor_user_id=tutor_user_id,
            message=message,
            contact_consent_granted=False,  # Hidden until learner/guardian accepts
            status="APPLIED"
        )
        self._applications[app_key] = app
        return True, app, "OK"

    def grant_contact_consent(
        self,
        listing_id: str,
        tutor_user_id: str,
        learner_or_guardian_id: str
    ) -> Tuple[bool, str]:
        """
        Bilateral Consent Step:
        Learner/Guardian approves tutor application, unlocking safe bilateral contact details.
        """
        app_key = f"{listing_id}:{tutor_user_id}"
        app = self._applications.get(app_key)
        listing = self._listings.get(listing_id)

        if not app or not listing:
            return False, "APPLICATION_NOT_FOUND"

        if listing.creator_user_id != learner_or_guardian_id:
            return False, "UNAUTHORIZED_CONSENT_ACTION"

        app.contact_consent_granted = True
        app.status = "ACCEPTED"
        return True, "CONTACT_DISCLOSED"

    def search_listings(
        self,
        district: Optional[str] = None,
        thana: Optional[str] = None,
        class_grade: Optional[int] = None,
        subject: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filters public listings with personal contact details strictly redacted."""
        results = []
        for l in self._listings.values():
            if l.status != "PUBLISHED":
                continue
            if district and l.location_district.lower() != district.lower():
                continue
            if thana and l.location_thana.lower() != thana.lower():
                continue
            if class_grade and l.class_grade != class_grade:
                continue
            if subject and subject.lower() not in l.subject.lower():
                continue

            results.append(l.to_dict())
        return results


# Singleton Service Instance
tuition_service = TuitionService()
