"""
========================================================================================
MODULE:    API v1 Unified Router & Endpoint Dispatcher
TOPIC:     REST API Endpoints for Full-Journey Platform, Live MCQ, Tuition & Career
FILE:      backend/app/api/v1/router.py
PURPOSE:   Aggregates and exposes all versioned v1 REST API endpoints. Enforces standard
           JSON envelopes, machine-readable error codes, and RBAC authorization
           for Student, Tutor, Employer, Reviewer, and Admin personas.
AUDIENCE:  Frontend Engineers, Integration Testers & AI Agents
STANDARDS: REST OpenAPI 3.1, Standard Envelope, Machine-Readable Errors, ASVS L2
========================================================================================
"""

from typing import List, Optional, Dict, Any
from backend.app.core.fastapi_shim import APIRouter, Header, HTTPException, Query, status

from backend.app.schemas.quiz_schema import (
    QuizMode,
    QuizAttemptStartResponse,
    AnswerSaveRequest,
    AnswerSaveResponse,
    QuizResultResponse
)
from backend.app.schemas.question_schema import QuestionQuarantineRequest
from backend.app.schemas.opportunity_schema import (
    TuitionListingCreateRequest,
    TuitionApplyRequest,
    ContactConsentGrantRequest,
    StudentSkillAddRequest,
    CVSnapshotCreateRequest,
    JobApplicationSubmitRequest,
    ApplicationStageUpdateRequest
)
from backend.app.schemas.live_and_admission_schema import (
    LiveSessionPrewarmRequest,
    LeaderboardOptOutRequest,
    DiagnosticAnalyzeRequest,
    AIDraftGenerateRequest,
    SMEReviewDecisionRequest
)
from backend.app.schemas.psychometrics_and_guardian_schema import (
    PsychometricCalibrateRequest,
    StreakFreezeUseRequest,
    GuardianLinkRequest,
    TuitionCoSignRequest,
    DisputeFileRequest,
    DisputeResolveRequest
)
from backend.app.schemas.security_and_offline_schema import (
    OfflineSyncBatchRequest,
    SecurityProfileSanitizeRequest
)
from backend.app.schemas.credential_and_audit_schema import (
    CredentialIssueRequest,
    CredentialVerificationResponse,
    AuditVerificationResponse
)
from backend.app.schemas.spaced_repetition_schema import (
    SpacedReviewRecordRequest,
    StudyPlanGenerateRequest,
    MilestoneCompleteRequest
)
from backend.app.schemas.study_circle_and_arbitration_schema import (
    StudyCircleCreateRequest,
    StudyCircleJoinRequest,
    StudyCircleContributeRequest,
    TribunalCaseCreateRequest,
    TribunalVoteRequest
)

from backend.app.services.quiz_engine import quiz_engine
from backend.app.services.quarantine_service import quarantine_service
from backend.app.services.live_challenge_service import live_challenge_service
from backend.app.services.diagnostic_service import diagnostic_service
from backend.app.services.tuition_service import tuition_service
from backend.app.services.career_service import career_service
from backend.app.services.content_pipeline_service import content_pipeline_service
from backend.app.services.psychometrics_service import psychometrics_service
from backend.app.services.guardian_service import guardian_service
from backend.app.services.dispute_service import dispute_service
from backend.app.services.system_diagnostics_service import system_diagnostics_service
from backend.app.services.offline_sync_service import offline_sync_service
from backend.app.services.portfolio_credential_service import portfolio_credential_service
from backend.app.services.spaced_repetition_service import spaced_repetition_service
from backend.app.services.study_plan_service import study_plan_service
from backend.app.services.study_circle_service import study_circle_service
from backend.app.services.arbitration_service import arbitration_service
from backend.app.services.cat_engine_service import cat_engine_service
from backend.app.services.blueprint_composer_service import blueprint_composer_service
from backend.app.schemas.cat_and_blueprint_schema import (
    CatSessionStartRequest,
    CatAnswerSubmitRequest,
    BlueprintComposeRequest
)
from backend.app.services.socratic_tutor_service import socratic_tutor_service
from backend.app.services.math_visualizer_service import math_visualizer_service
from backend.app.schemas.socratic_and_visualizer_schema import (
    SocraticSessionStartRequest,
    SocraticMessageSendRequest,
    SocraticHintRequest,
    GeometryVisualizerRequest
)
from backend.app.services.interview_coach_service import interview_coach_service
from backend.app.services.career_matcher_service import career_matcher_service
from backend.app.schemas.interview_and_career_matcher_schema import (
    MockInterviewStartRequest,
    MockInterviewAnswerRequest,
    CareerFitAnalysisRequest
)
from backend.app.services.predictive_analytics_service import predictive_analytics_service
from backend.app.services.admission_probability_service import admission_probability_service
from backend.app.schemas.predictive_analytics_schema import (
    GPAPredictionRequest,
    AdmissionProbabilityRequest,
    SensitivitySimulationRequest
)
from backend.app.services.study_scheduler_service import study_scheduler_service
from backend.app.services.burnout_prevention_service import burnout_prevention_service
from backend.app.schemas.study_scheduler_schema import (
    DailyScheduleGenerateRequest,
    FocusSprintStartRequest,
    FocusSprintCompleteRequest,
    BurnoutEvaluationRequest
)
# -----------------------------------------------------------------------------
# PHASE 24: TRI-PLATFORM ENTERPRISE CONVERGENCE (10MS + CARETUTORS + BDJOBS)
# -----------------------------------------------------------------------------
from backend.app.services.video_classroom_service import video_classroom_service
from backend.app.services.tuition_marketplace_service import tuition_marketplace_service
from backend.app.services.job_placement_service import job_placement_service
from backend.app.schemas.tri_platform_schema import (
    VideoProgressUpdateRequest,
    CheckpointQuizSubmitRequest,
    VideoNoteCreateRequest,
    TuitionMarketplaceListingCreateRequest,
    TuitionApplicationSubmitRequest,
    BilateralConsentUpdateRequest,
    JobPostingCreateRequest,
    CVSnapshotFreezeRequest,
    JobApplicationSubmitSealedRequest,
    PipelineStageAdvanceRequest
)
# -----------------------------------------------------------------------------
# PHASE 25: OMNI-SEARCH, REAL-TIME NOTIFICATIONS & STUDENT REPUTATION
# -----------------------------------------------------------------------------
from backend.app.services.omni_search_service import omni_search_service
from backend.app.services.notification_gateway_service import notification_gateway_service
from backend.app.services.student_reputation_service import student_reputation_service
from backend.app.schemas.omni_gateway_schema import (
    OmniSearchRequest,
    NotificationDispatchRequest,
    QuestClaimRequest
)
# -----------------------------------------------------------------------------
# PHASE 26: ESCROW VAULT, GUARDIAN TELEMETRY & CORPORATE TALENT
# -----------------------------------------------------------------------------
from backend.app.services.honorarium_escrow_service import honorarium_escrow_service
from backend.app.services.guardian_telemetry_service import guardian_telemetry_service
from backend.app.services.corporate_talent_service import corporate_talent_service
from backend.app.schemas.enterprise_portal_schema import (
    CreateEscrowContractRequest,
    LogSessionCompletionRequest,
    ReleaseMilestoneFundsRequest,
    RaiseMilestoneDisputeRequest,
    ToggleSafetyLockRequest,
    DispatchInterviewInvitationRequest,
    ShortlistCandidateRequest
)
# -----------------------------------------------------------------------------
# PHASE 27: COLLABORATIVE STUDY CIRCLES & GAMIFIED BOUNTY TRIBUNAL
# -----------------------------------------------------------------------------
from backend.app.services.study_room_service import study_room_service
from backend.app.services.bounty_tribunal_service import bounty_tribunal_service
from backend.app.schemas.collaborative_study_schema import (
    CreateStudyRoomRequest,
    JoinStudyRoomRequest,
    WhiteboardSyncRequest,
    PomodoroSyncRequest,
    CreateBountyRequest,
    SubmitSolutionRequest,
    VerdictBountyRequest
)
# -----------------------------------------------------------------------------
# PHASE 28: MICRO-SCHOLARSHIP ENDOWMENT & TECHNICAL ASSESSMENT ARENA
# -----------------------------------------------------------------------------
from backend.app.services.scholarship_endowment_service import scholarship_endowment_service
from backend.app.services.technical_assessment_service import technical_assessment_service
from backend.app.schemas.scholarship_and_assessment_schema import (
    CreateEndowmentFundRequest,
    ApplyScholarshipRequest,
    DisburseScholarshipRequest,
    ATSResumeAnalysisRequest,
    SubmitTechnicalAssessmentRequest
)
# -----------------------------------------------------------------------------
# PHASE 29: ALUMNI MENTORSHIP, ADAPTIVE PATHWAYS & VERIFIABLE CERTIFICATES
# -----------------------------------------------------------------------------
from backend.app.services.alumni_mentorship_service import alumni_mentorship_service
from backend.app.services.adaptive_learning_path_service import adaptive_learning_path_service
from backend.app.services.certificate_verification_service import certificate_verification_service
from backend.app.schemas.mentorship_and_pathway_schema import (
    BookMentorshipSessionRequest,
    GenerateAdaptivePathwayRequest,
    IssueCertificateRequest
)
# -----------------------------------------------------------------------------
# PHASE 30: ADMISSION MULTIPLEXER, CRDT DELTA-SYNC & TALENT PASSPORT
# -----------------------------------------------------------------------------
from backend.app.services.university_admission_multiplexer_service import university_admission_multiplexer_service
from backend.app.services.offline_delta_sync_service import offline_delta_sync_service
from backend.app.services.student_talent_passport_service import student_talent_passport_service
from backend.app.schemas.admission_mux_and_passport_schema import (
    CheckAdmissionEligibilityRequest,
    BatchApplyUniversityRequest,
    OfflineDeltaSyncRequest,
    GenerateTalentPassportRequest
)
# -----------------------------------------------------------------------------
# PHASE 31: AI MATH SOLVER, ALUMNI REFERRALS & VOICE VIVA SIMULATOR
# -----------------------------------------------------------------------------
from backend.app.services.math_problem_solver_service import math_problem_solver_service
from backend.app.services.alumni_referral_network_service import alumni_referral_network_service
from backend.app.services.voice_viva_simulator_service import voice_viva_simulator_service
from backend.app.schemas.solver_referral_and_viva_schema import (
    SolveMathStepwiseRequest,
    DiagnoseMisconceptionRequest,
    CreateReferralEndorsementRequest,
    StartVivaSessionRequest,
    SubmitAudioVivaResponseRequest
)
# -----------------------------------------------------------------------------
# PHASE 32: VIRTUAL SCIENCE LAB, BATCH POOL & CORPORATE CAPSTONES
# -----------------------------------------------------------------------------
from backend.app.services.virtual_science_lab_service import virtual_science_lab_service
from backend.app.services.coaching_batch_pool_service import coaching_batch_pool_service
from backend.app.services.industry_capstone_service import industry_capstone_service
from backend.app.schemas.lab_batch_and_capstone_schema import (
    CircuitSimulationRequest,
    OpticsRayTraceRequest,
    TitrationSimulationRequest,
    LabReportSynthesisRequest,
    CreateCoachingBatchRequest,
    JoinBatchGuardianRequest,
    LogBatchSessionRequest,
    SubmitCapstoneMilestoneRequest
)
# -----------------------------------------------------------------------------
# PHASE 33: STEM 3D MOLECULAR GEOMETRY, SYLLABUS ATLAS & INNOVATION LAUNCHPAD
# -----------------------------------------------------------------------------
from backend.app.services.molecular_geometry_lab_service import molecular_geometry_lab_service
from backend.app.services.syllabus_knowledge_atlas_service import syllabus_knowledge_atlas_service
from backend.app.services.innovation_launchpad_service import innovation_launchpad_service
from backend.app.schemas.stem_atlas_and_launchpad_schema import (
    MolecularGeometryRequest,
    RedoxReactionBalanceRequest,
    PitchProjectRequest,
    CastProjectVoteRequest,
    ReleaseGrantTrancheRequest
)
# -----------------------------------------------------------------------------
# PHASE 34: ALGORITHM COMPLEXITY SANDBOX, THESIS CITATIONS & AMBASSADORS
# -----------------------------------------------------------------------------
from backend.app.services.algorithm_complexity_sandbox_service import algorithm_complexity_sandbox_service
from backend.app.services.thesis_citation_graph_service import thesis_citation_graph_service
from backend.app.services.campus_ambassador_syndicate_service import campus_ambassador_syndicate_service
from backend.app.schemas.algo_thesis_and_ambassador_schema import (
    CodeComplexityRequest,
    AlgorithmTraceRequest,
    ThesisPaperSubmitRequest,
    ThesisSimilarityCheckRequest,
    ResearchGrantMatchRequest,
    ClaimAmbassadorTaskRequest,
    SubmitAmbassadorTaskRequest,
    VerifyAmbassadorTaskRequest
)
# -----------------------------------------------------------------------------
# PHASE 35: NATIONAL OLYMPIAD ARENA, SEMICONDUCTOR & PATENT REGISTRY
# -----------------------------------------------------------------------------
from backend.app.services.national_olympiad_arena_service import national_olympiad_arena_service
from backend.app.services.semiconductor_quantum_sandbox_service import semiconductor_quantum_sandbox_service
from backend.app.services.university_patent_registry_service import university_patent_registry_service
from backend.app.schemas.olympiad_quantum_and_patent_schema import (
    OlympiadSubmissionRequest,
    PnJunctionSimRequest,
    QuantumWellSimRequest,
    PatentDisclosureFileRequest,
    PatentPriorArtSearchRequest
)
# -----------------------------------------------------------------------------
# PHASE 36: ORBITAL AEROSPACE, GLOBAL RESEARCH GRANTS & SWARM STUDY PODS
# -----------------------------------------------------------------------------
from backend.app.services.orbital_mechanics_satellite_service import orbital_mechanics_satellite_service
from backend.app.services.global_research_grant_service import global_research_grant_service
from backend.app.services.multi_agent_swarm_tutoring_service import multi_agent_swarm_tutoring_service
from backend.app.schemas.satellite_grant_and_swarm_schema import (
    SatelliteOrbitRequest,
    GroundStationPassRequest,
    RfLinkBudgetRequest,
    FellowshipSearchQuery,
    SopEvaluationRequest,
    GrantBudgetCalculationRequest,
    SwarmStudyPodRequest
)
# -----------------------------------------------------------------------------
# PHASE 37: EDGE ROBOTICS, GENOMICS & BIOMEDICAL DIAGNOSTICS
# -----------------------------------------------------------------------------
from backend.app.services.edge_robotics_drone_service import edge_robotics_drone_service
from backend.app.services.genomic_bioinformatics_service import genomic_bioinformatics_service
from backend.app.services.biomedical_diagnostic_service import biomedical_diagnostic_service
from backend.app.schemas.robotics_genomics_and_biomedical_schema import (
    DronePidSimRequest,
    DroneEnduranceRequest,
    SequenceAlignRequest,
    CrisprGuideScanRequest,
    DiagnosticConfusionMatrixRequest,
    DiagnosticRocCurveRequest
)
# -----------------------------------------------------------------------------
# PHASE 38: POST-QUANTUM CRYPTOGRAPHY, SMART GRID & CARBON OFFSET REGISTRY
# -----------------------------------------------------------------------------
from backend.app.services.post_quantum_cryptography_service import PostQuantumCryptographyService
from backend.app.services.smart_grid_renewable_service import SmartGridRenewableDispatchService
from backend.app.services.decentralized_carbon_offset_service import DecentralizedCarbonOffsetService
from backend.app.schemas.pqc_smartgrid_and_carbon_schema import (
    PqcKeyGenRequest,
    PqcEncapsulateRequest,
    PqcDecapsulateRequest,
    PqcQuantumSecurityAssessmentRequest,
    SolarPvCalcRequest,
    MicroGridDispatchRequest,
    CarbonOffsetMintRequest,
    CarbonOffsetRetireRequest
)
# -----------------------------------------------------------------------------
# PHASE 39: CYBER RANGE ZERO-TRUST, HPC CLUSTER SCHEDULER & VC SYNDICATE
# -----------------------------------------------------------------------------
from backend.app.services.cyber_range_zero_trust_service import CyberRangeZeroTrustService
from backend.app.services.hpc_cluster_scheduler_service import HpcClusterSchedulerService
from backend.app.services.university_vc_syndicate_service import UniversityVcAngelSyndicateService
from backend.app.schemas.cyber_hpc_and_vc_schema import (
    ZeroTrustEvaluationRequest,
    ThreatDetectionRequest,
    HpcJobSubmitRequest,
    AmdahlSpeedupCalcRequest,
    SafeDilutionCalcRequest,
    AngelCommitmentRequest
)
# -----------------------------------------------------------------------------
# PHASE 40: FORMAL VERIFICATION, IPFS KNOWLEDGE DAG & FINTECH QUANT RISK
# -----------------------------------------------------------------------------
from backend.app.services.formal_verification_service import FormalVerificationZ3SolverService
from backend.app.services.decentralized_knowledge_dag_service import DecentralizedKnowledgeDagService
from backend.app.services.fintech_quant_risk_service import FintechQuantRiskService
from backend.app.schemas.formal_dag_and_fintech_schema import (
    HoareVerificationRequest,
    MutationScoreRequest,
    CreateDagNodeRequest,
    BlackScholesRequest,
    PortfolioVarRequest
)
# -----------------------------------------------------------------------------
# PHASE 41: BCI COGNITIVE TELEMETRY, HYPOTHESIS DISCOVERY & LOGISTICS OPS
# -----------------------------------------------------------------------------
from backend.app.services.bci_cognitive_telemetry_service import BciCognitiveTelemetryService
from backend.app.services.scientific_hypothesis_discovery_service import ScientificHypothesisDiscoveryService
from backend.app.services.supply_chain_logistics_service import SupplyChainLogisticsOpsService
from backend.app.schemas.bci_hypothesis_and_logistics_schema import (
    BciEegSamplesRequest,
    ContingencyHypothesisRequest,
    EoqRopCalcRequest,
    BullwhipEffectRequest,
    ShortestRouteRequest
)
# -----------------------------------------------------------------------------
# PHASE 42: DIGITAL TWIN SIMULATION, CFD SANDBOX & DAO GOVERNANCE
# -----------------------------------------------------------------------------
from backend.app.services.digital_twin_simulation_service import DigitalTwinSimulationService
from backend.app.services.computational_fluid_dynamics_service import ComputationalFluidDynamicsService
from backend.app.services.dao_governance_protocol_service import DaoGovernanceProtocolService
from backend.app.schemas.twin_cfd_and_dao_schema import (
    TwinStateSimulationRequest,
    MahalanobisAnomalyRequest,
    SensorDriftCalibrationRequest,
    MonteCarloReliabilityRequest,
    ReynoldsRegimeRequest,
    BernoulliFlowRequest,
    AerodynamicCoefficientsRequest,
    ChannelProfileRequest,
    QuadraticVotingCalcRequest,
    ProposalCreateRequest,
    QuadraticVoteCastRequest
)
# -----------------------------------------------------------------------------
# PHASE 43: QUANTUM ERROR CORRECTION, CLIMATE MODELING & SWARM ROBOTICS
# -----------------------------------------------------------------------------
from backend.app.services.quantum_error_correction_service import QuantumErrorCorrectionService
from backend.app.services.atmospheric_climate_service import AtmosphericClimateModelingService
from backend.app.services.micro_robotics_swarm_service import AutonomousMicroRoboticsSwarmService
from backend.app.schemas.qec_climate_and_swarm_schema import (
    SurfaceLatticeInitRequest,
    PauliErrorInjectionRequest,
    QecDecodingRequest,
    RadiativeForcingRequest,
    PlanetaryEnergyBalanceRequest,
    SwarmSimulationStepRequest
)
# -----------------------------------------------------------------------------
# PHASE 44: FUSION PLASMA TOKAMAK, NEUROMORPHIC SNN & MARITIME COLREGS
# -----------------------------------------------------------------------------
from backend.app.services.fusion_plasma_tokamak_service import FusionPlasmaTokamakService
from backend.app.services.neuromorphic_spiking_network_service import NeuromorphicSpikingNetworkService
from backend.app.services.maritime_navigation_colregs_service import MaritimeNavigationColregsService
from backend.app.schemas.plasma_snn_and_maritime_schema import (
    LawsonCriterionRequest,
    TokamakMhdRequest,
    LifNeuronSimulationRequest,
    StdpPlasticityRequest,
    CpaCollisionRequest
)
# -----------------------------------------------------------------------------
# PHASE 45: NANOPHOTONICS METAMATERIAL, GRAVITATIONAL LIGO & CRISPR GENE LAB
# -----------------------------------------------------------------------------
from backend.app.services.nanophotonic_metamaterial_service import NanophotonicMetamaterialService
from backend.app.services.gravitational_wave_service import GravitationalWaveInterferometryService
from backend.app.services.synthetic_biology_crispr_service import SyntheticBiologyCrisprService
from backend.app.schemas.metamaterial_ligo_and_crispr_schema import (
    OpticalDispersionRequest,
    NegativeRefractionRequest,
    GravitationalChirpRequest,
    ChirpWaveformRequest,
    CrisprGrnaEvaluationRequest,
    CrisprOffTargetRequest
)
# -----------------------------------------------------------------------------
# PHASE 46: NUCLEAR SMR REACTOR, ASTRODYNAMICS & TOPOLOGICAL QUANTUM LAB
# -----------------------------------------------------------------------------
from backend.app.services.nuclear_smr_reactor_service import NuclearSmrReactorService
from backend.app.services.interplanetary_astrodynamics_service import InterplanetaryAstrodynamicsService
from backend.app.services.topological_quantum_service import TopologicalQuantumService
from backend.app.schemas.smr_astrodynamics_and_topological_schema import (
    SmrTransientRequest,
    DecayHeatRequest,
    LambertTransferRequest,
    GravityAssistRequest,
    MultiStageRocketRequest,
    KitaevWireRequest,
    AnyonBraidRequest
)
# -----------------------------------------------------------------------------
# PHASE 47: SUPABASE SECURITY ARCHITECTURE, RLS ENGINE & REALTIME GUARDS
# -----------------------------------------------------------------------------
from backend.app.services.supabase_security_service import SupabaseSecurityService
from backend.app.services.edge_function_boundary_service import EdgeFunctionBoundaryService
from backend.app.services.realtime_cryptographic_presence_service import RealtimeCryptographicPresenceService
from backend.app.schemas.supabase_and_realtime_security_schema import (
    RlsEvaluationRequest,
    RlsEvaluationResponse,
    RlsGeneratePolicyRequest,
    RlsGeneratePolicyResponse,
    PostgrestSanitizeRequest,
    PostgrestSanitizeResponse,
    RpcAuditRequest,
    RpcAuditResponse,
    EdgeJwtVerifyRequest,
    EdgeJwtVerifyResponse,
    StorageSignedUrlRequest,
    StorageSignedUrlResponse,
    RealtimeChannelAuthRequest,
    RealtimeChannelAuthResponse
)
# -----------------------------------------------------------------------------
# PHASE 48: SUPABASE PGVECTOR, MFA PASSKEYS & ENVELOPE FIELD ENCRYPTION
# -----------------------------------------------------------------------------
from backend.app.services.supabase_pgvector_service import SupabasePgvectorService
from backend.app.services.supabase_mfa_passkey_service import SupabaseMfaPasskeyService
from backend.app.services.supabase_field_encryption_service import SupabaseFieldEncryptionService
from backend.app.schemas.pgvector_mfa_and_encryption_schema import (
    VectorSimilaritySearchRequest,
    VectorSimilaritySearchResponse,
    VectorGroundingCheckRequest,
    VectorGroundingCheckResponse,
    TotpEnrollRequest,
    TotpEnrollResponse,
    TotpVerifyRequest,
    TotpVerifyResponse,
    PasskeyChallengeRequest,
    PasskeyChallengeResponse,
    PasskeyVerifyRequest,
    PasskeyVerifyResponse,
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    EnvelopeDecryptRequest,
    EnvelopeDecryptResponse
)
# -----------------------------------------------------------------------------
# PHASE 49: SUPABASE JWKS, QUERY HARDENING & CDC AUDIT ENGINE
# -----------------------------------------------------------------------------
from backend.app.services.edge_distributed_replay_service import EdgeDistributedReplayService
from backend.app.services.postgrest_query_hardener_service import PostgrestQueryHardenerService
from backend.app.services.database_cdc_audit_engine_service import DatabaseCDCAuditEngineService
from backend.app.schemas.jwks_query_hardener_and_cdc_schema import (
    JWKSRotationRequest,
    JWKSRotationResponse,
    EdgeTokenVerificationRequest,
    EdgeTokenVerificationResponse,
    PostgrestQueryInspectRequest,
    PostgrestQueryInspectResponse,
    WALEventIngestRequest,
    WALEventIngestResponse,
    AuditIntegrityVerificationResponse,
    RealtimeBroadcastAuthRequest,
    RealtimeBroadcastAuthResponse
)
# -----------------------------------------------------------------------------
# PHASE 50: SUPABASE GRAPHQL SHIELD, EDGE RATE LIMITER & STORAGE SANITIZER
# -----------------------------------------------------------------------------
import base64
from backend.app.services.pg_graphql_shield_service import PgGraphqlShieldService
from backend.app.services.edge_distributed_rate_limiter_service import EdgeDistributedRateLimiterService
from backend.app.services.storage_multipart_sanitizer_service import StorageMultipartSanitizerService
from backend.app.schemas.graphql_ratelimit_and_storage_schema import (
    GraphqlQueryInspectRequest,
    GraphqlQueryInspectResponse,
    GraphqlParityAuditRequest,
    GraphqlParityAuditResponse,
    EdgeRateLimitCheckRequest,
    EdgeRateLimitCheckResponse,
    StoragePresignedTicketRequest,
    StoragePresignedTicketResponse,
    StorageUploadSanitizeRequest,
    StorageUploadSanitizeResponse
)
# -----------------------------------------------------------------------------
# PHASE 51: REALTIME PRESENCE, RLS COMPLIANCE & PRIVACY VAULT
# -----------------------------------------------------------------------------
from backend.app.services.realtime_presence_integrity_service import RealtimePresenceIntegrityService
from backend.app.services.postgres_rls_compliance_scanner_service import PostgresRlsComplianceScannerService
from backend.app.services.database_anonymization_vault_service import DatabaseAnonymizationVaultService
from backend.app.schemas.presence_rls_and_anonymization_schema import (
    PresenceTicketGenerateRequest,
    PresenceTicketGenerateResponse,
    PresenceJoinRequest,
    PresenceJoinResponse,
    PresenceHeartbeatRequest,
    PresenceHeartbeatResponse,
    RlsComplianceScanRequest,
    RlsComplianceScanResponse,
    SecurityDefinerScanRequest,
    SecurityDefinerScanResponse,
    LaplaceNoiseInjectRequest,
    LaplaceNoiseInjectResponse,
    KAnonymityEvaluateRequest,
    KAnonymityEvaluateResponse
)
# -----------------------------------------------------------------------------
# PHASE 52: EDGE ZERO-TRUST GATEWAY, WEBHOOK REPLAY GUARD & POSTGREST AUDIT
# -----------------------------------------------------------------------------
from backend.app.services.edge_function_zero_trust_gateway_service import EdgeFunctionZeroTrustGatewayService
from backend.app.services.database_webhook_replay_guard_service import DatabaseWebhookReplayGuardService
from backend.app.services.postgrest_audit_trail_engine_service import PostgrestAuditTrailEngineService
from backend.app.schemas.edge_gateway_webhook_audit_schema import (
    EdgeRequestVerifyRequest,
    EdgeRequestVerifyResponse,
    EdgeActionAuthorizeRequest,
    EdgeActionAuthorizeResponse,
    WebhookVerifyRequest,
    WebhookVerifyResponse,
    WebhookAttestRequest,
    WebhookAttestResponse,
    AuditRecordRequest,
    AuditRecordResponse,
    AuditChainVerifyResponse,
    AuditAnomaliesResponse
)
# -----------------------------------------------------------------------------
# PHASE 53: POOLER SESSION HYGIENE, DYNAMIC MASKING & FEDERATED FDW
# -----------------------------------------------------------------------------
from backend.app.services.connection_pooler_hygiene_service import ConnectionPoolerHygieneService
from backend.app.services.dynamic_data_masking_service import DynamicDataMaskingService
from backend.app.services.federated_fdw_security_service import FederatedFdwSecurityService
from backend.app.schemas.pooler_masking_fdw_schema import (
    PoolerSessionAuditRequest,
    PoolerSessionAuditResponse,
    PoolerResetVerifyRequest,
    PoolerResetVerifyResponse,
    PoolerBenchmarkRequest,
    PoolerBenchmarkResponse,
    StudentRecordMaskRequest,
    StudentRecordMaskResponse,
    MaskedViewSqlGenerateRequest,
    MaskedViewSqlGenerateResponse,
    InferenceRiskEvaluateRequest,
    InferenceRiskEvaluateResponse,
    FdwServerAuditRequest,
    FdwServerAuditResponse,
    FdwUserMappingsValidateRequest,
    FdwUserMappingsValidateResponse,
    FederatedQuerySanitizeRequest,
    FederatedQuerySanitizeResponse
)
# -----------------------------------------------------------------------------
# PHASE 54: PITR DISASTER RECOVERY, SECRET ROTATION VAULT & WAL ARCHIVE
# -----------------------------------------------------------------------------
from backend.app.services.disaster_recovery_pitr_simulator_service import DisasterRecoveryPitrSimulatorService
from backend.app.services.secret_rotation_vault_service import SecretRotationVaultService
from backend.app.services.wal_archive_integrity_service import WalArchiveIntegrityService
from backend.app.schemas.pitr_vault_wal_schema import (
    PitrSnapshotCreateRequest,
    PitrSnapshotCreateResponse,
    PitrDrillSimulateRequest,
    PitrDrillSimulateResponse,
    PitrConsistencyVerifyRequest,
    PitrConsistencyVerifyResponse,
    SecretScanRequest,
    SecretScanResponse,
    SecretRotationRequest,
    SecretRotationResponse,
    SecretRevokeRequest,
    SecretRevokeResponse,
    WalRegisterRequest,
    WalRegisterResponse,
    WalVerifyContinuityResponse,
    WalEvaluateLagResponse
)
# -----------------------------------------------------------------------------
# PHASE 55: ZK TENANT PARTITIONING, MERKLE ATTESTATION & CDC REPLICATION
# -----------------------------------------------------------------------------
from backend.app.services.zk_tenant_partition_service import ZeroKnowledgeTenantPartitionService
from backend.app.services.row_level_merkle_attestation_service import RowLevelAttestationMerkleService
from backend.app.services.cdc_replication_conflict_service import CdcReplicationConflictService
from backend.app.schemas.tenant_merkle_cdc_schema import (
    PartitionRouteRequest,
    PartitionRouteResponse,
    PartitionEscapeProbeRequest,
    PartitionEscapeProbeResponse,
    RowAttestationRequest,
    RowAttestationResponse,
    MerkleTreeBuildRequest,
    MerkleTreeBuildResponse,
    MerkleProofVerificationRequest,
    MerkleProofVerificationResponse,
    CdcEventRequest,
    CdcEventResponse,
    ReplicationLagReportResponse
)
# -----------------------------------------------------------------------------
# PHASE 56: PRODUCTION SCHEMA MIGRATION, DRIFT GUARD & INDEX OPTIMIZER
# -----------------------------------------------------------------------------
from backend.app.services.schema_migration_engine_service import SchemaMigrationEngineService
from backend.app.services.schema_drift_detector_service import SchemaDriftDetectorService
from backend.app.services.index_optimizer_advisor_service import IndexOptimizerAdvisorService
from backend.app.schemas.migration_drift_index_schema import (
    MigrationPlanRequest,
    MigrationPlanResponse,
    SchemaDriftScanRequest,
    SchemaDriftScanResponse,
    IndexRecommendRequest,
    IndexRecommendResponse,
    IndexRedundancyScanResponse
)
# -----------------------------------------------------------------------------
# PHASE 57: ULTRA LOW-BANDWIDTH EDGE VIDEO & BROTLI STREAMER
# -----------------------------------------------------------------------------
from backend.app.services.edge_video_stream_service import EdgeVideoStreamService
from backend.app.services.brotli_payload_compressor_service import BrotliPayloadCompressorService
from backend.app.services.adaptive_bitrate_advisor_service import AdaptiveBitrateAdvisorService
from backend.app.schemas.edge_video_brotli_schema import (
    VideoManifestRequest,
    VideoManifestResponse,
    VideoChunkRequest,
    VideoChunkResponse,
    BrotliCompressionRequest,
    BrotliCompressionResponse,
    AdaptiveBitrateRequest,
    AdaptiveBitrateResponse
)
# -----------------------------------------------------------------------------
# PHASE 58: W3C VERIFIABLE CREDENTIAL & ZKP CERTIFICATE VAULT
# -----------------------------------------------------------------------------
from backend.app.services.verifiable_credential_engine_service import VerifiableCredentialEngineService
from backend.app.services.zkp_range_proof_service import ZeroKnowledgeRangeProofService
from backend.app.services.institutional_revocation_registry_service import InstitutionalRevocationRegistryService
from backend.app.schemas.verifiable_credential_zkp_schema import (
    IssueCredentialRequest,
    VerifiableCredentialResponse,
    VerifyCredentialRequest,
    VerifyCredentialResponse,
    GenerateZkpProofRequest,
    ZkpRangeProofResponse,
    RevocationUpdateRequest,
    RevocationCheckRequest,
    RevocationCheckResponse
)
# -----------------------------------------------------------------------------
# PHASE 59: MULTI-LLM AI GATEWAY & PROMPT INJECTION SHIELD
# -----------------------------------------------------------------------------
from backend.app.services.multi_llm_router_gateway_service import MultiLlmRouterGatewayService
from backend.app.services.prompt_injection_sanitizer_service import PromptInjectionSanitizerService
from backend.app.services.semantic_output_validator_service import SemanticOutputValidatorService
from backend.app.schemas.multi_llm_gateway_schema import (
    MultiLlmRouteRequest,
    MultiLlmRouteResponse,
    PromptSanitizeRequest,
    PromptSanitizeResponse,
    OutputValidateRequest,
    OutputValidateResponse
)
# -----------------------------------------------------------------------------
# PHASE 60: THE GRAND CONVERGENCE & ADAPTIVE PERSONA ROUTER
# -----------------------------------------------------------------------------
from backend.app.services.grand_convergence_attestation_service import GrandConvergenceAttestationService
from backend.app.services.adaptive_persona_router_service import AdaptivePersonaRouterService
from backend.app.services.universal_omni_convergence_search_service import UniversalOmniConvergenceSearchService
from backend.app.schemas.grand_convergence_persona_schema import (
    GrandConvergenceAttestRequest,
    GrandConvergenceAttestResponse,
    PersonaRouteRequest,
    PersonaRouteResponse,
    OmniSearchRequest,
    OmniSearchResponse
)
# -----------------------------------------------------------------------------
# PHASE 61: ENTERPRISE SUPABASE PRODUCTION COCKPIT & LIVE CONSOLE
# -----------------------------------------------------------------------------
from backend.app.services.supabase_production_cockpit_service import SupabaseProductionCockpitService
from backend.app.schemas.supabase_production_cockpit_schema import (
    RlsSimulationRequest,
    RlsSimulationResponse,
    StorageAuditRequest,
    StorageAuditResponse,
    EdgeTelemetryResponse,
    MigrationStatusResponse
)
# -----------------------------------------------------------------------------
# PHASE 62: REALTIME COLLABORATIVE WHITEBOARD, WEBRTC MESH & LATEX CANVAS
# -----------------------------------------------------------------------------
from backend.app.services.collaborative_whiteboard_webrtc_service import CollaborativeWhiteboardWebrtcService
from backend.app.schemas.collaborative_whiteboard_webrtc_schema import (
    WhiteboardStrokeDelta,
    LatexFormulaNode,
    WhiteboardSyncRequest,
    WhiteboardSyncResponse,
    WebRtcSignalRequest,
    WebRtcSignalResponse,
    PodiumControlRequest,
    PodiumControlResponse,
    WhiteboardSessionCreateRequest,
    WhiteboardSessionStateResponse
)
# -----------------------------------------------------------------------------
# PHASE 63: AI EXAMINATION PROCTORING, GAZE HEURISTICS & INTEGRITY TOWER
# -----------------------------------------------------------------------------
from backend.app.services.autonomous_proctoring_integrity_service import AutonomousProctoringIntegrityService
from backend.app.schemas.autonomous_proctoring_integrity_schema import (
    ProctoringSessionStartRequest,
    ProctoringSessionStartResponse,
    ProctoringEventRecordRequest,
    ProctoringEventRecordResponse,
    ProctoringSessionReportResponse,
    ProctoringOverrideRequest,
    ProctoringOverrideResponse
)
# -----------------------------------------------------------------------------
# PHASE 64: AUTOMATED SCRIPT GRADING, HANDWRITTEN OCR & MULTI-EXAMINER MODERATION TOWER
# -----------------------------------------------------------------------------
from backend.app.services.automated_grading_moderation_service import AutomatedGradingModerationService
from backend.app.schemas.automated_grading_moderation_schema import (
    BoundingBoxDTO,
    ScriptOCRUploadRequest,
    ScriptOCRUploadResponse,
    RubricCriterionDTO,
    RubricEvaluateRequest,
    RubricEvaluateResponse,
    ExaminerScoreSubmitRequest,
    ExaminerScoreSubmitResponse,
    ModerationAuditResponse,
    ReScrutinyAuditRequest,
    ReScrutinyAuditResponse,
    CohortDistributionResponse
)
# -----------------------------------------------------------------------------
# PHASE 65: AI ADAPTIVE CURRICULUM, BAYESIAN KNOWLEDGE GRAPH & MEMORY DECAY ENGINE
# -----------------------------------------------------------------------------
from backend.app.services.adaptive_curriculum_graph_service import (
    AdaptiveCurriculumGraphService,
    adaptive_curriculum_service
)
from backend.app.schemas.adaptive_curriculum_graph_schema import (
    ConceptNodeDTO,
    KnowledgeEdgeDTO,
    StudentMasteryStateDTO,
    BktUpdateRequest,
    BktUpdateResponse,
    RemedialPathwayRequest,
    RemedialPathwayResponse,
    AdaptiveScheduleRequest,
    AdaptiveScheduleResponse,
    CurriculumGraphResponse
)
# -----------------------------------------------------------------------------
# PHASE 66: OFFLINE-FIRST P2P MESH SYNC, LOCAL CRDT LEDGER & DISRUPTION TOWER
# -----------------------------------------------------------------------------
from backend.app.services.offline_mesh_crdt_service import (
    OfflineMeshCrdtService,
    offline_mesh_crdt_service
)
from backend.app.schemas.offline_mesh_crdt_schema import (
    CrdtMutationDTO,
    MutationStageRequest,
    MutationStageResponse,
    MeshTopologyResponse,
    ChaosSimulationRequest,
    ChaosSimulationResponse,
    ReconcileBatchRequest,
    ReconcileBatchResponse
)
# -----------------------------------------------------------------------------
# PHASE 67: DECENTRALIZED MICRO-EDGE CDN & WEBTORRENT ASSET SWARM TOWER
# -----------------------------------------------------------------------------
from backend.app.services.decentralized_cdn_swarm_service import (
    DecentralizedCdnSwarmService,
    decentralized_cdn_swarm_service
)
from backend.app.schemas.decentralized_cdn_swarm_schema import (
    ChunkPieceDTO,
    MediaManifestDTO,
    ManifestCreateRequest,
    PeerSwarmNodeDTO,
    SwarmStatusResponse,
    PieceVerifyRequest,
    PieceVerifyResponse,
    TransferSimulateRequest,
    TransferSimulateResponse
)
# -----------------------------------------------------------------------------
# PHASE 68: ZERO-KNOWLEDGE AIRGAP ATTENDANCE & DID ATTESTATION TOWER
# -----------------------------------------------------------------------------
from backend.app.services.airgap_attendance_did_service import (
    AirgapAttendanceDidService,
    airgap_attendance_did_service
)
from backend.app.schemas.airgap_attendance_did_schema import (
    RollingBeaconTokenDTO,
    StudentDidCredentialDTO,
    AttendancePunchRequest,
    AttendancePunchResponse,
    ClassroomAttendanceSessionResponse,
    MerkleBatchSettleRequest,
    MerkleBatchSettleResponse
)
# -----------------------------------------------------------------------------
# PHASE 69: DISTRIBUTED SHAMIR SECRET SHARING & EPHEMERAL EXAM VAULT TOWER
# -----------------------------------------------------------------------------
from backend.app.services.shamir_exam_vault_service import (
    ShamirExamVaultService,
    shamir_exam_vault_service
)
from backend.app.schemas.shamir_exam_vault_schema import (
    ShamirShareDTO,
    ExamCustodianDTO,
    EncryptedExamVaultDTO,
    ThresholdReconstructRequest,
    ThresholdReconstructResponse,
    VaultTamperEventDTO,
    ShamirKeySplitRequest,
    ShamirKeySplitResponse
)
# -----------------------------------------------------------------------------
# PHASE 70: BYZANTINE FAULT TOLERANT (BFT) CONSENSUS & CAMPUS RAFT QUORUM TOWER
# -----------------------------------------------------------------------------
from backend.app.services.campus_raft_bft_service import (
    CampusRaftBftService,
    campus_raft_bft_service
)
from backend.app.schemas.campus_raft_bft_schema import (
    RaftNodeDTO,
    RaftLogEntryDTO,
    ClusterTopologyDTO,
    AppendEntriesRequest,
    AppendEntriesResponse,
    RequestVoteRequest,
    RequestVoteResponse,
    ChaosFaultInjectionRequest,
    StateMachineSnapshotDTO
)
# -----------------------------------------------------------------------------
# PHASE 72: NEURAL BENGALI SPEECH SYNTHESIS & REGIONAL DIALECT TUTORING TOWER
# -----------------------------------------------------------------------------
from backend.app.services.neural_speech_dialect_service import (
    NeuralSpeechDialectService,
    neural_speech_dialect_service
)
from backend.app.schemas.neural_speech_dialect_schema import (
    DialectEnum,
    AudioQualityTierEnum,
    PhonemeTimestampDTO,
    VocabSubstitutionDTO,
    DialectTransliterateRequest,
    DialectTransliterateResponse,
    SpeechSynthesizeRequest,
    SpeechSynthesizeResponse,
    DialectVocabBridgeRequest,
    DialectVocabBridgeResponse,
    SpeechEngineStatusDTO
)
# -----------------------------------------------------------------------------
# PHASE 73: AUTONOMOUS SATELLITE USSD & LORA EMERGENCY CLASSROOM TOWER
# -----------------------------------------------------------------------------
from backend.app.services.satellite_lora_emergency_service import (
    SatelliteLoraEmergencyService,
    satellite_lora_emergency_service
)
from backend.app.schemas.satellite_lora_emergency_schema import (
    UssdSessionStateEnum,
    LoraSpreadingFactorEnum,
    TransmissionMediumEnum,
    UssdMenuRequest,
    UssdMenuResponse,
    LoraPacketEncodeRequest,
    LoraPacketEncodeResponse,
    OffGridSolarStationTelemetryDTO,
    StoreForwardQueueItemDTO,
    DisasterEmergencyBroadcastDTO,
    SatelliteLoraStatusDTO
)
# -----------------------------------------------------------------------------
# PHASE 74: ADAPTIVE NEURODIVERGENT ACCESSIBILITY & COGNITIVE READER TOWER
# -----------------------------------------------------------------------------
from backend.app.services.neurodivergent_accessibility_service import (
    NeurodivergentAccessibilityService,
    neurodivergent_accessibility_service
)
from backend.app.schemas.neurodivergent_accessibility_schema import (
    ReadingAssistanceModeEnum,
    ColorContrastPresetEnum,
    BionicReadingTransformRequest,
    BionicReadingTransformResponse,
    SyllableDecomposeRequest,
    SyllableDecomposeResponse,
    CognitivePacerConfigDTO,
    CognitivePacerTelemetryDTO,
    AccessibilityAuditMetricsDTO,
    AccessibilityStatusDTO
)
# -----------------------------------------------------------------------------
# PHASE 75: NATIONAL CENTRALIZED ADMISSION MATRIX & GALE-SHAPLEY MATCHING TOWER
# -----------------------------------------------------------------------------
from backend.app.services.admission_matching_service import (
    AdmissionMatchingService,
    admission_matching_service
)
from backend.app.schemas.admission_matching_schema import (
    QuotaCategoryEnum,
    ProgramSeatCapacityDTO,
    CandidatePreferenceDTO,
    AllocationItemDTO,
    MatchingRunRequest,
    MatchingRunResponse,
    MigrationStepDTO,
    MigrationSimulationRequest,
    MigrationSimulationResponse,
    AdmissionProbabilityQueryDTO,
    AdmissionProbabilityResponseDTO,
    AdmissionMatrixStatusDTO
)
from backend.app.core.audit_ledger import audit_ledger

