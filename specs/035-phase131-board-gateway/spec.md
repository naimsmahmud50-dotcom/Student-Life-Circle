# SPECIFICATION: Phase 131 — Ministry of Education & National Curriculum Accreditation API Gateway

## 1. Executive Summary & Objective
Phase 131 establishes the official API Gateway and Webhook Clearinghouse interconnecting the Ogrojatra Student Platform with the Ministry of Education, the National Curriculum and Textbook Board (NCTB), and the 9 General, Madrasah, and Technical Education Boards of Bangladesh. The gateway enforces cryptographic non-repudiation using Ed25519 digital signatures, synchronizes W3C Verifiable Credentials (VC) for curriculum accreditation and student certificates, and defends against untrusted traffic via IP whitelisting and sliding-window rate limiting.

## 2. Mandatory Architectural Standards
- **Developer Architecture Note Header**: Every created or modified file MUST feature the standardized block header documenting Phase 131, ASVS L2, Ed25519 Cryptographic Signatures, and Rate Limiting standards.
- **Pure Academic & Governmental Clearinghouse Visual Philosophy (Zero AI Vibe)**:
  * Official ministry and regulatory audit interface (Ministry of Education / Board Clearinghouse style).
  * High-contrast Paper Ivory (`#FAFAF8`) background, Paper White (`#FFFFFF`) card dockets, Oxford Academic Navy (`#0A2540`), and Government Emerald (`#065F46`).
  * 3D tactile push buttons with physical depth: `bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg`.
  * Strict Zero-Emoji Rule: 100% pure Lucide-React SVG vector icons only.

## 3. Technical Requirements

### A. Education Board Gateway Engine (`backend/integrations/education_board_gateway.py`)
1. **Registered Board Nodes**:
   - `NCTB`: National Curriculum and Textbook Board (Curriculum accreditation & syllabus revisions).
   - `DHAKA_BOARD`: Board of Intermediate and Secondary Education, Dhaka.
   - `CHITTAGONG_BOARD`: Board of Intermediate and Secondary Education, Chattogram.
   - `RAJSHAHI_BOARD`: Board of Intermediate and Secondary Education, Rajshahi.
   - `COMILLA_BOARD`: Board of Intermediate and Secondary Education, Cumilla.
   - `JESSORE_BOARD`: Board of Intermediate and Secondary Education, Jashore.
   - `BARISAL_BOARD`: Board of Intermediate and Secondary Education, Barishal.
   - `SYLHET_BOARD`: Board of Intermediate and Secondary Education, Sylhet.
   - `DINAJPUR_BOARD`: Board of Intermediate and Secondary Education, Dinajpur.
   - `MYMENSINGH_BOARD`: Board of Intermediate and Secondary Education, Mymensingh.
   - `MADRASAH_BOARD`: Bangladesh Madrasah Education Board.
   - `TECHNICAL_BOARD`: Bangladesh Technical Education Board (BTEB).
2. **Ed25519 Cryptographic Signatures**:
   - Every outgoing and incoming webhook payload must be signed using Ed25519 (`cryptography.hazmat.primitives.asymmetric.ed25519`).
   - Webhook headers: `X-Board-Signature: <hex_encoded_signature>`, `X-Board-Key-Id: <node_key_id>`, `X-Timestamp: <epoch_seconds>`.
   - Replay protection: Rejects requests with timestamps older than 300 seconds ($\Delta t > 5\text{ mins}$).
3. **W3C Verifiable Credentials (VC) Batch Sync**:
   - Ingests and serializes compliant W3C Verifiable Credentials:
     * `@context`: `["https://www.w3.org/2018/credentials/v1", "https://ogrojatra.edu.bd/credentials/v1"]`
     * `type`: `["VerifiableCredential", "NCTBCurriculumAccreditationCredential"]`
     * `credentialSubject`: Subject syllabus version, approved competencies, hash, and issuing authority.
     * `proof`: `type: "Ed25519Signature2020"`, `jws` signature, and verification method.
4. **Security & Rate Limiting (ASVS L2)**:
   - IP Whitelisting: Rejects requests originating from unauthorized network addresses with `IPNotWhitelistedException`.
   - Token Bucket / Sliding Window Rate Limiting: Enforces 60 requests/minute per board node, throttling excesses with `RateLimitExceededException`.

### B. Supabase Security & RLS (`backend/migrations/009_education_board_gateway_rls.sql`)
1. **Tables**:
   - `board_accreditation_nodes`: Node registry, public keys, whitelisted CIDRs, and sync health.
   - `webhook_events`: Ingested and dispatched webhook events with Ed25519 signatures and audit status.
   - `verifiable_credentials_batch`: W3C credential batches synchronized from boards.
   - `gateway_audit_logs`: Immutable security audit logs for clearinghouse telemetry.
2. **Row Level Security (RLS)**:
   - Enabled and forced on all tables.
   - Access restricted to `service_role` and verified ministry gateway administrators.

### C. Frontend Governance Clearinghouse Portal (`frontend/src/pages/governance/board-gateway.tsx`)
1. **National Clearinghouse Monitor**:
   - Active status grid of all 12 Education Boards and NCTB with uptime and public key fingerprints.
   - Live Ed25519 signature generator and signature verification validator.
   - W3C Verifiable Credential payload inspector with JSON syntax highlighting.
   - Real-time webhook traffic audit stream (200 OK, Ed25519 Verified).
   - 3D tactile buttons and pure Lucide SVG vector icons.

### D. Automated Test Suite (`backend/tests/test_phase131_board_gateway.py`)
- Full test coverage of Ed25519 keypair generation, signing, verification, and forgery detection.
- IP whitelisting and rate limiting tests.
- W3C Verifiable Credential serialization and batch validation.
- Supabase migration 009 RLS integrity.
- Zero-Emoji and Developer Architecture Note compliance.
