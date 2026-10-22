"""
Test Suite: UI Language Architecture Standardization
Verifies that preview.html complies with the strict architectural mandate:
- 100% English UI Chrome (buttons, tabs, headers, KPI metrics, tables, forms)
- Dynamic Question Medium Switcher available for students (English vs Bengali)
- Zero emoji policy with SVG icons
"""

import os
import re
import unittest

class TestUILanguageArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preview_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../preview.html'))
        with open(cls.preview_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

    def test_html_lang_attribute_is_english(self):
        """Verify the root html tag specifies lang='en'."""
        self.assertIn('<html lang="en"', self.html_content)

    def test_page_title_is_english(self):
        """Verify page title is in professional English."""
        self.assertIn('<title>Agrojatra | Student Life Circle - Enterprise Growth Platform</title>', self.html_content)

    def test_all_41_tabs_are_english(self):
        """Verify all 41 navigation tabs are defined with English labels."""
        expected_tabs = [
            "Practice & Live MCQ",
            "Live Challenges & Leaderboard",
            "Admission Hub & Diagnostics",
            "Tuition & Bilateral Consent",
            "Career & CV Snapshot",
            "Admin Quarantine & Audit",
            "AI Pipeline & SME Approval",
            "Psychometrics & Habit Engine",
            "Guardian Safety & Dispute Center",
            "Enterprise Telemetry & Health",
            "Offline Sync & Security Shield",
            "Cryptographic Ledger & Credentials",
            "Spaced Repetition & Study Plan",
            "Peer Circles & Tribunal Arbitration",
            "Computerized Adaptive Testing (CAT)",
            "Socratic AI Tutor & Vector Graph",
            "AI Mock Interview & Career Fit",
            "Predictive CGPA & National Rank",
            "Daily Study Scheduler & Burnout Shield",
            "Student Growth & Reputation Radar",
            "Guardian Telemetry & Escrow Vault",
            "Peer Study Circles & Bounty Tribunal",
            "Micro-Scholarship & Technical Arena",
            "Alumni Mentorship & Adaptive Pathways",
            "Admission Multiplexer & Talent Passport",
            "Math Solver, Alumni Referrals & Voice Viva",
            "Virtual Science Lab, Batch Pool & Capstones",
            "Molecular Geometry, Syllabus Atlas & Innovation Launchpad",
            "Algorithm Complexity, Thesis Citations & Campus Ambassadors",
            "National Olympiad Arena, Semiconductor Lab & Patent Registry",
            "Orbital Aerospace Telemetry, Global Research Grants & Swarm Study Pods",
            "Edge Robotics & Drone Lab, Genomic Bioinformatics & Medical Diagnostics",
            "Post-Quantum Cryptography, Smart Grid Lab & Carbon Registry",
            "Cyber Range Zero-Trust, HPC Supercomputer Lab & Student VC Syndicate",
            "Formal Verification Sandbox, Decentralized IPFS DAG & FinTech Quantitative Risk Arena",
            "BCI Cognitive Telemetry, Scientific Hypothesis Discovery & Logistics Operations Sandbox",
            "Digital Twin Simulation, CFD Flow Sandbox & DAO Governance Protocol",
            "Quantum Error Correction, Climate Dynamics & Swarm Robotics Arena",
            "Fusion Tokamak Physics, Neuromorphic SNN & Maritime COLREGs Sandbox",
            "Nanophotonics Metamaterial, Gravitational LIGO & CRISPR Gene Lab",
            "Nuclear SMR Reactor, Interplanetary Astrodynamics & Topological Quantum Lab"
        ]
        for tab_name in expected_tabs:
            self.assertIn(tab_name, self.html_content, f"Navigation tab '{tab_name}' not found in preview.html")

    def test_question_medium_switcher_present(self):
        """Verify Question Medium Switcher is present in the UI with EN and BN modes."""
        self.assertIn('Question Medium:', self.html_content)
        self.assertIn('setQuestionLang(\'en\')', self.html_content)
        self.assertIn('setQuestionLang(\'bn\')', self.html_content)
        self.assertIn('id="langBtnEn"', self.html_content)
        self.assertIn('id="langBtnBn"', self.html_content)

    def test_bengali_characters_strictly_isolated_to_academic_content(self):
        """
        Verify that Bengali characters are ONLY present in:
        1. practiceQuestions.bn data object (for dynamic curriculum adaptation)
        2. Socratic student prompt parser (supporting students typing in Bengali)
        Zero Bengali in any button, navigation tab, metric card, or UI element.
        """
        lines = self.html_content.splitlines()
        for idx, line in enumerate(lines, 1):
            bengali_matches = re.findall(r'[\u0980-\u09FF]+', line)
            if bengali_matches:
                is_academic_dict = ('curriculum:' in line or 'topic:' in line or 'stem:' in line or 
                                    'explanation:' in line or 'options:' in line or
                                    'rules:' in line or 'standard:' in line or 'example:' in line or
                                    'word:' in line or 'dialect' in line.lower() or
                                    line.strip().startswith('a:') or line.strip().startswith('b:') or 
                                    line.strip().startswith('c:') or line.strip().startswith('d:'))
                is_socratic_parser = ('lower.includes' in line or 'text.includes' in line)
                self.assertTrue(
                    is_academic_dict or is_socratic_parser,
                    f"Forbidden Bengali text found in UI chrome at line {idx}: {line.strip()}"
                )

    def test_10ms_video_classroom_module_present(self):
        """Verify 10 Minute School benchmark: Video Micro-Classroom & In-Lecture Checkpoint Quiz."""
        self.assertIn('NCTB SYLLABUS MASTERCLASS', self.html_content)
        self.assertIn('Playback Speed:', self.html_content)
        self.assertIn('setPlaybackSpeed', self.html_content)
        self.assertIn('In-Lecture Checkpoint Quiz', self.html_content)
        self.assertIn('triggerInLectureQuizSim()', self.html_content)
        self.assertIn('videoProgressBar', self.html_content)

    def test_caretutors_live_tuition_feed_and_wizard_present(self):
        """Verify CareTutors benchmark: Live Tuition Job Feed, City Filters & Guardian Request Wizard."""
        self.assertIn('CareTutors Benchmark: Verified Marketplace', self.html_content)
        self.assertIn('Post a Tuition Request', self.html_content)
        self.assertIn('togglePostTuitionWizard()', self.html_content)
        self.assertIn('Apply for Tuition', self.html_content)
        self.assertIn('applyForTuitionJobSim', self.html_content)
        self.assertIn('filterTuitionRegion', self.html_content)

    def test_bdjobs_student_career_arena_and_pipeline_present(self):
        """Verify Bdjobs benchmark: Student Opportunities, Verified CV Snapshot & Application Pipeline."""
        self.assertIn('Bdjobs Benchmark: Student Career Arena', self.html_content)
        self.assertIn('Live Application Pipeline Tracker:', self.html_content)
        self.assertIn('1-Click Apply with Verified CV', self.html_content)
        self.assertIn('applyJobWithSealedCvSim', self.html_content)
        self.assertIn('Export Verified CV (PDF)', self.html_content)
        self.assertIn('downloadCvSnapshotPdfSim()', self.html_content)

    def test_collaborative_whiteboard_and_bounty_tribunal_present(self):
        """Verify Phase 27: Peer Study Circles, Whiteboard Scratchpad & Gamified Bounty Arena."""
        self.assertIn('Peer Study Circles & Gamified Bounty Tribunal', self.html_content)
        self.assertIn('whiteboardCanvas', self.html_content)
        self.assertIn('formulaScratchpadFeed', self.html_content)
        self.assertIn('Gamified Bounty Tribunal', self.html_content)
        self.assertIn('awardBountySim', self.html_content)
        self.assertIn('submitSolutionModal', self.html_content)
        self.assertIn('postBountyModal', self.html_content)

    def test_micro_scholarship_and_technical_arena_present(self):
        """Verify Phase 28: Micro-Scholarships, Need-Index Engine & Career Technical Assessment Arena."""
        self.assertIn('content-scholarships', self.html_content)
        self.assertIn('Micro-Scholarship Endowment & Career Technical Arena', self.html_content)
        self.assertIn('openApplyScholarshipModal', self.html_content)
        self.assertIn('disburseScholarshipSim', self.html_content)
        self.assertIn('runAtsResumeAnalysisSim', self.html_content)
        self.assertIn('runTechnicalCodeTestSim', self.html_content)

    def test_alumni_mentorship_and_adaptive_pathways_present(self):
        """Verify Phase 29: Alumni Mentorship Marketplace, Adaptive Pathways & Verifiable Certificates."""
        self.assertIn('content-mentorship', self.html_content)
        self.assertIn('Alumni Mentorship Marketplace & Adaptive Learning Pathways', self.html_content)
        self.assertIn('openBookMentorModal', self.html_content)
        self.assertIn('generateAdaptivePathwaySim', self.html_content)
        self.assertIn('completePathwayStepSim', self.html_content)
        self.assertIn('verifyCertificateSim', self.html_content)

    def test_admission_multiplexer_and_talent_passport_present(self):
        """Verify Phase 30: Autonomous Admission Multiplexer, CRDT Delta-Sync & Talent Passport."""
        self.assertIn('content-admission-passport', self.html_content)
        self.assertIn('Centralized Admission Multiplexer', self.html_content)
        self.assertIn('Offline CRDT Delta-Sync Engine', self.html_content)
        self.assertIn('Universal Student Talent Passport', self.html_content)
        self.assertIn('checkEligibilitySim', self.html_content)
        self.assertIn('batchApplySim', self.html_content)
        self.assertIn('toggleOfflineSimulation', self.html_content)
        self.assertIn('syncDeltaMutationsSim', self.html_content)
        self.assertIn('setPassportViewMode', self.html_content)

    def test_math_solver_alumni_referrals_and_viva_present(self):
        """Verify Phase 31: Autonomous AI LaTeX Math Solver, Alumni Referrals & Voice Viva."""
        self.assertIn('content-solver-referral-viva', self.html_content)
        self.assertIn('AI LaTeX Math Stepwise Solver', self.html_content)
        self.assertIn('Campus Alumni Referral Graph', self.html_content)
        self.assertIn('Smart Voice Viva-Voce Oral Simulator', self.html_content)
        self.assertIn('solveMathStepwiseSim', self.html_content)
        self.assertIn('diagnoseStepMisconceptionSim', self.html_content)
        self.assertIn('generateReferralEndorsementSim', self.html_content)
        self.assertIn('startVivaSessionSim', self.html_content)
        self.assertIn('submitVivaAudioResponseSim', self.html_content)

    def test_virtual_science_lab_batch_pool_and_capstones_present(self):
        """Verify Phase 32: Virtual Science Lab, Batch Pool & Corporate Capstones."""
        self.assertIn('content-lab-batch-capstone', self.html_content)
        self.assertIn('Virtual Science Lab, Batch Pool & Capstones', self.html_content)
        self.assertIn('Virtual Science Lab', self.html_content)
        self.assertIn('Micro-Coaching Pool', self.html_content)
        self.assertIn('Corporate Capstones', self.html_content)
        self.assertIn('simulateCircuitSim', self.html_content)
        self.assertIn('simulateOpticsSim', self.html_content)
        self.assertIn('simulateTitrationSim', self.html_content)
        self.assertIn('createCoachingBatchSim', self.html_content)
        self.assertIn('submitCapstoneMilestoneSim', self.html_content)

    def test_molecular_geometry_syllabus_atlas_and_launchpad_present(self):
        """Verify Phase 33: Molecular Geometry Lab, Syllabus Knowledge Atlas & Innovation Launchpad."""
        self.assertIn('content-stem-atlas-launchpad', self.html_content)
        self.assertIn('Molecular Geometry, Syllabus Atlas & Innovation Launchpad', self.html_content)
        self.assertIn('STEM Molecular Lab', self.html_content)
        self.assertIn('Syllabus Knowledge Atlas', self.html_content)
        self.assertIn('Innovation Launchpad', self.html_content)
        self.assertIn('simulateMolecularGeometrySim', self.html_content)
        self.assertIn('simulateRedoxBalanceSim', self.html_content)
        self.assertIn('filterSyllabusAtlasSim', self.html_content)
        self.assertIn('pitchInnovationProjectSim', self.html_content)
        self.assertIn('castProjectVoteSim', self.html_content)

    def test_algorithm_complexity_thesis_citations_and_ambassadors_present(self):
        """Verify Phase 34: Algorithm Complexity Sandbox, Thesis Citations & Campus Ambassadors."""
        self.assertIn('content-algo-thesis-ambassador', self.html_content)
        self.assertIn('Algorithm Complexity, Thesis Citations & Campus Ambassadors', self.html_content)
        self.assertIn('Algorithm Complexity Sandbox', self.html_content)
        self.assertIn('Thesis Citation Graph', self.html_content)
        self.assertIn('Campus Ambassador Syndicate', self.html_content)
        self.assertIn('analyzeCodeComplexitySim', self.html_content)
        self.assertIn('simulateAlgoTraceSim', self.html_content)
        self.assertIn('checkThesisSimilaritySim', self.html_content)
        self.assertIn('claimAmbassadorTaskSim', self.html_content)
        self.assertIn('submitAmbassadorTaskSim', self.html_content)

    def test_national_olympiad_semiconductor_and_patent_present(self):
        """Verify Phase 35: National Olympiad Arena, Semiconductor Lab & Patent Registry."""
        self.assertIn('content-olympiad-quantum-patent', self.html_content)
        self.assertIn('National Olympiad Arena, Semiconductor Lab & Patent Registry', self.html_content)
        self.assertIn('National STEM Olympiad', self.html_content)
        self.assertIn('Semiconductor & Quantum Lab', self.html_content)
        self.assertIn('University Patent Registry', self.html_content)
        self.assertIn('submitOlympiadSolutionSim', self.html_content)
        self.assertIn('simulatePnJunctionSim', self.html_content)
        self.assertIn('simulateQuantumWellSim', self.html_content)
        self.assertIn('searchPriorArtSim', self.html_content)
        self.assertIn('filePatentDisclosureSim', self.html_content)

    def test_orbital_satellite_grants_and_swarm_present(self):
        """Verify Phase 36: Orbital Aerospace Telemetry, Global Grants & Swarm Study Pods."""
        self.assertIn('content-satellite-grant-swarm', self.html_content)
        self.assertIn('Orbital Aerospace Telemetry, Global Research Grants & Swarm Study Pods', self.html_content)
        self.assertIn('Orbital Aerospace Sandbox', self.html_content)
        self.assertIn('Global Research Grants', self.html_content)
        self.assertIn('Swarm Peer Study Pod', self.html_content)
        self.assertIn('calculateSatelliteOrbitSim', self.html_content)
        self.assertIn('evaluateSopSim', self.html_content)
        self.assertIn('runSwarmStudyPodSim', self.html_content)

    def test_edge_robotics_genomics_and_biomedical_present(self):
        """Verify Phase 37: Edge Robotics & Drone Lab, Genomic Bioinformatics & Medical Diagnostics."""
        self.assertIn('content-robotics-genomics-biomedical', self.html_content)
        self.assertIn('Edge Robotics & Drone Lab, Genomic Bioinformatics & Medical Diagnostics', self.html_content)
        self.assertIn('Edge Robotics & Drone Lab', self.html_content)
        self.assertIn('Genomics & CRISPR Lab', self.html_content)
        self.assertIn('Biomedical Diagnostic Lab', self.html_content)
        self.assertIn('simulateDroneFlightSim', self.html_content)
        self.assertIn('alignGenomicSequenceSim', self.html_content)
        self.assertIn('tuneDiagnosticThresholdSim', self.html_content)

    def test_post_quantum_crypto_smart_grid_and_carbon_present(self):
        """Verify Phase 38: Post-Quantum Cryptography, Smart Grid Lab & Carbon Registry."""
        self.assertIn('content-pqc-smartgrid-carbon', self.html_content)
        self.assertIn('Post-Quantum Cryptography, Smart Grid Lab & Carbon Registry', self.html_content)
        self.assertIn('Post-Quantum Cryptography', self.html_content)
        self.assertIn('Smart Renewable Microgrid', self.html_content)
        self.assertIn('Carbon Offset Registry', self.html_content)
        self.assertIn('simulatePqcKeygenSim', self.html_content)
        self.assertIn('simulatePqcEncapSim', self.html_content)
        self.assertIn('simulateSmartGridDispatchSim', self.html_content)
        self.assertIn('mintCarbonCertificateSim', self.html_content)
        self.assertIn('retireCarbonCertificateSim', self.html_content)

    def test_cyber_range_hpc_and_vc_syndicate_present(self):
        """Verify Phase 39: Cyber Range Zero-Trust, HPC Supercomputer Lab & Student VC Syndicate."""
        self.assertIn('content-cyber-hpc-vc', self.html_content)
        self.assertIn('Cyber Range Zero-Trust, HPC Supercomputer Lab & Student VC Syndicate', self.html_content)
        self.assertIn('Zero-Trust Cyber Range', self.html_content)
        self.assertIn('HPC Supercomputer Lab', self.html_content)
        self.assertIn('Student VC Syndicate', self.html_content)
        self.assertIn('simulateZeroTrustEvaluationSim', self.html_content)
        self.assertIn('setCyberPayloadPreset', self.html_content)
        self.assertIn('simulateHpcSpeedupSim', self.html_content)
        self.assertIn('simulateSafeDilutionSim', self.html_content)
        self.assertIn('commitAngelSyndicateSim', self.html_content)

    def test_formal_verification_dag_and_fintech_present(self):
        """Verify Phase 40: Formal Verification Sandbox, Decentralized IPFS DAG & FinTech Quantitative Risk Arena."""
        self.assertIn('content-formal-dag-fintech', self.html_content)
        self.assertIn('Formal Verification Sandbox, Decentralized IPFS DAG & FinTech Quantitative Risk Arena', self.html_content)
        self.assertIn('Formal Verification Sandbox', self.html_content)
        self.assertIn('Decentralized Knowledge DAG', self.html_content)
        self.assertIn('FinTech Quantitative Risk', self.html_content)
        self.assertIn('verifyHoareTripleSim', self.html_content)
        self.assertIn('setFormalPreset', self.html_content)
        self.assertIn('publishDagNodeSim', self.html_content)
        self.assertIn('verifyDagIntegritySim', self.html_content)
        self.assertIn('calculateFintechBlackScholesSim', self.html_content)

    def test_bci_hypothesis_and_logistics_present(self):
        """Verify Phase 41: BCI Cognitive Telemetry, Scientific Hypothesis Discovery & Logistics Operations Sandbox."""
        self.assertIn('content-bci-hypothesis-logistics', self.html_content)
        self.assertIn('BCI Cognitive Telemetry, Scientific Hypothesis Discovery & Logistics Operations Sandbox', self.html_content)
        self.assertIn('BCI Cognitive Telemetry', self.html_content)
        self.assertIn('Scientific Hypothesis Discovery', self.html_content)
        self.assertIn('Logistics Operations Research', self.html_content)
        self.assertIn('decomposeBciEegSim', self.html_content)
        self.assertIn('setBciElectrodePreset', self.html_content)
        self.assertIn('evaluateScientificHypothesisSim', self.html_content)
        self.assertIn('calculateEoqInventorySim', self.html_content)
        self.assertIn('calculateShortestLogisticsRouteSim', self.html_content)

    def test_digital_twin_cfd_and_dao_present(self):
        """Verify Phase 42: Digital Twin Simulation, CFD Flow Sandbox & DAO Governance Protocol."""
        self.assertIn('content-twin-cfd-dao', self.html_content)
        self.assertIn('Digital Twin Simulation, CFD Flow Sandbox & DAO Governance Protocol', self.html_content)
        self.assertIn('Digital Twin Telemetry', self.html_content)
        self.assertIn('Computational Fluid Dynamics', self.html_content)
        self.assertIn('DAO Governance Protocol', self.html_content)
        self.assertIn('simulateDigitalTwinSim', self.html_content)
        self.assertIn('setDigitalTwinPreset', self.html_content)
        self.assertIn('solveCfdSimulationSim', self.html_content)
        self.assertIn('castDaoVoteSim', self.html_content)
        self.assertIn('evaluateDaoOutcomeSim', self.html_content)

    def test_qec_climate_and_swarm_present(self):
        """Verify Phase 43: Quantum Error Correction, Climate Dynamics & Swarm Robotics Arena."""
        self.assertIn('content-qec-climate-swarm', self.html_content)
        self.assertIn('Quantum Error Correction, Climate Dynamics & Swarm Robotics Arena', self.html_content)
        self.assertIn('Quantum Surface Code', self.html_content)
        self.assertIn('Atmospheric Climate Dynamics', self.html_content)
        self.assertIn('Micro-Robotics Swarm', self.html_content)
        self.assertIn('decodeQecSurfaceSim', self.html_content)
        self.assertIn('calculateClimateForcingSim', self.html_content)
        self.assertIn('simulateSwarmStepSim', self.html_content)

    def test_fusion_plasma_snn_and_maritime_present(self):
        """Verify Phase 44: Fusion Tokamak Physics, Neuromorphic SNN & Maritime COLREGs Sandbox."""
        self.assertIn('content-plasma-snn-maritime', self.html_content)
        self.assertIn('Fusion Tokamak Physics, Neuromorphic SNN & Maritime COLREGs Sandbox', self.html_content)
        self.assertIn('Tokamak Fusion Physics', self.html_content)
        self.assertIn('Neuromorphic SNN', self.html_content)
        self.assertIn('Maritime AIS COLREGs', self.html_content)
        self.assertIn('evaluateFusionLawsonSim', self.html_content)
        self.assertIn('simulateLifNeuronSim', self.html_content)
        self.assertIn('calculateStdpPlasticitySim', self.html_content)
        self.assertIn('calculateMaritimeCpaSim', self.html_content)

    def test_metamaterial_ligo_and_crispr_present(self):
        """Verify Phase 45: Nanophotonics Metamaterial, Gravitational LIGO & CRISPR Gene Lab."""
        self.assertIn('content-metamaterial-ligo-crispr', self.html_content)
        self.assertIn('Nanophotonics Metamaterial, Gravitational LIGO & CRISPR Gene Lab', self.html_content)
        self.assertIn('Nanophotonics Metamaterial', self.html_content)
        self.assertIn('Gravitational Wave Interferometry', self.html_content)
        self.assertIn('Synthetic Biology CRISPR-Cas9', self.html_content)
        self.assertIn('calculateMetamaterialDispersionSim', self.html_content)
        self.assertIn('calculateGravitationalChirpSim', self.html_content)
        self.assertIn('evaluateCrisprGrnaSim', self.html_content)
        self.assertIn('calculateCrisprOffTargetSim', self.html_content)

    def test_smr_astrodynamics_and_topological_present(self):
        """Verify Phase 46: Nuclear SMR Reactor, Interplanetary Astrodynamics & Topological Quantum Lab."""
        self.assertIn('content-smr-astrodynamics-topological', self.html_content)
        self.assertIn('Nuclear SMR Reactor, Interplanetary Astrodynamics & Topological Quantum Lab', self.html_content)
        self.assertIn('Nuclear SMR Reactor Kinetics', self.html_content)
        self.assertIn('Interplanetary Astrodynamics', self.html_content)
        self.assertIn('Topological Quantum Studio', self.html_content)
        self.assertIn('simulateSmrTransientSim', self.html_content)
        self.assertIn('calculateLambertTransferSim', self.html_content)
        self.assertIn('calculateGravityAssistSim', self.html_content)
        self.assertIn('evaluateKitaevWireSim', self.html_content)
        self.assertIn('simulateAnyonBraidingSim', self.html_content)

    def test_router_py_contains_zero_non_academic_bengali_strings(self):
        """
        Verify that backend/app/api/v1/router.py contains zero non-academic Bengali strings:
        Bengali characters are strictly confined to question stems, options, and explanations.
        Zero Bengali in any exception details, response messages, status codes, or parameters.
        """
        router_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/api/v1/router.py'))
        with open(router_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        academic_keys = ['"stem_bn"', '"option_text_bn"', '"explanation_bn"']
        for idx, line in enumerate(lines, 1):
            bengali_matches = re.findall(r'[\u0980-\u09FF]+', line)
            if bengali_matches:
                is_academic_content = any(k in line for k in academic_keys)
                self.assertTrue(
                    is_academic_content,
                    f"Forbidden Bengali string found in router.py at line {idx}: {line.strip()}"
                )

if __name__ == '__main__':
    unittest.main()
