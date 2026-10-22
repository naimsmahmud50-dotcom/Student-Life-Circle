# SPEC: Phase 135 — Offline LoRa & SMS-Bridge Rural Exam Synchronizer for Grid Outages

## 1. Overview
Phase 135 establishes the **Offline LoRa & SMS-Bridge Rural Exam Synchronizer**, a resilient disaster-recovery telecommunications bridge designed for national exam centers, char areas, and remote islands during electrical grid outages and complete internet blackout. The system compresses full 100-question MCQ answer sheets into an ultra-dense binary payload of strictly $\le 140$ bytes (fitting within a single GSM 8-bit SMS PDU or LoRaWAN maximum transmission unit). Answer sheets are cryptographically signed on-device while offline and batch-reconciled when LoRa mesh gateways or cellular base stations restore intermittent connectivity.

## 2. Architectural Pillars
1. **Developer Architecture Note Standard**: Mandatory block comment on every created/modified file.
2. **Ultra-Compressed Binary Payload Protocol (BAP-140)**:
   - 100 MCQ questions packed into dense bitstreams (3 bits per question: 0=Unanswered, 1=A, 2=B, 3=C, 4=D) = 300 bits = 37.5 bytes.
   - Header (Student Roll Hash, Exam ID, Timestamp, CRC-16 Checksum, Cryptographic signature tag) totaling $\approx 78$ bytes.
   - Strict constraint: Total packet size $\le 140$ bytes.
   - Bitwise roundtrip fidelity: 100% loss-free serialization and deserialization.
3. **Offline Cryptographic Signature & Anti-Tamper Sealing**:
   - Device signs the answer sheet with its local keypair before packetization.
   - Server validates signature and checks timestamp window against exam submission curfew.
4. **LoRaWAN / GSM SMS Multi-Channel Gateway Router**:
   - Supports 868/915 MHz LoRa mesh packet routing with fallback to GSM SMS PDU clearinghouse.
   - Idempotent deduplication engine preventing replay when multiple gateways pick up the same broadcast.
5. **Supabase Migration 013 with 100% RLS**:
   - Tables: `rural_exam_packets`, `lora_gateway_nodes`, `offline_signed_answer_sheets`, `reconciliation_audit_logs`.
   - Complete multi-tenant tenancy isolation.
6. **Telecom Terminal Console Aesthetic**:
   - Oxford Academic Navy (`#0A2540`), Telecom Amber (`#B45309`), Signal Emerald (`#065F46`), Paper Ivory (`#FAFAF8`).
   - Hex / Binary PDU visualizer, 3D physical tactile push buttons, and pure Lucide vector icons with 0% emojis.

## 3. File Inventory
- `backend/rural/__init__.py`: Package exports for rural synchronizer and binary protocol.
- `backend/rural/lora_sms_synchronizer.py`: Core logic for bit-packing 100 MCQs, CRC16 verification, offline signing, and gateway deduplication.
- `backend/migrations/013_offline_lora_mesh_rls.sql`: Database schema with gateway tracking, packets, and RLS.
- `frontend/src/pages/rural/synchronizer.tsx`: Disaster recovery telecom console with binary PDU inspector, LoRa/SMS channel switch, and batch reconciler.
- `backend/tests/test_phase135_lora_sms_synchronizer.py`: Automated test suite.
