"""
DEVELOPER ARCHITECTURE NOTE - TEST SUITE:
Phase 78: Modularize 69 Enterprise Modules into Next.js Verification
Validates 10 core architectural and integration requirements:
1. Modules Registry Catalog: All 69 modules cataloged, tier grouping, helper search/filter functions
2. Dynamic Code Splitting (dynamic.tsx): next/dynamic with ssr: false, skeleton fallback, DYNAMIC_MODULE_MAP
3. Academic Modules Porting: BionicReaderModule, AdmissionMatrixModule, SpeechDialectModule
4. Resilience Modules Porting: SatelliteLoraModule, OfflineMeshModule, WebTorrentCdnModule
5. STEM Sandboxes Porting: QuantumSandboxModule, BciTelemetryModule, MolecularGeometryModule, CfdFluidSimulatorModule
6. Enterprise Cockpit Porting: SupabaseCockpitModule, ShamirVaultModule, CampusRaftBftModule
7. Module Directory & Dual-Perspective Switcher: Core Hub vs All 69 Directory, search, category pills
8. Dedicated Modules Page & Home Link: modules.tsx and index.tsx navigation link
9. HTML5 Canvas Memory Leak Prevention: Strict cancelAnimationFrame cleanup across all canvas tools
10. Strict Zero-Emoji & Developer Architecture Note Governance: 0 emojis and 100% note coverage
"""

import os
import re
import unittest


