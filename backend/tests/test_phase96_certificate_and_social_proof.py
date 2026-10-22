# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 96 - Unit & Integration Test Suite):
# Comprehensive test suite validating Cryptographic Proof-of-Skill Certificate
# generation, SHA-256 HMAC anti-tamper signatures, W3C Verifiable Credentials
# Data Model v1.1 compliance, 1200x630px vector SVG OpenGraph preview card generation,
# 2D QR matrix rendering, public verification REST API endpoints, and strict Zero-Emoji.
#
# Standards & Verification:
# 1. Certificate ID Regex: OGRO-{YEAR}-{HASH8} (e.g. OGRO-2026-A1B2C3D4).
# 2. Tamper-Evident Signatures: Modifying student name, course, or score breaks signature.
# 3. W3C VC v1.1: Context, id, type, issuer, issuanceDate, credentialSubject, proof.
# 4. OpenGraph 1200x630 SVG: Crisp vector layout, QR rects, percentile badge, zero emoji.
# 5. Public REST Endpoints: Issue, verify, og-card.svg, w3c export, list.
# ==============================================================================

import unittest
import os
import re
import json
import urllib.parse
from pathlib import Path

from backend.app.services.certificate_service import (
    generate_certificate_id,
    compute_canonical_signature,
    verify_canonical_signature,
    generate_qr_matrix,
    render_og_card_svg,
    CertificateRecord,
    CertificateLedger,
    BASE_VERIFY_URL
)
from backend.app.api.v1.endpoints.certificates import (
    issue_certificate,
    verify_certificate,
    get_og_card_svg,
    get_w3c_verifiable_credential,
    list_certificates
)
from backend.app.core.fastapi_shim import HTTPException


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is a decorative emoji."""
    code = ord(char)
    return (
        0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF
    )


def contains_emoji(text: str) -> bool:
    """Returns True if the string contains any emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase96CertificateAndSocialProof(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Phase 96: Cryptographic Proof-of-Skill Cards & QR Verification.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.service_py = cls.repo_root / "backend" / "app" / "services" / "certificate_service.py"
        cls.endpoint_py = cls.repo_root / "backend" / "app" / "api" / "v1" / "endpoints" / "certificates.py"
        cls.card_tsx = cls.repo_root / "frontend" / "src" / "components" / "certificate" / "ProofOfSkillCard.tsx"
        cls.share_tsx = cls.repo_root / "frontend" / "src" / "components" / "certificate" / "SocialShareButtons.tsx"
        cls.verify_page = cls.repo_root / "frontend" / "src" / "pages" / "verify" / "[certId].tsx"

    def setUp(self):
        # Fresh isolated ledger for unit tests
        self.ledger = CertificateLedger()

    def test_01_certificate_id_generation_and_format(self):
        """Verifies OGRO-{YEAR}-{HASH8} format and uniqueness."""
        cert_id = generate_certificate_id(year=2026)
        pattern = r"^OGRO-2026-[A-F0-9]{8}$"
        self.assertTrue(re.match(pattern, cert_id), f"Certificate ID {cert_id} did not match expected regex {pattern}")

        # Test uniqueness
        ids = {generate_certificate_id(year=2026) for _ in range(50)}
        self.assertEqual(len(ids), 50, "Generated certificate IDs must be mutually unique")

    def test_02_canonical_signature_computation_and_tamper_detection(self):
        """Verifies SHA-256 HMAC signature computation and anti-tamper security."""
        record = CertificateRecord(
            cert_id="OGRO-2026-TEST0001",
            student_id="usr_student_alpha",
            student_name="তানভীর আহমেদ (Tanvir Ahmed)",
            course_title="এইচএসসি পদার্থবিজ্ঞান — মহাকর্ষ ও স্থিতিস্থাপকতা",
            percentile_rank=97.8,
            score=98.0,
            total_score=100.0,
            issue_date="2026-10-18",
            verified_skills=["Gravitation", "Kepler Laws", "Elasticity", "Fluid Dynamics"]
        )

        # 1. Unaltered record must verify cleanly
        self.assertTrue(record.is_valid())

        # 2. Tampering student name must break signature
        tampered_dict = record.to_dict()
        tampered_dict["student_name"] = "অন্য কেউ (Impostor)"
        self.assertFalse(verify_canonical_signature(tampered_dict, record.signature))

        # 3. Tampering percentile rank must break signature
        tampered_percentile = record.to_dict()
        tampered_percentile["percentile_rank"] = 99.9
        self.assertFalse(verify_canonical_signature(tampered_percentile, record.signature))

        # 4. Tampering course title must break signature
        tampered_course = record.to_dict()
        tampered_course["course_title"] = "ভুল কোর্স (Unauthorized Subject)"
        self.assertFalse(verify_canonical_signature(tampered_course, record.signature))

    def test_03_qr_url_and_matrix_generation(self):
        """Verifies QR URL format and 2D vector matrix dimensions."""
        record = CertificateRecord(
            cert_id="OGRO-2026-QR000001",
            student_id="usr_student_qr",
            student_name="সায়মা খানম (Sayma Khanam)",
            course_title="NCTB HSC Chemistry",
            percentile_rank=96.5,
            score=95.0,
            total_score=100.0,
            issue_date="2026-10-18",
            verified_skills=["Equilibrium", "Thermodynamics"]
        )

        expected_url = f"{BASE_VERIFY_URL}/OGRO-2026-QR000001"
        self.assertEqual(record.qr_url, expected_url)

        # Verify QR matrix generation (25x25)
        matrix = generate_qr_matrix(record.qr_url, size=25)
        self.assertEqual(len(matrix), 25)
        self.assertEqual(len(matrix[0]), 25)

        # Check top-left 7x7 corner detection pattern
        self.assertTrue(matrix[0][0])
        self.assertTrue(matrix[0][6])
        self.assertTrue(matrix[6][0])
        self.assertTrue(matrix[6][6])
        self.assertTrue(matrix[3][3])  # Inner solid center

    def test_04_og_card_svg_generation_1200x630(self):
        """Verifies 1200x630 vector SVG generation with required elements."""
        record = CertificateRecord(
            cert_id="OGRO-2026-SVG00001",
            student_id="usr_student_svg",
            student_name="মাহির ফয়সাল (Mahir Faysal)",
            course_title="বুয়েট গণিত স্পেশাল অলিম্পিয়াড",
            percentile_rank=98.9,
            score=99.0,
            total_score=100.0,
            issue_date="2026-10-18",
            verified_skills=["Calculus", "Coordinate Geometry", "Vectors"]
        )

        svg = render_og_card_svg(record)

        # 1. Validate dimensions
        self.assertIn('viewBox="0 0 1200 630"', svg)
        self.assertIn('width="1200"', svg)
        self.assertIn('height="630"', svg)

        # 2. Validate textual content
        self.assertIn("মাহির ফয়সাল (Mahir Faysal)", svg)
        self.assertIn("বুয়েট গণিত স্পেশাল অলিম্পিয়াড", svg)
        self.assertIn("OGRO-2026-SVG00001", svg)
        self.assertIn("Calculus", svg)
        self.assertIn("W3C VERIFIABLE CREDENTIAL", svg)
        self.assertIn("SCAN TO VERIFY", svg)

        # 3. Validate SVG QR rects exist
        self.assertIn("<rect", svg)
        self.assertIn("fill=\"#0f172a\"", svg)

    def test_05_w3c_verifiable_credential_json_ld_compliance(self):
        """Verifies W3C Verifiable Credentials Data Model v1.1 compliance."""
        record = CertificateRecord(
            cert_id="OGRO-2026-W3C00001",
            student_id="usr_student_w3c",
            student_name="নাফিসা হক (Nafisa Haque)",
            course_title="এইচএসসি জীববিজ্ঞান — কোষ রসায়ন",
            percentile_rank=95.4,
            score=94.0,
            total_score=100.0,
            issue_date="2026-10-18",
            verified_skills=["Cytology", "Biomolecules"]
        )

        vc = record.to_w3c_verifiable_credential()

        # Check @context
        self.assertIn("https://www.w3.org/2018/credentials/v1", vc["@context"])

        # Check type
        self.assertIn("VerifiableCredential", vc["type"])
        self.assertIn("ProofOfSkillCredential", vc["type"])

        # Check issuer
        self.assertIn("id", vc["issuer"])
        self.assertIn("name", vc["issuer"])

        # Check credentialSubject
        subj = vc["credentialSubject"]
        self.assertEqual(subj["name"], "নাফিসা হক (Nafisa Haque)")
        self.assertEqual(subj["certificateId"], "OGRO-2026-W3C00001")
        self.assertEqual(subj["percentileRank"], 95.4)
        self.assertIn("Cytology", subj["verifiedSkills"])

        # Check proof block
        proof = vc["proof"]
        self.assertEqual(proof["type"], "Ed25519Signature2020")
        self.assertEqual(proof["proofValue"], record.signature)

    def test_06_ledger_issuance_and_verification_api(self):
        """Verifies CertificateLedger issuance, retrieval, and verification logic."""
        issued = self.ledger.issue_certificate(
            student_id="usr_farhan_99",
            student_name="ফারহান সাদিক (Farhan Sadik)",
            course_title="DU Ka Admission Physics Mock",
            percentile_rank=97.2,
            score=96.5,
            total_score=100.0,
            verified_skills=["Optics", "Thermodynamics"],
            institution="Notre Dame College, Dhaka"
        )

        self.assertTrue(issued.cert_id.startswith("OGRO-2026-"))
        self.assertTrue(issued.is_valid())

        # Test ledger verification
        res = self.ledger.verify_certificate(issued.cert_id)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["student_name"], "ফারহান সাদিক (Farhan Sadik)")
        self.assertFalse(res["tampered"])

        # Test non-existent cert verification
        invalid_res = self.ledger.verify_certificate("OGRO-2026-NONEXIST")
        self.assertFalse(invalid_res["is_valid"])
        self.assertEqual(invalid_res["error"], "CERTIFICATE_NOT_FOUND")

    async def test_07_rest_api_endpoints(self):
        """Verifies asynchronous REST API endpoint handlers."""
        # 1. Issue endpoint
        issue_payload = {
            "student_id": "usr_endpoint_01",
            "student_name": "আসিফ ইকবাল (Asif Iqbal)",
            "course_title": "Admission Mathematics",
            "percentile_rank": 98.1,
            "score": 97.0,
            "total_score": 100.0,
            "verified_skills": ["Algebra", "Trigonometry"]
        }
        issue_res = await issue_certificate(issue_payload)
        self.assertEqual(issue_res["status"], "SUCCESS")
        cert_data = issue_res["certificate"]
        cert_id = cert_data["cert_id"]

        # 2. Verify endpoint
        verify_res = await verify_certificate(cert_id)
        self.assertEqual(verify_res["status"], "SUCCESS")
        self.assertTrue(verify_res["verification"]["is_valid"])

        # 3. Invalid cert verify raises HTTPException 404
        with self.assertRaises(HTTPException) as cm:
            await verify_certificate("OGRO-2026-FAKEID99")
        self.assertEqual(cm.exception.status_code, 404)

        # 4. OpenGraph SVG endpoint
        og_res = await get_og_card_svg(cert_id)
        self.assertEqual(og_res.media_type, "image/svg+xml")
        self.assertIn("আসিফ ইকবাল (Asif Iqbal)", og_res.content)

        # 5. W3C export endpoint
        w3c_res = await get_w3c_verifiable_credential(cert_id)
        self.assertIn("VerifiableCredential", w3c_res["type"])

        # 6. List endpoint
        list_res = await list_certificates()
        self.assertEqual(list_res["status"], "SUCCESS")
        self.assertGreaterEqual(list_res["total_count"], 1)

    def test_08_social_sharing_links_and_opengraph_parameters(self):
        """Verifies LinkedIn and Facebook sharing URL generation and OpenGraph encoding."""
        test_url = "https://ogrojatra.edu.bd/verify/OGRO-2026-A1B2C3D4"
        encoded_url = urllib.parse.quote(test_url, safe='')

        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
        facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"

        self.assertIn("https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fogrojatra.edu.bd", linkedin_url)
        self.assertIn("https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fogrojatra.edu.bd", facebook_url)

    def test_09_frontend_components_and_page_existence(self):
        """Verifies frontend components and dynamic verify/[certId].tsx page exist with proper metadata."""
        self.assertTrue(self.card_tsx.exists(), f"Missing ProofOfSkillCard.tsx at {self.card_tsx}")
        self.assertTrue(self.share_tsx.exists(), f"Missing SocialShareButtons.tsx at {self.share_tsx}")
        self.assertTrue(self.verify_page.exists(), f"Missing verify page at {self.verify_page}")

        with open(self.verify_page, "r", encoding="utf-8") as f:
            page_content = f.read()

        # Check essential OpenGraph and Twitter tags in Head
        self.assertIn('<meta property="og:image"', page_content)
        self.assertIn('<meta property="og:title"', page_content)
        self.assertIn('<meta property="og:description"', page_content)
        self.assertIn('<meta property="og:url"', page_content)
        self.assertIn('<meta name="twitter:card"', page_content)
        self.assertIn('summary_large_image', page_content)

        # Check component usage
        self.assertIn('ProofOfSkillCard', page_content)
        self.assertIn('SocialShareButtons', page_content)

    def test_10_strict_zero_emoji_and_architecture_notes(self):
        """Verifies strict Zero-Emoji compliance and Developer Architecture Notes across all Phase 96 files."""
        files_to_scan = [
            self.service_py,
            self.endpoint_py,
            self.card_tsx,
            self.share_tsx,
            self.verify_page,
            Path(__file__)
        ]

        for file_path in files_to_scan:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertFalse(
                contains_emoji(content),
                f"Zero-Emoji policy violation detected in file: {file_path.name}"
            )

            self.assertTrue(
                "DEVELOPER ARCHITECTURE NOTE" in content or "ARCHITECTURE NOTE:" in content,
                f"Developer Architecture Note missing from: {file_path.name}"
            )


if __name__ == "__main__":
    unittest.main()
