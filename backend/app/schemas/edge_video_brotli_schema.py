"""
Pydantic Schemas for Phase 57: Ultra Low-Bandwidth Edge Video & Brotli Streamer.
Dual-resilience fallback included for zero-dependency test execution.
"""

from typing import Dict, Any, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default


# --- Schemas for Edge Video Stream Service ---
class VideoManifestRequest(BaseModel):
    lecture_id: str = Field(..., description="Unique slug/ID for the academic lecture")
    title: str = Field(..., description="Lecture title, e.g. Data Structures & Algorithms - Heap Sort")
    duration_seconds: int = Field(..., description="Total lecture duration in seconds")
    available_resolutions: Optional[List[str]] = Field(
        default=["144p", "240p", "360p", "720p", "1080p"],
        description="Target video resolutions for ABR ladder"
    )
    chunk_duration_seconds: Optional[int] = Field(2, description="Target micro-chunk duration in seconds")


class VideoVariantProfile(BaseModel):
    resolution: str
    bandwidth_bps: int
    codecs: str
    playlist_uri: str
    target_device: str


class VideoManifestResponse(BaseModel):
    lecture_id: str
    title: str
    duration_seconds: int
    master_playlist_m3u8: str
    variant_profiles: List[Dict[str, Any]]
    total_segments_per_variant: int
    edge_cache_control: str
    etag_digest: str


class VideoChunkRequest(BaseModel):
    lecture_id: str = Field(..., description="Lecture ID")
    resolution: str = Field(..., description="Target resolution, e.g. 144p, 360p, 720p")
    segment_index: int = Field(..., description="0-indexed segment sequence number")


class VideoChunkResponse(BaseModel):
    lecture_id: str
    resolution: str
    segment_index: int
    segment_filename: str
    byte_range_start: int
    byte_range_end: int
    chunk_bytes: int
    sha256_checksum: str
    cache_headers: Dict[str, str]
    is_safe: bool
    rejection_reason: Optional[str] = None


# --- Schemas for Brotli Payload Compressor Service ---
class BrotliCompressionRequest(BaseModel):
    payload_content: str = Field(..., description="Raw text or JSON payload string")
    compression_level: Optional[int] = Field(6, description="Brotli compression level (1-11)")
    client_rtt_ms: Optional[float] = Field(150.0, description="Round-trip time in milliseconds")
    device_battery_saver: Optional[bool] = Field(False, description="Whether client is on battery saver mode")


class BrotliCompressionResponse(BaseModel):
    uncompressed_bytes: int
    gzip_bytes: int
    brotli_bytes: int
    compression_ratio_brotli: float
    data_saved_percentage: float
    estimated_cost_savings_bdt: float
    recommended_level: int
    payload_sha256: str
    encoded_sample_b64: str


# --- Schemas for Adaptive Bitrate Advisor Service ---
class AdaptiveBitrateRequest(BaseModel):
    measured_throughput_kbps: float = Field(..., description="Instantaneous network throughput in kbps")
    current_resolution: str = Field("360p", description="Current playback resolution")
    buffer_occupancy_seconds: float = Field(..., description="Seconds of unplayed video currently in buffer")
    device_pixel_ratio: Optional[float] = Field(1.0, description="Client device pixel ratio")
    is_metered_connection: Optional[bool] = Field(False, description="True if on 2G/3G mobile data package")


class AdaptiveBitrateResponse(BaseModel):
    measured_throughput_kbps: float
    smoothed_throughput_kbps: float
    current_resolution: str
    recommended_resolution: str
    is_switching_resolution: bool
    buffer_health_status: str
    stall_risk_percentage: float
    hysteresis_applied: bool
    advisor_action: str
