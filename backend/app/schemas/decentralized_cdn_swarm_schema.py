"""
Pydantic v2 Data Models: Decentralized Micro-Edge CDN & WebTorrent Asset Swarm (Phase 67)
Enterprise schemas for media chunk slicing, BitTorrent-style piece bitfields,
Merkle chunk trees, peer seeding telemetry, and bandwidth savings calculations.
"""

from typing import List, Dict, Optional, Any
try:
    from pydantic import BaseModel, Field, ConfigDict
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default
    def ConfigDict(**kwargs):
        return {}

class ChunkPieceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    piece_index: int = Field(..., ge=0, description="0-indexed sequence of the chunk")
    byte_offset: int = Field(..., ge=0, description="Starting byte offset in the media stream")
    byte_length: int = Field(..., gt=0, description="Length of this piece in bytes")
    sha256_hash: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 hash of piece")
    verified: bool = Field(True, description="Whether the chunk passed Merkle validation")

class MediaManifestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    manifest_id: str = Field(..., description="Unique manifest ID (e.g., MNFST-PHYS-001)")
    content_id: str = Field(..., description="Unique media asset ID")
    title: str = Field(..., description="Academic lecture / simulation asset title")
    total_bytes: int = Field(..., gt=0, description="Total media payload in bytes")
    piece_size_bytes: int = Field(1048576, gt=0, description="Default piece slice size (1MB = 1048576 bytes)")
    total_pieces: int = Field(..., gt=0, description="Total number of chunks")
    merkle_root: str = Field(..., description="Root SHA-256 hash of the balanced binary piece tree")
    created_at: str = Field(..., description="ISO 8601 creation timestamp")
    pieces: List[ChunkPieceDTO] = Field(default_factory=list, description="Ordered chunk array")

class ManifestCreateRequest(BaseModel):
    content_id: str = Field(..., min_length=3, max_length=64)
    title: str = Field(..., min_length=3, max_length=128)
    total_bytes: int = Field(67108864, ge=1048576, description="Media size in bytes (e.g. 64 MB default)")
    piece_size_bytes: int = Field(1048576, ge=65536, le=4194304, description="Chunk size (default 1MB)")

class PeerSwarmNodeDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    peer_id: str = Field(..., description="Unique peer ID (e.g., PEER-SAKIB-TAB)")
    peer_name: str = Field(..., description="Human-readable device alias")
    device_type: str = Field(..., description="Hardware profile: Tablet, Mobile, Laptop, Gateway")
    role: str = Field("leecher", description="'seeder' (100% chunks), 'leecher' (<100%), or 'gateway'")
    downloaded_pieces: int = Field(..., ge=0)
    total_pieces: int = Field(..., gt=0)
    upload_rate_kbps: float = Field(0.0, ge=0.0)
    download_rate_kbps: float = Field(0.0, ge=0.0)
    choked: bool = Field(False, description="BitTorrent tit-for-tat choke status")
    bitfield_hex: str = Field(..., description="Compact hex representation of completed pieces")
    is_gateway: bool = Field(False, description="Whether this peer is the classroom hardware tower")

class SwarmStatusResponse(BaseModel):
    manifest_id: str
    content_title: str
    total_pieces: int
    total_bytes: int
    swarm_seeders: int
    swarm_leechers: int
    total_p2p_transferred_mb: float
    total_isp_gateway_mb: float
    bandwidth_saved_percentage: float
    average_swarm_speed_mbps: float
    merkle_root: str
    peers: List[PeerSwarmNodeDTO]

class PieceVerifyRequest(BaseModel):
    manifest_id: str
    piece_index: int = Field(..., ge=0)
    candidate_hash: str = Field(..., min_length=64, max_length=64)

class PieceVerifyResponse(BaseModel):
    piece_index: int
    is_valid: bool
    expected_hash: str
    message: str

class TransferSimulateRequest(BaseModel):
    manifest_id: str
    source_peer_id: str
    target_peer_id: str
    piece_index: int = Field(..., ge=0)

class TransferSimulateResponse(BaseModel):
    success: bool
    piece_index: int
    source_peer_id: str
    target_peer_id: str
    transfer_duration_ms: float
    transfer_rate_mbps: float
    target_completion_ratio: float
    message: str