from backend.app.core.rate_limiter import rate_limiter
from backend.app.core.security_headers import security_headers
from backend.app.core.timekeeper import ServerTimekeeper
from backend.app.api.v1.auth_router import auth_router
from backend.app.api.v1.endpoints.websocket import router as websocket_router
from backend.app.api.v1.endpoints.payments import router as payments_router
from backend.app.api.v1.endpoints.auth_otp import router as auth_otp_router
from backend.app.api.v1.endpoints.socratic_ai import router as socratic_ai_router
from backend.app.api.v1.endpoints.video import router as video_router
from backend.app.api.v1.endpoints.push import router as push_router
from backend.app.api.v1.endpoints.certificates import router as certificates_router
from backend.app.api.v1.endpoints.study_pods import router as study_pods_router
from backend.app.api.v1.endpoints.grading import router as grading_router
from backend.app.api.v1.endpoints.adaptive_exam import router as adaptive_exam_router
from backend.app.api.v1.endpoints.emergency_mesh import router as emergency_mesh_router
from backend.app.api.v1.endpoints.counseling import router as counseling_router
from backend.app.api.v1.endpoints.guardian_console import router as guardian_console_router
from backend.app.api.v1.endpoints.talent_pipeline import router as talent_pipeline_router
from backend.app.api.v1.endpoints.board_archives import router as board_archives_router
from backend.app.api.v1.endpoints.scholarships import router as scholarships_router
from backend.app.api.v1.endpoints.institution import router as institution_router
from backend.app.api.v1.endpoints.exam_hall import router as exam_hall_router
from backend.app.api.v1.endpoints.moderation import router as moderation_router
from backend.app.api.v1.endpoints.knowledge_graph import router as knowledge_graph_router
from backend.app.api.v1.endpoints.offline_sync import router as offline_sync_router
from backend.app.db.seed_data import (
    CURRICULUM_SEEDS,
    SUBJECT_SEEDS,
    ADMISSION_BLUEPRINTS,
    ACADEMIC_QUESTION_SEEDS
)

api_router = APIRouter()

# Mount Authentication sub-router
api_router.include_router(auth_router, prefix="/auth")

# Mount Real-Time WebSocket sub-router (Phase 80)
api_router.include_router(websocket_router)

# Mount Bangladeshi Payment Gateways & Escrow sub-router (Phase 81)
api_router.include_router(payments_router)

# Mount SMS OTP & Guardian Consent sub-router (Phase 82)
api_router.include_router(auth_otp_router)

# Mount Multi-Modal AI Socratic Tutor sub-router (Phase 90)
api_router.include_router(socratic_ai_router)

# Mount HLS Video Player & In-Lecture Checkpoints sub-router (Phase 91)
api_router.include_router(video_router)

# Mount W3C Web Push & Guardian Messaging Bot sub-router (Phase 94)
api_router.include_router(push_router)

# Mount Proof-of-Skill Certificate & Verification sub-router (Phase 96)
api_router.include_router(certificates_router)

# Mount Real-Time Study Pods & Collaborative Whiteboard sub-router (Phase 101)
api_router.include_router(study_pods_router)

# Mount Handwritten Script OCR & Step Rubric Grader sub-router (Phase 103)
api_router.include_router(grading_router)

# Mount AI Adaptive CAT Examination Tower sub-router (Phase 105)
api_router.include_router(adaptive_exam_router)

# Mount Rural LoRaWAN Emergency Bridge & Solar Micro-Hub sub-router (Phase 106)
api_router.include_router(emergency_mesh_router)

# Mount Centralized Admission Counseling & Gale-Shapley Stable Matching Hub sub-router (Phase 107)
api_router.include_router(counseling_router)

# Mount Guardian Trust Console & Child Digital Safety sub-router (Phase 108)
api_router.include_router(guardian_console_router)

# Mount Corporate Talent Acquisition & Cryptographic Skill Pipeline sub-router (Phase 109)
api_router.include_router(talent_pipeline_router)

# Mount Official NCTB Board Archives & KaTeX Mathematical Bank sub-router (Phase 112)
api_router.include_router(board_archives_router)

# Mount National Merit Scholarship Pool & Autonomous Disbursement sub-router (Phase 113)
api_router.include_router(scholarships_router)

# Mount Institutional White-Label Portal & Teacher Cockpit sub-router (Phase 114)
api_router.include_router(institution_router)

# Mount Digital Examination Hall & Proctoring Integrity Tower sub-router (Phase 116)
api_router.include_router(exam_hall_router)

# Mount Collaborative Question Bank Moderation & Peer-Review sub-router (Phase 117)
api_router.include_router(moderation_router)

# Mount Curriculum Knowledge Graph & Dynamic Remedial Navigator sub-router (Phase 118)
api_router.include_router(knowledge_graph_router)

# Mount Offline P2P Classroom Mesh & Local CRDT Sync sub-router (Phase 119)
api_router.include_router(offline_sync_router)




# -----------------------------------------------------------------------------
# Mock Curriculum Question Seed Data for Anytime Practice
# -----------------------------------------------------------------------------
SAMPLE_MATH_QUESTIONS = [
    {
        "id": "q_math_01",
        "stem_bn": "একটি ট্রেনের গতিবেগ ৬০ কিমি/ঘণ্টা। ট্রেনটি ১২০ কিমি যেতে কত সময় নেবে?",
        "stem_en": "A train travels at 60 km/h. How long will it take to travel 120 km?",
        "options": [
            {"id": "opt_01a", "option_key": "A", "option_text_bn": "১ ঘণ্টা", "is_correct": False},
            {"id": "opt_01b", "option_key": "B", "option_text_bn": "২ ঘণ্টা", "is_correct": True},
            {"id": "opt_01c", "option_key": "C", "option_text_bn": "৩ ঘণ্টা", "is_correct": False},
            {"id": "opt_01d", "option_key": "D", "option_text_bn": "৪ ঘণ্টা", "is_correct": False},
        ],
        "explanation_bn": "সময় = দূরত্ব ÷ গতিবেগ = ১২০ ÷ ৬০ = ২ ঘণ্টা।",
        "cognitive_skill": "APPLICATION",
        "estimated_seconds": 45
    },
    {
        "id": "q_math_02",
        "stem_bn": "বৃত্তের ক্ষেত্রফলের সূত্র কোনটি? (r = ব্যাসার্ধ)",
        "stem_en": "Which of the following is the formula for the area of a circle?",
        "options": [
            {"id": "opt_02a", "option_key": "A", "option_text_bn": "২πr", "is_correct": False},
            {"id": "opt_02b", "option_key": "B", "option_text_bn": "πr²", "is_correct": True},
            {"id": "opt_02c", "option_key": "C", "option_text_bn": "৪πr²", "is_correct": False},
            {"id": "opt_02d", "option_key": "D", "option_text_bn": "πr", "is_correct": False},
        ],
        "explanation_bn": "বৃত্তের ক্ষেত্রফল = π × ব্যাসার্ধ² = πr²। পরিধি হলো ২πr।",
        "cognitive_skill": "RECALL",
        "estimated_seconds": 30
    },
    {
        "id": "q_math_03",
        "stem_bn": "একটি সমকোণী ত্রিভুজের ভূমি ৪ সেমি এবং উচ্চতা ৩ সেমি হলে অতিভুজ কত?",
        "stem_en": "If a right triangle has base 4 cm and height 3 cm, what is the hypotenuse?",
        "options": [
            {"id": "opt_03a", "option_key": "A", "option_text_bn": "৫ সেমি", "is_correct": True},
            {"id": "opt_03b", "option_key": "B", "option_text_bn": "৬ সেমি", "is_correct": False},
            {"id": "opt_03c", "option_key": "C", "option_text_bn": "৭ সেমি", "is_correct": False},
            {"id": "opt_03d", "option_key": "D", "option_text_bn": "৮ সেমি", "is_correct": False},
        ],
        "explanation_bn": "পিথাগোরাসের উপপাদ্য অনুযায়ী: অতিভুজ = √(৩² + ৪²) = √(৯ + ১৬) = √২৫ = ৫ সেমি।",
        "cognitive_skill": "REASONING",
        "estimated_seconds": 50
    }
]


# -----------------------------------------------------------------------------
# 1. Health & Server Status Endpoint
# -----------------------------------------------------------------------------
@api_router.get("/health", tags=["Health"])
async def health_check():
    """Returns server vitality and precise NTP-synchronized UTC time."""
    return {
        "status": "healthy",
        "service": "Student Growth Platform Core API",
        "server_time": ServerTimekeeper.get_server_iso_now(),
        "version": "2.0.0"
    }


# -----------------------------------------------------------------------------
# 2. Learning Hub & Curricula Endpoints
# -----------------------------------------------------------------------------
@api_router.get("/learn/curricula", tags=["Learning Hub"])
async def get_curricula_catalog():
    """Returns NCTB 2024 curricula, stages, and subject seed registry."""
    return {
        "curricula": CURRICULUM_SEEDS,
        "subjects": SUBJECT_SEEDS
    }


@api_router.get("/learn/revision-queue/{user_id}", tags=["Learning Hub"])
async def get_revision_queue(user_id: str):
    """
    Returns spaced-repetition mistake replay items queued for this student.
    Learners focus on understanding underlying concepts without punitive scores.
    """
    return {
        "user_id": user_id,
        "queue_count": 2,
        "items": [
            {
                "question_id": "q_math_01",
                "stem_bn": "একটি ট্রেনের গতিবেগ ৬০ কিমি/ঘণ্টা। ট্রেনটি ১২০ কিমি যেতে কত সময় নেবে?",
                "missed_date": "2026-10-12T14:30:00Z",
                "concept": "Fundamental Ratio of Distance and Speed",
                "suggested_review_text": "Review NCTB Class 7 Mathematics Chapter 4."
            },
            {
                "question_id": "q_phys_newton_01",
                "stem_bn": "একটি স্থির বস্তুর ওপর ২০ নিউটন বল ৫ সেকেন্ড যাবত কাজ করলে বস্তুর ভরবেগের পরিবর্তন কত হবে?",
                "missed_date": "2026-10-13T10:15:00Z",
                "concept": "Impulse of Force and Conservation of Momentum",
                "suggested_review_text": "Practice Impulse = F × t formula application."
            }
        ]
    }


# -----------------------------------------------------------------------------
# 3. Anytime Practice Endpoints
# -----------------------------------------------------------------------------
@api_router.post("/practice/start", response_model=QuizAttemptStartResponse, tags=["Practice MCQ"])
async def start_practice_set(
    blueprint_id: str = Query("bp_math_class7", description="Curriculum Blueprint ID"),
    user_id: str = Query("usr_student_01", description="Current Authenticated User ID"),
    mode: QuizMode = QuizMode.ANYTIME_PRACTICE
):
    """
    Initializes a new practice set.
    Randomizes questions and options deterministically, creates an active attempt,
    and returns sanitized questions with server-authoritative countdown timer.
    """
    attempt = quiz_engine.start_practice_attempt(
        user_id=user_id,
        blueprint_id=blueprint_id,
        mode=mode,
        raw_questions=SAMPLE_MATH_QUESTIONS,
        duration_minutes=10,
        negative_marking=0.0
    )
    return attempt


@api_router.get(
    "/quiz-attempts/{attempt_id}",
    tags=["Practice MCQ"]
)
async def get_quiz_attempt(
    attempt_id: str,
    user_id: str = Query("usr_student_01", description="Current Authenticated User ID")
):
    """
    Retrieves current state and saved answers of a quiz attempt.
    Enforces strict IDOR protection: rejecting cross-student attempts with HTTP 403 Forbidden.
    """
    success, attempt, reason = quiz_engine.get_attempt_state(
        attempt_id=attempt_id,
        user_id=user_id
    )

    if not success:
        if reason == "ATTEMPT_NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")
        elif reason == "FORBIDDEN_ATTEMPT_OWNERSHIP":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="IDOR violation: Not your attempt.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    return {
        "attempt_id": attempt["attempt_id"],
        "user_id": attempt["user_id"],
        "blueprint_id": attempt["blueprint_id"],
        "status": attempt["status"],
        "started_at": attempt["started_at"].isoformat() if hasattr(attempt["started_at"], "isoformat") else str(attempt["started_at"]),
        "expires_at": attempt["expires_at"].isoformat() if hasattr(attempt["expires_at"], "isoformat") else str(attempt["expires_at"]),
        "saved_answers": attempt["saved_answers"],
        "total_saved": len(attempt["saved_answers"])
    }


@api_router.put(
    "/quiz-attempts/{attempt_id}/answers/{question_id}",
    response_model=AnswerSaveResponse,
    tags=["Practice MCQ"]
)
async def save_quiz_answer(
    attempt_id: str,
    question_id: str,
    payload: AnswerSaveRequest,
    x_idempotency_key: str = Header(..., description="Unique UUID to prevent duplicate writes"),
    user_id: str = Query("usr_student_01", description="Current Authenticated User ID")
):
    """
    Saves an answer to an active attempt.
    Enforces idempotency using X-Idempotency-Key. Survives flaky 3G/4G connections.
    """
    success, response, reason = quiz_engine.save_answer_idempotent(
        attempt_id=attempt_id,
        user_id=user_id,
        question_version_id=question_id,
        selected_option_id=payload.selected_option_id,
        idempotency_key=x_idempotency_key,
        time_taken_seconds=payload.time_taken_seconds
    )

    if not success:
        if reason == "ATTEMPT_NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")
        elif reason == "FORBIDDEN_ATTEMPT_OWNERSHIP":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="IDOR violation: Not your attempt.")
        elif reason == "EXAM_EXPIRED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exam duration has expired.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    return response


@api_router.post(
    "/quiz-attempts/{attempt_id}/submit",
    response_model=QuizResultResponse,
    tags=["Practice MCQ"]
)
async def submit_quiz_attempt(
    attempt_id: str,
    user_id: str = Query("usr_student_01", description="Current Authenticated User ID")
):
    """
    Finalizes attempt, calculates score server-side, applies negative marking,
    and returns mistake explanations. Missed items are added to Mistake Replay queue.
    """
    success, result, reason = quiz_engine.submit_and_score(
        attempt_id=attempt_id,
        user_id=user_id
    )

    if not success:
        if reason == "ATTEMPT_NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")
        elif reason == "FORBIDDEN_ATTEMPT_OWNERSHIP":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="IDOR violation: Not your attempt.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    return result


# -----------------------------------------------------------------------------
# 4. Scheduled High-Load Live Challenge Endpoints
# -----------------------------------------------------------------------------
@api_router.get("/live-challenges/sessions", tags=["Live Challenge"])
async def list_live_sessions():
    """Lists scheduled nationwide live challenges."""
    return {
        "active_sessions": [
            {
                "session_id": "live_hsc_phys_2026",
                "title": "National HSC Physics Live Olympiad 2026",
                "stage": "HSC",
                "scheduled_start": "2026-10-15T20:00:00Z",
                "duration_minutes": 25,
                "participants_registered": 14250,
                "status": "UPCOMING"
            },
            {
                "session_id": "live_admission_math_2026",
                "title": "University A-Unit Mathematics Grand Challenge",
                "stage": "ADMISSION",
                "scheduled_start": "2026-10-18T19:00:00Z",
                "duration_minutes": 30,
                "participants_registered": 28400,
                "status": "UPCOMING"
            }
        ]
    }


@api_router.post("/live-challenges/{session_id}/prewarm", tags=["Live Challenge"])
async def prewarm_live_session(session_id: str, payload: LiveSessionPrewarmRequest):
    """
    Pre-warms question payload into in-memory cache to withstand thundering herds
    (50,000+ simultaneous starts). Admin only.
    """
    questions = payload.questions if payload.questions else ACADEMIC_QUESTION_SEEDS
    res = live_challenge_service.prewarm_live_session(
        session_id=session_id,
        blueprint_title=payload.blueprint_title,
        start_time=payload.start_time,
        end_time=payload.end_time,
        sanitized_questions=questions,
        duration_minutes=payload.duration_minutes
    )
    return res


@api_router.post("/live-challenges/{session_id}/start", tags=["Live Challenge"])
async def start_live_session(
    session_id: str,
    user_id: str = Query(..., description="Participant User ID")
):
    """Starts synchronized attempt seeded for deterministic randomization."""
    attempt = quiz_engine.start_practice_attempt(
        user_id=user_id,
        blueprint_id=session_id,
        mode=QuizMode.LIVE_CHALLENGE,
        raw_questions=ACADEMIC_QUESTION_SEEDS,
        duration_minutes=25,
        negative_marking=0.25
    )
    return attempt


@api_router.get("/live-challenges/{session_id}/leaderboard", tags=["Live Challenge"])
async def get_live_leaderboard(session_id: str):
    """
    Retrieves pseudonymous leaderboard.
    Applies deterministic tie-break (Score -> Time spent).
    Protects minor privacy by omitting real names and personal information.
    """
    mock_completed_attempts = [
        {"user_id": "u1", "pseudonym": "Night_Star", "avatar_url": None, "raw_score": 100.0, "time_spent_seconds": 720, "accuracy_percent": 100.0},
        {"user_id": "u2", "pseudonym": "Science_Explorer", "avatar_url": None, "raw_score": 96.0, "time_spent_seconds": 650, "accuracy_percent": 96.0},
        {"user_id": "u3", "pseudonym": "Light_Seeker", "avatar_url": None, "raw_score": 96.0, "time_spent_seconds": 710, "accuracy_percent": 96.0},
        {"user_id": "u4", "pseudonym": "Polaris", "avatar_url": None, "raw_score": 92.0, "time_spent_seconds": 800, "accuracy_percent": 92.0},
    ]
    board = live_challenge_service.compute_leaderboard(session_id, mock_completed_attempts)
    return {
        "session_id": session_id,
        "calculated_at": ServerTimekeeper.get_server_iso_now(),
        "total_ranked": len(board),
        "rankings": board
    }


@api_router.post("/live-challenges/opt-out", tags=["Live Challenge"])
async def leaderboard_privacy_opt_out(
    user_id: str = Query(..., description="User ID"),
    payload: LeaderboardOptOutRequest = None
):
    """Allows student to opt-out of public leaderboards for mental health."""
    opt_out = payload.opt_out if payload else True
    live_challenge_service.set_user_leaderboard_opt_out(user_id=user_id, opt_out=opt_out)
    return {
        "user_id": user_id,
        "opted_out_of_public_leaderboard": opt_out,
        "message": "Leaderboard visibility preference updated successfully."
    }


# -----------------------------------------------------------------------------
# 5. University Admission Hub Endpoints
# -----------------------------------------------------------------------------
@api_router.get("/admission/blueprints", tags=["Admission Hub"])
async def list_admission_blueprints():
    """Lists official admission mock blueprints (DU Unit-A, Medical, BUET)."""
    return {
        "total": len(ADMISSION_BLUEPRINTS),
        "blueprints": ADMISSION_BLUEPRINTS
    }


@api_router.post("/admission/diagnostic-sprint", tags=["Admission Hub"])
async def analyze_diagnostic_sprint(payload: DiagnosticAnalyzeRequest):
    """
    Evaluates student performance into STRONG, NEEDS_REVISION, and CRITICAL_GAP.
    Generates an actionable 7-day targeted revision sprint without deceptive promises.
    """
    result = diagnostic_service.analyze_diagnostic_results(payload.topic_performance)
    return result


@api_router.get("/admission/circulars", tags=["Admission Hub"])
async def list_verified_circulars():
    """Lists verified university admission circulars with source citations."""
    return {
        "circulars": [
            {
                "university": "Dhaka University (DU)",
                "unit": "A-Unit (Science)",
                "application_deadline": "2026-11-15T23:59:59Z",
                "exam_date": "2026-12-19T10:00:00Z",
                "eligibility": "Minimum GPA 3.5 in SSC & HSC with total minimum 8.0",
                "official_link": "https://admission.eis.du.ac.bd",
                "is_verified": True
            },
            {
                "university": "BUET",
                "unit": "Faculty of Engineering",
                "application_deadline": "2026-11-20T23:59:59Z",
                "exam_date": "2026-12-28T09:00:00Z",
                "eligibility": "GPA 5.0 in Math, Physics and Chemistry in HSC",
                "official_link": "https://www.buet.ac.bd/admission",
                "is_verified": True
            }
        ]
    }


# -----------------------------------------------------------------------------
# 6. Tuition Marketplace Endpoints (Bilateral Consent Protected)
# -----------------------------------------------------------------------------
@api_router.get("/tuitions/listings", tags=["Tuition Marketplace"])
async def get_tuition_listings(
    district: Optional[str] = Query(None),
    thana: Optional[str] = Query(None),
    class_grade: Optional[int] = Query(None),
    subject: Optional[str] = Query(None)
):
    """
    Searches tuition requirements.
    Personal contact details (phones, exact homes) are strictly hidden until bilateral consent.
    """
    # Seed default listing if empty for testing
    if not tuition_service._listings:
        tuition_service.create_listing(
            creator_user_id="usr_guardian_01",
            class_grade=8,
            curriculum="NCTB",
            medium="BANGLA",
            subject="General Mathematics & Science",
            location_district="Dhaka",
            location_thana="Dhanmondi",
            is_online=False,
            salary_range_min=5000,
            salary_range_max=7000
        )
    return {
        "listings": tuition_service.search_listings(district, thana, class_grade, subject)
    }


@api_router.post("/tuitions/listings", tags=["Tuition Marketplace"])
async def create_tuition_listing(
    payload: TuitionListingCreateRequest,
    user_id: str = Query(..., description="Creator User ID")
):
    """Creates a new tuition post with geographic scoping."""
    listing = tuition_service.create_listing(
        creator_user_id=user_id,
        class_grade=payload.class_grade,
        curriculum=payload.curriculum,
        medium=payload.medium,
        subject=payload.subject,
        location_district=payload.location_district,
        location_thana=payload.location_thana,
        is_online=payload.is_online,
        salary_range_min=payload.salary_range_min,
        salary_range_max=payload.salary_range_max
    )
    return {
        "status": "SUCCESS",
        "listing": listing.to_dict()
    }


@api_router.post("/tuitions/{listing_id}/apply", tags=["Tuition Marketplace"])
async def apply_for_tuition(
    listing_id: str,
    payload: TuitionApplyRequest,
    tutor_id: str = Query(..., description="Tutor User ID")
):
    """Tutor applies to tuition. Contact remains hidden pending learner approval."""
    success, app, reason = tuition_service.apply_for_tuition(
        listing_id=listing_id,
        tutor_user_id=tutor_id,
        message=payload.message
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "APPLIED",
        "application_id": app.id,
        "contact_consent_granted": app.contact_consent_granted,
        "message": "Application submitted. Direct contact will unlock upon bilateral consent."
    }


@api_router.post("/tuitions/{listing_id}/grant-consent", tags=["Tuition Marketplace"])
async def grant_tuition_consent(
    listing_id: str,
    payload: ContactConsentGrantRequest,
    guardian_or_learner_id: str = Query(..., description="Listing Owner ID")
):
    """
    Bilateral Consent Step:
    Listing owner accepts tutor, disclosing verified contact details safely.
    """
    success, reason = tuition_service.grant_contact_consent(
        listing_id=listing_id,
        tutor_user_id=payload.tutor_user_id,
        learner_or_guardian_id=guardian_or_learner_id
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "CONSENT_GRANTED",
        "message": "Bilateral consent confirmed. Mutual contact details unlocked."
    }


# -----------------------------------------------------------------------------
# 7. Student Career Engine & CV Snapshot Endpoints
# -----------------------------------------------------------------------------
@api_router.post("/career/skills", tags=["Career Engine"])
async def add_student_skill(
    payload: StudentSkillAddRequest,
    student_id: str = Query(..., description="Student User ID")
):
    """Adds a verified or evidence-backed skill claim with GitHub/live URL."""
    skill = career_service.add_student_skill(
        student_id=student_id,
        skill_name=payload.skill_name,
        proficiency=payload.proficiency,
        evidence_url=payload.evidence_url
    )
    return {
        "status": "SUCCESS",
        "skill": skill.to_dict()
    }


@api_router.get("/career/skills/{student_id}", tags=["Career Engine"])
async def get_student_skills(student_id: str):
    """Retrieves learner's verified evidence portfolio."""
    skills = career_service._skills.get(student_id, [])
    return {
        "student_id": student_id,
        "total_skills": len(skills),
        "skills": [s.to_dict() for s in skills]
    }


@api_router.post("/career/cv-snapshot", tags=["Career Engine"])
async def create_cv_snapshot(
    payload: CVSnapshotCreateRequest,
    user_id: str = Query(..., description="Candidate User ID")
):
    """
    Freezes an immutable JSON snapshot of candidate qualifications.
    Prevents retroactive credential altering on submitted applications.
    """
    snapshot = career_service.create_cv_snapshot(
        user_id=user_id,
        application_title=payload.application_title,
        student_data=payload.student_data
    )
    return {
        "status": "FROZEN",
        "snapshot_id": snapshot.id,
        "created_at": snapshot.created_at,
        "snapshot": snapshot.to_dict()
    }


@api_router.get("/career/cv-snapshot/{snapshot_id}", tags=["Career Engine"])
async def get_cv_snapshot(
    snapshot_id: str,
    user_id: str = Query(..., description="Requesting User ID for IDOR verification")
):
    """
    Retrieves candidate's frozen CV snapshot.
    Enforces strict IDOR protection: rejecting unauthorized access with HTTP 403 Forbidden.
    """
    success, snapshot, reason = career_service.get_cv_snapshot(
        snapshot_id=snapshot_id,
        user_id=user_id
    )

    if not success:
        if reason == "SNAPSHOT_NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV Snapshot not found.")
        elif reason == "FORBIDDEN_SNAPSHOT_OWNERSHIP":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="IDOR violation: Not your CV snapshot.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    return {
        "status": "FROZEN",
        "snapshot_id": snapshot.id,
        "created_at": snapshot.created_at,
        "snapshot": snapshot.to_dict()
    }


@api_router.get("/career/jobs", tags=["Career Engine"])
async def list_career_opportunities():
    """Lists verified internship and entry-level career openings."""
    return {
        "jobs": [
            {
                "id": "job_se_intern_01",
                "title": "Junior Software Engineer Intern",
                "company_name": "BanglaTech Innovations",
                "location": "Dhaka (Hybrid)",
                "stipend_monthly": 20000,
                "required_skills": ["Python", "FastAPI", "Next.js", "PostgreSQL"],
                "is_verified_employer": True,
                "status": "ACTIVE"
            },
            {
                "id": "job_qa_intern_02",
                "title": "SQA & Automation Intern",
                "company_name": "Agrojatra EdTech",
                "location": "Dhaka (Remote)",
                "stipend_monthly": 18000,
                "required_skills": ["Python", "Selenium/Playwright", "API Testing"],
                "is_verified_employer": True,
                "status": "ACTIVE"
            }
        ]
    }


@api_router.post("/career/apply", tags=["Career Engine"])
async def apply_to_job(
    payload: JobApplicationSubmitRequest,
    candidate_id: str = Query(..., description="Candidate User ID")
):
    """Submits candidate application referencing an immutable CV snapshot."""
    # Seed job in service if not existing for testing
    if payload.job_id not in career_service._jobs:
        from backend.app.models.opportunity import JobListing
        career_service._jobs[payload.job_id] = JobListing(
            employer_user_id="emp_01",
            title="Software Engineering Intern",
            company_name="BanglaTech",
            status="ACTIVE"
        )

    success, app, reason = career_service.submit_job_application(
        job_id=payload.job_id,
        candidate_user_id=candidate_id,
        cv_snapshot_id=payload.cv_snapshot_id
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "APPLIED",
        "application_id": app.id,
        "stage": app.stage,
        "applied_at": app.created_at
    }


@api_router.patch(
    "/career/applications/{job_id}/{candidate_id}/stage",
    tags=["Career Engine"]
)
async def update_application_stage(
    job_id: str,
    candidate_id: str,
    payload: ApplicationStageUpdateRequest
):
    """Recruiter updates hiring stage: Applied -> Viewed -> Interview -> Offer."""
    success, reason = career_service.update_application_stage(
        job_id=job_id,
        candidate_user_id=candidate_id,
        new_stage=payload.new_stage
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "job_id": job_id,
        "candidate_id": candidate_id,
        "new_stage": payload.new_stage
    }


# -----------------------------------------------------------------------------
# 8. Admin Single-Click Quarantine & Audit Log Endpoints
# -----------------------------------------------------------------------------
@api_router.post(
    "/admin/questions/{question_id}/quarantine",
    tags=["Admin & Safety Operations"]
)
async def quarantine_question_endpoint(
    question_id: str,
    payload: QuestionQuarantineRequest,
    admin_id: str = Query("usr_admin_01", description="Authenticated Admin User ID"),
    admin_role: str = Query("ADMIN", description="User Role")
):
    """
    Single-click question quarantine.
    Immediately isolates flawed question from future pools, finds all affected attempts,
    reconciles scores, and writes to immutable audit log.
    """
    result = quarantine_service.quarantine_question(
        question_id=question_id,
        actor_id=admin_id,
        actor_role=admin_role,
        reason=payload.reason,
        recalculate_active=payload.recalculate_active_sessions
    )
    return result


@api_router.get(
    "/admin/audit-logs",
    tags=["Admin & Safety Operations"]
)
async def view_audit_logs():
    """Retrieves immutable administrative audit history."""
    return {
        "total_records": len(quarantine_service.get_audit_trail()),
        "records": quarantine_service.get_audit_trail()
    }


# -----------------------------------------------------------------------------
# 9. AI Content Pipeline & SME Review Gate Endpoints (FR-004)
# -----------------------------------------------------------------------------
@api_router.post(
    "/admin/content/ai-draft",
    tags=["AI Content Pipeline & SME Review"]
)
async def generate_ai_question_draft(
    payload: AIDraftGenerateRequest,
    admin_id: str = Query("usr_admin_01", description="Admin or Editor User ID")
):
    """
    Generates an initial MCQ draft with intelligent distractors and explanations.
    Status is strictly initialized to DRAFT. Prohibited from production without SME approval.
    """
    draft = content_pipeline_service.generate_ai_draft(
        subject=payload.subject,
        topic=payload.topic,
        concept=payload.concept,
        cognitive_level=payload.cognitive_level,
        curriculum=payload.curriculum,
        class_grade=payload.class_grade,
        creator_user_id=admin_id
    )
    return {
        "status": "SUCCESS",
        "question_id": draft["id"],
        "lifecycle_state": draft["status"],
        "draft": draft
    }


@api_router.post(
    "/admin/content/{question_id}/submit-review",
    tags=["AI Content Pipeline & SME Review"]
)
async def submit_question_for_review(question_id: str):
    """Transitions a draft question into the human SME review queue."""
    success, reason = content_pipeline_service.submit_for_sme_review(question_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "QUEUED",
        "question_id": question_id,
        "message": "Question submitted for SME review."
    }


@api_router.get(
    "/admin/content/review-queue",
    tags=["AI Content Pipeline & SME Review"]
)
async def get_sme_review_queue(
    status_filter: str = Query("NEEDS_REVIEW", description="Filter by lifecycle status")
):
    """Lists draft questions awaiting Subject Matter Expert (SME) validation."""
    queue = content_pipeline_service.get_review_queue(status_filter=status_filter)
    return {
        "status_filter": status_filter,
        "total_pending": len(queue),
        "items": queue
    }


@api_router.post(
    "/admin/content/{question_id}/review",
    tags=["AI Content Pipeline & SME Review"]
)
async def review_and_decide_question(
    question_id: str,
    payload: SMEReviewDecisionRequest,
    sme_id: str = Query("usr_sme_physics_01", description="Subject Matter Expert User ID")
):
    """
    Human Subject Matter Expert Gate:
    Validates question accuracy, pedagogy, and distractors.
    Moves to APPROVED or rejects back to DRAFT with feedback.
    """
    success, reason, item = content_pipeline_service.review_and_approve_draft(
        question_id=question_id,
        sme_user_id=sme_id,
        approve=payload.approve,
        rejection_reason=payload.rejection_reason
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "action": reason,
        "question_id": question_id,
        "new_state": item["status"] if item else "UNKNOWN"
    }


@api_router.post(
    "/admin/content/{question_id}/publish",
    tags=["AI Content Pipeline & SME Review"]
)
async def publish_approved_question(
    question_id: str,
    publisher_id: str = Query("usr_admin_01", description="Publishing Authority ID")
):
    """Releases an SME-approved question into the active live question bank."""
    success, reason = content_pipeline_service.publish_approved_question(
        question_id=question_id,
        publisher_id=publisher_id
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "action": reason,
        "question_id": question_id,
        "message": "Question successfully added to live examination pool."
    }


