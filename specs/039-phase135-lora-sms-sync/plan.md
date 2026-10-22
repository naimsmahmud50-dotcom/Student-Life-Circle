# PLAN: Phase 135 — Offline LoRa & SMS-Bridge Rural Exam Synchronizer for Grid Outages

## 1. Architectural Strategy
The rural exam synchronizer acts as an offline-first telemetry and disaster recovery bridge. In remote areas without cellular data or grid power, tablets and client nodes encode exam submissions into compact binary datagrams for radio or SMS broadcast.

```mermaid
flowchart TD
    ExamTablet[Offline Exam Tablet / Client Device] --> MCQAnswers[100 MCQ Answer Sheet]
    MCQAnswers --> BitPacker[Dense Bit-Packer: 300 bits / 38 bytes]
    BitPacker --> OfflineSigner[Offline Device Cryptographic Signer]
    OfflineSigner --> PacketEnvelope["140-Byte Datagram: [Header | Bitstream | Signature | CRC16]"]
    PacketEnvelope --> Selector{Channel Available?}
    Selector -->|LoRa Mesh (868/915 MHz)| LoRaNode[LoRa Relay Node]
    Selector -->|Cellular 2G SMS| GSMBridge[GSM Modem SMS PDU]
    LoRaNode --> GatewayReceiver[Rural Gateway Station]
    GSMBridge --> GatewayReceiver
    GatewayReceiver --> Deduplicator[Packet Deduplication & CRC16 Check]
    Deduplicator --> Reconciler[Signature Verification & Auto-Grading Engine]
    Reconciler --> Supabase[(Supabase Database with 100% RLS)]
```

## 2. Implementation Steps
1. **Backend Package & Binary Synchronizer**:
   - Write `backend/rural/__init__.py`.
   - Write `backend/rural/lora_sms_synchronizer.py` with `BinaryAnswerPacket`, `MCQOption`, `TransmissionChannel`, `LoRaSMSSynchronizerService`.
2. **Database Migration with 100% RLS**:
   - Write `backend/migrations/013_offline_lora_mesh_rls.sql` with tables `rural_exam_packets`, `lora_gateway_nodes`, `offline_signed_answer_sheets`, `reconciliation_audit_logs`.
3. **Frontend Telecom Console UI**:
   - Write `frontend/src/pages/rural/synchronizer.tsx` with hex binary inspector, telemetry gauges (SNR, channel frequency, MTU progress), 100-question answer sheet simulator, 3D tactile buttons, and pure Lucide vector icons.
4. **Automated Test Suite**:
   - Write `backend/tests/test_phase135_lora_sms_synchronizer.py` verifying headers, zero-emoji, 100 MCQ compression $\le 140$ bytes, exact bitwise roundtrip accuracy, signature tamper checks, and migration 013 RLS integrity.
5. **Execution & Regression Verification**:
   - Run zero-emoji sweep.
   - Run Phase 135 test suite.
   - Run full backend discovery (all 1,503+ tests).
   - Compile Next.js production bundle (`npm run build`).
   - Start daemon and verify HTTP 200 on `/rural/synchronizer`.
