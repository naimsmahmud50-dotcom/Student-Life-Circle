"""
Service: Decentralized Micro-Edge CDN & WebTorrent Asset Swarm (Phase 67)
Manages cryptographic media chunk slicing, SHA-256 Merkle piece validation,
classroom WebRTC peer bitfield tracking, tit-for-tat rarest-first chunk scheduling,
and rural ISP bandwidth savings aggregation.
"""

import math
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from backend.app.schemas.decentralized_cdn_swarm_schema import (
    ChunkPieceDTO,
    MediaManifestDTO,
    ManifestCreateRequest,
    PeerSwarmNodeDTO,
    SwarmStatusResponse,
    PieceVerifyRequest,
    PieceVerifyResponse,
    TransferSimulateRequest,
    TransferSimulateResponse,
)

class DecentralizedCdnSwarmService:
    def __init__(self):
        self._manifests: Dict[str, MediaManifestDTO] = {}
        self._peers: Dict[str, List[PeerSwarmNodeDTO]] = {}
        self._p2p_transferred_mb: Dict[str, float] = {}
        self._isp_gateway_mb: Dict[str, float] = {}

        # Preload canonical NCTB Class 10 Higher Math 3D Lecture Manifest
        self._init_default_manifest()

    def _init_default_manifest(self):
        default_manifest = self.create_manifest(
            ManifestCreateRequest(
                content_id="NCTB-MATH-3D-SIM-001",
                title="Class 10 Higher Mathematics 3D Vector Geometry & Kinematics Lab",
                total_bytes=67108864,  # 64 MB
                piece_size_bytes=1048576,  # 1 MB = 64 pieces
            )
        )
        manifest_id = default_manifest.manifest_id

        # Setup standard classroom swarm
        self._peers[manifest_id] = [
            PeerSwarmNodeDTO(
                peer_id="GW-DHAKA-CENTRAL",
                peer_name="Classroom Gateway Server",
                device_type="Gateway Tower",
                role="gateway",
                downloaded_pieces=64,
                total_pieces=64,
                upload_rate_kbps=48200.0,
                download_rate_kbps=0.0,
                choked=False,
                bitfield_hex="F" * 16,  # 64 bits all 1s
                is_gateway=True,
            ),
            PeerSwarmNodeDTO(
                peer_id="PEER-SAKIB-TAB",
                peer_name="Sakib Tablet (Squad Seeder)",
                device_type="Tablet",
                role="seeder",
                downloaded_pieces=64,
                total_pieces=64,
                upload_rate_kbps=28400.0,
                download_rate_kbps=0.0,
                choked=False,
                bitfield_hex="F" * 16,
                is_gateway=False,
            ),
            PeerSwarmNodeDTO(
                peer_id="PEER-FAHIM-MOB",
                peer_name="Fahim Mobile (Leecher)",
                device_type="Mobile",
                role="leecher",
                downloaded_pieces=42,
                total_pieces=64,
                upload_rate_kbps=8500.0,
                download_rate_kbps=24300.0,
                choked=False,
                bitfield_hex="FFFFFFFFFFFF0000",
                is_gateway=False,
            ),
            PeerSwarmNodeDTO(
                peer_id="PEER-NADIA-LAP",
                peer_name="Nadia Laptop (Relay Seeder)",
                device_type="Laptop",
                role="seeder",
                downloaded_pieces=60,
                total_pieces=64,
                upload_rate_kbps=34100.0,
                download_rate_kbps=12400.0,
                choked=False,
                bitfield_hex="FFFFFFFFFFFFFF00",
                is_gateway=False,
            ),
            PeerSwarmNodeDTO(
                peer_id="PEER-TANVIR-MOB",
                peer_name="Tanvir Mobile (Edge Leecher)",
                device_type="Mobile",
                role="leecher",
                downloaded_pieces=26,
                total_pieces=64,
                upload_rate_kbps=3200.0,
                download_rate_kbps=29800.0,
                choked=False,
                bitfield_hex="FFFFFFFFFF000000",
                is_gateway=False,
            ),
        ]

        self._isp_gateway_mb[manifest_id] = 64.0  # Downloaded once from internet
        self._p2p_transferred_mb[manifest_id] = 192.0  # 3 peers downloaded from P2P

    @staticmethod
    def _compute_merkle_root(leaf_hashes: List[str]) -> str:
        """Compute the binary Merkle root hash for an array of SHA-256 leaves."""
        if not leaf_hashes:
            return hashlib.sha256(b"empty_merkle_tree").hexdigest()

        current_level = leaf_hashes[:]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = left + right
                parent = hashlib.sha256(combined.encode("utf-8")).hexdigest()
                next_level.append(parent)
            current_level = next_level

        return current_level[0]

    def create_manifest(self, req: ManifestCreateRequest) -> MediaManifestDTO:
        """Slices a media asset into uniform chunk pieces and generates Merkle root."""
        total_pieces = math.ceil(req.total_bytes / req.piece_size_bytes)
        manifest_id = f"MNFST-{req.content_id[:12]}-{total_pieces}P"

        pieces: List[ChunkPieceDTO] = []
        leaf_hashes: List[str] = []

        for idx in range(total_pieces):
            byte_offset = idx * req.piece_size_bytes
            remaining_bytes = req.total_bytes - byte_offset
            length = min(req.piece_size_bytes, remaining_bytes)

            # Deterministic piece hash synthesis based on asset id, index, and byte bounds
            piece_seed = f"ASSET:{req.content_id}:PIECE:{idx}:OFFSET:{byte_offset}:LEN:{length}"
            piece_sha256 = hashlib.sha256(piece_seed.encode("utf-8")).hexdigest()

            piece_dto = ChunkPieceDTO(
                piece_index=idx,
                byte_offset=byte_offset,
                byte_length=length,
                sha256_hash=piece_sha256,
                verified=True,
            )
            pieces.append(piece_dto)
            leaf_hashes.append(piece_sha256)

        merkle_root = self._compute_merkle_root(leaf_hashes)
        now_iso = datetime.now(timezone.utc).isoformat()

        manifest = MediaManifestDTO(
            manifest_id=manifest_id,
            content_id=req.content_id,
            title=req.title,
            total_bytes=req.total_bytes,
            piece_size_bytes=req.piece_size_bytes,
            total_pieces=total_pieces,
            merkle_root=merkle_root,
            created_at=now_iso,
            pieces=pieces,
        )

        self._manifests[manifest_id] = manifest
        if manifest_id not in self._peers:
            self._peers[manifest_id] = []
            self._p2p_transferred_mb[manifest_id] = 0.0
            self._isp_gateway_mb[manifest_id] = round(req.total_bytes / (1024 * 1024), 2)

        return manifest

    def get_manifest(self, manifest_id: str) -> Optional[MediaManifestDTO]:
        return self._manifests.get(manifest_id)

    def verify_piece(self, req: PieceVerifyRequest) -> PieceVerifyResponse:
        """Verifies candidate chunk hash against authorized NCTB cryptographic manifest."""
        manifest = self._manifests.get(req.manifest_id)
        if not manifest:
            return PieceVerifyResponse(
                piece_index=req.piece_index,
                is_valid=False,
                expected_hash="",
                message=f"Manifest '{req.manifest_id}' not found.",
            )

        if req.piece_index < 0 or req.piece_index >= len(manifest.pieces):
            return PieceVerifyResponse(
                piece_index=req.piece_index,
                is_valid=False,
                expected_hash="",
                message=f"Piece index {req.piece_index} out of bounds (total: {manifest.total_pieces}).",
            )

        expected = manifest.pieces[req.piece_index].sha256_hash
        is_valid = req.candidate_hash.lower() == expected.lower()

        msg = "Piece verified against NCTB Merkle leaf." if is_valid else "Poisoned chunk detected: SHA-256 hash mismatch! Chunk discarded."
        return PieceVerifyResponse(
            piece_index=req.piece_index,
            is_valid=is_valid,
            expected_hash=expected,
            message=msg,
        )

    def get_swarm_status(self, manifest_id: str) -> Optional[SwarmStatusResponse]:
        """Returns classroom peer swarm topology, bitfields, and bandwidth savings."""
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            # Fallback to the first available manifest if requested one is not found
            if self._manifests:
                manifest_id = list(self._manifests.keys())[0]
                manifest = self._manifests[manifest_id]
            else:
                return None

        peers = self._peers.get(manifest_id, [])
        seeders = sum(1 for p in peers if p.downloaded_pieces >= manifest.total_pieces or p.is_gateway)
        leechers = len(peers) - seeders

        p2p_mb = self._p2p_transferred_mb.get(manifest_id, 0.0)
        isp_mb = self._isp_gateway_mb.get(manifest_id, 64.0)
        total_delivered_mb = p2p_mb + isp_mb

        savings_pct = (p2p_mb / total_delivered_mb * 100.0) if total_delivered_mb > 0 else 0.0

        # Compute average LAN P2P swarm transfer speed
        active_speeds = [p.download_rate_kbps for p in peers if p.download_rate_kbps > 0]
        avg_speed_mbps = (sum(active_speeds) / len(active_speeds) / 1024.0) if active_speeds else 38.5

        return SwarmStatusResponse(
            manifest_id=manifest_id,
            content_title=manifest.title,
            total_pieces=manifest.total_pieces,
            total_bytes=manifest.total_bytes,
            swarm_seeders=seeders,
            swarm_leechers=leechers,
            total_p2p_transferred_mb=round(p2p_mb, 2),
            total_isp_gateway_mb=round(isp_mb, 2),
            bandwidth_saved_percentage=round(savings_pct, 1),
            average_swarm_speed_mbps=round(avg_speed_mbps, 1),
            merkle_root=manifest.merkle_root,
            peers=peers,
        )

    def simulate_p2p_transfer(self, req: TransferSimulateRequest) -> TransferSimulateResponse:
        """Simulates WebRTC DataChannel chunk transmission between classroom peers."""
        manifest = self._manifests.get(req.manifest_id)
        if not manifest:
            return TransferSimulateResponse(
                success=False,
                piece_index=req.piece_index,
                source_peer_id=req.source_peer_id,
                target_peer_id=req.target_peer_id,
                transfer_duration_ms=0.0,
                transfer_rate_mbps=0.0,
                target_completion_ratio=0.0,
                message=f"Manifest '{req.manifest_id}' not found.",
            )

        peers = self._peers.get(req.manifest_id, [])
        src = next((p for p in peers if p.peer_id == req.source_peer_id), None)
        tgt = next((p for p in peers if p.peer_id == req.target_peer_id), None)

        if not src or not tgt:
            return TransferSimulateResponse(
                success=False,
                piece_index=req.piece_index,
                source_peer_id=req.source_peer_id,
                target_peer_id=req.target_peer_id,
                transfer_duration_ms=0.0,
                transfer_rate_mbps=0.0,
                target_completion_ratio=0.0,
                message="Source or target peer not found in swarm.",
            )

        # Simulate 1MB piece transfer over classroom 5GHz / 2.4GHz Wi-Fi WebRTC
        piece_mb = manifest.piece_size_bytes / (1024 * 1024)
        simulated_rate_mbps = 42.5  # ~42.5 Mbps LAN transfer
        duration_ms = round((piece_mb * 8 / simulated_rate_mbps) * 1000, 2)

        if tgt.downloaded_pieces < manifest.total_pieces:
            tgt.downloaded_pieces += 1
            if tgt.downloaded_pieces >= manifest.total_pieces:
                tgt.role = "seeder"

        # Increment P2P transferred volume
        self._p2p_transferred_mb[req.manifest_id] = self._p2p_transferred_mb.get(req.manifest_id, 0.0) + piece_mb
        ratio = round(tgt.downloaded_pieces / manifest.total_pieces, 3)

        return TransferSimulateResponse(
            success=True,
            piece_index=req.piece_index,
            source_peer_id=req.source_peer_id,
            target_peer_id=req.target_peer_id,
            transfer_duration_ms=duration_ms,
            transfer_rate_mbps=simulated_rate_mbps,
            target_completion_ratio=ratio,
            message=f"Piece #{req.piece_index} streamed P2P in {duration_ms}ms at {simulated_rate_mbps} Mbps.",
        )

    def get_rarest_first_schedule(self, manifest_id: str) -> List[Dict[str, int]]:
        """Calculates piece frequency across peers to prioritize rarest pieces."""
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            if self._manifests:
                manifest_id = list(self._manifests.keys())[0]
                manifest = self._manifests[manifest_id]
            else:
                return []

        # Frequency histogram for 64 pieces
        frequency = {i: 0 for i in range(manifest.total_pieces)}
        peers = self._peers.get(manifest_id, [])

        for p in peers:
            # First 40 pieces are abundant, later pieces are rarer
            limit = min(p.downloaded_pieces, manifest.total_pieces)
            for i in range(limit):
                frequency[i] += 1

        sorted_pieces = sorted(frequency.items(), key=lambda x: (x[1], x[0]))
        return [{"piece_index": k, "availability_count": v} for k, v in sorted_pieces[:10]]

decentralized_cdn_swarm_service = DecentralizedCdnSwarmService()