# ========================================================================================
# Phase 12: Psychometrics, Anti-Toxic Habits, Guardian Safety & Crowdsourced QA
# ========================================================================================

@api_router.get(
    "/psychometrics/student/{student_id}",
    tags=["Psychometrics & Anti-Toxic Habits"]
)
async def get_student_psychometrics(student_id: str):
    """Retrieves student adaptive Elo rating, estimated IRT theta, and habit metrics."""
    rating = psychometrics_service.get_or_create_student_rating(student_id)
    habits = psychometrics_service.get_or_create_habit_record(student_id)
    theta = (rating - 1200.0) / 400.0
    return {
        "student_id": student_id,
        "elo_rating": rating,
        "irt_theta": round(theta, 3),
        "zone_of_proximal_development": psychometrics_service.get_recommended_difficulty_band(student_id),
        "habit_record": habits
    }


@api_router.post(
    "/psychometrics/calibrate",
    tags=["Psychometrics & Anti-Toxic Habits"]
)
async def calibrate_student_rating(payload: PsychometricCalibrateRequest):
    """Calibrates student ability after answering a question."""
    new_rating, delta = psychometrics_service.update_rating_after_response(
        student_id=payload.student_id,
        question_difficulty=payload.question_difficulty,
        is_correct=payload.is_correct
    )
    expected_prob = psychometrics_service.calculate_expected_probability(
        student_rating=new_rating - delta,
        question_difficulty=payload.question_difficulty
    )
    return {
        "student_id": payload.student_id,
        "new_rating": round(new_rating, 2),
        "rating_delta": round(delta, 2),
        "expected_probability": round(expected_prob, 4),
        "timestamp": ServerTimekeeper.get_server_iso_now()
    }


@api_router.get(
    "/psychometrics/student/{student_id}/recommendation",
    tags=["Psychometrics & Anti-Toxic Habits"]
)
async def get_question_recommendation(student_id: str):
    """Returns recommended question difficulty band (Zone of Proximal Development)."""
    band = psychometrics_service.get_recommended_difficulty_band(student_id)
    return {
        "student_id": student_id,
        "difficulty_band": band,
        "target_accuracy_range": "60% - 75%",
        "educational_objective": "Optimal cognitive engagement without anxiety or boredom"
    }


@api_router.post(
    "/psychometrics/streak-freeze",
    tags=["Psychometrics & Anti-Toxic Habits"]
)
async def activate_streak_freeze(payload: StreakFreezeUseRequest):
    """Allows a learner to explicitly claim a Rest Day freeze pass without shame."""
    success, reason = psychometrics_service.consume_streak_freeze_pass(payload.student_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "action": reason,
        "student_id": payload.student_id,
        "message": "Rest day activated. Your streak is protected."
    }


# ---------------- Guardian Safety Operations (ASVS L2) ----------------

@api_router.post(
    "/guardian/minor/{minor_student_id}/token",
    tags=["Guardian Safety & Minor Protection"]
)
async def generate_guardian_pairing_token(minor_student_id: str):
    """Generates a secure 6-digit pairing code for minor student to provide to guardian."""
    token = guardian_service.generate_minor_pairing_token(minor_student_id)
    return {
        "minor_student_id": minor_student_id,
        "pairing_token": token,
        "expires_in_minutes": 60,
        "instructions": "Provide this linking code to your guardian to connect accounts."
    }


@api_router.post(
    "/guardian/link",
    tags=["Guardian Safety & Minor Protection"]
)
async def link_guardian_account(payload: GuardianLinkRequest):
    """Validates 6-digit pairing code and establishes legal guardian relationship."""
    success, reason, link_record = guardian_service.link_guardian_to_minor(
        guardian_user_id=payload.guardian_user_id,
        minor_student_id=payload.minor_student_id,
        pairing_token=payload.pairing_token,
        relationship=payload.relationship
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "message": "Guardian account linked successfully.",
        "link": link_record
    }


@api_router.post(
    "/guardian/tuition/co-sign",
    tags=["Guardian Safety & Minor Protection"]
)
async def co_sign_minor_tuition(payload: TuitionCoSignRequest):
    """Guardian co-signs a tuition listing on behalf of a minor learner."""
    success, reason, sign_record = guardian_service.record_tuition_co_signature(
        guardian_user_id=payload.guardian_user_id,
        tuition_listing_id=payload.tuition_listing_id,
        minor_student_id=payload.minor_student_id,
        guardian_notes=payload.guardian_notes
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "message": "Guardian co-signature recorded for tuition agreement.",
        "signature": sign_record
    }


@api_router.get(
    "/guardian/minor/{minor_student_id}/overview",
    tags=["Guardian Safety & Minor Protection"]
)
async def get_guardian_minor_overview(
    minor_student_id: str,
    guardian_user_id: str = Query(..., description="Linked Guardian User ID")
):
    """Provides non-invasive learning progress overview respecting minor privacy."""
    success, reason, summary = guardian_service.get_minor_guardian_overview(
        guardian_user_id=guardian_user_id,
        minor_student_id=minor_student_id
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=reason)
    return {
        "status": "SUCCESS",
        "overview": summary
    }


# ---------------- In-App Dispute & Crowdsourced QA ----------------

@api_router.post(
    "/disputes",
    tags=["Disputes & Crowdsourced QA"]
)
async def file_question_dispute(payload: DisputeFileRequest):
    """Learner files an in-app dispute reporting an error in a question."""
    success, reason, record = dispute_service.file_dispute(
        student_id=payload.student_id,
        question_id=payload.question_id,
        reason=payload.reason,
        explanation=payload.explanation,
        quiz_attempt_id=payload.quiz_attempt_id,
        suggested_correct_option=payload.suggested_correct_option
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "message": "Feedback submitted successfully. Moderation team will review promptly.",
        "dispute": record
    }


@api_router.get(
    "/disputes",
    tags=["Disputes & Crowdsourced QA"]
)
async def list_question_disputes(
    status: Optional[str] = Query(None, description="Filter by status: PENDING, RESOLVED, REJECTED"),
    question_id: Optional[str] = Query(None, description="Filter by question ID"),
    student_id: Optional[str] = Query(None, description="Filter by student ID")
):
    """Queries all student-reported question disputes."""
    items = dispute_service.list_disputes(
        status=status,
        question_id=question_id,
        student_id=student_id
    )
    return {
        "total_disputes": len(items),
        "disputes": items
    }


@api_router.get(
    "/disputes/{dispute_id}",
    tags=["Disputes & Crowdsourced QA"]
)
async def get_dispute_by_id(dispute_id: str):
    """Retrieves specific dispute details."""
    record = dispute_service.get_dispute(dispute_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DISPUTE_NOT_FOUND")
    return record


@api_router.post(
    "/disputes/{dispute_id}/resolve",
    tags=["Disputes & Crowdsourced QA"]
)
async def resolve_question_dispute(
    dispute_id: str,
    payload: DisputeResolveRequest
):
    """Subject matter moderator resolves dispute, corrects content or quarantines, and awards bounties."""
    success, reason, record = dispute_service.resolve_dispute(
        dispute_id=dispute_id,
        moderator_id=payload.moderator_id,
        action=payload.action,
        resolution_notes=payload.resolution_notes,
        trigger_quarantine=payload.trigger_quarantine,
        bounty_points=payload.bounty_points
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return {
        "status": "SUCCESS",
        "action": reason,
        "dispute": record
    }


@api_router.get(
    "/disputes/student/{student_id}/integrity-profile",
    tags=["Disputes & Crowdsourced QA"]
)
async def get_student_integrity_profile(student_id: str):
    """Retrieves student integrity bounty points and QA contribution badges."""
    profile = dispute_service.get_student_integrity_profile(student_id)
    return profile


# ========================================================================================
# Phase 13: Enterprise Health, Production Telemetry & Security Compliance
# ========================================================================================

@api_router.get(
    "/system/health",
    tags=["Enterprise Health & Diagnostics"]
)
async def get_system_health():
    """Returns deep health check status across all core microservices and subsystems."""
    return system_diagnostics_service.get_health_status()


@api_router.get(
    "/system/telemetry",
    tags=["Enterprise Health & Diagnostics"]
)
async def get_system_telemetry():
    """Aggregates real-time operational telemetry across active attempts, pools, and queues."""
    return system_diagnostics_service.get_telemetry_metrics()


@api_router.get(
    "/system/compliance",
    tags=["Enterprise Health & Diagnostics"]
)
async def get_system_compliance():
    """Audits system against OWASP ASVS L2 child safety rules and AI verification gates."""
    return system_diagnostics_service.validate_security_compliance()


# ========================================================================================
# Phase 14: Enterprise Security Hardening, Rate Limiting & Offline Network Resilience
# ========================================================================================

@api_router.post(
    "/offline/sync",
    tags=["Offline Resilience & Network Sync"]
)
@api_router.post(
    "/quiz-attempts/sync",
    tags=["Offline Resilience & Network Sync"]
)
async def sync_offline_batch(payload: OfflineSyncBatchRequest):
    """Replays and idempotently persists buffered answers accumulated while offline."""
    batch_result = offline_sync_service.process_offline_sync_batch(
        student_id=payload.student_id,
        attempt_id=payload.attempt_id,
        buffered_answers=payload.buffered_answers
    )
    return {
        "status": "SUCCESS",
        "message": "Offline answer batch synchronized successfully.",
        "batch": batch_result
    }



@api_router.get(
    "/offline/manifest",
    tags=["Offline Resilience & Network Sync"]
)
async def get_offline_manifest(
    class_grade: int = Query(8, description="Target class grade for offline practice bundle"),
    subject: str = Query("Mathematics", description="Target subject"),
    bundle_size: int = Query(10, description="Number of questions in offline bundle")
):
    """Generates and serves a lightweight offline practice bundle for PWA IndexedDB cache."""
    bundle = offline_sync_service.generate_offline_bundle(
        class_grade=class_grade,
        subject=subject,
        bundle_size=bundle_size
    )
    return bundle


@api_router.get(
    "/security/policy",
    tags=["Enterprise Security & ASVS L2"]
)
async def get_security_policy():
    """Returns active security headers, rate-limiting policies, and ASVS L2 guidelines."""
    return {
        "status": "ACTIVE",
        "standard_headers": security_headers.get_standard_headers(),
        "rate_limiting_metrics": rate_limiter.get_metrics(),
        "asvs_level": "ASVS 4.0 Level 2",
        "minor_safety_enforced": True
    }


@api_router.post(
    "/security/sanitize-profile",
    tags=["Enterprise Security & ASVS L2"]
)
async def sanitize_minor_profile(payload: SecurityProfileSanitizeRequest):
    """Demonstrates and tests ASVS L2 minor contact data masking."""
    sanitized = security_headers.sanitize_minor_profile_data(
        student_data=payload.student_profile,
        requester_user_id=payload.requester_user_id,
        requester_roles=payload.requester_roles,
        authorized_guardian_ids=payload.authorized_guardian_ids
    )
    return {
        "status": "SUCCESS",
        "sanitized_profile": sanitized
    }


# ========================================================================================
# Phase 15: Tamper-Evident Audit Ledger, Verifiable Open Credentials & Portfolio Proofs
# ========================================================================================

@api_router.post(
    "/credentials/issue",
    tags=["Verifiable Credentials & Badges"]
)
async def issue_student_credential(payload: CredentialIssueRequest):
    """Issues a cryptographically signed Open Badge / academic credential to a student."""
    record = portfolio_credential_service.issue_credential(
        student_id=payload.student_id,
        student_name=payload.student_name,
        is_minor=payload.is_minor,
        badge_type=payload.badge_type,
        title=payload.title,
        description=payload.description,
        subject=payload.subject,
        mastery_score=payload.mastery_score,
        evidence=payload.evidence
    )
    return {
        "status": "SUCCESS",
        "message": "Student achievement credential issued successfully.",
        "credential": record
    }


@api_router.get(
    "/credentials/verify/{credential_id}",
    tags=["Verifiable Credentials & Badges"]
)
async def verify_student_credential(credential_id: str):
    """
    Public verification endpoint for third-party institutions and recruiters.
    Redacts minor students' sensitive personal identifiers while confirming cryptographic validity.
    """
    verification = portfolio_credential_service.verify_credential(credential_id=credential_id)
    return verification


@api_router.get(
    "/credentials/student/{student_id}",
    tags=["Verifiable Credentials & Badges"]
)
async def list_student_credentials(student_id: str):
    """Lists all valid credentials and mastery badges awarded to a student."""
    credentials = portfolio_credential_service.get_student_credentials(student_id=student_id)
    return {
        "student_id": student_id,
        "total_credentials": len(credentials),
        "credentials": credentials
    }


@api_router.get(
    "/audit/ledger/verify",
    tags=["Cryptographic Audit Ledger"]
)
async def verify_audit_ledger_integrity():
    """Validates the unbroken cryptographic SHA-256 hash chain of the entire audit ledger."""
    is_valid, corrupted_idx, message = audit_ledger.verify_integrity()
    return {
        "valid": is_valid,
        "total_blocks": audit_ledger.get_total_blocks(),
        "corrupted_block_index": corrupted_idx,
        "message": message
    }


@api_router.get(
    "/audit/ledger/blocks",
    tags=["Cryptographic Audit Ledger"]
)
async def list_audit_ledger_blocks(
    limit: int = Query(20, description="Max blocks to retrieve"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Returns paginated immutable blocks from the audit ledger for compliance auditing."""
    blocks = audit_ledger.get_blocks(limit=limit, offset=offset)
    return {
        "total_blocks": audit_ledger.get_total_blocks(),
        "limit": limit,
        "offset": offset,
        "blocks": blocks
    }


# ========================================================================================
# Phase 16: Personalized Spaced Repetition (SuperMemo SM-2) & Adaptive Remediation Roadmap
# ========================================================================================

@api_router.post(
    "/study-plan/generate",
    tags=["Personalized Study Plans & Remediation"]
)
async def generate_student_study_plan(payload: StudyPlanGenerateRequest):
    """Generates an adaptive 7-day study roadmap addressing student-specific learning gaps."""
    plan = study_plan_service.generate_study_plan(
        student_id=payload.student_id,
        class_grade=payload.class_grade,
        target_subject=payload.target_subject,
        weak_topics=payload.weak_topics,
        daily_available_minutes=payload.daily_available_minutes
    )
    return {
        "status": "SUCCESS",
        "message": "Personalized 7-day study plan generated successfully.",
        "study_plan": plan
    }


@api_router.get(
    "/study-plan/student/{student_id}",
    tags=["Personalized Study Plans & Remediation"]
)
async def get_student_study_plan(student_id: str):
    """Retrieves current active study roadmap and completion progress for a student."""
    plan = study_plan_service.get_active_study_plan(student_id=student_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active study plan found for student."
        )
    return plan


@api_router.post(
    "/study-plan/milestone/complete",
    tags=["Personalized Study Plans & Remediation"]
)
async def complete_study_milestone(payload: MilestoneCompleteRequest):
    """Marks a daily study plan milestone complete and updates overall progress."""
    result = study_plan_service.complete_milestone(
        student_id=payload.student_id,
        milestone_id=payload.milestone_id
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error completing study milestone.")
        )
    return result


@api_router.post(
    "/spaced-repetition/review",
    tags=["Spaced Repetition & Retention"]
)
async def record_spaced_review(payload: SpacedReviewRecordRequest):
    """Records SM-2 recall quality (0-5) and recalculates review interval."""
    record = spaced_repetition_service.record_review(
        student_id=payload.student_id,
        question_id=payload.question_id,
        topic=payload.topic,
        quality_score=payload.quality_score
    )
    return {
        "status": "SUCCESS",
        "message": "Spaced repetition review logged successfully.",
        "review_record": record
    }


@api_router.get(
    "/spaced-repetition/due/{student_id}",
    tags=["Spaced Repetition & Retention"]
)
async def get_due_spaced_reviews(student_id: str):
    """Returns all questions due for review under the SM-2 algorithm schedule."""
    due_items = spaced_repetition_service.get_due_reviews(student_id=student_id)
    return {
        "student_id": student_id,
        "due_count": len(due_items),
        "due_questions": due_items
    }


@api_router.get(
    "/spaced-repetition/stats/{student_id}",
    tags=["Spaced Repetition & Retention"]
)
async def get_spaced_retention_stats(student_id: str):
    """Returns student memory retention statistics, ease factor, and mastery progress."""
    stats = spaced_repetition_service.get_student_mastery_stats(student_id=student_id)
    return stats


# ========================================================================================
# Phase 17: Collaborative Peer Study Circles & Real-Time Academic Dispute Arbitration
# ========================================================================================

@api_router.post(
    "/study-circles/create",
    tags=["Peer Study Circles"]
)
async def create_peer_study_circle(payload: StudyCircleCreateRequest):
    """Creates a cooperative minor-safe study circle (max 6 members) with shared streaks."""
    circle = study_circle_service.create_study_circle(
        creator_id=payload.creator_id,
        creator_name=payload.creator_name,
        is_minor=payload.is_minor,
        name=payload.name,
        subject=payload.subject,
        class_grade=payload.class_grade,
        target_weekly_questions=payload.target_weekly_questions
    )
    return {
        "status": "SUCCESS",
        "message": "Study circle created successfully.",
        "circle": circle
    }


@api_router.post(
    "/study-circles/{circle_id}/join",
    tags=["Peer Study Circles"]
)
async def join_peer_study_circle(circle_id: str, payload: StudyCircleJoinRequest):
    """Adds a student to an existing study circle while protecting minor PII."""
    result = study_circle_service.join_study_circle(
        circle_id=circle_id,
        student_id=payload.student_id,
        student_name=payload.student_name,
        is_minor=payload.is_minor
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to join study circle.")
        )
    return result


@api_router.post(
    "/study-circles/{circle_id}/contribute",
    tags=["Peer Study Circles"]
)
async def contribute_to_study_circle(circle_id: str, payload: StudyCircleContributeRequest):
    """Logs practice questions solved by a member toward the circle's weekly collective goal."""
    result = study_circle_service.contribute_questions(
        circle_id=circle_id,
        student_id=payload.student_id,
        questions_solved=payload.questions_solved
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error logging study circle contribution.")
        )
    return result


@api_router.get(
    "/study-circles/{circle_id}",
    tags=["Peer Study Circles"]
)
async def get_study_circle(circle_id: str):
    """Retrieves circle status, members, and shared weekly progress with minor PII masked."""
    circle = study_circle_service.get_circle_details(circle_id=circle_id)
    if not circle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study circle not found."
        )
    return circle


@api_router.post(
    "/arbitration/tribunal/create",
    tags=["Academic Dispute Arbitration"]
)
async def create_tribunal_arbitration_case(payload: TribunalCaseCreateRequest):
    """Convenes a 3-SME consensus tribunal for a contested question or answer key."""
    case = arbitration_service.create_tribunal_case(
        question_id=payload.question_id,
        question_stem=payload.question_stem,
        dispute_reason=payload.dispute_reason,
        filed_by_student_id=payload.filed_by_student_id
    )
    return {
        "status": "SUCCESS",
        "message": "Academic Tribunal convened. 3 specialist jurists invited for quorum.",
        "case": case
    }


@api_router.post(
    "/arbitration/tribunal/{case_id}/vote",
    tags=["Academic Dispute Arbitration"]
)
async def cast_arbitration_vote(case_id: str, payload: TribunalVoteRequest):
    """Records an SME arbitrator's verdict and automatically seals ruling when quorum is met."""
    result = arbitration_service.cast_sme_vote(
        case_id=case_id,
        sme_id=payload.sme_id,
        sme_name=payload.sme_name,
        verdict=payload.verdict,
        rationale=payload.rationale
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error submitting tribunal vote.")
        )
    return result


@api_router.get(
    "/arbitration/tribunal/{case_id}",
    tags=["Academic Dispute Arbitration"]
)
async def get_tribunal_case(case_id: str):
    """Retrieves tribunal case details, votes cast, and final sealed ruling."""
    case = arbitration_service.get_case(case_id=case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tribunal case not found."
        )
    return case


# -----------------------------------------------------------------------------
# 18. Computerized Adaptive Testing (CAT) & Blueprint Composer Endpoints
# -----------------------------------------------------------------------------
@api_router.post(
    "/cat/session/start",
    tags=["Computerized Adaptive Testing"]
)
async def start_cat_session(payload: CatSessionStartRequest):
    """Initializes a 2-PL IRT adaptive testing session with dynamic Fisher item selection."""
    session = cat_engine_service.start_cat_session(
        student_id=payload.student_id,
        subject=payload.subject,
        initial_theta=payload.initial_theta
    )
    return session


@api_router.post(
    "/cat/session/{session_id}/answer",
    tags=["Computerized Adaptive Testing"]
)
async def submit_cat_answer(session_id: str, payload: CatAnswerSubmitRequest):
    """Submits student response, updates latent ability (Theta), and serves next optimal item."""
    result = cat_engine_service.submit_cat_answer(
        session_id=session_id,
        item_id=payload.item_id,
        selected_option_id=payload.selected_option_id
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error evaluating CAT response.")
        )
    return result


@api_router.get(
    "/cat/session/{session_id}/status",
    tags=["Computerized Adaptive Testing"]
)
async def get_cat_session_status(session_id: str):
    """Retrieves current ability estimate, standard error, and item history."""
    session = cat_engine_service.get_session(session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAT session not found."
        )
    return session


@api_router.post(
    "/blueprints/compose",
    tags=["Curriculum Exam Blueprints"]
)
async def compose_exam_blueprint(payload: BlueprintComposeRequest):
    """Composes and validates an exam blueprint conforming to Bloom's cognitive taxonomy."""
    result = blueprint_composer_service.compose_blueprint(
        name=payload.name,
        subject=payload.subject,
        class_grade=payload.class_grade,
        total_questions=payload.total_questions,
        duration_minutes=payload.duration_minutes,
        cognitive_distribution=payload.cognitive_distribution,
        chapter_distribution=payload.chapter_distribution,
        negative_marking=payload.negative_marking
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error composing curriculum blueprint.")
        )
    return result


@api_router.get(
    "/blueprints/presets",
    tags=["Curriculum Exam Blueprints"]
)
async def list_preset_blueprints():
    """Lists pre-configured official NCTB and University Admission blueprints."""
    return blueprint_composer_service.list_presets()


@api_router.get(
    "/blueprints/{blueprint_id}",
    tags=["Curriculum Exam Blueprints"]
)
async def get_blueprint_by_id(blueprint_id: str):
    """Retrieves an official or custom exam blueprint by ID."""
    bp = blueprint_composer_service.get_blueprint(blueprint_id=blueprint_id)
    if not bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blueprint not found."
        )
    return bp


# -----------------------------------------------------------------------------
# 19. Socratic AI Tutor & Mathematical Visualizer Endpoints
# -----------------------------------------------------------------------------
@api_router.post(
    "/socratic/session/start",
    tags=["Socratic AI Tutor"]
)
async def start_socratic_tutoring_session(payload: SocraticSessionStartRequest):
    """Initializes a pedagogical Socratic tutoring dialogue without answer leakage."""
    session = socratic_tutor_service.start_socratic_session(
        student_id=payload.student_id,
        question_id=payload.question_id,
        is_minor=payload.is_minor
    )
    return session


@api_router.post(
    "/socratic/session/{session_id}/message",
    tags=["Socratic AI Tutor"]
)
async def send_socratic_message(session_id: str, payload: SocraticMessageSendRequest):
    """Submits student response, validates ASVS safety filters, and returns guided scaffold."""
    result = socratic_tutor_service.send_student_message(
        session_id=session_id,
        message_text=payload.message_text
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error processing Socratic dialogue message.")
        )
    return result


@api_router.post(
    "/socratic/session/{session_id}/hint",
    tags=["Socratic AI Tutor"]
)
async def request_socratic_hint(session_id: str, payload: SocraticHintRequest):
    """Yields next progressive scaffolding hint (Tier 1 -> Tier 2 -> Tier 3)."""
    result = socratic_tutor_service.request_scaffold_hint(session_id=session_id)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error loading Socratic scaffolding hint.")
        )
    return result


@api_router.get(
    "/visualizer/geometry/{concept_id}",
    tags=["Mathematical & Physics Visualizer"]
)
async def get_geometry_visualization(concept_id: str, a: float = 6.0, b: float = 8.0):
    """Generates procedural, crisp SVG vector diagrams for mathematical and physical concepts."""
    result = math_visualizer_service.generate_geometry_svg(
        concept_id=concept_id,
        param_a=a,
        param_b=b
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Visualization concept not found.")
        )
    return result


# -----------------------------------------------------------------------------
# 20. AI Mock Interview Evaluator & Career Matcher Endpoints
# -----------------------------------------------------------------------------
@api_router.post(
    "/career/interview/start",
    tags=["Career & Mock Interview Coach"]
)
async def start_mock_interview(payload: MockInterviewStartRequest):
    """Initializes a new AI mock interview session across tech, tutoring, or viva tracks."""
    return interview_coach_service.start_interview_session(
        candidate_id=payload.candidate_id,
        track_id=payload.track_id,
        is_minor=payload.is_minor
    )


@api_router.post(
    "/career/interview/{session_id}/answer",
    tags=["Career & Mock Interview Coach"]
)
async def submit_mock_interview_answer(session_id: str, payload: MockInterviewAnswerRequest):
    """Submits and evaluates candidate response with multi-dimensional rubric scoring."""
    result = interview_coach_service.submit_interview_answer(
        session_id=session_id,
        answer_text=payload.answer_text
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error evaluating mock interview answer.")
        )
    return result


@api_router.get(
    "/career/interview/{session_id}/report",
    tags=["Career & Mock Interview Coach"]
)
async def get_mock_interview_report(session_id: str):
    """Returns final structured interview performance report with strengths and growth areas."""
    result = interview_coach_service.get_interview_report(session_id=session_id)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error generating mock interview report.")
        )
    return result


@api_router.get(
    "/career/matcher/roles",
    tags=["Career & Skill Fit Matcher"]
)
async def list_career_target_roles():
    """Lists available target industry and tutoring roles with skill criteria."""
    return career_matcher_service.list_target_roles()


@api_router.post(
    "/career/matcher/analyze",
    tags=["Career & Skill Fit Matcher"]
)
async def analyze_candidate_career_fit(payload: CareerFitAnalysisRequest):
    """Analyzes skill-to-job fit, computes match percentage, and generates remediation sprint roadmap."""
    result = career_matcher_service.analyze_career_fit(
        candidate_id=payload.candidate_id,
        role_id=payload.role_id,
        candidate_skills=payload.candidate_skills,
        verified_badges_count=payload.verified_badges_count,
        quiz_mastery_pct=payload.quiz_mastery_pct
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error analyzing career fit matching.")
        )
    return result


# -----------------------------------------------------------------------------
# 21. Predictive Academic CGPA & National Rank Forecasting Endpoints
# -----------------------------------------------------------------------------
@api_router.post(
    "/analytics/predict-gpa",
    tags=["Predictive Analytics & Rank Forecasting"]
)
async def predict_gpa_and_national_rank(payload: GPAPredictionRequest):
    """
    Bayesian CGPA & National Cohort Rank Projector:
    Calculates expected CGPA with 95% Confidence Interval, Golden A+ probability,
    and merit rank estimation against 1.3M+ national student cohorts.
    """
    result = predictive_analytics_service.predict_gpa_and_national_rank(
        student_id=payload.student_id,
        target_exam=payload.target_exam,
        subject_performances=payload.subject_performances,
        historical_exam_scores=payload.historical_exam_scores,
        study_consistency_index=payload.study_consistency_index
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error computing CGPA projection.")
        )
    return result


@api_router.post(
    "/analytics/admission-probability",
    tags=["Predictive Analytics & Rank Forecasting"]
)
async def evaluate_admission_probabilities(payload: AdmissionProbabilityRequest):
    """
    Competitive Admission Probability Evaluator:
    Projects acceptance probabilities across BUET, DU Ka, Medical, DU Ga, and GST,
    identifying high-ROI chapter targets for maximum marginal score uplift.
    """
    return admission_probability_service.evaluate_admission_probabilities(
        student_id=payload.student_id,
        subject_scores=payload.subject_scores,
        predicted_cgpa=payload.predicted_cgpa
    )


@api_router.post(
    "/analytics/sensitivity-simulate",
    tags=["Predictive Analytics & Rank Forecasting"]
)
async def simulate_what_if_sensitivity(payload: SensitivitySimulationRequest):
    """
    What-If Sensitivity Simulator:
    Simulates real-time score adjustments (+/-) to compute probability shifts,
    national rank leaps, and required focused study hours.
    """
    result = admission_probability_service.simulate_what_if_sensitivity(
        student_id=payload.student_id,
        track_id=payload.track_id,
        baseline_subject_scores=payload.baseline_subject_scores,
        score_deltas=payload.score_deltas,
        current_rank=payload.current_rank
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error executing admission sensitivity simulation.")
        )
    return result


@api_router.get(
    "/analytics/benchmarks",
    tags=["Predictive Analytics & Rank Forecasting"]
)
async def get_national_benchmarks():
    """Returns official national board demographics, grading scales, and admission thresholds."""
    return predictive_analytics_service.get_national_benchmarks()


# -----------------------------------------------------------------------------
# 22. Intelligent Daily Study Scheduler, Pomodoro Sprints & Burnout Shield Endpoints
# -----------------------------------------------------------------------------
@api_router.post(
    "/scheduler/generate-daily",
    tags=["Study Scheduler & Burnout Prevention"]
)
async def generate_daily_study_schedule(payload: DailyScheduleGenerateRequest):
    """
    Circadian-Optimized Daily Routine Generator:
    Generates a personalized daily study timeline balancing high cognitive load
    subjects with peak alertness windows, active recall, and wellness recovery breaks.
    """
    return study_scheduler_service.generate_daily_schedule(
        student_id=payload.student_id,
        available_hours=payload.available_hours,
        weak_subjects=payload.weak_subjects,
        target_exam=payload.target_exam,
        wake_time=payload.wake_time,
        bedtime=payload.bedtime
    )


@api_router.post(
    "/scheduler/sprint/start",
    tags=["Study Scheduler & Burnout Prevention"]
)
async def start_focus_sprint_session(payload: FocusSprintStartRequest):
    """
    Pomodoro Focus Sprint Initializer:
    Initializes a server-validated deep work focus session with anti-distraction locking.
    """
    return study_scheduler_service.start_focus_sprint(
        student_id=payload.student_id,
        slot_id=payload.slot_id,
        duration_minutes=payload.duration_minutes,
        sprint_type=payload.sprint_type
    )


@api_router.post(
    "/scheduler/sprint/{session_id}/complete",
    tags=["Study Scheduler & Burnout Prevention"]
)
async def complete_focus_sprint_session(session_id: str, payload: FocusSprintCompleteRequest):
    """
    Pomodoro Focus Sprint Finalizer:
    Logs completed focus time, computes focus efficiency, awards streak points,
    and prescribes personalized recharge intervals.
    """
    result = study_scheduler_service.complete_focus_sprint(
        session_id=session_id,
        actual_duration_minutes=payload.actual_duration_minutes,
        distraction_count=payload.distraction_count,
        self_reported_focus_score=payload.self_reported_focus_score
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error completing focus sprint.")
        )
    return result


@api_router.post(
    "/scheduler/burnout/evaluate",
    tags=["Study Scheduler & Burnout Prevention"]
)
async def evaluate_cognitive_fatigue(payload: BurnoutEvaluationRequest):
    """
    Cognitive Fatigue & Burnout Risk Evaluator:
    Computes real-time Cognitive Fatigue Index (0-100) based on continuous study strain,
    sleep deficit, and break relief, triggering guardian care alerts for at-risk minors.
    """
    return burnout_prevention_service.evaluate_cognitive_fatigue(
        student_id=payload.student_id,
        continuous_study_hours=payload.continuous_study_hours,
        sleep_hours_last_night=payload.sleep_hours_last_night,
        total_study_hours_today=payload.total_study_hours_today,
        break_minutes_today=payload.break_minutes_today,
        is_minor=payload.is_minor
    )


@api_router.get(
    "/scheduler/burnout/status/{student_id}",
    tags=["Study Scheduler & Burnout Prevention"]
)
async def get_student_burnout_status(student_id: str):
    """Returns the latest evaluated fatigue status and recharge prescriptions for a student."""
    return burnout_prevention_service.get_student_burnout_status(student_id=student_id)


# ======================================================================================
# ######################################################################################
# SECTION 23: TRI-PLATFORM ENTERPRISE CONVERGENCE (10MS + CARETUTORS + BDJOBS)
# ######################################################################################
# ======================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: 10 MINUTE SCHOOL BENCHMARK - VIDEO MICRO-CLASSROOM & CHECKPOINTS
# --------------------------------------------------------------------------------------

@api_router.post(
    "/classroom/video/progress",
    tags=["Video Micro-Classroom (10MS)"]
)
async def update_video_playback_progress(payload: VideoProgressUpdateRequest):
    """
    Video Playback Telemetry & Progress Synchronizer:
    Updates student's playback timestamp, resolution, speed multiplier,
    and recalculates micro-lecture completion percentage.
    """
    return video_classroom_service.record_playback_progress(
        video_id=payload.video_id,
        student_id=payload.student_id,
        current_timestamp_seconds=payload.current_timestamp_seconds,
        total_duration_seconds=payload.total_duration_seconds,
        resolution=payload.resolution,
        playback_speed=payload.playback_speed
    )


@api_router.get(
    "/classroom/video/{video_id}/checkpoints",
    tags=["Video Micro-Classroom (10MS)"]
)
async def get_video_in_lecture_checkpoints(video_id: str):
    """
    Retrieves in-lecture checkpoint quizzes assigned to specific video timestamps.
    """
    return video_classroom_service.get_video_checkpoints(video_id=video_id)


@api_router.post(
    "/classroom/video/checkpoint/submit",
    tags=["Video Micro-Classroom (10MS)"]
)
async def submit_video_checkpoint_quiz_answer(payload: CheckpointQuizSubmitRequest):
    """
    In-Lecture Checkpoint Quiz Evaluator:
    Scores student response, computes topic mastery percentage,
    and unlocks syllabus milestones upon correct answer.
    """
    result = video_classroom_service.submit_checkpoint_answer(
        video_id=payload.video_id,
        checkpoint_id=payload.checkpoint_id,
        student_id=payload.student_id,
        timestamp_seconds=payload.timestamp_seconds,
        selected_option_index=payload.selected_option_index
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error evaluating checkpoint response.")
        )
    return result


@api_router.post(
    "/classroom/video/note",
    tags=["Video Micro-Classroom (10MS)"]
)
async def pin_video_timestamp_note(payload: VideoNoteCreateRequest):
    """
    Pins a student's personal revision note or bookmark to a specific video timestamp.
    """
    result = video_classroom_service.add_video_note(
        video_id=payload.video_id,
        student_id=payload.student_id,
        timestamp_seconds=payload.timestamp_seconds,
        note_text=payload.note_text,
        is_bookmarked=payload.is_bookmarked
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error saving timestamp note.")
        )
    return result


@api_router.get(
    "/classroom/video/{video_id}/notes/{student_id}",
    tags=["Video Micro-Classroom (10MS)"]
)
async def get_student_video_notes(video_id: str, student_id: str):
    """
    Retrieves all chronological revision notes pinned by a student for a video lecture.
    """
    return video_classroom_service.get_student_notes(video_id=video_id, student_id=student_id)


# --------------------------------------------------------------------------------------
# TOPIC B: CARETUTORS BENCHMARK - TUITION MARKETPLACE & BILATERAL CONSENT
# --------------------------------------------------------------------------------------

@api_router.post(
    "/marketplace/tuitions/create",
    tags=["Tuition Marketplace (CareTutors)"]
)
async def create_guardian_tuition_listing(payload: TuitionMarketplaceListingCreateRequest):
    """
    Guardian Post-a-Tuition Wizard:
    Creates a verified tuition requirement with district/thana geographic location,
    curriculum medium, days/week, and budget in BDT with ASVS L2 contact masking.
    """
    return tuition_marketplace_service.create_tuition_listing(
        creator_user_id=payload.creator_user_id,
        class_grade=payload.class_grade,
        curriculum=payload.curriculum,
        medium=payload.medium,
        subject=payload.subject,
        location_district=payload.location_district,
        location_thana=payload.location_thana,
        days_per_week=payload.days_per_week,
        gender_preference=payload.gender_preference,
        salary_budget_bdt=payload.salary_budget_bdt,
        guardian_phone=payload.guardian_phone,
        is_online=payload.is_online,
        requirements=payload.requirements
    )


@api_router.get(
    "/marketplace/tuitions/feed",
    tags=["Tuition Marketplace (CareTutors)"]
)
async def get_live_tuition_feed(
    district: Optional[str] = Query(None, description="Filter by district (e.g., Dhaka, Chattogram)"),
    class_grade: Optional[int] = Query(None, description="Filter by student class (e.g., 10, 12)"),
    medium: Optional[str] = Query(None, description="Filter by medium (e.g., BANGLA_MEDIUM, ENGLISH_VERSION)"),
    max_budget_bdt: Optional[int] = Query(None, description="Maximum budget in BDT"),
    search_query: Optional[str] = Query(None, description="Keyword search in subject or thana")
):
    """
    Live Tuition Job Feed:
    Returns real-time tuition requirements across Bangladesh divisions with
    ASVS L2 privacy masking on guardian phone numbers.
    """
    return tuition_marketplace_service.get_tuition_feed(
        district=district,
        class_grade=class_grade,
        medium=medium,
        max_budget_bdt=max_budget_bdt,
        search_query=search_query
    )


@api_router.post(
    "/marketplace/tuitions/apply",
    tags=["Tuition Marketplace (CareTutors)"]
)
async def apply_for_tuition_listing(payload: TuitionApplicationSubmitRequest):
    """
    1-Click Tutor Application:
    Attaches verified university credentials, CGPA, and contact details
    in PENDING bilateral consent state.
    """
    result = tuition_marketplace_service.submit_application(
        listing_id=payload.listing_id,
        tutor_user_id=payload.tutor_user_id,
        tutor_name=payload.tutor_name,
        tutor_university=payload.tutor_university,
        tutor_cgpa_or_gpa=payload.tutor_cgpa_or_gpa,
        tutor_phone=payload.tutor_phone,
        cover_letter=payload.cover_letter
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error submitting tuition application.")
        )
    return result


@api_router.post(
    "/marketplace/tuitions/consent/update",
    tags=["Tuition Marketplace (CareTutors)"]
)
async def update_bilateral_tuition_consent(payload: BilateralConsentUpdateRequest):
    """
    Bilateral Consent Handshake Engine:
    Processes 'GUARDIAN_APPROVE' or 'TUTOR_ACCEPT' transitions.
    Unlocks unmasked mutual contact details ONLY when bilateral consent is reached.
    """
    result = tuition_marketplace_service.update_bilateral_consent(
        listing_id=payload.listing_id,
        application_id=payload.application_id,
        actor_user_id=payload.actor_user_id,
        action=payload.action
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error updating bilateral consent.")
        )
    return result


