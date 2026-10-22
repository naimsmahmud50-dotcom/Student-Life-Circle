"""
Comprehensive Automated Unit Tests for Phase 57:
Ultra Low-Bandwidth Edge Video & Brotli Streamer.
"""

import unittest
from backend.app.services.edge_video_stream_service import EdgeVideoStreamService
from backend.app.services.brotli_payload_compressor_service import BrotliPayloadCompressorService
from backend.app.services.adaptive_bitrate_advisor_service import AdaptiveBitrateAdvisorService


class TestPhase57EdgeVideoAndBrotli(unittest.TestCase):

    def setUp(self):
        self.video_service = EdgeVideoStreamService()
        self.brotli_service = BrotliPayloadCompressorService()
        self.abr_service = AdaptiveBitrateAdvisorService()

    # --- EdgeVideoStreamService Tests ---
    def test_edge_video_master_playlist_generation(self):
        res = self.video_service.generate_master_playlist(
            lecture_id="cse201-heap-sort",
            title="Data Structures: Heap Sort",
            duration_seconds=120,
            available_resolutions=["144p", "240p", "360p", "720p", "1080p"],
            chunk_duration_seconds=2
        )
        self.assertEqual(res["lecture_id"], "cse201-heap-sort")
        self.assertEqual(res["total_segments_per_variant"], 60)
        self.assertIn("#EXTM3U", res["master_playlist_m3u8"])
        self.assertIn("#EXT-X-STREAM-INF:BANDWIDTH=96000", res["master_playlist_m3u8"])
        self.assertIn("#EXT-X-STREAM-INF:BANDWIDTH=4200000", res["master_playlist_m3u8"])
        self.assertEqual(len(res["variant_profiles"]), 5)
        self.assertTrue(res["etag_digest"].startswith('"'))
        self.assertEqual(res["edge_cache_control"], "public, max-age=31536000, immutable")

    def test_edge_video_variant_playlist(self):
        variant_m3u8 = self.video_service.generate_variant_playlist(
            lecture_id="phy101-newton",
            resolution="360p",
            duration_seconds=10,
            chunk_duration_seconds=2
        )
        self.assertIn("#EXT-X-TARGETDURATION:2", variant_m3u8)
        self.assertIn("#EXTINF:2.0,", variant_m3u8)
        self.assertIn("segment_00000.ts", variant_m3u8)
        self.assertIn("segment_00004.ts", variant_m3u8)
        self.assertIn("#EXT-X-ENDLIST", variant_m3u8)

    def test_edge_video_security_path_traversal_blocked(self):
        with self.assertRaises(ValueError):
            self.video_service.generate_master_playlist(
                lecture_id="../secrets/private_key",
                title="Hacking attempt",
                duration_seconds=60
            )

        with self.assertRaises(ValueError):
            self.video_service.sanitize_identifier("lecture; rm -rf /")

        chunk_res = self.video_service.resolve_video_chunk(
            lecture_id="../../etc/passwd",
            resolution="360p",
            segment_index=0
        )
        self.assertFalse(chunk_res["is_safe"])
        self.assertIn("Illegal path traversal", chunk_res["rejection_reason"])

    def test_edge_video_chunk_resolution(self):
        chunk = self.video_service.resolve_video_chunk(
            lecture_id="math301-calculus",
            resolution="360p",
            segment_index=3,
            chunk_duration_seconds=2
        )
        self.assertTrue(chunk["is_safe"])
        self.assertEqual(chunk["segment_filename"], "segment_00003.ts")
        # 360p = 480,000 bps -> 60,000 bytes/sec -> 120,000 bytes per 2s chunk
        self.assertEqual(chunk["chunk_bytes"], 120000)
        self.assertEqual(chunk["byte_range_start"], 360000)
        self.assertEqual(chunk["byte_range_end"], 479999)
        self.assertEqual(len(chunk["sha256_checksum"]), 64)
        self.assertEqual(chunk["cache_headers"]["Accept-Ranges"], "bytes")

    def test_edge_video_negative_segment_rejected(self):
        chunk = self.video_service.resolve_video_chunk(
            lecture_id="math301-calculus",
            resolution="360p",
            segment_index=-5
        )
        self.assertFalse(chunk["is_safe"])
        self.assertIn("negative", chunk["rejection_reason"])

    # --- BrotliPayloadCompressorService Tests ---
    def test_brotli_compress_payload_metrics(self):
        sample_payload = (
            '{"curriculum": "HSC Science 2026", "chapters": ["Vector", "Dynamics", "Thermodynamics"], '
            '"questions": [{"id": 1, "stem": "Explain Carnot Cycle efficiency.", "options": ["A", "B", "C", "D"]}]} '
            * 30
        )
        res = self.brotli_service.compress_payload(sample_payload, compression_level=7)
        self.assertGreater(res["uncompressed_bytes"], 1000)
        self.assertLess(res["brotli_bytes"], res["uncompressed_bytes"])
        self.assertGreater(res["data_saved_percentage"], 60.0)
        self.assertGreater(res["compression_ratio_brotli"], 2.0)
        self.assertGreater(res["estimated_cost_savings_bdt"], 0.0)
        self.assertEqual(len(res["payload_sha256"]), 64)

    def test_brotli_empty_payload(self):
        res = self.brotli_service.compress_payload("")
        self.assertEqual(res["uncompressed_bytes"], 0)
        self.assertEqual(res["brotli_bytes"], 0)
        self.assertEqual(res["data_saved_percentage"], 0.0)

    def test_brotli_level_recommendations(self):
        # Battery saver active
        self.assertEqual(self.brotli_service.recommend_compression_level(100.0, device_battery_saver=True), 4)
        # Slow 2G rural mobile
        self.assertEqual(self.brotli_service.recommend_compression_level(320.0, device_battery_saver=False), 11)
        # 3G mobile
        self.assertEqual(self.brotli_service.recommend_compression_level(180.0, device_battery_saver=False), 8)
        # High speed fiber
        self.assertEqual(self.brotli_service.recommend_compression_level(25.0, device_battery_saver=False), 5)

    # --- AdaptiveBitrateAdvisorService Tests ---
    def test_abr_ema_smoothing(self):
        s1 = self.abr_service.advise_bitrate(
            measured_throughput_kbps=1000.0,
            session_id="test_student_1"
        )
        self.assertEqual(s1["measured_throughput_kbps"], 1000.0)

        # Spike to 3000 kbps: EMA smoothing should dampen spike
        s2 = self.abr_service.advise_bitrate(
            measured_throughput_kbps=3000.0,
            session_id="test_student_1"
        )
        # EMA: 0.35 * 3000 + 0.65 * 1000 = 1050 + 650 = 1700
        self.assertEqual(s2["smoothed_throughput_kbps"], 1700.0)

    def test_abr_emergency_downgrade_on_buffer_starvation(self):
        res = self.abr_service.advise_bitrate(
            measured_throughput_kbps=4000.0,
            current_resolution="720p",
            buffer_occupancy_seconds=2.1,  # Buffer starving!
            session_id="test_starving"
        )
        self.assertEqual(res["recommended_resolution"], "360p")
        self.assertEqual(res["buffer_health_status"], "CRITICAL_STARVATION")
        self.assertGreater(res["stall_risk_percentage"], 80.0)
        self.assertIn("Emergency downscale", res["advisor_action"])

    def test_abr_metered_connection_cap(self):
        res = self.abr_service.advise_bitrate(
            measured_throughput_kbps=10000.0,  # 10 Mbps campus speed
            current_resolution="360p",
            buffer_occupancy_seconds=20.0,
            is_metered_connection=True,  # Student requested data saver
            session_id="test_metered"
        )
        # Should NOT upgrade to 1080p, capped at 360p
        self.assertEqual(res["recommended_resolution"], "360p")

    def test_abr_hysteresis_damping(self):
        # Current resolution 360p, throughput rises to 1600 kbps (barely over 720p min of 1500),
        # but 1500 * 1.20 = 1800 headroom required!
        res = self.abr_service.advise_bitrate(
            measured_throughput_kbps=1600.0,
            current_resolution="360p",
            buffer_occupancy_seconds=10.0,
            session_id="test_hysteresis"
        )
        self.assertEqual(res["recommended_resolution"], "360p")
        self.assertTrue(res["hysteresis_applied"])
        self.assertIn("Hysteresis active", res["advisor_action"])


if __name__ == "__main__":
    unittest.main()
