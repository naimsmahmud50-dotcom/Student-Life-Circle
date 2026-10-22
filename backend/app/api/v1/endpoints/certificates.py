# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 96 - Certificate & Social Proof Endpoints):
# Exposes public and authenticated REST API endpoints for Proof-of-Skill Certificate
# generation, public QR verification, dynamic OpenGraph card SVG delivery,
# and W3C Verifiable Credentials export.
#
# Endpoints:
# 1. POST /certificates/issue: Issues a new tamper-evident certificate.
# 2. GET  /certificates/verify/{cert_id}: Public verification endpoint against database ledger.
# 3. GET  /certificates/{cert_id}/og-card.svg: Dynamic 1200x630px vector SVG preview card.
# 4. GET  /certificates/{cert_id}/w3c: Exports W3C Verifiable Credential JSON-LD envelope.
# 5. GET  /certificates: Lists all issued certificates in the ledger.
#
# Standards: W3C Verifiable Credentials Data Model v1.1, OpenGraph, Strict Zero-Emoji.
# ==============================================================================

from typing import Dict, Any, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    Response,
    Query,
    status
)
from backend.app.services.certificate_service import (
    certificate_service,
    render_og_card_svg
)

router = APIRouter(prefix="/certificates", tags=["Proof-of-Skill Certificates & Verification"])


@router.post("/issue", status_code=status.HTTP_201_CREATED)
async def issue_certificate(payload: Dict[str, Any]):
    """
    Issues a new tamper-evident certificate with unique ID and SHA-256 digital signature.
    """
    student_id = payload.get("student_id")
    student_name = payload.get("student_name")
    course_title = payload.get("course_title")
    percentile_rank = payload.get("percentile_rank", 95.0)
    score = payload.get("score", 90.0)
    total_score = payload.get("total_score", 100.0)
    verified_skills = payload.get("verified_skills", [])
    institution = payload.get("institution", "National Curriculum & Admission Board")
    custom_cert_id = payload.get("custom_cert_id")

    if not student_id or not student_name or not course_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'student_id', 'student_name', and 'course_title' are mandatory."
        )

    record = certificate_service.issue_certificate(
        student_id=student_id,
        student_name=student_name,
        course_title=course_title,
        percentile_rank=float(percentile_rank),
        score=float(score),
        total_score=float(total_score),
        verified_skills=verified_skills,
        institution=institution,
        custom_cert_id=custom_cert_id
    )

    return {
        "status": "SUCCESS",
        "message": f"Certificate {record.cert_id} successfully issued and digitally signed.",
        "certificate": record.to_dict()
    }


@router.get("/verify/{cert_id}")
async def verify_certificate(cert_id: str):
    """
    Publicly accessible endpoint verifying certificate authenticity against the ledger.
    Returns student name, issuing date, verified skills, and cryptographic signature validity badge.
    """
    result = certificate_service.verify_certificate(cert_id)
    if not result.get("is_valid"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Certificate verification failed.")
        )
    return {
        "status": "SUCCESS",
        "verification": result
    }


@router.get("/{cert_id}/og-card.svg")
async def get_og_card_svg(cert_id: str):
    """
    Renders and streams dynamic 1200x630px vector SVG card for OpenGraph sharing previews.
    """
    record = certificate_service.get_certificate(cert_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificate {cert_id} not found."
        )

    svg_content = render_og_card_svg(record)
    return Response(
        content=svg_content,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=86400, s-maxage=86400",
            "Content-Disposition": f'inline; filename="{record.cert_id}_og_card.svg"'
        }
    )


@router.get("/{cert_id}/w3c")
async def get_w3c_verifiable_credential(cert_id: str):
    """
    Exports certificate conforming to W3C Verifiable Credentials Data Model v1.1.
    """
    record = certificate_service.get_certificate(cert_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificate {cert_id} not found."
        )

    return record.to_w3c_verifiable_credential()


@router.get("")
async def list_certificates():
    """
    Lists all issued certificates currently registered in the ledger.
    """
    certs = certificate_service.list_certificates()
    return {
        "status": "SUCCESS",
        "total_count": len(certs),
        "certificates": [c.to_dict() for c in certs]
    }