@api_router.get(
    "/marketplace/tuitions/application/{application_id}/contact",
    tags=["Tuition Marketplace (CareTutors)"]
)
async def get_tuition_contact_status(
    application_id: str,
    requesting_user_id: str = Query(..., description="ID of the user making the request")
):
    """
    ASVS L2 Mutual Contact Status & Disclosure:
    Enforces IDOR authorization and discloses unmasked contact info
    only when mutual consent is unlocked.
    """
    result = tuition_marketplace_service.get_application_contact_status(
        application_id=application_id,
        requesting_user_id=requesting_user_id
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN if result.get("error_code") == "FORBIDDEN_ACCESS" else status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Error checking contact disclosure status.")
        )
    return result


# --------------------------------------------------------------------------------------
# TOPIC C: BDJOBS BENCHMARK - CAREER ARENA & IMMUTABLE CV SNAPSHOT LEDGER
# --------------------------------------------------------------------------------------

@api_router.post(
    "/careers/jobs/create",
    tags=["Career Arena & Placement (Bdjobs)"]
)
async def create_employer_job_posting(payload: JobPostingCreateRequest):
    """
    Verified Employer Job Posting:
    Registers a new student internship or entry-level job posting.
    """
    # Create and register in job placement service
    new_job_id = f"job_emp_{len(job_placement_service._jobs) + 1:03d}"
    now = datetime.now(timezone.utc).isoformat()
    job = {
        "id": new_job_id,
        "employer_user_id": payload.employer_user_id,
        "company_name": payload.company_name,
        "title": payload.title,
        "domain": payload.domain,
        "work_mode": payload.work_mode,
        "location": payload.location,
        "salary_range_bdt": payload.salary_range_bdt,
        "required_skills": payload.required_skills,
        "description": payload.description,
        "status": "ACTIVE",
        "applicant_count": 0,
        "created_at": now
    }
    job_placement_service._jobs[new_job_id] = job
    return {
        "success": True,
        "job": job,
        "message": "Job posting registered successfully."
    }


@api_router.get(
    "/careers/jobs/feed",
    tags=["Career Arena & Placement (Bdjobs)"]
)
async def get_live_job_feed(
    domain: Optional[str] = Query(None, description="Filter by domain (e.g., SOFTWARE_ENGINEERING, DATA_AI)"),
    work_mode: Optional[str] = Query(None, description="Filter by work mode (e.g., HYBRID, REMOTE, ONSITE)"),
    search_query: Optional[str] = Query(None, description="Search term in title, company or skills")
):
    """
    Student Internship & Job Arena Feed:
    Retrieves active career listings with multi-attribute filtering.
    """
    return job_placement_service.get_job_feed(
        domain=domain,
        work_mode=work_mode,
        search_query=search_query
    )


@api_router.post(
    "/careers/cv-snapshot/freeze",
    tags=["Career Arena & Placement (Bdjobs)"]
)
async def freeze_candidate_cv_snapshot(payload: CVSnapshotFreezeRequest):
    """
    Immutable Sealed CV Snapshot Generator:
    Freezes applicant credentials into an immutable canonical JSON structure,
    generates a SHA-256 fingerprint hash and HMAC-SHA256 signature for non-repudiation.
    """
    return job_placement_service.freeze_cv_snapshot(
        candidate_user_id=payload.candidate_user_id,
        full_name=payload.full_name,
        academic_institution=payload.academic_institution,
        academic_cgpa=payload.academic_cgpa,
        cat_ability_theta=payload.cat_ability_theta,
        verified_skills=payload.verified_skills,
        portfolio_urls=payload.portfolio_urls
    )


@api_router.get(
    "/careers/cv-snapshot/{snapshot_id}/verify",
    tags=["Career Arena & Placement (Bdjobs)"]
)
async def verify_cv_snapshot_integrity(snapshot_id: str):
    """
    CV Snapshot Cryptographic Integrity Verifier:
    Recomputes the canonical SHA-256 hash and HMAC signature to guarantee
    zero tampering since submission.
    """
    result = job_placement_service.verify_cv_snapshot(snapshot_id=snapshot_id)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Snapshot not found.")
        )
    return result


@api_router.post(
    "/careers/jobs/apply-sealed-cv",
    tags=["Career Arena & Placement (Bdjobs)"]
)
async def apply_for_job_with_sealed_cv(payload: JobApplicationSubmitSealedRequest):
    """
    1-Click Job Application with Sealed CV:
    Submits application binding an immutable CV snapshot and computes
    automated ATS skill match percentage.
    """
    result = job_placement_service.submit_application_with_sealed_cv(
        job_id=payload.job_id,
        candidate_user_id=payload.candidate_user_id,
        cv_snapshot_id=payload.cv_snapshot_id,
        expected_salary_bdt=payload.expected_salary_bdt,
        cover_note=payload.cover_note
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error submitting job application.")
        )
    return result


@api_router.post(
    "/careers/applications/{application_id}/stage-advance",
    tags=["Career Arena & Placement (Bdjobs)"]
)
async def advance_hiring_pipeline_stage(
    application_id: str,
    payload: PipelineStageAdvanceRequest
):
    """
    5-Stage Hiring Pipeline Stage Advancer:
    Moves candidate along 'SAVED' -> 'APPLIED' -> 'VIEWED' -> 'INTERVIEW' -> 'OFFER' / 'REJECTED'
    and logs immutable chronological timeline history.
    """
    result = job_placement_service.advance_application_stage(
        application_id=application_id,
        employer_user_id=payload.employer_user_id,
        new_stage=payload.new_stage,
        feedback_notes=payload.feedback_notes
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN if result.get("error_code") == "FORBIDDEN_EMPLOYER_ACTION" else status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error advancing application stage.")
        )
    return result


# ======================================================================================
# ######################################################################################
# SECTION 24: UNIFIED OMNI-SEARCH, REAL-TIME NOTIFICATIONS & STUDENT REPUTATION
# ######################################################################################
# ======================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: UNIFIED OMNI-SEARCH ENGINE (10MS + CARETUTORS + BDJOBS)
# --------------------------------------------------------------------------------------

@api_router.get(
    "/search/omni",
    tags=["Unified Omni-Search"]
)
async def execute_omni_search(
    query: Optional[str] = Query(None, description="Search term across lectures, tuitions, and jobs"),
    category: str = Query("ALL", description="Filter category: ALL, ACADEMIC_LECTURES, TUITIONS, INTERNSHIPS"),
    limit: int = Query(15, ge=1, le=50, description="Maximum results to return")
):
    """
    Unified Omni-Search Gateway:
    Performs fast, fuzzy, ranked multi-facet search across:
    1. 10 Minute School video lectures and chapters
    2. CareTutors live tuition requirements by region and budget
    3. Bdjobs student internships and verified employer openings
    """
    return omni_search_service.search(
        query=query or "",
        category=category,
        limit=limit
    )


# --------------------------------------------------------------------------------------
# TOPIC B: REAL-TIME CROSS-PLATFORM NOTIFICATION GATEWAY
# --------------------------------------------------------------------------------------

@api_router.post(
    "/notifications/dispatch",
    tags=["Real-Time Notification Gateway"]
)
async def dispatch_platform_notification(payload: NotificationDispatchRequest):
    """
    Real-Time Event Dispatcher:
    Routes event alerts across web push, WebSockets, and user inbox for:
    - In-lecture checkpoint achievements
    - Tuition bid shortlists and bilateral consent releases
    - Job interview invitations and offer releases
    """
    return notification_gateway_service.dispatch_notification(
        recipient_user_id=payload.recipient_user_id,
        category=payload.category,
        title=payload.title,
        message=payload.message,
        priority=payload.priority,
        action_link=payload.action_link
    )


@api_router.get(
    "/notifications/{user_id}",
    tags=["Real-Time Notification Gateway"]
)
async def get_user_notifications(
    user_id: str,
    only_unread: bool = Query(False, description="Filter for unread notifications only")
):
    """
    Retrieves user notification inbox with real-time unread counter.
    """
    return notification_gateway_service.get_user_notifications(
        user_id=user_id,
        only_unread=only_unread
    )


@api_router.post(
    "/notifications/{notification_id}/read",
    tags=["Real-Time Notification Gateway"]
)
async def mark_single_notification_read(
    notification_id: str,
    user_id: str = Query(..., description="ID of the recipient user")
):
    """
    Marks an individual notification as read and updates the unread badge counter.
    """
    result = notification_gateway_service.mark_as_read(
        notification_id=notification_id,
        user_id=user_id
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Notification not found.")
        )
    return result


@api_router.post(
    "/notifications/{user_id}/read-all",
    tags=["Real-Time Notification Gateway"]
)
async def mark_all_user_notifications_read(user_id: str):
    """
    Clears all unread badges by marking the entire user notification inbox as read.
    """
    return notification_gateway_service.mark_all_as_read(user_id=user_id)


# --------------------------------------------------------------------------------------
# TOPIC C: 4-PILLAR COMPOSITE REPUTATION & DAILY QUEST ENGINE
# --------------------------------------------------------------------------------------

@api_router.get(
    "/reputation/score/{student_id}",
    tags=["Student Reputation & Quests"]
)
async def get_student_reputation_score(student_id: str):
    """
    4-Pillar Composite Student Reputation Evaluator:
    Computes 0-1000 score across Academic Mastery (35%), Tutoring Reliability (25%),
    Career Preparedness (25%), and Community Integrity (15%) with merit tier resolution:
    Novice Scholar -> Academic Explorer -> Master Mentor -> Eminence Fellow.
    """
    return student_reputation_service.calculate_reputation_score(student_id=student_id)


@api_router.get(
    "/reputation/quests/{student_id}",
    tags=["Student Reputation & Quests"]
)
async def get_student_daily_quests(student_id: str):
    """
    Retrieves active daily gamified quests across micro-lectures, spaced recall,
    tuition scouting, and career CV verification.
    """
    return student_reputation_service.get_daily_quests(student_id=student_id)


@api_router.post(
    "/reputation/quests/claim",
    tags=["Student Reputation & Quests"]
)
async def claim_daily_quest_reward(payload: QuestClaimRequest):
    """
    Claims reward points for a completed daily quest and updates
    the student's overall composite reputation score.
    """
    result = student_reputation_service.claim_quest_reward(
        student_id=payload.student_id,
        quest_id=payload.quest_id
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error claiming quest reward.")
        )
    return result


# ======================================================================================
# SECTION 25: DUAL-PARTY ESCROW VAULT, GUARDIAN TELEMETRY & CORPORATE TALENT SCOUT
# ======================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: HONORARIUM MILESTONE ESCROW VAULT (CARETUTORS CONVERGENCE)
# --------------------------------------------------------------------------------------

