"""
Test Suite: Phase 67 Decentralized Micro-Edge CDN & WebTorrent Asset Swarm
Verifies media chunk slicing, binary Merkle tree root calculation,
poison chunk detection, WebRTC LAN transfer simulation, and rarest-first scheduling.
"""

import unittest
from backend.app.services.decentralized_cdn_swarm_service import (
    DecentralizedCdnSwarmService,
    decentralized_cdn_swarm_service,
)
from backend.app.schemas.decentralized_cdn_swarm_schema import (
    ManifestCreateRequest,
    PieceVerifyRequest,
    TransferSimulateRequest,
)

class TestPhase67DecentralizedCdnSwarm(unittest.TestCase):
    def setUp(self):
        self.service = DecentralizedCdnSwarmService()

    def test_01_manifest_creation_and_merkle_root(self):
        """Verify media is sliced into uniform chunks and produces valid Merkle root."""
        req = ManifestCreateRequest(
            content_id="PHYS-HSC-ROTATIONAL-3D",
            title="HSC Physics Rotational Dynamics 3D Lab Simulation",
            total_bytes=33554432,  # 32 MB
            piece_size_bytes=1048576,  # 1 MB
        )
        manifest = self.service.create_manifest(req)

        self.assertEqual(manifest.total_pieces, 32)
        self.assertEqual(len(manifest.pieces), 32)
        self.assertEqual(len(manifest.merkle_root), 64)

        # Check chunk offset continuity
        prev_offset = 0
        for p in manifest.pieces:
            self.assertEqual(p.byte_offset, prev_offset)
            self.assertEqual(p.byte_length, 1048576)
            self.assertEqual(len(p.sha256_hash), 64)
            prev_offset += p.byte_length

    def test_02_piece_verification_authentic(self):
        """Authentic piece hash must pass validation."""
        req = ManifestCreateRequest(
            content_id="CHEM-SOLVER-001",
            title="Organic Chemistry Molecular Solver",
            total_bytes=8388608,  # 8 MB = 8 pieces
            piece_size_bytes=1048576,
        )
        manifest = self.service.create_manifest(req)
        piece_0 = manifest.pieces[0]

        verify_req = PieceVerifyRequest(
            manifest_id=manifest.manifest_id,
            piece_index=0,
            candidate_hash=piece_0.sha256_hash,
        )
        res = self.service.verify_piece(verify_req)
        self.assertTrue(res.is_valid)
        self.assertIn("verified", res.message.lower())

    def test_03_piece_verification_poisoned(self):
        """Tampered piece hash must be rejected and flagged as poisoned chunk."""
        req = ManifestCreateRequest(
            content_id="BIO-CELL-3D",
            title="Cellular Biology 3D Organelle Atlas",
            total_bytes=4194304,
            piece_size_bytes=1048576,
        )
        manifest = self.service.create_manifest(req)

        fake_hash = "a" * 64
        verify_req = PieceVerifyRequest(
            manifest_id=manifest.manifest_id,
            piece_index=1,
            candidate_hash=fake_hash,
        )
        res = self.service.verify_piece(verify_req)
        self.assertFalse(res.is_valid)
        self.assertIn("poisoned", res.message.lower())

    def test_04_piece_verification_bounds_check(self):
        """Out of bounds piece index must return clean validation failure."""
        req = PieceVerifyRequest(
            manifest_id="MNFST-NCTB-MATH-3-64P",
            piece_index=999,
            candidate_hash="0" * 64,
        )
        res = self.service.verify_piece(req)
        self.assertFalse(res.is_valid)

    def test_05_swarm_status_and_bandwidth_savings(self):
        """Classroom swarm status must calculate bandwidth savings from P2P transfers."""
        status = self.service.get_swarm_status("default")
        self.assertIsNotNone(status)
        self.assertGreaterEqual(len(status.peers), 5)
        self.assertGreater(status.total_p2p_transferred_mb, 0.0)
        self.assertGreater(status.bandwidth_saved_percentage, 50.0)
        self.assertGreater(status.average_swarm_speed_mbps, 0.0)

    def test_06_simulate_p2p_transfer(self):
        """Simulating chunk transfer over WebRTC must update target peer and P2P metric."""
        status_before = self.service.get_swarm_status("default")
        manifest_id = status_before.manifest_id

        req = TransferSimulateRequest(
            manifest_id=manifest_id,
            source_peer_id="GW-DHAKA-CENTRAL",
            target_peer_id="PEER-FAHIM-MOB",
            piece_index=43,
        )
        res = self.service.simulate_p2p_transfer(req)
        self.assertTrue(res.success)
        self.assertGreater(res.transfer_rate_mbps, 20.0)
        self.assertGreater(res.transfer_duration_ms, 0.0)

        # Check target peer received the chunk
        status_after = self.service.get_swarm_status(manifest_id)
        fahim = next(p for p in status_after.peers if p.peer_id == "PEER-FAHIM-MOB")
        self.assertEqual(fahim.downloaded_pieces, 43)

    def test_07_rarest_first_scheduling(self):
        """Rarest-first schedule must return pieces with least availability."""
        schedule = self.service.get_rarest_first_schedule("default")
        self.assertTrue(len(schedule) > 0)
        # Verify sorted ascending by availability
        counts = [item["availability_count"] for item in schedule]
        self.assertEqual(counts, sorted(counts))

    def test_08_singleton_and_custom_manifest_caching(self):
        """Singleton service instance must persist custom manifests across calls."""
        req = ManifestCreateRequest(
            content_id="ROBOTICS-AVR-001",
            title="Embedded Robotics Microcontroller Lab",
            total_bytes=16777216,  # 16 MB
            piece_size_bytes=1048576,
        )
        created = decentralized_cdn_swarm_service.create_manifest(req)
        fetched = decentralized_cdn_swarm_service.get_manifest(created.manifest_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.manifest_id, created.manifest_id)
        self.assertEqual(fetched.total_pieces, 16)

if __name__ == "__main__":
    unittest.main()
