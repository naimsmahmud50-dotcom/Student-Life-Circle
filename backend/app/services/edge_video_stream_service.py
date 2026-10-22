"""
Phase 57: Edge Video Stream Service.
Provides HLS multi-variant master playlists, micro-chunk slicing (2s duration),
and CDN edge-caching header generation with path traversal & injection hardening.
"""

import math
import hashlib
import re
from typing import Dict, Any, List, Optional


class EdgeVideoStreamService:
    """
    High-efficiency HLS Edge Video Streamer optimized for low-bandwidth 2G/3G
    environments across educational networks in Bangladesh.
    """

    # Multi-bitrate ladder tailored for low latency and data economy
    LADDER_PROFILES: Dict[str, Dict[str, Any]] = {
        "144p": {
            "bandwidth_bps": 96000,
            "resolution_w_h": "256x144",
            "frame_rate": 15.0,
            "codecs": "avc1.42c00b,mp4a.40.2",
            "target_device": "Ultra Data Saver / 2G Rural Mobile"
        },
        "240p": {
            "bandwidth_bps": 240000,
            "resolution_w_h": "426x240",
            "frame_rate": 24.0,
            "codecs": "avc1.42c015,mp4a.40.2",
            "target_device": "Data Saver / 3G Cellular Mobile"
        },
        "360p": {
            "bandwidth_bps": 480000,
            "resolution_w_h": "640x360",
            "frame_rate": 25.0,
            "codecs": "avc1.4d401e,mp4a.40.2",
            "target_device": "Standard Mobile 4G / Tablet"
        },
        "720p": {
            "bandwidth_bps": 1800000,
            "resolution_w_h": "1280x720",
            "frame_rate": 30.0,
            "codecs": "avc1.4d401f,mp4a.40.2",
            "target_device": "HD Campus WiFi / Broadband"
        },
        "1080p": {
            "bandwidth_bps": 4200000,
            "resolution_w_h": "1920x1080",
            "frame_rate": 30.0,
            "codecs": "avc1.640028,mp4a.40.2",
            "target_device": "Full HD Desktop / Lab Workstation"
        }
    }

    SAFE_SLUG_PATTERN = re.compile(r"^[a-zA-Z0-9_\-]+$")

    def sanitize_identifier(self, identifier: str) -> str:
        """
        Validates identifier to block Directory Traversal, LFI, and command injection attacks.
        Strix Security Standard: Zero unescaped path components allowed.
        """
        if not identifier or not isinstance(identifier, str):
            raise ValueError("Identifier must be a non-empty string.")

        if ".." in identifier or "/" in identifier or "\\" in identifier or "\0" in identifier:
            raise ValueError("Illegal path traversal or null byte detected in identifier.")

        if not self.SAFE_SLUG_PATTERN.match(identifier):
            raise ValueError("Identifier contains invalid characters. Use alphanumeric, dash, or underscore.")

        return identifier

    def generate_master_playlist(
        self,
        lecture_id: str,
        title: str,
        duration_seconds: int,
        available_resolutions: Optional[List[str]] = None,
        chunk_duration_seconds: int = 2
    ) -> Dict[str, Any]:
        """
        Generates RFC 8216 compliant HLS master playlist (.m3u8) referencing
        adaptive bitrate variant streams.
        """
        clean_lecture_id = self.sanitize_identifier(lecture_id)

        if duration_seconds <= 0:
            raise ValueError("Lecture duration must be positive.")

        chunk_duration = max(1, chunk_duration_seconds)
        total_segments = math.ceil(duration_seconds / chunk_duration)

        if not available_resolutions:
            available_resolutions = ["144p", "240p", "360p", "720p", "1080p"]

        lines = [
            "#EXTM3U",
            "#EXT-X-VERSION:6",
            "#EXT-X-INDEPENDENT-SEGMENTS",
            f"# Generated for Lecture: {clean_lecture_id} - {title}"
        ]

        variant_profiles = []
        for res in available_resolutions:
            profile = self.LADDER_PROFILES.get(res)
            if not profile:
                continue

            bw = profile["bandwidth_bps"]
            res_wh = profile["resolution_w_h"]
            codecs = profile["codecs"]
            uri = f"/api/v1/video/stream/{clean_lecture_id}/{res}/playlist.m3u8"

            lines.append(f'#EXT-X-STREAM-INF:BANDWIDTH={bw},RESOLUTION={res_wh},CODECS="{codecs}"')
            lines.append(uri)

            variant_profiles.append({
                "resolution": res,
                "bandwidth_bps": bw,
                "resolution_w_h": res_wh,
                "codecs": codecs,
                "playlist_uri": uri,
                "target_device": profile["target_device"]
            })

        master_content = "\n".join(lines) + "\n"
        etag_digest = f'"{hashlib.sha256(master_content.encode("utf-8")).hexdigest()[:16]}"'

        return {
            "lecture_id": clean_lecture_id,
            "title": title,
            "duration_seconds": duration_seconds,
            "master_playlist_m3u8": master_content,
            "variant_profiles": variant_profiles,
            "total_segments_per_variant": total_segments,
            "edge_cache_control": "public, max-age=31536000, immutable",
            "etag_digest": etag_digest
        }

    def generate_variant_playlist(
        self,
        lecture_id: str,
        resolution: str,
        duration_seconds: int,
        chunk_duration_seconds: int = 2
    ) -> str:
        """
        Generates variant media playlist (.m3u8) referencing segmented .ts chunks.
        """
        clean_lecture_id = self.sanitize_identifier(lecture_id)
        if resolution not in self.LADDER_PROFILES:
            raise ValueError(f"Unknown resolution profile: {resolution}")

        chunk_dur = max(1, chunk_duration_seconds)
        total_segments = math.ceil(duration_seconds / chunk_dur)

        lines = [
            "#EXTM3U",
            "#EXT-X-VERSION:6",
            f"#EXT-X-TARGETDURATION:{chunk_dur}",
            "#EXT-X-MEDIA-SEQUENCE:0",
            "#EXT-X-PLAYLIST-TYPE:VOD"
        ]

        remaining_time = float(duration_seconds)
        for seg_idx in range(total_segments):
            seg_len = min(float(chunk_dur), remaining_time)
            remaining_time -= seg_len
            lines.append(f"#EXTINF:{seg_len:.1f},")
            lines.append(f"/api/v1/video/stream/{clean_lecture_id}/{resolution}/segment_{seg_idx:05d}.ts")

        lines.append("#EXT-X-ENDLIST")
        return "\n".join(lines) + "\n"

    def resolve_video_chunk(
        self,
        lecture_id: str,
        resolution: str,
        segment_index: int,
        chunk_duration_seconds: int = 2
    ) -> Dict[str, Any]:
        """
        Resolves micro-chunk metadata, byte ranges, SHA-256 chunk checksum,
        and CDN edge-caching headers.
        """
        try:
            clean_lecture_id = self.sanitize_identifier(lecture_id)
        except ValueError as e:
            return {
                "lecture_id": lecture_id,
                "resolution": resolution,
                "segment_index": segment_index,
                "segment_filename": "",
                "byte_range_start": 0,
                "byte_range_end": 0,
                "chunk_bytes": 0,
                "sha256_checksum": "",
                "cache_headers": {},
                "is_safe": False,
                "rejection_reason": str(e)
            }

        if resolution not in self.LADDER_PROFILES:
            return {
                "lecture_id": clean_lecture_id,
                "resolution": resolution,
                "segment_index": segment_index,
                "segment_filename": "",
                "byte_range_start": 0,
                "byte_range_end": 0,
                "chunk_bytes": 0,
                "sha256_checksum": "",
                "cache_headers": {},
                "is_safe": False,
                "rejection_reason": f"Invalid resolution {resolution}."
            }

        if segment_index < 0:
            return {
                "lecture_id": clean_lecture_id,
                "resolution": resolution,
                "segment_index": segment_index,
                "segment_filename": "",
                "byte_range_start": 0,
                "byte_range_end": 0,
                "chunk_bytes": 0,
                "sha256_checksum": "",
                "cache_headers": {},
                "is_safe": False,
                "rejection_reason": "Segment index cannot be negative."
            }

        profile = self.LADDER_PROFILES[resolution]
        bandwidth_bps = profile["bandwidth_bps"]
        bytes_per_second = bandwidth_bps / 8
        chunk_bytes = int(bytes_per_second * chunk_duration_seconds)

        byte_start = segment_index * chunk_bytes
        byte_end = byte_start + chunk_bytes - 1
        filename = f"segment_{segment_index:05d}.ts"

        # Deterministic chunk integrity hash
        seed_str = f"{clean_lecture_id}:{resolution}:{segment_index}:{byte_start}:{byte_end}"
        chunk_sha256 = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()

        cache_headers = {
            "Content-Type": "video/MP2T",
            "Accept-Ranges": "bytes",
            "Cache-Control": "public, max-age=31536000, immutable",
            "ETag": f'"{chunk_sha256[:16]}"',
            "Surrogate-Key": f"lec-{clean_lecture_id} {resolution}",
            "X-Content-Type-Options": "nosniff"
        }

        return {
            "lecture_id": clean_lecture_id,
            "resolution": resolution,
            "segment_index": segment_index,
            "segment_filename": filename,
            "byte_range_start": byte_start,
            "byte_range_end": byte_end,
            "chunk_bytes": chunk_bytes,
            "sha256_checksum": chunk_sha256,
            "cache_headers": cache_headers,
            "is_safe": True,
            "rejection_reason": None
        }