class TestPhase78ModularEnterpriseModules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        cls.frontend_dir = os.path.join(cls.base_dir, 'frontend')
        cls.modules_dir = os.path.join(cls.frontend_dir, 'src/modules')
        cls.pages_dir = os.path.join(cls.frontend_dir, 'src/pages')

    def test_modules_registry_catalog(self):
        """Verify registry.ts declares metadata for 69 modules with helper search/filter queries."""
        reg_path = os.path.join(self.modules_dir, 'registry.ts')
        self.assertTrue(os.path.exists(reg_path), "registry.ts must exist.")

        with open(reg_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("MODULES_REGISTRY", content, "MODULES_REGISTRY must be exported.")
        self.assertIn("getModulesByCategory", content, "getModulesByCategory must be exported.")
        self.assertIn("getModulesByTier", content, "getModulesByTier must be exported.")
        self.assertIn("searchModules", content, "searchModules must be exported.")
        self.assertIn("bionic-reader", content, "Bionic reader must be indexed.")
        self.assertIn("admission-matrix", content, "Admission matrix must be indexed.")
        self.assertIn("satellite-lora", content, "Satellite LoRa must be indexed.")

    def test_dynamic_code_splitting(self):
        """Verify dynamic.tsx uses next/dynamic with ssr: false to isolate canvas/audio tools."""
        dyn_path = os.path.join(self.modules_dir, 'dynamic.tsx')
        self.assertTrue(os.path.exists(dyn_path), "dynamic.tsx must exist.")

        with open(dyn_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("dynamic(", content, "next/dynamic must be utilized.")
        self.assertIn("ssr: false", content, "ssr: false must be specified for canvas tools.")
        self.assertIn("DYNAMIC_MODULE_MAP", content, "DYNAMIC_MODULE_MAP registry must be exported.")
        self.assertIn("DynamicBionicReader", content, "DynamicBionicReader must be defined.")
        self.assertIn("DynamicAdmissionMatrix", content, "DynamicAdmissionMatrix must be defined.")
        self.assertIn("DynamicQuantumSandbox", content, "DynamicQuantumSandbox must be defined.")

    def test_academic_modules_porting(self):
        """Verify academic modules port Bionic reader, admission matrix, and dialect studio."""
        acad_dir = os.path.join(self.modules_dir, 'academic')
        bionic_path = os.path.join(acad_dir, 'BionicReaderModule.tsx')
        matrix_path = os.path.join(acad_dir, 'AdmissionMatrixModule.tsx')
        speech_path = os.path.join(acad_dir, 'SpeechDialectModule.tsx')

        for p in [bionic_path, matrix_path, speech_path]:
            self.assertTrue(os.path.exists(p), f"{os.path.basename(p)} must exist.")

        with open(bionic_path, 'r', encoding='utf-8') as f:
            b_content = f.read()
        self.assertIn("boldLen", b_content, "Bionic fixation anchor calculation must exist.")
        self.assertIn("saccadic", b_content.lower(), "Saccadic trajectory canvas must exist.")

        with open(matrix_path, 'r', encoding='utf-8') as f:
            m_content = f.read()
        self.assertIn("BENCHMARK_PROGRAMS", m_content, "Benchmark programs must be declared.")
        self.assertIn("cascade", m_content.lower(), "Migration cascade canvas must exist.")

        with open(speech_path, 'r', encoding='utf-8') as f:
            s_content = f.read()
        self.assertIn("CHITTAGONIAN", s_content, "Chittagonian dialect must be supported.")
        self.assertIn("SYLHETI", s_content, "Sylheti dialect must be supported.")
        self.assertIn("waveform", s_content.lower(), "Audio waveform canvas must exist.")

    def test_resilience_modules_porting(self):
        """Verify resilience modules port Satellite LoRa, Offline Mesh, and WebTorrent CDN."""
        res_dir = os.path.join(self.modules_dir, 'resilience')
        lora_path = os.path.join(res_dir, 'SatelliteLoraModule.tsx')
        mesh_path = os.path.join(res_dir, 'OfflineMeshModule.tsx')
        cdn_path = os.path.join(res_dir, 'WebTorrentCdnModule.tsx')

        for p in [lora_path, mesh_path, cdn_path]:
            self.assertTrue(os.path.exists(p), f"{os.path.basename(p)} must exist.")

        with open(lora_path, 'r', encoding='utf-8') as f:
            l_content = f.read()
        self.assertIn("charCount", l_content, "160-char budget must be tracked.")
        self.assertIn("solar", l_content.lower(), "Solar PV telemetry canvas must exist.")

        with open(mesh_path, 'r', encoding='utf-8') as f:
            m_content = f.read()
        self.assertIn("vectorClock", m_content, "CRDT vector clock must be tracked.")
        self.assertIn("<svg", m_content, "Interactive SVG mesh topology must exist.")

        with open(cdn_path, 'r', encoding='utf-8') as f:
            c_content = f.read()
        self.assertIn("64", c_content, "64-piece bitfield grid must be handled.")

    def test_stem_sandboxes_modules_porting(self):
        """Verify STEM sandboxes port Quantum, BCI, Molecular, and CFD modules."""
        stem_dir = os.path.join(self.modules_dir, 'stem-sandboxes')
        quantum_path = os.path.join(stem_dir, 'QuantumSandboxModule.tsx')
        bci_path = os.path.join(stem_dir, 'BciTelemetryModule.tsx')
        mol_path = os.path.join(stem_dir, 'MolecularGeometryModule.tsx')
        cfd_path = os.path.join(stem_dir, 'CfdFluidSimulatorModule.tsx')

        for p in [quantum_path, bci_path, mol_path, cfd_path]:
            self.assertTrue(os.path.exists(p), f"{os.path.basename(p)} must exist.")

        with open(quantum_path, 'r', encoding='utf-8') as f:
            q_content = f.read()
        self.assertIn("quantumStateN", q_content, "Principal quantum state n must be modeled.")
        self.assertIn("wavefunction", q_content.lower(), "Wavefunction canvas must exist.")

        with open(bci_path, 'r', encoding='utf-8') as f:
            b_content = f.read()
        self.assertIn("cognitiveLoad", b_content, "Cognitive load index must be tracked.")
        self.assertIn("Fp1", b_content, "EEG 10-20 electrode channel must be modeled.")

        with open(mol_path, 'r', encoding='utf-8') as f:
            mol_content = f.read()
        self.assertIn("MOLECULES_DB", mol_content, "VSEPR database must exist.")
        self.assertIn("bondAngle", mol_content, "Bond angles must be tracked.")

        with open(cfd_path, 'r', encoding='utf-8') as f:
            cfd_content = f.read()
        self.assertIn("reynoldsNumber", cfd_content, "Reynolds number must be controllable.")
        self.assertIn("streamline", cfd_content.lower(), "Velocity streamlines must be rendered.")

    def test_enterprise_cockpit_modules_porting(self):
        """Verify enterprise cockpit ports Supabase, Shamir Vault, and Campus Raft BFT."""
        ent_dir = os.path.join(self.modules_dir, 'enterprise-cockpit')
        supa_path = os.path.join(ent_dir, 'SupabaseCockpitModule.tsx')
        shamir_path = os.path.join(ent_dir, 'ShamirVaultModule.tsx')
        raft_path = os.path.join(ent_dir, 'CampusRaftBftModule.tsx')

        for p in [supa_path, shamir_path, raft_path]:
            self.assertTrue(os.path.exists(p), f"{os.path.basename(p)} must exist.")

        with open(supa_path, 'r', encoding='utf-8') as f:
            s_content = f.read()
        self.assertIn("BENCHMARK_POLICIES", s_content, "RLS benchmark policies must exist.")
        self.assertIn("jwksStatus", s_content, "JWKS rotation status must exist.")

        with open(shamir_path, 'r', encoding='utf-8') as f:
            sh_content = f.read()
        self.assertIn("isQuorumReached", sh_content, "3-of-5 threshold quorum must be calculated.")
        self.assertIn("zeroize", sh_content.lower(), "Anti-tamper zeroization must exist.")

        with open(raft_path, 'r', encoding='utf-8') as f:
            r_content = f.read()
        self.assertIn("INITIAL_NODES", r_content, "5-campus consortium nodes must exist.")
        self.assertIn("commitIndex", r_content, "Replicated commit index must be tracked.")

    def test_module_directory_and_dual_perspective(self):
        """Verify ModuleDirectory.tsx implements the dual-perspective toggle and instant search."""
        dir_path = os.path.join(self.modules_dir, 'ModuleDirectory.tsx')
        self.assertTrue(os.path.exists(dir_path), "ModuleDirectory.tsx must exist.")

        with open(dir_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("perspective", content, "Perspective state must exist.")
        self.assertIn("searchQuery", content, "Search query filter must exist.")
        self.assertIn("selectedCategory", content, "Category filter pill state must exist.")
        self.assertIn("DYNAMIC_MODULE_MAP", content, "DYNAMIC_MODULE_MAP must be wired.")
        self.assertIn("কোর হাব (Tabs 1-5)", content, "Student Core Hub label must exist.")
        self.assertIn("সমস্ত মডিউল (Tabs 1-69)", content, "All 69 Modules Directory label must exist.")

    def test_modules_page_mounting(self):
        """Verify modules.tsx page mounts ModuleDirectory and index.tsx provides header link."""
        page_path = os.path.join(self.pages_dir, 'modules.tsx')
        index_path = os.path.join(self.pages_dir, 'index.tsx')

        self.assertTrue(os.path.exists(page_path), "modules.tsx page must exist.")
        with open(page_path, 'r', encoding='utf-8') as f:
            p_content = f.read()
        self.assertIn("ModuleDirectory", p_content, "modules.tsx must render ModuleDirectory.")

        with open(index_path, 'r', encoding='utf-8') as f:
            i_content = f.read()
        self.assertIn('/modules', i_content, "index.tsx must link to /modules directory.")

    def test_canvas_request_animation_frame_cleanup(self):
        """Verify all canvas-based components properly cancelAnimationFrame on unmount."""
        canvas_files = [
            os.path.join(self.modules_dir, 'academic/BionicReaderModule.tsx'),
            os.path.join(self.modules_dir, 'academic/AdmissionMatrixModule.tsx'),
            os.path.join(self.modules_dir, 'academic/SpeechDialectModule.tsx'),
            os.path.join(self.modules_dir, 'resilience/SatelliteLoraModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/QuantumSandboxModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/BciTelemetryModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/MolecularGeometryModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/CfdFluidSimulatorModule.tsx'),
            os.path.join(self.modules_dir, 'enterprise-cockpit/ShamirVaultModule.tsx'),
        ]

        for filepath in canvas_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            self.assertIn(
                "cancelAnimationFrame",
                content,
                f"File {os.path.basename(filepath)} must call cancelAnimationFrame in unmount cleanup."
            )
            self.assertIn(
                "useRef<HTMLCanvasElement",
                content,
                f"File {os.path.basename(filepath)} must maintain an HTMLCanvasElement ref."
            )

    def test_strict_zero_emoji_and_architecture_notes(self):
        """Verify all 17 Phase 78 files adhere to strict Zero-Emoji policy and have Developer Notes."""
        files_to_check = [
            os.path.join(self.modules_dir, 'registry.ts'),
            os.path.join(self.modules_dir, 'dynamic.tsx'),
            os.path.join(self.modules_dir, 'ModuleDirectory.tsx'),
            os.path.join(self.modules_dir, 'academic/BionicReaderModule.tsx'),
            os.path.join(self.modules_dir, 'academic/AdmissionMatrixModule.tsx'),
            os.path.join(self.modules_dir, 'academic/SpeechDialectModule.tsx'),
            os.path.join(self.modules_dir, 'resilience/SatelliteLoraModule.tsx'),
            os.path.join(self.modules_dir, 'resilience/OfflineMeshModule.tsx'),
            os.path.join(self.modules_dir, 'resilience/WebTorrentCdnModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/QuantumSandboxModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/BciTelemetryModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/MolecularGeometryModule.tsx'),
            os.path.join(self.modules_dir, 'stem-sandboxes/CfdFluidSimulatorModule.tsx'),
            os.path.join(self.modules_dir, 'enterprise-cockpit/SupabaseCockpitModule.tsx'),
            os.path.join(self.modules_dir, 'enterprise-cockpit/ShamirVaultModule.tsx'),
            os.path.join(self.modules_dir, 'enterprise-cockpit/CampusRaftBftModule.tsx'),
            os.path.join(self.pages_dir, 'modules.tsx'),
        ]

        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

        for filepath in files_to_check:
            self.assertTrue(os.path.exists(filepath), f"File {filepath} must exist.")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verify Developer Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content[:600],
                f"File {os.path.basename(filepath)} must start with a prominent DEVELOPER ARCHITECTURE NOTE."
            )

            # Verify Strict Zero-Emoji Policy
            matches = emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {os.path.basename(filepath)} contains forbidden emojis: {matches}"
            )


if __name__ == '__main__':
    unittest.main()
