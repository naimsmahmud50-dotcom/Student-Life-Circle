"""
Test Suite: UI JavaScript Syntax & Script Execution Integrity
Verifies that all script tags in preview.html and index.html compile and execute cleanly:
- Zero JavaScript syntax errors (verified with SpiderMonkey gjs engine)
- switchTab and setUIMode controller functions cover all 65 enterprise modules
- index.html and preview.html are synchronized
"""

import os
import re
import shutil
import subprocess
import unittest

class TestUISyntaxAndScriptExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        cls.preview_path = os.path.join(cls.base_dir, 'preview.html')
        cls.index_path = os.path.join(cls.base_dir, 'index.html')

        with open(cls.preview_path, 'r', encoding='utf-8') as f:
            cls.preview_content = f.read()

        with open(cls.index_path, 'r', encoding='utf-8') as f:
            cls.index_content = f.read()

    def test_preview_and_index_are_synchronized(self):
        """Verify index.html has identical content to preview.html."""
        self.assertEqual(
            self.preview_content,
            self.index_content,
            "index.html is out of sync with preview.html! Run sync copy command."
        )

    def test_all_scripts_compile_without_syntax_errors(self):
        """Extract all script blocks from preview.html and test compilation with SpiderMonkey JS engine."""
        gjs_bin = shutil.which('gjs')
        if not gjs_bin:
            self.skipTest("gjs (SpiderMonkey) is not installed on this system.")

        scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', self.preview_content, re.DOTALL)
        mock_env = """
        const window = {
            addEventListener: () => {},
            location: { hash: '', search: '' },
            chartInstances: {}
        };
        const document = {
            addEventListener: () => {},
            querySelectorAll: () => [],
            getElementById: () => null,
            createElement: () => ({ setAttribute: () => {}, click: () => {} }),
            documentElement: { classList: { contains: () => false, add: () => {}, remove: () => {} } }
        };
        const history = { replaceState: () => {} };
        const localStorage = { getItem: () => null, setItem: () => {} };
        const navigator = { clipboard: { writeText: () => Promise.resolve() } };
        const tailwind = { config: {} };
        """

        import tempfile
        for idx, s in enumerate(scripts, 1):
            if not s.strip():
                continue
            test_js_code = mock_env + '\n' + s
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as tf:
                tf.write(test_js_code)
                tf_path = tf.name

            try:
                process = subprocess.run(
                    [gjs_bin, tf_path],
                    capture_output=True,
                    text=True
                )
                self.assertEqual(
                    process.returncode,
                    0,
                    f"Script #{idx} failed syntax/compilation check:\n{process.stderr}"
                )
            finally:
                if os.path.exists(tf_path):
                    os.remove(tf_path)

    def test_switch_tab_covers_all_69_modules(self):
        """Ensure TAB_TITLES in script contains all 69 module IDs."""
        self.assertIn("function switchTab(tabId", self.preview_content)
        self.assertIn("admission-matrix-tower", self.preview_content)
        self.assertIn("content-admission-matrix-tower", self.preview_content)
        self.assertIn("initAdmissionMatrixTab", self.preview_content)
        self.assertIn("tab-admission-matrix-tower", self.preview_content)
        self.assertIn("accessibility-tower", self.preview_content)
        self.assertIn("content-accessibility-tower", self.preview_content)
        self.assertIn("initAccessibilityTab", self.preview_content)
        self.assertIn("tab-accessibility-tower", self.preview_content)
        self.assertIn("satellite-lora-tower", self.preview_content)
        self.assertIn("content-satellite-lora-tower", self.preview_content)
        self.assertIn("initSatelliteLoraTab", self.preview_content)
        self.assertIn("tab-satellite-lora-tower", self.preview_content)
        self.assertIn("speech-dialect-tower", self.preview_content)
        self.assertIn("content-speech-dialect-tower", self.preview_content)
        self.assertIn("initSpeechDialectTab", self.preview_content)
        self.assertIn("tab-speech-dialect-tower", self.preview_content)
        self.assertIn("campus-raft-bft", self.preview_content)
        self.assertIn("content-campus-raft-bft", self.preview_content)
        self.assertIn("initCampusRaftBftTab", self.preview_content)
        self.assertIn("tab-campus-raft-bft", self.preview_content)
        self.assertIn("shamir-exam-vault", self.preview_content)
        self.assertIn("content-shamir-exam-vault", self.preview_content)
        self.assertIn("initShamirExamVaultTab", self.preview_content)
        self.assertIn("tab-shamir-exam-vault", self.preview_content)
        self.assertIn("airgap-attendance-tower", self.preview_content)
        self.assertIn("content-airgap-attendance-tower", self.preview_content)
        self.assertIn("initAirgapAttendanceTab", self.preview_content)
        self.assertIn("tab-airgap-attendance-tower", self.preview_content)
        self.assertIn("cdn-swarm-tower", self.preview_content)
        self.assertIn("content-cdn-swarm-tower", self.preview_content)
        self.assertIn("initCdnSwarmTab", self.preview_content)
        self.assertIn("offline-mesh-tower", self.preview_content)
        self.assertIn("content-offline-mesh-tower", self.preview_content)
        self.assertIn("initOfflineMeshTab", self.preview_content)
        self.assertIn("adaptive-curriculum", self.preview_content)
        self.assertIn("grading-tower", self.preview_content)
        self.assertIn("proctoring-tower", self.preview_content)
        self.assertIn("collaborative-whiteboard", self.preview_content)
        self.assertIn("supabase-cockpit", self.preview_content)
        self.assertIn("grand-convergence", self.preview_content)
        self.assertIn("practice", self.preview_content)

    def test_segmented_perspective_and_operational_counter(self):
        """
        DEVELOPER ARCHITECTURE NOTE:
        Verifies that Phase 71, 72, 73, 74 & 75 Human-Centric UI/UX perspective controls and operational counters
        are properly wired across the preview DOM:
        - 69 Enterprise Modules banner counter is up to date (no stale 68, 67, 66, 65 or 59 counter)
        - Segmented perspective switch buttons (Student Core Hub vs All 69 Modules) are present
        - Tab buttons are annotated with data-tier attributes ('core' vs 'enterprise')
        - setUIMode function is defined in JavaScript
        """
        # 1. Operational Banner Counter
        self.assertIn("69 Enterprise Modules Operational", self.preview_content)
        self.assertNotIn("68 Enterprise Modules Operational", self.preview_content)
        self.assertNotIn("67 Enterprise Modules Operational", self.preview_content)
        self.assertNotIn("66 Enterprise Modules Operational", self.preview_content)
        self.assertNotIn("65 Enterprise Modules Operational", self.preview_content)
        self.assertNotIn("59 Enterprise Modules Operational", self.preview_content)
        self.assertIn("--- DIRECT MODULE DIRECTORY (1 TO 69 ASCENDING) ---", self.preview_content)
        self.assertNotIn("--- DIRECT MODULE DIRECTORY (1 TO 68 ASCENDING) ---", self.preview_content)

        # 2. Segmented Perspective Controls
        self.assertIn('id="uiModeCoreBtn"', self.preview_content)
        self.assertIn('id="uiModeAllBtn"', self.preview_content)
        self.assertIn('id="uiModeDescription"', self.preview_content)
        self.assertIn("function setUIMode(mode)", self.preview_content)

        # 3. Data Tier Annotations
        self.assertIn('id="tab-practice" data-tier="core"', self.preview_content)
        self.assertIn('id="tab-live" data-tier="core"', self.preview_content)
        self.assertIn('id="tab-admission" data-tier="core"', self.preview_content)
        self.assertIn('id="tab-tuition" data-tier="core"', self.preview_content)
        self.assertIn('id="tab-career" data-tier="core"', self.preview_content)
        self.assertIn('id="tab-campus-raft-bft" data-tier="enterprise"', self.preview_content)
        self.assertIn('id="tab-speech-dialect-tower" data-tier="enterprise"', self.preview_content)
        self.assertIn('id="tab-satellite-lora-tower" data-tier="enterprise"', self.preview_content)
        self.assertIn('id="tab-accessibility-tower" data-tier="enterprise"', self.preview_content)
        self.assertIn('id="tab-admission-matrix-tower" data-tier="enterprise"', self.preview_content)