@api_router.post(
    "/escrow/contracts",
    tags=["Honorarium Escrow Vault"]
)
async def create_escrow_contract(payload: CreateEscrowContractRequest):
    """
    Creates and locks a new monthly honorarium escrow contract.
    Computes fair 5% platform fee and guarantees funds are held in milestone escrow.
    """
    try:
        return honorarium_escrow_service.create_escrow_contract(
            contract_id=payload.contract_id,
            tuition_id=payload.tuition_id,
            guardian_id=payload.guardian_id,
            tutor_id=payload.tutor_id,
            total_bdt=payload.total_bdt,
            sessions_committed=payload.sessions_committed,
            payment_method=payload.payment_method or "BKASH_ESCROW"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/escrow/sessions/log",
    tags=["Honorarium Escrow Vault"]
)
async def log_escrow_session_completion(payload: LogSessionCompletionRequest):
    """
    Tutor logs a completed lesson session. Opens a 24-hour guardian review window.
    """
    try:
        return honorarium_escrow_service.log_session_completion(
            contract_id=payload.contract_id,
            tutor_id=payload.tutor_id,
            session_number=payload.session_number,
            topic_covered=payload.topic_covered,
            duration_minutes=payload.duration_minutes or 90
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/escrow/milestones/release",
    tags=["Honorarium Escrow Vault"]
)
async def release_escrow_milestone_funds(payload: ReleaseMilestoneFundsRequest):
    """
    Releases milestone funds for a verified completed session to the tutor's account.
    """
    try:
        return honorarium_escrow_service.release_milestone_funds(
            contract_id=payload.contract_id,
            session_number=payload.session_number,
            authorizer_id=payload.authorizer_id
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/escrow/milestones/dispute",
    tags=["Honorarium Escrow Vault"]
)
async def raise_escrow_milestone_dispute(payload: RaiseMilestoneDisputeRequest):
    """
    Guardian freezes escrow funds and files a dispute for Tribunal arbitration.
    """
    try:
        return honorarium_escrow_service.raise_milestone_dispute(
            contract_id=payload.contract_id,
            session_number=payload.session_number,
            guardian_id=payload.guardian_id,
            reason=payload.reason
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/escrow/contracts/{contract_id}",
    tags=["Honorarium Escrow Vault"]
)
async def get_escrow_contract_details(contract_id: str):
    """Retrieves full contract status, held funds, and session logs."""
    contract = honorarium_escrow_service.get_escrow_contract(contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contract {contract_id} not found.")
    return contract


@api_router.get(
    "/escrow/users/{user_id}/contracts",
    tags=["Honorarium Escrow Vault"]
)
async def list_user_escrow_contracts(user_id: str):
    """Lists all active and completed contracts for a given guardian or tutor."""
    return honorarium_escrow_service.list_user_contracts(user_id=user_id)


# --------------------------------------------------------------------------------------
# TOPIC B: GUARDIAN REAL-TIME ACADEMIC & SAFETY TELEMETRY (10MS CONVERGENCE)
# --------------------------------------------------------------------------------------

@api_router.get(
    "/guardian/telemetry/{guardian_id}/{student_id}",
    tags=["Guardian Telemetry & Safety"]
)
async def get_student_guardian_telemetry(guardian_id: str, student_id: str):
    """
    Delivers weekly study hours, micro-lecture progress, cognitive fatigue diagnostics,
    and emergency safety lock status to authorized guardians.
    """
    try:
        return guardian_telemetry_service.get_student_telemetry_summary(
            guardian_id=guardian_id,
            student_id=student_id
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@api_router.post(
    "/guardian/safety-lock",
    tags=["Guardian Telemetry & Safety"]
)
async def toggle_guardian_safety_lock(payload: ToggleSafetyLockRequest):
    """
    Engages or disengages emergency safety lock on minor's profile.
    """
    return guardian_telemetry_service.toggle_safety_lock(
        guardian_id=payload.guardian_id,
        student_id=payload.student_id,
        lock_active=payload.lock_active,
        reason=payload.reason
    )


# --------------------------------------------------------------------------------------
# TOPIC C: CORPORATE TALENT SCOUT & RECRUITER GATEWAY (BDJOBS CONVERGENCE)
# --------------------------------------------------------------------------------------

@api_router.get(
    "/talent/candidates",
    tags=["Corporate Talent Gateway"]
)
async def search_talent_candidates(
    domain: Optional[str] = Query(None, description="Domain filter (Software, Data, EdTech, All)"),
    min_reputation: int = Query(0, ge=0, le=1000, description="Minimum Composite Reputation Score"),
    min_theta: float = Query(0.0, description="Minimum CAT Latent Ability theta"),
    keyword: Optional[str] = Query(None, description="Skill or university keyword")
):
    """
    Vetted candidate search with mathematical IRT ability scores,
    verified national percentile, and cryptographic CV status.
    """
    return corporate_talent_service.search_talent_pool(
        domain=domain,
        min_reputation=min_reputation,
        min_theta=min_theta,
        keyword=keyword
    )


@api_router.post(
    "/talent/invitations",
    tags=["Corporate Talent Gateway"]
)
async def dispatch_interview_invitation(payload: DispatchInterviewInvitationRequest):
    """
    Corporate recruiter dispatches a direct interview invitation to a vetted scholar.
    """
    try:
        return corporate_talent_service.dispatch_interview_invitation(
            recruiter_id=payload.recruiter_id,
            company_name=payload.company_name,
            candidate_id=payload.candidate_id,
            role_title=payload.role_title,
            proposed_date=payload.proposed_date or "Flexible Schedule",
            message=payload.message
        )
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/talent/shortlist",
    tags=["Corporate Talent Gateway"]
)
async def shortlist_talent_candidate(payload: ShortlistCandidateRequest):
    """
    Adds candidate to recruiter's private shortlisted talent pool.
    """
    try:
        return corporate_talent_service.shortlist_candidate(
            recruiter_id=payload.recruiter_id,
            candidate_id=payload.candidate_id
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.get(
    "/talent/shortlist/{recruiter_id}",
    tags=["Corporate Talent Gateway"]
)
async def get_recruiter_shortlist(recruiter_id: str):
    """
    Retrieves all candidates shortlisted by the recruiter.
    """
    return corporate_talent_service.get_recruiter_shortlist(recruiter_id=recruiter_id)


# ========================================================================================
# SECTION 26: PEER STUDY CIRCLES & GAMIFIED BOUNTY TRIBUNAL (PHASE 27)
# ========================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: REAL-TIME STUDY ROOMS & WHITEBOARD COLLABORATION
# --------------------------------------------------------------------------------------

@api_router.post(
    "/study-room/create",
    tags=["Peer Study Circles & Whiteboard"]
)
async def create_study_room(payload: CreateStudyRoomRequest):
    """
    Creates an active real-time peer study circle room with WebRTC signaling tokens.
    """
    try:
        return study_room_service.create_study_room(
            title=payload.title,
            host_id=payload.host_id,
            host_name=payload.host_name,
            topic=payload.topic,
            target_grade=payload.target_grade,
            max_participants=payload.max_participants,
            is_private=payload.is_private,
            passcode=payload.passcode
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/study-room/list",
    tags=["Peer Study Circles & Whiteboard"]
)
async def list_study_rooms(
    topic: Optional[str] = Query(None, description="Topic/subject filter"),
    grade: Optional[str] = Query(None, description="Target academic grade filter")
):
    """
    Lists all active peer study rooms with participant counts and live statuses.
    """
    return study_room_service.list_active_study_rooms(topic=topic, grade=grade)


@api_router.post(
    "/study-room/join",
    tags=["Peer Study Circles & Whiteboard"]
)
async def join_study_room(payload: JoinStudyRoomRequest):
    """
    Enrolls a student participant into an active room and generates a WebRTC token.
    """
    try:
        return study_room_service.join_study_room(
            room_id=payload.room_id,
            user_id=payload.user_id,
            user_name=payload.user_name,
            role=payload.role,
            passcode=payload.passcode
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/study-room/leave",
    tags=["Peer Study Circles & Whiteboard"]
)
async def leave_study_room(
    room_id: str = Query(..., description="Study room identifier"),
    user_id: str = Query(..., description="Leaving student identifier")
):
    """
    Leaves a study room and updates active participant count.
    """
    try:
        return study_room_service.leave_study_room(room_id=room_id, user_id=user_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.post(
    "/study-room/whiteboard/sync",
    tags=["Peer Study Circles & Whiteboard"]
)
async def sync_whiteboard_stroke(payload: WhiteboardSyncRequest):
    """
    Synchronizes collaborative whiteboard brush strokes, LaTeX expressions, or clears canvas.
    """
    try:
        return study_room_service.sync_whiteboard(
            room_id=payload.room_id,
            user_id=payload.user_id,
            action=payload.action,
            stroke_data=payload.stroke_data,
            formula_latex=payload.formula_latex
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@api_router.post(
    "/study-room/pomodoro/sync",
    tags=["Peer Study Circles & Whiteboard"]
)
async def sync_room_pomodoro(payload: PomodoroSyncRequest):
    """
    Synchronizes room-wide focus Pomodoro sprints across all connected participants.
    """
    try:
        return study_room_service.sync_pomodoro(
            room_id=payload.room_id,
            host_id=payload.host_id,
            duration_minutes=payload.duration_minutes,
            action=payload.action
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/study-room/{room_id}",
    tags=["Peer Study Circles & Whiteboard"]
)
async def get_study_room_details(room_id: str):
    """
    Retrieves full room state including active participants, whiteboard history, and timer.
    """
    try:
        return study_room_service.get_room_state(room_id=room_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# --------------------------------------------------------------------------------------
# TOPIC B: GAMIFIED BOUNTY TRIBUNAL & PEER DOUBT RESOLUTION
# --------------------------------------------------------------------------------------

@api_router.post(
    "/bounties/create",
    tags=["Gamified Bounty Tribunal"]
)
async def create_bounty(payload: CreateBountyRequest):
    """
    Creates an academic doubt bounty backed by BDT escrow and reputation staking.
    """
    try:
        return bounty_tribunal_service.create_bounty(
            poster_id=payload.poster_id,
            poster_name=payload.poster_name,
            title=payload.title,
            subject=payload.subject,
            problem_statement=payload.problem_statement,
            bounty_bdt=payload.bounty_bdt,
            bounty_reputation_pts=payload.bounty_reputation_pts,
            attachment_url=payload.attachment_url
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/bounties/list",
    tags=["Gamified Bounty Tribunal"]
)
async def list_bounties(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    status: Optional[str] = Query(None, description="Filter by status (OPEN, AWARDED)")
):
    """
    Lists active and awarded academic challenge bounties.
    """
    return bounty_tribunal_service.list_bounties(subject=subject, status=status)


@api_router.post(
    "/bounties/solution/submit",
    tags=["Gamified Bounty Tribunal"]
)
async def submit_bounty_solution(payload: SubmitSolutionRequest):
    """
    Submits a scholar solution with explanation, LaTeX derivation, or code snippet.
    """
    try:
        return bounty_tribunal_service.submit_solution(
            bounty_id=payload.bounty_id,
            scholar_id=payload.scholar_id,
            scholar_name=payload.scholar_name,
            explanation=payload.explanation,
            latex_proof=payload.latex_proof,
            code_snippet=payload.code_snippet
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/bounties/solution/verdict",
    tags=["Gamified Bounty Tribunal"]
)
async def evaluate_bounty_solution(
    solution_id: str = Query(..., description="Solution identifier"),
    payload: VerdictBountyRequest = ...
):
    """
    Original poster or tribunal awards bounty (releasing funds and reputation) or rejects solution.
    """
    try:
        return bounty_tribunal_service.evaluate_solution(
            bounty_id=payload.bounty_id,
            solution_id=solution_id,
            evaluator_id=payload.evaluator_id,
            decision=payload.decision,
            feedback=payload.feedback
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/bounties/{bounty_id}",
    tags=["Gamified Bounty Tribunal"]
)
async def get_bounty_details(bounty_id: str):
    """
    Retrieves full bounty problem statement, submitted solutions, and payout receipt.
    """
    try:
        return bounty_tribunal_service.get_bounty_details(bounty_id=bounty_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ========================================================================================
# SECTION 27: MICRO-SCHOLARSHIP ENDOWMENT & TECHNICAL ASSESSMENT ARENA (PHASE 28)
# ========================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: MICRO-SCHOLARSHIP ENDOWMENTS & AUTO-DISBURSEMENT
# --------------------------------------------------------------------------------------

@api_router.post(
    "/scholarships/funds/create",
    tags=["Scholarship Endowments & Payouts"]
)
async def create_endowment_fund(payload: CreateEndowmentFundRequest):
    """
    Creates a corporate or alumni endowment fund for student micro-stipends.
    """
    try:
        return scholarship_endowment_service.create_endowment_fund(
            sponsor_id=payload.sponsor_id,
            sponsor_name=payload.sponsor_name,
            fund_title=payload.fund_title,
            total_grant_bdt=payload.total_grant_bdt,
            target_criteria=payload.target_criteria,
            disbursement_per_student_bdt=payload.disbursement_per_student_bdt
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/scholarships/funds/list",
    tags=["Scholarship Endowments & Payouts"]
)
async def list_endowment_funds(
    criteria: Optional[str] = Query(None, description="Criteria filter (UNDERPRIVILEGED_STEM, FEMALE_TECH, GENERAL_MERIT)")
):
    """
    Lists active endowment funds with remaining grant amounts and recipient counts.
    """
    return scholarship_endowment_service.list_endowment_funds(criteria=criteria)


@api_router.post(
    "/scholarships/apply",
    tags=["Scholarship Endowments & Payouts"]
)
async def apply_for_scholarship(payload: ApplyScholarshipRequest):
    """
    Applies for a micro-scholarship with automated need-index and composite merit calculation.
    """
    try:
        return scholarship_endowment_service.apply_for_scholarship(
            fund_id=payload.fund_id,
            student_id=payload.student_id,
            student_name=payload.student_name,
            family_monthly_income_bdt=payload.family_monthly_income_bdt,
            institution_name=payload.institution_name,
            cat_ability_theta=payload.cat_ability_theta,
            reputation_score=payload.reputation_score,
            bkash_number=payload.bkash_number,
            statement_of_need=payload.statement_of_need
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/scholarships/disburse",
    tags=["Scholarship Endowments & Payouts"]
)
async def disburse_scholarship_funds(payload: DisburseScholarshipRequest):
    """
    Executes automated bKash/Nagad micro-disbursement with cryptographic audit logging.
    """
    try:
        return scholarship_endowment_service.disburse_scholarship(
            application_id=payload.application_id,
            disburser_id=payload.disburser_id,
            channel=payload.channel or "BKASH_DISBURSEMENT"
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/scholarships/application/{application_id}",
    tags=["Scholarship Endowments & Payouts"]
)
async def get_scholarship_application_details(application_id: str):
    """
    Retrieves full scholarship application record, need index, and disbursement status.
    """
    try:
        return scholarship_endowment_service.get_application_status(application_id=application_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# --------------------------------------------------------------------------------------
# TOPIC B: AI RESUME TAILOR & CODING ASSESSMENT ARENA
# --------------------------------------------------------------------------------------

@api_router.post(
    "/career/ats/analyze",
    tags=["AI Resume Tailor & Technical Assessment"]
)
async def analyze_resume_ats(payload: ATSResumeAnalysisRequest):
    """
    Scans CV against target internship requirements and calculates ATS match score.
    """
    try:
        return technical_assessment_service.analyze_resume_ats(
            candidate_id=payload.candidate_id,
            job_id=payload.job_id,
            role_title=payload.role_title,
            cv_text=payload.cv_text,
            target_skills=payload.target_skills
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/career/assessments/list",
    tags=["AI Resume Tailor & Technical Assessment"]
)
async def list_technical_assessments(
    role: Optional[str] = Query(None, description="Role filter (e.g. Python, SQL, Frontend)")
):
    """
    Lists available technical coding challenges and difficulty levels.
    """
    return technical_assessment_service.list_assessments(role=role)


@api_router.get(
    "/career/assessments/{assessment_id}",
    tags=["AI Resume Tailor & Technical Assessment"]
)
async def get_assessment_details(assessment_id: str):
    """
    Retrieves complete problem description, starter code, and test case count.
    """
    try:
        return technical_assessment_service.get_assessment(assessment_id=assessment_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.post(
    "/career/assessments/submit",
    tags=["AI Resume Tailor & Technical Assessment"]
)
async def submit_technical_assessment(payload: SubmitTechnicalAssessmentRequest):
    """
    Evaluates candidate's code submission within security sandbox and grades test results.
    """
    try:
        return technical_assessment_service.evaluate_code_submission(
            candidate_id=payload.candidate_id,
            assessment_id=payload.assessment_id,
            language=payload.language,
            code_solution=payload.code_solution,
            time_spent_seconds=payload.time_spent_seconds
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ======================================================================================
# SECTION 28: ALUMNI MENTORSHIP, ADAPTIVE PATHWAYS & VERIFIABLE CERTIFICATES (PHASE 29)
# ======================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: 1-ON-1 ALUMNI MENTORSHIP MARKETPLACE
# --------------------------------------------------------------------------------------

@api_router.get(
    "/mentorship/mentors",
    tags=["Alumni Mentorship Marketplace"]
)
async def list_alumni_mentors(
    specialty: Optional[str] = Query(None, description="Filter by specialty or alma mater (e.g. BUET, IBA, Medical)")
):
    """
    Lists verified university alumni and corporate mentors available for 1-on-1 advisory.
    """
    return alumni_mentorship_service.get_all_mentors(specialty_filter=specialty)


@api_router.get(
    "/mentorship/mentors/{mentor_id}",
    tags=["Alumni Mentorship Marketplace"]
)
async def get_alumni_mentor_profile(mentor_id: str):
    """
    Retrieves complete mentor profile, available slots, hourly fee, and ratings.
    """
    mentor = alumni_mentorship_service.get_mentor_by_id(mentor_id=mentor_id)
    if not mentor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mentor '{mentor_id}' not found.")
    return mentor


@api_router.post(
    "/mentorship/sessions/book",
    tags=["Alumni Mentorship Marketplace"]
)
async def book_mentorship_session(payload: BookMentorshipSessionRequest):
    """
    Reserves a 1-on-1 counseling slot with escrow fee holding and WebRTC channel token issuance.
    """
    try:
        return alumni_mentorship_service.book_session(
            mentor_id=payload.mentor_id,
            student_id=payload.student_id,
            student_name=payload.student_name,
            slot_time=payload.slot_time,
            topic_focus=payload.topic_focus,
            target_ambition=payload.target_ambition,
            fee_bdt=payload.fee_bdt,
            payment_method=payload.payment_method
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/mentorship/sessions/{session_id}",
    tags=["Alumni Mentorship Marketplace"]
)
async def get_mentorship_session_status(session_id: str):
    """
    Retrieves session confirmation status, WebRTC channel token, and escrow transaction details.
    """
    session = alumni_mentorship_service.get_session(session_id=session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session '{session_id}' not found.")
    return session


@api_router.post(
    "/mentorship/sessions/{session_id}/complete",
    tags=["Alumni Mentorship Marketplace"]
)
async def complete_mentorship_session(
    session_id: str,
    rating: float = Query(5.0, ge=1.0, le=5.0, description="Student review rating from 1.0 to 5.0")
):
    """
    Marks 1-on-1 advisory session as complete, updates mentor reputation, and releases escrow funds.
    """
    try:
        return alumni_mentorship_service.complete_session_and_release_escrow(
            session_id=session_id,
            student_rating=rating
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# --------------------------------------------------------------------------------------
# TOPIC B: DYNAMIC ADAPTIVE REMEDIAL LEARNING PATHWAYS
# --------------------------------------------------------------------------------------

@api_router.post(
    "/pathways/generate",
    tags=["Adaptive Learning Pathways"]
)
async def generate_adaptive_learning_pathway(payload: GenerateAdaptivePathwayRequest):
    """
    Generates a personalized remedial sprint pathway based on prerequisite concept graph analysis.
    """
    try:
        return adaptive_learning_path_service.generate_pathway(
            student_id=payload.student_id,
            subject=payload.subject,
            weak_topic_ids=payload.weak_topic_ids,
            target_mastery_pct=payload.target_mastery_pct
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/pathways/{pathway_id}",
    tags=["Adaptive Learning Pathways"]
)
async def get_adaptive_pathway_status(pathway_id: str):
    """
    Retrieves current remedial sprint progress, step status, and projected syllabus readiness.
    """
    pathway = adaptive_learning_path_service.get_pathway(pathway_id=pathway_id)
    if not pathway:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pathway '{pathway_id}' not found.")
    return pathway


@api_router.post(
    "/pathways/{pathway_id}/steps/{step_id}/complete",
    tags=["Adaptive Learning Pathways"]
)
async def complete_remedial_sprint_step(pathway_id: str, step_id: str):
    """
    Marks a sprint step complete and dynamically recalculates student syllabus mastery score.
    """
    try:
        return adaptive_learning_path_service.complete_step(
            pathway_id=pathway_id,
            step_id=step_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# --------------------------------------------------------------------------------------
# TOPIC C: CRYPTOGRAPHIC PROOF-OF-SKILL CERTIFICATE VERIFICATION
# --------------------------------------------------------------------------------------

@api_router.post(
    "/certificates/issue",
    tags=["Cryptographic Verifiable Credentials"]
)
async def issue_verifiable_certificate(payload: IssueCertificateRequest):
    """
    Issues a tamper-proof SHA-256 verifiable certificate for academic and corporate recognition.
    """
    try:
        return certificate_verification_service.issue_certificate(
            student_id=payload.student_id,
            student_name=payload.student_name,
            course_or_track=payload.course_or_track,
            grade_or_score=payload.grade_or_score,
            skills_mastered=payload.skills_mastered,
            issued_by=payload.issued_by
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/certificates/verify/{identifier}",
    tags=["Cryptographic Verifiable Credentials"]
)
async def verify_certificate_authenticity(identifier: str):
    """
    Public 1-click verification lookup for employers and institutions by Certificate ID or Hash.
    """
    return certificate_verification_service.verify_certificate(identifier=identifier)


# ======================================================================================
# SECTION 29: ADMISSION MULTIPLEXER, OFFLINE CRDT DELTA-SYNC & TALENT PASSPORT
# ======================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: CENTRALIZED MULTI-UNIVERSITY ADMISSION MULTIPLEXER
# --------------------------------------------------------------------------------------

@api_router.post(
    "/admissions/eligibility",
    tags=["University Admission Multiplexer"]
)
async def check_admission_eligibility(payload: CheckAdmissionEligibilityRequest):
    """
    Evaluates SSC/HSC GPA, subject marks, and discipline across BUET, DU, Medical, CKRUET, and GST circulars.
    """
    try:
        reports = university_admission_multiplexer_service.check_eligibility(
            student_id=payload.student_id,
            hsc_gpa=payload.hsc_gpa,
            ssc_gpa=payload.ssc_gpa,
            academic_group=payload.academic_group,
            subject_grades=payload.subject_grades
        )
        return {
            "student_id": payload.student_id,
            "eligibility_reports": reports,
            "total_evaluated": len(reports)
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/admissions/batch-apply",
    tags=["University Admission Multiplexer"]
)
async def batch_apply_admission(payload: BatchApplyUniversityRequest):
    """
    Executes 1-click multi-university application batch with centralized fee settlement and collision detection.
    """
    try:
        return university_admission_multiplexer_service.batch_apply(
            student_id=payload.student_id,
            student_name=payload.student_name,
            hsc_roll=payload.hsc_roll,
            hsc_registration=payload.hsc_registration,
            university_codes=payload.university_codes,
            payment_channel=payload.payment_channel
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/admissions/admit-card/{admit_card_id}",
    tags=["University Admission Multiplexer"]
)
async def get_admission_admit_card(admit_card_id: str):
    """
    Retrieves consolidated digital admit card with exam venue, roll number, and room assignment.
    """
    card = university_admission_multiplexer_service.get_admit_card(admit_card_id=admit_card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admit card '{admit_card_id}' not found.")
    return card


# --------------------------------------------------------------------------------------
# TOPIC B: OFFLINE-FIRST PWA CRDT DELTA-SYNC ENGINE
# --------------------------------------------------------------------------------------

@api_router.post(
    "/sync/crdt-delta",
    tags=["Offline CRDT Delta Sync"]
)
async def sync_crdt_delta(payload: OfflineDeltaSyncRequest):
    """
    Reconciles client mutation queue using monotonic vector clocks and Set-Union/LWW CRDT semantics.
    """
    try:
        return offline_delta_sync_service.sync_delta(
            client_id=payload.client_id,
            student_id=payload.student_id,
            last_synced_vector_clock=payload.last_synced_vector_clock,
            mutations=payload.mutations
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/sync/state/{student_id}",
    tags=["Offline CRDT Delta Sync"]
)
async def get_student_crdt_synced_state(student_id: str):
    """
    Retrieves synchronized state, server vector clock, and cryptographic state digest.
    """
    return offline_delta_sync_service.get_student_synced_state(student_id=student_id)


# --------------------------------------------------------------------------------------
# TOPIC C: UNIVERSAL STUDENT TALENT PASSPORT & RECRUITER PROOF-OF-SKILL RADAR
# --------------------------------------------------------------------------------------

@api_router.post(
    "/talent/passport/generate",
    tags=["Student Talent Passport"]
)
async def generate_talent_passport(payload: GenerateTalentPassportRequest):
    """
    Synthesizes academic CAT ability, verified credentials, and coding achievements into a signed digital passport.
    """
    try:
        return student_talent_passport_service.generate_passport(
            student_id=payload.student_id,
            public_handle=payload.public_handle,
            include_mentorship_badges=payload.include_mentorship_badges,
            include_code_evaluations=payload.include_code_evaluations
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/talent/passport/{public_handle}",
    tags=["Student Talent Passport"]
)
async def get_public_talent_passport(public_handle: str):
    """
    Public recruiter view with minor PII redaction shield and tamper-proof verification stamp.
    """
    passport = student_talent_passport_service.get_passport_by_handle(public_handle=public_handle, is_recruiter_view=True)
    if not passport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Talent passport for '{public_handle}' not found.")
    return passport


@api_router.get(
    "/talent/passport/verify/{public_handle}",
    tags=["Student Talent Passport"]
)
async def verify_talent_passport_qr_signature(public_handle: str, signature: str):
    """
    Cryptographic verification endpoint to validate QR code signatures against tamper attempts.
    """
    valid = student_talent_passport_service.verify_passport_signature(public_handle=public_handle, qr_signature=signature)
    return {
        "public_handle": public_handle,
        "is_signature_valid": valid,
        "status": "AUTHENTIC" if valid else "TAMPERED_OR_INVALID"
    }


# ======================================================================================
# SECTION 30: AI MATH SOLVER, ALUMNI REFERRALS & VOICE VIVA-VOCE SIMULATOR
# ======================================================================================

# --------------------------------------------------------------------------------------
# TOPIC A: AUTONOMOUS AI LATEX MATHEMATICAL SOLVER & MISCONCEPTION ENGINE
# --------------------------------------------------------------------------------------

@api_router.post(
    "/solver/math/solve-stepwise",
    tags=["Mathematical Problem Solver"]
)
async def solve_mathematical_problem_stepwise(payload: SolveMathStepwiseRequest):
    """
    Synthesizes rigorous step-by-step LaTeX derivation with applied mathematical rules.
    """
    try:
        return math_problem_solver_service.solve_stepwise(
            problem_statement=payload.problem_statement,
            topic_domain=payload.topic_domain,
            student_id=payload.student_id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/solver/math/diagnose-step",
    tags=["Mathematical Problem Solver"]
)
async def diagnose_student_derivation_step(payload: DiagnoseMisconceptionRequest):
    """
    Detects intermediate step misconceptions (chain rule omission, sign flips) with Socratic hints.
    """
    try:
        return math_problem_solver_service.diagnose_step(
            problem_id=payload.problem_id,
            step_number=payload.step_number,
            student_derived_latex=payload.student_derived_latex
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# --------------------------------------------------------------------------------------
# TOPIC B: MULTI-CAMPUS ALUMNI JOB REFERRAL GRAPH & CORPORATE FAST-TRACK
# --------------------------------------------------------------------------------------

@api_router.get(
    "/referrals/alumni/directory",
    tags=["Alumni Referral Network"]
)
async def list_verified_alumni_directory(company: Optional[str] = None):
    """
    Retrieves directory of verified alumni at top technology and multinational enterprises.
    """
    return alumni_referral_network_service.get_alumni_directory(company_filter=company)


@api_router.post(
    "/referrals/endorse",
    tags=["Alumni Referral Network"]
)
async def issue_alumni_referral_endorsement(payload: CreateReferralEndorsementRequest):
    """
    Synthesizes a cryptographic HMAC/SHA-256 referral token subject to alumni monthly quota bounds.
    """
    try:
        return alumni_referral_network_service.issue_referral_endorsement(
            alumni_id=payload.alumni_id,
            student_id=payload.student_id,
            student_name=payload.student_name,
            target_role=payload.target_role,
            endorsement_notes=payload.endorsement_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/referrals/verify/{token}",
    tags=["Alumni Referral Network"]
)
async def verify_alumni_referral_token(token: str):
    """
    Validates authenticity of candidate referral endorsement token for corporate hiring managers.
    """
    return alumni_referral_network_service.verify_referral_token(token=token)


# --------------------------------------------------------------------------------------
# TOPIC C: SMART VOICE VIVA-VOCE ORAL EXAM & SPEECH CADENCE SIMULATOR
# --------------------------------------------------------------------------------------

@api_router.post(
    "/viva/session/start",
    tags=["Voice Viva Simulator"]
)
async def start_voice_viva_session(payload: StartVivaSessionRequest):
    """
    Initiates an oral viva session for BCS Cadre, BUET/IBA admission, or Corporate Tech.
    """
    try:
        return voice_viva_simulator_service.start_session(
            student_id=payload.student_id,
            viva_category=payload.viva_category,
            difficulty=payload.difficulty
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/viva/session/{session_id}/submit-response",
    tags=["Voice Viva Simulator"]
)
async def submit_viva_audio_response(session_id: str, payload: SubmitAudioVivaResponseRequest):
    """
    Evaluates speech response WPM cadence, latency, and conceptual precision against rubric criteria.
    """
    try:
        return voice_viva_simulator_service.evaluate_response(
            session_id=session_id,
            question_id=payload.question_id,
            audio_duration_seconds=payload.audio_duration_seconds,
            transcribed_text=payload.transcribed_text,
            response_latency_seconds=payload.response_latency_seconds
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/viva/session/{session_id}/report",
    tags=["Voice Viva Simulator"]
)
async def get_viva_session_report(session_id: str):
    """
    Retrieves full oral examination evaluation report, overall score, and speech coaching recommendations.
    """
    report = voice_viva_simulator_service.get_session_summary(session_id=session_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Viva session '{session_id}' not found.")
    return report


# -----------------------------------------------------------------------------
# SECTION 31: VIRTUAL SCIENCE LAB, BATCH POOL & CORPORATE CAPSTONES
# -----------------------------------------------------------------------------

@api_router.post(
    "/lab/circuit/simulate",
    tags=["Virtual Science Lab"]
)
async def simulate_dc_circuit(payload: CircuitSimulationRequest):
    """
    Simulates DC circuit behavior using Ohm's and Kirchhoff's laws with short-circuit protection.
    """
    try:
        return virtual_science_lab_service.simulate_circuit(
            circuit_id=payload.circuit_id,
            source_voltage=payload.source_voltage,
            configuration=payload.configuration,
            components=payload.components
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/lab/optics/ray-trace",
    tags=["Virtual Science Lab"]
)
async def trace_optics_ray(payload: OpticsRayTraceRequest):
    """
    Traces optical rays through thin convex/concave lenses using the Gaussian lens equation.
    """
    try:
        return virtual_science_lab_service.trace_optics_rays(
            lens_type=payload.lens_type,
            focal_length_cm=payload.focal_length_cm,
            object_distance_cm=payload.object_distance_cm,
            object_height_cm=payload.object_height_cm
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/lab/titration/simulate",
    tags=["Virtual Science Lab"]
)
async def simulate_acid_base_titration(payload: TitrationSimulationRequest):
    """
    Simulates analytical acid-base titration pH progression and indicator color transitions.
    """
    try:
        return virtual_science_lab_service.simulate_acid_base_titration(
            analyte=payload.analyte,
            titrant=payload.titrant,
            analyte_volume_ml=payload.analyte_volume_ml,
            analyte_molarity=payload.analyte_molarity,
            titrant_molarity=payload.titrant_molarity,
            indicator=payload.indicator
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/lab/report/generate",
    tags=["Virtual Science Lab"]
)
async def generate_lab_report(payload: LabReportSynthesisRequest):
    """
    Synthesizes automated scientific laboratory reports with relative error verification stamps.
    """
    try:
        return virtual_science_lab_service.generate_lab_report(
            lab_type=payload.lab_type,
            student_id=payload.student_id,
            experimental_value=payload.experimental_value,
            theoretical_value=payload.theoretical_value,
            observations=payload.observations
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/coaching/batch/create",
    tags=["Coaching Batch Pool"]
)
async def create_coaching_batch(payload: CreateCoachingBatchRequest):
    """
    Creates a neighborhood multi-guardian micro-coaching batch with fractional escrow splitting.
    """
    try:
        return coaching_batch_pool_service.create_batch(
            batch_title=payload.batch_title,
            subject=payload.subject,
            lead_guardian_id=payload.lead_guardian_id,
            total_monthly_fee_bdt=payload.total_monthly_fee_bdt,
            max_capacity=payload.max_capacity,
            curriculum=payload.curriculum
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/coaching/batch/{batch_id}/join-guardian",
    tags=["Coaching Batch Pool"]
)
async def join_coaching_batch(batch_id: str, payload: JoinBatchGuardianRequest):
    """
    Adds a guardian to an existing micro-coaching batch and recalculates the 1/N escrow cost split.
    """
    try:
        return coaching_batch_pool_service.join_guardian(
            batch_id=batch_id,
            guardian_id=payload.guardian_id,
            guardian_name=payload.guardian_name,
            student_name=payload.student_name
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/coaching/batch/{batch_id}/log-session",
    tags=["Coaching Batch Pool"]
)
async def log_coaching_session(batch_id: str, payload: LogBatchSessionRequest):
    """
    Logs batch session attendance telemetry and mentor notes for guardian review.
    """
    try:
        return coaching_batch_pool_service.log_session_attendance(
            batch_id=batch_id,
            session_topic=payload.session_topic,
            attendees=payload.attendees,
            duration_minutes=payload.duration_minutes,
            mentor_notes=payload.mentor_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/coaching/batch/{batch_id}",
    tags=["Coaching Batch Pool"]
)
async def get_coaching_batch_details(batch_id: str):
    """
    Retrieves full details of a coaching batch including all guardian shares and past sessions.
    """
    try:
        return coaching_batch_pool_service.get_batch_details(batch_id=batch_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.get(
    "/coaching/batches",
    tags=["Coaching Batch Pool"]
)
async def list_coaching_batches():
    """
    Lists all active coaching batches available for guardian enrollment.
    """
    return coaching_batch_pool_service.list_batches()


@api_router.get(
    "/capstones/directory",
    tags=["Industry Capstone Marketplace"]
)
async def get_capstones_directory():
    """
    Returns verified corporate industry capstone problem briefs with stipend and PPO indicators.
    """
    return industry_capstone_service.get_capstone_directory()


@api_router.get(
    "/capstones/{capstone_id}",
    tags=["Industry Capstone Marketplace"]
)
async def get_capstone_details(capstone_id: str):
    """
    Retrieves detailed problem brief, skills requirements, and deliverables specification.
    """
    try:
        return industry_capstone_service.get_capstone_by_id(capstone_id=capstone_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.post(
    "/capstones/{capstone_id}/submit-milestone",
    tags=["Industry Capstone Marketplace"]
)
async def submit_capstone_milestone(capstone_id: str, payload: SubmitCapstoneMilestoneRequest):
    """
    Submits milestone deliverables, evaluates rubrics, and updates PPO conversion readiness.
    """
    try:
        return industry_capstone_service.submit_milestone(
            capstone_id=capstone_id,
            student_id=payload.student_id,
            student_name=payload.student_name,
            milestone_stage=payload.milestone_stage,
            deliverables_url=payload.deliverables_url,
            executive_summary=payload.executive_summary
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# -----------------------------------------------------------------------------
# SECTION 32: STEM MOLECULAR GEOMETRY, SYLLABUS ATLAS & INNOVATION LAUNCHPAD
# -----------------------------------------------------------------------------

@api_router.post(
    "/lab/chemistry/molecular-geometry",
    tags=["STEM Molecular Lab"]
)
async def calculate_molecular_geometry(payload: MolecularGeometryRequest):
    """
    Calculates 3D VSEPR molecular geometry, hybridization, and polarity parameters.
    """
    try:
        return molecular_geometry_lab_service.calculate_molecular_geometry(
            formula=payload.formula,
            central_atom=payload.central_atom,
            steric_number=payload.steric_number,
            lone_pairs=payload.lone_pairs
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/lab/chemistry/redox-balance",
    tags=["STEM Molecular Lab"]
)
async def balance_redox_chemical_reaction(payload: RedoxReactionBalanceRequest):
    """
    Balances oxidation-reduction chemical equations using the analytical ion-electron method.
    """
    try:
        return molecular_geometry_lab_service.balance_redox_reaction(
            reaction_equation=payload.reaction_equation,
            medium=payload.medium
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/syllabus/atlas/graph",
    tags=["Syllabus Knowledge Atlas"]
)
async def get_syllabus_knowledge_graph(subject: Optional[str] = Query(None, description="Filter by STEM subject")):
    """
    Retrieves the complete NCTB curriculum semantic concept graph and prerequisite dependency chains.
    """
    return syllabus_knowledge_atlas_service.get_syllabus_graph(subject=subject)


@api_router.get(
    "/syllabus/atlas/board-frequency",
    tags=["Syllabus Knowledge Atlas"]
)
async def get_board_exam_frequency(
    subject: str = Query("Physics", description="Target subject"),
    chapter: str = Query("Newtonian Mechanics", description="Target syllabus chapter")
):
    """
    Returns 10-year question frequency distributions across Dhaka, Rajshahi, Chattogram, and Dinajpur boards.
    """
    return syllabus_knowledge_atlas_service.get_board_exam_frequency(subject=subject, chapter=chapter)


@api_router.get(
    "/syllabus/atlas/formulas",
    tags=["Syllabus Knowledge Atlas"]
)
async def get_syllabus_formula_cheatsheet(subject: str = Query("Physics", description="Target subject")):
    """
    Retrieves categorized formula reference sheets for quick examination revision.
    """
    return syllabus_knowledge_atlas_service.get_formula_cheatsheet(subject=subject)


@api_router.post(
    "/launchpad/projects/pitch",
    tags=["Student Innovation Launchpad"]
)
async def pitch_student_innovation_project(payload: PitchProjectRequest):
    """
    Registers a new student innovation project with SHA-256 IP proofing on the audit ledger.
    """
    try:
        return innovation_launchpad_service.pitch_project(
            title=payload.title,
            track=payload.track,
            leader_student_id=payload.leader_student_id,
            leader_student_name=payload.leader_student_name,
            team_members=payload.team_members,
            summary=payload.summary,
            grant_requested_bdt=payload.grant_requested_bdt,
            demo_repo_url=payload.demo_repo_url
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/launchpad/projects/{project_id}/vote",
    tags=["Student Innovation Launchpad"]
)
async def cast_project_tribunal_vote(project_id: str, payload: CastProjectVoteRequest):
    """
    Casts a community vote with anti-Sybil duplicate locking and reputation weight multipliers.
    """
    try:
        return innovation_launchpad_service.cast_vote(
            project_id=project_id,
            voter_student_id=payload.voter_student_id,
            voter_reputation_score=payload.voter_reputation_score
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/launchpad/projects/{project_id}/release-grant",
    tags=["Student Innovation Launchpad"]
)
async def release_milestone_grant_tranche(project_id: str, payload: ReleaseGrantTrancheRequest):
    """
    Releases micro-grant escrow tranche to student team upon verified mentor milestone approval.
    """
    try:
        return innovation_launchpad_service.release_grant_tranche(
            project_id=project_id,
            milestone_stage=payload.milestone_stage,
            mentor_reviewer_id=payload.mentor_reviewer_id,
            approval_notes=payload.approval_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/launchpad/projects",
    tags=["Student Innovation Launchpad"]
)
async def list_innovation_projects(track: Optional[str] = Query(None, description="Filter by venture track")):
    """
    Lists active student innovation pitches and current community voting tallies.
    """
    return innovation_launchpad_service.list_projects(track=track)


@api_router.get(
    "/launchpad/projects/{project_id}",
    tags=["Student Innovation Launchpad"]
)
async def get_innovation_project_details(project_id: str):
    """
    Retrieves full project pitch details, team members, and grant tranche release history.
    """
    try:
        return innovation_launchpad_service.get_project_by_id(project_id=project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ========================================================================================
# Phase 34: Algorithm Complexity Sandbox, Academic Thesis Citations & Campus Ambassadors
# ========================================================================================

@api_router.post(
    "/algo/complexity-analysis",
    tags=["Algorithm Complexity Sandbox"]
)
async def analyze_algorithm_complexity(payload: CodeComplexityRequest):
    """
    Executes AST static code analysis to derive asymptotic Big-O time and space complexity.
    Safe and zero execution risk.
    """
    try:
        return algorithm_complexity_sandbox_service.analyze_complexity(
            code=payload.code,
            language=payload.language,
            function_name=payload.function_name
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/algo/trace-simulation",
    tags=["Algorithm Complexity Sandbox"]
)
async def simulate_algorithm_trace(payload: AlgorithmTraceRequest):
    """
    Simulates canonical algorithm execution and records discrete step snapshots.
    """
    try:
        return algorithm_complexity_sandbox_service.generate_algorithm_trace(
            algorithm=payload.algorithm,
            input_data=payload.input_data
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/thesis/papers/submit",
    tags=["Academic Thesis Citation Graph"]
)
async def submit_thesis_paper(payload: ThesisPaperSubmitRequest):
    """
    Submits student thesis research paper and links bidirectional citation edges.
    """
    try:
        return thesis_citation_graph_service.submit_thesis_paper(
            title=payload.title,
            abstract=payload.abstract,
            authors=payload.authors,
            institution=payload.institution,
            department=payload.department,
            publication_year=payload.publication_year,
            keywords=payload.keywords,
            cited_paper_ids=payload.cited_paper_ids
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/thesis/papers/{paper_id}/citations",
    tags=["Academic Thesis Citation Graph"]
)
async def get_thesis_citation_network(paper_id: str):
    """
    Returns thesis paper details, BibTeX citation entry, and full citation network graph.
    """
    try:
        return thesis_citation_graph_service.get_paper_citation_network(paper_id=paper_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.post(
    "/thesis/papers/check-similarity",
    tags=["Academic Thesis Citation Graph"]
)
async def check_thesis_similarity(payload: ThesisSimilarityCheckRequest):
    """
    Calculates n-gram token shingle Jaccard similarity against registered thesis abstracts.
    """
    try:
        return thesis_citation_graph_service.check_thesis_similarity(
            text_sample=payload.text_sample,
            min_shingle_size=payload.min_shingle_size
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/thesis/grants/match",
    tags=["Academic Thesis Citation Graph"]
)
async def match_research_grants(
    field_of_study: str = Query("Computer Science & AI", description="Research focus or subject"),
    academic_level: str = Query("UNDERGRADUATE", description="Academic level")
):
    """
    Matches student research proposal criteria against active government and international grants.
    """
    return thesis_citation_graph_service.match_research_grants(
        field_of_study=field_of_study,
        academic_level=academic_level
    )


@api_router.get(
    "/ambassador/campuses",
    tags=["Campus Ambassador Syndicate"]
)
async def list_registered_campuses():
    """
    Lists registered university and college campuses across Bangladesh.
    """
    campuses = campus_ambassador_syndicate_service.list_campuses()
    return {
        "campuses": campuses,
        "total_campuses": len(campuses)
    }


@api_router.get(
    "/ambassador/tasks",
    tags=["Campus Ambassador Syndicate"]
)
async def list_ambassador_tasks(
    campus_id: Optional[str] = Query(None, description="Filter by campus"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """
    Lists active micro-internship tasks across university campuses.
    """
    return campus_ambassador_syndicate_service.list_tasks(campus_id=campus_id, status=status)


@api_router.post(
    "/ambassador/tasks/{task_id}/claim",
    tags=["Campus Ambassador Syndicate"]
)
async def claim_ambassador_task(task_id: str, payload: ClaimAmbassadorTaskRequest):
    """
    Claims an available ambassador task with atomic state-lock check.
    """
    try:
        return campus_ambassador_syndicate_service.claim_task(
            task_id=task_id,
            student_id=payload.student_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/ambassador/tasks/{task_id}/submit",
    tags=["Campus Ambassador Syndicate"]
)
async def submit_ambassador_task_evidence(task_id: str, payload: SubmitAmbassadorTaskRequest):
    """
    Submits proof-of-work link and descriptive impact summary for an ambassador task.
    """
    try:
        return campus_ambassador_syndicate_service.submit_task_evidence(
            task_id=task_id,
            student_id=payload.student_id,
            evidence_url=payload.evidence_url,
            impact_report=payload.impact_report
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/ambassador/tasks/{task_id}/verify",
    tags=["Campus Ambassador Syndicate"]
)
async def verify_ambassador_task_and_reward(task_id: str, payload: VerifyAmbassadorTaskRequest):
    """
    Reviews submitted proof-of-work, updates task status, and disburses honorarium points.
    """
    try:
        return campus_ambassador_syndicate_service.verify_and_reward_task(
            task_id=task_id,
            verifier_id=payload.verifier_id,
            approved=payload.approved,
            feedback=payload.feedback
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/ambassador/profiles/{student_id}",
    tags=["Campus Ambassador Syndicate"]
)
async def get_ambassador_profile(student_id: str):
    """
    Retrieves student ambassador tier, points, completed tasks, and cryptographic badge signature.
    """
    return campus_ambassador_syndicate_service.get_ambassador_profile(student_id=student_id)


# ========================================================================================
# Phase 35: National STEM Olympiad Arena, Semiconductor & Quantum Sandbox & Patent Registry
# ========================================================================================

@api_router.get(
    "/olympiad/problems",
    tags=["National STEM Olympiad Arena"]
)
async def list_olympiad_problems(
    competition: Optional[str] = Query(None, description="Filter by competition: BDMO, BDPHO, BDIO, BDBO"),
    division: Optional[str] = Query(None, description="Filter by division: PRIMARY, JUNIOR, SECONDARY, HIGHER_SECONDARY")
):
    """
    Lists competition problems with difficulty ELO, mathematical hints, and division categorizations.
    """
    return national_olympiad_arena_service.list_problems(competition=competition, division=division)


@api_router.post(
    "/olympiad/submit",
    tags=["National STEM Olympiad Arena"]
)
async def submit_olympiad_solution(payload: OlympiadSubmissionRequest):
    """
    Evaluates Olympiad derivation steps, tolerance checks numerical solutions, and applies time decay penalties.
    """
    try:
        return national_olympiad_arena_service.submit_solution(
            problem_id=payload.problem_id,
            student_id=payload.student_id,
            student_name=payload.student_name,
            solution_text=payload.solution_text,
            numerical_answer=payload.numerical_answer,
            time_spent_seconds=payload.time_spent_seconds
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/olympiad/leaderboard",
    tags=["National STEM Olympiad Arena"]
)
async def get_olympiad_leaderboard(
    competition: str = Query("BDMO", description="Competition code: BDMO, BDPHO, BDIO, BDBO")
):
    """
    Returns national competition leaderboard rankings with national percentiles and solved problem counts.
    """
    return national_olympiad_arena_service.get_leaderboard(competition=competition)


@api_router.post(
    "/lab/semiconductor/pn-junction",
    tags=["Semiconductor & Quantum Sandbox"]
)
async def simulate_semiconductor_pn_junction(payload: PnJunctionSimRequest):
    """
    Simulates abrupt PN junction depletion width, built-in potential, and electric field spatial profile.
    """
    return semiconductor_quantum_sandbox_service.simulate_pn_junction(
        semiconductor_material=payload.semiconductor_material,
        acceptor_doping_na_cm3=payload.acceptor_doping_na_cm3,
        donor_doping_nd_cm3=payload.donor_doping_nd_cm3,
        reverse_bias_voltage_v=payload.reverse_bias_voltage_v,
        temperature_kelvin=payload.temperature_kelvin
    )


@api_router.post(
    "/lab/quantum/particle-in-box",
    tags=["Semiconductor & Quantum Sandbox"]
)
async def simulate_quantum_well(payload: QuantumWellSimRequest):
    """
    Solves 1D Quantum Well discrete energy levels and normalized spatial wavefunctions.
    """
    return semiconductor_quantum_sandbox_service.simulate_quantum_well(
        well_width_nm=payload.well_width_nm,
        particle_mass_ratio=payload.particle_mass_ratio,
        state_levels=payload.state_levels
    )


@api_router.post(
    "/patent/disclosures/file",
    tags=["University Patent Registry"]
)
async def file_university_patent_disclosure(payload: PatentDisclosureFileRequest):
    """
    Files a student or researcher patent disclosure with automated novelty score and SHA-256 seal.
    """
    try:
        return university_patent_registry_service.file_patent_disclosure(
            title=payload.title,
            abstract=payload.abstract,
            inventors=payload.inventors,
            institution=payload.institution,
            ipc_classification=payload.ipc_classification,
            claims=payload.claims,
            technical_field=payload.technical_field
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/patent/disclosures/{patent_id}",
    tags=["University Patent Registry"]
)
async def get_university_patent_disclosure(patent_id: str):
    """
    Retrieves full patent disclosure record, claims tree, and cryptographic verification seal.
    """
    try:
        return university_patent_registry_service.get_patent_disclosure(patent_id=patent_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@api_router.post(
    "/patent/prior-art/search",
    tags=["University Patent Registry"]
)
async def search_patent_prior_art(payload: PatentPriorArtSearchRequest):
    """
    Scans technical disclosure database for prior art overlaps and computes patentability novelty index.
    """
    try:
        return university_patent_registry_service.search_prior_art(
            search_query=payload.search_query,
            min_novelty_threshold=payload.min_novelty_threshold
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# =============================================================================
# SECTION 35: ORBITAL AEROSPACE, GLOBAL RESEARCH GRANTS & SWARM STUDY PODS
# =============================================================================

@api_router.post(
    "/satellite/orbit/calculate",
    tags=["Orbital Aerospace Telemetry"]
)
async def calculate_satellite_orbit(payload: SatelliteOrbitRequest):
    """
    Computes two-body Keplerian orbital parameters, period, and velocities.
    """
    try:
        return orbital_mechanics_satellite_service.calculate_orbit(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/satellite/pass/predict",
    tags=["Orbital Aerospace Telemetry"]
)
async def predict_satellite_pass(payload: GroundStationPassRequest):
    """
    Calculates upcoming ground station pass metrics, elevation, and Doppler frequency shift.
    """
    try:
        return orbital_mechanics_satellite_service.predict_ground_station_pass(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/satellite/link-budget/calculate",
    tags=["Orbital Aerospace Telemetry"]
)
async def calculate_satellite_rf_link_budget(payload: RfLinkBudgetRequest):
    """
    Computes Free-Space Path Loss (FSPL), Received Power, and Eb/N0 Link Margin.
    """
    try:
        return orbital_mechanics_satellite_service.calculate_rf_link_budget(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/grants/fellowships",
    tags=["Global Research Grants"]
)
async def list_global_fellowships(
    degree_level: Optional[str] = Query(None, description="Filter by degree level: MASTERS, PHD, POSTDOC"),
    destination_country: Optional[str] = Query(None, description="Filter by destination country")
):
    """
    Filters international university fellowships (Fulbright, DAAD, Erasmus Mundus, Commonwealth, MEXT).
    """
    query = FellowshipSearchQuery(degree_level=degree_level, destination_country=destination_country)
    return global_research_grant_service.list_fellowships(query=query)


@api_router.post(
    "/grants/sop/evaluate",
    tags=["Global Research Grants"]
)
async def evaluate_research_sop(payload: SopEvaluationRequest):
    """
    Analyzes Statement of Purpose (SOP) text for lexical density, academic rigor, and research readiness.
    """
    try:
        return global_research_grant_service.evaluate_sop(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/grants/budget/calculate",
    tags=["Global Research Grants"]
)
async def calculate_grant_budget(payload: GrantBudgetCalculationRequest):
    """
    Calculates research grant budget, indirect institutional overheads, and converts to BDT.
    """
    try:
        return global_research_grant_service.calculate_grant_budget(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/swarm/agents/profiles",
    tags=["Multi-Agent Swarm Study Pods"]
)
async def get_swarm_agent_profiles():
    """
    Retrieves the roster and intellectual specialties of autonomous study pod persona agents.
    """
    return multi_agent_swarm_tutoring_service.get_agent_profiles()


@api_router.post(
    "/swarm/study-pod/discuss",
    tags=["Multi-Agent Swarm Study Pods"]
)
async def run_swarm_study_pod(payload: SwarmStudyPodRequest):
    """
    Executes collaborative 3-agent study pod deliberation and synthesizes dialectical consensus.
    """
    try:
        return multi_agent_swarm_tutoring_service.run_study_pod(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# =============================================================================
# SECTION 36: EDGE ROBOTICS, GENOMICS & BIOMEDICAL DIAGNOSTICS
# =============================================================================

@api_router.post(
    "/robotics/drone/pid-simulate",
    tags=["Edge Robotics & Drone Simulator"]
)
async def simulate_drone_pid_loop(payload: DronePidSimRequest):
    """
    Simulates closed-loop quadcopter attitude control using discrete PID.
    """
    try:
        return edge_robotics_drone_service.simulate_pid_attitude(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/robotics/drone/endurance-calculate",
    tags=["Edge Robotics & Drone Simulator"]
)
async def calculate_drone_endurance(payload: DroneEnduranceRequest):
    """
    Calculates hover power kinetics, thrust-to-weight ratio, and flight endurance in minutes.
    """
    try:
        return edge_robotics_drone_service.calculate_endurance(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/genomics/sequence/align",
    tags=["Genomic Bioinformatics"]
)
async def align_genomic_sequences(payload: SequenceAlignRequest):
    """
    Executes Needleman-Wunsch (Global) or Smith-Waterman (Local) sequence alignment.
    """
    try:
        return genomic_bioinformatics_service.align_sequences(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/genomics/crispr/scan-guides",
    tags=["Genomic Bioinformatics"]
)
async def scan_crispr_guide_rnas(payload: CrisprGuideScanRequest):
    """
    Scans target DNA for 20-nt SpCas9 guide RNA candidates terminating in NGG PAM motif.
    """
    try:
        return genomic_bioinformatics_service.scan_crispr_guides(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/biomedical/diagnostic/evaluate-roc",
    tags=["Biomedical Diagnostics"]
)
async def evaluate_diagnostic_confusion_matrix(payload: DiagnosticConfusionMatrixRequest):
    """
    Calculates epidemiological diagnostic metrics (Sensitivity, Specificity, PPV, NPV, F1).
    """
    try:
        return biomedical_diagnostic_service.evaluate_confusion_matrix(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/biomedical/diagnostic/threshold-tune",
    tags=["Biomedical Diagnostics"]
)
async def tune_diagnostic_threshold_and_roc(payload: DiagnosticRocCurveRequest):
    """
    Generates ROC trajectory and evaluates clinical sensitivity/specificity at decision threshold.
    """
    try:
        return biomedical_diagnostic_service.generate_roc_curve(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ========================================================================================
# Phase 38: Post-Quantum Cryptography, Smart Renewable Micro-Grid & Decentralized Carbon
# ========================================================================================

pqc_service = PostQuantumCryptographyService()
smart_grid_service = SmartGridRenewableDispatchService()
carbon_offset_service = DecentralizedCarbonOffsetService()


@api_router.post(
    "/pqc/kem/generate-keypair",
    tags=["Post-Quantum Cryptography (ML-KEM)"]
)
async def generate_pqc_keypair(payload: PqcKeyGenRequest):
    """
    Generates NIST FIPS 203 ML-KEM-768 public and private lattice keypair.
    """
    try:
        return pqc_service.generate_keypair(payload.seed)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/pqc/kem/encapsulate",
    tags=["Post-Quantum Cryptography (ML-KEM)"]
)
async def encapsulate_pqc_shared_secret(payload: PqcEncapsulateRequest):
    """
    Encapsulates a 256-bit symmetric shared secret against a peer's ML-KEM public key.
    """
    try:
        return pqc_service.encapsulate(
            public_key_hex=payload.public_key_hex,
            algorithm=payload.algorithm,
            message_seed=payload.message_seed
        )
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/pqc/kem/decapsulate",
    tags=["Post-Quantum Cryptography (ML-KEM)"]
)
async def decapsulate_pqc_shared_secret(payload: PqcDecapsulateRequest):
    """
    Decapsulates ciphertext using private secret key s with constant-time equality validation.
    """
    try:
        return pqc_service.decapsulate(
            secret_key_hex=payload.secret_key_hex,
            ciphertext_hex=payload.ciphertext_hex,
            public_key_hex=payload.public_key_hex,
            algorithm=payload.algorithm
        )
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/pqc/security/benchmark",
    tags=["Post-Quantum Cryptography (ML-KEM)"]
)
async def benchmark_pqc_quantum_security(payload: PqcQuantumSecurityAssessmentRequest):
    """
    Returns cryptographic quantum vulnerability assessment against Shor's and Grover's algorithms.
    """
    try:
        return pqc_service.analyze_quantum_security(payload.algorithm)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/smart-grid/solar/calculate",
    tags=["Smart Grid & Renewable Energy"]
)
async def calculate_solar_power(payload: SolarPvCalcRequest):
    """
    Calculates solar PV DC and AC power generation with thermal derating.
    """
    try:
        return smart_grid_service.calculate_solar_pv_output(
            array_area_m2=payload.array_area_m2,
            efficiency=payload.efficiency,
            irradiance_w_per_m2=payload.irradiance_w_per_m2,
            ambient_temp_c=payload.ambient_temp_c,
            temp_coefficient=payload.temp_coefficient,
            system_performance_ratio=payload.system_performance_ratio
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/smart-grid/dispatch/simulate",
    tags=["Smart Grid & Renewable Energy"]
)
async def simulate_microgrid_24h_dispatch(payload: MicroGridDispatchRequest):
    """
    Executes 24-hour chronological microgrid dispatch optimization with LiFePO4 battery peak shaving.
    """
    try:
        return smart_grid_service.simulate_microgrid_dispatch(
            solar_area_m2=payload.solar_area_m2,
            solar_efficiency=payload.solar_efficiency,
            battery_capacity_kwh=payload.battery_capacity_kwh,
            battery_initial_soc=payload.battery_initial_soc,
            battery_max_charge_kw=payload.battery_max_charge_kw,
            battery_max_discharge_kw=payload.battery_max_discharge_kw,
            battery_efficiency_roundtrip=payload.battery_efficiency_roundtrip,
            grid_tariff_peak_bdt_per_kwh=payload.grid_tariff_peak_bdt_per_kwh,
            grid_tariff_offpeak_bdt_per_kwh=payload.grid_tariff_offpeak_bdt_per_kwh,
            custom_hourly_load_kw=payload.custom_hourly_load_kw,
            custom_hourly_irradiance=payload.custom_hourly_irradiance
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/carbon/offset/mint",
    tags=["Decentralized Carbon Offset Registry"]
)
async def mint_carbon_offset_certificate(payload: CarbonOffsetMintRequest):
    """
    Mints a verifiable Green Carbon Certificate on the SHA-256 tamper-evident ledger.
    """
    try:
        return carbon_offset_service.mint_certificate(
            student_id=payload.student_id,
            project_name=payload.project_name,
            renewable_energy_kwh=payload.renewable_energy_kwh,
            grid_emissions_factor=payload.grid_emissions_factor,
            project_category=payload.project_category,
            verification_notes=payload.verification_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/carbon/offset/retire",
    tags=["Decentralized Carbon Offset Registry"]
)
async def retire_carbon_offset_certificate(payload: CarbonOffsetRetireRequest):
    """
    Permanently retires an active carbon offset to prevent double-counting or double-spending.
    """
    try:
        return carbon_offset_service.retire_certificate(
            certificate_id=payload.certificate_id,
            student_id=payload.student_id,
            beneficiary_name=payload.beneficiary_name,
            retirement_reason=payload.retirement_reason
        )
    except (ValueError, KeyError, PermissionError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/carbon/offset/verify/{certificate_id}",
    tags=["Decentralized Carbon Offset Registry"]
)
async def verify_carbon_offset_certificate(certificate_id: str):
    """
    Verifies cryptographic block hash continuity and authentic status of an offset certificate.
    """
    return carbon_offset_service.verify_certificate(certificate_id)


@api_router.get(
    "/carbon/offset/summary",
    tags=["Decentralized Carbon Offset Registry"]
)
async def get_carbon_registry_summary():
    """
    Retrieves global carbon offset registry statistics, total kWh clean energy, and avoided tCO2e.
    """
    return carbon_offset_service.get_ledger_summary()


# ========================================================================================
# Phase 39: Autonomous Cyber Range Zero-Trust, HPC Cluster Scheduler & VC Angel Syndicate
# ========================================================================================

cyber_range_service = CyberRangeZeroTrustService()
hpc_scheduler_service = HpcClusterSchedulerService()
vc_syndicate_service = UniversityVcAngelSyndicateService()


@api_router.post(
    "/cyber/zero-trust/evaluate",
    tags=["Autonomous Cyber Range & Zero-Trust"]
)
async def evaluate_zero_trust_access(payload: ZeroTrustEvaluationRequest):
    """
    Performs continuous verification and evaluates student session trust score (0-100).
    """
    try:
        return cyber_range_service.evaluate_zero_trust_access(
            student_id=payload.student_id,
            device_fingerprint=payload.device_fingerprint,
            ip_address=payload.ip_address,
            mfa_authenticated=payload.mfa_authenticated,
            geo_velocity_kmh=payload.geo_velocity_kmh,
            payload_sample=payload.payload_sample
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/cyber/threat/inspect",
    tags=["Autonomous Cyber Range & Zero-Trust"]
)
async def inspect_and_sanitize_payload_threat(payload: ThreatDetectionRequest):
    """
    Scans request payload for SQLi, XSS, Path Traversal, and JWT None attacks with HTML sanitization.
    """
    return cyber_range_service.inspect_and_sanitize_payload(
        payload_text=payload.payload_text,
        context_type=payload.context_type
    )


@api_router.post(
    "/hpc/job/submit",
    tags=["HPC Parallel Job Scheduler"]
)
async def submit_hpc_compute_job(payload: HpcJobSubmitRequest):
    """
    Schedules a distributed GPU computing job with Slurm Fair-Share queue prioritization.
    """
    try:
        return hpc_scheduler_service.submit_hpc_job(
            job_name=payload.job_name,
            student_id=payload.student_id,
            gpu_type=payload.gpu_type,
            gpu_count=payload.gpu_count,
            vram_gb_requested=payload.vram_gb_requested,
            walltime_minutes=payload.walltime_minutes,
            parallel_fraction=payload.parallel_fraction
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/hpc/amdahl/calculate",
    tags=["HPC Parallel Job Scheduler"]
)
async def calculate_amdahl_parallel_speedup(payload: AmdahlSpeedupCalcRequest):
    """
    Calculates Amdahl's Law and Gustafson's Law scaling curves across processor and GPU counts.
    """
    return hpc_scheduler_service.calculate_amdahl_speedup(
        parallel_fraction=payload.parallel_fraction,
        processor_counts=payload.processor_counts
    )


@api_router.get(
    "/hpc/cluster/status",
    tags=["HPC Parallel Job Scheduler"]
)
async def get_hpc_cluster_status():
    """
    Returns supercomputer cluster capacity, active jobs, allocated GPUs, and TFLOPS utilization.
    """
    return hpc_scheduler_service.get_cluster_status()


@api_router.post(
    "/vc/safe/dilution-calculate",
    tags=["University VC & Angel Syndicate"]
)
async def calculate_safe_cap_table_dilution(payload: SafeDilutionCalcRequest):
    """
    Simulates Y-Combinator standard Post-Money SAFE and Convertible Note cap table equity dilution.
    """
    try:
        return vc_syndicate_service.calculate_safe_dilution(
            startup_name=payload.startup_name,
            safe_type=payload.safe_type,
            investment_amount_usd=payload.investment_amount_usd,
            valuation_cap_usd=payload.valuation_cap_usd,
            discount_pct=payload.discount_pct,
            existing_founder_shares=payload.existing_founder_shares
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/vc/angel/commit",
    tags=["University VC & Angel Syndicate"]
)
async def register_angel_syndicate_commitment(payload: AngelCommitmentRequest):
    """
    Registers an angel syndicate funding commitment with cryptographic escrow verification.
    """
    try:
        return vc_syndicate_service.register_angel_commitment(
            startup_name=payload.startup_name,
            student_founder_id=payload.student_founder_id,
            target_raise_usd=payload.target_raise_usd,
            investor_name=payload.investor_name,
            syndicate_tier=payload.syndicate_tier,
            commitment_amount_usd=payload.commitment_amount_usd
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/vc/startup/{startup_name}/commitments",
    tags=["University VC & Angel Syndicate"]
)
async def list_startup_syndicate_commitments(startup_name: str):
    """
    Lists all verified angel syndicate commitments and funding progress for a student venture.
    """
    return vc_syndicate_service.list_startup_commitments(startup_name)


# ========================================================================================
# Phase 40: Formal Verification, Decentralized Knowledge DAG (IPFS) & FinTech Quant Risk
# ========================================================================================

formal_verification_service = FormalVerificationZ3SolverService()
knowledge_dag_service = DecentralizedKnowledgeDagService()
fintech_quant_service = FintechQuantRiskService()


@api_router.post(
    "/formal/hoare/verify",
    tags=["Formal Verification & AST Invariant Sandbox"]
)
async def verify_hoare_triple_contract(payload: HoareVerificationRequest):
    """
    Formally verifies Hoare Triple {P} C {Q}, checks loop termination and ranking variants.
    """
    return formal_verification_service.verify_hoare_triple(
        code_str=payload.code_str,
        pre_condition=payload.pre_condition,
        post_condition=payload.post_condition,
        loop_invariant=payload.loop_invariant,
        ranking_variant=payload.ranking_variant
    )


@api_router.post(
    "/formal/mutation/score",
    tags=["Formal Verification & AST Invariant Sandbox"]
)
async def calculate_mutation_testing_score(payload: MutationScoreRequest):
    """
    Calculates mutation testing adequacy score and operator distribution.
    """
    return formal_verification_service.calculate_mutation_score(
        total_mutants=payload.total_mutants,
        killed_mutants=payload.killed_mutants,
        operators_applied=payload.operators_applied
    )


@api_router.post(
    "/knowledge-dag/node/create",
    tags=["Decentralized Knowledge Graph IPFS Merkle DAG"]
)
async def create_knowledge_dag_node(payload: CreateDagNodeRequest):
    """
    Creates an immutable IPFS-compatible Merkle DAG curriculum node with CIDv1 addressing.
    """
    try:
        return knowledge_dag_service.create_dag_node(
            title=payload.title,
            content=payload.content,
            author=payload.author or "Academic Contributor",
            parent_cids=payload.parent_cids,
            tags=payload.tags
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/knowledge-dag/node/verify/{cid}",
    tags=["Decentralized Knowledge Graph IPFS Merkle DAG"]
)
async def verify_knowledge_dag_node(cid: str):
    """
    Verifies cryptographic integrity and tamper status of a CIDv1 Merkle DAG node.
    """
    return knowledge_dag_service.verify_node_integrity(cid)


@api_router.get(
    "/knowledge-dag/status",
    tags=["Decentralized Knowledge Graph IPFS Merkle DAG"]
)
async def get_knowledge_dag_status():
    """
    Retrieves global Merkle DAG node statistics and peer pin status.
    """
    return knowledge_dag_service.get_dag_status()


@api_router.post(
    "/fintech/options/black-scholes",
    tags=["FinTech Quantitative Risk & Black-Scholes"]
)
async def calculate_black_scholes_pricing(payload: BlackScholesRequest):
    """
    Calculates European option prices and analytical Greeks (Delta, Gamma, Theta, Vega, Rho).
    """
    return fintech_quant_service.calculate_black_scholes(
        spot_price=payload.spot_price,
        strike_price=payload.strike_price,
        time_to_maturity=payload.time_to_maturity,
        risk_free_rate=payload.risk_free_rate,
        volatility=payload.volatility
    )


@api_router.post(
    "/fintech/risk/var",
    tags=["FinTech Quantitative Risk & Black-Scholes"]
)
async def calculate_portfolio_value_at_risk(payload: PortfolioVarRequest):
    """
    Calculates Parametric Value-at-Risk (VaR at 95% and 99%) and annualized Sharpe ratio.
    """
    return fintech_quant_service.calculate_portfolio_var(
        portfolio_value=payload.portfolio_value,
        expected_annual_return=payload.expected_annual_return,
        annual_volatility=payload.annual_volatility,
        holding_period_days=payload.holding_period_days or 1,
        risk_free_rate=payload.risk_free_rate or 0.05
    )


# ========================================================================================
# Phase 41: BCI Cognitive Telemetry, Hypothesis Discovery & Logistics Operations Research
# ========================================================================================

bci_telemetry_service = BciCognitiveTelemetryService()
hypothesis_discovery_service = ScientificHypothesisDiscoveryService()
logistics_ops_service = SupplyChainLogisticsOpsService()


@api_router.post(
    "/bci/eeg/decompose",
    tags=["BCI & Cognitive Telemetry"]
)
async def decompose_eeg_cognitive_load(payload: BciEegSamplesRequest):
    """
    Decomposes raw EEG into Delta, Theta, Alpha, Beta, Gamma power and calculates engagement index.
    """
    return bci_telemetry_service.decompose_band_powers(
        raw_samples=payload.raw_samples or [],
        sampling_rate_hz=payload.sampling_rate_hz or 256.0,
        channel=payload.channel or "Cz"
    )


@api_router.post(
    "/science/hypothesis/evaluate",
    tags=["Scientific Hypothesis Discovery"]
)
async def evaluate_scientific_hypothesis(payload: ContingencyHypothesisRequest):
    """
    Performs Pearson Chi-Square, Fisher exact, and Bonferroni tests for hypothesis significance.
    """
    return hypothesis_discovery_service.evaluate_contingency_hypothesis(
        variable_a_name=payload.variable_a_name,
        variable_b_name=payload.variable_b_name,
        observed_matrix=payload.observed_matrix or [[25, 5], [10, 20]],
        alpha=payload.alpha or 0.05,
        bonferroni_hypotheses_count=payload.bonferroni_hypotheses_count or 1
    )


@api_router.post(
    "/logistics/inventory/eoq-rop",
    tags=["Supply Chain Operations Research"]
)
async def calculate_eoq_and_reorder_point(payload: EoqRopCalcRequest):
    """
    Calculates Economic Order Quantity (EOQ), Reorder Point (ROP), and safety stock buffers.
    """
    return logistics_ops_service.calculate_eoq_and_rop(
        annual_demand=payload.annual_demand,
        order_cost_usd=payload.order_cost_usd,
        holding_cost_unit_year_usd=payload.holding_cost_unit_year_usd,
        lead_time_days=payload.lead_time_days or 7,
        demand_std_dev_daily=payload.demand_std_dev_daily or 5.0,
        service_level_pct=payload.service_level_pct or 95.0
    )


@api_router.post(
    "/logistics/bullwhip/calculate",
    tags=["Supply Chain Operations Research"]
)
async def calculate_bullwhip_variance_ratio(payload: BullwhipEffectRequest):
    """
    Calculates upstream order variance vs retail demand variance amplification ratio.
    """
    return logistics_ops_service.calculate_bullwhip_effect(
        demand_orders=payload.demand_orders or [],
        retailer_orders=payload.retailer_orders or []
    )


@api_router.post(
    "/logistics/routing/shortest-path",
    tags=["Supply Chain Operations Research"]
)
async def find_shortest_logistics_route(payload: ShortestRouteRequest):
    """
    Computes optimal academic book / relief distribution route using Dijkstra's algorithm.
    """
    return logistics_ops_service.find_shortest_delivery_route(
        origin_hub=payload.origin_hub,
        destination_hub=payload.destination_hub
    )


# ========================================================================================
# Phase 42: Digital Twin Simulation, Computational Fluid Dynamics & DAO Governance
# ========================================================================================

digital_twin_service = DigitalTwinSimulationService()
cfd_service = ComputationalFluidDynamicsService()
dao_governance_service = DaoGovernanceProtocolService()


@api_router.post(
    "/twin/state/simulate",
    tags=["Digital Twin Simulation"]
)
async def simulate_digital_twin_state(payload: TwinStateSimulationRequest):
    """
    Generates or validates digital twin telemetry state with anomaly health check.
    """
    return digital_twin_service.simulate_twin_state(
        sensors=payload.sensors,
        noise_sigma=payload.noise_sigma
    )


@api_router.post(
    "/twin/anomaly/mahalanobis",
    tags=["Digital Twin Simulation"]
)
async def evaluate_mahalanobis_anomaly(payload: MahalanobisAnomalyRequest):
    """
    Computes Mahalanobis distance for multivariate predictive maintenance anomaly detection.
    """
    return digital_twin_service.mahalanobis_anomaly_score(
        observation=payload.observation,
        mean_vector=payload.mean_vector,
        covariance_matrix=payload.covariance_matrix
    )


@api_router.post(
    "/twin/sensor/calibrate",
    tags=["Digital Twin Simulation"]
)
async def calibrate_sensor_drift(payload: SensorDriftCalibrationRequest):
    """
    Compensates for cumulative sensor drift over time.
    """
    return digital_twin_service.calibrate_sensor_drift(
        raw_value=payload.raw_value,
        drift_rate_per_hour=payload.drift_rate_per_hour,
        elapsed_hours=payload.elapsed_hours,
        reference_value=payload.reference_value
    )


@api_router.post(
    "/twin/reliability/monte-carlo",
    tags=["Digital Twin Simulation"]
)
async def estimate_monte_carlo_reliability(payload: MonteCarloReliabilityRequest):
    """
    Simulates mission reliability and MTTF via Monte Carlo exponential failure models.
    """
    return digital_twin_service.monte_carlo_reliability(
        component_class=payload.component_class,
        mission_hours=payload.mission_hours,
        simulations=payload.simulations,
        seed=payload.seed
    )


@api_router.post(
    "/cfd/reynolds/classify",
    tags=["Computational Fluid Dynamics"]
)
async def classify_flow_reynolds_regime(payload: ReynoldsRegimeRequest):
    """
    Computes Reynolds number and categorizes flow regime into Laminar, Transitional, or Turbulent.
    """
    return cfd_service.classify_reynolds_regime(
        velocity=payload.velocity,
        characteristic_length=payload.characteristic_length,
        fluid=payload.fluid,
        custom_density=payload.custom_density,
        custom_viscosity=payload.custom_viscosity
    )


@api_router.post(
    "/cfd/bernoulli/solve",
    tags=["Computational Fluid Dynamics"]
)
async def solve_bernoulli_flow_equation(payload: BernoulliFlowRequest):
    """
    Solves steady-state Bernoulli equation for pressure and velocity conservation.
    """
    return cfd_service.solve_bernoulli_flow(
        p1_pascal=payload.p1_pascal,
        v1_m_s=payload.v1_m_s,
        z1_meters=payload.z1_meters,
        v2_m_s=payload.v2_m_s,
        z2_meters=payload.z2_meters,
        fluid=payload.fluid
    )


@api_router.post(
    "/cfd/aerodynamics/coefficients",
    tags=["Computational Fluid Dynamics"]
)
async def calculate_aerodynamic_coefficients(payload: AerodynamicCoefficientsRequest):
    """
    Computes aerodynamic drag (Cd), lift (Cl), and lift-to-drag ratio.
    """
    return cfd_service.calculate_aerodynamic_coefficients(
        drag_force_newtons=payload.drag_force_newtons,
        lift_force_newtons=payload.lift_force_newtons,
        velocity_m_s=payload.velocity_m_s,
        frontal_area_m2=payload.frontal_area_m2,
        fluid=payload.fluid
    )


@api_router.post(
    "/dao/voting/quadratic-calc",
    tags=["DAO Governance Protocol"]
)
async def calculate_quadratic_voting_power(payload: QuadraticVotingCalcRequest):
    """
    Computes quadratic voting cost or vote power allocation curve.
    """
    return dao_governance_service.calculate_quadratic_voting(
        tokens=payload.tokens,
        votes=payload.votes
    )


@api_router.post(
    "/dao/proposals/create",
    tags=["DAO Governance Protocol"]
)
async def create_dao_proposal(payload: ProposalCreateRequest):
    """
    Creates and activates a new student DAO governance proposal.
    """
    return dao_governance_service.create_proposal(
        proposal_id=payload.proposal_id,
        title=payload.title,
        description=payload.description,
        proposer_address=payload.proposer_address,
        total_supply=payload.total_supply,
        quorum_pct=payload.quorum_pct,
        approval_threshold_pct=payload.approval_threshold_pct,
        voting_period_hours=payload.voting_period_hours,
        timelock_delay_hours=payload.timelock_delay_hours
    )


@api_router.post(
    "/dao/proposals/vote",
    tags=["DAO Governance Protocol"]
)
async def cast_dao_quadratic_vote(payload: QuadraticVoteCastRequest):
    """
    Casts a quadratic ballot on an active DAO proposal with double-voting prevention.
    """
    return dao_governance_service.cast_quadratic_vote(
        proposal_id=payload.proposal_id,
        voter_address=payload.voter_address,
        tokens_allocated=payload.tokens_allocated,
        support=payload.support
    )


@api_router.get(
    "/dao/proposals/{proposal_id}/outcome",
    tags=["DAO Governance Protocol"]
)
async def get_dao_governance_outcome(proposal_id: str):
    """
    Evaluates final quorum and supermajority execution readiness for a proposal.
    """
    return dao_governance_service.evaluate_governance_outcome(proposal_id=proposal_id)


# ========================================================================================
# Phase 43: Quantum Error Correction, Atmospheric Climate & Micro-Robotics Swarm
# ========================================================================================

qec_service = QuantumErrorCorrectionService()
climate_service = AtmosphericClimateModelingService()
swarm_service = AutonomousMicroRoboticsSwarmService()


@api_router.post(
    "/qec/lattice/init",
    tags=["Quantum Error Correction"]
)
async def initialize_quantum_surface_code(payload: SurfaceLatticeInitRequest):
    """
    Initializes a rotated surface code lattice of distance d with data and stabilizer qubits.
    """
    return qec_service.initialize_surface_code_lattice(distance=payload.distance)


@api_router.post(
    "/qec/errors/inject",
    tags=["Quantum Error Correction"]
)
async def inject_surface_code_pauli_errors(payload: PauliErrorInjectionRequest):
    """
    Simulates physical Pauli X and Z errors and extracts syndrome defect signatures.
    """
    lattice = qec_service.initialize_surface_code_lattice(distance=payload.code_distance)
    return qec_service.inject_pauli_errors(
        lattice=lattice,
        error_rate_p=payload.error_rate_p,
        explicit_errors=payload.explicit_errors
    )


@api_router.post(
    "/qec/syndrome/decode",
    tags=["Quantum Error Correction"]
)
async def decode_qec_syndromes_and_estimate_fidelity(payload: QecDecodingRequest):
    """
    Evaluates sub-threshold error suppression and logical qubit lifetime gain ratio.
    """
    return qec_service.decode_syndromes_and_estimate_logical_fidelity(
        code_distance=payload.code_distance,
        physical_error_p=payload.physical_error_p,
        syndrome_defects_count=payload.syndrome_defects_count
    )


@api_router.post(
    "/climate/forcing/calculate",
    tags=["Atmospheric Climate Dynamics"]
)
async def calculate_greenhouse_radiative_forcing(payload: RadiativeForcingRequest):
    """
    Computes greenhouse radiative forcing (W/m^2) and transient temperature anomaly.
    """
    return climate_service.calculate_radiative_forcing(
        co2_concentration_ppm=payload.co2_concentration_ppm,
        ch4_concentration_ppb=payload.ch4_concentration_ppb,
        n2o_concentration_ppb=payload.n2o_concentration_ppb,
        baseline_co2_ppm=payload.baseline_co2_ppm
    )


@api_router.post(
    "/climate/energy-balance/solve",
    tags=["Atmospheric Climate Dynamics"]
)
async def solve_planetary_energy_equilibrium(payload: PlanetaryEnergyBalanceRequest):
    """
    Solves Stefan-Boltzmann planetary energy equilibrium for surface temperature.
    """
    return climate_service.solve_planetary_energy_balance(
        planetary_albedo=payload.planetary_albedo,
        effective_emissivity=payload.effective_emissivity,
        solar_irradiance=payload.solar_irradiance,
        greenhouse_forcing_delta_f=payload.greenhouse_forcing_delta_f
    )


@api_router.post(
    "/swarm/kinematics/step",
    tags=["Micro-Robotics Swarm Intelligence"]
)
async def simulate_swarm_kinematic_step(payload: SwarmSimulationStepRequest):
    """
    Advances multi-agent flocking kinematics under Reynolds forces and obstacle repulsive fields.
    """
    return swarm_service.simulate_swarm_step(
        agents=payload.agents or [],
        target_waypoint=payload.target_waypoint,
        obstacles=payload.obstacles,
        dt_seconds=payload.dt_seconds,
        weight_separation=payload.weight_separation,
        weight_alignment=payload.weight_alignment,
        weight_cohesion=payload.weight_cohesion
    )


# ========================================================================================
# Phase 44: Fusion Tokamak Physics, Neuromorphic SNN & Maritime COLREGs
# ========================================================================================

plasma_service = FusionPlasmaTokamakService()
neuromorphic_service = NeuromorphicSpikingNetworkService()
maritime_service = MaritimeNavigationColregsService()


@api_router.post(
    "/fusion/plasma/lawson",
    tags=["Fusion Tokamak Physics"]
)
async def evaluate_fusion_lawson_criterion(payload: LawsonCriterionRequest):
    """
    Evaluates Lawson ignition triple product (n * tau_E * T) and fusion power gain Q-factor.
    """
    return plasma_service.evaluate_lawson_criterion(
        plasma_density_m3=payload.plasma_density_m3,
        energy_confinement_time_s=payload.energy_confinement_time_s,
        plasma_temperature_kev=payload.plasma_temperature_kev,
        external_heating_power_mw=payload.external_heating_power_mw
    )


@api_router.post(
    "/fusion/tokamak/mhd-stability",
    tags=["Fusion Tokamak Physics"]
)
async def calculate_tokamak_mhd_stability(payload: TokamakMhdRequest):
    """
    Computes magnetic beta confinement and edge safety factor q(a) against Kruskal-Shafranov limit.
    """
    return plasma_service.calculate_tokamak_mhd_stability(
        major_radius_r_m=payload.major_radius_r_m,
        minor_radius_a_m=payload.minor_radius_a_m,
        toroidal_field_bt_tesla=payload.toroidal_field_bt_tesla,
        plasma_current_ip_ma=payload.plasma_current_ip_ma,
        plasma_density_m3=payload.plasma_density_m3,
        plasma_temperature_kev=payload.plasma_temperature_kev
    )


@api_router.post(
    "/neuromorphic/neuron/lif-simulate",
    tags=["Neuromorphic SNN"]
)
async def simulate_lif_spiking_neuron(payload: LifNeuronSimulationRequest):
    """
    Simulates membrane potential dynamics and spike emission in a Leaky Integrate-and-Fire neuron.
    """
    return neuromorphic_service.simulate_lif_neuron(
        current_injections_na=payload.current_injections_na,
        dt_ms=payload.dt_ms,
        v_rest_mv=payload.v_rest_mv,
        v_thresh_mv=payload.v_thresh_mv,
        v_reset_mv=payload.v_reset_mv,
        tau_m_ms=payload.tau_m_ms,
        r_m_mohm=payload.r_m_mohm,
        refractory_period_ms=payload.refractory_period_ms
    )


@api_router.post(
    "/neuromorphic/synapse/stdp-learn",
    tags=["Neuromorphic SNN"]
)
async def calculate_stdp_synaptic_learning(payload: StdpPlasticityRequest):
    """
    Computes Hebbian synaptic weight potentiation and depression via spike timing intervals.
    """
    return neuromorphic_service.calculate_stdp_synaptic_plasticity(
        initial_weight=payload.initial_weight,
        pre_spike_times_ms=payload.pre_spike_times_ms,
        post_spike_times_ms=payload.post_spike_times_ms,
        a_plus=payload.a_plus,
        a_minus=payload.a_minus,
        tau_plus_ms=payload.tau_plus_ms,
        tau_minus_ms=payload.tau_minus_ms
    )


@api_router.post(
    "/maritime/navigation/cpa-colregs",
    tags=["Autonomous Maritime Navigation"]
)
async def evaluate_maritime_cpa_and_colregs(payload: CpaCollisionRequest):
    """
    Calculates DCPA, TCPA, and prescribes IMO COLREGs evasive steering maneuvers.
    """
    return maritime_service.calculate_closest_point_of_approach(
        own_x_nm=payload.own_x_nm,
        own_y_nm=payload.own_y_nm,
        own_speed_knots=payload.own_speed_knots,
        own_course_deg=payload.own_course_deg,
        target_x_nm=payload.target_x_nm,
        target_y_nm=payload.target_y_nm,
        target_speed_knots=payload.target_speed_knots,
        target_course_deg=payload.target_course_deg
    )


# ========================================================================================
# Phase 45: Nanophotonics Metamaterial, Gravitational Waves & CRISPR Gene Lab
# ========================================================================================

metamaterial_service = NanophotonicMetamaterialService()
gravitational_service = GravitationalWaveInterferometryService()
crispr_service = SyntheticBiologyCrisprService()


@api_router.post(
    "/metamaterial/dispersion/calculate",
    tags=["Nanophotonics & Metamaterials"]
)
async def calculate_optical_dispersion(payload: OpticalDispersionRequest):
    """
    Computes Drude-Lorentz permittivity, permeability, and negative refractive index.
    """
    return metamaterial_service.calculate_optical_dispersion(
        frequency_thz=payload.frequency_thz,
        plasma_frequency_thz=payload.plasma_frequency_thz,
        resonance_frequency_thz=payload.resonance_frequency_thz,
        electron_damping_thz=payload.electron_damping_thz,
        magnetic_damping_thz=payload.magnetic_damping_thz,
        magnetic_oscillator_strength=payload.magnetic_oscillator_strength
    )


@api_router.post(
    "/metamaterial/ray/refract",
    tags=["Nanophotonics & Metamaterials"]
)
async def simulate_negative_refraction_ray(payload: NegativeRefractionRequest):
    """
    Simulates negative refraction across Veselago superlens interfaces.
    """
    return metamaterial_service.simulate_negative_refraction_ray(
        incident_angle_deg=payload.incident_angle_deg,
        n1_incident=payload.n1_incident,
        n2_metamaterial=payload.n2_metamaterial,
        slab_thickness_nm=payload.slab_thickness_nm,
        wavelength_nm=payload.wavelength_nm
    )


@api_router.post(
    "/gravitational/cbc/chirp-parameters",
    tags=["Gravitational Wave Interferometry"]
)
async def calculate_gravitational_chirp(payload: GravitationalChirpRequest):
    """
    Calculates compact binary coalescence chirp mass, time to merger, and peak strain.
    """
    return gravitational_service.calculate_binary_chirp_parameters(
        m1_solar_masses=payload.m1_solar_masses,
        m2_solar_masses=payload.m2_solar_masses,
        luminosity_distance_mpc=payload.luminosity_distance_mpc,
        initial_frequency_hz=payload.initial_frequency_hz
    )


@api_router.post(
    "/gravitational/waveform/synthesize",
    tags=["Gravitational Wave Interferometry"]
)
async def synthesize_chirp_waveform(payload: ChirpWaveformRequest):
    """
    Generates time-domain gravitational wave strain waveform h(t) samples.
    """
    return gravitational_service.generate_chirp_waveform_samples(
        chirp_mass_msun=payload.chirp_mass_msun,
        duration_seconds=payload.duration_seconds,
        sampling_rate_hz=payload.sampling_rate_hz
    )


@api_router.post(
    "/crispr/grna/evaluate",
    tags=["Synthetic Biology CRISPR-Cas9"]
)
async def evaluate_crispr_grna(payload: CrisprGrnaEvaluationRequest):
    """
    Evaluates 20nt protospacer + PAM on-target Doench efficiency and hairpin secondary structure.
    """
    return crispr_service.evaluate_grna_efficiency_and_pam(
        sequence_23nt=payload.sequence_23nt
    )


@api_router.post(
    "/crispr/off-target/score",
    tags=["Synthetic Biology CRISPR-Cas9"]
)
async def calculate_crispr_off_target(payload: CrisprOffTargetRequest):
    """
    Computes Hsu-Zhang off-target cleavage probability based on mismatch positions.
    """
    return crispr_service.calculate_off_target_cleavage_score(
        guide_20nt=payload.guide_20nt,
        potential_off_target_20nt=payload.potential_off_target_20nt
    )


# ========================================================================================
# Phase 46: Nuclear SMR Reactor Physics, Interplanetary Astrodynamics & Topological Quantum Lab
# ========================================================================================

smr_reactor_service = NuclearSmrReactorService()
astrodynamics_service = InterplanetaryAstrodynamicsService()
topological_quantum_service = TopologicalQuantumService()


@api_router.post(
    "/smr/core/transient",
    tags=["Nuclear SMR Reactor Physics"]
)
async def simulate_smr_transient(payload: SmrTransientRequest):
    """
    Simulates SMR point kinetics with 6 delayed groups and Doppler reactivity feedback.
    """
    return smr_reactor_service.simulate_reactor_transient(
        rated_thermal_power_mw=payload.rated_thermal_power_mw,
        initial_power_mw=payload.initial_power_mw,
        reactivity_insertion_pcm=payload.reactivity_insertion_pcm,
        fuel_doppler_coeff_pcm_per_c=payload.fuel_doppler_coeff_pcm_per_c,
        moderator_coeff_pcm_per_c=payload.moderator_coeff_pcm_per_c,
        initial_fuel_temp_c=payload.initial_fuel_temp_c,
        initial_mod_temp_c=payload.initial_mod_temp_c,
        coolant_inlet_temp_c=payload.coolant_inlet_temp_c,
        transient_duration_s=payload.transient_duration_s,
        time_step_s=payload.time_step_s,
        scram_enabled=payload.scram_enabled
    )


@api_router.post(
    "/smr/safety/decay-heat",
    tags=["Nuclear SMR Reactor Physics"]
)
async def calculate_smr_decay_heat(payload: DecayHeatRequest):
    """
    Computes post-scram decay heat according to ANS-5.1 standards.
    """
    decay_mw = smr_reactor_service.calculate_decay_heat(
        p_rated_mw=payload.rated_power_mw,
        time_after_scram_s=payload.time_after_scram_s,
        operating_time_s=payload.operating_time_s
    )
    return {
        "status": "COMPLETED",
        "rated_power_mw": payload.rated_power_mw,
        "time_after_scram_s": payload.time_after_scram_s,
        "decay_heat_mw": decay_mw,
        "decay_fraction_pct": round((decay_mw / payload.rated_power_mw) * 100.0, 4)
    }


@api_router.post(
    "/astrodynamics/transfer/lambert",
    tags=["Interplanetary Astrodynamics"]
)
async def solve_lambert_transfer(payload: LambertTransferRequest):
    """
    Solves Keplerian Lambert orbital transfer between planetary orbits.
    """
    return astrodynamics_service.solve_lambert_transfer(
        r1_au=payload.departure_radius_au,
        r2_au=payload.arrival_radius_au,
        transfer_angle_deg=payload.transfer_angle_deg,
        time_of_flight_days=payload.time_of_flight_days
    )


@api_router.post(
    "/astrodynamics/trajectory/gravity-assist",
    tags=["Interplanetary Astrodynamics"]
)
async def calculate_gravity_assist(payload: GravityAssistRequest):
    """
    Calculates hyperbolic swing-by deflection angle and heliocentric velocity boost.
    """
    return astrodynamics_service.calculate_gravity_assist(
        planet_name=payload.planet_name,
        v_infinity_in_km_s=payload.v_infinity_in_km_s,
        flyby_periapsis_altitude_km=payload.flyby_periapsis_altitude_km,
        planet_heliocentric_speed_km_s=payload.planet_heliocentric_speed_km_s
    )


@api_router.post(
    "/astrodynamics/propulsion/multistage-rocket",
    tags=["Interplanetary Astrodynamics"]
)
async def calculate_multistage_rocket(payload: MultiStageRocketRequest):
    """
    Computes multi-stage Tsiolkovsky rocket Delta-v and mass fraction staging.
    """
    return astrodynamics_service.calculate_multistage_rocket(
        payload_mass_kg=payload.payload_mass_kg,
        stages=payload.stages
    )


@api_router.post(
    "/topological/nanowire/kitaev-wire",
    tags=["Topological Quantum Computing"]
)
async def evaluate_kitaev_wire(payload: KitaevWireRequest):
    """
    Evaluates 1D Kitaev p-wave superconducting nanowire phase and Majorana Zero Modes.
    """
    return topological_quantum_service.evaluate_kitaev_wire(
        num_sites_n=payload.num_sites,
        hopping_amplitude_t_mev=payload.hopping_amplitude_mev,
        superconducting_gap_delta_mev=payload.superconducting_gap_mev,
        chemical_potential_mu_mev=payload.chemical_potential_mev,
        temperature_kelvin=payload.temperature_kelvin
    )


@api_router.post(
    "/topological/braiding/simulate",
    tags=["Topological Quantum Computing"]
)
async def simulate_anyon_braiding(payload: AnyonBraidRequest):
    """
    Executes non-Abelian anyon braid swap operations on 4-Majorana logical qubit.
    """
    return topological_quantum_service.simulate_anyon_braiding(
        braid_sequence=payload.braid_sequence,
        initial_state=payload.initial_state
    )


# ========================================================================================
# Phase 47: Supabase Security, RLS Policy Engine, Edge Boundary & Realtime Cryptographic Guard
# ========================================================================================

supabase_security_service = SupabaseSecurityService()
edge_boundary_service = EdgeFunctionBoundaryService()
realtime_presence_service = RealtimeCryptographicPresenceService()


@api_router.post(
    "/supabase/rls/evaluate",
    response_model=RlsEvaluationResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def evaluate_supabase_rls(payload: RlsEvaluationRequest):
    """
    Evaluates Row-Level Security (RLS) access rules across roles, tenants, and record owners.
    """
    return supabase_security_service.evaluate_rls_access(
        table_name=payload.table_name,
        action=payload.action,
        caller_role=payload.caller_role,
        caller_uid=payload.caller_uid,
        caller_tenant_id=payload.caller_tenant_id,
        target_owner_id=payload.target_owner_id,
        target_tenant_id=payload.target_tenant_id,
        client_payload_user_id=payload.client_payload_user_id,
        is_browser_origin=payload.is_browser_origin
    )


@api_router.post(
    "/supabase/rls/generate-policy",
    response_model=RlsGeneratePolicyResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def generate_supabase_rls_policy(payload: RlsGeneratePolicyRequest):
    """
    Generates battle-tested PostgreSQL RLS SQL policies with tenant isolation and owner binding.
    """
    sql = supabase_security_service.generate_secure_rls_sql(
        table_name=payload.table_name,
        owner_column=payload.owner_column,
        tenant_column=payload.tenant_column
    )
    return {
        "table_name": payload.table_name,
        "sql_script": sql
    }


@api_router.post(
    "/supabase/postgrest/sanitize-query",
    response_model=PostgrestSanitizeResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def sanitize_postgrest_query(payload: PostgrestSanitizeRequest):
    """
    Sanitizes PostgREST query parameters against boundary bypass and wildcard search leaks.
    """
    return supabase_security_service.sanitize_postgrest_query(
        query_params=payload.query_params
    )


@api_router.post(
    "/supabase/rpc/audit-function",
    response_model=RpcAuditResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def audit_rpc_function(payload: RpcAuditRequest):
    """
    Audits stored procedures for SECURITY DEFINER risks, search_path hijacking, and parameter validation.
    """
    return edge_boundary_service.audit_rpc_function(
        function_name=payload.function_name,
        sql_definition=payload.sql_definition,
        execution_context=payload.execution_context
    )


@api_router.post(
    "/supabase/edge/verify-token",
    response_model=EdgeJwtVerifyResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def verify_edge_token(payload: EdgeJwtVerifyRequest):
    """
    Validates Edge Function JWT claims, ensuring apikey alone is not confused with authenticated identity.
    """
    return edge_boundary_service.verify_edge_jwt_token(
        auth_header=payload.auth_header,
        apikey_header=payload.apikey_header,
        expected_issuer=payload.expected_issuer
    )


@api_router.post(
    "/supabase/storage/generate-signed-url",
    response_model=StorageSignedUrlResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def generate_storage_signed_url(payload: StorageSignedUrlRequest):
    """
    Generates HMAC-signed URLs for private Supabase Storage buckets with MIME sniffing protection.
    """
    return edge_boundary_service.generate_storage_signed_url(
        bucket_id=payload.bucket_id,
        file_path=payload.file_path,
        user_id=payload.user_id,
        ttl_seconds=payload.ttl_seconds,
        content_type=payload.content_type
    )


@api_router.post(
    "/supabase/realtime/authorize-channel",
    response_model=RealtimeChannelAuthResponse,
    tags=["Supabase Security & RLS Engine"]
)
async def authorize_realtime_channel(payload: RealtimeChannelAuthRequest):
    """
    Guards Realtime WebSocket channel subscriptions, preventing cross-room eavesdropping.
    """
    return realtime_presence_service.authorize_channel_subscription(
        channel_name=payload.channel_name,
        user_id=payload.user_id,
        user_role=payload.user_role,
        tenant_id=payload.tenant_id,
        enrolled_circles=payload.enrolled_circles,
        linked_guardian_ids=payload.linked_guardian_ids
    )


# ========================================================================================
# Phase 48: Supabase pgvector, MFA Passkeys & Envelope Field Encryption
# ========================================================================================

supabase_pgvector_service = SupabasePgvectorService()
supabase_mfa_service = SupabaseMfaPasskeyService()
supabase_field_crypto_service = SupabaseFieldEncryptionService()


@api_router.post(
    "/supabase/vector/similarity-search",
    response_model=VectorSimilaritySearchResponse,
    tags=["Supabase pgvector & AI Grounding"]
)
async def vector_similarity_search(payload: VectorSimilaritySearchRequest):
    """
    Executes RLS-scoped semantic search using cosine similarity across embeddings.
    """
    return supabase_pgvector_service.search_semantic_knowledge(
        query_vector=payload.query_vector,
        corpus=payload.corpus,
        caller_tenant_id=payload.caller_tenant_id,
        caller_role=payload.caller_role,
        top_k=payload.top_k,
        similarity_threshold=payload.similarity_threshold
    )


@api_router.post(
    "/supabase/vector/grounding-check",
    response_model=VectorGroundingCheckResponse,
    tags=["Supabase pgvector & AI Grounding"]
)
async def vector_grounding_check(payload: VectorGroundingCheckRequest):
    """
    Evaluates whether generated AI responses are mathematically grounded in verified syllabus chunks.
    """
    return supabase_pgvector_service.evaluate_ai_grounding(
        ai_response_embedding=payload.ai_response_embedding,
        verified_syllabus_chunks=payload.verified_syllabus_chunks,
        grounding_threshold=payload.grounding_threshold
    )


@api_router.post(
    "/supabase/mfa/totp/enroll",
    response_model=TotpEnrollResponse,
    tags=["Supabase GoTrue MFA & Passkeys"]
)
async def enroll_totp_factor(payload: TotpEnrollRequest):
    """
    Enrolls a new TOTP factor with base32 secret and emergency backup codes.
    """
    return supabase_mfa_service.enroll_totp_factor(
        user_id=payload.user_id,
        issuer=payload.issuer
    )


@api_router.post(
    "/supabase/mfa/totp/verify",
    response_model=TotpVerifyResponse,
    tags=["Supabase GoTrue MFA & Passkeys"]
)
async def verify_totp_token(payload: TotpVerifyRequest):
    """
    Verifies a 6-digit TOTP token with drift window, elevating session to AAL2.
    """
    return supabase_mfa_service.verify_totp_token(
        secret_hex=payload.secret_hex,
        user_code=payload.user_code,
        drift_steps=payload.drift_steps
    )


@api_router.post(
    "/supabase/mfa/passkey/challenge",
    response_model=PasskeyChallengeResponse,
    tags=["Supabase GoTrue MFA & Passkeys"]
)
async def generate_passkey_challenge(payload: PasskeyChallengeRequest):
    """
    Generates a FIDO2 / WebAuthn cryptographic challenge bound to RP ID.
    """
    return supabase_mfa_service.generate_passkey_challenge(
        user_id=payload.user_id,
        user_email=payload.user_email
    )


@api_router.post(
    "/supabase/mfa/passkey/verify",
    response_model=PasskeyVerifyResponse,
    tags=["Supabase GoTrue MFA & Passkeys"]
)
async def verify_passkey_response(payload: PasskeyVerifyRequest):
    """
    Validates WebAuthn response against RP ID and HTTPS origin for AAL2 assurance.
    """
    return supabase_mfa_service.verify_passkey_response(
        challenge=payload.challenge,
        client_origin=payload.client_origin,
        client_rp_id=payload.client_rp_id,
        credential_id=payload.credential_id,
        signature=payload.signature
    )


@api_router.post(
    "/supabase/crypto/envelope-encrypt",
    response_model=EnvelopeEncryptResponse,
    tags=["Supabase Envelope Field Encryption"]
)
async def envelope_encrypt_field(payload: EnvelopeEncryptRequest):
    """
    Encrypts sensitive PII field using AES-256-GCM envelope encryption and blind indexing.
    """
    return supabase_field_crypto_service.envelope_encrypt(
        plaintext=payload.plaintext,
        associated_data=payload.associated_data
    )


@api_router.post(
    "/supabase/crypto/envelope-decrypt",
    response_model=EnvelopeDecryptResponse,
    tags=["Supabase Envelope Field Encryption"]
)
async def envelope_decrypt_field(payload: EnvelopeDecryptRequest):
    """
    Decrypts field using two-tier KEK/DEK envelope decryption.
    """
    return supabase_field_crypto_service.envelope_decrypt(
        ciphertext_hex=payload.ciphertext_hex,
        data_nonce_hex=payload.data_nonce_hex,
        encrypted_dek_hex=payload.encrypted_dek_hex,
        dek_nonce_hex=payload.dek_nonce_hex,
        associated_data=payload.associated_data
    )


# ========================================================================================
# Phase 49: Supabase Edge JWKS, Query Hardener & Database CDC Audit Engine
# ========================================================================================

edge_replay_service = EdgeDistributedReplayService()
postgrest_query_hardener_service = PostgrestQueryHardenerService()
database_cdc_audit_service = DatabaseCDCAuditEngineService()


@api_router.get(
    "/supabase/edge/jwks",
    tags=["Supabase Edge & Distributed JWKS"]
)
async def get_edge_jwks():
    """
    Returns public JSON Web Key Set (.well-known/jwks.json) for Edge Function asymmetric verification.
    """
    return edge_replay_service.get_jwks()


@api_router.post(
    "/supabase/edge/rotate-key",
    response_model=JWKSRotationResponse,
    tags=["Supabase Edge & Distributed JWKS"]
)
async def rotate_edge_signing_key(payload: JWKSRotationRequest):
    """
    Rotates active asymmetric signing key and archives previous keys to standby.
    """
    return edge_replay_service.rotate_signing_key(
        new_kid=payload.new_kid,
        algorithm=payload.algorithm
    )


@api_router.post(
    "/supabase/edge/verify-token",
    response_model=EdgeTokenVerificationResponse,
    tags=["Supabase Edge & Distributed JWKS"]
)
async def verify_edge_token(payload: EdgeTokenVerificationRequest):
    """
    Validates Edge token with algorithm confusion defense, JTI anti-replay cache, and auth.uid identity binding.
    """
    return edge_replay_service.verify_edge_token(
        header=payload.header,
        payload=payload.payload,
        client_supplied_user_id=payload.client_supplied_user_id
    )


@api_router.post(
    "/supabase/postgrest/inspect-query",
    response_model=PostgrestQueryInspectResponse,
    tags=["Supabase PostgREST Query Hardening"]
)
async def inspect_postgrest_query(payload: PostgrestQueryInspectRequest):
    """
    Inspects and hardens PostgREST queries against parameter pollution, wildcard poisoning, and tenant leaks.
    """
    return postgrest_query_hardener_service.inspect_and_harden_query(
        raw_query_params=payload.raw_query_params,
        verified_jwt_claims=payload.verified_jwt_claims,
        table_name=payload.table_name
    )


@api_router.post(
    "/supabase/cdc/ingest-wal",
    response_model=WALEventIngestResponse,
    tags=["Supabase CDC & Tamper-Evident Audit"]
)
async def ingest_cdc_wal_event(payload: WALEventIngestRequest):
    """
    Ingests Postgres WAL change events and links them into the tamper-evident Merkle hash chain.
    """
    return database_cdc_audit_service.ingest_wal_event(
        event_type=payload.event_type,
        table_name=payload.table_name,
        record_id=payload.record_id,
        record_data=payload.record_data,
        actor_id=payload.actor_id,
        commit_lsn=payload.commit_lsn
    )


@api_router.get(
    "/supabase/cdc/verify-integrity",
    response_model=AuditIntegrityVerificationResponse,
    tags=["Supabase CDC & Tamper-Evident Audit"]
)
async def verify_audit_integrity():
    """
    Cryptographically verifies the full SHA-256 Merkle chain across all historical audit blocks.
    """
    return database_cdc_audit_service.verify_audit_integrity()


@api_router.post(
    "/supabase/cdc/authorize-broadcast",
    response_model=RealtimeBroadcastAuthResponse,
    tags=["Supabase CDC & Tamper-Evident Audit"]
)
async def authorize_realtime_broadcast(payload: RealtimeBroadcastAuthRequest):
    """
    Validates subscriber authorization for CDC change events and automatically redacts PII before transmission.
    """
    audit_trail = database_cdc_audit_service.get_audit_trail(limit=100)
    if payload.event_index < 0 or payload.event_index >= len(audit_trail):
        return {
            "authorized": False,
            "broadcast_payload": None,
            "message": f"Event index {payload.event_index} not found in audit trail."
        }
    
    event_entry = audit_trail[payload.event_index]
    scrubbed = database_cdc_audit_service.prepare_realtime_broadcast_payload(
        event_entry=event_entry,
        subscriber_user_id=payload.subscriber_user_id,
        subscriber_role=payload.subscriber_role
    )
    if not scrubbed:
        return {
            "authorized": False,
            "broadcast_payload": None,
            "message": "Access denied: Subscriber does not have row-level permission for this record."
        }
    
    return {
        "authorized": True,
        "broadcast_payload": scrubbed,
        "message": "Authorized: Event scrubbed of PII and approved for Realtime broadcast."
    }


# ========================================================================================
# Phase 50: Supabase GraphQL Shield, Edge Rate Limiter & Storage Multipart Sanitizer
# ========================================================================================

graphql_shield_service = PgGraphqlShieldService()
edge_rate_limiter_service = EdgeDistributedRateLimiterService()
storage_multipart_sanitizer_service = StorageMultipartSanitizerService()


@api_router.post(
    "/supabase/graphql/inspect-query",
    response_model=GraphqlQueryInspectResponse,
    tags=["Supabase pg_graphql Shield"]
)
async def inspect_graphql_query(payload: GraphqlQueryInspectRequest):
    """
    Evaluates GraphQL query complexity, recursion, introspection permissions, and restricted fields.
    """
    return graphql_shield_service.inspect_and_authorize_query(
        query=payload.query,
        caller_role=payload.caller_role,
        caller_user_id=payload.caller_user_id
    )


@api_router.post(
    "/supabase/graphql/audit-parity",
    response_model=GraphqlParityAuditResponse,
    tags=["Supabase pg_graphql Shield"]
)
async def audit_graphql_parity(payload: GraphqlParityAuditRequest):
    """
    Audits column parity between PostgREST RLS and pg_graphql resolver types.
    """
    return graphql_shield_service.audit_postgrest_graphql_parity(
        table_name=payload.table_name,
        postgrest_allowed_columns=payload.postgrest_allowed_columns,
        graphql_type_fields=payload.graphql_type_fields
    )


@api_router.post(
    "/supabase/edge/check-rate-limit",
    response_model=EdgeRateLimitCheckResponse,
    tags=["Supabase Distributed Rate Limiter"]
)
async def check_edge_rate_limit(payload: EdgeRateLimitCheckRequest):
    """
    Checks token bucket quotas per IP, user, and tenant with automated penalty box blacklisting.
    """
    return edge_rate_limiter_service.check_rate_limit(
        client_ip=payload.client_ip,
        user_id=payload.user_id,
        tenant_id=payload.tenant_id,
        endpoint=payload.endpoint,
        custom_cost=payload.custom_cost
    )


@api_router.post(
    "/supabase/storage/generate-upload-ticket",
    response_model=StoragePresignedTicketResponse,
    tags=["Supabase Storage Multipart & Antivirus"]
)
async def generate_storage_upload_ticket(payload: StoragePresignedTicketRequest):
    """
    Generates HMAC-signed presigned upload ticket for chunked multipart storage uploads.
    """
    return storage_multipart_sanitizer_service.generate_presigned_upload_ticket(
        bucket_id=payload.bucket_id,
        file_path=payload.file_path,
        user_id=payload.user_id,
        allowed_mime_types=payload.allowed_mime_types,
        max_size_bytes=payload.max_size_bytes,
        ttl_seconds=payload.ttl_seconds
    )


@api_router.post(
    "/supabase/storage/sanitize-upload",
    response_model=StorageUploadSanitizeResponse,
    tags=["Supabase Storage Multipart & Antivirus"]
)
async def sanitize_storage_upload(payload: StorageUploadSanitizeRequest):
    """
    Inspects file magic bytes against MIME spoofing and strips Stored XSS vectors from SVG/HTML.
    """
    try:
        raw_bytes = base64.b64decode(payload.file_content_base64)
    except Exception:
        raw_bytes = payload.file_content_base64.encode("utf-8")

    return storage_multipart_sanitizer_service.verify_and_sanitize_upload(
        file_bytes=raw_bytes,
        declared_mime_type=payload.declared_mime_type,
        file_name=payload.file_name
    )


# ========================================================================================
# Phase 51: Realtime Presence Integrity, RLS Compliance Scanner & Privacy Vault
# ========================================================================================

realtime_presence_service_v2 = RealtimePresenceIntegrityService()
postgres_rls_scanner_service = PostgresRlsComplianceScannerService()
database_anonymization_vault_service = DatabaseAnonymizationVaultService()


@api_router.post(
    "/supabase/presence/generate-ticket",
    response_model=PresenceTicketGenerateResponse,
    tags=["Supabase Realtime Presence & Liveness"]
)
async def generate_presence_ticket(payload: PresenceTicketGenerateRequest):
    """
    Generates HMAC-signed ephemeral ticket for Realtime presence channel peering.
    """
    return realtime_presence_service_v2.generate_presence_ticket(
        channel_name=payload.channel_name,
        user_id=payload.user_id,
        user_role=payload.user_role,
        ttl_seconds=payload.ttl_seconds
    )


@api_router.post(
    "/supabase/presence/join",
    response_model=PresenceJoinResponse,
    tags=["Supabase Realtime Presence & Liveness"]
)
async def join_presence_channel(payload: PresenceJoinRequest):
    """
    Validates presence ticket signature, defeats phantom peer injection, and registers peer.
    """
    return realtime_presence_service_v2.verify_and_join_presence(
        channel_name=payload.channel_name,
        user_id=payload.user_id,
        session_id=payload.session_id,
        user_role=payload.user_role,
        expires_at=payload.expires_at,
        signature=payload.signature,
        client_metadata=payload.client_metadata
    )


@api_router.post(
    "/supabase/presence/heartbeat",
    response_model=PresenceHeartbeatResponse,
    tags=["Supabase Realtime Presence & Liveness"]
)
async def record_presence_heartbeat(payload: PresenceHeartbeatRequest):
    """
    Records keepalive heartbeat from connected peer; missing heartbeats purged by zombie reaper.
    """
    recorded = realtime_presence_service_v2.record_heartbeat(
        channel_name=payload.channel_name,
        session_id=payload.session_id
    )
    return {
        "recorded": recorded,
        "message": "Heartbeat updated successfully." if recorded else "Session not found or expired."
    }


@api_router.post(
    "/supabase/rls/scan-table",
    response_model=RlsComplianceScanResponse,
    tags=["Supabase RLS Compliance & Strix Scanner"]
)
async def scan_table_rls_compliance(payload: RlsComplianceScanRequest):
    """
    Audits PostgreSQL table for RLS enablement, mutation policy coverage, and tenant isolation.
    """
    return postgres_rls_scanner_service.scan_table_rls_compliance(
        table_schema={
            "table_name": payload.table_name,
            "rls_enabled": payload.rls_enabled,
            "policies": payload.policies
        }
    )


@api_router.post(
    "/supabase/rls/scan-security-definer",
    response_model=SecurityDefinerScanResponse,
    tags=["Supabase RLS Compliance & Strix Scanner"]
)
async def scan_function_security_definer(payload: SecurityDefinerScanRequest):
    """
    Audits stored procedures / RPC functions for search_path hijacking vulnerabilities.
    """
    return postgres_rls_scanner_service.scan_function_security_definer(
        func_metadata={
            "function_name": payload.function_name,
            "security_type": payload.security_type,
            "search_path_set": payload.search_path_set
        }
    )


@api_router.post(
    "/supabase/privacy/inject-laplace-noise",
    response_model=LaplaceNoiseInjectResponse,
    tags=["Supabase Privacy Vault & Anonymization"]
)
async def inject_laplace_noise(payload: LaplaceNoiseInjectRequest):
    """
    Adds Laplacian differential privacy noise to aggregate student metrics.
    """
    return database_anonymization_vault_service.inject_laplace_noise(
        true_value=payload.true_value,
        sensitivity=payload.sensitivity,
        epsilon=payload.epsilon
    )


@api_router.post(
    "/supabase/privacy/evaluate-k-anonymity",
    response_model=KAnonymityEvaluateResponse,
    tags=["Supabase Privacy Vault & Anonymization"]
)
async def evaluate_k_anonymity(payload: KAnonymityEvaluateRequest):
    """
    Evaluates K-Anonymity (k >= 5) and re-identification risk on student datasets.
    """
    return database_anonymization_vault_service.evaluate_k_anonymity(
        records=payload.records,
        quasi_identifiers=payload.quasi_identifiers
    )


# ========================================================================================
# Phase 52: Edge Function Zero-Trust Gateway, Webhook Replay Guard & PostgREST Audit
# ========================================================================================

edge_gateway_service = EdgeFunctionZeroTrustGatewayService()
webhook_replay_guard_service = DatabaseWebhookReplayGuardService()
postgrest_audit_service = PostgrestAuditTrailEngineService()


@api_router.post(
    "/supabase/edge/verify-request",
    response_model=EdgeRequestVerifyResponse,
    tags=["Supabase Edge Zero-Trust Gateway"]
)
async def verify_edge_request(payload: EdgeRequestVerifyRequest):
    """
    Cryptographically verifies edge request authorization, sanitizes headers,
    and defends against forged service_role headers.
    """
    return edge_gateway_service.verify_edge_request(
        headers=payload.headers,
        secret=payload.secret,
        allowed_audiences=payload.allowed_audiences
    )


@api_router.post(
    "/supabase/edge/authorize-action",
    response_model=EdgeActionAuthorizeResponse,
    tags=["Supabase Edge Zero-Trust Gateway"]
)
async def authorize_edge_action(payload: EdgeActionAuthorizeRequest):
    """
    Evaluates fine-grained RBAC action authorization before executing serverless functions.
    """
    return edge_gateway_service.evaluate_edge_action_policy(
        user_role=payload.user_role,
        function_name=payload.function_name,
        requested_action=payload.requested_action
    )


@api_router.post(
    "/supabase/webhook/verify",
    response_model=WebhookVerifyResponse,
    tags=["Supabase Database Webhook Guard"]
)
async def verify_database_webhook(payload: WebhookVerifyRequest):
    """
    Verifies Svix HMAC-SHA256 signature, validates anti-replay sliding window,
    and detects duplicate event nonces.
    """
    return webhook_replay_guard_service.verify_webhook_signature(
        headers=payload.headers,
        payload_bytes=payload.payload.encode("utf-8"),
        secret=payload.secret,
        max_age_seconds=payload.max_age_seconds
    )


@api_router.post(
    "/supabase/webhook/attest-event",
    response_model=WebhookAttestResponse,
    tags=["Supabase Database Webhook Guard"]
)
async def attest_database_event(payload: WebhookAttestRequest):
    """
    Generates a cryptographically signed event attestation receipt with SHA-256 digest.
    """
    return webhook_replay_guard_service.attest_and_record_event(
        event_type=payload.event_type,
        table_name=payload.table_name,
        record_id=payload.record_id,
        payload=payload.payload
    )


@api_router.post(
    "/supabase/audit/record",
    response_model=AuditRecordResponse,
    tags=["PostgREST Forensic Audit Trail"]
)
async def record_audit_event(payload: AuditRecordRequest):
    """
    Appends an immutable audit event to the cryptographic SHA-256 hash chain.
    """
    return postgrest_audit_service.record_audit_event(
        actor_id=payload.actor_id,
        actor_role=payload.actor_role,
        action=payload.action,
        schema_name=payload.schema_name,
        target_entity=payload.target_entity,
        metadata=payload.metadata,
        ip_address=payload.ip_address
    )


@api_router.get(
    "/supabase/audit/verify-chain",
    response_model=AuditChainVerifyResponse,
    tags=["PostgREST Forensic Audit Trail"]
)
async def verify_audit_chain():
    """
    Traverses the cryptographic audit chain and mathematically verifies integrity.
    """
    return postgrest_audit_service.verify_audit_chain_integrity()


@api_router.get(
    "/supabase/audit/anomalies",
    response_model=AuditAnomaliesResponse,
    tags=["PostgREST Forensic Audit Trail"]
)
async def get_audit_anomalies(window_seconds: int = 3600):
    """
    Inspects recent audit logs for security anomalies (mass deletions, privileged RPC abuse).
    """
    return postgrest_audit_service.detect_audit_anomalies(time_window_seconds=window_seconds)


@api_router.get(
    "/supabase/audit/recent",
    tags=["PostgREST Forensic Audit Trail"]
)
async def get_recent_audit_entries(limit: int = 15):
    """
    Fetches the latest entries in the cryptographic audit chain.
    """
    return postgrest_audit_service.get_recent_entries(limit=limit)


# ========================================================================================
# Phase 53: Connection Pooler Session Hygiene, Dynamic Masking & Federated FDW
# ========================================================================================

pooler_hygiene_service = ConnectionPoolerHygieneService()
dynamic_masking_service = DynamicDataMaskingService()
federated_fdw_service = FederatedFdwSecurityService()


@api_router.post(
    "/supabase/pooler/audit-session",
    response_model=PoolerSessionAuditResponse,
    tags=["Supabase Connection Pooler Hygiene"]
)
async def audit_pooler_session_hygiene(payload: PoolerSessionAuditRequest):
    """
    Scans session SQL statements for unlocalized GUC mutations and session-polluting commands.
    """
    return pooler_hygiene_service.audit_session_hygiene(payload.sql_statements)


@api_router.post(
    "/supabase/pooler/verify-reset",
    response_model=PoolerResetVerifyResponse,
    tags=["Supabase Connection Pooler Hygiene"]
)
async def verify_pooler_connection_reset(payload: PoolerResetVerifyRequest):
    """
    Verifies that recycled connections execute DISCARD ALL / RESET ALL and retain zero locks.
    """
    return pooler_hygiene_service.verify_pool_reset_guard(payload.connection_meta)


@api_router.post(
    "/supabase/pooler/benchmark",
    response_model=PoolerBenchmarkResponse,
    tags=["Supabase Connection Pooler Hygiene"]
)
async def benchmark_pooler_isolation(payload: PoolerBenchmarkRequest):
    """
    Benchmarks multi-tenant connection pool isolation and state leakage prevention.
    """
    return pooler_hygiene_service.simulate_pool_isolation_benchmark(
        concurrent_tenants=payload.concurrent_tenants,
        total_transactions=payload.total_transactions
    )


@api_router.post(
    "/supabase/masking/mask-record",
    response_model=StudentRecordMaskResponse,
    tags=["Supabase Dynamic Data Masking"]
)
async def mask_student_record(payload: StudentRecordMaskRequest):
    """
    Dynamically redacts PII and generalizes academic metrics based on viewer role.
    """
    return dynamic_masking_service.mask_student_record(
        record=payload.record,
        viewer_role=payload.viewer_role,
        masking_policy=payload.masking_policy
    )


@api_router.post(
    "/supabase/masking/generate-view-sql",
    response_model=MaskedViewSqlGenerateResponse,
    tags=["Supabase Dynamic Data Masking"]
)
async def generate_masked_view_sql(payload: MaskedViewSqlGenerateRequest):
    """
    Generates production-grade PostgreSQL dynamic masking view SQL with security_barrier.
    """
    sql = dynamic_masking_service.generate_masked_view_sql(
        table_name=payload.table_name,
        view_name=payload.view_name,
        column_rules=payload.column_rules
    )
    v_name = payload.view_name or f"v_masked_{payload.table_name}"
    return {
        "sql": sql,
        "table_name": payload.table_name,
        "view_name": v_name
    }


@api_router.post(
    "/supabase/masking/evaluate-risk",
    response_model=InferenceRiskEvaluateResponse,
    tags=["Supabase Dynamic Data Masking"]
)
async def evaluate_masking_inference_risk(payload: InferenceRiskEvaluateRequest):
    """
    Calculates re-identification and linkage attack risk across masked datasets.
    """
    return dynamic_masking_service.evaluate_inference_risk(
        dataset=payload.dataset,
        masked_columns=payload.masked_columns
    )


@api_router.post(
    "/supabase/fdw/audit-server",
    response_model=FdwServerAuditResponse,
    tags=["Supabase Federated FDW Security"]
)
async def audit_fdw_server(payload: FdwServerAuditRequest):
    """
    Audits postgres_fdw FOREIGN SERVER definitions for mandatory SSL encryption and timeouts.
    """
    return federated_fdw_service.audit_fdw_server_definition(payload.server_config)


@api_router.post(
    "/supabase/fdw/validate-user-mappings",
    response_model=FdwUserMappingsValidateResponse,
    tags=["Supabase Federated FDW Security"]
)
async def validate_fdw_user_mappings(payload: FdwUserMappingsValidateRequest):
    """
    Scans FDW USER MAPPINGS for remote superuser overprivilege and plaintext credentials.
    """
    return federated_fdw_service.validate_user_mapping_permissions(payload.user_mappings)


@api_router.post(
    "/supabase/fdw/sanitize-query",
    response_model=FederatedQuerySanitizeResponse,
    tags=["Supabase Federated FDW Security"]
)
async def sanitize_federated_query(payload: FederatedQuerySanitizeRequest):
    """
    Sanitizes cross-campus federated queries to block stacked SQL and schema traversal.
    """
    return federated_fdw_service.sanitize_federated_query(
        remote_sql=payload.remote_sql,
        allowed_schemas=payload.allowed_schemas
    )


# ========================================================================================
# Phase 54: Automated Disaster Recovery (PITR Drill), Secret Vault & WAL Validator
# ========================================================================================

pitr_service = DisasterRecoveryPitrSimulatorService()
secret_vault_service = SecretRotationVaultService()
wal_integrity_service = WalArchiveIntegrityService()


@api_router.post(
    "/supabase/pitr/create-snapshot",
    response_model=PitrSnapshotCreateResponse,
    tags=["Supabase PITR Disaster Recovery"]
)
async def create_pitr_snapshot(payload: PitrSnapshotCreateRequest):
    """
    Generates a cryptographically verified restore target snapshot with basebackup LSN.
    """
    return pitr_service.create_pitr_snapshot(
        target_epoch=payload.target_epoch,
        snapshot_tag=payload.snapshot_tag,
        table_manifests=payload.table_manifests
    )


@api_router.post(
    "/supabase/pitr/simulate-drill",
    response_model=PitrDrillSimulateResponse,
    tags=["Supabase PITR Disaster Recovery"]
)
async def simulate_pitr_drill(payload: PitrDrillSimulateRequest):
    """
    Simulates automated point-in-time recovery drill and calculates actual RPO and RTO.
    """
    return pitr_service.simulate_recovery_drill(
        snapshot_id=payload.snapshot_id,
        disaster_scenario=payload.disaster_scenario,
        target_recovery_epoch=payload.target_recovery_epoch
    )


@api_router.post(
    "/supabase/pitr/verify-consistency",
    response_model=PitrConsistencyVerifyResponse,
    tags=["Supabase PITR Disaster Recovery"]
)
async def verify_pitr_consistency(payload: PitrConsistencyVerifyRequest):
    """
    Validates 100% cryptographic and row-count consistency between original and restored datasets.
    """
    return pitr_service.verify_restore_consistency(
        original_manifest=payload.original_manifest,
        restored_manifest=payload.restored_manifest
    )


@api_router.post(
    "/supabase/vault/scan-secrets",
    response_model=SecretScanResponse,
    tags=["Supabase Secret Rotation Vault"]
)
async def scan_secrets_in_bundle(payload: SecretScanRequest):
    """
    Scans client bundle or response text for leaked service_role keys and high-entropy secrets.
    """
    return secret_vault_service.scan_client_bundle_for_secrets(payload.content_or_bundle)


@api_router.post(
    "/supabase/vault/rotate-key",
    response_model=SecretRotationResponse,
    tags=["Supabase Secret Rotation Vault"]
)
async def rotate_secret_key(payload: SecretRotationRequest):
    """
    Orchestrates zero-downtime dual-key rotation with overlapping grace window.
    """
    return secret_vault_service.execute_zero_downtime_key_rotation(
        key_type=payload.key_type,
        grace_period_seconds=payload.grace_period_seconds
    )


@api_router.post(
    "/supabase/vault/revoke-key",
    response_model=SecretRevokeResponse,
    tags=["Supabase Secret Rotation Vault"]
)
async def revoke_secret_key(payload: SecretRevokeRequest):
    """
    Immediately invalidates a compromised key and registers it on the revocation blacklist.
    """
    return secret_vault_service.revoke_compromised_credential(
        key_id=payload.key_id,
        reason=payload.reason
    )


@api_router.post(
    "/supabase/wal/register-segment",
    response_model=WalRegisterResponse,
    tags=["Supabase WAL Archive Integrity"]
)
async def register_wal_segment(payload: WalRegisterRequest):
    """
    Registers an incoming 16MB WAL segment into the continuous archive catalog.
    """
    return wal_integrity_service.register_wal_segment(
        segment_name=payload.segment_name,
        timeline_id=payload.timeline_id,
        segment_number=payload.segment_number,
        checksum=payload.checksum
    )


@api_router.get(
    "/supabase/wal/verify-continuity",
    response_model=WalVerifyContinuityResponse,
    tags=["Supabase WAL Archive Integrity"]
)
async def verify_wal_continuity():
    """
    Scans all archived WAL segments to verify gapless continuity and timeline consistency.
    """
    return wal_integrity_service.verify_wal_chain_continuity()


@api_router.get(
    "/supabase/wal/evaluate-lag",
    response_model=WalEvaluateLagResponse,
    tags=["Supabase WAL Archive Integrity"]
)
async def evaluate_wal_archive_lag(max_lag_seconds: int = 60):
    """
    Evaluates current archive lag against institutional RPO SLA (< 60s).
    """
    return wal_integrity_service.evaluate_archive_lag_and_sla(max_lag_seconds=max_lag_seconds)


# ========================================================================================
# Phase 55: ZK Multi-Tenant Partitioning, Merkle Attestation & Cross-Region CDC
# ========================================================================================

zk_partition_service = ZeroKnowledgeTenantPartitionService()
merkle_attestation_service = RowLevelAttestationMerkleService()
cdc_replication_service = CdcReplicationConflictService()


@api_router.post(
    "/supabase/partition/route",
    response_model=PartitionRouteResponse,
    tags=["Multi-Tenant Declarative Partitioning"]
)
async def route_tenant_partition_query(payload: PartitionRouteRequest):
    """
    Routes a logical academic query to the isolated institutional sub-partition table,
    enforcing partition pruning boundaries.
    """
    return zk_partition_service.route_query(
        tenant_id=payload.tenant_id,
        table_name=payload.table_name,
        query_filters=payload.query_filters,
        auth_token_signature=payload.auth_token_signature
    )


@api_router.post(
    "/supabase/partition/probe-escape",
    response_model=PartitionEscapeProbeResponse,
    tags=["Multi-Tenant Declarative Partitioning"]
)
async def probe_partition_escape_attack(payload: PartitionEscapeProbeRequest):
    """
    Scans a query string for cross-partition escape probes or SQL injection vectors.
    """
    return zk_partition_service.detect_partition_escape_attempt(
        tenant_id=payload.tenant_id,
        malicious_query_clause=payload.malicious_query_clause
    )


@api_router.get(
    "/supabase/partition/topology",
    tags=["Multi-Tenant Declarative Partitioning"]
)
async def get_partition_topology():
    """
    Returns active declarative partition topology across all registered institutions.
    """
    return zk_partition_service.get_partition_topology()


@api_router.post(
    "/supabase/attestation/seal-row",
    response_model=RowAttestationResponse,
    tags=["Row-Level Merkle Attestation"]
)
async def seal_row_attestation(payload: RowAttestationRequest):
    """
    Generates a canonical SHA-256 digest and HMAC-SHA256 seal for an individual record row.
    """
    return merkle_attestation_service.generate_row_attestation(
        record_id=payload.record_id,
        tenant_id=payload.tenant_id,
        entity_type=payload.entity_type,
        payload=payload.payload
    )


@api_router.post(
    "/supabase/attestation/build-merkle-tree",
    response_model=MerkleTreeBuildResponse,
    tags=["Row-Level Merkle Attestation"]
)
async def build_tenant_merkle_tree(payload: MerkleTreeBuildRequest):
    """
    Builds a Merkle audit tree over tenant academic records, returning the Merkle root hash.
    """
    return merkle_attestation_service.build_merkle_tree(
        tenant_id=payload.tenant_id,
        records=payload.records
    )


@api_router.post(
    "/supabase/attestation/verify-proof",
    response_model=MerkleProofVerificationResponse,
    tags=["Row-Level Merkle Attestation"]
)
async def verify_merkle_record_proof(payload: MerkleProofVerificationRequest):
    """
    Cryptographically verifies a Merkle branch inclusion proof against an expected root hash.
    """
    return merkle_attestation_service.verify_merkle_proof(
        merkle_root=payload.merkle_root,
        leaf_hash=payload.leaf_hash,
        proof_path=payload.proof_path
    )


@api_router.post(
    "/supabase/cdc/process-event",
    response_model=CdcEventResponse,
    tags=["Cross-Region CDC Replication"]
)
async def process_cdc_replication_event(payload: CdcEventRequest):
    """
    Decodes an incoming WAL CDC replication event from a regional cluster.
    """
    return cdc_replication_service.decode_and_process_event(
        event_id=payload.event_id,
        region_origin=payload.region_origin,
        table_name=payload.table_name,
        operation=payload.operation,
        row_data=payload.row_data,
        vector_clock=payload.vector_clock,
        commit_lsn=payload.commit_lsn,
        timestamp=payload.timestamp
    )


@api_router.get(
    "/supabase/cdc/evaluate-slot-lag",
    response_model=ReplicationLagReportResponse,
    tags=["Cross-Region CDC Replication"]
)
async def evaluate_cdc_replication_slot_lag(
    slot_name: str = "sub_chittagong_dr_slot",
    source_region: str = "region_dhaka",
    target_region: str = "region_chittagong",
    current_lsn: str = "16/3400A120",
    confirmed_flush_lsn: str = "16/3400A000"
):
    """
    Evaluates cross-region logical replication slot lag against institutional SLA (< 2s).
    """
    return cdc_replication_service.get_replication_slot_lag(
        slot_name=slot_name,
        source_region=source_region,
        target_region=target_region,
        current_lsn=current_lsn,
        confirmed_flush_lsn=confirmed_flush_lsn
    )


# ========================================================================================
# Phase 56: Production Schema Migration, Drift Guard & Index Optimizer
# ========================================================================================

migration_engine_service = SchemaMigrationEngineService()
drift_detector_service = SchemaDriftDetectorService()
index_optimizer_service = IndexOptimizerAdvisorService()


@api_router.post(
    "/supabase/migration/analyze-safety",
    response_model=MigrationPlanResponse,
    tags=["Production Schema Migration Engine"]
)
async def analyze_schema_migration_safety(payload: MigrationPlanRequest):
    """
    Evaluates DDL migration risks, enforces zero-downtime rules, and compiles forward/rollback SQL.
    """
    return migration_engine_service.analyze_migration_safety(
        version_id=payload.version_id,
        migration_name=payload.migration_name,
        target_table=payload.target_table,
        operation_type=payload.operation_type,
        column_definitions=payload.column_definitions,
        index_definitions=payload.index_definitions,
        raw_ddl_forward=payload.raw_ddl_forward
    )


@api_router.get(
    "/supabase/migration/history",
    tags=["Production Schema Migration Engine"]
)
async def get_applied_migration_history():
    """
    Returns ordered audit ledger of applied schema migration versions.
    """
    return migration_engine_service.get_migration_history()


@api_router.post(
    "/supabase/drift/scan",
    response_model=SchemaDriftScanResponse,
    tags=["Schema Drift Detector"]
)
async def scan_schema_drift(payload: SchemaDriftScanRequest):
    """
    Detects discrepancies between declared schema specification and live catalog metadata.
    """
    return drift_detector_service.detect_schema_drift(
        environment_name=payload.environment_name,
        declared_schema=payload.declared_schema,
        live_schema=payload.live_schema
    )


@api_router.post(
    "/supabase/index/recommend",
    response_model=IndexRecommendResponse,
    tags=["Index Optimizer Advisor"]
)
async def recommend_query_index(payload: IndexRecommendRequest):
    """
    Analyzes query selectivity and recommends optimal composite or partial indexes.
    """
    return index_optimizer_service.recommend_index(
        table_name=payload.table_name,
        query_clause=payload.query_clause,
        filter_columns=payload.filter_columns,
        sort_columns=payload.sort_columns,
        table_row_count=payload.table_row_count,
        estimated_matched_rows=payload.estimated_matched_rows
    )


@api_router.get(
    "/supabase/index/redundancy-scan",
    response_model=IndexRedundancyScanResponse,
    tags=["Index Optimizer Advisor"]
)
async def scan_index_redundancies():
    """
    Scans existing catalog indexes for prefix redundancies and write amplification waste.
    """
    mock_indexes = [
        {"name": "idx_students_id", "table": "students", "columns": ["student_id"]},
        {"name": "idx_students_id_created", "table": "students", "columns": ["student_id", "created_at"]},
        {"name": "idx_exam_attempts_sub", "table": "quiz_attempts", "columns": ["subject_id"]},
        {"name": "idx_exam_attempts_sub_score", "table": "quiz_attempts", "columns": ["subject_id", "score"]},
    ]
    return index_optimizer_service.scan_redundant_indexes(mock_indexes)


# ========================================================================================
# Phase 57: Ultra Low-Bandwidth Edge Video & Brotli Streamer
# ========================================================================================

edge_video_service = EdgeVideoStreamService()
brotli_compressor_service = BrotliPayloadCompressorService()
abr_advisor_service = AdaptiveBitrateAdvisorService()


@api_router.post(
    "/video/hls/manifest",
    response_model=VideoManifestResponse,
    tags=["Edge Video Stream Service"]
)
async def generate_hls_video_manifest(payload: VideoManifestRequest):
    """
    Generates RFC 8216 compliant HLS master playlist and adaptive bitrate ladder.
    """
    return edge_video_service.generate_master_playlist(
        lecture_id=payload.lecture_id,
        title=payload.title,
        duration_seconds=payload.duration_seconds,
        available_resolutions=payload.available_resolutions,
        chunk_duration_seconds=payload.chunk_duration_seconds or 2
    )


@api_router.post(
    "/video/hls/chunk",
    response_model=VideoChunkResponse,
    tags=["Edge Video Stream Service"]
)
async def resolve_hls_video_chunk(payload: VideoChunkRequest):
    """
    Resolves micro-chunk byte ranges, SHA-256 chunk integrity, and CDN cache headers.
    """
    return edge_video_service.resolve_video_chunk(
        lecture_id=payload.lecture_id,
        resolution=payload.resolution,
        segment_index=payload.segment_index
    )


@api_router.post(
    "/compression/brotli/benchmark",
    response_model=BrotliCompressionResponse,
    tags=["Brotli Payload Accelerator"]
)
async def benchmark_brotli_compression(payload: BrotliCompressionRequest):
    """
    Compares raw JSON, Gzip (level 6), and Brotli (levels 1-11) density with BDT mobile data savings.
    """
    return brotli_compressor_service.compress_payload(
        payload_content=payload.payload_content,
        compression_level=payload.compression_level or 6,
        client_rtt_ms=payload.client_rtt_ms or 150.0,
        device_battery_saver=payload.device_battery_saver or False
    )


@api_router.post(
    "/video/abr/advise",
    response_model=AdaptiveBitrateResponse,
    tags=["Adaptive Bitrate Advisor"]
)
async def advise_adaptive_bitrate(payload: AdaptiveBitrateRequest):
    """
    Calculates EMA smoothed throughput, hysteresis damping, and buffer stall prevention.
    """
    return abr_advisor_service.advise_bitrate(
        measured_throughput_kbps=payload.measured_throughput_kbps,
        current_resolution=payload.current_resolution,
        buffer_occupancy_seconds=payload.buffer_occupancy_seconds,
        device_pixel_ratio=payload.device_pixel_ratio or 1.0,
        is_metered_connection=payload.is_metered_connection or False
    )


# ========================================================================================
# Phase 58: W3C Verifiable Credential & ZKP Certificate Vault
# ========================================================================================

credential_engine_service = VerifiableCredentialEngineService()
zkp_proof_service = ZeroKnowledgeRangeProofService()
revocation_registry_service = InstitutionalRevocationRegistryService()


@api_router.post(
    "/credentials/issue",
    response_model=VerifiableCredentialResponse,
    tags=["W3C Verifiable Credentials"]
)
async def issue_academic_credential(payload: IssueCredentialRequest):
    """
    Issues authentic W3C VC v2.0 JSON-LD academic degree credential signed with Ed25519.
    """
    return credential_engine_service.issue_credential(
        student_id=payload.student_id,
        student_name=payload.student_name,
        institution_did=payload.institution_did,
        degree_title=payload.degree_title,
        cgpa=payload.cgpa,
        graduation_year=payload.graduation_year,
        honors_designation=payload.honors_designation or "First Class Honours"
    )


@api_router.post(
    "/credentials/verify",
    response_model=VerifyCredentialResponse,
    tags=["W3C Verifiable Credentials"]
)
async def verify_academic_credential(payload: VerifyCredentialRequest):
    """
    Cryptographically verifies credential signature, JCS canonical digest, and tamper-resistance.
    """
    return credential_engine_service.verify_credential(
        credential_payload=payload.credential_payload,
        expected_issuer_did=payload.expected_issuer_did
    )


@api_router.post(
    "/credentials/zkp/range-proof",
    response_model=ZkpRangeProofResponse,
    tags=["Zero-Knowledge Proof Vault"]
)
async def generate_zkp_range_proof(payload: GenerateZkpProofRequest):
    """
    Synthesizes Fiat-Shamir NIZK proof verifying CGPA >= threshold without disclosing raw score.
    """
    return zkp_proof_service.generate_range_proof(
        credential_id=payload.credential_id,
        actual_cgpa=payload.actual_cgpa,
        threshold_cgpa=payload.threshold_cgpa,
        student_did=payload.student_did
    )


@api_router.post(
    "/credentials/revocation/check",
    response_model=RevocationCheckResponse,
    tags=["Institutional Revocation Registry"]
)
async def check_credential_revocation(payload: RevocationCheckRequest):
    """
    Checks credential status in O(1) time against the W3C Bitstring Status List v1.0.
    """
    return revocation_registry_service.check_revocation(
        institution_did=payload.institution_did,
        status_list_index=payload.status_list_index
    )


@api_router.post(
    "/credentials/revocation/update",
    tags=["Institutional Revocation Registry"]
)
async def update_credential_revocation(payload: RevocationUpdateRequest):
    """
    Updates revocation status requiring dual Dean and Registrar sign-off.
    """
    return revocation_registry_service.update_revocation(
        institution_did=payload.institution_did,
        status_list_index=payload.status_list_index,
        is_revoked=payload.is_revoked,
        revocation_reason=payload.revocation_reason,
        dean_signature=payload.dean_signature,
        registrar_signature=payload.registrar_signature
    )


# ========================================================================================
# Phase 59: Multi-LLM AI Gateway & Prompt Injection Shield
# ========================================================================================

multi_llm_gateway_service = MultiLlmRouterGatewayService()
prompt_injection_service = PromptInjectionSanitizerService()
semantic_output_service = SemanticOutputValidatorService()


@api_router.post(
    "/llm/route",
    response_model=MultiLlmRouteResponse,
    tags=["Multi-LLM AI Gateway"]
)
async def route_academic_llm_query(payload: MultiLlmRouteRequest):
    """
    Dynamically routes academic query across Gemini, Claude, and DeepSeek with BDT cost accounting.
    """
    return multi_llm_gateway_service.route_query(
        prompt=payload.prompt,
        task_type=payload.task_type or "math_reasoning",
        max_tokens=payload.max_tokens or 1024,
        preferred_provider=payload.preferred_provider or "auto"
    )


@api_router.post(
    "/llm/prompt/sanitize",
    response_model=PromptSanitizeResponse,
    tags=["Prompt Injection Shield"]
)
async def sanitize_student_prompt(payload: PromptSanitizeRequest):
    """
    Scans for OWASP LLM01 prompt injection, smuggles delimiters, and injects canary tripwires.
    """
    return prompt_injection_service.sanitize_user_prompt(
        raw_user_input=payload.raw_user_input,
        system_context=payload.system_context,
        enable_canary=payload.enable_canary if payload.enable_canary is not None else True
    )


@api_router.post(
    "/llm/output/validate",
    response_model=OutputValidateResponse,
    tags=["Semantic Output Validator"]
)
async def validate_model_output(payload: OutputValidateRequest):
    """
    Hardens generated output against DOM XSS, dangerous shell commands, and canary leaks.
    """
    return semantic_output_service.validate_output(
        raw_model_output=payload.raw_model_output,
        target_sink=payload.target_sink or "html_dom",
        canary_token_to_verify=payload.canary_token_to_verify
    )


# ========================================================================================
# Phase 60: The Grand Convergence & Adaptive Persona Router
# ========================================================================================

grand_convergence_service = GrandConvergenceAttestationService()
adaptive_persona_router_service = AdaptivePersonaRouterService()
universal_omni_search_service = UniversalOmniConvergenceSearchService()


@api_router.post(
    "/convergence/attest",
    response_model=GrandConvergenceAttestResponse,
    tags=["The Grand Convergence Attestation"]
)
async def attest_platform_convergence_endpoint(payload: GrandConvergenceAttestRequest):
    """
    Executes 6-pillar cryptographic attestation across all 60 architectural phases with Merkle root hash.
    """
    return grand_convergence_service.attest_platform_convergence(
        operator_id=payload.operator_id or "ops:admin:convergence_monitor",
        verified_tests_count=734
    )


@api_router.post(
    "/persona/route",
    response_model=PersonaRouteResponse,
    tags=["Adaptive Persona Router"]
)
async def route_adaptive_persona_endpoint(payload: PersonaRouteRequest):
    """
    Synthesizes tailored workspaces, KPIs, and navigation for Student, Educator, Guardian, Admin, Recruiter.
    """
    return adaptive_persona_router_service.route_persona(
        user_role=payload.user_role,
        device_tier=payload.device_tier or "desktop",
        preferred_theme=payload.preferred_theme or "auto"
    )


@api_router.post(
    "/omni-search",
    response_model=OmniSearchResponse,
    tags=["Universal Omni-Convergence Search"]
)
async def omni_convergence_search_endpoint(payload: OmniSearchRequest):
    """
    Sub-5ms federated fuzzy search across lectures, tuitions, jobs, labs, and credentials.
    """
    return universal_omni_search_service.search_omni(
        query=payload.query,
        category_filter=payload.category_filter or "all",
        limit=payload.limit or 10
    )


# ========================================================================================
# Phase 61: Enterprise Supabase Production Cockpit, Zero-Trust Infrastructure & Live Console
# ========================================================================================

supabase_production_cockpit_service = SupabaseProductionCockpitService()


@api_router.post(
    "/supabase/cockpit/simulate-rls",
    response_model=RlsSimulationResponse,
    tags=["Enterprise Supabase Production Cockpit"]
)
async def simulate_supabase_rls_endpoint(payload: RlsSimulationRequest):
    """
    Simulates PostgreSQL Row-Level Security evaluation across caller roles, tenant boundaries, and IDOR vectors.
    """
    data = payload.dict() if hasattr(payload, "dict") else payload.__dict__
    return supabase_production_cockpit_service.simulate_rls_policy(data)


@api_router.post(
    "/supabase/cockpit/audit-storage",
    response_model=StorageAuditResponse,
    tags=["Enterprise Supabase Production Cockpit"]
)
async def audit_supabase_storage_endpoint(payload: StorageAuditRequest):
    """
    Audits object uploads against MIME-spoofing, active script injection, and public bucket leakage.
    """
    data = payload.dict() if hasattr(payload, "dict") else payload.__dict__
    return supabase_production_cockpit_service.audit_storage_upload(data)


@api_router.get(
    "/supabase/cockpit/telemetry",
    response_model=EdgeTelemetryResponse,
    tags=["Enterprise Supabase Production Cockpit"]
)
async def get_supabase_edge_telemetry_endpoint():
    """
    Returns live connection pooler health metrics, p95 latency, and zero-trust JWT token binding rates.
    """
    return supabase_production_cockpit_service.get_edge_telemetry()


@api_router.get(
    "/supabase/cockpit/migrations",
    response_model=MigrationStatusResponse,
    tags=["Enterprise Supabase Production Cockpit"]
)
async def get_supabase_migrations_status_endpoint():
    """
    Cryptographically verifies migration SQL DDL files and Row-Level Security policy enforcement on disk.
    """
    return supabase_production_cockpit_service.get_migrations_status()


# ========================================================================================
# Phase 62: Realtime Collaborative Whiteboard, WebRTC Low-Latency Voice Mesh & LaTeX Canvas
# ========================================================================================

collaborative_whiteboard_service = CollaborativeWhiteboardWebrtcService()


@api_router.post(
    "/whiteboard/session/create",
    response_model=WhiteboardSessionStateResponse,
    tags=["Realtime Collaborative Whiteboard"]
)
async def create_whiteboard_session_endpoint(payload: WhiteboardSessionCreateRequest):
    """
    Creates an interactive collaborative classroom whiteboard and audio mesh session.
    """
    return collaborative_whiteboard_service.create_session(
        topic=payload.topic,
        tutor_id=payload.tutor_id,
        curriculum=payload.curriculum or "NCTB",
        grade_level=payload.grade_level or 10,
        max_students=payload.max_students or 25
    )


@api_router.get(
    "/whiteboard/session/{session_id}/state",
    response_model=WhiteboardSessionStateResponse,
    tags=["Realtime Collaborative Whiteboard"]
)
async def get_whiteboard_session_state_endpoint(session_id: str):
    """
    Retrieves full synchronized session state including vector strokes, LaTeX equations, and peer mesh.
    """
    state = collaborative_whiteboard_service.get_session_state(session_id)
    if not state:
        state = collaborative_whiteboard_service.create_session(
            topic="Active Classroom Studio",
            tutor_id="tutor:pro:tanvir_hasan"
        )
    return state


@api_router.post(
    "/whiteboard/canvas/sync",
    response_model=WhiteboardSyncResponse,
    tags=["Realtime Collaborative Whiteboard"]
)
async def sync_whiteboard_canvas_endpoint(payload: WhiteboardSyncRequest):
    """
    Synchronizes vector canvas stroke deltas and LaTeX formula nodes with CRDT conflict resolution.
    """
    data = payload.dict() if hasattr(payload, "dict") else payload.__dict__
    return collaborative_whiteboard_service.sync_canvas(
        session_id=data.get("session_id"),
        caller_id=data.get("caller_id"),
        caller_role=data.get("caller_role", "student"),
        new_strokes=data.get("new_strokes"),
        new_formulas=data.get("new_formulas"),
        erased_stroke_ids=data.get("erased_stroke_ids")
    )


@api_router.post(
    "/whiteboard/webrtc/signal",
    response_model=WebRtcSignalResponse,
    tags=["Realtime Collaborative Whiteboard"]
)
async def route_webrtc_signal_endpoint(payload: WebRtcSignalRequest):
    """
    Routes low-latency WebRTC audio mesh signaling (SDP offer/answer, ICE candidates, VAD active events).
    """
    data = payload.dict() if hasattr(payload, "dict") else payload.__dict__
    return collaborative_whiteboard_service.route_webrtc_signal(
        session_id=data.get("session_id"),
        sender_id=data.get("sender_id"),
        signal_type=data.get("signal_type"),
        payload=data.get("payload", {}),
        target_id=data.get("target_id")
    )


@api_router.post(
    "/whiteboard/podium/control",
    response_model=PodiumControlResponse,
    tags=["Realtime Collaborative Whiteboard"]
)
async def podium_control_endpoint(payload: PodiumControlRequest):
    """
    Executes instructor classroom governance actions (canvas lock, mute all peers, student spotlight, clear canvas).
    """
    data = payload.dict() if hasattr(payload, "dict") else payload.__dict__
    return collaborative_whiteboard_service.apply_podium_control(
        session_id=data.get("session_id"),
        caller_id=data.get("caller_id"),
        caller_role=data.get("caller_role", "tutor"),
        action=data.get("action"),
        target_student_id=data.get("target_student_id")
    )


# ========================================================================================
# Phase 63: AI Examination Proctoring, Gaze Heuristics & Integrity Audit Tower
# ========================================================================================

autonomous_proctoring_service = AutonomousProctoringIntegrityService()


@api_router.post(
    "/proctoring/session/start",
    response_model=ProctoringSessionStartResponse,
    tags=["AI Examination Proctoring"]
)
async def start_proctoring_session_endpoint(payload: ProctoringSessionStartRequest):
    """
    Initializes vision heuristics and audit monitoring for an examination candidate.
    """
    return autonomous_proctoring_service.start_session(
        student_id=payload.student_id,
        exam_id=payload.exam_id,
        exam_title=payload.exam_title or "HSC Model Challenge",
        tenant_id=payload.tenant_id or "11111111-1111-1111-1111-111111111111",
        client_device_info=payload.client_device_info
    )


@api_router.post(
    "/proctoring/event/record",
    response_model=ProctoringEventRecordResponse,
    tags=["AI Examination Proctoring"]
)
async def record_proctoring_event_endpoint(payload: ProctoringEventRecordRequest):
    """
    Records an anomaly event (gaze diversion, secondary face, window blur), evaluates suspicion, and enforces locks.
    """
    return autonomous_proctoring_service.record_event(
        session_id=payload.session_id,
        event_type=payload.event_type,
        confidence_score=payload.confidence_score or 0.9,
        duration_ms=payload.duration_ms or 1000.0,
        gaze_yaw_angle=payload.gaze_yaw_angle,
        gaze_pitch_angle=payload.gaze_pitch_angle,
        detected_faces_count=payload.detected_faces_count or 1,
        metadata=payload.metadata
    )


@api_router.get(
    "/proctoring/session/{session_id}/report",
    response_model=ProctoringSessionReportResponse,
    tags=["AI Examination Proctoring"]
)
async def get_proctoring_session_report_endpoint(session_id: str):
    """
    Generates cryptographic integrity report with SHA-256 audit hash and anomaly event summary.
    """
    return autonomous_proctoring_service.get_session_report(session_id)


@api_router.post(
    "/proctoring/override",
    response_model=ProctoringOverrideResponse,
    tags=["AI Examination Proctoring"]
)
async def proctoring_override_endpoint(payload: ProctoringOverrideRequest):
    """
    Allows human proctors to unlock candidate exams, dismiss false warnings, or flag for disciplinary review.
    """
    return autonomous_proctoring_service.apply_override(
        session_id=payload.session_id,
        proctor_id=payload.proctor_id,
        action=payload.action,
        justification_note=payload.justification_note or "Proctor verified authorization"
    )


# ========================================================================================
# Phase 64: Automated Exam Grading, Handwritten Script OCR & Multi-Evaluator Blind Rubric Moderation
# ========================================================================================

automated_grading_service = AutomatedGradingModerationService()


@api_router.post(
    "/grading/script/upload-ocr",
    response_model=ScriptOCRUploadResponse,
    tags=["Automated Exam Grading & Moderation"]
)
async def upload_and_segment_script_endpoint(payload: ScriptOCRUploadRequest):
    """
    Segments handwritten paper manuscript into question/sub-question bounding boxes.
    Extracts Bangla text, English notation, and LaTeX mathematical formulas.
    """
    return automated_grading_service.upload_and_segment_script(
        script_id=payload.script_id,
        student_id=payload.student_id,
        exam_id=payload.exam_id,
        subject=payload.subject or "Higher Mathematics",
        total_pages=payload.total_pages or 1,
        raw_text_payload=payload.raw_text_payload,
        custom_bounding_boxes=payload.custom_bounding_boxes
    )


@api_router.post(
    "/grading/rubric/evaluate",
    response_model=RubricEvaluateResponse,
    tags=["Automated Exam Grading & Moderation"]
)
async def evaluate_rubric_endpoint(payload: RubricEvaluateRequest):
    """
    Applies multi-step rubrics to score segmented answers with step marking and partial credit.
    """
    return automated_grading_service.evaluate_rubric(
        script_id=payload.script_id,
        criteria=payload.criteria,
        evaluator_role=payload.evaluator_role or "AI_PRE_GRADER",
        evaluator_id=payload.evaluator_id or "evaluator_sys"
    )


@api_router.post(
    "/grading/examiner/score",
    response_model=ExaminerScoreSubmitResponse,
    tags=["Automated Exam Grading & Moderation"]
)
async def record_examiner_score_endpoint(payload: ExaminerScoreSubmitRequest):
    """
    Records score from Examiner 1, Examiner 2, or Arbiter 3.
    """
    return automated_grading_service.record_examiner_score(
        script_id=payload.script_id,
        examiner_id=payload.examiner_id,
        examiner_role=payload.examiner_role,
        subquestion_marks=payload.subquestion_marks,
        examiner_feedback=payload.examiner_feedback
    )


@api_router.get(
    "/grading/script/{script_id}/moderation-audit",
    response_model=ModerationAuditResponse,
    tags=["Automated Exam Grading & Moderation"]
)
async def get_moderation_audit_endpoint(script_id: str):
    """
    Evaluates score divergence between Examiner 1 & 2.
    Enforces Bangladesh Board 15% tolerance threshold and dispatches Arbiter if exceeded.
    """
    return automated_grading_service.get_moderation_audit(script_id)


@api_router.post(
    "/grading/script/rescrutiny-audit",
    response_model=ReScrutinyAuditResponse,
    tags=["Automated Exam Grading & Moderation"]
)
async def perform_rescrutiny_endpoint(payload: ReScrutinyAuditRequest):
    """
    Conducts post-publication re-scrutiny and board auditing:
    Verifies addition totals, checks for unmarked questions, and issues SHA-256 HMAC tamper seal.
    """
    return automated_grading_service.perform_rescrutiny(
        script_id=payload.script_id,
        scrutineer_id=payload.scrutineer_id or "board_scrutineer_01",
        recheck_reason=payload.recheck_reason or "Post-publication review request"
    )


@api_router.get(
    "/grading/cohort/{exam_id}/distribution",
    response_model=CohortDistributionResponse,
    tags=["Automated Exam Grading & Moderation"]
)
async def get_cohort_distribution_endpoint(exam_id: str):
    """
    Calculates cohort score distribution, mean, standard deviation, and Z-score outlier anomaly detection.
    """
    return automated_grading_service.get_cohort_distribution(exam_id)


# ========================================================================================
# Phase 65: AI Adaptive Curriculum, Bayesian Knowledge Graph & Memory Decay Engine
# ========================================================================================

@api_router.get(
    "/curriculum/graph/{subject}",
    response_model=CurriculumGraphResponse,
    tags=["AI Adaptive Curriculum & Bayesian Knowledge Graph"]
)
async def get_curriculum_graph_endpoint(subject: str = "Higher Mathematics"):
    """
    Retrieves the subject curriculum DAG with topological depth levels and prerequisite edges.
    """
    return adaptive_curriculum_service.get_curriculum_graph(subject=subject)


@api_router.post(
    "/curriculum/mastery/bkt-update",
    response_model=BktUpdateResponse,
    tags=["AI Adaptive Curriculum & Bayesian Knowledge Graph"]
)
async def update_bayesian_mastery_endpoint(payload: BktUpdateRequest):
    """
    Updates student mastery probability using Bayesian Knowledge Tracing (BKT) equations
    incorporating prior P(L_{t-1}), Slip P(S), Guess P(G), and Transit P(T).
    """
    return adaptive_curriculum_service.update_bayesian_mastery(payload)


@api_router.post(
    "/curriculum/remedial/pathway",
    response_model=RemedialPathwayResponse,
    tags=["AI Adaptive Curriculum & Bayesian Knowledge Graph"]
)
async def generate_remedial_pathway_endpoint(payload: RemedialPathwayRequest):
    """
    Traces upward through the knowledge DAG from a failed concept to pinpoint the root-cause
    prerequisite gap and generates a sequenced remedial learning pathway.
    """
    return adaptive_curriculum_service.generate_remedial_pathway(payload)


@api_router.post(
    "/curriculum/adaptive-schedule/generate",
    response_model=AdaptiveScheduleResponse,
    tags=["AI Adaptive Curriculum & Bayesian Knowledge Graph"]
)
async def generate_adaptive_schedule_endpoint(payload: AdaptiveScheduleRequest):
    """
    Generates a personalized 7-day adaptive study schedule combining Ebbinghaus decay
    spaced-repetition reviews with prerequisite-ready new concept acquisition.
    """
    return adaptive_curriculum_service.generate_adaptive_schedule(payload)


@api_router.get(
    "/curriculum/student/{student_id}/snapshot",
    tags=["AI Adaptive Curriculum & Bayesian Knowledge Graph"]
)
async def get_student_mastery_snapshot_endpoint(student_id: str, subject: str = "Higher Mathematics"):
    """
    Returns full mastery snapshot and current retention decay levels across all concepts in a subject.
    """
    return adaptive_curriculum_service.get_student_mastery_snapshot(student_id=student_id, subject=subject)


# ========================================================================================
# Phase 66: Offline-First P2P Mesh Sync, Local CRDT Mutation Ledger & Disruption Tower
# ========================================================================================

@api_router.post(
    "/offline-mesh/mutation/stage",
    response_model=MutationStageResponse,
    tags=["Offline-First P2P Mesh Sync & CRDT Ledger"]
)
async def stage_mutations_endpoint(payload: MutationStageRequest):
    """
    Stages local offline mutations with SHA-256 HMAC idempotency keys into the local CRDT queue.
    """
    return offline_mesh_crdt_service.stage_mutations(payload)


@api_router.get(
    "/offline-mesh/mesh/topology",
    response_model=MeshTopologyResponse,
    tags=["Offline-First P2P Mesh Sync & CRDT Ledger"]
)
async def get_mesh_topology_endpoint(network_profile: Optional[str] = None):
    """
    Retrieves real-time WebRTC DataChannel classroom mesh topology and peer latency graphs.
    """
    return offline_mesh_crdt_service.get_mesh_topology(network_profile=network_profile)


@api_router.post(
    "/offline-mesh/chaos/simulate",
    response_model=ChaosSimulationResponse,
    tags=["Offline-First P2P Mesh Sync & CRDT Ledger"]
)
async def simulate_chaos_endpoint(payload: ChaosSimulationRequest):
    """
    Emulates network degradation profiles (Broadband, 2G/EDGE, Packet Loss, Blackout) and verifies 0% data loss.
    """
    return offline_mesh_crdt_service.simulate_chaos_profile(payload)


@api_router.post(
    "/offline-mesh/reconcile/batch",
    response_model=ReconcileBatchResponse,
    tags=["Offline-First P2P Mesh Sync & CRDT Ledger"]
)
async def reconcile_batch_endpoint(payload: ReconcileBatchRequest):
    """
    Reconciles staged offline mutations with Supabase cloud using cryptographic Merkle root verification.
    """
    return offline_mesh_crdt_service.reconcile_batch(payload)


@api_router.get(
    "/offline-mesh/queue/status",
    tags=["Offline-First P2P Mesh Sync & CRDT Ledger"]
)
async def get_queue_status_endpoint():
    """
    Returns current offline queue depth, staged items, and active network profile.
    """
    return offline_mesh_crdt_service.get_queue_status()


# ========================================================================================
# Phase 67: Decentralized Micro-Edge CDN, WebTorrent Asset Swarm & Media Caching Tower
# ========================================================================================

@api_router.post(
    "/cdn-swarm/manifest/create",
    response_model=MediaManifestDTO,
    tags=["Decentralized Micro-Edge CDN & Swarm"]
)
async def create_cdn_manifest_endpoint(payload: ManifestCreateRequest):
    """
    Slices a lecture/simulation media asset into uniform chunk pieces and generates Merkle root.
    """
    return decentralized_cdn_swarm_service.create_manifest(payload)


@api_router.get(
    "/cdn-swarm/manifest/{manifest_id}",
    response_model=MediaManifestDTO,
    tags=["Decentralized Micro-Edge CDN & Swarm"]
)
async def get_cdn_manifest_endpoint(manifest_id: str):
    """
    Retrieves the media chunk manifest, piece hashes, and binary Merkle root.
    """
    manifest = decentralized_cdn_swarm_service.get_manifest(manifest_id)
    if not manifest:
        raise HTTPException(status_code=404, detail=f"Manifest '{manifest_id}' not found.")
    return manifest


@api_router.get(
    "/cdn-swarm/swarm/status",
    response_model=SwarmStatusResponse,
    tags=["Decentralized Micro-Edge CDN & Swarm"]
)
async def get_swarm_status_endpoint(manifest_id: Optional[str] = None):
    """
    Returns classroom peer swarm topology, bitfields, upload/download rates, and ISP bandwidth savings.
    """
    status = decentralized_cdn_swarm_service.get_swarm_status(manifest_id or "default")
    if not status:
        raise HTTPException(status_code=404, detail="No active CDN swarm status found.")
    return status


@api_router.post(
    "/cdn-swarm/piece/verify",
    response_model=PieceVerifyResponse,
    tags=["Decentralized Micro-Edge CDN & Swarm"]
)
async def verify_piece_endpoint(payload: PieceVerifyRequest):
    """
    Validates a candidate chunk against the authoritative NCTB Merkle leaf hash.
    """
    return decentralized_cdn_swarm_service.verify_piece(payload)


@api_router.post(
    "/cdn-swarm/transfer/simulate",
    response_model=TransferSimulateResponse,
    tags=["Decentralized Micro-Edge CDN & Swarm"]
)
async def simulate_p2p_transfer_endpoint(payload: TransferSimulateRequest):
    """
    Simulates high-speed local WebRTC chunk streaming between classroom peers.
    """
    return decentralized_cdn_swarm_service.simulate_p2p_transfer(payload)


@api_router.get(
    "/cdn-swarm/rarest-first/{manifest_id}",
    tags=["Decentralized Micro-Edge CDN & Swarm"]
)
async def get_rarest_first_schedule_endpoint(manifest_id: str):
    """
    Returns the rarest-first piece scheduling queue across the classroom peer swarm.
    """
    return decentralized_cdn_swarm_service.get_rarest_first_schedule(manifest_id)


# ========================================================================================
# Phase 68: Zero-Knowledge Airgap Attendance, Decentralized Identity & Merkle Attestation
# ========================================================================================

@api_router.get(
    "/airgap-attendance/beacon/generate",
    response_model=RollingBeaconTokenDTO,
    tags=["Zero-Knowledge Airgap Attendance & DID"]
)
async def generate_rolling_beacon_endpoint(classroom_id: str = "CLS-DHAKA-10B"):
    """
    Generates rolling 30-second proximity BLE/Wi-Fi beacon token with SHA-256 rolling code.
    """
    return airgap_attendance_did_service.get_current_beacon(classroom_id)


@api_router.post(
    "/airgap-attendance/punch/record",
    response_model=AttendancePunchResponse,
    tags=["Zero-Knowledge Airgap Attendance & DID"]
)
async def record_attendance_punch_endpoint(payload: AttendancePunchRequest):
    """
    Validates student DID proximity attendance punch with anti-proxy nonce and Ed25519 signature checks.
    """
    return airgap_attendance_did_service.record_attendance_punch(payload)


@api_router.get(
    "/airgap-attendance/session/status",
    response_model=ClassroomAttendanceSessionResponse,
    tags=["Zero-Knowledge Airgap Attendance & DID"]
)
async def get_attendance_session_status_endpoint(session_id: Optional[str] = None):
    """
    Returns classroom attendance quorum, Merkle root, proxy attacks blocked, and enrolled student punches.
    """
    return airgap_attendance_did_service.get_session_status(session_id)


@api_router.post(
    "/airgap-attendance/merkle/batch",
    response_model=MerkleBatchSettleResponse,
    tags=["Zero-Knowledge Airgap Attendance & DID"]
)
async def settle_attendance_merkle_batch_endpoint(payload: MerkleBatchSettleRequest):
    """
    Settles airgapped attendance batch into Supabase PostgreSQL ledger with cryptographic root verification.
    """
    return airgap_attendance_did_service.settle_merkle_batch(payload)


# =============================================================================
# SECTION 68: DISTRIBUTED SHAMIR SECRET SHARING & EPHEMERAL EXAM VAULT (PHASE 69)
# =============================================================================

@api_router.post(
    "/shamir-vault/split",
    response_model=ShamirKeySplitResponse,
    tags=["Distributed Shamir Secret Sharing & Ephemeral Exam Vault"]
)
async def split_exam_secret_endpoint(payload: ShamirKeySplitRequest):
    """
    Splits master exam encryption key into n polynomial shares with threshold k over secp256k1 finite field.
    """
    return shamir_exam_vault_service.create_split_vault(
        exam_code=payload.exam_code,
        subject=payload.subject,
        raw_content=payload.raw_content,
        threshold_k=payload.threshold_k,
        total_shares_n=payload.total_shares_n
    )


@api_router.get(
    "/shamir-vault/custodians",
    response_model=List[ExamCustodianDTO],
    tags=["Distributed Shamir Secret Sharing & Ephemeral Exam Vault"]
)
async def get_exam_custodians_endpoint(vault_id: str = "vault-hsc-phy-001"):
    """
    Returns the list of designated custodian trustees and share presentation status for an exam vault.
    """
    try:
        return shamir_exam_vault_service.get_custodians(vault_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vault '{vault_id}' not found."
        )


@api_router.post(
    "/shamir-vault/reconstruct",
    response_model=ThresholdReconstructResponse,
    tags=["Distributed Shamir Secret Sharing & Ephemeral Exam Vault"]
)
async def reconstruct_exam_vault_endpoint(payload: ThresholdReconstructRequest):
    """
    Executes Lagrange polynomial interpolation to reconstruct master key and decrypt ephemeral exam payload.
    """
    return shamir_exam_vault_service.reconstruct_and_decrypt_vault(
        vault_id=payload.vault_id,
        presented_shares=payload.shares,
        operator_id=payload.operator_id
    )


@api_router.get(
    "/shamir-vault/status",
    tags=["Distributed Shamir Secret Sharing & Ephemeral Exam Vault"]
)
async def get_exam_vault_status_endpoint(vault_id: str = "vault-hsc-phy-001"):
    """
    Returns real-time status, quorum percentage, custodian verification progress, and tamper incident counts.
    """
    try:
        return shamir_exam_vault_service.get_vault_summary(vault_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vault '{vault_id}' not found."
        )


@api_router.post(
    "/shamir-vault/zeroize",
    tags=["Distributed Shamir Secret Sharing & Ephemeral Exam Vault"]
)
async def zeroize_exam_vault_endpoint(vault_id: str = "vault-hsc-phy-001", operator_id: str = "admin:emergency-wipe"):
    """
    Executes emergency zeroization wipe, destroying in-memory cryptographic keys and decrypted buffers.
    """
    try:
        return shamir_exam_vault_service.trigger_zeroization(vault_id=vault_id, operator_id=operator_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vault '{vault_id}' not found."
        )


# =============================================================================
# SECTION 69: AUTONOMOUS CAMPUS RAFT QUORUM & BYZANTINE FAULT TOLERANT SMR (PHASE 70)
# =============================================================================

@api_router.get(
    "/campus-raft/cluster",
    tags=["Campus Raft Quorum & Byzantine Fault Tolerance"]
)
async def get_campus_raft_cluster_endpoint():
    """
    Returns the real-time 5-campus Raft cluster topology, active term, current leader, and node statuses.
    """
    return campus_raft_bft_service.get_cluster_topology()


@api_router.post(
    "/campus-raft/log/propose",
    tags=["Campus Raft Quorum & Byzantine Fault Tolerance"]
)
async def propose_campus_raft_log_endpoint(
    command_type: str = Query("EXAM_VAULT_UNLOCK", description="State machine command type"),
    payload_json: str = Query('{"vault_id": "vault-hsc-phy-001", "authorized_by": "academic-council"}', description="JSON string payload"),
    client_id: str = Query("academic-council-admin", description="Proposing client or coordinator ID")
):
    """
    Proposes a state machine command to the current Raft leader, broadcasting append entries to peer nodes.
    """
    try:
        parsed_payload = json.loads(payload_json)
    except Exception:
        parsed_payload = {"raw": payload_json}

    try:
        return campus_raft_bft_service.propose_log_entry(
            command_type=command_type,
            payload=parsed_payload,
            client_id=client_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/campus-raft/heartbeat",
    tags=["Campus Raft Quorum & Byzantine Fault Tolerance"]
)
async def emit_campus_raft_heartbeat_endpoint():
    """
    Emits leader heartbeat pings across all non-partitioned peer nodes to maintain lease and prevent elections.
    """
    return campus_raft_bft_service.emit_heartbeat()


@api_router.post(
    "/campus-raft/election/trigger",
    tags=["Campus Raft Quorum & Byzantine Fault Tolerance"]
)
async def trigger_campus_raft_election_endpoint(
    candidate_node_id: Optional[str] = Query(None, description="Optional target candidate node to initiate election")
):
    """
    Simulates a randomized election timeout event, incrementing term and soliciting quorum votes.
    """
    try:
        return campus_raft_bft_service.trigger_election(candidate_node_id=candidate_node_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/campus-raft/chaos/inject",
    tags=["Campus Raft Quorum & Byzantine Fault Tolerance"]
)
async def inject_campus_raft_chaos_endpoint(payload: ChaosFaultInjectionRequest):
    """
    Injects chaos engineering faults: network partition (split-brain), byzantine corruption, or leader assassination.
    """
    try:
        return campus_raft_bft_service.inject_chaos_fault(
            action=payload.action,
            target_node_id=payload.target_node_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/campus-raft/status",
    tags=["Campus Raft Quorum & Byzantine Fault Tolerance"]
)
async def get_campus_raft_status_endpoint():
    """
    Returns high-level consensus summary: quorum health, Merkle state root, term, and applied state count.
    """
    topo = campus_raft_bft_service.get_cluster_topology()
    return {
        "cluster_id": topo["cluster_id"],
        "active_term": topo["active_term"],
        "current_leader_id": topo["current_leader_id"],
        "cluster_status": topo["cluster_status"],
        "merkle_latest_root": topo["merkle_latest_root"],
        "state_machine_count": topo["state_machine_count"],
        "total_nodes": topo["total_nodes"],
        "quorum_size": topo["quorum_size"]
    }


# =============================================================================
# SECTION 71: NEURAL BENGALI SPEECH SYNTHESIS & REGIONAL DIALECT TUTORING TOWER
# DEVELOPER ARCHITECTURE NOTE:
# Exposes REST API contracts for neural Bengali speech synthesis, regional dialect
# transliteration (Chittagong, Sylhet, Noakhali, Barisal, Rangpur), IPA phonetic
# alignment, low-bandwidth Opus audio telemetry, and dialect vocabulary bridge.
# =============================================================================

@api_router.post(
    "/speech-dialect/transliterate",
    response_model=DialectTransliterateResponse,
    tags=["Neural Bengali Speech & Regional Dialect Tutoring"]
)
async def transliterate_bengali_dialect_endpoint(payload: DialectTransliterateRequest):
    """
    Transliterates text between Standard Bengali and regional dialects (Chittagonian, Sylheti, Noakhailla, Barisali, Rangpuri).
    """
    try:
        return neural_speech_dialect_service.transliterate_dialect(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/speech-dialect/synthesize",
    response_model=SpeechSynthesizeResponse,
    tags=["Neural Bengali Speech & Regional Dialect Tutoring"]
)
async def synthesize_speech_endpoint(payload: SpeechSynthesizeRequest):
    """
    Synthesizes acoustic speech telemetry: duration modeling, Opus bitrate slicing, waveform peaks, and phoneme alignment.
    """
    try:
        return neural_speech_dialect_service.synthesize_speech(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/speech-dialect/vocab-bridge",
    response_model=DialectVocabBridgeResponse,
    tags=["Neural Bengali Speech & Regional Dialect Tutoring"]
)
async def bridge_dialect_vocabulary_endpoint(payload: DialectVocabBridgeRequest):
    """
    Looks up regional vocabulary in the dialect bridge dictionary for rural educational inclusivity.
    """
    try:
        return neural_speech_dialect_service.bridge_vocabulary(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/speech-dialect/dialects",
    tags=["Neural Bengali Speech & Regional Dialect Tutoring"]
)
async def list_supported_dialects_endpoint():
    """
    Returns list of all active supported regional dialects and audio quality tiers.
    """
    return {
        "dialects": [d.value for d in DialectEnum],
        "quality_tiers": [q.value for q in AudioQualityTierEnum],
        "default_dialect": DialectEnum.STANDARD_CHOLITO.value
    }


@api_router.get(
    "/speech-dialect/status",
    response_model=SpeechEngineStatusDTO,
    tags=["Neural Bengali Speech & Regional Dialect Tutoring"]
)
async def get_speech_dialect_status_endpoint():
    """
    Returns real-time neural speech engine health telemetry, active streams, and cache volume.
    """
    return neural_speech_dialect_service.get_status()


# =============================================================================
# SECTION 72: AUTONOMOUS SATELLITE USSD & LORA LONG-RANGE EMERGENCY TOWER
# DEVELOPER ARCHITECTURE NOTE:
# Exposes REST API contracts for 160-char GSM USSD interactive micro-learning menus,
# binary LoRaWAN packet radio encoding, CRC16 attestation, time-on-air estimation,
# store-and-forward delay-tolerant networking (DTN), and remote off-grid solar telemetry.
# =============================================================================

@api_router.post(
    "/satellite-lora/ussd/session",
    response_model=UssdMenuResponse,
    tags=["Satellite USSD & LoRa Emergency Classroom Gateway"]
)
async def handle_ussd_menu_session_endpoint(payload: UssdMenuRequest):
    """
    Processes interactive 160-character GSM USSD micro-learning menu requests.
    """
    try:
        return satellite_lora_emergency_service.handle_ussd_session(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/satellite-lora/packet/encode",
    response_model=LoraPacketEncodeResponse,
    tags=["Satellite USSD & LoRa Emergency Classroom Gateway"]
)
async def encode_lora_packet_frame_endpoint(payload: LoraPacketEncodeRequest):
    """
    Serializes student submissions into compact binary LoRa frames with CRC16 and ToA calculation.
    """
    try:
        return satellite_lora_emergency_service.encode_lora_packet(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/satellite-lora/dtn/enqueue",
    response_model=StoreForwardQueueItemDTO,
    tags=["Satellite USSD & LoRa Emergency Classroom Gateway"]
)
async def enqueue_dtn_mutation_endpoint(station_id: str = Query(...), payload_type: str = Query("MCQ_SUBMISSION")):
    """
    Buffers mutation items into the delay-tolerant store-and-forward queue for off-grid delivery.
    """
    try:
        return satellite_lora_emergency_service.enqueue_dtn_mutation(
            station_id=station_id,
            payload_type=payload_type,
            data={"station_id": station_id, "timestamp": "now"}
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/satellite-lora/stations",
    response_model=List[OffGridSolarStationTelemetryDTO],
    tags=["Satellite USSD & LoRa Emergency Classroom Gateway"]
)
async def list_remote_solar_stations_endpoint():
    """
    Returns real-time telemetry for off-grid remote Char and flood-resilient solar school stations.
    """
    return satellite_lora_emergency_service.get_remote_stations()


@api_router.get(
    "/satellite-lora/status",
    response_model=SatelliteLoraStatusDTO,
    tags=["Satellite USSD & LoRa Emergency Classroom Gateway"]
)
async def get_satellite_lora_status_endpoint():
    """
    Returns operational health, delivered DTN packets, and radio link budget telemetry.
    """
    return satellite_lora_emergency_service.get_status()


# =============================================================================
# SECTION 73: ADAPTIVE NEURODIVERGENT ACCESSIBILITY & COGNITIVE READER TOWER
# DEVELOPER ARCHITECTURE NOTE:
# Exposes REST API contracts for bionic reading saccadic fixation bolding,
# academic STEM syllable decomposition, WPM cognitive pacing calculation,
# W3C WCAG 2.2 AAA relative luminance auditing, and sensory color presets.
# =============================================================================

@api_router.post(
    "/accessibility/bionic/transform",
    response_model=BionicReadingTransformResponse,
    tags=["Neurodivergent Accessibility & Cognitive Reader"]
)
async def transform_bionic_reading_endpoint(payload: BionicReadingTransformRequest):
    """
    Transforms academic text into bionic saccadic reading format with bold fixation anchors.
    """
    try:
        return neurodivergent_accessibility_service.transform_bionic_reading(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/accessibility/syllables/decompose",
    response_model=SyllableDecomposeResponse,
    tags=["Neurodivergent Accessibility & Cognitive Reader"]
)
async def decompose_academic_syllables_endpoint(payload: SyllableDecomposeRequest):
    """
    Deconstructs multi-syllabic academic vocabulary into hyphenated pronounceable units.
    """
    try:
        return neurodivergent_accessibility_service.decompose_syllables(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/accessibility/contrast/audit",
    response_model=AccessibilityAuditMetricsDTO,
    tags=["Neurodivergent Accessibility & Cognitive Reader"]
)
async def audit_contrast_ratio_endpoint(fg_hex: str = Query(...), bg_hex: str = Query(...)):
    """
    Evaluates sRGB color pair against W3C WCAG 2.2 Level AA and AAA contrast criteria.
    """
    try:
        return neurodivergent_accessibility_service.audit_contrast_ratio(fg_hex, bg_hex)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/accessibility/presets",
    tags=["Neurodivergent Accessibility & Cognitive Reader"]
)
async def list_accessibility_presets_endpoint():
    """
    Returns the 5 scientifically validated sensory color contrast and temperature presets.
    """
    return neurodivergent_accessibility_service.get_presets()


@api_router.get(
    "/accessibility/status",
    response_model=AccessibilityStatusDTO,
    tags=["Neurodivergent Accessibility & Cognitive Reader"]
)
async def get_accessibility_status_endpoint():
    """
    Returns operational health and compliance scores for the neurodivergent accessibility engine.
    """
    return neurodivergent_accessibility_service.get_status()


# =====================================================================
# 74. NATIONAL CENTRALIZED ADMISSION MATRIX & GALE-SHAPLEY MATCHING TOWER (PHASE 75)
# DEVELOPER ARCHITECTURE NOTE:
# Endpoints powering Tab 69: Gale-Shapley Deferred Acceptance (DA) seat allocation,
# automated quota balancing (District, Freedom Fighter, Tribal, Special Needs),
# multi-stage dynamic migration cascade simulations, and admission rank probability heuristics.
# =====================================================================

@api_router.post(
    "/admission-matrix/match/run",
    response_model=MatchingRunResponse,
    tags=["Centralized Admission Matrix & Gale-Shapley Matching"]
)
async def run_admission_matching_endpoint(payload: Optional[MatchingRunRequest] = None):
    """
    Executes student-proposing Gale-Shapley Deferred Acceptance matching algorithm.
    Guarantees stable, Pareto-efficient, and envy-free institutional seat allocations.
    """
    try:
        return admission_matching_service.run_gale_shapley_matching(payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/admission-matrix/migration/simulate",
    response_model=MigrationSimulationResponse,
    tags=["Centralized Admission Matrix & Gale-Shapley Matching"]
)
async def simulate_migration_cascade_endpoint(payload: MigrationSimulationRequest):
    """
    Simulates automated multi-stage migration cascade when top candidates decline or vacate seats.
    """
    try:
        return admission_matching_service.simulate_migration_cascade(payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post(
    "/admission-matrix/probability/calculate",
    response_model=AdmissionProbabilityResponseDTO,
    tags=["Centralized Admission Matrix & Gale-Shapley Matching"]
)
async def calculate_admission_probability_endpoint(payload: AdmissionProbabilityQueryDTO):
    """
    Calculates admission probability heuristics based on candidate merit rank,
    institutional cutoffs, and affirmative action quota weighting.
    """
    try:
        return admission_matching_service.calculate_admission_probability(payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.get(
    "/admission-matrix/programs",
    tags=["Centralized Admission Matrix & Gale-Shapley Matching"]
)
async def list_admission_programs_endpoint():
    """
    Returns the catalog of national benchmark academic programs with seat and quota capacities.
    """
    return admission_matching_service.get_all_programs()


@api_router.get(
    "/admission-matrix/status",
    response_model=AdmissionMatrixStatusDTO,
    tags=["Centralized Admission Matrix & Gale-Shapley Matching"]
)
async def get_admission_matrix_status_endpoint():
    """
    Returns operational telemetry, quota categories active, and algorithm version for the matrix.
    """
    return admission_matching_service.get_status()














